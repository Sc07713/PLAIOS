---
name: Hillside loan topped up to fund Sassafras purchase
description: Hillside (investment) loan was increased to fund the Sassafras PPOR acquisition, so rental income from Hillside does not cover its full mortgage repayment.
type: project
originSessionId: rebuild-2026-04-19
---
**What happened:** The Hillside (Celendine Drive, investment) loan was topped up / increased in order to fund the acquisition of 31 Sassafras Drive (PPOR). This means the Hillside loan balance is higher than the standalone purchase price of Hillside would imply.

**Consequence:** Rental income from Hillside tenants ($2,200/mo combined) does NOT cover the Hillside mortgage repayment ($2,928/mo). There is a structural cash gap of ~$728/mo that must come from operating cash.

**Confirmed by:** Scott McKennie, 2026-04-19 during PocketSmith budget rebuild session.

**The spreadsheet error this caused:** The household spreadsheet had a line labelled "$800 extra" for Hillside. This was misread as extra principal repayment. It was actually the approximate cash top-up needed each month to cover the gap between rent and full repayment (~$728 rounded). There is NO separate "extra principal" event in the live PocketSmith model — the $610/mo principal event already reflects the full repayment minus interest.

**How to apply:**
- Do not assume Hillside rental income covers its mortgage — it does not.
- Hillside actual repayment: $2,928/mo (interest $2,318 + principal $610)
- Hillside rent: $2,200/mo
- Monthly operating cash contribution required: ~$728/mo
- Annual operating contribution: ~$8,736/yr
