# PocketSmith Budget Rebuild — Discovery Notes (2026-04-19)

## Account → Scenario Map

All accounts for user 783484 (Scott McKennie):

| account_id | Title | Number (last 6) | Institution | scenario_id | scenario_title | Balance |
|------------|-------|-----------------|-------------|-------------|----------------|---------|
| 4852609 | NetBank Saver | ...784212 | CommBank | 5009789 | NetBank Saver | $0.02 |
| 4852614 | Complete Access | ...247233 | CommBank | 5009794 | Complete Access | $173.55 |
| 4852619 | Commonwealth Direct Investment Account | ...712080 | CommBank | 5009799 | Commonwealth Direct Investment Account | $0.35 |
| 4852624 | NetBank Saver | ...346506 | CommBank | 5009804 | NetBank Saver | $0.01 |
| 4852629 | Complete Access | ...003194 | CommBank | 5009809 | Complete Access | $0.90 |
| 4854509 | Residential Investment Loan | ...299801 | ANZ | 5011749 | Residential Investment Loan | -$491,099.25 |
| 4854514 | ANZ Online Saver | ...008862 | ANZ | 5011754 | ANZ Online Saver | $0.01 |
| 4854519 | Variable Home Loan | ...299828 | ANZ | 5011759 | Variable Home Loan | -$439,347.92 |
| 4854524 | ANZ One Offset Account | ...485465 | ANZ | 5011764 | ANZ One Offset Account | $0.01 |
| 4854529 | Residential Investment Loan | ...548206 | ANZ | 5011769 | Residential Investment Loan | -$659,700.61 |
| 4854564 | Go Account | ...280769 | Virgin Money | 5011809 | Go Account | $1,573.96 |
| 4854569 | Boost Saver | ...552361 | Virgin Money | 5011814 | Boost Saver | — |
| 4859349 | 31 Sassafras Dr, Sunbury (PPOR) | (manual) | Real Estate | 5016724 | 31 Sassafras Dr, Sunbury (PPOR) | — |
| 4859354 | 18 Park View Tce, Sydenham (Investment) | (manual) | Real Estate | 5016729 | 18 Park View Tce, Sydenham (Investment) | — |
| 4859359 | 3 Celendine Pl, Hillside (Investment) | (manual) | Real Estate | 5016734 | 3 Celendine Pl, Hillside (Investment) | — |
| 4859364 | Harmoney Home Improvement Loan | (manual) | Harmoney | 5016739 | Harmoney Home Improvement Loan | — |
| 4862451 | Westpac Choice | ...593340 | Westpac | 5019943 | Westpac Choice | $735.10 |

### Key Scenarios (confirmed)

- **Complete Access (Scott, ends 7233):** account_id=4852614, scenario_id=**5009794**
- **Go Account (Mina's Virgin Money):** account_id=4854564, scenario_id=**5011809**
- **Variable Home Loan = Sassafras PPOR:** account_id=4854519, scenario_id=**5011759** (balance -$439k, repayment $2,550/mo)
- **Park View loan (Sydenham investment, settled Sep 2025):** account_id=4854529, scenario_id=**5011769** (balance -$660k, repayment $3,822/mo; settlement transactions on 2025-09-29 confirm this is the recently purchased property)
- **Hillside loan (Celendine):** account_id=4854509, scenario_id=**5011749** (balance -$491k, repayment $2,928/mo)
- **Account ending 7233 = Complete Access (Scott):** confirmed above — number 06314110**247233**
- **ANZ One Offset Account:** account_id=4854524, scenario_id=**5011764** (destination for rent per PLAIOS memory)
- **Harmoney Home Improvement Loan:** account_id=4859364, scenario_id=**5016739**

### FLAGGED: Unidentified scenarios

The following accounts were NOT clearly identifiable as specific roles:

- **Mina's pay landing account:** UNKNOWN. Candidates are:
  - account_id=4852629 "Complete Access" (CommBank, BSB 063984, ..003194) — likely Mina's CommBank account
  - account_id=4862451 "Westpac Choice" (Westpac, added 2026-04-19, balance $735.10) — brand new account, possibly Mina's pay account (Westpac)
  - **Scott's recommendation needed:** Which account does Mina's pay land in?
  
- **Park View rental landing:** UNKNOWN. No account title clearly identifies it as Park View rental income. Per PLAIOS memory, rent is being restructured to go into ANZ One Offset (4854524). Until that restructure is live, rental income destination is unclear.

- **Hillside rental landing:** Rinoa pays $2,200/mo into UNKNOWN account. Per memory, $800 was outstanding Apr 2026. Same destination uncertainty as Park View.

> These unknowns do not block Task 2 (wipe) but must be resolved before Task 3+ if events need to be placed in rental income scenarios.

---

## Existing Events Snapshot

- **Total events found: 31** (matches expected ~31)
- **Snapshot file:** `domains/finance/reference/_budget_dumps/2026-04-19-pre-rebuild-events.json`
- **Date range queried:** 2026-04-01 to 2026-05-31

### Manual Edit Flags (Step 1.3)

Comparing `created_at` vs `updated_at` for each event:

- Events in **Go Account scenario (5011809):** All show `created_at: 2026-04-17T14:57:30Z` and `updated_at: 2026-04-19T05:02:06Z`. Delta = ~1.5 days. **FLAGGED** — these appear to have been batch-updated on 2026-04-19. 15 events affected. All Go Account events share identical updated_at timestamp suggesting a single bulk operation, not manual individual edits.

- Events in **Complete Access scenario (5009794):** `created_at: 2026-04-17T06:11:31Z`, `updated_at: 2026-04-18T16:08:56Z`. Delta = ~1.3 days. **FLAGGED** — updated roughly 1.3 days after creation. 5 events affected.

- **Variable Home Loan Interest event (5011759):** `created_at: 2026-04-17T06:11:35Z`, `updated_at: 2026-04-18T01:46:36Z`. Delta = ~19 hours. Marginal flag.

- **Rentals event (5011809):** `updated_at: 2026-04-18T01:46:37Z` — updated the day after creation, likely part of the same Apr 18 bulk update.

**Assessment:** The >1 day gaps appear to be from a single session of edits on 2026-04-17 and 2026-04-18 (shortly after PocketSmith was set up on 2026-04-17). These are likely initial setup adjustments, NOT cherished manual edits. However, Scott should confirm before the wipe that none of these represent intentional customisations he wants to preserve.

**Notably: zero events were manually created separately from the initial setup batch. Safe to wipe pending Scott's confirm.**

---

## Mortgage Interest History (avg per loan)

### Method
Pulled transactions with category_id=31204939 (Loan Interest) for each loan account, 2025-09-01 to 2026-04-18. All three loans returned full results from Loan Interest category — no fallback to old Interest category needed.

### Sassafras PPOR — Account 4854519 "Variable Home Loan"

| Date | Interest charged |
|------|-----------------|
| 2025-09-25 | $2,020.35 |
| 2025-10-27 | $1,951.37 |
| 2025-11-25 | $2,008.87 |
| 2025-12-29 | $1,948.18 |
| 2026-01-27 | $2,012.03 |
| 2026-02-25 | $2,045.47 |
| 2026-03-25 | $1,886.60 |

**Total: $13,872.87 / 7 months = $1,981.84/mo average**
**Repayment: $2,550.01/mo**

### Park View (Sydenham) — Account 4854529 "Residential Investment Loan"

Loan settled 2025-09-29. Interest charge cadence is irregular (some months have two charges: first-of-month and end-of-month). 6 interest charges over ~6 months:

| Date | Interest charged |
|------|-----------------|
| 2025-10-29 | $3,066.99 |
| 2025-12-01 | $3,162.32 |
| 2025-12-29 | $3,061.04 |
| 2026-01-29 | $3,158.85 |
| 2026-03-02 | $3,121.81 |
| 2026-03-30 | $3,090.42 |

Note: No Nov 2025 interest charge visible. Two charges in Dec 2025 and two in Mar 2026 — likely due to fortnightly or irregular ANZ billing cycle on this loan.

**Total: $19,661.43 / 6 charges = $3,276.91/mo average**
**Repayment: $3,821.77/mo**

**NOTE:** The billing cadence irregularity means the average may be slightly off. Consider using $3,100-3,150 range (median cluster) or the most recent charge ($3,090) as the event amount.

### Hillside — Account 4854509 "Residential Investment Loan"

| Date | Interest charged |
|------|-----------------|
| 2025-09-25 | $2,362.61 |
| 2025-10-27 | $2,281.51 |
| 2025-11-25 | $2,353.23 |
| 2025-12-29 | $2,274.11 |
| 2026-01-27 | $2,348.74 |
| 2026-02-25 | $2,390.03 |
| 2026-03-25 | $2,214.64 |

**Total: $16,224.87 / 7 months = $2,317.84/mo average**
**Repayment: $2,928-2,932/mo**

### Hillside vs $2,200 assumption

The task validates Hillside interest ≈ $2,200/mo. **Actual avg = $2,318/mo — diverges by +5.3%.** Within ±10% threshold, no stop required. Recorded as a minor divergence.

**BIGGER CONCERN:** The task description template uses "$2,200" as the Hillside REPAYMENT figure ("Hillside (min): $2,200 - interest = principal"). But actual minimum repayment per transactions is **$2,928/mo** (not $2,200). The $2,200 figure in PLAIOS memory refers to Rinoa's RENT payment, not the loan repayment. This needs Scott's eyes — the principal/interest split in Task 4 should be based on $2,928 repayment, not $2,200.

---

## Principal Portion Calculations (for Task 4)

Using actual repayments from transaction history:

- **Sassafras:** $2,550 - $1,982 = **$568/mo principal**
- **Park View:** $3,822 - $3,277 = **$545/mo principal** (or use $3,822 - $3,100 = $722 based on median)
- **Hillside (min repayment):** $2,928 - $2,318 = **$610/mo principal**
- **Hillside (extra):** $800/mo (Rinoa's rent shortfall or extra repayment — per memory, ~$800 outstanding Apr 2026)

> NOTE: If the plan intends $2,200 as Hillside repayment minimum, that differs from $2,928 actual. Flagged for human review.

---

## Water Sub-Category

- **Decision:** Created
- **Category ID: 31227443**
- **Title:** Water
- **Parent:** Utilities and Services (id 31156994)
- **Colour:** #5c87c1
- **Created:** 2026-04-19T05:11:04Z

---

## Scenario IDs to Use in Build Phase

| Role | account_id | scenario_id | Notes |
|------|-----------|-------------|-------|
| Complete Access (Scott's main) | 4852614 | **5009794** | Number ends 7233 |
| Go Account (Mina's spending) | 4854564 | **5011809** | Virgin Money credit card |
| Sassafras loan (Variable Home Loan) | 4854519 | **5011759** | PPOR, balance -$439k |
| Park View loan (Sydenham investment) | 4854529 | **5011769** | Settled Sep 2025, balance -$660k |
| Hillside loan (Celendine) | 4854509 | **5011749** | Balance -$491k |
| Harmoney Home Improvement Loan | 4859364 | **5016739** | Manual account |
| ANZ One Offset Account | 4854524 | **5011764** | Future rent destination |
| Mina's pay landing | UNKNOWN | UNKNOWN | See flagged items above |
| Park View rent landing | UNKNOWN | UNKNOWN | See flagged items above |
| Hillside rent landing | UNKNOWN | UNKNOWN | See flagged items above |
| Mina CommBank Complete Access | 4852629 | 5009809 | Best guess for Mina's landing |
| Westpac Choice (brand new) | 4862451 | 5019943 | Added 2026-04-19, possibly Mina's pay |

---

## Anomalies / Decisions for Human Review

### 1. MUST CONFIRM: Mina's pay landing account
No account title clearly identifies where Mina's salary lands. Two candidates: CommBank Complete Access (BSB 063984, account 4852629) or brand-new Westpac Choice (added 2026-04-19). **Scott: where does Mina's pay land?**

### 2. MUST CONFIRM: Rental income landing accounts
No accounts labelled as Park View rental or Hillside rental income. Per PLAIOS memory, rent restructure to ANZ One Offset is not yet live. **Scott: which account(s) currently receive Park View and Hillside rent?**

### 3. MUST CONFIRM: Hillside repayment figure
Task description uses $2,200 as Hillside minimum repayment, but actual transaction history shows $2,928/mo repayments. The $2,200 is Rinoa's rent, not the loan repayment. Confirm: should interest + principal events for Hillside use $2,928 (actual) or $2,200 (template)?

### 4. NOTE: Park View interest billing cadence irregular
6 charges over Oct 2025-Mar 2026 with two charges in both Dec 2025 and Mar 2026 (no charge visible in Nov 2025). Average of $3,277 may not reflect true monthly run rate. Recommend using $3,100-$3,150 range or most recent charge ($3,090) for the budget event amount.

### 5. NOTE: Go Account "updated_at" flags
All 15 Go Account events show updated_at ~1.5 days after created_at (bulk update 2026-04-19). These are almost certainly initial setup adjustments, not cherished edits. But confirm before wipe.

### 6. NOTE: Westpac Choice is brand new (added 2026-04-19)
This account didn't exist when PocketSmith was set up on 2026-04-17. It may be relevant to the budget rebuild if it's a new pay/rent landing account.

---

## Series IDs for Wipe (Task 2)

All 31 events identified. Series IDs to delete (use `behaviour="all"`):

| series_id | category | scenario | amount | repeat |
|-----------|----------|----------|--------|--------|
| 423106324 | Interest | Variable Home Loan (5011759) | -$7,000 | monthly |
| 423106349 | Bank Fees | Go Account (5011809) | -$65 | monthly |
| 423106354 | Income | Complete Access (5009794) | +$7,600 | monthly |
| 423106364 | Recreation | Go Account (5011809) | -$170 | monthly |
| 423106369 | Fuel | Go Account (5011809) | -$45 | monthly |
| 423106374 | Entertainment | Go Account (5011809) | -$14 | monthly |
| 423106379 | Automotive | Go Account (5011809) | -$150 | monthly |
| 423106384 | Professional Services | Go Account (5011809) | -$550 | monthly |
| 423106389 | Alcohol & Bars | Go Account (5011809) | -$90 | monthly |
| 423106394 | Transport | Complete Access (5009794) | -$170 | monthly |
| 423106399 | Healthcare / Medical | Go Account (5011809) | -$260 | monthly |
| 423106404 | Education | Go Account (5011809) | -$1,300 | monthly |
| 423106409 | Cash Withdrawal | Complete Access (5009794) | -$150 | monthly |
| 423106414 | Media | Go Account (5011809) | -$40 | monthly |
| 423106419 | Home Improvement | Complete Access (5009794) | -$1,000 | monthly |
| 423106424 | Clothing | Go Account (5011809) | -$50 | monthly |
| 423106429 | Housing | Go Account (5011809) | -$900 | monthly |
| 423106434 | Government Services | Go Account (5011809) | -$40 | monthly |
| 423106439 | Internet | Go Account (5011809) | -$30 | monthly |
| 423106444 | Personal Care | Go Account (5011809) | -$320 | monthly |
| 423106449 | Power | Go Account (5011809) | -$400 | monthly |
| 423106454 | Child Care | Go Account (5011809) | -$600 | monthly |
| 423106464 | Phone | Go Account (5011809) | -$120 | monthly |
| 423106469 | Pets | Go Account (5011809) | -$25 | monthly |
| 423106474 | Rentals | Go Account (5011809) | -$17 | monthly |
| 423106329 | Transfers | Complete Access (5009794) | -$4,600 | weekly |
| 423106334 | Eating Out | Go Account (5011809) | -$360 | weekly |
| 423106339 | Groceries | Go Account (5011809) | -$340 | weekly |
| 423106344 | Computing | Complete Access (5009794) | -$30 | weekly |
| 423106359 | Household | Go Account (5011809) | -$1,900 | weekly |

> Note: Only 30 series_ids listed above. The snapshot contains 31 event instances (two date slots for some weekly series in the Apr 1 - May 31 window), but there are 30 unique series. Double-check count in wipe phase.
