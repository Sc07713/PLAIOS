# Next session — kickoff prompt

**Saved:** 2026-05-06
**For:** insurance audit, the first real run of the multi-agent procedure shipped earlier today

---

## Copy-paste this into the next session

```
We're starting the insurance audit using the multi-agent procedure that shipped 2026-05-06.

CONTEXT (from prior session)

Mina has proposed insurance replacements. We need to audit current coverage vs alternatives and decide what to drop / replace / restructure — life, income protection, TPD, trauma, home/contents, car, and any others Mina has flagged.

Procedure: protocols/multi-agent.md
Cross-tool baseline: AGENTS.md
Full design spec: docs/superpowers/specs/2026-05-06-plaios-multi-agent-design.md

PRIVACY PLAN (already ratified — don't re-litigate)

- Tier B default + Tier D Health/Family overrides + minimum-required clause
- Real salaries and ages (insurance maths)
- Mina described as "expecting, due ~Q4 2026" (mat-leave timing is load-bearing for life/IP)
- Kids as K1–K4 with real ages, no school names
- No medical history piped to Codex/Gemini reviewers — I verify underwriting facts locally with insurer documents
- If a Tier D restricted appendix is needed for a specific decision, I grant explicit consent per invocation
- Bundles start with `--- Tier: B ---` (or D-Health / D-Family) metadata header

CONVERGENCE TARGET (the binding outcome we're driving toward)

Decide which insurances to drop / replace / restructure, producing:
- 1-page decision record at journal/decisions/{date}-insurance-audit.md
- Full investigation record at journal/investigations/{date}-insurance-audit/10-final-output.md
- Specific switch tasks if any policy needs to change

HOW TO START (no need to re-design — just execute)

1. From D:\PLAIOS\ root, run: .\bin\new-investigation.ps1 -Slug 'insurance-audit'
2. Drive phase 00 (topic intake) by asking me, one question at a time, for:
   - Current policies: which insurer / product / cover amount / premium / waiting period (per policy)
   - Mina's proposed alternatives: which insurers / products / why she found them attractive
   - Any pending claims or known coverage gaps
   - Decision deadline (e.g., before the pregnancy reaches a stage where new IP/life cover becomes harder to get)
3. After phase 00, follow the 10-phase pattern in protocols/multi-agent.md. The orchestrator (you) routes work to Codex (adversarial review) and Gemini (long-context / pattern channel) at the named convergence checkpoints.
4. Update the investigation README.md after each phase boundary so the audit trail stays useful for cold-start review.

GUARDRAILS

- Convergence is the goal, not dialogue.
- All multi-agent CLI invocations run from D:\PLAIOS\ root.
- Keep bundles minimal — derived ratios over raw amounts where the maths allows.
- If a phase exceeds ~2 hours of wall-clock, escalate or rethink scope.
- If reviewers can't converge after mediation, I (Scott) decide; record disagreement in 09-resolution.md.
```

---

## Notes for the orchestrator (Claude in next session)

- Don't re-design the procedure. It's shipped. Use it as written.
- Phase 00 is information-gathering. Ask one question at a time. Wait for answer. Capture in `00-topic.md`.
- Phase 01 (questions from each model) can be done in parallel by piping a topic-summary brief to Codex and Gemini independently. Read AGENTS.md, follow its conventions, return curt structured questions.
- The first real adversarial test for the procedure is whether the multi-agent review **materially changes the insurance decision logic at least once**. If it doesn't, the multi-agent overhead wasn't earned and the procedure should be downgraded for this class of decision.
- If anything in the procedure breaks under contact with the real audit, capture it in `08-meta-reflection.md` for v2 of `/investigate`.
