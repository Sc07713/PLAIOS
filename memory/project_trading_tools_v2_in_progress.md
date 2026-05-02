---
name: trading-tools V2 — code complete, ingest+baseline+closeout pending
description: V2 strategy register + harness + 11 strategies all built and tested 2026-05-02; need IB ingest, 251 baseline runs, then docs/notebook/push to finish
type: project
originSessionId: f7943455-e60e-4ac8-9d10-15a64ba1e70d
---
V2 build is ~95% code-complete on `D:\Plaios-tools\trading-tools\` master branch (35 of 37 plan tasks committed). Sc07713/trading-tools is unaware — not pushed yet.

**What's built and tested (63 tests passing):**
- Phase 1 — TOP_25 universe, `--since` flag, exponential-backoff retry on IB pacing
- Phase 2 — strategies table + `db.upsert_strategy` + `@register` decorator + `spy_buy_hold`/`asset_buy_hold`
- Phase 3 — test DB isolation (`trading_data_test`), `backtest_runs`/`backtest_results` tables, reproducibility (git_sha/dirty/data_as_of), stats (CAGR/Sharpe/DD/IR), 3-way benchmarks, harness core (run_backtest/list_runs/load_result/set_verdict/compare), CLI subcommands
- Phase 4 — plotting (3 plotly + 2 mpl + summary.html stitcher) + chart deps in pyproject
- Phase 5 — `_base.py` indicator primitives (PipBoy BB, SMA, EMA, ATR, rolling) + `bb_meanrev` + `bb_squeeze`
- Phase 6 — 7 more strategies: `ma_cross`, `engulfing`, `hammer`, `star`, `three_soldiers_crows`, `double_top_bottom`, `high_52w_breakout`
- Task 31 — `run_baseline.py` driver

**What's pending (next session):**
- Task 4 — full IB ingest of all 25 TOP_25 symbols + VIX (~25 min). Note: prod `trading_data` is empty (V1 conftest pre-isolation wiped it during this session's V1 test runs); so ingest needs all 25 symbols, not the 23 the plan assumed.
- Task 32 — V2 baseline (251 backtests via `python -m trading_tools.backtest.run_baseline`, ~5-15 min). Requires Task 4 first.
- Tasks 33-37 — Phase 8 closeout: notebook, docs/strategies.md, project-state + decisions.md, push to GitHub `master` (NOT `main` — the plan's Task 36 says `main` but the actual branch is `master`), update PLAIOS memory file (split V1 entry → V1+V2 entries).

**Plan deviations to remember:**
- Branch is `master` not `main` (plan said `main`)
- Two stats.py test fixes: CAGR test tolerance loosened to abs=5e-3 (366-day leap-year span vs 365.25 days/year is ~0.3% noise); Sharpe `s == 0` check changed to `abs(s) < 1e-12` (handles float-noise variance)
- bb_squeeze test reduced squeeze_lookback from 120 to 80 and switched to perfectly-flat closes (zero-width BB) so 130 bars are enough for the rolling quantile
- hammer test had to add the `wick_to_body_ratio` param explicitly (plan test was missing it)
- double_top_bottom rewritten with "near-low touched ≥2 times in lookback" heuristic instead of plan's single-bar near_low check (plan version never fires); test added 8-bar warmup prefix
- pyarrow installed early (Phase 4 dep, but harness needs it for parquet writes in Phase 3 tests)
- `trading_data_test` Postgres DB created during Task 9
- Harness `_ensure_strategy_imported` does `importlib.reload` if module already imported but REGISTRY cleared — needed because test_register_decorator's autouse fixture clears REGISTRY between tests

**Files:** plan at `D:\PLAIOS\docs\superpowers\plans\2026-05-01-trading-tools-v2.md`, spec at `D:\PLAIOS\docs\superpowers\specs\2026-05-01-trading-tools-v2-design.md`. Repo at `D:\Plaios-tools\trading-tools\`.
