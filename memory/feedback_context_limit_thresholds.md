---
name: Context limit thresholds — close out at 250k, never past 500k
description: Scott's tiered context budget for when to proactively suggest closing out a session vs pushing through
type: feedback
originSessionId: fb24bd11-1fee-469b-8616-1708b50cd5bb
---

Scott's context budget tiers:

- **≤250k tokens (soft limit):** Operate normally.
- **~250k tokens:** **Proactively suggest closing out and chunking remaining work into a new session.** Don't wait for the user to ask. Plan workload around this — if a task chunk is likely to push past 250k, flag it before starting and propose a natural break point.
- **~500k tokens:** Context rot becomes meaningful — quality degrades. **Strongly avoid going past this** unless the user explicitly opts in for a specific reason.
- **~1M tokens:** Compaction territory (auto-summarisation kicks in, lossy). Treat as the hard ceiling.

**Why:** Established 2026-04-29 after a long trading-tools build session reached deep context. Quality degradation at higher context is real, and Scott doesn't want to lose fidelity by pushing too far. He'd rather close out early and resume with fresh context (using mirrored memory + plan/spec files for continuity) than push a single session into rot.

**How to apply:**
- Track conversation depth implicitly. When the session feels "deep" or token-heavy, check in before taking on a major new chunk.
- When approaching 250k: proactively say "we're getting deep, X is a natural close-out point — want to chunk the rest into a new session?" rather than continuing silently.
- Plan multi-task work around this: when laying out a plan with N tasks, mentally pre-mark which tasks make good close-out boundaries.
- Memory writes become more important near these thresholds — capture state for the next session before closing.
- Hard NO past 500k without explicit user approval.
