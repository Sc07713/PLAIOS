---
name: PocketSmith budget rebuilt 2026-04-19 — 35-event baseline
description: PocketSmith budget rebuilt from household spreadsheet 2026-04-19. 35 hand-built events; mortgages split Interest/Principal per property. Spreadsheet claimed +$22,925/yr surplus; reality is ~-$13,784/yr cash flow after interest before discretionary.
type: project
originSessionId: rebuild-2026-04-19
---
**What was done (2026-04-19):** Wiped 31 default auto-generated PocketSmith budget events. Built 35 new events from scratch using `mckennie-household-budget.xlsx` (2026 Forecast v2) as source, with bank actuals for mortgage figures.

**Model structure:**
- Mortgage Interest events: on each loan account scenario (NOT visible in standard budget summary — query Loan Interest category directly)
- Mortgage Principal events: on Complete Access operating scenario (category: Loan Repayment)
- Lumpy items at actual cadence: school fees termly, council rates quarterly, water quarterly, rego yearly
- Monthly income events: Scott salary ($8k), Mina salary ($5.5k), Park View rent ($2,040), Hillside rent ($2,200)

**Headline finding:** The spreadsheet was claiming +$22,925/yr surplus before discretionary. Corrected model:
- Total income: $264,312/yr (salary + rent, confirmed by PocketSmith)
- Total expenses excl. interest: ~$189,296/yr (all committed costs)
- Mortgage interest: $88,800/yr (1,982 + 3,100 + 2,318) × 12
- **Cash flow after interest, before discretionary: ~-$13,784/yr**
- Offset by ~$22,800/yr principal/equity gain — so net is roughly break-even before discretionary

**Discretionary is NOT yet modelled.** Eating out, fuel, alcohol, entertainment, clothing, travel, gifts, kids one-offs are all excluded by design pending August 2026 review with Mina (after 3 months of post-rebuild actuals).

**Late-day 2026-04-19 update — BNPL discovery:** Three offline BNPL accounts added to PocketSmith totalling $6,270 (GEM by Latitude $4,010, ZipPlus $1,877, PayPal $383). Confirmed as historic discretionary overspend (mostly eating out). The "discretionary gap" is no longer hypothetical — it has already manifested as financed debt being paid down at ~$300/mo from Virgin. Household rule established same day: **no eating out** until BNPL cleared. See `feedback_no_eating_out_rule.md` and `project_bnpl_discretionary_residue.md`.

**Key corrections from spreadsheet:**
- Sassafras and Park View repayments were SWAPPED in spreadsheet. Actuals: Sassafras $2,550, Park View $3,822.
- Hillside repayment $2,928/mo, not $2,200 (that's the rent). Gap of ~$728/mo from operating cash.

**How to apply:**
- For finance questions, query PocketSmith first — it is now the source of truth for committed cashflow.
- The spreadsheet is historical reference only.
- Mapping doc with all event IDs: `domains/finance/reference/pocketsmith-budget-mapping.md`
- Next recalibration: 2026-07-19 (mortgage interest quarterly pull)
- Discretionary conversation with Mina: target 2026-08
