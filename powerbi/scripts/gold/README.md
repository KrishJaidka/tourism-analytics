# TourismPulse — Gold Layer SQL Scripts

These SQL scripts implement the Gold layer in a SQL Warehouse-compatible way, using Unity Catalog naming (`workspace.gold_layer.*`). They mirror the Gold notebooks (`05 Gold Dimensions.ipynb` … `09 Power BI Preparation.ipynb`).

## Execution

Run the proposed execution script in order (it creates the schema first):

```powershell
.\00_execute_gold.ps1
```

This script executes:

1. `01_dim_country.sql`
2. `02_dim_date.sql`
3. `03_fact_tourism_arrivals.sql`
4. `04_fact_nights_spent.sql`
5. `05_fact_hotel_performance.sql`
6. `06_fact_hotel_occupancy.sql`
7. `07_gold_analytics.sql`
8. `08_gold_source_comparison.sql`
9. `09_powerbi_preparation.sql`

It uses Databricks CLI profile `TOURISMPULSE` and Warehouse ID `699426b61c5cd41b`. It does not execute anything until run and approved.

## Notes

- Tables are written to `workspace.gold_layer.*`, not to `/Volumes/.../gold_layer/`.
- `country_key` is the ISO3 string for countries in all Gold tables.
- Silver tables are read directly from `/Volumes/.../silver_layer/`.
- See `docs/technical_review.md` for the full review and risk analysis.
- See `docs/gold_schema.md` for the full Gold schema.
