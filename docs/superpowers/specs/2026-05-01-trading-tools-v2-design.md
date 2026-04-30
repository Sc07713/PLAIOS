# trading-tools V2 — Strategy Register + Backtest Harness Design

**Date:** 2026-05-01
**Owner:** Scott McKennie
**Repo:** `D:\Plaios-tools\trading-tools\` (continuation of V1; GitHub `Sc07713/trading-tools`)
**Agent identity:** Cybernetic Trader-Analyst v4 (`CLAUDE.md` at repo root)
**Predecessor:** [V1 — Data Substrate](2026-04-29-trading-tools-v1-design.md) (complete; 22K+ equity bars + 6K+ index bars in Postgres `trading_data` for SPY/NVDA/VIX over 20Y)
**Reference work surfaced during brainstorm:**
- VWEMA-BB Momentum (Pine v5) — `D:\PLAIOS\domains\trading\legacy\algos\VWEMA-BB-momentum-strategy.pine`
- PipBoy V2 (MQL4 EA — multi-indicator points-scoring confluence engine) — `D:\OneDrive\Development\Personal\MQL4\PipBoy-{EURUSD,NAS100,US500,XPDUSD}-V2.mq4`

## Goal

Build a strategy register and backtest harness on top of V1's data substrate. Validate the harness against three known-answer cases (SPY-BH ≈ SPY total return, NVDA-BH ≈ NVDA total return, deterministic re-run produces identical equity curves). Ship 11 seed strategies — most are folklore or contested-edge candidates — with their results honestly reported per the v4 prompt's pedagogical directive.

V2 is **not** a portfolio optimizer, not a real-time signal engine, not an options modeller. It is the smallest useful next step: a queryable, reproducible record of what was tested, what was found, and what was decided.

## Why

Per the v4 prompt:

> *"Strategy design-test-store loop ... most strategies die in Phase 3 — that's success, not failure. The goal is finding real edge, not generating activity."*
> *"Test the test — when writing a backtest, verify the harness on a known case (e.g., buy-and-hold SPY) before trusting strategy results."*
> *"Smallest useful next step. Build what's needed for the current question."*

V1 put honest market data in a queryable store. V2 puts honest *strategy results* in a queryable store, with full audit trail (signal-level, trade-level, code-version-level) and forced-cite-the-source registration. Every subsequent phase (V2.5 fundamentals, V3 options/PipBoy port, V4 ESG falsification) consumes V2's tables without modifying them.

## Universal Design Rules (load-bearing across all phases)

These are not features — they are the substrate every strategy lives inside.

1. **Three-way benchmark, every run.** Every backtest result reports `{strategy, SPY-BH, asset-BH}` over the same period. SPY-BH is the universal cheapest-alternative benchmark; asset-BH is the buy-and-hold of the underlying instrument the strategy traded. Both stored in `backtest_results`.
2. **Cite-the-source at registration.** A strategy cannot be registered without `edge_status` ∈ `{documented, mixed_lit, folklore, falsification, contested, benchmark}` and `edge_source` (academic paper, replication study, practitioner reference, or explicitly-attributed user heuristic). Folklore patterns are explicitly classified, not silently passed off as edges.
3. **Falsification framing.** Backtest results are reported as edge / no edge / inconclusive — not as proof of anything. Most V2 strategies are expected to fail vs SPY-BH; that is the honest result of falsification.
4. **Reproducibility metadata, every run.** Each `backtest_runs` row records `git_sha`, `git_dirty`, `data_as_of`, `params`, `start_date`, `end_date`. Dirty-tree runs are flagged; deterministic re-run produces identical equity curves.
5. **Read-only safety preserved.** V2 adds zero IB-touching code. Order classes from `ib_async` remain forbidden imports.

## In Scope

- **Universe expansion** — top 25 S&P/QQQ-overlap names by market cap as of 2026-04-30, hardcoded seed list in `universe.py`
- **Ingest hardening** — `--since DATE` flag for incremental ingest; exponential-backoff retry on IB rate limits
- **Strategy register** — `strategies` DB table + `register()` Python decorator; function-based strategy interface (class escape hatch deferred until needed)
- **Backtest harness** — pure pandas/numpy; single-instrument, daily bars (weekly available, used opportunistically); long/short configurable per strategy; synthetic execution (no borrow fee, no slippage, no commissions)
- **Three-way benchmark machinery** — every result reports {strategy, SPY-BH, asset-BH}
- **Reproducibility plumbing** — `backtest_runs` (BIGSERIAL run_id, git_sha, data_as_of, params), `backtest_results` (3 rows per run — one per benchmark)
- **Per-run artifacts** — `runs/<id>/{trades,signals,equity_curve}.parquet` + `summary.json` + 3 Plotly HTML charts + 2 matplotlib PNGs + `summary.html`
- **Verdict + decision recording** — DB columns + CLI command to capture review outcomes per the v4 design-test-store loop
- **11 seed strategies** (see Appendix A for full table with citations)
- **Two consumer surfaces** — CLI (`backtest`, `list-runs`, `show-run`, `compare`, `verdict`) and Jupyter notebook (`notebooks/explore.ipynb`); same harness, no duplication
- **Visualisation** — 3 Plotly interactive (equity curve, drawdown, trades) + 2 matplotlib PNG (returns distribution, monthly heatmap); `summary.html` stitches them; CDN-loaded plotly.js for sane file size

## Explicitly Out of Scope

| Deferred to | Why |
|---|---|
| **V2.5** — Fundamentals substrate (IB `reqFundamentalData` or Yahoo); enables weak-fundamentals short (Novy-Marx 2013, Asness/Frazzini/Pedersen 2019) | Each substrate gets its own brainstorm-design-build cycle; cramming creates 4 partial substrates instead of 1 complete harness |
| **V2.6** — IPO calendar + float substrate (Polygon paid tier likely); enables low-float / hot-IPO short (Ritter 1991, Loughran & Ritter 1995) | Same |
| **V3** — Options chains + IV rank + Greeks; replaces synthetic shorts with put-options shorts (defined risk per user preference) | Options modelling is a deep rabbit hole; clean separation lets V2's strategy register stay unchanged when V3 swaps the execution layer |
| **V3** — VWEMA-BB Pine port (anchor strategy from V1 spec) | Multi-timeframe + TTM Squeeze + tiered exits = own project tier alongside PipBoy port |
| **V3** — PipBoy V2 confluence-engine port (13 indicators, points-scoring) | 2,041 lines of MQL4; standalone V3 effort |
| **V3+** — True portfolio-level / cross-sectional strategies (e.g., 12-1 momentum, value/quality factor sorts) | Top-25 universe is too small for cross-sectional signal; expand universe + add ranking machinery in V3 |
| **V4** — ESG / board-composition data substrate; enables DEI/ESG falsification test (Friede 2015 vs Bebchuk & Tallarita 2022 — contested hypothesis) | Paid data sources; honest expectation is noisy/inconclusive results requiring careful regime + size-effect controls |
| **V4+** — Order placement | Forbidden by import discipline; never V2 |
| Strategy DSL / config-only strategies | Earns its keep when non-coders write strategies; not now |
| `vectorbt` / heavyweight backtest libraries | KISS: V2's strategies are simple enough that library machinery is a liability, not an asset; reversible if we hit a wall |
| Web dashboard / Streamlit / Dash | `summary.html` + notebook + CLI is enough for V2; bigger lift earns entry when actually needed |
| Persistent run-cache via input-hash `run_id` | Over-engineered for V2 scale; auto-increment `BIGSERIAL` is enough; query-the-table caching is one-liner if ever needed |
| Garbage collection of `runs/` | At ~1-2MB per run, 1000 runs = 1-2GB. Add `cleanup-runs --older-than 90d` when it actually matters |
| `strategies_history` audit table | Git history of `strategies/` is the audit trail |

## Decisions Locked In

| # | Decision | Choice | Rationale |
|---|---|---|---|
| 1 | Backtest engine | Roll-your-own pandas + numpy | KISS aligned with V1; full control over 3-way benchmark; vectorbt's portfolio machinery is speculative generality at V2 scale |
| 2 | Strategy interface | Function `signal(df, params) -> DataFrame` returning {entry_long, entry_short, exit_long, exit_short} + optional indicator-state columns | Stateless = easy to test; class escape hatch added only when a strategy needs state (V3+) |
| 3 | Strategy registration | DB row (`strategies` table) + Python `@register(...)` decorator that upserts the row | DB row makes register queryable; decorator enforces metadata at registration time; ON CONFLICT DO UPDATE keeps current state in sync with code |
| 4 | Direction semantics | `direction ∈ {'long', 'short', 'long_short'}` per strategy | Honest — bearish patterns can short, not just exit; matches user's intention to test both sides |
| 5 | Short execution (V2) | Synthetic short on stock; **all symbols assumed shortable**; no borrow fee, no slippage, no commissions | V2 measures signal edge; V3 swaps execution to put-spreads (defined risk) without touching the strategy register |
| 6 | Position sizing | Starting capital = `$10,000` per backtest. Each entry signal allocates 100% of current equity to the position. One position at a time per (symbol, strategy). | Simplest honest baseline; only relative returns vs benchmark matter; pyramiding/Kelly deferred until needed |
| 7 | Bar timing | Entry on next bar's open after signal fires; exit on next bar's open after exit signal | Avoids look-ahead bias |
| 7b | Bar adjustment basis | Adjusted bars (`adjusted=true`) for return computation; unadjusted bars for level-based signals (e.g., 52w-high breakout uses unadjusted highs). Strategy declares which it needs. | v4 prompt rule: adjusted for returns, unadjusted for level-based signals; NVDA splits make this load-bearing |
| 8 | `run_id` shape | `BIGSERIAL` integer | Earlier hash-based design rejected as over-engineered; integers are friendlier in CLI and notebooks |
| 9 | Code reproducibility | `git_sha = git rev-parse HEAD`, `git_dirty = working tree status`, stored verbatim | One git command; warning logged when dirty |
| 10 | Data versioning | `data_as_of = max(ingested_at)` of bars used in run | Replaces hash; same audit value |
| 11 | Three-way benchmark | Every run computes strategy + SPY-BH + asset-BH; all 3 stored in `backtest_results` | Universal rule per user direction 2026-04-30; prevents "looks good" results that lose to passive holding |
| 12 | Bollinger band primitive | 20-period, 2-stddev; lower band = SMA(LOW) − 2×stddev(LOW), upper band = SMA(HIGH) + 2×stddev(HIGH) | Extracted from PipBoy V2 (`PipBoy-US500-V2.mq4` line 1716, 1723); deviation from textbook (which uses CLOSE) preserves user's reference baseline for V3 PipBoy port |
| 13 | Universe size | Top 25 names by market cap, S&P/QQQ overlap | Big enough to detect pattern hit-rate; small enough to ingest in ~17 min; cross-sectional strategies need wider universe (V3) |
| 14 | Universe maintenance | Hardcoded seed list as of 2026-04-30 | "Biggest *today*" — survivorship bias acknowledged and flagged in harness output, not pretended-solved |
| 15 | Visualisation stack | 3 Plotly HTML (equity, drawdown, trades) + 2 matplotlib PNG (returns dist, monthly heatmap); `summary.html` stitches all 5 inline | Plotly only where pan/zoom + hover earn keep; PNG where static is natural; CDN-loaded plotly.js keeps file size ~200KB-1MB per run |
| 16 | Verdict workflow | DB columns `verdict`, `decision`, `decision_note`, `reviewed_at` on `backtest_runs`; CLI `verdict <run_id> --verdict ... --decision ... --note ...` | Encodes v4 prompt's design-test-store-loop Phase 4 in queryable form |
| 17 | Notebook surface | `notebooks/explore.ipynb` imports harness; harness logic does NOT live in notebook | Strategies + harness as Python modules = testable + reproducible; notebook is a consumer |
| 18 | Strategy file granularity | One file per strategy in `strategies/`; helpers in `_base.py` | Acceptable repetition over premature abstraction; each strategy is independently scannable |
| 19 | Test database isolation | V2 creates separate `trading_data_test` DB to fix V1's known issue (tests share production DB) | Fixes V1's known-gaps item; production data no longer wiped by `pytest` |

## Architecture

### Repo extension (V1 modules untouched, V2 additions only)

```
D:\Plaios-tools\trading-tools\
├── trading_tools\
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py                      # V1 + V2 subcommands: backtest, list-runs, show-run, compare, verdict
│   ├── db.py                       # V1 + V2 query/upsert helpers for new tables
│   ├── ib_data.py                  # V1, untouched (+ retry/backoff added in Phase 1)
│   ├── schema.sql                  # V1 tables + V2 additions (strategies, backtest_runs, backtest_results)
│   ├── universe.py                 # V2 NEW — TOP_25 seed list + lookup helpers
│   ├── strategies\                 # V2 NEW
│   │   ├── __init__.py             # REGISTRY dict + register() decorator + StrategyMeta dataclass
│   │   ├── _base.py                # signal-fn protocol; primitives: bollinger_bands, sma, ema, atr, rolling_high, rolling_low
│   │   ├── spy_buy_hold.py         # universal benchmark
│   │   ├── asset_buy_hold.py       # auto-applied per-asset benchmark
│   │   ├── ma_cross.py             # NVDA 50/200-DMA
│   │   ├── bb_meanrev.py           # BB mean-reversion (PipBoy 20/2 high-low primitive)
│   │   ├── bb_squeeze.py           # BB squeeze → directional breakout
│   │   ├── engulfing.py            # bullish/bearish engulfing
│   │   ├── hammer.py               # hammer / hanging-man
│   │   ├── star.py                 # morning / evening star
│   │   ├── three_soldiers_crows.py # three white soldiers / three black crows
│   │   ├── double_top_bottom.py    # double-top / double-bottom (Bulkowski definition)
│   │   └── high_52w_breakout.py    # 52-week-high momentum (George & Hwang 2004)
│   └── backtest\                   # V2 NEW
│       ├── __init__.py
│       ├── harness.py              # run_backtest, list_runs, load_result, set_verdict, compare
│       ├── benchmarks.py           # 3-way comparison machinery
│       ├── stats.py                # CAGR, Sharpe, max DD, win rate, profit factor, IR, beat-rate
│       ├── reproducibility.py      # git_sha, git_dirty, data_as_of capture
│       └── plots.py                # 3 Plotly + 2 mpl PNG generators; summary.html stitcher
├── notebooks\                      # V2 NEW
│   └── explore.ipynb               # imports harness; iteration patterns from §3 of design
├── runs\                           # V2 NEW (gitignored)
│   └── <run_id>\
│       ├── trades.parquet
│       ├── signals.parquet
│       ├── equity_curve.parquet
│       ├── summary.json
│       ├── charts\
│       │   ├── equity_curve.html   # Plotly
│       │   ├── drawdown.html       # Plotly
│       │   ├── trades.html         # Plotly with BB overlays + entry/exit markers + hover
│       │   ├── returns_dist.png    # mpl
│       │   └── monthly_heatmap.png # mpl
│       └── summary.html            # stitches all 5 + stats table + decision note
├── tests\
│   ├── conftest.py                 # uses TEST_DATABASE_URL → trading_data_test
│   ├── test_db.py                  # V1
│   ├── test_smoke.py               # V1
│   ├── test_universe_seed.py       # V2 NEW
│   ├── test_register_decorator.py  # V2 NEW
│   ├── test_strategies.py          # V2 NEW — per-strategy unit tests on hand-crafted DataFrames
│   ├── test_harness.py             # V2 NEW — SPY-BH validation, NVDA-BH validation, run_id monotonicity
│   ├── test_reproducibility.py     # V2 NEW — same params = identical equity curve
│   └── test_plots.py               # V2 NEW — smoke (files exist, non-empty)
├── docs\
│   ├── project-state.md            # updated each session
│   ├── decisions.md                # append-only
│   └── strategies.md               # V2 NEW — one-pager per registered strategy
├── pyproject.toml                  # V2 adds: matplotlib, mplfinance, plotly, jupyter
└── ...
```

### Schema additions (applied by `db.init_schema()`)

```sql
-- V2.1 — strategy register
CREATE TABLE IF NOT EXISTS strategies (
    name           TEXT PRIMARY KEY,
    module         TEXT NOT NULL,                -- 'trading_tools.strategies.bb_squeeze'
    description    TEXT NOT NULL,
    direction      TEXT NOT NULL,                -- 'long' | 'short' | 'long_short'
    edge_status    TEXT NOT NULL,                -- see Universal Design Rule #2
    edge_source    TEXT,                         -- citation; nullable only for benchmark strategies
    default_params JSONB NOT NULL DEFAULT '{}',
    asset_classes  TEXT[] NOT NULL,              -- ['equity'] etc.
    timeframes     TEXT[] NOT NULL,              -- ['daily'] etc.
    registered_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- V2.2 — backtest run record
CREATE TABLE IF NOT EXISTS backtest_runs (
    run_id         BIGSERIAL PRIMARY KEY,
    strategy       TEXT NOT NULL REFERENCES strategies(name),
    symbol         TEXT NOT NULL REFERENCES instruments(symbol),
    start_date     DATE NOT NULL,
    end_date       DATE NOT NULL,
    timeframe      TEXT NOT NULL,
    direction      TEXT NOT NULL,
    params         JSONB NOT NULL,
    git_sha        TEXT NOT NULL,
    git_dirty      BOOLEAN NOT NULL,
    data_as_of     TIMESTAMPTZ NOT NULL,
    duration_ms    INTEGER,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    artifact_dir   TEXT NOT NULL,
    -- review fields, NULL until reviewed:
    verdict        TEXT,                         -- 'edge' | 'no_edge' | 'inconclusive' | 'benchmark'
    decision       TEXT,                         -- 'shelf' | 'iterate' | 'promote' | 'benchmark'
    decision_note  TEXT,
    reviewed_at    TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS backtest_runs_strategy_idx ON backtest_runs(strategy, created_at DESC);
CREATE INDEX IF NOT EXISTS backtest_runs_symbol_idx   ON backtest_runs(symbol,   created_at DESC);

-- V2.3 — per-run benchmark results (3 rows per run: strategy / spy_bh / asset_bh)
CREATE TABLE IF NOT EXISTS backtest_results (
    run_id          BIGINT NOT NULL REFERENCES backtest_runs(run_id) ON DELETE CASCADE,
    benchmark       TEXT NOT NULL,               -- 'strategy' | 'spy_bh' | 'asset_bh'
    cagr            NUMERIC(10,6),
    sharpe          NUMERIC(10,6),
    max_drawdown    NUMERIC(10,6),
    total_return    NUMERIC(10,6),
    n_trades        INTEGER,
    win_rate        NUMERIC(10,6),
    profit_factor   NUMERIC(10,6),
    -- relative-to-benchmark fields populated for benchmark='strategy' only:
    excess_return_vs_spy_bh   NUMERIC(10,6),
    info_ratio_vs_spy_bh      NUMERIC(10,6),
    excess_return_vs_asset_bh NUMERIC(10,6),
    info_ratio_vs_asset_bh    NUMERIC(10,6),
    PRIMARY KEY (run_id, benchmark)
);
```

### Strategy interface (Python)

```python
# trading_tools/strategies/__init__.py
from dataclasses import dataclass
from typing import Callable, Literal
import pandas as pd

REGISTRY: dict[str, "StrategyMeta"] = {}

@dataclass(frozen=True)
class StrategyMeta:
    name: str
    fn: Callable[[pd.DataFrame, dict], pd.DataFrame]
    description: str
    direction: Literal['long', 'short', 'long_short']
    edge_status: Literal['documented', 'mixed_lit', 'folklore', 'falsification', 'contested', 'benchmark']
    edge_source: str | None
    default_params: dict
    asset_classes: list[str]
    timeframes: list[str]

def register(name: str, **meta) -> Callable:
    """Decorator. Adds the function + meta to REGISTRY and upserts the strategies row."""
    def decorator(fn):
        REGISTRY[name] = StrategyMeta(name=name, fn=fn, **meta)
        # upsert into DB happens lazily on first use, or eagerly on import via db.upsert_strategy(REGISTRY[name])
        return fn
    return decorator
```

A strategy:

```python
# trading_tools/strategies/bb_squeeze.py
import pandas as pd
from . import register
from ._base import bollinger_bands

@register(
    name='bb_squeeze',
    description="Long when BB width contracts (squeeze) then breaks above the upper band; "
                "short on inverse. Hypothesis: low-vol compression precedes directional expansion.",
    direction='long_short',
    edge_status='falsification',
    edge_source='Bollinger 1993 (primitive); PipBoy V2 (signal recipe). '
                'Marshall et al. 2008 found breakout strategies generally fail randomness tests.',
    default_params={'period': 20, 'stddev': 2.0, 'squeeze_lookback': 120},
    asset_classes=['equity'],
    timeframes=['daily'],
)
def signal(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    """df: OHLCV with DatetimeIndex.
    Returns DataFrame with REQUIRED bool cols {entry_long, entry_short, exit_long, exit_short}
    plus OPTIONAL indicator-state cols (bb_upper, bb_middle, bb_lower, width, in_squeeze, ...)."""
    bb = bollinger_bands(df, period=params['period'], stddev=params['stddev'])
    width = bb['upper'] - bb['lower']
    in_squeeze = width <= width.rolling(params['squeeze_lookback']).quantile(0.20)
    breakout_up   = (df['close'] > bb['upper']) & in_squeeze.shift(1).fillna(False)
    breakout_down = (df['close'] < bb['lower']) & in_squeeze.shift(1).fillna(False)
    return pd.DataFrame({
        'entry_long':  breakout_up,
        'entry_short': breakout_down,
        'exit_long':   df['close'] < bb['middle'],
        'exit_short':  df['close'] > bb['middle'],
        'bb_upper':    bb['upper'],
        'bb_middle':   bb['middle'],
        'bb_lower':    bb['lower'],
        'width':       width,
        'in_squeeze':  in_squeeze,
    }, index=df.index)
```

### Backtest harness API

```python
# trading_tools/backtest/harness.py

def run_backtest(
    strategy: str, symbol: str, start: date | str, end: date | str, *,
    timeframe: str = 'daily',
    params: dict | None = None,           # None → use strategy's default_params
    direction_override: str | None = None, # None → use strategy's direction
) -> Result:
    """End-to-end: load bars → call signal_fn → walk signals → compute trades + equity →
    compute 3-way benchmark stats → persist row + parquets + charts → return Result."""

def list_runs(
    strategy: str | None = None, symbol: str | None = None,
    since: date | None = None, verdict: str | None = None,
) -> pd.DataFrame:
    """Return runs filtered by strategy/symbol/since/verdict, latest first."""

def load_result(run_id: int) -> Result:
    """Reload a previously-computed run from DB + parquets, no recomputation."""

def set_verdict(run_id: int, *, verdict: str, decision: str, note: str) -> None:
    """Record the v4 design-test-store loop Phase 4 outcome."""

def compare(run_id_a: int, run_id_b: int) -> pd.DataFrame:
    """Side-by-side stats diff."""
```

### Data flow (one backtest run)

```
1. CLI / notebook calls harness.run_backtest('bb_squeeze', 'NVDA', '2010-01-01', '2026-04-29')
2. Resolve strategy from REGISTRY → fn + default_params
3. Load adjusted daily bars from equity_bars via db.query
4. Capture data_as_of = max(ingested_at) of returned bars
5. Capture git_sha = `git rev-parse HEAD`; git_dirty = `git status --porcelain` is non-empty
6. Call signal_fn(df, params) → returns full signals DataFrame (required + optional cols)
7. Walk signals → trade ledger using next-bar-open execution; one position at a time
8. Compute strategy equity curve from trades
9. Compute SPY-BH equity curve over same period (load SPY bars; reinvested holding)
10. Compute asset-BH equity curve (same logic, instrument-specific)
11. stats.compare_three_way(strategy, spy_bh, asset_bh) → CAGR/Sharpe/MaxDD + relative metrics
12. INSERT INTO backtest_runs RETURNING run_id  (run_id allocated by BIGSERIAL)
13. INSERT 3 rows INTO backtest_results
14. Write runs/<run_id>/{trades,signals,equity_curve}.parquet + summary.json
15. plots.generate_all(result) → 3 Plotly HTMLs + 2 PNGs + summary.html
16. Return Result object
```

## Implementation Phases

Each phase is independently testable + reversible. Commit after each phase.

### Phase 1 — Data expansion + ingest hardening
- `universe.py` with `TOP_25` hardcoded list (S&P/QQQ overlap by market cap as of 2026-04-30)
- `--since DATE` flag in `cli.ingest`
- Exponential-backoff retry on IB rate limit errors (max 3 retries, base 10s)
- New tests: `test_universe_seed`, `test_incremental_ingest`
- Run full ingest: 22 new symbols × 4 variants ≈ 17 min
- **Reversibility:** `TRUNCATE equity_bars WHERE symbol NOT IN ('SPY','NVDA')` + `git revert`
- **Commit:** `data: top-25 universe + incremental ingest`

### Phase 2 — Strategy register infrastructure
- `strategies/__init__.py` with `REGISTRY` + `StrategyMeta` + `register()` decorator
- `strategies` table in `schema.sql`
- `db.upsert_strategy()` helper
- `spy_buy_hold.py` + `asset_buy_hold.py` (the two benchmark strategies)
- Tests: `test_register_decorator`
- **Reversibility:** `DROP TABLE strategies` + remove `strategies/` dir
- **Commit:** `strategies: register decorator + benchmark strategies`

### Phase 3 — Backtest harness
- `backtest/{harness,stats,benchmarks,reproducibility}.py`
- `backtest_runs` + `backtest_results` tables
- CLI subcommands: `backtest`, `list-runs`, `show-run`, `compare`, `verdict`
- **Test the test:**
  - `test_spy_bh_reproduces_spy_total_return` — within 0.5% of manual `(close_last/close_first)-1`
  - `test_asset_bh_matches_for_nvda` — same for NVDA
  - `test_run_id_monotonic` — same backtest twice → distinct run_ids
- `tests/conftest.py` switch to `TEST_DATABASE_URL → trading_data_test` (fixes V1 known-gap)
- **Reversibility:** `DROP TABLE backtest_runs, backtest_results CASCADE` + remove `backtest/` dir
- **Commit:** `backtest: harness + 3-way benchmark + reproducibility`

### Phase 4 — Plotting + summary HTML
- `backtest/plots.py` with: 3 Plotly (equity_curve, drawdown, trades) + 2 mpl PNG (returns_dist, monthly_heatmap) + `summary.html` stitcher
- `pyproject.toml` adds `plotly`, `mplfinance` (matplotlib transitive)
- Hook into `harness.run_backtest` so charts auto-generate
- Tests: `test_plots_smoke`
- **Reversibility:** `git revert`; `runs/` is gitignored
- **Commit:** `backtest: plotting + summary HTML`

### Phase 5 — BB strategies (harness validation)
- `_base.py` with: `bollinger_bands(df, period, stddev, source_low='low', source_high='high')` (PipBoy primitive), `sma`, `ema`, `atr`, `rolling_high`, `rolling_low`
- `bb_meanrev.py` + `bb_squeeze.py` per Architecture
- Tests: hand-crafted DataFrame with known squeeze/breakout events; assert signal columns fire on expected bars
- Eyeball `summary.html` for SPY + NVDA + 3 other names; confirm trade markers land where logic predicts
- **Commit:** `strategies: BB mean-reversion + BB squeeze (PipBoy primitive)`

### Phase 6 — Remaining 8 seed strategies
- `ma_cross.py` (NVDA 50/200-DMA, golden/death cross)
- `engulfing.py`, `hammer.py`, `star.py`, `three_soldiers_crows.py` (4 candlestick patterns)
- `double_top_bottom.py` (Bulkowski definition: 5%+ correction between peaks)
- `high_52w_breakout.py` (George & Hwang 2004 — close > rolling 252-day high)
- Each with one unit test + smoke run on 2-3 symbols
- **Commits:** likely 3 — `strategies: MA cross`, `strategies: candlesticks`, `strategies: chart patterns + 52w-high`

### Phase 7 — V2 baseline run
- Run baseline:
  - `spy_buy_hold` on SPY only — 1 run
  - `asset_buy_hold` on every universe symbol — 25 runs
  - 9 active strategies × 25 universe symbols — 225 runs
  - **Total: 251 backtest runs → 753 rows in `backtest_results`** (3 benchmarks × 251)
- Eyeball results for harness anomalies (e.g., suspicious total returns might indicate look-ahead)
- Set initial verdict + decision on each via CLI
- **Commit:** `v2 baseline: 251 runs across 11 strategies × 25 symbols, initial verdicts`

### Phase 8 — V2 closeout
- `notebooks/explore.ipynb` with the iteration patterns (loop strategies, sweep params, audit history)
- `docs/strategies.md` one-pager per registered strategy: hypothesis, edge status, citation, baseline result
- `docs/project-state.md` updated to V2-complete
- Append decisions to `docs/decisions.md` (one entry per locked decision in this spec)
- Push to GitHub
- Update PLAIOS memory: project entry pointing to V2 spec + repo
- **Commit:** `docs + notebook: V2 closeout`

## Reproducibility

Per v4 prompt: *"Every backtest run is logged with parameters, code version, and timestamp. Results without reproducibility metadata are anecdotes."*

V2 captures:
- `git_sha` — exact strategy code at run time (git ls-files-based; falls back to HEAD)
- `git_dirty` — flags non-reproducible runs (working tree had uncommitted changes)
- `data_as_of` — bar version snapshot (max ingested_at of bars used)
- `params` — full parameter set used
- `created_at` — when the run executed
- `duration_ms` — runtime (for performance regression tracking)

To reproduce a run:
1. `git checkout <git_sha_of_run>`
2. Re-ingest bars to get `ingested_at <= data_as_of` state (or accept newer bars; data_as_of just records what we had)
3. Re-run with same `(strategy, symbol, start, end, params)`
4. Compare equity curves bit-for-bit (modulo float rounding)

## Success Criteria

1. `python -m trading_tools backtest --strategy spy_buy_hold --symbol SPY --start 2010-01-01 --end 2026-04-29` runs end-to-end; reported total return matches SPY's manual `(close_last/close_first)-1` within 0.5%
2. `python -m trading_tools backtest --strategy bb_squeeze --symbol NVDA --start 2010-01-01 --end 2026-04-29` runs end-to-end; produces all 5 chart files + summary.html in `runs/<id>/charts/`
3. `python -m trading_tools list-runs` returns ≥251 rows after Phase 7
4. `SELECT COUNT(*) FROM backtest_runs WHERE git_dirty = false;` returns ≥251 (all baseline runs reproducible)
5. `SELECT COUNT(*) FROM backtest_results;` returns ≥753 (3 benchmark rows × 251 runs)
6. `notebooks/explore.ipynb` re-runs end-to-end without kernel errors
7. `pytest` passes: V1 tests + new V2 tests, against `trading_data_test` DB (does NOT touch production data)
8. `docs/strategies.md` exists with one entry per registered strategy
9. `docs/project-state.md` reflects V2-complete state
10. PLAIOS memory updated

## Reversibility

| Phase | Undo |
|---|---|
| 1 | `TRUNCATE equity_bars WHERE symbol NOT IN ('SPY','NVDA')`; `git revert` |
| 2 | `DROP TABLE strategies`; remove `strategies/` |
| 3 | `DROP TABLE backtest_runs, backtest_results CASCADE`; remove `backtest/` |
| 4 | `git revert`; charts in `runs/` are gitignored |
| 5-6 | Remove individual strategy files (their REGISTRY entries vanish on next import) |
| 7 | Drop `runs/` directory + `TRUNCATE backtest_runs CASCADE` |
| 8 | `git revert`; pop GitHub push |

DB drops are gated on user confirmation; never automated.

---

## Appendix A — Seed strategy table (Phase 5-6)

| # | name | direction | edge_status | edge_source |
|---|---|---|---|---|
| 1 | `spy_buy_hold` | long | benchmark | Universal benchmark — see Universal Design Rule #1 |
| 2 | `asset_buy_hold` | long | benchmark | Per-asset benchmark — see Universal Design Rule #1 |
| 3 | `ma_cross` (NVDA 50/200) | long_short | folklore | Practitioner folklore ("golden cross", "death cross"); no consistent academic edge |
| 4 | `bb_meanrev` (PipBoy 20/2 high-low) | long_short | falsification | Bollinger 1993 (primitive); standalone BB mean-reversion typically fails randomness tests outside specific regimes |
| 5 | `bb_squeeze` (PipBoy 20/2 high-low + 120-bar squeeze quantile) | long_short | falsification | Bollinger 1993 (primitive); PipBoy V2 (signal recipe); Marshall et al. 2008 found breakout strategies generally fail randomness tests |
| 6 | `engulfing` (bullish/bearish) | long_short | mixed_lit | Marshall, Young & Rose 2006 ("Candlestick technical trading strategies: Can they create value for investors?", *Journal of Banking & Finance*) — weak edge in some markets |
| 7 | `hammer` / hanging-man | long_short | folklore | Bulkowski, *Encyclopedia of Candlestick Charts*; weak/decayed edge in tested patterns |
| 8 | `star` (morning/evening) | long_short | mixed_lit | Marshall et al. 2006; Bulkowski |
| 9 | `three_soldiers_crows` | long_short | folklore | Bulkowski; common practitioner pattern, weak academic support |
| 10 | `double_top_bottom` (Bulkowski 5%+ correction) | long_short | folklore | Bulkowski (*Encyclopedia of Chart Patterns*) found marginal edge with strict definition |
| 11 | `high_52w_breakout` | long | documented | George & Hwang 2004 ("The 52-Week High and Momentum Investing", *Journal of Finance*) — stocks near 52w highs continue outperforming |

## Appendix B — PipBoy V2 BB primitive (extracted from MQL4 source)

From `D:\OneDrive\Development\Personal\MQL4\PipBoy-US500-V2.mq4`:

```mql4
// line 1716
return iBands(NULL, timePeriod, 20, 2, 0, PRICE_LOW,  MODE_LOWER, shift);
// line 1723
return iBands(NULL, timePeriod, 20, 2, 0, PRICE_HIGH, MODE_UPPER, shift);
```

**Decoding:** standard 20-period, 2-stddev Bollinger Bands; **deviation from textbook**: lower band uses `PRICE_LOW`, upper band uses `PRICE_HIGH` (textbook uses `PRICE_CLOSE` for both). Tighter envelope around bar extremes.

V2's `bollinger_bands(df, period=20, stddev=2.0, source_low='low', source_high='high')` reproduces this:

```python
def bollinger_bands(df, period=20, stddev=2.0,
                    source_low='low', source_high='high'):
    sma_low  = df[source_low].rolling(period).mean()
    std_low  = df[source_low].rolling(period).std()
    sma_high = df[source_high].rolling(period).mean()
    std_high = df[source_high].rolling(period).std()
    return pd.DataFrame({
        'lower':  sma_low  - stddev * std_low,
        'middle': df['close'].rolling(period).mean(),
        'upper':  sma_high + stddev * std_high,
    }, index=df.index)
```

This deliberately matches PipBoy V2's primitive so that when V3 ports the full PipBoy confluence engine, the BB component is already validated against the user's historical reference baseline.

## Appendix C — Future phase pre-seeds (informational; not built in V2)

**V2.5 — Fundamentals substrate** (next after V2):
- Source: IB `reqFundamentalData` (XML; quarterly), or Yahoo as fallback
- New tables: `fundamentals_quarterly` (revenue, gross_profit, op_income, eps, shares_outstanding, etc.)
- New strategies: weak-fundamentals short (Novy-Marx 2013 quality factor; Asness/Frazzini/Pedersen 2019 quality-minus-junk)

**V2.6 — IPO/float substrate:**
- Source: Polygon paid tier (likely)
- New tables: `instrument_metadata` (ipo_date, float_shares, sector, industry)
- New strategies: low-float / hot-IPO short (Ritter 1991; Loughran & Ritter 1995 — IPOs underperform 3-year forward)

**V3 — Options + heavy strategy ports:**
- Options chains substrate (IB options or Polygon)
- IV rank/percentile per name
- Greeks computation (Black-Scholes minimum)
- Put-debit-spread executor (replaces V2's synthetic shorts)
- VWEMA-BB Pine port (anchor strategy)
- PipBoy V2 confluence-engine port

**V4 — Governance/ESG falsification:**
- ESG scores + board composition (paid: MSCI ESG, ISS, Equilar)
- Test contested hypothesis: do DEI/ESG-heavy names underperform during market drawdowns?
- Frame as falsification; expect noisy/inconclusive results requiring careful regime + size-effect controls

---

*End of V2 design spec. Next phase: writing-plans skill produces the implementation plan from this spec; implementation across multiple sessions per Phase 1-8 above.*
