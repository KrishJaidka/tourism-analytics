# TourismPulse — Power BI Connection Guide

**Date:** 2026-11-21  
**Gold tables:** `workspace.gold_layer.*`  
**Warehouse:** `699426b61c5cd41b` (Serverless Starter Warehouse)  
**Workspace:** `https://dbc-8409e0b7-429a.cloud.databricks.com/` (org `7474653857041139`)

> **Note:** Power BI Desktop is installed at `C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe`. Use the connection steps below to build the report. Save the final report as `TourismPulse_Gold.pbix` or `TourismPulse_Gold.pbip`.

---

## 1. Check for a SQL Warehouse

Use the Databricks UI:

- Left nav → **SQL Warehouses**.
- Warehouse: **Serverless Starter Warehouse**, ID `699426b61c5cd41b`, status **STOPPED** (auto-resumes when used).

The existing SQL Warehouse is sufficient. Databricks Power BI connectors:

1. **Databricks SQL Warehouse connector** (recommended).
2. **Databricks Unity Catalog (catalog/schema/table) connector**.

---

## 2. Connect Power BI to Databricks (SQL Warehouse)

### 2.1 In Power BI Desktop (on a machine with Power BI installed)

1. Get Data → **Databricks** → **Databricks SQL Warehouse**.
2. Enter:
   - Server: `https://dbc-8409e0b7-429a.cloud.databricks.com`
   - Warehouse ID: `699426b61c5cd41b`
   - Authentication: **Personal Access Token (PAT)**.
3. Select schema: **`workspace.gold_layer`**.
4. Import the Gold tables below.

### 2.2 SQL used by the connectors

```sql
-- Dimensions
SELECT * FROM workspace.gold_layer.dim_country;
SELECT * FROM workspace.gold_layer.dim_date;

-- Facts
SELECT * FROM workspace.gold_layer.fact_tourism_arrivals;
SELECT * FROM workspace.gold_layer.fact_nights_spent;
SELECT * FROM workspace.gold_layer.fact_hotel_performance;
SELECT * FROM workspace.gold_layer.fact_hotel_occupancy;

-- Gold analytics
SELECT * FROM workspace.gold_layer.gold_yearly_arrivals_by_country;
SELECT * FROM workspace.gold_layer.gold_monthly_arrivals_by_country;
SELECT * FROM workspace.gold_layer.gold_tourism_growth_yearly;
SELECT * FROM workspace.gold_layer.gold_tourism_growth_monthly;
SELECT * FROM workspace.gold_layer.gold_destination_rankings;
SELECT * FROM workspace.gold_layer.gold_tourism_seasonality;
SELECT * FROM workspace.gold_layer.gold_nights_spent_trends;
SELECT * FROM workspace.gold_layer.gold_hotel_capacity_trends;
SELECT * FROM workspace.gold_layer.gold_hotel_occupancy_trends;
SELECT * FROM workspace.gold_layer.gold_visitor_category_analysis;
SELECT * FROM workspace.gold_layer.gold_country_comparison;
SELECT * FROM workspace.gold_layer.gold_source_comparison;

-- Power BI-ready tables
SELECT * FROM workspace.gold_layer.pbi_total_arrivals;
SELECT * FROM workspace.gold_layer.pbi_avg_occupancy;
```

---

## 3. Connect via Unity Catalog (Alternative)

If you prefer a push dataset:

1. Get Data → **Databricks** → **Unity Catalog**.
2. Enter the same host/workspace.
3. Authenticate with PAT.
4. Browse `workspace.gold_layer` and import the tables above.

---

## 4. Install Power BI Desktop

Power BI Desktop is installed via Winget:

```powershell
winget install --id Microsoft.PowerBI --exact --source winget --accept-package-agreements --accept-source-agreements
```

Installed at `C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe`. Run the steps in §2 now that it is installed.

---

## 5. Security Notes

- Never paste access tokens into documentation or chat.
- Store PATs in a secure credential manager.
- Use a PAT with minimal scope.
- The PAT used for the audit should be rotated after use.

---

## 6. Deliverables

Once Power BI Desktop is installed:

1. Connect using §2.
2. Import all tables from §2.2.
3. Build the five dashboard pages per `docs/powerbi_dashboard_specs.md`.
4. Add the DAX measures from `docs/powerbi_measures.md`.
5. Save the report as `TourismPulse_Gold.pbix` or `TourismPulse_Gold.pbip`.
6. Take screenshots and save them to `docs/powerbi_screenshots/`.
