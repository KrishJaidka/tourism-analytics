# TourismPulse — Silver Readiness Report

**Phase:** 2 — Silver validation (provisional)  
**Date:** 2026-11-21  
**Repository commit:** `9a133768e751b05c096bed25e40835480400b23c`  
**Status:** **PROVISIONAL — static findings.** Live structure and SQL-based Silver validation are documented in §2 and §3. The static findings below come from (a) a static review of the committed cleaning/normalization notebooks and (b) direct profiling of the six supplied raw files. They are not live table counts.

---

## 2. Live Silver validation (verified)

Live checks were run via Databricks SQL API using profile `TOURISMPULSE` on the `Serverless Starter Warehouse` (ID `699426b61c5cd41b`). All queries were read-only.

### 2.1 `estat_tour_occ_arm`

- Row count: **895,230**
- Frequency: **M** (all rows); period range **1990-01-01 .. 2026-09-01** (441 months)
- Schema: `geo_code STRING, frequency STRING, residence_category STRING, unit_code STRING, activity_code STRING, geography_type STRING, period DATE, tourism_value DOUBLE, observation_flag STRING, country_iso3 STRING`
- Nulls: `tourism_value` = 591,124; `country_iso3` = 59,535
- Duplicates: 0
- Value stats: min = -100.0, max = 1.477e8, negatives = 61,616, zeros = 4,054
- Units: `NR` 284,445; `PCH_SM` 273,861; `PCH_SM_19` 254,016; `PCH_SM_2Y` 82,908
- Geography: 39 distinct non-null ISO3; `eu_aggregate` = 59,535 rows

### 2.2 `estat_tour_occ_mnor`

- Row count: **37,926**
- Frequency: **M**; period range **1990-01-01 .. 2026-09-01**
- Schema: `geo_code STRING, frequency STRING, accommodation_unit STRING, unit_code STRING, geography_type STRING, period DATE, occupancy_rate DOUBLE, observation_flag STRING, country_iso3 STRING`
- Nulls: `occupancy_rate` = 18,757; `country_iso3` = 3,528
- Duplicates: 0
- Value stats: min = 0.0, max = 105.9, negatives = 0, zeros = 17
- Units: `PC`; `accommodation_unit` = `BEDPL`/`BEDRM`
- Geography: 39 distinct non-null ISO3; `eu_aggregate` = 3,528 rows

### 2.3 `estat_tour_occ_nim`

- Row count: **893,466**
- Frequency: **M**; period range **1990-01-01 .. 2026-09-01**
- Schema: `geo_code STRING, frequency STRING, residence_category STRING, unit_code STRING, activity_code STRING, geography_type STRING, period DATE, nights_spent DOUBLE, observation_flag STRING, country_iso3 STRING`
- Nulls: `nights_spent` = 582,504; `country_iso3` = 59,535
- Duplicates: 0
- Value stats: min = -100.0, max = 5.34e8, negatives = 67,309, zeros = 4,110
- Units: `NR` 284,445; `PCH_SM` 273,861; `PCH_SM_19` 254,016; `PCH_SM_2Y` 81,144
- Geography: 39 distinct non-null ISO3; `eu_aggregate` = 59,535 rows

### 2.4 `un_tourism_accommodation_hotels`

- Row count: **18,594**
- Time range: **1995 .. 2024**
- Schema: `reporter_area_code INT, indicator_code STRING, indicator_label STRING, reporter_area STRING, geography_type STRING, year INT, hotel_capacity DOUBLE, unit STRING, observation_flag STRING, flag_label STRING, reporter_country_iso3 STRING`
- Nulls: `observation_flag`/`flag_label` = 18,356; `hotel_capacity` = 0
- Duplicates: 0
- Value stats: min = 0.12, max = 5,491,227; negatives = 0; zeros = 0
- Units: `units` 11,608; `percent` 4,036; `overnights` 2,950
- Geography: `geography_type` = `country`; `reporter_country_iso3` null = 0, 212 distinct ISO3
- Indicators: 6 UN accommodation indicators preserved

### 2.5 `un_tourism_inbound_arrivals`

- Row count: **13,903**
- Time range: **1995 .. 2025**
- Schema: `partner_area_code INT, reporter_area_code INT, indicator_code STRING, indicator_label STRING, reporter_area STRING, reporter_geography_type STRING, partner_area STRING, partner_geography_type STRING, year INT, arrivals DOUBLE, unit STRING, observation_flag STRING, flag_label STRING, reporter_country_iso3 STRING, partner_country_iso3 STRING`
- Nulls: `arrivals` = 0; `observation_flag`/`flag_label` = 13,743; `partner_country_iso3` = 13,903 (all null; partner is World)
- Duplicates: 0
- Value stats: min = 0.0, max = 2.18e8; negatives = 0; zeros = 1
- Units: `NR`
- Geography: `reporter_geography_type` = `country` (13,903); `partner_geography_type` = `world_aggregate` (13,903); `reporter_country_iso3` null = 0, 213 distinct ISO3
- Indicators: 4 UN inbound categories preserved (`TOTL_TOUR` 5,244; `VSTR` 3,794; `EXCR` 2,985; `CRUS_EXCR` 1,880)

### 2.6 `world_bank_international_arrivals`

- Row count: **6,916**
- Time range: **1995 .. 2020**
- Schema: `country_name STRING, country_code STRING, indicator_name STRING, indicator_code STRING, geography_type STRING, year INT, arrivals DOUBLE, country_iso3 STRING`
- Nulls: `arrivals` = 1,110
- Duplicates: 0
- Value stats: min = 700.0, max = 2.403e9; negatives = 0; zeros = 0
- Geography: `geography_type` = `country` 6,838; `regional_aggregate` 78; `country_iso3` null = 1,326, 215 distinct ISO3
- Indicator: `ST.INT.ARVL`

---

## 1. Method

### 1.0 Live verification (current, 2026-11-21)

- Catalog `workspace`; schema `workspace/default`; volume `tourismdata` exists.
- Folder structure: `raw`, `bronze_layer`, `silver_layer`, `gold_layer`.
- `raw`: six expected files plus `weather_2010_2024.nc` (out of scope, 4.09 GB).
- `bronze_layer`: six Delta directories.
- `silver_layer`: six Delta directories — `estat_tour_occ_arm`, `estat_tour_occ_mnor`, `estat_tour_occ_nim`, `un_tourism_accommodation_hotels`, `un_tourism_inbound_arrivals`, `world_bank_international_arrivals`.
- `gold_layer`: empty (no Gold tables exist).
- Live raw file sizes match the supplied files; see `docs/current_project_status.md` §4.
- The workspace Git folder contains the same 13 notebooks as GitHub plus an extra notebook `Rough - Dont include in github`.
- Live SQL access is not yet available; Silver schemas, row counts, nulls, duplicates and execution state are pending.


1. Cloned `https://github.com/KrishJaidka/tourism-analytics` at `main` / `9a13376`.
2. Read all 13 notebooks and `config/config.py`.
3. Profiled the six supplied raw files with Python/pandas:
   - row counts, columns, encodings;
   - indicator × unit cross-tabs;
   - year/period coverage;
   - distinct geographies;
   - null/missing markers;
   - duplicates on candidate grains;
   - negative/zero values;
   - observation flags.
4. Derived the expected Silver schema and row count from each notebook’s `select(...)` and explode logic.
5. Compared the derived geography classifications with `pycountry` ISO2/ISO3/M49 mappings and the notebook’s exceptions.

No notebook, table or volume was modified.

---

## 2. Readiness summary

| Silver table | Expected rows | Frequency | Primary period (2012–2019) | Readiness | Prompt compliance | Blocking warning |
|---|---:|---|---|---|---|---|
| `world_bank_international_arrivals` | 6,916 | Annual | 2012–2019 present | **READY WITH WARNINGS** | **FAIL** — 47 aggregates misclassified | Complete aggregate list required before country totals |
| `un_tourism_inbound_arrivals` | 13,903 | Annual | 2012–2019 present | **READY WITH WARNINGS** | **FAIL** — original unit lost | Restore original value/unit provenance |
| `un_tourism_accommodation_hotels` | 18,594 | Annual | 2012–2019 present | **READY WITH WARNINGS** | **PARTIAL** — metrics conflated | Split counts, percentages and overnights |
| `estat_tour_occ_arm` | 895,230 | Monthly | 2012–2019 present | **READY WITH WARNINGS** | **PARTIAL** — units mixed in one column | Filter `NR` for counts; treat `PCH_*` as growth rates |
| `estat_tour_occ_nim` | 893,466 | Monthly | 2012–2019 present | **READY WITH WARNINGS** | **PARTIAL** — units mixed in one column | Filter `NR` for counts; treat `PCH_*` as growth rates |
| `estat_tour_occ_mnor` | 37,926 | Monthly | 2012–2019 present | **READY WITH WARNINGS** | **PASS with caveats** — rates only | Keep `BEDPL` and `BEDRM` separate; never sum |

**Overall verdict:** **PROVISIONALLY READY WITH WARNINGS.** The raw data is intact and the expected grains are sound, but no table is certified. The P0 issues in `docs/current_project_status.md` must be handled in Gold logic (or by a controlled Silver fix) before any country totals, rankings or comparisons are published.

---

## 3. Table-by-table assessment

### 3.1 `world_bank_international_arrivals`

**Source:** World Bank `ST.INT.ARVL`, annual 1995–2020.  
**Expected grain:** `country_code × year × indicator_code` (one row per entity per year).  
**Expected rows:** `266 entities × 26 years = 6,916`.

**Expected Silver columns:**

```text
country_name, country_code, indicator_name, indicator_code,
geography_type, year, arrivals, country_iso3
```

**Data quality (from the supplied file):**

| Check | Result |
|---|---|
| Non-null `arrivals` | 5,806 / 6,916 (83.95%) |
| Null `arrivals` | 1,110 (16.05%) — blank cells preserved as null |
| Negative values | 0 |
| Zero values | 0 |
| Duplicate `country_code × year` | 0 |
| Entities | 266: 215 ISO3 countries, 50 aggregates, 1 territory (`XKX` Kosovo) |
| `country_iso3` nulls | 1,326 rows expected: 1,300 aggregate rows + 26 `XKX` rows |
| Frequency | Annual only — do not manufacture months |
| Unit | Absolute number of arrivals; **no unit column in Silver** |

**Geography problem:**

The cleaning notebook marks only `AFE`, `AFW` and `ARB` as `regional_aggregate`. The file contains **50 aggregates** (Appendix A of the status report) plus Kosovo `XKX`. The other 47 aggregates — including `WLD`, `EUU`, `ECS`, `HIC`, `LMY`, `SAS`, `SSF` — are labelled `country`. If Gold groups by `geography_type = 'country'`, it will double-count and inflate totals.

**Readiness:** **READY WITH WARNINGS.**  
**Required before Gold:**

- Use the complete 50-code aggregate list; do not rely on the current `geography_type`.
- Map `XKX` as a special geography/territory, not an aggregate and not an unmapped null.
- Add `unit = 'number of arrivals'` (persons) in Gold.
- Exclude aggregates from country-level facts, rankings and totals.
- Preserve nulls; never replace blanks with zero.

---

### 3.2 `un_tourism_inbound_arrivals`

**Source:** UN Tourism inbound arrivals, annual 1995–2025.  
**Expected grain:** `indicator_code × reporter_area_code × partner_area_code × year`.  
**Expected rows:** 13,903.

**Expected Silver columns:**

```text
indicator_code, indicator_label, reporter_area_code, reporter_area,
reporter_geography_type, partner_area_code, partner_area,
partner_geography_type, year, arrivals, unit,
observation_flag, flag_label, reporter_country_iso3, partner_country_iso3
```

**Data quality (from the supplied file):**

| Check | Result |
|---|---|
| Non-null `value` | 13,903 / 13,903 (100%) |
| Null values | 0 |
| Negative values | 0 |
| Zero values | 1 |
| Duplicate keys | 0 |
| Years | 1995–2025 (31 years) |
| Reporters | 215: 212 ISO3 + 3 BES special areas |
| Partner | `World` (`999`) for every row |
| Indicators | 4 (overnight tourists, total visitors, same-day excursionists, cruise same-day) |
| Raw unit | `thousand trips` for every row |
| Flags | `D` 141, `E` 16, `B` 2, `P` 1 |

**Unit problem:**

The cleaning notebook does:

```python
df = df.withColumn("arrivals", col("arrivals") * 1000) \
       .withColumn("unit", lit("NR"))
```

This converts `thousand trips` to persons and overwrites the unit. The conversion is arithmetically reversible, but the original value and unit are not preserved in Silver. That fails the project requirement to keep original measurements and document conversions.

**Category problem:**

The four indicators are distinct and must stay distinct:

| Code | Meaning | Rows |
|---|---|---:|
| `INBD_TRIP_TOTL_TOTL_TOUR` | Overnight visitors (tourists) | 5,244 |
| `INBD_TRIP_TOTL_TOTL_VSTR` | Visitors (total) | 3,794 |
| `INBD_TRIP_TOTL_TOTL_EXCR` | Same-day visitors (excursionists) | 2,985 |
| `INBD_TRIP_TOTL_CRUS_EXCR` | Cruise-ship same-day visitors | 1,880 |

`TOTL_VSTR` is a total and may already include the component categories. Do not add it to `TOTL_TOUR`, `TOTL_EXCR` or `CRUS_EXCR`. Also, the 141 `D`-flagged `TOTL_VSTR` rows are overnight-only because same-day data was unavailable; they must not be treated as complete total visitors.

**Geography:**

- 212 reporters map through `pycountry` M49.
- `5351 Bonaire`, `5352 Saba`, `5353 St. Eustatius` are mapped to `BES` by the notebook. This collapses three areas into one entity; document it.
- `partner_area_code = 999` (World) has no ISO3 and is correctly typed `world_aggregate`.

**Readiness:** **READY WITH WARNINGS.**  
**Required before Gold:**

- Restore `original_value = arrivals / 1000`, `original_unit = 'thousand trips'`, `standardized_value = arrivals`, `standardized_unit = 'persons'`.
- Keep indicator codes and labels; never sum totals with components.
- Respect `D`, `E`, `B`, `P` flags; do not silently drop flagged rows.
- Keep reporter and partner geography separate.
- Do not treat `BES` as three countries.

---

### 3.3 `un_tourism_accommodation_hotels`

**Source:** UN Tourism accommodation/hotels, annual 1995–2024.  
**Expected grain:** `indicator_code × reporter_area_code × year`.  
**Expected rows:** 18,594.

**Expected Silver columns:**

```text
indicator_code, indicator_label, reporter_area_code, reporter_area,
geography_type, year, hotel_capacity, unit,
observation_flag, flag_label, reporter_country_iso3
```

**Data quality (from the supplied file):**

| Check | Result |
|---|---|
| Non-null `value` | 18,594 / 18,594 (100%) |
| Null values | 0 |
| Negative values | 0 |
| Zero values | 0 (minimum 0.12) |
| Duplicate keys | 0 |
| Years | 1995–2024 (30 years) |
| Reporters | 214: 211 ISO3 + 3 BES special areas |
| Indicators | 6 |
| Units | `units` 11,608; `percent` 4,036; `overnights` 2,950 |
| Flags | `E` 211, `B` 16, `W` 5, `B,E` 5, `P` 1 |

**Metric problem:**

The cleaning notebook renames `value` to `hotel_capacity` for **all six indicators**:

| Indicator | Meaning | Unit | Rows |
|---|---|---|---:|
| `CPTY_ACCM_HOTL_ESTB` | Establishments | `units` | 3,253 |
| `CPTY_ACCM_HOTL_BEDS` | Bed places | `units` | 3,796 |
| `CPTY_ACCM_HOTL_ROOM` | Rooms | `units` | 4,559 |
| `CPTY_ACCM_HOTL_BEDS_RATE` | Bed-place rate | `percent` | 1,588 |
| `CPTY_ACCM_HOTL_ROOM_RATE` | Room rate | `percent` | 2,448 |
| `CPTY_ACCM_HOTL_STAY_AVRG` | Average length of stay | `overnights` | 2,950 |

`hotel_capacity` is therefore not a capacity measure. It is a mixed numeric column. Gold must split it by `indicator_code` and `unit`; never sum or average across indicators.

**Provenance loss:**

The notebook drops `indicator_previous_code` and `notes`. Flags survive, but definition notes (for example, “Year-end figure”, “Average of monthly rooms over 12 months”, “Includes data from another category”) do not.

**Geography:**

- 211 reporters map through `pycountry` M49; the three BES areas map to `BES` via the notebook exception.
- No regional aggregates appear in this file; `geography_type = 'country'` for all rows is acceptable for the supplied data, but the status should be explicit.

**Readiness:** **READY WITH WARNINGS.**  
**Required before Gold:**

- Create separate measures for establishments, rooms, bed places, bed-place rate, room rate and average length of stay.
- Keep `percent` and `overnights` out of count aggregations.
- Preserve flags and, where possible, notes/previous codes in a sidecar table.
- Do not treat `BES` as three countries.

---

### 3.4 `estat_tour_occ_arm`

**Source:** Eurostat monthly arrivals at tourist accommodation establishments, 1990-01–2026-09.  
**Expected grain:** `frequency × residence_category × unit_code × activity_code × geo_code × period`.  
**Expected rows:** `2,030 dimension rows × 441 months = 895,230`.

**Expected Silver columns:**

```text
frequency, residence_category, unit_code, activity_code,
geo_code, geography_type, period, tourism_value,
observation_flag, country_iso3
```

**Data quality (from the supplied file):**

| Check | Result |
|---|---|
| Total exploded rows | 895,230 |
| Non-null `tourism_value` | 304,106 (33.97%) |
| Null `tourism_value` (`:` in raw) | 588,710 (65.76%) |
| Negative values | 61,616 — **all in `PCH_*` units** |
| Duplicate full-grain keys | 0 |
| Frequency | `M` only (monthly) |
| Period coverage | 1990-01–2026-09 (441 months) |
| Geographies | 43: 39 ISO2 + 4 EU aggregates |
| `country_iso3` nulls | 59,535 rows expected (EU aggregates, all periods) |
| Primary 2012–2019 `NR` numeric rows | 54,872 |
| Primary 2012–2019 `PCH_SM` numeric rows | 49,411 |
| Primary 2012–2019 `PCH_SM_19` / `PCH_SM_2Y` | 0 |

**Unit problem:**

`tourism_value` contains four different measures:

| Unit | Meaning | Numeric cells | Negatives |
|---|---|---:|---:|
| `NR` | Absolute arrivals | 136,287 | 0 |
| `PCH_SM` | % change vs same month previous year | 124,876 | 39,868 |
| `PCH_SM_19` | % change vs same month 2019 | 38,761 | 19,901 |
| `PCH_SM_2Y` | % change vs same month 2 years earlier | 4,182 | 1,847 |

The negative values are **valid percentage declines**, not data errors. Any anomaly rule that treats `tourism_value < 0` as invalid will produce false positives. Counts must be filtered to `unit_code = 'NR'`; growth rates must be modelled separately.

**Overlapping categories:**

- `residence_category`: `TOTAL`, `DOM`, `FOR`. `TOTAL` is an aggregate of `DOM + FOR`; never sum `TOTAL` with its components.
- `activity_code`: `I551`, `I552`, `I553`, `I552_I553`, `I551-I553`. The last two are aggregates; never sum them with their components.

**Geography:**

- 39 ISO2 countries; `EL → GRC`, `UK → GBR`, `XK → XKX` are handled.
- 4 EU aggregates (`EU25`, `EU27_2007`, `EU27_2020`, `EU28`) are marked `eu_aggregate`; their `country_iso3` is null. Never sum them with countries or with each other.

**Missingness:**

`:` means “not available”. It is correctly converted to null, not zero. The table is 65.76% null by construction because every dimension combination is exploded across all 441 months, including months with no observation. Gold must filter null measures, not impute them.

**Readiness:** **READY WITH WARNINGS.**  
**Required before Gold:**

- Filter `unit_code = 'NR'` for arrival counts.
- Model `PCH_*` as growth-rate facts with their own unit.
- Filter `residence_category = 'TOTAL'` for country totals; use `DOM`/`FOR` only for splits.
- Filter `activity_code = 'I551-I553'` (or the appropriate total) for all-accommodation totals; never sum totals with components.
- Keep `period` monthly; never derive monthly rows from annual sources.
- Preserve nulls; do not fill them.

---

### 3.5 `estat_tour_occ_nim`

**Source:** Eurostat monthly nights spent at tourist accommodation establishments, 1990-01–2026-09.  
**Expected grain:** `frequency × residence_category × unit_code × activity_code × geo_code × period`.  
**Expected rows:** `2,026 dimension rows × 441 months = 893,466`.

**Expected Silver columns:**

```text
frequency, residence_category, unit_code, activity_code,
geo_code, geography_type, period, nights_spent,
observation_flag, country_iso3
```

**Data quality (from the supplied file):**

| Check | Result |
|---|---|
| Total exploded rows | 893,466 |
| Non-null `nights_spent` | 310,962 (34.80%) |
| Null `nights_spent` (`:`) | 580,079 (64.92%) |
| Negative values | 67,309 — **all in `PCH_*` units** |
| Duplicate full-grain keys | 0 |
| Frequency | `M` only |
| Period coverage | 1990-01–2026-09 (441 months) |
| Geographies | 43: 39 ISO2 + 4 EU aggregates |
| `country_iso3` nulls | 59,535 rows expected (EU aggregates) |
| Primary 2012–2019 `NR` numeric rows | 55,290 |
| Primary 2012–2019 `PCH_SM` numeric rows | 50,025 |
| Primary 2012–2019 `PCH_SM_19` / `PCH_SM_2Y` | 0 |

**Unit breakdown:**

| Unit | Meaning | Numeric cells | Negatives |
|---|---|---:|---:|
| `NR` | Absolute nights spent | 139,419 | 0 |
| `PCH_SM` | % change vs same month previous year | 128,300 | 44,649 |
| `PCH_SM_19` | % change vs same month 2019 | 38,965 | 20,284 |
| `PCH_SM_2Y` | % change vs same month 2 years earlier | 4,278 | 2,376 |

The same rules as `estat_tour_occ_arm` apply: counts use `NR`; growth rates are separate; `TOTAL` is not summed with `DOM`/`FOR`; `I551-I553`/`I552_I553` are not summed with components; nulls stay null.

**Readiness:** **READY WITH WARNINGS.**  
**Required before Gold:** same as §3.4.

---

### 3.6 `estat_tour_occ_mnor`

**Source:** Eurostat monthly net occupancy rates of bed places and bedrooms, 1990-01–2026-09.  
**Expected grain:** `frequency × accommodation_unit × unit_code × geo_code × period`.  
**Expected rows:** `86 dimension rows × 441 months = 37,926`.

**Expected Silver columns:**

```text
frequency, accommodation_unit, unit_code, geo_code,
geography_type, period, occupancy_rate,
observation_flag, country_iso3
```

**Data quality (from the supplied file):**

| Check | Result |
|---|---|
| Total exploded rows | 37,926 |
| Non-null `occupancy_rate` | 19,169 (50.54%) |
| Null `occupancy_rate` (`:`) | 18,663 (49.21%) |
| Negative values | 0 |
| Zero values | 17 |
| Maximum | 105.9 (review; do not auto-delete) |
| Duplicate full-grain keys | 0 |
| Frequency | `M` only |
| Period coverage | 1990-01–2026-09 (441 months) |
| Geographies | 43: 39 ISO2 + 4 EU aggregates |
| `country_iso3` nulls | 3,528 rows expected (EU aggregates) |
| Accommodation units | `BEDPL` (bed places), `BEDRM` (bedrooms) |
| Unit | `PC` only (percent) |
| Primary 2012–2019 numeric rows | 7,272 |

**Semantics:**

- `BEDPL` and `BEDRM` are different occupancy measures. Keep them as separate series; do not sum or average them together.
- Occupancy is a percentage. Never sum percentages. If an aggregate is required, use a documented weighted average with a valid denominator; if no denominator exists, report the simple average of country rates as a descriptive statistic, clearly labelled.
- Values above 100% are unusual but can occur through methodology/coverage differences. Review them; do not automatically delete them.

**Readiness:** **READY WITH WARNINGS.**  
**Required before Gold:**

- Keep `BEDPL` and `BEDRM` separate.
- Never sum occupancy percentages.
- Use a documented average/weighted-average method.
- Preserve nulls; do not fill them.
- Review `>100` values with the source metadata.

---

## 4. Cross-cutting findings

### 4.1 Annual and monthly data are not interchangeable

| Source | Frequency | Coverage |
|---|---|---|
| UN inbound | Annual | 1995–2025 |
| UN accommodation | Annual | 1995–2024 |
| World Bank | Annual | 1995–2020 |
| Eurostat arrivals | Monthly | 1990-01–2026-09 |
| Eurostat nights | Monthly | 1990-01–2026-09 |
| Eurostat occupancy | Monthly | 1990-01–2026-09 |

Rules:

- Never manufacture monthly observations from annual data.
- Never join annual and monthly facts on `year` alone.
- Keep annual and monthly measures separate in Gold and Power BI.
- Use 2012–2019 as the default analytical filter, but retain all years in Silver and Gold.

### 4.2 Overlapping totals and components

Do not add:

- UN `TOTL_VSTR` + `TOTL_TOUR` + `TOTL_EXCR` + `CRUS_EXCR`.
- Eurostat `TOTAL` + `DOM` + `FOR`.
- Eurostat `I551-I553` + `I551` + `I552` + `I553`.
- Eurostat `I552_I553` + `I552` + `I553`.
- Eurostat `EU27_2020` + member countries.
- World Bank `WLD`/`EUU`/regional aggregates + countries.
- Eurostat occupancy `BEDPL` + `BEDRM`.

### 4.3 Units are not interchangeable

Do not add or average across:

- `thousand trips` vs persons.
- Absolute counts (`NR`) vs percentage changes (`PCH_*`).
- `units` vs `percent` vs `overnights`.
- Occupancy percentages vs capacity counts.
- Arrivals vs nights spent.

### 4.4 Missing values are meaningful

Eurostat uses `:` for “not available”; UN and World Bank use blanks. All are converted to null by the current code. That is correct. Do not:

- replace nulls with zero;
- fill missing months with interpolation unless a documented, approved method exists;
- treat missing as “no tourism”.

### 4.5 Flags must survive

Preserve:

- UN `observation_flag` and `flag_label` (`D`, `E`, `B`, `W`, `P`, combinations such as `B,E`);
- Eurostat observation flags (`b`, `e`, `u`, `be`);
- source notes where available.

Flags affect interpretation. For example, the 141 `D`-flagged UN total-visitor rows are overnight-only.

### 4.6 Geography must be explicit

The current `geography_type` values are too coarse. Gold needs a `dim_country` with at least:

```text
MAPPED_COUNTRY
MAPPED_AGGREGATE
SPECIAL_GEOGRAPHY
UNMAPPED
```

Do not silently drop unmapped codes. Do not count aggregates as countries.

### 4.7 Negative values are not automatically errors

- World Bank: no negatives.
- UN: no negatives.
- Eurostat `NR`: no negatives.
- Eurostat `PCH_*`: negatives are valid declines.

Anomaly detection must branch on `unit_code` before applying a “negative is invalid” rule.

### 4.8 Duplicates

No duplicate candidate-grain keys were found in the supplied raw files. The live tables must still be checked, because overwrites, re-runs or joins can introduce duplicates.

---

## 5. Schema and grain notes for Gold

The Silver tables are **not** a star schema. They are source-shaped Delta tables. Gold should not simply copy them. Recommended treatment:

| Silver table | Gold treatment |
|---|---|
| `world_bank_international_arrivals` | `fact_tourism_arrivals` with `source_system = 'WORLD_BANK'`, `visitor_category = 'international_arrivals'`, `frequency = 'A'`; exclude aggregates from country facts. |
| `un_tourism_inbound_arrivals` | `fact_tourism_arrivals` with `source_system = 'UN_TOURISM'`; keep the four indicator categories; restore original unit. |
| `un_tourism_accommodation_hotels` | `fact_hotel_performance` split by `accommodation_metric` and `unit`; counts, percentages and overnights remain separate. |
| `estat_tour_occ_arm` | `fact_tourism_arrivals` with `source_system = 'EUROSTAT'`, `frequency = 'M'`; counts use `unit_code = 'NR'`; growth rates go to a separate growth fact. |
| `estat_tour_occ_nim` | `fact_nights_spent` with `frequency = 'M'`; counts use `unit_code = 'NR'`; growth rates separate. |
| `estat_tour_occ_mnor` | `fact_hotel_occupancy` with `accommodation_unit` (`BEDPL`/`BEDRM`) and `occupancy_rate`; never sum. |

Do not create one universal arrivals table that loses source definitions. A single fact table can hold multiple sources only if every row keeps `source_system`, `indicator_code`, `visitor_category`, `residence_category`, `accommodation_category`, `frequency` and `unit`, and if no query sums across incompatible rows.

---

## 6. What is safe to do now

Without live access, the following are safe:

- Finalize the Gold schema and grain definitions.
- Build the `dim_country` mapping tables from the observed codes (World Bank aggregates, Eurostat ISO2 + EU aggregates, UN M49 + BES, Kosovo).
- Build the `dim_date` calendar (2012–2019 default, full coverage available).
- Write Gold transformation code that reads Silver paths, but do not execute or publish it yet.
- Write validation queries and expected-results checks.
- Write the Power BI measure definitions and connection guide as drafts.

Do not:

- create Gold tables;
- overwrite Silver tables;
- assume the volume exists;
- claim live row counts;
- push to GitHub.

---

## 7. Required Silver fixes vs Gold-side handling

| Issue | Fix in Silver? | Fix in Gold? | Recommendation |
|---|---|---|---|
| World Bank aggregate classification | Optional | **Required** | Prefer a complete `dim_country` + `mapping_status` in Gold; avoid rewriting Silver. |
| UN inbound unit loss | Optional | **Required** | Restore original value/unit in Gold; optionally add columns to Silver later. |
| UN accommodation mixed metric | No | **Required** | Split by `indicator_code`/`unit` in Gold. |
| Eurostat unit mixing | No | **Required** | Filter `NR` for counts; separate `PCH_*` facts. |
| Eurostat overlapping totals | No | **Required** | Filter totals/components explicitly. |
| Anomaly detection overwrite | **Yes** | — | Stop overwriting Silver; write a quality/quarantine table. |
| Missing notes/previous codes | Optional | Optional | Preserve in a sidecar metadata table. |
| `03 Data Processing` placeholder | Optional | — | Implement or remove from the execution order. |

The only change that should be made to the existing Silver pipeline before Gold is the destructive anomaly-detection overwrite. The other issues can be handled correctly in Gold without rebuilding Silver.

---

## 8. Live validation queries to execute in Phase 2

Run these in a Databricks notebook after authentication. They are read-only.

```python
from pyspark.sql import functions as F

tables = {
    "estat_tour_occ_arm": {
        "keys": ["frequency", "residence_category", "unit_code", "activity_code", "geo_code", "period"],
        "measure": "tourism_value",
        "time": "period",
    },
    "estat_tour_occ_mnor": {
        "keys": ["frequency", "accommodation_unit", "unit_code", "geo_code", "period"],
        "measure": "occupancy_rate",
        "time": "period",
    },
    "estat_tour_occ_nim": {
        "keys": ["frequency", "residence_category", "unit_code", "activity_code", "geo_code", "period"],
        "measure": "nights_spent",
        "time": "period",
    },
    "un_tourism_accommodation_hotels": {
        "keys": ["indicator_code", "reporter_area_code", "year"],
        "measure": "hotel_capacity",
        "time": "year",
    },
    "un_tourism_inbound_arrivals": {
        "keys": ["indicator_code", "reporter_area_code", "partner_area_code", "year"],
        "measure": "arrivals",
        "time": "year",
    },
    "world_bank_international_arrivals": {
        "keys": ["country_code", "year", "indicator_code"],
        "measure": "arrivals",
        "time": "year",
    },
}

for table, cfg in tables.items():
    path = f"{silver_path}/{table}"
    print("\n" + "=" * 90)
    print("TABLE:", table)
    print("=" * 90)

    df = spark.read.format("delta").load(path)
    df.printSchema()

    total = df.count()
    print("rows:", total)

    # Duplicate grain
    dup = (
        df.groupBy(*cfg["keys"]).count()
          .filter(F.col("count") > 1)
          .count()
    )
    print("duplicate grain groups:", dup)

    # Measure nulls / negatives / zeros
    m = cfg["measure"]
    df.select(
        F.count(F.when(F.col(m).isNull(), 1)).alias("null_measure"),
        F.count(F.when(F.col(m) < 0, 1)).alias("negative_measure"),
        F.count(F.when(F.col(m) == 0, 1)).alias("zero_measure"),
        F.min(m).alias("min_measure"),
        F.max(m).alias("max_measure"),
    ).show(truncate=False)

    # Time coverage
    df.select(
        F.min(cfg["time"]).alias("min_time"),
        F.max(cfg["time"]).alias("max_time"),
        F.countDistinct(cfg["time"]).alias("distinct_time"),
    ).show(truncate=False)

    # Unit / category distributions
    for c in ["unit_code", "unit", "geography_type", "observation_flag"]:
        if c in df.columns:
            print("--", c)
            df.groupBy(c).count().orderBy(F.desc("count")).show(50, truncate=False)

    # Country mapping
    for c in ["country_iso3", "reporter_country_iso3", "partner_country_iso3"]:
        if c in df.columns:
            print("-- null", c)
            df.filter(F.col(c).isNull()).count()
```

Additional checks:

```python
# Eurostat: confirm negatives only occur in PCH_* units
for t in ["estat_tour_occ_arm", "estat_tour_occ_nim"]:
    df = spark.read.format("delta").load(f"{silver_path}/{t}")
    m = "tourism_value" if t == "estat_tour_occ_arm" else "nights_spent"
    df.filter(F.col(m) < 0).groupBy("unit_code").count().show()

# World Bank: list every code the current Silver labels as a country
wb = spark.read.format("delta").load(f"{silver_path}/world_bank_international_arrivals")
wb.filter(F.col("geography_type") == "country") \
  .select("country_code", "country_name") \
  .distinct().orderBy("country_code").show(300, truncate=False)

# UN accommodation: confirm indicator × unit mapping
hotels = spark.read.format("delta").load(f"{silver_path}/un_tourism_accommodation_hotels")
hotels.groupBy("indicator_code", "unit").count().orderBy("indicator_code").show(50, truncate=False)

# UN inbound: confirm the unit is uniform and the categories are intact
un = spark.read.format("delta").load(f"{silver_path}/un_tourism_inbound_arrivals")
un.groupBy("indicator_code", "unit").count().orderBy("indicator_code").show(50, truncate=False)
```

Record the actual outputs in this report. Until then, the readiness labels remain **provisional**.

---

## 9. Verdict

| Question | Answer |
|---|---|
| Are the six Silver tables present? | **Unknown** — live workspace not inspected. |
| Do they have the expected schemas? | **Expected from code; not verified.** |
| Do they have the expected row counts? | **Expected from raw dimensions; not verified.** |
| Is the data complete enough for Gold? | **Yes, provisionally** — the raw sources are complete and the grains are sound. |
| Are there correctness issues? | **Yes** — World Bank aggregates, UN unit loss, UN accommodation metric mixing, Eurostat unit mixing, destructive anomaly overwrite. |
| Can Gold development start? | **Schema/design work: yes. Execution/publication: no**, until live access and the P0 fixes are in place. |

**Next action:** authenticate to Databricks (see §8 of `docs/current_project_status.md`), then run the §8 queries above and replace the provisional figures with live results.

---

*End of provisional Silver readiness report.*
