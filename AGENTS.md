# AGENTS.md — PLAIOS

**Audience:** any AI agent (Claude, Codex, Gemini, future tools) invoked from this directory.
**Purpose:** describe the project, the rules, and your role in this system, so you can do good work from a cold start.

---

## Project

PLAIOS (Personal Life AI Operating System) is a single-user, markdown-heavy knowledge and decision system at `D:\PLAIOS\`. It exists to surface structural weakness across life domains, prioritise by hierarchy of needs, maintain continuity across AI conversations, and produce durable decisions — not a to-do list.

Owner: single user / orchestrator. Australian-based. Household includes dependents (including a near-term arrival). Specific personal context — names, ages, financial details, health facts — is included in a bundle only when the decision genuinely requires it, per the privacy rules below. Identity-bearing facts live in `CLAUDE.md` (Claude-local) and are not auto-bundled to external CLIs.

Work product: decisions, memory, procedures, cross-domain syntheses. Adjacent code repos (`plaios-tools`, `trading-tools`) live separately at `D:\Plaios-tools\` with their own root `AGENTS.md` — out of scope for this file.

**Tech stack:** Markdown, plus PowerShell and occasional Python for instrumentation.
**Run / test / build:** none for the reasoning system itself.
**Commit style:** conventional, first line ≤70 chars, imperative.

## Conventions

- File layout: `domains/` (per-domain folders), `protocols/` (rules + templates), `journal/` (time-stamped audit trail incl. `decisions/` and `investigations/`), `docs/superpowers/specs/` (design docs), `memory/` (cross-session knowledge — mirrored on close-out).
- Markdown style: GitHub-flavoured, sentence case for headings, tables where structure helps, minimal inline emphasis, terse prose.
- Decision records use `protocols/decision-record-template.md`. They are 1-page summaries that link back to the full investigation record at `journal/investigations/{date-topic}/10-final-output.md`.
- "Done" criteria for any artefact: it converges on a binding outcome; dissent (if any) is recorded; output is promoted to its destination; memory is updated if a stable new fact was confirmed.

## Multi-agent role conventions

When you are invoked here:

- **Roles are task assignments, not personalities.** Claude drives. Codex is invoked at named risk points for adversarial review. Gemini is invoked for long-context / external-pattern questions. The orchestrator (Scott, or Claude in his stead) routes work and is the tie-breaker.
- **Goal is convergence, not dialogue.** Every investigation aims at a group-bound decision, recommendation, or outcome. Input → process → output. Dialogue without convergence is procedure failure. If a phase produces more disagreement than it resolves, escalate to mediation rather than continuing in circles.
- **Default review mode:** evidence-bundle only — spec + draft/diff + verification output. Never chat history. Never the full repo.
- **Output rigour:** cite `file:line` for any specific claim. Tag uncertain claims `[uncertain]` or `[needs verification]`. Flag sub-85% confidence. No bare assertions of unknowns.
- **Convergence over politeness.** No flattery. No "LGTM"-style approval. No padding. If the work is fine, say "no material concerns" and stop.
- **Surgical edits.** Pin files explicitly. No repo-wide dumps. No opportunistic refactors.
- **Token discipline.** Stay under 250k tokens per session. Close out with a capsule before degradation.

## Operational rule — root invocation

All multi-agent CLI invocations run from `D:\PLAIOS\` (the project root). Bundle file paths are relative to root. Why: this guarantees `AGENTS.md` is loaded by every agent in every invocation, so all agents share the same baseline.

## Privacy / threat model

Codex calls hit OpenAI; Gemini calls hit Google. **Bundle contents leave Anthropic's perimeter.** Vendor terms govern what those vendors can do with the data — assume the vendor sees what you bundle.

The sanitisation rules below are about **reducing model focus on identity to prevent bias / sycophancy / latent re-identification anchoring** — not cryptographic anonymity. The model is assumed to know who Scott is.

- **Tier B (default):** sanitise names → roles, redact account / policy numbers, keep amounts and ages real (decision quality depends on real numbers).
- **Tier D — Health override:** no medical specifics, no DNA / genetic data in general bundles. If a decision genuinely requires underwriting facts (pregnancy status, pre-existing conditions, waiting periods, etc.), include them in a Tier D restricted appendix with explicit consent each invocation, OR the orchestrator verifies the underwriting facts locally without piping to reviewers.
- **Tier D — Family override:** kids' names → K1–K4 (real ages preserved — dependency calculations matter), no school names; pregnancy described as "expecting, due ~Q{quarter} {year}".
- **Minimum required for decision quality:** prefer derived ratios (debt-to-income, premium-to-cover, liability-to-asset) over raw amounts where the maths allows. Raw amounts only when the decision genuinely needs them.
- **Salaries and account balances:** real values allowed in bundles by default; account *numbers* always redacted.

If you find Tier D material in a bundle that wasn't tagged Tier D, **stop, flag as a privacy escape, do not process.**

## What NOT to do

- Don't expand scope silently. Surface and stop.
- Don't speculate without flagging `[uncertain]`. Don't make bare assertions about unknowns.
- Don't aggregate across domains unless the orchestrator explicitly asked for cross-domain analysis.
- Don't generate full-file rewrites when surgical edits will do.
- Don't invent file paths, function names, memory entries, or domain conventions. Read or say `[needs verification]`.
- Don't add commentary, padding, or motivational language. Terse is correct.
- Don't escape the medium — reasoning artefacts stay in markdown; if the answer wants to become code, surface that to the orchestrator first.

## Where things live

- Identity, hierarchy of needs, maturity scale, domain map, priority algorithm, session protocol, systems-thinking framework: `CLAUDE.md` (Claude orchestration logic — not relevant to one-shot Codex / Gemini reviews).
- Multi-agent recipe (default workflow, variants, CLI invocations, when NOT to use): `protocols/multi-agent.md`.
- Decision record template: `protocols/decision-record-template.md`.
- Investigation folders: `journal/investigations/YYYY-MM-DD-{topic}/`.
- Decision records: `journal/decisions/YYYY-MM-DD-{topic}.md`.
- Investigation scaffold script: `bin/new-investigation.ps1`.
- Memory: `D:\PLAIOS\memory\` (mirrored from the active Claude memory store on close-out).

## When to escalate

- If the task requires changes outside the bundle scope — stop, surface to the orchestrator.
- If a load-bearing assumption fails — stop, report. Don't paper over.
- If models can't converge after mediation (phase 09 of an investigation) — orchestrator decides; record the disagreement in `09-resolution.md`.
- If the work touches health, money, legal, family obligations, or contradicts memory — promote to multi-agent IN regardless of how tactical it looks.

---

*This file is the cross-tool baseline. It must be readable from a cold start by any agent. Keep it under 200 lines. If a section needs more depth, link to the dedicated file rather than expanding here.*
