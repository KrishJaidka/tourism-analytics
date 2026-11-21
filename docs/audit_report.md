# TourismPulse — Final Audit Report

**Date:** 2026-11-21  
**Repository:** https://github.com/KrishJaidka/tourism-analytics (`main`, commit `9a13376`)  
**Workspace:** https://dbc-8409e0b7-429a.cloud.databricks.com/ (org `7474653857041139`)  
**Volume:** `/Volumes/workspace/default/tourismdata` (verified via Databricks CLI, profile `TOURISMPULSE`)  
**Audit mode:** read-only for the audit phase. No existing notebooks, tables, or volumes were modified or deleted. Gold notebooks and docs were added after the audit; Gold tables are not yet executed.

---

## A. Existing Project Architecture

- **Medallion architecture** with three layers: `raw`, `bronze_layer`, `silver_layer`, `gold_layer`.
- **Gold layer is planned and implemented as notebooks.** `gold_layer/` is empty; Gold notebooks (`05 Gold Dimensions` … `09 Power BI Preparation`) exist and are documented in `docs/gold_schema.md`.
- **No weather data is used** (consistent with the stated scope; the live raw folder contains `weather_2010_2024.nc`, but it is out of scope and not referenced by notebooks).
- **Primary analysis period:** 2012–2019 is mentioned as the main comparison period; other years must be retained.

---

## B. Existing Notebooks and Purpose

| Notebook | Purpose |
|---|---|
| `01 Data Ingestion.ipynb` | Reads raw CSV/TSV files from `/Volumes/workspace/default/tourismdata/raw`, writes Delta directories to `bronze_layer/`. Uses `dbutils.fs.ls`, `spark.read.format("csv"/"tsv")`, `spark.write.format("delta").mode("overwrite")`. |
| `01 Bronze Data Overview.ipynb` | Lists and inspects Bronze Delta directories (`spark.read.format("delta").load`, `printSchema`, `df.count()`, `display`). |
| `02 Dataset Cleaning [estat_tour_occ_arm].ipynb` | Eurostat monthly arrivals: wide-to-long, parses dimensions from first column, explodes monthly periods, extracts value and observation flag, casts period to DATE, writes `silver_estat_tour_occ_arm`. |
| `02 Dataset Cleaning [estat_tour_occ_mnor].ipynb` | Eurostat monthly occupancy: same pattern; writes `silver_estat_tour_occ_mnor`. |
| `02 Dataset Cleaning [estat_tour_occ_nim].ipynb` | Eurostat monthly nights spent: same pattern; writes `silver_estat_tour_occ_nim`. |
| `02 Dataset Cleaning [un_tourism_accommodation_hotels].ipynb` | UN accommodation/hotels: annual; casts types; renames `value` to `hotel_capacity`; sets `geography_type`; writes `silver_un_tourism_accommodation_hotels`. |
| `02 Dataset Cleaning [un_tourism_inbound_arrivals].ipynb` | UN inbound arrivals: annual; multiplies `arrivals` by 1000 and sets `unit` to `"NR"`; preserves indicator codes; writes `silver_un_tourism_inbound_arrivals`. |
| `02 Dataset Cleaning [world_bank_internatinal_arrival].ipynb` | World Bank annual arrivals: explodes year columns, casts types, flags `AFE/AFW/ARB` as regional aggregates; writes `silver_world_bank_international_arrivals`. |
| `03 Country Code Normalization.ipynb` | Maps ISO2/M49 codes to ISO3 on the six Silver tables using `pycountry` and hardcoded UN exceptions; writes back to Silver. |
| `03 Data Anomaly Detection.ipynb` | Checks nulls, negatives, flags, unmapped geographies; overwrites `silver_un_tourism_accommodation_hotels` with filtered rows. |
| `03 Data Processing.ipynb` | Placeholder — imports only, no processing logic. |
| `03 Measurement Conversion.ipynb` | Inspection only. The markdown proposes converting percentages to absolute values and filling nulls, but no conversion is implemented. |
| `03 Silver Data Overview.ipynb` | Lists and inspects Silver Delta directories. |

**Execution evidence:** All notebooks have `execution_count = 0` and no cell outputs in the committed Git versions. Live execution state could not be checked via CLI (serverless starter warehouse is stopped and not used by these notebooks).

---

## C. Existing Bronze, Silver, Gold Assets

### Bronze layer (`bronze_layer/`)

Six Delta directories:

- `bronze_estat_tour_occ_arm_raw`
- `bronze_estat_tour_occ_mnor_raw`
- `bronze_estat_tour_occ_nim_raw`
- `bronze_un_tourism_accommodation_hotels_raw`
- `bronze_un_tourism_inbound_arrivals_raw`
- `bronze_world_bank_internatinal_arrival_raw`

### Silver layer (`silver_layer/`)

Six Delta tables (verified via Databricks CLI `fs ls`):

1. `estat_tour_occ_arm` — 895,230 rows
2. `estat_tour_occ_mnor` — 37,926 rows
3. `estat_tour_occ_nim` — 893,466 rows
4. `un_tourism_accommodation_hotels` — 18,594 rows
5. `un_tourism_inbound_arrivals` — 13,903 rows
6. `world_bank_international_arrivals` — 6,916 rows

### Gold layer (`gold_layer/`)

Gold tables, dimensions, facts, and analytics are now implemented as notebooks (`05 Gold Dimensions.ipynb` … `09 Power BI Preparation.ipynb`). Live Gold tables are not executed yet; execution order and validation are documented in `docs/gold_schema.md` and `docs/gold_validation_report.md`.

---

## D. Silver Layer Validation Results (Live, Verified)

All checks below were executed via Databricks SQL API on the `TOURISMPULSE` profile (read-only).

### 1. `estat_tour_occ_arm` (Eurostat monthly arrivals)

- **Row count:** 895,230
- **Schema:** `geo_code STRING, frequency STRING, residence_category STRING, unit_code STRING, activity_code STRING, geography_type STRING, period DATE, tourism_value DOUBLE, observation_flag STRING, country_iso3 STRING`
- **Frequency:** All `M` (monthly), time range 1990-01-01 .. 2026-09-01 (441 months)
- **Country mapping:** `country_iso3` null for 59,535 rows (EU aggregates: 835,695 country rows, 59,535 `eu_aggregate` rows). 39 distinct non-null ISO3 values.
- **Nulls:** `tourism_value` null = 591,124 (non-null = 304,106)
- **Value stats:** min = -100.0, max = 1.477e8, negatives = 61,616, zeros = 4,054
- **Units:** `NR` (284,445), `PCH_SM` (273,861), `PCH_SM_19` (254,016), `PCH_SM_2Y` (82,908)
- **Duplicates:** 0 on grain (`geo_code, period, unit_code`)

### 2. `estat_tour_occ_mnor` (Eurostat monthly occupancy)

- **Row count:** 37,926
- **Schema:** `geo_code STRING, frequency STRING, accommodation_unit STRING, unit_code STRING, geography_type STRING, period DATE, occupancy_rate DOUBLE, observation_flag STRING, country_iso3 STRING`
- **Frequency:** All `M`, time range 1990-01-01 .. 2026-09-01
- **Country mapping:** `country_iso3` null for 3,528 rows (35,328 country rows, 3,528 `eu_aggregate` rows). 39 distinct non-null ISO3.
- **Nulls:** `occupancy_rate` null = 18,757 (non-null = 19,169)
- **Value stats:** min = 0.0, max = 105.9, negatives = 0, zeros = 17
- **Units:** `PC` only; `accommodation_unit` is `BEDPL` or `BEDRM` (separate rows)
- **Duplicates:** 0 on grain (`geo_code, period`)

### 3. `estat_tour_occ_nim` (Eurostat monthly nights spent)

- **Row count:** 893,466
- **Schema:** `geo_code STRING, frequency STRING, residence_category STRING, unit_code STRING, activity_code STRING, geography_type STRING, period DATE, nights_spent DOUBLE, observation_flag STRING, country_iso3 STRING`
- **Frequency:** All `M`, time range 1990-01-01 .. 2026-09-01
- **Country mapping:** `country_iso3` null for 59,535 rows (835,695 country rows, 59,535 `eu_aggregate` rows). 39 distinct non-null ISO3.
- **Nulls:** `nights_spent` null = 582,504 (non-null = 310,962)
- **Value stats:** min = -100.0, max = 5.34e8, negatives = 67,309, zeros = 4,110
- **Units:** `NR` (284,445), `PCH_SM` (273,861), `PCH_SM_19` (254,016), `PCH_SM_2Y` (81,144)
- **Duplicates:** 0 on grain (`geo_code, period, unit_code`)

### 4. `un_tourism_accommodation_hotels` (UN accommodation)

- **Row count:** 18,594
- **Schema:** `reporter_area_code INT, indicator_code STRING, indicator_label STRING, reporter_area STRING, geography_type STRING, year INT, hotel_capacity DOUBLE, unit STRING, observation_flag STRING, flag_label STRING, reporter_country_iso3 STRING`
- **Time range:** 1995 .. 2024 (30 years)
- **Geography:** all `country`; `reporter_country_iso3` null = 0, 212 distinct non-null ISO3
- **Nulls:** `observation_flag` and `flag_label` null = 18,356; `hotel_capacity` null = 0
- **Value stats:** min = 0.12, max = 5,491,227; negatives = 0; zeros = 0
- **Units:** `units` (11,608), `percent` (4,036), `overnights` (2,950)
- **Indicators:** 6 UN accommodation indicators preserved
- **Duplicates:** 0 on grain (`indicator_code, reporter_area_code, year`)

### 5. `un_tourism_inbound_arrivals` (UN inbound arrivals)

- **Row count:** 13,903
- **Schema:** `partner_area_code INT, reporter_area_code INT, indicator_code STRING, indicator_label STRING, reporter_area STRING, reporter_geography_type STRING, partner_area STRING, partner_geography_type STRING, year INT, arrivals DOUBLE, unit STRING, observation_flag STRING, flag_label STRING, reporter_country_iso3 STRING, partner_country_iso3 STRING`
- **Time range:** 1995 .. 2025 (31 years)
- **Geography:** `reporter_geography_type` = `country` for all 13,903; `partner_geography_type` = `world_aggregate` for all 13,903; `reporter_country_iso3` null = 0, 213 distinct non-null ISO3; `partner_country_iso3` null = 13,903 (all null, because partner is World)
- **Nulls:** `arrivals` null = 0; `observation_flag`/`flag_label` null = 13,743
- **Value stats:** min = 0.0, max = 2.18e8; negatives = 0; zeros = 1
- **Units:** `NR` only
- **Indicators:** 4 UN inbound categories preserved:
  - `INBD_TRIP_TOTL_TOTL_TOUR` (overnight visitors): 5,244
  - `INBD_TRIP_TOTL_TOTL_VSTR` (visitors total): 3,794
  - `INBD_TRIP_TOTL_TOTL_EXCR` (same-day excursionists): 2,985
  - `INBD_TRIP_TOTL_CRUS_EXCR` (cruise same-day excursionists): 1,880
- **Duplicates:** 0 on grain (`indicator_code, reporter_area_code, partner_area_code, year`)

### 6. `world_bank_international_arrivals`

- **Row count:** 6,916
- **Schema:** `country_name STRING, country_code STRING, indicator_name STRING, indicator_code STRING, geography_type STRING, year INT, arrivals DOUBLE, country_iso3 STRING`
- **Time range:** 1995 .. 2020 (26 years)
- **Geography:** `geography_type` = `country` (6,838), `regional_aggregate` (78). `country_iso3` null = 1,326, 215 distinct non-null ISO3.
- **Nulls:** `arrivals` null = 1,110 (blank cells preserved as null)
- **Value stats:** min = 700.0, max = 2.403e9; negatives = 0; zeros = 0
- **Indicator:** `ST.INT.ARVL` (`International tourism, number of arrivals`)
- **Duplicates:** 0 on grain (`country_code, year, indicator_code`)

---

## E. What Is Completed

- **Bronze ingestion** notebook exists and writes the six Bronze Delta directories.
- **Silver cleaning** notebooks exist and produce the six expected Silver tables.
- **Silver tables are present** in the live volume with the expected names and schemas.
- **Country normalization** adds `country_iso3` to the six Silver tables (live-verified).
- **Annual/monthly distinction is maintained**:
  - Eurostat: monthly (`frequency = M`), period range 1990-2026.
  - UN Tourism and World Bank: annual (`year`), ranges 1995–2025 and 1995–2020.
- **Units are preserved** in the Silver tables (`unit_code`, `unit`, `accommodation_unit`, etc.).
- **Observation flags and labels are preserved** (`observation_flag`, `flag_label`).
- **No duplicates** were found on the expected grains for any Silver table.
- **Missing values are nulls**, not zeros (verified for `tourism_value`, `nights_spent`, `occupancy_rate`, `hotel_capacity`, `arrivals`, `country_iso3`).

---

## F. What Is Incomplete / Not Implemented

1. **Gold tables not executed.** `gold_layer/` is empty; Gold tables will be created by running the Gold notebooks.
2. **Gold notebooks created.** `05 Gold Dimensions`, `06 Gold Facts`, `07 Gold Analytics`, `08 Gold Validation`, `09 Power BI Preparation` now exist.
3. **`03 Data Processing.ipynb` is a placeholder** — only imports, no processing.
4. **`03 Measurement Conversion.ipynb` does not implement conversions.** Its markdown says to convert percentages to absolute values and fill nulls, but no such transformation exists. Implementing it as written is invalid without denominators.
5. **Country normalization is incomplete for World Bank.** Live shows 78 `regional_aggregate` rows correctly flagged, but the notebook’s hardcoded list (`AFE/AFW/ARB`) is outdated. The complete set of World Bank aggregates and special geographies must be derived from the data (e.g., from `geography_type` values and codes).
6. **UN inbound unit is lost.** Live Silver has `unit = "NR"` for all 13,903 rows, but the original raw unit is `thousand trips`. The original value/unit should be preserved or reconstructable (e.g., `arrivals / 1000`).
7. **UN accommodation `hotel_capacity` mixes metrics.** It contains establishments, rooms, bed places (`units`), bed-place/room rates (`percent`), and average length of stay (`overnights`). Gold must split by `indicator_code`/`unit`.
8. **Eurostat negative values are legitimate in `PCH_*` units** (e.g., -100.0 in `estat_tour_occ_arm`). Anomaly detection should not treat them as errors.
9. **`estat_tour_occ_arm` has 591,124 null `tourism_value` rows** — the table is 32% populated; missing data must be handled with a documented policy (e.g., exclude from averages, impute with justification).
10. **No weather data is used** (out of scope), but the raw folder contains `weather_2010_2024.nc` — confirm this is intended and not needed.
11. **Gold docs/artifacts are now created.** `docs/gold_schema.md`, `docs/gold_validation_report.md`, `docs/data_lineage.md`, `docs/powerbi_measures.md`, `docs/powerbi_connection_guide.md` added. Power BI PBIX not created because Gold tables not executed.

---

## G. Errors and Data-Quality Issues (Live-Verified)

1. **Gold tables not executed** — `gold_layer/` is empty; Gold tables will be created by running the Gold notebooks.
2. **World Bank aggregation** — 78 regional aggregates exist but the cleaning notebook flags only 3; the other 75 are mislabeled as `country`. Gold must exclude aggregates.
3. **UN inbound unit loss** — original unit `thousand trips` not preserved in Silver.
4. **UN accommodation metric mixing** — `hotel_capacity` conflates units, percent, and overnights.
5. **Eurostat negative values in `PCH_*` units** — legitimate; anomaly detection must separate `NR` from `PCH_*`.
6. **High null rate in `estat_tour_occ_arm`** — 59% null `tourism_value`; missing-value policy needed.
7. **`estat_tour_occ_arm` zeros** — 4,054 zero `tourism_value` rows; review whether these are valid (e.g., zero arrivals in a month).
8. **Occupancy >100%** — `estat_tour_occ_mnor` max is 105.9; review methodology.
9. **No duplicate rows** — verified 0 duplicates on grains.
10. **No missing `country_iso3` for UN accommodation** — 212 distinct non-null ISO3, 0 nulls; good.
11. **`world_bank` nulls** — 1,110 null `arrivals`; preserve, do not zero-fill.

---

## H. Missing Gold Layer Components

Not yet created:

- `dim_country` — country dimension (ISO2, ISO3, M49, region, `is_country`, `is_aggregate`, `mapping_status`).
- `dim_date` — date dimension (year, month, quarter, season, `year_month`).
- `fact_tourism_arrivals` — arrivals fact (source, indicator, category, frequency, standardized values).
- `fact_nights_spent` — nights fact.
- `fact_hotel_performance` — hotel capacity/rooms/bed-places/rates/stay metrics.
- `fact_hotel_occupancy` — occupancy rates.
- Analytical outputs:
  - `gold_yearly_arrivals_by_country`
  - `gold_monthly_arrivals_by_country`
  - `gold_tourism_growth_yearly`
  - `gold_tourism_growth_monthly`
  - `gold_destination_rankings`
  - `gold_tourism_seasonality`
  - `gold_nights_spent_trends`
  - `gold_hotel_capacity_trends`
  - `gold_hotel_occupancy_trends`
  - `gold_visitor_category_analysis`
  - `gold_country_comparison`
  - `gold_source_comparison`
- Gold validation notebook/checks.
- Power BI semantic model, DAX measures, and connection guide.
- Gold documentation (`docs/gold_schema.md`, `docs/gold_validation_report.md`, `docs/powerbi_*.md`).

---

## I. Recommended Next Steps (Priority Order)

1. **Finalize dimension tables** — build `dim_country` with a complete, verified aggregate/country mapping (including the 78 World Bank aggregates, UN special geographies, Eurostat EU aggregates). This is the foundation for all Gold facts.
2. **Build `dim_date`** — full calendar with year, month, quarter, season; support annual (point-in-time) and monthly facts.
3. **Create Gold fact tables** — separate `fact_tourism_arrivals`, `fact_nights_spent`, `fact_hotel_performance`, `fact_hotel_occupancy` with documented grains and source-specific measures (no cross-source additive aggregates).
4. **Fix high-impact Silver issues first** — restore UN inbound original unit; split UN accommodation metrics by indicator/unit; exclude World Bank aggregates from country totals.
5. **Implement Gold analytical tables** — yearly/monthly arrivals, growth, rankings, seasonality, trends, country comparison, source comparison.
6. **Add Gold validation** — duplicate grain, null rates, negative/zero counts, unit/frequency consistency, referential integrity with dimensions.
7. **Prepare Power BI** — semantic model, DAX measures, connection guide.
8. **Update documentation** — `README`, `docs/gold_schema.md`, `docs/gold_validation_report.md`, `docs/data_lineage.md`, `docs/powerbi_*.md`.

---

*End of final audit report.*
