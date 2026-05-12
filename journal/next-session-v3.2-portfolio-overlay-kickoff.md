# Next session — kickoff prompt

**Saved:** 2026-05-12
**For:** trading-tools V3.2 — portfolio overlay (the cheapest mechanical path to a real >0.9 Sharpe)

---

## Copy-paste this into the next session

```
We're starting trading-tools V3.2 — the portfolio overlay. This is a brainstorm-then-build session: please use the brainstorming skill (it's creative design work), drive the design questions one at a time, present a design, get my approval, write the spec + plan, then implement.

WHERE WE ARE (from prior sessions)

Repo: D:\Plaios-tools\trading-tools (GitHub Sc07713/trading-tools, master). Postgres 17 local, port 5432, db trading_data, user postgres, password QLHr3rmx@*rZWd (literal @ and *). Connect: $env:PGPASSWORD='QLHr3rmx@*rZWd'; & 'C:\Program Files\PostgreSQL\17\bin\psql.exe' -h 127.0.0.1 -U postgres -d trading_data ... . Python: D:\Plaios-tools\trading-tools\.venv\Scripts\python.exe . Tests: .\.venv\Scripts\python.exe -m pytest -q (91 pass).

V3 is decomposed into 3 sub-projects (decision log 2026-05-11): V3.1 robustness layer — SHIPPED 2026-05-11; V3.2 portfolio overlay — THIS SESSION; V3.3 fundamentals/PEAD — later. Read first: docs/project-state.md, docs/decisions.md, docs/strategies.md, docs/specs/2026-05-11-v3.1-robustness-layer.md, docs/plans/2026-05-11-v3.1-robustness-layer.md, and memory project_trading_v3_scope_pending.md.

What V3.1 left in place (build on it, don't rebuild it): transaction costs (cost_bps, 5 bps round-trip in runners; _walk_signals default 0.0); full/IS/OOS split (periods.py — OOS = last 30% of bars by bar count, shared boundary bar); Probabilistic + Deflated Sharpe Ratio in backtest/stats.py (stdlib-only); backtest_period_stats table + cost_bps/oos_fraction cols on backtest_runs; tt verdict-report <run_id> → REAL EDGE (OOS Sharpe>0.9 ∧ DSR≥0.95) / PROMISING (∧ PSR(0.9)≥0.95) / NO EDGE; run_baseline.backfill_dsr().

V3.1 result (the motivation for V3.2): the 250-run cost-aware re-run found 0 REAL EDGE, 0 PROMISING. Best OOS Sharpe anywhere is AVGO buy-and-hold at 1.52 — but PSR(0.9)=0.87, DSR=0.65, and AVGO is survivorship (a 2026-TOP-25 name because it won). The deflated SR* threshold over the 224-trial family is ≈1.31 annualised. Single-symbol Sharpe is bounded by single-stock vol; the hypothesis V3.2 tests is that combining a real ~0.5-0.8 single-name edge across the 25-name universe mechanically lifts portfolio Sharpe to 0.9-1.1 from diversification alone — and that the IS-fit / OOS-test machinery finally becomes a real held-out test (today's strategies are parameter-free, so IS/OOS is only a stability check).

WHAT V3.2 IS

A multi-instrument portfolio layer on top of the existing single-instrument harness: take a strategy's signals across all 25 names, hold a portfolio of positions, rebalance on a cadence, report cost-aware full/IS/OOS Sharpe + PSR + DSR vs SPY-BH AND vs an equal-weight-universe-BH benchmark. The harness today (backtest/harness.py::_walk_signals) walks ONE symbol — V3.2 needs a portfolio walk that holds N positions concurrently.

DESIGN QUESTIONS TO RESOLVE IN BRAINSTORMING (one at a time — don't dump these all at once)

- Scope of "portfolio": one strategy spread across the 25 names (a portfolio of that strategy's positions), or an ensemble that blends multiple strategies? Start with the former; ensemble can be V3.2b.
- Weighting scheme: equal-weight active positions, inverse-volatility, risk-parity, or market-neutral long/short (dollar-neutral)? Trade-offs: equal-weight is simplest and the honest first cut; inverse-vol is the standard "free Sharpe" lever; market-neutral matters for the long_short strategies but inherits the synthetic-short caveat (no borrow cost — flag it).
- Rebalance cadence: daily, weekly, monthly? Affects turnover → cost. The cost_bps model already exists; portfolio rebalancing multiplies trade count, so this is where costs start to bite.
- Position cap / cash drag: max N concurrent positions? What happens when fewer than N names have a signal — hold cash, or scale up the ones that do?
- Parameter fitting: does V3.2 introduce ANY fitted parameter (e.g., the weighting scheme's lookback, the position cap, a signal threshold)? If yes — fit on IS only, report on OOS. This is the first time the IS/OOS split is load-bearing; get the fit/test discipline right.
- Schema: new portfolio_runs / portfolio_period_stats tables, or reuse backtest_runs with a synthetic symbol like 'PORTFOLIO:<strategy>'? Lean toward a small new table — a portfolio run has a universe + weighting + rebalance cadence, not a single symbol.
- Benchmark set: SPY-BH is one. The asset-BH analogue for a portfolio is "equal-weight buy-and-hold of the same 25 names" — add that as the portfolio's asset-BH. Both mandatory (standing rule).
- Charts / artifacts: per-name contribution attribution? Equity curve vs both benchmarks? Keep it minimal for V3.2; expand later.

STANDING RULES (don't re-litigate)

- Every backtest reports vs SPY-BH AND vs buy-and-hold on the underlying (for a portfolio: equal-weight-universe-BH). Both mandatory.
- Cost-aware by default in the runner; 20-year data window is enough (pre-IB-window regime not analogous).
- The base case is "buy and hold quality stocks with good management" — V3.2 is hunting the small alpha on top of BH, not a BH-substitute. If the portfolio overlay can't beat equal-weight-universe-BH on a DSR basis, that's a real (negative) result, not a failure to push harder.
- Universe is hardcoded TOP_25, survivorship-flagged not -corrected. Don't try to solve survivorship in V3.2.
- Use the brainstorming skill, then writing-plans, then implement TDD with frequent commits (the V3.1 plan in docs/plans/ is the template for granularity).

HOW TO START

1. Read the docs listed above + the V3.1 spec/plan to internalise the conventions.
2. Invoke the brainstorming skill. Explore the codebase (harness.py, periods.py, stats.py, run_baseline.py, schema.sql, cli.py). Then drive the design questions above, one at a time.
3. Present a design, get my approval, write docs/specs/{date}-v3.2-portfolio-overlay.md + docs/plans/{date}-v3.2-portfolio-overlay.md, commit, then implement.
4. End state: a tt CLI path to run a portfolio backtest, the new schema, a re-run across the strategy set, and an honest entry in docs/strategies.md — does ANY strategy's portfolio overlay clear REAL EDGE? (Expectation: maybe high_52w_breakout in a cross-sectional rank-and-hold frame, per its literature; most others probably still NO EDGE. The point is to find out, rigorously.)
```

---

## Notes for the orchestrator (Claude in next session)

- Don't rebuild V3.1. Costs, periods, PSR/DSR, verdict-report all exist and work. Build the portfolio walk on top.
- The single biggest open design call is the weighting scheme — recommend starting with equal-weight (honest baseline) and inverse-vol (the standard free-Sharpe lever) as the two to ship, holding risk-parity / market-neutral for V3.2b.
- Watch the synthetic-short caveat: a market-neutral long/short portfolio overlay inherits "no borrow cost, no slippage on shorts" — flag it loudly in the spec and the verdict-report output. The honest version of market-neutral waits for the V4 put-spread layer.
- The IS/OOS discipline finally matters here. Any fitted parameter: fit on IS bars, freeze, evaluate on OOS bars. Don't peek at OOS to pick the weighting scheme. If you find yourself comparing OOS Sharpes across weighting schemes to decide which to use, you've broken the held-out test — decide on IS, report on OOS.
- high_52w_breakout (George & Hwang 2004) is genuinely a cross-sectional strategy in the literature — "rank by 52-week-high nearness, long the top decile, hold, rebalance monthly". The single-symbol V2/V3.1 version isn't the real strategy. A portfolio frame is its natural home — worth treating as the showcase case for V3.2, and re-run it on adjusted=False bars (level-based signal).
- If V3.2's portfolio overlay produces a REAL EDGE, V3.3's priority drops (note it in the decision log). If it doesn't, that's still a clean result — record it and move to V3.3 fundamentals.
- Stale: journal/next-session-insurance-audit-kickoff.md (that audit shipped 2026-05-06) — ignore it.
