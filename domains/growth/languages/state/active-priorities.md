# Languages Sub-Domain Active Priorities

## Current Focus

### Cantonese — CantonesePlus V3.1 Rebuild
- **Status:** Active — Phase 1 of 4 complete
- **What:** Rebuilding cantoneseplus.com as a self-adaptive Cantonese learning platform
- **Revenue:** ~$30 USD/month (current V2)
- **Editors:** 2 active (older Cantonese speakers)
- **Tech:** .NET 8 + Dapper + MySQL (API), SvelteKit + TypeScript + TailwindCSS (frontend)
- **Repo:** github.com/Sc07713/CantonesePlusV3, branch `feature/v3.1-self-adaptive`
- **Corpus:** 8,111 characters, 218,409 words, 116,942 sentences — 3.6x Cantodict
- **Phase 1 done (2026-04-04):** DB migrations, frequency-ranked search, tone colouring, sentence decomposition, Jyutping/Yale toggle, retired filtering. 13 commits, 36 tests passing.
- **Phase 2 next:** Auth, user registration, vocabulary tracking, adaptive suggestions, report buttons
- **Phase 3:** Editor tools (AI draft queue, report queue, corpus gaps dashboard)
- **Phase 4:** AI batch pipeline (local machine, Claude Max, SSH tunnel to HK server)
- **Design spec:** `docs/superpowers/specs/2026-04-03-cantoneseplus-v3.1-design.md`
- **Implementation plan:** `docs/superpowers/plans/2026-04-04-cantoneseplus-v3.1-implementation.md`

## Queued

- Mandarin, Korean, Spanish, Japanese — status TBD. Likely aspirational until Cantonese is systematic.

## Blocked

- Cantonese speaking practice — no structured immersion. Passive family exposure only.
