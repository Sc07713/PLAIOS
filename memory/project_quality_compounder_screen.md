---
name: project_quality_compounder_screen
description: "Next-session research study — screen for EARLY-stage quality compounders (fat margins, high ROIC, growth, owner-operator mgmt); point-in-time backtest is the make-or-break"
metadata: 
  node_type: memory
  type: project
  originSessionId: c496d953-8194-4634-a1d8-f636f5f1f416
---

Scott's investing thesis (stated 2026-05-22): **"a team that knows how to win will know how to keep winning"** — management quality + fat margins persist and predict. Wants to find quality compounders **EARLY** (before the long track record exists) to capture the most capital growth as they scale. This is the quality factor (gross-margin/Novy-Marx, ROIC persistence, founder-led outperformance) — empirically grounded.

**Planned analysis (deferred to a future session, his request):** systematic screen + backtest for companies with best Sharpe / CAGR / growth / quality management / fat margins, tilted to small-mid caps with runway. A satellite research STUDY (hypothesis-factory shape), sits BESIDE the validated SPY_top_5 core, does not replace it.

**Early-compounder fingerprint params to screen on (can't use long price-Sharpe — names won't have it yet):**
- Fat AND expanding gross margin (pricing power)
- High + rising ROIC/ROE (capital-allocation = mgmt signal)
- Durable 20%+ revenue growth WITH operating leverage (EPS faster than rev)
- Owner-operator / founder mgmt + real insider ownership
- Already profitable / not diluting (keeps the no-cash-burn discipline)
- Small/mid-cap + large TAM (room to scale)
- Basket game (own 10-15, let winners run) — NOT 2-3 name concentration

**Three make-or-break constraints (flagged to Scott):**
1. DATA GAP: need fundamentals across a BROAD small/mid universe; DB `fundamental_facts` only covers ~27 names. Plumbing exists (SEC EDGAR/XBRL sourced) — needs widening the ingestion first. That's the build prerequisite.
2. POINT-IN-TIME BACKTEST is the actual edge: test "what the screen would have picked in 2015/17/19 and how those cohorts did over next 3-5yr" with NO look-ahead. Otherwise it's hindsight storytelling.
3. Valuation guardrail (quality-at-reasonable-price) — quality compounders often already expensive; multiple compression can eat the business win.

**For contrast — the survivorship-biased screen already run 2026-05-22** (proven 14yr winners, NOT early): top by Sharpe vs SPY (0.93) over 2012-2026 were AVGO/COST/TT/LLY/CTAS/MPWR/PGR/CDNS/ORLY. Useful as "what a mature winner looks like"; the new study is the inverse problem (catch them young). See [[project_ai_energy_power_basket]] for the prior session's deployed decision and [[user_investment_philosophy]] (this REFINES it — quality/management persistence lens added).

**Kickoff spec WRITTEN 2026-05-22:** `D:\Plaios-tools\trading-tools\docs\specs\2026-05-22-early-quality-compounder-screen.md` (uncommitted — part of pending repo lock-in). KEY FINDING from writing it: most machinery ALREADY EXISTS — V3.3a PIT fundamentals engine (`derived_metrics` already computes margins/growth/ROE/FCF/gross_profitability), V3.3b-quality `fundamentals` aux + `quality_gp`, V3.3d `tt scan`/`universe_sp500` PIT membership/rank_hold, and the V3.4 winners-falsification forward-return template. New work = (Phase 0) WIDEN fundamental data from ~24 names to sp500_union 959 (the parked "V3.2b decorrelated universe" is this precondition) + resolve delisting/survivorship gap; (Phase 1) freeze a quality-growth composite cut incl. a size band for "early"; (Phase 2) PIT winners-falsification backtest as LONG holds (not monthly — V3.3d proved the +951% winners-cut lift is a long-hold phenomenon, which ALIGNS with Scott's buy-and-hold/CGT mandate); (Phase 3) tt scan watchlist + qualitative mgmt/runway/valuation overlay. quality_gp already found NO EDGE on TOP_25 (survivorship) — the broad universe is the honest test.
