# AI Household CFO — Architecture Research

**Date:** 2026-04-06
**Context:** Research for building an AI-powered personal finance advisor using Claude as the reasoning engine, Firefly III as the data layer, and PLAIOS Finance domain frameworks as the operating logic.

---

## 1. Structuring Household Financial Data for LLM Reasoning

### The Core Problem

Claude reasons well over text and structured data, but poorly over raw transaction dumps. 500 transactions at ~30 tokens each = 15,000 tokens of noise. The key insight from research: **Claude needs pre-computed summaries for reasoning, with raw data available on-demand for drill-down.**

### Recommended Three-Layer Data Architecture

```
Layer 1: RAW TRANSACTIONS (stored in Firefly III)
├── Every transaction, full detail
├── Never sent to Claude in bulk
├── Queried via API for specific lookups
└── Source of truth

Layer 2: MONTHLY AGGREGATES (pre-computed, stored as markdown/JSON)
├── Income by source (salary, dividends, other)
├── Spending by category (housing, transport, discretionary, etc.)
├── Savings rate
├── Net cash flow
├── Guardrail status (% of income per category)
├── Notable transactions (>$500 or flagged)
└── ~200-400 tokens per month = 12 months fits in ~4,000 tokens

Layer 3: ROLLING SNAPSHOT (the "briefing document")
├── Current month actuals vs budget
├── 3-month trend summary
├── Net worth position (quarterly)
├── Active alerts/breaches
├── Upcoming known expenses
└── ~500-800 tokens total
```

### Why This Works

- **Layer 3** is always loaded — gives Claude enough context to answer 80% of questions
- **Layer 2** is loaded on-demand — monthly summaries for trend analysis, 12 months at ~4,000 tokens is efficient
- **Layer 1** is queried selectively — "show me all dining transactions in March" fetches via API, not pre-loaded

### Data Format

**Markdown tables for summaries** — Claude processes these with near-perfect accuracy. Clean, human-readable, low token overhead.

```markdown
## March 2026 Summary
| Category | Budget | Actual | % Income | Guardrail | Status |
|----------|--------|--------|----------|-----------|--------|
| Housing | $4,200 | $4,180 | 28% | <=30% | OK |
| Transport | $800 | $920 | 6% | <=10% | OK |
| Discretionary | $2,000 | $2,450 | 16% | <=15% | BREACH |
| Children | $1,500 | $1,380 | 9% | - | OK |
| Savings | $2,500 | $2,070 | 14% | >=10% | OK |

Income: $15,000 | Expenses: $12,930 | Savings rate: 13.8%
Notable: School camp $680, Car service $450
```

**JSON for machine processing** — when the data layer computes aggregates, store as JSON for programmatic access and convert to markdown for Claude.

### Granularity Guidance

| Question Type | Data Needed | Granularity |
|---|---|---|
| "Are we on track this month?" | Layer 3 snapshot | Current month summary |
| "Can we afford X?" | Layer 3 + income/obligations | Snapshot + upcoming commitments |
| "Where did we overspend last quarter?" | Layer 2, 3 months | Monthly aggregates by category |
| "What's our savings rate trend?" | Layer 2, 6-12 months | Monthly savings rate series |
| "Show me all Uber Eats spending" | Layer 1 (API query) | Raw transactions, filtered |
| "What if income drops 20%?" | Layer 2 averages + Layer 3 | Aggregated baseline + scenario model |

---

## 2. Proactive Monitoring Architecture

### How It Works

A scheduled task runs Claude against pre-computed financial data on a fixed cadence, checking against the PLAIOS Finance domain guardrails and escalation triggers.

### Implementation Using Claude Code Scheduled Tasks

Claude Code supports desktop scheduled tasks via `/schedule` — they run locally, have full access to files, MCP servers, and tools, and fire on a cron expression. This is the correct mechanism.

### Recommended Cadence

| Check | Frequency | What It Does |
|---|---|---|
| **Weekly pulse** | Sunday evening | Pull current week's transactions from Firefly III API, compute category totals for the month-to-date, compare against guardrails, flag breaches |
| **Monthly review prep** | 1st of month | Compute full prior month aggregates, update Layer 2 summary, compare against all guardrails and escalation triggers, generate review briefing |
| **Quarterly snapshot** | 1st of quarter | Net worth update, savings rate trend, goal progress check, generate quarterly state update |

### What the "Check" Looks Like

The scheduled task would:

1. **Query Firefly III API** for transactions since last check
2. **Run a local script** (Python or TypeScript) that computes:
   - Category totals for current month
   - Running savings rate
   - Guardrail percentages
   - Comparison against previous month
3. **Pass the computed summary to Claude** with the Finance domain context, asking it to:
   - Evaluate against PLAIOS escalation triggers
   - Identify patterns (not just threshold breaches)
   - Generate alerts if needed
   - Update the Layer 3 rolling snapshot
4. **Write output** to PLAIOS state files and optionally notify

### Alert Classification

Map directly to PLAIOS escalation triggers:

| Alert Level | Trigger | Example |
|---|---|---|
| **Critical** | L1-L2 dimension rated 1 | Income loss, savings rate below 5% for 2 months |
| **Warning** | Guardrail breach (single month) | Discretionary at 18% (guardrail: 15%) |
| **Pattern** | Multi-month trend | Discretionary rising 3 months running |
| **Info** | Noteworthy but not actionable | Large one-off expense, income increase |

### Practical Implementation

```
Scheduled task (weekly):
  1. Python script queries Firefly III API
  2. Computes aggregates → writes to temp file
  3. Claude Code reads temp file + Finance domain state
  4. Claude evaluates, generates alert if needed
  5. Updates domains/finance/state/current-assessment.md
  6. Writes alert to domains/finance/state/active-priorities.md if warranted
```

The Python script is essential — it does the computation, not Claude. Claude does the interpretation and judgment. This keeps costs low (small context per run) and reliable (deterministic math).

---

## 3. Scenario Modelling Data Structure

### What Claude Needs to Run Projections

Claude does not need a spreadsheet engine. It needs a **baseline financial model** as structured data, plus the ability to modify variables and reason about the consequences.

### The Household Financial Model

Store as a YAML or JSON file that Claude can read and reason over:

```yaml
# domains/finance/state/financial-model.yaml
model_date: 2026-04-01
period: monthly

income:
  scott_salary: 12000
  scott_dividends: 3000  # quarterly, averaged monthly
  mina_income: 0
  other: 0
  total_gross: 15000

fixed_obligations:
  mortgage: 3200
  insurance_home: 180
  insurance_health: 350
  insurance_life: 120
  school_fees: 0
  childcare: 800
  utilities: 450
  subscriptions: 200
  loan_repayments: 0
  super_contributions: 500
  total: 5800

variable_essentials:
  groceries: 1200
  transport: 600
  medical: 200
  clothing_kids: 150
  home_maintenance: 200
  total: 2350

discretionary:
  dining: 400
  entertainment: 300
  personal_scott: 500
  personal_mina: 500
  hobbies: 200
  total: 1900

savings_investment:
  offset_account: 2000
  investment: 500
  total: 2500

# Derived
total_expenses: 12550
surplus_deficit: 2450
savings_rate_pct: 16.3

# Assets and liabilities (quarterly update)
assets:
  ppor_value: 1200000
  super_scott: 350000
  super_mina: 120000
  investments: 45000
  savings_offset: 85000
  business_equity: 500000  # conservative
  total: 2300000

liabilities:
  mortgage_balance: 620000
  mortgage_rate: 5.89
  mortgage_type: variable
  hecs: 15000
  business_guarantees: 200000
  total: 835000

net_worth: 1465000
```

### Scenario Queries Claude Can Handle

With this model loaded (~300 tokens), Claude can directly compute:

- **"What if Mina goes part-time at $3,000/month?"** — Add to income, recalculate savings rate, check guardrails
- **"What if we fix the mortgage at 5.5%?"** — Adjust mortgage payment, compare variable vs fixed cost, break-even analysis
- **"What if income drops 20%?"** — Reduce income, identify which categories get cut, how long emergency fund lasts
- **"What if we add private school at $15k/year?"** — Add to fixed obligations, impact on savings rate, what needs to change
- **"When can we afford to renovate ($80k)?"** — Project savings trajectory at current rate, when target is reached

### How Scenario Modelling Works in Practice

```
User: "Can we afford to put Wulfric in private school next year?"

Claude loads:
  1. Financial model (baseline) — ~300 tokens
  2. Layer 3 snapshot (current actuals) — ~500 tokens
  3. Finance domain claude.md (frameworks) — already loaded
  
Claude reasons:
  1. Private school cost: ~$15,000/year = $1,250/month added to fixed obligations
  2. Current surplus: $2,450/month
  3. New surplus: $1,200/month
  4. New savings rate: 8% (down from 16.3%)
  5. Still above 5% critical threshold but below 10% "healthy" floor
  6. Impact on emergency fund build rate
  7. Flags: this pushes savings into "minimum viable" range
  8. Suggests: what would Mina earning $X change?
```

### The Google Sheets Forecast Connection

The existing household financial forecast in Google Sheets is the current source of truth. The model file above is a Claude-readable extract of it. The workflow:

1. Maintain the Google Sheet as the "official" model (human-editable, shareable with Mina)
2. Periodically export key parameters to the YAML model file (could be automated)
3. Claude reads the YAML for scenario work
4. If a scenario is approved, update the Google Sheet

This avoids building a competing spreadsheet inside PLAIOS.

---

## 4. Existing Open-Source Projects

### Directly Relevant

| Project | What It Does | Relevance |
|---|---|---|
| **Firefly III MCP Servers** ([horsfallnathan](https://github.com/horsfallnathan/firefly-iii-mcp-server), [etnperlong](https://github.com/etnperlong/firefly-iii-mcp), [fabianonetto](https://github.com/fabianonetto/mcp-server-firefly-iii), [RadCod3/LamPyrid](https://github.com/RadCod3/LamPyrid)) | MCP servers that let Claude query Firefly III via natural language | **High** — multiple implementations exist, fabianonetto's has 100% API coverage (66 tools). This is the bridge between data layer and intelligence layer |
| **Personal-Finance-Agent** ([Kirushikesh](https://github.com/Kirushikesh/Personal-Finance-Agent)) | LLM agent that translates natural language to SQL queries over transaction data | **Medium** — demonstrates the NL-to-query pattern, but Firefly III MCP servers do this better |
| **expense-manager** ([pablovazquezg](https://github.com/pablovazquezg/expense-manager)) | LLM-powered transaction consolidation and categorization | **Medium** — good reference for how to prompt LLMs for categorization |
| **Local LLMs for Finance** ([thu-vu92](https://github.com/thu-vu92/local-llms-analyse-finance), [darshan106](https://github.com/darshan106/Personal-Finance-Dashboard)) | Local Llama2 for transaction categorization | **Low** — privacy-focused but less capable than Claude API |
| **Anthropic Financial Services Plugins** ([anthropics](https://github.com/anthropics/financial-services-plugins)) | Official Anthropic plugins for financial analysis (DCF, comps, etc.) | **Low** — aimed at institutional finance, not household. But demonstrates Claude's financial reasoning patterns |

### Key Takeaway

The Firefly III MCP server ecosystem is the most important finding. Multiple implementations already exist that bridge Firefly III's data to Claude. Rather than building a custom data access layer from scratch, one of these MCP servers provides the read/write interface, and the AI CFO logic is built as a PLAIOS layer on top.

---

## 5. Data Layer vs Intelligence Layer Boundary

### Principle: Compute Deterministically, Reason with AI

| Responsibility | Layer | Why |
|---|---|---|
| Store transactions | Data (Firefly III) | Structured storage, API access, rule-based categorization |
| Categorize transactions | Data (Firefly III rules) + AI (edge cases) | Rules handle 80%+; Claude handles ambiguous ones on review |
| Compute aggregates | Data (Python script) | Deterministic math must be deterministic — don't ask Claude to sum 500 transactions |
| Check guardrail thresholds | Data (Python script) | Simple comparison: is 18% > 15%? Don't waste AI tokens on arithmetic |
| Interpret patterns | Intelligence (Claude) | "Discretionary spending up 3 months running — is this lifestyle creep or seasonal?" |
| Generate alerts | Intelligence (Claude) | Context-aware judgment: "This breach coincides with school holidays — likely one-off" |
| Run scenarios | Intelligence (Claude) | "If income drops 20%, here's the cascade of consequences" |
| Advise on decisions | Intelligence (Claude) | "Given your priorities and current position, here's my recommendation" |
| Maintain the financial model | Human (Google Sheets) | Both partners own this; AI proposes changes, doesn't make them |

### Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│                    HUMAN LAYER                   │
│  Google Sheets forecast (source of truth)        │
│  Monthly money meeting                           │
│  Decision authority                              │
└───────────────────────┬─────────────────────────┘
                        │ parameters
                        ▼
┌─────────────────────────────────────────────────┐
│              INTELLIGENCE LAYER (Claude)          │
│                                                   │
│  PLAIOS Finance Domain Context                    │
│  ├── claude.md (identity, frameworks, guardrails)│
│  ├── state/current-assessment.md                 │
│  ├── state/financial-model.yaml                  │
│  └── reference/ (on-demand)                      │
│                                                   │
│  Three Modes:                                     │
│  1. Reactive — answer questions via conversation  │
│  2. Proactive — scheduled checks write alerts     │
│  3. Strategic — scenario modelling on demand      │
│                                                   │
└───────────────┬──────────────────┬──────────────┘
                │ queries          │ reads/writes
                ▼                  ▼
┌──────────────────────┐  ┌──────────────────────┐
│    DATA LAYER        │  │   PLAIOS STATE       │
│                      │  │                      │
│  Firefly III         │  │  financial-model.yaml│
│  ├── Transactions    │  │  current-assessment  │
│  ├── Accounts        │  │  active-priorities   │
│  ├── Categories      │  │  monthly-summaries/  │
│  ├── Budgets         │  │  alerts/             │
│  └── Rules           │  │                      │
│                      │  │                      │
│  Accessed via:       │  │  Accessed via:       │
│  MCP Server (query)  │  │  Filesystem (direct) │
│  Python scripts      │  │                      │
│  (compute)           │  │                      │
└──────────────────────┘  └──────────────────────┘
```

---

## 6. Context Budget Per Query Type

### Token Budget Analysis

Claude Opus 4.6 has a 1M token context window, but cost and latency scale with input size. The goal is **minimum viable context** per query type.

| Query Type | Always Loaded | On-Demand | Total Estimate |
|---|---|---|---|
| **Quick check** ("savings rate?") | Finance claude.md (~1,500t) + Layer 3 snapshot (~500t) | None | ~2,000 tokens |
| **Monthly review** | Finance claude.md + snapshot | Layer 2 current + prior month (~800t) | ~2,800 tokens |
| **Trend analysis** | Finance claude.md + snapshot | Layer 2, 6-12 months (~3,000t) | ~5,000 tokens |
| **Scenario modelling** | Finance claude.md + snapshot | Financial model YAML (~300t) | ~2,300 tokens |
| **Complex scenario** | Finance claude.md + snapshot | Model + 12-month history + reference docs | ~8,000 tokens |
| **Transaction drill-down** | Finance claude.md + snapshot | Specific transactions via API (~varies) | ~3,000-5,000 tokens |

### Key Principle

**Never send full transaction history.** 12 months of transactions at ~500/month = 6,000 transactions = ~180,000 tokens. Wasteful, slow, expensive, and Claude's accuracy degrades with noise. Pre-computed summaries are both cheaper AND more effective.

### What NOT to Send

- Raw transaction lists for aggregate questions (pre-compute the aggregate)
- Full reference docs when only one section applies (use manifest-based loading)
- Historical data beyond what the question needs (default to 3 months, expand on request)
- Account numbers, BSBs, or other identifying financial details (not needed for reasoning)

---

## 7. Privacy Considerations

### Threat Model

PLAIOS runs locally, and Claude API calls are covered by Anthropic's data usage policy (no training on API data). The primary risk is not breach — it's sending more than necessary.

### Data Classification

| Data Type | Sensitivity | Send to Claude? | Notes |
|---|---|---|---|
| Category totals ("Groceries: $1,200") | Low | Yes | No PII, needed for reasoning |
| Savings rate, net worth | Medium | Yes | Needed for financial advice |
| Merchant names ("Woolworths, Uber Eats") | Low | On drill-down only | Not needed for summary analysis |
| Account balances | Medium | Yes (aggregated) | Don't send account numbers |
| Account numbers, BSBs | High | Never | Not needed for any reasoning |
| Income amounts | Medium | Yes | Needed for ratio calculations |
| Employer/business names | Medium | Minimize | Use "primary employment" not company name |
| Specific addresses | High | Never | Not needed |
| Tax file numbers | Critical | Never | Not needed |
| Insurance policy numbers | High | Never | Not needed |

### Minimum Data for Each Mode

**Reactive advisor:** Category summaries + financial model + question context. No raw transactions unless specifically drilling down, and even then, merchant name + amount + date is sufficient (no account numbers).

**Proactive monitor:** Pre-computed guardrail status (percentages, not raw data). Claude sees "Discretionary: 18% (guardrail: 15%) - BREACH" not the underlying transactions.

**Strategic planner:** Financial model YAML (income, expenses, assets, liabilities as numbers). No identifying details needed — Claude reasons over the math, not the identity.

### Implementation

The Python compute layer is the privacy boundary. It:
1. Queries Firefly III (local, no external API)
2. Computes aggregates (deterministic, no AI)
3. Strips identifying details
4. Passes summaries to Claude

This means raw transaction data never leaves the local machine. Only pre-computed summaries and the financial model reach Claude's API.

---

## 8. Recommended Build Sequence

### Phase 1: Data Foundation (Week 1-2)

**Goal:** Firefly III running, bank data flowing, basic categorization working.

1. Deploy Firefly III + Data Importer via Docker (already researched — see `tooling-research-personal-finance-apps.md`)
2. Configure CBA and ANZ CSV import using community configurations
3. Import 3-6 months of transaction history
4. Build initial categorization rules (housing, transport, groceries, discretionary, children, etc.)
5. Map categories to PLAIOS Finance domain guardrails

**Output:** Categorized transaction database accessible via API.

### Phase 2: Compute Layer (Week 2-3)

**Goal:** Python scripts that turn raw transactions into Claude-ready summaries.

1. Write a Python script that:
   - Queries Firefly III API for transactions in a date range
   - Computes monthly aggregates by category
   - Calculates savings rate, guardrail percentages
   - Flags notable transactions (>$500 or category anomalies)
   - Outputs Layer 2 summary as markdown
   - Outputs Layer 3 snapshot as markdown
2. Create the financial model YAML from Google Sheets data
3. Store computed summaries in `domains/finance/state/monthly-summaries/`

**Output:** Monthly summary files and a rolling snapshot, updated by script.

### Phase 3: Reactive Advisor (Week 3-4)

**Goal:** Claude can answer financial questions with real data.

1. Install a Firefly III MCP server (evaluate fabianonetto's 100% coverage vs simpler options)
2. Integrate with PLAIOS — Claude Code sessions in the Finance domain now have:
   - Finance domain context (frameworks, guardrails, escalation triggers)
   - Layer 3 snapshot (current position)
   - MCP access to Firefly III (transaction drill-down)
   - Financial model YAML (scenario inputs)
3. Test with real queries: "Can we afford X?", "What's our savings rate this month?"

**Output:** Working conversational finance advisor.

### Phase 4: Proactive Monitor (Week 4-5)

**Goal:** Scheduled checks that flag issues before they're asked about.

1. Create a Claude Code scheduled task (weekly) that:
   - Runs the compute script to update summaries
   - Passes summary to Claude with Finance domain context
   - Claude evaluates against escalation triggers
   - Writes findings to `state/current-assessment.md`
   - Creates alerts in `state/active-priorities.md` if warranted
2. Create a monthly scheduled task that generates a full review briefing
3. Test: manually create guardrail breaches and verify alerts fire

**Output:** Self-updating financial health assessment.

### Phase 5: Strategic Planner (Week 5-6)

**Goal:** Claude can model "what if" scenarios against real data.

1. Refine the financial model YAML with actual data from Google Sheets
2. Build a small library of scenario templates (income change, expense addition, mortgage change, etc.)
3. Test scenario modelling accuracy against manual spreadsheet calculations
4. Create a monthly money meeting prep document that Claude generates automatically

**Output:** Scenario modelling capability and automated meeting prep.

### Phase 6: Refinement (Ongoing)

- Tune categorization rules as new merchant patterns emerge
- Refine guardrail thresholds based on actual household data
- Add Ghostfolio for investment/super tracking if needed
- Explore browser automation for CSV download (reduce weekly friction)
- Consider Claude Desktop integration via MCP when system is stable

---

## 9. Technology Stack Summary

| Component | Technology | Purpose |
|---|---|---|
| Transaction storage | Firefly III (Docker) | Store and categorize all financial transactions |
| Data import | Firefly III Data Importer | CSV import from CBA/ANZ |
| API bridge | Firefly III MCP Server | Let Claude query transaction data via natural language |
| Compute layer | Python scripts | Aggregate transactions, compute guardrails, build summaries |
| Intelligence | Claude (via Claude Code / API) | Interpret, advise, alert, model scenarios |
| Financial model | YAML file in PLAIOS | Claude-readable baseline for scenario modelling |
| Forecasting | Google Sheets (existing) | Human-owned, shareable, source of truth for the model |
| Scheduling | Claude Code scheduled tasks | Weekly/monthly automated checks |
| State management | PLAIOS Finance domain files | Assessments, priorities, summaries, alerts |
| Investment tracking | Ghostfolio (optional, Docker) | Portfolio performance, super balances |

---

## 10. What This Does NOT Require

- No custom web application
- No database beyond Firefly III's built-in PostgreSQL
- No separate AI server or inference infrastructure
- No paid third-party API for bank data (CSV manual import)
- No custom LLM fine-tuning
- No mobile app development (Claude Mobile + PLAIOS handles this)
- No complex ML pipeline — Claude's general reasoning is sufficient for household finance

The entire system is: Firefly III (Docker) + Python scripts + Claude Code + PLAIOS files. One technical person, one machine, off-the-shelf components.

---

## Sources

- [Firefly III MCP Server (horsfallnathan)](https://github.com/horsfallnathan/firefly-iii-mcp-server)
- [Firefly III MCP Server (etnperlong)](https://github.com/etnperlong/firefly-iii-mcp)
- [Firefly III MCP Server (fabianonetto) — 100% API coverage](https://github.com/fabianonetto/mcp-server-firefly-iii)
- [LamPyrid MCP Server](https://github.com/RadCod3/LamPyrid)
- [Firefly III API Documentation](https://api-docs.firefly-iii.org/)
- [Firefly III CBA Import Config](https://github.com/firefly-iii/import-configurations/tree/main/au/commonwealth-bank)
- [Firefly III ANZ Import Config](https://github.com/firefly-iii/import-configurations/blob/main/au/anz/default.json)
- [Claude Code Scheduled Tasks Documentation](https://code.claude.com/docs/en/scheduled-tasks)
- [Claude for Financial Services](https://www.anthropic.com/news/claude-for-financial-services)
- [Anthropic Financial Services Plugins](https://github.com/anthropics/financial-services-plugins)
- [Build Financial Models with Claude](https://claude.com/resources/use-cases/build-financial-models)
- [Personal Finance Agent (Kirushikesh)](https://github.com/Kirushikesh/Personal-Finance-Agent)
- [Expense Manager (pablovazquezg)](https://github.com/pablovazquezg/expense-manager)
- [Local LLMs for Finance (thu-vu92)](https://github.com/thu-vu92/local-llms-analyse-finance)
- [Build a Private AI Finance Analyzer With LLMs](https://dzone.com/articles/local-llm-finance-tracker)
- [Token-Efficient Data Prep for LLM Workloads](https://thenewstack.io/a-guide-to-token-efficient-data-prep-for-llm-workloads/)
- [Ghostfolio](https://github.com/ghostfolio/ghostfolio)
