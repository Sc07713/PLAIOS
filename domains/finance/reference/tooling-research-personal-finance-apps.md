# Personal Finance App Research — Self-Hosted / Open Source

**Date:** 2026-04-06
**Context:** Evaluating self-hosted personal finance tools for an Australian family (CBA + ANZ accounts). Requirements: cash flow analysis, transaction categorization, budgeting, minimum ongoing effort.

---

## The Australian Bank Data Problem

Before evaluating individual tools, the critical constraint for Australia:

**No open-source tool has automated bank sync for CBA or ANZ.**

- **Enable Banking** (Firefly III's primary provider): Europe-only (29 EU countries via PSD2)
- **GoCardless/Nordigen** (formerly used by Firefly III and Actual): EU/UK only. Also stopped accepting new accounts from July 2025
- **SimpleFIN** (Actual Budget): US/Canada only
- **Pluggy.ai** (Actual Budget): Brazil only
- **Australian CDR/Open Banking**: Exists, but accessing consumer transaction data requires ACCC accreditation as a data recipient — individuals cannot self-serve
- **Basiq** (Australian open banking aggregator): Supports 135+ AU banks including CBA and ANZ, but is a commercial B2B API platform with 12-month minimum contracts and sales-gated pricing — not viable for personal use
- **Up Bank**: Only Australian bank with a public API. There's a Firefly III importer for it, but irrelevant for CBA/ANZ

**Bottom line for CBA/ANZ:** Manual CSV import is the only realistic path. Both CBA (NetBank) and ANZ offer CSV export of transactions. CBA allows up to 600 transactions / 15 months of history per export. Pre-built Firefly III import configurations exist for both CBA and ANZ on GitHub.

---

## 1. Firefly III

**What it is:** Double-entry personal finance manager. The most mature and feature-complete open-source option.

### Setup
- **Docker:** Official Docker image, straightforward `docker-compose.yml`. Requires a separate Data Importer container. Expect 1-2 hours to get fully running with both containers configured.
- **Tech stack:** PHP/Laravel, MySQL or PostgreSQL
- **Latest version:** v6.5.7 (actively developed, development builds through April 2026)
- **GitHub:** ~17k stars, single dedicated maintainer (James Cole) with community contributions

### Bank Data (Australia)
- **Automated:** Not available for CBA/ANZ (see above)
- **CSV import:** Well-supported. Community-contributed import configurations exist for both [Commonwealth Bank](https://github.com/firefly-iii/import-configurations/tree/main/au/commonwealth-bank) and [ANZ](https://github.com/firefly-iii/import-configurations/blob/main/au/anz/default.json)
- **Import automation:** The Data Importer can be cron-scheduled, but for CSV you still need to manually download the file from NetBank/ANZ first, then trigger the import
- **Workflow:** Download CSV from bank website -> upload to Data Importer -> auto-categorized via rules

### Cash Flow & Reporting
- Built-in reports: income/expense, budget, category, tag, account balance
- Default dashboard shows account balances, recent transactions, budget status, expense/income summaries
- Budget reports with trend lines
- Weekly/monthly/yearly analysis views
- Expense category breakdowns
- **Strength:** Comprehensive reporting. Double-entry means every dollar is tracked with full audit trail
- **Weakness:** Reports are functional but not beautiful. No drag-and-drop dashboard customization

### Categorization & Budgeting
- **Auto-categorization:** Rule engine that matches transactions by description, amount, account, etc. and applies categories, tags, budgets automatically. Very powerful once configured — reduces ongoing effort significantly
- **Budgets:** Monthly budget limits per category with rollover options
- **Categories and tags:** Flexible dual taxonomy
- **Recurring transactions:** Scheduled expected transactions for forecasting

### Mobile Access
- Web UI is responsive but not mobile-optimized — usable but not pleasant
- **Third-party mobile apps:**
  - **Abacus** (iOS + Android) — native app, well-regarded
  - **Firefly Pico** — companion web app designed mobile-first (Vue/Nuxt, feels native)
  - **Waterfly III** — Android app (Flutter/Material 3)

### Maintenance Burden
- Periodic Docker image updates (`docker pull` + restart)
- Rule engine needs tuning as new transaction patterns emerge
- CSV import is the ongoing friction point: ~10 min/week to download, upload, review
- Database backups needed (standard Docker volume backup)

### Verdict
**Best overall tool for the stated requirements.** Most complete feature set, strongest rule engine for auto-categorization, best reporting. The CSV import friction is manageable at weekly cadence. The rule engine means categorization effort front-loads then drops off sharply.

---

## 2. Actual Budget

**What it is:** Envelope budgeting app (like YNAB). Local-first architecture — runs in browser, server is just a sync endpoint.

### Setup
- **Docker:** Single container, trivially simple. 15-30 minutes to get running
- **Tech stack:** TypeScript/Node.js, SQLite
- **Latest version:** Actively developed through 2026
- **GitHub:** ~25k stars, large community of contributors

### Bank Data (Australia)
- **Automated:** Not available for CBA/ANZ. SimpleFIN (US/Canada), GoCardless (EU/UK, no new signups), Pluggy (Brazil)
- **CSV import:** Supports CSV, QIF, OFX, QFX file formats
- **No import configurations repo** like Firefly III — you map columns manually (but it remembers mappings)

### Cash Flow & Reporting
- Built-in net worth and cash flow reports
- Cash flow shows income vs expenses over time
- Custom report builder for deeper analysis
- **Strength:** Clean, modern UI. Reports are visually appealing
- **Weakness:** Reporting is secondary to budgeting — less depth than Firefly III for pure cash flow analysis

### Categorization & Budgeting
- **Envelope budgeting:** Every dollar gets assigned to a category. Strong discipline model
- **Rules:** Basic auto-categorization via payee rules (less powerful than Firefly III's rule engine)
- **Budget focus:** This is the core strength — budget creation, tracking, rollover, goal-based saving
- Zero-sum approach: forces intentional allocation of every dollar

### Mobile Access
- **Progressive Web App** — responsive, works well on mobile browsers
- Local-first means it's fast even on mobile
- No native mobile app, but PWA experience is good

### Maintenance Burden
- Very low server maintenance (SQLite, minimal resources)
- Same CSV import friction as Firefly III
- End-to-end encryption available for sync

### Verdict
**Best for pure budgeting / envelope methodology.** Faster to set up, more modern UI, lower maintenance. But weaker on cash flow analysis and transaction categorization automation. If the primary goal is "where is our money going?" rather than "how do we allocate every dollar?", Firefly III is the better fit. If the goal is disciplined budget adherence, Actual is excellent.

---

## 3. GnuCash

**What it is:** Traditional double-entry accounting software. Desktop application (not web-based).

### Setup
- **No Docker / no web UI** — desktop application installed on Windows/Mac/Linux
- No self-hosting needed (runs locally), but also no remote access
- Latest version: 5.15.1 (March 2026), actively maintained. GnuCash 6.0 planned for March 2027

### Bank Data (Australia)
- Manual import of OFX, QIF, CSV files
- No automated bank sync of any kind
- No import configuration community for Australian banks

### Cash Flow & Reporting
- Full accounting reports: profit/loss, balance sheet, cash flow statement, portfolio valuation
- Reports are comprehensive but accounting-oriented (not consumer-friendly)
- Scheduling module for recurring transactions
- **Strength:** If you want proper accounting-grade reporting, GnuCash does it
- **Weakness:** Reports look like they're from 2005. Not designed for quick "where's my money going?" glances

### Categorization & Budgeting
- Manual categorization via account hierarchy (double-entry style)
- Budgeting exists but is rudimentary compared to Firefly III or Actual
- No rule engine for auto-categorization

### Mobile Access
- Android/iOS app exists but only for recording transactions — must manually sync to desktop
- No web interface at all
- No remote access to data

### Maintenance Burden
- Low (desktop app, local data files)
- But high manual effort per transaction — no automation, no rules, no smart categorization
- Requires accounting knowledge to use effectively

### Verdict
**Not recommended for this use case.** GnuCash is a proper accounting tool that happens to work for personal finance, not a personal finance tool. The manual effort per transaction is too high for a time-constrained user, there's no web access, no mobile story, and the UX is dated. It would be the right tool for someone who wants to maintain a proper set of books, but overkill and simultaneously underpowered for family cash flow monitoring.

---

## 4. Ghostfolio

**What it is:** Investment and wealth management tracker. Not a budgeting or cash flow tool.

### Setup
- **Docker:** Official compose file, straightforward. Requires PostgreSQL + Redis
- **Tech stack:** Angular + NestJS + Prisma + TypeScript
- Latest version: 2.248.0 (March 2026), very actively developed
- **GitHub:** ~8.1k stars, active community

### Investment Tracking
- Track stocks, ETFs, crypto, bonds, commodities, real estate
- **Data providers:** Yahoo Finance, CoinGecko, manual entry
- **ASX support:** Yahoo Finance provides ASX data (tickers with .AX suffix), though some users report occasional data provider errors for specific tickers
- Performance analysis with benchmarks, risk analysis, portfolio rebalancing tools
- Multi-currency support (AUD included)

### What It Does NOT Do
- No transaction tracking / cash flow
- No budgeting
- No bank account integration
- No expense categorization

### Mobile Access
- Progressive Web App (PWA) with mobile-first design — works well on phone

### Maintenance Burden
- Low — mainly Docker updates and ensuring data providers stay working
- Market data refreshes automatically

### Verdict
**Complementary tool, not a replacement.** Ghostfolio fills a specific niche: investment portfolio tracking with performance analytics. It would pair with Firefly III or Actual (Firefly III handles cash flow + budgeting, Ghostfolio handles investment portfolio). Worth considering if investment tracking is a priority, but it doesn't address any of the stated cash flow / budgeting requirements.

---

## 5. Other Notable Tools

### ezBookkeeping
- Lightweight, self-hosted, mobile-first PWA
- Smallest Docker footprint (~58MB image, 25MB idle RAM)
- AI receipt recognition via MCP (interesting for expense tracking)
- 2FA, PIN lock, WebAuthn security
- **Limitation:** No budgeting features, no rule engine, weaker reporting than Firefly III
- **Best for:** Quick daily transaction logging on mobile. Could complement Firefly III rather than replace it

### Sure (fork of Maybe Finance)
- Community fork of the abandoned Maybe Finance ($1M+ development, shut down July 2025)
- Ruby on Rails, self-hosted via Docker
- AI-powered budget suggestions, automatic categorization
- **Risk:** Community fork maturity is uncertain. The original was abandoned twice. Active development as of March 2026 but the contributor base and long-term viability are unclear
- **Best for:** Someone willing to bet on a young fork with a polished UI

### Financial Freedom (serversideup)
- Early-stage open source alternative to Mint/YNAB
- Laravel-based, Docker deployment
- Still in development — not production-ready

---

## Recommendation

### Primary Tool: Firefly III

**Why:**
1. **Most complete feature set** for cash flow analysis, categorization, and budgeting
2. **Rule engine** is the key differentiator — front-load categorization rules, then ongoing effort drops dramatically
3. **Pre-built CBA and ANZ CSV import configurations** exist
4. **Best reporting** for answering "where is our money going?"
5. **Strong community** and actively maintained
6. **Double-entry** means the numbers always balance — audit trail is built in

**Weekly workflow (estimated 10-15 min):**
1. Log into CBA NetBank and ANZ → export CSV for last 7 days
2. Upload to Firefly III Data Importer (with saved configurations)
3. Review auto-categorized transactions, fix any misses
4. Glance at dashboard

**Setup investment:**
- 2-3 hours for Docker setup (Firefly III + Data Importer)
- 2-3 hours for initial configuration (accounts, categories, budgets, rules)
- 1-2 hours for first CSV import and rule tuning
- Total: ~1 day to get fully operational

### Optional Add-on: Ghostfolio (if investment tracking matters)

Separate Docker stack. Track shares, super balances, crypto. 1 hour setup.

### Why Not Actual Budget

Actual is excellent software with a better UI, but:
- Its rule engine is weaker (Firefly III's is critical for minimizing ongoing effort)
- Its reporting focuses on budget adherence rather than cash flow analysis
- For "maximum visibility, minimum effort," Firefly III's automation capabilities win
- If the household later decides to adopt strict envelope budgeting, Actual could replace or complement Firefly III

---

## Future Automation Possibilities

The manual CSV download is the main friction point. Potential future improvements:

1. **Browser automation:** A Playwright/Puppeteer script could log into NetBank/ANZ, download CSV, and feed it to the Data Importer API on a schedule. Fragile (breaks on UI changes) but possible
2. **Australian CDR maturation:** If/when personal-use CDR access becomes available without commercial accreditation, automated bank sync would become viable
3. **Basiq or similar:** If Basiq ever offers a personal/developer tier at reasonable cost, it could bridge the gap
4. **Email parsing:** Some banks email transaction notifications — a script could parse these into Firefly III via API (partial, but real-time)

---

## Sources

- [Firefly III](https://www.firefly-iii.org/) | [GitHub](https://github.com/firefly-iii/firefly-iii) | [Docs](https://docs.firefly-iii.org/)
- [Firefly III CBA Import Config](https://github.com/firefly-iii/import-configurations/tree/main/au/commonwealth-bank) | [ANZ Import Config](https://github.com/firefly-iii/import-configurations/blob/main/au/anz/default.json)
- [Actual Budget](https://actualbudget.org/) | [GitHub](https://github.com/actualbudget/actual) | [Bank Sync Docs](https://actualbudget.org/docs/advanced/bank-sync/)
- [GnuCash](https://www.gnucash.org/) | [GitHub](https://github.com/Gnucash/gnucash)
- [Ghostfolio](https://www.ghostfol.io/) | [GitHub](https://github.com/ghostfolio/ghostfolio)
- [ezBookkeeping](https://ezbookkeeping.mayswind.net/) | [GitHub](https://github.com/mayswind/ezbookkeeping)
- [Sure (Maybe Finance fork)](https://github.com/we-promise/sure)
- [Basiq](https://www.basiq.io/) | [Australian Open Banking Database](https://github.com/LukePrior/Australian-Open-Banking-Data-Database)
- [Australian CDR Standards](https://consumerdatastandardsaustralia.github.io/standards/)
