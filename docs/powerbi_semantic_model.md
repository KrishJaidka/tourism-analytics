# TourismPulse — Power BI Semantic Model

**Date:** 2026-11-21  
**Gold schema:** `workspace.gold_layer`  
**Warehouse:** `699426b61c5cd41b` (Serverless Starter Warehouse)  
**Status:** Semantic model documented; Power BI Desktop installed at `C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe`. The PBIP is generated at `TourismPulse_Gold.pbip` (see `docs/powerbi_build_report.md`).

---

## 1. Tables

| Table | Type | Key | Notes |
|---|---|---|---|
| `dim_country` | Dimension | `country_key` (ISO3) | Canonicalized; 230 rows; no duplicates. |
| `dim_date` | Dimension | `date_key` | Monthly `YYYYMMDD`, annual year keys (1990–2027). |
| `fact_tourism_arrivals` | Fact | `country_key, geo_code, year, month, date_key, frequency, source_system, indicator_code, visitor_category, residence_category, accommodation_category` | Full grain; 0 duplicates. |
| `fact_nights_spent` | Fact | `country_key, geo_code, year, month, date_key, residence_category, activity_category, source_system` | Full grain; 0 duplicates. |
| `fact_hotel_performance` | Fact | `country_key, geo_code, year, date_key, indicator_code` | UN accommodation metrics. |
| `fact_hotel_occupancy` | Fact | `country_key, geo_code, year, month, date_key, accommodation_unit` | BEDPL/BEDRM separate. |
| `gold_yearly_arrivals_by_country` | Gold | `country_key, year, source_system, indicator_code, visitor_category` | Annual arrivals. |
| `gold_monthly_arrivals_by_country` | Gold | `country_key, year, month, source_system, indicator_code, visitor_category` | Monthly arrivals. |
| `gold_tourism_growth_yearly` | Gold | `country_key, year, source_system, indicator_code, visitor_category` | YoY growth. |
| `gold_tourism_growth_monthly` | Gold | `country_key, year, month, source_system, indicator_code, visitor_category` | YoY monthly growth. |
| `gold_destination_rankings` | Gold | `country_key` | Top destinations. |
| `gold_tourism_seasonality` | Gold | `month` | Monthly average/median/peak arrivals. |
| `gold_nights_spent_trends` | Gold | `country_key, year` | Total nights per country/year. |
| `gold_hotel_capacity_trends` | Gold | `country_key, year, accommodation_metric` | establishments/rooms/bed places. |
| `gold_hotel_occupancy_trends` | Gold | `country_key, year, month` | Average occupancy rate. |
| `gold_visitor_category_analysis` | Gold | `country_key, year, visitor_category` | Overnight/excursionist composition. |
| `gold_country_comparison` | Gold | `country_key, year` | Country-level arrivals. |
| `gold_source_comparison` | Gold | `country_key` | Cross-source comparison. |
| `pbi_total_arrivals` | Gold | `country_key, year` | DAX-ready annual arrivals. |
| `pbi_avg_occupancy` | Gold | `country_key, year, month` | DAX-ready average occupancy. |

---

## 2. Relationships

| From | To | Relationship | Cardinality | Cross-filter |
|---|---|---|---|---|
| `dim_country` | `fact_tourism_arrivals` | `country_key` | 1:* | Bi-directional |
| `dim_country` | `fact_nights_spent` | `country_key` | 1:* | Bi-directional |
| `dim_country` | `fact_hotel_performance` | `country_key` | 1:* | Bi-directional |
| `dim_country` | `fact_hotel_occupancy` | `country_key` | 1:* | Bi-directional |
| `dim_date` | `fact_tourism_arrivals` | `date_key` | 1:* | Bi-directional |
| `dim_date` | `fact_nights_spent` | `date_key` | 1:* | Bi-directional |
| `dim_date` | `fact_hotel_occupancy` | `date_key` | 1:* | Bi-directional |
| `fact_tourism_arrivals` | `gold_yearly_arrivals_by_country` | `country_key, year, source_system, indicator_code, visitor_category` | 1:1 | Bi-directional |
| `fact_tourism_arrivals` | `gold_monthly_arrivals_by_country` | `country_key, year, month, source_system, indicator_code, visitor_category` | 1:1 | Bi-directional |
| `fact_tourism_arrivals` | `gold_tourism_growth_yearly` | `country_key, year, source_system, indicator_code, visitor_category` | 1:* | Bi-directional |
| `fact_tourism_arrivals` | `gold_tourism_growth_monthly` | `country_key, year, month, source_system, indicator_code, visitor_category` | 1:* | Bi-directional |
| `fact_tourism_arrivals` | `gold_visitor_category_analysis` | `country_key, year, visitor_category` | 1:1 | Bi-directional |
| `fact_nights_spent` | `gold_nights_spent_trends` | `country_key, year` | 1:1 | Bi-directional |
| `fact_hotel_performance` | `gold_hotel_capacity_trends` | `country_key, year, accommodation_metric` | 1:1 | Bi-directional |
| `fact_hotel_occupancy` | `gold_hotel_occupancy_trends` | `country_key, year, month` | 1:1 | Bi-directional |
| `gold_yearly_arrivals_by_country` | `gold_destination_rankings` | `country_key, year` | 1:1 | Bi-directional |
| `gold_yearly_arrivals_by_country` | `gold_country_comparison` | `country_key, year, source_system` | 1:1 | Bi-directional |
| `fact_tourism_arrivals` | `pbi_total_arrivals` | `country_key, year` | 1:1 | Bi-directional |
| `fact_hotel_occupancy` | `pbi_avg_occupancy` | `country_key, year, month` | 1:1 | Bi-directional |

**Avoiding ambiguous joins:**
- All facts use ISO3 `country_key`; `dim_country` is canonicalized with 0 duplicate keys.
- Growth tables are joined to their parent fact/analytical tables on the full grain.
- Do not join `fact_tourism_arrivals` to `gold_yearly_arrivals_by_country` directly unless you aggregate first.
- Do not join annual and monthly facts on `year` alone; use `date_key` or `frequency` + `year` + `month`.

---

## 3. DAX Measures

See `docs/powerbi_measures.md` for detailed DAX definitions. The most important measures:

| Measure | Definition |
|---|---|
| **Total International Arrivals** | `SUMX(fact_tourism_arrivals, standardized_value)` filtered to `frequency='A'` |
| **Total Overnight Stays** | `SUMX(fact_tourism_arrivals, standardized_value)` filtered to `visitor_category='Overnight visitors (tourists)'` and `frequency='M'` |
| **Tourism Growth %** | `DIVIDE(curr - prev, prev)` using `gold_tourism_growth_yearly` |
| **Average Hotel Occupancy** | `AVERAGEX(fact_hotel_occupancy, occupancy_rate)` |
| **Country Rank** | `RANKX(ALL(dim_country), [Total International Arrivals], , DESC)` |
| **Hotel Capacity** | `SUMX(fact_hotel_performance, standardized_value)` filtered by metric (Establishments, Rooms, Bed places) |

All DAX measures are null-safe and respect source/frequency/unit filters.

---

## 4. Dashboard Structure (high level)

See `docs/powerbi_dashboard_specs.md` for the five dashboard pages.
