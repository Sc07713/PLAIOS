---
name: au-cgt-constraint-asx-buy-and-hold-only
description: "AU CGT rules make active trading of ASX/AU-held positions punitive — short-term gains taxed at full marginal rate, only >12mo holds get the 50% CGT discount; this means trading-tools active strategies are US-only by design, ASX work (if any) is a separate long-term-buy-and-hold watchlist thread"
metadata: 
  node_type: memory
  type: project
  originSessionId: 631f04e5-e90f-4124-a992-f1153412b23e
---

Scott confirmed 2026-05-14 (during winners-characterization study scoping):

**AU CGT rules** make active strategies on ASX-listed names unviable for him. Capital gains on positions held <12 months are taxed at full marginal rate; only positions held >12 months qualify for the 50% CGT discount. **Government tightening this further** — described as "getting greedy" — pushing day-trading-as-investment toward day-trading-as-business-income classification by ATO, which would lose the CGT-discount entirely and impose ordinary income tax on all turnover.

**Concrete implications for trading-tools scope:**

1. **trading-tools is US-equities-only by design** going forward. NYSE + NASDAQ are the active-strategy universes. The IBKR account, the V3.1 / V3.2 / V3.3 strategy work, the universe expansion to S&P 1500 / Russell 1000 — all US.

2. **ASX is parked** — not deferred, parked. Don't plan ASX fundamentals ingestion, don't plan ASX bar ingestion, don't plan an ASX-EW-BH benchmark. The "find money extractors across multiple asset classes" framing from 2026-05-14 earlier in the same session is revised: cross-asset = US sectors / asset classes, not international.

3. **If a separate ASX thread emerges later**, its shape is different: a **long-term-hold watchlist / advisory layer**, not a backtester. The deliverable would be "5-10 ASX names that look like multi-year compounders, hold for ≥12mo to capture the CGT discount." That's a Scott-as-investor decision support tool, not trading-tools active strategy work. Probably a different sub-project entirely (could live in `domains/finance/` rather than `domains/trading/`).

4. **Tax-jurisdiction note for US-equity trades from AU residence:** Scott as an AU tax resident still pays AU CGT on US-equity gains in his IBKR account. The 12-month rule applies the same way. So even on US names, frequent turnover hurts after-tax returns vs. holding. This doesn't invalidate trading-tools' active-strategy thesis — the framework is for finding strategies that *beat passive after-tax*, and high turnover is one of the costs the cost-aware (5 bps round-trip) accounting captures structurally, but the AU tax wedge is additional and worth noting in any "is this strategy actually worth running" calculus.

**How to apply:** When planning trading-tools work, scope universes US-only. Decline to expand to international markets even when "decorrelation" or "cross-asset edge testing" arguments come up — the after-tax economics don't survive the AU CGT wedge for short-hold strategies.

Supersedes the earlier-same-session [[project_trading_universe_scope_multiasset]] — that memo's ASX-as-primary expansion plan is wrong given the tax reality; ASX is parked.

Related: [[user_investment_philosophy]] (the quality-compounder thesis still applies — ASX-fit would be a separate long-hold watchlist, not active), [[project_property_portfolio]] (Scott's other AU-domiciled wealth is in property, which has its own CGT regime).
