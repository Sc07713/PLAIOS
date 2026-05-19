# Next-session kickoff — leverage-push sweep

**Status:** Open. Was originally queued by
[[project_stack_and_lever_fusion_2026-05-19]] but pivoted out of the
2026-05-19 session when the user asked for live deployment translation
instead. This doc captures the original intent so it can be picked up
in a later session.

## Question

The stack-and-lever fusion landed at avg L 2.02× / DD -29% on the
"honest" cell (ma200 70/30 tv=0.25). That's 16pp of unused DD headroom
under the -45% cap. Can the strategy push further on leverage without
breaching the gate?

## Hypothesis

**Plausible ceiling:** tv=0.30 + cap=3.0 → CAGR 33-37% / DD -35 to -40%
/ avg L 2.4-2.6×. Still under the -45% gate.

**Falsification gates:**
- DD must stay above -45% (hard cap)
- Sharpe must stay above 1.10 (don't degrade risk-adjusted return for
  raw CAGR — the prior Arm C aggressive at Sharpe 1.14 is the floor)
- Beat SPY-BH (essentially automatic)
- Beat SPY_top_5 baseline on Sharpe (currently 1.03)

## Sweep grid

`scripts/stack_and_lever_fusion_study.py` is the template — extend the
TARGET_VOLS and add a LEV_CAPS sweep:

```python
TARGET_VOLS = [0.275, 0.30, 0.325, 0.35, 0.375, 0.40]   # 6 values
LEV_CAPS    = [2.5, 3.0, 3.5]                            # 3 values
WEIGHTS     = [(0.7, 0.3)]                               # fix at the winner
GATE_VARIANTS = ["ma200"]                                # fix at the honest gate
```

= 18 cells. All on the honest cell (ma200 + 70/30) — no skip-September
(retracted) and no weight sweep (70/30 already won).

## Expected outputs

1. `runs/leverage_push/results.csv` — all 18 cells with metrics
2. `docs/studies/2026-05-XX-leverage-push.md` — writeup with:
   - Pareto frontier (CAGR vs Sharpe vs DD)
   - Did the strategy break the -45% DD ceiling? At what L?
   - Did Sharpe degrade past 1.10? At what L?
   - New deployable cell or no improvement?
3. Memory update if a new best cell lands

## What might falsify the hypothesis

- **Borrow-cost erodes the gain** — at L > 2.5×, borrow cost compounds.
  At spread=1%, cost of leverage at 2.5× = 1.5% of capital/year (1% on
  the 1.5× borrowed). At 3.0× = 2% drag. Diminishing returns.
- **Vol of vol** — vol-targeting works when realized vol is stable.
  At higher target_vol, the strategy gets whipsawed more by vol spikes
  (leverage steps down hard then back up). Net Sharpe could degrade.
- **Tail events** — average DD is benign at higher L because the gate
  catches the slow drawdowns. But a fast single-day shock at high L
  could exceed the gate's response time.

## Skip if

The user is happy with the current Aggressive deployment and isn't
asking for more aggressive sizing. This is a "what's the ceiling"
study, not a "we need more returns" study.

## Related

- [[project_stack_and_lever_fusion_2026-05-19]] — predecessor study
- [[project_levered_spy_top5_study_2026-05-18]] — Arm C origin
- [[project_deployment_state_2026-05-19]] — live deployment that
  could absorb a higher-leverage profile if found
