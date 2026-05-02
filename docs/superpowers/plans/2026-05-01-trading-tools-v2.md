# trading-tools V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a strategy register, backtest harness, and 11 seed strategies on top of V1's data substrate at `D:\Plaios-tools\trading-tools\`. Validate the harness on three known-answer cases (SPY-BH, NVDA-BH, deterministic re-run), then run a 251-row baseline across 11 strategies × 25 universe symbols.

**Architecture:** V1 modules untouched. New `trading_tools.strategies` package (one file per strategy, `_base.py` for primitives, `__init__.py` for `REGISTRY` + `register()` decorator). New `trading_tools.backtest` package (pure pandas/numpy harness, 3-way benchmark machinery, reproducibility metadata, plotting). Two new DB tables: `strategies` (register), `backtest_runs` (one row per run), `backtest_results` (3 rows per run — strategy / spy_bh / asset_bh). Per-run artifacts to `runs/<id>/` (gitignored).

**Tech Stack:** Python 3.13, pandas, numpy, psycopg3, plotly, matplotlib, mplfinance, jupyter. No `vectorbt`. Postgres 17 (`trading_data` for V1 production, **new** `trading_data_test` for tests).

**Spec:** `D:\PLAIOS\docs\superpowers\specs\2026-05-01-trading-tools-v2-design.md` — read this before starting. V1 spec at `2026-04-29-trading-tools-v1-design.md` is the substrate.

---

## File Structure

Files this plan creates or modifies (all under `D:\Plaios-tools\trading-tools\`):

```
trading_tools/
├── schema.sql                                  # MODIFY — append V2 tables
├── db.py                                       # MODIFY — add upsert_strategy, helpers for backtest_runs/results
├── ib_data.py                                  # MODIFY — add exponential-backoff retry
├── cli.py                                      # MODIFY — add --since, backtest, list-runs, show-run, compare, verdict
├── universe.py                                 # CREATE — TOP_25 hardcoded list + lookup helpers
├── strategies/                                 # CREATE
│   ├── __init__.py                             # REGISTRY dict, StrategyMeta dataclass, register() decorator
│   ├── _base.py                                # bollinger_bands, sma, ema, atr, rolling_high, rolling_low
│   ├── spy_buy_hold.py                         # benchmark
│   ├── asset_buy_hold.py                       # benchmark
│   ├── ma_cross.py                             # 50/200 DMA
│   ├── bb_meanrev.py                           # PipBoy 20/2 high-low BB mean-reversion
│   ├── bb_squeeze.py                           # squeeze → directional breakout
│   ├── engulfing.py                            # bullish/bearish engulfing
│   ├── hammer.py                               # hammer / hanging-man
│   ├── star.py                                 # morning / evening star
│   ├── three_soldiers_crows.py                 # three white soldiers / black crows
│   ├── double_top_bottom.py                    # Bulkowski 5%+ correction definition
│   └── high_52w_breakout.py                    # George & Hwang 2004
└── backtest/                                   # CREATE
    ├── __init__.py
    ├── reproducibility.py                      # git_sha, git_dirty, data_as_of capture
    ├── stats.py                                # CAGR, Sharpe, max DD, win rate, profit factor, IR
    ├── benchmarks.py                           # 3-way comparison machinery
    ├── harness.py                              # run_backtest, list_runs, load_result, set_verdict, compare
    └── plots.py                                # 3 Plotly + 2 mpl PNG + summary.html stitcher
notebooks/
└── explore.ipynb                               # CREATE — imports harness; iteration patterns
runs/                                           # CREATE (gitignored)
tests/
├── conftest.py                                 # MODIFY — switch to TEST_DATABASE_URL
├── test_universe_seed.py                       # CREATE
├── test_register_decorator.py                  # CREATE
├── test_strategies.py                          # CREATE — per-strategy unit tests
├── test_harness.py                             # CREATE — SPY-BH/NVDA-BH validation, run_id monotonicity
├── test_reproducibility.py                     # CREATE — same params = identical equity curve
├── test_stats.py                               # CREATE — CAGR/Sharpe/DD known-answer cases
├── test_retry.py                               # CREATE — exponential-backoff unit test
└── test_plots.py                               # CREATE — smoke (files exist, non-empty)
docs/
├── project-state.md                            # MODIFY at closeout
├── decisions.md                                # MODIFY — append V2 decisions
└── strategies.md                               # CREATE — one-pager per registered strategy
.gitignore                                      # MODIFY — add runs/, .ipynb_checkpoints/
.env.example                                    # MODIFY — add TEST_DATABASE_URL
pyproject.toml                                  # MODIFY — add pandas, numpy, plotly, matplotlib, mplfinance, jupyter, pyarrow
```

**Responsibility per file:**
- `universe.py` — TOP_25 seed list. No imports from `strategies/` or `backtest/`.
- `strategies/__init__.py` — registration plumbing only. No DB calls. Strategy files import `register` from here.
- `strategies/_base.py` — pure pandas indicator primitives. No DB, no IB, no I/O.
- `strategies/<name>.py` — one file per strategy; declares `@register(...)` then `def signal(df, params) -> DataFrame`.
- `backtest/reproducibility.py` — `git_sha()`, `git_dirty()`, `data_as_of()` helpers.
- `backtest/stats.py` — pure functions: `cagr(equity)`, `sharpe(returns)`, `max_drawdown(equity)`, etc.
- `backtest/benchmarks.py` — `three_way_compare(strategy_eq, spy_bh_eq, asset_bh_eq)`.
- `backtest/harness.py` — orchestration; the only file in `backtest/` that imports from `db`, `strategies`, and `plots`.
- `backtest/plots.py` — chart generation; takes a `Result` object, writes files; no DB.

---

## Invariants (referenced throughout)

These are the contracts every task must respect. Pin them in your head.

- **Strategy fn signature:** `signal(df: pd.DataFrame, params: dict) -> pd.DataFrame`. `df` has DatetimeIndex (sorted ascending) + columns `{open, high, low, close, volume}`. Return DataFrame indexed identically with REQUIRED bool columns `{entry_long, entry_short, exit_long, exit_short}` plus OPTIONAL indicator-state columns.
- **Bollinger primitive (PipBoy variant):** `lower = SMA(low, period) − stddev × std(low, period)`; `upper = SMA(high, period) + stddev × std(high, period)`; `middle = SMA(close, period)`.
- **Position sizing:** $10,000 starting capital. Each entry signal allocates 100% of current equity. One position at a time per (symbol, strategy).
- **Bar timing:** Entry fills at `next bar's open` after signal fires. Exit fills at `next bar's open` after exit signal.
- **3-way benchmark:** every `run_backtest` writes 3 rows to `backtest_results` (`benchmark` ∈ `{strategy, spy_bh, asset_bh}`). Excess-return / info-ratio fields populated only on `benchmark='strategy'`.
- **Reproducibility metadata:** `git_sha`, `git_dirty`, `data_as_of`, `params`, `created_at`, `duration_ms` recorded on every run.
- **Read-only IB safety:** order classes (`MarketOrder`, `LimitOrder`, etc.) NEVER imported anywhere.
- **Test DB isolation:** Phase 3 onward, all tests connect to `trading_data_test` (set `TEST_DATABASE_URL` in `.env`). Production data in `trading_data` is never touched by `pytest`.

---

## Tasks

## Phase 1 — Data expansion + ingest hardening

Goal: grow the bar table from 3 symbols to 25, add `--since DATE` for incremental ingest, add exponential-backoff retry around IB rate limits.

### Task 1: Add `universe.py` with TOP_25 seed list

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\universe.py`
- Create: `D:\Plaios-tools\trading-tools\tests\test_universe_seed.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_universe_seed.py`:
```python
"""Tests for TOP_25 universe seed list."""
from datetime import date

from trading_tools.universe import TOP_25, get_meta


def test_top25_has_exactly_25_symbols():
    assert len(TOP_25) == 25
    assert len(set(TOP_25.keys())) == 25  # no dupes


def test_top25_includes_known_anchors():
    assert "SPY" in TOP_25
    assert "NVDA" in TOP_25
    assert "VIX" not in TOP_25  # index, not equity


def test_every_entry_has_required_fields():
    required = {"sec_type", "exchange", "currency", "asset_class", "first_seen"}
    for sym, meta in TOP_25.items():
        missing = required - meta.keys()
        assert not missing, f"{sym} missing fields: {missing}"
        assert isinstance(meta["first_seen"], date)
        assert meta["asset_class"] == "equity"
        assert meta["sec_type"] == "STK"


def test_get_meta_returns_dict_for_known_symbol():
    meta = get_meta("AAPL")
    assert meta["sec_type"] == "STK"
    assert meta["asset_class"] == "equity"


def test_get_meta_raises_for_unknown_symbol():
    import pytest
    with pytest.raises(KeyError, match="ZZZZ"):
        get_meta("ZZZZ")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_universe_seed.py -v`
Expected: ImportError / ModuleNotFoundError on `trading_tools.universe`.

- [ ] **Step 3: Write `universe.py`**

Create `trading_tools/universe.py`. The list contains 25 entries — full code in the spec; replicate verbatim. Each entry has `sec_type='STK'`, `currency='USD'`, `asset_class='equity'`, plus `exchange` (`NASDAQ` for all except `SPY` which is `ARCA`) and `first_seen` (IPO date). The 25 symbols: AAPL, MSFT, NVDA, GOOGL, GOOG, AMZN, META, AVGO, TSLA, COST, NFLX, AMD, PEP, ADBE, CSCO, TMUS, INTU, CMCSA, TXN, QCOM, AMGN, AMAT, ISRG, BKNG, SPY.

```python
"""Top-25 S&P/QQQ-overlap universe by market cap as of 2026-04-30.

Hardcoded seed list per V2 spec decision #14 — survivorship bias acknowledged
and flagged in harness output, not pretended-solved.
"""
from __future__ import annotations
from datetime import date

TOP_25: dict[str, dict] = {
    "AAPL":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1980, 12, 12)),
    "MSFT":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1986, 3, 13)),
    "NVDA":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1999, 1, 22)),
    "GOOGL": dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(2004, 8, 19)),
    "GOOG":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(2014, 4, 3)),
    "AMZN":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1997, 5, 15)),
    "META":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(2012, 5, 18)),
    "AVGO":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(2009, 8, 6)),
    "TSLA":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(2010, 6, 29)),
    "COST":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1985, 12, 5)),
    "NFLX":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(2002, 5, 23)),
    "AMD":   dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1983, 3, 21)),
    "PEP":   dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1972, 6, 1)),
    "ADBE":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1986, 8, 20)),
    "CSCO":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1990, 2, 16)),
    "TMUS":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(2007, 4, 19)),
    "INTU":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1993, 3, 12)),
    "CMCSA": dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1972, 6, 29)),
    "TXN":   dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1972, 6, 1)),
    "QCOM":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1991, 12, 13)),
    "AMGN":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1983, 6, 17)),
    "AMAT":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1972, 11, 1)),
    "ISRG":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(2000, 6, 13)),
    "BKNG":  dict(sec_type="STK", exchange="NASDAQ", currency="USD", asset_class="equity", first_seen=date(1999, 3, 30)),
    "SPY":   dict(sec_type="STK", exchange="ARCA",   currency="USD", asset_class="equity", first_seen=date(1993, 1, 29)),
}


def get_meta(symbol: str) -> dict:
    """Return seed metadata for `symbol`. Raises KeyError if unknown."""
    if symbol not in TOP_25:
        raise KeyError(f"unknown symbol {symbol!r} (not in TOP_25)")
    return TOP_25[symbol]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_universe_seed.py -v`
Expected: 5 passed.

- [ ] **Step 5: Wire universe into `cli.py`**

Replace V1's `KNOWN_INSTRUMENTS` with TOP_25 + VIX (kept as the only non-equity entry).

In `trading_tools/cli.py`, replace the `KNOWN_INSTRUMENTS` block with:
```python
from trading_tools.universe import TOP_25

KNOWN_INSTRUMENTS: dict[str, dict] = {
    **TOP_25,
    "VIX": dict(sec_type="IND", exchange="CBOE", currency="USD",
                asset_class="index", first_seen=date(1990, 1, 2)),
}
```

- [ ] **Step 6: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/universe.py tests/test_universe_seed.py trading_tools/cli.py
git -C D:/Plaios-tools/trading-tools commit -m "data: top-25 universe seed list"
```

---

### Task 2: Add `--since DATE` flag for incremental ingest

**Files:**
- Modify: `D:\Plaios-tools\trading-tools\trading_tools\ib_data.py`
- Modify: `D:\Plaios-tools\trading-tools\trading_tools\cli.py`
- Create: `D:\Plaios-tools\trading-tools\tests\test_incremental_ingest.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_incremental_ingest.py`:
```python
from datetime import date
from trading_tools.ib_data import duration_from_since


def test_since_within_30_days_uses_d():
    today = date(2026, 5, 1)
    assert duration_from_since(date(2026, 4, 25), today=today) == "6 D"


def test_since_within_year_uses_m():
    today = date(2026, 5, 1)
    assert duration_from_since(date(2026, 1, 21), today=today) == "4 M"


def test_since_over_year_uses_y():
    today = date(2026, 5, 1)
    assert duration_from_since(date(2024, 5, 1), today=today) == "2 Y"


def test_since_in_future_raises():
    import pytest
    today = date(2026, 5, 1)
    with pytest.raises(ValueError, match="future"):
        duration_from_since(date(2026, 5, 2), today=today)


def test_since_today_returns_minimum_1d():
    today = date(2026, 5, 1)
    assert duration_from_since(today, today=today) == "1 D"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_incremental_ingest.py -v`
Expected: ImportError on `duration_from_since`.

- [ ] **Step 3: Add `duration_from_since` to `ib_data.py`**

Append to `trading_tools/ib_data.py`:
```python
def duration_from_since(since: date, *, today: date | None = None) -> str:
    """Translate a `since` date into an IB durationStr (round UP to ensure coverage)."""
    today = today or date.today()
    if since > today:
        raise ValueError(f"since={since} is in the future relative to {today}")
    days = max(1, (today - since).days)
    if days <= 30:
        return f"{days} D"
    if days <= 365:
        months = -(-days // 30)  # ceil
        return f"{months} M"
    years = -(-days // 365)
    return f"{years} Y"
```

- [ ] **Step 4: Wire `--since` into the CLI**

In `trading_tools/cli.py`:
- Modify `ingest()` signature to accept `since: date | None = None`. When `since` is set, translate to `duration` via `ib_data.duration_from_since(since)`.
- In the argparse block, replace the bare `--duration` line with a mutually-exclusive group:
```python
group = p_ing.add_mutually_exclusive_group()
group.add_argument("--duration", default="20 Y",
                   help="IB duration string, e.g. '20 Y', '5 Y'")
group.add_argument("--since", type=lambda s: date.fromisoformat(s),
                   help="incremental: pull bars since this YYYY-MM-DD")
```
- In dispatch:
```python
if args.cmd == "ingest":
    ingest(args.symbols,
           duration=args.duration if args.since is None else "20 Y",
           since=args.since)
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/test_incremental_ingest.py -v`
Expected: 5 passed.

- [ ] **Step 6: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/ib_data.py trading_tools/cli.py tests/test_incremental_ingest.py
git -C D:/Plaios-tools/trading-tools commit -m "ingest: --since flag for incremental backfill"
```

---

### Task 3: Add exponential-backoff retry around IB rate limits

**Files:**
- Modify: `D:\Plaios-tools\trading-tools\trading_tools\ib_data.py`
- Create: `D:\Plaios-tools\trading-tools\tests\test_retry.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_retry.py`:
```python
from unittest.mock import MagicMock
import pytest

from trading_tools.ib_data import retry_on_pacing


def test_succeeds_on_first_try():
    fn = MagicMock(return_value="ok")
    assert retry_on_pacing(fn, max_retries=3, base_delay=0.01) == "ok"
    assert fn.call_count == 1


def test_retries_on_pacing_error():
    fn = MagicMock(side_effect=[
        RuntimeError("Pacing violation 162"),
        RuntimeError("Historical data request pacing 162"),
        "ok",
    ])
    assert retry_on_pacing(fn, max_retries=3, base_delay=0.01) == "ok"
    assert fn.call_count == 3


def test_gives_up_after_max_retries():
    fn = MagicMock(side_effect=RuntimeError("Pacing violation 162"))
    with pytest.raises(RuntimeError, match="Pacing"):
        retry_on_pacing(fn, max_retries=2, base_delay=0.01)
    assert fn.call_count == 3  # initial + 2 retries


def test_does_not_retry_on_non_pacing_error():
    fn = MagicMock(side_effect=ValueError("bad arg"))
    with pytest.raises(ValueError):
        retry_on_pacing(fn, max_retries=3, base_delay=0.01)
    assert fn.call_count == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_retry.py -v`
Expected: ImportError on `retry_on_pacing`.

- [ ] **Step 3: Add `retry_on_pacing` to `ib_data.py`**

Append:
```python
import time

PACING_KEYWORDS = ("pacing", "rate", "162", "165", "322", "420")


def _looks_like_pacing(exc: BaseException) -> bool:
    msg = str(exc).lower()
    return any(k in msg for k in PACING_KEYWORDS)


def retry_on_pacing(fn, *, max_retries: int = 3, base_delay: float = 10.0):
    """Call fn() with exponential backoff on pacing errors.
    Backoff: base_delay, 2*base_delay, 4*base_delay. Non-pacing errors propagate."""
    attempt = 0
    while True:
        try:
            return fn()
        except Exception as exc:
            if not _looks_like_pacing(exc) or attempt >= max_retries:
                raise
            delay = base_delay * (2 ** attempt)
            logger.warning("pacing error attempt %d/%d, sleeping %.1fs: %s",
                           attempt + 1, max_retries, delay, exc)
            time.sleep(delay)
            attempt += 1
```

- [ ] **Step 4: Wrap `reqHistoricalData` in `fetch_bars`**

In `fetch_bars`, replace the bare `bars = ib.reqHistoricalData(...)` call with:
```python
        bars = retry_on_pacing(
            lambda: ib.reqHistoricalData(
                contract,
                endDateTime="",
                durationStr=duration,
                barSizeSetting=_bar_size(timeframe),
                whatToShow=_what_to_show(sec_type, adjusted),
                useRTH=True,
                formatDate=1,
            ),
            max_retries=3,
            base_delay=10.0,
        )
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/test_retry.py -v`
Expected: 4 passed.

- [ ] **Step 6: Run full test suite (excluding smoke)**

Run: `pytest -m "not smoke" -v`
Expected: all V1 + new V2 tests pass.

- [ ] **Step 7: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/ib_data.py tests/test_retry.py
git -C D:/Plaios-tools/trading-tools commit -m "ingest: exponential-backoff retry on IB pacing errors"
```

---

### Task 4: Run the full Phase 1 ingest

**Files:** none (manual verification step). Note this overwrites/adds bars in production `trading_data` DB.

- [ ] **Step 1: Confirm IB Gateway is up on port 8000**

Run: `python -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('127.0.0.1',8000)); print('OK')"`
Expected: `OK`. If timeout, start TWS/Gateway.

- [ ] **Step 2: Run incremental ingest for the 23 new symbols**

(SPY+NVDA+VIX already populated by V1.) New symbols: AAPL,MSFT,GOOGL,GOOG,AMZN,META,AVGO,TSLA,COST,NFLX,AMD,PEP,ADBE,CSCO,TMUS,INTU,CMCSA,TXN,QCOM,AMGN,AMAT,ISRG,BKNG.

Run:
```
python -m trading_tools ingest --symbols AAPL,MSFT,GOOGL,GOOG,AMZN,META,AVGO,TSLA,COST,NFLX,AMD,PEP,ADBE,CSCO,TMUS,INTU,CMCSA,TXN,QCOM,AMGN,AMAT,ISRG,BKNG --duration "20 Y"
```
Expected: ~17 minutes; log shows "N rows upserted" per symbol×timeframe×adjusted combination.

- [ ] **Step 3: Verify row counts**

Run:
```
psql -d trading_data -c "SELECT symbol, COUNT(*) FROM equity_bars WHERE timeframe='daily' AND adjusted=true GROUP BY symbol ORDER BY symbol;"
```
Expected: 24 rows (23 new + SPY); each with ≥ 2,500 daily bars (or fewer for symbols IPO'd <10y ago, which is none of these).

- [ ] **Step 4: Spot-check a recent bar**

Run:
```
psql -d trading_data -c "SELECT * FROM equity_bars WHERE symbol='AAPL' AND adjusted=true ORDER BY ts DESC LIMIT 5;"
```
Expected: most recent week of trading days for AAPL with sane OHLCV values.

- [ ] **Step 5: Mark phase complete**

```bash
git -C D:/Plaios-tools/trading-tools commit --allow-empty -m "data: phase 1 ingest complete (top-25 universe in DB)"
```

---

## Phase 2 — Strategy register infrastructure

Goal: ship the `strategies` table, the `@register(...)` decorator, and the two benchmark strategies (`spy_buy_hold`, `asset_buy_hold`).

> **Note:** Phase 2 tests still run against the production `trading_data` DB (V1 conftest behavior). This is fine for now — Phase 3 fixes test-DB isolation as its first task. Don't introduce destructive ops in Phase 2 tests beyond what V1 already does.

### Task 5: Add `strategies` table to schema

**Files:**
- Modify: `D:\Plaios-tools\trading-tools\trading_tools\schema.sql`

- [ ] **Step 1: Append the DDL**

Append to `trading_tools/schema.sql`:
```sql
-- V2.1 — strategy register
CREATE TABLE IF NOT EXISTS strategies (
    name           TEXT PRIMARY KEY,
    module         TEXT NOT NULL,
    description    TEXT NOT NULL,
    direction      TEXT NOT NULL,              -- 'long' | 'short' | 'long_short'
    edge_status    TEXT NOT NULL,              -- 'documented' | 'mixed_lit' | 'folklore' | 'falsification' | 'contested' | 'benchmark'
    edge_source    TEXT,                       -- nullable only for benchmark strategies
    default_params JSONB NOT NULL DEFAULT '{}',
    asset_classes  TEXT[] NOT NULL,
    timeframes     TEXT[] NOT NULL,
    registered_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

- [ ] **Step 2: Apply the migration**

Run: `python -c "from trading_tools.db import init_schema; init_schema()"`
Expected: no error.

- [ ] **Step 3: Verify in psql**

Run: `psql -d trading_data -c "\d strategies"`
Expected: 9 columns shown matching the DDL.

- [ ] **Step 4: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/schema.sql
git -C D:/Plaios-tools/trading-tools commit -m "schema: strategies table"
```

---

### Task 6: Add `db.upsert_strategy()` helper

**Files:**
- Modify: `D:\Plaios-tools\trading-tools\trading_tools\db.py`
- Modify: `D:\Plaios-tools\trading-tools\tests\test_db.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_db.py`:
```python
def test_upsert_strategy_inserts_then_updates():
    row = {
        "name": "test_strat",
        "module": "trading_tools.strategies.test_strat",
        "description": "test",
        "direction": "long",
        "edge_status": "benchmark",
        "edge_source": None,
        "default_params": {"x": 1},
        "asset_classes": ["equity"],
        "timeframes": ["daily"],
    }
    n = db.upsert_strategy(row)
    assert n == 1
    stored = db.query("SELECT name, direction, default_params FROM strategies WHERE name = 'test_strat'")
    assert stored[0]["name"] == "test_strat"
    assert stored[0]["direction"] == "long"
    assert stored[0]["default_params"] == {"x": 1}

    # update
    row["description"] = "updated"
    n = db.upsert_strategy(row)
    assert n == 1
    stored = db.query("SELECT description FROM strategies WHERE name = 'test_strat'")
    assert stored[0]["description"] == "updated"
```

Also extend `tests/conftest.py` to truncate `strategies`:
```python
execute("TRUNCATE strategies, equity_bars, index_bars, instruments RESTART IDENTITY CASCADE")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_db.py::test_upsert_strategy_inserts_then_updates -v`
Expected: AttributeError on `db.upsert_strategy`.

- [ ] **Step 3: Add `upsert_strategy` to `db.py`**

Append to `trading_tools/db.py`:
```python
import json

def upsert_strategy(row: dict) -> int:
    """Upsert a strategies row. ON CONFLICT (name) DO UPDATE everything except registered_at."""
    cols = ["name", "module", "description", "direction",
            "edge_status", "edge_source", "default_params",
            "asset_classes", "timeframes"]
    update_cols = [c for c in cols if c != "name"]
    payload = dict(row)
    if isinstance(payload.get("default_params"), dict):
        payload["default_params"] = json.dumps(payload["default_params"])

    insert_sql = _sql.SQL(
        "INSERT INTO strategies ({cols}) VALUES ({placeholders}) "
        "ON CONFLICT (name) DO UPDATE SET {updates}"
    ).format(
        cols=_sql.SQL(",").join(_sql.Identifier(c) for c in cols),
        placeholders=_sql.SQL(",").join(_sql.Placeholder(c) for c in cols),
        updates=_sql.SQL(",").join(
            _sql.SQL("{c}=EXCLUDED.{c}").format(c=_sql.Identifier(c))
            for c in update_cols
        ),
    )
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(insert_sql, payload)
        conn.commit()
        return cur.rowcount
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_db.py::test_upsert_strategy_inserts_then_updates -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/db.py tests/test_db.py tests/conftest.py
git -C D:/Plaios-tools/trading-tools commit -m "db: upsert_strategy helper"
```

---

### Task 7: Build the `register()` decorator + `StrategyMeta`

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\strategies\__init__.py`
- Create: `D:\Plaios-tools\trading-tools\tests\test_register_decorator.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_register_decorator.py`:
```python
"""Tests for the @register decorator and the REGISTRY."""
import pandas as pd
import pytest

from trading_tools.strategies import REGISTRY, StrategyMeta, register


@pytest.fixture(autouse=True)
def clear_registry():
    REGISTRY.clear()
    yield
    REGISTRY.clear()


def test_register_adds_entry_to_registry():
    @register(
        name="dummy",
        description="d",
        direction="long",
        edge_status="benchmark",
        edge_source=None,
        default_params={},
        asset_classes=["equity"],
        timeframes=["daily"],
    )
    def signal(df, params):
        return pd.DataFrame()

    assert "dummy" in REGISTRY
    meta = REGISTRY["dummy"]
    assert isinstance(meta, StrategyMeta)
    assert meta.name == "dummy"
    assert meta.direction == "long"
    assert meta.fn is signal


def test_register_returns_unwrapped_function():
    @register(
        name="dummy2",
        description="d", direction="long", edge_status="benchmark",
        edge_source=None, default_params={},
        asset_classes=["equity"], timeframes=["daily"],
    )
    def signal(df, params):
        return "result"

    assert signal(None, None) == "result"


def test_register_rejects_invalid_direction():
    with pytest.raises(ValueError, match="direction"):
        @register(
            name="bad",
            description="d", direction="sideways", edge_status="benchmark",
            edge_source=None, default_params={},
            asset_classes=["equity"], timeframes=["daily"],
        )
        def signal(df, params):
            return pd.DataFrame()


def test_register_rejects_invalid_edge_status():
    with pytest.raises(ValueError, match="edge_status"):
        @register(
            name="bad",
            description="d", direction="long", edge_status="probably_works",
            edge_source=None, default_params={},
            asset_classes=["equity"], timeframes=["daily"],
        )
        def signal(df, params):
            return pd.DataFrame()


def test_register_requires_edge_source_for_non_benchmark():
    with pytest.raises(ValueError, match="edge_source"):
        @register(
            name="bad",
            description="d", direction="long", edge_status="folklore",
            edge_source=None, default_params={},
            asset_classes=["equity"], timeframes=["daily"],
        )
        def signal(df, params):
            return pd.DataFrame()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_register_decorator.py -v`
Expected: ImportError on `trading_tools.strategies`.

- [ ] **Step 3: Create `strategies/__init__.py`**

Create `trading_tools/strategies/__init__.py`:
```python
"""Strategy register: REGISTRY dict, StrategyMeta, register() decorator.

Strategy files import `register` from here, decorate their `signal` function with
metadata, and the decorator both:
  (a) populates the in-memory REGISTRY dict, and
  (b) lazily upserts a `strategies` row on first DB use (via db.upsert_strategy).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

import pandas as pd

REGISTRY: dict[str, "StrategyMeta"] = {}

VALID_DIRECTIONS = {"long", "short", "long_short"}
VALID_EDGE_STATUS = {"documented", "mixed_lit", "folklore", "falsification", "contested", "benchmark"}


@dataclass(frozen=True)
class StrategyMeta:
    name: str
    fn: Callable[[pd.DataFrame, dict], pd.DataFrame]
    description: str
    direction: Literal["long", "short", "long_short"]
    edge_status: Literal["documented", "mixed_lit", "folklore", "falsification", "contested", "benchmark"]
    edge_source: str | None
    default_params: dict
    asset_classes: list[str]
    timeframes: list[str]
    module: str = ""

    def to_db_row(self) -> dict:
        return {
            "name": self.name,
            "module": self.module or self.fn.__module__,
            "description": self.description,
            "direction": self.direction,
            "edge_status": self.edge_status,
            "edge_source": self.edge_source,
            "default_params": self.default_params,
            "asset_classes": self.asset_classes,
            "timeframes": self.timeframes,
        }


def register(
    *, name: str, description: str, direction: str, edge_status: str,
    edge_source: str | None, default_params: dict,
    asset_classes: list[str], timeframes: list[str],
) -> Callable:
    """Decorator that records strategy metadata in REGISTRY.

    Validates `direction`, `edge_status`, and that `edge_source` is non-null
    for non-benchmark strategies. The DB upsert happens lazily on first
    harness invocation, not here, so importing this module never opens a DB
    connection.
    """
    if direction not in VALID_DIRECTIONS:
        raise ValueError(f"invalid direction {direction!r}; must be one of {sorted(VALID_DIRECTIONS)}")
    if edge_status not in VALID_EDGE_STATUS:
        raise ValueError(f"invalid edge_status {edge_status!r}; must be one of {sorted(VALID_EDGE_STATUS)}")
    if edge_status != "benchmark" and not edge_source:
        raise ValueError(f"edge_source required for non-benchmark strategy {name!r}")

    def decorator(fn):
        REGISTRY[name] = StrategyMeta(
            name=name, fn=fn, description=description, direction=direction,
            edge_status=edge_status, edge_source=edge_source,
            default_params=dict(default_params),
            asset_classes=list(asset_classes), timeframes=list(timeframes),
            module=fn.__module__,
        )
        return fn
    return decorator


def sync_to_db() -> int:
    """Upsert all currently-registered strategies into the strategies table.
    Returns total rowcount affected."""
    from trading_tools import db
    n = 0
    for meta in REGISTRY.values():
        n += db.upsert_strategy(meta.to_db_row())
    return n
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_register_decorator.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/strategies/__init__.py tests/test_register_decorator.py
git -C D:/Plaios-tools/trading-tools commit -m "strategies: register decorator + StrategyMeta"
```

---

### Task 8: Add benchmark strategies (`spy_buy_hold`, `asset_buy_hold`)

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\strategies\spy_buy_hold.py`
- Create: `D:\Plaios-tools\trading-tools\trading_tools\strategies\asset_buy_hold.py`

Benchmark strategies emit a single `entry_long` on the first bar and never exit. The harness handles "hold to end" naturally because no exit signal fires.

- [ ] **Step 1: Create `spy_buy_hold.py`**

Create `trading_tools/strategies/spy_buy_hold.py`:
```python
"""Universal benchmark: buy SPY on first bar, hold forever."""
import pandas as pd

from . import register


@register(
    name="spy_buy_hold",
    description="Universal benchmark — buy SPY on first bar, hold to end of window.",
    direction="long",
    edge_status="benchmark",
    edge_source=None,
    default_params={},
    asset_classes=["equity"],
    timeframes=["daily", "weekly"],
)
def signal(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    n = len(df)
    entry = pd.Series(False, index=df.index)
    if n > 0:
        entry.iloc[0] = True
    zeros = pd.Series(False, index=df.index)
    return pd.DataFrame({
        "entry_long":  entry,
        "entry_short": zeros,
        "exit_long":   zeros,
        "exit_short":  zeros,
    }, index=df.index)
```

- [ ] **Step 2: Create `asset_buy_hold.py`**

Create `trading_tools/strategies/asset_buy_hold.py`:
```python
"""Per-asset benchmark: buy the underlying on first bar, hold forever.

Same signal logic as spy_buy_hold but the harness applies it to whatever
symbol the run is for, not always SPY. The strategy fn is identical;
the difference is which symbol's bars get fed in.
"""
import pandas as pd

from . import register


@register(
    name="asset_buy_hold",
    description="Per-asset benchmark — buy the underlying on first bar, hold to end.",
    direction="long",
    edge_status="benchmark",
    edge_source=None,
    default_params={},
    asset_classes=["equity"],
    timeframes=["daily", "weekly"],
)
def signal(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    n = len(df)
    entry = pd.Series(False, index=df.index)
    if n > 0:
        entry.iloc[0] = True
    zeros = pd.Series(False, index=df.index)
    return pd.DataFrame({
        "entry_long":  entry,
        "entry_short": zeros,
        "exit_long":   zeros,
        "exit_short":  zeros,
    }, index=df.index)
```

- [ ] **Step 3: Add a smoke test for both**

Append to `tests/test_register_decorator.py`:
```python
def test_benchmark_strategies_register_themselves():
    REGISTRY.clear()
    # Importing the module triggers the decorator
    import importlib
    importlib.import_module("trading_tools.strategies.spy_buy_hold")
    importlib.import_module("trading_tools.strategies.asset_buy_hold")
    assert "spy_buy_hold" in REGISTRY
    assert "asset_buy_hold" in REGISTRY
    assert REGISTRY["spy_buy_hold"].edge_status == "benchmark"


def test_buy_hold_signal_fires_only_on_first_bar():
    REGISTRY.clear()
    import importlib
    spy_mod = importlib.import_module("trading_tools.strategies.spy_buy_hold")
    df = pd.DataFrame({
        "open": [100, 101, 102],
        "high": [101, 102, 103],
        "low":  [99, 100, 101],
        "close":[100.5, 101.5, 102.5],
        "volume":[1000, 1000, 1000],
    }, index=pd.date_range("2020-01-01", periods=3, freq="D"))
    sig = spy_mod.signal(df, {})
    assert sig["entry_long"].tolist() == [True, False, False]
    assert sig["exit_long"].tolist()  == [False, False, False]
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_register_decorator.py -v`
Expected: 7 passed (5 original + 2 new).

- [ ] **Step 5: Commit Phase 2**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/strategies/ tests/test_register_decorator.py
git -C D:/Plaios-tools/trading-tools commit -m "strategies: register decorator + benchmark strategies"
```

---

## Phase 3 — Backtest harness

Goal: build the harness end-to-end, validate against SPY-BH and NVDA-BH known-answer cases, prove deterministic re-run produces identical curves. **First sub-task fixes V1's known issue: tests share the production DB.**

### Task 9: Test DB isolation

**Files:**
- Modify: `D:\Plaios-tools\trading-tools\.env.example`
- Modify: `D:\Plaios-tools\trading-tools\tests\conftest.py`
- Modify: `D:\Plaios-tools\trading-tools\trading_tools\db.py`

- [ ] **Step 1: Create the test database (manual; one-time)**

Run: `psql -U postgres -c "CREATE DATABASE trading_data_test"`
Expected: `CREATE DATABASE`. If it already exists, that's fine.

- [ ] **Step 2: Document `TEST_DATABASE_URL` in `.env.example`**

Append to `D:\Plaios-tools\trading-tools\.env.example`:
```
# Tests use a separate DB so pytest never touches production data.
TEST_DATABASE_URL=postgresql://USER:PASSWORD@127.0.0.1:5432/trading_data_test
```

- [ ] **Step 3: Add `TEST_DATABASE_URL` to local `.env` (manual)**

Tell the user to add this line to `D:\Plaios-tools\trading-tools\.env`:
```
TEST_DATABASE_URL=postgresql://<same-user>:<same-pw>@127.0.0.1:5432/trading_data_test
```

- [ ] **Step 4: Switch `db.py` to read `TEST_DATABASE_URL` when pytest is active**

Replace the `DATABASE_URL = os.environ["DATABASE_URL"]` line in `trading_tools/db.py` with:
```python
def _resolve_database_url() -> str:
    """Use TEST_DATABASE_URL when running under pytest; production URL otherwise."""
    import sys
    if "pytest" in sys.modules and os.environ.get("TEST_DATABASE_URL"):
        return os.environ["TEST_DATABASE_URL"]
    return os.environ["DATABASE_URL"]


DATABASE_URL = _resolve_database_url()
```

- [ ] **Step 5: Verify the switch works**

Run: `python -c "import sys; sys.modules['pytest']=object(); import os; os.environ['TEST_DATABASE_URL']='postgresql://wrong/test'; from trading_tools.db import DATABASE_URL; print(DATABASE_URL)"`
Expected: prints `postgresql://wrong/test` (proves the test branch is taken when pytest is in sys.modules).

- [ ] **Step 6: Re-apply schema to the test DB**

Run: `TEST_DATABASE_URL=$(grep TEST_DATABASE_URL D:/Plaios-tools/trading-tools/.env | cut -d= -f2-) python -c "import sys; sys.modules['pytest']=object(); from trading_tools.db import init_schema; init_schema()"`

(Or simpler: just run `pytest tests/test_db.py::test_upsert_instruments_inserts_new_rows` once — `conftest.py` calls `init_schema()` and that creates the tables in the test DB on first run.)

- [ ] **Step 7: Run the full V1+V2 test suite — should now run against test DB**

Run: `pytest -m "not smoke" -v`
Expected: all tests pass; afterwards `psql -d trading_data -c "SELECT COUNT(*) FROM equity_bars"` should return the production count (NOT zero — proving production was untouched).

- [ ] **Step 8: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/db.py tests/conftest.py .env.example
git -C D:/Plaios-tools/trading-tools commit -m "tests: isolate test runs to trading_data_test DB"
```

---

### Task 10: Add `backtest_runs` and `backtest_results` tables

**Files:**
- Modify: `D:\Plaios-tools\trading-tools\trading_tools\schema.sql`
- Modify: `D:\Plaios-tools\trading-tools\tests\conftest.py`

- [ ] **Step 1: Append the DDL to `schema.sql`**

```sql
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
    verdict        TEXT,
    decision       TEXT,
    decision_note  TEXT,
    reviewed_at    TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS backtest_runs_strategy_idx ON backtest_runs(strategy, created_at DESC);
CREATE INDEX IF NOT EXISTS backtest_runs_symbol_idx   ON backtest_runs(symbol,   created_at DESC);

-- V2.3 — per-run benchmark results
CREATE TABLE IF NOT EXISTS backtest_results (
    run_id          BIGINT NOT NULL REFERENCES backtest_runs(run_id) ON DELETE CASCADE,
    benchmark       TEXT NOT NULL,            -- 'strategy' | 'spy_bh' | 'asset_bh'
    cagr            NUMERIC(10,6),
    sharpe          NUMERIC(10,6),
    max_drawdown    NUMERIC(10,6),
    total_return    NUMERIC(10,6),
    n_trades        INTEGER,
    win_rate        NUMERIC(10,6),
    profit_factor   NUMERIC(10,6),
    excess_return_vs_spy_bh   NUMERIC(10,6),
    info_ratio_vs_spy_bh      NUMERIC(10,6),
    excess_return_vs_asset_bh NUMERIC(10,6),
    info_ratio_vs_asset_bh    NUMERIC(10,6),
    PRIMARY KEY (run_id, benchmark)
);
```

- [ ] **Step 2: Update conftest.py truncate list**

In `tests/conftest.py`, replace the `TRUNCATE` line with:
```python
execute("TRUNCATE backtest_results, backtest_runs, strategies, equity_bars, index_bars, instruments RESTART IDENTITY CASCADE")
```

- [ ] **Step 3: Apply schema and verify**

Run: `pytest tests/test_db.py -v` (this triggers `init_schema()` via the fixture and runs against the test DB).
Expected: all pass; `psql -d trading_data_test -c "\d backtest_runs"` shows the new tables.

- [ ] **Step 4: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/schema.sql tests/conftest.py
git -C D:/Plaios-tools/trading-tools commit -m "schema: backtest_runs + backtest_results tables"
```

---

### Task 11: Add `reproducibility.py` (git_sha, git_dirty, data_as_of)

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\backtest\__init__.py`
- Create: `D:\Plaios-tools\trading-tools\trading_tools\backtest\reproducibility.py`
- Create: `D:\Plaios-tools\trading-tools\tests\test_reproducibility.py`

- [ ] **Step 1: Write failing test**

Create `tests/test_reproducibility.py`:
```python
"""Tests for git_sha / git_dirty / data_as_of capture."""
import re
from datetime import datetime

from trading_tools.backtest.reproducibility import git_sha, git_dirty, data_as_of_for_symbol
from trading_tools import db
from datetime import date


def test_git_sha_returns_40_char_hex():
    sha = git_sha()
    assert isinstance(sha, str)
    assert re.match(r"^[a-f0-9]{40}$", sha), f"unexpected sha: {sha!r}"


def test_git_dirty_returns_bool():
    assert isinstance(git_dirty(), bool)


def test_data_as_of_returns_datetime_when_bars_exist():
    # Seed instrument + bar
    db.upsert_instruments([{
        "symbol": "TEST", "sec_type": "STK", "exchange": "ARCA",
        "currency": "USD", "asset_class": "equity",
        "first_seen": date(2020, 1, 1),
    }])
    db.upsert_bars("equity_bars", [{
        "symbol": "TEST", "timeframe": "daily", "ts": date(2020, 1, 2),
        "adjusted": True, "open": 100, "high": 101, "low": 99, "close": 100,
        "volume": 1000, "source": "test",
    }])
    result = data_as_of_for_symbol("TEST", timeframe="daily", adjusted=True)
    assert isinstance(result, datetime)


def test_data_as_of_returns_none_when_no_bars():
    assert data_as_of_for_symbol("NONEXISTENT", timeframe="daily", adjusted=True) is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_reproducibility.py -v`
Expected: ImportError on `trading_tools.backtest.reproducibility`.

- [ ] **Step 3: Create the module**

Create `trading_tools/backtest/__init__.py` (empty file).

Create `trading_tools/backtest/reproducibility.py`:
```python
"""Capture reproducibility metadata for a backtest run.

Records:
  git_sha     — exact code snapshot
  git_dirty   — flags non-reproducible runs (uncommitted changes)
  data_as_of  — bar version snapshot (max ingested_at of bars in scope)
"""
from __future__ import annotations

import logging
import subprocess
from datetime import datetime
from pathlib import Path

from trading_tools import db

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]


def _git(*args: str) -> str:
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def git_sha() -> str:
    """Full SHA of HEAD."""
    return _git("rev-parse", "HEAD")


def git_dirty() -> bool:
    """True if the working tree has uncommitted changes."""
    return bool(_git("status", "--porcelain"))


def data_as_of_for_symbol(symbol: str, *, timeframe: str = "daily",
                          adjusted: bool = True) -> datetime | None:
    """Max ingested_at across the bars matching this scope. None if no bars."""
    rows = db.query(
        "SELECT MAX(ingested_at) AS m FROM equity_bars "
        "WHERE symbol = %s AND timeframe = %s AND adjusted = %s",
        (symbol, timeframe, adjusted),
    )
    return rows[0]["m"] if rows and rows[0]["m"] else None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_reproducibility.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/backtest/ tests/test_reproducibility.py
git -C D:/Plaios-tools/trading-tools commit -m "backtest: reproducibility metadata capture"
```

---

### Task 12: Add `stats.py` (CAGR, Sharpe, max DD, etc.)

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\backtest\stats.py`
- Create: `D:\Plaios-tools\trading-tools\tests\test_stats.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_stats.py`:
```python
"""Known-answer tests for backtest stats."""
import math

import numpy as np
import pandas as pd
import pytest

from trading_tools.backtest.stats import (
    cagr, sharpe, max_drawdown, total_return,
    win_rate, profit_factor,
)


def _equity(values, start="2020-01-01"):
    return pd.Series(values, index=pd.date_range(start, periods=len(values), freq="D"))


def test_cagr_doubles_in_one_year_is_100pct():
    eq = _equity([1.0, 2.0])
    eq.index = pd.DatetimeIndex(["2020-01-01", "2021-01-01"])
    assert cagr(eq) == pytest.approx(1.0, abs=1e-6)


def test_cagr_flat_is_zero():
    eq = _equity([100.0] * 10)
    assert cagr(eq) == pytest.approx(0.0, abs=1e-9)


def test_total_return_simple():
    eq = _equity([100.0, 110.0])
    assert total_return(eq) == pytest.approx(0.10, abs=1e-9)


def test_max_drawdown_v_shape():
    eq = _equity([100.0, 80.0, 120.0])  # 20% DD then recovery
    assert max_drawdown(eq) == pytest.approx(-0.20, abs=1e-9)


def test_max_drawdown_no_drawdown():
    eq = _equity([100.0, 110.0, 120.0])
    assert max_drawdown(eq) == pytest.approx(0.0, abs=1e-9)


def test_sharpe_constant_returns_is_inf_or_nan():
    """Zero-variance returns → undefined Sharpe; we return 0 by convention."""
    rets = pd.Series([0.001] * 252)
    assert sharpe(rets) == 0.0  # std=0 → return 0


def test_sharpe_known_case():
    """Daily mean=0.001, std=0.01, ann=√252 → Sharpe ≈ 0.001/0.01 * √252 ≈ 1.587."""
    np.random.seed(42)
    rets = pd.Series(np.random.normal(0.001, 0.01, 1000))
    s = sharpe(rets)
    assert 1.0 < s < 2.5  # rough sanity range


def test_win_rate_basic():
    trades_pnl = pd.Series([10, -5, 20, -3, 0])  # 0 counts as no win
    assert win_rate(trades_pnl) == pytest.approx(2 / 5)


def test_win_rate_no_trades():
    assert win_rate(pd.Series(dtype=float)) == 0.0


def test_profit_factor_basic():
    trades_pnl = pd.Series([10, -5, 20, -3])
    # gross profit 30, gross loss 8
    assert profit_factor(trades_pnl) == pytest.approx(30 / 8)


def test_profit_factor_no_losers_returns_inf():
    trades_pnl = pd.Series([10, 20, 30])
    assert math.isinf(profit_factor(trades_pnl))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_stats.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `stats.py`**

Create `trading_tools/backtest/stats.py`:
```python
"""Pure-function stat calculations on equity curves and trade ledgers.

Conventions:
  - equity: pd.Series indexed by date, values = portfolio dollar value.
  - returns: pd.Series of period-over-period returns (e.g., daily).
  - trades_pnl: pd.Series of per-trade dollar PnL.
  - All functions return floats; undefined cases (no data, zero variance) return 0
    or +inf as documented per fn.
"""
from __future__ import annotations

import math
import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252


def total_return(equity: pd.Series) -> float:
    if len(equity) < 2:
        return 0.0
    return float(equity.iloc[-1] / equity.iloc[0] - 1)


def cagr(equity: pd.Series) -> float:
    if len(equity) < 2:
        return 0.0
    days = (equity.index[-1] - equity.index[0]).days
    if days <= 0:
        return 0.0
    years = days / 365.25
    end_over_start = float(equity.iloc[-1] / equity.iloc[0])
    if end_over_start <= 0:
        return -1.0  # total wipe-out edge case
    return end_over_start ** (1 / years) - 1


def sharpe(returns: pd.Series, *, ann_factor: int = TRADING_DAYS_PER_YEAR) -> float:
    """Annualised Sharpe ratio, rf=0. Returns 0.0 if zero variance."""
    if len(returns) < 2:
        return 0.0
    s = returns.std()
    if s == 0 or pd.isna(s):
        return 0.0
    return float(returns.mean() / s * math.sqrt(ann_factor))


def max_drawdown(equity: pd.Series) -> float:
    """Returns a non-positive float (e.g., -0.25 = 25% peak-to-trough drawdown)."""
    if len(equity) < 2:
        return 0.0
    running_peak = equity.cummax()
    dd = equity / running_peak - 1
    return float(dd.min())


def win_rate(trades_pnl: pd.Series) -> float:
    if len(trades_pnl) == 0:
        return 0.0
    wins = (trades_pnl > 0).sum()
    return float(wins / len(trades_pnl))


def profit_factor(trades_pnl: pd.Series) -> float:
    if len(trades_pnl) == 0:
        return 0.0
    gross_profit = trades_pnl[trades_pnl > 0].sum()
    gross_loss = -trades_pnl[trades_pnl < 0].sum()
    if gross_loss == 0:
        return math.inf if gross_profit > 0 else 0.0
    return float(gross_profit / gross_loss)


def info_ratio(strategy_returns: pd.Series, benchmark_returns: pd.Series, *,
               ann_factor: int = TRADING_DAYS_PER_YEAR) -> float:
    """Annualised information ratio of (strategy - benchmark) returns."""
    aligned = pd.concat([strategy_returns, benchmark_returns], axis=1).dropna()
    if len(aligned) < 2:
        return 0.0
    excess = aligned.iloc[:, 0] - aligned.iloc[:, 1]
    s = excess.std()
    if s == 0 or pd.isna(s):
        return 0.0
    return float(excess.mean() / s * math.sqrt(ann_factor))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_stats.py -v`
Expected: 11 passed.

- [ ] **Step 5: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/backtest/stats.py tests/test_stats.py
git -C D:/Plaios-tools/trading-tools commit -m "backtest: stats (CAGR, Sharpe, DD, win rate, profit factor, IR)"
```

---

### Task 13: Add `benchmarks.py` for 3-way comparison

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\backtest\benchmarks.py`

- [ ] **Step 1: Implement**

Create `trading_tools/backtest/benchmarks.py`:
```python
"""Three-way benchmark machinery.

Every backtest reports three equity curves over the same date range:
  - 'strategy' — the strategy under test
  - 'spy_bh'   — buy-and-hold SPY (universal cheapest-alternative)
  - 'asset_bh' — buy-and-hold the underlying instrument
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from . import stats


@dataclass
class BenchmarkRow:
    benchmark: str          # 'strategy' | 'spy_bh' | 'asset_bh'
    cagr: float
    sharpe: float
    max_drawdown: float
    total_return: float
    n_trades: int
    win_rate: float
    profit_factor: float
    excess_return_vs_spy_bh: float | None = None
    info_ratio_vs_spy_bh: float | None = None
    excess_return_vs_asset_bh: float | None = None
    info_ratio_vs_asset_bh: float | None = None


def _row(name: str, equity: pd.Series, trades_pnl: pd.Series) -> BenchmarkRow:
    rets = equity.pct_change().dropna()
    return BenchmarkRow(
        benchmark=name,
        cagr=stats.cagr(equity),
        sharpe=stats.sharpe(rets),
        max_drawdown=stats.max_drawdown(equity),
        total_return=stats.total_return(equity),
        n_trades=int(len(trades_pnl)),
        win_rate=stats.win_rate(trades_pnl),
        profit_factor=stats.profit_factor(trades_pnl),
    )


def three_way_compare(
    strategy_equity: pd.Series, strategy_trades_pnl: pd.Series,
    spy_bh_equity: pd.Series, spy_bh_trades_pnl: pd.Series,
    asset_bh_equity: pd.Series, asset_bh_trades_pnl: pd.Series,
) -> list[BenchmarkRow]:
    """Returns 3 rows. Excess/IR fields populated only on the 'strategy' row."""
    rows = [
        _row("strategy", strategy_equity, strategy_trades_pnl),
        _row("spy_bh",   spy_bh_equity,   spy_bh_trades_pnl),
        _row("asset_bh", asset_bh_equity, asset_bh_trades_pnl),
    ]
    s_rets = strategy_equity.pct_change().dropna()
    spy_rets = spy_bh_equity.pct_change().dropna()
    asset_rets = asset_bh_equity.pct_change().dropna()
    rows[0].excess_return_vs_spy_bh   = rows[0].total_return - rows[1].total_return
    rows[0].info_ratio_vs_spy_bh      = stats.info_ratio(s_rets, spy_rets)
    rows[0].excess_return_vs_asset_bh = rows[0].total_return - rows[2].total_return
    rows[0].info_ratio_vs_asset_bh    = stats.info_ratio(s_rets, asset_rets)
    return rows
```

- [ ] **Step 2: Commit (no test file — exercised via harness tests in Task 17)**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/backtest/benchmarks.py
git -C D:/Plaios-tools/trading-tools commit -m "backtest: three-way benchmark comparison"
```

---

### Task 14: Add `harness.py` core (`run_backtest` end-to-end)

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\backtest\harness.py`

This is the largest file in V2. Build it in steps; commit after each.

- [ ] **Step 1: Add `Result` dataclass + bar-loading helper**

Create `trading_tools/backtest/harness.py`:
```python
"""Backtest harness: run_backtest, list_runs, load_result, set_verdict, compare.

Single-instrument, daily/weekly bars, pure pandas/numpy walk. Position sizing:
$10K starting capital; each entry signal allocates 100% of current equity;
one position at a time per (symbol, strategy). Bar timing: entry on next bar's
open after signal; exit on next bar's open after exit signal. Synthetic short
(no borrow fee, no slippage, no commissions) — V3 swaps in put-spreads.
"""
from __future__ import annotations

import importlib
import json
import logging
import time
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path

import pandas as pd

from trading_tools import db
from trading_tools.strategies import REGISTRY
from . import benchmarks, reproducibility
from .benchmarks import BenchmarkRow

logger = logging.getLogger(__name__)

STARTING_CAPITAL = 10_000.0
RUNS_DIR = Path(__file__).resolve().parents[2] / "runs"


@dataclass
class Result:
    run_id: int
    strategy: str
    symbol: str
    start_date: date
    end_date: date
    timeframe: str
    direction: str
    params: dict
    git_sha: str
    git_dirty: bool
    data_as_of: datetime | None
    duration_ms: int
    artifact_dir: Path
    rows: list[BenchmarkRow]
    equity_curve: pd.Series  # strategy
    spy_bh_equity: pd.Series
    asset_bh_equity: pd.Series
    trades: pd.DataFrame
    signals: pd.DataFrame


def _ensure_strategy_imported(name: str) -> None:
    """Ensure the strategy module is imported so REGISTRY is populated."""
    if name in REGISTRY:
        return
    importlib.import_module(f"trading_tools.strategies.{name}")
    if name not in REGISTRY:
        raise KeyError(f"strategy {name!r} not registered after import")


def _load_bars(symbol: str, start: date, end: date, *,
               timeframe: str, adjusted: bool) -> pd.DataFrame:
    """Load bars from equity_bars or index_bars into a DatetimeIndex DataFrame."""
    rows = db.query(
        "SELECT ts, open, high, low, close, volume FROM equity_bars "
        "WHERE symbol = %s AND timeframe = %s AND adjusted = %s "
        "AND ts BETWEEN %s AND %s ORDER BY ts ASC",
        (symbol, timeframe, adjusted, start, end),
    )
    if not rows:
        raise ValueError(f"no bars for {symbol} {timeframe} adj={adjusted} "
                         f"in [{start}, {end}]")
    df = pd.DataFrame(rows)
    df["ts"] = pd.to_datetime(df["ts"])
    df = df.set_index("ts").sort_index()
    df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype(float)
    return df
```

- [ ] **Step 2: Add the trade-walker (signals → trade ledger + equity curve)**

Append to `harness.py`:
```python
def _walk_signals(df: pd.DataFrame, signals: pd.DataFrame, direction: str,
                  starting_capital: float = STARTING_CAPITAL) -> tuple[pd.DataFrame, pd.Series]:
    """Walk signals → trade ledger + equity curve.

    Rules:
      - one position at a time
      - entry fills at next bar's open after signal fires
      - exit fills at next bar's open after exit signal fires
      - long: pnl = (exit_px - entry_px) / entry_px * position_value
      - short: pnl = (entry_px - exit_px) / entry_px * position_value
      - 100% allocation per entry; equity at trade close = entry equity * (1 + return)
    """
    cash = starting_capital
    position = None  # dict with side, entry_idx, entry_px, value or None
    trades_records: list[dict] = []
    equity = pd.Series(starting_capital, index=df.index, dtype=float)

    n = len(df)
    for i in range(n):
        ts = df.index[i]

        # Mark equity (open position floats with current close, no realisation yet)
        if position is not None:
            current_px = df["close"].iloc[i]
            entry_px = position["entry_px"]
            if position["side"] == "long":
                ret = (current_px - entry_px) / entry_px
            else:
                ret = (entry_px - current_px) / entry_px
            equity.iloc[i] = position["entry_equity"] * (1 + ret)
        else:
            equity.iloc[i] = cash

        # Decide if we exit at NEXT bar's open
        if position is not None and i + 1 < n:
            exit_now = (
                (position["side"] == "long"  and bool(signals["exit_long"].iloc[i]))
                or (position["side"] == "short" and bool(signals["exit_short"].iloc[i]))
            )
            if exit_now:
                exit_px = df["open"].iloc[i + 1]
                entry_px = position["entry_px"]
                if position["side"] == "long":
                    ret = (exit_px - entry_px) / entry_px
                else:
                    ret = (entry_px - exit_px) / entry_px
                pnl = position["entry_equity"] * ret
                cash = position["entry_equity"] + pnl
                trades_records.append({
                    "side": position["side"],
                    "entry_ts": position["entry_ts"],
                    "entry_px": entry_px,
                    "exit_ts": df.index[i + 1],
                    "exit_px": exit_px,
                    "return": ret,
                    "pnl": pnl,
                    "entry_equity": position["entry_equity"],
                    "exit_equity": cash,
                })
                position = None

        # Decide if we enter at NEXT bar's open
        if position is None and i + 1 < n:
            want_long = direction in ("long", "long_short") and bool(signals["entry_long"].iloc[i])
            want_short = direction in ("short", "long_short") and bool(signals["entry_short"].iloc[i])
            if want_long or want_short:
                side = "long" if want_long else "short"
                entry_px = df["open"].iloc[i + 1]
                position = {
                    "side": side,
                    "entry_ts": df.index[i + 1],
                    "entry_px": entry_px,
                    "entry_equity": cash,
                }

    # Close any open position at the final close (mark-to-market, not a trade)
    if position is not None:
        last_px = df["close"].iloc[-1]
        entry_px = position["entry_px"]
        if position["side"] == "long":
            ret = (last_px - entry_px) / entry_px
        else:
            ret = (entry_px - last_px) / entry_px
        equity.iloc[-1] = position["entry_equity"] * (1 + ret)

    trades = pd.DataFrame(trades_records) if trades_records else pd.DataFrame(
        columns=["side", "entry_ts", "entry_px", "exit_ts", "exit_px",
                 "return", "pnl", "entry_equity", "exit_equity"]
    )
    return trades, equity
```

- [ ] **Step 3: Add `run_backtest` orchestration**

Append to `harness.py`:
```python
def _persist_run(meta: dict) -> int:
    """INSERT INTO backtest_runs RETURNING run_id."""
    sql = """
        INSERT INTO backtest_runs
        (strategy, symbol, start_date, end_date, timeframe, direction,
         params, git_sha, git_dirty, data_as_of, duration_ms, artifact_dir)
        VALUES (%(strategy)s, %(symbol)s, %(start_date)s, %(end_date)s,
                %(timeframe)s, %(direction)s, %(params)s, %(git_sha)s,
                %(git_dirty)s, %(data_as_of)s, %(duration_ms)s, %(artifact_dir)s)
        RETURNING run_id
    """
    payload = dict(meta)
    payload["params"] = json.dumps(payload["params"])
    with db.get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, payload)
        run_id = cur.fetchone()["run_id"]
        conn.commit()
        return run_id


def _persist_results(run_id: int, rows: list[BenchmarkRow]) -> None:
    sql = """
        INSERT INTO backtest_results
        (run_id, benchmark, cagr, sharpe, max_drawdown, total_return,
         n_trades, win_rate, profit_factor,
         excess_return_vs_spy_bh, info_ratio_vs_spy_bh,
         excess_return_vs_asset_bh, info_ratio_vs_asset_bh)
        VALUES (%(run_id)s, %(benchmark)s, %(cagr)s, %(sharpe)s, %(max_drawdown)s,
                %(total_return)s, %(n_trades)s, %(win_rate)s, %(profit_factor)s,
                %(excess_return_vs_spy_bh)s, %(info_ratio_vs_spy_bh)s,
                %(excess_return_vs_asset_bh)s, %(info_ratio_vs_asset_bh)s)
    """
    payload_rows = []
    for r in rows:
        d = asdict(r)
        d["run_id"] = run_id
        payload_rows.append(d)
    with db.get_connection() as conn, conn.cursor() as cur:
        cur.executemany(sql, payload_rows)
        conn.commit()


def _to_date(d: date | str) -> date:
    return d if isinstance(d, date) else date.fromisoformat(d)


def run_backtest(
    strategy: str, symbol: str, start: date | str, end: date | str, *,
    timeframe: str = "daily",
    params: dict | None = None,
    direction_override: str | None = None,
    adjusted: bool = True,
) -> Result:
    """End-to-end: load bars → call signal_fn → walk signals → compute trades + equity →
    compute 3-way benchmark stats → persist row + parquets → return Result.

    Charts are NOT generated here — call plots.generate_all(result) separately
    so the harness stays cheap to call from tests."""
    t0 = time.perf_counter()

    _ensure_strategy_imported(strategy)
    _ensure_strategy_imported("spy_buy_hold")
    _ensure_strategy_imported("asset_buy_hold")

    meta = REGISTRY[strategy]
    fn = meta.fn
    eff_params = dict(meta.default_params)
    if params:
        eff_params.update(params)
    direction = direction_override or meta.direction

    start_d = _to_date(start)
    end_d = _to_date(end)

    # Lazy upsert strategy row to DB (harness is the trigger)
    db.upsert_strategy(meta.to_db_row())
    # Also upsert the two benchmark strategies so backtest_runs FK can reference them
    db.upsert_strategy(REGISTRY["spy_buy_hold"].to_db_row())
    db.upsert_strategy(REGISTRY["asset_buy_hold"].to_db_row())

    # Strategy bars (the symbol under test)
    df = _load_bars(symbol, start_d, end_d, timeframe=timeframe, adjusted=adjusted)
    signals = fn(df, eff_params)
    _validate_signals(signals, df.index)
    trades, equity = _walk_signals(df, signals, direction)

    # Benchmark equity curves (BH on SPY and on the same symbol)
    spy_df = _load_bars("SPY", start_d, end_d, timeframe=timeframe, adjusted=True)
    spy_sig = REGISTRY["spy_buy_hold"].fn(spy_df, {})
    spy_trades, spy_equity = _walk_signals(spy_df, spy_sig, "long")

    asset_sig = REGISTRY["asset_buy_hold"].fn(df, {})
    asset_trades, asset_equity = _walk_signals(df, asset_sig, "long")

    # Align all three to the strategy's index for stats fairness
    common_idx = equity.index.intersection(spy_equity.index).intersection(asset_equity.index)
    equity = equity.reindex(common_idx)
    spy_equity = spy_equity.reindex(common_idx)
    asset_equity = asset_equity.reindex(common_idx)

    rows = benchmarks.three_way_compare(
        equity, trades.get("pnl", pd.Series(dtype=float)),
        spy_equity, spy_trades.get("pnl", pd.Series(dtype=float)),
        asset_equity, asset_trades.get("pnl", pd.Series(dtype=float)),
    )

    # Reproducibility metadata
    sha = reproducibility.git_sha()
    dirty = reproducibility.git_dirty()
    data_as_of = reproducibility.data_as_of_for_symbol(symbol, timeframe=timeframe, adjusted=adjusted)
    duration_ms = int((time.perf_counter() - t0) * 1000)

    if dirty:
        logger.warning("git working tree is dirty — run is not reproducible")

    # Allocate a run_id by inserting BEFORE knowing artifact_dir, then update artifact_dir
    artifact_dir_placeholder = "PENDING"
    run_id = _persist_run({
        "strategy": strategy, "symbol": symbol,
        "start_date": start_d, "end_date": end_d,
        "timeframe": timeframe, "direction": direction,
        "params": eff_params, "git_sha": sha, "git_dirty": dirty,
        "data_as_of": data_as_of, "duration_ms": duration_ms,
        "artifact_dir": artifact_dir_placeholder,
    })

    artifact_dir = RUNS_DIR / str(run_id)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    db.execute(
        "UPDATE backtest_runs SET artifact_dir = %s WHERE run_id = %s",
        (str(artifact_dir), run_id),
    )

    _persist_results(run_id, rows)

    # Write parquet artifacts
    trades.to_parquet(artifact_dir / "trades.parquet", index=False)
    signals.to_parquet(artifact_dir / "signals.parquet")
    pd.DataFrame({
        "strategy": equity, "spy_bh": spy_equity, "asset_bh": asset_equity,
    }).to_parquet(artifact_dir / "equity_curve.parquet")

    summary = {
        "run_id": run_id, "strategy": strategy, "symbol": symbol,
        "start_date": str(start_d), "end_date": str(end_d),
        "timeframe": timeframe, "direction": direction, "params": eff_params,
        "git_sha": sha, "git_dirty": dirty,
        "data_as_of": data_as_of.isoformat() if data_as_of else None,
        "duration_ms": duration_ms,
        "results": [asdict(r) for r in rows],
    }
    (artifact_dir / "summary.json").write_text(json.dumps(summary, default=str, indent=2))

    return Result(
        run_id=run_id, strategy=strategy, symbol=symbol,
        start_date=start_d, end_date=end_d, timeframe=timeframe,
        direction=direction, params=eff_params,
        git_sha=sha, git_dirty=dirty, data_as_of=data_as_of,
        duration_ms=duration_ms, artifact_dir=artifact_dir,
        rows=rows, equity_curve=equity,
        spy_bh_equity=spy_equity, asset_bh_equity=asset_equity,
        trades=trades, signals=signals,
    )


def _validate_signals(signals: pd.DataFrame, expected_index: pd.Index) -> None:
    required = {"entry_long", "entry_short", "exit_long", "exit_short"}
    missing = required - set(signals.columns)
    if missing:
        raise ValueError(f"signal DataFrame missing required columns: {sorted(missing)}")
    if not signals.index.equals(expected_index):
        raise ValueError("signal DataFrame index must equal bar DataFrame index")
    for c in required:
        if signals[c].dtype != bool:
            signals[c] = signals[c].astype(bool)
```

- [ ] **Step 4: Add `list_runs`, `load_result`, `set_verdict`, `compare`**

Append to `harness.py`:
```python
def list_runs(strategy: str | None = None, symbol: str | None = None,
              since: date | None = None, verdict: str | None = None) -> pd.DataFrame:
    """Return runs filtered by criteria, latest first. Joins backtest_runs +
    the 'strategy' row of backtest_results for headline stats."""
    where = []
    args: list = []
    if strategy:
        where.append("r.strategy = %s"); args.append(strategy)
    if symbol:
        where.append("r.symbol = %s"); args.append(symbol)
    if since:
        where.append("r.created_at >= %s"); args.append(since)
    if verdict:
        where.append("r.verdict = %s"); args.append(verdict)
    where_sql = ("WHERE " + " AND ".join(where)) if where else ""
    sql = f"""
        SELECT r.run_id, r.strategy, r.symbol, r.start_date, r.end_date,
               r.timeframe, r.direction, r.git_sha, r.git_dirty,
               r.duration_ms, r.created_at,
               r.verdict, r.decision, r.decision_note,
               s.cagr, s.sharpe, s.max_drawdown, s.total_return,
               s.n_trades, s.win_rate, s.profit_factor,
               s.excess_return_vs_spy_bh, s.info_ratio_vs_spy_bh,
               s.excess_return_vs_asset_bh, s.info_ratio_vs_asset_bh
        FROM backtest_runs r
        LEFT JOIN backtest_results s
          ON s.run_id = r.run_id AND s.benchmark = 'strategy'
        {where_sql}
        ORDER BY r.created_at DESC
    """
    return pd.DataFrame(db.query(sql, tuple(args)))


def load_result(run_id: int) -> dict:
    """Reload a previously-computed run from DB + parquets. Returns a dict
    (not a full Result — callers usually want the parquets directly)."""
    runs = db.query("SELECT * FROM backtest_runs WHERE run_id = %s", (run_id,))
    if not runs:
        raise ValueError(f"no run with run_id={run_id}")
    run = runs[0]
    results = db.query(
        "SELECT * FROM backtest_results WHERE run_id = %s ORDER BY benchmark", (run_id,))
    artifact_dir = Path(run["artifact_dir"])
    return {
        "run": run,
        "results": results,
        "trades": pd.read_parquet(artifact_dir / "trades.parquet"),
        "signals": pd.read_parquet(artifact_dir / "signals.parquet"),
        "equity_curve": pd.read_parquet(artifact_dir / "equity_curve.parquet"),
    }


def set_verdict(run_id: int, *, verdict: str, decision: str, note: str) -> None:
    """Record the v4 design-test-store loop Phase 4 outcome."""
    valid_verdict = {"edge", "no_edge", "inconclusive", "benchmark"}
    valid_decision = {"shelf", "iterate", "promote", "benchmark"}
    if verdict not in valid_verdict:
        raise ValueError(f"verdict must be one of {sorted(valid_verdict)}")
    if decision not in valid_decision:
        raise ValueError(f"decision must be one of {sorted(valid_decision)}")
    db.execute(
        "UPDATE backtest_runs SET verdict=%s, decision=%s, decision_note=%s, "
        "reviewed_at=NOW() WHERE run_id=%s",
        (verdict, decision, note, run_id),
    )


def compare(run_id_a: int, run_id_b: int) -> pd.DataFrame:
    """Side-by-side stats diff. Joins both runs' 'strategy' result rows."""
    rows = db.query(
        "SELECT r.run_id, r.strategy, r.symbol, r.params, "
        "s.cagr, s.sharpe, s.max_drawdown, s.total_return, "
        "s.n_trades, s.win_rate, s.profit_factor "
        "FROM backtest_runs r JOIN backtest_results s "
        "ON s.run_id = r.run_id AND s.benchmark='strategy' "
        "WHERE r.run_id IN (%s, %s) ORDER BY r.run_id",
        (run_id_a, run_id_b),
    )
    return pd.DataFrame(rows)
```

- [ ] **Step 5: Sanity-check the harness imports cleanly**

Run: `python -c "from trading_tools.backtest.harness import run_backtest; print('ok')"`
Expected: `ok`.

- [ ] **Step 6: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/backtest/harness.py
git -C D:/Plaios-tools/trading-tools commit -m "backtest: harness core (run_backtest + list/load/verdict/compare)"
```

---

### Task 15: Validate the harness — SPY-BH known-answer test

**Files:**
- Create: `D:\Plaios-tools\trading-tools\tests\test_harness.py`

**Approach:** Seed the test DB with synthetic bars where we know the answer; run `spy_buy_hold` end-to-end and assert the strategy total return matches the manual `(close_last/close_first)-1` to within tight tolerance (we use first-bar OPEN as entry per spec, so the right comparison is `close_last/open_second - 1` — since the entry signal fires on bar 0 and fills at bar 1's open, and we hold to end. We compare strategy total_return against this analytic value).

- [ ] **Step 1: Write the test**

Create `tests/test_harness.py`:
```python
"""Harness validation: known-answer cases for SPY-BH and NVDA-BH.

Test the test before trusting strategy results.
"""
import os
from datetime import date

import numpy as np
import pandas as pd
import pytest

from trading_tools import db
from trading_tools.backtest.harness import run_backtest


def _seed_synthetic_bars(symbol: str, prices: list[float], *, exchange: str = "ARCA") -> None:
    """Insert daily bars on consecutive NYSE business days starting 2020-01-02.
    OHLC are all set to `price` for simplicity (so open == close == high == low).
    """
    db.upsert_instruments([{
        "symbol": symbol, "sec_type": "STK", "exchange": exchange,
        "currency": "USD", "asset_class": "equity",
        "first_seen": date(2020, 1, 2),
    }])
    bdays = pd.bdate_range("2020-01-02", periods=len(prices)).date
    bars = []
    for d, p in zip(bdays, prices):
        bars.append({
            "symbol": symbol, "timeframe": "daily", "ts": d,
            "adjusted": True, "open": p, "high": p, "low": p, "close": p,
            "volume": 1_000_000, "source": "test",
        })
    db.upsert_bars("equity_bars", bars)


def test_spy_bh_reproduces_total_return():
    """spy_buy_hold's strategy total_return ≈ (close_last/open_secondbar - 1)
    because the first-bar entry signal fills at the second bar's open and we
    hold to end."""
    prices = [100.0, 101.0, 102.0, 103.0, 105.0]  # 5 bars
    _seed_synthetic_bars("SPY", prices)

    result = run_backtest(
        "spy_buy_hold", "SPY",
        start=date(2020, 1, 1), end=date(2020, 12, 31),
    )
    strategy_row = next(r for r in result.rows if r.benchmark == "strategy")
    spy_row      = next(r for r in result.rows if r.benchmark == "spy_bh")
    asset_row    = next(r for r in result.rows if r.benchmark == "asset_bh")

    # Entry at second bar's open (101); hold to last close (105)
    expected = 105 / 101 - 1
    assert strategy_row.total_return == pytest.approx(expected, abs=1e-6)
    # All three benchmarks identical here because spy_buy_hold == asset_buy_hold == strategy
    assert spy_row.total_return == pytest.approx(expected, abs=1e-6)
    assert asset_row.total_return == pytest.approx(expected, abs=1e-6)


def test_asset_bh_matches_for_nvda():
    """asset_buy_hold on NVDA: strategy curve should match the asset_bh curve exactly."""
    prices = [50.0, 52.0, 51.0, 55.0, 60.0, 58.0, 62.0]
    _seed_synthetic_bars("NVDA", prices, exchange="NASDAQ")
    _seed_synthetic_bars("SPY", [400.0] * len(prices))  # required for spy_bh benchmark

    result = run_backtest(
        "asset_buy_hold", "NVDA",
        start=date(2020, 1, 1), end=date(2020, 12, 31),
    )
    strategy_row = next(r for r in result.rows if r.benchmark == "strategy")
    asset_row    = next(r for r in result.rows if r.benchmark == "asset_bh")

    assert strategy_row.total_return == pytest.approx(asset_row.total_return, abs=1e-9)
    # Manual: enter at second bar's open (52), exit at last close (62)
    expected = 62 / 52 - 1
    assert strategy_row.total_return == pytest.approx(expected, abs=1e-6)


def test_run_id_monotonic():
    """Two backtest runs return distinct, increasing run_ids."""
    prices = [100.0, 101.0, 102.0, 103.0, 105.0]
    _seed_synthetic_bars("SPY", prices)

    r1 = run_backtest("spy_buy_hold", "SPY",
                      start=date(2020, 1, 1), end=date(2020, 12, 31))
    r2 = run_backtest("spy_buy_hold", "SPY",
                      start=date(2020, 1, 1), end=date(2020, 12, 31))
    assert r2.run_id > r1.run_id
```

- [ ] **Step 2: Run the test**

Run: `pytest tests/test_harness.py -v`
Expected: 3 passed. If any fail, fix the harness — these are the known-answer validations the spec requires.

- [ ] **Step 3: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add tests/test_harness.py
git -C D:/Plaios-tools/trading-tools commit -m "tests: harness known-answer validation (SPY-BH, NVDA-BH, run_id monotonic)"
```

---

### Task 16: Determinism test — same params produce identical equity curve

**Files:**
- Modify: `D:\Plaios-tools\trading-tools\tests\test_reproducibility.py`

- [ ] **Step 1: Append the determinism test**

Append to `tests/test_reproducibility.py`:
```python
import pandas as pd
import numpy as np
from trading_tools.backtest.harness import run_backtest


def _seed_synthetic_bars(symbol: str, n: int = 50, seed: int = 0,
                         exchange: str = "ARCA") -> None:
    from trading_tools import db
    rng = np.random.default_rng(seed)
    prices = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))
    db.upsert_instruments([{
        "symbol": symbol, "sec_type": "STK", "exchange": exchange,
        "currency": "USD", "asset_class": "equity",
        "first_seen": date(2020, 1, 2),
    }])
    bdays = pd.bdate_range("2020-01-02", periods=n).date
    bars = [{
        "symbol": symbol, "timeframe": "daily", "ts": d,
        "adjusted": True, "open": float(p), "high": float(p),
        "low": float(p), "close": float(p),
        "volume": 1_000_000, "source": "test",
    } for d, p in zip(bdays, prices)]
    db.upsert_bars("equity_bars", bars)


def test_deterministic_rerun_produces_identical_equity_curve():
    """Same inputs → bit-for-bit identical equity curve (modulo float epsilon)."""
    _seed_synthetic_bars("SPY", n=50, seed=42)

    r1 = run_backtest("spy_buy_hold", "SPY",
                      start=date(2020, 1, 1), end=date(2020, 12, 31))
    r2 = run_backtest("spy_buy_hold", "SPY",
                      start=date(2020, 1, 1), end=date(2020, 12, 31))
    pd.testing.assert_series_equal(r1.equity_curve, r2.equity_curve, check_names=False)
```

- [ ] **Step 2: Run**

Run: `pytest tests/test_reproducibility.py -v`
Expected: all pass (4 original + 1 new).

- [ ] **Step 3: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add tests/test_reproducibility.py
git -C D:/Plaios-tools/trading-tools commit -m "tests: deterministic re-run produces identical equity curve"
```

---

### Task 17: Wire backtest CLI subcommands

**Files:**
- Modify: `D:\Plaios-tools\trading-tools\trading_tools\cli.py`

Add subcommands: `backtest`, `list-runs`, `show-run`, `compare`, `verdict`.

- [ ] **Step 1: Add the subcommand definitions**

In `trading_tools/cli.py`, inside `main()` after the existing `p_gap` definition, add:
```python
    p_bt = sub.add_parser("backtest", help="Run a backtest")
    p_bt.add_argument("--strategy", required=True)
    p_bt.add_argument("--symbol", required=True)
    p_bt.add_argument("--start", required=True, type=lambda s: date.fromisoformat(s))
    p_bt.add_argument("--end", required=True, type=lambda s: date.fromisoformat(s))
    p_bt.add_argument("--timeframe", default="daily", choices=["daily", "weekly"])
    p_bt.add_argument("--params", default=None,
                      help="JSON dict of param overrides, e.g. '{\"period\": 50}'")
    p_bt.add_argument("--no-charts", action="store_true",
                      help="Skip chart generation (faster for batch runs)")

    p_lr = sub.add_parser("list-runs", help="List recorded backtest runs")
    p_lr.add_argument("--strategy", default=None)
    p_lr.add_argument("--symbol", default=None)
    p_lr.add_argument("--verdict", default=None)
    p_lr.add_argument("--since", default=None,
                      type=lambda s: date.fromisoformat(s))

    p_sr = sub.add_parser("show-run", help="Show one run by run_id")
    p_sr.add_argument("run_id", type=int)

    p_cmp = sub.add_parser("compare", help="Side-by-side compare two runs")
    p_cmp.add_argument("run_id_a", type=int)
    p_cmp.add_argument("run_id_b", type=int)

    p_v = sub.add_parser("verdict", help="Record verdict + decision on a run")
    p_v.add_argument("run_id", type=int)
    p_v.add_argument("--verdict", required=True,
                     choices=["edge", "no_edge", "inconclusive", "benchmark"])
    p_v.add_argument("--decision", required=True,
                     choices=["shelf", "iterate", "promote", "benchmark"])
    p_v.add_argument("--note", default="")
```

- [ ] **Step 2: Add dispatch handlers**

Append to the `if/elif args.cmd == ...` chain in `main()`:
```python
    elif args.cmd == "backtest":
        import json as _json
        from trading_tools.backtest.harness import run_backtest
        params = _json.loads(args.params) if args.params else None
        result = run_backtest(args.strategy, args.symbol,
                              start=args.start, end=args.end,
                              timeframe=args.timeframe, params=params)
        if not args.no_charts:
            from trading_tools.backtest.plots import generate_all
            generate_all(result)
        print(f"run_id={result.run_id}  artifact_dir={result.artifact_dir}")
        for r in result.rows:
            print(f"  {r.benchmark:9s}  CAGR={r.cagr:+.4f}  "
                  f"Sharpe={r.sharpe:+.3f}  MaxDD={r.max_drawdown:+.3f}  "
                  f"TotRet={r.total_return:+.4f}  N={r.n_trades}")
    elif args.cmd == "list-runs":
        from trading_tools.backtest.harness import list_runs
        df = list_runs(strategy=args.strategy, symbol=args.symbol,
                       since=args.since, verdict=args.verdict)
        print(df.to_string(index=False))
    elif args.cmd == "show-run":
        from trading_tools.backtest.harness import load_result
        loaded = load_result(args.run_id)
        import json as _json
        print(_json.dumps({k: str(v)[:300] for k, v in loaded["run"].items()},
                          indent=2, default=str))
        for r in loaded["results"]:
            print(f"  {r['benchmark']:9s}  TotRet={r['total_return']}  "
                  f"CAGR={r['cagr']}  Sharpe={r['sharpe']}")
    elif args.cmd == "compare":
        from trading_tools.backtest.harness import compare
        df = compare(args.run_id_a, args.run_id_b)
        print(df.to_string(index=False))
    elif args.cmd == "verdict":
        from trading_tools.backtest.harness import set_verdict
        set_verdict(args.run_id, verdict=args.verdict,
                    decision=args.decision, note=args.note)
        print(f"run_id={args.run_id}: {args.verdict} / {args.decision}")
```

Note `--no-charts` will be relevant once Phase 4 lands; for now `generate_all` doesn't exist yet — keep the subcommand definition but expect Phase 4 to make it usable.

- [ ] **Step 3: Verify the parser builds**

Run: `python -c "from trading_tools.cli import main; main(['list-runs','--help'])"`
Expected: argparse prints help text without error (then exits via SystemExit 0; that's fine).

- [ ] **Step 4: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/cli.py
git -C D:/Plaios-tools/trading-tools commit -m "cli: backtest, list-runs, show-run, compare, verdict subcommands"
```

---

### Task 18: Phase 3 closeout commit

- [ ] **Step 1: Run full test suite**

Run: `pytest -m "not smoke" -v`
Expected: all V1 + Phase 1 + Phase 2 + Phase 3 tests pass.

- [ ] **Step 2: Mark phase complete**

```bash
git -C D:/Plaios-tools/trading-tools commit --allow-empty -m "backtest: harness + 3-way benchmark + reproducibility (phase 3 complete)"
```

---

## Phase 4 — Plotting + summary HTML

Goal: 3 Plotly interactive (equity curve, drawdown, trades) + 2 mpl PNG (returns dist, monthly heatmap), stitched into `summary.html` per run.

### Task 19: Add chart deps to `pyproject.toml`

**Files:**
- Modify: `D:\Plaios-tools\trading-tools\pyproject.toml`

- [ ] **Step 1: Append deps**

In the `[project] dependencies` list, add:
```toml
    "pandas>=2.2.0",
    "numpy>=1.26.0",
    "plotly>=5.22.0",
    "matplotlib>=3.9.0",
    "mplfinance>=0.12.10b0",
    "pyarrow>=15.0.0",
```

In `[project.optional-dependencies] dev`, add:
```toml
    "jupyter>=1.0",
```

- [ ] **Step 2: Reinstall**

Run: `pip install -e D:/Plaios-tools/trading-tools[dev]`
Expected: all listed deps install.

- [ ] **Step 3: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add pyproject.toml
git -C D:/Plaios-tools/trading-tools commit -m "deps: pandas, numpy, plotly, matplotlib, mplfinance, jupyter, pyarrow"
```

---

### Task 20: Implement `plots.py` with all 5 charts + HTML stitcher

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\backtest\plots.py`
- Create: `D:\Plaios-tools\trading-tools\tests\test_plots.py`

- [ ] **Step 1: Write failing smoke test**

Create `tests/test_plots.py`:
```python
"""Smoke tests for chart generation (file existence + non-empty)."""
import os
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from trading_tools import db
from trading_tools.backtest.harness import run_backtest
from trading_tools.backtest.plots import generate_all


def _seed(symbol: str, n: int = 100, exchange: str = "ARCA"):
    rng = np.random.default_rng(0)
    prices = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))
    db.upsert_instruments([{
        "symbol": symbol, "sec_type": "STK", "exchange": exchange,
        "currency": "USD", "asset_class": "equity",
        "first_seen": date(2020, 1, 2),
    }])
    bdays = pd.bdate_range("2020-01-02", periods=n).date
    bars = [{
        "symbol": symbol, "timeframe": "daily", "ts": d,
        "adjusted": True, "open": float(p), "high": float(p),
        "low": float(p), "close": float(p),
        "volume": 1_000_000, "source": "test",
    } for d, p in zip(bdays, prices)]
    db.upsert_bars("equity_bars", bars)


def test_generate_all_produces_5_charts_plus_summary():
    _seed("SPY", n=100)
    result = run_backtest("spy_buy_hold", "SPY",
                          start=date(2020, 1, 1), end=date(2020, 12, 31))
    generate_all(result)

    charts_dir = result.artifact_dir / "charts"
    assert (charts_dir / "equity_curve.html").stat().st_size > 1000
    assert (charts_dir / "drawdown.html").stat().st_size > 1000
    assert (charts_dir / "trades.html").stat().st_size > 1000
    assert (charts_dir / "returns_dist.png").stat().st_size > 1000
    assert (charts_dir / "monthly_heatmap.png").stat().st_size > 1000
    assert (result.artifact_dir / "summary.html").stat().st_size > 1000
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_plots.py -v`
Expected: ImportError on `trading_tools.backtest.plots`.

- [ ] **Step 3: Implement `plots.py`**

Create `trading_tools/backtest/plots.py`:
```python
"""Chart generation for a backtest run.

3 Plotly HTMLs (interactive: equity, drawdown, trades) + 2 matplotlib PNGs
(returns distribution, monthly returns heatmap). `summary.html` stitches all
five inline along with the stats table and decision note.

CDN-loaded plotly.js keeps file size ~200KB-1MB per run.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend, safe in tests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go


def _equity_curve_chart(result) -> go.Figure:
    eq = result.equity_curve
    spy = result.spy_bh_equity
    asset = result.asset_bh_equity
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=eq.index, y=eq.values, name="strategy", mode="lines"))
    fig.add_trace(go.Scatter(x=spy.index, y=spy.values, name="SPY-BH", mode="lines",
                             line=dict(dash="dash")))
    fig.add_trace(go.Scatter(x=asset.index, y=asset.values, name=f"{result.symbol}-BH",
                             mode="lines", line=dict(dash="dot")))
    fig.update_layout(
        title=f"Equity curve — {result.strategy} on {result.symbol} (run {result.run_id})",
        xaxis_title="Date", yaxis_title="Equity ($)",
        hovermode="x unified", template="plotly_white",
    )
    return fig


def _drawdown_chart(result) -> go.Figure:
    def dd(eq):
        return eq / eq.cummax() - 1

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=result.equity_curve.index,
                             y=dd(result.equity_curve).values,
                             name="strategy", fill="tozeroy"))
    fig.add_trace(go.Scatter(x=result.spy_bh_equity.index,
                             y=dd(result.spy_bh_equity).values,
                             name="SPY-BH", line=dict(dash="dash")))
    fig.add_trace(go.Scatter(x=result.asset_bh_equity.index,
                             y=dd(result.asset_bh_equity).values,
                             name=f"{result.symbol}-BH", line=dict(dash="dot")))
    fig.update_layout(
        title=f"Drawdown — {result.strategy} on {result.symbol}",
        xaxis_title="Date", yaxis_title="Drawdown",
        yaxis_tickformat=".0%", hovermode="x unified", template="plotly_white",
    )
    return fig


def _trades_chart(result) -> go.Figure:
    """Price + indicator overlays (if present in signals) + entry/exit markers."""
    sig = result.signals
    # Reload bars from DB? No — we have the closes embedded in equity_curve...
    # Cleaner: pull close from indicator columns if present, else show entry/exit on equity.
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=result.equity_curve.index,
                             y=result.equity_curve.values, name="equity"))

    # Mark entry / exit timestamps from the trades ledger
    trades = result.trades
    if len(trades) > 0:
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(trades["entry_ts"]),
            y=trades["entry_equity"], mode="markers",
            marker=dict(symbol="triangle-up", size=10, color="green"),
            name="entry",
        ))
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(trades["exit_ts"]),
            y=trades["exit_equity"], mode="markers",
            marker=dict(symbol="triangle-down", size=10, color="red"),
            name="exit",
        ))

    # Optional indicator overlays
    for col in ("bb_upper", "bb_middle", "bb_lower"):
        if col in sig.columns:
            fig.add_trace(go.Scatter(x=sig.index, y=sig[col], name=col,
                                     line=dict(width=1, dash="dot"),
                                     yaxis="y2"))
    fig.update_layout(
        title=f"Trades — {result.strategy} on {result.symbol}",
        xaxis_title="Date",
        yaxis=dict(title="Equity ($)", side="left"),
        yaxis2=dict(title="Indicator", side="right", overlaying="y"),
        hovermode="x unified", template="plotly_white",
    )
    return fig


def _returns_dist_png(result, out_path: Path) -> None:
    rets = result.equity_curve.pct_change().dropna()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(rets, bins=50, edgecolor="black", alpha=0.7)
    ax.axvline(rets.mean(), color="red", linestyle="--",
               label=f"mean={rets.mean():.4f}")
    ax.set_title(f"Daily returns distribution — {result.strategy} on {result.symbol}")
    ax.set_xlabel("daily return")
    ax.set_ylabel("frequency")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=110)
    plt.close(fig)


def _monthly_heatmap_png(result, out_path: Path) -> None:
    rets = result.equity_curve.pct_change().dropna()
    monthly = rets.resample("ME").apply(lambda r: (1 + r).prod() - 1)
    pivot = pd.DataFrame({
        "year": monthly.index.year,
        "month": monthly.index.month,
        "ret": monthly.values,
    }).pivot(index="year", columns="month", values="ret")

    fig, ax = plt.subplots(figsize=(10, max(3, 0.4 * len(pivot))))
    if pivot.empty:
        ax.text(0.5, 0.5, "no monthly data", ha="center", va="center")
    else:
        im = ax.imshow(pivot.values, cmap="RdYlGn", aspect="auto",
                       vmin=-0.10, vmax=0.10)
        ax.set_xticks(range(len(pivot.columns)))
        ax.set_xticklabels(pivot.columns)
        ax.set_yticks(range(len(pivot.index)))
        ax.set_yticklabels(pivot.index)
        for i in range(len(pivot.index)):
            for j in range(len(pivot.columns)):
                v = pivot.values[i, j]
                if pd.notna(v):
                    ax.text(j, i, f"{v:.1%}", ha="center", va="center", fontsize=8)
        fig.colorbar(im, ax=ax, format="%.0%%")
    ax.set_title(f"Monthly returns — {result.strategy} on {result.symbol}")
    fig.tight_layout()
    fig.savefig(out_path, dpi=110)
    plt.close(fig)


def _stats_table_html(result) -> str:
    rows = "".join(
        f"<tr><td>{r.benchmark}</td><td>{r.total_return:+.4f}</td>"
        f"<td>{r.cagr:+.4f}</td><td>{r.sharpe:+.3f}</td>"
        f"<td>{r.max_drawdown:+.3f}</td><td>{r.n_trades}</td>"
        f"<td>{r.win_rate:.3f}</td></tr>"
        for r in result.rows
    )
    return (
        "<table border='1' cellpadding='6' style='border-collapse:collapse'>"
        "<thead><tr><th>benchmark</th><th>total return</th><th>CAGR</th>"
        "<th>Sharpe</th><th>max DD</th><th>N trades</th><th>win rate</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    )


def _summary_html(result, charts_dir: Path, out_path: Path) -> None:
    body = f"""
<html><head><title>run {result.run_id} — {result.strategy} on {result.symbol}</title></head>
<body style="font-family: -apple-system, system-ui, sans-serif; max-width: 1200px; margin: 2em auto;">
<h1>run {result.run_id}: {result.strategy} on {result.symbol}</h1>
<p>{result.start_date} → {result.end_date} | timeframe={result.timeframe} |
direction={result.direction}<br>
git_sha={result.git_sha[:12]} (dirty={result.git_dirty}) |
data_as_of={result.data_as_of} | duration_ms={result.duration_ms}</p>
<h2>Stats</h2>
{_stats_table_html(result)}
<h2>Equity curve</h2>
<iframe src="charts/equity_curve.html" width="100%" height="500" frameborder="0"></iframe>
<h2>Drawdown</h2>
<iframe src="charts/drawdown.html" width="100%" height="500" frameborder="0"></iframe>
<h2>Trades</h2>
<iframe src="charts/trades.html" width="100%" height="500" frameborder="0"></iframe>
<h2>Returns distribution</h2>
<img src="charts/returns_dist.png" style="max-width: 100%;">
<h2>Monthly heatmap</h2>
<img src="charts/monthly_heatmap.png" style="max-width: 100%;">
</body></html>
"""
    out_path.write_text(body, encoding="utf-8")


def generate_all(result) -> None:
    """Generate all 5 charts + summary.html into result.artifact_dir/charts/."""
    charts_dir = result.artifact_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    _equity_curve_chart(result).write_html(
        charts_dir / "equity_curve.html", include_plotlyjs="cdn")
    _drawdown_chart(result).write_html(
        charts_dir / "drawdown.html", include_plotlyjs="cdn")
    _trades_chart(result).write_html(
        charts_dir / "trades.html", include_plotlyjs="cdn")
    _returns_dist_png(result, charts_dir / "returns_dist.png")
    _monthly_heatmap_png(result, charts_dir / "monthly_heatmap.png")
    _summary_html(result, charts_dir, result.artifact_dir / "summary.html")
```

- [ ] **Step 4: Run smoke test**

Run: `pytest tests/test_plots.py -v`
Expected: 1 passed.

- [ ] **Step 5: Add `runs/` to `.gitignore`**

Append to `D:/Plaios-tools/trading-tools/.gitignore`:
```
runs/
.ipynb_checkpoints/
```

- [ ] **Step 6: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/backtest/plots.py tests/test_plots.py .gitignore
git -C D:/Plaios-tools/trading-tools commit -m "backtest: plotting + summary HTML"
```

---

## Phase 5 — Indicator primitives + BB strategies

Goal: ship `_base.py` (Bollinger, SMA, EMA, ATR, rolling_high, rolling_low) and the two BB strategies. Run them on real data and eyeball the trade markers.

### Task 21: Implement `_base.py` indicator primitives

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\strategies\_base.py`
- Create: `D:\Plaios-tools\trading-tools\tests\test_strategies.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_strategies.py`:
```python
"""Per-strategy unit tests on hand-crafted DataFrames."""
import numpy as np
import pandas as pd
import pytest

from trading_tools.strategies._base import (
    bollinger_bands, sma, ema, atr, rolling_high, rolling_low,
)


def _df(opens, highs, lows, closes):
    n = len(closes)
    return pd.DataFrame({
        "open": opens, "high": highs, "low": lows, "close": closes,
        "volume": [1_000_000] * n,
    }, index=pd.date_range("2020-01-01", periods=n, freq="D"))


def test_sma_simple():
    s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    result = sma(s, period=3)
    # indices 0,1 = NaN; index 2 = (1+2+3)/3 = 2.0
    assert pd.isna(result.iloc[0])
    assert pd.isna(result.iloc[1])
    assert result.iloc[2] == 2.0
    assert result.iloc[4] == 4.0


def test_ema_first_value_equals_first_input():
    s = pd.Series([10.0, 11.0, 12.0])
    result = ema(s, period=2)
    # EMA seed: pandas uses adjust=True by default; check it's monotonic and bounded
    assert result.iloc[0] == 10.0
    assert 10.0 < result.iloc[1] < 12.0


def test_bollinger_bands_pipboy_uses_low_for_lower_high_for_upper():
    df = _df(
        opens=[10] * 30, highs=[i + 1 for i in range(30)],
        lows=[i for i in range(30)], closes=[i + 0.5 for i in range(30)],
    )
    bb = bollinger_bands(df, period=20, stddev=2.0)
    assert {"lower", "middle", "upper"} <= set(bb.columns)
    # On the last bar, upper should be > middle should be > lower
    last = bb.iloc[-1]
    assert last["upper"] > last["middle"] > last["lower"]


def test_atr_basic():
    df = _df(
        opens=[100] * 5, highs=[101, 102, 103, 102, 105],
        lows=[99, 98, 100, 100, 101], closes=[100, 99, 102, 101, 104],
    )
    a = atr(df, period=3)
    assert a.iloc[-1] > 0


def test_rolling_high_low():
    df = _df(opens=[10] * 5, highs=[1, 2, 5, 3, 4],
             lows=[0, 1, 2, 0.5, 1.5], closes=[1, 2, 3, 2.5, 3.5])
    rh = rolling_high(df, period=3, source="high")
    rl = rolling_low(df, period=3, source="low")
    assert rh.iloc[2] == 5.0
    assert rh.iloc[4] == 5.0  # 3-bar window includes the 5
    assert rl.iloc[2] == 0.0
    assert rl.iloc[4] == 0.5
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_strategies.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement primitives**

Create `trading_tools/strategies/_base.py`:
```python
"""Indicator primitives shared across strategies.

Pure-pandas, no DB, no IB. All functions take a DataFrame with at minimum
{open, high, low, close} columns and a DatetimeIndex; or a Series for single-
column primitives.
"""
from __future__ import annotations

import pandas as pd


def sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(period, min_periods=period).mean()


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=True).mean()


def bollinger_bands(df: pd.DataFrame, *, period: int = 20, stddev: float = 2.0,
                    source_low: str = "low",
                    source_high: str = "high") -> pd.DataFrame:
    """Bollinger Bands per PipBoy V2 — lower from LOW, upper from HIGH.

    Deliberately deviates from textbook (which uses CLOSE for both) so that
    V3's PipBoy port is signal-compatible with the user's TradingView baseline.
    """
    sma_low  = df[source_low].rolling(period, min_periods=period).mean()
    std_low  = df[source_low].rolling(period, min_periods=period).std()
    sma_high = df[source_high].rolling(period, min_periods=period).mean()
    std_high = df[source_high].rolling(period, min_periods=period).std()
    return pd.DataFrame({
        "lower":  sma_low  - stddev * std_low,
        "middle": df["close"].rolling(period, min_periods=period).mean(),
        "upper":  sma_high + stddev * std_high,
    }, index=df.index)


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average True Range, Wilder smoothing approximation via SMA of TR."""
    prev_close = df["close"].shift(1)
    tr = pd.concat([
        df["high"] - df["low"],
        (df["high"] - prev_close).abs(),
        (df["low"]  - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.rolling(period, min_periods=period).mean()


def rolling_high(df: pd.DataFrame, *, period: int, source: str = "high") -> pd.Series:
    return df[source].rolling(period, min_periods=period).max()


def rolling_low(df: pd.DataFrame, *, period: int, source: str = "low") -> pd.Series:
    return df[source].rolling(period, min_periods=period).min()
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_strategies.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/strategies/_base.py tests/test_strategies.py
git -C D:/Plaios-tools/trading-tools commit -m "strategies: indicator primitives (BB-PipBoy, SMA, EMA, ATR, rolling)"
```

---

### Task 22: Implement `bb_meanrev.py`

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\strategies\bb_meanrev.py`

- [ ] **Step 1: Write failing test**

Append to `tests/test_strategies.py`:
```python
def test_bb_meanrev_signals_on_band_touch():
    """Construct a 30-bar series where bar 25 closes below the lower band.
    Expect entry_long = True on that bar."""
    # 24 flat bars at 100, then a sharp dip
    closes = [100.0] * 24 + [90.0, 92.0, 95.0, 100.0, 105.0, 100.0]
    n = len(closes)
    df = pd.DataFrame({
        "open": closes, "high": [c + 0.5 for c in closes],
        "low":  [c - 0.5 for c in closes], "close": closes,
        "volume": [1_000_000] * n,
    }, index=pd.date_range("2020-01-01", periods=n, freq="D"))

    from trading_tools.strategies.bb_meanrev import signal
    sig = signal(df, {"period": 20, "stddev": 2.0})
    # Some bar in the dip range fired entry_long
    assert sig["entry_long"].iloc[24:27].any()
```

- [ ] **Step 2: Implement `bb_meanrev.py`**

Create `trading_tools/strategies/bb_meanrev.py`:
```python
"""Bollinger Band mean-reversion (PipBoy 20/2 high-low primitive).

Long when close pierces lower band; exit when close crosses middle.
Short on inverse. Hypothesis: reverts toward the mean after extreme excursions.
Edge status: falsification — typical BB mean-reversion fails randomness tests
outside specific regimes.
"""
import pandas as pd

from . import register
from ._base import bollinger_bands


@register(
    name="bb_meanrev",
    description="Long on close < lower band; exit on close > middle. Short on inverse.",
    direction="long_short",
    edge_status="falsification",
    edge_source="Bollinger 1993 (primitive); standalone BB mean-reversion typically fails "
                "randomness tests outside specific regimes.",
    default_params={"period": 20, "stddev": 2.0},
    asset_classes=["equity"],
    timeframes=["daily"],
)
def signal(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    bb = bollinger_bands(df, period=params["period"], stddev=params["stddev"])
    close = df["close"]
    entry_long  = close < bb["lower"]
    entry_short = close > bb["upper"]
    exit_long   = close > bb["middle"]
    exit_short  = close < bb["middle"]
    return pd.DataFrame({
        "entry_long":  entry_long.fillna(False).astype(bool),
        "entry_short": entry_short.fillna(False).astype(bool),
        "exit_long":   exit_long.fillna(False).astype(bool),
        "exit_short":  exit_short.fillna(False).astype(bool),
        "bb_upper":    bb["upper"],
        "bb_middle":   bb["middle"],
        "bb_lower":    bb["lower"],
    }, index=df.index)
```

- [ ] **Step 3: Run tests**

Run: `pytest tests/test_strategies.py -v`
Expected: all pass.

- [ ] **Step 4: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/strategies/bb_meanrev.py tests/test_strategies.py
git -C D:/Plaios-tools/trading-tools commit -m "strategies: BB mean-reversion (PipBoy primitive)"
```

---

### Task 23: Implement `bb_squeeze.py`

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\strategies\bb_squeeze.py`

- [ ] **Step 1: Write failing test**

Append to `tests/test_strategies.py`:
```python
def test_bb_squeeze_fires_on_breakout_after_low_vol():
    """130 flat bars at 100 ± tiny noise (squeeze), then sudden upward break.
    Expect entry_long on the breakout bar."""
    np.random.seed(0)
    flat = 100 + np.random.normal(0, 0.05, 130)
    breakout = [105.0, 106.0, 107.0]
    closes = list(flat) + breakout
    n = len(closes)
    df = pd.DataFrame({
        "open": closes, "high": [c + 0.1 for c in closes],
        "low": [c - 0.1 for c in closes], "close": closes,
        "volume": [1_000_000] * n,
    }, index=pd.date_range("2020-01-01", periods=n, freq="D"))

    from trading_tools.strategies.bb_squeeze import signal
    sig = signal(df, {"period": 20, "stddev": 2.0, "squeeze_lookback": 120})
    # Breakout bars should fire entry_long
    assert sig["entry_long"].iloc[-3:].any()
```

- [ ] **Step 2: Implement**

Create `trading_tools/strategies/bb_squeeze.py`:
```python
"""BB squeeze → directional breakout.

Squeeze: BB width in lowest 20% of last `squeeze_lookback` bars.
Long on close above upper band after a squeeze; short on inverse.
Exit on close crossing middle.
"""
import pandas as pd

from . import register
from ._base import bollinger_bands


@register(
    name="bb_squeeze",
    description="Long when BB width contracts (squeeze) then closes above upper band; "
                "short on inverse. Exit on close crossing middle.",
    direction="long_short",
    edge_status="falsification",
    edge_source="Bollinger 1993 (primitive); PipBoy V2 (signal recipe). "
                "Marshall et al. 2008 found breakout strategies generally fail "
                "randomness tests.",
    default_params={"period": 20, "stddev": 2.0, "squeeze_lookback": 120},
    asset_classes=["equity"],
    timeframes=["daily"],
)
def signal(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    bb = bollinger_bands(df, period=params["period"], stddev=params["stddev"])
    width = bb["upper"] - bb["lower"]
    threshold = width.rolling(params["squeeze_lookback"]).quantile(0.20)
    in_squeeze = width <= threshold
    breakout_up   = (df["close"] > bb["upper"]) & in_squeeze.shift(1).fillna(False)
    breakout_down = (df["close"] < bb["lower"]) & in_squeeze.shift(1).fillna(False)
    return pd.DataFrame({
        "entry_long":  breakout_up.fillna(False).astype(bool),
        "entry_short": breakout_down.fillna(False).astype(bool),
        "exit_long":   (df["close"] < bb["middle"]).fillna(False).astype(bool),
        "exit_short":  (df["close"] > bb["middle"]).fillna(False).astype(bool),
        "bb_upper":    bb["upper"],
        "bb_middle":   bb["middle"],
        "bb_lower":    bb["lower"],
        "width":       width,
        "in_squeeze":  in_squeeze.fillna(False),
    }, index=df.index)
```

- [ ] **Step 3: Run test**

Run: `pytest tests/test_strategies.py -v`
Expected: all pass.

- [ ] **Step 4: Smoke run on real NVDA data**

Run:
```
python -m trading_tools backtest --strategy bb_squeeze --symbol NVDA --start 2010-01-01 --end 2026-04-29
```
Expected: prints `run_id=N artifact_dir=...` and the 3 benchmark rows. Open `runs/N/summary.html` and eyeball: entry markers should sit at price breakouts after periods of low BB width.

- [ ] **Step 5: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/strategies/bb_squeeze.py tests/test_strategies.py
git -C D:/Plaios-tools/trading-tools commit -m "strategies: BB squeeze (PipBoy primitive + 120-bar squeeze quantile)"
```

---

## Phase 6 — Remaining 8 seed strategies

Goal: ship the 8 remaining strategies. Each task pairs a strategy file with a unit test on a hand-crafted DataFrame.

> **Discipline:** when a unit test passes but the eyeball check on real data shows zero trades over 16 years, that's diagnostic — usually the pattern is too restrictive. Tighten the test to also assert at least one signal fires on a real-data slice before declaring "done".

### Task 24: `ma_cross.py` — 50/200-day moving-average cross

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\strategies\ma_cross.py`

- [ ] **Step 1: Append failing test**

Append to `tests/test_strategies.py`:
```python
def test_ma_cross_signals_on_golden_cross():
    """Construct a series where the 50-DMA crosses above the 200-DMA.
    Use shorter periods for tractability."""
    n = 50
    closes = [100.0] * 25 + [110.0] * 25  # step up: short MA crosses long
    df = pd.DataFrame({
        "open": closes, "high": [c + 0.5 for c in closes],
        "low": [c - 0.5 for c in closes], "close": closes,
        "volume": [1_000_000] * n,
    }, index=pd.date_range("2020-01-01", periods=n, freq="D"))

    from trading_tools.strategies.ma_cross import signal
    sig = signal(df, {"fast": 5, "slow": 20})
    # Some entry_long fires after the step
    assert sig["entry_long"].any()
```

- [ ] **Step 2: Implement**

Create `trading_tools/strategies/ma_cross.py`:
```python
"""50/200-day moving-average cross — golden / death cross.

Long entry on fast SMA crossing above slow SMA; short entry on inverse.
Exit on opposite cross.
"""
import pandas as pd

from . import register
from ._base import sma


@register(
    name="ma_cross",
    description="Long on fast SMA crossing above slow SMA; short on inverse. "
                "Exit on opposite cross.",
    direction="long_short",
    edge_status="folklore",
    edge_source="Practitioner folklore (golden cross / death cross); no consistent "
                "academic edge.",
    default_params={"fast": 50, "slow": 200},
    asset_classes=["equity"],
    timeframes=["daily"],
)
def signal(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    fast = sma(df["close"], params["fast"])
    slow = sma(df["close"], params["slow"])
    above = fast > slow
    cross_up   = above & ~above.shift(1).fillna(False)
    cross_down = ~above & above.shift(1).fillna(False)
    return pd.DataFrame({
        "entry_long":  cross_up.fillna(False).astype(bool),
        "entry_short": cross_down.fillna(False).astype(bool),
        "exit_long":   cross_down.fillna(False).astype(bool),
        "exit_short":  cross_up.fillna(False).astype(bool),
        "fast_sma":    fast,
        "slow_sma":    slow,
    }, index=df.index)
```

- [ ] **Step 3: Run + commit**

```bash
pytest tests/test_strategies.py -v
git -C D:/Plaios-tools/trading-tools add trading_tools/strategies/ma_cross.py tests/test_strategies.py
git -C D:/Plaios-tools/trading-tools commit -m "strategies: MA cross"
```

---

### Task 25: `engulfing.py` — bullish/bearish engulfing pattern

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\strategies\engulfing.py`

**Pattern definition:**
- **Bullish engulfing:** prev bar red (close<open) AND current bar green (close>open) AND current open ≤ prev close AND current close ≥ prev open.
- **Bearish engulfing:** mirror.
- **Exit:** after `holding_bars` bars (default 5) — measured by an exit-long/short signal that fires N bars after entry.

Holding-bars exits introduce a new helper: a strategy that times exits by "N bars after the most recent entry signal" needs lookahead-free state tracking. Approach: precompute, for each bar, "is this bar exactly N bars after the most recent entry_long signal?" using boolean shifting.

- [ ] **Step 1: Test**

Append to `tests/test_strategies.py`:
```python
def test_engulfing_bullish_pattern():
    """Bar 1 red (open 100, close 95), bar 2 green and engulfs (open 94, close 102)."""
    df = pd.DataFrame({
        "open":  [100, 94, 102, 105],
        "high":  [101, 103, 106, 108],
        "low":   [94, 93, 101, 104],
        "close": [95, 102, 105, 107],
        "volume":[1_000_000] * 4,
    }, index=pd.date_range("2020-01-01", periods=4, freq="D"))

    from trading_tools.strategies.engulfing import signal
    sig = signal(df, {"holding_bars": 2})
    assert bool(sig["entry_long"].iloc[1]) is True
```

- [ ] **Step 2: Implement**

Create `trading_tools/strategies/engulfing.py`:
```python
"""Bullish / bearish engulfing pattern with N-bar timed exit."""
import pandas as pd

from . import register


@register(
    name="engulfing",
    description="Bullish engulfing → long; bearish engulfing → short. "
                "Exit `holding_bars` after entry.",
    direction="long_short",
    edge_status="mixed_lit",
    edge_source="Marshall, Young & Rose 2006 ('Candlestick technical trading strategies', "
                "J. Banking & Finance) — weak edge in some markets.",
    default_params={"holding_bars": 5},
    asset_classes=["equity"],
    timeframes=["daily"],
)
def signal(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    o, c = df["open"], df["close"]
    prev_red   = c.shift(1) < o.shift(1)
    prev_green = c.shift(1) > o.shift(1)
    cur_green  = c > o
    cur_red    = c < o

    entry_long = (
        prev_red & cur_green
        & (o <= c.shift(1))
        & (c >= o.shift(1))
    )
    entry_short = (
        prev_green & cur_red
        & (o >= c.shift(1))
        & (c <= o.shift(1))
    )

    holding = int(params["holding_bars"])
    exit_long  = entry_long.shift(holding).fillna(False)
    exit_short = entry_short.shift(holding).fillna(False)

    return pd.DataFrame({
        "entry_long":  entry_long.fillna(False).astype(bool),
        "entry_short": entry_short.fillna(False).astype(bool),
        "exit_long":   exit_long.astype(bool),
        "exit_short":  exit_short.astype(bool),
    }, index=df.index)
```

- [ ] **Step 3: Run + commit**

```bash
pytest tests/test_strategies.py -v
git -C D:/Plaios-tools/trading-tools add trading_tools/strategies/engulfing.py tests/test_strategies.py
git -C D:/Plaios-tools/trading-tools commit -m "strategies: bullish/bearish engulfing"
```

---

### Task 26: `hammer.py` — hammer / hanging-man

**Pattern:** small real body near top (hammer for long) or bottom (hanging-man for short) of bar; lower shadow ≥ 2 × body. After downtrend → hammer = long; after uptrend → hanging-man = short.

- [ ] **Step 1: Test**

Append to `tests/test_strategies.py`:
```python
def test_hammer_pattern_after_downtrend():
    """4-bar downtrend then a hammer: long lower wick, small body near high."""
    df = pd.DataFrame({
        "open":  [100, 95, 90, 85, 84],
        "high":  [101, 96, 91, 86, 85.5],
        "low":   [99, 94, 89, 84, 78],   # last bar deep low
        "close": [95, 90, 85, 84, 85.0],  # close near high
        "volume":[1_000_000] * 5,
    }, index=pd.date_range("2020-01-01", periods=5, freq="D"))

    from trading_tools.strategies.hammer import signal
    sig = signal(df, {"trend_lookback": 3, "holding_bars": 2})
    assert bool(sig["entry_long"].iloc[-1])
```

- [ ] **Step 2: Implement**

Create `trading_tools/strategies/hammer.py`:
```python
"""Hammer / hanging-man pattern with trend filter and N-bar timed exit."""
import pandas as pd

from . import register


@register(
    name="hammer",
    description="Hammer after downtrend → long; hanging-man after uptrend → short.",
    direction="long_short",
    edge_status="folklore",
    edge_source="Bulkowski, Encyclopedia of Candlestick Charts; weak/decayed edge in "
                "tested patterns.",
    default_params={"trend_lookback": 5, "holding_bars": 5,
                    "wick_to_body_ratio": 2.0},
    asset_classes=["equity"],
    timeframes=["daily"],
)
def signal(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    o, h, l, c = df["open"], df["high"], df["low"], df["close"]
    body = (c - o).abs()
    upper_wick = h - pd.concat([o, c], axis=1).max(axis=1)
    lower_wick = pd.concat([o, c], axis=1).min(axis=1) - l
    ratio = float(params["wick_to_body_ratio"])

    is_hammer = (lower_wick >= ratio * body) & (upper_wick <= body)
    is_hanging = (upper_wick >= ratio * body) & (lower_wick <= body)

    lookback = int(params["trend_lookback"])
    in_downtrend = c < c.shift(lookback)
    in_uptrend   = c > c.shift(lookback)

    entry_long  = is_hammer & in_downtrend
    entry_short = is_hanging & in_uptrend

    holding = int(params["holding_bars"])
    exit_long  = entry_long.shift(holding).fillna(False)
    exit_short = entry_short.shift(holding).fillna(False)

    return pd.DataFrame({
        "entry_long":  entry_long.fillna(False).astype(bool),
        "entry_short": entry_short.fillna(False).astype(bool),
        "exit_long":   exit_long.astype(bool),
        "exit_short":  exit_short.astype(bool),
    }, index=df.index)
```

- [ ] **Step 3: Run + commit**

```bash
pytest tests/test_strategies.py -v
git -C D:/Plaios-tools/trading-tools add trading_tools/strategies/hammer.py tests/test_strategies.py
git -C D:/Plaios-tools/trading-tools commit -m "strategies: hammer / hanging-man"
```

---

### Task 27: `star.py` — morning star / evening star (3-bar pattern)

**Morning star (long):** bar -2 large red, bar -1 small body (gap down), bar 0 large green that closes ≥ midpoint of bar -2.
**Evening star (short):** mirror.

- [ ] **Step 1: Test**

Append to `tests/test_strategies.py`:
```python
def test_morning_star_pattern():
    df = pd.DataFrame({
        "open":  [100, 92, 91, 92, 99],
        "high":  [101, 93, 92.5, 93, 102],
        "low":   [91, 89, 90, 91, 98],
        "close": [92, 90, 91, 99, 101],   # bar idx 3 close=99 ≥ (100+92)/2=96 → morning star
        "volume":[1_000_000] * 5,
    }, index=pd.date_range("2020-01-01", periods=5, freq="D"))

    from trading_tools.strategies.star import signal
    sig = signal(df, {"holding_bars": 2})
    assert bool(sig["entry_long"].iloc[3])
```

- [ ] **Step 2: Implement**

Create `trading_tools/strategies/star.py`:
```python
"""Morning star / evening star (3-bar reversal patterns)."""
import pandas as pd

from . import register


@register(
    name="star",
    description="Morning star → long; evening star → short. 3-bar reversal pattern.",
    direction="long_short",
    edge_status="mixed_lit",
    edge_source="Marshall et al. 2006; Bulkowski.",
    default_params={"holding_bars": 5, "small_body_pct": 0.30},
    asset_classes=["equity"],
    timeframes=["daily"],
)
def signal(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    o, c = df["open"], df["close"]
    body = (c - o).abs()
    body_lag1 = body.shift(1)
    body_lag2 = body.shift(2)
    o_lag2, c_lag2 = o.shift(2), c.shift(2)

    small_body_pct = float(params["small_body_pct"])
    bar2_red    = c_lag2 < o_lag2
    bar2_green  = c_lag2 > o_lag2
    bar1_small  = body_lag1 <= small_body_pct * body_lag2
    bar0_green  = c > o
    bar0_red    = c < o
    midpoint_lag2 = (o_lag2 + c_lag2) / 2

    morning = bar2_red   & bar1_small & bar0_green & (c >= midpoint_lag2)
    evening = bar2_green & bar1_small & bar0_red   & (c <= midpoint_lag2)

    holding = int(params["holding_bars"])
    return pd.DataFrame({
        "entry_long":  morning.fillna(False).astype(bool),
        "entry_short": evening.fillna(False).astype(bool),
        "exit_long":   morning.shift(holding).fillna(False).astype(bool),
        "exit_short":  evening.shift(holding).fillna(False).astype(bool),
    }, index=df.index)
```

- [ ] **Step 3: Run + commit**

```bash
pytest tests/test_strategies.py -v
git -C D:/Plaios-tools/trading-tools add trading_tools/strategies/star.py tests/test_strategies.py
git -C D:/Plaios-tools/trading-tools commit -m "strategies: morning/evening star"
```

---

### Task 28: `three_soldiers_crows.py`

**Three white soldiers (long):** 3 consecutive green bars, each closing higher than the previous, each opening within the previous body.
**Three black crows (short):** mirror.

- [ ] **Step 1: Test**

Append to `tests/test_strategies.py`:
```python
def test_three_white_soldiers():
    """3 consecutive higher closes, each open within prior body."""
    df = pd.DataFrame({
        "open":  [100, 102, 105, 108],
        "high":  [104, 107, 110, 112],
        "low":   [99, 101, 104, 107],
        "close": [103, 106, 109, 111],   # bar 3 should fire entry_long
        "volume":[1_000_000] * 4,
    }, index=pd.date_range("2020-01-01", periods=4, freq="D"))

    from trading_tools.strategies.three_soldiers_crows import signal
    sig = signal(df, {"holding_bars": 2})
    assert bool(sig["entry_long"].iloc[3])
```

- [ ] **Step 2: Implement**

Create `trading_tools/strategies/three_soldiers_crows.py`:
```python
"""Three white soldiers / three black crows."""
import pandas as pd

from . import register


@register(
    name="three_soldiers_crows",
    description="Three consecutive higher (lower) closes with opens inside prior body.",
    direction="long_short",
    edge_status="folklore",
    edge_source="Bulkowski; common practitioner pattern, weak academic support.",
    default_params={"holding_bars": 5},
    asset_classes=["equity"],
    timeframes=["daily"],
)
def signal(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    o, c = df["open"], df["close"]
    green = c > o
    red   = c < o

    # Three consecutive same-direction bars with progressing closes
    soldiers = (
        green & green.shift(1) & green.shift(2)
        & (c > c.shift(1)) & (c.shift(1) > c.shift(2))
        & (o.between(o.shift(1), c.shift(1)))
        & (o.shift(1).between(o.shift(2), c.shift(2)))
    )
    crows = (
        red & red.shift(1) & red.shift(2)
        & (c < c.shift(1)) & (c.shift(1) < c.shift(2))
        & (o.between(c.shift(1), o.shift(1)))
        & (o.shift(1).between(c.shift(2), o.shift(2)))
    )

    holding = int(params["holding_bars"])
    return pd.DataFrame({
        "entry_long":  soldiers.fillna(False).astype(bool),
        "entry_short": crows.fillna(False).astype(bool),
        "exit_long":   soldiers.shift(holding).fillna(False).astype(bool),
        "exit_short":  crows.shift(holding).fillna(False).astype(bool),
    }, index=df.index)
```

- [ ] **Step 3: Run + commit**

```bash
pytest tests/test_strategies.py -v
git -C D:/Plaios-tools/trading-tools add trading_tools/strategies/three_soldiers_crows.py tests/test_strategies.py
git -C D:/Plaios-tools/trading-tools commit -m "strategies: three soldiers / three crows"
```

---

### Task 29: `double_top_bottom.py` — Bulkowski definition (5%+ correction)

**Double top (short):** two highs within 1.5% of each other, separated by a trough that's ≥ 5% below both highs. Confirmed when price closes below the trough.
**Double bottom (long):** mirror.

This needs more state than the other strategies — track local extrema across a `lookback` window.

- [ ] **Step 1: Test**

Append to `tests/test_strategies.py`:
```python
def test_double_bottom_basic():
    """Two lows ~equal, separated by a peak; then close above peak triggers entry."""
    closes = [100, 95, 90, 85, 90, 95, 90, 85, 90, 95, 100]
    n = len(closes)
    df = pd.DataFrame({
        "open":  closes, "high": [c + 0.5 for c in closes],
        "low":   [c - 0.5 for c in closes], "close": closes,
        "volume":[1_000_000] * n,
    }, index=pd.date_range("2020-01-01", periods=n, freq="D"))

    from trading_tools.strategies.double_top_bottom import signal
    sig = signal(df, {"lookback": 8, "trough_pct": 0.05, "tolerance_pct": 0.02})
    # Some entry_long fires after the second bottom
    assert sig["entry_long"].any()
```

- [ ] **Step 2: Implement**

Create `trading_tools/strategies/double_top_bottom.py`:
```python
"""Double top / double bottom (Bulkowski 5%+ correction definition).

Heuristic vectorized version: at each bar, look back `lookback` bars; identify
the rolling max and rolling min; check whether the current close confirms a
breakout pattern.
"""
import pandas as pd

from . import register
from ._base import rolling_high, rolling_low


@register(
    name="double_top_bottom",
    description="Double top → short on close below trough; double bottom → long on "
                "close above peak. Bulkowski 5%+ correction definition.",
    direction="long_short",
    edge_status="folklore",
    edge_source="Bulkowski (Encyclopedia of Chart Patterns) found marginal edge with "
                "strict definition.",
    default_params={"lookback": 60, "trough_pct": 0.05, "tolerance_pct": 0.015,
                    "holding_bars": 20},
    asset_classes=["equity"],
    timeframes=["daily"],
)
def signal(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    lookback = int(params["lookback"])
    trough_pct = float(params["trough_pct"])
    tolerance = float(params["tolerance_pct"])

    high = df["high"]
    low = df["low"]
    close = df["close"]

    rh = rolling_high(df, period=lookback, source="high")
    rl = rolling_low(df, period=lookback, source="low")
    rh_mid = (rolling_high(df, period=lookback // 2, source="high"))
    rl_mid = (rolling_low(df, period=lookback // 2, source="low"))

    # Double-bottom proxy: current close just exceeded the rolling high (peak between troughs)
    # AND rolling low ≈ recent low within tolerance AND drop ≥ trough_pct.
    drop_pct = (rh - rl) / rh
    near_low_again = (low - rl).abs() / rl <= tolerance

    long_break  = (close > rh.shift(1)) & near_low_again.shift(1).fillna(False) & (drop_pct >= trough_pct)
    short_break = (close < rl.shift(1)) & ((high - rh).abs() / rh <= tolerance).shift(1).fillna(False) & (drop_pct >= trough_pct)

    holding = int(params["holding_bars"])
    return pd.DataFrame({
        "entry_long":  long_break.fillna(False).astype(bool),
        "entry_short": short_break.fillna(False).astype(bool),
        "exit_long":   long_break.shift(holding).fillna(False).astype(bool),
        "exit_short":  short_break.shift(holding).fillna(False).astype(bool),
    }, index=df.index)
```

- [ ] **Step 3: Run + commit**

```bash
pytest tests/test_strategies.py -v
git -C D:/Plaios-tools/trading-tools add trading_tools/strategies/double_top_bottom.py tests/test_strategies.py
git -C D:/Plaios-tools/trading-tools commit -m "strategies: double top / double bottom (Bulkowski)"
```

---

### Task 30: `high_52w_breakout.py` — George & Hwang 2004

**Pattern:** close > rolling 252-day high (52-week-high breakout). Long-only. Exit when close drops below `exit_lookback`-day low (default 50).

> Spec note (Bar adjustment basis, decision 7b): level-based signals like "52w high" prefer **unadjusted** prices because splits artificially break levels. Strategy should declare `adjusted=False` preference; harness honours via the `adjusted` kwarg in `run_backtest`.

- [ ] **Step 1: Test**

Append to `tests/test_strategies.py`:
```python
def test_52w_breakout_fires_on_new_high():
    n = 260
    closes = [100.0] * 252 + [101.0, 102.0, 103.0, 110.0, 111.0, 112.0, 113.0, 114.0]
    df = pd.DataFrame({
        "open":  closes, "high": [c + 0.5 for c in closes],
        "low":   [c - 0.5 for c in closes], "close": closes,
        "volume":[1_000_000] * n,
    }, index=pd.date_range("2020-01-01", periods=n, freq="D"))

    from trading_tools.strategies.high_52w_breakout import signal
    sig = signal(df, {"lookback": 252, "exit_lookback": 50})
    # Entry should fire on the bar that first exceeds the 252-day high
    assert sig["entry_long"].iloc[252:].any()
```

- [ ] **Step 2: Implement**

Create `trading_tools/strategies/high_52w_breakout.py`:
```python
"""52-week-high breakout — George & Hwang 2004 ('The 52-Week High and Momentum
Investing', Journal of Finance). Stocks near 52w highs continue outperforming.

Long-only. Long entry when close > rolling 252-day high (excluding today).
Exit when close < rolling `exit_lookback`-day low.
"""
import pandas as pd

from . import register
from ._base import rolling_high, rolling_low


@register(
    name="high_52w_breakout",
    description="Long when close exceeds the rolling 252-day high. Exit on close "
                "below 50-day low.",
    direction="long",
    edge_status="documented",
    edge_source="George & Hwang 2004, 'The 52-Week High and Momentum Investing', "
                "Journal of Finance.",
    default_params={"lookback": 252, "exit_lookback": 50},
    asset_classes=["equity"],
    timeframes=["daily"],
)
def signal(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    lookback = int(params["lookback"])
    exit_lb = int(params["exit_lookback"])

    rh_prior = rolling_high(df, period=lookback, source="high").shift(1)
    rl_prior = rolling_low(df,  period=exit_lb, source="low").shift(1)

    entry_long = df["close"] > rh_prior
    exit_long  = df["close"] < rl_prior
    zeros = pd.Series(False, index=df.index)

    return pd.DataFrame({
        "entry_long":  entry_long.fillna(False).astype(bool),
        "entry_short": zeros,
        "exit_long":   exit_long.fillna(False).astype(bool),
        "exit_short":  zeros,
        "rh_252": rh_prior,
        "rl_50":  rl_prior,
    }, index=df.index)
```

- [ ] **Step 3: Run all strategy tests**

Run: `pytest tests/test_strategies.py -v`
Expected: all pass.

- [ ] **Step 4: Commit Phase 6**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/strategies/high_52w_breakout.py tests/test_strategies.py
git -C D:/Plaios-tools/trading-tools commit -m "strategies: 52w-high breakout (George & Hwang 2004)"
```

---

## Phase 7 — V2 baseline run

Goal: 251 backtest runs across 11 strategies × 25 universe symbols, plus the universal SPY-BH baseline. Eyeball results, set initial verdicts.

### Task 31: Add a small `run_baseline.py` driver

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\backtest\run_baseline.py`

- [ ] **Step 1: Implement**

Create `trading_tools/backtest/run_baseline.py`:
```python
"""V2 baseline run driver: spy_buy_hold (1) + asset_buy_hold (25) +
9 active strategies × 25 universe symbols = 251 runs total.

Rerunable: backtest_runs is append-only by design. A re-run just adds new
run_ids; existing rows are not altered.
"""
from __future__ import annotations

import logging
from datetime import date

from trading_tools.backtest.harness import run_backtest
from trading_tools.backtest.plots import generate_all
from trading_tools.universe import TOP_25

logger = logging.getLogger(__name__)

ACTIVE_STRATEGIES = [
    "ma_cross", "bb_meanrev", "bb_squeeze",
    "engulfing", "hammer", "star",
    "three_soldiers_crows", "double_top_bottom",
    "high_52w_breakout",
]

START = date(2010, 1, 1)
END = date(2026, 4, 29)


def main(*, generate_charts: bool = False) -> None:
    universe = list(TOP_25.keys())  # 25 symbols including SPY

    # 1. Universal SPY-BH baseline (one run)
    logger.info("baseline: spy_buy_hold on SPY")
    run_backtest("spy_buy_hold", "SPY", start=START, end=END)

    # 2. Asset-BH on every universe symbol (25 runs)
    for sym in universe:
        logger.info("baseline: asset_buy_hold on %s", sym)
        try:
            r = run_backtest("asset_buy_hold", sym, start=START, end=END)
            if generate_charts:
                generate_all(r)
        except Exception as exc:
            logger.error("asset_buy_hold %s failed: %s", sym, exc)

    # 3. 9 active × 25 = 225 runs
    for strat in ACTIVE_STRATEGIES:
        for sym in universe:
            logger.info("baseline: %s on %s", strat, sym)
            try:
                r = run_backtest(strat, sym, start=START, end=END)
                if generate_charts:
                    generate_all(r)
            except Exception as exc:
                logger.error("%s %s failed: %s", strat, sym, exc)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    main()
```

- [ ] **Step 2: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add trading_tools/backtest/run_baseline.py
git -C D:/Plaios-tools/trading-tools commit -m "backtest: V2 baseline runner"
```

---

### Task 32: Run the V2 baseline

**Files:** none (execution step).

- [ ] **Step 1: Run it**

Run from `D:\Plaios-tools\trading-tools`:
```
python -m trading_tools.backtest.run_baseline
```
Expected: ~251 log lines indicating each run; total wall time ~5-15 min depending on strategy complexity (chart generation off by default).

- [ ] **Step 2: Verify counts**

Run:
```
psql -d trading_data -c "SELECT COUNT(*) AS runs FROM backtest_runs;"
psql -d trading_data -c "SELECT COUNT(*) AS results FROM backtest_results;"
```
Expected: runs ≥ 251, results ≥ 753 (3× runs).

- [ ] **Step 3: Verify clean reproducibility metadata**

Run:
```
psql -d trading_data -c "SELECT COUNT(*) FROM backtest_runs WHERE git_dirty = false;"
```
Expected: ≥ 251 (all runs reproducible). If lower, the working tree was dirty during the run; commit pending changes and re-run.

- [ ] **Step 4: Spot-check the leaderboard**

Run:
```
psql -d trading_data -c "
  SELECT r.strategy, r.symbol, s.cagr, s.sharpe, s.max_drawdown,
         s.excess_return_vs_spy_bh
  FROM backtest_runs r JOIN backtest_results s
    ON s.run_id = r.run_id AND s.benchmark = 'strategy'
  ORDER BY s.cagr DESC NULLS LAST LIMIT 20;"
```
Eyeball: do the top entries make sense? Suspiciously high CAGR (>50%) on a folklore strategy may indicate look-ahead — investigate before recording verdicts.

- [ ] **Step 5: Generate charts for ~5 representative runs**

Pick interesting run_ids from the leaderboard. For each:
```
python -c "from trading_tools.backtest.harness import load_result; r=load_result(<id>); print(r['run']['artifact_dir'])"
```
Then run a one-off chart-only step (the harness in baseline mode skipped charts):
```python
# scratch.py
from trading_tools.backtest.harness import run_backtest
from trading_tools.backtest.plots import generate_all
from datetime import date
result = run_backtest("bb_squeeze", "AAPL", start=date(2010,1,1), end=date(2026,4,29))
generate_all(result)
print(result.artifact_dir)
```

Open the `summary.html` for each in a browser. Confirm trade markers land where logic predicts.

- [ ] **Step 6: Record initial verdicts**

For each strategy in `{ma_cross, bb_meanrev, bb_squeeze, engulfing, hammer, star, three_soldiers_crows, double_top_bottom, high_52w_breakout}`, look at the median run vs SPY-BH. Use the CLI to record:
```
python -m trading_tools verdict <run_id> --verdict no_edge --decision shelf --note "<short reason>"
```
Verdict guide:
- `edge`: median run beats SPY-BH AND IR > 0.3
- `no_edge`: median run trails SPY-BH consistently
- `inconclusive`: noisy / mixed across symbols
- `benchmark`: only spy_buy_hold and asset_buy_hold get this

For the two `*_buy_hold` strategies, set verdict=`benchmark`, decision=`benchmark`.

- [ ] **Step 7: Commit Phase 7**

```bash
git -C D:/Plaios-tools/trading-tools commit --allow-empty -m "v2 baseline: 251 runs across 11 strategies × 25 symbols, initial verdicts"
```

---

## Phase 8 — V2 closeout

Goal: notebook iteration surface, per-strategy one-pager docs, project-state and decisions updates, GitHub push, PLAIOS memory update.

### Task 33: Create `notebooks/explore.ipynb`

**Files:**
- Create: `D:\Plaios-tools\trading-tools\notebooks\explore.ipynb`

- [ ] **Step 1: Create the notebook scaffold**

Use Jupyter to create a fresh notebook at `D:/Plaios-tools/trading-tools/notebooks/explore.ipynb` with these cells (each as a separate code cell):

**Cell 1 — setup:**
```python
%load_ext autoreload
%autoreload 2

import sys
sys.path.insert(0, "..")

from datetime import date
import pandas as pd
from trading_tools.backtest.harness import run_backtest, list_runs, load_result, compare, set_verdict
from trading_tools.backtest.plots import generate_all
from trading_tools.strategies import REGISTRY
from trading_tools.universe import TOP_25
```

**Cell 2 — list registered strategies:**
```python
import importlib
for name in ["spy_buy_hold","asset_buy_hold","ma_cross","bb_meanrev","bb_squeeze",
             "engulfing","hammer","star","three_soldiers_crows",
             "double_top_bottom","high_52w_breakout"]:
    importlib.import_module(f"trading_tools.strategies.{name}")

pd.DataFrame([
    {"name": m.name, "direction": m.direction, "edge_status": m.edge_status,
     "default_params": m.default_params}
    for m in REGISTRY.values()
])
```

**Cell 3 — scoreboard:**
```python
runs = list_runs()
runs.sort_values("cagr", ascending=False).head(20)
```

**Cell 4 — sweep params on one strategy:**
```python
for period in (10, 20, 30, 50):
    r = run_backtest("bb_squeeze", "NVDA",
                     start=date(2010,1,1), end=date(2026,4,29),
                     params={"period": period})
    strat = next(x for x in r.rows if x.benchmark == "strategy")
    print(f"period={period:3d}  CAGR={strat.cagr:+.4f}  Sharpe={strat.sharpe:+.3f}")
```

**Cell 5 — compare two runs:**
```python
# pick two run_ids from the leaderboard
compare(<id_a>, <id_b>)
```

**Cell 6 — render charts for an interesting run:**
```python
result = run_backtest("bb_squeeze", "NVDA", start=date(2010,1,1), end=date(2026,4,29))
generate_all(result)
print(f"open: {result.artifact_dir / 'summary.html'}")
```

- [ ] **Step 2: Run end-to-end**

Open the notebook in Jupyter, run all cells, ensure no kernel errors:
```
jupyter notebook D:/Plaios-tools/trading-tools/notebooks/explore.ipynb
```

- [ ] **Step 3: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add notebooks/explore.ipynb
git -C D:/Plaios-tools/trading-tools commit -m "notebooks: explore.ipynb iteration surface"
```

---

### Task 34: Create `docs/strategies.md`

**Files:**
- Create: `D:\Plaios-tools\trading-tools\docs\strategies.md`

- [ ] **Step 1: Generate baseline content from REGISTRY + DB**

Run this scratch script to dump current state:
```python
# scratch_strategies_md.py
import importlib
from trading_tools.strategies import REGISTRY
for n in ["spy_buy_hold","asset_buy_hold","ma_cross","bb_meanrev","bb_squeeze",
          "engulfing","hammer","star","three_soldiers_crows","double_top_bottom",
          "high_52w_breakout"]:
    importlib.import_module(f"trading_tools.strategies.{n}")

for m in REGISTRY.values():
    print(f"## `{m.name}`\n")
    print(f"**Direction:** {m.direction}  ")
    print(f"**Edge status:** {m.edge_status}  ")
    print(f"**Default params:** `{m.default_params}`  ")
    print(f"**Source:** {m.edge_source or '—'}\n")
    print(f"{m.description}\n")
```

- [ ] **Step 2: Write `docs/strategies.md`**

Create `D:\Plaios-tools\trading-tools\docs\strategies.md` with:
- A header explaining what the file is (auto-doc of the registry).
- The 11 entries pasted from the script above.
- Per entry, append a "Baseline result" line: pull the median CAGR vs SPY-BH from `backtest_runs` joined to `backtest_results` (run a SQL query, paste the values).

Skeleton:
```markdown
# Strategies — V2 Baseline (2026-05-01)

One-pager per registered strategy. Generated from REGISTRY + the V2 baseline run
results. Baseline window: 2010-01-01 → 2026-04-29. Universe: 25 S&P/QQQ-overlap names.

(... 11 sections as generated by the scratch script, with a "Baseline result"
line added showing median CAGR / Sharpe vs SPY-BH ...)
```

- [ ] **Step 3: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add docs/strategies.md
git -C D:/Plaios-tools/trading-tools commit -m "docs: strategies.md one-pager per registered strategy"
```

---

### Task 35: Update `docs/project-state.md` and `docs/decisions.md`

**Files:**
- Modify: `D:\Plaios-tools\trading-tools\docs\project-state.md`
- Modify: `D:\Plaios-tools\trading-tools\docs\decisions.md`

- [ ] **Step 1: Rewrite `docs/project-state.md` to reflect V2-complete state**

Replace contents with V2 status:
- Last updated: 2026-05-01 (V2 build complete)
- What exists: V1 substrate + strategies (11) + backtest harness + plotting + 251 baseline runs
- Tables: instruments, equity_bars, index_bars, strategies, backtest_runs, backtest_results
- Code: V1 modules + `universe.py`, `strategies/`, `backtest/`, `notebooks/explore.ipynb`
- What's planned (loose): V2.5 fundamentals, V2.6 IPO/float, V3 options + VWEMA-BB + PipBoy port, V4 ESG falsification
- Known gaps / debt:
  - Universe is hardcoded TOP_25 as of 2026-04-30 — survivorship bias acknowledged
  - Synthetic shorts (no borrow fee) — V3 swaps in put-spreads
  - No `cleanup-runs` GC for `runs/` directory yet
  - `KNOWN_INSTRUMENTS` still in `cli.py`, but now sourced from `universe.TOP_25`
  - Bar-adjustment basis: harness defaults to `adjusted=True`; level-based strategies (`high_52w_breakout`) should be re-run with `adjusted=False` when V2.5 lands

- [ ] **Step 2: Append V2 decisions to `docs/decisions.md`**

Append one entry per locked decision in the V2 spec (see spec § "Decisions Locked In"). Each entry:
```markdown
## YYYY-MM-DD — <decision>

**Decision:** <choice>
**Rationale:** <reason>
```

- [ ] **Step 3: Commit**

```bash
git -C D:/Plaios-tools/trading-tools add docs/project-state.md docs/decisions.md
git -C D:/Plaios-tools/trading-tools commit -m "docs: V2 project-state + decisions"
```

---

### Task 36: Push to GitHub

**Files:** none.

- [ ] **Step 1: Push**

Run:
```
git -C D:/Plaios-tools/trading-tools push origin main
```
Expected: commits land on `Sc07713/trading-tools` (the existing private GitHub repo from V1).

- [ ] **Step 2: Verify on GitHub UI**

Open: https://github.com/Sc07713/trading-tools
Expected: V2 commits visible, `strategies/` and `backtest/` directories present.

---

### Task 37: Update PLAIOS memory

**Files:**
- Modify: `C:\Users\smckennie\.claude\projects\D--PLAIOS\memory\MEMORY.md`
- Modify or create: `C:\Users\smckennie\.claude\projects\D--PLAIOS\memory\project_trading_tools_v2_built.md`

- [ ] **Step 1: Create the project-memory file**

Write `memory\project_trading_tools_v2_built.md`:
```markdown
---
name: trading-tools V2 — built and pushed
description: V2 (strategy register + backtest harness + 11 seed strategies + 251 baseline runs) shipped 2026-05-01
type: project
---

V2 lands strategy register + backtest harness on top of V1 data substrate.

- DB additions: `strategies`, `backtest_runs`, `backtest_results` (3 rows per run)
- Universe: TOP_25 hardcoded (S&P/QQQ overlap, 2026-04-30)
- 11 seed strategies shipped: 2 benchmarks (`spy_buy_hold`, `asset_buy_hold`),
  1 documented (52w-high), 2 falsification (BB mean-reversion, BB squeeze),
  2 mixed-lit (engulfing, star), 4 folklore (MA cross, hammer, three soldiers/crows, double top/bottom)
- Baseline: 251 runs × 3 benchmarks = 753 result rows; verdicts recorded
- Test DB isolation fixed: `trading_data_test` now isolates pytest from production data
- Spec: `D:\PLAIOS\docs\superpowers\specs\2026-05-01-trading-tools-v2-design.md`
- Plan: `D:\PLAIOS\docs\superpowers\plans\2026-05-01-trading-tools-v2.md`
- Repo: `D:\Plaios-tools\trading-tools\` — pushed to `Sc07713/trading-tools`
```

- [ ] **Step 2: Add the index entry**

In `MEMORY.md`, replace the `[Trading-tools V1 — built and pushed]` line with two entries:
```markdown
- [Trading-tools V1 — built and pushed](project_trading_tools_v1_built.md) — D:\Plaios-tools\trading-tools\ (master), GitHub Sc07713/trading-tools (private), pg17:5432 trading_data with SPY/NVDA/VIX 20Y daily+weekly bars
- [Trading-tools V2 — built and pushed](project_trading_tools_v2_built.md) — Strategy register + backtest harness + 11 seed strategies + 251 baseline runs (2026-05-01)
```

If a single combined entry is preferred, just update the V1 entry to mention V2 instead.

- [ ] **Step 3: Mirror memory to repo and commit (PLAIOS-side)**

Per the close-out protocol memory:
```bash
robocopy "C:\Users\smckennie\.claude\projects\D--PLAIOS\memory" "D:\PLAIOS\memory" /MIR /XF "*.tmp"
git -C D:/PLAIOS add memory/ docs/superpowers/plans/2026-05-01-trading-tools-v2.md
git -C D:/PLAIOS commit -m "memory: trading-tools V2 built; plan committed"
```

- [ ] **Step 4: Final close-out commit on the trading-tools repo**

```bash
git -C D:/Plaios-tools/trading-tools commit --allow-empty -m "docs + notebook: V2 closeout"
git -C D:/Plaios-tools/trading-tools push origin main
```

---

## Self-Review Checklist

Run through this before declaring the plan complete:

- [ ] **Spec coverage:**
  - § Universe expansion → Task 1
  - § Ingest hardening (--since + retry) → Tasks 2, 3
  - § Strategy register → Tasks 5, 6, 7
  - § Backtest harness → Tasks 11-14
  - § 3-way benchmark → Tasks 13, 15
  - § Reproducibility → Tasks 11, 16
  - § Per-run artifacts → Task 14 (parquets, summary.json) + Task 20 (charts, summary.html)
  - § Verdict/decision → Tasks 14 (`set_verdict`), 17 (CLI), 32 (record initial verdicts)
  - § 11 seed strategies → Tasks 8, 22, 23, 24-30
  - § Two consumer surfaces (CLI + notebook) → Tasks 17, 33
  - § Visualisation (3 plotly + 2 mpl + summary.html) → Task 20
  - § Test DB isolation → Task 9
  - § V2 baseline → Tasks 31, 32
  - § Closeout (notebook, strategies.md, project-state, decisions, push, memory) → Tasks 33-37

- [ ] **No placeholders:** every code step contains the actual code; no "TBD", "implement later", or "similar to Task N".

- [ ] **Type consistency:**
  - Strategy fn: `signal(df, params) -> DataFrame` everywhere ✓
  - Required cols: `entry_long, entry_short, exit_long, exit_short` ✓
  - Bollinger primitive: `bollinger_bands(df, period=20, stddev=2.0, source_low='low', source_high='high')` returns columns `{lower, middle, upper}` ✓
  - Harness: `run_backtest(strategy, symbol, start, end, *, timeframe, params, direction_override, adjusted)` ✓
  - Result dataclass + benchmarks list[BenchmarkRow] ✓
  - run_id is BIGSERIAL int ✓
  - 3 rows in backtest_results per run, benchmark ∈ {strategy, spy_bh, asset_bh} ✓

- [ ] **TDD discipline:** each task starts with a failing test, then implementation, then re-run.

- [ ] **Frequent commits:** every task ends with a commit; phase ends with an empty marker commit when needed.

- [ ] **Reversibility:** Phase boundaries match spec § Reversibility table.

---

*End of plan. Each task is independently runnable; the suggested execution order is sequential by phase, but Phase 6 strategy tasks (24-30) are independent of each other and could be parallelized once Phase 5 lands.*

