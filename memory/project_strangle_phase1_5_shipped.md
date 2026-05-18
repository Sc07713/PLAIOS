---
name: strangle-low-iv-phase1-5-FALSIFIED-2026-05-18
description: "Long-strangle low-IV Phase 1.5 VERDICT FALSIFIED 2026-05-18 — the 'edge confirmed' result was a same-bar IV-shift backtest bug; corrected engine shows long-strangle on SPY loses money under realistic spread. See [[options-systematic-spy-falsification-2026-05-18]] for the comprehensive replacement study."
metadata: 
  node_type: memory
  type: project
  originSessionId: 2130c773-0bce-4741-83dd-41949e3c053c
---

> **STATUS 2026-05-18: FALSIFIED.** The Phase 1.5 "edge confirmed" verdict was caused by a same-bar IV-shift bug in `scripts/strangle_low_iv_study.py` (entry priced at `vix[i]`, MTM at bar i+1 used `vix[i+1]` → systematic free-vega gains; most trades exited same bar on profit_50%). See [[options-systematic-spy-falsification-2026-05-18]] for the full investigation. The recommendations below are preserved for historical record but should NOT be acted on. Tier 2 tastytrade calibration is no longer high-confidence justified — long-strangle on SPY structurally loses money under corrected mechanics + realistic spread.

---

Phase 1.5 of the long-strangle-low-IV study SHIPPED 2026-05-17 (same-day continuation of the Phase 1 build session). Phase 1 was INCONCLUSIVE with positive signal (OOS Sharpe 1.07 but IS→OOS drop 59.6% failed the <30% gate; picks clustered at grid edge). Phase 1.5 expanded the grid (`delta ∈ {0.05..0.16}`, `dte ∈ {20..40}`, spread=0.15 fixed), used a regularised selection rule (`max(min_sharpe)`), and **flipped the verdict to EDGE CONFIRMED**.

**Phase 1.5 chosen pick:** `vix_pct=0.30, dte=25, delta=0.05, exit=combined, spread=0.15`
- IS Sharpes across 5 cohorts: 1.79 / 2.15 / 2.49 / 2.53 / 3.35 (mean 2.46, min 1.79)
- **C6 OOS Sharpe: 1.87** (CAGR 20.1%, MaxDD -10.0%, win 63%, 46 trades)
- IS→OOS drop: **23.9% (gate <30% PASS)** — was the only failing gate in Phase 1
- 7/8 gates PASS (DSR deferred, still proxied); 0 FAILS
- OOS beats SPY-BH 1.37, random-entry 1.10, opposite-short -0.04

**The mechanism:** deeper OTM (0.05Δ vs 0.10Δ) + shorter DTE (25 vs 30) means cheaper premium per trade → less spread tax → more trades per cohort (192 vs 114 avg) → tighter Sharpe estimate. At low-VIX entry, deep-OTM legs are very cheap; if realised vol or directional move materialises, the legs convert efficiently.

**Why:** the Phase 1 fail-mode was a grid-edge artifact + unrealistic spread=0.05 assumption — NOT a fundamental absence of edge. Phase 1.5 picked a better point in parameter space under realistic cost assumptions and the edge held.

**How to apply:** the strangle book is now a viable parallel sleeve candidate to [[user_investment_philosophy]]'s SPY_top_5 equity book — but NOT YET DEPLOYABLE. Three caveats:
1. Pick is at the deepest-OTM edge of the new grid (delta=0.05); all top-10 picks share this. Real optimum may be at delta<0.05 (BS-synth unreliable there).
2. BS-synth pricing under-estimates real OTM premium (no skew) — worst at deep OTM. Tier 2 with skew-aware pricing is the validation step.
3. Single OOS window; rolling-window robustness still untested.

**Decision tree branch hit:** "iterated pick passes ALL 8 gates → proceed to Tier 2." Kickoff for next session at `D:\Plaios-tools\trading-tools\journal\next-session-strangle-tier2.md` — covers scope brainstorm (skew-overlay study vs full IV-surface backfill vs live forward-test).

**Rolling-window OOS validation SHIPPED same session (addendum):** chose 5 non-overlapping 6-month windows 2024-H1 to 2026-H1. **4/5 windows positive Sharpe** (range 2.41 → 4.60, mean 2.72); W3_2025H1 had zero trades (filter correctly stayed out — VIX wasn't in bottom-30% of trailing year). 4/5 beat SPY-BH in same window. **Confirms Phase 1.5 verdict was NOT window-luck → Tier 2 elevated from "justified" to HIGH-CONFIDENCE.** Methodological note: rolling-window approach pre-loads 380 days of warmup VIX before each window so the 252-bar percentile rank is honest at trade time. The original C6 cohort measurement (46 trades / 28 months ≈ 20/yr) under-counted vs the rolling-window measurement (112 trades / 30 months ≈ 45/yr) because in-cohort warmup NaN-locks the first 252 bars. **For Tier 2 execution sizing, plan ~45 trades/year of 0.05Δ contracts, not 20.**

**Files / artefacts:**
- Writeup: `docs/studies/2026-05-17-strangle-low-iv-phase1-5.md`
- Sweep driver: `scripts/strangle_low_iv_minisweep.py`
- Re-selection + OOS: `scripts/strangle_reselect_phase1_5_minisweep.py`
- Pick artefact: `runs/strangle_low_iv/phase1_5_minisweep_pick.json`
- 750 + 1 new run artefacts under `runs/strangle_low_iv/{cohort}/{hash}/`

Tests stayed green (21 options + strangle pass; full suite ~285).

See [[project_tastytrade_options_account]] (venue context for Tier 2), [[user_investment_philosophy]] (sleeve allocation rationale), [[feedback_trading_tools_is_a_hypothesis_factory]] (Phase 1.5 is a study output — Tier 2 may be study or build depending on scope).
