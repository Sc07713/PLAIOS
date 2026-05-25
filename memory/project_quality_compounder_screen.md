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

**Phase 0 done:** SEC fundamentals widened to 634/959 S&P-500-union symbols (15.6M fact rows); 549 have both fundamentals + price. Delisting bias = accept-and-flag for v1 (decision log).

**Phases 1–2 EXECUTED 2026-05-22 (Claude session, after a Codex run Scott wasn't happy with — Codex did the data plumbing but produced ZERO symbols).** Key events:
- **Engine bug found + FIXED (trading-tools commit `8f48b77`).** `resolve_metric`/`_flows_by_period_end` returned the FIRST XBRL candidate tag with any match, never unioning — so a tag transition froze a metric at the old tag's last period. NVDA TTM revenue stuck at 2020 ($27B) vs gross_profit 2026 ($153B) → "570% gross margin"; its "+40.8% growth" was a silent stale 2019→2020 comparison. SILENT corruption across any name that switched revenue tags. Fix = per-period-end priority union. NVDA now 71.1% margin / +89.8% rev. 338 tests green. **This was the real deliverable — the prior screen was untrustworthy.** Residual separate gap: 7 REIT/conglomerate names (SBAC/ESS/DD/BIIB...) still >100% margin (total-revenue tag unmapped) — caught by a data-suspect guard, off-thesis.
- **Frozen screen = single source of truth:** `trading_tools/fundamentals/quality_screen.py` (v2026-05-22.1), DUAL-LANE. Lane A = established (fat/rising margin, 20%+ growth+op-leverage, rising ROE, FCF+). **Lane B = emerging/blitzscale (Scott's Atlassian insight 2026-05-22): drops profitability gates, demands fat 60%+ gross margin not eroding + 25%+ growth + improving op-margin trend + Rule-of-40 — catches the VC-funded land-grab compounder before it tightens to profit.** Commit `675784d` (study + phase1/phase2 scripts + 7 tests).
- **Phase 2 PIT VERDICT = inconclusive-but-encouraging.** Lane A beat SPY-BH AND univ-EW in ALL 4 cohorts (2014/16/18/20), both 3y+5y (2016: +430% vs +132% at 5y; 2018: 100% win). BUT underpowered (n=1–6, <30 total obs = fails spec kill-criterion) and NVDA-dependent (+1060%/+1381% carries the means). **Lane B essentially UNTESTABLE on S&P-500 universe — 0–3 names/cohort, lost where testable (2020). The blitzscale names (TEAM/SNOW/NET/DDOG/CRWD/SHOP) literally aren't in our DB** (checked: only NOW+WDAY have both funda+bars). Not falsified, not validated.
- **As-of-now large-cap watchlist (fixed engine):** durable Lane-A = DECK, RL, MNST (owner-op Sacks/Schlosberg), PTC, PAYC (owner-op Richison), ADBE, ISRG, AVGO, IDXX, RMD, MPWR; cyclical-suspect flagged (MU/WDC/TER); market cap missing ~95% (shares_outstanding coverage gap → no size tilt yet).

**THE UNLOCK (next session) = down-cap / broader universe (path A).** ONLY way to (a) test Lane B / blitzscale thesis at all and (b) grow cohorts to statistical power. Needs mid/small-cap fundamentals + delisted prices + historical ticker→CIK mapping (real data-acquisition sub-project). Secondary: risk-adjust (Sharpe/DD not just total return), fix shares_outstanding coverage for the size band, re-run with NVDA excluded to size its contribution. Writeup: `docs/studies/2026-05-22-early-quality-compounder-screen.md`.
