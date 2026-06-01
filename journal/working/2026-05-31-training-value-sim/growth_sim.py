"""
Lean Athlete v7 — Stage 1 growth model (dose-response).

The upgrade over the v6 coverage model: value is a 12-week CONCAVE growth curve
that is a function of weekly VOLUME, not a one-touch saturation. That makes weekly
volume the thing being optimised — which is what the coverage model got wrong.

Built test-first; see test_growth_sim.py for the sanity gates.
"""
import math

# Hypertrophy dose-response constants (per muscle, weekly effective sets).
# Anchored to volume-landmark literature: productive to ~MAV, junk past MRV.
HYP_GMAX = 1.0       # asymptotic stimulus ceiling
HYP_K = 6.0          # ~10 sets -> ~81% of ceiling
HYP_MRV = 22.0       # maximum recoverable volume (sets/muscle/wk)
HYP_OVER_PENALTY = 0.01   # net cost per set past MRV (junk volume)


def hypertrophy_growth(weekly_effective_sets):
    """12-week hypertrophy stimulus for one muscle given weekly effective sets.

    Concave (diminishing returns) to MRV, then a junk-volume penalty past it.
    """
    s = weekly_effective_sets
    base = HYP_GMAX * (1 - math.exp(-s / HYP_K))
    penalty = HYP_OVER_PENALTY * max(0.0, s - HYP_MRV)
    return base - penalty


def effective_sets(sets, rir):
    """Sets weighted by proximity to failure. <=2 RIR full, 3-4 partial, >4 light."""
    if rir <= 2:
        weight = 1.0
    elif rir <= 4:
        weight = 0.7
    else:
        weight = 0.4
    return sets * weight


def frequency_factor(frequency):
    """Same weekly volume spread over more sessions yields more, up to a cap."""
    return 1.0 + 0.10 * min(max(frequency - 1, 0), 2)


def weekly_hypertrophy(weekly_effective_sets, frequency=1):
    """Hypertrophy stimulus including the frequency bonus."""
    return hypertrophy_growth(weekly_effective_sets) * frequency_factor(frequency)


# ---- Goal taxonomy + weighting (Aesthetics 40 / Longevity 20 / Basketball 20 / Mobility 20) ----

GOAL_WEIGHTS = {"A": 0.40, "L": 0.20, "B": 0.20, "M": 0.20}

# Sub-dimensions per goal. Leanness is NOT here — it's an exogenous multiplier on A.
GOAL_SUBDIMS = {
    "A": ["delts", "back", "arms", "chest_upper"],
    "L": ["vo2", "strength", "resilience"],
    "B": ["power", "speed", "cod", "conditioning", "skill", "contact"],
    "M": ["ankle", "hip", "tspine", "adductor"],
}
SUBDIM_GOAL = {sd: g for g, sds in GOAL_SUBDIMS.items() for sd in sds}


def goal_scores(subdim_growth):
    """Mean growth across each goal's full sub-dim set (missing sub-dims = 0).

    Averaging over the full set means breadth matters: one strong sub-dim with the
    rest empty scores low, which is what keeps a goal from being faked by one lift.
    """
    out = {}
    for goal, subdims in GOAL_SUBDIMS.items():
        total = sum(subdim_growth.get(sd, 0.0) for sd in subdims)
        out[goal] = total / len(subdims)
    return out


def weighted_total(scores, leanness=1.0):
    """40/20/20/20-weighted total. Leanness multiplies the aesthetics term only."""
    return (
        GOAL_WEIGHTS["A"] * scores.get("A", 0.0) * leanness
        + GOAL_WEIGHTS["L"] * scores.get("L", 0.0)
        + GOAL_WEIGHTS["B"] * scores.get("B", 0.0)
        + GOAL_WEIGHTS["M"] * scores.get("M", 0.0)
    )


# ---- Dose -> per-sub-dim growth, then the greedy budget optimizer ----

GENERIC_K = 6.0  # fallback saturation constant

# Per-quality saturation constants (Codex + Gemini validated 2026-05-31).
# Higher K = absorbs more weekly volume before saturating (slower adaptation).
SUBDIM_K = {
    "vo2": 11.0, "conditioning": 9.0,        # cardio: slow, volume-dependent
    "strength": 6.0, "resilience": 6.0,      # moderate (resilience is a coarse bucket)
    "power": 4.0, "speed": 4.0,              # neural qualities saturate fast
    "cod": 5.0, "contact": 5.0,
    "skill": 16.0,                           # absorbs lots of practice volume
    "ankle": 5.0, "hip": 5.0, "tspine": 5.0, "adductor": 5.0,  # mobility: early ROM gains fast
}


def subdim_growth_from_dose(subdim, dose):
    """Growth (0-1) for one sub-dim from accumulated weekly dose units.

    Aesthetics sub-dims use the hypertrophy curve (with its junk-volume penalty);
    every other quality uses a saturating curve with its OWN time-constant K.
    """
    if SUBDIM_GOAL.get(subdim) == "A":
        return hypertrophy_growth(dose)
    k = SUBDIM_K.get(subdim, GENERIC_K)
    return 1 - math.exp(-dose / k)


def _scores_from_doses(doses):
    growth = {sd: subdim_growth_from_dose(sd, d) for sd, d in doses.items()}
    return goal_scores(growth)


def optimize(catalog, budget_min, step=1.0, floors=None, leanness=1.0):
    """Greedy allocation of a weekly time budget across exercises.

    Each growth curve is concave and the budget is linear, so spending the next
    minute on the highest marginal-weighted-growth-per-minute exercise is optimal.
    `floors` (goal -> min score) are met first when achievable, then the rest is
    allocated freely.

    Returns {alloc, doses, scores, total, trace}.
    """
    floors = floors or {}
    doses = {}
    alloc = {}
    trace = []
    spent = 0.0

    def apply(ex):
        for sd, dpm in catalog[ex].items():
            doses[sd] = doses.get(sd, 0.0) + dpm * step
        alloc[ex] = alloc.get(ex, 0.0) + step

    def marginal_per_min(ex):
        before = weighted_total(_scores_from_doses(doses), leanness)
        # trial-add
        trial = dict(doses)
        for sd, dpm in catalog[ex].items():
            trial[sd] = trial.get(sd, 0.0) + dpm * step
        after = weighted_total(_scores_from_doses(trial), leanness)
        return (after - before) / step

    while spent + step <= budget_min + 1e-9:
        scores = _scores_from_doses(doses)
        unmet = [g for g, f in floors.items() if scores.get(g, 0.0) < f]
        if unmet:
            # restrict to exercises that serve an unmet-floor goal
            candidates = [ex for ex in catalog
                          if any(SUBDIM_GOAL.get(sd) in unmet for sd in catalog[ex])]
            if not candidates:
                candidates = list(catalog)
        else:
            candidates = list(catalog)
        # deterministic: highest marginal/min, ties broken by catalog order
        best = max(candidates, key=lambda ex: (marginal_per_min(ex), -list(catalog).index(ex)))
        trace.append(marginal_per_min(best))
        apply(best)
        spent += step

    scores = _scores_from_doses(doses)
    return {"alloc": alloc, "doses": doses, "scores": scores,
            "total": weighted_total(scores, leanness), "trace": trace}
