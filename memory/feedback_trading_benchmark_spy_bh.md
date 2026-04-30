---
name: Trading benchmarks — SPY-BH and asset-class-BH always
description: Every backtest in trading-tools reports against TWO benchmarks: SPY buy-and-hold (universal) and buy-and-hold on the underlying instrument the strategy traded (asset-class). Permanent design rule.
type: feedback
originSessionId: 0d218a34-186a-4cde-a701-6a21bc41bfe8
---
Every strategy backtest must report a side-by-side comparison against TWO benchmarks over the same period:

1. **SPY buy-and-hold** — universal benchmark. The cheapest baseline an investor could hold instead of running any strategy.
2. **Buy-and-hold on the underlying instrument** — asset-class benchmark. If a strategy trades NVDA, the comparison is against NVDA-BH. Tells you whether the strategy beats just owning the thing it trades.

Both comparisons are mandatory in every backtest result.

**Why:** Beating SPY proves the strategy beats the cheapest passive alternative. Beating asset-BH proves the strategy adds value over passively holding what it trades. A strategy can lose to SPY but beat asset-BH (good strategy on a weak underlying), or beat SPY but lose to asset-BH (the underlying ran hot regardless of signal). Both numbers matter and tell different stories. Stated by Scott 2026-04-30 during V2 brainstorm.

**How to apply:** Backtest result schema includes both benchmark comparisons (excess return, info ratio, beat-rate). Harness validation case: SPY-BH strategy should reproduce SPY's actual total return; asset-BH for any other strategy should reproduce that asset's total return. Both are sanity checks against the harness itself.
