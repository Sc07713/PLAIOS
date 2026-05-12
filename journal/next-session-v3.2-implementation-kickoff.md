# Next-session kickoff — trading-tools V3.2 (implementation)

We're implementing trading-tools V3.2 — the portfolio overlay. **The design is done and the spec is committed.** This session: read the spec, use the writing-plans skill to produce the implementation plan, get my approval on the plan, then implement it TDD with frequent commits. (The brainstorm is over — do not re-open design questions unless implementation surfaces a real contradiction in the spec.)

## WHERE WE ARE

Repo: `D:\Plaios-tools\trading-tools` (GitHub `Sc07713/trading-tools`, branch `master`). Postgres 17 local, port 5432, db `trading_data`, user `postgres`, password `QLHr3rmx@*rZWd` (literal `@` and `*`). Connect: `$env:PGPASSWORD='QLHr3rmx@*rZWd'; & 'C:\Program Files\PostgreSQL\17\bin\psql.exe' -h 127.0.0.1 -U postgres -d trading_data ...` . Python: `D:\Plaios-tools\trading-tools\.venv\Scripts\python.exe`. Tests: `.\.venv\Scripts\python.exe -m pytest -q` (91 pass, all green at start).

V3 is decomposed (decision log 2026-05-11): **V3.1 robustness layer — SHIPPED 2026-05-11**; **V3.2 portfolio overlay — THIS SESSION** (spec done 2026-05-12, commit `0addc67`); **V3.3 fundamentals/PEAD — later**.

**READ FIRST:** `docs/specs/2026-05-12-v3.2-portfolio-overlay.md` — the V3.2 spec, the source of truth for this session. Also re-skim: `docs/plans/2026-05-11-v3.1-robustness-layer.md` (the **granularity template** for the new plan — Task 0 green baseline → numbered tasks each with failing-test → impl → pass → commit → final verification + push), `docs/project-state.md`, `docs/decisions.md`, `docs/strategies.md`, and PLAIOS memory `project_trading_v3_scope_pending.md` + `user_investment_philosophy.md` + `project_tastytrade_options_account.md`.

## WHAT V3.2 IS (one-paragraph summary — the spec has the detail)

An equity-sleeve-only multi-instrument layer on top of the single-instrument harness. A *portfolio run* takes one strategy, forward-fills its `entry_long`/`exit_long` into a per-name held-state (long-only — short cols ignored), and on a **weekly** cadence (param ∈ {daily, weekly, monthly}) holds **≤ 7** cash-equity positions + a **gold (GLD) residual sleeve** ("when in doubt hold gold" → zero theses = 100% GLD; one lone thesis = 60% it / 40% GLD). Two modes — same machine, different trim-to-7 tie-break: **basket** (trim by greedily dropping the highest-pairwise-correlation name, 120-day window) and **rank_hold** (trim to top-K ≤ 7 by a strategy-emitted `score` column — only `high_52w_breakout` gets one in V3.2: `close / rolling-252-high`). Held names are weighted by **equal** (default) / **inv_vol** (60d) / **risk_parity** (120d cov), then a hard **60% per-position cap** (excess redistributed pro-rata, then to gold). Cost = one-way turnover × `cost_bps`/10000 per rebalance (default 5 bps). **Fit-only-K-on-IS discipline:** rank_hold's K ∈ {3, 5, 7} is the *only* fitted param — grid-searched on the first 70% of bars by IS Sharpe, frozen, OOS reported on the frozen K (3-pt grid feeds DSR `n_trials`); basket mode has no fitted param so IS/OOS stays a stability check there. **Four-way benchmark:** `strategy` / `spy_bh` / `universe_ew_bh` / `gold_bh` — all mandatory. **Verdict:** REAL EDGE = OOS Sharpe > 0.9 ∧ DSR ≥ 0.95 ∧ beats *both* `universe_ew_bh` & `gold_bh` OOS Sharpe; PROMISING = OOS Sharpe > 0.9 ∧ PSR(0.9) ≥ 0.95; else NO EDGE. New modules `backtest/portfolio.py` + `backtest/portfolio_weights.py` + `backtest/run_portfolio_baseline.py`; new tables `portfolio_runs` + `portfolio_period_stats`; new strategy `gold_buy_hold` on GLD; GLD added to `KNOWN_INSTRUMENTS` (not `TOP_25`); CLI `portfolio-backtest` + `portfolio-report`; artifacts under `runs/portfolio/<id>/`. Per-rebalance thesis ranking emitted as the hook for a future options scanner.

## WHAT'S ALREADY THERE — build on it, don't rebuild it

- **V3.1 substrate:** transaction costs (`cost_bps`, 5 bps round-trip in runners; `_walk_signals` default 0.0); full/IS/OOS split (`backtest/periods.py` — `split_index`, `period_slices`, `split_timestamp`, `trades_by_period`; OOS = last 30% of bars by bar count); PSR + DSR in `backtest/stats.py` (`skewness`, `kurtosis`, `psr`, `expected_max_sharpe`, `deflated_sharpe` — stdlib-only); `backtest_period_stats` table; `tt verdict-report`; `run_baseline.backfill_dsr()`. **Reuse `stats.py` and `periods.py` unchanged.**
- **Signal interface:** every strategy is `fn(df, params) -> DataFrame` with bool columns `entry_long`/`entry_short`/`exit_long`/`exit_short` indexed to the bar index, plus optional extra columns (indicators — ignored by the walk). V3.2 adds an *optional* `score` column to this contract.
- **The single-instrument harness** (`backtest/harness.py` — `_walk_signals`, `run_backtest`, `Result`, `list_runs`, `load_result`, `set_verdict`, `compare`): **do not change it.** The portfolio walk is a *new* module that produces a portfolio equity curve and feeds it through the same `stats`/`periods` machinery.

## OPEN QUESTIONS THE PLAN MUST PIN (from the spec's "open questions for the plan stage")

1. `universe=None` ⇒ `list(TOP_25.keys())` (25 symbols incl. SPY — matches `run_baseline`).
2. Risk-parity solver = fixed-iteration multiplicative update (~50 iters, no SciPy) with an inverse-vol fallback on a singular/degenerate covariance. Pin a numerical test.
3. Cadence bar = the first available trading bar of each ISO week / month (robust to holidays); `daily` = every bar.
4. DSR `n_trials` = (count of distinct basket-mode portfolio runs of non-benchmark strategies) + 3·(count of fitted rank_hold runs); trial Sharpe variance = cross-sectional variance of annualised OOS Sharpes across the portfolio-run family (incl. the `asset_buy_hold` basket run).
5. `universe_ew_bh` = buy 1/25 of each name on bar 0 and let it drift (true buy-and-hold, weights diverge); one round-trip cost at the ends — like the single-instrument BH curves.

## HOW TO START

1. Read the spec + the docs above.
2. Invoke the **writing-plans** skill. Produce `docs/plans/2026-05-12-v3.2-portfolio-overlay.md` at the V3.1 plan's task-by-task granularity (Task 0 green baseline → stats/weights → schema → portfolio walk → CLI → baseline + DSR back-fill → docs → final verification + push), each task: failing test → implement → pass → commit. Commit the plan.
3. Get my approval on the plan before implementing.
4. Implement TDD, one commit per task. **Ingest GLD bars early** (`tt ingest --symbols GLD`, or the direct `db`/`ib_data` path) — the portfolio walk and `gold_bh` need GLD daily-adjusted bars over the 2010–2026 window. Run the ~12-run `run_portfolio_baseline`. Update `docs/strategies.md` (portfolio leaderboard + the "Sharpe lift vs each strategy's best single-name V3.1 run" read), `docs/project-state.md`, `docs/decisions.md` (decision entries: gold residual + 4-way benchmark + beat-gold hurdle in the verdict; ≤7 cap & 60% per-position cap; weekly cadence; portfolio cost = turnover × cost_bps; only-K-fitted discipline; equity-sleeve-only / tastytrade-options-is-V4). Full suite green. `git push` (branch `master`).

## END STATE

`tt portfolio-backtest` + `tt portfolio-report` working; `portfolio_runs` / `portfolio_period_stats` populated; the ~12-run portfolio baseline done; an honest entry in `docs/strategies.md` answering: does ANY strategy's portfolio overlay clear REAL EDGE? And — separately — how much did the overlay lift OOS Sharpe vs each strategy's best single-name V3.1 run (the diversification number, even if nothing clears the bar)? Expectation (per the V3.1 result + the literature): maybe `high_52w_breakout` in rank_hold; most basket runs probably still NO EDGE but with a higher Sharpe than their single-name versions — quantify it. The point is to find out, rigorously.

## STANDING RULES (don't re-litigate)

- **Equity-sleeve only.** The tastytrade options account is a separate sleeve, integration = V4. Options opportunity scanner is a parked post-V3.2 item.
- Every backtest reports vs SPY-BH AND vs buy-and-hold on the underlying — for a portfolio: `spy_bh` + `universe_ew_bh` + `gold_bh`, all mandatory.
- Cost-aware by default in the runner; 5 bps; 20-year data window is enough.
- Base case = "buy and hold quality stocks with good management" — V3.2 hunts small alpha *on top of* BH; if a portfolio overlay can't beat `universe_ew_bh` AND `gold_bh` on a DSR basis, that's a real (negative) result, not a failure to push harder.
- Universe is hardcoded `TOP_25`, survivorship-flagged not -corrected — don't solve survivorship in V3.2 (decorrelated-universe rebuild is parked as V3.2b). Gold (GLD) is the residual sleeve, **not** a universe member.
- Use writing-plans, then implement TDD with frequent commits (the V3.1 plan in `docs/plans/` is the granularity template).
