# Lean Athlete v7 — growth-simulation pipeline (study)

**Date:** 2026-05-31 → 2026-06-01 · **Weights:** Aesthetics 40 / Longevity 20 / Basketball 20 / Mobility 20
**Output:** `training-program-lean-athlete-v7.md` (v7.2) · **Spec:** `docs/superpowers/specs/2026-05-31-lean-athlete-v7-growth-sim-design.md`
**Code + artefacts:** `journal/working/2026-05-31-training-value-sim/` (`growth_sim.py` + 14 tests, `run_stage1.py`, bundles, reviews, sim syntheses)

A two-stage pipeline replacing the v6 static-coverage model. Each stage covers the other's blind spot: Stage 1 (math) picks the exercises and rewards weekly volume; Stage 2 (behaviour) proves the assembled week survives a real life.

---

## STAGE 1 — growth model (math)

**The fix over v6:** the value function is now a **12-week concave growth curve that is a function of weekly volume** — not a one-touch coverage saturation. Volume is the thing being optimised, which is what v6 got wrong for a hypertrophy-led goal.

**Engine (built test-first, 14/14 sanity gates green):**
- Hypertrophy dose-response per muscle: rises to MAV (~10–20 sets/wk), junk-volume penalty past MRV (~22).
- Effective sets weighted by RIR; frequency bonus (2× beats 1× at equal volume).
- Per-quality saturation constants K (Codex + Gemini-validated): VO2 ~11, conditioning ~9, strength/resilience ~6, power/speed ~4, cod/contact ~5, **skill ~16** (can't be "solved" in one session), mobility ~5.
- Greedy budget optimiser: concave growth + linear time budget → spending the next minute on the highest weighted-marginal-growth/min is provably optimal; per-goal floors keep nothing starved.

**Catalog validation (Codex + Gemini):** killed the single-K assumption; deflated `resilience`/`power`/`contact` as catch-alls; re-credited 4×4 VO2; added Dips. See `review2-catalog.md`.

**Leaderboard (weighted growth/min, validated catalog):** Incline press · Pull-ups · Chin-ups · Dips · DB Row lead. **Methodological catch:** high-K qualities (VO2, skill) score low *solo* because they need accumulated volume — so the trustworthy output is the **optimiser with floors**, not the raw solo rank. Skill is structurally under-served by the math (sole supplier of one of six basketball facets) → handled via fixed game/court time outside the budget.

---

## STAGE 2 — behavioural sim (reality), run twice

5 blind models (Opus, Sonnet, Haiku, Codex, Gemini) each lived the assembled week for 12 weeks, scoring adherence + 4-goal outcome + injury + sequencing.

### Round 1 — v7-draft (all high-CNS lower consolidated on Monday)
Convergent (`stage2-behavioral-sim-synthesis.md`):
- **[5/5] Aesthetics (top goal) under-served — its accelerator volume sat on the skipped Friday.** Same stranded-value pathology as v6.2/v6.3.
- **[4/5] Monday over-stuffed** (the CNS-consolidation over-corrected) → calf risk.
- **[3/5] push/pull imbalance** (double-pressing) hurts the V-taper.
→ **v7.1:** V-taper onto fixed Tue (pull) + Thu (push); sprints off Monday; Fri demoted to a tiny optional pump.

### Round 2 — v7.1 (loop closure)
- **✅ The aesthetics fix worked** — outcome rose 3→4 across most models; fixed-day adherence 80–87%; Opus: "design intent achieved."
- **⚠️ But the stranding MOVED, not vanished:** by putting 4×4 + sprints on the optional Saturday, **conditioning/longevity became the new stranded item** (Gemini scored Longevity 1.0). **[4/5] #1 fix: pull conditioning onto a fixed day.**
- **[3/5] secondary:** 1× push + 1× pull/week is thin frequency for a 40% goal → nudge toward 2×.
→ **v7.2:** 4×4 becomes a 10–12 min Tuesday finisher; sprints seeded on Monday; Saturday pure-optional; a light 2nd back/delt touch on Thursday.

### The converged lesson (three versions running)
With **four goals and ~4 reliable days you cannot put everything load-bearing on fixed days** — something is always stranded on the optional days. The only question is *what*. The correct call is to strand the lowest-priority thing: v7.2 protects Aesthetics (40%) AND the minimum conditioning dose on fixed days, leaving only true nice-to-haves optional.

---

## OPEN

- **v7.2 has NOT been behaviourally re-simmed** — its fixes are applied from the v7.1 convergent findings. Re-sim next session (`journal/next-session-v7-test.md`).
- The growth model is selection-grade, not physiology-grade; `resilience` is a coarse sub-dim (deferred split).
- **Highest-leverage parallel build: testosterone + nutrition layer** — leanness (~90% diet) is the true aesthetics lever the training can't reach.
