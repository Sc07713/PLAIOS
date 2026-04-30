---
name: Trading data — 20Y window is enough; pre-1990s gaps are not bugs
description: For trading-tools, IB's ~20Y history horizon is sufficient; pre-window "gaps" reported by check_gaps should be ignored, not fixed
type: feedback
originSessionId: a5fe304d-bd5e-4951-8a07-05e21d545f3b
---
For the trading-tools data substrate (V1 and beyond), the 20-year IB history window is sufficient for the strategies in scope. Gaps reported by `check_gaps` for dates before what IB actually delivers (e.g., SPY 1993–2006, NVDA 1999–2006, VIX 1990–2006) are noise, not bugs.

**Why:** Pre-1990s market context (algorithmic trading, retail participation, regulatory regime, information flow) is not analogous to today's. Backtesting against that era doesn't represent current market behaviour. Scott raised this 2026-04-30 when the Task 11 ingest log showed 3398/1838/4138 "gaps" for SPY/NVDA/VIX and I was about to fix `check_gaps` semantics to suppress them.

**How to apply:**
- Do NOT propose changes to `db.check_gaps` to redefine `start` semantics relative to actual stored data — the current default (`first_seen`) is fine, the noisy gap report is fine.
- When triaging gap-check output, only treat gaps *within the captured window* (post-2006 for these symbols) as real signals.
- If a strategy in V2+ ever requires pre-2006 data for a symbol, that's a fetch-side problem (different data source, e.g., FRED for VIX), not a `check_gaps` problem.
