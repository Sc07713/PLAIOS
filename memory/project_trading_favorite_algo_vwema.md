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

**Status update (2026-05-12):** the V2 port `vwema_bb_meanrev` is a *lobotomised* version — binary 100%-in/out, no tiered exits, no stop-loss, next-bar-open fills (the EVWMA-band signal generation is faithful via `_base.vwema_bb`; everything else was dropped because the harness couldn't do it). The Pine's long/default-flags tiered-exit state machine has now been **decoded and a faithful port designed + approved** (½→¼→⅛→⅛ scale-out at middle/upper/middle-down + break-even exits + the `×0.9` StopPercentage stop on the pre-tier-1 state + immediate lower-band re-entry, via a new harness `tiered_meanrev` position-management mode with limit-at-level intrabar fills, single-instrument only). Plan/impl is next session — full design in `journal/next-session-vwema-bb-tiered-port-kickoff.md` and [[project_trading_v3_scope_pending]]. Parked follow-ons: RL/linreg parameter tuning; **pyramiding into momentum** ("add to winners on an incoming big momentum move" — the open problem; the Pine computes the ingredients — TTM squeeze, momentum osc, DSTHigh/52w-high touches — but the default path ignores them; → a future `pyramid_momentum` mode).
