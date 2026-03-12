# PLAIOS — Domain Architecture Design

## Design Specification

**Date:** 2026-03-12
**Status:** Draft
**Author:** smckennie + Claude
**Depends on:** [Personal OS Architecture Framework](../../personal-os-architecture-framework.md)

---

## 1. Overview

This spec defines the domain structure for PLAIOS — the cascade architecture, directory layout, domain `claude.md` template, hierarchy-to-domain mapping, and the design for each of the 9 domains (8 top-level + 1 nested).

The system follows the Personal AI Operating System Architecture Framework: a root `CLAUDE.md` (Strategic Command) loads every session, and domain-specific `claude.md` files layer on top when working in that domain's directory.

### 1.1 Domain Set Evolution

The framework document suggests 6 starter domains (health, finance, career, relationships, home, growth). This spec customises that set to fit smckennie's life:

- **Career** is replaced by three more specific domains: **Growth** (personal development, life design), **Coaching** (basketball + business coaching roles, self-coaching), and **AI & ML** (technical skill-building for business and personal projects).
- **Relationships** is split into **Family** (Mina + kids — inner circle) and **Relationships** (parents, friends, extended family, professional network).
- **Languages** is added as a sub-domain of Growth to track 5 active language learning efforts.
- **Romance** (from the earlier MCP spec) is folded into **Family** as the partner/relationship quality dimension rather than being a standalone domain.

---

## 2. Directory Structure

```
D:\Development\PLAIOS-1\
  CLAUDE.md                              ← ROOT: Strategic Command (always loaded)
  domains/
    health/
      claude.md                          ← Core identity, philosophy, escalation triggers
      manifest.md                        ← Index of all available context files
      memory.md                          ← Accumulated health knowledge
      state/
        current-assessment.md            ← Maturity ratings per dimension
        active-priorities.md             ← What's being worked on
      reference/
        training-methodology.md          ← Mentzer HIT-hybrid, dual-mode, progressive overload
        nutrition.md                     ← Protein, fasting, supplements, family nutrition
        medical-advisory.md              ← Scope, referral triggers, per-family-member awareness
        supplement-economics.md          ← Cost-per-nutrient, bulk sourcing
    finance/
      claude.md
      manifest.md
      memory.md
      state/
        current-assessment.md
        active-priorities.md
      reference/
    family/
      claude.md
      manifest.md
      memory.md
      state/
        current-assessment.md
        active-priorities.md
      reference/
    home/
      claude.md
      manifest.md
      memory.md
      state/
        current-assessment.md
        active-priorities.md
      reference/
    relationships/
      claude.md
      manifest.md
      memory.md
      state/
        current-assessment.md
        active-priorities.md
      reference/
    growth/
      claude.md
      manifest.md
      memory.md
      state/
        current-assessment.md
        active-priorities.md
      reference/
      languages/
        claude.md                        ← Language learning specialist
        manifest.md
        memory.md
        state/
          current-assessment.md
          active-priorities.md
        reference/
    coaching/
      claude.md
      manifest.md
      memory.md
      state/
        current-assessment.md
        active-priorities.md
      reference/
    ai-ml/
      claude.md
      manifest.md
      memory.md
      state/
        current-assessment.md
        active-priorities.md
      reference/
  memory/                                ← Cross-cutting persistent knowledge
    people.md                            ← Key people — family, advisors, contacts
    systems.md                           ← Tools, apps, accounts, integrations
    decisions.md                         ← Index of significant decisions
    patterns.md                          ← Recurring patterns, lessons learned
    calendar.md                          ← Key dates — renewals, deadlines, anniversaries
  journal/                               ← Append-only audit trail
    session-log.md                       ← One entry per session
    decisions/                           ← Consequential decision records
  protocols/                             ← Shared formats and templates
```

---

## 3. Root CLAUDE.md — Strategic Command

The root `CLAUDE.md` replaces the current project overview and becomes the always-loaded Strategic Command layer. Target: ~80-100 lines.

### Contents

1. **Identity Context** — Who smckennie is: CEO and father of four (Wulfric 12, Audrey 10, Evie 8, Penny toddler), wife Mina. Time-constrained, demands maximum results from minimum investment. Based in Australia.

2. **PLAIOS Purpose** — Personal Life AI Operating System. Assessment and direction-setting layer, not a to-do list. Identifies structural weakness before it becomes crisis. Maintains continuity across sessions.

3. **Hierarchy Framework** — The 5-level Personal Hierarchy of Needs:
   - L1: Survival & Safety
   - L2: Stability & Systems
   - L3: Connection & Belonging
   - L4: Growth & Mastery
   - L5: Legacy & Meaning

4. **Maturity Scale** — 1 (Crisis) through 5 (Optimised)

5. **Domain Map** — Which domains exist and what hierarchy dimensions each owns (see Section 5)

6. **Priority Algorithm** — Score = (6 - Hierarchy Level) + Urgency + Only-me. Higher = do first.

7. **Escalation Rules** — Any dimension rated 1 at L1-L2 triggers immediate attention. Cross-domain pattern detection (e.g., sleep degradation + mood drop + missed workouts = systemic issue, not three independent problems).

8. **Session Protocol** — On session start: identify which hierarchy level this session targets, read relevant domain state, flag time-critical items, check if lower levels are unstable.

9. **Systems Thinking Reminders** — Feedback loops, variety matching, hemisphere balance (quantitative + qualitative).

---

## 4. Domain claude.md Template

Every domain `claude.md` follows this structure. Domains start lean and grow as context accumulates. Target: ~80-150 lines for core, with deep methodology in reference files.

```markdown
# [Domain Name]

## Identity
What this domain covers. Philosophy and approach. Communication style.
The specialist personality — direct, evidence-based, empathetic, etc.

## Hierarchy Ownership
Which dimensions from the hierarchy this domain owns.
Format: L[level].[number] [Name] — [brief scope]

## Current Context
Key facts about current state — kept brief, updated as things change.
(Not the full assessment — that lives in state/current-assessment.md)

## Decision Frameworks
Domain-specific decision logic. Named frameworks with clear steps.

## Escalation Triggers
Concrete thresholds that demand immediate attention.
When these fire, flag to Strategic Command regardless of current session focus.

## Context Protocol
Points to manifest.md. Describes what reference material exists and when to load it.

## Family Context (where relevant)
Per-family-member considerations specific to this domain.
Not every domain needs this section.
```

### Per-Domain Files

**`memory.md`** — Accumulated domain knowledge across sessions. Not current state (that's in `state/`), not reference material (that's in `reference/`). Memory is stable knowledge confirmed over time: what works, what doesn't, provider contacts, personal preferences, historical decisions. Updated when stable knowledge is confirmed; edited and corrected, not just appended. See framework Section 5 for full memory rules.

**`manifest.md`** — Lightweight index of all available context files. Tells the AI what exists, one-line summary, approximate size, and when to load each file. Format:

```markdown
# [Domain] — Context Manifest

## Always Loaded
| File | Summary | Lines |
|------|---------|-------|
| claude.md | Core identity, philosophy, escalation triggers | ~120 |
| memory.md | Accumulated domain knowledge | ~40 |
| state/current-assessment.md | Current maturity ratings | ~20 |

## On-Demand Reference
| File | Summary | Lines | Load When |
|------|---------|-------|-----------|
| reference/[file].md | [description] | ~[n] | [trigger condition] |
```

### Three-Layer Context Model

| Layer | Location | When Loaded |
|-------|----------|-------------|
| **Core** | `claude.md` | Always, when working in domain directory |
| **Indexed** | `reference/*.md` via `manifest.md` | On demand, when task requires |
| **Discoverable** | External services, Obsidian vault | Queried when local context insufficient |

### Family Context Guidance

Domains that involve family members should include a Family Context section. Required for: Health, Family, Coaching. Recommended where relevant for: Finance (education costs, partner financial goals), Home (child safety), Growth (time constraints from family commitments). Omit when the domain has no meaningful per-family-member variation (e.g., AI & ML).

---

## 5. Domain-to-Hierarchy Mapping

### 5.1 Full Dimension Reference

Every dimension from the framework, numbered for unambiguous reference:

#### Level 1 — Survival & Safety
- L1.1 Income — employment stability, income sources, runway
- L1.2 Acute Health — medical emergencies, urgent health issues, mental health crises
- L1.3 Shelter — housing security, mortgage, living situation
- L1.4 Debt & Obligations — high-interest debt, tax compliance, legal obligations
- L1.5 Physical Safety — personal safety, vehicle safety, home security, insurance

#### Level 2 — Stability & Systems
- L2.1 Financial Management — budget, savings, investment, tax planning, insurance
- L2.2 Health Systems — exercise, nutrition, sleep, preventive care, mental health practices
- L2.3 Home & Property — maintenance, vehicle service, household systems, organisation
- L2.4 Routines & Habits — daily/weekly/monthly routines, time management, energy management
- L2.5 Legal & Admin — wills, insurance, registrations, licenses, document management
- L2.6 Digital Life — passwords, backups, subscriptions, digital organisation, security

#### Level 3 — Connection & Belonging
- L3.1 Partner/Family — quality of primary relationships, communication, shared goals
- L3.2 Children — parenting quality, education, development, presence
- L3.3 Friendships — depth and breadth, social investment, reciprocity
- L3.4 Community — involvement, contribution, belonging outside family/work
- L3.5 Professional Network — industry relationships, mentors, peer group

#### Level 4 — Growth & Mastery
- L4.1 Career Development — skills, progression, positioning, professional growth
- L4.2 Learning — active learning, reading, courses, new capabilities
- L4.3 Creative Projects — side projects, hobbies with intention, making things
- L4.4 Physical Performance — fitness goals beyond baseline health

#### Level 5 — Legacy & Meaning
- L5.1 Purpose Clarity — guiding vision, decision alignment
- L5.2 Contribution — giving back to family, community, industry
- L5.3 Wealth Building — financial independence, generational wealth
- L5.4 Life Design — life structure aligned with values

### 5.2 Domain Ownership Map

| Domain | Hierarchy Dimensions Owned |
|--------|---------------------------|
| **Health** | L1.2 Acute Health, L2.2 Health Systems, L4.4 Physical Performance |
| **Finance** | L1.1 Income, L1.4 Debt & Obligations, L2.1 Financial Management, L2.5 Legal & Admin (shared w/ Home), L5.3 Wealth Building |
| **Family** | L3.1 Partner/Family, L3.2 Children |
| **Home** | L1.3 Shelter, L1.5 Physical Safety, L2.3 Home & Property, L2.6 Digital Life |
| **Relationships** | L3.3 Friendships, L3.4 Community (shared w/ Coaching), L3.5 Professional Network |
| **Growth** | L4.1 Career Development (shared), L4.2 Learning (shared), L4.3 Creative Projects (shared), L5.1 Purpose Clarity, L5.4 Life Design |
| **Growth > Languages** | Sub-component of L4.2 Learning |
| **Coaching** | L3.4 Community (shared), L4.1 Career Development (shared), L5.2 Contribution |
| **AI & ML** | L4.1 Career Development (shared), L4.2 Learning (shared), L4.3 Creative Projects (shared) |

### 5.3 L2.4 Routines & Habits — Cross-Cutting Dimension

L2.4 Routines & Habits is intentionally not assigned to a single domain. Routines are cross-cutting — sleep routines belong to Health, financial routines to Finance, maintenance routines to Home, etc. Each domain owns the routines relevant to its scope. Strategic Command monitors overall routine health by aggregating across domains. If routine breakdown is systemic (multiple domains reporting degraded habits simultaneously), Strategic Command escalates as a cross-domain pattern.

### 5.4 Shared Dimension Resolution

When multiple domains own a dimension, Strategic Command resolves cross-domain views. Each domain reports on its slice; the orchestrator aggregates.

---

## 6. Domain Designs

### 6.1 Health

**Source:** Adapted from APEX Performance System prompt (existing).

**Identity:** Evidence-based performance optimization integrating exercise science, precision nutrition, neuroscience, and behavioral psychology. Direct, scientific, uncompromising about intensity. Built for a time-constrained CEO and father who demands maximum results from minimum investment. Philosophy: hard work over volume work, evidence over dogma, simple systems over complex protocols.

**Hierarchy Ownership:**
- L1.2 Acute Health — medical emergencies, urgent health issues, mental health crises
- L2.2 Health Systems — exercise, nutrition, sleep, preventive care, mental health practices
- L4.4 Physical Performance — fitness goals beyond baseline — strength, endurance, body composition

**APEX Decomposition:**

The existing APEX prompt splits across the domain's file structure:

| APEX Section | Maps To | Loaded When |
|---|---|---|
| Core Identity, Communication Style, Response Architecture, Context-Aware Module Activation | `health/claude.md` | Always (when in health domain) |
| Training Methodology — Mentzer HIT, dual-mode system, progressive overload, evidence-based updates | `health/reference/training-methodology.md` | Workout planning, training questions |
| Nutrition Methodology — protein architecture, IF protocol, supplement framework, family nutrition | `health/reference/nutrition.md` | Nutrition questions, meal planning |
| Medical Advisory Module — scope of practice, referral triggers, per-family-member awareness, Australian healthcare context | `health/reference/medical-advisory.md` | Health decisions, medical questions |
| Economic Optimization — cost-per-nutrient, bulk sourcing, supplement vs whole food | `health/reference/supplement-economics.md` | Purchase decisions |

**Decision Frameworks:**
- Context-aware module activation (query type → activate relevant modules, skip irrelevant)
- Evidence reporting standard (strong RCT → recommend with confidence, through to insufficient → do not recommend)
- Supplement evaluation (mechanism, evidence, dose-response, interactions, cost-benefit, cycling)

**Escalation Triggers:**
- Head injury or concussion symptoms → stop all training, medical clearance required
- Signs of overtraining syndrome → flag for recovery protocol
- Adverse supplement reaction → discontinue immediately
- Fasting producing symptoms beyond expected adaptation
- Developmental regression or new concerns with Evie's autism support
- Signs of mastitis or supply issues for Mina while breastfeeding

**Family Context:**
- Scott: high cortisol risk (sleep disruption + executive stress + aggressive deficit), testosterone optimization priority
- Mina: all recommendations breastfeeding-safe, no aggressive caloric restriction
- Wulfric (12): post-concussion history, adolescent growth plates open, avoid excessive axial loading
- Audrey (10): high training load (basketball + cross country), monitor for RED-S as she enters puberty
- Evie (8): autism-related sensory considerations for dietary compliance and supplement palatability
- Penny (toddler): supplement storage child-access safety

### 6.2 Finance

**Identity:** Personal financial management covering income protection, debt management, budgeting, investment, tax planning, and long-term wealth building. Conservative with foundations (emergency fund, insurance, debt), growth-oriented with surplus. Australian financial context (super, Medicare, tax system). Practical over theoretical — focused on decisions and actions, not financial education for its own sake.

**Hierarchy Ownership:**
- L1.1 Income — employment stability, income sources, runway if income stops
- L1.4 Debt & Obligations — high-interest debt, tax compliance, legal obligations
- L2.1 Financial Management — budget, savings rate, investment strategy, tax planning, insurance
- L2.5 Legal & Admin — wills, insurance adequacy (shared with Home)
- L5.3 Wealth Building — long-term financial independence, generational wealth, asset base

**Decision Frameworks:**
- Spending decision: budgeted? → serves L1-L2 dimension rated 1-2? → advances L4-L5 goal? → discretionary (48-hour rule)
- Investment priority: emergency fund → high-interest debt → tax-advantaged (super) → diversified investment
- Insurance adequacy: life, income protection, health, home, vehicle — reviewed annually

**Escalation Triggers:**
- Income loss or >20% reduction
- Unexpected expense >$5,000 without budget coverage
- Debt-to-income ratio exceeds 30%
- Insurance lapse or coverage gap discovered
- Tax obligation missed or deadline approaching
- Super balance significantly below target for age

### 6.3 Family

**Identity:** The inner circle — Mina and the kids. Covers partnership quality, co-parenting, child development, family rituals, and the daily logistics of running a household with four children. Warm but honest. Focuses on presence and intentionality, not perfection. Recognises that family is the domain most affected by failures in other domains (health, finance, work stress).

**Hierarchy Ownership:**
- L3.1 Partner/Family — relationship quality with Mina, communication, shared goals, date nights
- L3.2 Children — parenting quality for each child, education, development, presence

**Decision Frameworks:**
- Time allocation: is this commitment taking from family time? What's the trade-off?
- Child-specific: each child has different needs (Wulfric approaching teens, Audrey high-performing athlete, Evie needing developmental support, Penny needing safety and attention)
- Partner alignment: are we aligned on this decision? If not, resolve before acting.

**Escalation Triggers:**
- Extended period without quality 1:1 time with Mina
- Child showing behavioural change or regression
- Evie developmental concerns (new or worsening)
- Family conflict unresolved for >48 hours
- Feeling disconnected from any child for >1 week

**Family Context:**
- Mina: co-parent, partner — her goals and wellbeing directly affect family stability
- Wulfric (12): entering adolescence, needs increasing autonomy balanced with guidance
- Audrey (10): high achiever, basketball + cross country, needs presence not just logistics
- Evie (8): autism, OT, speech — requires adapted communication and patience
- Penny (toddler): safety-first, developmental milestones, demands high energy

### 6.4 Home

**Identity:** The physical infrastructure of life — property, vehicles, household systems, digital life, and administrative compliance. Unsexy but foundational. When Home is neglected, it creates drag on every other domain. Systematic approach: maintenance schedules, checklists, and prevention over reactive repair.

**Hierarchy Ownership:**
- L1.3 Shelter — housing security, mortgage status, living situation stability
- L1.5 Physical Safety — personal safety, vehicle safety, home security, insurance coverage
- L2.3 Home & Property — maintenance schedules, vehicle service, household systems, organisation
- L2.6 Digital Life — passwords, backups, subscriptions, digital organisation, security

**Decision Frameworks:**
- Maintenance: scheduled prevention > reactive repair. Annual maintenance calendar.
- Purchase: need vs want, longevity vs cost, does it reduce ongoing friction?
- Digital: password manager, backup strategy, subscription audit quarterly

**Escalation Triggers:**
- Safety issue in the home (electrical, structural, security)
- Vehicle overdue for service or registration
- Insurance lapse or policy renewal missed
- Major appliance failure affecting daily life
- Data loss risk (backup failure, compromised accounts)

### 6.5 Relationships

**Identity:** Extended family, friends, and professional network — the people outside the inner family circle who matter. This domain is about intentional maintenance, not letting relationships decay through neglect. Tracks contact frequency, important dates, and reciprocity. Honest about the reality that a busy CEO and father will lose relationships without a system.

**Hierarchy Ownership:**
- L3.3 Friendships — depth and breadth, social investment, reciprocity
- L3.4 Community — involvement, contribution, belonging outside family/work (shared with Coaching)
- L3.5 Professional Network — industry relationships, mentors, peer group

**Decision Frameworks:**
- Contact priority: who haven't I spoken to that I should? Weighted by relationship importance and time since last contact.
- Event response: birthday/milestone approaching → what's the appropriate response for this relationship?
- Investment vs drain: is this relationship reciprocal? Energy-giving or energy-draining?

**Escalation Triggers:**
- Parent not contacted in >14 days
- Close friend not contacted in >30 days
- Important date missed (birthday, anniversary, milestone)
- Relationship conflict unresolved
- Feeling socially isolated

### 6.6 Growth

**Identity:** Personal development, learning, career progression, creative projects, and life design. The domain that asks "am I becoming who I want to be?" Covers both structured learning (courses, reading) and experiential growth (projects, experiments). Parent domain for Languages. Balances ambition with the reality of available time and energy.

**Hierarchy Ownership:**
- L4.1 Career Development — skills, progression, positioning (shared with Coaching, AI & ML)
- L4.2 Learning — active learning, reading, courses, new capabilities (shared with AI & ML)
- L4.3 Creative Projects — side projects, hobbies with intention (shared with AI & ML)
- L5.1 Purpose Clarity — do you know what you're building toward?
- L5.4 Life Design — is your life structure aligned with your values?

**Decision Frameworks:**
- Learning ROI: will this skill compound? Does it serve multiple domains or just one?
- Project filter: does this project advance a goal, or is it procrastination disguised as productivity?
- Time allocation: growth activities must not cannibalise L1-L3 foundations

**Escalation Triggers:**
- No learning activity in >2 weeks
- Creative project stalled for >1 month with no decision to continue or kill
- Career feels stagnant — no progression signal in >3 months
- Life design misalignment — values say one thing, calendar says another

### 6.7 Growth > Languages

**Identity:** Active language learning across five target languages: Cantonese, Mandarin, Korean, Spanish, and Japanese. Nested under Growth as a sub-domain because language learning is a specific, trackable component of L4.2 Learning. Each language has its own proficiency level, method, and practice cadence. Practical communication focus over academic perfection.

**Hierarchy Ownership:**
- Sub-component of L4.2 Learning

**Per-Language Tracking:**
- Current proficiency level (beginner / elementary / intermediate / advanced)
- Active learning method (app, tutor, immersion, course)
- Practice frequency target and actual
- Next milestone

**Decision Frameworks:**
- Priority ranking: which language gets focus this quarter? Based on opportunity (travel, business, community) and momentum.
- Method selection: what's working? What's not? Switch methods before quitting a language.
- Time budget: languages share a fixed time allocation — adding one means reducing another or expanding the budget.

**Escalation Triggers:**
- No practice in any language for >1 week
- A language with active investment showing no progress over 2 months

### 6.8 Coaching

**Identity:** Dual-purpose domain. Outward: smckennie's roles as basketball coach and business coach — planning, people management, leadership development, game strategy. Inward: the system coaching smckennie on personal behaviour and habits (put down the phone, get to bed, follow through on commitments). Coaching others teaches leadership; being coached prevents drift.

**Hierarchy Ownership:**
- L3.4 Community — coaching is a form of community contribution (shared with Relationships)
- L4.1 Career Development — coaching skills transfer to professional leadership (shared with Growth)
- L5.2 Contribution — what are you giving back to others?

**Decision Frameworks:**
- Basketball coaching: season planning, player development priorities, game preparation
- Business coaching: client focus, framework selection, session preparation
- Self-coaching: behaviour triggers (time of day, context) → nudge (specific, actionable, non-judgmental)

**Escalation Triggers:**
- Basketball: game/training unprepared
- Business coaching: client session unprepared
- Self-coaching: same behaviour correction needed >3 times without change (escalate to Strategic Command — the system isn't working, need a structural intervention)

### 6.9 AI & ML

**Identity:** Developing expertise in AI, ML, and Claude specifically to build business infrastructure and personal projects (e.g., cantoneseplus.com). Practical builder focus — not academic ML theory, but hands-on proficiency with the tools, APIs, SDKs, and patterns needed to ship AI-powered products. Stays current with Claude capabilities, Anthropic documentation, and emerging best practices.

**Hierarchy Ownership:**
- L4.1 Career Development — AI/ML skills as professional differentiator (shared with Growth, Coaching)
- L4.2 Learning — active technical learning (shared with Growth)
- L4.3 Creative Projects — building AI-powered products (shared with Growth)

**Key Resources:**
- Claude API & SDK documentation: https://docs.claude.com/
- Anthropic learning resources: https://www.anthropic.com/learn
- Tutorials: https://claude.com/resources/tutorials
- PLAIOS itself as a learning vehicle — building it develops the skills

**Decision Frameworks:**
- Build vs learn: is this a learning exercise or a shipping exercise? Different standards apply.
- Tool selection: use the simplest tool that solves the problem. Don't over-engineer for learning's sake.
- Project viability: does this project have a user (even if just me)? If not, it's a tutorial, not a project.

**Escalation Triggers:**
- Major API/SDK breaking change that affects active projects
- Project blocked on a technical capability gap for >1 week
- No hands-on building activity in >2 weeks (reading without doing)

---

## 7. Cross-Cutting Systems

### 7.1 Central Memory (`memory/`)

| File | Purpose |
|------|---------|
| `people.md` | Key people — family, advisors, doctors, coaches, tradespeople, contacts |
| `systems.md` | Tools, apps, accounts, integrations (not passwords) |
| `decisions.md` | Index of significant decisions with dates and rationale |
| `patterns.md` | Recurring patterns, lessons learned, what works and doesn't |
| `calendar.md` | Key dates — renewals, appointments, deadlines, anniversaries |

### 7.2 Journal (`journal/`)

- `session-log.md` — append-only, one entry per session (format: see framework Section 7)
- `decisions/` — consequential decision records (format: see framework Section 7, "Decision Records")

### 7.3 Protocols (`protocols/`)

Shared formats and templates used across domains. Formats are defined in the framework document and cross-referenced here for implementation:

- `assessment-template.md` — maturity rating format (see framework Section 6)
- `decision-record-template.md` — consequential decision format (see framework Section 7)
- `session-checklist.md` — opening and closing session protocol (see framework Section 9)

### 7.4 Privacy Considerations

Some domain data is sensitive and should not be surfaced casually (e.g., during screen shares or in cross-domain summaries):

| Domain | Sensitive Data | Handling |
|--------|---------------|----------|
| **Family** | Partner relationship details, children's developmental information (especially Evie's autism) | Exclude from hot-tier summaries by default. Require explicit query to surface. |
| **Health** | Medical history, family member health conditions, breastfeeding status | Exclude per-family-member medical details from cross-domain views. |
| **Finance** | Specific balances, debt amounts, income figures | Show status/rating in summaries, not specific numbers. |
| **Relationships** | Relationship dynamics, conflict details | Exclude from cross-domain summaries. |

General rule: cross-domain summaries show **status and alerts**, not **detail**. Detail requires navigating into the domain.

### 7.5 Cross-Domain Escalation Patterns

Strategic Command detects systemic issues by looking for correlated signals across domains. Examples:

- **Sleep degradation** (Health) + **mood drop** (Health) + **missed workouts** (Health) + **relationship friction** (Family) = burnout risk, not four independent problems
- **Financial stress** (Finance) + **work hours increasing** (Growth) + **family disconnect** (Family) = work-life balance crisis
- **Multiple domains reporting routine breakdown** (L2.4 cross-cutting) = systemic capacity issue

These patterns are Strategic Command's responsibility, not any single domain's. When detected, Strategic Command identifies the root cause domain and escalates there rather than treating symptoms in each domain independently.

### 7.6 Review Cadence

| Frequency | Scope | Purpose |
|-----------|-------|---------|
| **Weekly** | Quick scan of all domain statuses | Catch anything slipping before it becomes structural |
| **Monthly** | Deep review of 2-3 domains (rotating) | Update assessments, review trends, adjust priorities |
| **Quarterly** | Full assessment across all levels | Recalibrate hierarchy ratings, update thresholds, strategic direction |

---

## 8. Implementation Order

Root `CLAUDE.md` (Strategic Command) is written first, before any domains. Then domains are built in sequence. Each domain follows the same process: create directory structure, write `claude.md`, write `manifest.md`, create initial `state/current-assessment.md`.

| Order | Domain | Rationale |
|-------|--------|-----------|
| 0 | **Strategic Command** (root CLAUDE.md) | Foundation — everything references it |
| 1 | **Health** | APEX prompt exists as source material — fastest to build, validates the pattern |
| 2 | **Finance** | L1-heavy domain — highest hierarchy priority after Health |
| 3 | **Family** | L3 core — most personally impactful domain |
| 4 | **Home** | L1-L2 infrastructure — foundational stability |
| 5 | **Relationships** | L3 extended — builds on Family patterns |
| 6 | **Growth** | L4-L5 — parent domain needed before Languages |
| 7 | **Growth > Languages** | Sub-domain of Growth — requires Growth to exist first |
| 8 | **Coaching** | L3-L5 hybrid — cross-cutting, benefits from other domains being established |
| 9 | **AI & ML** | L4 focused — least urgent, most likely to evolve as PLAIOS itself develops |

---

## 9. Relationship to Existing PLAIOS Spec

The original PLAIOS design spec (`2026-03-12-plaios-design.md`) defined an MCP server architecture with orchestrator, domain agents, connectors, and workers. This domain architecture spec defines the **context and assessment layer** — the structured knowledge, decision frameworks, and state that those agents would operate on.

The two specs are complementary:
- **This spec** defines what each domain knows, how it assesses, and how it decides
- **The MCP spec** defines how domains are invoked, how they communicate, and how they integrate with external services

The cascade `claude.md` architecture also serves as an immediate, functional system — usable today via Claude Code's native `CLAUDE.md` loading — while the MCP server infrastructure is built incrementally.

### 9.1 Domain Mapping: MCP Spec → This Spec

The MCP spec defined 5 domain agents. This spec defines 9 domains. The mapping:

| MCP Spec Agent | This Spec Domain(s) | Notes |
|---------------|---------------------|-------|
| Relationships Agent | **Relationships** + **Family** | Split: Family = inner circle, Relationships = extended |
| Romance Agent | **Family** (L3.1 Partner/Family) | Folded into Family as the partner relationship dimension |
| Fitness Agent | **Health** | Expanded from fitness to full health/medical/nutrition |
| Professional Agent | **Growth** + **Coaching** + **AI & ML** | Decomposed into three more specific domains |
| Wellbeing Agent | **Health** (mental health) + **Coaching** (self-coaching) | Distributed across domains rather than standalone |

The MCP spec's Orchestrator maps to this spec's Strategic Command (root `CLAUDE.md`). The MCP spec's connectors and workers are infrastructure concerns orthogonal to the domain context layer defined here. When the MCP server is built, its domain agents will load the `claude.md` files defined in this spec as their system prompts.
