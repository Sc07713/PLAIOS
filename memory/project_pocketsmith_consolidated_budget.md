---
name: PocketSmith budget — consolidated to one event per category (2026-04-24)
description: Budget architecture: single event per category, all on Scott's Complete Access, date-1 of month. Annualised for termly/quarterly items.
type: project
originSessionId: c021306b-3185-4efd-b11a-5da8d0f159ff
---
**Architecture rule (user directive 2026-04-24):** ONE budget event per category. Termly/quarterly/annual items amortised to monthly. All household events on Scott's Complete Access (scenario 5009794), dated 1st of month, monthly recurring.

**15 household events + 5 Korea events = 20 total.**

Event IDs and amounts in `domains/finance/reference/pocketsmith-budget-mapping.md`.

**Monthly totals:**
- Income: +$17,736 (Income $13,496 + Rentals $4,240)
- Expenses: -$16,718 (13 expense categories)
- Surplus: +$1,018/mo → +$12,216/yr
- Korea trip 2026: -$11,799 one-off (Jul/Aug)
- 12-month net with Korea: +$417 (razor-thin)

**Trade-offs accepted:**
- Per-account scenario forecasts are now inaccurate (CA shows over-positive flow because Mina salary + Park View rent are budgeted there but actually land in Go Account). Household aggregate is correct.
- Granular visibility lost: no per-property mortgage breakdown, no per-policy insurance, no termly school fee hits. See mapping doc notes for the detail that was collapsed.
- If user ever asks to split a category again, push back — this was an explicit simplification.

**Still open (pick up next session):**
- **Korea savings plan** — ringfence via Virgin Boost Saver rename to "Korea Trip 2026", $1,500/mo auto-sweep May-Aug + tax refund redirect (~$12,500 accumulated vs $11,799 need). Recommendation made, not executed.
- **Rent → offset restructure** — drafted, not live. Biggest remaining structural win.
- **BNPL paydown events** — not yet in budget. GEM $4,010, ZipPlus $1,877, PayPal $383 = $6,270 total. Plan Path B: clear PayPal first, rest to trip fund, GEM+ZipPlus carry until post-trip.
- **Category budget targets (UI-only)** — the tile amounts on the Budget page may still show old sticky targets unrelated to events. If tiles don't match event sums after UI refresh, user has to edit each category's monthly target manually.
- **Mina's second Complete Access (4852629)** — to be closed by Mina; no events should be on scenario 5009809 anymore.

**Don't re-verify on next session:**
- Event structure is clean as of 2026-04-24. Start by asking user what they want to do, not by running a full audit.
