# Lean Athlete v6 — value-maximisation COMBINATION simulation (equal weights)

**Date:** 2026-05-31 · **Weights:** Longevity / Aesthetics / Basketball = **33 / 33 / 33**
**Companions:** `v6-movement-index-and-simulation.md` (ROI index + 5-model sim, Part C scorecard), `training-program-lean-athlete-v6.0.md` (now v6.3)
**Method artefacts:** `journal/working/2026-05-31-training-value-sim/` (sim code `value_sim.py`, 2× Codex + 2× Gemini reviews, bundles)

This is the lens Scott asked for: not "rank movements," but "which movement **combinations** add the most cross-domain value, accounting for **overlap** (don't double-count two movements hitting the same goal) and **time cost**." It produces the simplest LPP-based program that captures the most value per session.

---

## STEP 1 — Scorecard validated (Codex + Gemini), then adjusted

The Part C L/A/B scores were a Claude first pass. Both reviewers pressure-tested them. **Convergent corrections applied** (full reviews: `journal/working/.../review-{codex,gemini}.md`):

| Movement | L | A | B | Equal | Change vs Part C | Driver |
|----------|:-:|:-:|:-:|:---:|---|---|
| 4×4 / conditioning | 5 | 3 | 4 | **4.00** | A 4→3, B 3→4 | Gemini (leanness is diet, HIIT interferes with A) + Codex (repeat-sprint transfer) |
| Pull-ups | 4 | 5 | 3 | **4.00** | — | — |
| **Chin-ups** (new) | 4 | 5 | 3 | **4.00** | added | both: pull-up + more arm/aesthetic |
| **DB Row** | 4 | 5 | 3 | **4.00** | B 2→3 | both: rebounding / box-out / post-up = horizontal pull |
| Single-leg RDL | 4 | 3 | 4 | 3.67 | — | (flag: DB-ceiling caps strength gain ~3 mo) |
| Bulgarian SS | 4 | 3 | 4 | 3.67 | — | high-variance: ramp/knee/load-ceiling |
| Acceleration sprints | 3 | 3 | 5 | 3.67 | L 4→3, B 4→5 | Gemini (CNS/tissue tax) + Codex (direct first-step transfer); **ramp-gated** |
| **Carries** | 4 | 3 | 4 | **3.67** | B 3→4 | Codex (contact/grip; grip = longevity marker) |
| **Face pull** (new) | 4 | 4 | 3 | 3.67 | added | Gemini: shoulder health + rear-delt width + posture; outscores rear delt fly |
| Abs / leg raise | 3 | 4 | 3 | 3.33 | — | — |
| Decel ladder | 3 | 1 | 5 | 3.00 | — | kept L=3 (rubric counts tissue-resilience; tie-break vs Gemini L→1 / Codex L→4) |
| Jumps / plyo | 2 | 2 | 5 | **3.00** | L 3→2 | both: ramp tendon risk > BMD benefit; **ramp-gated** |
| Pullover | 3 | 4 | 2 | 3.00 | — | — |
| Incline DB Press | 3 | 3 | 3 | **3.00** | L 4→3, A 4→3 | both: pressing is aesthetic not a longevity pillar; DB ceiling |
| DB OHP | 3 | 3 | 3 | **3.00** | L 4→3, A 4→3 | Codex: redundant front-delt vs incline (already optional) |
| Pallof / med-ball | 3 | 1 | 4 | 2.67 | A 2→1 | Codex: no aesthetic contribution |
| Soleus / calf | 3 | 1 | 4 | 2.67 | A 2→1 | Codex: calf definition minor — but **insurance value, see below** |
| Copenhagen | 3 | 1 | 4 | 2.67 | — | insurance (kept L=3 for symmetry with decel) |
| Lateral raise | 2 | 5 | 1 | 2.67 | — | pure-aesthetic polish |
| Skills | 2 | 1 | 5 | 2.67 | L 1→2 | Gemini: reactive-coordination brain-health [<85%]; **sole skill supplier** |
| Rear delt fly | 2 | 4 | 1 | 2.33 | B 2→1 | Codex; face-pull supersedes |
| Curls / triceps | 2 | 3 | 1 | 2.00 | A 4→3 | Codex: load-ceiling, low equal-weight efficiency |

**Systematic biases both reviewers flagged and I corrected:** (1) **L-inflation** — Longevity was a proxy for "general movement"; now reserved for true mortality levers (VO2, big-compound strength, grip). (2) **A over-credit for cardio + isolation** — leanness is ~90% diet, so conditioning's A trimmed and isolations don't earn an aesthetic premium they don't pay. (3) **B under-credited strength transfer** for contact/post-up (rows, carries) — corrected up.

---

## STEP 2 — The combination model (how overlap is priced)

Each session is a **coverage problem** over 13 goal sub-dimensions (L×3, A×4, B×6), equal goal weights, equal split within each goal. Coverage of each sub-dimension **saturates**: `coverage = 1 − e^(−Σstim/τ)`. A second movement hitting an already-covered sub-dimension adds ≈0 — that *is* "don't double-count." Time cost (minutes incl. setup) is the denominator. Two readouts:

- **Marginal value / min** — greedily add the next movement worth the most per minute. Rewards **broad compounds** that double-dip.
- **Unique coverage** — value lost if a movement were removed from *everything*. Isolates the **irreplaceable** movements (sole supplier of a sub-dimension).

Robustness checked across τ ∈ {2,3,4,6}; the top tier is stable.

---

## STEP 3 — What the simulation found

### 3a. The backbone (robust across all saturation settings)
Highest value/min are the **broad compounds that double-dip:** Carries, DB Row, Lateral lunge, Incline press, Jumps, Chin-up/Pull-up, 4×4. Scott's "simple LPP is best" instinct is mathematically correct and **does not depend on the saturation assumption.** This is settled — we refine *which* compounds and *where they sit*, not the LPP shape.

### 3b. The headline restructure — the two best movements are stranded on the skipped day
**Carries (#1) and DB Row (#2) by value/min currently live on the always-skipped bonus Thursday.** This is the *identical pathology* the 5-model sim found with the armor in v6.2 (best-value work parked where it never happens). **Fix: fold DB Row + a Carry onto the protected Tuesday** → Tuesday "Push" becomes "**Upper**" (push + pull + carry). Both reviewers signed this (Gemini 95%: keeps High–Low CNS cadence; Codex 80–85%, with guardrails: Tue 45–55 min, row 3–4 hard sets, carry 4–8 total, suitcase/offset rotation, don't tax Wed's grip/feet).

### 3c. Coverage ≠ adaptation — the model's own blind spot (both reviewers refused finding 2/3)
The model said "4-day base = 77% of max coverage; full week = 86%," implying the bonus is marginal. **Both reviewers refused this as a real-world claim, correctly.** The model is *one-touch*: it prices the 2nd/3rd weekly hit on a sub-dimension at ~0. But **hypertrophy and the V-taper need weekly volume and progressive overload** — the repeated hits *are* where much of the aesthetic adaptation lives. So:

- The 77% is a **coverage** number, not a **value/adaptation** number.
- The base's weakest goal is **Aesthetics (69% coverage vs L 91% / B 72%)** — and aesthetics is Scott's **top** lever. The base under-serves exactly the goal he cares about most, because the upper/pull volume was bonus-gated.
- **Therefore the bonus volume is not marginal for aesthetics — it is the accelerator for the #1 goal.** Two moves follow: (i) load the protected days with real pull/upper volume (3b puts Row+Carry on Tue → base aesthetics coverage rises), and (ii) **relabel Friday from "pure bonus" to "the aesthetic accelerator"** — still zero-guilt for adherence, but named as the session that moves the look fastest.

### 3d. The armor — zero offensive value is exactly why it's load-bearing
Soleus/calf, Copenhagen, Pallof have **near-zero unique coverage (0.01–0.04)** — their sub-dimensions get covered by RDL/row/carry/decel anyway. The breadth math says "redundant." **Both reviewers refused "dispensable."** The model can't price (a) injury-probability reduction or (b) *tissue-specific* load tolerance — a row trains "posterior chain" but not the Achilles/adductor load that actually fails mid-game. The zero-visible-payoff is precisely *why* it gets skipped — which is the argument for **protecting** it, not cutting it. **Verdict: keep exactly as v6.2 — a 6–10 min non-negotiable insurance micro-dose woven into protected Monday, never its own block.** Relabel "near-zero value" → "high-priority insurance."

### 3e. Skills — low breadth, irreplaceable
Skills are the **sole supplier of the SKILL sub-dimension** (unique coverage 3.97, second only to conditioning). They score low on breadth-math because they're single-axis — but the coverage model *correctly* flags sole-supplier status. **Resolves Scott's gut question: keep skills, exactly as instinct says.** They're the point of the B goal and nothing else touches them. Court/game/Sat + daily home microdose.

### 3f. Session value map (equal weights)
| Session | Coverage | L / A / B (of each goal) | Read |
|---|:---:|---|---|
| Mon Lower | 38% | 62 / 6 / 47 | B+L engine; A≈0 *by design* (lean legs = diet) |
| Tue **Upper** (restructured) | ↑ | push+pull+carry → lifts A off bonus-gate | the A engine, now de-risked |
| Thu Pull (bonus) | — | most balanced session, but now lighter (Row/Carry moved to Tue) → genuinely droppable |
| Sun Run | 27% | 33 / 13 / 36 | sole VO2+speed supplier; irreplaceable |
| Sat Court | 5% | 0 / 0 / 16 | sole SKILL supplier; irreplaceable despite low % |

---

## STEP 4 — The output: simplest value-optimised LPP (→ program v6.3)

**Mnemonic: RUN · LOWER · UPPER · GAME = the week. Everything else is accelerator.**

- **4 PROGRAM days (the realistic ceiling — hitting these = a successful week):**
  - **Sun RUN** — speed when fresh + intervals (sole engine: VO2 + speed + calorie burn).
  - **Mon LOWER** — jumps → lean-strength (RIR/explosive) → **armor insurance micro-dose** → decel.
  - **Tue UPPER** — incline press → chin/row → row/pull → **carry finish.** ← the restructure: the two best movements now protected; this is the aesthetic floor.
  - **Wed GAME** — skill + conditioning + contact, the real thing.
- **3 ACCELERATOR days (zero-guilt, but named for what they do):**
  - **Fri UPPER PUMP = the aesthetic accelerator** — the weekly hypertrophy *volume* that builds the V-taper (the one finding-3c says is not marginal for the #1 goal). Take it when flush.
  - **Thu pull micro / Sat court** — extra pull volume + the sole skill supplier; both genuinely droppable now that Tue carries the load-bearing pull.
- **Daily microdose:** dribble / post-up footwork at home (sole skill supplier, no session needed).

**Satellites sized to weights (by unique coverage):** pure-aesthetic isolations (laterals, curls, rear-delt→face-pull) = thinnest polish, Fri only; prehab armor = small but non-negotiable insurance, Mon; skills = protected on court because nothing substitutes.

**Ramp note (Scott is mid re-entry):** Tuesday Upper lands light first — don't stack Row+Carry+pump in wk 1–2 (RPE 5–6, no failure). Sun run = Zone-2/strides, not 4×4/max sprints, until the recovery gate clears. The restructure is structural; the ramp governs the dose.

---

## Caveat (carry this forward)
This coverage model is a **movement-selection** tool, not a **volume-prescription** tool. Use it to decide *what* and *where* (it's excellent at exposing overlap and stranded value). Do **not** read its coverage % as adaptation — weekly volume, progressive overload, and minimum effective dose live outside it. Both reviewers were emphatic on this.
