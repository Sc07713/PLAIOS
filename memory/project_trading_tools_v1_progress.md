---
name: Trading-tools V1 — data ingestion substrate, mid-build
description: V1 ingestion repo at D:\Plaios-tools\trading-tools\, Tasks 1–8/14 done as of 2026-04-29; key environmental quirks captured for next session
type: project
originSessionId: fb24bd11-1fee-469b-8616-1708b50cd5bb
---

V1 of the Trading domain's data substrate is being built in a **separate repo from PLAIOS**:

- **Repo path:** `D:\Plaios-tools\trading-tools\`
- **Default branch:** `master` (NOT `main`) — relevant when Task 14 pushes to GitHub
- **Plan:** `docs/superpowers/plans/2026-04-29-trading-tools-v1.md` (in PLAIOS)
- **Spec:** `docs/superpowers/specs/2026-04-29-trading-tools-v1-design.md` (in PLAIOS)
- **Execution mode:** subagent-driven development (per-task implementer + spec reviewer + code quality reviewer)

**Progress at close-out 2026-04-29:** Tasks 1–8 complete and committed. Last commit `d0dee13` (volume 100x fix). Working tree clean. Tasks 9–14 pending (cli.py, smoke test, full ingest run, optional VIX FRED fallback, docs, GitHub push).

**Hard environmental facts the next session must respect:**

- **Postgres:** pg17 on port 5432 (pg18 also installed on 5433 — do NOT switch). DB name `trading_data`. Password contains `@` and `*` so URL-encoded as `%40` and `%2A` in `DATABASE_URL`.
- **IB Gateway:** port 8000, **live data (NOT paper)**, but enforced read-only at two layers — import whitelist (no Order/Trade/MarketOrder etc.) + `ib.reqHistoricalData(..., useRTH=True)` with no order surface touched.
- **ib-async version:** 2.1.0. Plan was written for 1.x API surface; verified empirically compatible at Task 8. Core API stable — `IB()`, `connect()`, `qualifyContracts()`, `reqHistoricalData()`, `disconnect()`, `Stock()`, `Index()`, `util.df()` all work.
- **IB volume convention (CRITICAL):** US equity daily/weekly bars come back in **100-share lots**, NOT actual shares. `ib_data.py` multiplies by 100 before upsert. Confirmed empirically: SPY 2026-04-28 raw=135,950 → stored=13,595,000. Index bars (VIX) have `volume=NULL` by schema and are not affected.
- **Schema design (locked, do not revisit):** per-asset-class flat tables (`equity_bars`, `index_bars`) + `instruments` dimension. NO views. NO Python dataclasses per table. Dynamic SQL with `psycopg.sql.Identifier` and `dict_row` factory throughout.
- **`last_updated` semantics:** field on `instruments` is updated by `upsert_instruments` only, not by bar upserts. Means "instrument metadata last seen", not "bars last refreshed".
- **`cur.rowcount` after `executemany`:** psycopg3 in pipeline mode returns -1 unless explicitly disabled. `upsert_bars` returns `len(rows)` instead of `cur.rowcount` for this reason.

**Pending volume-fix reviews:** Task 8's post-fix commit `d0dee13` was deferred without spec/quality review. Empirical evidence is unambiguous (raw values are nonsensically small for SPY) so deferral is low-risk, but next session should run those reviewers before moving on, OR explicitly accept the fix and proceed.

**Anchor strategy reminder:** V2's backtest harness must be able to express the VWEMA-BB Momentum algo (see `project_trading_favorite_algo_vwema.md`). V1 just gets the data in the DB.

**Why:** Mid-build state captured because context was getting deep and Tasks 9–14 form a coherent next chunk. Without this memory, the next session would re-discover the volume convention, the pg17 vs pg18 question, and the master-not-main branch fact the hard way.

**How to apply:** When the user resumes, read this + the plan + spec. Resume at Task 8 review (or accept and skip to Task 9). Do NOT re-litigate the schema or library choices — they are locked. Do NOT switch to pg18, paper trading, or `main` branch.
