---
name: tastytrade-options-account-separate-sleeve-integration-deferred-to-v4
description: "Scott runs an options account on tastytrade alongside the IBKR cash-equity book; trading-tools models the equity sleeve only; options-sleeve modeling + tastytrade integration is V4, a read-only options-opportunity scanner is a parked post-V3.2 item"
metadata: 
  node_type: memory
  type: project
  originSessionId: aa1f7ac6-451d-4ff0-891d-92ea9c49d323
---

Scott has an **options account on tastytrade**, run alongside whatever equity book trading-tools manages (the equity side is IBKR — see [[project_trading_tools_v1_built]]). Decided 2026-05-12 during the V3.2 brainstorm: **trading-tools models the IBKR cash-equity sleeve only**; the tastytrade options sleeve is deliberately out of scope for now.

**Why:** keeps V3.2 (the equity portfolio overlay) tractable — an options sleeve needs options chains, an implied-vol surface, and a risk/reward model, none of which is ingested. The equity book is one of *two* sleeves, not the whole picture.

**How to apply:** when designing trading-tools features, don't pretend the options sleeve doesn't exist, but don't try to model it before V4. The V3.2 portfolio overlay deliberately emits a per-rebalance ranked-thesis-with-conviction-and-volatility object precisely so a future scanner can consume it. Parking lot:
- **Options opportunity scanner** (post-V3.2, read-only; numbering loose) — consumes the overlay's thesis ranking + ingested options chains + an IV model → proposes defined-risk structures (debit/credit spreads etc.) with risk/reward; Scott trades them manually on tastytrade. No capital coupling, no live orders, no Greeks-management engine. Needs an options-data ingestion path first: **IB serves *current* option chains via `reqSecDefOptParams` + market-data ticks** (fine for a live scanner); IB's *historical* options depth is shallow, so a proper options *backtest* (V4) would want a vendor (ORATS / CBOE DataShop / Polygon).
- **V4 options layer** — put-spreads replacing synthetic shorts in the backtester (→ honest long_short); options-sleeve capital modeling; live tastytrade account integration.

See [[project_trading_v3_scope_pending]] and [[user_investment_philosophy]].
