---
name: trading-tools-is-a-hypothesis-factory
description: "trading-tools is a hypothesis-testing factory, not a single-strategy product — each sub-piece is a falsification attempt; '0 REAL EDGE' is a feature; studies (notebook + writeup) sit alongside builds (spec/plan/TDD/ship) as first-class output"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 631f04e5-e90f-4124-a992-f1153412b23e
---

The framework's purpose is **hypothesis-testing, not strategy-hunting-until-something-works**. Each sub-piece (V3.1 robustness, V3.2 overlay, VWEMA-BB tiered port, V3.3a fundamentals, V3.3b PEAD, V3.3b-quality, etc.) is a falsifiable test of an idea — not a step toward a single production strategy. If something tests as "0 REAL EDGE" (the V3.2 baseline did, V3.3b PEAD did, V3.3b-quality did), that's a *feature* of an honest framework, not a failure. The point is to know what doesn't work as cleanly as what does.

**Two output shapes are first-class:**

1. **Builds** — full spec → plan → TDD → ship cadence: new code (strategies, aux datasets, harness changes), tests, docs updates, baseline runs, push. Examples: V3.2 portfolio overlay, V3.3a fundamentals backbone, V3.3b earnings layer + PEAD, V3.3b-quality.

2. **Studies** — notebook + markdown writeup in `docs/studies/`. Investigation, hypothesis-generation, descriptive analysis. Single-session, no production code, no new infra. Examples: V3.3a's `notebooks/fundamentals_earnings_study.ipynb` (filing-date-keyed growth event study), V3.3b's `notebooks/pead_announcement_study.ipynb` (announcement-date event study), the just-proposed "winners characterization" / "money-extractor" study.

**Why:** Don't waste spec/plan/TDD cycles on exploratory questions. Don't pretend a notebook investigation is a falsifiable trading edge.

**How to apply:** When a user request describes characterizing / understanding / decomposing / exploring — that's a study. When it describes adding a strategy, an indicator, a new dataset to the harness, or running a new baseline — that's a build. Both can run in parallel sessions (a study doesn't block a build and vice versa). A study can also *inform* a later build (the V3.3a study → V3.3b spec; the proposed money-extractor study could inform a future V3.3d screener build).

Related: [[user_investment_philosophy]] (Scott's investing principles inform the studies' hypotheses); [[project_trading_v3_scope_pending]] (the V3 roadmap).
