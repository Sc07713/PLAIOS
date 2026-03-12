# PLAIOS Domain Scaffolding — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the full PLAIOS cascade architecture — root Strategic Command, 9 domain directories with claude.md files, cross-cutting memory/journal/protocols, and the Health domain fully decomposed from the APEX prompt.

**Architecture:** Cascade of CLAUDE.md files. Root = Strategic Command (always loaded). Each domain directory has its own claude.md that layers on top. Three-layer context model: core (always), indexed (on demand via manifest), discoverable (external).

**Tech Stack:** Markdown + YAML frontmatter. No code — this is a context architecture, not a software build.

**Spec:** `docs/superpowers/specs/2026-03-12-plaios-domains-design.md`
**Framework:** `docs/personal-os-architecture-framework.md`

---

## Chunk 1: Foundation (Strategic Command + Cross-Cutting)

### Task 1: Create root CLAUDE.md — Strategic Command

**Files:**
- Modify: `CLAUDE.md` (replace current 14-line placeholder)

- [ ] **Step 1: Write Strategic Command root CLAUDE.md**

Replace the current CLAUDE.md with Strategic Command. Content per spec Section 3:

```markdown
# PLAIOS — Strategic Command

You are operating within PLAIOS (Personal Life AI Operating System) — a personal command centre for smckennie.

## Identity

Scott McKennie. CEO, father of four, based in Australia. Wife: Mina. Children: Wulfric (12), Audrey (10), Evie (8), Penny (toddler). Time-constrained — demands maximum results from minimum investment.

## Purpose

PLAIOS is an assessment and direction-setting layer, not a to-do list. It:
- Surfaces structural weakness before it becomes crisis
- Provides full context across all life domains
- Maintains continuity across AI conversations
- Prioritises by hierarchy level, not by what feels most urgent

## Personal Hierarchy of Needs

Lower levels must be stable before investing at higher levels.

| Level | Name | Focus |
|-------|------|-------|
| L1 | Survival & Safety | Income, acute health, shelter, debt, physical safety |
| L2 | Stability & Systems | Financial management, health systems, home, routines, legal/admin, digital life |
| L3 | Connection & Belonging | Partner/family, children, friendships, community, professional network |
| L4 | Growth & Mastery | Career development, learning, creative projects, physical performance |
| L5 | Legacy & Meaning | Purpose clarity, contribution, wealth building, life design |

## Maturity Scale

| Rating | Label | Definition |
|--------|-------|-----------|
| 1 | Crisis | Failing or non-existent. Immediate risk. No feedback loop. |
| 2 | Fragile | Exists but unreliable. Breaks under stress. |
| 3 | Functional | Works but not optimised. Manual, inconsistent. |
| 4 | Systematic | Documented, measured, consistently followed. Self-correcting. |
| 5 | Optimised | Automated where possible, continuously improving, resilient. |

## Domains

| Domain | Path | Hierarchy Dimensions |
|--------|------|---------------------|
| Health | `domains/health/` | L1.2, L2.2, L4.4 |
| Finance | `domains/finance/` | L1.1, L1.4, L2.1, L2.5, L5.3 |
| Family | `domains/family/` | L3.1, L3.2 |
| Home | `domains/home/` | L1.3, L1.5, L2.3, L2.6 |
| Relationships | `domains/relationships/` | L3.3, L3.4, L3.5 |
| Growth | `domains/growth/` | L4.1, L4.2, L4.3, L5.1, L5.4 |
| Languages | `domains/growth/languages/` | Sub-component of L4.2 |
| Coaching | `domains/coaching/` | L3.4, L4.1, L5.2 |
| AI & ML | `domains/ai-ml/` | L4.1, L4.2, L4.3 |

L2.4 (Routines & Habits) is cross-cutting — each domain owns its own routines.

## Priority Algorithm

Score = (6 - Hierarchy Level) + Urgency (1-2) + Only-me (0-1). Max = 8. Higher = do first.

## Escalation Rules

- Any dimension rated 1 at L1-L2 → immediate attention
- Cross-domain pattern detection: correlated signals across domains indicate systemic issues (e.g., sleep + mood + missed workouts = burnout, not three problems)
- When detected, identify root cause domain — treat the cause, not each symptom

## Session Protocol

1. What level of the hierarchy is this session about?
2. Read relevant domain state files
3. Flag time-critical items
4. If working at a higher level, check if lower levels are unstable — flag the dependency

## Privacy

Cross-domain summaries show status and alerts, not detail. Sensitive data (Family relationship details, Health medical history, Finance specific numbers, Relationships dynamics) requires explicit navigation into the domain.

## Systems Thinking

- **Feedback loops**: Every dimension needs self-correction. If the only loop is "I notice when it's bad," it's fragile.
- **Variety matching**: Management systems must scale with life complexity.
- **Hemisphere balance**: After every quantitative rating, ask: "What is this score not telling me about how I actually feel?"
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "Replace placeholder CLAUDE.md with Strategic Command root prompt"
```

### Task 2: Create cross-cutting directories and files

**Files:**
- Create: `memory/people.md`
- Create: `memory/systems.md`
- Create: `memory/decisions.md`
- Create: `memory/patterns.md`
- Create: `memory/calendar.md`
- Create: `journal/session-log.md`
- Create: `protocols/assessment-template.md`
- Create: `protocols/decision-record-template.md`
- Create: `protocols/session-checklist.md`

- [ ] **Step 1: Create memory/ files**

Each file starts with a header and empty structure ready for content:

`memory/people.md`:
```markdown
# People

Key people in smckennie's life — family, advisors, doctors, coaches, tradespeople, contacts.

## Family
- **Mina** — wife, co-parent
- **Wulfric** (12) — eldest son
- **Audrey** (10) — daughter, basketball + cross country
- **Evie** (8) — daughter, autism (OT, speech therapy)
- **Penny** — toddler

## Advisors & Professionals
<!-- Add as encountered: accountant, doctor, dentist, etc. -->

## Tradespeople & Services
<!-- Add as encountered -->

## Key Contacts
<!-- Friends, mentors, professional network with context -->
```

`memory/systems.md`:
```markdown
# Systems

Tools, apps, accounts, and integrations used across domains. No passwords — just what exists, where, and what it's for.

## AI & Development
- **Claude Code** — primary development interface for PLAIOS
- **Claude Desktop** — conversational interface, visual artifacts
- **Claude Mobile** — on-the-go data collection

## Productivity
<!-- Add as encountered: calendar, email, task management, etc. -->

## Financial
<!-- Add as encountered: banking, accounting, investment platforms -->

## Health & Fitness
<!-- Add as encountered: fitness apps, health trackers -->
```

`memory/decisions.md`:
```markdown
# Decisions

Index of significant decisions with dates and rationale. For full decision records, see `journal/decisions/`.

| Date | Domain | Decision | Record |
|------|--------|----------|--------|
<!-- Add as decisions are made -->
```

`memory/patterns.md`:
```markdown
# Patterns

Recurring patterns, lessons learned, things that work and don't work.

## What Works
<!-- Add as confirmed -->

## What Doesn't Work
<!-- Add as confirmed -->

## Recurring Patterns
<!-- Add as observed -->
```

`memory/calendar.md`:
```markdown
# Calendar

Key dates — renewals, appointments, deadlines, anniversaries. Not day-to-day scheduling — structural dates that matter.

## Birthdays & Anniversaries
<!-- Add family, close friends, key dates -->

## Renewals & Deadlines
<!-- Insurance, registrations, tax deadlines, etc. -->

## Recurring Commitments
<!-- Coaching seasons, school terms, etc. -->
```

- [ ] **Step 2: Create journal/ files**

`journal/session-log.md`:
```markdown
# Session Log

One entry per PLAIOS session. Append-only.

<!-- Format:
## YYYY-MM-DD | Domain(s) | Brief Title
Summary of what was discussed, decided, or changed.
-->
```

Create empty `journal/decisions/` directory with a `.gitkeep`.

- [ ] **Step 3: Create protocols/ files**

`protocols/assessment-template.md`:
```markdown
# Assessment Template

Use this format for domain current-assessment.md files.

---

**Last Updated:** YYYY-MM-DD
**Next Review:** YYYY-MM-DD

| Dimension | Rating | Trend | Key Finding |
|-----------|--------|-------|-------------|
| [Dimension name] | [1-5] | [↑ → ↓] | [One-line finding] |

**Overall Domain Status:** [Crisis / Fragile / Functional / Systematic / Optimised]

**Top Priority:** [Single most important action for this domain]
```

`protocols/decision-record-template.md`:
```markdown
# Decision: [Title]

**Date:** YYYY-MM-DD
**Domain:** [Domain name]
**Context:** [What prompted this decision]
**Options Considered:** [What alternatives were evaluated]
**Decision:** [What was decided and why]
**Expected Outcome:** [What should happen as a result]
**Review Date:** [When to check if it worked]
```

`protocols/session-checklist.md`:
```markdown
# Session Checklist

## Opening
1. What level of the hierarchy is this session about?
2. Read `manifest.md` (if in a domain) to see what's available
3. Read `memory.md` for accumulated knowledge
4. Read `state/` files for current operational state
5. Any time-critical items?
6. If working at a higher level but lower levels are unstable, flag the dependency
7. Load reference material from `reference/` as needed — not upfront

## Closing
1. Append session summary to `journal/session-log.md`
2. If consequential decisions were made, create decision records in `journal/decisions/`
3. Update memory files if stable new knowledge was confirmed
4. Update state files if assessments or priorities changed
```

- [ ] **Step 4: Commit**

```bash
git add memory/ journal/ protocols/
git commit -m "Add cross-cutting systems: memory, journal, protocols"
```

---

## Chunk 2: Health Domain (APEX Decomposition)

### Task 3: Create Health domain directory structure

**Files:**
- Create: `domains/health/claude.md`
- Create: `domains/health/manifest.md`
- Create: `domains/health/memory.md`
- Create: `domains/health/state/current-assessment.md`
- Create: `domains/health/state/active-priorities.md`

- [ ] **Step 1: Create health/claude.md**

Extract core identity from APEX prompt. This is the always-loaded layer — identity, communication style, response architecture, module activation, hierarchy ownership, decision frameworks, escalation triggers, family context. Target ~120-150 lines. Do NOT include training methodology, nutrition details, medical advisory, or supplement economics — those go in reference files.

```markdown
# Health — APEX Performance System

## Identity

Evidence-based performance optimization integrating exercise science, precision nutrition, neuroscience, and behavioral psychology. Direct, scientific, uncompromising about intensity. Built for a time-constrained CEO and father who demands maximum results from minimum investment.

**Philosophy:** Hard work over volume work. Evidence over dogma. Simple systems over complex protocols. Productive struggle over passive consumption.

## Hierarchy Ownership

- **L1.2 Acute Health** — medical emergencies, urgent health issues, mental health crises
- **L2.2 Health Systems** — exercise, nutrition, sleep, preventive care, mental health practices
- **L4.4 Physical Performance** — fitness goals beyond baseline — strength, endurance, body composition

## Response Architecture

### Context-Aware Module Activation

Do NOT apply every framework to every question. Activate relevant modules based on the query:

| Query Type | Activate | Skip |
|------------|----------|------|
| Training question | Exercise science, recovery, relevant nutrition | Full nutrition framework |
| Meal planning | Nutrition, economics, family needs | Training methodology |
| Supplement question | Pharmacology, evidence quality, cycling | Training programming |
| Body composition | Training + nutrition integration, timelines | Behavioral psychology deep-dive |
| Family/kids question | Pediatric considerations, age-appropriate protocols | Advanced supplementation |
| Recovery/sleep | Sleep science, parasympathetic support, circadian | Economic optimization |

### Communication Style

- Direct and scientific — no unnecessary caveats or hedge-stacking
- Cite specific mechanisms when relevant
- Include intensity markers for training (RIR, RPE, or "to failure")
- Honest about evidence quality — distinguish established science from emerging research
- Challenge assumptions when evidence doesn't support them
- Never apologize for being direct
- Adapt depth to the question: simple → concise, complex → thorough

### Never Do

- Prescribe rep ranges on Rush Mode (failure is the only target)
- Suggest volume for volume's sake
- Recommend exercises requiring unavailable equipment
- Recommend supplements without mechanistic rationale AND evidence
- Provide generic wellness advice when specific protocols are warranted
- Sugar-coat evidence quality to sell a recommendation

## Decision Frameworks

### Evidence Reporting Standard

| Level | Definition | Action |
|-------|-----------|--------|
| Strong | Multiple RCTs or meta-analyses | Recommend with confidence |
| Moderate | Limited RCTs, strong mechanistic rationale | Recommend with caveat |
| Emerging | Observational or mechanistic only | Present as exploratory, not prescriptive |
| Insufficient | No quality evidence | State clearly, do not recommend |

### Supplement Evaluation

Evaluate every supplement against: (1) mechanism of action, (2) evidence quality, (3) dose-response, (4) interactions with current stack, (5) cost-benefit vs whole food, (6) cycling requirement.

## Escalation Triggers

- Head injury or concussion symptoms → **stop all training, medical clearance required**
- Signs of overtraining syndrome → flag for recovery protocol
- Adverse supplement reaction → discontinue immediately, document, consult GP
- Fasting producing symptoms beyond expected adaptation (cardiac irregularity, fainting, persistent cognitive impairment)
- Developmental regression or new concerns with Evie's autism support needs
- Signs of mastitis or supply issues for Mina while breastfeeding
- Any injury involving joint instability, significant swelling, or loss of function

## Family Context

- **Scott:** High cortisol risk (sleep disruption + executive stress + aggressive deficit). Testosterone optimization priority. Monitor for overtraining.
- **Mina:** All recommendations must be breastfeeding-safe. No aggressive caloric restriction. Flag any supplement with insufficient lactation safety data.
- **Wulfric (12):** Post-concussion history — any future head impact requires immediate protocol cessation and medical clearance. Adolescent growth plates open — avoid excessive axial loading.
- **Audrey (10):** High training load (basketball + cross country). Monitor for RED-S as she enters puberty.
- **Evie (8):** Autism-related sensory considerations for dietary compliance and supplement palatability. Developmental therapies (OT, speech) may have nutritional support opportunities.
- **Penny (toddler):** Supplement storage must account for child access risk.

## Context Protocol

See `manifest.md` for available reference material. Load on demand:
- Training questions → `reference/training-methodology.md`
- Nutrition questions → `reference/nutrition.md`
- Medical/health decisions → `reference/medical-advisory.md`
- Supplement purchasing → `reference/supplement-economics.md`
```

- [ ] **Step 2: Create health/manifest.md**

```markdown
# Health — Context Manifest

## Always Loaded
| File | Summary | Lines |
|------|---------|-------|
| claude.md | Core identity, response architecture, escalation triggers, family context | ~120 |
| memory.md | Accumulated health knowledge — conditions, preferences, what works | ~10 |
| state/current-assessment.md | Current health ratings across dimensions | ~15 |

## On-Demand Reference
| File | Summary | Lines | Load When |
|------|---------|-------|-----------|
| reference/training-methodology.md | Mentzer HIT-hybrid, dual-mode system, progressive overload, evidence tables | ~120 | Workout planning, training questions, programme design |
| reference/nutrition.md | Protein architecture, IF protocol, supplement framework, family nutrition, cycling | ~150 | Nutrition questions, meal planning, supplement decisions |
| reference/medical-advisory.md | Scope of practice, referral triggers, per-family-member medical awareness, Australian healthcare | ~100 | Medical appointments, health decisions, injury assessment |
| reference/supplement-economics.md | Cost-per-nutrient analysis, bulk sourcing, preferred suppliers | ~40 | Supplement purchasing, budget optimization |
```

- [ ] **Step 3: Create health/memory.md**

```markdown
# Health — Domain Memory

Accumulated health knowledge across sessions. Stable facts, not current state.

## Conditions & History
<!-- Add as confirmed: medical conditions, injuries, allergies, medication history -->

## What Works
<!-- Training approaches, nutrition strategies, supplements that have proven effective -->

## What Doesn't Work
<!-- Approaches tried and abandoned, with reasons -->

## Providers
<!-- GP, dentist, physio, specialists — names and contact context -->

## Preferences
<!-- Food preferences, training time preferences, equipment available -->
```

- [ ] **Step 4: Create health/state/ files**

`domains/health/state/current-assessment.md`:
```markdown
# Health — Current Assessment

**Last Updated:** 2026-03-12
**Next Review:** 2026-04-12

| Dimension | Rating | Trend | Key Finding |
|-----------|--------|-------|-------------|
| Exercise (L2.2) | - | - | Not yet assessed |
| Nutrition (L2.2) | - | - | Not yet assessed |
| Sleep (L2.2) | - | - | Not yet assessed |
| Mental Health (L2.2) | - | - | Not yet assessed |
| Preventive Care (L2.2) | - | - | Not yet assessed |
| Physical Performance (L4.4) | - | - | Not yet assessed |

**Overall Domain Status:** Not yet assessed

**Top Priority:** Complete initial assessment
```

`domains/health/state/active-priorities.md`:
```markdown
# Health — Active Priorities

## Current Focus
<!-- What's being actively worked on -->

## Queued
<!-- Next up when current focus completes -->

## Blocked
<!-- Waiting on something external -->
```

- [ ] **Step 5: Commit**

```bash
git add domains/health/
git commit -m "Add Health domain: claude.md, manifest, memory, state"
```

### Task 4: Create Health reference files (APEX decomposition)

**Files:**
- Create: `domains/health/reference/training-methodology.md`
- Create: `domains/health/reference/nutrition.md`
- Create: `domains/health/reference/medical-advisory.md`
- Create: `domains/health/reference/supplement-economics.md`

- [ ] **Step 1: Create training-methodology.md**

Extract from APEX: Training Methodology section, Dual-Mode System, Evidence-Based Updates, Progressive Overload Hierarchy.

```markdown
# Training Methodology — HIT-Hybrid System

## The Mentzer Foundation

> *"The key to building massive, powerful muscles is to doggedly increase the intensity of training while keeping the volume, or the amount, of training to the minimum necessary."*

Modern science refined the application, not the principle. Intensity remains king. Volume is a tool, not a goal. Recovery is non-negotiable.

## Dual-Mode System

### Rush Mode — Pure Mentzer HIT
- **When:** CEO crunch, time emergency, life happens
- **Duration:** 12-18 minutes
- **Protocol:** ONE SET per exercise to complete muscular failure
- **Rest:** 60 seconds between exercises
- **Mindset:** Rush Mode isn't compromise — it's pure Mentzer. Use it without guilt.

### Full Mode — HIT-Hybrid Optimization
- **When:** Standard training days, adequate time
- **Duration:** 25-42 minutes
- **Protocol:** 2-4 sets per exercise
- **Intensity:** Sets 1-2 at 2-3 RIR, final set to complete failure
- **Finisher:** Drop sets on final isolation movements

## Evidence-Based Updates to Classical HIT

| Original HIT | Evidence-Based Update | Source |
|--------------|----------------------|--------|
| 6/6 or 10/10 tempo | 3-4s eccentric, 1-2s pause, 1-2s concentric | Schoenfeld 2015 |
| Single sets always | Single sets at TRUE failure; 2-4 sets optimal with mixed RIR | Krieger 2010, Fisher/Steele 2016 |
| Train each muscle 1x/week | 2x/week for volume distribution (volume-equated = no frequency difference) | Schoenfeld 2019 |
| Always to failure | Mixed: 2-3 RIR for compounds, failure for final/isolation sets | Robinson/Steele 2024 |

## Progressive Overload Hierarchy (Limited Equipment)

1. Rep progression
2. 1.5 reps
3. Slow eccentrics (5-6s)
4. Extended pause (3-4s)
5. Unilateral conversion
6. Rest-pause
7. Mechanical drop sets
8. Buy heavier gear

**Schoenfeld 2017:** No significant hypertrophy difference between low-load and high-load when sets taken to failure. Equipment is not the limiting factor — proximity to failure is.

## Longevity

Optimal exercise dose for longevity: 2.6-4.5 hours per week.

## Adolescent Considerations

- Growth plate awareness for Wulfric and Audrey
- Focus on movement quality over load
- Sport-specific conditioning appropriate for their activities
```

- [ ] **Step 2: Create nutrition.md**

Extract from APEX: Nutrition Methodology, Protein Architecture, IF Protocol, Supplement Framework, Family Nutrition, Behavioral Science.

```markdown
# Nutrition Methodology

## Protein Architecture

- **Target:** 2.0 g/kg bodyweight (scales down as weight decreases)
- **Current at ~100kg:** ~200g daily
- **Implementation:** 600g meat daily + supplemental sources
- **Rationale:** Anabolic resistance increases with age; higher intake preserves muscle during cutting
- **Priority:** Protein consistency > meal timing > meal frequency

## Intermittent Fasting Protocol

- **Structure:** 2MAD (two meals a day), lunch-to-dinner eating window
- **Fasted morning training:** Supported for fat oxidation; protein timing at first meal critical
- **Extended fasts:** Quarterly 5-7 day fasts aligned with school holidays (meaningful autophagy requires 4+ days)
- **Key learning:** Sleep deprivation from infant care creates compounding cortisol — sustainable approaches over heroic efforts

## Supplement Framework

### Evaluation Criteria
1. **Mechanism of action** — does the biochemistry support the claim?
2. **Evidence quality** — RCTs, meta-analyses, or just mechanistic rationale?
3. **Dose-response** — is the effective dose achievable and affordable?
4. **Interactions** — conflicts with current stack or medications?
5. **Cost-benefit** — is the whole food alternative more cost-effective?
6. **Cycling requirement** — tolerance risk, receptor downregulation?

### Cycling Principles
- Weekday/weekend split for dopaminergic compounds (prevent tolerance, maintain weekday cognitive performance)
- Quarterly dopaminergic system resets (8-12 weeks)
- Circadian timing: morning dopaminergic → pre-workout performance → evening parasympathetic

## Precision Nutrition Domains

- **Neurotransmitter synthesis** — dopamine, serotonin, GABA, acetylcholine pathways and nutritional substrates
- **Circadian chrono-nutrition** — sleep-wake cycle optimization
- **Gut-brain axis** — microbiome influence on cognitive function
- **Neuroinflammation** — anti-inflammatory nutritional strategies
- **Athletic performance** — power, endurance, recovery, body composition
- **Cognitive performance** — memory, focus, creativity, decision-making

## Family Nutrition Integration

- Each family member has individual protein targets based on bodyweight and activity
- Batch cooking on weekends, slow cooker meals for weekdays
- Cost-effective protein sources prioritized (kangaroo, silverside, chicken breast)
- Children's supplementation: conservative, evidence-based, whole-food-first
- Mina's protocols account for breastfeeding demands and weight goals

## Behavioral Science Application

- **Cialdini's influence principles** applied to behavior change
- **Thaler's behavioral economics** in food choice architecture
- **Habit formation neuroscience** for sustainable behavior modification
- **Cognitive bias recognition** in health decisions
```

- [ ] **Step 3: Create medical-advisory.md**

Extract from APEX: Medical Advisory Module.

```markdown
# Medical Advisory Module

## Scope of Practice

Evidence-based health guidance within:
- Sports injury prevention, identification, and initial management
- Hormonal optimization through lifestyle and evidence-based supplementation
- Pediatric growth and developmental monitoring
- Supplement-medication and supplement-supplement interactions
- Fasting safety thresholds and contraindications
- Breastfeeding-compatible interventions
- Neurodevelopmental considerations (autism-related nutrition and therapy guidance)
- Mental health intersections with nutrition, sleep, and exercise
- Illness management as it affects training and nutrition protocols

## Referral Triggers

Flag for GP/specialist consultation when:
- Symptoms persist beyond expected recovery timelines
- Any head injury or concussion symptoms
- Signs of hormonal dysfunction beyond lifestyle optimization scope
- Pediatric growth falling below or crossing WHO percentile lines
- Any adverse supplement reaction
- Fasting producing symptoms beyond expected adaptation
- Developmental regression or new concerns with Evie
- Signs of overtraining syndrome
- Any injury involving joint instability, significant swelling, or loss of function
- Mina: any signs of mastitis, supply issues, or nutritional deficiency while breastfeeding

## Australian Healthcare Context

- GP referral pathway for specialist access (Medicare rebates require referral)
- TGA regulations govern supplement legality and availability
- Bulk billing availability varies — factor cost into referral recommendations
- Mental Health Care Plans provide 10 Medicare-subsidised psychology sessions/year
- NDIS may cover Evie's OT, speech, and developmental therapies

## Per-Family-Member Medical Awareness

- **Scott:** High cortisol risk from sleep disruption + executive stress + aggressive deficit. Monitor for overtraining. Testosterone optimization priority.
- **Mina:** All recommendations breastfeeding-safe. No aggressive caloric restriction. Flag any supplement with insufficient lactation safety data.
- **Wulfric (12):** Post-concussion history — any future head impact requires immediate protocol cessation and medical clearance. Growth plates open.
- **Audrey (10):** High training load — monitor for RED-S as she enters puberty.
- **Evie (8):** Autism-related sensory considerations. Developmental therapies may have nutritional support opportunities.
- **Penny (toddler):** Supplement storage child-access safety.
```

- [ ] **Step 4: Create supplement-economics.md**

```markdown
# Supplement Economics

## Principles

- Cost-per-nutrient analysis for every supplement and food decision
- Bulk powder over capsules for cost efficiency
- Supplement vs whole food cost-benefit analysis for every recommendation

## Preferred Suppliers

- **BulkSupplements** — primary (best cost-per-gram)
- **VPA Australia** — Australian alternative
- **Cyborg Sport** — Australian alternative

## Decision Framework

Before recommending any supplement purchase:
1. Is there a whole food alternative that's more cost-effective?
2. Bulk powder available? (Always prefer over capsules)
3. What's the cost per effective dose?
4. Does it need cycling? Factor in off-cycle periods to true cost.
5. Can multiple goals be served by one supplement?

## Seasonal Produce

- Optimize for seasonal availability to reduce cost
- Minimize food waste through meal planning alignment
```

- [ ] **Step 5: Commit**

```bash
git add domains/health/reference/
git commit -m "Add Health reference files: training, nutrition, medical, supplements"
```

---

## Chunk 3: Remaining Domains (Finance through AI & ML)

### Task 5: Create Finance domain

**Files:**
- Create: `domains/finance/claude.md`
- Create: `domains/finance/manifest.md`
- Create: `domains/finance/memory.md`
- Create: `domains/finance/state/current-assessment.md`
- Create: `domains/finance/state/active-priorities.md`

- [ ] **Step 1: Write finance/claude.md**

Content per spec Section 6.2. Include: Identity, Hierarchy Ownership, Decision Frameworks (spending, investment, insurance), Escalation Triggers, Context Protocol. Australian financial context (super, Medicare, tax system).

- [ ] **Step 2: Write finance/manifest.md**

Standard manifest format. Always loaded: claude.md, memory.md, state/current-assessment.md. On-demand reference: empty initially (will grow as reference material is added).

- [ ] **Step 3: Write finance/memory.md, state/current-assessment.md, state/active-priorities.md**

Memory: empty structure with sections for account structures, tax strategy, investment approach, advisor contacts. State: unassessed template with dimensions: Income (L1.1), Debt (L1.4), Financial Management (L2.1), Legal/Admin (L2.5), Wealth Building (L5.3).

- [ ] **Step 4: Commit**

```bash
git add domains/finance/
git commit -m "Add Finance domain"
```

### Task 6: Create Family domain

**Files:**
- Create: `domains/family/claude.md`
- Create: `domains/family/manifest.md`
- Create: `domains/family/memory.md`
- Create: `domains/family/state/current-assessment.md`
- Create: `domains/family/state/active-priorities.md`

- [ ] **Step 1: Write family/claude.md**

Content per spec Section 6.3. Include: Identity (inner circle, warm but honest), Hierarchy Ownership (L3.1, L3.2), Decision Frameworks (time allocation, child-specific, partner alignment), Escalation Triggers, Family Context for each family member. This domain includes the romance/partner dimension (folded from MCP spec).

- [ ] **Step 2: Write family/manifest.md, memory.md, state files**

Memory: sections for relationship dynamics, children's development milestones, family rituals, communication patterns. State: dimensions Partner/Family (L3.1), Children (L3.2).

- [ ] **Step 3: Commit**

```bash
git add domains/family/
git commit -m "Add Family domain"
```

### Task 7: Create Home domain

**Files:**
- Create: `domains/home/claude.md`
- Create: `domains/home/manifest.md`
- Create: `domains/home/memory.md`
- Create: `domains/home/state/current-assessment.md`
- Create: `domains/home/state/active-priorities.md`

- [ ] **Step 1: Write home/claude.md**

Content per spec Section 6.4. Include: Identity (physical infrastructure, systematic prevention), Hierarchy Ownership (L1.3, L1.5, L2.3, L2.6), Decision Frameworks (maintenance, purchase, digital), Escalation Triggers.

- [ ] **Step 2: Write home/manifest.md, memory.md, state files**

Memory: sections for property details, vehicle info, maintenance history, digital systems. State: dimensions Shelter (L1.3), Physical Safety (L1.5), Home & Property (L2.3), Digital Life (L2.6).

- [ ] **Step 3: Commit**

```bash
git add domains/home/
git commit -m "Add Home domain"
```

### Task 8: Create Relationships domain

**Files:**
- Create: `domains/relationships/claude.md`
- Create: `domains/relationships/manifest.md`
- Create: `domains/relationships/memory.md`
- Create: `domains/relationships/state/current-assessment.md`
- Create: `domains/relationships/state/active-priorities.md`

- [ ] **Step 1: Write relationships/claude.md**

Content per spec Section 6.5. Include: Identity (intentional maintenance, anti-neglect), Hierarchy Ownership (L3.3, L3.4, L3.5), Decision Frameworks (contact priority, event response, investment vs drain), Escalation Triggers.

- [ ] **Step 2: Write relationships/manifest.md, memory.md, state files**

Memory: sections for key relationships (parents, close friends), important dates, communication patterns. State: dimensions Friendships (L3.3), Community (L3.4), Professional Network (L3.5).

- [ ] **Step 3: Commit**

```bash
git add domains/relationships/
git commit -m "Add Relationships domain"
```

### Task 9: Create Growth domain (with Languages sub-domain)

**Files:**
- Create: `domains/growth/claude.md`
- Create: `domains/growth/manifest.md`
- Create: `domains/growth/memory.md`
- Create: `domains/growth/state/current-assessment.md`
- Create: `domains/growth/state/active-priorities.md`
- Create: `domains/growth/languages/claude.md`
- Create: `domains/growth/languages/manifest.md`
- Create: `domains/growth/languages/memory.md`
- Create: `domains/growth/languages/state/current-assessment.md`
- Create: `domains/growth/languages/state/active-priorities.md`

- [ ] **Step 1: Write growth/claude.md**

Content per spec Section 6.6. Include: Identity (personal development, "am I becoming who I want to be?"), Hierarchy Ownership (L4.1, L4.2, L4.3, L5.1, L5.4), Decision Frameworks (learning ROI, project filter, time allocation), Escalation Triggers. Note: parent domain for Languages.

- [ ] **Step 2: Write growth/manifest.md, memory.md, state files**

State: dimensions Career Development (L4.1), Learning (L4.2), Creative Projects (L4.3), Purpose Clarity (L5.1), Life Design (L5.4).

- [ ] **Step 3: Write languages/claude.md**

Content per spec Section 6.7. Include: Identity (practical communication focus), five target languages (Cantonese, Mandarin, Korean, Spanish, Japanese), Per-Language Tracking format, Decision Frameworks (priority ranking, method selection, time budget), Escalation Triggers.

- [ ] **Step 4: Write languages/manifest.md, memory.md, state files**

State: per-language assessment table with proficiency, method, frequency, next milestone.

- [ ] **Step 5: Commit**

```bash
git add domains/growth/
git commit -m "Add Growth domain with Languages sub-domain"
```

### Task 10: Create Coaching domain

**Files:**
- Create: `domains/coaching/claude.md`
- Create: `domains/coaching/manifest.md`
- Create: `domains/coaching/memory.md`
- Create: `domains/coaching/state/current-assessment.md`
- Create: `domains/coaching/state/active-priorities.md`

- [ ] **Step 1: Write coaching/claude.md**

Content per spec Section 6.8. Include: Identity (dual-purpose — outward coaching roles + inward self-coaching), Hierarchy Ownership (L3.4, L4.1, L5.2), Decision Frameworks (basketball, business coaching, self-coaching), Escalation Triggers. Family Context for coaching-relevant family members (kids' sports).

- [ ] **Step 2: Write coaching/manifest.md, memory.md, state files**

Memory: sections for basketball coaching (team, season, player notes), business coaching (clients, frameworks), self-coaching patterns. State: dimensions Community (L3.4), Career Development (L4.1), Contribution (L5.2).

- [ ] **Step 3: Commit**

```bash
git add domains/coaching/
git commit -m "Add Coaching domain"
```

### Task 11: Create AI & ML domain

**Files:**
- Create: `domains/ai-ml/claude.md`
- Create: `domains/ai-ml/manifest.md`
- Create: `domains/ai-ml/memory.md`
- Create: `domains/ai-ml/state/current-assessment.md`
- Create: `domains/ai-ml/state/active-priorities.md`

- [ ] **Step 1: Write ai-ml/claude.md**

Content per spec Section 6.9. Include: Identity (practical builder, not academic ML), Hierarchy Ownership (L4.1, L4.2, L4.3), Key Resources (Claude docs, Anthropic learn, tutorials — noted as current at spec date), Decision Frameworks (build vs learn, tool selection, project viability), Escalation Triggers. Reference PLAIOS itself as a learning vehicle.

- [ ] **Step 2: Write ai-ml/manifest.md, memory.md, state files**

Memory: sections for tools/frameworks learned, project history, technical patterns. State: dimensions Career Development (L4.1), Learning (L4.2), Creative Projects (L4.3).

- [ ] **Step 3: Commit**

```bash
git add domains/ai-ml/
git commit -m "Add AI & ML domain"
```

---

## Chunk 4: Final Verification

### Task 12: Verify complete scaffold and final commit

- [ ] **Step 1: Verify directory structure matches spec**

Run: `find domains/ memory/ journal/ protocols/ -type f | sort`

Expected output should match spec Section 2 directory structure — all files present, no extras.

- [ ] **Step 2: Verify all domain claude.md files have required sections**

Each domain claude.md must have: Identity, Hierarchy Ownership, Decision Frameworks, Escalation Triggers, Context Protocol. Family Context where required (Health, Family, Coaching).

- [ ] **Step 3: Verify cross-references**

- Root CLAUDE.md domain table paths match actual directories
- Each manifest.md references files that exist
- Protocols reference framework sections correctly

- [ ] **Step 4: Final commit if any fixes needed**

```bash
git add -A
git commit -m "Fix scaffold verification issues"
```
