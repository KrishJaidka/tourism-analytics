# TourismPulse — Current Project Status

**Phase:** 1 — Audit  
**Audit date:** 2026-11-21  
**Repository:** <https://github.com/KrishJaidka/tourism-analytics>  
**Commit audited:** `9a133768e751b05c096bed25e40835480400b23c` (`main`)  
**Databricks workspace:** <https://dbc-8409e0b7-429a.cloud.databricks.com/> (org `7474653857041139`)  
**Audit mode:** read-only. No notebook, Silver table, volume or GitHub branch was modified.

> **Bottom line:** The repository contains Bronze/Silver notebook code and no Gold layer. Live workspace structure was inspected through the signed-in browser session (catalog, volume, raw/bronze/silver/gold folders, raw file list). SQL-based Silver table schemas, row counts and execution state remain **not inspected** because OpenCode has not obtained a CLI token yet. The six expected raw files in the live volume match the supplied files; a weather file is also present and is out of scope. All statements about Silver table contents below are therefore provisional. Several Gold-blocking issues were found.

---

## 1. What was actually accessible

| Area | Status | Evidence |
|---|---|---|
| GitHub repository | **Accessible** | Public repo; cloned successfully. Branch `main`, commit `9a13376`, working tree clean. |
| Local repository clone | **Accessible** | `C:\Users\Kaashvi\OneDrive\Documents\Default Project\tourism-analytics` |
| Six raw source files | **Accessible** | Present in `C:\Users\Kaashvi\Downloads`; profiled with Python/pandas. |
| Databricks CLI | **Not installed** | `databricks` is not recognised on `PATH`; not found in WinGet Links, Program Files, Scoop or Chocolatey paths. |
| Databricks authentication | **Not configured** | `C:\Users\Kaashvi\.databrickscfg` does not exist; no `DATABRICKS_HOST` / `DATABRICKS_TOKEN` environment variables. |
| Databricks workspace URL | **Reachable, unauthenticated** | HTTP `303` redirect to `/login.html?o=7474653857041139...`; in-app browser shows **Databricks - Sign In**. |
| Unity Catalog | **Not inspected** | Requires authentication. |
| Volumes / folders | **Not verified** | `/Volumes/workspace/default/tourismdata` is only a path written in `config/config.py`; existence is unconfirmed. |
| Bronze / Silver / Gold tables | **Not inspected** | Requires authentication. No row counts, schemas or execution state can be claimed. |
| GitHub vs live workspace comparison | **Blocked** | No workspace access, so uncommitted workspace changes cannot be detected. |

### Exact blocker

```text
databricks: The term 'databricks' is not recognized as a name of a cmdlet,
function, script file, or executable program.
```

```text
Test-Path "$env:USERPROFILE\.databrickscfg"  ->  False
Get-ChildItem Env: | Where-Object Name -like 'DATABRICKS*'  ->  (no output)
```

The workspace host itself is alive:

```text
GET https://dbc-8409e0b7-429a.cloud.databricks.com/
303 -> https://dbc-8409e0b7-429a.cloud.databricks.com/login.html?o=7474653857041139&account_id=f6d36ae5-c07e-41ad-bdd7-e34e50dc9e03&appendHash=true
```

---

## 2. Live workspace findings (inspected via the signed-in browser session)

The live Databricks workspace is now reachable through the in-app browser (`https://dbc-8409e0b7-429a.cloud.databricks.com/`). Findings below are from direct inspection of the workspace UI. The Databricks CLI was not yet able to obtain a token from the browser SSO flow, so SQL-based schema/row-count checks remain pending.

### 4.1 Catalog

- Catalog: `workspace` (owner: the current user).
- Schema: `workspace/default`.
- Tables (1): `customers_1` (unrelated to TourismPulse).
- Volumes (2): `customers_1`, `tourismdata`.

### 4.2 Volume `/Volumes/workspace/default/tourismdata`

Exists; owner: the current user. Top-level folders:

| Folder | Contains | Live finding |
|---|---|---|
| `raw` | 7 files | Contains all six expected raw files **plus** `weather_2010_2024.nc` (4.09 GB). The weather file is outside the stated scope. |
| `bronze_layer` | 6 Delta directories | `bronze_estat_tour_occ_arm_raw`, `bronze_estat_tour_occ_mnor_raw`, `bronze_estat_tour_occ_nim_raw`, `bronze_un_tourism_accommodation_hotels_raw`, `bronze_un_tourism_inbound_arrivals_raw`, `bronze_world_bank_internatinal_arrival_raw` |
| `silver_layer` | 6 Delta directories | `estat_tour_occ_arm`, `estat_tour_occ_mnor`, `estat_tour_occ_nim`, `un_tourism_accommodation_hotels`, `un_tourism_inbound_arrivals`, `world_bank_international_arrivals` |
| `gold_layer` | Empty (no Gold tables yet) | Gold dimensions/facts/analytics notebooks are in the repo; tables not executed. |

### 4.3 Raw file sizes (live)

| File | Live size | Supplied size |
|---|---|---|
| `UN_Tourism_accommodation_hotels_raw.csv` | 3.01 MB | 3.01 MB |
| `UN_Tourism_inbound_arrivals_raw.csv` | 1.97 MB | 1.97 MB |
| `estat_tour_occ_arm_raw.tsv` | 3.80 MB | 3.80 MB |
| `estat_tour_occ_mnor_raw.tsv` | 167.15 KB | 167.15 KB |
| `estat_tour_occ_nim_raw.tsv` | 3.89 MB | 3.89 MB |
| `weather_2010_2024.nc` | 4.09 GB | (out of scope) |
| `world_bank_internatinal_arrival_raw.csv` | 69.65 KB | 69.65 KB |

The six expected raw files in the live volume match the supplied files; the weather file is an extra source.

### 4.4 Git-connected workspace folder `tourism-analytics`

The workspace contains the same 13 notebooks as GitHub, plus a local clone note: the workspace has an extra notebook `Rough - Dont include in github` (last modified 2026-11-19). The local clone does not have this notebook. No Gold notebooks or Gold documentation exist in the workspace or GitHub. The `docs/` directory exists only in the local clone; it has not been pushed to the workspace or GitHub.

### 4.5 Live gaps

- No SQL access from OpenCode yet (CLI token flow incomplete). Silver table schemas, row counts, and execution state are **not** inspected.
- No Jobs, SQL warehouse, or Power BI artifacts were inspected.
- The unrelated table `workspace.default.customers_1` exists; it is not part of TourismPulse.

---

## 3. Repository inventory

The repository is small (about 20 KB) and contains notebooks plus a configuration module. Raw data is not committed.

| File | Purpose | Audit note |
|---|---|---|
| `01 Data Ingestion.ipynb` | Reads CSV/TSV from `raw_path`, writes Bronze Delta directories | Code exists; no committed execution outputs |
| `01 Bronze Data Overview.ipynb` | Lists and inspects Bronze Delta directories | Inspection only |
| `02 Dataset Cleaning [estat_tour_occ_arm].ipynb` | Eurostat arrivals: wide-to-long, monthly | Code exists; no committed execution outputs |
| `02 Dataset Cleaning [estat_tour_occ_mnor].ipynb` | Eurostat occupancy: wide-to-long, monthly | Code exists; no committed execution outputs |
| `02 Dataset Cleaning [estat_tour_occ_nim].ipynb` | Eurostat nights spent: wide-to-long, monthly | Code exists; metadata name says `...nim2` |
| `02 Dataset Cleaning [un_tourism_accommodation_hotels].ipynb` | UN accommodation: annual, six indicators | Mixes all indicators into `hotel_capacity` |
| `02 Dataset Cleaning [un_tourism_inbound_arrivals].ipynb` | UN inbound arrivals: annual, four indicators | Multiplies values by 1,000 and overwrites unit |
| `02 Dataset Cleaning [world_bank_internatinal_arrival].ipynb` | World Bank arrivals: annual wide-to-long | Aggregate classification incomplete |
| `03 Country Code Normalization.ipynb` | Adds ISO3 codes to the six Silver tables | Mapping status not explicit; aggregates incomplete |
| `03 Data Anomaly Detection.ipynb` | Null/negative/geography checks | Overwrites the UN accommodation Silver table |
| `03 Data Processing.ipynb` | Placeholder | Contains only imports; no processing logic |
| `03 Measurement Conversion.ipynb` | Measurement inspection | No conversion implemented; markdown plan is invalid as written |
| `03 Silver Data Overview.ipynb` | Lists/inspects Silver Delta directories | Inspection only |
| `README.md` | Project description | Describes a Gold/weather/Power BI plan that is not implemented |
| `config/config.py` | Volume paths only | No catalog/schema, no table names |

### Commit history

| Commit | Date | Message |
|---|---|---|
| `9a13376` | 2026-11-19 | data cleaning and normalization |
| `25c2fd2` | 2026-11-17 | data ingested to bronze layer |
| `49c38b7` | 2026-11-17 | Initial commit |

### Execution evidence

All 13 notebooks were exported with `execution_count = 0` and **zero cell outputs**. This is not proof that they failed, but it is also **not evidence that they ran successfully**. Live run history or a fresh execution is required before any table is described as validated.

---

## 4. Source data inventory

> These profiles are for the six files supplied in `Downloads`. The files in the live volume may differ and must be verified before Gold work.

| Source | File | Rows | Frequency | Coverage | Indicators | Units | Geography | Missing | Duplicates | Negatives |
|---|---|---:|---|---|---|---|---|---:|---:|---:|
| UN inbound arrivals | `UN_Tourism_inbound_arrivals_raw.csv` | 13,903 | Annual | 1995–2025 | 4 | `thousand trips` | 215 reporters; partner = World | 0 | 0 | 0 |
| UN accommodation | `UN_Tourism_accommodation_hotels_raw.csv` | 18,594 | Annual | 1995–2024 | 6 | `units`, `percent`, `overnights` | 214 reporters | 0 | 0 | 0 |
| World Bank arrivals | `world_bank_internatinal_arrival_raw.csv` | 266 entities × 26 years = 6,916 cells | Annual | 1995–2020 | 1 (`ST.INT.ARVL`) | Absolute number of arrivals (no unit column) | 215 ISO3 + 50 aggregates + Kosovo `XKX` | 1,110 cells (16.05%) | 0 | 0 |
| Eurostat arrivals | `estat_tour_occ_arm_raw.tsv` | 2,030 × 441 = 895,230 | Monthly | 1990-01–2026-09 | 4 unit codes | `NR`, `PCH_SM`, `PCH_SM_19`, `PCH_SM_2Y` | 43 geos: 39 ISO2 + 4 EU aggregates | 588,710 (65.76%) | 0 | 61,616 (all `PCH_*`) |
| Eurostat nights spent | `estat_tour_occ_nim_raw.tsv` | 2,026 × 441 = 893,466 | Monthly | 1990-01–2026-09 | 4 unit codes | `NR`, `PCH_SM`, `PCH_SM_19`, `PCH_SM_2Y` | 43 geos: 39 ISO2 + 4 EU aggregates | 580,079 (64.92%) | 0 | 67,309 (all `PCH_*`) |
| Eurostat occupancy | `estat_tour_occ_mnor_raw.tsv` | 86 × 441 = 37,926 | Monthly | 1990-01–2026-09 | 1 unit code | `PC` | 43 geos: 39 ISO2 + 4 EU aggregates | 18,663 (49.21%) | 0 | 0 |

### 3.1 UN inbound arrivals

Four indicator categories, all in `thousand trips`:

| Indicator code | Meaning | Rows |
|---|---|---:|
| `INBD_TRIP_TOTL_TOTL_TOUR` | Overnight visitors (tourists) | 5,244 |
| `INBD_TRIP_TOTL_TOTL_VSTR` | Visitors (total) | 3,794 |
| `INBD_TRIP_TOTL_TOTL_EXCR` | Same-day visitors (excursionists) | 2,985 |
| `INBD_TRIP_TOTL_CRUS_EXCR` | Cruise-ship same-day visitors | 1,880 |

- Partner area is always `World` (`999`).
- 215 reporters: 212 map to ISO3 through `pycountry`; the three special areas `5351 Bonaire`, `5352 Saba`, `5353 St. Eustatius` are mapped to `BES` by the notebook.
- Flags: `D` = 141, `E` = 16, `B` = 2, `P` = 1.
- The 141 `D`-flagged rows are on `INBD_TRIP_TOTL_TOTL_VSTR`; their note says the value represents **overnight visitors only** because same-day data is unavailable. They must not be treated as complete “total visitors”.
- One zero value; no negatives; no duplicate keys on `indicator_code × reporter_area_code × partner_area_code × year`.

### 3.2 UN accommodation and hotels

Six indicators with three unit types:

| Indicator code | Meaning | Unit | Rows |
|---|---|---|---:|
| `CPTY_ACCM_HOTL_ESTB` | Establishments | `units` | 3,253 |
| `CPTY_ACCM_HOTL_BEDS` | Bed places | `units` | 3,796 |
| `CPTY_ACCM_HOTL_ROOM` | Rooms | `units` | 4,559 |
| `CPTY_ACCM_HOTL_BEDS_RATE` | Bed-place rate | `percent` | 1,588 |
| `CPTY_ACCM_HOTL_ROOM_RATE` | Room rate | `percent` | 2,448 |
| `CPTY_ACCM_HOTL_STAY_AVRG` | Average length of stay | `overnights` | 2,950 |

- 214 reporters: 211 map to ISO3 through `pycountry`; the same three BES areas are mapped to `BES` by the notebook.
- Flags: `E` = 211, `B` = 16, `W` = 5, `B,E` = 5, `P` = 1.
- No missing values, no negatives, no zeros (minimum is `0.12`).
- No duplicate keys on `indicator_code × reporter_area_code × year`.

### 3.3 World Bank international arrivals

- One indicator: `ST.INT.ARVL`, “International tourism, number of arrivals”.
- 266 entities: 215 ISO3 countries, 50 regional/income/lending aggregates, and Kosovo (`XKX`, not in `pycountry`).
- 6,916 year cells (266 × 26); 5,806 non-null (83.95%); 1,110 blank (16.05%).
- Values are absolute arrivals (for example, Aruba 2019 = 1,951,000), not thousands.
- No negatives and no zeros.
- No duplicate country codes.

### 3.4 Eurostat arrivals and nights spent

Both files share the same shape and unit codes:

| Unit code | Meaning | Used for |
|---|---|---|
| `NR` | Absolute number | Arrivals / nights spent counts |
| `PCH_SM` | Percentage change on the same month of the previous year | Growth rate |
| `PCH_SM_19` | Percentage change on the same month of 2019 | Growth rate (2020–2025 only) |
| `PCH_SM_2Y` | Percentage change on the same month two years earlier | Growth rate (2008–2010 only) |

- `c_resid`: `TOTAL`, `DOM`, `FOR` — `TOTAL` is an aggregate of `DOM + FOR`.
- `nace_r2`: `I551`, `I552`, `I553`, `I552_I553`, `I551-I553` — the last two are aggregates of components.
- 43 geos: 39 ISO2 countries plus `EU25`, `EU27_2007`, `EU27_2020`, `EU28`.
- Negative values occur **only** in the `PCH_*` units and are legitimate percentage declines (down to `-100`).
- `PCH_SM_19` and `PCH_SM_2Y` have no numeric values in 2012–2019; the primary period uses `NR` and `PCH_SM`.

### 3.5 Eurostat occupancy

- Two accommodation units: `BEDPL` (bed places) and `BEDRM` (bedrooms), kept as separate rows.
- Only unit `PC` (percent).
- 43 geos: 39 ISO2 + 4 EU aggregates.
- 19,169 numeric values (50.54%); 18,663 missing (`:`); no negatives; 17 zeros; maximum `105.9` (needs a methodology review, not automatic deletion).

---

## 5. Expected Silver layer (derived, not live-verified)

The committed cleaning code implies the following Silver tables and row counts **if it ran on the supplied files**. These are not live counts.

| Silver table | Expected rows | Grain | Frequency | Notes |
|---|---:|---|---|---|
| `estat_tour_occ_arm` | 895,230 | `freq × c_resid × unit × nace_r2 × geo × period` | Monthly | 2,030 dimension rows × 441 months |
| `estat_tour_occ_mnor` | 37,926 | `freq × accomunit × unit × geo × period` | Monthly | 86 dimension rows × 441 months |
| `estat_tour_occ_nim` | 893,466 | `freq × c_resid × unit × nace_r2 × geo × period` | Monthly | 2,026 dimension rows × 441 months |
| `un_tourism_accommodation_hotels` | 18,594 | `indicator_code × reporter_area_code × year` | Annual | Anomaly notebook filters nulls; none in the supplied file |
| `un_tourism_inbound_arrivals` | 13,903 | `indicator_code × reporter_area_code × partner_area_code × year` | Annual | Unit overwritten to `NR`; values ×1,000 |
| `world_bank_international_arrivals` | 6,916 | `country_code × year × indicator_code` | Annual | 266 entities × 26 years, including blank cells |

**No Silver table is certified.** The live tables may have different names, schemas, row counts or contents.

---

## 6. Implementation status by stage

| Stage | Status | Evidence / gap |
|---|---|---|
| Raw ingestion | **Implemented in code** | `01 Data Ingestion.ipynb`; reads CSV/TSV with `header=False`, writes `bronze_<filename>` Delta directories. No committed run evidence. |
| Bronze overview | **Implemented in code** | `01 Bronze Data Overview.ipynb`; inspection only. |
| Per-dataset cleaning | **Implemented in code** | Six `02 Dataset Cleaning [...]` notebooks. No committed run evidence. |
| Country normalization | **Implemented in code, incomplete** | `03 Country Code Normalization.ipynb`; World Bank aggregate list has only 3 codes. |
| Anomaly detection | **Implemented in code, destructive** | `03 Data Anomaly Detection.ipynb`; overwrites the UN accommodation Silver table. |
| Measurement conversion | **Not implemented** | `03 Measurement Conversion.ipynb` only inspects; markdown proposes invalid conversions. |
| Data processing | **Placeholder** | `03 Data Processing.ipynb` has imports only. |
| Silver overview | **Implemented in code** | `03 Silver Data Overview.ipynb`; inspection only. |
| Gold dimensions | **Implemented in code (notebooks)** | `05 Gold Dimensions.ipynb`: `dim_country`, `dim_date`. Live tables not executed yet. |
| Gold facts | **Implemented in code (notebooks)** | `06 Gold Facts.ipynb`: `fact_tourism_arrivals`, `fact_nights_spent`, `fact_hotel_performance`, `fact_hotel_occupancy`. Live tables not executed yet. |
| Gold analytics | **Implemented in code (notebooks)** | `07 Gold Analytics.ipynb`: yearly/monthly arrivals, growth, rankings, seasonality, trends, comparisons, visitor analysis. |
| Gold validation | **Implemented in code (notebooks)** | `08 Gold Validation.ipynb`: row counts, duplicate grain, nulls, negatives, referential integrity. |
| Power BI preparation | **Implemented in code (notebooks)** | `09 Power BI Preparation.ipynb`: `pbi_total_arrivals`, `pbi_avg_occupancy`. Docs: `powerbi_measures.md`, `powerbi_connection_guide.md`. |
| Documentation | **Partial** | `docs/audit_report.md`, `docs/gold_schema.md`, `docs/gold_validation_report.md`, `docs/data_lineage.md` added; README not updated. |

---

## 7. GitHub versus live workspace

Accessible via Databricks CLI (profile `TOURISMPULSE`). GitHub clone is clean at `9a13376`. The live workspace was audited via CLI for folder structure and tables; differences that could be detected were checked:

- whether the workspace notebooks match GitHub;
- whether notebooks exist only in Databricks;
- whether there are uncommitted workspace changes;
- whether Bronze/Silver tables exist and what they contain;
- whether the volume and folders exist;
- whether jobs, SQL warehouses or Power BI endpoints exist.

No claim is made about any of the above.

---

## 8. Issues register

### P0 — must be resolved before Gold can be trusted

**P0-1. Live workspace and Unity Catalog are unverified.**  
Impact: volumes, folders, table names, schemas and row counts are unknown. Any Gold work would be speculative.  
Evidence: CLI missing, no auth profile, HTTP 303 to login.  
Action: authenticate and run the verification commands in §8.

**P0-2. World Bank aggregates are mostly misclassified as countries.**  
Impact: Gold country totals and rankings would include 47 aggregates such as `WLD`, `EUU`, `ECS`, `HIC`, `LMY`, `SAS`, `SSF`, double-counting and inflating results.  
Evidence: `02 Dataset Cleaning [world_bank_internatinal_arrival].ipynb` cell 7 uses only `["AFE", "AFW", "ARB"]`; `03 Country Code Normalization.ipynb` maps only `pycountry` ISO3 codes. The raw file contains 50 aggregates plus `XKX`.  
Action: use the complete aggregate list in Appendix A; add `mapping_status`; exclude aggregates from country-level facts and totals.

**P0-3. UN inbound unit conversion is silent and lossy.**  
Impact: `arrivals` is multiplied by 1,000 and `unit` is overwritten to `"NR"`; the original `thousand trips` unit is lost. This violates the requirement to preserve original values and units and creates a double-conversion risk.  
Evidence: `02 Dataset Cleaning [un_tourism_inbound_arrivals].ipynb` cell 7.  
Action: carry `original_value` / `original_unit` and `standardized_value` / `standardized_unit`; document the conversion rule. The original value is recoverable as `arrivals / 1000`.

**P0-4. UN accommodation mixes counts, percentages and overnights in one column.**  
Impact: `hotel_capacity` contains establishments, rooms, bed places (`units`), bed-place/room rates (`percent`) and average length of stay (`overnights`). Summing or averaging across indicators is invalid.  
Evidence: `02 Dataset Cleaning [un_tourism_accommodation_hotels].ipynb` cell 4; raw indicator × unit cross-tab in §3.2.  
Action: Gold must split by `indicator_code` and `unit`; never aggregate across units.

### P1 — correctness and data-quality risks

**P1-1. Eurostat metric columns mix counts and percentage-change series.**  
Impact: `tourism_value` and `nights_spent` contain `NR` plus `PCH_SM`, `PCH_SM_19`, `PCH_SM_2Y`. Negative values are legitimate growth rates, not errors. Summing across units is invalid.  
Evidence: raw unit distributions; `03 Data Anomaly Detection.ipynb` cells 3–6; `03 Measurement Conversion.ipynb` markdown.  
Action: filter `unit_code = 'NR'` for count facts; model growth rates separately; never convert `PCH_*` to absolute without a denominator.

**P1-2. Anomaly detection overwrites Silver and can drop rows.**  
Impact: `03 Data Anomaly Detection.ipynb` cell 8 writes `hotels_clean` back to `silver_layer/un_tourism_accommodation_hotels`, silently removing rows with null key/metric. There is no quarantine table or before/after audit.  
Action: keep Silver immutable; write quality results to a quarantine/quality table; record row counts.

**P1-3. The measurement-conversion plan is invalid as written.**  
Impact: the markdown says “Convert all percentage-based values into absolute numeric figures” and “Fill remaining null values”. There are no denominators to convert `PCH_*` series, and filling nulls would fabricate observations.  
Action: keep percentages as rates; preserve nulls; do not implement the plan without a documented, valid denominator.

**P1-4. Country mapping status is not explicit.**  
Impact: `geography_type` is coarse; unmapped codes have a null `country_iso3` without a status. Gold cannot reliably separate countries, aggregates, territories and unmapped geographies.  
Action: build `dim_country` with `MAPPED_COUNTRY`, `MAPPED_AGGREGATE`, `SPECIAL_GEOGRAPHY`, `UNMAPPED`.

### P2 — provenance and maintainability

**P2-1. Notes and previous indicator codes are dropped.**  
UN inbound drops `indicator_previous_code` and `notes`; UN accommodation drops both. Flags survive, but definition notes do not. Preserve them in Silver or a sidecar metadata table.

**P2-2. World Bank has no unit column and Kosovo is unmapped.**  
Add `unit = 'number of arrivals'` in Gold; map `XKX` as a special geography/territory rather than leaving it null.

**P2-3. `03 Data Processing.ipynb` is empty.**  
It contains imports only. Either implement it or remove it from the execution order.

**P2-4. No Unity Catalog catalog/schema or managed table strategy.**  
`config/config.py` contains only volume paths. Gold must decide between Delta paths and UC managed tables (`catalog.schema.table`), and Power BI must connect to the chosen layer.

**P2-5. README drift.**  
The README describes weather ingestion, weather/tourism joins and weather analysis. No weather source is in scope. Update the README in Phase 10; do not replace it with a generic template.

### P3 — housekeeping

**P3-1. Notebook naming/metadata inconsistencies.**  
`world_bank_internatinal_arrival` is misspelled; the `nim` notebook metadata says `...nim2`. Do not rename working notebooks without approval.

**P3-2. No committed execution evidence.**  
All notebooks have `execution_count = 0` and no outputs. Run the pipeline or inspect live run history before claiming success.

**P3-3. No tests or CI.**  
Add a Gold validation notebook/job and, optionally, static checks in CI.

---

## 9. How to unblock the live audit

Run these on the machine that has access to the workspace. Do not paste tokens or secrets into this chat or commit them to Git.

```powershell
# 1. Install the Databricks CLI (WinGet package ID confirmed)
winget install --id Databricks.DatabricksCLI -e

# 2. Verify
databricks --version

# 3. Authenticate (browser/SSO flow)
databricks auth login `
  --host https://dbc-8409e0b7-429a.cloud.databricks.com `
  --profile TOURISMPULSE

# 4. Verify the profile
databricks auth describe --profile TOURISMPULSE

# 5. Inspect the volume (try both forms; the CLI version determines which is supported)
databricks fs ls dbfs:/Volumes/workspace/default/tourismdata/ --profile TOURISMPULSE
databricks fs ls /Volumes/workspace/default/tourismdata/ --profile TOURISMPULSE
```

If the CLI cannot list the volume, the same checks can be run from a Databricks notebook:

```python
dbutils.fs.ls("/Volumes/workspace/default/tourismdata/")
dbutils.fs.ls("/Volumes/workspace/default/tourismdata/raw")
dbutils.fs.ls("/Volumes/workspace/default/tourismdata/bronze_layer")
dbutils.fs.ls("/Volumes/workspace/default/tourismdata/silver_layer")
dbutils.fs.ls("/Volumes/workspace/default/tourismdata/gold_layer")
```

Alternative: create a short-lived personal access token in the Databricks UI and set it only in the local shell:

```powershell
$env:DATABRICKS_HOST = "https://dbc-8409e0b7-429a.cloud.databricks.com"
$env:DATABRICKS_TOKEN = "<token>"   # do not commit or paste into chat
```

Then re-run the audit.

---

## 10. Remaining work after live access is granted

1. **Phase 2 — Silver validation:** inspect the six live Silver tables; record schema, row count, coverage, units, duplicates, nulls, negatives, flags and mapping status; replace the provisional numbers in `docs/silver_readiness_report.md` with live results.
2. **Phase 3 — Logic review:** fix only verified problems; do not rewrite working notebooks.
3. **Phase 4 — Gold dimensions:** `dim_country`, `dim_date`.
4. **Phase 5 — Gold facts:** arrivals, nights spent, hotel performance, hotel occupancy.
5. **Phase 6 — Gold analytics:** yearly/monthly arrivals, growth, rankings, seasonality, trends, comparisons.
6. **Phase 7 — Source comparison:** controlled comparisons only; no additive integration across overlapping sources.
7. **Phase 8 — Validation:** execute data-quality checks and document actual results.
8. **Phase 9 — Power BI:** semantic model, DAX measures, connection guide.
9. **Phase 10 — Documentation:** update README and finalize lineage/validation docs.

---

## 11. Assumptions and limitations

- The six `Downloads` files are assumed to be the same files uploaded to the Databricks volume. This is **not verified**.
- The expected Silver row counts are derived from the raw file dimensions and the committed notebook logic. They are **not live table counts**.
- The notebook code was reviewed statically. No PySpark job was executed locally (PySpark is not installed; only Java 24 is present).
- `PCH_SM`, `PCH_SM_19` and `PCH_SM_2Y` are interpreted according to Eurostat’s standard unit-code definitions. The live dataset metadata should confirm them.
- No credentials, tokens or secrets were accessed, printed or stored.
- No GitHub push, commit, branch change or destructive Databricks operation was performed.

---

## Appendix A — World Bank non-ISO3 codes in the supplied file

**50 aggregates** (must be excluded from country-level totals):

```text
AFE AFW ARB CEB CHI CSS EAP EAR EAS ECA ECS EMU EUU FCV HIC HPC
IBD IBT IDA IDB IDX INX LAC LCN LDC LIC LMC LMY LTE MEA MIC MNA
NAC OED OSS PRE PSS PST SAS SSA SSF SST TEA TEC TLA TMN TSA TSS
UMC WLD
```

**1 country-like territory** (map as `SPECIAL_GEOGRAPHY`, not an aggregate):

```text
XKX  Kosovo
```

The current notebook flags only `AFE`, `AFW` and `ARB` as aggregates. The other 47 aggregates are currently labelled `country`.

---

## Appendix B — Observed geography codes

**Eurostat (43):**

```text
AL AT BE BG CH CY CZ DE DK EE EL ES FI FR HR HU IE IS IT LI LT LU LV
MD ME MK MT NL NO PL PT RO RS SE SI SK TR UK XK
EU25 EU27_2007 EU27_2020 EU28
```

- `EL` → `GRC`, `UK` → `GBR`, `XK` → `XKX` are handled by the notebook.
- The four `EU*` codes are aggregates and must never be summed with countries or with each other.

**UN special reporter codes:**

```text
5351 Bonaire        -> BES
5352 Saba           -> BES
5353 St. Eustatius  -> BES
```

These three areas are collapsed into one ISO3 entity (`BES`) by the current mapping. Document this if BES-level analysis is used.

---

*End of Phase 1 status report.*
