---
name: options-systematic-spy-falsification-2026-05-18
description: "Comprehensive options-on-SPY testing session 2026-05-17/18 — 39+ variants tested, found same-bar IV-shift bug in Phase 1 engine, falsified Phase 1.5 'edge confirmed' verdict, established that no systematic SPY options strategy beats SPY-BH on absolute return; best automated is short strangle V1 weekly 30d hold (+7.1% CAGR vs SPY-BH +14.2%)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2130c773-0bce-4741-83dd-41949e3c053c
---

Long session 2026-05-17 → 2026-05-18 testing systematic options strategies on SPY. Started as Phase 1.5 follow-up; turned into a comprehensive options-on-SPY falsification exercise after Scott's holding-day question exposed a critical bug.

## The bug discovery (overturns Phase 1.5)

Scott noticed median holding-period was **0 days** with 65% win-rate on Phase 1.5's "winning" pick. Investigation revealed two backtest mechanic bugs in `scripts/strangle_low_iv_study.py`:

1. **Same-bar IV-shift bug**: entry priced at `vix[i]` (signal-day VIX), MTM at bar i+1 used `vix[i+1]`. Strategy systematically captured free vega gains because VIX is mean-reverting from low-percentile entries. Most trades exited same bar on profit_50%.
2. **synthetic_expiry sometimes returned <21d DTE**: combined with `time_21dte` exit, caused immediate same-bar time-stops on entry.

**Phase 1.5's "edge confirmed" verdict was an artifact** of these bugs. Corrected mechanics in new `scripts/strangle_ttm_study.py` use `vix[i+1]` for entry pricing and `synthetic_expiry_robust` that rolls to next month if picked Friday is too close. The corrected long-strangle on TTM Squeeze fires LOSES money under realistic 0.15 spread.

**Status of prior memory `project_strangle_phase1_5_shipped`**: needs flagging as falsified. The 7/8 gate-pass result was a same-bar-IV-shift artifact. The "Tier 2 high-confidence" recommendation should be downgraded.

## Strategies tested this session (39 variants, continuous 2010-2026, $100k start)

**Best automated: short strangle V1 weekly + 30d + hold-to-expiry**
- Final $307,941 / +208% / CAGR +7.1% / Sharpe 0.83 / max DD -15%
- Closest to SPY-BH on Sharpe (0.86), HALF the max drawdown (SPY -34%)
- Only loses in 1 of 16 years (2018 Volmageddon, -6%)
- Strong in flat/down years (2011 +14.6%, 2022 +13.7%)

**Surprising new positive: inverse-squeeze short straddle + TP50 + roll**
- Final $121,294 / +21% / CAGR +1.19% / Sharpe 0.33 / max DD -12%
- 189 trades — actually active
- Counterintuitive: sell premium when TTM Squeeze is OFF (during expansion/quiet, NOT during compression)
- Worth refining in next session

**Catastrophic: long calls on BB-lower-pierce at 16Δ**
- Final $27,397 / -73% / CAGR -7.6% / max DD -73%
- "Buy OTM calls on oversold" is a money-burner — most pierces aren't reversals
- ATM version (50Δ) was -0.4% CAGR (nearly breakeven). Higher delta required.

**The systematic SPY conclusion: no automated options strategy beats SPY-BH on absolute return.** Even the best (short strangle) ended with $308k vs SPY-BH's $882k. The structural reason: equity risk premium (~5-6%/yr) > vol risk premium (~2-3%/yr). Options strategies are decorrelation sleeves, not absolute-return generators on broad indices.

## Important model bias: BS-synth has no skew

BS-synth uses VIX/100 as σ for all strikes. Real markets have:
- **Put skew**: OTM puts trade at HIGHER IV than ATM (30-50% uplift at 0.16Δ)
- **Call skew**: OTM calls trade at LOWER IV than ATM (modest)

This makes the model:
- **Under-price short put premium** (real put-sellers collect more than backtest) → real-world short-put likely works better than -1.6% CAGR shown
- **Over-price short call premium** (real call-sellers collect less than backtest) → real-world short-call worse than 3.7% CAGR shown
- **Approximately right on strangles** (biases offset)

This is why the strangle result is the most trustworthy. Short-put / short-call individual results are model-favored or model-penalized.

## Where real edge lives (out of this study's scope)

1. **Individual stock options** — single-name move sizes >> SPY; skew premium less standardized
2. **Earnings vol crush** — sell ATM straddle day-before-earnings, close day-after; IV crush is large and reliable
3. **Event-day calendars** — Fed/OPEX/earnings have predictable IV term-structure mispricings
4. **Skew-aware structures** — risk reversals, ratio spreads, broken-wing butterflies
5. **Discretionary entry timing** — Scott's tastytrade flow, where judgment + skew + name selection are the edge
6. **Political/insider flow following** — Pelosi options trades, Congress disclosure following (capitoltrades, whalewisdom, etc.)

**How to apply:** when designing next-iteration trading-tools work, target the above rather than more SPY-systematic refinement. SPY systematic options is settled — no edge to find there beyond what we've already characterized.

## Decision-tree for "options sleeve sizing"

For Scott's actual portfolio:
- **Do NOT replace SPY-BH with options strategies.** SPY-BH wins on absolute return.
- **CAN use short strangle V1 weekly 30d hold as a 10-20% decorrelated sleeve** alongside SPY-BH. Pays carry in flat/down regimes (2011, 2015, 2022), modest drag in strong-up regimes. Blended Sharpe ~0.95 (better than SPY alone 0.86).
- **The inverse-squeeze short straddle TP50** is a candidate higher-trade-count sleeve worth refining before deployment.

## Files / artefacts

- Corrected engine: `D:\Plaios-tools\trading-tools\scripts\strangle_ttm_study.py`
- TTM Squeeze module: `D:\Plaios-tools\trading-tools\trading_tools\strategies\ttm_squeeze.py`
- Continuous walker: `D:\Plaios-tools\trading-tools\scripts\strangle_ttm_continuous.py`
- 39 variants results: `D:\Plaios-tools\trading-tools\runs\strangle_ttm\continuous_log_v8.txt` (and v1-v7 for sub-tests)
- Phase 1.5 visualization (still up — but note the Phase 1.5 result is now known artifact): `D:\Plaios-tools\trading-tools\docs\studies\2026-05-17-strangle-phase1-5-fires.html`
- Next-session kickoff: `D:\Plaios-tools\trading-tools\journal\next-session-options-tier1-followups.md`

Related: [[project_strangle_phase1_5_shipped]] (needs updating — verdict was artifact), [[project_tastytrade_options_account]] (venue), [[user_investment_philosophy]] (decorrelation thesis still applies for sleeve sizing).
