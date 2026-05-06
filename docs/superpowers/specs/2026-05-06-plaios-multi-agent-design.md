# PLAIOS Multi-Agent Development Procedure — Design Spec

**Date:** 2026-05-06
**Author:** Claude (in-session with Scott McKennie)
**Reviewers:** Codex (adversarial) + Gemini (long-context / pattern cross-check) — see `journal/investigations/2026-05-06-multi-agent-procedure-design/`
**Status:** Spec — ready for user review prior to implementation planning.

---

## 1. Purpose

Adopt the multi-agent development recipe that was 3-model-ratified for ICX (`D:\RAIOS-outputs\investigations\multi-agent-dev-practices-20260505-2237\`) inside PLAIOS, where the work product is mostly non-code reasoning (decisions, memory, procedures, cross-domain syntheses). Validate the adaptation by running it on a real durable decision (insurance audit) before considering skill automation.

## 2. Approach — "Core + PLAIOS overlay"

Lift the load-bearing parts of the source recipe verbatim — CLI invocations, 10-phase investigation structure, evidence-bundle context firewall, token discipline, default workflow, variants. Layer PLAIOS-specifics on top: trigger rules for life-domain artefacts, privacy/threat-model rules, output destinations, investigation folder placement.

**Rejected:** immediate/faithful port with no overlay — loses PLAIOS-specific framing (life-domain trigger rules, vendor-hosted privacy threat model).

**Considered but not chosen:** PLAIOS-tailored from scratch — doubles work, risks drift from the recipe Scott uses at ICX. Kept the simpler "core + overlay" path.

## 2a. Procedure goal — convergence on a binding outcome

Every investigation that runs through this procedure exists to produce a **group-bound decision, recommendation, or outcome** — not a balanced essay, not a perspectives roundup. The structure is **input → process → output**:

- **Input:** topic + spec + evidence
- **Process:** independent research, parallel deliberation, mediated reconciliation
- **Output:** one binding artefact (decision record, procedure, recommendation), with dissent recorded but not sovereign

When the three models converge, the orchestrator (Scott) ratifies and ships. When they don't converge after mediation (phase 09), the orchestrator decides; the disagreement is recorded in `09-resolution.md` so future investigations can learn from it. The orchestrator is always the tie-breaker — no 4th-model arbiter.

**Dialogue without convergence is procedure failure.** If a phase produces more disagreement than it resolves, the procedure escalates to mediation rather than continuing in circles.

**Quality property — every agent gets it from a cold read.** The procedure document and `AGENTS.md` must each be readable by a model that has zero prior context and still let it understand: who it is in this system, what its role is for this invocation, what's allowed in the bundle, what response shape converges toward an outcome. KISS / irreducible complexity is the *test*, not the *aspiration*.

## 3. File layout

| File / folder | Status | Purpose | Audience |
|---|---|---|---|
| `D:\PLAIOS\AGENTS.md` | NEW | Cross-tool baseline. Project description, conventions, multi-agent role conventions, privacy/threat-model rules, what NOT to do, where things live. Auto-picked-up by Codex CLI, Gemini CLI, and Claude Code. Self-contained for cold-start strangers. | All three CLIs |
| `D:\PLAIOS\CLAUDE.md` | MODIFY (+1 pointer line) | Existing content stays. New line near top: *"For project conventions and multi-agent role rules, see `AGENTS.md` — don't duplicate them here."* | Claude Code only |
| `D:\PLAIOS\protocols\multi-agent.md` | NEW | The recipe — core lifted from RAIOS `10-final-recipe.md` + PLAIOS overlay. One file, two clearly-delineated sections. | Humans + Claude when planning |
| `D:\PLAIOS\bin\new-investigation.ps1` | NEW | Tiny scaffold: takes `<topic-slug>`, creates `journal/investigations/YYYY-MM-DD-<slug>/` and the empty 00–10 files plus `README.md`. ~15 lines. | Humans |
| `D:\PLAIOS\journal\investigations\YYYY-MM-DD-{topic}\` | NEW (per investigation) | Folder-as-state-machine. 10-phase pattern. Includes `README.md` for current-phase / status tracking. | Audit trail |
| `D:\PLAIOS\journal\decisions\` | EXISTING (empty) | 1-page summary decision records, link back to `10-final-output.md` for full context. | Long-term decision log |
| `D:\PLAIOS\.claude\skills\investigate\` | DEFERRED (v2) | `/investigate` skill — built only if the manual workflow earns it after at least one real investigation. | Claude Code only |

**Two specific calls:**
- **Recipe is one file.** Core + overlay is a mental model, not a file split.
- **Investigation folders live under `journal/investigations/`** (not a separate `D:\PLAIOS-outputs\` like RAIOS). PLAIOS is private, single-user, one git history.

**Note on adjacent code repos:** `D:\Plaios-tools\trading-tools\` and any future `plaios-tools` repos are **separate git repos**, not nested under PLAIOS. Each will have its own `AGENTS.md` at its repo root. No bleed-through risk; no precedence ambiguity.

## 4. `AGENTS.md` vs `CLAUDE.md` — separation of concerns

| Content | Lives in | Why |
|---|---|---|
| Project description (PLAIOS = markdown reasoning system, no build/test/run for most domains) | AGENTS.md | All three CLIs need it |
| Multi-agent role conventions (evidence-bundle only, surgical edits, sub-85% confidence flagged, citations) | AGENTS.md | Codex/Gemini need it; Claude reads it too — single source |
| Privacy / threat-model rules (B default + D Health/Family + minimum-required clause + vendor-hosted disclosure) | AGENTS.md | Reviewer must know what's allowed in the bundle |
| Root-invocation rule (CLIs run from `D:\PLAIOS\`) | AGENTS.md | Cross-tool operational rule |
| What NOT to do (no scope creep, no speculative reasoning unflagged, no cross-domain aggregation unasked) | AGENTS.md | Cross-tool baseline |
| Where things live (domain map, journal, protocols, decisions) | AGENTS.md | All tools benefit |
| Identity, hierarchy of needs, maturity scale, priority algorithm, escalation rules, session protocol, systems-thinking framework | CLAUDE.md (existing) | Claude orchestration logic; not relevant to a one-shot Codex review |
| Privacy *principle* ("sensitive requires explicit navigation") | CLAUDE.md (existing) | Claude session-level rule; the *tier policy* lives in AGENTS.md |
| Sub-agent definitions, skill bindings (close-out, future /investigate) | CLAUDE.md | Claude-only |

**Drafting `AGENTS.md`:** start from `D:\RAIOS-outputs\...\12-AGENTS-template.md` as **structure**, not verbatim content. Customise PLAIOS-specific sections. Run a quick adversarial pass (Codex, evidence-bundle = drafted file) before committing.

## 5. `protocols/multi-agent.md` — content

### Top half — lifted from RAIOS `10-final-recipe.md`
- Where each model fits (Claude=driver, Codex=adversarial reviewer, Gemini=long-context/pattern channel)
- Default workflow: Plan → Implement → Verify → Review (by risk) → Narrate → Close out
- Bug-fix variant (failing test first, fix, Codex review)
- Decision variant (multi-model deliberation via `/investigate`, no code, output is a decision record)
- CLI invocations (`codex exec - < bundle.md`; `gemini --skip-trust -p ...`)
- Token discipline (250k per session)
- When NOT to do this (one-line edits, <30min tasks, pure exploration)

### Bottom half — PLAIOS overlay

**Operational rule:**
- All multi-agent CLI invocations run from `D:\PLAIOS\` (the project root). Bundle file paths are relative to root. Why: ensures `AGENTS.md` is always loaded.

**Trigger rules — multi-agent IN:**
- Durable decisions in life domains (insurance, schools, property, fertility/baby planning, vendor switches, debt restructure, household-level rules)
- Cross-domain syntheses ("where am I structurally weak?")
- Memory updates that contradict prior memories
- Skill / procedure design changes
- Code work in `plaios-tools` / `trading-tools` (use RAIOS recipe directly via repo-local `AGENTS.md`)

**Trigger rules — multi-agent OUT:**
- Routine state reads, daily journal lines
- Single-domain memory updates that don't contradict anything
- Tactical PocketSmith tweaks, calendar events, gmail drafts
- Anything ephemeral

**OUT override clause:** the OUT list applies *unless* the artefact creates an external commitment (Gmail to insurer/lawyer/doctor/lender), changes a durable model (PocketSmith budget structure, not just an event amount), affects money/legal/health/family obligations, or contradicts memory. In those cases promote to IN.

**Privacy / threat model:**

Reframed per Gemini: sanitisation rules are about **reducing model focus on identity to prevent bias / sycophancy / latent re-identification anchoring** — not cryptographic anonymity. Vendor terms (OpenAI for Codex; Google for Gemini) are the actual privacy boundary. Anything bundled and piped out leaves Anthropic's perimeter.

- **Vendor-hosted disclosure** (load-bearing): Codex calls hit OpenAI, Gemini calls hit Google. Bundle contents are subject to those vendors' terms. If the data is bundle-inappropriate even for a friendly vendor (raw medical history, DNA), keep it out and verify locally.
- **Tier B (default):** sanitise names → roles, redact account / policy numbers, keep amounts and ages real (decision quality depends on real numbers).
- **Tier D — Health override:** no medical specifics, no DNA / genetic data in general bundles. Insurance/health decisions that **require** underwriting facts (pregnancy status, pre-existing conditions, waiting periods) get a Tier D restricted appendix with explicit consent each invocation OR Scott verifies the underwriting facts locally without piping to reviewers.
- **Tier D — Family override:** kids' names → K1–K4 (real ages preserved — dependency calculations matter), no school names; pregnancy described as "expecting, due ~Q{quarter} {year}" (mat-leave timing is load-bearing).
- **Minimum required for decision quality:** prefer derived ratios (debt-to-income, liability-to-asset, premium-to-cover) over raw amounts where the maths allows. Raw amounts only when the decision needs them (insurance premium maths, mat-leave hole sizing).
- **Salaries and account balances:** real values allowed in bundles by default; account *numbers* always redacted.

**Output destinations:**
- Decisions → `journal/decisions/YYYY-MM-DD-{topic}.md` — **1-page summary** using the existing `protocols/decision-record-template.md`, with explicit link to `10-final-output.md` for full record
- Full investigation record → `journal/investigations/YYYY-MM-DD-{topic}/10-final-output.md` — alternatives considered, evidence used, dissent noted, privacy tier applied, follow-up tasks
- Procedures → `protocols/`
- Memory → memory dir (close-out skill handles)
- Skill specs → `docs/superpowers/specs/`

## 6. Investigation folder structure (10-phase, single pattern)

`journal/investigations/YYYY-MM-DD-{topic}/`:
```
README.md  (current phase, status, last-touched, brief summary — for cold-start orientation)
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
10-final-output.md  (full investigation record — promoted summary lives in journal/decisions/)
```

**Single pattern, no "lite" variant.**

**Early termination semantics (NOT "n/a"):**
- If an investigation can close before phase 09 (research is conclusive, no deliberation warranted), `07-disposition.md` declares this explicitly: *"Closed at phase N: <reason>. No deliberation/mediation needed."*
- Phase files past the termination point are **omitted** from the folder, OR if created they say *"Not reached. Investigation closed at phase N — see 07-disposition.md."*
- This preserves audit truth — the trail shows the investigation terminated by evidence, not skipped procedurally.

**Bootstrap:** `bin/new-investigation.ps1 <topic-slug>` creates the folder, the empty 00–10 files, and the README. ~15 lines of PowerShell. Not the `/investigate` skill — just a folder-scaffold convenience.

## 7. Insurance audit — validating worked example

**Folder:** `journal/investigations/2026-05-06-insurance-audit/` (bootstrapped via `bin/new-investigation.ps1`)

**Topic:** Mina has proposed insurance replacements; audit current coverage vs alternatives, decide what to drop / replace / restructure across life, income protection, TPD, trauma, home/contents, car (and any others Mina has flagged).

**Privacy plan:**
- Real salaries and ages (insurance maths)
- Mina described as "expecting, due ~Q4 2026" (mat-leave timing is load-bearing for life/IP)
- Kids as K1–K4 with real ages, no school names
- No medical history piped to reviewers — Scott verifies underwriting facts locally with insurer documents
- If a Tier D appendix is needed for a specific decision, explicit consent per invocation

**Underwriting verification:** Scott (with Mina) reads insurer PDS / underwriting questionnaires directly. Reviewers (Codex/Gemini) pressure-test the **decision logic** (which policy wins on which dimension, where the gaps are), not the **eligibility** (which is a yes/no from the insurer).

**Pre-flight:** Codex and Gemini installed and authenticated — verified for this design review.

**Final output:**
- `10-final-output.md` — full investigation record with per-policy comparison, alternatives, evidence, dissent, follow-ups
- `journal/decisions/2026-05-06-insurance-audit.md` — 1-page summary using `protocols/decision-record-template.md`, links back to `10-final-output.md`
- Any policy-switch tasks in the user's task system

## 8. `/investigate` skill v2 — deferred

**Scope (when built):** automate folder scaffolding (currently `bin/new-investigation.ps1`), prompt templates per phase, evidence-bundle assembly, CLI orchestration to Codex/Gemini, sanitisation pre-flight check.

**Trigger to build:** after at least one real investigation validates the manual workflow. If the insurance audit shows manual orchestration is fine and the bootstrap script covers the friction, defer further.

**Backlog:** V1–V14 from the RAIOS investigation outputs (`09-resolution.md` §G), plus any lessons captured from the insurance audit.

## 9. Open design questions — answered

| Question | Answer |
|---|---|
| Are Codex / Gemini local or vendor-hosted? | Vendor-hosted (OpenAI / Google). Encoded in the threat-model section. |
| Should exact salaries be in bundles or derived ratios? | Derived ratios where the question allows; raw values when the maths needs them. Captured in "minimum required" clause. |
| Who owns underwriting verification? | Scott + Mina + insurer documents. Reviewers test decision logic, not eligibility. |
| Will adjacent code repos have their own `AGENTS.md`? | Yes — `plaios-tools`, `trading-tools` are separate repos with their own root `AGENTS.md`. No nesting under PLAIOS. |
| Wall-clock time budget per investigation phase? | Soft cap ~2 hours per phase; if exceeded, escalate or rethink scope. |
| Evidence bundle disposal in git history? | Bundles stay in PLAIOS git (private, single-user). Redaction overkill for now. |
| Cross-model tie-breaker if Codex / Gemini disagree? | Orchestrator (Scott) is the tie-breaker; disagreement recorded in `09-resolution.md`. No 4th-model arbiter. |

## 10. Implementation order (what gets built when)

1. `D:\PLAIOS\AGENTS.md` — drafted from the RAIOS template (structure only), customised for PLAIOS, adversarially reviewed before commit.
2. `D:\PLAIOS\protocols\multi-agent.md` — recipe + overlay.
3. `D:\PLAIOS\CLAUDE.md` — add the 1-line pointer to `AGENTS.md`.
4. `D:\PLAIOS\bin\new-investigation.ps1` — scaffold script.
5. Bootstrap the insurance audit folder via the script. Run phase 00 (topic intake).
6. Defer `/investigate` skill until the audit validates the manual workflow.

## 11. Success criteria

- The insurance audit completes through to a decision record. Reviewers materially change the decision logic at least once (otherwise the multi-agent overhead wasn't earned).
- Scott voluntarily uses the procedure on a second durable decision without prompting.
- AGENTS.md is referenced by both Codex and Gemini in subsequent runs (verifiable via output content / behaviour).
- Bundle minimisation rule observed: no raw account numbers, no medical history, no kids' names in any committed bundle.
