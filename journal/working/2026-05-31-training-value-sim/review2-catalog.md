# Catalog validation — Codex + Gemini (2026-05-31)

## Convergent (binding)
- **K=6 for all non-hypertrophy sub-dims is indefensible** (both). Per-quality K:
  | quality | reconciled K | source |
  |---|--:|---|
  | vo2 | 11 | Codex 8-12, Gemini 12 |
  | conditioning | 9 | Codex 8-10 |
  | strength | 6 | Codex 5-8, Gemini ~6 |
  | power/speed | 4 | Codex 3-5 (quality saturates fast) |
  | cod/contact | 5 | Codex 4-6 |
  | skill | 16 | Codex 10-15, Gemini 24 (absorbs lots of volume; must NOT "solve" in one session) |
  | mobility (ankle/hip/tspine/adductor) | 5 | Codex 3-5, Gemini ~5 |
  | resilience | 6 | Codex 4-7, "no single clean K" — coarse bucket, flagged |
- **`resilience` is an overused catch-all** (both) — face pull/jumps/ladder/Pallof/calf/Copenhagen/carry all paid through it → inflates prehab ranks.
- **`power` over-dosed on slow strength lifts** (Codex): Bulgarian SS .16→.06, SL-RDL .06→.02.
- **`contact` over-broad** (both): chin/pull .10→.03, skills .06→.02, face pull →0; carry stays the one high-contact lift (.20→.14 compromise).
- **chin-up arms inflated** (both) .22→.15; **carry arms** .06→.01 (Codex).
- **4×4 vo2 under-credited** (Codex) .30→.38; **Zone-2 vo2** .18→.12.
- **decel cod** .40→.25 (Codex, ladder ≠ reactive COD); **ATG strength** .10→.16; **sprints vo2** .06→.02.
- **Missing top-10:** Dips (Gemini — chest_upper/arms/delts/strength); weighted-chin = loaded variant of chin-ups (progression note, not new line).
- **Goal dilution** (both): A has 4 sub-dims, B has 6 → an A-dose point ≈ 1.5× a B-dose point. The solo leaderboard is therefore aesthetics-biased BY CONSTRUCTION; basketball is protected by floors + fixed game/court time, not by leaderboard rank. (Confirms the skill-under-served flag already raised.)

## Applied
Per-quality K in the engine (test-first); the dose corrections above; added Dips.
Resilience coarseness logged as a known limitation (would need splitting into tendon/tissue
vs trunk-bracing to fully fix — deferred, not worth the sub-dim sprawl now).
