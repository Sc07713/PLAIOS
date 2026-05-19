---
name: deployment-state-2026-05-19
description: "Live deployment orders for the trading book — $20k capital, Aggressive profile (tv=0.25), tactical 65/35 gold overweight with hard return trigger to 70/30 on 2026-05-29. First real-money deployment of the stack-and-lever fusion strategy."
metadata: 
  node_type: memory
  type: project
  originSessionId: b289a59b-eae4-4325-b0f4-d2c8dda6ba73
---

First real-money deployment of the stack-and-lever fusion strategy
([[project_stack_and_lever_fusion_2026-05-19]]). Capital $20,000 via
IBKR US equity account, Reg-T margin.

**Why:** the stack-and-lever fusion landed a deployable winner at the
end of the prior thread; user asked "what would I do today?" which
forced the translation from backtest to live orders.

**How to apply:** when user references "my live trading book" or
"the active deployment" in future sessions, this is the snapshot.
Pair with the discipline checklist below.

## Configuration locked in 2026-05-19

| Parameter | Value |
|---|---|
| Capital | $20,000 |
| Account | IBKR US equity (Reg-T, not portfolio margin) |
| Profile | Aggressive (target_vol=0.25, cap=2.5×) |
| Current leverage | 1.52× (computed from 42d realized vol 16.40%) |
| Tactical overlay | **65/35 equity/gold** (5pp overweight on GLD pullback) |
| Return trigger | **2026-05-29** — hard return to 70/30 systematic weight |

## Orders placed 2026-05-19 (lump-sum, all positions)

| Symbol | Shares | Dollars | % of capital |
|---|---|---|---|
| NVDA | 17.80 | $3,963 | 19.8% |
| GOOGL | 9.76 | $3,963 | 19.8% |
| AAPL | 13.29 | $3,963 | 19.8% |
| MSFT | 9.40 | $3,963 | 19.8% |
| AMZN | 14.80 | $3,963 | 19.8% |
| GLD | 25.48 | $10,669 | 53.4% |
| **Total notional** | | **$30,484** | 152.4% |
| Borrowed on margin | | $10,484 | 52.4% |

Closes used (2026-05-18): NVDA $222.68, GOOGL $406.11, AAPL $298.16,
MSFT $421.73, AMZN $267.80, GLD $418.69. Top-5 universe = same as
the 2026-04-30 rebal selection.

## What's parked

- **Semi-cap thematic basket** (LRCX + KLAC + AMAT) — selected via
  rs_vol scan but skipped at $20k capital. KLAC at $1,756/share is
  ~9% of capital in one name — too concentrated. Activate when
  capital reaches ~$50k+. See [[project_trading_v3_scope_pending]].
- **4-week DCA on equity sleeve** — recommended at $100k illustrative
  base but switched to lump-sum at $20k (DCA dollar drag outweighs
  the behavioral cushion at this capital level).

## Operational discipline (recorded for future-session continuity)

| Cadence | Action |
|---|---|
| Daily | Eyeball SPY vs $674 (200d MA, gate level). Equity flips to T-bills if SPY < MA for 2+ sessions. |
| Weekly Monday | Run `python scripts/deploy_today.py` in trading-tools repo. Re-step leverage if it moved >0.1×. |
| **2026-05-29 (next rebal)** | **Hard return to 70/30**. Trim GLD by ~$3,200 (7.5 shares), redeploy across the 5 mega-caps equally. Re-rank top 5 by mcap (AVGO at #6 watching for graduation). |
| Monthly thereafter | Same — rebal SPY_top_5 equal-weight, re-step leverage, re-run rs_vol scan for basket candidates. |

## Reg-T constraint note

At sub-$100k NLV at IBKR, user is on Reg-T (2× max), not portfolio
margin. Aggressive (cap 2.5×) is rarely binding at current vol but
will pinch in low-vol periods (realized vol < 12.5% → strategy wants
2.0-2.5×, broker caps ~1.9× after IRM haircuts). Expected drag vs
full Aggressive: ~1-2pp CAGR. Still beats Balanced execution.

## AU CGT note for tactical trim

The 2026-05-29 trim of GLD back to 70/30 is a <12mo holding period —
no 50% CGT discount, full marginal rate on any gain. At ~$3,200 of
trim, ~$160 gain (5% move) → ~$70 tax. Small but eats the tactical
edge. Tactical trades carry CGT cost that fixed-weight strategies
don't.

## Related

- [[project_stack_and_lever_fusion_2026-05-19]] — strategy origin
- [[project_levered_spy_top5_study_2026-05-18]] — Arm C predecessor
- [[user_investment_philosophy]] — beat-gold-BH + crash-as-opportunity
- [[project_au_cgt_constraint_asx_buy_and_hold_only]] — CGT memo
- [[feedback_dont_diminish_savings_value]] — concrete orders over abstract framing
