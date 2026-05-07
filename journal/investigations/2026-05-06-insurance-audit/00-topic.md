# 00 — Topic intake: insurance audit

**Date opened:** 2026-05-06
**Initiator:** Scott
**Trigger:** Mina has proposed insurance replacements; need to audit current vs alternatives.

## Convergence target (narrowed 2026-05-06 by user)

**In scope:** building, contents, car insurance — best price for adequate cover.
**Out of scope (parked for later session):** life / IP / TPD / trauma / super-based cover, private health (Medibank), pet (PetSure).

Decision: for each in-scope line, keep current (Budget Direct) / switch to CBA-Hollard / switch to a third insurer / restructure. Plus: add building cover for currently-uninsured Hillside.

Outputs: 1-page decision record at `journal/decisions/2026-05-06-insurance-audit.md`, full record at `10-final-output.md`, switch tasks for each line touched.

## Out-of-scope findings (logged for later session)

The investigation identified severe under-insurance in life / IP / TPD / trauma cover and zero buffer for self-insurance, with a pregnancy-driven underwriting deadline of ~late Aug/Sep 2026. **User parked this; flag in close-out memory.** Do not let the parking erase the timing pressure — surface again in the next strategic session.

## Financial picture (derived from PocketSmith 2026-05-06)

**Income:**
- Scott (RapidMap payroll): ~$104k/yr net take-home (~$145k gross, rough — confirm in spec phase). Fortnightly payroll $4,000.62.
- Mina: $0 visible in PocketSmith — likely either non-working or income flows to an account not connected to PocketSmith. Confirm in spec phase.
- Rental income: ~$2,200/mo Hillside (Rinoa+Sam+Mina's mum, partially paid Apr) + ~$2,098/mo Sydenham (Park View, net of property manager). Combined ~$4,300/mo gross rent.

**Liabilities:**
- Mortgages: $1,588,879 total
  - Sassafras (PPOR, ANZ Variable): $438,961
  - Sydenham / Park View (ANZ Investment): $659,203
  - Hillside / Celendine (ANZ Investment): $490,716
- Harmoney home-improvement loan: $19,000
- BNPL: GEM $4,010 + ZipPlus $1,877 + PayPal $383 = $6,270
- **Total debt: $1,614,149**

**Liquid assets:**
- ANZ One Offset: $2,403
- Other transaction/savings accounts: ~$2,150 combined
- **Total liquid: ~$4,500.** No emergency buffer.

**Self-insurance feasibility:** liquid buffer $4.5k, total debt $1.6M, single income, 5 dependants. **Self-insurance is not viable for life / IP / TPD / trauma at the magnitudes needed.** It may be viable for pet insurance and possibly trauma if equity grows.

## Adequacy gut-check (Scott, AustralianSuper default)

Assumes Scott gross ~$145k, sole earner, 5 dependants, $1.6M debt.

| Cover | Held | Need (rough) | Gap | Verdict |
|---|---|---|---|---|
| Death | $171k | $3.5–4M (debt clear $1.62M + 22yr living $1.5M + education $0.5M) | **~$3.3–3.8M** | Severely under |
| TPD | $47k | $2–3M (debt clear + 30yr living + medical) | **~$2–3M** | Severely under |
| IP | $3,100/mo, 2-yr benefit, 60-day wait | ~$9k/mo (75% of gross), benefit to age 65 | **~$6k/mo amount gap + ~28yr duration gap** | Severely under |
| Trauma | $0 | $145–290k (1–2× gross) | **$145–290k** | Gap |

**Mina (Aware Super, pending):** likely similar default-table inadequacy. Mina's life/TPD need is driven by *replacement cost of caregiving* (5 kids + childcare + housekeeping), not income replacement — rough estimate $1–2M.

## Underwriting timing (load-bearing)

- Mina pregnant ~early stages (per memory note 2026-04-24).
- New retail IP/life/TPD/trauma applications generally face standard underwriting until ~24 weeks gestation.
- After ~24 weeks: most insurers exclude pregnancy-related claims; some impose pregnancy loadings or defer underwriting until 6 months post-birth.
- Estimated practical underwriting window for fresh retail cover: **now → late Aug / Sep 2026** (~14–18 weeks).
- **This sets the audit decision deadline.**

## Privacy plan (already ratified)

Tier B default + Tier D-Health/Family overrides + minimum-required clause. Real salaries and ages allowed (insurance maths). Mina described as "expecting, due ~Q4 2026". Kids as K1–K4 with real ages. No medical history piped to Codex/Gemini — orchestrator verifies underwriting facts locally with insurer documents.

## Current insurance inventory — confirmed 2026-05-06

**Sources:** PocketSmith bank-feed (May 2025–May 2026), consolidated `Insurance` budget event note, Mina's email quotes 2026-05-06.

| Policy line | Insurer | Confirmed premium | Annualised | Source |
|---|---|---|---|---|
| Private health | Medibank Private | (TBC) | ~$3,121–$3,396/yr | PocketSmith DD |
| Car (2010 Honda CR-V) | Budget Direct | **$154.75/mo** | $1,857/yr | Mina's email |
| Sassafras building+contents (PPOR, 31 Sassafras Dr Sunbury) | Budget Direct | **$163.80/mo** | $1,966/yr | Mina's email |
| Sydenham landlord building (18 Park View Tce — *"Park View" = Sydenham*) | Budget Direct | **$138.42/mo** | $1,661/yr | Mina's email |
| Pet | PetSure-underwritten | **$60/mo** | $720/yr | User confirmed |
| **Total general+health+pet (confirmed)** | | **~$558+/mo** | **~$9,300+/yr** | |

**Resolved from prior open questions:**
- "Park View" = 18 Park View Tce, Sydenham. Sydenham investment IS the landlord-insured property.
- Pet insurance is $60/mo, not $8/mo as the budget event note stated. Budget event needs updating.
- Car insurance is $154.75/mo not $150/mo as the budget event note stated.
- Sassafras home is $163.80/mo not $177/mo (budget overstates).

**Sums insured (sanity check for under-insurance):**
- Sassafras building: $450k (rebuild cost in Sunbury VIC may exceed this — verify in spec phase)
- Sassafras contents: **$20k** (low — likely Mina-selected for premium minimisation; revisit)
- Sydenham landlord building: $350k

## Mina's proposed alternatives — CBA Insurance (underwritten by Hollard)

| Line | CBA option | Monthly | vs Current | Annual saving |
|---|---|---|---|---|
| Car | Comprehensive | $80.56 | -$74.19 | **$890** |
| Car | Comprehensive Saver | $63.05 | -$91.70 | **$1,100** |
| Sassafras | Building+Contents Classic (15% combined discount) | $129.30 | -$34.50 | **$414** |
| Sassafras | Building+Contents Plus | $139.59 | -$24.21 | **$291** |
| Sydenham | Landlord Building | $106.16 | -$32.26 | **$387** |

**Bundle scenarios (assuming combined-policy discount applies across all three):**
- Comprehensive + Classic + Landlord: **$316/mo → save $1,691/yr**
- Comprehensive Saver + Classic + Landlord: **$298.51/mo → save $1,902/yr**

**Caveats to validate in research phase:**
- 15% combined-policy discount must apply if you take all three; verify it does and on which lines
- Comprehensive Saver = restricted driver / mileage / agreed-value variant; check if the trade-offs fit the household (need to compare driver schedule, sums insured, excesses, optional covers)
- Sassafras building sum on the CBA quote ($450k) matches Mina's request, but rebuild-cost adequacy is independent of insurer
- Hollard is the underwriter — same insurer that underwrites Hollard-distributed brands; check claims-experience reputation

## Gaps PocketSmith cannot see

These are policies that, if held, are likely paid from super balance (not visible in bank feeds). Status unknown until user confirms:

- **Life cover** — not visible
- **Income protection (IP)** — not visible
- **TPD (total & permanent disability)** — not visible
- **Trauma / critical illness** — not visible

Given the 5th child on the way and Mina's mat-leave income hole ($33–66K), these are the highest-leverage line items in the audit. If they don't exist, **that itself is the audit finding**.

## Confirmed state (after 2026-05-06 user replies)

- **Hillside:** currently **uninsured**. User agreed to look into it. Major risk item: a family home with Mina's family rent contributing — building loss = catastrophic uncovered exposure.
- **Renewal dates:** Budget Direct policies are **not locked-in contracts**. No contractual switching barrier — switching window is whenever the audit closes.
- **Health (Medibank) + Pet (PetSure):** Mina has **not** quoted alternatives for these. They are out of scope of the current quote batch.
- **Life / IP / TPD / trauma:** confirmed default super cover only; no retail cover.

  **Scott — AustralianSuper (Blue Collar work rating, age-based design, as at 2026-05-06):**
  - Death cover: $171,000
  - TPD cover: $47,000
  - IP: $3,100/month, 60-day waiting period, 2-year benefit period
  - Premium: not captured (deducted from super balance)
  - No trauma cover

  **Mina — Aware Super:** cover details pending; user expects it's similar magnitude.

## Open intake questions remaining

1. ~~Park View~~ — resolved.
2. ~~Hillside~~ — resolved (uninsured; addressed in research phase).
3. ~~Renewal dates / contract lock~~ — resolved (not locked-in).
4. ~~Health/pet alternative quotes~~ — confirmed not done; we'll keep these in scope or descope based on user direction.
5. **Life / IP / TPD / trauma — pull the actual cover details from AustralianSuper for Scott + Mina (cover types, amounts, waiting periods, premiums).** ← next ask
6. Pending claims — assumed none unless user flags.

## Definitions (for user reference)

- **Death (life) cover:** lump sum to nominated beneficiaries if the insured dies. Pays off mortgage + supports dependants until self-supporting.
- **TPD (Total & Permanent Disability):** lump sum if the insured can never work again due to illness/injury.
- **Income Protection (IP):** monthly benefit (typically 75% of pre-disability income) if the insured is sick/injured and unable to work, paid after a waiting period (e.g. 30/60/90 days) for a benefit period (e.g. 2 years / to age 65).
- **Trauma / critical illness:** lump sum on diagnosis of a defined serious condition (cancer, heart attack, stroke, etc.). Distinct from TPD because you don't have to be unable to work.

These are *separate* from "shopping around" — the audit asks: do you have each, are the amounts right, is the structure right (super vs retail), and *only then* whether to shop the premium.
