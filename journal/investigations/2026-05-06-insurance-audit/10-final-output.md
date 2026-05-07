# 10 — Final output: insurance audit (general lines)

**Date:** 2026-05-06
**Status:** closed at phase 07. No mediation required.
**Privacy tier:** B.

## Executive summary

Mina pulled CBA quotes that promised ~$1,691/yr saving on the bundle. **Don't take it.** CBA distributes a Hollard product, and Hollard is the subject of active ASIC litigation for severe claims-handling failures. The premium saving is real; the catastrophic tail risk it buys is too large for a household with $4.5k liquid buffer and a sole income.

The audit concluded with revised guidance:
- **Drop CBA / Hollard from all four lines.**
- Quote against Budget Direct (re-quoted fresh), AAMI, RACV, and QBE for the property bundle. Quote car standalone against Budget Direct, AAMI, Bingle.
- **Lift sums insured.** Sassafras contents $20k → $120k floor. Building rebuilds need insurer-calculator verification — likely $600k+ for Sassafras and $500k+ for Sydenham.
- **Insure Hillside.** Property is currently uninsured against $490k of mortgage debt. Use building + public liability cover (not landlord), with related-party tenancy disclosed.
- **Bundle the buildings, stand-alone the car.**

The audit also identified a separate, larger issue (severe under-insurance in life / IP / TPD / trauma cover) that the user explicitly parked. The pregnancy-driven underwriting clock on those parked items has been recorded in memory; do not let the parking erase the timing.

## What was decided

### 1. CBA / Hollard — dropped from comparison set

Reason: ASIC 25-057MR (Federal Court hearing 2026-05-26) alleges Hollard delayed a Victorian home claim 18 months, refused make-safe works, allowed the home to rot to demolition, then rejected the claim. AFCA has separately criticised Hollard for "unreasonable" storm-claim delays. Trustpilot 1.3/5. The premium saving from switching to Hollard does not compensate for the claims-handling tail risk on a PPOR for a household that cannot self-fund 18 months of alternative accommodation while a claim drags.

### 2. Comparator shortlist (final)

**Property bundle (PPOR + 2 landlord):**
- Budget Direct (re-quoted as new business — current insurer; Canstar 2026 Insurer of the Year)
- AAMI (Finder 2026 Best Value Home; Suncorp Group)
- RACV (VIC local; Outstanding Customer Satisfaction 3 years; pattern-match for high-friction family claims)
- QBE (Canstar 2026 home & contents winner; landlord product depth; quality anchor)

**Car (standalone):**
- Budget Direct (Finder 2026 Best Value Car)
- AAMI
- Bingle (Auto & General's price-aggressive sub-brand)

### 3. Hillside — pivot to building + public liability cover

Standard Australian landlord policies will not pay rent default or tenant damage for related-party (family) tenants regardless of what's on the policy schedule. So buying "landlord cover" at Hillside is paying for protections that won't apply.

**Replace with:** building + public liability cover (Investment / Owner-not-occupier), with related-party tenancy disclosed at quote stage. RACV and QBE are reported to write family-let cleanly with disclosure.

### 4. Sums insured — revised targets

| Line | Current | New | Method |
|---|---|---|---|
| Sassafras building | $450k | **$600k+ (verify with insurer rebuild calculator)** | 200sqm 4-bed at 2026 outer Melbourne build cost $3,000-$3,500/sqm + extras |
| Sassafras contents | $20k | **$120k floor** | 6-person household replacement; ICA calculator |
| Sydenham building | $350k | **$500k+ (verify)** | 2026 rebuild guidance |
| Hillside building | $0 | **calculator-verified** | New cover required |

### 5. Bundle strategy

- Bundle PPOR + 2 landlord with one insurer (10–15% combined-policy discount typical).
- Quote car standalone — combined-policy discount rarely overcomes Budget Direct/Bingle's car base-rate advantage.

### 6. Hillside tenancy — required prep before any quote

Before binding any cover at Hillside or relying on any tenant-related cover at any property:
- Written lease with Mina's mother + siblings.
- Rent at market rate (or near), recorded.
- Bond held in line with VIC RTA practice.
- Disclose related-party tenancy in writing on every quote.
- Get insurer's written acceptance of the related-party arrangement before binding cover.

## What was NOT decided (and why)

**Real apples-to-apples premium numbers** for AAMI / RACV / QBE — these need Mina to run the quotes. The audit's deliverable stops at the quote-comparison spec at `05-research-pack.md`. The decision on which insurer wins is data-dependent.

**Whether the household actually has the budget** for the additional premium that proper sums + Hillside cover will require. Audit assumes yes (PocketSmith shows ~$20k/yr surplus before discretionary, currently absorbed by BNPL paydown + eating-out cleanup). Confirm at switch time.

## Out-of-scope finding (parked, but flagged)

**Severe under-insurance in the life / IP / TPD / trauma cluster.** User explicitly parked this for later session. Recording for re-open:

- Default AustralianSuper cover only (Scott): Death $171k, TPD $47k, IP $3,100/mo with **2-year benefit period**.
- Need (rough): Death $3.5–4M, TPD $2–3M, IP $9k/mo to age 65.
- Sole earner with $1.59M mortgage debt + 4 dependants + 1 expected. $4.5k liquid buffer.
- Spouse pregnant (estimated due Q4 2026). Retail underwriting tightens around 24 weeks gestation; post-natal exclusions complicate rebuild for 6+ months.
- **Practical decision deadline for retail life/IP underwriting: late August / September 2026 (~14–18 weeks).**

This is the largest structural risk in the household; the general-insurance work is necessary but not sufficient. **Memory entry created for re-opening.**

## How the multi-agent procedure ran

- **Phase 00** — topic intake. PocketSmith + Mina's quote emails + AustralianSuper data. Closed.
- **Phase 01-02** — skipped (question was clear from intake).
- **Phase 03** — spec drafted (`03-spec.md`).
- **Phase 04** — Claude channel research via WebSearch (`04-research-claude.md`); Codex + Gemini reviewed in deliberation phase (`06-deliberation-codex.md`, `06-deliberation-gemini.md`).
- **Phase 05** — research pack with quote-comparison sheet for Mina (`05-research-pack.md`).
- **Phase 06** — three-channel deliberation. All three reviewers converged.
- **Phase 07** — binding disposition. Closed here.

No mediation phase required (08, 09 not reached).

## Sources

- [ASIC 25-057MR Hollard claims handling](https://www.asic.gov.au/about-asic/news-centre/find-a-media-release/2025-releases/25-057mr-asic-sues-hollard-insurance-alleging-serious-claim-handling-failures/)
- [ASIC 26-036MR Auto & General discount misrepresentation](https://www.asic.gov.au/about-asic/news-centre/find-a-media-release/2026-releases/26-036mr-asic-sues-auto-general-alleging-policy-discount-misrepresentations-made-to-millions-of-consumers-in-budget-direct-insurance-ads/)
- [Canstar Insurer of the Year 2026](https://www.canstar.com.au/star-ratings-awards/insurer-of-the-year-award/)
- [Choice Best Home & Contents 2026](https://www.choice.com.au/money/insurance/home-and-contents/review-and-compare/home-and-contents-insurance)
- [Finder Best Home Insurance 2026 (AAMI Best Value)](https://www.finder.com.au/home-insurance/best-home-insurance)
- [Allianz Rent Default cover guide](https://www.allianz.com.au/home-insurance/rent-default.html)
- [AAMI landlord FAQ](https://www.aami.com.au/faq/will-i-be-covered-by-my-landlord-insurance-if-my-tenant-stops-paying-the-rent-but-does-not-leave-my-property.html)
- [Insurance Council of Australia consumer calculators](https://insurancecouncil.com.au/consumers/calculators/)

## Files in this investigation

- `00-topic.md` — intake summary
- `03-spec.md` — comparison spec
- `04-research-claude.md` — driver's research
- `05-research-pack.md` — quote-comparison sheet for Mina
- `06-deliberation-claude.md`, `06-deliberation-codex.md`, `06-deliberation-gemini.md` — per-channel reviews
- `06-deliberation.md` — consolidated
- `07-disposition.md` — binding outcome
- `bundles/reviewer-bundle.md` — Tier B sanitised bundle sent to Codex + Gemini
- `10-final-output.md` (this file)
