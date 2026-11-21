# TourismPulse — Technical Review of Gold Layer Execution Plan

**Date:** 2026-11-21  
**Audience:** Execution team  
**Scope:** Review of Gold notebooks/SQL scripts, Silver source verification, SQL Warehouse compatibility, Unity Catalog architecture, dependencies, and execution plan. **No execution performed.**

---

## 1. Inspection Summary

### 1.1 Gold artifacts inspected

| Artifact | Inspected | Notes |
|---|---|---|
| `05 Gold Dimensions.ipynb` | Yes | Uses PySpark; writes to `gold_path` volume paths. |
| `06 Gold Facts.ipynb` | Yes | Uses PySpark; writes to `gold_path` volume paths. |
| `07 Gold Analytics.ipynb` | Yes | Uses PySpark; writes to `gold_path` volume paths. |
| `08 Gold Validation.ipynb` | Yes | Uses PySpark; reads `gold_path` tables. |
| `09 Power BI Preparation.ipynb` | Yes | Uses PySpark; writes to `gold_path` volume paths. |
| `scripts/gold/01_dim_country.sql` | Yes | SQL Warehouse compatible, Unity Catalog naming, ISO3 keys. |
| `scripts/gold/02_dim_date.sql` | Yes | SQL Warehouse compatible, Unity Catalog naming. |
| `scripts/gold/03_fact_tourism_arrivals.sql` | Yes | SQL Warehouse compatible, Unity Catalog naming, ISO3 keys. |
| `scripts/gold/04_fact_nights_spent.sql` | Yes | SQL Warehouse compatible, Unity Catalog naming. |
| `scripts/gold/05_fact_hotel_performance.sql` | Yes | SQL Warehouse compatible, Unity Catalog naming. |
| `scripts/gold/06_fact_hotel_occupancy.sql` | Yes | SQL Warehouse compatible, Unity Catalog naming. |
| `scripts/gold/07_gold_analytics.sql` | Yes | SQL Warehouse compatible, Unity Catalog naming. |
| `scripts/gold/08_gold_source_comparison.sql` | Yes | SQL Warehouse compatible, Unity Catalog naming. |
| `scripts/gold/09_powerbi_preparation.sql` | Yes | SQL Warehouse compatible, Unity Catalog naming. |
| `scripts/gold/00_execute_gold.ps1` | Yes | Proposed execution script. |

### 1.2 Silver source verification (read-only via SQL API, Warehouse `699426b61c5cd41b`)

| Silver table | Rows (verified) |
|---|---:|
| `estat_tour_occ_arm` | 895,230 |
| `estat_tour_occ_mnor` | 37,926 |
| `estat_tour_occ_nim` | 893,466 |
| `un_tourism_accommodation_hotels` | 18,594 |
| `un_tourism_inbound_arrivals` | 13,903 |
| `world_bank_international_arrivals` | 6,916 |

All six Silver tables are accessible via Databricks SQL Warehouse.

### 1.3 Unity Catalog architecture (verified via UC API)

- Catalog: `workspace`
- Schemas in `workspace`: `default`, `information_schema`
- **No `gold_layer` schema exists yet.**
- Recommended: create schema `gold_layer` in catalog `workspace` and use `workspace.gold_layer.*` table names for Gold Delta tables.
- **Do not create Delta tables under `/Volumes/workspace/default/tourismdata/gold_layer/`** (as the user instructed).

---

## 2. SQL Warehouse Compatibility Findings

The corrected SQL scripts in `scripts/gold/` are compatible with Databricks SQL Warehouse:

| Artifact | Compatibility | Notes |
|---|---|---|
| `01_dim_country.sql` | Compatible | Uses ISO3 strings as `country_key`; no `pycountry`. |
| `02_dim_date.sql` | Compatible | Uses `sequence`, `explode`, `date_format`, `MONTHNAME`, `QUARTER`. |
| `03_fact_tourism_arrivals.sql` | Compatible | Uses `YEAR()`, `MONTH()`, `CASE WHEN`, `UNION ALL`, `CREATE OR REPLACE TABLE`. |
| `04_fact_nights_spent.sql` | Compatible | Same as above. |
| `05_fact_hotel_performance.sql` | Compatible | Uses ISO3 `country_key`. |
| `06_fact_hotel_occupancy.sql` | Compatible | Uses `YEAR()`, `MONTH()`. |
| `07_gold_analytics.sql` | Compatible | Uses `MAX` instead of `FIRST`; `PERCENTILE_APPROX` instead of `MEDIAN`. |
| `08_gold_source_comparison.sql` | Compatible | Uses `FULL OUTER JOIN`, `GREATEST`. |
| `09_powerbi_preparation.sql` | Compatible | Uses `SUM`, `AVG`. |

Previously incompatible items are now resolved:

- `pycountry` removed from `dim_country`.
- `period.year` / `period.month` replaced with `YEAR(period)` / `MONTH(period)`.
- `FIRST` replaced with `MAX`.
- `MEDIAN` replaced with `PERCENTILE_APPROX(x, 0.5)`.
- Volume paths replaced with `workspace.gold_layer.*`.

---

## 3. Key Schema Decision

`dim_country.country_key` is the **ISO3 string** for countries (e.g., `USA`, `DEU`, `KEN`). Aggregates use descriptive surrogate keys (e.g., `WORLD`, `AFR`). This is consistent across `dim_country`, facts, and analytics.

---

## 4. Dependencies and Execution Order

```
00_execute_gold.ps1 (creates schema workspace.gold_layer)
01_dim_country.sql               (dim_country; depends on Silver: un_tourism_inbound_arrivals, un_tourism_accommodation_hotels, estat_tour_occ_arm, world_bank_international_arrivals)
02_dim_date.sql                  (dim_date; no dependencies)
03_fact_tourism_arrivals.sql     (fact_tourism_arrivals; depends on dim_country, dim_date, Silver: world_bank_international_arrivals, un_tourism_inbound_arrivals, estat_tour_occ_arm)
04_fact_nights_spent.sql         (fact_nights_spent; depends on dim_country, dim_date, Silver: estat_tour_occ_nim)
05_fact_hotel_performance.sql    (fact_hotel_performance; depends on dim_country, dim_date, Silver: un_tourism_accommodation_hotels)
06_fact_hotel_occupancy.sql      (fact_hotel_occupancy; depends on dim_country, dim_date, Silver: estat_tour_occ_mnor)
07_gold_analytics.sql            (gold_yearly_arrivals_by_country, gold_monthly_arrivals_by_country, gold_tourism_growth_yearly, gold_tourism_growth_monthly, gold_destination_rankings, gold_tourism_seasonality, gold_nights_spent_trends, gold_hotel_capacity_trends, gold_hotel_occupancy_trends, gold_visitor_category_analysis, gold_country_comparison; depends on facts and dim_date)
08_gold_source_comparison.sql    (gold_source_comparison; depends on Silver tables)
09_powerbi_preparation.sql       (pbi_total_arrivals, pbi_avg_occupancy; depends on fact_tourism_arrivals, fact_hotel_occupancy)
```

---

## 5. Proposed Execution Script

**`scripts/gold/00_execute_gold.ps1`**

The script:

1. Creates schema `workspace.gold_layer`.
2. Executes SQL files in the order above via the Databricks SQL API on Warehouse `699426b61c5cd41b`.
3. Prints `OK` or the failure message per file.
4. Does **not** execute anything yet.

---

## 6. Tables to be Created (Proposed)

| Table | Schema | Type |
|---|---|---|
| `dim_country` | `workspace.gold_layer` | Dimension |
| `dim_date` | `workspace.gold_layer` | Dimension |
| `fact_tourism_arrivals` | `workspace.gold_layer` | Fact |
| `fact_nights_spent` | `workspace.gold_layer` | Fact |
| `fact_hotel_performance` | `workspace.gold_layer` | Fact |
| `fact_hotel_occupancy` | `workspace.gold_layer` | Fact |
| `gold_yearly_arrivals_by_country` | `workspace.gold_layer` | Gold |
| `gold_monthly_arrivals_by_country` | `workspace.gold_layer` | Gold |
| `gold_tourism_growth_yearly` | `workspace.gold_layer` | Gold |
| `gold_tourism_growth_monthly` | `workspace.gold_layer` | Gold |
| `gold_destination_rankings` | `workspace.gold_layer` | Gold |
| `gold_tourism_seasonality` | `workspace.gold_layer` | Gold |
| `gold_nights_spent_trends` | `workspace.gold_layer` | Gold |
| `gold_hotel_capacity_trends` | `workspace.gold_layer` | Gold |
| `gold_hotel_occupancy_trends` | `workspace.gold_layer` | Gold |
| `gold_visitor_category_analysis` | `workspace.gold_layer` | Gold |
| `gold_country_comparison` | `workspace.gold_layer` | Gold |
| `gold_source_comparison` | `workspace.gold_layer` | Gold |
| `pbi_total_arrivals` | `workspace.gold_layer` | Power BI prep |
| `pbi_avg_occupancy` | `workspace.gold_layer` | Power BI prep |

---

## 7. Tables to be Modified

None. All Gold tables are new. No existing Silver or volume tables will be modified.

---

## 8. Risks to Existing Data

- The Serverless Starter Warehouse is currently **STOPPED**; it will auto-resume on first use.
- `CREATE OR REPLACE TABLE` on Gold tables is idempotent but destructive if tables already exist; verify before approval.
- If `gold_layer` schema is created, it becomes a new Unity Catalog schema; no existing data is affected.
- SQL scripts use `CREATE OR REPLACE TABLE`; if any target table name conflicts with an existing object in `workspace.gold_layer`, it will be replaced.

---

## 9. Recommended Next Steps

1. Review and approve the proposed execution script (`scripts/gold/00_execute_gold.ps1`).
2. Approve creation of `workspace.gold_layer` schema.
3. Approve execution of corrected SQL on Warehouse `699426b61c5cd41b`.
4. After execution, verify:
   - Schema of each Gold table via `SHOW TABLES` / `DESCRIBE`.
   - Row counts via `SELECT COUNT(*)`.
   - Referential integrity between `dim_country.country_key` and fact tables.
5. Proceed to Power BI Dashboard Phase.

---

*End of Technical Review.*
