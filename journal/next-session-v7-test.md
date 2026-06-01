# Next session — re-sim Lean Athlete v7.2 (close the loop)

**Queued:** 2026-06-01 · **Domain:** Health (L2.2 / L4.4)

## Why
v7.2's structure was derived by applying the v7.1 behavioural-sim convergent findings (fold
conditioning onto a fixed day; seed sprints on Monday; Fri/Sat truly optional). It has NOT
itself been behaviourally simulated. Close that loop.

## The job
1. Re-run the 5-model "virtual Scott" 12-week behavioural sim on **v7.2** (the program now in
   `domains/health/reference/training-program-lean-athlete-v7.md`). Same harness as last time:
   - Build a Tier-B bundle like `journal/working/2026-05-31-training-value-sim/bundle-v71-behavioral-sim.md` but with the v7.2 week.
   - Dispatch Opus + Sonnet + Haiku (Agent tool, model override) + Codex + Gemini (CLI), blind.
   - Extract convergent findings; compare adherence + 4-goal outcome + injury vs v7.1.
2. **Check specifically:** did folding conditioning onto Tuesday fix the longevity-stranding
   (Gemini scored it 1.0 on v7.1)? Did seeding sprints on Monday remove the cold-sprint calf
   risk? Is the 1× → ~2× back-frequency nudge enough, or is upper volume still thin for a 40%
   aesthetics goal?
3. If it converges clean → v7.2 is final. If a new item is stranded → that's the v7.3 signal
   (and reinforces the "4 goals can't all be load-bearing on 4 days" structural truth).

## Tooling notes (save time)
- `growth_sim.py` (14 tests green) + `run_stage1.py` are reusable; the catalog is validated.
- Codex/Gemini CLI: pipe the bundle via stdin with a forward-slash absolute path
  (`cat "D:/PLAIOS/.../bundle.md" | codex exec -`); relative paths flaked this session.
- Gemini: `cat bundle | gemini --skip-trust -p "<instruction>"` (its `-p` appends to stdin).

## Also still parked (higher leverage than more sim rounds)
- **Testosterone + nutrition layer** — leanness is ~90% diet and is the true aesthetics lever
  the training can't reach. `scott-nutrition-protocol.md` to update. Arguably do this BEFORE
  another sim round.
