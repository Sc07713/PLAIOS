---
name: trading-tools V1 built
description: V1 data ingestion substrate complete; code at D:\Plaios-tools\trading-tools\ (master branch), pushed to private GitHub Sc07713/trading-tools, Postgres 17 trading_data with SPY/NVDA/VIX 20Y daily+weekly bars
type: project
originSessionId: 634e79a8-c4bf-4e59-b679-0ee07f9eec5f
---
trading-tools V1 (data ingestion substrate) built 2026-04-29, finalized 2026-04-30.

**Local repo:** `D:\Plaios-tools\trading-tools\` (default branch `master`, NOT `main`)
**GitHub:** `https://github.com/Sc07713/trading-tools` (private)
**Spec:** `D:\PLAIOS\docs\superpowers\specs\2026-04-29-trading-tools-v1-design.md`
**Plan:** `D:\PLAIOS\docs\superpowers\plans\2026-04-29-trading-tools-v1.md`

**What's in the DB:**
- Postgres **17** on port 5432, database `trading_data` (pg18 also installed on 5433 — do NOT switch)
- Tables: `instruments` (3 rows), `equity_bars` (~22K rows), `index_bars` (~6K rows)
- Universe: SPY, NVDA, VIX
- Window: 20 years (earliest 2006-05-05, latest 2026-04-29)
- Equities: daily adjusted + unadjusted, weekly **unadjusted only** (IB rejects ADJUSTED_LAST with multi-day bar sizes — Warning 321)
- Index: VIX daily + weekly from IB (FRED fallback was scoped but unneeded — IB returned full series)

**Hard environmental facts (carry forward to V2):**
- Password contains `@` and `*` → URL-encoded as `%40` and `%2A` in `DATABASE_URL`
- IB Gateway: port 8000, **live data**, enforced read-only by import discipline (no Order classes imported) + `useRTH=True`
- `ib-async` 2.1.0 (plan written for 1.x but core API stable; `IB()`, `connect()`, `qualifyContracts()`, `reqHistoricalData()`, `disconnect()`, `Stock()`, `Index()`, `util.df()` all work)
- IB volume convention: US equity daily/weekly bars come back in **100-share lots**, multiplied by 100 in `ib_data.fetch_bars` before upsert
- `last_updated` on `instruments` = "metadata last seen", not "bars last refreshed"
- psycopg3 `cur.rowcount` returns -1 in pipeline mode after `executemany`; `upsert_bars` returns `len(rows)` instead

**Deferred work explicitly accepted, not done:**
- `KNOWN_INSTRUMENTS` is hardcoded in cli.py — replace with discovery when universe >10
- No incremental ingest (`--since` flag) — every run re-pulls full history
- No retry/backoff on IB rate-limit errors
- `check_gaps` flags trading days between `instruments.first_seen` and the actual data start as gaps; large pre-2006 gap counts for SPY/NVDA/VIX are expected with a 20Y window. Recent-30-day window is verified clean per ingest.

**Why:** Substrate for V2 (strategy register + backtest harness — first strategy = VWEMA-BB Momentum at `D:\PLAIOS\domains\trading\legacy\algos\`). V3 adds pillar gates + flow detection + stance arbitration. V4+ adds decisions/advisory.

**How to apply:** When user asks about trading data, point at this repo. To add a symbol: edit `KNOWN_INSTRUMENTS` in `cli.py` and re-run ingest. To start V2: brainstorm strategy register + backtest harness as a separate project that consumes this substrate's tables. Do NOT switch to pg18, paper trading, or `main` branch. Schema/library choices are locked — do not re-litigate.
