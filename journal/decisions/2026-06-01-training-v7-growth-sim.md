# Decision: Lean Athlete v7.2 — growth-simulation pipeline (4-goal, aesthetics-led)

**Date:** 2026-06-01
**Domain:** Health (L2.2 Health Systems / L4.4 Physical Performance)
**Context:** Scott restarted the training optimisation with a 4th goal (functional mobility) and an aesthetics-led weighting, asking for a *growth* simulation (12-week adaptation) rather than the v6 static-coverage model, and a single fixed weekly LPP pattern to follow. Brainstormed → spec (`docs/superpowers/specs/2026-05-31-lean-athlete-v7-growth-sim-design.md`) → built.

**Process (multi-agent + TDD):** Two-stage pipeline. Stage 1 = a dose-response growth model + greedy budget optimiser, built test-first (14 sanity gates green), with the exercise catalog validated by 2× Codex + 2× Gemini (killed a single-saturation-constant assumption; deflated catch-all sub-dims). Stage 2 = a 5-model "virtual Scott" 12-week behavioural sim (Opus/Sonnet/Haiku/Codex/Gemini), run twice to convergence. Study: `domains/health/reference/v7-growth-sim-pipeline.md`.

**Weighting:** Aesthetics 40 / Longevity 20 / Basketball 20 / Mobility 20 (Scott's call; mobility is a scoring lens, not a separate day).

**Options Considered:**
- Static coverage model (v6) — rejected: volume-blind and sequencing-blind (the two flaws Scott caught).
- Individual-exercise growth sim only / daily-plan behavioural sim only — rejected: each leaves one flaw unaddressed. Chose the **pipeline** (both).
- v7-draft (all high-CNS lower on Monday) — falsified by the sim (Monday overload + aesthetics stranded on Friday).
- v7.1 (V-taper on fixed days, sprints to Saturday) — improved aesthetics but the re-sim showed conditioning then stranded on the optional Saturday.

**Decision (v7.2):** LPP fixed-3 — **Mon Lower+Power · Tue Pull+intervals · Thu Push** — carries every goal. V-taper on fixed Tue/Thu; 4×4 conditioning folded onto Tuesday; sprints seeded on Monday; armor a non-negotiable Monday micro-dose; a light 2nd back/delt touch on Thursday for frequency. **Fri (small pump) and Sat (court + Zone-2) are genuinely optional.** Lands in re-entry ramp mode first.

**The converged principle (learned across v6.3 → v7.1 → v7.2):** anything load-bearing must sit on a FIXED day; reward days can only ever be extras. With 4 goals and ~4 reliable days, something is always stranded on the optional days — so strand the lowest priority, never the top goal.

**Expected Outcome:** The top goal (aesthetics/V-taper) and the minimum longevity dose (intervals) both happen on days that actually get done (~80–87% fixed-day adherence in sim); injury risk reduced by seeding sprints vs a cold weekly block. Leanness — the true aesthetics lever — remains diet-gated (testosterone+nutrition layer still parked, now the highest-leverage next build).

**Status / caveat:** v7.2's fixes are applied from v7.1's convergent findings but **not yet behaviourally re-simmed.** Queued: `journal/next-session-v7-test.md`.

**Review Date:** next session (re-sim v7.2) + ~2026-07-15 after real adherence.
