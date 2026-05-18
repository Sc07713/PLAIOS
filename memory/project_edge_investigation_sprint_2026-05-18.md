---
name: edge-investigation-sprint-2026-05-18
description: "8-study sweep — 6 falsifications, 1 refinement (Tier 1.2 16Δ/21d/TP65), 1 follow-up to chase (lever the gold-blend), 1 data-acquisition punt. No new strategy beats SPY_top_5 baseline."
metadata: 
  node_type: memory
  type: project
  originSessionId: aad0f973-7da5-4223-826e-567d41f6abac
---

End-to-end edge-discovery investigation sprint shipped 2026-05-18. Eight
studies in one session, covering remaining roadmap threads + Tier 1
options follow-ups. **Why:** the user asked for "all the investigations
done" — opportunistic batch run before committing to a deployment
decision on Thread 4. **How to apply:** when the user asks about
trading-tools status, point to `docs/studies/2026-05-18-edge-investigation-sprint.md`
for the full synthesis.

## Findings summary

| Study | Verdict |
|---|---|
| Gap-up momentum Option A/B | **Falsified** — best 8.7% CAGR vs SPY-BH 11.0%; position stacking sharpe gains are dilution artefacts |
| Thread 5 — long options on TTM Squeeze fires | **Falsified** — 0/10 cells beat SPY-BH; 33 fires/16y too sparse |
| Thread 3 H3a — gold sleeve | **Trade-off zone** — 60/40 SPY_top_5/GLD-BH: Sharpe 1.17 (+0.14), DD -31.25% (-15pp). GLD-BH beats GLD-trend in this window. Sets up Thread 3+4 fusion: lever the blend. |
| Thread 2 H2b — VIX regime switch | **Falsified** — 200d-MA gate (H2a) beats every VIX-threshold variant on Sharpe (1.11 vs 1.06) |
| Tier 1.1 — single-name short strangles | **Falsified** — 0/7 names beat name-BH; 90%+ DDs on 16Δ variants. Needs iron condor wings + smaller sizing. |
| **Tier 1.2 — inverse-squeeze short premium refinement** | **REFINED** — new best: 16Δ short strangle / 21 DTE / TP 65% / squeeze-off entry: +5.56% CAGR / Sharpe 0.52 / -37.25% DD / 312 trades / 87.5% WR. **4-5× the prior known cell.** OTM > ATM at TP≥50%. |
| Tier 1.3 — earnings vol-crush | **Falsified at realistic IV bump** — 1.4-1.6× IV/RV (academic norm) still loses on every name. Needs defined-risk wings. |
| Tier 1.4 — Pelosi/Congress follower | **Deferred** — needs QuiverQuant $10 or DIY scraper. Memo at `journal/next-session-pelosi-congress-data-acquisition.md`. |

## Open follow-ups (ranked)

1. **Thread 3+4 fusion** — lever the 60/40 SPY_top_5+GLD-BH blend; -31%
   DD leaves ~14pp of leverage headroom under the -45% cap. Likely
   highest-EV next step.
2. Tier 1.2 V2 — defined-risk iron condor on the refined 16Δ/21d/TP65 cell.
3. Tier 1.4 — Pelosi follower (cheap data investment).
4. Earnings iron condors (Tier 1.3 with wings).
5. Single-name iron condors on mean-reverting universe (Tier 1.1 V2).

## Related

- [[project_trading_v3_scope_pending]] — broader strategy roadmap
- [[project_levered_spy_top5_study_2026-05-18]] — Thread 4 deployment decision
  still pending
- [[project_options_systematic_spy_falsification_2026-05-18]] — original
  options-on-SPY falsification (this sprint extends it)
- [[user_investment_philosophy]] — lens-3 (passive flow) thesis aligned
  with deferred Pelosi follower
- [[feedback_trading_tools_is_a_hypothesis_factory]] — falsification IS
  a deliverable; 6/8 falsifications here is healthy
