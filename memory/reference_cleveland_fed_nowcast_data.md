---
name: cleveland-fed-nowcast-data
description: "Free, programmatic, vintage-correct macro consensus source (CPI/PCE nowcasts) — useful for any future macro-surprise study in trading-tools"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 095178a1-d2a3-43c0-a8f4-3d71a6cf15aa
---

Cleveland Fed Inflation Nowcasting = a free, reproducible source of macro
**consensus** (model-based) for CPI, core CPI, PCE, core PCE — MoM and YoY.
Found 2026-05-21 during the CPI-surprise study ([[project_trading_v3_scope_pending]]).

- **Endpoints** (need a `Mozilla/...` User-Agent; the HTML page 403s bots but the JSON files serve fine):
  `https://www.clevelandfed.org/-/media/files/webcharts/inflationnowcasting/nowcast_month.json` (MoM)
  and `.../nowcast_year.json` (YoY). Each is a FusionCharts JSON: a list of ~155 charts, one per reference month.
- **Why it's valuable:** each chart carries the *daily* nowcast evolution, so you can extract the
  **last pre-release vintage** = look-ahead-free consensus. It also carries the realized "Actual"
  series in definitionally-matched units (cross-checks exactly vs FRED NSA YoY).
- **History starts 2013-07** (the binding window constraint — NOT 2006).
- **FRED ALFRED** complements it for exact release dates: `series/observations?series_id=CPIAUCSL&output_type=4`
  (initial-release only) returns first-print value + its publication date in `realtime_start`. FRED key in
  `D:\Plaios-tools\trading-tools\.fred_api_key` (gitignored). Note: `realtime_end` must not be a future date — use `9999-12-31`.
- Working ingest reference: `D:\Plaios-tools\trading-tools\scripts\ingest_cpi.py`.
