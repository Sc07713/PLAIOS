"""
Stage 1 growth-model sanity gates (the tests promised in the v7 spec).
If the model violates known training science, these fail.
"""
import growth_sim as gs


# ---- Cycle 1: hypertrophy dose-response curve ----

def test_zero_dose_zero_growth():
    """No sets to a muscle => no hypertrophy."""
    assert gs.hypertrophy_growth(0) == 0


def test_growth_rises_with_volume_but_diminishes():
    """More weekly sets => more growth, but with diminishing marginal returns."""
    g2, g5, g10 = gs.hypertrophy_growth(2), gs.hypertrophy_growth(5), gs.hypertrophy_growth(10)
    assert g2 < g5 < g10                       # monotonic in the productive range
    first_5 = gs.hypertrophy_growth(5) - gs.hypertrophy_growth(0)
    next_5 = gs.hypertrophy_growth(10) - gs.hypertrophy_growth(5)
    assert next_5 < first_5                     # diminishing returns


def test_junk_volume_past_mrv_reduces_net_growth():
    """Volume well past MRV (~22 sets) is net-negative vs a sane dose."""
    assert gs.hypertrophy_growth(32) < gs.hypertrophy_growth(20)


# ---- Cycle 2: effective sets (RIR) + frequency ----

def test_sets_near_failure_count_more():
    """3 sets at 1 RIR stimulate more than 3 sets at 4 RIR (same set count)."""
    assert gs.effective_sets(3, rir=1) > gs.effective_sets(3, rir=4)


def test_full_effort_sets_count_fully():
    """Sets at <=2 RIR count at full weight."""
    assert gs.effective_sets(3, rir=1) == 3.0


def test_frequency_split_beats_single_session():
    """Same weekly volume across 2 sessions beats 1 (refreshed protein synthesis)."""
    once = gs.weekly_hypertrophy(10, frequency=1)
    split = gs.weekly_hypertrophy(10, frequency=2)
    assert split > once


# ---- Cycle 3: weighted aggregate + leanness multiplier ----

def test_goal_weights_are_40_20_20_20():
    """Total weights aesthetics 40, the rest 20 each."""
    assert gs.weighted_total({"A": 1, "L": 0, "B": 0, "M": 0}) == 0.40
    assert gs.weighted_total({"A": 0, "L": 1, "B": 0, "M": 0}) == 0.20
    assert gs.weighted_total({"A": 0, "L": 0, "B": 1, "M": 0}) == 0.20
    assert gs.weighted_total({"A": 0, "L": 0, "B": 0, "M": 1}) == 0.20


def test_leanness_scales_aesthetics_only():
    """A 0.5 leanness factor halves the aesthetics contribution, nothing else."""
    full = gs.weighted_total({"A": 1, "L": 1, "B": 1, "M": 1}, leanness=1.0)
    half = gs.weighted_total({"A": 1, "L": 1, "B": 1, "M": 1}, leanness=0.5)
    assert full == 1.0
    assert half == 0.40 * 0.5 + 0.20 + 0.20 + 0.20


def test_goal_scores_average_subdims_with_missing_as_zero():
    """One filled aesthetics sub-dim of four => A score 0.25 (breadth matters)."""
    scores = gs.goal_scores({"delts": 1.0})
    assert scores["A"] == 0.25


def test_qualities_saturate_at_different_rates():
    """Skill absorbs far more volume before saturating than mobility; VO2 slower than power.
    (Both reviewers refused a single K for all non-hypertrophy qualities.)"""
    # at equal dose, the slower-saturating quality shows LESS growth so far
    assert gs.subdim_growth_from_dose("skill", 6) < gs.subdim_growth_from_dose("ankle", 6)
    assert gs.subdim_growth_from_dose("vo2", 6) < gs.subdim_growth_from_dose("power", 6)


# ---- Cycle 4: greedy budget optimizer ----
# Tiny synthetic catalog: one aesthetics exercise, one longevity exercise,
# both delivering 1 dose-unit per minute to a single sub-dim.
CAT = {
    # aesthetics exercise filling ALL four A sub-dims -> stays attractive, would
    # eat the whole budget and starve longevity unless a floor intervenes.
    "exA": {"delts": 1.0, "back": 1.0, "arms": 1.0, "chest_upper": 1.0},
    "exB": {"vo2": 1.0},     # goal L (longevity, weight 0.20)
}


def test_allocation_respects_budget():
    """Never spends more than the weekly time budget."""
    res = gs.optimize(CAT, budget_min=10, step=1.0)
    assert sum(res["alloc"].values()) <= 10 + 1e-9


def test_first_minute_goes_to_higher_weighted_goal():
    """At equal curves, the first minute buys aesthetics (0.40) over longevity (0.20)."""
    res = gs.optimize(CAT, budget_min=1, step=1.0)
    assert res["alloc"].get("exA", 0) == 1
    assert res["alloc"].get("exB", 0) == 0


def test_marginal_value_is_non_increasing():
    """Concave growth + greedy => each successive minute is worth <= the last."""
    res = gs.optimize(CAT, budget_min=20, step=1.0)
    trace = res["trace"]
    assert all(trace[i] >= trace[i + 1] - 1e-9 for i in range(len(trace) - 1))


def test_floor_forces_underweighted_goal_to_be_trained():
    """A longevity floor pulls budget to exB even though aesthetics is higher-weighted."""
    # budget 16 so the floor stays achievable now that vo2 saturates slower (K=11)
    free = gs.optimize(CAT, budget_min=16, step=1.0)
    floored = gs.optimize(CAT, budget_min=16, step=1.0, floors={"L": 0.20})
    assert floored["alloc"].get("exB", 0) > free["alloc"].get("exB", 0)
    assert floored["scores"]["L"] >= 0.20 - 1e-9
