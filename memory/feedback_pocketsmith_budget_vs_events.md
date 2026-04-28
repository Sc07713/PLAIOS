---
name: PocketSmith — Budget page targets vs events are separate
description: The PocketSmith Budget page shows manually-set category monthly targets that the API cannot update; events only drive the calendar and net worth forecast
type: feedback
originSessionId: c021306b-3185-4efd-b11a-5da8d0f159ff
---
**Rule:** In PocketSmith, the numbers on the "Budget" page tiles (e.g. "Mortgage Repayments $9,300/mo") are NOT automatically derived from events. They can be manually-set category-level monthly targets that are stored separately and the MCP API has no write tool for them.

**Why:** Discovered 2026-04-23 during mortgage recategorisation. After moving 3 mortgage events from "Loan Repayments" to "Mortgage Repayments" (via delete + recreate), the calendar and net worth forecast updated correctly, but the Budget page kept showing stale category targets ($3,890/mo Mortgage, $83/mo Loan, $100/mo Insurance) that didn't match the event sums. The `update_category` tool has no budget-amount field; `delete_forecast_cache` returns an auth error (OAuth scope limitation).

**How to apply:**
- When asked to "update the budget" for a category, clarify whether they mean events (for calendar/forecast) or the Budget page tile amount (manual target).
- For event changes: use delete_event + create_event OR update_event (notes/amounts/cadence only — category and date are immutable, must delete+recreate).
- For Budget page target changes: tell the user to edit in the PocketSmith UI directly. I can tell them the right number to enter, but I can't set it via API.
- The two numbers SHOULD match (event sum = category target) — after any major event restructure, remind the user to sync the Budget page targets manually.

**Related gotchas:**
- `update_event` cannot change category or date — delete + recreate is required, which loses series history prior to the new start date. Always recreate with original series_start date to preserve historical budget visibility.
- `delete_forecast_cache` requires a scope the standard OAuth flow doesn't grant. Workaround: make a trivial `update_event` call to force per-series recalc, or ask user to reload UI.
