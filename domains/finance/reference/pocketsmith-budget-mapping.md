# PocketSmith Budget — Mapping & Provenance

**Last rebuilt:** 2026-04-19
**Source:** `mckennie-household-budget.xlsx` (sheet: 2026 Forecast v2)
**Design spec:** `docs/superpowers/specs/2026-04-19-pocketsmith-budget-design.md`
**Implementation plan:** `docs/superpowers/plans/2026-04-19-pocketsmith-budget-rebuild.md`

PocketSmith is now the source of truth for committed household cashflow. The spreadsheet is retained as historical input only.

---

## How to interpret the numbers

**Loan Interest events live on loan account scenarios** — they will NOT appear in the standard PocketSmith expense dashboard or budget summary for the Complete Access scenario. To see total household interest cost ($88,800/yr), query the Loan Interest category directly across all scenarios, or look at each loan scenario individually.

**Loan Repayment (principal) events are on the Complete Access operating scenario** and are NOT marked as transfers in PocketSmith (that is a future refinement). They DO show as expenses. The net effect is correct: cash leaves the operating account and reduces the loan balance.

**The model will appear "expense heavy"** because the same mortgage repayment dollar shows up in two places:
- As an interest cost on the loan account scenario (economic cost of debt)
- As a principal expense on the operating account scenario (cash leaving to reduce balance)

Total cash leaving operating accounts per mortgage each month = interest event + principal event combined. This is accurate cashflow modelling — it just requires knowing which layer you are looking at.

**Spreadsheet vs. reality corrections made during this rebuild:**
- Sassafras and Park View repayment amounts were SWAPPED in the spreadsheet. Bank actuals: Sassafras = $2,550/mo, Park View = $3,822/mo.
- Hillside total repayment is $2,928/mo — NOT $2,200/mo. The $2,200 is the rent income that partially offsets it; there is a ~$728/mo gap funded from operating cash.
- The spreadsheet's "$800 extra Hillside" line was a misread of the operating cash top-up needed to cover that gap — not extra principal repayment. No separate Hillside-extra event exists in the live model.
- The spreadsheet was claiming +$22,925/yr surplus before discretionary. The corrected model shows approximately **-$13,784/yr cash flow after interest, before discretionary**, offset by ~$22,800/yr principal/equity gain.

---

## Mortgage events (per property)

For each property, two events exist:
- **Interest** event on the loan account scenario — category `Loan Interest` (id 31204939) — economic cost of debt, calibrated from 7-month transaction history
- **Principal** event on the Complete Access scenario — category `Loan Repayment` (id 31156839) — cash leaving operating account for debt reduction

| Property | Total repayment | Interest event ID | Interest amount | Principal event ID | Principal amount | Interest scenario | Principal scenario |
|---|---|---|---|---|---|---|---|
| Sassafras Drive (PPOR) | $2,550/mo | 423646903 | $1,982/mo | 423646919 | $568/mo | Variable Home Loan (5011759) | Complete Access (5009794) |
| Park View Tce, Sydenham | $3,822/mo | 423646911 | $3,100/mo | 423647011 | $722/mo | Residential Investment Loan (5011769) | Complete Access (5009794) |
| Hillside, Celendine (combined) | $2,928/mo | 423646915 | $2,318/mo | 423647015 | $610/mo | Residential Investment Loan (5011749) | Complete Access (5009794) |

**Notes on mortgage amounts:**
- Sassafras: 7-month avg interest $1,981.84/mo; rounded to $1,982. Principal = $2,550 − $1,982 = $568.
- Park View: 6-charge avg $3,277 but irregular billing cadence; $3,100 used (recent median, better reflects current run rate). Principal = $3,822 − $3,100 = $722. Flag for recalibration at next quarterly review (2026-07-19).
- Hillside: 7-month avg interest $2,317.84/mo; rounded to $2,318. Principal = $2,928 − $2,318 = $610. Rent income ($2,200/mo from Rinoa + Sam + Mina's mum) partially offsets repayment; ~$728/mo gap funded from operating cash.
- ANZ product labelling anomaly: PPOR Sassafras is on a product labelled "Residential Investment Loan" and vice versa — flag for accountant at EOFY for interest deductibility review.

---

## Non-mortgage events

| Spreadsheet line | Category | Category ID | Cadence | Amount | Event ID | Scenario |
|---|---|---|---|---|---|---|
| Salesian College fees (Wulfric) | Education | 31156959 | termly (quarterly) | $2,898 | 423632815 | Complete Access (5009794) |
| Holy Trinity fees (Audrey & Evie) | Education | 31156959 | termly (quarterly) | $1,005 | 423632819 | Complete Access (5009794) |
| Music Education Academy | Education | 31156959 | monthly | $434 | 423647019 | Complete Access (5009794) |
| Audrey basketball JETS | Education | 31156959 | monthly | $61 | 423647023 | Complete Access (5009794) |
| Evie basketball JETS | Education | 31156959 | monthly | $61 | 423647027 | Complete Access (5009794) |
| Wulfric Boxing / Jujitsu | Education | 31156959 | monthly | $240 | 423647035 | Complete Access (5009794) |
| MIC Basketball training (Audrey) | Education | 31156959 | termly (quarterly) | $370 | 423632839 | Complete Access (5009794) |
| Salesian guitar lessons (Wulfric) | Education | 31156959 | termly (quarterly) | $240 | 423632843 | Complete Access (5009794) |
| Little Lane childcare (Penny) | Child Care | 31172219 | monthly | $764 | 423647039 | Complete Access (5009794) |
| Medibank Private Health | Insurance | 31172234 | monthly* | $252 | 423647043 | Complete Access (5009794) |
| Budget Direct — car | Insurance | 31172234 | monthly* | $140 | 423647071 | Complete Access (5009794) |
| Budget Direct — Sassafras building | Insurance | 31172234 | monthly* | $83 | 423647075 | Complete Access (5009794) |
| Budget Direct — Park View building | Insurance | 31172234 | monthly* | $70 | 423647103 | Complete Access (5009794) |
| Pet insurance — Titus | Insurance | 31172234 | monthly | $50 | 423647111 | Complete Access (5009794) |
| Greater Western Water (Park View) | Water | 31227443 | quarterly | $540 | 423632871 | Complete Access (5009794) |
| Greater Western Water (Sassafras) | Water | 31227443 | quarterly | $540 | 423632875 | Complete Access (5009794) |
| Momentum Energy — electricity | Power | 31172214 | monthly | $200 | 423647119 | Complete Access (5009794) |
| Momentum Energy — gas | Power | 31172214 | monthly | $232 | 423647127 | Complete Access (5009794) |
| Wulfric mobile | Phone | 31172239 | monthly | $20 | 423647135 | Complete Access (5009794) |
| Mina mobile | Phone | 31172239 | monthly | $120 | 423647139 | Complete Access (5009794) |
| VicRoads rego | Government Services | 31156989 | yearly | $840 | 423632903 | Complete Access (5009794) |
| Brimbank Council rates (Park View) | Government Services | 31156989 | quarterly | $460 | 423632915 | Complete Access (5009794) |
| Hume City Council rates (Sassafras) | Government Services | 31156989 | quarterly | $654 | 423632919 | Complete Access (5009794) |
| Groceries | Groceries | 31156854 | monthly | $1,000 | 423647147 | Complete Access (5009794) |
| Harmoney repayment (home reno) | Loan Repayment | 31156839 | fortnightly | $165.55 | 423632927 | Complete Access (5009794) |
| Scott salary | Income | 31156879 | monthly | $8,000 | 423647151 | Complete Access (5009794) |
| Mina salary | Income | 31156879 | monthly | $5,496 | 423647155 | Go Account / Mina (5011809) |
| Park View rent (Sydenham) | Rentals | 31172254 | monthly | $2,040 | 423647163 | Westpac Choice (5019943) |
| Hillside rent (Celendine) | Rentals | 31172254 | monthly | $2,200 | 423647167 | Complete Access (5009794) |

*Insurance monthly placeholders — switch to actual yearly cadence and renewal date when next bill arrives.

**Note on Mina's salary scenario:** At build time, Mina's pay was placed on the Go Account scenario (5011809) as the best available match. Confirm landing account once a clean pay cycle is visible in PocketSmith, and relocate event if needed.

**Note on Park View rent scenario:** Lands in the brand-new Westpac Choice account (5019943, opened 2026-04-19 by Mina). Relocate event post-restructure when rent funnels to ANZ One Offset.

---

## Annual budget headline (2027 full year — first complete year with all events active)

| Line | Annual | Notes |
|---|---|---|
| Scott salary | $96,000 | $8,000 × 12 |
| Mina salary | $65,952 | $5,496 × 12 |
| Park View rent | $24,480 | $2,040 × 12 |
| Hillside rent | $26,400 | $2,200 × 12 |
| **Total income** | **$212,832** | Confirmed by PocketSmith summary |
| Loan Interest (3 properties) | $88,800 | (1,982 + 3,100 + 2,318) × 12 — on loan scenarios, excluded from PS budget summary |
| Loan Repayment (principal, 3 mortgages) | $22,800 | (568 + 722 + 610) × 12 |
| Harmoney | $4,304 | $165.55 × 26 fortnightly |
| Education | $27,604 | Termly + monthly items |
| Child Care | $9,168 | $764 × 12 |
| Insurance | $7,140 | $595 × 12 |
| Power | $5,184 | ($200 + $232) × 12 |
| Water | $4,320 | ($540 + $540) × 4 quarters |
| Phone | $1,680 | ($20 + $120) × 12 |
| Government Services | $6,296 | $840 + ($460 + $654) × 4 |
| Groceries | $12,000 | $1,000 × 12 |
| **Total expenses (excl. interest)** | **$100,496** | Principal + all other committed costs |
| **Cash flow after interest, before discretionary** | **~-$13,784** | Income $212,832 − expenses $100,496 − interest $88,800 — offset by ~$22,800 principal/equity gain |

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
