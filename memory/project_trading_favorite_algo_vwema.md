---
name: Favorite trading algo — VWEMA-BB Momentum Strategy
description: Scott's favourite algo from previous trading work; saved as anchor artefact for the new Trading domain
type: project
originSessionId: fb24bd11-1fee-469b-8616-1708b50cd5bb
---
Scott's nominated "favourite algo I built" for the new Trading domain is the **Volume Weighted Exponential Moving Average + Bollinger Bands + Momentum strategy** (Pine Script v5, fork of RezzaHmt's original on TradingView).

Saved at: `domains/trading/legacy/algos/VWEMA-BB-momentum-strategy.pine` (added 2026-04-28).

Key features the design-test-store loop will need to honour when porting / testing:
- Volume-weighted EVMA (custom function `f_evwma`) blended across 4 lookback fractions (1.0×, 0.75×, 0.5×, 0.25×) — not a vanilla VWMA
- Multi-timeframe: Daily Short Term (default 20), Daily Long Term (default 200), Weekly (default 100)
- Tiered exit ladder (tier 0→1→2→3) with partial closes at middle/upper bands
- Two regime modes: **mean-reversion** (default — buy lower band) and **momentum** (52-week high / DSTHigh-touch breakout)
- TTM Squeeze integration (when `stdev(20)*2 < ATR(20)*1.5` → squeeze on)
- Long-only / Short-only / Long-and-Short modes (`Short` input: 0/1/2)
- Default 10% stop loss (`StopPercentage = 0.9`)
- Re-entry logic: on stop-out at lower band, immediately re-enter

**Why:** Anchors the new Trading domain in something concrete Scott already trusts. Per v4 prompt's "current state precedes new state," any backtest infra will be measured against whether it can reproduce this strategy faithfully on real data before being trusted on novel strategies.

**How to apply:** When designing the backtest harness, the harness must be able to express tiered exits, regime switches, multi-timeframe inputs, and custom volume-weighted moving averages. Don't pick a backtest library that can't handle these (rules out the most simplistic ones; vectorbt or similar is fine).
