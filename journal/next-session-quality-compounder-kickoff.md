# Next-session kickoff — quality-compounder study (+ AI-energy status check)

**Drafted:** 2026-05-22 close-out. Two live trading threads from the 2026-05-21/22 session.

---

## Paste-ready prompt

> Read `memory/project_quality_compounder_screen.md` and `D:\Plaios-tools\trading-tools\docs\specs\2026-05-22-early-quality-compounder-screen.md`, then **start the early-quality-compounder study at Phase 0**: scope and run the fundamental-data widening across the `sp500_union_2004_2024.csv` universe (~959 names) using the existing `tt ingest-fundamentals` pipeline (rate-limit/back-off for ~959 CIKs), and **decide the delisting/survivorship-gap approach** (source delisted price+fundamental data vs accept-and-flag the bias). Then bring me a **Phase 1–2 plan** — freeze the quality-growth composite cut (fat + rising gross margin, ROIC >15% & rising, rev growth >20% with operating leverage, FCF+, no serial dilution, a small/mid-cap size band for "early"), and design the **point-in-time backtest as LONG holds** (annual as-of dates, 3–5yr forward returns, no look-ahead via `filed_date`) — **before** running any backtest. Don't reinvent the PIT engine, `universe_sp500`, the rank_hold overlay, or `tt scan` — they exist (V3.3a/b/d). Confirm IB Gateway is up before any ingest.
>
> Also do a 30-second **AI-energy status check**: did Scott place GEV/VRT on Tasty, and has TLN or CEG reclaimed its 200-day MA (the watch trigger)?

---

## Thread 1 — Early quality-compounder screen (the main work)

**Thesis:** "a team that knows how to win keeps winning" — find quality compounders *early* (before they scale), hold them. The repo's V3.4 winners-falsification work already showed the edge is a **long-hold phenomenon** (+951% mean 10yr fwd in the pass set; evaporates under monthly rebal) — which *aligns* with Scott's buy-and-hold/CGT mandate.

**What exists (build on, don't rebuild):** V3.3a PIT fundamentals engine (`derived_metrics` already computes margins/growth/ROE/FCF/gross_profitability), V3.3b `fundamentals` aux + `quality_gp` (found NO edge on TOP_25 — survivorship), V3.3d `universe_sp500` PIT membership + rank_hold + `tt scan`, V3.4 winners-falsification forward-return template.

**The 4 phases** are in the spec. Phase 0 (data widening + delisting gap) is the blocker on everything. Make-or-break risks: survivorship/delisting in price+fundamental data; look-ahead; overfitting; valuation; "early" needs down-cap data; the edge is long-hold not monthly.

**Deliverable:** a study writeup (`docs/studies/...`); graduate to a `tt scan` cut + registered strategy only if it validates repeatably across as-of dates.

## Thread 2 — AI-energy basket (decision DONE; mostly Scott's action)

Multi-agent-converged (Codex+Gemini) 10% satellite. **Buy:** GEV ~0.84 sh + VRT ~1.81 sh (of $20k AUD). **Watch (200-day reclaim):** TLN, CEG. **Excluded:** VST/BE/CRWV/ONDS. Full detail + dissent in `memory/project_ai_energy_power_basket.md`. Email draft is in Scott's Gmail.

*Optional tidy-up if asked:* write the formal decision record at `journal/decisions/2026-05-21-ai-energy-basket.md` (memory already captures the decision + the TLN dissent, so this is housekeeping, not necessity).

## Repo state at close-out
- PLAIOS `e5320f9` (memory), trading-tools `663fda0` (tickers) + `d7655a3` (spec). **Neither repo pushed** — push is opt-in.
- IB Gateway was up this session (port 8000); fundamentals ingest in Thread 1 will need it (or SEC EDGAR direct, which `ingest-fundamentals` uses — verify whether that path needs IB at all; it's HTTP to SEC, so likely independent of IB).
