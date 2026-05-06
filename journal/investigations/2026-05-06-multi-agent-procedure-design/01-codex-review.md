OpenAI Codex v0.128.0 (research preview)
--------
workdir: D:\PLAIOS\journal\investigations\2026-05-06-multi-agent-procedure-design
model: gpt-5.5
provider: openai
approval: never
sandbox: read-only
reasoning effort: none
reasoning summaries: none
session id: 019dfc72-ee2a-78a0-8b4d-1bbbf5136f66
--------
user
# Multi-Agent Development Procedure for PLAIOS — Design Bundle for Review

**Date:** 2026-05-06
**Author:** Claude (in-session with Scott McKennie)
**Reviewers requested:** Codex (adversarial) + Gemini (long-context / pattern cross-check)
**Status:** Pre-shipping. Not yet committed to PLAIOS.

---

## What you (the reviewer) need to know up front

This is a **design review**, not a code review. The artefact under review is a procedure proposal — how PLAIOS (a personal life knowledge / decision system) should adopt multi-agent development practices that were ratified for ICX (a software org) in a prior `/investigate` dry-run.

You are being invoked because the recipe being adopted *says* artefacts of this kind (durable, consequential, affects all future workflow) should be reviewed adversarially before shipping. Eating own dog food.

**Privacy of this bundle:** No personal financial / medical / family data is included. The design itself is the only content. Privacy tier B is trivially satisfied.

---

## 1. Context

### What PLAIOS is

PLAIOS = Personal Life AI Operating System. A markdown-heavy, single-user knowledge and decision system at `D:\PLAIOS\`. Owner: Scott McKennie, CEO of an Australian software org (RapidMap / ICX), father of four (fifth on the way), based in Australia.

PLAIOS is **not a codebase**. It is a reasoning system. The work product is decisions, memory, procedures, cross-domain syntheses. Two adjacent code repos (`plaios-tools/`, `trading-tools/`) exist for instrumentation but are out of scope for the procedure being designed — they'll use the unmodified RAIOS recipe with their own per-repo `AGENTS.md`.

PLAIOS structure:
- `domains/` — life-domain folders (health, finance, family, home, relationships, growth, coaching, ai-ml, trading)
- `protocols/` — rules and templates (session checklist, decision-record template, assessment template)
- `journal/` — time-stamped audit trail (`session-log.md`, `decisions/`, and proposed `investigations/`)
- `docs/superpowers/specs/` and `docs/superpowers/plans/` — design docs and plans for major work
- `CLAUDE.md` — project-level Claude instructions (identity, hierarchy of needs, maturity scale, domain map, priority algorithm, escalation rules, session protocol, privacy principle, systems-thinking framework)
- `memory/` — accumulated cross-session knowledge (separate location, mirrored to repo on close-out)

### The source recipe

A 3-model `/investigate` dry-run conducted 2026-05-05 produced a ratified multi-agent dev recipe at `D:\RAIOS-outputs\investigations\multi-agent-dev-practices-20260505-2237\`. Key files:
- `10-final-recipe.md` — distributable recipe (CLI invocations, default workflow, bug-fix variant, decision variant, when NOT to use)
- `11-instruction-manual.md` — full manual including section 9 on RAIOS-style non-code work
- `12-AGENTS-template.md` — drop-in template for `AGENTS.md` at repo root, picked up automatically by Claude Code, Codex CLI, and Gemini CLI

Core principle of the source recipe: **roles are task assignments, not personalities.** Claude drives. Codex is invoked for adversarial review at risk points. Gemini is invoked for long-context / external-pattern questions. Each model runs in its own context window. The developer (or PLAIOS owner) is the orchestrator — passes artefacts (spec, diff, test output, bundle) between them via CLI.

The investigation explicitly argues against using all three on every task. Pick the channel by risk. The trigger rule for non-code work: invoke multi-agent when the artefact is **durable** (decisions, procedures, memory updates, cross-domain briefs); skip for ephemeral artefacts.

### What's being decided here

Whether and how to adopt that recipe inside PLAIOS, given that:
1. PLAIOS is mostly non-code reasoning (closer to RAIOS than ICX in nature)
2. Owner wants strict separation: `CLAUDE.md` for Claude orchestration logic, `AGENTS.md` for the cross-tool baseline that other agents pick up
3. Owner wants an `/investigate` skill eventually, but not as a prerequisite — manual orchestration first, skill earns the right to be built after at least one real run validates the workflow
4. First validating run will be an insurance audit (durable, consequential, cross-domain — Finance + Family + Home)

---

## 2. The design

### Approach chosen: "Core + PLAIOS overlay"

Lift the load-bearing parts of the source recipe verbatim (CLI invocations, 10-phase structure, evidence-bundle context firewall, token discipline, default workflow, variants). Layer PLAIOS-specifics on top: trigger rules for life-domain artefacts, privacy tiering, output destinations, investigation folder placement.

Rejected alternatives:
- Faithful port of the RAIOS recipe with no overlay — written for code/RAIOS work; PLAIOS-specific framing (life domains, hierarchy of needs, privacy tiering for personal data) doesn't transfer cleanly
- PLAIOS-tailored from scratch — doubles the work, risks drift from the version Scott uses at ICX, over-fits to the insurance audit example

### File layout

| File / folder | Purpose | Audience |
|---|---|---|
| `D:\PLAIOS\AGENTS.md` (NEW) | Cross-tool baseline. Project description, conventions, multi-agent role conventions, privacy tier policy, what NOT to do, where things live. Auto-picked-up by Codex CLI, Gemini CLI, and Claude Code. Self-contained (a stranger model lands cold and understands what to do). | All three CLIs |
| `D:\PLAIOS\CLAUDE.md` (existing, +1 pointer line) | Identity, hierarchy of needs, maturity scale, domain map, priority algorithm, escalation rules, session protocol, privacy *principle*, systems-thinking framework. New pointer: *"For project conventions and multi-agent role rules, see `AGENTS.md` — don't duplicate them here."* Sub-agent definitions and skill bindings stay here. | Claude Code only |
| `D:\PLAIOS\protocols\multi-agent.md` (NEW) | The recipe — core lifted verbatim from RAIOS `10-final-recipe.md` + PLAIOS overlay (trigger rules, privacy tier, output destinations). One file, two clearly-delineated sections. Read by humans triggering the workflow. | Humans + Claude when planning |
| `D:\PLAIOS\journal\investigations\YYYY-MM-DD-{topic}\` (NEW) | Folder-as-state-machine. 10-phase pattern, mirrors RAIOS investigation outputs but lives inside PLAIOS git repo (private, single-user). | Audit trail |
| `D:\PLAIOS\journal\decisions\` (existing, empty) | Final decision records promoted here when an investigation produces a binding outcome. Uses existing `protocols/decision-record-template.md`. | Long-term decision log |
| `D:\PLAIOS\docs\superpowers\specs\2026-05-06-plaios-multi-agent-design.md` (NEW) | The spec for this design itself. | Reference / brainstorm artefact |
| `D:\PLAIOS\.claude\skills\investigate\` (DEFERRED) | Empty for now. Built in v2 only after at least one real investigation validates the manual workflow. | Claude Code only |

Two specific calls:
- **Recipe is one file, not two.** "Core + overlay" is a mental model, not a file split. Reduces "which file?" friction at use time.
- **Investigation folders live under `journal/investigations/`** (not a separate `D:\PLAIOS-outputs\` like RAIOS). PLAIOS is private, single-user, one git history.

### `AGENTS.md` vs `CLAUDE.md` separation

| Content | Lives in | Why |
|---|---|---|
| Project description (PLAIOS = markdown reasoning system, no build/test/run for most domains) | AGENTS.md | All three CLIs need it |
| Multi-agent role conventions (evidence-bundle only, surgical edits, sub-85% confidence flagged, citations) | AGENTS.md | Codex/Gemini need it; Claude reads it too — single source |
| Privacy tier rules (B default + D Health/Family) | AGENTS.md | Reviewer must know what's allowed in the bundle |
| What NOT to do (no scope creep, no speculative reasoning unflagged, no cross-domain aggregation unasked) | AGENTS.md | Cross-tool baseline |
| Where things live (domain map, journal, protocols, decisions) | AGENTS.md | All tools benefit |
| Identity, hierarchy of needs, maturity scale, priority algorithm, escalation rules, session protocol, systems-thinking framework | CLAUDE.md | Claude orchestration logic; not relevant to a one-shot Codex review |
| Privacy *principle* ("sensitive requires explicit navigation") | CLAUDE.md | Claude session-level rule; the *tier policy* lives in AGENTS.md |
| Sub-agent definitions, skill bindings (close-out, future /investigate) | CLAUDE.md | Claude-only |

`AGENTS.md` template will be lifted verbatim from RAIOS `12-AGENTS-template.md` with bracketed sections customised for PLAIOS — no rewriting.

### `protocols/multi-agent.md` content (one file)

**Top half — lifted verbatim from RAIOS `10-final-recipe.md`:**
- Where each model fits (Claude=driver, Codex=adversarial reviewer, Gemini=long-context/pattern channel)
- Default workflow: Plan → Implement → Verify → Review (by risk) → Narrate → Close out
- Bug-fix variant (failing test first, fix, Codex review)
- Decision variant (multi-model deliberation via `/investigate`, no code, output is a decision record)
- CLI invocations (`codex exec - < bundle.md`; `gemini --skip-trust -p ...`)
- Token discipline (250k per session)
- When NOT to do this (one-line edits, <30min tasks, pure exploration)

**Bottom half — PLAIOS overlay:**

Trigger rules — multi-agent IN:
- Durable decisions in life domains (insurance, schools, property, fertility/baby planning, vendor switches)
- Cross-domain syntheses ("where am I structurally weak?")
- Memory updates that contradict prior memories
- Skill / procedure design changes
- Code work in `plaios-tools` / `trading-tools` (use RAIOS recipe directly via repo-local `AGENTS.md`)

Trigger rules — multi-agent OUT:
- Routine state reads, daily journal lines
- Single-domain memory updates that don't contradict anything
- Tactical PocketSmith tweaks, calendar events, gmail drafts
- Anything ephemeral

Privacy tier (B default + D Health/Family):
- Default: sanitise names → roles, redact account / policy numbers, keep amounts and ages **real** (decision quality depends on real numbers)
- Override for Health: no medical specifics, no DNA / genetic info
- Override for Family: kids' names → K1–K4 (real ages preserved — dependency calculations matter), no school names; pregnancy described as "expecting, due ~Q{quarter} {year}" (mat-leave timing is load-bearing)
- Salaries and account balances real, account *numbers* redacted

Output destinations:
- Decisions → `journal/decisions/YYYY-MM-DD-{topic}.md` using `protocols/decision-record-template.md`
- Procedures → `protocols/`
- Memory → memory dir (close-out skill handles)
- Skill specs → `docs/superpowers/specs/`

### Investigation folder structure (10-phase, single pattern)

`journal/investigations/YYYY-MM-DD-{topic}/`:
```
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
10-final-output.md  (decision record / procedure / recipe — promoted to its destination)
```

**Single pattern, no "lite" variant.** Phases that don't apply (e.g. mediation when there's no disagreement) get a 1-line "n/a — no disagreement, disposition stands" file. Two mental models doubles cognitive load; the trigger rules already filter out the trivial cases.

### Insurance audit (the validating worked example)

- Folder: `journal/investigations/2026-05-06-insurance-audit/`
- Topic: Mina has proposed insurance replacements; audit current coverage vs alternatives, decide what to drop / replace / restructure
- Privacy: salaries and ages real (insurance maths), Mina described as "expecting, due ~Q4 2026" (mat-leave timing load-bearing for life/IP), kids as K1–K4 with real ages, no medical history (none active right now)
- Pre-flight: verify Codex and Gemini installed and authenticated (already verified for this design review)
- Final output: decision record at `journal/decisions/2026-05-06-insurance-audit.md` + any policy-switch tasks

### `/investigate` skill v2 — deferred

Scope: automate folder scaffolding, prompt templates per phase, evidence-bundle assembly, CLI orchestration to Codex/Gemini, sanitisation pre-flight check.

Built only if the manual run earns it. If insurance audit shows manual orchestration is fine, defer further. Backlog: V1–V14 from the RAIOS investigation as starting items, plus any lessons from the insurance audit.

---

## 3. Specific questions for the reviewer

### For Codex (adversarial)
1. Where will this break in practice? Any load-bearing assumption you can identify that isn't stated?
2. The `AGENTS.md` self-containment claim ("a stranger model lands cold and understands what to do") — what's the failure mode if a future Codex/Gemini invocation runs from a *subdirectory* of PLAIOS (e.g., `domains/finance/`) and only picks up a more local context? Is the design robust to that?
3. The "single 10-phase pattern, skip empty phases with 1-line n/a" rule — does this hold up for an investigation that genuinely should have stopped at phase 4 (e.g., research is conclusive, no deliberation needed)? Is "skip with n/a" the right answer or does it create a false audit trail?
4. Privacy tier B+D — any obvious hole? E.g., is keeping real ages for kids while sanitising names actually a meaningful sanitisation, given Scott's role and the Australian context could re-identify trivially?
5. Trigger rules — anything in the IN list that's actually ephemeral, or anything in the OUT list that's actually durable?
6. The decision to not build the `/investigate` skill yet — premature deferral, or correct YAGNI?
7. Anything else that would catch you off-guard if you executed this procedure cold next week?

### For Gemini (long-context / pattern)
1. Does this PLAIOS adaptation match the **intent** of the original RAIOS investigation (see `D:\RAIOS-outputs\investigations\multi-agent-dev-practices-20260505-2237\11-instruction-manual.md`), or has anything load-bearing been lost in translation?
2. How do other single-user knowledge / decision systems (Obsidian / Logseq with AI plugins, Roam, Tana, personal Zettelkasten setups) handle multi-agent integration? Is there a known better-practice pattern we're missing?
3. The "AGENTS.md at root + CLAUDE.md as Claude-specific overlay" pattern — is this how other multi-tool repos in the wild are organising it, or is there a more canonical convention emerging?
4. The 10-phase investigation pattern (lifted from RAIOS) — is it well-suited to **personal** decision-making (insurance, schools, etc.), or is it too heavy / oriented toward organisational decisions?
5. Cross-temporal coherence: Scott already has memory entries (see CLAUDE.md memory index in his system) about prior PLAIOS choices. Does the proposed design contradict any pattern PLAIOS has already established in `protocols/` or `domains/*/CLAUDE.md`?
6. Is there a simpler shape that achieves 80% of the goal? KISS lens.

---

## 4. Response format requested

Concise. Cite specific section / paragraph of this bundle when raising a concern. Tag uncertain claims `[uncertain]`. Sub-85% confidence flagged. No flattery, no LGTM-style approvals — if the design is fine, say "no material concerns" and stop.

Output structure:
```
# Review

## Material concerns
[numbered list, each with: concern, where in bundle, severity (block / serious / minor), suggested fix]

## Things that are fine
[bullet list — short]

## Things you'd do differently but could go either way
[bullet list — short]

## Open questions back to the orchestrator
[numbered list]
```

codex
I’ll treat this as the Codex adversarial pass and ground it in the bundle you provided. I’ll also do a quick read-only check of the referenced local files where available so I’m not reviewing the adaptation entirely from memory.
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-ChildItem -Path 'D:\\PLAIOS\\protocols' -Force | Select-Object -ExpandProperty Name" in D:\PLAIOS\journal\investigations\2026-05-06-multi-agent-procedure-design
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Test-Path 'D:\\RAIOS-outputs\\investigations\\multi-agent-dev-practices-20260505-2237\\10-final-recipe.md'; Test-Path 'D:\\RAIOS-outputs\\investigations\\multi-agent-dev-practices-20260505-2237\\11-instruction-manual.md'; Test-Path 'D:\\RAIOS-outputs\\investigations\\multi-agent-dev-practices-20260505-2237\\12-AGENTS-template.md'; Test-Path 'D:\\PLAIOS\\CLAUDE.md'; Test-Path 'D:\\PLAIOS\\protocols\\decision-record-template.md'" in D:\PLAIOS\journal\investigations\2026-05-06-multi-agent-procedure-design
 succeeded in 641ms:
True
True
True
True
True
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

 succeeded in 692ms:
assessment-template.md
decision-record-template.md
session-checklist.md
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

codex
The referenced recipe/manual/template files and PLAIOS protocol files are present. I’m checking only the load-bearing structure now: whether the proposed overlay preserves source intent and whether existing PLAIOS protocols imply a conflicting shape.
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'rg -n "''^(#|##|###)|When NOT|token|Codex|Gemini|decision|non-code|RAIOS" '"'D:\\RAIOS-outputs\\investigations\\multi-agent-dev-practices-20260505-2237\\10-final-recipe.md'" in D:\PLAIOS\journal\investigations\2026-05-06-multi-agent-procedure-design
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'rg -n "''^(#|##|###)|non-code|decision|durable|RAIOS|investigate|privacy|AGENTS|CLAUDE" '"'D:\\RAIOS-outputs\\investigations\\multi-agent-dev-practices-20260505-2237\\11-instruction-manual.md'" in D:\PLAIOS\journal\investigations\2026-05-06-multi-agent-procedure-design
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'rg -n "''^(#|##|###)|Project|Privacy|multi-agent|Codex|Gemini|Claude|Where things live|Do not|confidence|citation" '"'D:\\RAIOS-outputs\\investigations\\multi-agent-dev-practices-20260505-2237\\12-AGENTS-template.md'" in D:\PLAIOS\journal\investigations\2026-05-06-multi-agent-procedure-design
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'rg -n "''^(#|##|###)|Decision|Status|Context|Consequences|Review|Template" '"'D:\\PLAIOS\\protocols\\decision-record-template.md' 'D:\\PLAIOS\\protocols\\session-checklist.md' 'D:\\PLAIOS\\protocols\\assessment-template.md'" in D:\PLAIOS\journal\investigations\2026-05-06-multi-agent-procedure-design
 succeeded in 830ms:
1:# ICX Multi-Agent Development Recipe
7:## Where each model fits
12:| **Codex** (`codex exec`) | **Adversarial reviewer.** Invoked on demand. | Different model, different blind spots — catches what same-model review misses. |
13:| **Gemini** (`gemini -p`) | **Long-context / external pattern channel.** Invoked on demand. | Long context window + different training — useful when the question is "is this how it's done elsewhere?" or "what does this entire file do." |
19:## The recipe (default workflow, any task more than a one-line edit)
32:   | Risky / shared module / performance-sensitive | **Codex** | Independent model = catches what Claude missed |
33:   | "Is this how it's done elsewhere?" / architectural question | **Gemini** | Long context + external pattern view |
39:6. **Close out** when the session approaches 200-250k tokens or spans days. Write a capsule: objective, decision, files changed, tests run, unresolved risks, exact next step. Diff-verify before reuse.
43:## How to actually invoke Codex and Gemini
45:**Codex (adversarial review):**
48:# build the evidence bundle (no chat history)
51:# invoke Codex with the bundle on stdin
55:**Gemini (long-context / pattern question):**
69:## For bugs (the variant)
71:1. **Reproduce first.** Either Claude Code or Codex writes a **failing test** that demonstrates the bug. Run it. It must fail as expected. **No fix is permitted until this test exists and fails.**
73:3. **Adversarial review with Codex.** Bundle = spec + diff + test output. Codex attacks for hallucinated assumptions, hidden complexity, missing edge cases.
78:## For architectural / irreversible decisions (not code)
80:Don't write code. Use **multi-model deliberation** — `/investigate` (or `/council`) — across Claude + Codex + Gemini. Output is a decision record, not a diff. Trigger when rollback cost exceeds the deliberation cost: schema migration, vendor selection, breaking API change.
84:## Worked example — CPD-5623 SWIFT JS race
86:1. **Reproduce.** Ask Codex (or Claude Code) to write a failing test that triggers the race. Test fails. Capture it.
88:3. **Adversarial review.** Pipe `spec.md + diff + test output` to Codex. Codex looks for hallucinated assumptions, fragile sequencing, perf regressions.
95:## Token discipline
97:Each model session stays under ~250k tokens by design. **No model ever holds the whole picture** — you pass small, curated artifacts between them. Full repo dumps are forbidden. If a session approaches the ceiling, close it out with a capsule and start fresh.
101:## When NOT to do this
109:## What to track per task
113:- Reviewer used: Claude / Codex / Gemini / none
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

 succeeded in 819ms:
D:\PLAIOS\protocols\decision-record-template.md:1:# Decision: [Title]
D:\PLAIOS\protocols\decision-record-template.md:5:**Context:** [What prompted this decision]
D:\PLAIOS\protocols\decision-record-template.md:7:**Decision:** [What was decided and why]
D:\PLAIOS\protocols\decision-record-template.md:9:**Review Date:** [When to check if it worked]
D:\PLAIOS\protocols\session-checklist.md:1:# Session Checklist
D:\PLAIOS\protocols\session-checklist.md:3:## Opening
D:\PLAIOS\protocols\session-checklist.md:12:## Closing
D:\PLAIOS\protocols\assessment-template.md:1:# Assessment Template
D:\PLAIOS\protocols\assessment-template.md:8:**Next Review:** YYYY-MM-DD
D:\PLAIOS\protocols\assessment-template.md:14:**Overall Domain Status:** [Crisis / Fragile / Functional / Systematic / Optimised]
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

 succeeded in 821ms:
1:# AGENTS.md template
3:**Purpose:** drop-in template for any RapidMap repo (RMAPP, SWIFT, Summit, RAIOS, etc.) so that Claude Code, Codex, and Gemini all pick up the same project context when invoked from the working directory.
7:**Why this file exists:** all three CLIs read `AGENTS.md` from the working directory automatically (Claude Code via fallback; Codex CLI as canonical; Gemini CLI in recent versions). One file, three tools, no drift. Roles are assigned at invocation time in the prompt — *not* in this file. This file describes the *project*, not the *agents*' personalities.
12:# AGENTS.md
14:## Project
25:## Conventions
34:## Multi-agent role conventions
36:When you (Claude / Codex / Gemini) are invoked in this repo:
45:## What NOT to do
53:## Where things live
58:- Multi-agent recipe: [link to `procedures/multi-agent-development.md`]
60:## When to escalate
64:- If the work touches [list of sensitive areas — e.g., authentication, payments, customer data], mandatory red-team review (Codex) before merge.
69:## Notes for adapters
73:3. **Roles are NOT in this file.** When you invoke Codex for adversarial review, the prompt says "review this bundle for X." Codex reads `AGENTS.md` for project context but takes its role from the prompt. This is deliberate — roles change, project context is stable.
76:6. **CLAUDE.md alongside is fine.** Claude Code reads both. Use CLAUDE.md for Claude-Code-specific extensions (sub-agent definitions, skill bindings) and AGENTS.md for the cross-tool baseline.
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

 succeeded in 828ms:
1:# Multi-Agent Development — Instruction Manual
3:**Audience:** Scott; ICX developers (Hoang, Kun); RAIOS operators (current and future).
4:**Scope:** how to use Claude + Codex + Gemini together as a development and reasoning practice — for code (delivery-icx) and for RAIOS work itself.
5:**Source:** RAIOS /investigate dry-run, 2026-05-05. Ratified by all three deliberating models.
10:## 1. The principle
16:## 2. Where each model fits
20:| **Claude (Claude Code)** | Driver | Native sub-agents, plan mode, file pinning, agentic loops, RAIOS MCP access | Always. Holds the session, writes the code or the brief, runs verification. |
22:| **Gemini (`gemini -p`)** | Long-context / pattern channel | Larger context window; different training; useful for "is this how it's done elsewhere?" or "does this match prior decisions?" | When the question is about external patterns, prior decisions, or long-context coherence. |
26:## 3. The default recipe (any task more than a one-line edit)
36:6. **Close out** when the session approaches 200-250k tokens or spans multiple sittings. Write a capsule: objective, decision, files changed, tests run, unresolved risks, exact next step. Diff-verify before reuse.
40:## 4. CLI invocations
42:### Codex (adversarial review)
45:# build the evidence bundle
48:# pipe via stdin (NOT positional argument — that pattern hangs)
52:### Gemini (long-context / pattern question)
62:### Claude Code
64:Open in the relevant repo. The CLI picks up `AGENTS.md` and `CLAUDE.md` from the working directory automatically.
66:## 5. Bug-fix variant (the "investigator-fixer-reviewer" chain)
73:## 6. Architectural / irreversible-decision variant
75:For decisions where rollback cost exceeds the deliberation cost — schema migrations, vendor selection, breaking API changes, structural RAIOS choices — don't write code. Use **multi-model deliberation** via `/investigate` or `/council`. Output is a decision record, not a diff. Three models deliberate; orchestrator consolidates; speakers ratify in mediation; resolution is binding.
77:## 7. The `AGENTS.md` pattern
79:Every repo where multi-agent dev happens needs an `AGENTS.md` at the root. All three CLIs pick it up automatically when invoked from that working directory.
89:Template: see `12-AGENTS-template.md` in this folder.
91:`CLAUDE.md` can layer on top for Claude-Code-specific extensions (sub-agent definitions, skill bindings). `AGENTS.md` is the cross-tool baseline.
93:## 8. For ICX development
106:| Architectural decision | §6 (multi-model deliberation) | Schema migration, vendor selection, breaking API. |
118:## 9. For RAIOS work itself
120:**Repos:** the RAIOS root (`D:/RAIOS/`) and per-domain repos (`domains/{name}/`). Work product is reasoning artefacts (briefs, decisions, procedures, memory, skills, syntheses) more than code.
122:**Why multi-agent is *more* valuable for RAIOS than for code:**
124:The work product is reasoning. Reasoning fails in ways code doesn't — sycophancy, groupthink, unfounded confidence, contradiction with prior decisions, missing cross-domain implications. Single-model review tends to miss exactly these failures because they're rooted in how the model produced the artefact in the first place. Independent-model challenge is the practical mitigation.
126:**The trigger rule for RAIOS:**
128:> Invoke multi-agent review when the artefact is **durable** (decision record, procedure, memory update, skill design, cross-domain brief). Don't bother for **ephemeral** artefacts (work-log rows, routine state reads, daily journal entries, dispatch directives).
130:**RAIOS-specific applications:**
134:| **Decision record** (`journal/decisions/`) | Drafts the record | Audits the rationale chain — gaps, weak evidence, hidden assumptions | Cross-checks against prior decisions, journal log; flags contradictions |
135:| **Procedure** (`procedures/`) | Drafts the procedure | Audits for completeness, edge cases, contradictions with existing procedures | Cross-checks against established RAIOS conventions |
137:| **Strategic Command synthesis** (cross-domain brief) | Reads published state, drafts brief | Audits logical chain — what claim is unsupported? | Cross-checks against journal, historical decisions, prior briefs |
139:| **Investigation runs** (`/investigate`) | Orchestrates phases | Acts as deliberator | Acts as deliberator |
140:| **Proposals** (`journal/proposals/`) | Reads, evaluates, drafts response | Audits the proposal's logic | Cross-checks against existing procedures / prior decisions |
142:**The pattern in RAIOS terms:**
145:Claude (with RAIOS MCP access)
168:`/investigate` is the RAIOS instantiation of multi-agent development applied to non-code work. The 8-phase + mediation structure (now 10 phases with the mediation addition) IS the RAIOS multi-agent recipe. So "how does multi-agent work for RAIOS?" answers in part: *like /investigate, generalised across more work products*.
170:**Concrete pilot for RAIOS:**
172:1. **Use multi-agent review on the next consequential RAIOS decision record** — pick the next decision Scott would have logged anyway, route it through the Claude → Codex → Gemini chain. Compare what the multi-agent review surfaced vs what single-Claude review would have missed.
173:2. **Use `/investigate` on the next deferred secondary thread** — Scott's RAIOS multi-agent system architecture question (the original O1). Validates v1 → v2 path on a contested topic before codifying.
174:3. **Pilot the AGENTS.md template at the RAIOS root** — drop a `RAIOS-tailored AGENTS.md` at `D:/RAIOS/AGENTS.md` so Codex/Gemini invocations from inside RAIOS pick up project context automatically. Test on the next session.
176:## 10. When NOT to use multi-agent
183:The multi-agent recipe is for **durable, consequential, or risky** work. Default to single-Claude-Code for everything else.
185:## 11. How to extend
192:4. **New trigger rules** — if a class of work emerges that benefits from multi-agent but isn't covered by the current trigger rules (durable / consequential / irreversible), add it to §8 or §9.
196:## 12. References
207:- `12-AGENTS-template.md` — AGENTS.md drop-in template
209:**v2 work items (V1-V14)** — for codifying `/investigate` as a real skill. See `09-resolution.md` §G.
211:**Related RAIOS files:**
212:- `journal/proposals/procedures/20260505-scott-investigate-skill-design.md` — original /investigate v1 spec (now superseded by the dry-run findings)
214:- `domains/delivery-icx/CLAUDE.md` — domain context for ICX
Cannot set property. Property setting is supported only on core types in this language mode.
At line:1 char:1
+ [Console]::OutputEncoding=[System.Text.Encoding]::UTF8;
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException
    + FullyQualifiedErrorId : PropertySetterNotSupportedInConstrainedLanguage
 

codex
# Review

## Material concerns

1. **Subdirectory invocation can silently drop the root contract**
   **Where:** File layout, `AGENTS.md`; specific Codex Q2; source claim “auto-picked-up”.
   **Severity:** serious.
   **Concern:** The design assumes root `D:\PLAIOS\AGENTS.md` is reliably loaded. If Codex/Gemini/Claude are invoked from `domains/finance/`, behavior may differ by CLI/version/config. Even if ancestor lookup works today, it is a brittle operational dependency.
   **Suggested fix:** Make the procedure state: “Invoke review CLIs from `D:\PLAIOS\` unless an evidence bundle explicitly includes `AGENTS.md`.” Also add tiny local `AGENTS.md` stubs in major subtrees only if needed, each saying “root context is authoritative; run from repo root.”

2. **The 10-phase pattern needs an explicit early-stop state**
   **Where:** “Investigation folder structure”; “Single pattern, no lite variant.”
   **Severity:** serious.
   **Concern:** Filling phases 6-9 with `n/a` after phase 4 research conclusively answers the question can create a misleading audit trail: it looks like deliberation was considered and skipped procedurally, not that the investigation terminated by evidence.
   **Suggested fix:** Keep the single folder pattern, but add a formal phase-gate rule: `07-disposition.md` may say `closed at phase 4: conclusive research; no deliberation warranted`. Later files should be named or worded as “not reached”, not “n/a”. That preserves audit truth without introducing a lite variant.

3. **Privacy tier B+D lacks a threat model**
   **Where:** “Privacy tier (B default + D Health/Family)”; insurance audit example.
   **Severity:** block for real insurance run until clarified.
   **Concern:** “Sanitise names, keep real ages/amounts” is not enough by itself. Given Scott’s public role, Australian context, four kids plus pregnancy timing, real ages may be re-identifying. Real salaries, balances, insurance premiums, and benefit amounts are also highly sensitive even without account numbers.
   **Suggested fix:** Define threat model explicitly: local-only agents vs vendor-hosted model calls vs saved repo artefacts. Add a rule that Tier D bundles get the minimum required detail per model. For example, Codex reviewing procedure logic may not need exact salary; insurance decision modelling may need exact benefit amounts. Store unsanitised source material separately from shareable review bundles.

4. **Health redaction may conflict with insurance decision quality**
   **Where:** “Override for Health: no medical specifics”; insurance audit worked example.
   **Severity:** serious.
   **Concern:** Insurance replacement decisions often depend on underwriting exclusions, pre-existing conditions, pregnancy, waiting periods, income protection definitions, and whether new policies require medical underwriting. A blanket “no medical specifics” rule could produce a materially wrong recommendation.
   **Suggested fix:** Add an exception: medical details are excluded from general bundles, but the orchestrator must either verify underwriting-sensitive facts locally or create a Tier D restricted appendix with explicit consent and minimised disclosure.

5. **Some OUT triggers are durable when they create commitments**
   **Where:** “Trigger rules — multi-agent OUT.”
   **Severity:** minor/serious depending on action.
   **Concern:** “Tactical PocketSmith tweaks, calendar events, gmail drafts” are usually ephemeral, but not always. A Gmail draft to an insurer, school, lawyer, doctor, or lender can bind framing. A calendar event for medical/family logistics can be consequential. PocketSmith changes can encode long-term budgeting assumptions.
   **Suggested fix:** Add an override: “OUT unless it creates an external commitment, changes a durable model, affects money/legal/health/family obligations, or contradicts memory.”

6. **“Lift AGENTS template verbatim” is incompatible with PLAIOS self-containment**
   **Where:** `AGENTS.md` separation; “template lifted verbatim… no rewriting.”
   **Severity:** minor.
   **Concern:** The source template is a repo template. PLAIOS is not a repo in the same sense and needs substantial domain/privacy wording. “Verbatim with bracketed sections customised” risks leaving ICX/RAIOS assumptions or vague placeholders.
   **Suggested fix:** Treat the template as structure, not content. Require a one-shot adversarial review of the actual drafted `AGENTS.md` before shipping.

7. **Decision records may be too thin for investigation outputs**
   **Where:** Output destinations; existing `decision-record-template.md`.
   **Severity:** minor.
   **Concern:** The current decision template appears minimal: context, decision, review date. It may not preserve alternatives rejected, evidence used, dissent, privacy tier, or follow-up tasks.
   **Suggested fix:** Either extend the decision template for investigation-backed decisions or make `10-final-output.md` the full record and let the promoted decision record link back to it.

## Things that are fine

- Core + PLAIOS overlay is the right shape. It preserves the source recipe while avoiding a generic copy-paste.
- Keeping `/investigate` skill v2 deferred is correct YAGNI. Manual run first is the right validation gate.
- Separating `AGENTS.md` as cross-tool baseline and `CLAUDE.md` as Claude orchestration logic is sound.
- Putting investigations under `journal/investigations/` fits PLAIOS better than a separate outputs directory.
- The insurance audit is an appropriate validating run: durable, consequential, cross-domain.

## Things you'd do differently but could go either way

- I would add a short “minimum viable investigation” checklist inside the single 10-phase pattern, not a lite variant: topic, evidence, adversarial pass, disposition, promoted output.
- I would include `privacy-tier.md` as a small standalone protocol if Tier B/D rules are going to govern many workflows.
- I would add a `README.md` inside each investigation folder explaining current phase/status, so resuming cold does not require reconstructing state from filenames.

## Open questions back to the orchestrator

1. Are Codex and Gemini invocations guaranteed to stay local/private enough for Tier D material, or are they vendor-hosted calls where disclosure minimisation must be stricter?
2. Should exact salaries/balances be included in reviewer bundles, or should Claude compute derived ratios locally and pass only what Codex/Gemini need?
3. For insurance, who owns underwriting verification: Claude from documents, Scott manually, Mina, or a deliberately restricted model pass?
4. Will nested code repos under `plaios-tools/` and `trading-tools/` have their own root `AGENTS.md` before this ships, to prevent accidental PLAIOS procedure bleed-through?
tokens used
19,879
# Review

## Material concerns

1. **Subdirectory invocation can silently drop the root contract**
   **Where:** File layout, `AGENTS.md`; specific Codex Q2; source claim “auto-picked-up”.
   **Severity:** serious.
   **Concern:** The design assumes root `D:\PLAIOS\AGENTS.md` is reliably loaded. If Codex/Gemini/Claude are invoked from `domains/finance/`, behavior may differ by CLI/version/config. Even if ancestor lookup works today, it is a brittle operational dependency.
   **Suggested fix:** Make the procedure state: “Invoke review CLIs from `D:\PLAIOS\` unless an evidence bundle explicitly includes `AGENTS.md`.” Also add tiny local `AGENTS.md` stubs in major subtrees only if needed, each saying “root context is authoritative; run from repo root.”

2. **The 10-phase pattern needs an explicit early-stop state**
   **Where:** “Investigation folder structure”; “Single pattern, no lite variant.”
   **Severity:** serious.
   **Concern:** Filling phases 6-9 with `n/a` after phase 4 research conclusively answers the question can create a misleading audit trail: it looks like deliberation was considered and skipped procedurally, not that the investigation terminated by evidence.
   **Suggested fix:** Keep the single folder pattern, but add a formal phase-gate rule: `07-disposition.md` may say `closed at phase 4: conclusive research; no deliberation warranted`. Later files should be named or worded as “not reached”, not “n/a”. That preserves audit truth without introducing a lite variant.

3. **Privacy tier B+D lacks a threat model**
   **Where:** “Privacy tier (B default + D Health/Family)”; insurance audit example.
   **Severity:** block for real insurance run until clarified.
   **Concern:** “Sanitise names, keep real ages/amounts” is not enough by itself. Given Scott’s public role, Australian context, four kids plus pregnancy timing, real ages may be re-identifying. Real salaries, balances, insurance premiums, and benefit amounts are also highly sensitive even without account numbers.
   **Suggested fix:** Define threat model explicitly: local-only agents vs vendor-hosted model calls vs saved repo artefacts. Add a rule that Tier D bundles get the minimum required detail per model. For example, Codex reviewing procedure logic may not need exact salary; insurance decision modelling may need exact benefit amounts. Store unsanitised source material separately from shareable review bundles.

4. **Health redaction may conflict with insurance decision quality**
   **Where:** “Override for Health: no medical specifics”; insurance audit worked example.
   **Severity:** serious.
   **Concern:** Insurance replacement decisions often depend on underwriting exclusions, pre-existing conditions, pregnancy, waiting periods, income protection definitions, and whether new policies require medical underwriting. A blanket “no medical specifics” rule could produce a materially wrong recommendation.
   **Suggested fix:** Add an exception: medical details are excluded from general bundles, but the orchestrator must either verify underwriting-sensitive facts locally or create a Tier D restricted appendix with explicit consent and minimised disclosure.

5. **Some OUT triggers are durable when they create commitments**
   **Where:** “Trigger rules — multi-agent OUT.”
   **Severity:** minor/serious depending on action.
   **Concern:** “Tactical PocketSmith tweaks, calendar events, gmail drafts” are usually ephemeral, but not always. A Gmail draft to an insurer, school, lawyer, doctor, or lender can bind framing. A calendar event for medical/family logistics can be consequential. PocketSmith changes can encode long-term budgeting assumptions.
   **Suggested fix:** Add an override: “OUT unless it creates an external commitment, changes a durable model, affects money/legal/health/family obligations, or contradicts memory.”

6. **“Lift AGENTS template verbatim” is incompatible with PLAIOS self-containment**
   **Where:** `AGENTS.md` separation; “template lifted verbatim… no rewriting.”
   **Severity:** minor.
   **Concern:** The source template is a repo template. PLAIOS is not a repo in the same sense and needs substantial domain/privacy wording. “Verbatim with bracketed sections customised” risks leaving ICX/RAIOS assumptions or vague placeholders.
   **Suggested fix:** Treat the template as structure, not content. Require a one-shot adversarial review of the actual drafted `AGENTS.md` before shipping.

7. **Decision records may be too thin for investigation outputs**
   **Where:** Output destinations; existing `decision-record-template.md`.
   **Severity:** minor.
   **Concern:** The current decision template appears minimal: context, decision, review date. It may not preserve alternatives rejected, evidence used, dissent, privacy tier, or follow-up tasks.
   **Suggested fix:** Either extend the decision template for investigation-backed decisions or make `10-final-output.md` the full record and let the promoted decision record link back to it.

## Things that are fine

- Core + PLAIOS overlay is the right shape. It preserves the source recipe while avoiding a generic copy-paste.
- Keeping `/investigate` skill v2 deferred is correct YAGNI. Manual run first is the right validation gate.
- Separating `AGENTS.md` as cross-tool baseline and `CLAUDE.md` as Claude orchestration logic is sound.
- Putting investigations under `journal/investigations/` fits PLAIOS better than a separate outputs directory.
- The insurance audit is an appropriate validating run: durable, consequential, cross-domain.

## Things you'd do differently but could go either way

- I would add a short “minimum viable investigation” checklist inside the single 10-phase pattern, not a lite variant: topic, evidence, adversarial pass, disposition, promoted output.
- I would include `privacy-tier.md` as a small standalone protocol if Tier B/D rules are going to govern many workflows.
- I would add a `README.md` inside each investigation folder explaining current phase/status, so resuming cold does not require reconstructing state from filenames.

## Open questions back to the orchestrator

1. Are Codex and Gemini invocations guaranteed to stay local/private enough for Tier D material, or are they vendor-hosted calls where disclosure minimisation must be stricter?
2. Should exact salaries/balances be included in reviewer bundles, or should Claude compute derived ratios locally and pass only what Codex/Gemini need?
3. For insurance, who owns underwriting verification: Claude from documents, Scott manually, Mina, or a deliberately restricted model pass?
4. Will nested code repos under `plaios-tools/` and `trading-tools/` have their own root `AGENTS.md` before this ships, to prevent accidental PLAIOS procedure bleed-through?
EXIT_CODE=0
