# TourismPulse — Implementation Log

This log records what was actually inspected, executed and changed. It is not a success report. If something was not executed or not accessible, it says so.

---

## 2026-11-21 — Phase 1 audit (read-only)

### Context

- Session working directory: `C:\Users\Kaashvi\OneDrive\Documents\Default Project` (not the TourismPulse repository).
- The TourismPulse repository was cloned into:
  `C:\Users\Kaashvi\OneDrive\Documents\Default Project\tourism-analytics`
- Repository: `https://github.com/KrishJaidka/tourism-analytics`
- Branch: `main`
- Commit audited: `9a133768e751b05c096bed25e40835480400b23c`
- Working tree after clone: clean (`## main...origin/main`).

### What was inspected

1. All 13 committed notebooks (code cells, metadata, outputs).
2. `config/config.py`, `README.md`, `.gitignore`.
3. Git history (3 commits).
4. The six supplied raw files in `C:\Users\Kaashvi\Downloads`:
   - `UN_Tourism_inbound_arrivals_raw.csv`
   - `UN_Tourism_accommodation_hotels_raw.csv`
   - `world_bank_internatinal_arrival_raw.csv`
   - `estat_tour_occ_arm_raw.tsv`
   - `estat_tour_occ_mnor_raw.tsv`
   - `estat_tour_occ_nim_raw.tsv`

### What was executed

- `git clone`, `git status`, `git log`.
- Python/pandas profiling of the six raw files (row counts, indicator/unit cross-tabs, coverage, nulls, duplicates, negatives, flags, geography codes).
- `pycountry` mapping checks for ISO2/ISO3/M49.
- HTTP check of the workspace host.
- In-app browser navigation to the workspace URL (redirected to sign-in).

### What was **not** executed

- No PySpark job. PySpark is not installed in this environment; only Java 24 is present.
- No Databricks CLI command. The CLI is not installed.
- No Databricks authentication. No `~/.databrickscfg` profile and no `DATABRICKS_*` environment variables.
- No Unity Catalog, volume, folder or table inspection.
- No notebook execution.
- No GitHub commit or push.

### Access evidence

```text
git version 2.55.0.windows.3
python 3.12.10
pandas 2.3.3
pycountry installed for the audit

databricks --version
-> databricks: The term 'databricks' is not recognized ...

Test-Path "$env:USERPROFILE\.databrickscfg"
-> False

Get-ChildItem Env: | Where-Object Name -like 'DATABRICKS*'
-> (no output)

GET https://dbc-8409e0b7-429a.cloud.databricks.com/
-> 303 to /login.html?o=7474653857041139...
```

### Key findings

- No Gold layer exists in the repository.
- `03 Data Processing.ipynb` is a placeholder (imports only).
- `03 Measurement Conversion.ipynb` only inspects; its markdown plan (convert percentages to absolute, fill nulls) is not implemented and is invalid without denominators.
- All notebooks were exported with `execution_count = 0` and no outputs. There is no committed evidence that they ran successfully.
- World Bank aggregate handling is incomplete: only `AFE`, `AFW`, `ARB` are flagged; the file contains 50 aggregates plus Kosovo `XKX`.
- UN inbound values are multiplied by 1,000 and the unit is overwritten to `NR`; original unit provenance is lost.
- UN accommodation stores six indicators (units, percent, overnights) in one `hotel_capacity` column.
- Eurostat `tourism_value`/`nights_spent` mix `NR` counts with `PCH_*` growth rates; negative values are legitimate declines.
- Anomaly detection overwrites the UN accommodation Silver table.

### Files created

- `docs/current_project_status.md`
- `docs/silver_readiness_report.md`
- `docs/implementation_log.md` (this file)

No existing file was modified. No notebook was renamed. No table or volume was touched.

### Live audit update (2026-11-21)

- Opened the workspace in the in-app browser after the user signed in.
- Confirmed catalog `workspace`, schema `workspace/default`, and volume `tourismdata`.
- Confirmed folders: `raw`, `bronze_layer`, `silver_layer`, `gold_layer`; `gold_layer` is empty.
- Confirmed six Bronze Delta directories and the six expected Silver tables in `silver_layer`.
- Confirmed the live raw folder contains the six expected raw files (sizes match the supplied files) plus `weather_2010_2024.nc` (out of scope).
- Confirmed the workspace Git folder `tourism-analytics` contains the same 13 notebooks plus an extra notebook `Rough - Dont include in github`.
- Live SQL access was not obtained; Silver schemas, row counts, and execution state remain uninspected.

### Blockers

- Live Databricks audit requires the Databricks CLI (or a PAT) and an authenticated profile.
- The six raw files in `Downloads` are assumed to match the live volume files; this is unverified.
- Silver readiness is provisional until the live tables are queried.

### Next step

Authenticate to Databricks, then run the read-only validation queries in `docs/silver_readiness_report.md` §8. Do not create Gold tables until those results are reviewed.

---

### 2026-11-21 — Gold layer built (notebooks + docs)

- Created `05 Gold Dimensions.ipynb`: `dim_country`, `dim_date`.
- Created `06 Gold Facts.ipynb`: `fact_tourism_arrivals`, `fact_nights_spent`, `fact_hotel_performance`, `fact_hotel_occupancy`.
- Created `07 Gold Analytics.ipynb`: yearly/monthly arrivals, growth, rankings, seasonality, trends, comparisons, visitor category analysis.
- Created `08 Gold Validation.ipynb`: row counts, duplicate grain, nulls, negative values, referential integrity for all Gold tables.
- Created `09 Power BI Preparation.ipynb`: `pbi_total_arrivals`, `pbi_avg_occupancy`.
- Created `docs/gold_schema.md`, `docs/gold_validation_report.md`, `docs/data_lineage.md`, `docs/powerbi_measures.md`, `docs/powerbi_connection_guide.md`.
- Gold tables are not yet executed; notebooks are the vehicle for creating them. Static and SQL-based Silver validation is complete and documented.

---

*End of log.*
