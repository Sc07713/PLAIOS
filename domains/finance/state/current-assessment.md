# Finance Domain Assessment

**Last Updated:** 2026-04-19
**Next Review:** 2026-07-19 (3-month post-rebuild check)

## L1.1 Income

- **Rating:** 3 (Functional)
- **Trend:** stable
- **Finding:** Multiple income streams visible (Scott salary/business, Mina transfers, rental). Rental income fragmented across CBA/ANZ/Virgin accounts with mixed payee strings; restructure planned to funnel all rent via ANZ One Offset. Expected monthly rent ~$4,240 (Park View $2,040 net + Hillside $2,200).

## L1.4 Debt & Obligations

- **Rating:** 3 (Functional)
- **Trend:** improving
- **Finding:** Mortgage repayments confirmed from bank transaction history (2026-04-19 rebuild): Sassafras $2,550/mo + Park View $3,822/mo + Hillside $2,928/mo = $9,300/mo total cash out. Note: the household spreadsheet had Sassafras and Park View repayment amounts swapped — corrected during rebuild. Hillside repayment is NOT self-funded by rent ($2,200/mo rent vs $2,928/mo repayment — gap of ~$728/mo from operating cash, because the Hillside loan was topped up to fund the Sassafras PPOR acquisition). Annual interest cost: $88,800 across 3 loans (1,982 + 3,100 + 2,318 averaged from 7-month history). Net principal reduction: ~$22,800/yr. Harmoney: $165.55/fortnight ($4,304/yr), 7-yr term. **BNPL/short-term debt added 2026-04-19 (3 offline accounts):** GEM by Latitude $4,010 + ZipPlus $1,877 + PayPal Pay in 4 $383 = $6,270 total. These are historic discretionary overspend (mostly eating out; GEM is Mina's overspending residue) that got financed rather than paid for cash. Repayments roughly $300/mo combined (variable) from Virgin Go Account. ANZ product labels vs. purpose are inverted (PPOR on investment product, Hillside investment on home product) — flag for accountant at EOFY for interest deductibility. Visibility improved from "spreadsheet estimate" to live-tracked.

## L2.1 Financial Management

- **Rating:** 3 (Functional) — trending Systematic
- **Trend:** improving
- **Finding:** PocketSmith budget rebuilt 2026-04-19 from household spreadsheet (2026 Forecast v2). 31 default events wiped; 35 hand-built events now live, modelling mortgages as Interest (expense, on loan scenarios) + Principal (cash out, on operating scenario) per property, with lumpy items at actual cadence (school fees termly, council rates quarterly, water quarterly, rego yearly). Mapping doc at `reference/pocketsmith-budget-mapping.md` — PocketSmith is now the source of truth; spreadsheet retained as historical input only. Key finding: the spreadsheet claimed +$22,925/yr surplus before discretionary; the corrected model shows approximately -$13,784/yr cash flow after interest before discretionary, offset by ~$22,800/yr principal/equity gain — roughly break-even before discretionary is added. **Late-day 2026-04-19 evidence:** $6,270 BNPL discovered (GEM $4,010 + ZipPlus $1,877 + PayPal $383), confirmed as historic discretionary overspend (mostly eating out). The discretionary gap is no longer hypothetical — it has already manifested as financed debt. New household rule established same day: **no eating out** until BNPL cleared and discretionary baseline established (target: 2026-08 review). Transaction backlog (2,687 uncategorised + 6,739 needs-review) remains unattacked but does not block the forecasting layer.

## L2.5 Legal & Admin

- **Rating:** -
- **Trend:** -
- **Finding:** Not yet assessed. Flag at next tax/accountant touchpoint: loan-purpose vs product-label mismatch for interest deductibility.

## L5.3 Wealth Building

- **Rating:** -
- **Trend:** -
- **Finding:** Not yet assessed. Household net worth snapshot ~+$598K based on $2.2M property equity offset by $1.61M total debt. Super, investments, business equity not yet in PocketSmith.
