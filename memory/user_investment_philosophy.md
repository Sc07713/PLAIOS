---
name: investment-philosophy-beat-gold-decorrelated-bets-crash-opportunity
description: "Scott's investing principles — every position should beat gold-BH (gold is also the default/residual sleeve), holdings should be decorrelated independent theses across industries, and a whole-of-market crash is the exception and the opportunity (mean-revert into oversold quality)"
metadata: 
  node_type: memory
  type: user
  originSessionId: aa1f7ac6-451d-4ff0-891d-92ea9c49d323
---

Scott's stated investing principles (2026-05-12, articulated during the trading-tools V3.2 brainstorm; they shape V3.2+):

- **Every investment should beat just holding gold.** Gold-BH is a hurdle rate. In the V3.2 portfolio overlay this is baked in two ways: `gold_bh` is a mandatory benchmark, *and* **gold (GLD) is the residual sleeve** — capital not deployed into a live thesis sits in gold ("when in doubt, hold gold"), so the portfolio's literal floor is gold-BH. Zero theses active → 100% gold; one lone high-confidence thesis → 60% it / 40% gold (60% is a hard per-position cap).
- **Holdings should be genuinely independent bets** — different industries, different theses, no shared macro or micro driver. The point of a basket is *real* diversification, not 25 names that secretly co-move. (The current trading-tools `TOP_25` universe is ~20 mega-cap tech/comms names — the opposite of this — so a diversification overlay on it understates the benefit; rebuilding a decorrelated cross-sector universe is parked as V3.2b. The V3.2 basket mode trims an over-full book by greedily dropping the most-correlated name, as a partial nod to this.)
  - **Exception (clarified 2026-05-14):** For a **money-extractor / quality-compounder** thesis specifically — where the dominant signal is "each individual position is an exceptional business that durably extracts value from the market" — the decorrelation rule is *relaxed*. A basket of 5-7 money extractors that all happen to share sector (e.g., mega-cap tech compounders) is a coherent thesis if each is selected on intrinsic quality, even though they correlate. Decorrelation is portfolio-construction; money-extractor is security-selection — different layers, different rules.
- **A whole-of-market crash is the one exception — and the opportunity.** When everything correlates to 1, that's the signal to hunt rebound positions: the most-oversold high-quality / sought-after names mean-revert hardest once conditions normalise. This is the seed of the parked V4 "crash-rebound regime overlay" (detect a broad drawdown → rank by oversold-ness × quality → hold for the bounce).
- Base case (from earlier sessions, still holds): "buy and hold quality stocks with good management." Strategies layer small alpha on top of buy-and-hold — not a BH-substitute. Hence every backtest reports vs SPY-BH AND vs asset-BH (and now, for portfolios, vs gold-BH and vs equal-weight-universe-BH too) — see [[feedback_trading_benchmark_spy_bh]].

See [[project_trading_v3_scope_pending]] and [[project_tastytrade_options_account]].
