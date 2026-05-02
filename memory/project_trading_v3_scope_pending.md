---
name: trading V3 scope — needs design session
description: Mid-2026-05-03 V2 finished + VWEMA-BB ported; V3 scoping deferred — event overlay (PEAD), news sentiment, harness extensions, quality fundamentals all on the table
type: project
originSessionId: f7943455-e60e-4ac8-9d10-15a64ba1e70d
---
V2 shipped 2026-05-02; VWEMA-BB Momentum simplified port added 2026-05-03 (run_id 253-258, contested edge_status). User wants V3 scoping done in a dedicated session — too many open design questions to resolve in passing.

**V3 scope items to weigh and prioritise (not yet decided):**

1. **Earnings event overlay (PEAD)** — Bernard & Thomas 1989. Free data (Finnhub/AlphaVantage/IB fundamentals). Adds `events` table + earnings ingest + `pead` strategy. ~1 day. Cheapest "real edge" candidate.
2. **News sentiment overlay** — User specifically asked about this. Wants positive-news → long on quality stocks, negative-news → short on quality stocks. Needs feed (Polygon/Benzinga/NewsAPI — mostly paid) + sentiment classifier (LLM or vendor score). Higher complexity, mixed academic edge. Likely V3.5.
3. **Quality fundamentals** — V2.5 in current roadmap. P/E, FCF growth, ROE. Required for "quality stocks only" filter that PEAD and news strategies need. Free via AlphaVantage/Finnhub.
4. **Harness extensions for faithful Pine ports** — to make VWEMA-BB Momentum match its TradingView baseline:
   - Per-strategy stop-loss param (entry-price-anchored % stop)
   - Limit-order fill semantics (fill at min(limit, next_open) for buy limits)
   - Fractional position management (sell ½, ¼, ⅛ on tiered triggers)
   - Currently V2 signal protocol is binary entry/exit + next-bar-open fill, which biases mean-reversion strategies down vs Pine
5. **Options layer** — V3 in roadmap. Replace synthetic shorts (no borrow cost) with put-spreads. Needed for honest long_short backtests.
6. **VWEMA-BB long_short variant** — easy after #5 lands. Pine supports Short=1 and Short=2 modes already documented.
7. **`backtest_results` schema fix** — NUMERIC(10,6) overflows for >9999x returns (caught by NVDA high_52w_breakout fail). Widen to NUMERIC(14,6) and re-run the failed runs.

**User's stated preference:** "buy and hold quality stocks with good management" appears to dominate. V3 should layer event/sentiment overlays on that base, not try to replace it. Frame V3 as "find the small alpha on top of BH, not as a BH-substitute".

**Current state:** trading-tools master at commit b03ce06 (VWEMA-BB), pushed to GitHub. 12 strategies registered. 256+ backtest runs in trading_data. 64 tests pass.

**Files:** plan + spec dirs at `D:\PLAIOS\docs\superpowers\{plans,specs}\`. Repo at `D:\Plaios-tools\trading-tools\`.
