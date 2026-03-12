# Personal AI Operating System — Architecture Framework

> **Purpose:** Blueprint for building a personal life management system using AI agents with structured context, persistent memory, and hierarchical assessment. Adapted from RAIOS (RapidMap AI Operating System) — a production system used to manage a 34-year, 20+ person business across 6 functional domains.
>
> **How to use this document:** Feed this to an AI assistant and ask it to help you map out your personal life using this framework. Customise the hierarchy, domains, and priorities to your situation.

---

## 1. CORE CONCEPT

You are building a **personal command centre** — a system that helps you:
- See your whole life clearly (not just the urgent parts)
- Identify what's structurally weak before it becomes a crisis
- Make decisions with full context across all life domains
- Track what you've learned, decided, and need to do
- Maintain continuity across AI conversations (persistent memory)

The system is NOT a to-do list. It's an **assessment and direction-setting layer** that sits above your tasks and helps you prioritise, connect patterns, and avoid the trap of being consumed by whatever feels most urgent.

---

## 2. THE CASCADE ARCHITECTURE

### How It Works

One root prompt (Strategic Command) loads in every session. When working on a specific life domain, that domain's specialist context layers on top.

```
personal-os/
  claude.md                    ← ROOT: Strategic Command (always loaded)
  /domains/
    /health/claude.md          ← Health & Fitness domain
    /finance/claude.md         ← Personal Finance domain
    /career/claude.md          ← Career & Professional Development
    /relationships/claude.md   ← Family, Friends, Community
    /home/claude.md            ← Property, Vehicles, Household
    /growth/claude.md          ← Learning, Projects, Purpose
  /memory/                     ← Cross-cutting persistent knowledge
  /journal/                    ← Session log and decision records
  /protocols/                  ← Shared formats
```

**The cascade rule:** Working at root level = strategic thinking across all domains. Working inside a domain directory = specialist focus with strategic awareness still active.

### Three-Layer Context Model

Every domain operates with three layers — this prevents overloading the AI with information it doesn't need for the current task:

| Layer | What It Contains | When It Loads | Size Target |
|-------|-----------------|---------------|-------------|
| **Core** (always loaded) | Identity, decision frameworks, escalation triggers, context protocol | Session start — automatic | ~150 lines per domain |
| **Indexed** (on demand) | Reference material — checklists, detailed criteria, procedures, history | Agent loads via manifest when task requires | Variable |
| **Discoverable** (external) | Calendar, email, documents, spreadsheets, apps | Agent queries when local context insufficient | Variable |

### The Manifest

Each domain has a `manifest.md` — a lightweight index of all available context. It tells the AI:
- What files exist
- One-line summary of each
- Approximate size
- When to load each file

```markdown
# Health Domain — Context Manifest

## Always Loaded
| File | Summary | Lines |
|------|---------|-------|
| claude.md | Core identity, health philosophy, escalation triggers | ~120 |
| memory.md | Accumulated health knowledge — conditions, preferences, history | ~40 |
| state/current-assessment.md | Current health ratings across dimensions | ~20 |

## On-Demand Reference
| File | Summary | Lines | Load When |
|------|---------|-------|-----------|
| reference/medical-history.md | Conditions, medications, allergies, providers | ~60 | Medical appointments, health decisions |
| reference/fitness-programme.md | Current training plan, targets, progression | ~40 | Workout planning, fitness assessment |
| reference/nutrition.md | Dietary approach, meal patterns, supplements | ~30 | Nutrition questions, meal planning |
```

---

## 3. THE PERSONAL HIERARCHY OF NEEDS

This is the core assessment framework. Every issue, decision, and recommendation gets located within this hierarchy. **Lower levels must be stable before investing at higher levels.**

```
STRATEGIC COMMAND (assessment + direction)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│
│   ┌─────────────────────────────────┐
│   │  5. LEGACY & MEANING            │  Purpose, contribution, what you leave behind
│   ├─────────────────────────────────┤
│   │  4. GROWTH & MASTERY            │  Learning, skills, projects, self-actualisation
│   ├─────────────────────────────────┤
│   │  3. CONNECTION & BELONGING      │  Relationships, community, social life
│   ├─────────────────────────────────┤
│   │  2. STABILITY & SYSTEMS         │  Routines, health systems, financial controls,
│   │                                 │  home maintenance, legal, insurance
│   ├─────────────────────────────────┤
│   │  1. SURVIVAL & SAFETY           │  Income, health emergencies, shelter, debt,
│   │                                 │  immediate threats
│   └─────────────────────────────────┘
│
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXTERNAL ENVIRONMENT (sensing what's changing)
```

### Hierarchy Rules

- Lower levels unstable → fix before investing at higher levels
- Crises at lower levels demand immediate attention regardless of aspirations
- Work multiple levels simultaneously, but always reinforce foundations first
- Every dimension needs a feedback loop — no self-correction = structurally fragile
- After every rating, ask: "What is this score not telling me about my lived experience?"

### Suggested Dimensions Per Level

Customise these to your life. Below is a starting template:

#### Level 1 — Survival & Safety
| Dimension | What It Covers |
|-----------|---------------|
| **Income** | Employment stability, income sources, job security, runway if income stops |
| **Acute Health** | Medical emergencies, urgent health issues, mental health crises |
| **Shelter** | Housing security, lease/mortgage status, living situation stability |
| **Debt & Obligations** | High-interest debt, legal obligations, tax compliance, child support |
| **Physical Safety** | Personal safety, vehicle safety, home security, insurance coverage |

#### Level 2 — Stability & Systems
| Dimension | What It Covers |
|-----------|---------------|
| **Financial Management** | Budget, savings rate, investment strategy, tax planning, insurance adequacy |
| **Health Systems** | Regular exercise, nutrition, sleep, preventive care, mental health practices |
| **Home & Property** | Maintenance schedules, vehicle service, household systems, organisation |
| **Routines & Habits** | Daily/weekly/monthly routines, time management, energy management |
| **Legal & Admin** | Wills, insurance, registrations, licenses, important document management |
| **Digital Life** | Passwords, backups, subscriptions, digital organisation, security |

#### Level 3 — Connection & Belonging
| Dimension | What It Covers |
|-----------|---------------|
| **Partner / Family** | Quality of primary relationships, communication, shared goals |
| **Children** | Parenting quality, education, development, presence |
| **Friendships** | Depth and breadth of friendships, social investment, reciprocity |
| **Community** | Involvement, contribution, belonging outside family/work |
| **Professional Network** | Industry relationships, mentors, peer group |

#### Level 4 — Growth & Mastery
| Dimension | What It Covers |
|-----------|---------------|
| **Career Development** | Skills, progression, positioning, professional growth |
| **Learning** | Active learning, reading, courses, new capabilities |
| **Creative Projects** | Side projects, hobbies pursued with intention, making things |
| **Physical Performance** | Fitness goals beyond baseline health — strength, endurance, sport |

#### Level 5 — Legacy & Meaning
| Dimension | What It Covers |
|-----------|---------------|
| **Purpose Clarity** | Do you know what you're building toward? Is it guiding decisions? |
| **Contribution** | What are you giving back — to family, community, industry, world? |
| **Wealth Building** | Long-term financial independence, generational wealth, asset base |
| **Life Design** | Is your life structure aligned with your values, or have you drifted? |

### Maturity Scale

| Rating | Label | Definition |
|--------|-------|-----------|
| 1 | **Crisis** | Failing or non-existent. Immediate risk. No feedback loop. |
| 2 | **Fragile** | Exists but unreliable, depends on willpower or luck. Breaks under stress. |
| 3 | **Functional** | Works but not optimised. Manual, inconsistent. You manage it but it doesn't manage itself. |
| 4 | **Systematic** | Documented routine, measured, consistently followed. Some automation. Self-correcting. |
| 5 | **Optimised** | Automated where possible, continuously improving, resilient. Works even when you're not thinking about it. |

---

## 4. DOMAIN STRUCTURE

### Root claude.md (Strategic Command)

The root prompt should contain:
- Your identity summary (who you are, what phase of life, key context)
- The hierarchy framework (levels, dimensions, maturity scale)
- Priority algorithm
- Domain-to-hierarchy mapping
- Escalation triggers (when to flag something as urgent)
- Session protocol (what to read on session start)
- Systems thinking reminders

### Domain claude.md (Each Life Area)

Each domain prompt should contain:
- Domain identity (what this area covers, your philosophy/approach)
- Hierarchy ownership (which dimensions this domain owns)
- Current state summary (key facts, active concerns)
- Decision frameworks (how to make decisions in this area)
- Escalation triggers (when something needs immediate attention)
- Context protocol (how to load more information)

### Example Domain: Personal Finance

```markdown
# Personal Finance Domain

## Identity
This domain manages all financial dimensions of your life — income, spending,
saving, investing, tax, insurance, and wealth building. It operates across
Survival (L1: income, debt), Stability (L2: budget, controls, insurance),
and Legacy (L5: wealth building, financial independence).

## Hierarchy Ownership
- L1.1 Income — employment stability, income diversification
- L1.4 Debt & Obligations — debt reduction, compliance
- L2.1 Financial Management — budget, savings, investments, tax
- L2.5 Legal & Admin — insurance, wills (shared with Home domain)
- L5.3 Wealth Building — long-term asset strategy, financial independence

## Decision Frameworks
### Spending Decision
- Is it budgeted? If no, what gets cut?
- Does it serve a dimension rated 1-2? (Priority spend)
- Does it advance a Level 4-5 goal? (Investment spend)
- Is it neither? (Discretionary — apply the 48-hour rule)

### Investment Decision
- Emergency fund funded first (3-6 months expenses)
- High-interest debt cleared second
- Tax-advantaged accounts maximised third
- Then: diversified investment per strategy

## Escalation Triggers
- Income loss or >20% reduction
- Unexpected expense >$5,000 without budget coverage
- Debt-to-income ratio exceeds 30%
- Insurance lapse or coverage gap discovered
- Tax obligation missed
```

---

## 5. MEMORY SYSTEM

Memory is how the system retains knowledge across conversations. Without it, every session starts from zero.

### Central Memory (`memory/`)

Cross-cutting knowledge that applies across all domains:

| File | Purpose |
|------|---------|
| `people.md` | Key people in your life — family, advisors, doctors, tradespeople, contacts |
| `systems.md` | Tools, apps, accounts, integrations, login locations (not passwords) |
| `decisions.md` | Index of significant decisions with dates and rationale |
| `patterns.md` | Recurring patterns, lessons learned, things that work/don't work for you |
| `calendar.md` | Key dates — renewals, appointments, deadlines, anniversaries |

### Domain Memory (`domains/*/memory.md`)

Per-domain knowledge accumulated across sessions. Each domain owns its memory file. Examples:
- Health domain: medical conditions, medication history, provider contacts, what works for fitness
- Finance domain: account structures, tax strategy decisions, investment approach, advisor contacts
- Relationships domain: important dates, communication patterns, relationship dynamics

### Memory Rules

1. **Update when stable knowledge is confirmed** — not speculative, not session-specific
2. **Memory is a living document** — edit and correct, don't just append
3. **When facts change, update the memory** — moved house? Changed doctor? Update.
4. **Memory is for accumulated knowledge, not current state** — state files handle what's active now
5. **No duplicates** — check before adding, update existing entries

---

## 6. STATE MANAGEMENT

State files track what's happening NOW — current assessments, active priorities, things in progress.

### Per Domain:

```
domains/health/state/
  current-assessment.md    ← Latest maturity ratings per dimension
  active-priorities.md     ← What's being worked on
```

### Assessment Format

```markdown
# Health — Current Assessment

**Last Updated:** 2026-03-12
**Next Review:** 2026-04-12

| Dimension | Rating | Trend | Key Finding |
|-----------|--------|-------|-------------|
| Exercise | 3 | ↑ | Consistent 3x/week. Need to add mobility work. |
| Nutrition | 2 | → | Meal prep inconsistent. Lunch defaults to takeaway. |
| Sleep | 2 | ↓ | Averaging 5.5 hours. Screen time before bed increasing. |
| Mental Health | 3 | → | Meditation practice holding. Stress from work manageable. |
| Preventive Care | 1 | → | Overdue: dentist (8 months), blood work (14 months). |
```

---

## 7. JOURNAL SYSTEM

The journal creates an audit trail of what happened across sessions. Append-only.

### Session Log (`journal/session-log.md`)

One entry per session:

```markdown
## 2026-03-12 | Finance | Quarterly Review
Reviewed Q1 spending vs budget. Over by 12% on discretionary.
Savings rate dropped to 15% (target 25%). Root cause: two unplanned
trips and subscription creep. Actions: cancel 3 subscriptions, set
up auto-transfer to savings on payday.
```

### Decision Records (`journal/decisions/`)

For consequential decisions — not routine. Format:

```markdown
# Decision: [Title]
**Date:** 2026-03-12
**Domain:** Finance
**Context:** [What prompted this decision]
**Options Considered:** [What alternatives were evaluated]
**Decision:** [What was decided and why]
**Expected Outcome:** [What should happen as a result]
**Review Date:** [When to check if it worked]
```

Examples of what warrants a decision record:
- Changing jobs, accepting/declining an offer
- Major purchase (property, vehicle)
- Investment strategy change
- Health treatment decision
- Relationship boundary decision
- Moving house

---

## 8. PRIORITY ALGORITHM

Simple scoring across three dimensions (max score = 8):

| Dimension | Scale | Definition |
|-----------|-------|-----------|
| **Hierarchy Level** | 1-5 | Survival=1 (most urgent), Legacy=5 |
| **Urgency** | 1-2 | 1=can wait, 2=time-critical |
| **Only-me** | 0-1 | 0=can delegate/automate, 1=only I can do this |

**Score = (6 - Hierarchy Level) + Urgency + Only-me**

Higher score = higher priority.

Examples:
- Overdue tax return (L1, urgent, only-me): (6-1) + 2 + 1 = **8** → do immediately
- Dentist appointment (L2, not urgent, only-me): (6-2) + 1 + 1 = **6** → schedule this week
- Research investment options (L5, not urgent, delegable): (6-5) + 1 + 0 = **2** → batch for later

---

## 9. SESSION PROTOCOL

### Opening Each Session

1. What level of the hierarchy is this session about?
2. Read `manifest.md` (if in a domain) to see what's available
3. Read `memory.md` for accumulated knowledge
4. Read `state/` files for current operational state
5. Any time-critical items?
6. If working at a higher level but lower levels are unstable, flag the dependency
7. Load reference material from `reference/` as needed — not upfront

### Closing Each Session

1. Append session summary to `journal/session-log.md`
2. If consequential decisions were made, create decision records
3. Update memory files if stable new knowledge was confirmed
4. Update state files if assessments or priorities changed

---

## 10. EXTERNAL ENVIRONMENT SENSING

Personal equivalent of market/competitive sensing:

| Domain | What to Monitor | Frequency |
|--------|----------------|-----------|
| Career | Industry trends, company health, role market value, network signals | Monthly |
| Finance | Interest rates, tax changes, investment performance, insurance market | Quarterly |
| Health | New health research relevant to your conditions, preventive care guidelines | Quarterly |
| Property | Property values, maintenance obligations, insurance adequacy, rates/levies | Annually |
| Relationships | Life stage changes in key relationships, community shifts | Ongoing |

---

## 11. SYSTEMS THINKING REMINDERS

Three lenses to apply (simplified from the business version):

### 1. Feedback Loops
Every dimension needs a way to self-correct. If the only feedback loop is "I notice when things get bad," that's a fragile system. Build in:
- Regular check-ins (weekly review, monthly assessment, quarterly deep dive)
- Automated alerts (calendar reminders, app notifications, auto-debits)
- Leading indicators (not just lagging — track inputs, not just outcomes)

### 2. Variety Matching
Your response capability must match the complexity of your life. If life gets more complex (new child, new job, health issue), your management systems need to scale too. The AI operating system helps amplify your variety without proportional time investment.

### 3. Hemisphere Balance
Left brain: measure, track, systematise, optimise.
Right brain: meaning, relationships, intuition, lived experience.
Both matter. After every quantitative rating, ask: "What is this score not telling me about how I actually feel?"

---

## 12. IMPLEMENTATION SEQUENCE

### Phase 1: Foundation (Session 1-2)
- Define YOUR hierarchy dimensions (customise the template above)
- Create the directory structure
- Write root claude.md with your context and hierarchy
- Do an initial honest assessment across all levels
- Identify the 2-3 dimensions rated 1-2 that need immediate attention

### Phase 2: Priority Domains (Session 3-5)
- Build out the 2-3 domains that contain your lowest-rated dimensions
- Create domain claude.md, manifest, memory, and state files
- Start the journal with session logs

### Phase 3: Full Coverage (Session 6-10)
- Build remaining domains
- Cross-reference domains (what does Finance need from Health? Career from Relationships?)
- Establish review cadence (weekly quick scan, monthly domain review, quarterly full assessment)

### Phase 4: Refinement (Ongoing)
- Tune based on what you actually use
- Prune what doesn't work
- Evolve the hierarchy as your life changes
- Build reference material as needed

---

## 13. WHAT MAKES THIS DIFFERENT FROM A TO-DO APP

| To-Do App | This System |
|-----------|-------------|
| Tracks tasks | Assesses life health across dimensions |
| Shows what's due | Shows what's structurally weak |
| Organises by project | Organises by hierarchy level |
| No memory between sessions | Persistent knowledge across conversations |
| Treats everything equally | Forces prioritisation by survival → legacy |
| Reactive (what's overdue?) | Proactive (what's fragile before it breaks?) |
| No feedback loops | Built-in self-correction mechanisms |
| No assessment framework | Maturity scale with trend tracking |

---

## 14. QUICK START PROMPT

Feed this to a new AI session to get started:

```
I want to build a Personal AI Operating System based on the attached framework.

Help me:
1. Customise the hierarchy dimensions to MY life (I'll tell you about my situation)
2. Do an initial honest assessment across all levels (rate each dimension 1-5)
3. Identify the structural weaknesses (what's rated 1-2 at Level 1-2?)
4. Create the directory structure and root prompt
5. Build the first priority domain based on my lowest ratings

Key principles:
- Be honest. Uncomfortable truths prevent crises.
- Lower levels before higher levels.
- Systems over willpower.
- Feedback loops everywhere.
- Memory persists across sessions.
```

---

*Personal AI Operating System — Architecture Framework v1.0*
*Adapted from RAIOS (RapidMap AI Operating System)*
*Architecture: Cascade (root + domain context layering)*
