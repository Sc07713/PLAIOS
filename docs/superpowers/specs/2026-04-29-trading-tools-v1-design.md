# trading-tools V1 — Data Substrate Design

**Date:** 2026-04-29
**Owner:** Scott McKennie
**Domain:** Trading (new — to be activated; PLAIOS-side `domains/trading/` exists with legacy artefacts only)
**Repo:** `D:\Plaios-tools\trading-tools\` — standalone git repo, GitHub remote `trading-tools`
**Agent identity:** Cybernetic Trader-Analyst v4 (user-provided system prompt)
**Anchor strategy:** VWEMA-BB Momentum Strategy, saved at `D:\PLAIOS\domains\trading\legacy\algos\VWEMA-BB-momentum-strategy.pine`

## Goal

Build the **data substrate** that future backtest, decision, and advisory engines will stand on. V1 ingests daily and weekly OHLCV bars for a small known universe (SPY, NVDA, VIX) into a Postgres database, with deliberate schema choices that make V2+ additive rather than refactor.

V1 is **not** a backtest engine, not a strategy register, not an analyst chat layer. It is the smallest useful next step that puts honest market data in a queryable store.

## Why

Per the user's v4 prompt:

> *"Data integrity precedes data interpretation. Bad data produces confident wrong answers. Validate at ingest, not at query time."*
> *"Smallest useful next step. Build what's needed for the current question. Avoid speculative generality."*
> *"Current state precedes new state. Read the project-state.md before proposing changes. Never pre-declare schemas, modules, or architecture that don't exist."*

The trading-tools repo's current state is empty. V1 establishes the substrate. Every subsequent phase (strategy register, backtest harness, pillar gates, flow detection, stance arbitration, advisory) consumes the V1 tables without modifying them.

## In Scope

- One git repo at `D:\Plaios-tools\trading-tools\`, pushed to GitHub as `trading-tools`
- Python 3.13, virtualenv at `.venv/`
- Postgres 18 (already installed at `C:\Program Files\PostgreSQL\18\`), one dedicated database
- Three tables: `instruments`, `equity_bars`, `index_bars` — flat, no views
- Three symbols: SPY, NVDA, VIX
- Two timeframes: daily and weekly (both ingested as physical rows, distinguished by `timeframe` column)
- Both adjusted and unadjusted prices for equities (split/dividend handling per v4 rule)
- IB connection via `ib-async`, `127.0.0.1:8000`, **live account, read-only by import discipline** (`MarketOrder`, `LimitOrder`, etc. never imported)
- VIX via IB `IND/CBOE/VIX` first; documented fallback to FRED `VIXCLS` if IB returns empty (fallback code only written if needed)
- Gap detection via `pandas-market-calendars`; reports gaps post-ingest, raises in smoke test
- One-shot backfill of max history IB returns (≥10 years per user requirement)
- Idempotent re-runs via `INSERT ... ON CONFLICT DO UPDATE`
- Smoke test that connects live IB, round-trips 5 SPY bars (IB → DB → query → assert), checks no recent gaps

## Explicitly Out of Scope

- **Order placement** — forbidden by import discipline; never V1
- **Incremental / scheduled updates** — V2; V1 is one-shot backfill
- **Intraday bars** — TimescaleDB question opens here; deferred until intraday is needed
- **Strategy code** — VWEMA-BB stays in `D:\PLAIOS\domains\trading\legacy\algos\` until a backtest harness exists to consume it
- **Backtest harness** — V3
- **Strategy register, pillar gates, flow detector, stance arbitrator** — V4+ (per architectural diagrams in design conversation)
- **Fundamentals data, analyst revisions, insider data, sentiment surveys, IV chains, options data, macro feeds** — each gets its own brainstorm and additive table when its use case lands
- **Auto-backfill of detected gaps** — V2 (V1 reports; V2 retries with policy)
- **Persistent gap registry table (`bar_gaps`)** — V2; on-demand computation is enough for V1
- **Cross-asset UNION view (`bars_all`)** — explicitly rejected by user; callers write UNION ALL inline when needed
- **Schema-mirror Python dataclasses** — explicitly rejected by user; rows are `dict` in/out via psycopg3's `dict_row` factory
- **Other tools in `D:\Plaios-tools\`** — each gets its own repo and brainstorm

## Decisions Locked In

| Decision | Choice | Rationale |
|---|---|---|
| Repo location | `D:\Plaios-tools\trading-tools\` | Standalone repo; `D:\Plaios-tools\` is just an organisational parent for separate tool repos |
| Code layout | Flat 4-module package (`ib_data.py`, `db.py`, `schema.sql`, `cli.py`) | KISS; no premature subdirs (`sources/`, `storage/`) until a second source/store earns them |
| Python interface | Dynamic SQL + `dict` rows; no per-table dataclasses | User preference; schema and code change at independent rates; no friction on column additions |
| Schema modelling | Per-asset-class tables (`equity_bars`, `index_bars`); per-symbol tables explicitly rejected | Tables represent entity *types*, not instances; cross-symbol queries are universal in backtests; per-symbol would force UNION ALL across N tables and make schema migrations O(N) |
| Views | None; flat physical tables only | User preference; views hide computation, complicate migrations, can't be indexed directly |
| Weekly bars | Ingested as physical rows alongside daily, same table, distinguished by `timeframe` column | IB returns weekly bars natively (`barSizeSetting='1 week'`) — calendar-week-aligned with real opens; more accurate than computing from daily |
| Adjustment | `adjusted` boolean column on `equity_bars`; both `TRUE` and `FALSE` ingested | v4 rule: adjusted for returns, unadjusted for level-based signals; NVDA splits (2000, 2007, 2021, 2024) make this load-bearing |
| Indices | No `adjusted` column, no `volume` column on `index_bars` | Honest schema; indices aren't split-adjusted, have no volume |
| Idempotency | `INSERT ... ON CONFLICT (PK) DO UPDATE` | Safe re-runs; handles IB's habit of restating recent bars |
| Migrations | Plain `schema.sql` with `CREATE TABLE IF NOT EXISTS`, run by `db.init_schema()` | One file, idempotent; Alembic earns entry when production data exists or the schema has ≥3 tables in active flux |
| IB library | `ib-async` (per v4 prompt) | Modern async wrapper; saner than raw `ibapi` callbacks |
| Sync style | Wrap async via `ib_async.util.run()` | `cli.py` stays synchronous and readable; no async-virus through codebase |
| Read-only safety | `ib_data.py` imports only historical-data classes (`IB`, `Stock`, `Index`, `util`); never order-related classes | Import-level enforcement: typo causes `NameError`, not an unintended order |
| IB connection | `127.0.0.1:8000`, live account | User-specified port (non-standard but per user's TWS/Gateway config); read-only by code discipline above |
| VIX path | Try IB `IND/CBOE/VIX` first; fallback to FRED `VIXCLS` only if IB returns empty | KISS; don't write fallback code that may not be needed |
| Gap detection | `pandas-market-calendars`; `db.check_gaps()` function | Library is the irreducible tool — building US trading calendar from scratch means hand-coding 35+ years of edge cases (NYSE half-days, 9/11, Sandy, COVID circuit breakers, etc.) |
| Logging | Stdlib `logging`, INFO→stdout, DEBUG→`trading-tools.log` | Stdlib is enough at V1 size; loguru adds a dep for marginal gain |
| Project state file | `docs/project-state.md` in repo, updated each session | Per v4 prompt's living-spec discipline |
| Decision log | `docs/decisions.md` in repo, append-only | Per v4 prompt's decision-log discipline |
| Agent prompt | `CLAUDE.md` at repo root, derived from v4 system prompt + pedagogical extension (see Appendix A) | Sets agent operating discipline from day 1 |
| History depth | Max IB returns; ≥10 years required | Cheap to pull once; gives more regimes (COVID 2020, 2022 bear, 2018 selloff at minimum; ideally GFC + dot-com) for honest base rates |
| Postgres version | 18 (newest installed) | No legacy data at risk; fresh DB |
| Database name | `trading_data` (proposed) | Clear, dedicated; user can override during setup |
| Dependencies | `ib-async`, `psycopg[binary]`, `pandas-market-calendars`, `python-dotenv`, `pytest` | Tight; each has a specific irreducible job. `pandas` is transitive (required by `ib-async` and `pandas-market-calendars`) |

## Architecture

### Repo layout

```
D:\Plaios-tools\trading-tools\
├── trading_tools\
│   ├── __init__.py
│   ├── ib_data.py          # fetch_bars(...) -> list[dict]; read-only IB imports only
│   ├── db.py               # init_schema, query, execute, upsert_bars, upsert_instruments, check_gaps
│   ├── schema.sql          # instruments + equity_bars + index_bars (idempotent CREATE TABLE IF NOT EXISTS)
│   └── cli.py              # KNOWN_INSTRUMENTS dict, ingest(), check_gaps_cmd()
├── tests\
│   └── test_smoke.py       # live IB → 5 SPY bars → upsert → query → assert; no gaps in last 30 days
├── docs\
│   ├── project-state.md    # living current-state per v4
│   └── decisions.md        # append-only decision log per v4
├── .env.example            # documents required env vars (no secrets)
├── .env                    # actual secrets (gitignored)
├── .gitignore              # .env, .venv/, __pycache__, *.log
├── pyproject.toml
├── README.md               # quickstart, deps, env setup, command reference
├── CLAUDE.md               # agent prompt — see Appendix A
└── LICENSE
```

### Schema (DDL — applied by `db.init_schema()`)

```sql
-- Dimension table
CREATE TABLE IF NOT EXISTS instruments (
    symbol       TEXT PRIMARY KEY,
    sec_type     TEXT NOT NULL,           -- 'STK' | 'IND' | future: 'OPT' | 'FUT' | 'CASH' | 'CRYPTO'
    exchange     TEXT NOT NULL,           -- 'ARCA' | 'NASDAQ' | 'CBOE' | 'SMART'
    currency     TEXT NOT NULL,           -- 'USD'
    asset_class  TEXT NOT NULL,           -- 'equity' | 'index' | future: 'option' | 'future' | 'fx' | 'crypto'
    first_seen   DATE NOT NULL,           -- earliest expected bar date
    last_updated TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Equity bars: full OHLCV, both adjusted and unadjusted variants
CREATE TABLE IF NOT EXISTS equity_bars (
    symbol       TEXT        NOT NULL REFERENCES instruments(symbol),
    timeframe    TEXT        NOT NULL,    -- 'daily' | 'weekly'
    ts           DATE        NOT NULL,
    adjusted     BOOLEAN     NOT NULL,
    open         NUMERIC(18,6),
    high         NUMERIC(18,6),
    low          NUMERIC(18,6),
    close        NUMERIC(18,6),
    volume       BIGINT      NOT NULL,
    source       TEXT        NOT NULL,    -- 'ib' | future: 'polygon' etc.
    ingested_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (symbol, timeframe, ts, adjusted)
);
CREATE INDEX IF NOT EXISTS equity_bars_symbol_ts_idx ON equity_bars(symbol, timeframe, ts DESC);

-- Index bars: no adjustment dimension, no volume
CREATE TABLE IF NOT EXISTS index_bars (
    symbol       TEXT        NOT NULL REFERENCES instruments(symbol),
    timeframe    TEXT        NOT NULL,    -- 'daily' | 'weekly'
    ts           DATE        NOT NULL,
    open         NUMERIC(18,6),
    high         NUMERIC(18,6),
    low          NUMERIC(18,6),
    close        NUMERIC(18,6),
    source       TEXT        NOT NULL,    -- 'ib' | 'fred' (fallback for VIX)
    ingested_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (symbol, timeframe, ts)
);
CREATE INDEX IF NOT EXISTS index_bars_symbol_ts_idx ON index_bars(symbol, timeframe, ts DESC);
```

Future tables (`option_bars`, `future_bars`, `fx_bars`, `crypto_bars`) follow the same pattern with their own asset-class-appropriate columns. They will be added in their own brainstorm-design-implement cycles, not pre-declared here.

### `db.py` API

```python
ALLOWED_BAR_TABLES = {'equity_bars', 'index_bars'}
TABLE_PK = {
    'equity_bars': ('symbol', 'timeframe', 'ts', 'adjusted'),
    'index_bars':  ('symbol', 'timeframe', 'ts'),
}

def init_schema() -> None:
    """Apply schema.sql idempotently."""

def query(sql_str: str, params: tuple = ()) -> list[dict]:
    """Run any SELECT, return list of dict rows."""

def execute(sql_str: str, params: tuple = ()) -> int:
    """Run any DML/DDL, return rowcount."""

def upsert_instruments(rows: list[dict]) -> int:
    """Bulk upsert into instruments. ON CONFLICT (symbol) DO UPDATE."""

def upsert_bars(table: str, rows: list[dict]) -> int:
    """Generic upsert into any *_bars table.
    Whitelist + psycopg.sql.Identifier = no SQL injection.
    Columns inferred from rows[0].keys()."""

def check_gaps(
    table: str, symbol: str, *,
    timeframe: str = 'daily',
    start: date | None = None,
    end: date | None = None,
    adjusted: bool | None = None,
) -> list[date]:
    """Return expected trading dates with no bar for this symbol.
    Looks up exchange + first_seen from `instruments`.
    Defaults: start=first_seen, end=yesterday."""
```

That's the entire data layer. Adding a new asset class requires: (1) DDL in `schema.sql`, (2) entry in `ALLOWED_BAR_TABLES`, (3) entry in `TABLE_PK`. **No new Python class. No code-path duplication.**

### `ib_data.py` API

```python
def fetch_bars(
    symbol: str, sec_type: str, exchange: str, currency: str, *,
    timeframe: str = 'daily',          # 'daily' | 'weekly'
    adjusted: bool = True,             # ignored for indices
    duration: str = '20 Y',
) -> list[dict]:
    """Fetch bars via ib-async. Returns dicts shaped for the appropriate table.
    Equity dicts have `volume` and `adjusted`; index dicts omit both."""
```

Imports limited to: `from ib_async import IB, Stock, Index, util`. **No order classes ever.**

### `cli.py` orchestration

```python
KNOWN_INSTRUMENTS: dict[str, dict] = {
    'SPY':  dict(sec_type='STK', exchange='ARCA',   currency='USD',
                 asset_class='equity', first_seen=date(1993, 1, 29)),
    'NVDA': dict(sec_type='STK', exchange='NASDAQ', currency='USD',
                 asset_class='equity', first_seen=date(1999, 1, 22)),
    'VIX':  dict(sec_type='IND', exchange='CBOE',   currency='USD',
                 asset_class='index',  first_seen=date(1990, 1, 2)),
}
ASSET_CLASS_TO_TABLE = {'equity': 'equity_bars', 'index': 'index_bars'}

def ingest(symbols: list[str], duration: str = '20 Y') -> None:
    """Pull max history (or `duration`), both daily+weekly, both adjusted+unadjusted
    (equities only), then check_gaps and log warnings."""

def check_gaps_cmd(symbols: list[str]) -> None:
    """Standalone gap check; prints gap summary per symbol."""

# Entrypoint:
#   python -m trading_tools.cli ingest --symbols SPY,NVDA,VIX
#   python -m trading_tools.cli check-gaps --symbols SPY,NVDA,VIX
```

## Implementation Phases

### Phase 1 — Scaffold

1. `git init` at `D:\Plaios-tools\trading-tools\`
2. Create folder structure per Architecture section
3. `pyproject.toml` with deps pinned: `ib-async`, `psycopg[binary]`, `pandas-market-calendars`, `python-dotenv`, `pytest`
4. `python -m venv .venv` + activate + `pip install -e .`
5. `.env.example` documenting `DATABASE_URL`, `IB_HOST=127.0.0.1`, `IB_PORT=8000`, `IB_CLIENT_ID=1`
6. `.gitignore`: `.env`, `.venv/`, `__pycache__/`, `*.log`, `*.egg-info/`
7. `README.md` with quickstart
8. `CLAUDE.md` per Appendix A
9. Empty `docs/project-state.md` and `docs/decisions.md`
10. Commit: "scaffold: empty trading-tools repo with pyproject + venv + docs"

### Phase 2 — Database up

1. Create database: `createdb trading_data` (or via psql)
2. Write `schema.sql` per DDL above
3. Write `db.py` `init_schema()`, `query()`, `execute()`, `upsert_instruments()`, `upsert_bars()`
4. Manual test: `python -c "from trading_tools.db import init_schema; init_schema()"` then verify via psql: `\d instruments; \d equity_bars; \d index_bars`
5. Commit: "db: schema + generic upsert/query API"

### Phase 3 — IB connection proven

1. Write `ib_data.py` `fetch_bars()` with read-only IB imports
2. Manual test: pull 1 year of SPY daily, print first 5 rows
3. Verify shape: dict keys match `equity_bars` columns
4. Confirm IB connection on port 8000 with live account works
5. Commit: "ib_data: read-only IB historical data fetcher"

### Phase 4 — Full ingest

1. Write `cli.py` with `KNOWN_INSTRUMENTS`, `ASSET_CLASS_TO_TABLE`, `ingest()` function
2. Add `argparse` entry: `python -m trading_tools.cli ingest --symbols ... [--duration '20 Y']`
3. Run end-to-end: `python -m trading_tools.cli ingest --symbols SPY,NVDA,VIX`
4. Verify in psql:
   ```sql
   SELECT symbol, timeframe, adjusted, COUNT(*) FROM equity_bars
   GROUP BY symbol, timeframe, adjusted ORDER BY symbol, timeframe, adjusted;

   SELECT symbol, timeframe, COUNT(*) FROM index_bars
   GROUP BY symbol, timeframe ORDER BY symbol, timeframe;

   SELECT * FROM instruments;
   ```
5. If VIX returns empty from IB: implement FRED fallback (separate function `_fetch_vix_from_fred()`), update `cli.py` to fall through, document in decisions.md
6. Commit: "cli: full ingest orchestration with asset-class dispatch"

### Phase 5 — Gap detection wired

1. Add `check_gaps()` to `db.py` using `pandas-market-calendars`
2. Add post-ingest gap check to `cli.ingest()` — log warnings, don't raise
3. Add `cli.check_gaps_cmd()` and wire it as `check-gaps` argparse subcommand (per the cli.py entrypoint comment block in the Architecture section)
4. Smoke test: `tests/test_smoke.py`:
   - Connect IB live, fetch 5 SPY daily bars, upsert to DB, query back, assert rowcount and one known field
   - `check_gaps('equity_bars', 'SPY', start=today-30d, adjusted=True)` returns `[]`
5. Commit: "gaps: detection + smoke test"

### Phase 6 — Documentation closeout

1. Update `docs/project-state.md` with what was built
2. Append decisions to `docs/decisions.md` (one entry per locked decision in this spec)
3. Push to GitHub: `gh repo create smckennie/trading-tools --private --source . --push`
4. Update PLAIOS memory: project memory entry pointing to repo + spec
5. Commit: "docs: project-state + decisions, V1 complete"

## Reproducibility

Per v4 prompt: *"Every backtest run is logged with parameters, code version, and timestamp. Results without reproducibility metadata are anecdotes."*

V1 has no backtests yet, but the substrate is reproducibility-aware:
- `ingested_at TIMESTAMPTZ` on every bar → know when data was pulled
- `source TEXT` on every bar → know which provider gave us this version
- Idempotent re-runs (ON CONFLICT DO UPDATE) → re-ingestion overwrites with the most recent provider state, audit trail in git commits
- Schema changes tracked in git via `schema.sql`

## Open Items / TBD

- **VIX from IB** — confirmed available via `IND/CBOE/VIX` per documentation, but actual ingest may surface market-data subscription gaps. Resolution: try first; if empty after 5 attempts on different `useRTH` / `whatToShow` combos, implement FRED fallback in Phase 4
- **NVDA split adjustments** — IB's `useRTH=1` + `whatToShow='ADJUSTED_LAST'` returns split-adjusted; `whatToShow='TRADES'` returns unadjusted. Verify both in Phase 3
- **Postgres connection string format** — `.env.example` will document; user sets actual `.env` during Phase 1 setup
- **GitHub repo visibility** — assumed private; confirm during Phase 6
- **`pandas-market-calendars` calendar names** — `'NYSE'` for SPY/NVDA, `'CBOE_Index_Options'` for VIX; verify exact names work in Phase 5

## Success Criteria

1. `python -m trading_tools.cli ingest --symbols SPY,NVDA,VIX` runs end-to-end without errors on a fresh DB
2. `SELECT COUNT(*) FROM equity_bars WHERE symbol='SPY' AND adjusted=true AND timeframe='daily';` returns ≥2,500 rows (10y daily)
3. `SELECT COUNT(*) FROM equity_bars WHERE symbol='NVDA' AND adjusted=false AND timeframe='daily';` returns ≥2,500 rows
4. `SELECT * FROM equity_bars WHERE symbol='SPY' ORDER BY ts DESC LIMIT 5;` returns the most recent week of trading days, both adjusted and unadjusted
5. `SELECT * FROM index_bars WHERE symbol='VIX' ORDER BY ts DESC LIMIT 5;` returns recent VIX values
6. `python -m trading_tools.cli check-gaps --symbols SPY,NVDA,VIX` reports zero gaps in the last 30 days for each symbol
7. `pytest` passes the smoke test
8. `docs/project-state.md` and `docs/decisions.md` are populated and reflect the build
9. Repo pushed to GitHub
10. PLAIOS memory updated with the new repo location

## Reversibility

Every step is reversible:
- Phase 1-3: pure file creation; `git reset --hard` undoes
- Phase 4 (ingest): `TRUNCATE TABLE equity_bars, index_bars, instruments` clears the data; re-run to restore
- Phase 5 (smoke test): adds files only
- Phase 6 (push): `gh repo delete` if we need to start over

DB drops are gated on user confirmation, never automated.

---

## Appendix A — `CLAUDE.md` plan for the trading-tools repo

The `CLAUDE.md` at the repo root sets the agent operating discipline. It is created in Phase 1 (Scaffold), thin in V1 (we have no strategies to teach about yet), and grows through V2/V3 as the strategy register and backtest harness arrive.

V1 content includes:

1. **Embed the v4 Cybernetic Trader-Analyst prompt verbatim** as the agent identity — preserves the operating mode the user has already designed
2. **Project context block**: "This repo's current state: V1 (data ingestion only). V2 will add strategy register + backtest harness. V3+ adds pillar gates, flow detection, stance arbitration, decisions and advisory."
3. **Reference paths**: `docs/project-state.md` (living current-state), `docs/decisions.md` (append-only decision log) — agent reads project-state.md before any substantive change, per v4 rule
4. **Pedagogical directive (per user request 2026-04-29)**:
   > When introducing or proposing any signal, indicator, strategy, or factor: cite the documented source of edge (academic paper, replication study, or practitioner reference). When proposing a backtest: frame it as a *falsification test* — what would have to be true in the data for this edge to NOT exist? Report results honestly: did the edge replicate, decay, or never exist in our sample? Distinguish documented edges from folklore patterns explicitly.
5. **Anti-pattern reminders**:
   - No single-pillar theses (per v4)
   - No backtest results without reproducibility metadata (run_id, code_hash, timestamp, params)
   - Sub-30 occurrences = anecdote, not edge — flag explicitly
   - Pooled stats across mixed regimes = misleading — segment by regime
6. **Read-only safety reminder**: imports of order-related classes from `ib_async` are prohibited at all levels of the codebase

V2/V3 expansions to `CLAUDE.md` will add strategy-register conventions, backtest-result conventions (Template C from v4 prompt), and the documented edges catalogue (per Appendix B).

## Appendix B — V2 strategy-register seed (built once V1 substrate exists)

Per user direction 2026-04-29, the strategy register's first entries map to **documented historical edges**, each with academic source, mechanism, known decay/regime sensitivity, and a falsification-test design. Listed here so the V2 brainstorm starts pre-loaded:

| Edge | Pillar(s) | Source | First test |
|---|---|---|---|
| Value (P/B, P/E) | Fundamental | Fama-French 1992 | Quintile sort over our universe — does cheap quintile beat expensive over 1y rolling? |
| Cross-sectional momentum (12-1) | Technical, Quant | Jegadeesh & Titman 1993; AQR 2013 | Top-decile vs bottom-decile 12-1 month return; rebalance monthly |
| Quality / profitability | Fundamental | Novy-Marx 2013 | Top-quintile gross profitability vs bottom |
| Low beta / low vol | Quantitative | Frazzini & Pedersen 2014 | Sharpe-ranked deciles by trailing beta |
| Long-term reversal | Fundamental, Behavioural | De Bondt & Thaler 1985 | 3-5y losers vs winners |
| Post-earnings drift (PEAD) | Fundamental, Behavioural | Bernard & Thomas 1989 | Drift over 60 trading days post-beat for top-quintile surprises |
| Insider cluster buying | Behavioural | Lakonishok-Lee 2001; Cohen et al 2012 | 3+ insiders buying within 30d → 6m forward return vs control |
| Yield curve inversion | Macro | Various | Stance-arbitration regime flag; lead time 6-24m |
| HY credit spread expansion | Macro | Various | Tactical stance flag; 1-3m equity drawdown lead |
| Volatility risk premium (VRP) | Quantitative | Various | Roll-yield strategies on VIX futures; tail-risk-adjusted Sharpe |
| **VWEMA-BB Momentum** (user's own) | Technical, Quant | User's TradingView fork of RezzaHmt | Replicate Pine Script logic in Python; backtest against TradingView reference results to validate harness fidelity before testing other strategies |

Notably, the **VWEMA-BB strategy is the harness-validation case** — we know it works in TradingView; if our Python backtest harness reproduces TradingView's results within tolerance, the harness is trustworthy. *Per v4 prompt: "Test the test — when writing a backtest, verify the harness on a known case (e.g., buy-and-hold SPY) before trusting strategy results."*

## Appendix C — Multi-pillar confluence setups (V3+)

Once the strategy register exists and pillar-gate data feeds land (V3+), the high-conviction setups from the design conversation become testable:

**Long setup (regime-permissive):**
- Value (Pillar 2): cheap on P/B, P/CF
- Quality (Pillar 2): top-quartile gross profitability
- PEAD (Pillar 4): recent earnings beat, top-quintile surprise
- Momentum (Pillar 3): 6-month price momentum positive
- Insider (Pillar 4): cluster buying in last 60 days
- Macro (Pillar 1): no HY blowout, curve not deeply inverted
- Vol (Pillar 5): IV rank < 40

**Short setup (regime-stressed):**
- Macro (Pillar 1): HY spread widening, MOVE rising
- Earnings (Pillar 2): recent miss + analyst downgrades
- Distribution (Pillar 3): below 200dma, lower-low structure
- Sentiment (Pillar 4): still bullish (gap = unwind fuel)
- Insider (Pillar 4): non-routine selling
- Vol (Pillar 5): IV > 60th percentile (use put debit spreads, not naked puts)

These are described here so V3's brainstorm starts with concrete confluence definitions rather than re-deriving them from scratch.
