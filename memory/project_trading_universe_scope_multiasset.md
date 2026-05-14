---
name: trading-universe-multi-asset-scope-asx-us-primary
description: "SUPERSEDED 2026-05-14: ASX dropped from trading-tools scope (AU CGT wedge); trading-tools is US-only by design. See project_au_cgt_constraint_asx_buy_and_hold_only.md for the binding constraint."
metadata: 
  node_type: memory
  type: project
  originSessionId: 631f04e5-e90f-4124-a992-f1153412b23e
---

**SUPERSEDED 2026-05-14 — same-session revision.** ASX-as-primary-expansion was scoped to be wrong given AU CGT constraints; trading-tools is US-only by design. See [[project_au_cgt_constraint_asx_buy_and_hold_only]] for why and what it means operationally. The text below is preserved as the original scoping articulation but no longer reflects current intent.

---

Universe expansion plan articulated 2026-05-14 (after V3.3b-quality ship, while scoping the winners-characterization study):

**Primary universes:**
- **US equities** — the existing TOP_25 (24 mega-cap operating names + SPY). SEC EDGAR XBRL fundamentals already ingested (`fundamental_facts` ~620K rows). Earnings data via Finnhub + EDGAR 8-K. All study/build work to date has been here.
- **ASX equities** — next addition. IB serves ASX bars (no ingestion code change required, just symbol additions to `KNOWN_INSTRUMENTS` in `cli.py`). But **ASX has no SEC-EDGAR-equivalent free XBRL feed** — fundamentals require a different ingestion path (ASX annual reports are PDF; Morningstar AU / Refinitiv / FMP are paid options; scraping company-website annual reports is the free-but-fragile path). This is a build sub-piece, not just a config tweak.

**Why:** Scott's investment edge is more likely to exist where the *coverage* is concentrated (he can analyze deeply) than spread thin. ASX is a natural extension — same English-language regulator regime, same accounting conventions roughly, very different sector mix (financials + miners + a few specialty like CSL/ResMed vs US mega-cap tech) ⇒ a real decorrelation benefit vs TOP_25. Singapore/HK/CN/EU are *candidates* but the bar is "where do we get the most bang for buck, and where do our edges work" — not a guaranteed addition.

**How to apply:**
- For any **study** scoped to TOP_25 today: design the methodology to be universe-agnostic so an ASX replay is a parameter swap, not a rewrite.
- For any **build** that needs cross-asset fundamentals: ASX ingestion is its own sub-piece (likely V3.4 or similar — separate spec/plan/ship). Don't fold it into a current sub-piece that's scoped to US.
- For backtest reporting: when the ASX universe lands, the four-way benchmark template needs an ASX-EW-BH analogue alongside SPY-BH for ASX-named runs.
- SG/CN/EU: parking-lot. Re-open when a finding from ASX justifies "this edge looks like it generalizes — let's check elsewhere."

Related: [[user_investment_philosophy]] (decorrelation rule; quality-compounder thesis), [[project_trading_v3_scope_pending]] (the V3 roadmap — ASX universe ingestion would slot as ~V3.4 or as a sub-piece of V3.3d screener depending on scope), [[feedback_trading_tools_is_a_hypothesis_factory]].
