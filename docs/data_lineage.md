# TourismPulse — Data Lineage

**Date:** 2026-11-21  
**Repository:** `tourism-analytics` @ `main` (`9a13376`)  
**Volume:** `/Volumes/workspace/default/tourismdata/`

## End-to-End Lineage

```
Raw files (bronze_layer inputs)
  ├── UN_Tourism_accommodation_hotels_raw.csv      → bronze_un_tourism_accommodation_hotels_raw → Silver: un_tourism_accommodation_hotels → Gold: fact_hotel_performance, fact_tourism_arrivals? (no, separate)
  ├── UN_Tourism_inbound_arrivals_raw.csv          → bronze_un_tourism_inbound_arrivals_raw        → Silver: un_tourism_inbound_arrivals          → Gold: fact_tourism_arrivals
  ├── estat_tour_occ_arm_raw.tsv                   → bronze_estat_tour_occ_arm_raw                  → Silver: estat_tour_occ_arm                   → Gold: fact_tourism_arrivals, fact_nights_spent? (arm only; nim is nights)
  ├── estat_tour_occ_mnor_raw.tsv                  → bronze_estat_tour_occ_mnor_raw                 → Silver: estat_tour_occ_mnor                  → Gold: fact_hotel_occupancy
  ├── estat_tour_occ_nim_raw.tsv                   → bronze_estat_tour_occ_nim_raw                  → Silver: estat_tour_occ_nim                   → Gold: fact_nights_spent
  └── world_bank_internatinal_arrival_raw.csv      → bronze_world_bank_internatinal_arrival_raw    → Silver: world_bank_international_arrivals   → Gold: fact_tourism_arrivals
```

## Gold → Power BI

```
dim_country   → Power BI dimension
dim_date      → Power BI dimension
fact_tourism_arrivals → Power BI fact (pbi_total_arrivals)
fact_nights_spent     → Power BI fact (nights trends)
fact_hotel_performance→ Power BI fact (hotel capacity)
fact_hotel_occupancy  → Power BI fact (occupancy rates)
gold_* tables         → Power BI semantic model (Star Schema)
```

## Per-Source Gold Mapping

| Source | Silver Table | Gold Tables |
|---|---|---|
| World Bank | `world_bank_international_arrivals` | `fact_tourism_arrivals` (annual) |
| UN Tourism | `un_tourism_inbound_arrivals` | `fact_tourism_arrivals` (annual) |
| UN Tourism | `un_tourism_accommodation_hotels` | `fact_hotel_performance` (annual) |
| Eurostat | `estat_tour_occ_arm` | `fact_tourism_arrivals` (monthly, NR only) |
| Eurostat | `estat_tour_occ_nim` | `fact_nights_spent` (monthly, NR only) |
| Eurostat | `estat_tour_occ_mnor` | `fact_hotel_occupancy` (monthly, BEDPL/BEDRM) |

## Provenance and Reconciliation

- `fact_tourism_arrivals` retains `source_system`, `indicator_code`, `visitor_category`, and original values/units.
- `fact_hotel_performance` retains indicator codes and units (`units`, `percent`, `overnights`).
- No cross-source additive totals are created where definitions differ (e.g., UN total visitors vs. components; World Bank vs. Eurostat; UN vs. Eurostat).
- Country mapping is tracked via `dim_country.mapping_status` (`MAPPED_COUNTRY`, `MAPPED_AGGREGATE`, `SPECIAL_GEOGRAPHY`, `UNMAPPED`).

## Notes

- Annual and monthly observations are not merged; `frequency` distinguishes them.
- Primary analysis period: 2012–2019 (`is_primary_period` on facts and dims).
- Full historical data is retained in Silver and Gold.
