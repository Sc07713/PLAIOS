# Lean Athlete v7 — growth-validated LPP simulation pipeline

**Date:** 2026-05-31 · **Domain:** Health (L2.2 / L4.4) · **Privacy tier:** B (training only)
**Status:** design approved (brainstorm), pending spec review → implementation plan
**Supersedes the method of:** `v6-value-combination-sim-equal-weights.md` (static coverage model — retired for being volume-blind and sequencing-blind)

---

## 1. Problem & motivation

The v6.3 work used a **static coverage** model. Two flaws surfaced (both caught by the user, both confirmed by Codex + Gemini):

1. **Volume-blind:** it priced the 2nd/3rd weekly hit on a muscle at ≈0. But hypertrophy — now the dominant goal — is *built* by accumulated weekly volume. Coverage ≠ adaptation.
2. **Sequencing-blind:** it had no concept of fatigue, recovery, or day-adjacency, so it produced a week with back-to-back lower-body days (Sun run → Mon legs) and a redundant Thursday.

v7 replaces the static model with a **two-stage growth pipeline** that explicitly models 12-week adaptation (fixing flaw 1) and validates the assembled week behaviourally (fixing flaw 2). The output is a single fixed weekly LPP pattern.

**Fixed constraints (not to be relitigated):**
- **LPP is the skeleton.** Legs / Push / Pull is the user's default and stays. The sim optimises *which exercises fill each slot*, not the shape.
- **Container = 3 fixed LPP strength days + 3 hypertrophy "reward" days + basketball** (game in between + supplementary skills). This is the user's enjoyed, revealed-preference rhythm.
- **Lands in re-entry ramp mode first** (post-RSV + post-fast); steady-state pattern is the target we ramp *into*.

---

## 2. Scoring lenses (goals & weights)

**Aesthetics 40 · Longevity 20 · Basketball 20 · Mobility 20.** Mobility is a **scoring lens only — it never consumes its own day** (it lives inside the LPP compounds, basketball, and a small prehab microdose, per the user's framing that mobility is "part of basketball and longevity").

Sub-dimensions the growth model tracks (~17):

| Goal (weight) | Sub-dimensions |
|---|---|
| **Aesthetics (40)** | delts (side/rear → V-taper width), back/lats (width), arms (bi/tri), upper chest, **× leanness reveal factor** (exogenous, diet-gated) |
| **Longevity (20)** | VO2max, strength / lean mass, bone-tendon-connective resilience |
| **Basketball (20)** | power, speed, COD/decel, conditioning, skill, contact/post-up |
| **Mobility (20)** | ankle, hip, t-spine, adductor (loaded ROM + movement quality) |

Aesthetics gets per-muscle granularity (it's 40% and hypertrophy is per-muscle); mobility gets per-joint granularity. Leanness is modelled as a **multiplier on aesthetic visibility**, not a trainable sub-dimension — it's diet-gated and parked to the nutrition layer. Default scenario: a moderate deficit *is* running (the v6 sim showed the aesthetic outcome lives or dies on it); a "no-deficit" scenario is reported as sensitivity.

---

## 3. Stage 1 — Individual-exercise growth simulation

**Purpose:** rank candidate exercises by the Aesthetics-40-weighted *adaptation yield* they produce over 12 weeks at a realistic weekly dose. **This is the flaw-1 fix:** the model is dose-response, so weekly volume is explicitly rewarded.

**Inputs per candidate exercise:**
- Stimulus vector: per-set effectiveness (0–1) for each sub-dimension it trains.
- Default weekly dose: sets/week × frequency × proximity-to-failure.
- Fatigue cost (systemic + local), injury risk (elevated for a deconditioned/ramp athlete), time cost (min incl. setup).

**Growth model (per sub-dimension, over 12 weeks):**
- **Hypertrophy sub-dims:** yield is a dose-response on **total effective weekly sets to that muscle** — rises steeply to MEV, diminishing returns through MAV (~10–20 sets/muscle/wk), penalty past MRV. Saturating form, e.g. `yield = Gmax·(1 − e^(−sets/k))` with an over-volume penalty. Accumulated over 12 weeks × adherence.
- **Strength / power:** intensity-driven dose-response, saturates at lower volume.
- **VO2 / conditioning:** minutes-at-intensity dose-response.
- **Skill:** practice-rep dose-response.
- **Mobility:** loaded-ROM exposure frequency.

**Outputs:** per-exercise growth vector across all sub-dims + fatigue/injury/time. Weighted by 40/20/20/20 → a ranked exercise leaderboard. **"Even it out"** = a floor constraint guaranteeing each goal reaches a minimum % of its achievable growth (diminishing returns does most of the de-duplication; the floor stops all volume piling onto one already-saturated muscle and starving VO2/mobility).

**Build:** a Python model (`growth_sim.py`), extending the structure of `journal/working/2026-05-31-training-value-sim/value_sim.py`. Reproducible, parameter-documented.

**Evidence grading (per Health domain standard):** hypertrophy volume landmarks and strength/VO2 dose-response = **Moderate-to-Strong** (Schoenfeld/Israetel-style volume literature, established strength & cardio dose-response). Cross-domain weighting = the user's **subjective** call. Per-exercise stimulus matrix = my draft, **graded Moderate, Codex + Gemini-validated before the output is trusted** (same procedure that corrected the v6.3 scorecard).

---

## 4. Stage 2 — Assembly + behavioural validation

**Purpose:** turn the Stage-1 leaderboard into a real week and prove it survives reality. **This is the flaw-2 fix.**

1. **Assemble:** fill the LPP-3 core + 3 hypertrophy rewards + basketball skeleton with Stage-1 winners, hitting the weekly **dose targets** (sets/muscle/wk for the aesthetic muscles; 1 VO2 session; power/speed/skill/contact for basketball; mobility microdose), evened across lenses, inside each session's time budget.
2. **Behavioural sim:** run the **5-model "virtual Scott" 12-week blind simulation** (Claude Opus / Sonnet / Haiku via sub-agents + Codex + Gemini via CLI) on the assembled program. Each scores the **weighted-4-goal outcome + adherence + injury + sequencing**. Extract convergent findings (the binding signal), as in v6.2.
3. **Adversarial review:** Codex + Gemini validate the Stage-1 growth-curve assumptions and review the final assembled program (evidence-bundle only, Tier B).
4. **Iterate to convergence:** if the behavioural sim flags fatigue-stacking, redundancy, or a guilt-tax, swap/re-sequence and re-validate. Converge on one binding program.

---

## 5. Deliverables

- `domains/health/reference/training-program-lean-athlete-v7.md` — **the fixed weekly LPP pattern** (3 core + 3 rewards + basketball), exercises chosen by growth-value, evened to 40/20/20/20, sequenced to survive the behavioural sim, **+ a ramp-mode version**.
- `domains/health/reference/v7-growth-sim-pipeline.md` — study writeup: methodology, growth leaderboard, behavioural-sim convergent findings, reviewer reconciliation, evidence grades, sensitivity (deficit vs no-deficit).
- `growth_sim.py` + bundles/reviews under `journal/working/2026-05-31-training-value-sim/` (or a v7 subfolder).
- `journal/decisions/2026-05-31-training-v7-growth-sim.md` — decision record.
- Memory update to `project-training-lean-athlete-v6` (→ v7) + MEMORY.md line.

---

## 6. Success criteria

1. A **single fixed weekly LPP pattern** the user can follow every week — not a menu.
2. Each slot's exercises chosen by **modelled 12-week growth**, weighted 40/20/20/20, with **no goal starved** (floor met).
3. The assembled week **survives the behavioural sim** — adherence holds and no sequencing red flags (no back-to-back high-CNS lower days, no redundant slot).
4. A **ramp-mode version** for the current re-entry.
5. Method honestly graded: dose-response curves cited, weighting flagged subjective, reviewer-validated.

---

## 7. Non-goals (YAGNI)

- **Not** building the nutrition / testosterone layer (parked; modelled only as the exogenous leanness multiplier + a deficit/no-deficit sensitivity).
- **Not** relitigating the LPP shape or the 3+3+basketball container — both fixed by user preference.
- **Not** a separate mobility day — mobility is a lens.
- **Not** real physiological simulation beyond literature-grade dose-response approximations. The model is a decision tool, not a digital twin.

---

## 8. Open parameters (resolved during implementation, not blockers)

- Exact per-exercise stimulus matrix and the candidate exercise list (drafted, then Codex/Gemini-validated).
- Dose-response curve constants (from literature; graded Moderate).
- Per-session time budget (from the user's real sessions; default ~45–55 min strength, ~25–30 min conditioning).
- Whether the 3 hypertrophy "reward" days are modelled as guaranteed or probabilistic (the v6 behavioural sim says rewards land ~half the weeks — the assembly must make the 3 *core* days deliver the aesthetic floor even if rewards are skipped).
