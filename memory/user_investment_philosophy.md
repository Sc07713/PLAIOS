---
name: investment-philosophy-beat-gold-decorrelated-bets-crash-opportunity
description: "Scott's investing principles — beat gold (hurdle + residual sleeve), decorrelated independent theses (with money-extractor exception), crash = opportunity, AND three flow/management lenses added 2026-05-15: (a) prices have an emotion/attention/resonance component not just DCF, (b) vol-band ∈ [0.25, 0.50] reads as management-extraction consistency = quality proxy, (c) mega-cap passive-flow concentration ('biggest gets biggest') is a structural tailwind that makes characteristic signals translate to portfolios on SP500 but NOT on R3000. **2026-05-17 update: dual-sleeve (SPY_top_5 + rs_vol watchlist) recommendation FALSIFIED — Study 1 + Study 2 both show no minhold/blend cell beats SPY_top_5 alone; recommendation is now 100% SPY_top_5 monthly-rebal.**"
metadata: 
  node_type: memory
  type: user
  originSessionId: aa1f7ac6-451d-4ff0-891d-92ea9c49d323
---

Scott's stated investing principles. Three layers: (A) the original 2026-05-12 V3.2 brainstorm principles; (B) the 2026-05-14 money-extractor refinement; (C) the 2026-05-15 flow/management/concentration lenses added during the post-V3.3d watchlist review.

## A. Core principles (2026-05-12)

- **Every investment should beat just holding gold.** Gold-BH is a hurdle rate. In the V3.2 portfolio overlay this is baked in two ways: `gold_bh` is a mandatory benchmark, *and* **gold (GLD) is the residual sleeve** — capital not deployed into a live thesis sits in gold ("when in doubt, hold gold"), so the portfolio's literal floor is gold-BH. Zero theses active → 100% gold; one lone high-confidence thesis → 60% it / 40% gold (60% is a hard per-position cap).
- **Holdings should be genuinely independent bets** — different industries, different theses, no shared macro or micro driver. The point of a basket is *real* diversification, not 25 names that secretly co-move. (The current trading-tools `TOP_25` universe is ~20 mega-cap tech/comms names — the opposite of this — so a diversification overlay on it understates the benefit; rebuilding a decorrelated cross-sector universe is parked as V3.2b. The V3.2 basket mode trims an over-full book by greedily dropping the most-correlated name, as a partial nod to this.)
- **A whole-of-market crash is the one exception — and the opportunity.** When everything correlates to 1, that's the signal to hunt rebound positions: the most-oversold high-quality / sought-after names mean-revert hardest once conditions normalise. This is the seed of the parked V4 "crash-rebound regime overlay" (detect a broad drawdown → rank by oversold-ness × quality → hold for the bounce).
- Base case (from earlier sessions, still holds): "buy and hold quality stocks with good management." Strategies layer small alpha on top of buy-and-hold — not a BH-substitute. Hence every backtest reports vs SPY-BH AND vs asset-BH (and now, for portfolios, vs gold-BH and vs equal-weight-universe-BH too) — see [[feedback_trading_benchmark_spy_bh]].

## B. Money-extractor refinement (2026-05-14)

- **Exception to the decorrelation rule:** For a **money-extractor / quality-compounder** thesis specifically — where the dominant signal is "each individual position is an exceptional business that durably extracts value from the market" — the decorrelation rule is *relaxed*. A basket of 5-7 money extractors that all happen to share sector (e.g., mega-cap tech compounders) is a coherent thesis if each is selected on intrinsic quality, even though they correlate. Decorrelation is portfolio-construction; money-extractor is security-selection — different layers, different rules.

## C. Flow / management / concentration lenses (2026-05-15)

Articulated when reading the 2026-05-15 watchlist results in light of the R3000 falsification. These reframe how to interpret characteristic-level signals and which universes to trust them on.

- **Stock prices have a meaningful emotion/attention/resonance component, not just DCF.** "A lot of stock investment is about emotion and human resonance." This means a characteristic-level signal (e.g. forward-return lift in the V3.4 cohorts) is only half the picture — the *other* half is whether there's a marginal buyer pool whose attention/emotion the signal can attract. **How to apply:** When evaluating any characteristic-level study, ask separately: "is the signal real?" AND "is there a marginal-buyer pool that will price-discover it?" The two can fail independently.

- **Vol band ∈ [0.25, 0.50] reads as management-extraction consistency, NOT as moderate risk.** Re-interpretation of the V3.4 vol filter: this is the band where management's quarterly extraction from the market is **consistent enough to be a thesis but volatile enough to have growth in it**. vol < 0.25 → either mature utility (no extraction growth) or hidden tail risk (looked stable until it wasn't). vol > 0.50 → erratic extraction = coinflip thesis (meme names, broken biotech, post-IPO chaos). The middle band ≈ "professional company, growth-stage, predictable enough to compound." Maps directly to Asness/Frazzini's "Quality Minus Junk." **How to apply:** Treat the vol-band filter as a *quality* signal in analysis writeups, not a risk filter. Frame future fundamental/quality strategies around this — vol-band membership ≈ "management is reliably extracting."

- **"Biggest gets biggest" — passive-flow concentration is a structural mega-cap tailwind.** "Owning the biggest leads to the biggest growth." Every dollar into VOO/VTI/SPY/index-of-the-week flows market-cap-weighted into the top 5-10 names (AAPL/MSFT/NVDA/GOOGL/AMZN/META/AVGO). For ~15 years, passive has been the dominant marginal flow, so mega-caps get a non-fundamental bid purely from index-inclusion mechanics. This is **why the V3.4 characteristic signal translates to a portfolio on SP500 but failed to translate on R3000**: SP500 has the passive bid, R3000's bottom 2500 don't. **How to apply:**
  1. The R3000 falsification is best read as a **scope clarification** ("the screener works where passive flow lives"), not as the signal being fake.
  2. When ranking watchlist names, separate them into **Tier 1 (mega-cap passive-flow recipients)** vs **Tier 2 (characteristic-level passers without the flow tailwind)** — Tier 1 is higher-conviction because two compounding tailwinds (signal + flow) stack.
  3. Universe choice for portfolio backtests should be SP500 / Russell 1000, not Russell 3000+ — and that's not survivorship-bias to confront, it's matching the universe to where the price-discovery mechanism actually functions.
  4. Future studies should consider an explicit *passive-flow-weighted* universe filter (e.g. names with > $X cap or > Y% index weight) as a regime gate.

### Validation of the flow thesis — SPY_top_K study (2026-05-15)

Tested directly: hold equal-weight top-K SPY mega-caps by real market cap, rebalance monthly, vs SPY-BH. Real market cap = unadjusted close × cumulative split factor × SEC EDGAR PIT shares-outstanding. Two windows: 2011-08 → 2026-05 (tech-mega-cap era only) and 2009-08 → 2026-05 (includes XOM-#1 era 2009-2011).

**Tech-era only (2011-08 → 2026-05, 14.67yr; candidates AAPL/MSFT/NVDA/AMZN/GOOG/GOOGL/AVGO/TSLA/META):**

| K | CAGR | Sharpe | MaxDD | Lift vs SPY | Robustness |
|---:|---:|---:|---:|---:|---|
| **1** | **20.91%** | 0.810 | -43.8% | **2.03×** | **Strong** — top-1 observable real-time |
| **3** | **25.21%** | **1.051** | -35.2% | **3.39×** | **Decent** — pool matches real top-3 |
| 5 | 28.04% | 1.128 | -38.3% | 4.70× | Inflated — excludes XOM/GE/JNJ |
| 9 | 37.12% | 1.332 | -45.1% | 12.85× | Mostly hindsight |
| SPY | 15.21% | 0.908 | -33.7% | 1.00× | — |

**Full window (2009-08 → 2026-05, 16.66yr; candidates above + XOM, JNJ):**

| K | CAGR | Sharpe | MaxDD | Lift vs SPY | Δ from tech-era |
|---:|---:|---:|---:|---:|---:|
| 1 | 16.69% | 0.698 | -49.1% | **1.38×** | -32% |
| 3 | 21.90% | 0.977 | -35.1% | **2.86×** | -15% |
| 5 | 23.95% | 1.071 | -38.3% | 3.77× | -20% |
| 9 | 28.23% | 1.190 | -42.8% | 6.64× | -48% |
| SPY | 14.46% | 0.875 | -33.7% | 1.00× | — |

**Refined findings (regime-dependence is critical):**
1. **The flow thesis is regime-dependent.** SPY_1 lift HALVED (2.03× → 1.38×) when extended back through the XOM-#1 era (2009-2011) — XOM underperformed SPY in 2009-2011 (+13% vs +19% real return). The thesis is specifically a **post-2011 / passive-flow-dominance / tech-leadership** phenomenon, not a universal law. Holding the #1 only works when the #1 is a passive-flow-magnet compounder.
2. **SPY_top_5 is the best-Sharpe play; SPY_top_3 is the most-defensible-empirically.** K=5 dominates K=3 on both lift and Sharpe in every window tested (11.92× vs 4.31× / Sharpe 0.952 vs 0.770 over 24.66yr). The K=5 lift number is hindsight-inflated (pool excludes GE/PFE/WMT/BRK.B which were real top-5 in pre-2011 eras and were slower compounders); a properly-modeled K=5 backtest would likely sit between K=3 and our K=5 — maybe 6-8× lift. But the **Sharpe advantage at K=5 is likely real** (more diversification within mega-caps smooths returns even with worse name selection).
3. **SPY_1 has *worse* Sharpe than SPY in both windows** — 0.810 vs 0.908 (tech era), 0.698 vs 0.875 (full). Single-name concentration is a risk-cost without a Sharpe-benefit even in the favourable regime. The lift is purely return-side; it's NOT risk-adjusted alpha.
4. **The Sharpe-better-than-SPY threshold starts at K=3.** K=3, K=5, K=7, K=9 all beat SPY on Sharpe in both windows. K=1 loses on Sharpe in both.
5. **K=3 has minimal hindsight bias** — pool covers the real SP500 top-3 in every era except 2001-2005 (missing GE). K=5 has more bias (missing 2-3 of the real top-5 in pre-2011 eras).

**Tradeable implication: SPY_top_5 equal-weight monthly-rebalance is the default actionable strategy; SPY_top_3 is the conservative variant.** Going forward (2026+), the actual SP500 top-5 = NVDA + AAPL + MSFT + GOOGL + AMZN — all in pool, all excellent compounders, no hindsight gap. Hold equal-weight, rebalance monthly. Risks: ~20% per name single-stock risk (vs SPY's ~30% combined for top-5), so a single-name catastrophic event hits ~3× harder than SPY. The regime-dependence finding means the edge could erode if leadership rotates back to slower-compounder sectors (e.g. a return to energy/industrials leadership) — though K=5's diversification softens this vs K=1.

These three lenses together imply that **the V3.3d/V3.4 family is more validated than the R3000 falsification suggests** — once the universe is matched to where passive flow operates, the characteristic signal IS an edge; what's still unproven is whether the rotation problem (counterfactual ≈ actual on R3000 but counterfactual > actual on SP500) means a fractional-overlay build is worthwhile or whether the SP500 OOS-2004 lift was itself cohort-specific. **The 17-month forward OOS test on rs_vol_screener showed: held variant lost to SPY (-1.27pp), but monthly-rebalance variant beat SPY (+19.67pp, Sharpe 1.143) — confirming rotation is needed to capture regime shifts (AI capex mega-caps came online via vol normalization Q2-Q3 2025).**

### SPY_top_K variants study (2026-05-15 → 2026-05-16) — the synthesis (since RETRACTED)

Four variants tested on top of the K=5 baseline (Sharpe 1.020, MDD −46%, CAGR +23.2% over 2010-2026):

| Variant | Verdict | K=5 result | Why |
|---|---|---|---|
| A. Regime gate (SPY 50d>200d) | ❌ worse | Sharpe 0.958, MDD −27% | DD-reduction tax > benefit; lags entry+exit |
| B. Momentum filter (12m>0%) | ❌ worse | Sharpe 0.973, MDD −36% | Same shape, gentler |
| C. Hybrid 70% SPY_top_3 + 30% rs_vol K=10 monthly | ❌ worse | Sharpe 0.952, MDD −39% | rs_vol K=10 monthly is itself Sharpe 0.626 < SPY-BH 0.847 — rotation kills the cohort lift (V3.3d Phase 2 finding) |
| D. Lump vs DCA-6 vs DCA-12 vs wait-for-pullback | ✓ lump wins | Lump dominated 12/12 entry months | Every layer of "smart timing" cost ~1pp CAGR |

**Entry-month sensitivity sub-cut: K=5 always-on beat SPY in 136/136 rolling 5y windows 2010-2021.** Median lift 1.43×, worst case 1.04× (still won). **Entry timing is a second-order question.**

### Watchlist sleeve validation (2026-05-17) — the synthesis is FALSIFIED

The two-sleeve "different timescales" synthesis from the 2026-05-16 SPY_top_K variants writeup was tested directly. Two studies, both converge to the same answer.

**Study 1 — hold-once-selected rs_vol** (11 cohorts 2010-2020 year-ends, scan SP500-as-of-T with rs_3y > 0.50 ∧ vol_1y ∈ [0.25, 0.50], take top-K, hold equal-weight 5y/10y forward, no rebalance, liquidate-to-cash on delisting):

| K | hold_y | watchlist CAGR | watchlist Sharpe | SPY-BH CAGR | SPY_top_5 CAGR | beats SPY-BH | beats SPY_top_5 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 5 | +18.70% | 0.787 | +13.56% | +22.63% | 8/11 | 3/11 |
| 10 | 10 | +20.39% | 0.816 | +14.33% | +23.65% | **10/11** | 3/11 |

Watchlist clears SPY-BH across all K × horizon cells but loses to SPY_top_5 in 8-9/11 cohorts on CAGR and 0.18-0.33 below on Sharpe. The standout cohorts (2016/2017/2018) all had NVDA as top scorer (4.21/5.98/2.30) — the watchlist's alpha source is "future mega-cap names before they hit top-5 by market cap."

**Study 2 — rank_hold_minhold hybrid** (re-run Variant C hybrid with rs_vol K=10 sleeve forced to minhold ∈ {6, 12, 24} months, blends 60/40, 70/30, 80/20):

| Sleeve | 60/40 Sharpe | 70/30 Sharpe | 80/20 Sharpe |
|---|---:|---:|---:|
| no-minhold (Variant C) | 0.921 | 0.952 | 0.974 |
| **minhold=6** | 0.936 | 0.963 | **0.982** |
| minhold=12 | 0.913 | 0.945 | 0.970 |
| minhold=24 | 0.918 | 0.950 | 0.974 |

**Best hybrid (80/20, minhold=6) Sharpe 0.982 — still below SPY_top_3 alone (0.997) AND SPY_top_5 alone (1.021).** minhold=6 IS the locally-optimal cadence for the standalone rs_vol sleeve (Sharpe 0.626 → 0.660, MaxDD −51% → −43%) but the improvement isn't enough to close the structural gap to mega-cap concentration.

**Conclusion: the dual-sleeve recommendation is FALSIFIED.** No (minhold, blend_ratio) pair beats SPY_top_5. The "different timescales should compose" intuition doesn't survive when the secondary sleeve has a 0.04+ Sharpe gap to the primary — blending dilutes monotonically toward the weaker. Writeup: `docs/studies/2026-05-16-watchlist-sleeve-validation.md`.

### Revised recommendation (2026-05-17)

| Bucket | Strategy | Timescale | Status |
|---|---|---|---|
| **Active equity sleeve** | SPY_top_5 monthly-rebal (K=3 for lower DD) | Months → years | ✅ shipped, validated 136/136 |
| ~~Watchlist parallel sleeve~~ | ~~rs_vol_screener, 3-5y holds, blended 30%~~ | — | ❌ **FALSIFIED 2026-05-17** |
| Sentiment/news overlay (lens 1) | V3.3c — unbuilt | TBD | TBD |

**Practical recommendation as of 2026-05-17:** for new capital → **100% SPY_top_5 monthly-rebal** (NVDA + AAPL + MSFT + GOOGL + AMZN equal-weight; lump-sum entry per Variant D). **No parallel rs_vol sleeve.** The watchlist (`tt scan rs_vol_screener`) remains as qualitative human-decision-support and as a feed for future strategies (e.g. a graduation overlay that adds rs_vol passers to SPY_top_K's candidate pool as they approach mega-cap threshold).

The watchlist isn't dead — Study 1 confirms it picks NVDA-like future winners before they hit mega-cap. The signal is real. But the right operational shape for it is NOT a fixed-percentage parallel sleeve in a systematic portfolio:
- (a) **Graduation feed.** Names that pass rs_vol AND have ≥$50B cap could be added to SPY_top_K's universe. Requires a separate study.
- (b) **Single-name conviction trade.** Top-3 watchlist names as candidates for an outside-the-systematic-book conviction long. Sized small, held long. Doesn't appear in systematic Sharpe accounting.
- (c) **Decision-support qualitative tag.** Just read `tt scan` output; don't auto-trade it.

What the watchlist should NOT be: a fixed-percentage second sleeve. The portfolio math doesn't work.

**Lens-3 (passive-flow / mega-cap concentration) is now confirmed as the dominant lens for active equity allocation** — every attempt to layer lens-2 (vol-band quality) on top has made things worse (Variant C 2026-05-16, Study 2 2026-05-17). Lens-2 still has interpretive value (helps explain *why* SPY_top_5 works — passive-flow-recipient mega-caps are also high-quality extractors) but not portfolio-allocation value as a separate sleeve.

### Vol-conditioned leverage on SPY_top_5 (2026-05-18) — Thread 4 of edge-discovery roadmap

Tested whether leveraging SPY_top_5 amplifies the existing edge. Full study at [[project_levered_spy_top5_study_2026-05-18]].

**Key finding: constant-leverage on always-on K=5 is impossible inside any reasonable DD ceiling (-45% gate breached at L=1.0 because unlevered baseline is already at -46% on 2001-2026). But VOL-CONDITIONED leverage works — Arm C with target_vol=0.20-0.25 produces CAGR 25-31% AT SIMILAR-OR-HIGHER Sharpe than the unlevered baseline.**

**3 deployment options on the table:**
- Conservative: target_vol=0.15 → CAGR 20.3%, Sharpe 1.21, MaxDD -22.6% (avg L 0.90× — mostly delevered)
- Balanced: target_vol=0.20 → CAGR 25.6%, Sharpe 1.17, MaxDD -29.9% (avg L 1.17×)
- Aggressive: target_vol=0.25, cap=2.5 → CAGR 31.2%, Sharpe 1.14, MaxDD -39.5% (avg L ~1.30×, clears all deploy-ready thresholds)

**Reframing of "lever the strategy up":** the literal answer (constant leverage) doesn't work. The real answer is vol-CONDITIONED leverage — auto-cuts in vol spikes, levers in calm regimes. This is now the active-strategy ceiling for the levered case. The unlevered SPY_top_5 monthly-rebal recommendation from 2026-05-17 remains the conservative default; the Balanced or Aggressive vol-targeted variants are the higher-CAGR options if Scott chooses to deploy leverage.

**AU CGT NOT modelled** — monthly rebal × high turnover means real after-tax CAGR materially below gross. Flag in any deployment conversation.

See [[project_trading_v3_scope_pending]] and [[project_tastytrade_options_account]] and [[feedback_trading_benchmark_spy_bh]] and [[project_levered_spy_top5_study_2026-05-18]].
