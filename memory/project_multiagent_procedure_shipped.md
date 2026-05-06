---
name: Multi-agent procedure shipped to PLAIOS
description: AGENTS.md + protocols/multi-agent.md + scaffold script live as of 2026-05-06; insurance audit is the validating run, deferred to next session
type: project
originSessionId: f0a76a67-abdf-4eac-9c7f-8adfdb74b91c
---
PLAIOS now has the multi-agent development procedure live. Roles: Claude = driver, Codex (`codex exec`) = adversarial reviewer at risk points, Gemini (`gemini --skip-trust -p`) = long-context / external-pattern channel.

Files shipped:
- `D:\PLAIOS\AGENTS.md` — cross-tool baseline; auto-loaded by Codex/Gemini/Claude when invoked from PLAIOS root
- `D:\PLAIOS\protocols\multi-agent.md` — the recipe (lifted core from RAIOS) + PLAIOS overlay (trigger rules, privacy, convergence)
- `D:\PLAIOS\bin\new-investigation.ps1` — folder scaffold; run from PLAIOS root with a `[a-z0-9-]+` slug
- `D:\PLAIOS\CLAUDE.md` — added a 1-line pointer to AGENTS.md; existing content untouched
- `D:\PLAIOS\protocols\decision-record-template.md` — extended with link slot to `10-final-output.md`

Design spec: `docs/superpowers/specs/2026-05-06-plaios-multi-agent-design.md`. Two rounds of Codex+Gemini review captured under `journal/investigations/2026-05-06-multi-agent-procedure-design/` (design bundle 00, design reviews 01-codex/01-gemini, implementation bundle 02, implementation reviews 03-codex/03-gemini).

**Why:** Procedure adoption is a durable workflow change. Investigations now have a single 10-phase pattern that converges on a binding outcome (decision record + full investigation record).

**How to apply:**
- For durable, consequential, or irreversible decisions in life domains: point user to `protocols/multi-agent.md`.
- For investigation-style work: bootstrap with `.\bin\new-investigation.ps1 -Slug '<topic>'` from PLAIOS root.
- Trigger rules + privacy tier rules + convergence framing are in `AGENTS.md`. Read it before any cross-tool invocation.
- The kickoff prompt for the insurance audit (the validating run) is at `D:\PLAIOS\journal\next-session-insurance-audit-kickoff.md`.

`/investigate` skill v2 is deferred — built only after the manual workflow earns it on a real investigation.
