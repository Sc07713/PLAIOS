---
name: PocketSmith forecast cleanup — RESOLVED 2026-04-22
description: Net worth forecast was dropping $10,814/mo due to phantom events from initial OAuth feed template; cleaned up to show $313/mo gain
type: project
originSessionId: c021306b-3185-4efd-b11a-5da8d0f159ff
---
**Status: RESOLVED 2026-04-22.**

**Root cause (confirmed, not the hypothesis):** The mortgage duplication wasn't in the Loan Repayment events — it was a single phantom lump-sum "Mortgage" event ($9,414/mo) firing on the ANZ One Offset scenario, plus PocketSmith-generated default template events on Mina's (separately-connected) Complete Access account scenario. Both came through during the initial 2026-04-17 OAuth feed setup and were never cleaned up.

**What was deleted:**
1. Phantom $9,414/mo "Mortgage" event (series 423694783) on ANZ One Offset scenario 5011764
2. Phantom $600/mo "Insurances" event (series 424368415) on Go Account scenario 5011809
3. All 14 template events on Mina's Complete Access scenario 5009809 (Transfers $1,140, Insurances $600, Home Improvement $270, Household/Clothing/Healthcare etc. — net $2,125/mo drag)

**What was moved:**
- Park View rent event: deleted from Westpac Choice scenario 5019943 (event 423647163), recreated on Go Account scenario 5011809 (new event 424927243). Rent actually lands in Go Account today; will migrate to Westpac Choice or ANZ One Offset at rent→offset restructure.

**Forecast impact (before → after):**
- Monthly change: -$10,814/mo → +$313/mo
- 12-month change: -$129,771 → +$3,758
- End balance (Mar 2027): $461,988 → $595,429

**Key structural insight for future sessions:**
- Mina has a second CommBank "Complete Access" account (id 4852629, BSB 063-984, acct 10003194, balance $0.90) — she will close it at some point. Its feed was included in the original OAuth. Don't delete the account; just keep its scenario clean.
- Scott's Complete Access is id 4852614 (BSB 063-141, acct 10247233) — the one that pays everything.
- Go Account (id 4854564, scenario 5011809) currently receives Mina's salary AND Park View rent.
- Complete Access in isolation bleeds ~$3,185/mo because it pays all 3 mortgages + household bills but only receives Scott's salary + Hillside rent. Household aggregate is fine; single-account calendar views will still look alarming until rent→offset restructure happens.

**Still open from this session:**
- Korea savings plan: ringfence via Virgin Boost Saver rename ("Korea Trip 2026"), $1,500/mo auto-sweep May-Aug + tax refund redirect (~$12,500 accumulated vs $11,799 need). Recommendation made, not executed.
- Rent→offset restructure: drafted, not live. Biggest remaining structural win.

**How to apply:**
- Do not re-verify Korea event existence — already confirmed live (events 423927119/423927127/423927139/423927143/423927147, $11,799 total, Complete Access scenario 5009794, Travel category 31172244).
- When Mina's second Complete Access is closed, delete the account from PocketSmith. Scenario 5009809 should be empty of events already.
- Mapping doc at `domains/finance/reference/pocketsmith-budget-mapping.md` updated with the Park View rent move (2026-04-22 entry).
