# Australian Bank Transaction Data — Programmatic Access Research

**Date:** 2026-04-06
**Context:** Research into all viable paths for an individual or small business to get automated transaction feeds from CBA and ANZ in Australia. This is the critical bottleneck for building a personal finance automation system.

---

## Executive Summary

**The landscape has shifted significantly since early 2025.** CBA's mandatory MFA (March 2025) killed screen scraping as a viable path, pushing the entire ecosystem toward CDR/Open Banking. For an individual wanting automated bank feeds from CBA and ANZ, there are exactly two realistic paths in 2026:

1. **PocketSmith as aggregator layer** (recommended) -- $10-25/month, bank feeds via Basiq CDR, full REST API to pull data out. Works today.
2. **Basiq direct** (possible but uncertain for individuals) -- Free sandbox, but production access requires sales engagement, 12-month minimum contract, $0.50/user/month + platform fee, likely requires business entity.

Everything else is either blocked by accreditation requirements ($250K+), enterprise-only pricing, NZ-only, or technically dead due to MFA.

---

## 1. Australian CDR (Consumer Data Right) / Open Banking

### Current State (April 2026)

The CDR is live and maturing. Key facts:

- **100+ financial institutions** now participate, including all Big 4 (CBA, NAB, Westpac, ANZ), regional banks, neobanks, credit unions, and building societies
- **Participant numbers grew 55% year-over-year** in 2025
- **Data available:** Account details, balances, transaction history (7 years for CBA), direct debits, scheduled payments, payees, product information
- **Security:** Financial-grade API (FAPI) 2.0 -- OAuth 2.0 with PKCE, mutual TLS, signed JWTs, encrypted transfer
- **Expanding scope:** Non-bank lenders from July 2026, energy already live, telecoms and potentially super planned

### Action Initiation (Write Access)

The Treasury Laws Amendment (Consumer Data Right) Act 2024 passed on 26 August 2024 with bipartisan support, bringing "action initiation" to CDR. This will eventually allow a consumer to permit a service provider to initiate payments on their behalf. Implementation timeline is still rolling out.

### Can an Individual Access Their Own Data Programmatically?

**No, not directly.** The CDR is designed as a B2B2C framework. To access consumer data via CDR APIs, you must be one of:

1. **Unrestricted Accredited Data Recipient (ADR):** Full ACCC accreditation. Estimated cost: **$250,000+** for the application, plus $50,000-70,000 for compliant data storage infrastructure. Takes months. Completely impractical for personal use.

2. **CDR Representative:** Partner with an existing unrestricted ADR as "principal." Faster (4-8 weeks), cheaper (no independent IT assurance report needed), but still requires a formal arrangement with a commercial ADR. Not designed for individuals.

3. **Sponsored Affiliate:** Access CDR data through a principal ADR. Same privileges as an ADR at lower cost and less time. Still a commercial arrangement.

**Bottom line:** There is no "log in with your MyGov and get your own bank API key" pathway. The CDR is designed for businesses serving consumers, not for consumers serving themselves. Industry bodies (FinTech Australia) have called for reform to simplify participation for SMEs, but nothing has changed yet.

### Secondary Users

An individual account holder can nominate another person as a "secondary user" who can then authorize data sharing. This doesn't help for self-service programmatic access -- it's about allowing a partner or family member to authorize CDR sharing to a (still-accredited) data recipient.

---

## 2. Basiq

### What It Is

Australian open banking API platform. ACCC-accredited Data Recipient. Connects to 135+ Australian and NZ financial institutions including CBA and ANZ. This is PocketSmith's data provider for Australia.

### Pricing (2026)

| Component | Cost |
|-----------|------|
| Customer data | $0.50 per user/month |
| Platform access fee | Not publicly disclosed (requires sales) |
| Data enrichment (Insights) | $0.25 per user/month (optional) |
| Affordability reports | From $3.00 per report (optional) |
| Minimum contract | **12 months** |
| User definition | Each unique customer who connects a bank account |

### Developer / Personal Access

- **Free sandbox:** Yes. Sign up, generate an API key, test against sandbox banks. Up to 500 sandbox connections per account. Includes a PFM demo kit.
- **Production access:** Requires contacting their sales team. Must go through a "go-live checklist" including dashboard setup, team invitations, institution selection, and a walkthrough with their onboarding team.
- **Individual/personal tier:** **Does not exist.** Basiq is a B2B platform. Pricing is per-user/month based on volume commitments negotiated with sales. There is no self-serve "pay $5/month for 1 user" option.
- **Startup options:** They mention "various commercial options to help startups minimize cash flow impact" but these are still negotiated, not published.

### Realistic Assessment for Personal Use

You could theoretically approach Basiq as a sole trader / ABN holder building a personal finance tool, but:
- 12-month minimum commitment
- Unknown platform access fee on top of per-user costs
- For 1 user (yourself), the economics make no sense from Basiq's perspective
- They are geared toward serving companies building products for many consumers

**Verdict:** Sandbox is useful for learning. Production access for personal use is not a viable path.

---

## 3. Yodlee (Envestnet)

### What It Is

Global financial data aggregator. Part of Envestnet. Historically one of the biggest screen-scraping providers, now transitioning to CDR/Open Banking in Australia.

### Australia Access

- Yodlee is a CDR-accredited data recipient in Australia
- They offer an "AU Open Banking" product through their developer portal
- **Developer tiers:** "Launch" tier gives access to a test bank for CDR test data only. Live data from real banks is **not available** through the developer portal
- **Production access:** Requires their "Enterprise" option -- contact sales
- **Pricing:** Under NDA. Not publicly disclosed. Multiple sources confirm pricing is negotiated case-by-case

### How PocketSmith Uses Yodlee

PocketSmith previously used Yodlee as their primary aggregator worldwide. They have been transitioning Australian feeds to **Basiq** (CDR-based) and now offer Basiq CDR feeds as the primary option for Australian banks. Yodlee feeds remain available as a backup/fallback for some institutions.

### Individual Developer Access

**Not viable.** The Launch tier only provides test data. Production requires enterprise engagement with NDA-protected pricing. There is no self-serve path to live Australian bank data through Yodlee.

---

## 4. Akahu

### What It Is

New Zealand's leading open finance platform. Connects to NZ banks and financial institutions via both screen scraping (legacy) and official open banking APIs.

### Australia Expansion

**Akahu has NOT expanded to Australia.** Their operations are exclusively New Zealand-focused. Key 2025-2026 developments:

- Received NZ CDR accreditation in December 2025
- Migrating all NZ traffic to official open banking APIs by March 2026
- Signed partnership with Westpac NZ
- Connects to 70+ NZ government, corporate, and fintech organizations

### Pricing (NZ only, for reference)

Akahu has published pricing for NZ: free tier available, usage-based pricing. But this is irrelevant for Australian bank access.

**Verdict:** Not applicable. NZ only.

---

## 5. Frollo

### What It Is

Australia's leading Open Banking platform provider and CDR-accredited data recipient. They operate both:
- A **consumer app** (Frollo -- money management / personal finance)
- A **B2B platform** (white-label money management, CDR data access for businesses)

### Consumer App

- Free personal finance app (iOS + Android)
- Uses CDR to link bank accounts (no credential sharing)
- Features: spending tracking, budgets, financial wellbeing tools, insights
- **Data export:** Users can export transaction data as CSV or download a PDF financial snapshot
- **No API for consumers.** The app is a closed consumer product

### B2B Platform / Developer API

- Frollo has a developer portal (developer.frollo.com.au) with CDR API documentation
- Their API provides CDR-compliant endpoints for retrieving consumer-permissioned data
- **But:** This is a B2B product. The API is for businesses building financial products, not for individuals
- Launched "Frollo for Brokers" in June 2025 -- CDR data access for mortgage brokers
- Pricing: Not published. Enterprise sales process

### Can You Use the Consumer App as a Data Source?

The Frollo consumer app lets you export CSV. You could theoretically:
1. Connect CBA + ANZ in the Frollo app
2. Periodically export CSV
3. Import into your own system

But this is manual, the same friction as downloading CSVs from the bank directly, and the app isn't designed as a data pipeline.

**Verdict:** Not a viable programmatic path. Consumer app is a closed product. B2B platform requires enterprise engagement.

---

## 6. Other Australian Fintech Aggregators (2025-2026)

### Fiskil

- Australian CDR platform provider
- Supports all three CDR access pathways (ADR, Representative, Sponsored)
- Connects to 100+ Australian financial institutions
- Banking API provides accounts, balances, transactions, direct debits, scheduled payments
- FAPI 2.0 compliant
- **Pricing:** Not publicly disclosed. Developer console available but production access requires engagement
- **Individual access:** Not addressed. Likely enterprise-focused like Basiq

### illion (now Experian)

- Among the first ACCC-accredited data recipients
- Focuses on credit risk, data aggregation, financial insights
- Part of Experian as of recent acquisition
- Open banking platform for businesses
- **Individual access:** No. Enterprise B2B only

### Up Bank

- Only Australian bank with a **public consumer API**
- But this is for Up Bank customers only -- irrelevant for CBA/ANZ data

### Wych.io

- New entrant marketing "removes biggest CDR barrier for smaller lenders and fintechs"
- Focused on making CDR accessible to smaller businesses
- Still a B2B platform, not individual-access

### Summary of New Entrants

No new aggregator has launched a personal/developer tier for individual access to Australian bank data in 2025-2026. The market remains firmly B2B. The CDR's accreditation framework effectively prevents individual access by design.

---

## 7. Bank-Specific Developer APIs

### Commonwealth Bank (CBA)

**Developer portal:** commbank.com.au/developer

**Available APIs:**
- **Product APIs:** Public, unauthenticated. CDR-compliant product information (interest rates, fees, features). Anyone can query these. No consumer data.
- **Transaction APIs:** CDR-compliant. 7 years of transaction history (from 1 Jan 2017) for active accounts. Includes transaction type, status, description, posting/execution date, amount, currency, reference. **But only accessible by accredited data recipients.**
- **PayTo API:** Payment initiation for businesses
- **NameCheck API:** Validate payment beneficiary details
- **Webhooks:** Real-time account notifications (for accredited recipients)

**Known issues (2025):** CBA reported intermittent issues with consumer API calls for new/amended consents, with a fix expected by 31 August 2025.

**Data sharing timeline:** Working to enable data sharing for all affected accounts by 30 September 2026.

**Individual developer access to transaction data:** **No.** Product APIs are public but contain no consumer data. Transaction/account APIs require CDR accreditation.

### ANZ

**Developer portal:** ANZ Product APIs at api.anz/cds-au/v1

**Available APIs:**
- **Product APIs:** Public, unauthenticated. CDR-compliant. `GET /banking/products` and `GET /banking/products/{productId}`. Product details, rates, fees.
- **Consumer data (accounts, transactions):** Only available to accredited data recipients via CDR

**NZ operations (separate):** ANZ NZ has launched Payment Requests and Data Sharing services through Akahu/NZ open banking standards. Not applicable to Australian accounts.

**Individual developer access to transaction data:** **No.** Same as CBA -- product APIs only for public access.

### Summary

Both CBA and ANZ offer **public product APIs** (what products exist, their rates and features). Neither offers any path for an individual to access their own transaction data via API. All consumer data access goes through CDR, which requires accreditation.

---

## 8. Screen Scraping / Automation Legality

### Legal Status (2026)

Screen scraping is **not explicitly illegal** in Australia (unlike the UK where it's been banned). However:

- **Bank Terms of Service:** Most Australian banks prohibit sharing credentials or automated access in their T&Cs. Violating T&Cs could void fraud protections under the ePayments Code
- **ePayments Code risk:** Consumers who share banking credentials may lose the right to be indemnified for unauthorized transactions. If your automated script leads to a compromise, you have no recourse
- **Criminal law:** No specific "hacking statute" for accessing your own accounts, but intent/method matters
- **Government position:** Treasury released a discussion paper on screen scraping in August 2023. OAIC recommended prohibiting screen scraping where safer alternatives (CDR) exist. No ban yet, but the direction is clear -- CDR is intended to replace screen scraping

### Practical Status (2026): DEAD

Regardless of legality, **screen scraping is now technically non-viable for CBA:**

- **CBA mandatory MFA (March 2025):** All NetBank logins now require multi-factor authentication -- one-time code or CommBank app approval. This cannot be satisfied by automated scripts
- **Impact:** Automated logins fail silently or break entirely. The MFA prompt blocks access
- **Other banks following:** The article notes "CommBank isn't alone, other banks are likely to follow with similar security upgrades"

### Unofficial CBA API Projects

There are community GitHub projects (jcwillox/commbank-api, thebowenfeng/commbank-api-client) that reverse-engineered CBA's mobile app API. These:
- Were fragile before MFA
- Are almost certainly broken now
- Violate CBA's terms of service
- Provide no stability guarantees

**Verdict:** Screen scraping is dead as a practical option in Australia, killed by MFA rollout. Even if it were technically possible, the legal risk (voiding fraud protections) makes it inadvisable.

---

## 9. PocketSmith as the Aggregator Layer

This is the most promising path by far. Here's the detailed analysis.

### How It Works

```
CBA/ANZ  --[CDR/Open Banking]-->  Basiq (accredited ADR)  --[API]-->  PocketSmith  --[REST API]-->  Your System
```

PocketSmith handles the CDR complexity. You never touch CDR directly.

### PocketSmith's Australian Bank Feed Architecture

- **Data provider:** Basiq (ACCC-accredited Data Recipient)
- **Connection method:** CDR/Open Banking (credential-free, consent-based)
- **Banks supported:** 120+ via Basiq, including all Big 4 (CBA, ANZ, NAB, Westpac)
- **Fallback:** Yodlee feeds remain as backup for some institutions
- **Connection flow:** User authorizes directly with their bank (redirected to bank's consent page). No banking credentials are shared with PocketSmith or Basiq

### PocketSmith Pricing (AUD, April 2026)

| Plan | Monthly | Annual (per month) | Connected Banks | Key Limits |
|------|---------|-------------------|----------------|------------|
| Free | $0 | $0 | 0 (manual only) | 2 accounts, 12 budgets, 6-month projection |
| Foundation | $14.95 | $9.99 | 6 | 1 country, 10-year projection |
| Flourish | $24.95 | $16.66 | 18 | All countries, 30-year projection |
| Fortune | $39.95 | $26.66 | Unlimited | Unlimited everything, priority support |

**For CBA + ANZ (2 banks, multiple accounts):** Foundation plan ($10-15/month) should suffice. Each "connected bank" means one bank institution, and you can connect multiple accounts at that bank.

### PocketSmith REST API

**Authentication:** Developer key (X-Developer-Key header). Generate via Profile > Security & Integrations > Manage developer keys. Key shown once at creation -- save it immediately.

**Cost:** The API is described as "available for anyone to use without restriction and free of charge." No additional cost beyond your PocketSmith plan.

**Available endpoints (v2):**

| Resource | Endpoints | Key Operations |
|----------|-----------|---------------|
| Users | User profile, preferences | Get user info |
| Institutions | Financial institution data | List connected institutions |
| Accounts | Bank/financial accounts | List, get, update accounts |
| Transaction Accounts | Transactional account detail | List, get transaction accounts |
| **Transactions** | **Individual transaction operations** | **List, get, create, update, delete** |
| Categories | Expense categorization | List, get, create, update, delete |
| Category Rules | Auto-categorization rules | CRUD on rules |
| Budgeting | Budget data and trends | Get budgets, budget analysis |
| Events | Scenario/calendar events | CRUD on events |
| Attachments | Document management | Upload, download |
| Labels | Transaction tags | List, manage |
| Saved Searches | Stored queries | CRUD |
| Currencies | Multi-currency support | List currencies |
| Time Zones | Timezone data | List |

**Transaction data returned:**
- Transaction ID, type (debit/credit), amount, date
- Payee/merchant name, memo
- Category, labels, notes
- Closing balance, transfer status
- Upload source, status (pending/posted)
- Created/updated timestamps

**API specification:** Full OpenAPI 3 spec at github.com/pocketsmith/api. Can generate typed clients for any language.

**Rate limits:** Not publicly documented. Likely reasonable for personal use.

### PocketSmith MCP Server (Official)

PocketSmith launched an **official MCP server** in April 2026. This is directly relevant to the Household CFO architecture.

**Setup:** `claude mcp add pocketsmith --transport http https://mcp.pocketsmith.com/mcp`

**Capabilities:**
- View all account balances (checking, savings, credit cards, investments)
- Get detailed account information with transaction history
- Track net worth across multiple accounts
- Budget summaries for any time period
- Analyze per-category spending vs budgets
- Spending trends across categories
- Compare actual vs forecasted amounts
- List, search, filter transactions
- Create new transactions (manual entries)
- Update transaction details (categorize, add notes, set labels)
- Delete duplicate or incorrect transactions
- List categories with hierarchical structure

**Access modes:** Read-only (insights only) or Full access (read + write)

### The PocketSmith-as-Aggregator Architecture

This is the recommended path:

```
┌─────────────────────────────────────┐
│           YOUR BANKS                │
│  CBA + ANZ (CDR-enabled)           │
└──────────────┬──────────────────────┘
               │ CDR consent (one-time, renewable)
               ▼
┌─────────────────────────────────────┐
│           BASIQ                     │
│  Accredited Data Recipient         │
│  Handles CDR compliance, MFA,      │
│  FAPI 2.0, token management        │
└──────────────┬──────────────────────┘
               │ Aggregated data feed
               ▼
┌─────────────────────────────────────┐
│        POCKETSMITH                  │
│  $10-15/month (Foundation plan)    │
│  Auto bank feeds, categorization   │
│  Budgeting, forecasting            │
│  REST API + MCP Server             │
└──────┬───────────────┬──────────────┘
       │ REST API      │ MCP Server
       ▼               ▼
┌──────────────┐ ┌────────────────────┐
│ Python       │ │ Claude Code        │
│ Compute      │ │ (via MCP)          │
│ Layer        │ │                    │
│ (aggregates, │ │ Direct queries,    │
│  guardrails) │ │ conversational     │
└──────┬───────┘ │ finance advisor    │
       │         └────────────────────┘
       ▼
┌─────────────────────────────────────┐
│        PLAIOS Finance Domain        │
│  State files, assessments, alerts   │
└─────────────────────────────────────┘
```

### Advantages of This Architecture

1. **No CDR accreditation needed.** PocketSmith + Basiq handle all compliance
2. **No screen scraping.** CDR consent flow is bank-grade secure
3. **CBA MFA is not a problem.** CDR bypasses MFA entirely (separate auth channel)
4. **Two data extraction paths:** REST API for compute scripts, MCP for Claude conversations
5. **Cost-effective:** $10-15/month for the aggregation layer
6. **Mina-friendly:** PocketSmith has a real UI. Both partners can see the data
7. **Rich data model:** Transactions come with merchant names, categories, amounts, dates
8. **Write-back capability:** Can categorize, label, and annotate transactions via API/MCP
9. **Incremental sync:** API supports `updated_since` parameter for efficient polling

### Limitations

1. **No webhooks.** Must poll for new transactions (but polling is lightweight)
2. **CDR consent renewal.** Consent typically lasts 12 months; must re-authorize periodically
3. **Lag:** Transactions may take up to 24 hours to appear (CDR batch processing)
4. **Super/business accounts:** Superannuation providers not yet CDR-enabled. Business/trust accounts may need bank enablement
5. **Basiq dependency:** If Basiq has issues, your feed is disrupted (check status.basiq.io)
6. **Rate limits:** API rate limits not publicly documented

### vs. Original Firefly III Architecture

The previous research recommended Firefly III with manual CSV import. PocketSmith-as-aggregator changes the calculus:

| Factor | Firefly III + CSV | PocketSmith + API |
|--------|-------------------|-------------------|
| Bank feeds | Manual CSV download weekly | Automatic via CDR |
| Ongoing effort | 10-15 min/week for CSV | Zero (automated) |
| Data freshness | Weekly at best | Daily (CDR batch) |
| Cost | Free (self-hosted) | $10-15/month |
| Mina accessibility | Web UI (local only) | Full consumer app + web |
| API for AI | Firefly III API (self-hosted) | PocketSmith REST API (cloud) |
| MCP integration | Community Firefly III MCP servers | Official PocketSmith MCP server |
| Self-hosting | Required (Docker) | None (SaaS) |
| Privacy | All data local | Data in PocketSmith cloud (NZ company) |
| Categorization | Manual rules in Firefly III | PocketSmith + manual refinement |

**The trade-off:** PocketSmith costs money and puts data in the cloud, but eliminates the manual CSV friction that was the biggest practical barrier. For a time-constrained household, automated feeds at $10-15/month is the clear winner.

---

## 10. Decision Matrix

| Path | Feasible? | Cost | Effort | Automation | Notes |
|------|-----------|------|--------|------------|-------|
| CDR direct (own ADR) | No | $250K+ | Months | Full | Absurd for personal use |
| CDR representative | No | Unknown | Weeks | Full | Requires commercial ADR partner |
| Basiq direct | Maybe | ~$6/yr min + platform fee | Medium | Full | 12-month contract, needs sales engagement, likely needs ABN |
| Yodlee direct | No | Enterprise NDA | High | Full | No self-serve path |
| Fiskil direct | No | Not disclosed | High | Full | Enterprise-focused |
| illion/Experian | No | Enterprise | High | Full | B2B only |
| Frollo app (CSV) | Yes | Free | High (manual) | None | Same as bank CSV export |
| CBA/ANZ APIs | No | N/A | N/A | N/A | CDR accreditation required |
| Screen scraping | No | Free | N/A | Dead | CBA MFA killed it March 2025 |
| Akahu | No | N/A | N/A | N/A | NZ only |
| **PocketSmith** | **Yes** | **$10-15/mo** | **Low** | **Full** | **Recommended path** |
| Manual CSV import | Yes | Free | Medium | None | Fallback option |

---

## 11. Recommendation

**Use PocketSmith as the aggregator layer.** The architecture is:

1. **PocketSmith Foundation plan** (~$10/month annual) -- connects CBA + ANZ via Basiq CDR
2. **PocketSmith REST API** -- Python compute layer polls for transactions, computes aggregates
3. **PocketSmith MCP Server** -- Claude has direct conversational access to financial data
4. **PLAIOS Finance Domain** -- state files, assessments, alerts, frameworks

This eliminates the bank data bottleneck entirely. The remaining work is building the intelligence layer (compute scripts, scheduled checks, scenario models), which is the interesting part.

### Immediate Next Steps

1. Get Mina's approval on PocketSmith
2. Sign up for Foundation plan ($10/month annual or $15/month monthly)
3. Connect CBA + ANZ via Basiq CDR consent flow
4. Generate developer API key
5. Set up PocketSmith MCP server in Claude Code
6. Let data accumulate 2-3 weeks
7. Begin building compute layer and Household CFO system

---

## Sources

- [Australian CDR Standards](https://consumerdatastandardsaustralia.github.io/standards/)
- [CDR Rollout Timeline](https://www.cdr.gov.au/rollout)
- [CDR Accreditation Guidelines v6](https://www.cdr.gov.au/sites/default/files/2025-08/CDR-accreditation-guidelines-version-6-published-26-August-2025.pdf)
- [CDR Action Initiation Legislation](https://www.ashurst.com/en/insights/action-initiation-under-australia-consumer-data-right-becomes-law/)
- [Basiq Pricing](https://www.basiq.io/pricing.html)
- [Basiq Developer Hub](https://api.basiq.io/docs/guides)
- [Basiq Go-Live Checklist](https://api.basiq.io/docs/go-live-checklist)
- [Basiq Quickstart API](https://api.basiq.io/docs/quickstart-api)
- [Yodlee AU Open Banking Developer Portal](https://developer.yodlee.com/products/yodlee/au-open-banking/docs/docs)
- [Yodlee Pricing (Quora)](https://www.quora.com/How-expensive-is-Yodlees-API)
- [Akahu Official](https://www.akahu.nz/)
- [Akahu November 2025 Update](https://www.2120.nz/p/akahu-november-2025-update)
- [Frollo CDR API](https://developer.frollo.com.au/docs/frollo-api/ZG9jOjI0MDgxNzkw-cdr)
- [Frollo Consumer App](https://frollo.com.au/frollo-app/)
- [Frollo Phasing Out Screen Scraping](https://blog.frollo.com.au/phasing-out-screen-scraping/)
- [Fiskil Open Banking AU](https://www.fiskil.com/grow/banking-api/open-banking-au)
- [Fiskil: CBA MFA and End of Screen Scraping](https://blog.fiskil.com/commbank-mfa-and-the-end-of-screen-scraping)
- [illion Open Banking](https://www.illion.com.au/credit-risk/open-banking/)
- [CommBank Developer Portal](https://www.commbank.com.au/developer)
- [CommBank Open Banking](https://www.commbank.com.au/banking/open-banking.html)
- [ANZ Product APIs](https://www.anz.com.au/support/legal/anz-apis/)
- [ANZ Open Banking Data Sharing](https://www.anz.com.au/privacy/centre/open-banking-data-sharing/)
- [Australian Open Banking Data Database (GitHub)](https://github.com/LukePrior/Australian-Open-Banking-Data-Database)
- [Treasury Screen Scraping Discussion Paper](https://treasury.gov.au/sites/default/files/2023-08/c2023-436961-dp.pdf)
- [PocketSmith: Basiq Australian CDR Provider](https://learn.pocketsmith.com/article/1367-about-basiq-our-australian-cdr-data-provider)
- [PocketSmith Plans and Pricing](https://my.pocketsmith.com/plans)
- [PocketSmith Developer Hub](https://developers.pocketsmith.com/)
- [PocketSmith API (GitHub OpenAPI spec)](https://github.com/pocketsmith/api)
- [PocketSmith Developer Keys](https://learn.pocketsmith.com/article/1538-pocketsmith-api-developer-keys)
- [PocketSmith Official MCP Server](https://www.pocketsmith.com/news/2026-04-01-pocketsmith-mcp-server-connect-ai-tools-to-pocketsmith/)
- [PocketSmith Data Connections Launch](https://www.pocketsmith.com/blog/data-connections-launch-sunrise/)
- [Open Banking Tracker: Australia](https://www.openbankingtracker.com/country/australia)
- [Basiq Alternatives (Meniga)](https://www.meniga.com/guides/basiq-alternatives/)
- [CDR Accreditation Cost Estimates (Lexology)](https://www.lexology.com/library/detail.aspx?g=6d51f9e1-6825-4157-8386-35c92c24b92c)
- [FinTech Australia 2025 CDR Ecosystem Report](https://www.fintechaustralia.org.au/newsroom/fintech-australia-unveils-2025-cdr-ecosystem-map-and-report-amid-record-consumer-data-requests-and-calls-for-reform)
- [Stripe: CDR Framework Overview](https://stripe.com/resources/more/the-state-of-open-banking-in-australia)
