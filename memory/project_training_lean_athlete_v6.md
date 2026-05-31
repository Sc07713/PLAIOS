---
name: project-training-lean-athlete-v6
description: Lean Athlete v7.2 training program shipped (4-goal aesthetics-led growth-sim pipeline); supersedes v6.3; re-sim of v7.2 queued; testosterone+nutrition layer is the next highest-leverage build
metadata: 
  node_type: memory
  type: project
  originSessionId: 590bb50e-ebdd-432b-8a34-6f6879f2e5c8
---

**Lean Athlete v7.2 SHIPPED 2026-06-01** — supersedes v6.3. **4-goal, aesthetics-led** weighting: **Aesthetics 40 / Longevity 20 / Basketball 20 / Mobility 20** (Scott added functional mobility as a 4th lens, then said it can fold into basketball+longevity → kept as a scoring lens, NOT a separate day). Built from a **two-stage growth-simulation pipeline** (brainstorm → spec → TDD): **Stage 1** = dose-response GROWTH model (rewards weekly volume — fixes the v6 coverage model's volume-blindness) + greedy budget optimiser, built test-first (14 sanity gates green in `journal/working/2026-05-31-training-value-sim/growth_sim.py`), exercise catalog validated by 2× Codex + 2× Gemini (killed a single-saturation-constant assumption → per-quality K; deflated resilience/power/contact catch-alls; added Dips). **Stage 2** = 5-model "virtual Scott" 12-week behavioural sim (Opus/Sonnet/Haiku/Codex/Gemini, blind), run twice.

**The program (v7.2):** LPP fixed-3 = **Mon LOWER+POWER · Tue PULL+10-12min 4×4 · Thu PUSH**; Wed GAME; Fri small pump + Sat court/Zone-2 both **truly optional**. Mnemonic LOWER·PULL·GAME·PUSH. V-taper on fixed Tue/Thu (not skipped reward days); conditioning folded onto Tue; sprints seeded on Mon (not a cold Sat block); armor non-negotiable Mon micro-dose. Lands in **re-entry ramp first** (post-RSV+post-fast). File: `domains/health/reference/training-program-lean-athlete-v7.md`.

**THE converged lesson (learned 3× now: v6.3 → v7.1 → v7.2):** *anything load-bearing MUST sit on a FIXED day; reward days can only ever be extras.* With 4 goals and ~4 reliable days, something is always stranded on the optional days — so strand the lowest priority, never the top goal. (v7-draft stranded aesthetics→fixed; v7.1 then stranded conditioning→fixed in v7.2.)

**Key methodological caveat (carry forward):** the growth model is a movement-SELECTION tool, not a physiology-grade volume model. High-K qualities (VO2, skill) score low SOLO because they need accumulated volume — trust the OPTIMISER-with-floors output, not raw solo ranks. Skill is structurally under-served by the math → lives in fixed game/court time, not the budget.

**OPEN — queued next session:** **v7.2 has NOT been behaviourally re-simmed** (its fixes were applied from v7.1's convergent findings). Re-sim to close the loop: `journal/next-session-v7-test.md`. Tooling notes (CLI stdin + absolute paths) in that file.

**Parked = next highest leverage (do BEFORE more sim rounds):** **testosterone + nutrition layer** — leanness is ~90% diet and is the TRUE aesthetics lever the training can't reach. `scott-nutrition-protocol.md` to update.

---

### History (superseded)

**Lean Athlete v6.3 (2026-05-31, now superseded by v7.2)** — value-optimised from an equal-weight (33/33/33) cross-domain **combination simulation**; supersedes v6.2 / LPP v5.4. Basketball overlay on a longevity base; aesthetic split = **lean/powerful legs** (RIR/explosive, NOT to failure, anti-chafe lever) + **hypertrophied upper body** (to failure). "Earn it" fractal model: **4-day BASE = the program** = a successful week; the rest is zero-guilt accelerator.

**v6.3's change from v6.2 — the headline:** the two highest value-per-minute movements (**DB Row + loaded Carry**) were stranded on the always-skipped bonus Thursday — the *same* pathology v6.2 caught with the armor. So **Tue Push → Tue Upper** (push to failure + DB Row + carry, ~45–55 min): the 4-day base now trains pull, not just push, closing the base's aesthetics gap. Mnemonic: **RUN (Sun) · LOWER (Mon) · UPPER (Tue) · GAME (Wed)** = the week. **Friday relabelled "the aesthetic accelerator"** (weekly hypertrophy volume that builds the V-taper — reach for it first when flush, since aesthetics is the top lever and the base serves it least). Thu = genuinely-droppable pull micro. Armor (soleus/Copenhagen/Pallof) stays a **high-priority insurance micro-dose on protected Mon** — its near-zero *offensive* coverage value is *why* it gets skipped, so it's protected, never its own block. Still lands in **ramp mode first** (post-RSV + post-fast: no failure 2 wks, maintenance calories until recovery markers green, no max sprints/depth jumps until gates pass; Tue Upper light wk 1–2; Sun = Zone-2/strides until gate clears).

**Key methodological finding (carry forward):** the coverage/combination model is a **movement-SELECTION** tool, not a **volume-PRESCRIPTION** tool. It prices the 2nd weekly hit on a muscle at ≈0, but that repeated volume is where hypertrophy lives — both Codex + Gemini *refused* the "4-day base = 77% of value" over-claim (it's 77% of *coverage*, not adaptation). Use it for what/where, not how-much. Backbone (compound LPP + conditioning) confirmed robust across all saturation settings.

**How it was built:** v6.1 = Codex+Gemini review; v6.2 = 5-model virtual-Scott blind sim + ROI index + goal-weighted scorecard; **v6.3 = equal-weight combination sim** (2× Codex + 2× Gemini: validated/adjusted the L/A/B scorecard, then adversarially checked the conclusions). Scorecard adjustments: DB Row + Carries up, Incline press/OHP down (L-inflation fix), added Chin-ups + Face pull, trimmed isolations.

**Goal weighting:** L / A / B = **EQUAL 33/33/33**. Aesthetics (leanness) is his stated **top lever**. Prefers simple memorable LPP; functional work right-sized as satellites by unique-coverage.

**Parked (next highest-leverage):** testosterone + nutrition layer — leanness is the top aesthetics lever AND it's ~90% diet, so the aesthetic *outcome* is gated on the deficit, not the training (the sim's own caveat). `scott-nutrition-protocol.md` to update.

**Artifacts:** `domains/health/reference/training-program-lean-athlete-v6.0.md` (holds v6.3), `.../v6-value-combination-sim-equal-weights.md` (this sim + reconciled scorecard + reviews), `.../v6-movement-index-and-simulation.md` (ROI index + 5-model sim + scorecard Part C), `journal/decisions/2026-05-31-training-value-optimisation.md`, `journal/decisions/2026-05-31-lean-athlete-v6-review.md`. Sim code + raw reviews: `journal/working/2026-05-31-training-value-sim/`. Relates to [[feedback_trading_tools_is_a_hypothesis_factory]] (studies-vs-builds output shape).
