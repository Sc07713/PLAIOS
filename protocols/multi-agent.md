# Multi-Agent Procedure for PLAIOS

**Source:** core lifted from `D:\RAIOS-outputs\investigations\multi-agent-dev-practices-20260505-2237\10-final-recipe.md` (3-model ratified). PLAIOS overlay added at the bottom.

**Read this when:** you're about to make a durable decision, change a procedure, update memory in ways that contradict prior memory, or run an investigation. See "When NOT to use" if you're not sure.

---

## Goal — convergence on a binding outcome

Every investigation through this procedure produces a **group-bound decision, recommendation, or outcome** — not a balanced essay, not a perspectives roundup. The structure is:

**Input → process → output.**

- **Input:** topic + spec + evidence
- **Process:** independent research, parallel deliberation, mediated reconciliation
- **Output:** one binding artefact, with dissent recorded but not sovereign

The orchestrator (Scott, or Claude in his stead) is always the tie-breaker. Disagreement is recorded; it is never the deliverable. **Dialogue without convergence is procedure failure.**

---

## Where each model fits

| Model | Role | Why |
|---|---|---|
| **Claude** (Claude Code) | Driver. Holds the session, drafts artefacts, runs verification, narrates. | Native sub-agents, plan mode, file pinning, agentic loops, MCP access. |
| **Codex** (`codex exec`) | Adversarial reviewer. Invoked on demand. | Different model, different blind spots — catches what same-model review misses. |
| **Gemini** (`gemini --skip-trust -p`) | Long-context / external-pattern channel. Invoked on demand. | Long context window, different training — useful for "is this how it's done elsewhere?" or "does this match prior decisions?" |

Each model runs in its own context window. They never talk to each other. **The orchestrator passes artefacts between them via CLI.**

## The default workflow for in-scope multi-agent work

(See "When NOT to use multi-agent" below — the OUT list is authoritative; this workflow only applies once the task is in scope.)

1. **Plan** in Claude Code. Hand it: objective, files, constraints, non-goals, what convergence looks like. Ratify the plan before any artefact is drafted.
2. **Draft** in Claude Code. Surgical edits only. Files pinned. No repo-wide dumps. No opportunistic refactors.
3. **Verify** in Claude Code. Run any checks, tests, or repro scripts inside the session.
4. **Review** — pick the channel by risk:

   | Risk | Reviewer | Why |
   |---|---|---|
   | Routine | Claude Code reviewer sub-agent (sees only spec + draft + verify output) | Cheap, in-session |
   | Risky / cross-domain / consequential | **Codex** | Independent model — catches what Claude missed |
   | "Is this how it's done elsewhere?" / pattern question | **Gemini** | Long context + external pattern view |

   The reviewer sees only the evidence bundle. Never the chat history. Never the full repo.

5. **Narrate & commit.** State in the commit message *why* the accepted outcome is correct, in your own words. No "LGTM"-style merges.
6. **Close out** when the session approaches 200–250k tokens or spans days. Write a capsule: objective, decision, files changed, checks run, unresolved risks, exact next step.

## CLI invocations

**All multi-agent invocations run from `D:\PLAIOS\` (the project root)**, so `AGENTS.md` is loaded automatically by every CLI.

### Bundle metadata convention

Every evidence bundle starts with a 3-line metadata block so any reviewer knows the privacy tier without inferring:

```markdown
---
Tier: B
---

# Bundle title
...
```

`Tier: B` is the default. Use `Tier: D-Health` or `Tier: D-Family` for restricted appendices. If a bundle has no `Tier:` line, treat it as **untagged → stop, flag as a privacy escape, do not process** (per `AGENTS.md`).

### Codex (adversarial review)

PowerShell 5.1 (the primary shell on this system):

```powershell
# build the evidence bundle (no chat history)
Get-Content .\spec.md, .\draft.md, .\verify-output.md | Set-Content .\bundle.md

# pipe via stdin (NOT positional argument — that pattern hangs)
Get-Content .\bundle.md -Raw | codex exec -
```

Bash equivalent (for WSL or other shells):

```bash
cat spec.md draft.md verify-output.md > bundle.md
codex exec - < bundle.md
```

### Gemini (long-context / pattern question)

PowerShell 5.1:

```powershell
$prompt = @'
Question: [your specific question]
Context: [paste relevant content or reference paths]
'@
gemini --skip-trust -p $prompt
```

Bash equivalent:

```bash
gemini --skip-trust -p "$(cat <<'EOF'
Question: [your specific question]
Context: [paste relevant content or reference paths]
EOF
)"
```

### Claude Code

Open in `D:\PLAIOS\`. The CLI auto-loads `AGENTS.md` and `CLAUDE.md` from the working directory.

## Variant — investigation (durable, consequential, irreversible)

For decisions where rollback cost exceeds the deliberation cost. **This is the variant that converges to a group-bound outcome.** Output is a decision record (and possibly a procedure / recommendation), never a diff alone.

**Folder:** `journal/investigations/YYYY-MM-DD-{topic}/`. Bootstrap with `bin/new-investigation.ps1 <topic-slug>`.

### 10-phase pattern (single track — no "lite" variant)

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

If research (phase 04) is conclusive and no deliberation is warranted, `07-disposition.md` says: *"Closed at phase N: <reason>. No deliberation/mediation needed."* Phases past termination are **omitted** OR explicitly marked *"Not reached. Investigation closed at phase N — see 07-disposition.md."* Never use "n/a" — that creates a misleading audit trail.

### Output destinations

- **1-page summary** at `journal/decisions/YYYY-MM-DD-{topic}.md` (using `protocols/decision-record-template.md`), with a link back to the full record
- **Full record** at `10-final-output.md`: alternatives considered, evidence used, dissent noted, privacy tier applied, follow-up tasks
- **Procedural outcome** (if the investigation produced a procedure or skill spec): promoted to `protocols/` or `docs/superpowers/specs/`
- **Memory updates** flowing from the decision: handled by the close-out skill

## Variant — bug fix

For PLAIOS this applies to `plaios-tools` / `trading-tools` code repos. Those use this variant directly via their own repo-local `AGENTS.md` — no PLAIOS overlay. Reasoning-domain bugs (memory contradictions, decision-record errors) use the investigation variant above instead.

1. **Reproduce first.** Either Claude Code or Codex writes a *failing test* that demonstrates the bug. Run it. **No fix is permitted until this test exists and fails.**
2. **Fix in Claude Code.** Surgical patch. Test now passes.
3. **Adversarial review with Codex.** Bundle = spec + diff + test output.
4. **Narrate & commit.**

## Token discipline

Each model session stays under ~250k tokens by design. **No model ever holds the whole picture** — small, curated artefacts pass between them. Full repo dumps are forbidden. If a session approaches the ceiling, close it out and start fresh.

## When NOT to use multi-agent

- One-line edits — just write it.
- Tasks under 30 minutes — overhead exceeds gain.
- Pure exploration — single Claude Code session, no review channel.
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

### Trigger rules — multi-agent IN

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
