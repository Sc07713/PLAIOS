# Implementation Review Bundle — PLAIOS Multi-Agent Procedure

**Date:** 2026-05-06
**Author:** Claude (in-session with Scott McKennie)
**Reviewers requested:** Codex (adversarial) + Gemini (long-context / pattern cross-check)
**Convergence target:** ratify these files for shipping, OR identify specific changes required before they ship.

---

## What you (the reviewer) need to know

The earlier design review (`00-design-bundle.md` in this folder, plus `01-codex-review.md` and `01-gemini-review.md`) ratified a design. This bundle contains the **actual implementation** drafted from that design. Your job is to check the implementation against the spec and against the goals the design promised — particularly:

1. **Cold-start readability:** can a fresh agent (Claude / Codex / Gemini) land in `D:\PLAIOS\` with no prior context, read `AGENTS.md` alone, and correctly understand its role, the rules, and what's allowed in a bundle?
2. **KISS / irreducible complexity:** is anything load-bearing missing? is anything over-engineered? could a section be cut without loss?
3. **Convergence-readiness:** does the procedure document make it clear that *every investigation is supposed to converge on a binding outcome*, not produce balanced dialogue?
4. **Match to spec:** does what was implemented match what was designed in `docs/superpowers/specs/2026-05-06-plaios-multi-agent-design.md`? Any silent drift?
5. **Privacy threat model:** does the privacy section accurately describe vendor-hosted exposure (OpenAI/Google), and does the Tier B/D rule survive contact with the insurance audit use case?

**Privacy of this bundle:** No personal financial / medical / family data. Privacy tier B trivially satisfied.

**Reviewer convergence rules:** if you find a blocking issue, mark it `block`. If you find a serious issue, mark it `serious`. If both reviewers mark the same thing block/serious, the orchestrator integrates the fix before shipping. If only one marks it serious and the other says it's fine, the orchestrator decides. **Convergence on a ship/no-ship outcome is the goal.**

---

## File 1 — `D:\PLAIOS\AGENTS.md`

```markdown
# AGENTS.md — PLAIOS

**Audience:** any AI agent (Claude, Codex, Gemini, future tools) invoked from this directory.
**Purpose:** describe the project, the rules, and your role in this system, so you can do good work from a cold start.

---

## Project

PLAIOS (Personal Life AI Operating System) is a single-user, markdown-heavy knowledge and decision system at `D:\PLAIOS\`. It exists to surface structural weakness across life domains, prioritise by hierarchy of needs, maintain continuity across AI conversations, and produce durable decisions — not a to-do list.

Owner: Scott McKennie. CEO of an Australian software org. Father of four with a fifth on the way.

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
```

---

## File 2 — `D:\PLAIOS\protocols\multi-agent.md`

[Full content lifted from `protocols/multi-agent.md` — see that file for canonical version. Reviewer should `cat` it from the working directory.]

Key sections to verify:
- "Goal — convergence on a binding outcome" — does this make the convergence requirement obvious?
- "10-phase pattern" — single track, no lite variant, early termination via disposition file (NOT "n/a")
- "Convergence checkpoints" at phase 02, 07, 09 — clear?
- "When NOT to use multi-agent" + OUT override — does the override clause cover the right cases?

---

## File 3 — `D:\PLAIOS\CLAUDE.md` (diff)

The single change is one block added immediately under the title:

```markdown
> **Cross-tool baseline:** project conventions, multi-agent role rules, and privacy/threat-model rules live in `AGENTS.md` at the PLAIOS root — read by Claude Code, Codex CLI, and Gemini CLI alike. The multi-agent procedure (when to invoke, how to bundle, convergence rules) lives at `protocols/multi-agent.md`. **Don't duplicate either here.** This file is for Claude orchestration logic only.
```

All other CLAUDE.md content unchanged.

---

## File 4 — `D:\PLAIOS\bin\new-investigation.ps1`

[Full content in repo. ~60 lines of PowerShell. Creates `journal/investigations/YYYY-MM-DD-<slug>/`, all 24 phase files, plus a seeded `README.md` with phase log.]

Reviewer to verify:
- File list matches the 10-phase pattern in the procedure doc
- README seed includes "Convergence target" field (ties to the convergence principle)
- No assumptions that break on Windows / PowerShell 5.1 (this is the user's primary shell)

---

## Specific questions

### For Codex (adversarial)
1. **Cold-start readability:** if you (Codex) were dropped into `D:\PLAIOS\` with no prior context and only `AGENTS.md` to read, would you correctly understand what's allowed in a bundle, your role, and how to converge with the other agents? What's missing or ambiguous?
2. **KISS / cuts:** is anything in the four files non-load-bearing — could be cut without loss of meaning?
3. **Match-to-spec:** the spec is at `D:\PLAIOS\docs\superpowers\specs\2026-05-06-plaios-multi-agent-design.md`. Any silent drift between spec and implementation?
4. **Privacy section vs insurance audit:** does the Tier B + D Health/Family rule survive contact with the upcoming insurance audit (concrete numbers, ages, mat-leave timing, underwriting maths)? Any obvious hole?
5. **Convergence framing:** is "convergence over dialogue" landed in BOTH AGENTS.md and protocols/multi-agent.md, or is it only in one place?
6. **Self-reference loop:** the spec was reviewed (one-shot) and now the implementation is being reviewed (this pass). After this, the procedure ships and gets used on the insurance audit. Is anything in the procedure undermining its own use, or creating circular dependencies?

### For Gemini (long-context / pattern)
1. **Does AGENTS.md actually describe what it claims to describe?** Test by reading it cold and asking yourself: "do I know the project, my role, the rules, and where to find more?" If yes, ship; if no, what's the specific gap?
2. **Does the procedure converge?** Read `protocols/multi-agent.md` and trace what happens for an insurance audit (durable, cross-domain, irreversible). Does the procedure clearly drive toward a binding outcome, or could a real run go sideways into "balanced perspectives" mode?
3. **Cross-temporal coherence:** PLAIOS already has `protocols/decision-record-template.md`, `protocols/session-checklist.md`, `protocols/assessment-template.md`. Does the new `protocols/multi-agent.md` integrate cleanly, or contradict/duplicate any of them?
4. **Pattern cross-check:** how do other personal knowledge / decision systems (Obsidian / Roam / Tana with AI integrations, personal Zettelkastens) handle multi-tool agent invocation? Is the AGENTS.md + per-tool extension pattern emerging as canonical, or is there a better-known pattern this should align with?
5. **One-pass simplicity:** is there a simpler shape that achieves 80% of this with 50% of the surface area? KISS lens.

---

## Response format

```
# Implementation Review

## Material concerns
[numbered, each with: concern, file:line if specific, severity (block / serious / minor), suggested fix]

## Things that are fine
[bullet list — short]

## Things you'd do differently but could go either way
[bullet list — short]

## Ship verdict
[ship / ship-after-fixes / no-ship — with one-sentence rationale]
```

The orchestrator will integrate concerns where reviewers converge. Where they don't converge, orchestrator decides and records the disagreement. **Goal: ship/no-ship convergence.**
