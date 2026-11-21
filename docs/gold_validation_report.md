# TourismPulse — Gold Validation Report

**Date:** 2026-11-21  
**Status:** Static pre-execution validation report. Live SQL validation via the `TOURISMPULSE` CLI profile is available; notebooks are the execution vehicle.  
**Gold layer status:** Gold dimensions, facts, and analytics are implemented as notebooks and documented in `docs/gold_schema.md`. Live tables will be created when the notebooks are executed in Databricks.

## Validation Approach

Gold tables are validated using two layers:

1. **Notebook-based validation** (`08 Gold Validation.ipynb`):
   - Row counts for all Gold tables.
   - Duplicate grain groups (`COUNT(*) > 1`).
   - Null counts in key columns.
   - Negative values in `standardized_value` for arrivals/nights.
   - Referential integrity spot checks against `dim_country`.
   - Unit/frequency consistency checks.

2. **SQL API validation** (executed during audit via `databricks api post /api/2.0/sql/statements` on the `Serverless Starter Warehouse`, ID `699426b61c5cd41b`):
   - All six Silver tables validated (schemas, row counts, nulls, duplicates, value stats, units, geography, time ranges). Results in `docs/audit_report.md` §D.

## Static Validation Findings

### `fact_tourism_arrivals`
- Grain: `country_key, geo_code, year, month, source_system, indicator_code, visitor_category, frequency`.
- Validations:
  - No negative `standardized_value` for arrivals (WB/UN/Eurostat counts are non-negative).
  - `frequency` is `A` or `M`; annual and monthly records are separate.
  - `visitor_category` for UN is mapped from indicator codes.
  - World Bank aggregates are excluded (`country_iso3 IS NOT NULL`).

### `fact_nights_spent`
- Grain: `country_key, geo_code, year, month`.
- Validations:
  - Only `unit_code = 'NR'` rows are included.
  - `standardized_value` is non-negative.

### `fact_hotel_performance`
- Grain: `country_key, year, accommodation_metric`.
- Validations:
  - Indicators are split by `accommodation_metric` (Establishments, Bed places, Rooms, Rates, Average length of stay).
  - Units `units`, `percent`, `overnights` are preserved.

### `fact_hotel_occupancy`
- Grain: `country_key, year, month, accommodation_unit`.
- Validations:
  - `accommodation_unit` is `BEDPL` or `BEDRM` (separate).
  - `occupancy_rate` is a percentage; no negative values.

### Analytical Gold tables
- `gold_yearly_arrivals_by_country`: annual only; `is_primary_period = TRUE` default.
- `gold_monthly_arrivals_by_country`: monthly only; no annual values.
- `gold_tourism_growth_yearly/monthly`: growth % is computed from current vs. previous-year/same-month values.
- `gold_destination_rankings`: top 50 by absolute arrivals.
- `gold_tourism_seasonality`: monthly averages across the full period.
- No cross-source additive totals are used where sources are incompatible.

## Known Issues to Fix Before Marking Gold Tables Validated

1. **Silver:** UN inbound original unit (`thousand trips`) is not preserved; Gold reconstructs it as `arrivals / 1000` (documented in `fact_tourism_arrivals`).
2. **Silver:** UN accommodation `hotel_capacity` mixes units/percent/overnights; Gold splits by `indicator_code`.
3. **Silver:** World Bank regional aggregates must be excluded from country-level totals; Gold uses `country_iso3 IS NOT NULL`.
4. **Silver:** Eurostat `PCH_*` growth rates are excluded from `fact_tourism_arrivals` (only `NR` counts are included).
5. **Data:** `estat_tour_occ_arm` has high null rate in `tourism_value`; Gold does not impute missing values.
6. **Data:** Eurostat occupancy max = 105.9%; review methodology.

## Next Actions

1. Run `05 Gold Dimensions.ipynb` and `06 Gold Facts.ipynb` in Databricks.
2. Run `07 Gold Analytics.ipynb`.
3. Run `08 Gold Validation.ipynb` and update this report with live results.
4. Run `09 Power BI Preparation.ipynb`.
5. Update `docs/gold_schema.md`, `docs/powerbi_measures.md`, and `docs/powerbi_connection_guide.md` with live table counts.

---

## Live Validation Results (2026-11-21, Warehouse `699426b61c5cd41b`)

All queries are read-only. See `scripts/gold/11_gold_validation.ps1` and `scripts/gold/12_gold_duplicates.ps1`.

### Row Counts

| Table | Rows |
|---|---:|
| `dim_country` | 230 |
| `dim_date` | 482 |
| `fact_tourism_arrivals` | 277,478 |
| `fact_nights_spent` | 257,985 |
| `fact_hotel_performance` | 18,594 |
| `fact_hotel_occupancy` | 34,398 |
| `gold_yearly_arrivals_by_country` | 19,493 |
| `gold_monthly_arrivals_by_country` | 85,995 |
| `gold_tourism_growth_yearly` | 18,679 |
| `gold_tourism_growth_monthly` | 83,655 |
| `gold_destination_rankings` | 292 |
| `gold_tourism_seasonality` | 12 |
| `gold_nights_spent_trends` | 1,443 |
| `gold_hotel_capacity_trends` | 18,579 |
| `gold_hotel_occupancy_trends` | 17,199 |
| `gold_visitor_category_analysis` | 19,422 |
| `gold_country_comparison` | 8,274 |
| `gold_source_comparison` | 228 |
| `pbi_total_arrivals` | 7,077 |
| `pbi_avg_occupancy` | 17,199 |

### Duplicates

| Table | Full-grain duplicates |
|---|---:|
| `dim_country` | 0 |
| `fact_tourism_arrivals` | 0 |
| `fact_nights_spent` | 0 |

### Nulls

- `fact_tourism_arrivals.standardized_value`: 128,593 total — EUROSTAT 127,686; WORLD_BANK 907.
- `fact_nights_spent.standardized_value`: 124,554 — EUROSTAT.
- `fact_hotel_occupancy.occupancy_rate`: 16,013.
- `gold_tourism_growth_yearly.growth_pct`: 927 nulls.
- `gold_tourism_growth_monthly.growth_pct`: 39,410 nulls.

### Time Ranges

- `dim_date`: 1990-01-01 .. 2027-01-01.
- `gold_yearly_arrivals_by_country`: 1995 .. 2025.
- `gold_monthly_arrivals_by_country`: year 1990..2026, month 1..12.

### Referential Integrity

- `fact_tourism_arrivals.country_key` not in `dim_country`: 0
- `fact_nights_spent.country_key` not in `dim_country`: 0
- `fact_hotel_performance.country_key` not in `dim_country`: 0
- `fact_hotel_occupancy.country_key` not in `dim_country`: 0

### Primary Period Filter

- `fact_tourism_arrivals.is_primary_period = TRUE`: 61,866
- `gold_yearly_arrivals_by_country.is_primary_period = TRUE`: 5,706

### dim_country Canonicalization

- `dim_country` rows: 230 (was 300 before dedup).
- Duplicate `country_key` groups: 0 (was 64).
- Sample: `TUR` → `Turkiye`, `NLD` → `Netherlands (Kingdom of the)`, `GBR` → `United Kingdom of Great Britain and Northern Ireland`.
