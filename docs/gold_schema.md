# TourismPulse — Gold Schema

**Date:** 2026-11-21  
**Repository:** `tourism-analytics` @ `main` (`9a13376`)  
**Volume:** `/Volumes/workspace/default/tourismdata/gold_layer/`

## Overview

The Gold layer is a Star Schema modeled for TourismPulse. Gold tables are written as Delta tables in the `gold_layer` volume. All queries in the Gold layer should filter on the primary analysis period (2012–2019) by default while retaining full historical data in the tables.

## Dimension Tables

### `dim_country`

| Column | Type | Description |
|---|---|---|
| `country_key` | INT | Primary key. For countries: M49 numeric code. For aggregates: negative surrogate ID. |
| `iso2` | STRING | ISO 2-letter code (nullable) |
| `iso3` | STRING | ISO 3-letter code (`XKX` for Kosovo, `BES` for Bonaire/Saba/St. Eustatius) |
| `country_name` | STRING | Human-readable name |
| `region` | STRING | Region name or `Aggregate` |
| `is_country` | BOOLEAN | True for countries, false for aggregates |
| `mapping_status` | STRING | `MAPPED_COUNTRY`, `MAPPED_AGGREGATE`, `SPECIAL_GEOGRAPHY`, `UNMAPPED` |

**Content:** Built from live Silver tables:
- World Bank countries (215 ISO3) and regional aggregates (78).
- UN inbound reporter areas (213 distinct ISO3).
- UN accommodation reporter areas (212 distinct ISO3).
- Eurostat countries (39 ISO2) and EU aggregates (EU25, EU27_2007, EU27_2020, EU28).
- Special: World (partner) and UN-specific geographies.

**Grain:** One row per geographic entity. Aggregates have `country_key < 0`.

### `dim_date`

| Column | Type | Description |
|---|---|---|
| `date_key` | INT | Monthly: `YYYYMMDD`; Annual: year (e.g., `2015`) |
| `date` | DATE | Date value |
| `year` | INT | Calendar year |
| `quarter` | INT | Calendar quarter (1–4) |
| `month` | INT | Month of year (1–12); null for annual |
| `month_name` | STRING | Month name; null for annual |
| `season` | STRING | Northern Hemisphere: Winter/Spring/Summer/Autumn; null for annual |
| `year_month` | STRING | `YYYYMM` for monthly; null for annual |
| `is_primary_period` | BOOLEAN | True for 2012–2019 |

**Grain:** One row per calendar day or annual year (1990–2027).

## Fact Tables

### `fact_tourism_arrivals`

| Column | Type | Description |
|---|---|---|
| `arrival_key` | INT | Surrogate key |
| `country_key` | INT | FK to `dim_country` |
| `geo_code` | STRING | Original source geography code |
| `country_name` | STRING | Original name (for readability) |
| `year` | INT | |
| `month` | INT | Nullable (annual facts) |
| `date_key` | INT | FK to `dim_date` |
| `frequency` | STRING | `A` (annual) or `M` (monthly) |
| `source_system` | STRING | `WORLD_BANK`, `UN_TOURISM`, `EUROSTAT` |
| `indicator_code` | STRING | Source indicator (e.g., `ST.INT.ARVL`, `INBD_TRIP_TOTL_TOTL_TOUR`) |
| `indicator_label` | STRING | Source indicator label |
| `visitor_category` | STRING | `Overnight visitors (tourists)`, `Visitors (total)`, `Same-day visitors (excursionists)`, `Cruise-ship same-day visitors`, `International arrivals` |
| `residence_category` | STRING | `DOM`, `FOR`, `TOTAL` (Eurostat) or null |
| `accommodation_category` | STRING | Source activity/geography code |
| `original_value` | DOUBLE | Raw value from Silver |
| `original_unit` | STRING | Raw unit (e.g., `thousand trips`, `number of arrivals`) |
| `standardized_value` | DOUBLE | Value in `standardized_unit` |
| `standardized_unit` | STRING | `persons` for UN/WB; `persons` for Eurostat `NR` |
| `observation_status` | STRING | Source observation flag (e.g., `D`, `E`, `B`, `P`, `u`, `e`) |
| `aggregation_level` | STRING | `Country`, `Aggregate`, `Territory`, `Special Geography` |
| `is_country` | BOOLEAN | FK to `dim_country.is_country` |
| `is_primary_period` | BOOLEAN | From `dim_date` |

**Grain:** One row per source observation. World Bank and UN are annual; Eurostat is monthly (`unit_code = 'NR'` only).

**Rules:**
- Do not sum `Visitors (total)` with component categories.
- Do not mix annual and monthly observations.
- UN inbound: original value = `arrivals / 1000`, original unit = `thousand trips`.

### `fact_nights_spent`

| Column | Type | Description |
|---|---|---|
| `nights_key` | INT | Surrogate key |
| `country_key` | INT | FK |
| `geo_code` | STRING | |
| `year` | INT | |
| `month` | INT | Nullable |
| `date_key` | INT | FK to `dim_date` |
| `residence_category` | STRING | `DOM`/`FOR`/`TOTAL` |
| `activity_category` | STRING | `nace_r2` code |
| `source_system` | STRING | `EUROSTAT` |
| `original_value` | DOUBLE | From Silver |
| `original_unit` | STRING | `nights` |
| `standardized_value` | DOUBLE | Same as original |
| `standardized_unit` | STRING | `nights` |
| `observation_status` | STRING | |
| `is_primary_period` | BOOLEAN | |

**Grain:** One row per monthly observation (`unit_code = 'NR'`).

### `fact_hotel_performance`

| Column | Type | Description |
|---|---|---|
| `hotel_perf_key` | INT | Surrogate key |
| `country_key` | INT | FK |
| `geo_code` | STRING | |
| `year` | INT | |
| `month` | INT | Nullable |
| `date_key` | INT | FK |
| `source_system` | STRING | `UN_TOURISM` |
| `indicator_code` | STRING | UN accommodation indicator |
| `indicator_label` | STRING | |
| `accommodation_metric` | STRING | `Establishments`, `Bed places`, `Rooms`, `Bed-place rate`, `Room rate`, `Average length of stay` |
| `original_value` | DOUBLE | From Silver |
| `original_unit` | STRING | `units`, `percent`, `overnights` |
| `standardized_value` | DOUBLE | Same as original |
| `standardized_unit` | STRING | Same as original |
| `observation_status` | STRING | |
| `is_primary_period` | BOOLEAN | |

**Grain:** One row per UN accommodation observation (annual). Metrics are not aggregated together.

### `fact_hotel_occupancy`

| Column | Type | Description |
|---|---|---|
| `occupancy_key` | INT | Surrogate key |
| `country_key` | INT | FK |
| `geo_code` | STRING | |
| `year` | INT | |
| `month` | INT | Nullable |
| `date_key` | INT | FK |
| `accommodation_unit` | STRING | `BEDPL` or `BEDRM` (separate) |
| `occupancy_rate` | DOUBLE | Percentage |
| `unit` | STRING | `PC` |
| `source_system` | STRING | `EUROSTAT` |
| `observation_status` | STRING | |
| `is_primary_period` | BOOLEAN | |

**Grain:** One row per monthly occupancy observation.

## Analytical Gold Tables

All analytical tables retain full history; `is_primary_period` marks the default 2012–2019 filter.

| Table | Description | Grain |
|---|---|---|
| `gold_yearly_arrivals_by_country` | Annual arrivals by country and source. | Country × Year × Source × Indicator × Visitor Category |
| `gold_monthly_arrivals_by_country` | Monthly arrivals by country and source. | Country × Year × Month × Source × Indicator × Visitor Category |
| `gold_tourism_growth_yearly` | Year-over-year growth % by country/source/indicator/category. | Country × Year × Source × Indicator × Visitor Category |
| `gold_tourism_growth_monthly` | Year-over-year monthly growth (same month previous year). | Country × Year × Month × Source × Indicator × Visitor Category |
| `gold_destination_rankings` | Top 50 destinations by absolute annual arrivals. | Country (sorted) |
| `gold_tourism_seasonality` | Monthly average, median, peak, lowest arrivals by month. | Month |
| `gold_nights_spent_trends` | Yearly total nights spent by country. | Country × Year |
| `gold_hotel_capacity_trends` | Yearly hotel capacity by metric. | Country × Year × Accommodation Metric |
| `gold_hotel_occupancy_trends` | Monthly average occupancy by country. | Country × Year × Month |
| `gold_visitor_category_analysis` | Annual arrivals by visitor category (overnight, excursionist, etc.). | Country × Year × Visitor Category |
| `gold_country_comparison` | Yearly arrivals by country and source. | Country × Source |
| `gold_source_comparison` | Controlled comparison across World Bank, UN, Eurostat (by country code). | Country Code |

## Primary Period (2012–2019)

Default analytical outputs filter on `is_primary_period = TRUE` (from `dim_date`). Full historical data is retained in all Gold tables.

## Next Steps

1. Run `05 Gold Dimensions.ipynb`, `06 Gold Facts.ipynb`, `07 Gold Analytics.ipynb` in Databricks.
2. Run `08 Gold Validation.ipynb` to validate row counts, duplicates, nulls, and referential integrity.
3. Run `09 Power BI Preparation.ipynb` to create DAX-ready tables.
4. Review `docs/gold_validation_report.md` and `docs/data_lineage.md` after execution.
