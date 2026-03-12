# PLAIOS — Personal Life AI Operating System

## Design Specification

**Date:** 2026-03-12
**Status:** Draft (v2 — post spec review)
**Author:** smckennie + Claude

---

## 1. Problem Statement

A busy professional needs a unified system to track and manage all life domains — relationships, family, romance, fitness, mental wellbeing, and professional foundations. The core pain point is having no single view of "how am I doing across my life," leading to dropped balls on important relationships, events, and personal health.

Existing tools (calendars, contacts, fitness apps) are fragmented. Claude Desktop prompts exist for individual domains but are ephemeral and disconnected. PLAIOS consolidates these into one coherent, persistent system.

## 2. Design Principles

- **Cybernetic feedback loops** — signals feed into status, status triggers actions, actions change signals. But the model respects human complexity: not everything reduces to a number.
- **Blended quantitative/qualitative** — fitness gets hard metrics, relationships get softer signals, the system surfaces patterns across both.
- **Separation of concerns** — each life domain is its own agent with its own data, context, and reasoning.
- **Context engineering** — follows Anthropic's principles: compaction, structured note-taking, tool result clearing, just-in-time retrieval, sub-agent context isolation.
- **No monolithic vector store** — structured data and explicit relationships over embedding-based retrieval. Avoids semantic collapse at scale.
- **No separate server** — the user's development machine hosts everything.

## 3. Architecture Overview

```
Claude Code (build, develop, deep queries, admin)
Claude Desktop (conversational, visual artifacts, dashboards)
Claude Mobile (data collection → shared cloud folder → ingested on PC wake)
        ↕ (Code & Desktop via local MCP)
PLAIOS MCP Server (local, on user's machine)
├── Orchestrator (LLM-powered, routes and reasons)
├── Domain Agents (MCP tool groups per domain)
├── Connectors (deterministic code — Outlook, Google APIs)
├── Vault Agent (Obsidian file operations)
└── Workers (Windows Scheduled Tasks — sync, compaction)
        ↕
Obsidian Vault (D:\Obsidian — local data backbone)
Outlook (primary calendar + reminders)
Google Calendar/Contacts (secondary, read-only)
```

### 3.1 Client Access

| Client | Role | Connection |
|--------|------|------------|
| **Claude Code** | Development, admin, deep queries, system evolution | Local MCP |
| **Claude Desktop** | Conversational interaction, visual artifacts/dashboards, migrated prompts | Local MCP |
| **Claude Mobile** | On-the-go data collection and quick notes | Cloud intermediary (see 3.3) |

### 3.2 No Hosted Server

The user's development machine runs the MCP server locally. Windows Scheduled Tasks handle background sync and context enrichment between sessions.

### 3.3 Mobile Sync Strategy

Claude Mobile cannot connect to the local MCP server. Instead:

1. **Data collection on mobile**: User logs notes, reflections, or quick data via Claude Mobile. Claude saves these as structured entries to a shared cloud location (e.g., a OneDrive folder or shared Obsidian sync folder).
2. **Ingestion on PC wake**: The `plaios-sync-mobile` scheduled task scans the shared cloud folder, parses entries, and routes them to the appropriate domain agent for processing.
3. **Format**: Mobile entries follow a simple convention: `YYYY-MM-DD-HH-MM-<domain>.md` with YAML frontmatter specifying domain and signal type.

This keeps the PC as the sole runtime while enabling mobile data collection.

## 4. Agent Hierarchy & Runtime Model

### 4.1 Terminology

The system uses three distinct component types:

- **Agents** (LLM-powered): The Orchestrator and Domain Agents. These make Claude API calls with domain-specific system prompts to reason about data. Invoked on demand, not persistent processes.
- **Connectors** (deterministic code): Integration components for Outlook, Google Calendar, Google Contacts. These are standard API client code — no LLM calls. Exposed as MCP tools.
- **Workers** (scheduled tasks): Background scripts triggered by Windows Task Scheduler. Deterministic code that syncs data, computes status, and runs compaction.

### 4.2 Agent Hierarchy

```
PLAIOS Orchestrator (LLM agent — routes queries, cross-domain reasoning)
├── Domain Agents (LLM agents — one per life domain)
│   ├── Relationships Agent (family, friends)
│   ├── Romance Agent
│   ├── Fitness Agent
│   ├── Professional Agent
│   └── Wellbeing Agent
├── Connectors (deterministic code — exposed as MCP tools)
│   ├── Outlook Connector (read + write — primary calendar)
│   ├── Google Calendar Connector (read-only)
│   ├── Google Contacts Connector (read-only)
│   └── Vault Connector (Obsidian file read/write)
└── Workers (Windows Scheduled Tasks)
    ├── plaios-sync-outlook
    ├── plaios-sync-contacts
    ├── plaios-sync-mobile
    ├── plaios-compact-history
    └── plaios-status-update
```

Note: Calendar & Events is not a separate domain agent. Calendar intelligence is handled by the Orchestrator aggregating outputs from the Outlook and Google Calendar connectors. This avoids a redundant agent layer for what is essentially a view over integration data.

### 4.3 Agent Runtime Model

- **Orchestrator**: An LLM call (Claude API) with a system prompt that includes the hot-tier index. Receives a user query, decides which domain agents and/or connectors to invoke, aggregates results, and responds. Triggered by user interaction via MCP tools.
- **Domain Agents**: Each is an LLM call with a domain-specific system prompt and access to that domain's warm-tier data. Invoked by the Orchestrator via tool use, not as persistent processes. Return a compacted summary (target: <1000 tokens) to the Orchestrator.
- **Connectors**: TypeScript/Python functions exposed as MCP tools. No LLM calls. Called by the Orchestrator or domain agents to read/write external services. Also called by workers during scheduled sync.
- **Inter-agent communication**: All communication flows through MCP tool calls. The Orchestrator calls domain agent tools; domain agents call connector tools. No direct agent-to-agent messaging.

### 4.4 Agent Responsibilities

| Component | Type | Responsibility | Reads From | Writes To |
|-----------|------|---------------|------------|-----------|
| **Orchestrator** | LLM agent | Cross-domain reasoning, routing queries, pattern detection | Hot index, domain agent summaries | Alerts, cross-domain insights |
| **Domain Agents** (x5) | LLM agent | Own their domain's signals, status reasoning, action suggestions | Obsidian vault (domain folder), connector outputs | Domain status, Obsidian notes |
| **Connectors** (x4) | Deterministic | Fetch/push to external services and Obsidian | Outlook, Google, Obsidian vault | Normalised data |
| **Workers** (x5) | Deterministic | Background sync, status computation, compaction | Connectors, vault files | Vault files, hot index |

### 4.5 Communication Rules

- Orchestrator never queries external services directly — always through connectors.
- Domain agents never talk to each other directly — cross-domain patterns are the orchestrator's job.
- Connectors return normalised, compacted data — never raw API responses.
- All agents return the smallest high-signal summary to their parent (context engineering principle).

## 5. Life Domains & Data Model

### 5.1 Domain Definitions

| Domain | Metric Type | Example Signals |
|--------|------------|-----------------|
| **Relationships** (family, friends) | Blended | Days since last contact, upcoming birthdays, neglect alerts |
| **Romance** | Mostly qualitative | Date nights planned, partner milestones, relationship rituals |
| **Fitness & Health** | Mostly quantitative | Workout frequency, sleep, streaks, body metrics |
| **Professional Foundation** | Blended | Key deadlines met, work-life balance signals, burnout indicators |
| **Mental Wellbeing** | Qualitative | Self-assessed mood, stress level, journaling frequency |

### 5.2 Domain State

Each domain has:
- **Status**: computed state — `thriving` / `maintaining` / `attention-needed` / `neglected`
- **Signals**: raw inputs from external services and manual logging
- **Thresholds**: configurable rules for status transitions
- **Actions**: suggested next steps when a domain needs attention

### 5.3 Status Computation Model

Status computation is **hybrid: deterministic rules with LLM escalation**.

**Layer 1 — Deterministic rules (workers):** The `plaios-status-update` worker evaluates `thresholds.yaml` rules against current signals. These are simple, fast, and free:

```yaml
# Example: relationships/thresholds.yaml
schema_version: 1
rules:
  - signal: days_since_last_contact
    target: "each person where priority >= high"
    thresholds:
      maintaining: 7
      attention-needed: 14
      neglected: 30
  - signal: upcoming_birthday
    target: "each person"
    thresholds:
      attention-needed: 7  # days until birthday, no gift/plan logged
```

```yaml
# Example: fitness/thresholds.yaml
schema_version: 1
rules:
  - signal: workouts_per_week
    target: "aggregate"
    thresholds:
      thriving: 4
      maintaining: 2
      attention-needed: 1
      neglected: 0
  - signal: days_since_last_workout
    target: "aggregate"
    thresholds:
      attention-needed: 5
      neglected: 10
```

**Layer 2 — LLM escalation (domain agents):** When signals are ambiguous, conflicting, or qualitative (e.g., wellbeing domain), the worker flags the domain for LLM review. The domain agent is invoked to assess nuanced status. This happens sparingly — only when rules can't resolve.

**Conflict resolution:** When multiple rules disagree, the most severe status wins. Manual overrides always take precedence.

### 5.4 Cybernetic Feedback Loop

Signals → Status computation (rules + optional LLM) → Action suggestions → User takes action → New signals

The system acknowledges unpredictable inputs by allowing manual overrides and qualitative notes that shift domain status independent of metrics.

## 6. Memory & State Architecture

### 6.1 Three Tiers

| Tier | What | Where | When Loaded |
|------|------|-------|-------------|
| **Hot** | Current domain statuses, active alerts, today's priorities | `D:\Obsidian\PLAIOS\index.yaml` | Every session start |
| **Warm** | Domain histories, relationship profiles, fitness logs, event archives | Obsidian vault (structured markdown + frontmatter) | On demand, when a domain is queried |
| **Cold** | Raw calendar data, email contacts, fitness API data | External services (Outlook, Google) | Fetched via connectors, extracted, raw discarded |

### 6.2 Hot Index Schema

```yaml
# D:\Obsidian\PLAIOS\index.yaml
schema_version: 1
last_updated: "2026-03-12T08:00:00Z"
domains:
  relationships:
    status: attention-needed
    top_alert: "No contact with Mum in 16 days"
    last_computed: "2026-03-12T06:30:00Z"
  romance:
    status: maintaining
    top_alert: "Anniversary in 5 days — no plan logged"
    last_computed: "2026-03-12T06:30:00Z"
  fitness:
    status: thriving
    top_alert: null
    last_computed: "2026-03-12T06:30:00Z"
  professional:
    status: maintaining
    top_alert: "Q1 review next week"
    last_computed: "2026-03-12T06:30:00Z"
  wellbeing:
    status: attention-needed
    top_alert: "No journal entry in 8 days"
    last_computed: "2026-03-12T06:30:00Z"
today:
  events:
    - "10:00 — Team standup (Outlook)"
    - "14:00 — Dentist (Google Calendar)"
  priorities:
    - "Call Mum"
    - "Plan anniversary dinner"
  alerts:
    - domain: relationships
      message: "Dad's birthday in 3 days"
      severity: attention-needed
```

### 6.3 Vault Directory Layout

```
D:\Obsidian\PLAIOS\
├── index.yaml                    (hot tier — loaded every session)
├── relationships\
│   ├── status.yaml
│   ├── thresholds.yaml
│   ├── people\
│   │   ├── mum.md
│   │   ├── dad.md
│   │   └── ...
│   ├── signals\
│   │   └── 2026-03-12-contact-mum.md
│   └── history\
│       └── 2026-03-summary.md
├── romance\
│   ├── status.yaml
│   ├── thresholds.yaml
│   ├── signals\
│   └── history\
├── fitness\
│   ├── status.yaml
│   ├── thresholds.yaml
│   ├── signals\
│   └── history\
├── professional\
│   ├── status.yaml
│   ├── thresholds.yaml
│   ├── signals\
│   └── history\
├── wellbeing\
│   ├── status.yaml
│   ├── thresholds.yaml
│   ├── signals\
│   └── history\
└── mobile-inbox\                  (mobile sync landing zone)
    └── 2026-03-12-14-30-fitness.md
```

### 6.4 Context Engineering Application

- **Compaction**: Domain agents summarise history; only high-signal state surfaces to orchestrator.
- **Structured note-taking**: Persistent files per domain in Obsidian, not conversation memory.
- **Tool result clearing**: Connectors extract and discard raw API responses.
- **Just-in-time retrieval**: Orchestrator holds lightweight pointers (hot index), loads domain detail on demand.
- **Sub-agent context isolation**: Each domain agent gets a clean context window.

## 7. Integration Layer

| Service | Direction | Purpose | Component |
|---------|-----------|---------|-----------|
| **Outlook** | Read + Write | Primary calendar. Reads events/deadlines, writes reminders. | Outlook Connector |
| **Google Calendar** | Read only | Secondary calendar. Pull events, no writes. | Google Calendar Connector |
| **Google Contacts** | Read only | Relationship metadata — birthdays, contact details. | Google Contacts Connector |
| **Obsidian** | Read + Write | Local data backbone — domain notes, journal, signals, status. | Vault Connector |
| **Mobile Cloud Folder** | Read only | Ingest mobile-collected entries on PC wake. | `plaios-sync-mobile` worker |

### 7.1 Credential Management

- OAuth tokens for Microsoft Graph (Outlook) and Google APIs stored in **Windows Credential Manager** — never in plain text, never in the Obsidian vault.
- Token refresh handled by connectors automatically.
- Connector code reads credentials from Credential Manager at runtime.

## 8. Windows Scheduled Tasks (Workers)

| Task | Purpose | Frequency | Depends On |
|------|---------|-----------|------------|
| `plaios-sync-outlook` | Refresh upcoming events and deadlines from Outlook | On PC wake / every 30 min | Outlook Connector |
| `plaios-sync-contacts` | Update relationship data from Google Contacts | Daily | Google Contacts Connector |
| `plaios-sync-mobile` | Ingest entries from shared cloud folder into domain signals | On PC wake / every 15 min | Cloud folder access |
| `plaios-compact-history` | Summarise recent chat transcripts into domain-relevant context | Daily | LLM call (budgeted) |
| `plaios-status-update` | Recompute domain statuses via threshold rules | After sync tasks complete | All sync workers |

### 8.1 Worker Resilience

- **Idempotency**: All workers are idempotent — safe to re-run without side effects. Processed files are moved to `processed/` subfolder.
- **Failure handling**: Workers log failures to `D:\Obsidian\PLAIOS\logs\`. Failed runs do not corrupt state — partial writes use temp files with atomic rename.
- **File locking**: Workers use file-level locks when writing to Obsidian vault files to prevent conflicts with manual edits.
- **Retry**: Failed sync tasks retry on next scheduled run. No retry loops within a single run.

## 9. Error Handling & Resilience

- **Outlook/Google API unreachable**: Connectors return stale data from last successful sync (cached in vault). Hot index shows `last_computed` timestamp so the user knows freshness.
- **Obsidian write conflicts**: Vault connector uses atomic writes (write to temp file, rename). If a conflict is detected (file modified since last read), the write is aborted and logged.
- **LLM output validation**: Domain agent responses are validated against expected schema before writing to vault. Malformed responses are logged and the previous status is retained.
- **Degraded mode**: If all external services are down, PLAIOS still functions using cached vault data. Status may be stale but the system remains queryable.

## 10. Privacy Considerations

- Romance domain data is excluded from the hot-tier `top_alert` field by default. Requires explicit query to surface (prevents accidental exposure during screen shares).
- All data stays local — no cloud storage except the mobile sync folder, which contains only the user's own entries.
- Chat history compaction uses LLM calls — be aware that conversation content is sent to Claude API during compaction.

## 11. V1 Scope

The first iteration delivers the full feedback loop in a scrappy form:

1. **Awareness** — see all life domains at a glance, each with a status, ask "what needs attention?"
2. **Calendar intelligence** — knows important dates/events, proactively reminds via Outlook
3. **Tracking** — log workouts, relationship touchpoints, reflections; track trends over time
4. **Queryable via Claude Code** — "How's my week looking?", "What have I neglected?", "When did I last talk to Dad?"

## 12. Tech Stack

- **MCP server**: TypeScript (best MCP SDK support, Obsidian ecosystem is JS-native)
- **Connectors**: TypeScript — Microsoft Graph API (Outlook), Google Calendar/Contacts API
- **Workers**: TypeScript scripts invoked by Windows Task Scheduler via Node.js
- **Obsidian interaction**: Direct file system read/write (markdown + YAML frontmatter)
- **Credential storage**: Windows Credential Manager
- **Schema versioning**: All YAML files include `schema_version` field from day one

## 13. Out of Scope (V1)

- Web dashboard
- Fitness API integrations (future)
- AI-generated insights beyond domain status (future)
- Multi-user support
- End-to-end encryption of vault data
- Automated testing suite (will be added incrementally)
