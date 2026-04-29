# trading-tools V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the data substrate at `D:\Plaios-tools\trading-tools\` — Postgres-backed ingestion of daily and weekly OHLCV bars for SPY, NVDA, VIX from Interactive Brokers, with gap detection and idempotent upserts.

**Architecture:** Flat 4-module Python package (`db.py`, `ib_data.py`, `cli.py`, `schema.sql`) inside `trading_tools/`. Per-asset-class fact tables (`equity_bars`, `index_bars`) plus `instruments` dimension. Dynamic SQL with `dict` rows in/out via psycopg3 — no schema-mirror dataclasses. Read-only IB account enforced by import discipline (order classes never imported).

**Tech Stack:** Python 3.13, `ib-async`, `psycopg[binary]` (psycopg3), `pandas-market-calendars`, `python-dotenv`, `pytest`, Postgres 18.

**Spec:** `D:\PLAIOS\docs\superpowers\specs\2026-04-29-trading-tools-v1-design.md` — read this first.

---

## File Structure

Files this plan creates (all under `D:\Plaios-tools\trading-tools\`):

```
trading-tools/
├── trading_tools/
│   ├── __init__.py            # empty
│   ├── __main__.py            # enables `python -m trading_tools <subcommand>`
│   ├── schema.sql             # idempotent DDL (instruments, equity_bars, index_bars)
│   ├── db.py                  # init_schema, query, execute, upsert_instruments, upsert_bars, check_gaps
│   ├── ib_data.py             # fetch_bars(...) → list[dict]; read-only IB imports only
│   └── cli.py                 # KNOWN_INSTRUMENTS, ingest(), check_gaps_cmd(), argparse setup
├── tests/
│   ├── __init__.py            # empty
│   ├── conftest.py            # pytest fixtures (DB connection)
│   ├── test_db.py             # unit tests for db.py (use a test DB schema)
│   └── test_smoke.py          # integration test: live IB → DB → query → assert
├── docs/
│   ├── project-state.md       # populated in Task 13
│   └── decisions.md           # populated in Task 13
├── .gitignore
├── .env.example
├── .env                       # gitignored — created at runtime, contains real creds
├── pyproject.toml
├── README.md
└── CLAUDE.md                  # agent prompt (v4 + pedagogical extension)
```

**Responsibility per file:**
- `schema.sql` — single source of truth for DB structure
- `db.py` — all Postgres I/O; pure data layer; no IB awareness
- `ib_data.py` — all IB I/O; pure fetch layer; no DB awareness; **read-only imports only**
- `cli.py` — orchestration; the only file that knows about both IB and DB; instrument metadata bootstrap
- `__main__.py` — argparse-free thin wrapper that delegates to `cli.main()`
- `conftest.py` — pytest test DB setup/teardown
- `test_db.py` — unit tests for `db.py` functions against a test DB
- `test_smoke.py` — full-loop integration test (live IB required)

---

## Tasks

### Task 1: Initialize repo and Python environment

**Files:**
- Create: `D:\Plaios-tools\trading-tools\.gitignore`
- Create: `D:\Plaios-tools\trading-tools\pyproject.toml`
- Create: `D:\Plaios-tools\trading-tools\.env.example`

- [ ] **Step 1: Create the parent and repo directories**

Run from any shell with write access to `D:\`:
```bash
mkdir -p "D:/Plaios-tools/trading-tools"
cd "D:/Plaios-tools/trading-tools"
git init
```
Expected: `Initialized empty Git repository in D:/Plaios-tools/trading-tools/.git/`

- [ ] **Step 2: Write `.gitignore`**

Create `D:\Plaios-tools\trading-tools\.gitignore`:
```
.env
.venv/
__pycache__/
*.py[cod]
*.egg-info/
*.log
dist/
build/
.pytest_cache/
.coverage
```

- [ ] **Step 3: Write `pyproject.toml`**

Create `D:\Plaios-tools\trading-tools\pyproject.toml`:
```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "trading-tools"
version = "0.1.0"
description = "Market data ingestion substrate for the PLAIOS trading domain"
authors = [{name = "Scott McKennie"}]
requires-python = ">=3.13"
dependencies = [
    "ib-async>=1.0.3",
    "psycopg[binary]>=3.2.0",
    "pandas-market-calendars>=4.4.0",
    "python-dotenv>=1.0.1",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
]

[tool.setuptools.packages.find]
include = ["trading_tools*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

- [ ] **Step 4: Create venv and install**

Run from `D:\Plaios-tools\trading-tools\`:
```bash
"C:/Python313/python.exe" -m venv .venv
.venv/Scripts/python.exe -m pip install --upgrade pip
.venv/Scripts/python.exe -m pip install -e ".[dev]"
```
Expected: `Successfully installed ib-async-... psycopg-... pandas-market-calendars-... python-dotenv-... pytest-...`

- [ ] **Step 5: Write `.env.example`**

Create `D:\Plaios-tools\trading-tools\.env.example`:
```
# Postgres connection
DATABASE_URL=postgresql://USER:PASSWORD@127.0.0.1:5432/trading_data

# Interactive Brokers (TWS/Gateway must be running)
IB_HOST=127.0.0.1
IB_PORT=8000
IB_CLIENT_ID=1
```

- [ ] **Step 6: Commit**

```bash
git add .gitignore pyproject.toml .env.example
git commit -m "chore: scaffold pyproject + venv + gitignore + env template"
```
Expected: a commit with 3 files added.

---

### Task 2: Project metadata (README, CLAUDE.md, package skeleton)

**Files:**
- Create: `D:\Plaios-tools\trading-tools\README.md`
- Create: `D:\Plaios-tools\trading-tools\CLAUDE.md`
- Create: `D:\Plaios-tools\trading-tools\trading_tools\__init__.py`
- Create: `D:\Plaios-tools\trading-tools\trading_tools\__main__.py`
- Create: `D:\Plaios-tools\trading-tools\tests\__init__.py`
- Create: `D:\Plaios-tools\trading-tools\docs\project-state.md`
- Create: `D:\Plaios-tools\trading-tools\docs\decisions.md`

- [ ] **Step 1: Create empty package and tests dirs**

```bash
mkdir -p trading_tools tests docs
touch trading_tools/__init__.py tests/__init__.py
```

- [ ] **Step 2: Write `trading_tools/__main__.py`** (so `python -m trading_tools` works)

```python
"""Allow `python -m trading_tools <subcommand>` to delegate to cli.main()."""
from trading_tools.cli import main

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Write `README.md`**

```markdown
# trading-tools

Market data ingestion substrate for the PLAIOS trading domain.
Pulls daily and weekly OHLCV bars from Interactive Brokers into a Postgres database, with gap detection and idempotent upserts.

V1 scope: data ingestion only. SPY, NVDA, VIX. See `D:\PLAIOS\docs\superpowers\specs\2026-04-29-trading-tools-v1-design.md` for the design spec.

## Setup

1. Install Postgres 18 (already installed at `C:\Program Files\PostgreSQL\18\`).
2. Create the database:
   ```
   "C:/Program Files/PostgreSQL/18/bin/createdb.exe" -U postgres trading_data
   ```
3. Copy `.env.example` to `.env` and fill in your `DATABASE_URL` and IB connection details.
4. Create venv and install:
   ```
   "C:/Python313/python.exe" -m venv .venv
   .venv/Scripts/python.exe -m pip install -e ".[dev]"
   ```
5. Initialize the schema:
   ```
   .venv/Scripts/python.exe -c "from trading_tools.db import init_schema; init_schema()"
   ```

## Run

Start TWS or IB Gateway with API enabled on port 8000 (or whatever you set in `.env`). Then:

```
.venv/Scripts/python.exe -m trading_tools ingest --symbols SPY,NVDA,VIX
.venv/Scripts/python.exe -m trading_tools check-gaps --symbols SPY,NVDA,VIX
```

## Test

```
.venv/Scripts/python.exe -m pytest
```

The smoke test requires live IB and a populated DB.
```

- [ ] **Step 4: Write `CLAUDE.md`**

This embeds the v4 Cybernetic Trader-Analyst system prompt the user provided in their original brief, plus the project-context block, pedagogical directive, and safety reminders per the spec's Appendix A.

```markdown
# trading-tools — Agent Operating Instructions

## Project Context

Repo: `D:\Plaios-tools\trading-tools\`
Owner: Scott McKennie
Domain: Trading (PLAIOS-side `domains/trading/`, currently legacy artefacts only)

**Current state:** V1 — data ingestion. SPY, NVDA, VIX. Daily and weekly bars in Postgres. Read this repo's `docs/project-state.md` before any substantive change.

**Future phases:**
- V2 — strategy register + backtest harness (validation case: VWEMA-BB algo at `D:\PLAIOS\domains\trading\legacy\algos\VWEMA-BB-momentum-strategy.pine`)
- V3 — pillar gates, cross-cutting vol/volume signal layers, flow detection, stance arbitration
- V4+ — decisions, advisory

**Living docs:**
- `docs/project-state.md` — current state of the repo (updated each session)
- `docs/decisions.md` — append-only decision log

---

## Pedagogical Directive

When introducing or proposing any signal, indicator, strategy, or factor: **cite the documented source of edge** — academic paper, replication study, or practitioner reference. When proposing a backtest: **frame it as a falsification test** — what would have to be true in the data for this edge to NOT exist? Report results honestly: did the edge replicate, decay, or never exist in our sample? **Distinguish documented edges from folklore patterns explicitly.** Do not present untested chart patterns or unsourced "rules" as edge.

---

## Anti-Patterns (zero-tolerance)

- No single-pillar theses (per v4 prompt below)
- No backtest results without reproducibility metadata: `run_id`, `code_hash`, timestamp, params
- Sub-30 occurrences = anecdote, not edge — flag explicitly in any reported result
- Pooled stats across mixed regimes = misleading — segment by regime always

---

## Safety Discipline (CODE-LEVEL)

`ib_data.py` (and any other module that touches IB) imports **only** the historical-data classes from `ib_async`:

```python
from ib_async import IB, Stock, Index, util  # ← allowed
# from ib_async import MarketOrder, LimitOrder, ...  ← FORBIDDEN
```

Even if a typo or an LLM-generated edit calls an order method, it must `NameError`, not fire an order. **This is V1 read-only safety.** When V4+ adds order placement, it will live in a separate module with explicit boundaries.

---

## Agent Identity — Cybernetic Trader-Analyst v4

[The full v4 prompt is preserved verbatim at:
`D:\PLAIOS\domains\trading\reference\cybernetic-trader-analyst-prompt-v4.md`

When generating CLAUDE.md, COPY the entire contents of that file inline at this point in CLAUDE.md (do not just link — embed verbatim, since CLAUDE.md should be self-contained). Skip the `# Cybernetic Trader-Analyst — System Prompt v4` H1 header at the very top of the source file when embedding (the H2 above already labels this section).]
```

**Note for implementer:** the v4 prompt source is at `D:\PLAIOS\domains\trading\reference\cybernetic-trader-analyst-prompt-v4.md` (saved 2026-04-29). Read that file and paste its contents in place of the `[...]` block above. Use the Read tool to load it, then the Edit/Write tool to insert it into the in-progress CLAUDE.md.

- [ ] **Step 5: Create empty `docs/project-state.md` placeholder**

Create `D:\Plaios-tools\trading-tools\docs\project-state.md`:
```markdown
# Project State

Populated at end of V1 build (Task 13). Until then, see the design spec at `D:\PLAIOS\docs\superpowers\specs\2026-04-29-trading-tools-v1-design.md`.
```

- [ ] **Step 6: Create empty `docs/decisions.md` placeholder**

Create `D:\Plaios-tools\trading-tools\docs\decisions.md`:
```markdown
# Decision Log

Append-only. Newest entries at top. Each entry: date, decision, context, alternatives, reasoning, revisit-if.

Populated at end of V1 build (Task 13).
```

- [ ] **Step 7: Commit**

```bash
git add README.md CLAUDE.md trading_tools/ tests/ docs/
git commit -m "chore: package skeleton + README + CLAUDE.md + docs placeholders"
```

---

### Task 3: Database schema and `db.init_schema()`

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\schema.sql`
- Create: `D:\Plaios-tools\trading-tools\trading_tools\db.py` (initial — `init_schema()` and connection helper only)

- [ ] **Step 1: Create the database manually (one-time setup)**

Run (replace `<password>` with the postgres user password set during install):
```bash
"C:/Program Files/PostgreSQL/18/bin/createdb.exe" -U postgres trading_data
```
Expected: prompt for password, then no output (success).

Verify:
```bash
"C:/Program Files/PostgreSQL/18/bin/psql.exe" -U postgres -l | grep trading_data
```
Expected: a line listing `trading_data | postgres | UTF8 | ...`.

- [ ] **Step 2: Set the `DATABASE_URL` in `.env`**

Create `D:\Plaios-tools\trading-tools\.env`:
```
DATABASE_URL=postgresql://postgres:<your-password>@127.0.0.1:5432/trading_data
IB_HOST=127.0.0.1
IB_PORT=8000
IB_CLIENT_ID=1
```

- [ ] **Step 3: Write `trading_tools/schema.sql`**

```sql
-- trading-tools V1 schema
-- Idempotent: safe to re-run.

CREATE TABLE IF NOT EXISTS instruments (
    symbol       TEXT        PRIMARY KEY,
    sec_type     TEXT        NOT NULL,
    exchange     TEXT        NOT NULL,
    currency     TEXT        NOT NULL,
    asset_class  TEXT        NOT NULL,
    first_seen   DATE        NOT NULL,
    last_updated TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS equity_bars (
    symbol       TEXT        NOT NULL REFERENCES instruments(symbol),
    timeframe    TEXT        NOT NULL,
    ts           DATE        NOT NULL,
    adjusted     BOOLEAN     NOT NULL,
    open         NUMERIC(18,6),
    high         NUMERIC(18,6),
    low          NUMERIC(18,6),
    close        NUMERIC(18,6),
    volume       BIGINT      NOT NULL,
    source       TEXT        NOT NULL,
    ingested_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (symbol, timeframe, ts, adjusted)
);

CREATE INDEX IF NOT EXISTS equity_bars_symbol_ts_idx
    ON equity_bars(symbol, timeframe, ts DESC);

CREATE TABLE IF NOT EXISTS index_bars (
    symbol       TEXT        NOT NULL REFERENCES instruments(symbol),
    timeframe    TEXT        NOT NULL,
    ts           DATE        NOT NULL,
    open         NUMERIC(18,6),
    high         NUMERIC(18,6),
    low          NUMERIC(18,6),
    close        NUMERIC(18,6),
    source       TEXT        NOT NULL,
    ingested_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (symbol, timeframe, ts)
);

CREATE INDEX IF NOT EXISTS index_bars_symbol_ts_idx
    ON index_bars(symbol, timeframe, ts DESC);
```

- [ ] **Step 4: Write `trading_tools/db.py` (skeleton + `init_schema`)**

```python
"""Postgres data layer for trading-tools.

All Postgres I/O lives here. No IB awareness.
Pattern: dynamic SQL with dict rows in/out via psycopg3.
"""
from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()
logger = logging.getLogger(__name__)

DATABASE_URL = os.environ["DATABASE_URL"]
SCHEMA_SQL_PATH = Path(__file__).parent / "schema.sql"


@contextmanager
def get_connection():
    """Yield a psycopg3 connection with dict_row factory. Auto-closes."""
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        yield conn


def init_schema() -> None:
    """Apply schema.sql idempotently. Safe to run repeatedly."""
    sql_text = SCHEMA_SQL_PATH.read_text(encoding="utf-8")
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql_text)
        conn.commit()
    logger.info("schema applied from %s", SCHEMA_SQL_PATH)
```

- [ ] **Step 5: Run `init_schema()` and verify**

```bash
.venv/Scripts/python.exe -c "from trading_tools.db import init_schema; init_schema()"
```
Expected: no error.

Verify in psql:
```bash
"C:/Program Files/PostgreSQL/18/bin/psql.exe" -U postgres -d trading_data -c "\dt"
```
Expected output (rows for `instruments`, `equity_bars`, `index_bars` in `public` schema).

- [ ] **Step 6: Commit**

```bash
git add trading_tools/schema.sql trading_tools/db.py
git commit -m "db: schema (instruments, equity_bars, index_bars) + init_schema()"
```

---

### Task 4: `db.query()` and `db.execute()` generic helpers

**Files:**
- Modify: `D:\Plaios-tools\trading-tools\trading_tools\db.py` (append two functions)

- [ ] **Step 1: Add `query()` and `execute()` to `db.py`**

Append at the end of `trading_tools/db.py`:

```python
def query(sql_str: str, params: tuple = ()) -> list[dict]:
    """Run any SELECT, return list of dict rows. Caller writes the SQL."""
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql_str, params)
        return cur.fetchall()


def execute(sql_str: str, params: tuple = ()) -> int:
    """Run any DML/DDL, return rowcount. Auto-commits."""
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql_str, params)
        rowcount = cur.rowcount
        conn.commit()
        return rowcount
```

- [ ] **Step 2: Verify by querying the empty `instruments` table**

```bash
.venv/Scripts/python.exe -c "from trading_tools.db import query; print(query('SELECT * FROM instruments'))"
```
Expected: `[]`

- [ ] **Step 3: Commit**

```bash
git add trading_tools/db.py
git commit -m "db: generic query() and execute() with dict rows"
```

---

### Task 5: `db.upsert_instruments()` with TDD

**Files:**
- Create: `D:\Plaios-tools\trading-tools\tests\conftest.py`
- Create: `D:\Plaios-tools\trading-tools\tests\test_db.py`
- Modify: `D:\Plaios-tools\trading-tools\trading_tools\db.py` (append function)

- [ ] **Step 1: Write `tests/conftest.py` (DB cleanup fixture)**

```python
"""Pytest fixtures for trading_tools.

The `clean_db` fixture truncates all tables in dependency order before each test.
Tests run against the real `trading_data` database (no mocking — psycopg3 is fast
enough that real connections are fine for V1's small test suite).
"""
import pytest

from trading_tools.db import execute, init_schema


@pytest.fixture(autouse=True)
def clean_db():
    """Ensure schema exists, then truncate all tables before each test."""
    init_schema()
    # Order matters: bars FK reference instruments
    execute("TRUNCATE equity_bars, index_bars, instruments RESTART IDENTITY CASCADE")
    yield
```

- [ ] **Step 2: Write the failing test for `upsert_instruments`**

Create `tests/test_db.py`:

```python
"""Unit tests for trading_tools.db functions."""
from datetime import date

from trading_tools import db


def test_upsert_instruments_inserts_new_rows():
    rows = [
        {"symbol": "SPY", "sec_type": "STK", "exchange": "ARCA",
         "currency": "USD", "asset_class": "equity",
         "first_seen": date(1993, 1, 29)},
        {"symbol": "VIX", "sec_type": "IND", "exchange": "CBOE",
         "currency": "USD", "asset_class": "index",
         "first_seen": date(1990, 1, 2)},
    ]
    n = db.upsert_instruments(rows)
    assert n == 2

    stored = db.query("SELECT symbol, asset_class FROM instruments ORDER BY symbol")
    assert stored == [
        {"symbol": "SPY", "asset_class": "equity"},
        {"symbol": "VIX", "asset_class": "index"},
    ]


def test_upsert_instruments_updates_existing_row():
    initial = [{"symbol": "SPY", "sec_type": "STK", "exchange": "ARCA",
                "currency": "USD", "asset_class": "equity",
                "first_seen": date(1993, 1, 29)}]
    db.upsert_instruments(initial)

    revised = [{"symbol": "SPY", "sec_type": "STK", "exchange": "NYSE",  # exchange changed
                "currency": "USD", "asset_class": "equity",
                "first_seen": date(1993, 1, 29)}]
    n = db.upsert_instruments(revised)
    assert n == 1

    rows = db.query("SELECT exchange FROM instruments WHERE symbol = 'SPY'")
    assert rows[0]["exchange"] == "NYSE"
```

- [ ] **Step 3: Run test, confirm it fails with AttributeError**

```bash
.venv/Scripts/python.exe -m pytest tests/test_db.py::test_upsert_instruments_inserts_new_rows -v
```
Expected: `AttributeError: module 'trading_tools.db' has no attribute 'upsert_instruments'`

- [ ] **Step 4: Implement `upsert_instruments`**

Append to `trading_tools/db.py`:

```python
from psycopg import sql as _sql


def upsert_instruments(rows: list[dict]) -> int:
    """Bulk upsert into `instruments`. ON CONFLICT (symbol) DO UPDATE.
    Returns total rowcount affected."""
    if not rows:
        return 0
    cols = ["symbol", "sec_type", "exchange", "currency", "asset_class", "first_seen"]
    insert_sql = _sql.SQL(
        "INSERT INTO instruments ({cols}) VALUES ({placeholders}) "
        "ON CONFLICT (symbol) DO UPDATE SET "
        "sec_type=EXCLUDED.sec_type, exchange=EXCLUDED.exchange, "
        "currency=EXCLUDED.currency, asset_class=EXCLUDED.asset_class, "
        "first_seen=EXCLUDED.first_seen, last_updated=NOW()"
    ).format(
        cols=_sql.SQL(",").join(_sql.Identifier(c) for c in cols),
        placeholders=_sql.SQL(",").join(_sql.Placeholder(c) for c in cols),
    )
    with get_connection() as conn, conn.cursor() as cur:
        cur.executemany(insert_sql, rows)
        conn.commit()
        return cur.rowcount
```

- [ ] **Step 5: Run tests, confirm both pass**

```bash
.venv/Scripts/python.exe -m pytest tests/test_db.py -v
```
Expected: both tests PASS.

- [ ] **Step 6: Commit**

```bash
git add tests/conftest.py tests/test_db.py trading_tools/db.py
git commit -m "db: upsert_instruments + tests"
```

---

### Task 6: `db.upsert_bars()` generic with whitelist (TDD)

**Files:**
- Modify: `D:\Plaios-tools\trading-tools\tests\test_db.py`
- Modify: `D:\Plaios-tools\trading-tools\trading_tools\db.py`

- [ ] **Step 1: Write the failing tests for `upsert_bars`**

Append to `tests/test_db.py`:

```python
def test_upsert_bars_equity_inserts():
    db.upsert_instruments([
        {"symbol": "SPY", "sec_type": "STK", "exchange": "ARCA",
         "currency": "USD", "asset_class": "equity",
         "first_seen": date(1993, 1, 29)},
    ])
    bars = [
        {"symbol": "SPY", "timeframe": "daily", "ts": date(2026, 4, 28),
         "adjusted": True, "open": 412.50, "high": 413.20, "low": 411.90,
         "close": 412.80, "volume": 65_000_000, "source": "ib"},
    ]
    n = db.upsert_bars("equity_bars", bars)
    assert n == 1

    stored = db.query("SELECT symbol, ts, close, volume FROM equity_bars")
    assert len(stored) == 1
    assert stored[0]["symbol"] == "SPY"
    assert stored[0]["volume"] == 65_000_000


def test_upsert_bars_idempotent():
    """Re-running upsert with the same row updates, doesn't duplicate."""
    db.upsert_instruments([
        {"symbol": "SPY", "sec_type": "STK", "exchange": "ARCA",
         "currency": "USD", "asset_class": "equity",
         "first_seen": date(1993, 1, 29)},
    ])
    bar = {"symbol": "SPY", "timeframe": "daily", "ts": date(2026, 4, 28),
           "adjusted": True, "open": 412.50, "high": 413.20, "low": 411.90,
           "close": 412.80, "volume": 65_000_000, "source": "ib"}
    db.upsert_bars("equity_bars", [bar])

    bar_revised = {**bar, "close": 413.00}  # new close
    db.upsert_bars("equity_bars", [bar_revised])

    rows = db.query("SELECT close FROM equity_bars")
    assert len(rows) == 1
    assert float(rows[0]["close"]) == 413.00


def test_upsert_bars_rejects_unknown_table():
    import pytest
    with pytest.raises(ValueError, match="unknown table"):
        db.upsert_bars("not_a_real_table", [{"x": 1}])
```

- [ ] **Step 2: Run tests, confirm they fail**

```bash
.venv/Scripts/python.exe -m pytest tests/test_db.py -v
```
Expected: 3 new tests FAIL with `AttributeError: ... has no attribute 'upsert_bars'`.

- [ ] **Step 3: Implement `upsert_bars` and `TABLE_PK`/`ALLOWED_BAR_TABLES`**

Append to `trading_tools/db.py`:

```python
ALLOWED_BAR_TABLES = {"equity_bars", "index_bars"}
TABLE_PK = {
    "equity_bars": ("symbol", "timeframe", "ts", "adjusted"),
    "index_bars":  ("symbol", "timeframe", "ts"),
}


def upsert_bars(table: str, rows: list[dict]) -> int:
    """Generic upsert into any allowed *_bars table.

    Whitelist + psycopg.sql.Identifier prevents SQL injection.
    Columns inferred from rows[0].keys(). All rows must have the same shape.
    Returns total rowcount.
    """
    if table not in ALLOWED_BAR_TABLES:
        raise ValueError(f"unknown table: {table!r} (allowed: {sorted(ALLOWED_BAR_TABLES)})")
    if not rows:
        return 0

    cols = list(rows[0].keys())
    pk_cols = TABLE_PK[table]
    update_cols = [c for c in cols if c not in pk_cols]

    insert_sql = _sql.SQL(
        "INSERT INTO {table} ({cols}) VALUES ({placeholders}) "
        "ON CONFLICT ({pk}) DO UPDATE SET {updates}, ingested_at=NOW()"
    ).format(
        table=_sql.Identifier(table),
        cols=_sql.SQL(",").join(_sql.Identifier(c) for c in cols),
        placeholders=_sql.SQL(",").join(_sql.Placeholder(c) for c in cols),
        pk=_sql.SQL(",").join(_sql.Identifier(c) for c in pk_cols),
        updates=_sql.SQL(",").join(
            _sql.SQL("{c}=EXCLUDED.{c}").format(c=_sql.Identifier(c))
            for c in update_cols
        ),
    )
    with get_connection() as conn, conn.cursor() as cur:
        cur.executemany(insert_sql, rows)
        conn.commit()
        return cur.rowcount
```

- [ ] **Step 4: Run tests, confirm all pass**

```bash
.venv/Scripts/python.exe -m pytest tests/test_db.py -v
```
Expected: 5 tests PASS (2 from Task 5 + 3 new).

- [ ] **Step 5: Commit**

```bash
git add tests/test_db.py trading_tools/db.py
git commit -m "db: generic upsert_bars with whitelist + tests"
```

---

### Task 7: `db.check_gaps()` using pandas-market-calendars (TDD)

**Files:**
- Modify: `D:\Plaios-tools\trading-tools\tests\test_db.py`
- Modify: `D:\Plaios-tools\trading-tools\trading_tools\db.py`

- [ ] **Step 1: Write the failing test for `check_gaps`**

Append to `tests/test_db.py`:

```python
def test_check_gaps_returns_empty_when_complete():
    """Insert one bar per expected NYSE trading day in a small range; expect no gaps."""
    import pandas_market_calendars as mcal
    db.upsert_instruments([
        {"symbol": "SPY", "sec_type": "STK", "exchange": "ARCA",
         "currency": "USD", "asset_class": "equity",
         "first_seen": date(2026, 4, 1)},
    ])
    cal = mcal.get_calendar("NYSE")
    expected = cal.schedule(start_date="2026-04-01", end_date="2026-04-15").index.date.tolist()
    bars = [
        {"symbol": "SPY", "timeframe": "daily", "ts": d, "adjusted": True,
         "open": 400.0, "high": 401.0, "low": 399.0, "close": 400.5,
         "volume": 50_000_000, "source": "ib"}
        for d in expected
    ]
    db.upsert_bars("equity_bars", bars)

    gaps = db.check_gaps("equity_bars", "SPY",
                         start=date(2026, 4, 1), end=date(2026, 4, 15),
                         adjusted=True)
    assert gaps == []


def test_check_gaps_detects_missing_day():
    """Skip one trading day; expect it to appear in gaps."""
    import pandas_market_calendars as mcal
    db.upsert_instruments([
        {"symbol": "SPY", "sec_type": "STK", "exchange": "ARCA",
         "currency": "USD", "asset_class": "equity",
         "first_seen": date(2026, 4, 1)},
    ])
    cal = mcal.get_calendar("NYSE")
    expected = cal.schedule(start_date="2026-04-01", end_date="2026-04-15").index.date.tolist()
    skip_date = expected[3]
    bars = [
        {"symbol": "SPY", "timeframe": "daily", "ts": d, "adjusted": True,
         "open": 400.0, "high": 401.0, "low": 399.0, "close": 400.5,
         "volume": 50_000_000, "source": "ib"}
        for d in expected if d != skip_date
    ]
    db.upsert_bars("equity_bars", bars)

    gaps = db.check_gaps("equity_bars", "SPY",
                         start=date(2026, 4, 1), end=date(2026, 4, 15),
                         adjusted=True)
    assert gaps == [skip_date]
```

- [ ] **Step 2: Run tests, confirm they fail**

```bash
.venv/Scripts/python.exe -m pytest tests/test_db.py -v -k check_gaps
```
Expected: both fail with `AttributeError: ... has no attribute 'check_gaps'`.

- [ ] **Step 3: Implement `check_gaps`**

Append to `trading_tools/db.py`:

```python
from datetime import date, timedelta

import pandas_market_calendars as mcal


EXCHANGE_TO_CALENDAR = {
    "ARCA":   "NYSE",
    "NASDAQ": "NYSE",
    "NYSE":   "NYSE",
    "CBOE":   "CBOE_Index_Options",
    "SMART":  "NYSE",
}


def check_gaps(
    table: str,
    symbol: str,
    *,
    timeframe: str = "daily",
    start: date | None = None,
    end: date | None = None,
    adjusted: bool | None = None,
) -> list[date]:
    """Return expected trading dates with no bar for this symbol.

    - Looks up exchange + first_seen from `instruments`.
    - Defaults: start = first_seen, end = yesterday.
    - For equity_bars, `adjusted` filters which version of bars to check.
      If `adjusted=None` for equities, raises (caller must specify which version).
    """
    if table not in ALLOWED_BAR_TABLES:
        raise ValueError(f"unknown table: {table!r}")
    if table == "equity_bars" and adjusted is None:
        raise ValueError("equity_bars requires `adjusted=True` or `adjusted=False`")

    inst_rows = query(
        "SELECT exchange, first_seen FROM instruments WHERE symbol = %s",
        (symbol,),
    )
    if not inst_rows:
        raise ValueError(f"symbol {symbol!r} not in instruments table")
    inst = inst_rows[0]

    cal_name = EXCHANGE_TO_CALENDAR[inst["exchange"]]
    start = start or inst["first_seen"]
    end = end or (date.today() - timedelta(days=1))
    expected = mcal.get_calendar(cal_name).schedule(
        start_date=start, end_date=end
    ).index.date.tolist()

    if table == "equity_bars":
        actual_rows = query(
            "SELECT ts FROM equity_bars "
            "WHERE symbol = %s AND timeframe = %s AND adjusted = %s "
            "AND ts BETWEEN %s AND %s",
            (symbol, timeframe, adjusted, start, end),
        )
    else:
        actual_rows = query(
            "SELECT ts FROM index_bars "
            "WHERE symbol = %s AND timeframe = %s AND ts BETWEEN %s AND %s",
            (symbol, timeframe, start, end),
        )
    actual = {r["ts"] for r in actual_rows}
    return [d for d in expected if d not in actual]
```

- [ ] **Step 4: Run tests, confirm all pass**

```bash
.venv/Scripts/python.exe -m pytest tests/test_db.py -v
```
Expected: 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_db.py trading_tools/db.py
git commit -m "db: check_gaps using pandas-market-calendars + tests"
```

---

### Task 8: `ib_data.fetch_bars()` — read-only IB fetcher

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\ib_data.py`

- [ ] **Step 1: Write `ib_data.py`**

Create `D:\Plaios-tools\trading-tools\trading_tools\ib_data.py`:

```python
"""Interactive Brokers historical data fetcher.

READ-ONLY DISCIPLINE: this module imports ONLY historical-data classes
from ib_async. Order classes (MarketOrder, LimitOrder, ...) are NEVER
imported here or anywhere else in this codebase. A typo or generated edit
calling an order method must `NameError`, not fire an order.
"""
from __future__ import annotations

import logging
import os
from datetime import date

from dotenv import load_dotenv
from ib_async import IB, Index, Stock, util  # ← whitelist; do not extend without review

load_dotenv()
logger = logging.getLogger(__name__)

IB_HOST = os.environ.get("IB_HOST", "127.0.0.1")
IB_PORT = int(os.environ.get("IB_PORT", "8000"))
IB_CLIENT_ID = int(os.environ.get("IB_CLIENT_ID", "1"))


def _make_contract(symbol: str, sec_type: str, exchange: str, currency: str):
    """Build an ib-async contract for the given parameters."""
    if sec_type == "STK":
        return Stock(symbol=symbol, exchange=exchange, currency=currency)
    if sec_type == "IND":
        return Index(symbol=symbol, exchange=exchange, currency=currency)
    raise ValueError(f"unsupported sec_type for V1: {sec_type!r}")


def _bar_size(timeframe: str) -> str:
    return {"daily": "1 day", "weekly": "1 week"}[timeframe]


def _what_to_show(sec_type: str, adjusted: bool) -> str:
    if sec_type == "IND":
        return "TRADES"  # indices have no adjustment
    return "ADJUSTED_LAST" if adjusted else "TRADES"


def fetch_bars(
    symbol: str,
    sec_type: str,
    exchange: str,
    currency: str,
    *,
    timeframe: str = "daily",
    adjusted: bool = True,
    duration: str = "20 Y",
) -> list[dict]:
    """Fetch historical bars from IB. Returns list of dicts shaped for the
    appropriate table.

    For STK (equities): dicts have all of {symbol, timeframe, ts, adjusted, open,
        high, low, close, volume, source}.
    For IND (indices): dicts have {symbol, timeframe, ts, open, high, low, close,
        source}. No `adjusted`, no `volume`.

    `duration` follows IB's format: '20 Y', '5 Y', '6 M', '30 D'.
    """
    contract = _make_contract(symbol, sec_type, exchange, currency)
    ib = IB()
    ib.connect(IB_HOST, IB_PORT, clientId=IB_CLIENT_ID, readonly=True)
    try:
        ib.qualifyContracts(contract)
        bars = ib.reqHistoricalData(
            contract,
            endDateTime="",
            durationStr=duration,
            barSizeSetting=_bar_size(timeframe),
            whatToShow=_what_to_show(sec_type, adjusted),
            useRTH=True,
            formatDate=1,
        )
    finally:
        ib.disconnect()

    if not bars:
        logger.warning("no bars returned for %s/%s/%s/%s",
                       symbol, sec_type, timeframe, adjusted)
        return []

    out: list[dict] = []
    for b in bars:
        ts = b.date if isinstance(b.date, date) else b.date.date()
        if sec_type == "IND":
            out.append({
                "symbol": symbol,
                "timeframe": timeframe,
                "ts": ts,
                "open": b.open,
                "high": b.high,
                "low": b.low,
                "close": b.close,
                "source": "ib",
            })
        else:
            out.append({
                "symbol": symbol,
                "timeframe": timeframe,
                "ts": ts,
                "adjusted": adjusted,
                "open": b.open,
                "high": b.high,
                "low": b.low,
                "close": b.close,
                "volume": int(b.volume),
                "source": "ib",
            })
    logger.info("fetched %d %s/%s bars for %s", len(out), timeframe,
                "adj" if adjusted else "unadj", symbol)
    return out
```

- [ ] **Step 2: Manual smoke check — pull 1 year of SPY**

Make sure TWS or IB Gateway is running with API enabled on port 8000, then:

```bash
.venv/Scripts/python.exe -c "from trading_tools.ib_data import fetch_bars; bars = fetch_bars('SPY', 'STK', 'ARCA', 'USD', duration='1 Y'); print(f'got {len(bars)} bars'); print(bars[0]); print(bars[-1])"
```
Expected: prints `got ~252 bars` (252 trading days/year), then two sample dicts with all expected keys.

If IB rejects the connection: confirm TWS/Gateway is running, API is enabled in Global Configuration → API → Settings, port matches `.env`, and "Read-Only API" is allowed (it should be — we're connecting `readonly=True`).

- [ ] **Step 3: Commit**

```bash
git add trading_tools/ib_data.py
git commit -m "ib_data: fetch_bars read-only IB historical fetcher"
```

---

### Task 9: `cli.py` — orchestration with KNOWN_INSTRUMENTS, ingest, check-gaps subcommands

**Files:**
- Create: `D:\Plaios-tools\trading-tools\trading_tools\cli.py`

- [ ] **Step 1: Write `cli.py`**

Create `D:\Plaios-tools\trading-tools\trading_tools\cli.py`:

```python
"""Command-line interface for trading-tools.

The only file that knows about both IB and DB. Per asset class, dispatches to
the right table and the right fetch shape.
"""
from __future__ import annotations

import argparse
import logging
import sys
from datetime import date

from trading_tools import db, ib_data

logger = logging.getLogger("trading_tools.cli")

# Bootstrap dict for V1 — replaces auto-discovery until we have it.
# Each entry must be sufficient to construct an IB contract and to seed
# the instruments table.
KNOWN_INSTRUMENTS: dict[str, dict] = {
    "SPY":  dict(sec_type="STK", exchange="ARCA",   currency="USD",
                 asset_class="equity", first_seen=date(1993, 1, 29)),
    "NVDA": dict(sec_type="STK", exchange="NASDAQ", currency="USD",
                 asset_class="equity", first_seen=date(1999, 1, 22)),
    "VIX":  dict(sec_type="IND", exchange="CBOE",   currency="USD",
                 asset_class="index",  first_seen=date(1990, 1, 2)),
}

ASSET_CLASS_TO_TABLE = {"equity": "equity_bars", "index": "index_bars"}


def _seed_instruments(symbols: list[str]) -> None:
    """Upsert instrument rows for the given symbols from KNOWN_INSTRUMENTS."""
    rows = []
    for sym in symbols:
        if sym not in KNOWN_INSTRUMENTS:
            raise SystemExit(f"unknown symbol {sym!r}; add it to KNOWN_INSTRUMENTS")
        meta = KNOWN_INSTRUMENTS[sym]
        rows.append({"symbol": sym, **meta})
    db.upsert_instruments(rows)


def ingest(symbols: list[str], duration: str = "20 Y") -> None:
    """Pull max history (or `duration`) from IB for each symbol, both daily and
    weekly, both adjusted and unadjusted (equities only). Then check gaps."""
    db.init_schema()
    _seed_instruments(symbols)

    for sym in symbols:
        meta = KNOWN_INSTRUMENTS[sym]
        table = ASSET_CLASS_TO_TABLE[meta["asset_class"]]

        for tf in ("daily", "weekly"):
            if meta["asset_class"] == "equity":
                for adj in (True, False):
                    rows = ib_data.fetch_bars(
                        sym, meta["sec_type"], meta["exchange"], meta["currency"],
                        timeframe=tf, adjusted=adj, duration=duration,
                    )
                    n = db.upsert_bars(table, rows)
                    logger.info("%s %s adj=%s: %d rows upserted", sym, tf, adj, n)
            else:  # index — no adjustment dimension
                rows = ib_data.fetch_bars(
                    sym, meta["sec_type"], meta["exchange"], meta["currency"],
                    timeframe=tf, duration=duration,
                )
                n = db.upsert_bars(table, rows)
                logger.info("%s %s: %d rows upserted", sym, tf, n)

        # Post-ingest gap check on daily
        if meta["asset_class"] == "equity":
            gaps = db.check_gaps(table, sym, timeframe="daily", adjusted=True)
        else:
            gaps = db.check_gaps(table, sym, timeframe="daily")
        if gaps:
            logger.warning("%s: %d gap(s) detected — first 5: %s",
                           sym, len(gaps), gaps[:5])


def check_gaps_cmd(symbols: list[str]) -> None:
    """Standalone gap check; prints summary per symbol."""
    for sym in symbols:
        if sym not in KNOWN_INSTRUMENTS:
            print(f"{sym}: unknown — skipping")
            continue
        meta = KNOWN_INSTRUMENTS[sym]
        table = ASSET_CLASS_TO_TABLE[meta["asset_class"]]
        if meta["asset_class"] == "equity":
            gaps = db.check_gaps(table, sym, timeframe="daily", adjusted=True)
        else:
            gaps = db.check_gaps(table, sym, timeframe="daily")
        if gaps:
            print(f"{sym}: {len(gaps)} gap(s) — first 10: {gaps[:10]}")
        else:
            print(f"{sym}: clean")


def _parse_symbols(s: str) -> list[str]:
    return [x.strip().upper() for x in s.split(",") if x.strip()]


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("trading-tools.log"),
        ],
    )

    p = argparse.ArgumentParser(prog="trading_tools")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_ing = sub.add_parser("ingest", help="Fetch + upsert bars from IB")
    p_ing.add_argument("--symbols", required=True, type=_parse_symbols,
                       help="comma-separated, e.g. SPY,NVDA,VIX")
    p_ing.add_argument("--duration", default="20 Y",
                       help="IB duration string, e.g. '20 Y', '5 Y'")

    p_gap = sub.add_parser("check-gaps", help="Check for missing bars")
    p_gap.add_argument("--symbols", required=True, type=_parse_symbols)

    args = p.parse_args(argv)

    if args.cmd == "ingest":
        ingest(args.symbols, duration=args.duration)
    elif args.cmd == "check-gaps":
        check_gaps_cmd(args.symbols)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Quick syntax verification**

```bash
.venv/Scripts/python.exe -c "from trading_tools.cli import main, KNOWN_INSTRUMENTS; print(list(KNOWN_INSTRUMENTS))"
```
Expected: `['SPY', 'NVDA', 'VIX']`

- [ ] **Step 3: Commit**

```bash
git add trading_tools/cli.py
git commit -m "cli: ingest + check-gaps subcommands with asset-class dispatch"
```

---

### Task 10: Smoke test — full live IB → DB → query loop

**Files:**
- Create: `D:\Plaios-tools\trading-tools\tests\test_smoke.py`

- [ ] **Step 1: Write `tests/test_smoke.py`**

Create `D:\Plaios-tools\trading-tools\tests\test_smoke.py`:

```python
"""Integration smoke test.

Requires:
  - TWS/IB Gateway running with API enabled on the port in $IB_PORT
  - Postgres running with $DATABASE_URL reachable

Asserts the full ingest loop (IB → upsert → query → readback) works.
Skip with `pytest -m 'not smoke'` (or run with `pytest tests/test_smoke.py`).
"""
from datetime import date, timedelta

import pytest

from trading_tools import db, ib_data
from trading_tools.cli import KNOWN_INSTRUMENTS


pytestmark = pytest.mark.smoke


def test_spy_5_bars_round_trip():
    """Pull 5 days of SPY daily, upsert, query back, assert match."""
    db.upsert_instruments([{"symbol": "SPY", **KNOWN_INSTRUMENTS["SPY"]}])

    bars = ib_data.fetch_bars("SPY", "STK", "ARCA", "USD",
                              timeframe="daily", adjusted=True, duration="5 D")
    assert len(bars) >= 3, f"expected ≥3 bars from IB, got {len(bars)}"
    assert all("close" in b and "volume" in b for b in bars)

    n = db.upsert_bars("equity_bars", bars)
    assert n >= 3

    stored = db.query(
        "SELECT ts, close FROM equity_bars "
        "WHERE symbol = 'SPY' AND adjusted = TRUE AND timeframe = 'daily' "
        "ORDER BY ts DESC LIMIT 5"
    )
    assert len(stored) >= 3
    # Most recent stored ts should match most recent fetched ts
    most_recent_fetched = max(b["ts"] for b in bars)
    assert stored[0]["ts"] == most_recent_fetched


def test_recent_30d_no_gaps():
    """SPY should have no gaps in the last 30 calendar days post-ingest.

    Assumes test_spy_5_bars_round_trip (or a full ingest) has populated some bars.
    For a more thorough check, run `python -m trading_tools ingest --symbols SPY`
    before this test.
    """
    db.upsert_instruments([{"symbol": "SPY", **KNOWN_INSTRUMENTS["SPY"]}])

    # Pull last 30 days to ensure recent data is present
    bars = ib_data.fetch_bars("SPY", "STK", "ARCA", "USD",
                              timeframe="daily", adjusted=True, duration="30 D")
    db.upsert_bars("equity_bars", bars)

    gaps = db.check_gaps(
        "equity_bars", "SPY",
        start=date.today() - timedelta(days=30),
        end=date.today() - timedelta(days=1),
        adjusted=True,
    )
    assert gaps == [], f"unexpected gaps in last 30d: {gaps}"
```

- [ ] **Step 2: Run the smoke test**

Confirm IB is running, then:

```bash
.venv/Scripts/python.exe -m pytest tests/test_smoke.py -v
```
Expected: 2 tests PASS.

If IB connection fails: see Task 8 troubleshooting.
If gap test fails with a holiday in the 30d window that wasn't pulled: this is a real signal — investigate before dismissing.

- [ ] **Step 3: Run all tests together**

```bash
.venv/Scripts/python.exe -m pytest -v
```
Expected: 7 unit tests + 2 smoke tests = 9 PASS total.

- [ ] **Step 4: Commit**

```bash
git add tests/test_smoke.py
git commit -m "test: smoke test for live IB → DB → query round-trip"
```

---

### Task 11: First full ingest run + success criteria verification

**Files:** none (this task runs the system and verifies)

- [ ] **Step 1: Truncate any test data**

```bash
"C:/Program Files/PostgreSQL/18/bin/psql.exe" -U postgres -d trading_data -c "TRUNCATE equity_bars, index_bars, instruments RESTART IDENTITY CASCADE;"
```
Expected: `TRUNCATE TABLE`.

- [ ] **Step 2: Confirm IB is running with API enabled on port 8000**

Open TWS/Gateway. File → Global Configuration → API → Settings:
- ✓ Enable ActiveX and Socket Clients
- Socket port: 8000
- ✓ Read-Only API (we're connecting `readonly=True` from code)
- Trusted IPs: 127.0.0.1

- [ ] **Step 3: Run the ingest**

```bash
.venv/Scripts/python.exe -m trading_tools ingest --symbols SPY,NVDA,VIX --duration "20 Y"
```
Expected: log lines for each (symbol, timeframe, adjusted) combination, totals like:
- SPY daily adj=True: ~5,000 rows
- SPY daily adj=False: ~5,000 rows
- SPY weekly adj=True: ~1,000 rows
- SPY weekly adj=False: ~1,000 rows
- NVDA daily adj=True: ~6,000 rows
- NVDA daily adj=False: ~6,000 rows
- (similar weekly)
- VIX daily: ~9,000 rows (if IB returns it)
- VIX weekly: ~1,800 rows (if IB returns it)

If VIX returns 0 rows: skip to Task 12 to add the FRED fallback.

- [ ] **Step 4: Verify success criteria via psql**

```bash
"C:/Program Files/PostgreSQL/18/bin/psql.exe" -U postgres -d trading_data
```

Then run each:

```sql
-- SC #2: SPY daily adjusted ≥2,500 rows
SELECT COUNT(*) FROM equity_bars
WHERE symbol = 'SPY' AND adjusted = TRUE AND timeframe = 'daily';

-- SC #3: NVDA daily unadjusted ≥2,500 rows
SELECT COUNT(*) FROM equity_bars
WHERE symbol = 'NVDA' AND adjusted = FALSE AND timeframe = 'daily';

-- SC #4: SPY recent week, both variants
SELECT * FROM equity_bars
WHERE symbol = 'SPY' AND timeframe = 'daily'
ORDER BY ts DESC LIMIT 5;

-- SC #5: VIX recent
SELECT * FROM index_bars
WHERE symbol = 'VIX' AND timeframe = 'daily'
ORDER BY ts DESC LIMIT 5;

-- Instruments populated
SELECT * FROM instruments;
```
Each query should return non-empty results matching expected magnitudes.

- [ ] **Step 5: Run gap check**

```bash
.venv/Scripts/python.exe -m trading_tools check-gaps --symbols SPY,NVDA,VIX
```
Expected: each symbol reports `clean` OR a small number of historical gaps that correspond to real IB data quirks (most common pre-2010). If ANY gap appears in the last 30 days, investigate before continuing.

- [ ] **Step 6: Commit (no file changes — but mark completion)**

If this task changed the schema or revealed a needed code change, commit those. Otherwise:
```bash
git log --oneline | head -10
```
to confirm the build state. No commit needed for verification-only tasks.

---

### Task 12: VIX FRED fallback (CONDITIONAL — only if Task 11 step 3 showed VIX 0 rows)

**Files:**
- Modify: `D:\Plaios-tools\trading-tools\trading_tools\ib_data.py`
- Modify: `D:\Plaios-tools\trading-tools\trading_tools\cli.py`

Skip this task if VIX ingested successfully from IB.

- [ ] **Step 1: Add `_fetch_vix_from_fred()` to `ib_data.py`**

Append to `trading_tools/ib_data.py`:

```python
import urllib.request
import csv
import io


def _fetch_vix_from_fred(timeframe: str = "daily") -> list[dict]:
    """Fallback: pull VIX from FRED's free public CSV endpoint.
    Used when IB returns no data for VIX.

    FRED series VIXCLS = CBOE Volatility Index, daily close.
    """
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS"
    logger.info("falling back to FRED for VIX (%s)", timeframe)
    with urllib.request.urlopen(url, timeout=30) as resp:
        text = resp.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    out: list[dict] = []
    for row in reader:
        # FRED column names: 'observation_date' (or 'DATE' in older formats), 'VIXCLS'
        date_key = "observation_date" if "observation_date" in row else "DATE"
        val = row.get("VIXCLS")
        if val in (None, "", "."):
            continue
        try:
            close = float(val)
        except ValueError:
            continue
        ts = date.fromisoformat(row[date_key])
        out.append({
            "symbol": "VIX",
            "timeframe": "daily",  # FRED is daily-only
            "ts": ts,
            "open": None,   # FRED gives close only
            "high": None,
            "low": None,
            "close": close,
            "source": "fred",
        })

    if timeframe == "weekly":
        # Aggregate to Monday-anchored weeks
        from collections import defaultdict
        weekly: dict[date, dict] = {}
        for r in out:
            wk = r["ts"] - timedelta(days=r["ts"].weekday())  # Monday of that week
            entry = weekly.setdefault(wk, {
                "symbol": "VIX", "timeframe": "weekly", "ts": wk,
                "open": None, "high": None, "low": None, "close": None,
                "source": "fred",
            })
            # Last close in the week wins
            entry["close"] = r["close"]
        out = sorted(weekly.values(), key=lambda r: r["ts"])

    logger.info("FRED returned %d VIX %s bars", len(out), timeframe)
    return out
```

- [ ] **Step 2: Modify `cli.ingest()` to fall back when IB VIX is empty**

In `trading_tools/cli.py`, replace the `else: # index` branch inside the `for tf in ('daily', 'weekly'):` loop with:

```python
            else:  # index — no adjustment dimension
                rows = ib_data.fetch_bars(
                    sym, meta["sec_type"], meta["exchange"], meta["currency"],
                    timeframe=tf, duration=duration,
                )
                if not rows and sym == "VIX":
                    logger.warning("IB returned no VIX %s bars; falling back to FRED", tf)
                    rows = ib_data._fetch_vix_from_fred(timeframe=tf)
                n = db.upsert_bars(table, rows)
                logger.info("%s %s: %d rows upserted", sym, tf, n)
```

- [ ] **Step 3: Re-run VIX ingest**

```bash
.venv/Scripts/python.exe -m trading_tools ingest --symbols VIX --duration "20 Y"
```
Expected: log line `IB returned no VIX daily bars; falling back to FRED`, then upsert success.

- [ ] **Step 4: Verify VIX is populated**

```bash
"C:/Program Files/PostgreSQL/18/bin/psql.exe" -U postgres -d trading_data -c "SELECT source, COUNT(*) FROM index_bars WHERE symbol='VIX' GROUP BY source;"
```
Expected: a row showing `fred | <count>` (or `ib | <count>` if IB worked).

- [ ] **Step 5: Commit**

```bash
git add trading_tools/ib_data.py trading_tools/cli.py
git commit -m "ib_data: VIX FRED fallback when IB returns empty"
```

---

### Task 13: Populate `docs/project-state.md` and `docs/decisions.md`

**Files:**
- Modify: `D:\Plaios-tools\trading-tools\docs\project-state.md`
- Modify: `D:\Plaios-tools\trading-tools\docs\decisions.md`

- [ ] **Step 1: Write `docs/project-state.md`**

Replace contents of `D:\Plaios-tools\trading-tools\docs\project-state.md` with:

```markdown
# Project State — trading-tools

**Last updated:** 2026-04-29 (V1 build complete)

## What exists

- **Postgres database** `trading_data` (Postgres 18, local)
- **Tables:**
  - `instruments` (3 rows: SPY, NVDA, VIX)
  - `equity_bars` (~26,000 rows: SPY + NVDA, daily + weekly, adjusted + unadjusted)
  - `index_bars` (~10,800 rows: VIX, daily + weekly; source = 'ib' or 'fred')
- **Code modules:**
  - `trading_tools/db.py` — generic Postgres I/O (init_schema, query, execute, upsert_instruments, upsert_bars, check_gaps)
  - `trading_tools/ib_data.py` — read-only IB historical fetcher (`fetch_bars`); VIX FRED fallback (`_fetch_vix_from_fred`)
  - `trading_tools/cli.py` — ingest + check-gaps subcommands; KNOWN_INSTRUMENTS bootstrap
  - `trading_tools/schema.sql` — idempotent DDL
- **Tests:**
  - `tests/test_db.py` — 7 unit tests (upsert_instruments, upsert_bars, check_gaps)
  - `tests/test_smoke.py` — 2 integration tests (live IB required)

## What's in progress

Nothing. V1 complete.

## What's planned (loose)

- **V2** — Strategy register + backtest harness. First strategy = VWEMA-BB Momentum (Pine→Python port), used as harness-validation case. See spec Appendix B for documented-edge seed list.
- **V3** — Pillar gates + cross-cutting vol/volume signal layers + flow detection + stance arbitration.
- **V4+** — Decisions, advisory.

## Key decisions made

See `docs/decisions.md`.

## Known gaps / debt

- `KNOWN_INSTRUMENTS` is hardcoded in `cli.py`. Replace with proper instrument-discovery code when universe grows beyond ~10 symbols.
- No incremental ingest yet — every run re-pulls full history from IB. Cheap at 3 symbols; needs `--since` flag in V2.
- No retry/backoff on IB rate-limit errors. Will earn its keep when ingesting a universe; current scale doesn't trigger limits.
- No persistent gap registry — gaps are computed on demand. Add a `bar_gaps` table in V2 if/when "known permanent gap" use case appears.
- `pandas-market-calendars` calendar mapping for IB exchanges is approximate (`ARCA`, `NASDAQ`, `SMART` all map to NYSE). Verify per-symbol if a gap check produces unexpected results.
```

- [ ] **Step 2: Write `docs/decisions.md`**

Replace contents of `D:\Plaios-tools\trading-tools\docs\decisions.md` with:

```markdown
# Decision Log

Append-only. Newest at top.

---

## 2026-04-29 — VIX FRED fallback (only if IB empty)

**Decision:** Don't pre-write the FRED fallback. Try IB `IND/CBOE/VIX` first; only implement the FRED fallback if IB returns 0 rows.

**Context:** Original design considered building a 3-step fallback chain (IB → FRED → CBOE CSV). Per KISS, skip what we may not need.

**Alternatives:** Pre-build full chain (rejected as speculative); skip VIX entirely (rejected — VIX is required for vol-regime context).

**Reasoning:** Dead code is debt. Build only when needed. Real fallback is well-documented; can be added in <30 min when triggered.

**Revisit if:** IB market-data subscription changes break the IND/CBOE path mid-flight.

---

## 2026-04-29 — Per-asset-class fact tables (no per-symbol tables)

**Decision:** `equity_bars` + `index_bars`, with `symbol` as a column. No `spy_bars`, `nvda_bars`, etc.

**Context:** User asked whether per-symbol tables would be cleaner.

**Alternatives:** Per-symbol tables (rejected); single `bars` table with asset_class column (rejected — different asset classes have different schemas).

**Reasoning:** Tables represent entity *types*, not instances. Per-symbol forces UNION ALL across N tables for cross-symbol queries (correlations, screens, ranking) and makes schema migrations O(N). Catalog bloat at scale. If physical isolation is needed later, Postgres declarative partitioning (`PARTITION BY LIST (symbol)`) gives the same isolation while keeping the logical table.

**Revisit if:** A specific use case shows >100x query slowdown that partitioning could solve.

---

## 2026-04-29 — No views

**Decision:** No `bars_weekly` view, no `bars_all` UNION view. Weekly bars are physical rows in the same table (distinguished by `timeframe` column). Cross-asset queries are caller-written `UNION ALL`.

**Context:** User explicitly preferred flat tables over views.

**Alternatives:** Maintain views for convenience.

**Reasoning:** Views hide computation, can't be indexed directly, complicate migrations. Physical rows are predictable and debuggable.

**Revisit if:** Common query patterns emerge that would benefit from materialized views (not unindexed views).

---

## 2026-04-29 — Dynamic SQL with dict rows (no per-table dataclasses)

**Decision:** psycopg3 with `dict_row` factory; no `EquityBar`, `IndexBar`, etc.

**Context:** User explicitly rejected schema-mirror dataclasses as ceremony.

**Alternatives:** Pydantic models per table; dataclass per table.

**Reasoning:** Schema and code change at independent rates. Adding columns doesn't require Python edits. Read API is "write the SELECT you need."

**Revisit if:** Production trading API exposes typed contracts to external callers (V4+).

---

## 2026-04-29 — Read-only IB by import discipline

**Decision:** `ib_data.py` and any IB-touching module imports ONLY: `IB`, `Stock`, `Index`, `util`. Order classes (`MarketOrder`, `LimitOrder`, ...) are NEVER imported in V1.

**Context:** Live IB account; never want a typo or generated code to fire an order.

**Alternatives:** Connect to paper account (rejected — historical data subscriptions differ).

**Reasoning:** Import-level enforcement is the strongest possible safety. A call to `MarketOrder(...)` raises `NameError` instead of executing. When V4+ adds order placement, it will live in a separate module with explicit boundaries.

**Revisit if:** V4+ order-placement module is added — define its boundary clearly.

---

## 2026-04-29 — `pandas-market-calendars` for gap detection

**Decision:** Use the library; do not hand-code US trading calendars.

**Context:** Per v4 prompt: "Validate at ingest, not at query time."

**Alternatives:** Hand-code (NYSE half-days, 9/11, Sandy, COVID circuit breakers — all edge cases over 35+ years); approximate via weekdays-minus-federal-holidays (lossy).

**Reasoning:** Library is the irreducible tool for this problem. Maintained, accurate, multi-exchange.

**Revisit if:** Library becomes unmaintained or wrong for our needs.

---

## 2026-04-29 — Postgres 18, no TimescaleDB

**Decision:** Vanilla Postgres 18. Skip Timescale.

**Context:** V1 is daily/weekly OHLCV — small data.

**Alternatives:** Timescale hypertables.

**Reasoning:** Timescale earns its keep at intraday/tick scale. Adds complexity (extension install, hypertable management, partitioning policies) for negligible benefit at our scale.

**Revisit if:** We ingest intraday bars (V2+).
```

- [ ] **Step 3: Commit**

```bash
git add docs/project-state.md docs/decisions.md
git commit -m "docs: project-state + decision log for V1"
```

---

### Task 14: Push to GitHub + update PLAIOS memory

**Files:**
- Modify: `C:\Users\smckennie\.claude\projects\D--PLAIOS\memory\MEMORY.md` (PLAIOS auto-memory index)
- Create: `C:\Users\smckennie\.claude\projects\D--PLAIOS\memory\project_trading_tools_v1_built.md` (PLAIOS memory entry)

- [ ] **Step 1: Create the GitHub repo and push**

```bash
gh repo create smckennie/trading-tools --private --source . --remote origin --push
```
Expected: confirms repo creation and pushes the current branch (likely `main` or `master`).

If the user prefers public, use `--public` instead. Default to private.

- [ ] **Step 2: Verify on GitHub**

```bash
gh repo view smckennie/trading-tools --web
```
Expected: opens browser to the repo. Confirm files are present.

- [ ] **Step 3: Add PLAIOS memory entry**

Create `C:\Users\smckennie\.claude\projects\D--PLAIOS\memory\project_trading_tools_v1_built.md`:

```markdown
---
name: trading-tools V1 built
description: Data ingestion substrate built for the new trading domain; code at D:\Plaios-tools\trading-tools\, GitHub at smckennie/trading-tools
type: project
---

trading-tools V1 (data ingestion substrate) built 2026-04-29.

**Repo:** `D:\Plaios-tools\trading-tools\` — also pushed to `https://github.com/smckennie/trading-tools` (private).
**Spec:** `D:\PLAIOS\docs\superpowers\specs\2026-04-29-trading-tools-v1-design.md`
**Plan:** `D:\PLAIOS\docs\superpowers\plans\2026-04-29-trading-tools-v1.md`

**What's in the DB:**
- Postgres 18, database `trading_data`
- Tables: `instruments`, `equity_bars`, `index_bars` (per-asset-class flat tables)
- Universe: SPY, NVDA, VIX
- Timeframes: daily + weekly (ingested as physical rows)
- Both adjusted + unadjusted equity bars per v4 prompt rule

**Why:** This is the substrate for V2 (strategy register + backtest harness — first strategy = VWEMA-BB Momentum at `D:\PLAIOS\domains\trading\legacy\algos\`). V3 adds pillar gates + flow detection + stance arbitration. V4+ adds decisions and advisory.

**How to apply:** When user asks about trading data, point at this repo. When they want a new symbol added, edit `KNOWN_INSTRUMENTS` in `cli.py` and re-run ingest. When they want to start V2, brainstorm the strategy register + backtest harness as a separate project that consumes this substrate's tables.
```

- [ ] **Step 4: Add the index entry to PLAIOS MEMORY.md**

Append a single line to `C:\Users\smckennie\.claude\projects\D--PLAIOS\memory\MEMORY.md`:

```
- [trading-tools V1 built 2026-04-29](project_trading_tools_v1_built.md) — Data substrate at D:\Plaios-tools\trading-tools\ (GitHub: smckennie/trading-tools); Postgres trading_data with SPY/NVDA/VIX daily+weekly bars
```

- [ ] **Step 5: Commit the memory file (PLAIOS-side, not trading-tools)**

```bash
cd "D:/PLAIOS"
git add memory/project_trading_tools_v1_built.md memory/MEMORY.md
git commit -m "memory: trading-tools V1 substrate built and pushed"
```

(Per close-out protocol: this is a memory-only change, safe to stage and commit without further user approval.)

- [ ] **Step 6: Final verification — re-run all tests against the built system**

```bash
cd "D:/Plaios-tools/trading-tools"
.venv/Scripts/python.exe -m pytest -v
```
Expected: 9 tests PASS.

```bash
.venv/Scripts/python.exe -m trading_tools check-gaps --symbols SPY,NVDA,VIX
```
Expected: each reports `clean` (or known historical gaps acknowledged in `docs/decisions.md`).

V1 complete.

---

## Self-Review

**Spec coverage check:**
- ✅ Repo at `D:\Plaios-tools\trading-tools\` standalone (Task 1)
- ✅ pyproject.toml, venv, .gitignore, .env.example (Task 1)
- ✅ README.md, CLAUDE.md with v4 + pedagogical extension, docs placeholders (Task 2)
- ✅ Schema (instruments, equity_bars, index_bars) (Task 3)
- ✅ db.py: init_schema, query, execute, upsert_instruments, upsert_bars, check_gaps (Tasks 3-7)
- ✅ ib_data.py read-only fetch_bars with import discipline (Task 8)
- ✅ cli.py KNOWN_INSTRUMENTS, ingest, check-gaps, argparse (Task 9)
- ✅ Unit tests (Tasks 5-7) + smoke test (Task 10)
- ✅ Full ingest run + success criteria verification (Task 11)
- ✅ VIX FRED fallback as conditional task (Task 12)
- ✅ docs/project-state.md + docs/decisions.md populated (Task 13)
- ✅ GitHub push + PLAIOS memory entry (Task 14)
- ✅ Read-only IB safety (Tasks 8, 13 decision log)
- ✅ Idempotent re-runs via ON CONFLICT (Task 6)
- ✅ Gap detection wired into ingest + standalone command (Tasks 7, 9)
- ✅ Live IB at port 8000 (Tasks 8, 11)

**Placeholder scan:** No "TBD", "TODO", "implement later", or vague "add error handling" in any task step. All code is concrete. The CLAUDE.md v4-prompt section has an explicit instruction to paste from user's brief (acceptable — the v4 prompt is a user-provided artefact, preserved in conversation history; alternative would be inlining ~3,000 words which bloats this plan).

**Type / signature consistency:**
- `db.upsert_instruments(rows: list[dict]) -> int` — used in Tasks 5, 9, 10, 11. ✓
- `db.upsert_bars(table: str, rows: list[dict]) -> int` — used in Tasks 6, 9, 10. ✓
- `db.check_gaps(table, symbol, *, timeframe='daily', start, end, adjusted) -> list[date]` — used in Tasks 7, 9, 10. ✓
- `ib_data.fetch_bars(symbol, sec_type, exchange, currency, *, timeframe, adjusted, duration) -> list[dict]` — used in Tasks 8, 9, 10. ✓
- `KNOWN_INSTRUMENTS` dict shape — `{symbol: {sec_type, exchange, currency, asset_class, first_seen}}` — used in Tasks 9, 10, 13. ✓
- `_fetch_vix_from_fred(timeframe)` — defined in Task 12, called from Task 12's cli edit. ✓
- CLI subcommands: `ingest` and `check-gaps` (with hyphen) — defined in Task 9, referenced in Tasks 11, 14, README, CLAUDE.md. ✓

No issues found.

---

## Execution Handoff

Plan complete and saved to `D:\PLAIOS\docs\superpowers\plans\2026-04-29-trading-tools-v1.md`.

Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration. Good for this plan because tasks are sequentially dependent (Task N+1 needs Task N's code) and review-between-tasks catches integration issues early.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints. Faster total wall-clock but harder to review intermediate states.

Which approach?
