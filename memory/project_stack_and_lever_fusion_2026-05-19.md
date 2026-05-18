---
name: stack-and-lever-fusion-2026-05-19
description: Stack-and-lever fusion shipped. New best deployable cell strictly dominates prior Arm C aggressive on Sharpe and DD. Honest ma200 70/30 tv=0.25 → 29.94% CAGR / Sharpe 1.20 / DD -28.92% / avg L 2.02×.
metadata: 
  node_type: memory
  type: project
  originSessionId: aad0f973-7da5-4223-826e-567d41f6abac
---

Thread 3+4 fusion shipped 2026-05-19. Composes the defensive layers
that worked in the 2026-05-18 sprint (70/30 SPY_top_5+GLD-BH blend +
200d-MA regime gate) then applies vol-targeted leverage on top.

**Why:** the sprint showed each defensive layer cuts DD ~15-18pp but
costs ~5pp CAGR; the levered SPY_top_5 study was bottlenecked at -45%
DD cap. Stacking the layers cuts unlevered DD to -17%, creating 28pp
of fresh leverage headroom. Filled with vol-targeted leverage at cap
2.5×, target_vol 0.25.

**How to apply:** when the user asks about the "best trading
strategy" or "what's the new best cell," point to this entry and
the writeup at `docs/studies/2026-05-19-stack-and-lever-fusion.md`.

## Headline result

| Cell | CAGR | Sharpe | DD | avg L | Note |
|---|---|---|---|---|---|
| **ma200 70/30 tv=0.25** | **+29.94%** | **1.20** | **-28.92%** | **2.02×** | **NEW BEST** |
| Arm C aggressive (prior) | +31% | 1.14 | -39.5% | 1.30× | superseded |
| SPY_top_5 baseline | +23.37% | 1.03 | -46.17% | 1.0× | reference |
| ma200 70/30 unlevered | +16.37% | 1.23 | -16.93% | 1.0× | cleanest base |

The unlevered stacked blend has Sharpe 1.23 — the best risk-adjusted
return found anywhere to date. Leverage amplifies a cleaner base.

## Three deployable cells, ranked by aggressiveness

| Profile | Cell | CAGR | Sharpe | DD |
|---|---|---|---|---|
| Conservative | ma200 70/30 tv=0.15 | +20.78% | 1.28 | -20.86% |
| Balanced | ma200 70/30 tv=0.20 | +25.98% | 1.23 | -25.35% |
| Aggressive | ma200 70/30 tv=0.25 | +29.94% | 1.20 | -28.92% |

All three strictly dominate the prior session's Arm C trio on Sharpe
and DD.

## Methodology audit — "skip September" RETRACTED

Initial fusion sweep found `ma200_skip_sep + 70/30 + tv=0.25` at 31.59%
CAGR / Sharpe 1.25 / DD -29.34%. Looks great. Then ran proper monthly
seasonality stats:

- **Bonferroni-corrected p-test (12 months)**: NO month significant
- **Split-sample test**: September sign FLIPS between halves
  - SPY-BH: +0.46% (2006-2015) → -1.22% (2016-2026)
  - SPY_top_5: +1.88% (2010-2017) → -3.55% (2018-2026)
- **Robust feature**: only July passes consistency check (positive in
  both halves, uncorrected p<0.01) but doesn't survive Bonferroni

Conclusion: skip-September was an in-sample-only artifact driven by
the second decade. Removed from deployable stack. The honest cell is
the ma200-only variant (no seasonality).

This is a useful template for future findings: any "skip month X" or
"buy month Y" claim needs Bonferroni + split-sample validation before
deployment.

## What's open

1. **Push leverage further** — DD is well under -45% cap; sweep
   tv ∈ {0.275-0.40} × cap ∈ {2.5-3.5}. Kickoff doc at
   `journal/next-session-leverage-push.md`. Plausible ceiling:
   tv=0.30 + cap=3.0 → 33-37% CAGR at DD -35 to -40%.
2. **V1 weekly short strangle as 10-15% sleeve** on top of this
   stack — Sharpe lift via decorrelation, no DD cost.
3. **Deployment decision** still required from user (Conservative /
   Balanced / Aggressive).

## Related

- [[project_edge_investigation_sprint_2026-05-18]] — the 8-study
  sprint that surfaced the components
- [[project_levered_spy_top5_study_2026-05-18]] — Arm C origin
  (now superseded as "best CAGR cell")
- [[user_investment_philosophy]] — beat-gold-BH + decorrelation
  philosophy is realized by the gold sleeve here
- [[feedback_trading_tools_is_a_hypothesis_factory]] — proper stats
  test killing the skip-Sep finding is the framework working as
  designed
