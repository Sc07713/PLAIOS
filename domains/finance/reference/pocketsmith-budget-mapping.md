# PocketSmith Budget — Mapping & Provenance

**Last rebuilt:** 2026-04-19 (mortgage restructure later same day)
**Source:** `mckennie-household-budget.xlsx` (sheet: 2026 Forecast v2)
**Design spec:** `docs/superpowers/specs/2026-04-19-pocketsmith-budget-design.md`
**Implementation plan:** `docs/superpowers/plans/2026-04-19-pocketsmith-budget-rebuild.md`

PocketSmith is now the source of truth for committed household cashflow. The spreadsheet is retained as historical input only.

---

## How to interpret the numbers

**Mortgage events show the full cash repayment** — each monthly event equals the exact amount leaving the bank account. The bank automatically allocates between interest and principal on its side. Interest will still post as bank charges on each loan account in PocketSmith — no separate budget event needed.

**Why simpler now:** The original build modelled Interest and Principal as separate events (6 events across 3 properties). While technically accurate, the Interest events on loan scenarios caused the dashboard to display ~$88,800/yr as an apparent expense, making the budget perpetually look like a loss. The interest cost is real — but it is already visible on each loan account as bank-posted charges. Forecasting it as a separate budget line adds psychological noise without adding information. The 3 full-repayment events show the real cash commitment without the double-count.

**Interest visibility after this change:** Interest charges will continue to appear on each loan account in PocketSmith as actual bank transactions. You can see total interest cost by viewing the Loan Interest category in transaction history, or by checking each loan account directly. The budget forecast now shows cash flow only.

**Spreadsheet vs. reality corrections made during this rebuild:**
- Sassafras and Park View repayment amounts were SWAPPED in the spreadsheet. Bank actuals: Sassafras = $2,550/mo, Park View = $3,822/mo.
- Hillside total repayment is $2,928/mo — NOT $2,200/mo. The $2,200 is the rent income that partially offsets it; there is a ~$728/mo gap funded from operating cash.
- The spreadsheet's "$800 extra Hillside" line was a misread of the operating cash top-up needed to cover that gap — not extra principal repayment. No separate Hillside-extra event exists in the live model.
- After restructure, April 2026 budget forecast: income $18,036/mo, expenses $16,748.55/mo, surplus ~$1,287/mo.

---

## Consolidated household budget events (rebuilt 2026-04-24)

**Architecture change 2026-04-24:** Per user direction, restructured to **one event per category**. All household events now consolidated to a single line per category, all on Scott's Complete Access (5009794). Trade-off: per-account scenario forecasting becomes inaccurate (CA shows over-positive flow because Mina salary + Park View rent are budgeted there but actually land in Go Account); household totals are correct. Granular line items (per-property mortgage breakdown, individual insurance policies, termly school fees) are no longer separately tracked in events — see notes below for breakdowns.

| # | Category | Cat ID | Amount | Cadence | Event ID | Notes |
|---|---|---|---:|---|---|---|
| 1 | Income | 31156879 | +$13,496 | monthly | 425545919 | Scott $8,000 + Mina $5,496 |
| 2 | Rentals | 31172254 | +$4,240 | monthly | 425545923 | Hillside $2,200 + Park View $2,040 |
| 3 | Mortgage Repayments | 31156984 | -$9,300 | monthly | 425545927 | Sassafras $2,550 + Park View $3,822 + Hillside $2,928 |
| 4 | Loan Repayments | 31156839 | -$358 | monthly | 425545935 | Harmoney only ($165.55/fortnight). Add BNPL paydown events when scheduled. |
| 5 | Education | 31156959 | -$2,300 | monthly | 425545939 | Annualised: monthly $796 (Music $434, JETS $61×2, Wulfric Boxing $240) + termly $1,504/mo amortised (Salesian $2,898/q, Holy Trinity $1,005/q, MIC $370/q, Salesian guitar $240/q). Total $27,604/yr ÷ 12. |
| 6 | Child Care | 31172219 | -$764 | monthly | 423647039 | Little Lane (Penny, 4 days/week). KEPT from earlier build. |
| 7 | Insurance | 31172234 | -$973 | monthly | 425545943 | Medibank $283 + car $150 + Sassafras bldg $177 + Park View bldg $155 + pet $8 + 2 landlord placeholders $100 each. Recalibrate when actual landlord quotes obtained. |
| 8 | Power | 31172214 | -$432 | monthly | 425545947 | Momentum: electricity $200 + gas $232 |
| 9 | Phone | 31172239 | -$140 | monthly | 425545951 | Wulfric $20 + Mina $120 |
| 10 | Water | 31227443 | -$360 | monthly | 425545955 | Quarterly $1,080 amortised. Park View + Sassafras Greater Western Water |
| 11 | Groceries | 31156854 | -$1,000 | monthly | 423647147 | Committed baseline. KEPT from earlier build. |
| 12 | Government Services | 31156989 | -$441 | monthly | 425545963 | Annualised: Brimbank Council $460/q + Hume Council $654/q ($371/mo) + VicRoads rego $840/yr ($70/mo). |
| 13 | Pets | 31172249 | -$100 | monthly | 425545967 | Titus food/vet placeholder. Pet insurance is in Insurance line. |
| 14 | Land Tax | 31229295 | -$300 | monthly | 425545975 | Placeholder. Update when next assessment arrives. |
| 15 | Basketball | 31229271 | -$250 | monthly | 425545983 | Kids basketball commitments combined. |

## Korea trip events (one-off, Travel category 31172244)

| Line | Date | Amount | Event ID |
|---|---|---:|---|
| Accommodation | 2026-07-01 | -$3,556 | 425545991 |
| Activities | 2026-08-21 | -$1,704 | 425545999 |
| Food | 2026-08-21 | -$3,081 | 425546003 |
| Transport | 2026-08-21 | -$1,573 | 425546011 |
| Misc/Shopping | 2026-08-21 | -$1,885 | 425546019 |
| **Total** | | **-$11,799** | |

Includes 30% buffer per user direction. Flights ($3,000) already paid Apr 2026, not in forecast.

## Mortgage detail (interest breakdown — for reference, not budget events)

The consolidated $9,300/mo Mortgage Repayments event covers:
- Sassafras Drive (PPOR): $2,550/mo total = ~$1,982 interest + ~$568 principal. EOFY flag: ANZ product labelling anomaly (PPOR on product labelled "Residential Investment Loan").
- Park View Tce, Sydenham (investment): $3,822/mo total = ~$3,100 interest + ~$722 principal. Rent ($2,040/mo) partially offsets. Recalibration 2026-07-19.
- Hillside, Celendine (investment, partial family rent): $2,928/mo total = ~$2,318 interest + ~$610 principal. Rent ($2,200/mo) partially offsets; ~$728/mo gap from operating cash.

Interest charges still post on each loan account in PocketSmith as actual bank transactions — visible per-property in the loan account history. Total interest cost ~$88,800/yr; principal paydown ~$22,800/yr.

## Architectural notes

- **Mina's Complete Access (4852629, scenario 5009809):** to be closed by Mina. Some user-created events landed here pre-rebuild — all relocated/deleted 2026-04-24.
- **Mina's Go Account (4854564, scenario 5011809):** receives Mina's salary + Park View rent in real life. Budget treats household as one pool, so these are consolidated to Complete Access in events. When Mina closes the second CA, only the Go Account remains as her side.
- **Cash flow accuracy:** Single-account scenario forecasts will be misleading until rent→offset restructure happens. Household total remains correct.

---

## Annual budget headline (post 2026-04-24 consolidation)

| Line | Monthly | Annual | Notes |
|---|---:|---:|---|
| Income | $13,496 | $161,952 | Scott + Mina |
| Rentals | $4,240 | $50,880 | Both properties |
| **Total inflows** | **$17,736** | **$212,832** | |
| Mortgage Repayments | $9,300 | $111,600 | Full cash repayment, all 3 loans |
| Education (annualised) | $2,300 | $27,600 | Monthly + termly amortised |
| Groceries | $1,000 | $12,000 | |
| Insurance | $973 | $11,676 | All policies + landlord placeholders |
| Child Care | $764 | $9,168 | |
| Government Services | $441 | $5,292 | Council rates + rego amortised |
| Power | $432 | $5,184 | Gas + electricity |
| Loan Repayments | $358 | $4,296 | Harmoney only |
| Water | $360 | $4,320 | Quarterly amortised |
| Land Tax | $300 | $3,600 | Placeholder |
| Basketball | $250 | $3,000 | |
| Phone | $140 | $1,680 | |
| Pets | $100 | $1,200 | |
| **Total expenses** | **$16,718** | **$200,616** | |
| **Surplus (before discretionary)** | **~$1,018** | **~$12,216** | |
| Korea trip 2026 | -$11,799 (Jul/Aug only) | -$11,799 | One-off |
| **12-month net (with Korea)** | | **~$417** | Razor-thin |

> True annual cushion is ~$12,200/yr before discretionary. Korea trip eats almost all of it in 2026. Discretionary spending (eating out, fuel, entertainment, clothing, gifts, kids one-offs) is NOT yet modelled; the August 2026 review with Mina is when discretionary gets added with 3 months of clean actuals as evidence.

Discretionary spending (eating out, fuel, clothing, travel, entertainment, gifts, kids one-offs) is NOT yet modelled. The August 2026 review with Mina is the target for adding this layer with 3 months of actuals as evidence.

---

## Deferred (not yet in PocketSmith)

- **Ambulance Victoria** — yearly amount unknown; create event when next bill arrives
- **Land tax** — yearly amount unknown (investment properties); create when next assessment arrives
- **Discretionary categories** (eating out, fuel, alcohol, entertainment, clothing, travel, gifts, kids one-offs) — separate Mina conversation, evidence-based after 3 months of post-rebuild actuals (target: 2026-08 review)

---

## Recalibration triggers

| Trigger | Action | Next due |
|---|---|---|
| Mortgage interest | Re-pull from 7-month history per loan; offset balance changes will move interest down over time | 2026-07-19 |
| Park View interest specifically | Irregular billing cadence — verify $3,100 is holding vs 6-charge average of $3,277 | 2026-07-19 |
| Income (salaries) | Calibrate from actuals after 3 clean months | 2026-08 review |
| Rental income | Calibrate after 3 clean months of post-restructure data | 2026-08 review |
| Insurance cadence | Switch each insurance line from monthly placeholder to actual yearly when its renewal hits | On renewal |
| Council rates | Confirm exact quarterly billing dates at next bill | On next bill |
| Mina salary scenario | Confirm correct landing account once a pay cycle is visible | 2026-05 |
| Park View rent scenario | Relocate from Westpac Choice to ANZ One Offset post-restructure | Post-restructure |
