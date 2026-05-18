---
name: project-levered-spy-top5-study-2026-05-18
description: Levered SPY_top_5 overlay study — vol-targeted Arm C beats unlevered baseline on Sharpe (1.21 vs 1.02) AND CAGR (up to 31% vs 23%); constant-leverage on always-on FAILS -45% DD gate at any L; aggressive cell target_vol=0.25/cap=2.5 = the deploy-ready answer
metadata: 
  node_type: memory
  type: project
  originSessionId: 9ec68a43-12e0-4204-a18c-384aeaeb83bc
---

**Verdict from the 5-thread edge-discovery brainstorm, Thread 4 shipped 2026-05-18.**

**Three deployment options on the table** (Scott to pick):

| Option | Cell (Arm C) | CAGR | Sharpe | MaxDD | Avg L |
|---|---|---:|---:|---:|---:|
| **Conservative** | target_vol=0.15, cap=2.0, no gate | 20.3% | 1.21 | -22.6% | 0.90× |
| **Balanced** | target_vol=0.20, cap=2.0, no gate | 25.6% | 1.17 | -29.9% | 1.17× |
| **Aggressive** | target_vol=0.25, cap=2.5, no gate | 31.2% | 1.14 | -39.5% | ~1.30× |

vs SPY-BH 14.0%/0.857/-33.7% and unlevered K=5 baseline 22.6%/1.01/-46.2%.

**Why:** vol-targeting K=5 self-limits DD by cutting exposure when realised vol spikes. The Conservative cell is mostly DELEVERED (65% of days under 1×) — the Sharpe lift comes from avoiding tail bleed, not amplification. The Aggressive cell actually LEVERS UP in calm regimes (2017/2019/2021) and cuts hard in vol spikes (2020/2022). Spread sensitivity is nearly zero (Sharpe range 0.016 across 150bps of borrow spread) because leverage is rarely the binding constraint.

**What was falsified:**
- **Arm A** — constant-leverage on always-on K=5: ALL 6 cells fail -45% DD gate (unlevered baseline already at -46.2% on 2001-2026 secondary window incl GFC). Cannot lever always-on inside the constraint.
- **Arm B** — constant-leverage regime-gated: 4/6 pass; L=1.7 best at CAGR 26.6% / Sharpe 0.87 / DD -44.2%. But Sharpe degrades with leverage (1.01→0.87). Dominated by Arm C at every comparable CAGR.

**Why this matters:** Scott's framing was "leverage compounds the existing method even better." The literal answer (Arm A) is impossible. The real answer (Arm C) is "vol-CONDITIONED leverage", not constant leverage — and the best version DELEVERS most of the time. This is a different shape than the original hypothesis but a stronger result.

**How to apply:**
- If Scott asks about deploying any of these, present the 3-option trade-off table, don't just hand him the Sharpe-best cell. The Aggressive option clears all 3 deploy-ready thresholds (Sharpe >1.10, CAGR >25%, DD ≤-40%).
- Tax friction NOT modelled — AU CGT on monthly rebal × ~$30%+ pre-tax CAGR = real after-tax materially lower (per [[project_au_cgt_constraint_asx_buy_and_hold_only]]). Flag this in any deployment conversation.
- Borrow cost is NOT the binding constraint — strategy is robust to 1.0%→2.5% spread.

**Parked follow-ups** (documented at end of writeup):
- Single-name vol-target comparison
- Vol-targeted SPY-BH (not K=5) A/B
- Daily vs weekly vol-target stepping
- Higher target_vol cap (3.0×, 4.0×)
- AU CGT after-tax modeling

**Writeup:** `D:\Plaios-tools\trading-tools\docs\studies\2026-05-18-levered-spy-top5-overlay.md`
**Spec:** `D:\Plaios-tools\trading-tools\docs\specs\2026-05-18-levered-spy-top5-overlay.md`
**Plan:** `D:\Plaios-tools\trading-tools\docs\plans\2026-05-18-levered-spy-top5-overlay.md`
**Roadmap (5 threads, this was #4):** `D:\Plaios-tools\trading-tools\docs\specs\2026-05-18-edge-discovery-roadmap.md`

**Next threads in roadmap:** Thread 5 (TTM-squeeze long calls), Thread 3 (gold/MF decorrelated sleeve), Thread 1 (passive-flow signal). All carry forward from this brainstorm.

Related: [[user_investment_philosophy]], [[project_trading_v3_scope_pending]], [[feedback_trading_tools_is_a_hypothesis_factory]], [[project_au_cgt_constraint_asx_buy_and_hold_only]].
