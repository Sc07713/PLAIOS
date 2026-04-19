# PocketSmith Budget Rebuild — Design

**Date:** 2026-04-19
**Owner:** Scott McKennie
**Domain:** Finance (L1.1, L1.4, L2.1)
**Source spreadsheet:** `domains/finance/reference/mckennie-household-budget.xlsx` (sheet: 2026 Forecast v2)

## Goal

Replace the household budget spreadsheet with a live PocketSmith budget that becomes the single source of truth for committed household cashflow. The spreadsheet is retired as the "where the budget lives" artifact once this lands; it remains in the repo as historical input.

## Why

PocketSmith's killer features over a spreadsheet are: (a) live actuals vs forecast variance, (b) multi-property net-worth and loan-balance accounting, (c) cashflow forecasting that respects lumpy bills. None of those work while budget events are PocketSmith's auto-generated defaults instead of the household's actual plan.

## In Scope

- Wipe the ~31 default auto-generated budget events
- Build new events from spreadsheet line items (one event per line, granular)
- Mortgages modelled as **Interest** (expense) + **Principal** (transfer) per property — not as conflated repayments
- Lumpy items entered at **actual cadence** (yearly/termly/quarterly), not smoothed to monthly
- Income side: match spreadsheet expectations; flag for recalibration after 3 clean months of post-restructure rent data
- Hillside rent shown as income even though it never lands in operating cash (economically it IS income, and the planned rent → offset restructure will make it visible later)

## Explicitly Out of Scope

- **Discretionary categories** (eating out, fuel, alcohol, entertainment, clothing, travel, gifts) — spreadsheet does not contain them; surplus is gross of all discretionary. Flagged for separate Mina conversation, NOT entered as budget events in this rebuild.
- **Backlog transaction categorisation** (2,687 uncategorised + 6,739 needs-review) — separate priority.
- **Rent → offset restructure** — user-led structural change to bank accounts, separate priority.
- **Discovery of true interest split** — happens in Phase 1 of implementation, not at design time.

## Decisions Locked In

| Decision | Choice | Rationale |
|---|---|---|
| Granularity | One event per spreadsheet line | Easier variance debugging; pause/edit individually as life changes |
| Cadence | Actual cadence (yearly/termly/quarterly/monthly) | Honors PocketSmith's cashflow forecast; "smooth to monthly" discards the killer feature over a spreadsheet |
| Mortgage modelling | Interest as expense + Principal as transfer, per property | Honors both views: economic cost visible on expenses dashboard; cashflow accurate; net worth tracks principal reduction correctly |
| Discretionary | Excluded from PocketSmith budget for now | Matches what Scott & Mina already agreed on; surfaces an "honest" conversation gap rather than fabricating numbers |
| Hillside rent | Included as income | Truth: it IS income; alignment with planned offset restructure |
| Income calibration | Use spreadsheet expectations; flag for 3-month recalibration | Rent only began flowing March 2026; insufficient data to forecast from actuals |

## Expense Events

Total expected: **~$13,586/mo committed** (per spreadsheet) plus the additional Hillside cash mortgage (modelled separately).

### Mortgages

For each property, two events:
1. **Interest portion** — `Loan Interest` category (expense), monthly. Amount derived from PocketSmith's 7-month transaction history per loan account (average actual interest charged).
2. **Principal portion** — `Loan Repayment` category (transfer), monthly. Amount = total scheduled repayment − average interest.

| Property | Total Repayment | Interest event amount | Principal event amount |
|---|---|---|---|
| Sassafras | $3,822/mo | TBD from history | balance |
| Park View | $2,552/mo | TBD from history | balance |
| Hillside (minimum, rent-funded) | $2,200/mo | TBD from history | balance |
| Hillside extra (operating cash) | $800/mo | $0 | $800/mo |

Note: Hillside minimum repayment is assumed equal to rent ($2,200/mo) — the rent self-funds the bank-mandated minimum. To be confirmed from history during Phase 1.

### Education (Family and Pets → Education)

| Line | Amount | Cadence |
|---|---|---|
| Salesian College fees (Wulfric) | $11,590/yr ($2,898/term × 4) | Termly |
| Holy Trinity fees (Audrey, Evie) | $4,020/yr ($1,005/term × 4) | Termly |
| Music Education Academy (3 kids) | $434/mo | Monthly |
| Audrey basketball JETS | $61/mo | Monthly |
| Evie basketball JETS | $61/mo | Monthly |
| Wulfric Boxing/Jujitsu | $240/mo | Monthly |
| MIC Basketball training (Audrey) | $370/term × 4 | Termly |
| Salesian guitar lessons (Wulfric) | $240/term × 4 | Termly |

### Childcare (Family and Pets → Child Care)

| Line | Amount | Cadence |
|---|---|---|
| Little Lane childcare (Penny, 4 days/wk) | $764/mo | Monthly |

### Insurance (Insurances → Insurance)

| Line | Amount | Cadence |
|---|---|---|
| Medibank Private Health | $252/mo (or actual annual on renewal) | Monthly placeholder; reconfirm at renewal |
| Budget Direct car | $140/mo (likely yearly renewal) | Confirm cadence at renewal; default monthly |
| Budget Direct Sassafras building | $83/mo (likely yearly) | As above |
| Budget Direct Park View building | $70/mo (likely yearly) | As above |
| Pet insurance Titus | $50/mo | Monthly |

### Utilities and Services

| Line | Amount | Cadence | Category |
|---|---|---|---|
| Greater Western Water — Park View | $540/quarter | Quarterly | Power (utility — closest existing match) or new "Water" subcategory |
| Greater Western Water — Sassafras | $540/quarter | Quarterly | As above |
| Momentum Energy — electricity | $200/mo | Monthly | Power |
| Momentum Energy — gas | $232/mo | Monthly | Power |
| Wulfric mobile | $20/mo | Monthly | Phone |
| Mina mobile | $120/mo | Monthly | Phone |

### Government Services (Miscellaneous → Government Services)

| Line | Amount | Cadence |
|---|---|---|
| VicRoads rego | $840/yr | Yearly on renewal |
| Brimbank Council rates (Park View) | $1,840/yr ($460/quarter) | Quarterly |
| Hume City Council rates (Sassafras) | $2,617/yr ($654/quarter) | Quarterly |

### Groceries (Eating and Drinking → Groceries)

| Line | Amount | Cadence |
|---|---|---|
| Groceries | $1,000/mo | Monthly |

### Other

| Line | Amount | Cadence | Category |
|---|---|---|---|
| Harmoney loan repayment | TBD from history | Monthly until end date | Loan Repayment (or TBD) |
| Ambulance Victoria | TBD ($) | Yearly | Insurance (placeholder event) |
| Land insurance | TBD ($) | Yearly | Insurance (placeholder event) |

## Income Events

| Event | Category | Amount | Cadence | Note |
|---|---|---|---|---|
| Scott salary | Income | $8,000/mo | Monthly | Match spreadsheet |
| Mina salary | Income | $5,496/mo | Monthly | Match spreadsheet |
| Park View rent (Sydenham) | Rentals | $2,040/mo | Monthly | Calibrate after 3 clean months |
| Hillside rent (Celendine) | Rentals | $2,200/mo | Monthly | Paid by Rinoa + Sam + Mina's mum (combined). Flows directly to loan/offset, not operating cash. Calibrate after 3 clean months. |

Total forecast income: **~$17,736/mo**.

## Implementation Phases

### Phase 1 — Discovery (read-only)

1. Pull last 7 months of interest charges per loan account → calculate average monthly interest per property → use as the Interest event amount for each mortgage.
2. Pull last 6 months of Harmoney repayments → confirm $386/mo and identify loan end date.
3. Inventory the 31 existing default budget events with their IDs and full JSON for snapshotting.
4. Confirm category IDs for every target category. Identify any new sub-categories needed (e.g. "Water" if separate tracking from Power is wanted; otherwise consolidate under Power for utility bills).

### Phase 2 — Snapshot & Wipe

5. Snapshot all 31 existing events to `domains/finance/reference/_budget_dumps/2026-04-19-pre-rebuild-events.json` (full JSON dump for restoration if needed).
6. Sanity check: confirm none of the existing events have been manually edited by Scott (e.g. the $7K Interest event was the auto-default, not a deliberate value).
7. Delete all 31 events using `delete_event`.

### Phase 3 — Build new events

8. Create the new event set per the tables above. Each event named clearly via the `note` field (e.g. "Salesian College — Wulfric & Audrey term fees"). Mortgage events should encode property name in the note.

### Phase 4 — Document the mapping

9. Write `domains/finance/reference/pocketsmith-budget-mapping.md` — canonical translation from spreadsheet line → PocketSmith event(s), with event IDs, amounts, cadences, and source notes. This is the document future-Scott reads to answer "where did this number come from".

### Phase 5 — Validate

10. Pull `get_budget_summary` for May 2026 → expected total expense ~$13,586/mo + interest delta. Confirm it adds up.
11. Update finance state files:
    - `current-assessment.md`: L2.1 rating moves from 2 (Fragile) → 3 (Functional, trending Systematic)
    - `active-priorities.md`: "Budget alignment" moves from Queued → Done; "Discretionary conversation with Mina" moves to active focus

## Reversibility

Phase 2 (delete) is the only destructive step. The Phase 2 snapshot file is the recovery path — every deleted event can be recreated from the JSON dump if the new model proves wrong. Phase 3 is fully reversible (delete the new events, recreate the old ones from snapshot).

## Open Items / TBD

- **Ambulance Victoria** — yearly amount unknown, will be placeholder event with note "TBD: confirm at next renewal"
- **Land insurance** — yearly amount unknown, will be placeholder event
- **Harmoney loan end date** — derive from history during Phase 1
- **Insurance billing cadence** — most insurance lines may be yearly, not monthly; will check transaction history during Phase 1 to set correct cadence and renewal dates
- **Water sub-category** — Greater Western Water bills currently land in Power; decide during Phase 1 whether to create a Water sub-category or accept consolidation

## Success Criteria

- All 31 default events wiped
- New event set live, summing to expected $13,586/mo committed expenses + correctly-modelled mortgage interest visible separately
- Mapping document committed
- Finance state files updated
- May 2026 budget summary reflects spreadsheet intent within ±5% on each major category

## Discretionary Conversation (deferred work)

This rebuild deliberately does NOT close the discretionary gap. The stated $1,910/mo "surplus" in the spreadsheet is gross of all discretionary spending (eating out, fuel, alcohol, entertainment, clothing, travel, gifts, kids' one-offs). After 3 clean months of post-rebuild data, run a "spreadsheet vs actuals" diff using PocketSmith history and surface the real discretionary number to Mina with evidence — not pre-negotiated guesses. That conversation gets its own brainstorm and design.
