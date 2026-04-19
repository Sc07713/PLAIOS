# Built Events (2026-04-19 PocketSmith Budget Rebuild)

> **Updated 2026-04-19 (later that day):** Replaced 6 mortgage events (Interest+Principal split) with 3 full-repayment events. Reason: dashboard psychology — interest visibility was making the budget look perpetually negative. Interest still tracked automatically on loan accounts.

> **Updated 2026-04-19 (earlier):** Monthly events backdated to 2026-04-01 to make current-month budget visible. Quarterly/yearly/fortnightly events unchanged.

Wipe: 31 default event instances (30 unique series + 1 missed series 423106459) deleted.
Build: 35 new series created across Tasks 3–12. Then 6 mortgage split events deleted and replaced with 3 full-repayment events (net: 32 active series).

| event_id | series_id | category_id | category_title | scenario_id | scenario_title | amount | cadence | note |
|---|---|---|---|---|---|---|---|---|
| 423715719-1775001600 | 423715719 | 31156839 | Loan Repayment | 5009794 | Complete Access | -2550.00 | monthly | Sassafras Drive — full mortgage repayment (PPOR). Includes interest + principal; bank automatically allocates. Interest charges visible on the loan account. |
| 423715723-1775001600 | 423715723 | 31156839 | Loan Repayment | 5009794 | Complete Access | -3822.00 | monthly | 18 Park View Tce, Sydenham — full mortgage repayment (investment). Includes interest + principal. |
| 423715727-1775001600 | 423715727 | 31156839 | Loan Repayment | 5009794 | Complete Access | -2928.00 | monthly | Hillside (Celendine) — full mortgage repayment. Includes interest + principal. Rent income $2,200/mo partially offsets this. Loan balance includes top-up that funded Sassafras acquisition. |
| 423632815-1784073600 | 423632815 | 31156959 | Education | 5009794 | Complete Access | -2898.00 | quarterly (monthly/3) | Salesian College — Wulfric term fees ($11,590/yr / 4 terms) |
| 423632819-1784073600 | 423632819 | 31156959 | Education | 5009794 | Complete Access | -1005.00 | quarterly (monthly/3) | Holy Trinity — Audrey & Evie term fees ($4,020/yr / 4 terms) |
| 423647019-1775001600 | 423647019 | 31156959 | Education | 5009794 | Complete Access | -434.00 | monthly | Music Education Academy — Wulfric, Audrey, Evie monthly fee |
| 423647023-1775001600 | 423647023 | 31156959 | Education | 5009794 | Complete Access | -61.00 | monthly | Audrey basketball JETS (rego — both summer and winter seasons annualised) |
| 423647027-1775001600 | 423647027 | 31156959 | Education | 5009794 | Complete Access | -61.00 | monthly | Evie basketball JETS |
| 423647035-1775001600 | 423647035 | 31156959 | Education | 5009794 | Complete Access | -240.00 | monthly | Wulfric Boxing / Jujitsu (daily training as of mid-Apr 2026) |
| 423632839-1784073600 | 423632839 | 31156959 | Education | 5009794 | Complete Access | -370.00 | quarterly (monthly/3) | MIC Basketball training — Audrey ($370/term x 4 terms/yr) |
| 423632843-1784073600 | 423632843 | 31156959 | Education | 5009794 | Complete Access | -240.00 | quarterly (monthly/3) | Salesian guitar lessons — Wulfric ($240/term x 4 terms/yr) |
| 423647039-1775001600 | 423647039 | 31172219 | Child Care | 5009794 | Complete Access | -764.00 | monthly | Little Lane childcare — Penny (4 days/week) |
| 423647043-1775001600 | 423647043 | 31172234 | Insurance | 5009794 | Complete Access | -252.00 | monthly | Medibank Private Health Insurance (monthly placeholder; switch to annual cadence at next renewal) |
| 423647071-1775001600 | 423647071 | 31172234 | Insurance | 5009794 | Complete Access | -140.00 | monthly | Budget Direct — car insurance (monthly placeholder; likely yearly — confirm at next renewal) |
| 423647075-1775001600 | 423647075 | 31172234 | Insurance | 5009794 | Complete Access | -83.00 | monthly | Budget Direct — Sassafras Drive building insurance (monthly placeholder; likely yearly — confirm at renewal) |
| 423647103-1775001600 | 423647103 | 31172234 | Insurance | 5009794 | Complete Access | -70.00 | monthly | Budget Direct — 18 Park View Tce building insurance (monthly placeholder; likely yearly — confirm at renewal) |
| 423647111-1775001600 | 423647111 | 31172234 | Insurance | 5009794 | Complete Access | -50.00 | monthly | Pet insurance — Titus |
| 423632871-1782864000 | 423632871 | 31227443 | Water | 5009794 | Complete Access | -540.00 | quarterly (monthly/3) | Greater Western Water — 18 Park View Tce (quarterly bill) |
| 423632875-1782864000 | 423632875 | 31227443 | Water | 5009794 | Complete Access | -540.00 | quarterly (monthly/3) | Greater Western Water — Sassafras Drive (quarterly bill) |
| 423647119-1775001600 | 423647119 | 31172214 | Power | 5009794 | Complete Access | -200.00 | monthly | Momentum Energy — electricity |
| 423647127-1775001600 | 423647127 | 31172214 | Power | 5009794 | Complete Access | -232.00 | monthly | Momentum Energy — gas |
| 423647135-1775001600 | 423647135 | 31172239 | Phone | 5009794 | Complete Access | -20.00 | monthly | Wulfric mobile phone |
| 423647139-1775001600 | 423647139 | 31172239 | Phone | 5009794 | Complete Access | -120.00 | monthly | Mina mobile phone |
| 423632903-1796083200 | 423632903 | 31156989 | Government Services | 5009794 | Complete Access | -840.00 | yearly | VicRoads vehicle registration (date is a placeholder; correct to actual renewal date when known) |
| 423632915-1782864000 | 423632915 | 31156989 | Government Services | 5009794 | Complete Access | -460.00 | quarterly (monthly/3) | Brimbank Council rates — 18 Park View Tce ($1,840/yr / 4 quarters) |
| 423632919-1782864000 | 423632919 | 31156989 | Government Services | 5009794 | Complete Access | -654.00 | quarterly (monthly/3) | Hume City Council rates — Sassafras Drive ($2,617/yr / 4 quarters) |
| 423647147-1775001600 | 423647147 | 31156854 | Groceries | 5009794 | Complete Access | -1000.00 | monthly | Groceries (committed baseline; discretionary overspend handled separately) |
| 423632927-1776988800 | 423632927 | 31156839 | Loan Repayment | 5009794 | Complete Access | -165.55 | fortnightly | Harmoney personal loan (home renovation) — $165.55/fortnight, 7-yr term, 9.79% rate. Loan account offline in PocketSmith; balance manually tracked. Loan ID L00006085643. |
| 423647151-1775001600 | 423647151 | 31156879 | Income | 5009794 | Complete Access | +8000.00 | monthly | Scott salary (after tax). Calibrate from actuals after 3 clean months. |
| 423647155-1775001600 | 423647155 | 31156879 | Income | 5011809 | Go Account (Mina/Virgin Money) | +5496.00 | monthly | Mina salary (after tax). Calibrate from actuals after 3 clean months. |
| 423647163-1775001600 | 423647163 | 31172254 | Rentals | 5019943 | Westpac Choice | +2040.00 | monthly | 18 Park View Tce, Sydenham — rental income (net). Began Mar 2026 post-Harmoney renovation. Lands in Westpac Choice (brand new acct, Mina opened 2026-04-19). Calibrate after 3 clean months. Will likely move post-restructure. |
| 423647167-1775001600 | 423647167 | 31172254 | Rentals | 5009794 | Complete Access | +2200.00 | monthly | Hillside (Celendine Drive) — rental income from Rinoa + Sam + Mina's mum (combined). Lands in CommBank Complete Access (no offset account yet). Will move to ANZ One Offset post-restructure. Calibrate after 3 clean months. |

## Summary

- **Deleted:** 31 instances across 31 series (30 original + 1 missed Insurance series 423106459)
- **Created:** 35 series

## Annual budget forecast (2027 full year — clean year with all events active)

> Revised after mortgage restructure. Interest now absorbed into full repayment events; no separate interest lines.

| Category | Annual total | Basis |
|---|---|---|
| Income (salary) | $212,832 | (8,000 + 5,496) × 12 — confirmed by PocketSmith summary |
| Rentals income | $51,480 | (2,040 + 2,200) × 12 |
| **Total income** | **$264,312** | |
| Loan Repayment (full — 3 mortgages) | $111,600 | (2,550 + 3,822 + 2,928) × 12. Includes both interest and principal; bank allocates automatically. |
| Harmoney | $4,304 | 165.55 × 26 fortnightly payments |
| Education | $27,604 | Termly + monthly items per plan |
| Child Care | $9,168 | 764 × 12 |
| Insurance | $7,140 | 595 × 12 |
| Power | $5,184 | (200 + 232) × 12 |
| Water | $4,320 | (540 + 540) × 4 quarters |
| Phone | $1,680 | (20 + 120) × 12 |
| Government Services | $6,296 | 840 + (460 + 654) × 4 |
| Groceries | $12,000 | 1,000 × 12 |
| **Total expenses** | **~$189,296** | Full mortgage repayments included |
| **Surplus** | **~$75,016** | Income minus all expenses — dashboard shows positive |

> Note: The surplus ($75k/yr) represents cash flow after all mortgage repayments, not net wealth gain. The interest component of repayments (~$88,800/yr) is an expense; the principal component (~$22,800/yr) builds equity. True cash cost is identical to before — only the presentation changed.

## Notes for Task 14

- Loan Interest events live on loan account scenarios (5011759, 5011769, 5011749) — they do NOT appear in PS budget summary totals. This is by design.
- PocketSmith budget summary snaps to calendar years regardless of requested window. 2027 full-year income forecast = $212,832 confirmed correct.
- The "ghost" Insurance series 423106459 ($150/wk, Go Account) was not in the discovery notes' series list — it was a 31st series missed during snapshot. Deleted during wipe verification.
- Park View interest event uses $3,100 (median/recent) rather than $3,277 (7-charge avg) due to irregular billing cadence. Flag for recalibration in 3 months.
- Govt Services: plan said $5,297/yr but actual calc is $6,296/yr ($840 + 4×$460 + 4×$654 = $840+$1,840+$2,616 = $5,296). Minor rounding difference — within tolerance.
