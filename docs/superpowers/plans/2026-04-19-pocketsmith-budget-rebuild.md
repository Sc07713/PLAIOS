# PocketSmith Budget Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace PocketSmith's auto-generated default budget with a hand-built event set that mirrors the household budget spreadsheet, modelling mortgages as Interest (expense) + Principal (transfer), and tracking lumpy items at their actual cadence.

**Architecture:** This is an MCP-tool-driven plan, not code. Each task issues PocketSmith MCP calls (read for discovery, then delete + create for the rebuild) and writes/updates a small set of local files (snapshot JSON, mapping doc, finance state files). There are no unit tests — verification is via PocketSmith query tools (`list_events`, `get_budget_summary`) confirming the resulting state.

**Tech Stack:** PocketSmith MCP server, local Markdown/JSON files, git for the local files.

**Spec:** `docs/superpowers/specs/2026-04-19-pocketsmith-budget-design.md`

**Working assumptions** (validated by spec):
- User ID: `783484` (Scott McKennie)
- Spreadsheet line item amounts as authoritative for non-mortgage cashflow
- Interest amounts derived from PocketSmith's 7-month transaction history per loan
- Hillside minimum repayment ≈ $2,200/mo (rent self-funds it, confirm in Task 1)
- Start dates: monthly events from 2026-05-01; quarterly aligned to 2026-07-01; yearly placed on best-known renewal date (or 2026-12-01 if unknown); termly school items at 2026-07-15 (Term 3 estimate); Harmoney 2026-04-24 (next debit)

---

## Task 1: Discovery — Inventory accounts, scenarios, and existing events

**Files:**
- Create: `domains/finance/reference/_budget_dumps/2026-04-19-discovery-notes.md` (working notes from this task; gets folded into the mapping doc later)

- [ ] **Step 1.1: List all accounts to map account → scenario IDs**

Call:
```
mcp__pocketsmith__list_accounts(user_id=783484)
```

Record into the discovery notes file: for each account, `account_id`, `account_title`, all `scenarios[*].id` and `scenarios[*].title`. Specifically identify these scenarios (will be referenced repeatedly):
- **Complete Access** (Scott's main operating account) — scenario for Scott salary, household debits, Sassafras/Park View/Hillside-extra repayments
- **Go Account** (Mina's spending account) — scenario for various household expenses already routed there
- **Variable Home Loan (Sassafras)** — loan account scenario, interest events live here
- **Park View loan** — loan account scenario
- **Hillside loan** — loan account scenario
- Any account ending in **7233** — Harmoney debit account

If any of these don't exist or are not obvious from titles, note the discrepancy in the discovery file and pause for human input.

- [ ] **Step 1.2: List existing budget events for snapshot**

Call:
```
mcp__pocketsmith__list_events(user_id=783484, start_date="2026-04-01", end_date="2026-05-31")
```

Save the FULL JSON response (do not transform) to:
```
domains/finance/reference/_budget_dumps/2026-04-19-pre-rebuild-events.json
```

Count the events. Should be ~31. Record count in discovery notes.

- [ ] **Step 1.3: Sanity-check for manual edits to existing events**

Open the snapshot JSON and look at `created_at` vs `updated_at` timestamps. Auto-generated defaults will have these very close together (within minutes). If any event has `updated_at` significantly later than `created_at` (e.g. >1 day), it may be a manual edit — flag it in discovery notes and confirm with the user before deleting.

- [ ] **Step 1.4: Pull mortgage interest history per loan account**

For EACH of the three loan accounts identified in Step 1.1, call:
```
mcp__pocketsmith__list_transactions(
  user_id=783484,
  account_id=<loan account id>,
  category_id="<Loan Interest category id, 31204939>",
  start_date="2025-09-01",
  end_date="2026-04-18",
  per_page=100
)
```

Note: pre-2026-04-18 the Loan Interest category did not exist (it was created 2026-04-18). Earlier interest charges may be in the old `Interest` category (id `31156824`). If `Loan Interest` returns nothing for older months, fall back to:
```
mcp__pocketsmith__list_transactions(
  user_id=783484,
  account_id=<loan account id>,
  category_id="31156824",
  start_date="2025-09-01",
  end_date="2026-04-18",
  per_page=100
)
```

Calculate the average monthly interest charged per loan. Record in discovery notes:
- Sassafras: average $X/mo over Y months
- Park View: average $X/mo over Y months
- Hillside: average $X/mo over Y months

Validate Hillside ≈ $2,200/mo (the assumption). If significantly different (>±10%), flag and confirm with user before proceeding.

- [ ] **Step 1.5: Decide on Water sub-category**

Check whether the spreadsheet's two Greater Western Water lines warrant a new sub-category vs consolidating under Power. Default decision: **CREATE the Water sub-category** (clean separation, easier reporting). Record decision in discovery notes.

If creating Water, call:
```
mcp__pocketsmith__create_category(
  user_id=783484,
  title="Water",
  parent_id=31156994,
  colour="#5c87c1",
  refund_behaviour="credits_are_refunds"
)
```

Record the new category ID in discovery notes.

- [ ] **Step 1.6: Commit discovery artefacts**

```bash
git -C D:/PLAIOS add domains/finance/reference/_budget_dumps/2026-04-19-pre-rebuild-events.json domains/finance/reference/_budget_dumps/2026-04-19-discovery-notes.md
git -C D:/PLAIOS commit -m "PocketSmith budget rebuild: discovery artefacts (event snapshot, interest averages, scenario map)"
```

---

## Task 2: Wipe existing budget events

**Files:** No local file changes.

- [ ] **Step 2.1: Confirm proceed with destructive wipe**

Read back the discovery notes from Task 1. Confirm:
- Snapshot JSON exists and contains all events
- No events were flagged as manually edited (or any flagged ones have human approval to delete)

If anything is unclear, STOP and ask the user.

- [ ] **Step 2.2: Delete all existing budget events**

For each event in the snapshot JSON, call:
```
mcp__pocketsmith__delete_event(id="<event id from snapshot>", behaviour="all")
```

The `behaviour="all"` parameter deletes the entire recurring series, not just the single occurrence.

Track progress: log each deleted event ID. Expected count: ~31.

- [ ] **Step 2.3: Verify wipe complete**

Call:
```
mcp__pocketsmith__list_events(user_id=783484, start_date="2026-04-01", end_date="2026-05-31")
```

Expected: empty array (or near-empty — flag any unexpected leftovers and stop if found).

---

## Task 3: Create mortgage Interest events (one per property)

**Files:** No local file changes.

Use interest averages from Task 1.4. For each, the date should be 2026-05-01 (clean start of month for validation).

- [ ] **Step 3.1: Create Sassafras Interest event**

```
mcp__pocketsmith__create_event(
  scenario_id=<Sassafras loan account scenario id from Task 1.1>,
  category_id=31204939,  # Loan Interest
  date="2026-05-01",
  amount=-<Sassafras avg interest from Task 1.4>,
  repeat_type="monthly",
  repeat_interval=1,
  note="Sassafras Drive — interest portion of repayment (PPOR). Calibrated from 7-month avg."
)
```

Verify: event ID is returned. Record ID in execution log.

- [ ] **Step 3.2: Create Park View Interest event**

```
mcp__pocketsmith__create_event(
  scenario_id=<Park View loan account scenario id from Task 1.1>,
  category_id=31204939,  # Loan Interest
  date="2026-05-01",
  amount=-<Park View avg interest from Task 1.4>,
  repeat_type="monthly",
  repeat_interval=1,
  note="18 Park View Terrace, Sydenham — interest portion of repayment (investment). Calibrated from 7-month avg."
)
```

- [ ] **Step 3.3: Create Hillside Interest event**

```
mcp__pocketsmith__create_event(
  scenario_id=<Hillside loan account scenario id from Task 1.1>,
  category_id=31204939,  # Loan Interest
  date="2026-05-01",
  amount=-<Hillside avg interest from Task 1.4>,
  repeat_type="monthly",
  repeat_interval=1,
  note="Hillside (Celendine) — interest portion of repayment. Bank-mandated repayment funded by tenant rent."
)
```

---

## Task 4: Create mortgage Principal/Repayment events (transfers)

**Files:** No local file changes.

The principal events live on the SOURCE scenario (where the cash leaves), and use the `Loan Repayment` category (id `31156839`). Amount = total scheduled repayment − interest portion.

- [ ] **Step 4.1: Create Sassafras Principal event**

Calculate: principal = $3,822 − Sassafras interest (from Task 1.4). 

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id from Task 1.1>,
  category_id=31156839,  # Loan Repayment
  date="2026-05-01",
  amount=-<calculated principal>,
  repeat_type="monthly",
  repeat_interval=1,
  note="Sassafras Drive — principal portion of $3,822/mo repayment (PPOR)"
)
```

- [ ] **Step 4.2: Create Park View Principal event**

Calculate: principal = $2,552 − Park View interest.

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156839,  # Loan Repayment
  date="2026-05-01",
  amount=-<calculated principal>,
  repeat_type="monthly",
  repeat_interval=1,
  note="18 Park View Terrace, Sydenham — principal portion of $2,552/mo repayment (investment)"
)
```

- [ ] **Step 4.3: Create Hillside minimum Principal event**

Calculate: principal = $2,200 − Hillside interest.

The Hillside minimum repayment is sourced from the rental income flow (currently routed to Complete Access pending offset restructure). Use Complete Access scenario for now; relocate post-restructure.

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156839,  # Loan Repayment
  date="2026-05-01",
  amount=-<calculated principal>,
  repeat_type="monthly",
  repeat_interval=1,
  note="Hillside (Celendine) — principal portion of $2,200/mo minimum repayment (rent-funded). Relocate to offset post-restructure."
)
```

- [ ] **Step 4.4: Create Hillside extra Principal event**

The $800/mo extra is all principal (regular repayment already covers interest).

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156839,  # Loan Repayment
  date="2026-05-01",
  amount=-800,
  repeat_type="monthly",
  repeat_interval=1,
  note="Hillside (Celendine) — extra principal repayment ($800/mo on top of minimum, from operating cash)"
)
```

---

## Task 5: Create Education events

**Files:** No local file changes.

All on category `31156959` (Education). Source scenario: Complete Access (assume school fees and kids' activities debit from main operating account; adjust if discovery shows otherwise).

- [ ] **Step 5.1: Salesian College fees (Wulfric)**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156959,
  date="2026-07-15",
  amount=-2898,
  repeat_type="monthly",
  repeat_interval=3,
  note="Salesian College — Wulfric term fees ($11,590/yr / 4 terms)"
)
```

(`repeat_interval=3` with `repeat_type=monthly` = quarterly, which approximates termly cadence. PocketSmith does not have a "termly" repeat type.)

- [ ] **Step 5.2: Holy Trinity fees (Audrey & Evie)**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156959,
  date="2026-07-15",
  amount=-1005,
  repeat_type="monthly",
  repeat_interval=3,
  note="Holy Trinity — Audrey & Evie term fees ($4,020/yr / 4 terms)"
)
```

- [ ] **Step 5.3: Music Education Academy**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156959,
  date="2026-05-01",
  amount=-434,
  repeat_type="monthly",
  repeat_interval=1,
  note="Music Education Academy — Wulfric, Audrey, Evie monthly fee"
)
```

- [ ] **Step 5.4: Audrey basketball JETS**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156959,
  date="2026-05-01",
  amount=-61,
  repeat_type="monthly",
  repeat_interval=1,
  note="Audrey basketball JETS (rego — both summer and winter seasons annualised)"
)
```

- [ ] **Step 5.5: Evie basketball JETS**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156959,
  date="2026-05-01",
  amount=-61,
  repeat_type="monthly",
  repeat_interval=1,
  note="Evie basketball JETS"
)
```

- [ ] **Step 5.6: Wulfric Boxing/Jujitsu**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156959,
  date="2026-05-01",
  amount=-240,
  repeat_type="monthly",
  repeat_interval=1,
  note="Wulfric Boxing / Jujitsu (daily training as of mid-Apr 2026)"
)
```

- [ ] **Step 5.7: MIC Basketball training (Audrey)**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156959,
  date="2026-07-15",
  amount=-370,
  repeat_type="monthly",
  repeat_interval=3,
  note="MIC Basketball training — Audrey ($370/term × 4 terms/yr)"
)
```

- [ ] **Step 5.8: Salesian guitar (Wulfric)**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156959,
  date="2026-07-15",
  amount=-240,
  repeat_type="monthly",
  repeat_interval=3,
  note="Salesian guitar lessons — Wulfric ($240/term × 4 terms/yr)"
)
```

---

## Task 6: Create Childcare event

**Files:** No local file changes.

- [ ] **Step 6.1: Little Lane childcare (Penny)**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31172219,  # Child Care
  date="2026-05-01",
  amount=-764,
  repeat_type="monthly",
  repeat_interval=1,
  note="Little Lane childcare — Penny (4 days/week)"
)
```

---

## Task 7: Create Insurance events

**Files:** No local file changes.

All on category `31172234` (Insurance). All set as monthly placeholders — actual cadence (likely yearly for Budget Direct lines) gets corrected when next bill arrives. Pet insurance left as monthly.

- [ ] **Step 7.1: Medibank Private Health**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31172234,
  date="2026-05-01",
  amount=-252,
  repeat_type="monthly",
  repeat_interval=1,
  note="Medibank Private Health Insurance (monthly placeholder; switch to annual cadence at next renewal)"
)
```

- [ ] **Step 7.2: Budget Direct car**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31172234,
  date="2026-05-01",
  amount=-140,
  repeat_type="monthly",
  repeat_interval=1,
  note="Budget Direct — car insurance (monthly placeholder; likely yearly — confirm at next renewal)"
)
```

- [ ] **Step 7.3: Budget Direct Sassafras building**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31172234,
  date="2026-05-01",
  amount=-83,
  repeat_type="monthly",
  repeat_interval=1,
  note="Budget Direct — Sassafras Drive building insurance (monthly placeholder; likely yearly — confirm at renewal)"
)
```

- [ ] **Step 7.4: Budget Direct Park View building**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31172234,
  date="2026-05-01",
  amount=-70,
  repeat_type="monthly",
  repeat_interval=1,
  note="Budget Direct — 18 Park View Tce building insurance (monthly placeholder; likely yearly — confirm at renewal)"
)
```

- [ ] **Step 7.5: Pet insurance Titus**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31172234,
  date="2026-05-01",
  amount=-50,
  repeat_type="monthly",
  repeat_interval=1,
  note="Pet insurance — Titus"
)
```

---

## Task 8: Create Utilities events

**Files:** No local file changes.

Use the new Water category ID from Task 1.5 if created; otherwise fall back to Power (`31172214`).

- [ ] **Step 8.1: Greater Western Water — Park View**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=<Water id from Task 1.5, or 31172214 Power if not created>,
  date="2026-07-01",
  amount=-540,
  repeat_type="monthly",
  repeat_interval=3,
  note="Greater Western Water — 18 Park View Tce (quarterly bill)"
)
```

- [ ] **Step 8.2: Greater Western Water — Sassafras**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=<Water id, or 31172214>,
  date="2026-07-01",
  amount=-540,
  repeat_type="monthly",
  repeat_interval=3,
  note="Greater Western Water — Sassafras Drive (quarterly bill)"
)
```

- [ ] **Step 8.3: Momentum Energy — electricity**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31172214,  # Power
  date="2026-05-01",
  amount=-200,
  repeat_type="monthly",
  repeat_interval=1,
  note="Momentum Energy — electricity"
)
```

- [ ] **Step 8.4: Momentum Energy — gas**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31172214,  # Power
  date="2026-05-01",
  amount=-232,
  repeat_type="monthly",
  repeat_interval=1,
  note="Momentum Energy — gas"
)
```

- [ ] **Step 8.5: Wulfric mobile**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31172239,  # Phone
  date="2026-05-01",
  amount=-20,
  repeat_type="monthly",
  repeat_interval=1,
  note="Wulfric mobile phone"
)
```

- [ ] **Step 8.6: Mina mobile**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31172239,  # Phone
  date="2026-05-01",
  amount=-120,
  repeat_type="monthly",
  repeat_interval=1,
  note="Mina mobile phone"
)
```

---

## Task 9: Create Government Services events

**Files:** No local file changes.

All on category `31156989` (Government Services).

- [ ] **Step 9.1: VicRoads rego**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156989,
  date="2026-12-01",
  amount=-840,
  repeat_type="yearly",
  repeat_interval=1,
  note="VicRoads vehicle registration (date is a placeholder; correct to actual renewal date when known)"
)
```

- [ ] **Step 9.2: Brimbank Council rates (Park View)**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156989,
  date="2026-07-01",
  amount=-460,
  repeat_type="monthly",
  repeat_interval=3,
  note="Brimbank Council rates — 18 Park View Tce ($1,840/yr / 4 quarters)"
)
```

- [ ] **Step 9.3: Hume City Council rates (Sassafras)**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156989,
  date="2026-07-01",
  amount=-654,
  repeat_type="monthly",
  repeat_interval=3,
  note="Hume City Council rates — Sassafras Drive ($2,617/yr / 4 quarters)"
)
```

---

## Task 10: Create Groceries event

**Files:** No local file changes.

- [ ] **Step 10.1: Groceries**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156854,  # Groceries
  date="2026-05-01",
  amount=-1000,
  repeat_type="monthly",
  repeat_interval=1,
  note="Groceries (committed baseline; discretionary overspend handled separately)"
)
```

---

## Task 11: Create Harmoney event

**Files:** No local file changes.

The Harmoney loan account is offline in PocketSmith (cannot sync). The event lives on the source scenario (account ending 7233 from Task 1.1).

- [ ] **Step 11.1: Harmoney repayment**

```
mcp__pocketsmith__create_event(
  scenario_id=<Account-ending-7233 scenario id from Task 1.1>,
  category_id=31156839,  # Loan Repayment
  date="2026-04-24",
  amount=-165.55,
  repeat_type="fortnightly",
  repeat_interval=1,
  note="Harmoney personal loan (home renovation) — $165.55/fortnight, 7-yr term, 9.79% rate. Loan account offline in PocketSmith; balance manually tracked. Loan ID L00006085643."
)
```

---

## Task 12: Create Income events

**Files:** No local file changes.

All on Earnings parent. Note the income calibration caveat (3 months of clean post-restructure data needed before treating these as accurate).

- [ ] **Step 12.1: Scott salary**

```
mcp__pocketsmith__create_event(
  scenario_id=<Complete Access scenario id>,
  category_id=31156879,  # Income
  date="2026-05-01",
  amount=8000,
  repeat_type="monthly",
  repeat_interval=1,
  note="Scott salary (after tax). Calibrate from actuals after 3 clean months."
)
```

- [ ] **Step 12.2: Mina salary**

Identify Mina's pay landing account from Task 1.1 (likely Complete Access; confirm). Use that scenario.

```
mcp__pocketsmith__create_event(
  scenario_id=<Mina's pay landing scenario id>,
  category_id=31156879,  # Income
  date="2026-05-01",
  amount=5496,
  repeat_type="monthly",
  repeat_interval=1,
  note="Mina salary (after tax). Calibrate from actuals after 3 clean months."
)
```

- [ ] **Step 12.3: Park View rent (Sydenham)**

Identify Park View rental landing account from Task 1.1. Use that scenario.

```
mcp__pocketsmith__create_event(
  scenario_id=<Park View rent landing scenario id>,
  category_id=31172254,  # Rentals
  date="2026-05-01",
  amount=2040,
  repeat_type="monthly",
  repeat_interval=1,
  note="18 Park View Tce, Sydenham — rental income (net). Began Mar 2026 post-Harmoney renovation. Calibrate after 3 clean months."
)
```

- [ ] **Step 12.4: Hillside rent (Celendine)**

Identify Hillside rental landing account from Task 1.1. Use that scenario (could be Complete Access pre-restructure, or the loan account's offset post-restructure).

```
mcp__pocketsmith__create_event(
  scenario_id=<Hillside rent landing scenario id>,
  category_id=31172254,  # Rentals
  date="2026-05-01",
  amount=2200,
  repeat_type="monthly",
  repeat_interval=1,
  note="Hillside (Celendine Drive) — rental income from Rinoa + Sam + Mina's mum (combined). Began Mar 2026. Flows to loan/offset post-restructure. Calibrate after 3 clean months."
)
```

---

## Task 13: Verify event totals match expectations

**Files:** No local file changes.

- [ ] **Step 13.1: Pull live event list and tally**

```
mcp__pocketsmith__list_events(user_id=783484, start_date="2026-05-01", end_date="2026-05-31")
```

Manually sum the events by category group. Expected (approximate, ±5% for interest split unknowns):

| Category group | Expected May 2026 |
|---|---|
| Loan Interest (across 3 properties) | sum of avg interest from Task 1.4 |
| Loan Repayment (principal + Harmoney) | (3 × principal portions) + 800 + 359 (Harmoney monthly equiv) |
| Education | 956 (school fees one of three terms; Task 5 puts these termly so May won't have term hits) → expect just monthly items: 434 + 61 + 61 + 240 = $796 |
| Child Care | 764 |
| Insurance | 252 + 140 + 83 + 70 + 50 = 595 |
| Power + Water | 200 + 232 = 432 (water is quarterly, doesn't hit May) |
| Phone | 20 + 120 = 140 |
| Government Services | 0 in May (rego yearly Dec; rates quarterly Jul-aligned) |
| Groceries | 1000 |
| Income (Scott + Mina + 2 rents) | 8000 + 5496 + 2040 + 2200 = 17,736 |

Note: May 2026 is a "quiet month" — no termly school fees, no quarterly rates, no quarterly water. That's accurate cashflow modelling. Run a 12-month summary for full picture (Step 13.2).

- [ ] **Step 13.2: Pull annual budget summary for sanity check**

```
mcp__pocketsmith__get_budget_summary(
  user_id=783484,
  period="years",
  interval=1,
  start_date="2026-05-01",
  end_date="2027-04-30"
)
```

Expected annual totals (as a check on cadence math):
- Education: 2898 (Salesian termly) × 4 + 1005 (Holy Trinity termly) × 4 + 434 × 12 + 61 × 12 + 61 × 12 + 240 × 12 + 370 (MIC termly) × 4 + 240 (guitar termly) × 4 = `~27,604/yr`
- Insurance: 595 × 12 = `~7,140/yr`
- Power + Water: (200 + 232) × 12 + (540 + 540) × 4 = `~9,504/yr`
- Phone: 140 × 12 = `1,680/yr`
- Government Services: 840 + 1,840 + 2,617 = `5,297/yr`
- Groceries: 12,000/yr
- Childcare: 9,168/yr
- Harmoney: 165.55 × 26 = `4,304/yr`
- Mortgage cash-out (principal events): (Sassafras + Park View + Hillside-min principals) × 12 + 800 × 12 = roughly 20-40K depending on interest splits
- Mortgage interest: sum × 12 = ~120K (per ~$10K/mo interest assumption)
- Income: 17,736 × 12 = `212,832/yr`

If totals deviate >10% from expectations on a category line, investigate before continuing.

---

## Task 14: Write the budget mapping document

**Files:**
- Create: `domains/finance/reference/pocketsmith-budget-mapping.md`

- [ ] **Step 14.1: Create the mapping document**

Write `domains/finance/reference/pocketsmith-budget-mapping.md` with this structure:

```markdown
# PocketSmith Budget — Mapping & Provenance

**Last rebuilt:** 2026-04-19
**Source:** `mckennie-household-budget.xlsx` (sheet: 2026 Forecast v2)
**Design spec:** `docs/superpowers/specs/2026-04-19-pocketsmith-budget-design.md`
**Implementation plan:** `docs/superpowers/plans/2026-04-19-pocketsmith-budget-rebuild.md`

PocketSmith is now the source of truth for committed household cashflow. The spreadsheet is retained as historical input only.

## Mortgage events (per property)

For each property, two events:
- **Interest** event on the loan account scenario, category `Loan Interest` — economic cost of debt
- **Principal** event on the cash-source scenario, category `Loan Repayment` — cash leaving for debt reduction

| Property | Total repayment | Interest event ID | Interest amount | Principal event ID | Principal amount | Source scenario |
|---|---|---|---|---|---|---|
| Sassafras | $3,822/mo | <id> | <amount> | <id> | <amount> | Complete Access |
| Park View | $2,552/mo | <id> | <amount> | <id> | <amount> | Complete Access |
| Hillside (min) | $2,200/mo | <id> | <amount> | <id> | <amount> | Complete Access (pre-restructure) |
| Hillside (extra) | $800/mo | n/a | $0 | <id> | $800 | Complete Access |

Interest amounts derived from 7-month transaction history per loan (Task 1.4 of rebuild plan).

## Non-mortgage events

| Spreadsheet line | Category | Cadence | Amount | Event ID |
|---|---|---|---|---|
| Salesian College fees | Education | termly | $2,898 | <id> |
| Holy Trinity fees | Education | termly | $1,005 | <id> |
| Music Education Academy | Education | monthly | $434 | <id> |
| Audrey basketball JETS | Education | monthly | $61 | <id> |
| Evie basketball JETS | Education | monthly | $61 | <id> |
| Wulfric Boxing/Jujitsu | Education | monthly | $240 | <id> |
| MIC Basketball training | Education | termly | $370 | <id> |
| Salesian guitar | Education | termly | $240 | <id> |
| Little Lane childcare | Child Care | monthly | $764 | <id> |
| Medibank Private Health | Insurance | monthly* | $252 | <id> |
| Budget Direct car | Insurance | monthly* | $140 | <id> |
| Budget Direct Sassafras building | Insurance | monthly* | $83 | <id> |
| Budget Direct Park View building | Insurance | monthly* | $70 | <id> |
| Pet insurance Titus | Insurance | monthly | $50 | <id> |
| Greater Western Water (Park View) | Water | quarterly | $540 | <id> |
| Greater Western Water (Sassafras) | Water | quarterly | $540 | <id> |
| Momentum Energy electricity | Power | monthly | $200 | <id> |
| Momentum Energy gas | Power | monthly | $232 | <id> |
| Wulfric mobile | Phone | monthly | $20 | <id> |
| Mina mobile | Phone | monthly | $120 | <id> |
| VicRoads rego | Government Services | yearly | $840 | <id> |
| Brimbank Council rates (Park View) | Government Services | quarterly | $460 | <id> |
| Hume Council rates (Sassafras) | Government Services | quarterly | $654 | <id> |
| Groceries | Groceries | monthly | $1,000 | <id> |
| Harmoney loan repayment | Loan Repayment | fortnightly | $165.55 | <id> |
| Scott salary | Income | monthly | $8,000 | <id> |
| Mina salary | Income | monthly | $5,496 | <id> |
| Park View rent | Rentals | monthly | $2,040 | <id> |
| Hillside rent | Rentals | monthly | $2,200 | <id> |

*Insurance monthly placeholders — switch to actual yearly cadence and renewal date when next bill arrives.

## Deferred (not in PocketSmith yet)

- **Ambulance Victoria** — yearly amount unknown; create when next bill arrives
- **Land insurance** — yearly amount unknown; create when next bill arrives
- **Discretionary categories** (eating out, fuel, alcohol, entertainment, clothing, travel, gifts, kids one-offs) — separate Mina conversation, evidence-based after 3 months of post-rebuild actuals

## Recalibration triggers

- **Mortgage interest** — re-pull from history quarterly; offset balance changes will move interest down over time
- **Income (rents)** — recalibrate after 3 clean months of post-restructure data (target: 2026-08 review)
- **Insurance cadence** — switch each insurance line from monthly placeholder to actual yearly when its renewal hits
- **Council rates** — confirm exact quarterly billing dates at next bill
```

Fill in the actual event IDs from execution log of Tasks 3-12. Fill in interest/principal amounts from Task 1.4 calculations.

- [ ] **Step 14.2: Commit the mapping document**

```bash
git -C D:/PLAIOS add domains/finance/reference/pocketsmith-budget-mapping.md
git -C D:/PLAIOS commit -m "Add PocketSmith budget mapping document (post-rebuild canonical reference)"
```

---

## Task 15: Update finance state files

**Files:**
- Modify: `domains/finance/state/current-assessment.md`
- Modify: `domains/finance/state/active-priorities.md`

- [ ] **Step 15.1: Update L2.1 rating in current-assessment.md**

Open `domains/finance/state/current-assessment.md`. Find the `## L2.1 Financial Management` section. Update:

- **Rating:** `2 (Fragile) — improving` → `3 (Functional) — trending Systematic`
- **Trend:** `improving` → `improving`
- **Finding:** Replace existing finding text with:

```
PocketSmith rebuilt 2026-04-19 from spreadsheet (2026 Forecast v2). 31 default events wiped; ~30 hand-built events live, modelling mortgages as Interest (expense) + Principal (transfer) per property, lumpy items at actual cadence (school fees termly, council rates quarterly, water quarterly, rego yearly). Mapping document at `reference/pocketsmith-budget-mapping.md`. Spreadsheet retired as source of truth — kept as historical input only. Discretionary spending still excluded by design; conversation with Mina deferred to post-3-month actuals review (target: 2026-08).
```

Update `Last Updated:` to `2026-04-19` and `Next Review:` to `2026-07-19` (3-month post-rebuild check).

- [ ] **Step 15.2: Update active-priorities.md**

Open `domains/finance/state/active-priorities.md`. Move "Budget alignment PocketSmith ↔ household spreadsheet" from Queued to a new **Completed (this cycle)** section at the bottom. Add a new entry under Queued:

```
- **Discretionary baseline conversation with Mina** — after 3 months of post-rebuild actuals (target: 2026-08), pull a "spreadsheet vs actuals" diff per category, surface real discretionary spend with evidence, propose a discretionary budget structure for negotiation.
```

Also update:
- "Transaction backlog cleanup" remains Queued, unchanged
- "Budget forecast recalibration" — REMOVE (now obsolete; the rebuild handles this)
- "Mortgage repayments as transfers" — REMOVE (now done via Loan Repayment events)

- [ ] **Step 15.3: Commit state updates**

```bash
git -C D:/PLAIOS add domains/finance/state/current-assessment.md domains/finance/state/active-priorities.md
git -C D:/PLAIOS commit -m "Finance state: PocketSmith budget rebuilt; L2.1 to Functional; queue discretionary conversation"
```

---

## Task 16: Final verification

**Files:** No local file changes.

- [ ] **Step 16.1: One last live event sanity check**

```
mcp__pocketsmith__list_events(user_id=783484, start_date="2026-05-01", end_date="2026-05-31")
```

Confirm event count matches what we created in Tasks 3–12. Spot-check 3 random events have the correct note, amount, and category.

- [ ] **Step 16.2: Update memory if anything changed**

If discovery or execution surfaced anything that updates an existing memory file (e.g. Celendine rent source memory needs updating from "Rinoa only" to "Rinoa + Sam + Mina's mum"), update those memory files now per the auto-memory protocol.

- [ ] **Step 16.3: Report completion**

Report to user: total events created, total deleted, expected May 2026 cashflow summary, list of placeholder/deferred items still requiring follow-up, and the new finance state ratings.

---

## Out of scope (do NOT do as part of this plan)

- Backlog transaction categorisation (separate priority)
- Rent → offset restructure (user-led, separate)
- Discretionary category buildout (separate brainstorm post-3-month review)
- Touching the spreadsheet file itself (kept as historical reference only)
