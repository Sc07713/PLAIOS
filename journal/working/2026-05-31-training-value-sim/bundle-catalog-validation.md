---
Tier: B
---

# Evidence bundle — validate the Stage-1 exercise catalog (dose values)

## Athlete
38M, recreational basketball, time-capped (~3 fixed strength + 3 reward + basketball/wk).
~1 month post respiratory infection + a fasting block → deconditioned, criteria-gated
re-entry ramp (no max plyo/sprints yet). Equipment: adjustable DBs to 21 kg, KBs to 24 kg,
flat+incline bench, plyo box, bike, treadmill, HR strap, band/anchor. No barbell/machines/cables.

## What the model does
Stage 1 of a growth-optimiser. Each exercise delivers a per-training-minute DOSE to goal
sub-dimensions. Doses accumulate weekly; a CONCAVE 12-week growth curve converts dose→growth
(hypertrophy curve for aesthetics sub-dims with a junk-volume penalty past ~22 sets/muscle/wk;
generic saturating curve for the rest). Goals are weighted **Aesthetics 40 / Longevity 20 /
Basketball 20 / Mobility 20**. The engine is unit-tested; THESE DOSE VALUES are the unreviewed,
load-bearing input.

Sub-dimensions: A = delts, back, arms, chest_upper (× exogenous leanness). L = vo2, strength,
resilience. B = power, speed, cod, conditioning, skill, contact. M = ankle, hip, tspine, adductor.

## Dose conventions (per training-minute, incl. setup/rest)
- Aesthetics sub-dims: EFFECTIVE SETS per minute (~0.4 if a hard set fully targets that muscle, a set ~2.5 min; scaled by how much of the muscle the lift hits).
- All other sub-dims: generic stimulus units/min, calibrated so a full session lands a sane dose against a saturation constant K=6.

## The draft catalog (per-exercise dose_per_min) — PRESSURE-TEST THIS
```
Chin-ups           back .30  arms .22  strength .18  contact .10
Pull-ups           back .34  arms .12  strength .18  contact .10
DB Row             back .32  arms .08  strength .16  contact .16  resilience .06
Loaded carry       strength .14  resilience .18  arms .06  contact .20  conditioning .10  hip .04
Face pull          back .12  resilience .16  contact .05
Incline DB press   chest_upper .34  delts .10  arms .14  strength .14
Lateral raise      delts .40
Overhead press     delts .22  arms .10  strength .14  chest_upper .06
Triceps/curls      arms .38
Pullover           back .14  chest_upper .14
Bulgarian split sq strength .24  power .16  resilience .10  hip .10  contact .08
Single-leg RDL     strength .18  resilience .16  hip .10  power .06
ATG split squat    strength .10  hip .18  ankle .18  resilience .12
Cossack/lat lunge  hip .16  adductor .20  ankle .08  resilience .08
Jumps/plyo         power .40  speed .10  resilience .10  cod .10  ankle .10
Accel sprints      speed .40  power .18  conditioning .12  vo2 .06
Decel ladder       cod .40  resilience .18  ankle .10  contact .06
4x4 intervals      vo2 .30  conditioning .22
Zone-2             vo2 .18  conditioning .10  resilience .04
Soleus/calf        resilience .34  ankle .16
Copenhagen         resilience .22  adductor .30
Pallof/anti-rot    resilience .14  contact .20  tspine .12
T-spine/hip mob    tspine .34  hip .18  ankle .06
Skills (shoot/etc) skill .40  contact .06
```

## Leaderboard this produced (weighted 12-wk growth/min, solo)
1 Incline press 9.66 · 2 Chin-ups 9.60 · 3 Pull-ups 8.70 · 4 DB Row 8.65 · 5 OHP 7.12 ·
6 Loaded carry 5.98 · 7 Bulgarian SS 5.32 · 8 Lateral raise 5.17 · 9 Triceps/curls 4.97 ·
10 ATG split squat 4.94 · 11 Decel 4.60 · 12 Jumps 4.58 · 13 SL-RDL 4.48 · 14 Pullover 4.26 ·
15 Soleus 4.24 · 16 Copenhagen 4.18 · 17 Cossack 4.14 · 18 T-spine mob 4.09 · 19 Sprints 3.87 ·
20 4x4 3.81 · 21 Face pull 3.72 · 22 Pallof 3.32 · 23 Zone-2 2.73 · 24 Skills 2.04

## What I need from you (terse, adversarial — do NOT redesign the program)
1. Flag any dose value miscalibrated enough to change rank order. Cite exercise + sub-dim + corrected value + one-line mechanism.
2. Systematic biases: is any sub-dim over/under-dosed across the catalog? (e.g. is "strength" under-credited on compounds? is "resilience" doing too much work as a catch-all? are mobility sub-dims double-paid?)
3. Calibration: is a single K=6 saturation for ALL non-hypertrophy sub-dims defensible, or do strength / vo2 / skill / mobility genuinely saturate at different rates? If different, give rough relative K.
4. Missing exercise that would plausibly crack the top 10 on these weights (aesthetics-led).
5. Anything that makes the leaderboard order untrustworthy.
Tag <85% confidence. No padding, no flattery. If a value is fine, say nothing.
