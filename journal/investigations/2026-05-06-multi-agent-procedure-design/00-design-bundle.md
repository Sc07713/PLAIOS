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
