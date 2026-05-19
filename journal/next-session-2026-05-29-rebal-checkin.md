# Next-session kickoff — 2026-05-29 monthly rebal + tactical return

**Trigger date:** Friday 2026-05-29 (last trading day of May)
**Type:** Operational rebal — both systematic monthly cadence AND the
hard return trigger for the 2026-05-19 tactical 65/35 GLD overweight.

## What needs to happen at this rebal

This is the most important rebal in the live deployment so far because
it executes two things at once:

1. **Hard return to 70/30** — the tactical overweight was placed with
   2026-05-29 as the pre-committed exit date. Trim GLD, redeploy in
   the 5 mega-cap names. Non-negotiable — without executing the
   return trigger, "tactical" becomes "permanent" through inaction.

2. **Standard monthly rebal** — re-rank top 5 by PIT mcap, equal-weight,
   re-step leverage from latest 42d realized vol.

## Run sequence (morning of 2026-05-29)

```bash
cd D:/Plaios-tools/trading-tools
.venv/Scripts/activate
python scripts/refresh_to_today.py data/deploy_today_universe.csv
python scripts/deploy_today.py
```

`deploy_today.py` will print target dollars and shares for every
position at the new leverage (which may have stepped from 1.52× as
vol drifts). Trade against the deltas, not absolute new positions.

## Specifically check at this rebal

- **AVGO graduation watch** — sitting at #6 by mcap ($1.98T) as of
  2026-04-30. To overtake AMZN ($2.85T) for a top-5 slot, needs ~40%
  relative outperformance. Unlikely in 30 days but check the ranking.
- **GLD position drift** — at 53.4% of capital on 2026-05-19. If GLD
  rallied, this is more than 53.4% of current capital and the trim
  back to ~45.7% is larger.
- **Leverage step** — current 1.52× is keyed off 16.4% realized vol.
  If vol fell, leverage wants to rise (Reg-T may cap). If vol rose,
  leverage drops automatically (welcome — natural defense).
- **rs_vol watchlist** — re-run `python -m trading_tools scan
  --strategy rs_vol_screener` and see if the semi-cap basket
  (LRCX/KLAC/AMAT) still passes. If yes and capital has grown
  toward $50k+, reconsider activation.

## Things to update post-rebal

1. **[[project_deployment_state_2026-05-19]]** — append a section
   "2026-05-29 rebal executed" with new share counts and the new
   leverage number. Lock the return-to-70/30 as completed.
2. **MEMORY.md index** — no new entries expected, just the update.

## Why this matters

This is the discipline test. The systematic strategy works because
the rebals get executed mechanically — not skipped, not delayed, not
adjusted because "the market feels weird." Every override compounds
into strategy drift. The 2026-05-29 trim of GLD back to 70/30 is the
first real test of "will Scott actually follow the rules he set on
2026-05-19?"

If the rebal doesn't get run, flag it loudly in the next session and
ask what the user wants to do (resume at the next monthly, or accept
the drift).

## Related

- [[project_deployment_state_2026-05-19]] — the live book
- [[project_stack_and_lever_fusion_2026-05-19]] — the strategy
