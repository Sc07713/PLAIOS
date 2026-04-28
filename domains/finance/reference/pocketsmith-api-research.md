# PocketSmith API Research — Bank Feed Aggregator Layer Evaluation

**Date:** 2026-04-06
**Context:** Evaluating PocketSmith as a "bank feed aggregator" data layer, where PocketSmith handles automated bank connections and we pull data out via API for an AI-powered financial analysis system (Claude as intelligence layer).

---

## Executive Summary

PocketSmith is a strong candidate for the data layer. It solves the core Australian bank connectivity problem (CBA + ANZ automated feeds) that made self-hosted tools impractical. The API is REST, free on all plans, well-documented with OpenAPI 3 spec, and covers transactions, accounts, categories, budgets, and forecasts. An official first-party MCP server exists with 57 tools and OAuth authentication. The main trade-off: you're paying $10-17 AUD/month for what is essentially a bank feed proxy, but the alternative (building your own CDR data recipient) costs $250K+ in accreditation.

**Verdict: PocketSmith as data layer + Claude as intelligence layer is the right architecture for this household.**

---

## 1. PocketSmith API — Detailed Capabilities

### Architecture

- **Type:** REST API
- **Base URL:** `https://api.pocketsmith.com/v2`
- **Specification:** OpenAPI 3.0 (published on GitHub: [pocketsmith/api](https://github.com/pocketsmith/api))
- **Response format:** JSON
- **Status:** Actively maintained, stable v2 API

### Authentication

Two methods available:

| Method | Use Case | Details |
|--------|----------|---------|
| **Developer Key** | Personal tools (our use case) | Generate under Settings > Security. Pass in `X-Developer-Key` header. Persistent access to your own account |
| **OAuth 2.0** | Multi-user applications | Register app via api@pocketsmith.com, receive client_id/client_secret. Standard OAuth flow |

The official MCP server uses **OAuth 2.0 with PKCE** — tokens are encrypted and stateless, nothing stored on the MCP server. Revocable via PocketSmith's authorized applications page.

### API Endpoints (Complete Listing)

**Users (3 endpoints)**
- `GET /me` — Authenticated user details
- `GET /users/{id}` — Specific user
- `PUT /users/{id}` — Update profile (name, timezone, currency)

**Institutions (5 endpoints)**
- `GET /institutions/{id}` — Institution details
- `PUT /institutions/{id}` — Update institution
- `DELETE /institutions/{id}` — Remove institution (with optional merge)
- `GET /users/{id}/institutions` — List user's institutions
- `POST /users/{id}/institutions` — Create institution

**Accounts (7 endpoints)**
- `GET /accounts/{id}` — Account details
- `PUT /accounts/{id}` — Update account
- `DELETE /accounts/{id}` — Remove account
- `GET /users/{id}/accounts` — List all user accounts
- `PUT /users/{id}/accounts` — Reorder accounts
- `POST /users/{id}/accounts` — Create account
- `GET /institutions/{id}/accounts` — List accounts within institution

**Transaction Accounts (3 endpoints)**
- `GET /transaction-accounts/{id}` — Transaction account details
- `PUT /transaction-accounts/{id}` — Update
- `GET /users/{id}/transaction-accounts` — List all transaction accounts

**Transactions (8 endpoints) — THE KEY RESOURCE**
- `GET /transactions/{id}` — Single transaction
- `PUT /transactions/{id}` — Update transaction (category, notes, labels, etc.)
- `DELETE /transactions/{id}` — Remove transaction
- `GET /users/{id}/transactions` — List all user transactions (with filters)
- `GET /accounts/{id}/transactions` — List by account
- `GET /categories/{id}/transactions` — List by category
- `GET /transaction-accounts/{id}/transactions` — List by transaction account
- `POST /transaction-accounts/{id}/transactions` — Create transaction

**Transaction Query Parameters (critical for our use case):**
- `start_date` — Return transactions on or after this date
- `end_date` — Return transactions on or before this date
- `updated_since` — ISO 8601 timestamp, return only transactions updated since then (enables incremental sync)
- `type` — Filter by "debit" or "credit"
- `search` — Keyword search across amount, account name, payee, category, note, labels
- `uncategorised` — Boolean, filter uncategorised transactions
- `needs_review` — Filter transactions flagged for review
- `page` — Pagination

**Categories (4 endpoints)**
- `GET /categories/{id}` — Category details
- `PUT /categories/{id}` — Update category
- `DELETE /categories/{id}` — Remove category
- `GET /users/{id}/categories` — List all categories
- `POST /users/{id}/categories` — Create category

**Category Rules (2 endpoints)**
- `GET /users/{id}/category-rules` — List auto-categorisation rules
- `POST /categories/{id}/category-rules` — Create categorisation rule

**Budgets & Analysis (4 endpoints)**
- `GET /users/{id}/budget` — Budget data
- `GET /users/{id}/budget-summary` — Budget overview
- `GET /users/{id}/trend-analysis` — Spending trends across categories
- `DELETE /users/{id}/forecast-cache` — Clear forecast cache

**Events / Scenarios (5 endpoints)**
- `GET /events/{id}` — Recurring transaction event
- `PUT /events/{id}` — Update event
- `DELETE /events/{id}` — Remove event
- `GET /users/{id}/events` — List all events
- `GET /scenarios/{id}/events` — List scenario events
- `POST /scenarios/{id}/events` — Create event in scenario

**Attachments (7 endpoints)**
- Full CRUD on attachments, plus attach/detach from transactions

**Labels & Saved Searches (2 endpoints)**
- `GET /users/{id}/labels` — List all labels
- `GET /users/{id}/saved-searches` — List saved searches

**Reference Data (3 endpoints)**
- `GET /currencies` — All supported currencies
- `GET /currencies/{id}` — Specific currency
- `GET /time-zones` — Available timezones

**Total: ~44 endpoints** covering the full PocketSmith data model.

### What You CAN Do Via API

- Pull all transactions with date range filtering and incremental sync (`updated_since`)
- Read account balances and details
- Read and create categories and auto-categorisation rules
- Read budget data and trend analysis
- Update transactions (add notes, labels, change category)
- Create manual transactions
- Read recurring events (scheduled/expected transactions)
- Search transactions by keyword
- Read forecast/projection data (via budget endpoints)
- Upload and manage attachments

### What You CANNOT Do Via API

- Trigger a bank feed refresh (feeds refresh on PocketSmith's schedule)
- Access the forecast projection engine directly (forecasts are computed server-side)
- Webhooks — no webhook support. Must poll for changes (but `updated_since` makes polling efficient)
- Bulk operations — no batch create/update endpoints

---

## 2. API Access by Plan Tier

### Key Finding: API Access is FREE on ALL Plans

From the official documentation: *"The API is available for anyone to use without restriction and free of charge."*

This means even the free tier includes API access. The plan tier determines bank feed limits and other features, not API access.

### Current Pricing (AUD, as of April 2026)

| Plan | Monthly | Annually (per month) | Bank Feeds | Key Features |
|------|---------|---------------------|------------|--------------|
| **Free** | $0 | $0 | Automatic feeds + manual import | 2 accounts, 2 dashboards, 12 budgets, 6-month projection |
| **Foundation** | $14.95 | $9.99 | 6 connected banks (1 country) | Unlimited accounts/budgets, 6 dashboards, 10-year projection |
| **Flourish** | $24.95 | $16.66 | 18 connected banks | Unlimited accounts/budgets, 18 dashboards, 30-year projection |
| **Fortune** | $39.95 | $26.66 | Unlimited connected banks | Unlimited everything, 60-year projection, priority support |

### Recommendation for Our Use Case

**Foundation at $9.99/month (annual)** is sufficient if CBA + ANZ = 2 bank feed connections. However, "connected banks" may count individual feed connections (e.g., CBA savings + CBA credit card + ANZ savings = 3 connections, not 2 banks). If you have more than 6 account connections across CBA and ANZ, **Flourish at $16.66/month** is the safe choice.

The free tier includes automatic bank feeds but is limited to 2 accounts — not enough for a household with multiple CBA + ANZ accounts.

---

## 3. Rate Limits and Data Completeness

### Rate Limits

PocketSmith's API documentation **does not publish explicit rate limits**. The developer docs make no mention of request quotas, throttling, or rate limit headers. This is unusual but consistent across all their documentation.

The community MCP server by dannyshaw implements rate limiting, retry with exponential backoff, and circuit breaker patterns as a defensive measure, suggesting the API may have undocumented limits.

**Practical implication:** For our use case (weekly/daily batch pulls, not high-frequency trading), rate limits are unlikely to be a concern. Even pulling a full month of transactions is a handful of paginated requests.

### Pagination

- **Default page size:** 30 records
- **Minimum:** 10 records per page
- **Maximum:** 1,000 records per page
- **Navigation:** `page` and `per_page` query parameters
- **Headers:** `Per-Page`, `Total`, `Link` (RFC 5988 compliant with first/last/next/prev)

At 1,000 records per page, a household's monthly transactions (~200-500) fit in a single request.

### Data Completeness

**Can you get ALL transaction data via API?** Yes. The API exposes the same transaction data that PocketSmith's UI shows. Every transaction has: id, date, amount, payee, original_payee, category, memo, note, labels, type (debit/credit), status (pending/posted), closing_balance, upload_source, cheque_number, is_transfer, needs_review, created_at, updated_at, and the associated transaction account.

**Transaction history limits are at the FEED level, not the API level:**

| Feed Provider | Initial History |
|---------------|----------------|
| Yodlee (global) | 1 year or more, sometimes only 90 days |
| Basiq (AU CDR) | Up to 2 years (per CDR legislation) |
| Salt Edge (UK/EU) | Up to 1 year |
| Akahu (NZ) | Up to 1 year, occasionally 90 days |
| Plaid (US/CA) | Up to 2 years |

**Once transactions are in PocketSmith, they are retained indefinitely and accessible via API.** The history limit only applies to the initial feed connection — ongoing transactions accumulate over time. After 3 years of use, you'd have 3 years of data regardless of the initial import window.

### Incremental Sync

The `updated_since` parameter on transaction endpoints enables efficient polling:
```
GET /users/{id}/transactions?updated_since=2026-04-05T00:00:00Z
```
This returns only transactions created or modified since that timestamp — ideal for the compute layer pulling daily/weekly deltas rather than full dumps.

---

## 4. MCP Servers and LLM Integrations

### Official PocketSmith MCP Server (First-Party)

PocketSmith launched an official MCP server on 1 April 2026.

| Detail | Value |
|--------|-------|
| **Full access URL** | `https://mcp.pocketsmith.com/mcp` |
| **Read-only URL** | `https://mcp-readonly.pocketsmith.com/mcp` |
| **Total tools (full)** | 57 |
| **Total tools (read-only)** | 38 |
| **Authentication** | OAuth 2.0 with PKCE (prompts on first use) |
| **Hosting** | Cloud-hosted by PocketSmith (no local server needed) |

**Setup with Claude Code:**
```bash
# Full access (read + write)
claude mcp add pocketsmith --transport http https://mcp.pocketsmith.com/mcp

# Read-only
claude mcp add pocketsmith-readonly --transport http https://mcp-readonly.pocketsmith.com/mcp
```

**Tool categories in the official MCP server:**

- **Insights (compound analysis):** Financial health snapshots, month-end reviews, spending comparisons, recurring expense detection, cash flow forecasting, net worth trajectory analysis, forecast accuracy evaluation
- **Budget analysis:** Per-category budget vs actual, trend analysis
- **Transaction management:** Full CRUD, search, categorisation
- **Account/institution handling:** List, read, manage
- **Category hierarchies:** Read, create, manage rules
- **Budget events:** Create and manage recurring/scheduled events
- **Attachments:** Upload, manage, link to transactions
- **Data feeds:** Synchronisation operations
- **User profile:** Read and update
- **Reference data:** Currencies, timezones

**Plan requirements:** Not explicitly stated, but API access is free on all plans. The MCP server uses the same API, so presumably works on any plan.

### Community MCP Servers

| Server | Author | Tools | Notes |
|--------|--------|-------|-------|
| [dannyshaw/pocketsmith-mcp](https://github.com/dannyshaw/pocketsmith-mcp) | Danny Shaw | 23 | Production-ready, rate limiting, retry with exponential backoff, circuit breaker. 45% API coverage focusing on most useful endpoints |
| [joho/pocketsmith-mcp](https://github.com/joho/pocketsmith-mcp) | John Barton | Unknown | Budget management focused |
| [ajanderson1/mcp_pocketsmith](https://github.com/ajanderson1/mcp_pocketsmith) | AJ Anderson | Unknown | Community implementation |

### Verdict on MCP

The official first-party MCP server with 57 tools is the clear winner. It's cloud-hosted (no local server to maintain), uses OAuth (no API key management), and has insight tools that go beyond raw API endpoints. This eliminates the need to build our own MCP server, unlike the Firefly III approach which required evaluating 4+ community options.

---

## 5. Data Export Capabilities

### Export Formats

| Format | Available From | Notes |
|--------|---------------|-------|
| **CSV** | Transactions page, Settings > Export data | Full transaction export with all fields |
| **XLSX (Excel)** | Transactions page | Same data as CSV in spreadsheet format |
| **JSON** | API only (not UI export) | All API responses are JSON |

### Export Methods

1. **Transactions page export:** Hover over Export > choose XLSX or CSV. Can export all transactions or filtered subsets (create a search first, then export results)
2. **Full backup:** Settings > User preferences > Export data > "Download a CSV" — exports ALL transactions as a complete backup
3. **API export:** All API endpoints return JSON. Pull any subset of data programmatically

### No Known Export Limits

No documented restrictions on export size or date range. The full backup exports everything.

### Import Formats

PocketSmith accepts: CSV, QIF, OFX — relevant for initial data migration or supplementing bank feeds with manual data.

---

## 6. Australian Bank Feed Coverage

### Dual Provider Architecture

PocketSmith uniquely offers **two separate aggregation providers** for Australian banks:

| Provider | Technology | AU Banks | Key Characteristic |
|----------|-----------|----------|-------------------|
| **Yodlee** (Envestnet) | Screen scraping / proprietary API | Major AU banks including CBA, ANZ | Established, 12,000+ global institutions. Traditional approach |
| **Basiq** | CDR (Consumer Data Right) / Open Banking | 120+ Australian banks | Newer, regulated, consent-based. 2-year history per CDR legislation |

Users can choose either provider per bank connection. If one has issues, switch to the other.

### CBA (Commonwealth Bank) — Known Behaviour

**Via Yodlee:**
- Transactions are set to **Pending status for at least 3 days** before moving to Posted. Yodlee does this because CBA often changes transaction details in the first few days. PocketSmith recommends enabling pending transactions in settings for CBA feeds
- This means there's a 3-day lag on "final" transaction data, but you get pending transactions immediately

**Via Basiq (CDR):**
- CDR connections deliver up to 2 years of initial history
- CDR consent flow may break with ad blockers or VPN connections
- Generally reliable but subject to "teething issues" as CDR matures

### ANZ — Known Behaviour

**Via Yodlee:**
- **Cannot provide pending transactions for ANZ Credit Card accounts** due to bank restrictions. Debit/savings accounts are fine
- Credit card transactions only appear once posted

**Via Basiq (CDR):**
- Available as an alternative. Same CDR limitations as CBA

### General Australian Feed Reliability

PocketSmith describes Basiq CDR feeds as "proving to be very reliable generally" but notes "it's still early days for CDR open banking feeds" with ongoing teething issues. Common problems across all providers:

- **Duplicate/missing transactions** — banks deliver inconsistently or change posted dates retroactively
- **Authorization failures** — occasional re-auth required
- **Sync errors** — temporary communication failures between Basiq and bank
- **Stalled accounts** — accounts stop receiving new transactions (rare, fixable by recreating feed)

**Workaround pattern:** If Basiq has issues, switch to Yodlee for that connection (or vice versa). Having dual providers is a significant resilience advantage.

### Superannuation

Dedicated super providers are **not available** via Basiq CDR. Some bank-integrated super accounts may work. This is a gap — Ghostfolio or manual tracking may still be needed for super.

---

## 7. PocketSmith API vs Firefly III API Comparison

| Dimension | PocketSmith API | Firefly III API |
|-----------|----------------|-----------------|
| **Type** | REST, JSON | REST, JSON |
| **Endpoint count** | ~44 endpoints | ~150+ endpoints |
| **Authentication** | Developer key (header) or OAuth 2.0 | Personal Access Token or OAuth 2.0 |
| **OpenAPI spec** | Yes (published on GitHub) | Yes (Swagger) |
| **Webhooks** | No | Yes (configurable triggers, responses, delivery formats) |
| **Bank feeds** | Built-in (Yodlee + Basiq for AU) | None for AU (manual CSV only) |
| **Transaction write-back** | Yes (update category, notes, labels) | Yes (full CRUD on all resources) |
| **Budget API** | Read budget summaries and trend analysis | Full CRUD on budgets, budget limits |
| **Rule engine API** | Read and create category rules | Full CRUD on rules with complex conditions |
| **Reports API** | Budget summary + trend analysis endpoints | Comprehensive reporting endpoints |
| **Recurring transactions** | Events/scenarios API | Bills and recurring transaction API |
| **Tags/labels** | Labels on transactions | Tags on transactions |
| **Attachments** | Full attachment API | Full attachment API |
| **Accounts** | Full CRUD | Full CRUD + account types, roles |
| **Currencies** | Multi-currency support | Multi-currency support |
| **Self-hosted** | No (SaaS only) | Yes (Docker, full control) |
| **Cost** | $0-27 AUD/month | Free (self-hosted) |
| **Hosting/maintenance** | Zero (cloud) | Docker management, backups, updates |
| **MCP servers** | Official first-party (57 tools) | 4+ community options (best: 66 tools) |
| **Rate limits** | Undocumented (presumably generous) | Self-hosted (no limits) |
| **Data sovereignty** | Data on PocketSmith servers (NZ company) | Data on your machine |
| **Incremental sync** | `updated_since` parameter | No native equivalent (filter by date) |

### Where Firefly III Wins

1. **More granular programmatic control** — 150+ endpoints vs 44. Full CRUD on everything including rules, piggy banks, recurrences, preferences
2. **Webhooks** — event-driven architecture possible. Firefly III can push notifications on transaction creation, which PocketSmith cannot
3. **Self-hosted data sovereignty** — all data stays on your machine
4. **No ongoing cost** — free software
5. **Double-entry accounting** — every transaction balances, full audit trail
6. **Rule engine depth** — complex multi-condition rules with actions beyond just categorisation

### Where PocketSmith Wins

1. **Australian bank feeds** — the killer feature. Automated CBA + ANZ connections via Yodlee or Basiq CDR. Firefly III has zero automated AU bank connectivity
2. **Zero infrastructure** — no Docker, no database backups, no server maintenance
3. **Official MCP server** — first-party, cloud-hosted, 57 tools, OAuth auth. Firefly III relies on community MCP servers
4. **Incremental sync** — `updated_since` parameter makes polling efficient
5. **Dual AU feed providers** — Yodlee and Basiq as fallbacks for each other
6. **Forecasting engine** — built-in projection capabilities (up to 60 years on Fortune plan)
7. **Partner access** — Mina can use the PocketSmith web/mobile UI directly without touching any technical infrastructure

### Verdict

**For an Australian household with CBA + ANZ, PocketSmith wins on the dimension that matters most: getting the data in automatically.** Firefly III is the superior tool for programmatic control, but it requires manual CSV imports for Australian banks, which is the friction that killed every previous budgeting attempt.

The optimal architecture is:
- **PocketSmith** handles: bank feed aggregation, transaction storage, basic categorisation, partner access (Mina), forecasting
- **Claude via MCP** handles: intelligent analysis, pattern detection, guardrail monitoring, scenario modelling, proactive alerts
- **Python compute layer** handles: deterministic aggregation, guardrail threshold checks, summary generation

---

## 8. PocketSmith Pricing — Full Breakdown

### All Plans (AUD)

| | Free | Foundation | Flourish | Fortune |
|---|---|---|---|---|
| **Monthly price** | $0 | $14.95 | $24.95 | $39.95 |
| **Annual price (per month)** | $0 | $9.99 | $16.66 | $26.66 |
| **Annual savings** | - | 33% | 33% | 33% |
| **Connected banks** | Yes (auto feeds) | 6 (1 country) | 18 | Unlimited |
| **Accounts** | 2 | Unlimited | Unlimited | Unlimited |
| **Dashboards** | 2 | 6 | 18 | Unlimited |
| **Budgets** | 12 | Unlimited | Unlimited | Unlimited |
| **Forecast projection** | 6 months | 10 years | 30 years | 60 years |
| **API access** | Yes (free) | Yes (free) | Yes (free) | Yes (free) |
| **MCP server** | Yes | Yes | Yes | Yes |
| **Support** | Community | Email | Email | Priority email |

### Recommendation

**Foundation ($9.99/month annual)** is the starting point. If you have 6 or fewer bank feed connections across CBA + ANZ, this covers it. Count each account connection separately (savings, transaction, credit card, mortgage offset, etc.).

If you have more than 6 connections, **Flourish ($16.66/month annual)** provides 18 connections which is more than enough for any household, plus 30-year forecasting and 18 dashboards.

**The free trial** should be the first step — connect one bank, verify the feed works, let Mina see the UI, then choose a paid plan.

---

## Architecture Decision: PocketSmith as Data Layer

### Why This Works

```
┌──────────────────────────────────────────────────────┐
│                    HUMAN LAYER                        │
│  PocketSmith UI (Mina's access point)                │
│  Google Sheets forecast (source of truth)             │
│  Monthly money meeting                                │
└────────────────────────┬─────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────┐
│              INTELLIGENCE LAYER (Claude)               │
│                                                        │
│  PLAIOS Finance Domain Context                         │
│  ├── claude.md (frameworks, guardrails)                │
│  ├── state/current-assessment.md                       │
│  ├── state/financial-model.yaml                        │
│  └── reference/ (on-demand)                            │
│                                                        │
│  PocketSmith MCP Server (57 tools)                     │
│  ├── Direct transaction queries                        │
│  ├── Budget vs actual analysis                         │
│  ├── Trend analysis                                    │
│  ├── Account balances                                  │
│  └── Write-back (categories, notes, labels)            │
│                                                        │
│  Three Modes:                                          │
│  1. Reactive — answer questions via conversation       │
│  2. Proactive — scheduled checks write alerts          │
│  3. Strategic — scenario modelling on demand            │
└────────────────────────┬─────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────┐
│                  DATA LAYER (PocketSmith)               │
│                                                        │
│  Bank Feeds (automated)                                │
│  ├── CBA accounts via Yodlee or Basiq CDR              │
│  ├── ANZ accounts via Yodlee or Basiq CDR              │
│  └── Auto-refresh on PocketSmith's schedule            │
│                                                        │
│  Transaction Storage                                   │
│  ├── Full history, indefinitely retained               │
│  ├── Pending + posted transactions                     │
│  └── Incremental sync via updated_since                │
│                                                        │
│  Categorisation                                        │
│  ├── Auto-categorisation rules                         │
│  ├── Category hierarchy                                │
│  └── AI can write back categories via MCP              │
│                                                        │
│  Forecasting                                           │
│  ├── Built-in projection engine                        │
│  └── Budget vs actual tracking                         │
│                                                        │
│  Accessed via:                                         │
│  ├── REST API (Python compute scripts)                 │
│  └── MCP Server (Claude direct queries)                │
└────────────────────────────────────────────────────────┘
```

### What PocketSmith Replaces

| Original Plan (Firefly III) | New Plan (PocketSmith) |
|------------------------------|------------------------|
| Manual CSV download from CBA/ANZ weekly | Automated bank feeds |
| Docker hosting + maintenance | Zero infrastructure |
| Community MCP server (evaluate 4 options) | Official MCP server (57 tools) |
| Build categorisation rules from scratch | PocketSmith's existing rule engine + AI write-back |
| No partner access without custom UI | Mina uses PocketSmith web/mobile directly |

### What Stays the Same

- Python compute layer for deterministic aggregation (savings rate, guardrail checks)
- Claude as intelligence layer (interpretation, advice, alerts, scenarios)
- PLAIOS state files (assessments, priorities, model)
- Google Sheets as human-owned forecast source of truth
- Scheduled tasks for proactive monitoring

### Key Risks

1. **Vendor dependency** — PocketSmith could change pricing, API terms, or shut down. Mitigation: regular CSV backup export, API data is portable
2. **Feed reliability** — Bank feeds can break temporarily. Mitigation: dual provider (Yodlee + Basiq), manual import as fallback
3. **No webhooks** — must poll for changes. Mitigation: `updated_since` makes polling efficient; for our cadence (daily/weekly), polling is fine
4. **Super tracking gap** — CDR doesn't cover dedicated super funds. Mitigation: manual tracking or Ghostfolio for investment/super
5. **Data not on our machine** — PocketSmith is a NZ company, data stored on their servers. Mitigation: API data is encrypted in transit, PocketSmith has SOC 2 Type II equivalent controls, acceptable risk for household finance data

---

## Sources

- [PocketSmith Developer Hub](https://developers.pocketsmith.com/)
- [PocketSmith API Introduction](https://developers.pocketsmith.com/docs/introduction)
- [PocketSmith OpenAPI Spec (GitHub)](https://github.com/pocketsmith/api)
- [PocketSmith API Pagination](https://developers.pocketsmith.com/docs/pagination)
- [PocketSmith Pricing Plans](https://my.pocketsmith.com/plans)
- [PocketSmith Billing & Plans](https://learn.pocketsmith.com/article/511-billing-plans)
- [PocketSmith API Developer Keys](https://learn.pocketsmith.com/article/1538-pocketsmith-api-developer-keys)
- [PocketSmith MCP Server Announcement](https://www.pocketsmith.com/news/2026-04-01-pocketsmith-mcp-server-connect-ai-tools-to-pocketsmith/)
- [PocketSmith MCP Server Docs](https://developers.pocketsmith.com/docs/pocketsmith-mcp-server)
- [dannyshaw/pocketsmith-mcp (Community)](https://github.com/dannyshaw/pocketsmith-mcp)
- [PocketSmith Bank Feeds Overview](https://learn.pocketsmith.com/article/500-feeds)
- [PocketSmith Basiq (AU CDR) Provider](https://learn.pocketsmith.com/article/1367-about-basiq-our-australian-cdr-data-provider)
- [PocketSmith Yodlee Provider](https://learn.pocketsmith.com/article/249-yodlee-and-the-bank-feed-service)
- [PocketSmith Bank Feed History Limits](https://learn.pocketsmith.com/article/280-bank-feed-transaction-history-limits)
- [PocketSmith Known Bank Feed Quirks](https://learn.pocketsmith.com/article/700-known-bank-feed-quirks)
- [PocketSmith Basiq Issues & Solutions](https://learn.pocketsmith.com/article/1373-possible-basiq-issues-and-solutions)
- [PocketSmith Transaction Export](https://learn.pocketsmith.com/article/158-exporting-your-transactions)
- [Firefly III API Documentation](https://api-docs.firefly-iii.org/)
- [Firefly III Webhooks](https://docs.firefly-iii.org/how-to/firefly-iii/features/webhooks/)
