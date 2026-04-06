# Languages Sub-Domain Active Priorities

## Current Focus

### Cantonese — CantonesePlus V3.1 Rebuild
- **Status:** Active — All 4 phases complete, local testing done, bug fixing phase
- **What:** Rebuilding cantoneseplus.com as a self-adaptive Cantonese learning platform
- **Revenue:** ~$30 USD/month (current V2)
- **Editors:** 2 active (older Cantonese speakers)
- **Tech:** .NET 8 + Dapper + MySQL (API), SvelteKit + TypeScript + TailwindCSS (frontend), AiBatch console app
- **Repo:** github.com/Sc07713/CantonesePlusV3, branch `feature/v3.1-self-adaptive`
- **Corpus:** 8,111 characters, 218,409 words, 116,942 sentences — 3.6x Cantodict
- **Phase 1 done (2026-04-04):** Search, tone colouring, frequency, detail pages. 13 commits, 36 tests.
- **Phase 2 done (2026-04-06):** Auth, user registration, admin user management (list/reset pwd/suspend), vocabulary tracking, activity logging, reports. 70 tests.
- **Phase 3 done (2026-04-06):** Editor tools — draft queue, report queue, corpus gaps dashboard. 79 tests.
- **Phase 4 done (2026-04-06):** AI batch pipeline (corpus gaps, learning engine, report triager), integration tests, CLAUDE.md updated.
- **Next:** Bug fixing — 6 issues filed on GitHub (search ranking, English search precision, admin login UX, migration runner, deployment, default password)
- **Design spec:** `docs/superpowers/specs/2026-04-03-cantoneseplus-v3.1-design.md`
- **Implementation plan:** `docs/superpowers/plans/2026-04-04-cantoneseplus-v3.1-implementation.md`

## Queued

- Mandarin, Korean, Spanish, Japanese — status TBD. Likely aspirational until Cantonese is systematic.

## Blocked

- Cantonese speaking practice — no structured immersion. Passive family exposure only.
