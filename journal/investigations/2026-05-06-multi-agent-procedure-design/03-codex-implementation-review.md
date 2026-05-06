OpenAI Codex v0.128.0 (research preview)
--------
workdir: D:\PLAIOS
model: gpt-5.5
provider: openai
approval: never
sandbox: read-only
reasoning effort: none
reasoning summaries: none
session id: 019dfc94-f45a-7333-b417-056526fb8d99
--------
user
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

codex
I’ll verify the canonical files rather than relying on the pasted bundle, then compare the implementation against the design spec and the supporting protocols where they matter.
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'Get-Content -Path AGENTS.md | ForEach-Object -Begin {$i=1} -Process {"$i`t$_"; $i++}' in D:\PLAIOS
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -Path protocols\\multi-agent.md | ForEach-Object -Begin {"'$i=1} -Process {"$i`t$_"; $i++}' in D:\PLAIOS
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -Path docs\\superpowers\\specs\\2026-05-06-plaios-multi-agent-design.md | ForEach-Object -Begin {"'$i=1} -Process {"$i`t$_"; $i++}' in D:\PLAIOS
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -Path bin\\new-investigation.ps1 | ForEach-Object -Begin {"'$i=1} -Process {"$i`t$_"; $i++}' in D:\PLAIOS
2026-05-06T09:18:43.615726Z ERROR codex_core::tools::router: error=`"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'Get-Content -Path AGENTS.md | ForEach-Object -Begin {$i=1} -Process {"$i`t$_"; $i++}'` rejected: blocked by policy
 declined in 0ms:
`"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'Get-Content -Path AGENTS.md | ForEach-Object -Begin {$i=1} -Process {"$i`t$_"; $i++}'` rejected: blocked by policy
 declined in 0ms:
`"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -Path protocols\\multi-agent.md | ForEach-Object -Begin {"'$i=1} -Process {"$i`t$_"; $i++}'` rejected: blocked by policy
2026-05-06T09:18:43.619348Z ERROR codex_core::tools::router: error=`"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -Path protocols\\multi-agent.md | ForEach-Object -Begin {"'$i=1} -Process {"$i`t$_"; $i++}'` rejected: blocked by policy
2026-05-06T09:18:43.623263Z ERROR codex_core::tools::router: error=`"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -Path docs\\superpowers\\specs\\2026-05-06-plaios-multi-agent-design.md | ForEach-Object -Begin {"'$i=1} -Process {"$i`t$_"; $i++}'` rejected: blocked by policy
 declined in 0ms:
`"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -Path docs\\superpowers\\specs\\2026-05-06-plaios-multi-agent-design.md | ForEach-Object -Begin {"'$i=1} -Process {"$i`t$_"; $i++}'` rejected: blocked by policy
 declined in 0ms:
`"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -Path bin\\new-investigation.ps1 | ForEach-Object -Begin {"'$i=1} -Process {"$i`t$_"; $i++}'` rejected: blocked by policy
2026-05-06T09:18:43.626897Z ERROR codex_core::tools::router: error=`"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -Path bin\\new-investigation.ps1 | ForEach-Object -Begin {"'$i=1} -Process {"$i`t$_"; $i++}'` rejected: blocked by policy
codex
The first read attempt hit the command policy wrapper on quoting. I’m switching to simpler file reads and will add line references from the numbered content where available.
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'Get-Content AGENTS.md' in D:\PLAIOS
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content docs\\superpowers\\specs\\2026-05-06-plaios-multi-agent-design.md" in D:\PLAIOS
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content protocols\\multi-agent.md" in D:\PLAIOS
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content bin\\new-investigation.ps1" in D:\PLAIOS
 succeeded in 619ms:
# Multi-Agent Procedure for PLAIOS

**Source:** core lifted from `D:\RAIOS-outputs\investigations\multi-agent-dev-practices-20260505-2237\10-final-recipe.md` (3-model ratified). PLAIOS overlay added at the bottom.

**Read this when:** you're about to make a durable decision, change a procedure, update memory in ways that contradict prior memory, or run an investigation. See "When NOT to use" if you're not sure.

---

## Goal ƒ?" convergence on a binding outcome

Every investigation through this procedure produces a **group-bound decision, recommendation, or outcome** ƒ?" not a balanced essay, not a perspectives roundup. The structure is:

**Input ƒ+' process ƒ+' output.**

- **Input:** topic + spec + evidence
- **Process:** independent research, parallel deliberation, mediated reconciliation
- **Output:** one binding artefact, with dissent recorded but not sovereign

The orchestrator (Scott, or Claude in his stead) is always the tie-breaker. Disagreement is recorded; it is never the deliverable. **Dialogue without convergence is procedure failure.**

---

## Where each model fits

| Model | Role | Why |
|---|---|---|
| **Claude** (Claude Code) | Driver. Holds the session, drafts artefacts, runs verification, narrates. | Native sub-agents, plan mode, file pinning, agentic loops, MCP access. |
| **Codex** (`codex exec`) | Adversarial reviewer. Invoked on demand. | Different model, different blind spots ƒ?" catches what same-model review misses. |
| **Gemini** (`gemini --skip-trust -p`) | Long-context / external-pattern channel. Invoked on demand. | Long context window, different training ƒ?" useful for "is this how it's done elsewhere?" or "does this match prior decisions?" |

Each model runs in its own context window. They never talk to each other. **The orchestrator passes artefacts between them via CLI.**

## The default workflow (any task more than a one-line edit)

1. **Plan** in Claude Code. Hand it: objective, files, constraints, non-goals, what convergence looks like. Ratify the plan before any artefact is drafted.
2. **Draft** in Claude Code. Surgical edits only. Files pinned. No repo-wide dumps. No opportunistic refactors.
3. **Verify** in Claude Code. Run any checks, tests, or repro scripts inside the session.
4. **Review** ƒ?" pick the channel by risk:

   | Risk | Reviewer | Why |
   |---|---|---|
   | Routine | Claude Code reviewer sub-agent (sees only spec + draft + verify output) | Cheap, in-session |
   | Risky / cross-domain / consequential | **Codex** | Independent model ƒ?" catches what Claude missed |
   | "Is this how it's done elsewhere?" / pattern question | **Gemini** | Long context + external pattern view |

   The reviewer sees only the evidence bundle. Never the chat history. Never the full repo.

5. **Narrate & commit.** State in the commit message *why* the accepted outcome is correct, in your own words. No "LGTM"-style merges.
6. **Close out** when the session approaches 200ƒ?"250k tokens or spans days. Write a capsule: objective, decision, files changed, checks run, unresolved risks, exact next step.

## CLI invocations

**All multi-agent invocations run from `D:\PLAIOS\` (the project root)**, so `AGENTS.md` is loaded automatically by every CLI.

### Codex (adversarial review)

```bash
# build the evidence bundle (no chat history)
cat spec.md draft.md verify-output.md > bundle.md

# pipe via stdin (NOT positional argument ƒ?" that pattern hangs)
codex exec - < bundle.md
```

### Gemini (long-context / pattern question)

```bash
gemini --skip-trust -p "$(cat <<'EOF'
Question: [your specific question]
Context: [paste relevant content or reference paths]
EOF
)"
```

### Claude Code

Open in `D:\PLAIOS\`. The CLI auto-loads `AGENTS.md` and `CLAUDE.md` from the working directory.

## Variant ƒ?" investigation (durable, consequential, irreversible)

For decisions where rollback cost exceeds the deliberation cost. **This is the variant that converges to a group-bound outcome.** Output is a decision record (and possibly a procedure / recommendation), never a diff alone.

**Folder:** `journal/investigations/YYYY-MM-DD-{topic}/`. Bootstrap with `bin/new-investigation.ps1 <topic-slug>`.

### 10-phase pattern (single track ƒ?" no "lite" variant)

```
README.md  (current phase, status, last-touched, convergence target)
00-topic.md
01-questions-{claude,codex,gemini}.md
02-consolidated-questions.md
03-spec.md
04-research-{claude,codex,gemini}.md
05-research-pack.md
06-deliberation-{claude,codex,gemini}.md  +  06-deliberation.md
07-disposition.md
08-meta-reflection-{claude,codex,gemini}.md  +  08-meta-reflection.md
09-mediation-{claude,codex,gemini}.md  +  09-resolution.md
10-final-output.md  (full investigation record)
```

### Convergence checkpoints

- **Phase 02:** orchestrator answers consolidated questions. Convergence on *what's being decided*.
- **Phase 07:** disposition declares the binding outcome (or early termination if research was conclusive).
- **Phase 09:** if disagreement remains after disposition, models mediate; resolution is binding. Orchestrator decides if mediation can't converge.

### Early termination

If research (phase 04) is conclusive and no deliberation is warranted, `07-disposition.md` says: *"Closed at phase N: <reason>. No deliberation/mediation needed."* Phases past termination are **omitted** OR explicitly marked *"Not reached. Investigation closed at phase N ƒ?" see 07-disposition.md."* Never use "n/a" ƒ?" that creates a misleading audit trail.

### Output destinations

- **1-page summary** at `journal/decisions/YYYY-MM-DD-{topic}.md` (using `protocols/decision-record-template.md`), with a link back to the full record
- **Full record** at `10-final-output.md`: alternatives considered, evidence used, dissent noted, privacy tier applied, follow-up tasks
- **Procedural outcome** (if the investigation produced a procedure or skill spec): promoted to `protocols/` or `docs/superpowers/specs/`
- **Memory updates** flowing from the decision: handled by the close-out skill

## Variant ƒ?" bug fix

For PLAIOS this applies to `plaios-tools` / `trading-tools` code repos. Those use this variant directly via their own repo-local `AGENTS.md` ƒ?" no PLAIOS overlay. Reasoning-domain bugs (memory contradictions, decision-record errors) use the investigation variant above instead.

1. **Reproduce first.** Either Claude Code or Codex writes a *failing test* that demonstrates the bug. Run it. **No fix is permitted until this test exists and fails.**
2. **Fix in Claude Code.** Surgical patch. Test now passes.
3. **Adversarial review with Codex.** Bundle = spec + diff + test output.
4. **Narrate & commit.**

## Token discipline

Each model session stays under ~250k tokens by design. **No model ever holds the whole picture** ƒ?" small, curated artefacts pass between them. Full repo dumps are forbidden. If a session approaches the ceiling, close it out and start fresh.

## When NOT to use multi-agent

- One-line edits ƒ?" just write it.
- Tasks under 30 minutes ƒ?" overhead exceeds gain.
- Pure exploration ƒ?" single Claude Code session, no review channel.
- Routine state reads, daily journal lines, ephemeral memory updates that don't contradict prior memories.
- Tactical PocketSmith tweaks, calendar events, gmail drafts.

### OUT override

The OUT list applies *unless* the artefact:
- Creates an external commitment (Gmail to insurer / lawyer / doctor / lender)
- Changes a durable model (PocketSmith budget structure, not just an event amount)
- Affects money / legal / health / family obligations
- Contradicts prior memory

In any of those cases, promote to IN.

---

## PLAIOS overlay

### Trigger rules ƒ?" multi-agent IN

- Durable decisions in life domains (insurance, schools, property, fertility / baby planning, vendor switches, debt restructure, household-level rules)
- Cross-domain syntheses ("where am I structurally weak?")
- Memory updates that contradict prior memories
- Skill / procedure design changes
- Code work in `plaios-tools` / `trading-tools` (use this recipe directly via repo-local `AGENTS.md`; no overlay needed for code work)

### Privacy / threat model

See `AGENTS.md` "Privacy / threat model" section. Summary: B default + D Health/Family overrides + minimum-required clause. Codex and Gemini are vendor-hosted (OpenAI, Google); bundle contents leave Anthropic's perimeter.

### When in doubt

If you're unsure whether something belongs in IN or OUT: default IN if it's durable and irreversible; default OUT if it's tactical and reversible. The override clauses handle edge cases.

### Wall-clock soft cap

If a single phase exceeds ~2 hours, escalate or rethink scope. The procedure should not become its own time sink.
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

 succeeded in 641ms:
# PLAIOS Multi-Agent Development Procedure ƒ?" Design Spec

**Date:** 2026-05-06
**Author:** Claude (in-session with Scott McKennie)
**Reviewers:** Codex (adversarial) + Gemini (long-context / pattern cross-check) ƒ?" see `journal/investigations/2026-05-06-multi-agent-procedure-design/`
**Status:** Spec ƒ?" ready for user review prior to implementation planning.

---

## 1. Purpose

Adopt the multi-agent development recipe that was 3-model-ratified for ICX (`D:\RAIOS-outputs\investigations\multi-agent-dev-practices-20260505-2237\`) inside PLAIOS, where the work product is mostly non-code reasoning (decisions, memory, procedures, cross-domain syntheses). Validate the adaptation by running it on a real durable decision (insurance audit) before considering skill automation.

## 2. Approach ƒ?" "Core + PLAIOS overlay"

Lift the load-bearing parts of the source recipe verbatim ƒ?" CLI invocations, 10-phase investigation structure, evidence-bundle context firewall, token discipline, default workflow, variants. Layer PLAIOS-specifics on top: trigger rules for life-domain artefacts, privacy/threat-model rules, output destinations, investigation folder placement.

**Rejected:** immediate/faithful port with no overlay ƒ?" loses PLAIOS-specific framing (life-domain trigger rules, vendor-hosted privacy threat model).

**Considered but not chosen:** PLAIOS-tailored from scratch ƒ?" doubles work, risks drift from the recipe Scott uses at ICX. Kept the simpler "core + overlay" path.

## 2a. Procedure goal ƒ?" convergence on a binding outcome

Every investigation that runs through this procedure exists to produce a **group-bound decision, recommendation, or outcome** ƒ?" not a balanced essay, not a perspectives roundup. The structure is **input ƒ+' process ƒ+' output**:

- **Input:** topic + spec + evidence
- **Process:** independent research, parallel deliberation, mediated reconciliation
- **Output:** one binding artefact (decision record, procedure, recommendation), with dissent recorded but not sovereign

When the three models converge, the orchestrator (Scott) ratifies and ships. When they don't converge after mediation (phase 09), the orchestrator decides; the disagreement is recorded in `09-resolution.md` so future investigations can learn from it. The orchestrator is always the tie-breaker ƒ?" no 4th-model arbiter.

**Dialogue without convergence is procedure failure.** If a phase produces more disagreement than it resolves, the procedure escalates to mediation rather than continuing in circles.

**Quality property ƒ?" every agent gets it from a cold read.** The procedure document and `AGENTS.md` must each be readable by a model that has zero prior context and still let it understand: who it is in this system, what its role is for this invocation, what's allowed in the bundle, what response shape converges toward an outcome. KISS / irreducible complexity is the *test*, not the *aspiration*.

## 3. File layout

| File / folder | Status | Purpose | Audience |
|---|---|---|---|
| `D:\PLAIOS\AGENTS.md` | NEW | Cross-tool baseline. Project description, conventions, multi-agent role conventions, privacy/threat-model rules, what NOT to do, where things live. Auto-picked-up by Codex CLI, Gemini CLI, and Claude Code. Self-contained for cold-start strangers. | All three CLIs |
| `D:\PLAIOS\CLAUDE.md` | MODIFY (+1 pointer line) | Existing content stays. New line near top: *"For project conventions and multi-agent role rules, see `AGENTS.md` ƒ?" don't duplicate them here."* | Claude Code only |
| `D:\PLAIOS\protocols\multi-agent.md` | NEW | The recipe ƒ?" core lifted from RAIOS `10-final-recipe.md` + PLAIOS overlay. One file, two clearly-delineated sections. | Humans + Claude when planning |
| `D:\PLAIOS\bin\new-investigation.ps1` | NEW | Tiny scaffold: takes `<topic-slug>`, creates `journal/investigations/YYYY-MM-DD-<slug>/` and the empty 00ƒ?"10 files plus `README.md`. ~15 lines. | Humans |
| `D:\PLAIOS\journal\investigations\YYYY-MM-DD-{topic}\` | NEW (per investigation) | Folder-as-state-machine. 10-phase pattern. Includes `README.md` for current-phase / status tracking. | Audit trail |
| `D:\PLAIOS\journal\decisions\` | EXISTING (empty) | 1-page summary decision records, link back to `10-final-output.md` for full context. | Long-term decision log |
| `D:\PLAIOS\.claude\skills\investigate\` | DEFERRED (v2) | `/investigate` skill ƒ?" built only if the manual workflow earns it after at least one real investigation. | Claude Code only |

**Two specific calls:**
- **Recipe is one file.** Core + overlay is a mental model, not a file split.
- **Investigation folders live under `journal/investigations/`** (not a separate `D:\PLAIOS-outputs\` like RAIOS). PLAIOS is private, single-user, one git history.

**Note on adjacent code repos:** `D:\Plaios-tools\trading-tools\` and any future `plaios-tools` repos are **separate git repos**, not nested under PLAIOS. Each will have its own `AGENTS.md` at its repo root. No bleed-through risk; no precedence ambiguity.

## 4. `AGENTS.md` vs `CLAUDE.md` ƒ?" separation of concerns

| Content | Lives in | Why |
|---|---|---|
| Project description (PLAIOS = markdown reasoning system, no build/test/run for most domains) | AGENTS.md | All three CLIs need it |
| Multi-agent role conventions (evidence-bundle only, surgical edits, sub-85% confidence flagged, citations) | AGENTS.md | Codex/Gemini need it; Claude reads it too ƒ?" single source |
| Privacy / threat-model rules (B default + D Health/Family + minimum-required clause + vendor-hosted disclosure) | AGENTS.md | Reviewer must know what's allowed in the bundle |
| Root-invocation rule (CLIs run from `D:\PLAIOS\`) | AGENTS.md | Cross-tool operational rule |
| What NOT to do (no scope creep, no speculative reasoning unflagged, no cross-domain aggregation unasked) | AGENTS.md | Cross-tool baseline |
| Where things live (domain map, journal, protocols, decisions) | AGENTS.md | All tools benefit |
| Identity, hierarchy of needs, maturity scale, priority algorithm, escalation rules, session protocol, systems-thinking framework | CLAUDE.md (existing) | Claude orchestration logic; not relevant to a one-shot Codex review |
| Privacy *principle* ("sensitive requires explicit navigation") | CLAUDE.md (existing) | Claude session-level rule; the *tier policy* lives in AGENTS.md |
| Sub-agent definitions, skill bindings (close-out, future /investigate) | CLAUDE.md | Claude-only |

**Drafting `AGENTS.md`:** start from `D:\RAIOS-outputs\...\12-AGENTS-template.md` as **structure**, not verbatim content. Customise PLAIOS-specific sections. Run a quick adversarial pass (Codex, evidence-bundle = drafted file) before committing.

## 5. `protocols/multi-agent.md` ƒ?" content

### Top half ƒ?" lifted from RAIOS `10-final-recipe.md`
- Where each model fits (Claude=driver, Codex=adversarial reviewer, Gemini=long-context/pattern channel)
- Default workflow: Plan ƒ+' Implement ƒ+' Verify ƒ+' Review (by risk) ƒ+' Narrate ƒ+' Close out
- Bug-fix variant (failing test first, fix, Codex review)
- Decision variant (multi-model deliberation via `/investigate`, no code, output is a decision record)
- CLI invocations (`codex exec - < bundle.md`; `gemini --skip-trust -p ...`)
- Token discipline (250k per session)
- When NOT to do this (one-line edits, <30min tasks, pure exploration)

### Bottom half ƒ?" PLAIOS overlay

**Operational rule:**
- All multi-agent CLI invocations run from `D:\PLAIOS\` (the project root). Bundle file paths are relative to root. Why: ensures `AGENTS.md` is always loaded.

**Trigger rules ƒ?" multi-agent IN:**
- Durable decisions in life domains (insurance, schools, property, fertility/baby planning, vendor switches, debt restructure, household-level rules)
- Cross-domain syntheses ("where am I structurally weak?")
- Memory updates that contradict prior memories
- Skill / procedure design changes
- Code work in `plaios-tools` / `trading-tools` (use RAIOS recipe directly via repo-local `AGENTS.md`)

**Trigger rules ƒ?" multi-agent OUT:**
- Routine state reads, daily journal lines
- Single-domain memory updates that don't contradict anything
- Tactical PocketSmith tweaks, calendar events, gmail drafts
- Anything ephemeral

**OUT override clause:** the OUT list applies *unless* the artefact creates an external commitment (Gmail to insurer/lawyer/doctor/lender), changes a durable model (PocketSmith budget structure, not just an event amount), affects money/legal/health/family obligations, or contradicts memory. In those cases promote to IN.

**Privacy / threat model:**

Reframed per Gemini: sanitisation rules are about **reducing model focus on identity to prevent bias / sycophancy / latent re-identification anchoring** ƒ?" not cryptographic anonymity. Vendor terms (OpenAI for Codex; Google for Gemini) are the actual privacy boundary. Anything bundled and piped out leaves Anthropic's perimeter.

- **Vendor-hosted disclosure** (load-bearing): Codex calls hit OpenAI, Gemini calls hit Google. Bundle contents are subject to those vendors' terms. If the data is bundle-inappropriate even for a friendly vendor (raw medical history, DNA), keep it out and verify locally.
- **Tier B (default):** sanitise names ƒ+' roles, redact account / policy numbers, keep amounts and ages real (decision quality depends on real numbers).
- **Tier D ƒ?" Health override:** no medical specifics, no DNA / genetic data in general bundles. Insurance/health decisions that **require** underwriting facts (pregnancy status, pre-existing conditions, waiting periods) get a Tier D restricted appendix with explicit consent each invocation OR Scott verifies the underwriting facts locally without piping to reviewers.
- **Tier D ƒ?" Family override:** kids' names ƒ+' K1ƒ?"K4 (real ages preserved ƒ?" dependency calculations matter), no school names; pregnancy described as "expecting, due ~Q{quarter} {year}" (mat-leave timing is load-bearing).
- **Minimum required for decision quality:** prefer derived ratios (debt-to-income, liability-to-asset, premium-to-cover) over raw amounts where the maths allows. Raw amounts only when the decision needs them (insurance premium maths, mat-leave hole sizing).
- **Salaries and account balances:** real values allowed in bundles by default; account *numbers* always redacted.

**Output destinations:**
- Decisions ƒ+' `journal/decisions/YYYY-MM-DD-{topic}.md` ƒ?" **1-page summary** using the existing `protocols/decision-record-template.md`, with explicit link to `10-final-output.md` for full record
- Full investigation record ƒ+' `journal/investigations/YYYY-MM-DD-{topic}/10-final-output.md` ƒ?" alternatives considered, evidence used, dissent noted, privacy tier applied, follow-up tasks
- Procedures ƒ+' `protocols/`
- Memory ƒ+' memory dir (close-out skill handles)
- Skill specs ƒ+' `docs/superpowers/specs/`

## 6. Investigation folder structure (10-phase, single pattern)

`journal/investigations/YYYY-MM-DD-{topic}/`:
```
README.md  (current phase, status, last-touched, brief summary ƒ?" for cold-start orientation)
00-topic.md
01-questions-{claude,codex,gemini}.md
02-consolidated-questions.md
03-spec.md
04-research-{claude,codex,gemini}.md
05-research-pack.md
06-deliberation-{claude,codex,gemini}.md  +  06-deliberation.md (consolidated)
07-disposition.md
08-meta-reflection-{claude,codex,gemini}.md  +  08-meta-reflection.md
09-mediation-{claude,codex,gemini}.md  +  09-resolution.md
10-final-output.md  (full investigation record ƒ?" promoted summary lives in journal/decisions/)
```

**Single pattern, no "lite" variant.**

**Early termination semantics (NOT "n/a"):**
- If an investigation can close before phase 09 (research is conclusive, no deliberation warranted), `07-disposition.md` declares this explicitly: *"Closed at phase N: <reason>. No deliberation/mediation needed."*
- Phase files past the termination point are **omitted** from the folder, OR if created they say *"Not reached. Investigation closed at phase N ƒ?" see 07-disposition.md."*
- This preserves audit truth ƒ?" the trail shows the investigation terminated by evidence, not skipped procedurally.

**Bootstrap:** `bin/new-investigation.ps1 <topic-slug>` creates the folder, the empty 00ƒ?"10 files, and the README. ~15 lines of PowerShell. Not the `/investigate` skill ƒ?" just a folder-scaffold convenience.

## 7. Insurance audit ƒ?" validating worked example

**Folder:** `journal/investigations/2026-05-06-insurance-audit/` (bootstrapped via `bin/new-investigation.ps1`)

**Topic:** Mina has proposed insurance replacements; audit current coverage vs alternatives, decide what to drop / replace / restructure across life, income protection, TPD, trauma, home/contents, car (and any others Mina has flagged).

**Privacy plan:**
- Real salaries and ages (insurance maths)
- Mina described as "expecting, due ~Q4 2026" (mat-leave timing is load-bearing for life/IP)
- Kids as K1ƒ?"K4 with real ages, no school names
- No medical history piped to reviewers ƒ?" Scott verifies underwriting facts locally with insurer documents
- If a Tier D appendix is needed for a specific decision, explicit consent per invocation

**Underwriting verification:** Scott (with Mina) reads insurer PDS / underwriting questionnaires directly. Reviewers (Codex/Gemini) pressure-test the **decision logic** (which policy wins on which dimension, where the gaps are), not the **eligibility** (which is a yes/no from the insurer).

**Pre-flight:** Codex and Gemini installed and authenticated ƒ?" verified for this design review.

**Final output:**
- `10-final-output.md` ƒ?" full investigation record with per-policy comparison, alternatives, evidence, dissent, follow-ups
- `journal/decisions/2026-05-06-insurance-audit.md` ƒ?" 1-page summary using `protocols/decision-record-template.md`, links back to `10-final-output.md`
- Any policy-switch tasks in the user's task system

## 8. `/investigate` skill v2 ƒ?" deferred

**Scope (when built):** automate folder scaffolding (currently `bin/new-investigation.ps1`), prompt templates per phase, evidence-bundle assembly, CLI orchestration to Codex/Gemini, sanitisation pre-flight check.

**Trigger to build:** after at least one real investigation validates the manual workflow. If the insurance audit shows manual orchestration is fine and the bootstrap script covers the friction, defer further.

**Backlog:** V1ƒ?"V14 from the RAIOS investigation outputs (`09-resolution.md` AG), plus any lessons captured from the insurance audit.

## 9. Open design questions ƒ?" answered

| Question | Answer |
|---|---|
| Are Codex / Gemini local or vendor-hosted? | Vendor-hosted (OpenAI / Google). Encoded in the threat-model section. |
| Should exact salaries be in bundles or derived ratios? | Derived ratios where the question allows; raw values when the maths needs them. Captured in "minimum required" clause. |
| Who owns underwriting verification? | Scott + Mina + insurer documents. Reviewers test decision logic, not eligibility. |
| Will adjacent code repos have their own `AGENTS.md`? | Yes ƒ?" `plaios-tools`, `trading-tools` are separate repos with their own root `AGENTS.md`. No nesting under PLAIOS. |
| Wall-clock time budget per investigation phase? | Soft cap ~2 hours per phase; if exceeded, escalate or rethink scope. |
| Evidence bundle disposal in git history? | Bundles stay in PLAIOS git (private, single-user). Redaction overkill for now. |
| Cross-model tie-breaker if Codex / Gemini disagree? | Orchestrator (Scott) is the tie-breaker; disagreement recorded in `09-resolution.md`. No 4th-model arbiter. |

## 10. Implementation order (what gets built when)

1. `D:\PLAIOS\AGENTS.md` ƒ?" drafted from the RAIOS template (structure only), customised for PLAIOS, adversarially reviewed before commit.
2. `D:\PLAIOS\protocols\multi-agent.md` ƒ?" recipe + overlay.
3. `D:\PLAIOS\CLAUDE.md` ƒ?" add the 1-line pointer to `AGENTS.md`.
4. `D:\PLAIOS\bin\new-investigation.ps1` ƒ?" scaffold script.
5. Bootstrap the insurance audit folder via the script. Run phase 00 (topic intake).
6. Defer `/investigate` skill until the audit validates the manual workflow.

## 11. Success criteria

- The insurance audit completes through to a decision record. Reviewers materially change the decision logic at least once (otherwise the multi-agent overhead wasn't earned).
- Scott voluntarily uses the procedure on a second durable decision without prompting.
- AGENTS.md is referenced by both Codex and Gemini in subsequent runs (verifiable via output content / behaviour).
- Bundle minimisation rule observed: no raw account numbers, no medical history, no kids' names in any committed bundle.
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

 succeeded in 645ms:
# bin/new-investigation.ps1
# Scaffold a new investigation folder under journal/investigations/.
# Usage (from PLAIOS root): .\bin\new-investigation.ps1 <topic-slug>

param(
    [Parameter(Mandatory=$true)]
    [string]$Slug
)

$Date = Get-Date -Format "yyyy-MM-dd"
$Folder = "journal/investigations/$Date-$Slug"

if (Test-Path $Folder) {
    Write-Error "Folder already exists: $Folder"
    exit 1
}

New-Item -ItemType Directory -Path $Folder | Out-Null

$Files = @(
    "00-topic.md"
    "01-questions-claude.md"
    "01-questions-codex.md"
    "01-questions-gemini.md"
    "02-consolidated-questions.md"
    "03-spec.md"
    "04-research-claude.md"
    "04-research-codex.md"
    "04-research-gemini.md"
    "05-research-pack.md"
    "06-deliberation-claude.md"
    "06-deliberation-codex.md"
    "06-deliberation-gemini.md"
    "06-deliberation.md"
    "07-disposition.md"
    "08-meta-reflection-claude.md"
    "08-meta-reflection-codex.md"
    "08-meta-reflection-gemini.md"
    "08-meta-reflection.md"
    "09-mediation-claude.md"
    "09-mediation-codex.md"
    "09-mediation-gemini.md"
    "09-resolution.md"
    "10-final-output.md"
)

foreach ($File in $Files) {
    New-Item -ItemType File -Path "$Folder/$File" | Out-Null
}

# Seed README.md with phase tracking
$Readme = @"
# Investigation: $Slug

**Started:** $Date
**Phase:** 00 (topic intake)
**Status:** open
**Last touched:** $Date

## Topic summary

[1-2 sentences on what is being decided. Filled in as ``00-topic.md`` is written.]

## Convergence target

[What does a converged outcome look like for this investigation? E.g., "Decide which insurances to drop / replace / restructure, with a 1-page decision record at journal/decisions/."]

## Phase log

- $Date ƒ?" folder bootstrapped; phase 00 (topic intake) starts here.
"@

Set-Content -Path "$Folder/README.md" -Value $Readme -Encoding utf8

Write-Host "Created $Folder" -ForegroundColor Green
Write-Host "Next: edit 00-topic.md to capture topic + initiator goals + phase model."
Write-Host "Update README.md after each phase boundary so a cold-start reader knows where the investigation is."
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

 succeeded in 675ms:
# AGENTS.md ƒ?" PLAIOS

**Audience:** any AI agent (Claude, Codex, Gemini, future tools) invoked from this directory.
**Purpose:** describe the project, the rules, and your role in this system, so you can do good work from a cold start.

---

## Project

PLAIOS (Personal Life AI Operating System) is a single-user, markdown-heavy knowledge and decision system at `D:\PLAIOS\`. It exists to surface structural weakness across life domains, prioritise by hierarchy of needs, maintain continuity across AI conversations, and produce durable decisions ƒ?" not a to-do list.

Owner: Scott McKennie. CEO of an Australian software org. Father of four with a fifth on the way.

Work product: decisions, memory, procedures, cross-domain syntheses. Adjacent code repos (`plaios-tools`, `trading-tools`) live separately at `D:\Plaios-tools\` with their own root `AGENTS.md` ƒ?" out of scope for this file.

**Tech stack:** Markdown, plus PowerShell and occasional Python for instrumentation.
**Run / test / build:** none for the reasoning system itself.
**Commit style:** conventional, first line ƒ%70 chars, imperative.

## Conventions

- File layout: `domains/` (per-domain folders), `protocols/` (rules + templates), `journal/` (time-stamped audit trail incl. `decisions/` and `investigations/`), `docs/superpowers/specs/` (design docs), `memory/` (cross-session knowledge ƒ?" mirrored on close-out).
- Markdown style: GitHub-flavoured, sentence case for headings, tables where structure helps, minimal inline emphasis, terse prose.
- Decision records use `protocols/decision-record-template.md`. They are 1-page summaries that link back to the full investigation record at `journal/investigations/{date-topic}/10-final-output.md`.
- "Done" criteria for any artefact: it converges on a binding outcome; dissent (if any) is recorded; output is promoted to its destination; memory is updated if a stable new fact was confirmed.

## Multi-agent role conventions

When you are invoked here:

- **Roles are task assignments, not personalities.** Claude drives. Codex is invoked at named risk points for adversarial review. Gemini is invoked for long-context / external-pattern questions. The orchestrator (Scott, or Claude in his stead) routes work and is the tie-breaker.
- **Goal is convergence, not dialogue.** Every investigation aims at a group-bound decision, recommendation, or outcome. Input ƒ+' process ƒ+' output. Dialogue without convergence is procedure failure. If a phase produces more disagreement than it resolves, escalate to mediation rather than continuing in circles.
- **Default review mode:** evidence-bundle only ƒ?" spec + draft/diff + verification output. Never chat history. Never the full repo.
- **Output rigour:** cite `file:line` for any specific claim. Tag uncertain claims `[uncertain]` or `[needs verification]`. Flag sub-85% confidence. No bare assertions of unknowns.
- **Convergence over politeness.** No flattery. No "LGTM"-style approval. No padding. If the work is fine, say "no material concerns" and stop.
- **Surgical edits.** Pin files explicitly. No repo-wide dumps. No opportunistic refactors.
- **Token discipline.** Stay under 250k tokens per session. Close out with a capsule before degradation.

## Operational rule ƒ?" root invocation

All multi-agent CLI invocations run from `D:\PLAIOS\` (the project root). Bundle file paths are relative to root. Why: this guarantees `AGENTS.md` is loaded by every agent in every invocation, so all agents share the same baseline.

## Privacy / threat model

Codex calls hit OpenAI; Gemini calls hit Google. **Bundle contents leave Anthropic's perimeter.** Vendor terms govern what those vendors can do with the data ƒ?" assume the vendor sees what you bundle.

The sanitisation rules below are about **reducing model focus on identity to prevent bias / sycophancy / latent re-identification anchoring** ƒ?" not cryptographic anonymity. The model is assumed to know who Scott is.

- **Tier B (default):** sanitise names ƒ+' roles, redact account / policy numbers, keep amounts and ages real (decision quality depends on real numbers).
- **Tier D ƒ?" Health override:** no medical specifics, no DNA / genetic data in general bundles. If a decision genuinely requires underwriting facts (pregnancy status, pre-existing conditions, waiting periods, etc.), include them in a Tier D restricted appendix with explicit consent each invocation, OR the orchestrator verifies the underwriting facts locally without piping to reviewers.
- **Tier D ƒ?" Family override:** kids' names ƒ+' K1ƒ?"K4 (real ages preserved ƒ?" dependency calculations matter), no school names; pregnancy described as "expecting, due ~Q{quarter} {year}".
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
- Don't escape the medium ƒ?" reasoning artefacts stay in markdown; if the answer wants to become code, surface that to the orchestrator first.

## Where things live

- Identity, hierarchy of needs, maturity scale, domain map, priority algorithm, session protocol, systems-thinking framework: `CLAUDE.md` (Claude orchestration logic ƒ?" not relevant to one-shot Codex / Gemini reviews).
- Multi-agent recipe (default workflow, variants, CLI invocations, when NOT to use): `protocols/multi-agent.md`.
- Decision record template: `protocols/decision-record-template.md`.
- Investigation folders: `journal/investigations/YYYY-MM-DD-{topic}/`.
- Decision records: `journal/decisions/YYYY-MM-DD-{topic}.md`.
- Investigation scaffold script: `bin/new-investigation.ps1`.
- Memory: `D:\PLAIOS\memory\` (mirrored from the active Claude memory store on close-out).

## When to escalate

- If the task requires changes outside the bundle scope ƒ?" stop, surface to the orchestrator.
- If a load-bearing assumption fails ƒ?" stop, report. Don't paper over.
- If models can't converge after mediation (phase 09 of an investigation) ƒ?" orchestrator decides; record the disagreement in `09-resolution.md`.
- If the work touches health, money, legal, family obligations, or contradicts memory ƒ?" promote to multi-agent IN regardless of how tactical it looks.

---

*This file is the cross-tool baseline. It must be readable from a cold start by any agent. Keep it under 200 lines. If a section needs more depth, link to the dedicated file rather than expanding here.*
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

codex
The implementation is readable enough to assess. I’m doing one narrower pass now for exact line anchors and for cross-protocol duplication/contradiction before giving the verdict.
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'findstr /n "''^" AGENTS.md' in D:\PLAIOS
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'findstr /n "''^" protocols'"\\multi-agent.md" in D:\PLAIOS
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'findstr /n "''^" bin'"\\new-investigation.ps1" in D:\PLAIOS
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'findstr /n "''^" protocols'"\\decision-record-template.md protocols\\session-checklist.md protocols\\assessment-template.md" in D:\PLAIOS
 succeeded in 476ms:
1:# AGENTS.md — PLAIOS
2:
3:**Audience:** any AI agent (Claude, Codex, Gemini, future tools) invoked from this directory.
4:**Purpose:** describe the project, the rules, and your role in this system, so you can do good work from a cold start.
5:
6:---
7:
8:## Project
9:
10:PLAIOS (Personal Life AI Operating System) is a single-user, markdown-heavy knowledge and decision system at `D:\PLAIOS\`. It exists to surface structural weakness across life domains, prioritise by hierarchy of needs, maintain continuity across AI conversations, and produce durable decisions — not a to-do list.
11:
12:Owner: Scott McKennie. CEO of an Australian software org. Father of four with a fifth on the way.
13:
14:Work product: decisions, memory, procedures, cross-domain syntheses. Adjacent code repos (`plaios-tools`, `trading-tools`) live separately at `D:\Plaios-tools\` with their own root `AGENTS.md` — out of scope for this file.
15:
16:**Tech stack:** Markdown, plus PowerShell and occasional Python for instrumentation.
17:**Run / test / build:** none for the reasoning system itself.
18:**Commit style:** conventional, first line ≤70 chars, imperative.
19:
20:## Conventions
21:
22:- File layout: `domains/` (per-domain folders), `protocols/` (rules + templates), `journal/` (time-stamped audit trail incl. `decisions/` and `investigations/`), `docs/superpowers/specs/` (design docs), `memory/` (cross-session knowledge — mirrored on close-out).
23:- Markdown style: GitHub-flavoured, sentence case for headings, tables where structure helps, minimal inline emphasis, terse prose.
24:- Decision records use `protocols/decision-record-template.md`. They are 1-page summaries that link back to the full investigation record at `journal/investigations/{date-topic}/10-final-output.md`.
25:- "Done" criteria for any artefact: it converges on a binding outcome; dissent (if any) is recorded; output is promoted to its destination; memory is updated if a stable new fact was confirmed.
26:
27:## Multi-agent role conventions
28:
29:When you are invoked here:
30:
31:- **Roles are task assignments, not personalities.** Claude drives. Codex is invoked at named risk points for adversarial review. Gemini is invoked for long-context / external-pattern questions. The orchestrator (Scott, or Claude in his stead) routes work and is the tie-breaker.
32:- **Goal is convergence, not dialogue.** Every investigation aims at a group-bound decision, recommendation, or outcome. Input → process → output. Dialogue without convergence is procedure failure. If a phase produces more disagreement than it resolves, escalate to mediation rather than continuing in circles.
33:- **Default review mode:** evidence-bundle only — spec + draft/diff + verification output. Never chat history. Never the full repo.
34:- **Output rigour:** cite `file:line` for any specific claim. Tag uncertain claims `[uncertain]` or `[needs verification]`. Flag sub-85% confidence. No bare assertions of unknowns.
35:- **Convergence over politeness.** No flattery. No "LGTM"-style approval. No padding. If the work is fine, say "no material concerns" and stop.
36:- **Surgical edits.** Pin files explicitly. No repo-wide dumps. No opportunistic refactors.
37:- **Token discipline.** Stay under 250k tokens per session. Close out with a capsule before degradation.
38:
39:## Operational rule — root invocation
40:
41:All multi-agent CLI invocations run from `D:\PLAIOS\` (the project root). Bundle file paths are relative to root. Why: this guarantees `AGENTS.md` is loaded by every agent in every invocation, so all agents share the same baseline.
42:
43:## Privacy / threat model
44:
45:Codex calls hit OpenAI; Gemini calls hit Google. **Bundle contents leave Anthropic's perimeter.** Vendor terms govern what those vendors can do with the data — assume the vendor sees what you bundle.
46:
47:The sanitisation rules below are about **reducing model focus on identity to prevent bias / sycophancy / latent re-identification anchoring** — not cryptographic anonymity. The model is assumed to know who Scott is.
48:
49:- **Tier B (default):** sanitise names → roles, redact account / policy numbers, keep amounts and ages real (decision quality depends on real numbers).
50:- **Tier D — Health override:** no medical specifics, no DNA / genetic data in general bundles. If a decision genuinely requires underwriting facts (pregnancy status, pre-existing conditions, waiting periods, etc.), include them in a Tier D restricted appendix with explicit consent each invocation, OR the orchestrator verifies the underwriting facts locally without piping to reviewers.
51:- **Tier D — Family override:** kids' names → K1–K4 (real ages preserved — dependency calculations matter), no school names; pregnancy described as "expecting, due ~Q{quarter} {year}".
52:- **Minimum required for decision quality:** prefer derived ratios (debt-to-income, premium-to-cover, liability-to-asset) over raw amounts where the maths allows. Raw amounts only when the decision genuinely needs them.
53:- **Salaries and account balances:** real values allowed in bundles by default; account *numbers* always redacted.
54:
55:If you find Tier D material in a bundle that wasn't tagged Tier D, **stop, flag as a privacy escape, do not process.**
56:
57:## What NOT to do
58:
59:- Don't expand scope silently. Surface and stop.
60:- Don't speculate without flagging `[uncertain]`. Don't make bare assertions about unknowns.
61:- Don't aggregate across domains unless the orchestrator explicitly asked for cross-domain analysis.
62:- Don't generate full-file rewrites when surgical edits will do.
63:- Don't invent file paths, function names, memory entries, or domain conventions. Read or say `[needs verification]`.
64:- Don't add commentary, padding, or motivational language. Terse is correct.
65:- Don't escape the medium — reasoning artefacts stay in markdown; if the answer wants to become code, surface that to the orchestrator first.
66:
67:## Where things live
68:
69:- Identity, hierarchy of needs, maturity scale, domain map, priority algorithm, session protocol, systems-thinking framework: `CLAUDE.md` (Claude orchestration logic — not relevant to one-shot Codex / Gemini reviews).
70:- Multi-agent recipe (default workflow, variants, CLI invocations, when NOT to use): `protocols/multi-agent.md`.
71:- Decision record template: `protocols/decision-record-template.md`.
72:- Investigation folders: `journal/investigations/YYYY-MM-DD-{topic}/`.
73:- Decision records: `journal/decisions/YYYY-MM-DD-{topic}.md`.
74:- Investigation scaffold script: `bin/new-investigation.ps1`.
75:- Memory: `D:\PLAIOS\memory\` (mirrored from the active Claude memory store on close-out).
76:
77:## When to escalate
78:
79:- If the task requires changes outside the bundle scope — stop, surface to the orchestrator.
80:- If a load-bearing assumption fails — stop, report. Don't paper over.
81:- If models can't converge after mediation (phase 09 of an investigation) — orchestrator decides; record the disagreement in `09-resolution.md`.
82:- If the work touches health, money, legal, family obligations, or contradicts memory — promote to multi-agent IN regardless of how tactical it looks.
83:
84:---
85:
86:*This file is the cross-tool baseline. It must be readable from a cold start by any agent. Keep it under 200 lines. If a section needs more depth, link to the dedicated file rather than expanding here.*
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

 succeeded in 491ms:
1:# Multi-Agent Procedure for PLAIOS
2:
3:**Source:** core lifted from `D:\RAIOS-outputs\investigations\multi-agent-dev-practices-20260505-2237\10-final-recipe.md` (3-model ratified). PLAIOS overlay added at the bottom.
4:
5:**Read this when:** you're about to make a durable decision, change a procedure, update memory in ways that contradict prior memory, or run an investigation. See "When NOT to use" if you're not sure.
6:
7:---
8:
9:## Goal — convergence on a binding outcome
10:
11:Every investigation through this procedure produces a **group-bound decision, recommendation, or outcome** — not a balanced essay, not a perspectives roundup. The structure is:
12:
13:**Input → process → output.**
14:
15:- **Input:** topic + spec + evidence
16:- **Process:** independent research, parallel deliberation, mediated reconciliation
17:- **Output:** one binding artefact, with dissent recorded but not sovereign
18:
19:The orchestrator (Scott, or Claude in his stead) is always the tie-breaker. Disagreement is recorded; it is never the deliverable. **Dialogue without convergence is procedure failure.**
20:
21:---
22:
23:## Where each model fits
24:
25:| Model | Role | Why |
26:|---|---|---|
27:| **Claude** (Claude Code) | Driver. Holds the session, drafts artefacts, runs verification, narrates. | Native sub-agents, plan mode, file pinning, agentic loops, MCP access. |
28:| **Codex** (`codex exec`) | Adversarial reviewer. Invoked on demand. | Different model, different blind spots — catches what same-model review misses. |
29:| **Gemini** (`gemini --skip-trust -p`) | Long-context / external-pattern channel. Invoked on demand. | Long context window, different training — useful for "is this how it's done elsewhere?" or "does this match prior decisions?" |
30:
31:Each model runs in its own context window. They never talk to each other. **The orchestrator passes artefacts between them via CLI.**
32:
33:## The default workflow (any task more than a one-line edit)
34:
35:1. **Plan** in Claude Code. Hand it: objective, files, constraints, non-goals, what convergence looks like. Ratify the plan before any artefact is drafted.
36:2. **Draft** in Claude Code. Surgical edits only. Files pinned. No repo-wide dumps. No opportunistic refactors.
37:3. **Verify** in Claude Code. Run any checks, tests, or repro scripts inside the session.
38:4. **Review** — pick the channel by risk:
39:
40:   | Risk | Reviewer | Why |
41:   |---|---|---|
42:   | Routine | Claude Code reviewer sub-agent (sees only spec + draft + verify output) | Cheap, in-session |
43:   | Risky / cross-domain / consequential | **Codex** | Independent model — catches what Claude missed |
44:   | "Is this how it's done elsewhere?" / pattern question | **Gemini** | Long context + external pattern view |
45:
46:   The reviewer sees only the evidence bundle. Never the chat history. Never the full repo.
47:
48:5. **Narrate & commit.** State in the commit message *why* the accepted outcome is correct, in your own words. No "LGTM"-style merges.
49:6. **Close out** when the session approaches 200–250k tokens or spans days. Write a capsule: objective, decision, files changed, checks run, unresolved risks, exact next step.
50:
51:## CLI invocations
52:
53:**All multi-agent invocations run from `D:\PLAIOS\` (the project root)**, so `AGENTS.md` is loaded automatically by every CLI.
54:
55:### Codex (adversarial review)
56:
57:```bash
58:# build the evidence bundle (no chat history)
59:cat spec.md draft.md verify-output.md > bundle.md
60:
61:# pipe via stdin (NOT positional argument — that pattern hangs)
62:codex exec - < bundle.md
63:```
64:
65:### Gemini (long-context / pattern question)
66:
67:```bash
68:gemini --skip-trust -p "$(cat <<'EOF'
69:Question: [your specific question]
70:Context: [paste relevant content or reference paths]
71:EOF
72:)"
73:```
74:
75:### Claude Code
76:
77:Open in `D:\PLAIOS\`. The CLI auto-loads `AGENTS.md` and `CLAUDE.md` from the working directory.
78:
79:## Variant — investigation (durable, consequential, irreversible)
80:
81:For decisions where rollback cost exceeds the deliberation cost. **This is the variant that converges to a group-bound outcome.** Output is a decision record (and possibly a procedure / recommendation), never a diff alone.
82:
83:**Folder:** `journal/investigations/YYYY-MM-DD-{topic}/`. Bootstrap with `bin/new-investigation.ps1 <topic-slug>`.
84:
85:### 10-phase pattern (single track — no "lite" variant)
86:
87:```
88:README.md  (current phase, status, last-touched, convergence target)
89:00-topic.md
90:01-questions-{claude,codex,gemini}.md
91:02-consolidated-questions.md
92:03-spec.md
93:04-research-{claude,codex,gemini}.md
94:05-research-pack.md
95:06-deliberation-{claude,codex,gemini}.md  +  06-deliberation.md
96:07-disposition.md
97:08-meta-reflection-{claude,codex,gemini}.md  +  08-meta-reflection.md
98:09-mediation-{claude,codex,gemini}.md  +  09-resolution.md
99:10-final-output.md  (full investigation record)
100:```
101:
102:### Convergence checkpoints
103:
104:- **Phase 02:** orchestrator answers consolidated questions. Convergence on *what's being decided*.
105:- **Phase 07:** disposition declares the binding outcome (or early termination if research was conclusive).
106:- **Phase 09:** if disagreement remains after disposition, models mediate; resolution is binding. Orchestrator decides if mediation can't converge.
107:
108:### Early termination
109:
110:If research (phase 04) is conclusive and no deliberation is warranted, `07-disposition.md` says: *"Closed at phase N: <reason>. No deliberation/mediation needed."* Phases past termination are **omitted** OR explicitly marked *"Not reached. Investigation closed at phase N — see 07-disposition.md."* Never use "n/a" — that creates a misleading audit trail.
111:
112:### Output destinations
113:
114:- **1-page summary** at `journal/decisions/YYYY-MM-DD-{topic}.md` (using `protocols/decision-record-template.md`), with a link back to the full record
115:- **Full record** at `10-final-output.md`: alternatives considered, evidence used, dissent noted, privacy tier applied, follow-up tasks
116:- **Procedural outcome** (if the investigation produced a procedure or skill spec): promoted to `protocols/` or `docs/superpowers/specs/`
117:- **Memory updates** flowing from the decision: handled by the close-out skill
118:
119:## Variant — bug fix
120:
121:For PLAIOS this applies to `plaios-tools` / `trading-tools` code repos. Those use this variant directly via their own repo-local `AGENTS.md` — no PLAIOS overlay. Reasoning-domain bugs (memory contradictions, decision-record errors) use the investigation variant above instead.
122:
123:1. **Reproduce first.** Either Claude Code or Codex writes a *failing test* that demonstrates the bug. Run it. **No fix is permitted until this test exists and fails.**
124:2. **Fix in Claude Code.** Surgical patch. Test now passes.
125:3. **Adversarial review with Codex.** Bundle = spec + diff + test output.
126:4. **Narrate & commit.**
127:
128:## Token discipline
129:
130:Each model session stays under ~250k tokens by design. **No model ever holds the whole picture** — small, curated artefacts pass between them. Full repo dumps are forbidden. If a session approaches the ceiling, close it out and start fresh.
131:
132:## When NOT to use multi-agent
133:
134:- One-line edits — just write it.
135:- Tasks under 30 minutes — overhead exceeds gain.
136:- Pure exploration — single Claude Code session, no review channel.
137:- Routine state reads, daily journal lines, ephemeral memory updates that don't contradict prior memories.
138:- Tactical PocketSmith tweaks, calendar events, gmail drafts.
139:
140:### OUT override
141:
142:The OUT list applies *unless* the artefact:
143:- Creates an external commitment (Gmail to insurer / lawyer / doctor / lender)
144:- Changes a durable model (PocketSmith budget structure, not just an event amount)
145:- Affects money / legal / health / family obligations
146:- Contradicts prior memory
147:
148:In any of those cases, promote to IN.
149:
150:---
151:
152:## PLAIOS overlay
153:
154:### Trigger rules — multi-agent IN
155:
156:- Durable decisions in life domains (insurance, schools, property, fertility / baby planning, vendor switches, debt restructure, household-level rules)
157:- Cross-domain syntheses ("where am I structurally weak?")
158:- Memory updates that contradict prior memories
159:- Skill / procedure design changes
160:- Code work in `plaios-tools` / `trading-tools` (use this recipe directly via repo-local `AGENTS.md`; no overlay needed for code work)
161:
162:### Privacy / threat model
163:
164:See `AGENTS.md` "Privacy / threat model" section. Summary: B default + D Health/Family overrides + minimum-required clause. Codex and Gemini are vendor-hosted (OpenAI, Google); bundle contents leave Anthropic's perimeter.
165:
166:### When in doubt
167:
168:If you're unsure whether something belongs in IN or OUT: default IN if it's durable and irreversible; default OUT if it's tactical and reversible. The override clauses handle edge cases.
169:
170:### Wall-clock soft cap
171:
172:If a single phase exceeds ~2 hours, escalate or rethink scope. The procedure should not become its own time sink.
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

 succeeded in 506ms:
1:# bin/new-investigation.ps1
2:# Scaffold a new investigation folder under journal/investigations/.
3:# Usage (from PLAIOS root): .\bin\new-investigation.ps1 <topic-slug>
4:
5:param(
6:    [Parameter(Mandatory=$true)]
7:    [string]$Slug
8:)
9:
10:$Date = Get-Date -Format "yyyy-MM-dd"
11:$Folder = "journal/investigations/$Date-$Slug"
12:
13:if (Test-Path $Folder) {
14:    Write-Error "Folder already exists: $Folder"
15:    exit 1
16:}
17:
18:New-Item -ItemType Directory -Path $Folder | Out-Null
19:
20:$Files = @(
21:    "00-topic.md"
22:    "01-questions-claude.md"
23:    "01-questions-codex.md"
24:    "01-questions-gemini.md"
25:    "02-consolidated-questions.md"
26:    "03-spec.md"
27:    "04-research-claude.md"
28:    "04-research-codex.md"
29:    "04-research-gemini.md"
30:    "05-research-pack.md"
31:    "06-deliberation-claude.md"
32:    "06-deliberation-codex.md"
33:    "06-deliberation-gemini.md"
34:    "06-deliberation.md"
35:    "07-disposition.md"
36:    "08-meta-reflection-claude.md"
37:    "08-meta-reflection-codex.md"
38:    "08-meta-reflection-gemini.md"
39:    "08-meta-reflection.md"
40:    "09-mediation-claude.md"
41:    "09-mediation-codex.md"
42:    "09-mediation-gemini.md"
43:    "09-resolution.md"
44:    "10-final-output.md"
45:)
46:
47:foreach ($File in $Files) {
48:    New-Item -ItemType File -Path "$Folder/$File" | Out-Null
49:}
50:
51:# Seed README.md with phase tracking
52:$Readme = @"
53:# Investigation: $Slug
54:
55:**Started:** $Date
56:**Phase:** 00 (topic intake)
57:**Status:** open
58:**Last touched:** $Date
59:
60:## Topic summary
61:
62:[1-2 sentences on what is being decided. Filled in as ``00-topic.md`` is written.]
63:
64:## Convergence target
65:
66:[What does a converged outcome look like for this investigation? E.g., "Decide which insurances to drop / replace / restructure, with a 1-page decision record at journal/decisions/."]
67:
68:## Phase log
69:
70:- $Date — folder bootstrapped; phase 00 (topic intake) starts here.
71:"@
72:
73:Set-Content -Path "$Folder/README.md" -Value $Readme -Encoding utf8
74:
75:Write-Host "Created $Folder" -ForegroundColor Green
76:Write-Host "Next: edit 00-topic.md to capture topic + initiator goals + phase model."
77:Write-Host "Update README.md after each phase boundary so a cold-start reader knows where the investigation is."
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

 succeeded in 521ms:
protocols\decision-record-template.md:1:# Decision: [Title]
protocols\decision-record-template.md:2:
protocols\decision-record-template.md:3:**Date:** YYYY-MM-DD
protocols\decision-record-template.md:4:**Domain:** [Domain name]
protocols\decision-record-template.md:5:**Context:** [What prompted this decision]
protocols\decision-record-template.md:6:**Options Considered:** [What alternatives were evaluated]
protocols\decision-record-template.md:7:**Decision:** [What was decided and why]
protocols\decision-record-template.md:8:**Expected Outcome:** [What should happen as a result]
protocols\decision-record-template.md:9:**Review Date:** [When to check if it worked]
protocols\session-checklist.md:1:# Session Checklist
protocols\session-checklist.md:2:
protocols\session-checklist.md:3:## Opening
protocols\session-checklist.md:4:1. What level of the hierarchy is this session about?
protocols\session-checklist.md:5:2. Read `manifest.md` (if in a domain) to see what's available
protocols\session-checklist.md:6:3. Read `memory.md` for accumulated knowledge
protocols\session-checklist.md:7:4. Read `state/` files for current operational state
protocols\session-checklist.md:8:5. Any time-critical items?
protocols\session-checklist.md:9:6. If working at a higher level but lower levels are unstable, flag the dependency
protocols\session-checklist.md:10:7. Load reference material from `reference/` as needed — not upfront
protocols\session-checklist.md:11:
protocols\session-checklist.md:12:## Closing
protocols\session-checklist.md:13:1. Append session summary to `journal/session-log.md`
protocols\session-checklist.md:14:2. If consequential decisions were made, create decision records in `journal/decisions/`
protocols\session-checklist.md:15:3. Update memory files if stable new knowledge was confirmed
protocols\session-checklist.md:16:4. Update state files if assessments or priorities changed
protocols\assessment-template.md:1:# Assessment Template
protocols\assessment-template.md:2:
protocols\assessment-template.md:3:Use this format for domain current-assessment.md files.
protocols\assessment-template.md:4:
protocols\assessment-template.md:5:---
protocols\assessment-template.md:6:
protocols\assessment-template.md:7:**Last Updated:** YYYY-MM-DD
protocols\assessment-template.md:8:**Next Review:** YYYY-MM-DD
protocols\assessment-template.md:9:
protocols\assessment-template.md:10:| Dimension | Rating | Trend | Key Finding |
protocols\assessment-template.md:11:|-----------|--------|-------|-------------|
protocols\assessment-template.md:12:| [Dimension name] | [1-5] | [↑ → ↓] | [One-line finding] |
protocols\assessment-template.md:13:
protocols\assessment-template.md:14:**Overall Domain Status:** [Crisis / Fragile / Functional / Systematic / Optimised]
protocols\assessment-template.md:15:
protocols\assessment-template.md:16:**Top Priority:** [Single most important action for this domain]
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "findstr /n \"Tier D Health Family insurance underwriting raw amounts salaries account balances\" docs\\superpowers\\specs\\2026-05-06-plaios-multi-agent-design.md" in D:\PLAIOS
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "findstr /n \"AGENTS.md protocols\\\\multi-agent.md new-investigation.ps1 10-phase Early termination Single pattern Output destinations\" docs\\superpowers\\specs\\2026-05-06-plaios-multi-agent-design.md" in D:\PLAIOS
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "findstr /n \"convergence binding Dialogue orchestrator tie-breaker\" docs\\superpowers\\specs\\2026-05-06-plaios-multi-agent-design.md" in D:\PLAIOS
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'findstr /n "Cross-tool baseline" CLAUDE.md' in D:\PLAIOS
 succeeded in 453ms:
22:## 2a. Procedure goal — convergence on a binding outcome
28:- **Output:** one binding artefact (decision record, procedure, recommendation), with dissent recorded but not sovereign
30:When the three models converge, the orchestrator (Scott) ratifies and ships. When they don't converge after mediation (phase 09), the orchestrator decides; the disagreement is recorded in `09-resolution.md` so future investigations can learn from it. The orchestrator is always the tie-breaker — no 4th-model arbiter.
32:**Dialogue without convergence is procedure failure.** If a phase produces more disagreement than it resolves, the procedure escalates to mediation rather than continuing in circles.
66:| Sub-agent definitions, skill bindings (close-out, future /investigate) | CLAUDE.md | Claude-only |
186:| Cross-model tie-breaker if Codex / Gemini disagree? | Orchestrator (Scott) is the tie-breaker; disagreement recorded in `09-resolution.md`. No 4th-model arbiter. |
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

 succeeded in 485ms:
1:# PLAIOS Multi-Agent Development Procedure — Design Spec
3:**Date:** 2026-05-06
12:Adopt the multi-agent development recipe that was 3-model-ratified for ICX (`D:\RAIOS-outputs\investigations\multi-agent-dev-practices-20260505-2237\`) inside PLAIOS, where the work product is mostly non-code reasoning (decisions, memory, procedures, cross-domain syntheses). Validate the adaptation by running it on a real durable decision (insurance audit) before considering skill automation.
32:**Dialogue without convergence is procedure failure.** If a phase produces more disagreement than it resolves, the procedure escalates to mediation rather than continuing in circles.
40:| `D:\PLAIOS\AGENTS.md` | NEW | Cross-tool baseline. Project description, conventions, multi-agent role conventions, privacy/threat-model rules, what NOT to do, where things live. Auto-picked-up by Codex CLI, Gemini CLI, and Claude Code. Self-contained for cold-start strangers. | All three CLIs |
41:| `D:\PLAIOS\CLAUDE.md` | MODIFY (+1 pointer line) | Existing content stays. New line near top: *"For project conventions and multi-agent role rules, see `AGENTS.md` — don't duplicate them here."* | Claude Code only |
42:| `D:\PLAIOS\protocols\multi-agent.md` | NEW | The recipe — core lifted from RAIOS `10-final-recipe.md` + PLAIOS overlay. One file, two clearly-delineated sections. | Humans + Claude when planning |
43:| `D:\PLAIOS\bin\new-investigation.ps1` | NEW | Tiny scaffold: takes `<topic-slug>`, creates `journal/investigations/YYYY-MM-DD-<slug>/` and the empty 00–10 files plus `README.md`. ~15 lines. | Humans |
44:| `D:\PLAIOS\journal\investigations\YYYY-MM-DD-{topic}\` | NEW (per investigation) | Folder-as-state-machine. 10-phase pattern. Includes `README.md` for current-phase / status tracking. | Audit trail |
45:| `D:\PLAIOS\journal\decisions\` | EXISTING (empty) | 1-page summary decision records, link back to `10-final-output.md` for full context. | Long-term decision log |
46:| `D:\PLAIOS\.claude\skills\investigate\` | DEFERRED (v2) | `/investigate` skill — built only if the manual workflow earns it after at least one real investigation. | Claude Code only |
50:- **Investigation folders live under `journal/investigations/`** (not a separate `D:\PLAIOS-outputs\` like RAIOS). PLAIOS is private, single-user, one git history.
52:**Note on adjacent code repos:** `D:\Plaios-tools\trading-tools\` and any future `plaios-tools` repos are **separate git repos**, not nested under PLAIOS. Each will have its own `AGENTS.md` at its repo root. No bleed-through risk; no precedence ambiguity.
54:## 4. `AGENTS.md` vs `CLAUDE.md` — separation of concerns
60:| Privacy / threat-model rules (B default + D Health/Family + minimum-required clause + vendor-hosted disclosure) | AGENTS.md | Reviewer must know what's allowed in the bundle |
61:| Root-invocation rule (CLIs run from `D:\PLAIOS\`) | AGENTS.md | Cross-tool operational rule |
64:| Identity, hierarchy of needs, maturity scale, priority algorithm, escalation rules, session protocol, systems-thinking framework | CLAUDE.md (existing) | Claude orchestration logic; not relevant to a one-shot Codex review |
65:| Privacy *principle* ("sensitive requires explicit navigation") | CLAUDE.md (existing) | Claude session-level rule; the *tier policy* lives in AGENTS.md |
66:| Sub-agent definitions, skill bindings (close-out, future /investigate) | CLAUDE.md | Claude-only |
68:**Drafting `AGENTS.md`:** start from `D:\RAIOS-outputs\...\12-AGENTS-template.md` as **structure**, not verbatim content. Customise PLAIOS-specific sections. Run a quick adversarial pass (Codex, evidence-bundle = drafted file) before committing.
74:- Default workflow: Plan → Implement → Verify → Review (by risk) → Narrate → Close out
76:- Decision variant (multi-model deliberation via `/investigate`, no code, output is a decision record)
84:- All multi-agent CLI invocations run from `D:\PLAIOS\` (the project root). Bundle file paths are relative to root. Why: ensures `AGENTS.md` is always loaded.
87:- Durable decisions in life domains (insurance, schools, property, fertility/baby planning, vendor switches, debt restructure, household-level rules)
105:- **Vendor-hosted disclosure** (load-bearing): Codex calls hit OpenAI, Gemini calls hit Google. Bundle contents are subject to those vendors' terms. If the data is bundle-inappropriate even for a friendly vendor (raw medical history, DNA), keep it out and verify locally.
106:- **Tier B (default):** sanitise names → roles, redact account / policy numbers, keep amounts and ages real (decision quality depends on real numbers).
107:- **Tier D — Health override:** no medical specifics, no DNA / genetic data in general bundles. Insurance/health decisions that **require** underwriting facts (pregnancy status, pre-existing conditions, waiting periods) get a Tier D restricted appendix with explicit consent each invocation OR Scott verifies the underwriting facts locally without piping to reviewers.
108:- **Tier D — Family override:** kids' names → K1–K4 (real ages preserved — dependency calculations matter), no school names; pregnancy described as "expecting, due ~Q{quarter} {year}" (mat-leave timing is load-bearing).
109:- **Minimum required for decision quality:** prefer derived ratios (debt-to-income, liability-to-asset, premium-to-cover) over raw amounts where the maths allows. Raw amounts only when the decision needs them (insurance premium maths, mat-leave hole sizing).
110:- **Salaries and account balances:** real values allowed in bundles by default; account *numbers* always redacted.
113:- Decisions → `journal/decisions/YYYY-MM-DD-{topic}.md` — **1-page summary** using the existing `protocols/decision-record-template.md`, with explicit link to `10-final-output.md` for full record
114:- Full investigation record → `journal/investigations/YYYY-MM-DD-{topic}/10-final-output.md` — alternatives considered, evidence used, dissent noted, privacy tier applied, follow-up tasks
121:`journal/investigations/YYYY-MM-DD-{topic}/`:
123:README.md  (current phase, status, last-touched, brief summary — for cold-start orientation)
144:**Bootstrap:** `bin/new-investigation.ps1 <topic-slug>` creates the folder, the empty 00–10 files, and the README. ~15 lines of PowerShell. Not the `/investigate` skill — just a folder-scaffold convenience.
148:**Folder:** `journal/investigations/2026-05-06-insurance-audit/` (bootstrapped via `bin/new-investigation.ps1`)
150:**Topic:** Mina has proposed insurance replacements; audit current coverage vs alternatives, decide what to drop / replace / restructure across life, income protection, TPD, trauma, home/contents, car (and any others Mina has flagged).
153:- Real salaries and ages (insurance maths)
156:- No medical history piped to reviewers — Scott verifies underwriting facts locally with insurer documents
157:- If a Tier D appendix is needed for a specific decision, explicit consent per invocation
159:**Underwriting verification:** Scott (with Mina) reads insurer PDS / underwriting questionnaires directly. Reviewers (Codex/Gemini) pressure-test the **decision logic** (which policy wins on which dimension, where the gaps are), not the **eligibility** (which is a yes/no from the insurer).
165:- `journal/decisions/2026-05-06-insurance-audit.md` — 1-page summary using `protocols/decision-record-template.md`, links back to `10-final-output.md`
172:**Trigger to build:** after at least one real investigation validates the manual workflow. If the insurance audit shows manual orchestration is fine and the bootstrap script covers the friction, defer further.
174:**Backlog:** V1–V14 from the RAIOS investigation outputs (`09-resolution.md` §G), plus any lessons captured from the insurance audit.
181:| Should exact salaries be in bundles or derived ratios? | Derived ratios where the question allows; raw values when the maths needs them. Captured in "minimum required" clause. |
182:| Who owns underwriting verification? | Scott + Mina + insurer documents. Reviewers test decision logic, not eligibility. |
190:1. `D:\PLAIOS\AGENTS.md` — drafted from the RAIOS template (structure only), customised for PLAIOS, adversarially reviewed before commit.
191:2. `D:\PLAIOS\protocols\multi-agent.md` — recipe + overlay.
192:3. `D:\PLAIOS\CLAUDE.md` — add the 1-line pointer to `AGENTS.md`.
193:4. `D:\PLAIOS\bin\new-investigation.ps1` — scaffold script.
194:5. Bootstrap the insurance audit folder via the script. Run phase 00 (topic intake).
195:6. Defer `/investigate` skill until the audit validates the manual workflow.
199:- The insurance audit completes through to a decision record. Reviewers materially change the decision logic at least once (otherwise the multi-agent overhead wasn't earned).
202:- Bundle minimisation rule observed: no raw account numbers, no medical history, no kids' names in any committed bundle.
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

 succeeded in 490ms:
5:> **Cross-tool baseline:** project conventions, multi-agent role rules, and privacy/threat-model rules live in `AGENTS.md` at the PLAIOS root — read by Claude Code, Codex CLI, and Gemini CLI alike. The multi-agent procedure (when to invoke, how to bundle, convergence rules) lives at `protocols/multi-agent.md`. **Don't duplicate either here.** This file is for Claude orchestration logic only.
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

 succeeded in 512ms:
5:**Reviewers:** Codex (adversarial) + Gemini (long-context / pattern cross-check) — see `journal/investigations/2026-05-06-multi-agent-procedure-design/`
16:Lift the load-bearing parts of the source recipe verbatim — CLI invocations, 10-phase investigation structure, evidence-bundle context firewall, token discipline, default workflow, variants. Layer PLAIOS-specifics on top: trigger rules for life-domain artefacts, privacy/threat-model rules, output destinations, investigation folder placement.
28:- **Output:** one binding artefact (decision record, procedure, recommendation), with dissent recorded but not sovereign
34:**Quality property — every agent gets it from a cold read.** The procedure document and `AGENTS.md` must each be readable by a model that has zero prior context and still let it understand: who it is in this system, what its role is for this invocation, what's allowed in the bundle, what response shape converges toward an outcome. KISS / irreducible complexity is the *test*, not the *aspiration*.
40:| `D:\PLAIOS\AGENTS.md` | NEW | Cross-tool baseline. Project description, conventions, multi-agent role conventions, privacy/threat-model rules, what NOT to do, where things live. Auto-picked-up by Codex CLI, Gemini CLI, and Claude Code. Self-contained for cold-start strangers. | All three CLIs |
41:| `D:\PLAIOS\CLAUDE.md` | MODIFY (+1 pointer line) | Existing content stays. New line near top: *"For project conventions and multi-agent role rules, see `AGENTS.md` — don't duplicate them here."* | Claude Code only |
42:| `D:\PLAIOS\protocols\multi-agent.md` | NEW | The recipe — core lifted from RAIOS `10-final-recipe.md` + PLAIOS overlay. One file, two clearly-delineated sections. | Humans + Claude when planning |
43:| `D:\PLAIOS\bin\new-investigation.ps1` | NEW | Tiny scaffold: takes `<topic-slug>`, creates `journal/investigations/YYYY-MM-DD-<slug>/` and the empty 00–10 files plus `README.md`. ~15 lines. | Humans |
44:| `D:\PLAIOS\journal\investigations\YYYY-MM-DD-{topic}\` | NEW (per investigation) | Folder-as-state-machine. 10-phase pattern. Includes `README.md` for current-phase / status tracking. | Audit trail |
52:**Note on adjacent code repos:** `D:\Plaios-tools\trading-tools\` and any future `plaios-tools` repos are **separate git repos**, not nested under PLAIOS. Each will have its own `AGENTS.md` at its repo root. No bleed-through risk; no precedence ambiguity.
54:## 4. `AGENTS.md` vs `CLAUDE.md` — separation of concerns
58:| Project description (PLAIOS = markdown reasoning system, no build/test/run for most domains) | AGENTS.md | All three CLIs need it |
59:| Multi-agent role conventions (evidence-bundle only, surgical edits, sub-85% confidence flagged, citations) | AGENTS.md | Codex/Gemini need it; Claude reads it too — single source |
60:| Privacy / threat-model rules (B default + D Health/Family + minimum-required clause + vendor-hosted disclosure) | AGENTS.md | Reviewer must know what's allowed in the bundle |
61:| Root-invocation rule (CLIs run from `D:\PLAIOS\`) | AGENTS.md | Cross-tool operational rule |
62:| What NOT to do (no scope creep, no speculative reasoning unflagged, no cross-domain aggregation unasked) | AGENTS.md | Cross-tool baseline |
63:| Where things live (domain map, journal, protocols, decisions) | AGENTS.md | All tools benefit |
65:| Privacy *principle* ("sensitive requires explicit navigation") | CLAUDE.md (existing) | Claude session-level rule; the *tier policy* lives in AGENTS.md |
68:**Drafting `AGENTS.md`:** start from `D:\RAIOS-outputs\...\12-AGENTS-template.md` as **structure**, not verbatim content. Customise PLAIOS-specific sections. Run a quick adversarial pass (Codex, evidence-bundle = drafted file) before committing.
73:- Where each model fits (Claude=driver, Codex=adversarial reviewer, Gemini=long-context/pattern channel)
84:- All multi-agent CLI invocations run from `D:\PLAIOS\` (the project root). Bundle file paths are relative to root. Why: ensures `AGENTS.md` is always loaded.
91:- Code work in `plaios-tools` / `trading-tools` (use RAIOS recipe directly via repo-local `AGENTS.md`)
95:- Single-domain memory updates that don't contradict anything
112:**Output destinations:**
119:## 6. Investigation folder structure (10-phase, single pattern)
137:**Single pattern, no "lite" variant.**
139:**Early termination semantics (NOT "n/a"):**
141:- Phase files past the termination point are **omitted** from the folder, OR if created they say *"Not reached. Investigation closed at phase N — see 07-disposition.md."*
144:**Bootstrap:** `bin/new-investigation.ps1 <topic-slug>` creates the folder, the empty 00–10 files, and the README. ~15 lines of PowerShell. Not the `/investigate` skill — just a folder-scaffold convenience.
148:**Folder:** `journal/investigations/2026-05-06-insurance-audit/` (bootstrapped via `bin/new-investigation.ps1`)
170:**Scope (when built):** automate folder scaffolding (currently `bin/new-investigation.ps1`), prompt templates per phase, evidence-bundle assembly, CLI orchestration to Codex/Gemini, sanitisation pre-flight check.
183:| Will adjacent code repos have their own `AGENTS.md`? | Yes — `plaios-tools`, `trading-tools` are separate repos with their own root `AGENTS.md`. No nesting under PLAIOS. |
190:1. `D:\PLAIOS\AGENTS.md` — drafted from the RAIOS template (structure only), customised for PLAIOS, adversarially reviewed before commit.
191:2. `D:\PLAIOS\protocols\multi-agent.md` — recipe + overlay.
192:3. `D:\PLAIOS\CLAUDE.md` — add the 1-line pointer to `AGENTS.md`.
193:4. `D:\PLAIOS\bin\new-investigation.ps1` — scaffold script.
201:- AGENTS.md is referenced by both Codex and Gemini in subsequent runs (verifiable via output content / behaviour).
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

codex
# Implementation Review

## Material concerns

1. **PowerShell CLI examples may fail in the user's primary shell.** Severity: serious.  
   `protocols/multi-agent.md:57-72` uses Bash-style stdin/heredoc examples. `cat` aliases in PowerShell, but `codex exec - < bundle.md` and `$(cat <<'EOF'...)` are not Windows PowerShell 5.1-safe. This undermines the root-invocation rule in `protocols/multi-agent.md:53`.  
   **Suggested fix:** add PowerShell-first examples, e.g. `Get-Content .\bundle.md -Raw | codex exec -` and `$prompt = @' ... '@; gemini --skip-trust -p $prompt`.

2. **AGENTS.md contradicts its own default sanitisation rule.** Severity: serious.  
   `AGENTS.md:49` says Tier B sanitises names to roles, but `AGENTS.md:12` names Scott and includes family-status facts in a file auto-loaded into every cross-tool invocation. This increases identity anchoring and makes every Codex/Gemini run include personal context whether needed or not.  
   **Suggested fix:** change line 12 to role-based language, e.g. “Primary user: Australian software executive; household obligations are load-bearing context and should be bundled only when relevant under the privacy rules.” Keep specific family facts in Claude-local memory or explicit Tier D bundles.

3. **Default workflow trigger conflicts with OUT rules.** Severity: minor.  
   `protocols/multi-agent.md:33` says “any task more than a one-line edit,” but `protocols/multi-agent.md:132-138` excludes tasks under 30 minutes and tactical/reversible work. A cold-start agent could over-invoke multi-agent review.  
   **Suggested fix:** rename the heading to “The default workflow for in-scope multi-agent work” and leave the OUT list authoritative.

4. **Scaffold script assumes correct root and unvalidated slug.** Severity: minor.  
   `bin/new-investigation.ps1:11` builds a relative path from raw `$Slug`. Running outside root or passing path separators could create the wrong folder shape.  
   **Suggested fix:** add a root preflight (`Test-Path .\AGENTS.md` and `.\journal\investigations`) and reject slugs outside `[a-z0-9-]+`.

## Things that are fine

- Convergence framing lands in both files: `AGENTS.md:25,32,35` and `protocols/multi-agent.md:9-19,102-110`.
- 10-phase scaffold matches the procedure: `protocols/multi-agent.md:87-100` and `bin/new-investigation.ps1:20-44`.
- README seed includes a convergence target: `bin/new-investigation.ps1:64-66`.
- Spec alignment is broadly intact: privacy rules match `docs/...design.md:105-110`; output destinations match `docs/...design.md:112-115`; single-track investigation shape matches `docs/...design.md:119-144`.
- Cross-temporal integration is clean: no contradiction found with `decision-record-template.md`, `session-checklist.md`, or `assessment-template.md`.

## Things you'd do differently but could go either way

- Cut the “Source lifted from RAIOS” line in `protocols/multi-agent.md:3` after shipping; useful during implementation, not load-bearing for future cold starts.
- Keep `AGENTS.md` closer to pure operating rules and move biographical context to Claude-local orchestration/memory.

## Ship verdict

**ship-after-fixes** — the procedure is structurally sound, but PowerShell-safe invocation examples and the AGENTS.md privacy/self-identification conflict should be fixed before using this on the insurance audit.
tokens used
59,855
# Implementation Review

## Material concerns

1. **PowerShell CLI examples may fail in the user's primary shell.** Severity: serious.  
   `protocols/multi-agent.md:57-72` uses Bash-style stdin/heredoc examples. `cat` aliases in PowerShell, but `codex exec - < bundle.md` and `$(cat <<'EOF'...)` are not Windows PowerShell 5.1-safe. This undermines the root-invocation rule in `protocols/multi-agent.md:53`.  
   **Suggested fix:** add PowerShell-first examples, e.g. `Get-Content .\bundle.md -Raw | codex exec -` and `$prompt = @' ... '@; gemini --skip-trust -p $prompt`.

2. **AGENTS.md contradicts its own default sanitisation rule.** Severity: serious.  
   `AGENTS.md:49` says Tier B sanitises names to roles, but `AGENTS.md:12` names Scott and includes family-status facts in a file auto-loaded into every cross-tool invocation. This increases identity anchoring and makes every Codex/Gemini run include personal context whether needed or not.  
   **Suggested fix:** change line 12 to role-based language, e.g. “Primary user: Australian software executive; household obligations are load-bearing context and should be bundled only when relevant under the privacy rules.” Keep specific family facts in Claude-local memory or explicit Tier D bundles.

3. **Default workflow trigger conflicts with OUT rules.** Severity: minor.  
   `protocols/multi-agent.md:33` says “any task more than a one-line edit,” but `protocols/multi-agent.md:132-138` excludes tasks under 30 minutes and tactical/reversible work. A cold-start agent could over-invoke multi-agent review.  
   **Suggested fix:** rename the heading to “The default workflow for in-scope multi-agent work” and leave the OUT list authoritative.

4. **Scaffold script assumes correct root and unvalidated slug.** Severity: minor.  
   `bin/new-investigation.ps1:11` builds a relative path from raw `$Slug`. Running outside root or passing path separators could create the wrong folder shape.  
   **Suggested fix:** add a root preflight (`Test-Path .\AGENTS.md` and `.\journal\investigations`) and reject slugs outside `[a-z0-9-]+`.

## Things that are fine

- Convergence framing lands in both files: `AGENTS.md:25,32,35` and `protocols/multi-agent.md:9-19,102-110`.
- 10-phase scaffold matches the procedure: `protocols/multi-agent.md:87-100` and `bin/new-investigation.ps1:20-44`.
- README seed includes a convergence target: `bin/new-investigation.ps1:64-66`.
- Spec alignment is broadly intact: privacy rules match `docs/...design.md:105-110`; output destinations match `docs/...design.md:112-115`; single-track investigation shape matches `docs/...design.md:119-144`.
- Cross-temporal integration is clean: no contradiction found with `decision-record-template.md`, `session-checklist.md`, or `assessment-template.md`.

## Things you'd do differently but could go either way

- Cut the “Source lifted from RAIOS” line in `protocols/multi-agent.md:3` after shipping; useful during implementation, not load-bearing for future cold starts.
- Keep `AGENTS.md` closer to pure operating rules and move biographical context to Claude-local orchestration/memory.

## Ship verdict

**ship-after-fixes** — the procedure is structurally sound, but PowerShell-safe invocation examples and the AGENTS.md privacy/self-identification conflict should be fixed before using this on the insurance audit.
EXIT_CODE=0
