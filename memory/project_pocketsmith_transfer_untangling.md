---
name: PocketSmith transfers — deferred cleanup, starting fresh May 2026
description: April 2026 Transfers category has $4,770/mo net leakage from misclassifications; user deferred untangling historical, will clean up from May onward
type: project
originSessionId: c021306b-3185-4efd-b11a-5da8d0f159ff
---
**Decision 2026-04-24:** User declined to untangle historical (April) transfers. Will reset from May and clean up new transactions as they come in.

**Context:** April Transfers category shows 22 transactions, net -$4,770 (should net to ~zero if all true inter-account moves). Leakage is mostly misclassification, not real spend.

**Known misclassifications in Transfers category (historical):**
- Hung Sam Ha +$1,200/mo → actually **Hillside rental income** (Mina's family's partial rent payment)
- Edmond Chen -$350 → **external payment, unclear purpose** (flag for user to identify)
- Mina "school fees" transfers (-$367 × 2 in April) → actually **Education** (Mina pays school fees, Scott transfers to her)
- Mina "childcare/bills" transfers (-$1,206, -$1,274 in April) → mix of **Child Care + bills** (Scott → Mina → bill pays)

**Household cash flow architecture (as understood 2026-04-24):**
- Scott earns to CommBank Complete Access (xx7233)
- Money is often routed Scott's CA → Mina's CA (xx3194) → Mina's Go Account → actual bill payment
- Mortgage servicing: CA → ANZ One Offset → mortgage debits (multiple hops per real payment)
- Bills like childcare, school fees are often paid from Mina's side with Scott pre-funding via transfer
- This multi-hop flow makes PocketSmith's transfer pairing fail cross-bank

**Next session actions (when user returns post-May data):**
1. Pull May 2026 Transfer transactions (date ≥ 2026-05-01)
2. Identify recurring misclassification patterns
3. Create category rules to auto-fix future ones: Hung Sam Ha → Rentals, school fees transfers → Education, etc.
4. If user wants, also re-categorise historical April transactions (optional)

**How to apply:** When user mentions Transfers not balancing or unexpected budget numbers, remember this is a known pattern — the Scott→Mina→bill pipeline appears as Transfer outflow with no matching inflow in PocketSmith's view. Either accept the noise or set up category rules.
