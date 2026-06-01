# Decision: Lean Athlete v6.3 — equal-weight value optimisation

**Date:** 2026-05-31
**Domain:** Health (L2.2 Health Systems / L4.4 Physical Performance)
**Context:** Scott queued a value-maximisation simulation (journal kickoff 2026-05-31): under EQUAL goal weights (Longevity/Aesthetics/Basketball = 33/33/33), find which workout/movement *combinations* add the most cross-domain value — accounting for overlap (don't double-count) and time cost — and output the simplest LPP-based program capturing maximal value/session. Pre-step: validate the Part C L/A/B scorecard with Codex + Gemini, then optimise. Don't relitigate the LPP shape.

**Process (multi-agent, per `protocols/multi-agent.md`):** Built a saturating coverage model over 13 goal sub-dimensions (`journal/working/2026-05-31-training-value-sim/value_sim.py`). Two Codex + two Gemini passes: (1) validated/adjusted the L/A/B scorecard; (2) adversarially checked the simulation's conclusions. Both reviewers signed the restructure and *refused* one over-claim (below). Study: `domains/health/reference/v6-value-combination-sim-equal-weights.md`.

**Options Considered:**
- Keep v6.2 as-is (Push-only Tuesday, Row+Carry on bonus Thu). Rejected: strands the two highest value/min movements on the day adherence data says gets skipped.
- Give the armor / skills their own protected blocks. Rejected: armor has near-zero *offensive* coverage value (justified only as insurance); skills stay on court/game.
- Read "4-day base = 77% coverage" as proof the bonus is marginal. **Refused by both reviewers** — coverage ≠ adaptation; aesthetics needs weekly volume the one-touch model can't price.

**Decision (v6.3):**
1. **Tue Push → Tue Upper** — fold DB Row + a loaded Carry onto the protected day (off skipped Thu). The 4-day base now trains pull, not just push, closing the base's aesthetics gap. Guardrails: ~45–55 min, row 3–4 hard sets, carry 4–8 total, don't tax grip/feet for Wed's game.
2. **Friday = "the aesthetic accelerator"** — relabel from pure bonus. It's the weekly hypertrophy *volume* that builds the V-taper; since aesthetics is the top lever and the base serves it least, reach for it first when flush (still zero-guilt).
3. **Thu** demoted to a genuinely-droppable pull micro (load-bearing pull now on Tue).
4. **Armor** confirmed as a high-priority *insurance* micro-dose on Mon — its near-zero offensive value is *why* it gets skipped, so it's protected, never its own block.
5. **Scorecard adjusted** (both reviewers): DB Row + Carries up; Incline press/OHP down (L-inflation fix); added Chin-ups + Face pull; trimmed isolations.

**Expected Outcome:** A 4-day week now covers the full upper body (not half), so the aesthetic floor no longer depends on a skipped day; injury insurance stays protected; skills/conditioning (sole suppliers) untouched. Backbone (compound LPP + conditioning) confirmed robust across all saturation settings — the shape was not relitigated, only *which* compounds sit *where*. Lands in **ramp mode first** (post-RSV/post-fast): Tue Upper light in wk 1–2, Sun = Zone-2/strides until the recovery gate clears.

**Caveat carried forward:** the coverage model is a movement-*selection* tool, not a volume-*prescription* tool. Do not read coverage % as adaptation.

**Review Date:** ~2026-07-15 — after ~6 weeks of real adherence + once out of the ramp; check (a) is Tue Upper actually getting done / not stealing Wed, (b) is the aesthetics outcome moving (gated on the deficit, not just training — see testosterone+nutrition layer, still parked).
