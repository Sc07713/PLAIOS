"""
Stage 1 RUN — first-draft exercise catalog + growth leaderboard + optimized weekly dose.

IMPORTANT: the per-exercise dose values below are a FIRST DRAFT (my judgement).
They are the load-bearing, subjective input the v7 spec flags for Codex + Gemini
validation BEFORE the leaderboard is trusted. The ENGINE (growth_sim.py) is tested;
these numbers are directional until the catalog is reviewed.

Dose conventions (per training-minute, incl. setup/rest):
- Aesthetics sub-dims (delts/back/arms/chest_upper): EFFECTIVE SETS per minute.
  A hard set ~2.5 min -> ~0.4 set/min if it fully targets the muscle; scaled by how
  much of that muscle the exercise actually hits.
- Non-hypertrophy sub-dims (strength/resilience/vo2/power/speed/cod/conditioning/
  skill/contact/ankle/hip/tspine/adductor): generic stimulus units per minute,
  calibrated so a full working session lands a sane dose against GENERIC_K=6.
"""
import growth_sim as gs

# exercise -> {sub-dim: dose_per_min}
# v2 — Codex + Gemini validated (see review2-catalog.md): resilience/power/contact
# deflated, VO2 re-credited, Dips added, per-quality K now in the engine.
CATALOG = {
    # ---- Pulls / back (the v6 winners) ----
    "Chin-ups":          {"back": 0.30, "arms": 0.15, "strength": 0.18, "contact": 0.03},
    "Pull-ups":          {"back": 0.34, "arms": 0.12, "strength": 0.18, "contact": 0.03},
    "DB Row":            {"back": 0.32, "arms": 0.08, "strength": 0.16, "contact": 0.08, "resilience": 0.06},
    "Loaded carry":      {"strength": 0.14, "resilience": 0.18, "arms": 0.01, "contact": 0.14, "conditioning": 0.10, "hip": 0.04},
    "Face pull":         {"back": 0.12, "resilience": 0.07},
    # ---- Push / upper aesthetics ----
    "Incline DB press":  {"chest_upper": 0.34, "delts": 0.10, "arms": 0.14, "strength": 0.14},
    "Dips":              {"chest_upper": 0.20, "arms": 0.20, "delts": 0.08, "strength": 0.12},
    "Lateral raise":     {"delts": 0.40},
    "Overhead press":    {"delts": 0.22, "arms": 0.10, "strength": 0.14, "chest_upper": 0.06},
    "Triceps/curls":     {"arms": 0.38},
    "Pullover":          {"back": 0.14, "chest_upper": 0.14},
    # ---- Legs (lean/power, not hypertrophy) ----
    "Bulgarian split sq":{"strength": 0.24, "power": 0.06, "resilience": 0.10, "hip": 0.10, "contact": 0.08},
    "Single-leg RDL":    {"strength": 0.18, "resilience": 0.16, "hip": 0.10, "power": 0.02},
    "ATG split squat":   {"strength": 0.16, "hip": 0.18, "ankle": 0.18, "resilience": 0.12},
    "Cossack/lat lunge": {"hip": 0.16, "adductor": 0.20, "ankle": 0.08, "resilience": 0.08},
    # ---- Power / speed / court qualities ----
    "Jumps/plyo":        {"power": 0.40, "speed": 0.10, "resilience": 0.05, "cod": 0.10, "ankle": 0.10},
    "Accel sprints":     {"speed": 0.40, "power": 0.18, "conditioning": 0.12, "vo2": 0.02},
    "Decel ladder":      {"cod": 0.25, "resilience": 0.18, "ankle": 0.10, "contact": 0.06},
    # ---- Conditioning / longevity engine ----
    "4x4 intervals":     {"vo2": 0.38, "conditioning": 0.22},
    "Zone-2":            {"vo2": 0.12, "conditioning": 0.10, "resilience": 0.04},
    # ---- Prehab / mobility / armor ----
    "Soleus/calf":       {"resilience": 0.34, "ankle": 0.16},
    "Copenhagen":        {"resilience": 0.22, "adductor": 0.30},
    "Pallof/anti-rot":   {"resilience": 0.14, "contact": 0.20, "tspine": 0.03},
    "T-spine/hip mob":   {"tspine": 0.34, "hip": 0.18, "ankle": 0.06},
    # ---- Skill (sole supplier; high K so it can't be "solved" in one session) ----
    "Skills (shoot/etc)":{"skill": 0.40, "contact": 0.02},
}


def standalone_growth_per_min(ex, dose_min=8.0):
    """Weighted 12-week growth this exercise produces per minute, run solo at a
    representative dose (8 min ~= 3 hard sets). The 'which exercises won' lens."""
    doses = {sd: dpm * dose_min for sd, dpm in CATALOG[ex].items()}
    scores = gs.goal_scores({sd: gs.subdim_growth_from_dose(sd, d) for sd, d in doses.items()})
    return gs.weighted_total(scores) / dose_min


print("=" * 64)
print("STAGE 1 — exercise leaderboard (weighted 12-wk growth per minute, solo)")
print("draft catalog — pending Codex/Gemini validation")
print("=" * 64)
ranked = sorted(CATALOG, key=lambda e: -standalone_growth_per_min(e))
for i, ex in enumerate(ranked, 1):
    goals = "".join(sorted({gs.SUBDIM_GOAL.get(sd, "?") for sd in CATALOG[ex]}))
    print(f"{i:>2} {ex:<20} {standalone_growth_per_min(ex)*1000:>6.2f}   hits:{goals}")

print("\n" + "=" * 64)
print("OPTIMIZED WEEKLY DOSE — greedy allocation of a strength+conditioning budget")
print("=" * 64)
# Weekly time budget for programmable strength+conditioning (game + skills sit
# outside this; ~3 strength sessions + conditioning). Floors keep every goal alive.
BUDGET = 180  # minutes/week
FLOORS = {"L": 0.45, "B": 0.40, "M": 0.35}  # aesthetics is the 0.40-weighted free objective
res = gs.optimize(CATALOG, budget_min=BUDGET, step=2.0, floors=FLOORS)
print(f"budget {BUDGET} min/wk | floors {FLOORS}")
print(f"weighted total: {res['total']:.3f}   goal scores: "
      f"A {res['scores']['A']:.2f}  L {res['scores']['L']:.2f}  "
      f"B {res['scores']['B']:.2f}  M {res['scores']['M']:.2f}")
print("\nminutes allocated (descending):")
for ex, mins in sorted(res["alloc"].items(), key=lambda kv: -kv[1]):
    print(f"   {ex:<20} {mins:>5.0f} min")
