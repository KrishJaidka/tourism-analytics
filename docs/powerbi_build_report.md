# TourismPulse — Power BI Build Report

**Date:** 2026-11-21  
**PBIP:** `C:\Users\Kaashvi\OneDrive\Documents\Default Project\tourism-analytics\TourismPulse_Gold.pbip`  
**Backup:** `C:\Users\Kaashvi\OneDrive\Documents\Default Project\tourism-analytics\TourismPulse_Gold_pbip_backup`
**Semantic model:** `TourismPulse_Gold.SemanticModel`  
**Report skeleton:** `TourismPulse_Gold.Report`  
**Power BI Desktop:** `C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe`

---

## 1. What was generated

| Item | Path |
|---|---|
| Power BI Project | `C:\Users\Kaashvi\OneDrive\Documents\Default Project\tourism-analytics\TourismPulse_Gold.pbip` |
| Semantic model | `TourismPulse_Gold.SemanticModel/definition/` |
| Report skeleton | `TourismPulse_Gold.Report/definition/` |
| 5 report pages | `TourismPulse_Gold.Report/definition/pages/` |

### Semantic model contents

- Tables: all 20 Gold tables from `workspace.gold_layer`.
- Relationships: 19 relationships from `docs/powerbi_semantic_model.md`.
- Measures: key DAX measures added to `fact_tourism_arrivals`, `fact_nights_spent`, `fact_hotel_performance`, `fact_hotel_occupancy`.

### Implemented visuals

The report definition now contains 34 visuals (`scripts/powerbi/add_visuals.py`). Visual JSON files are validated with `ConvertFrom-Json`.

#### Page1 — Tourism Overview

| Visual | Type | Content |
|---|---|---|
| `Page1_kpi_total_arrivals` | Card | Total Annual Arrivals |
| `Page1_kpi_monthly_arrivals` | Card | Total Monthly Arrivals |
| `Page1_kpi_nights_spent` | Card | Total Nights Spent |
| `Page1_kpi_yoy_growth` | Card | Tourism Growth % (Yearly) |
| `Page1_kpi_total_arrivals_yearly` | Card | Annual total arrivals |
| `Page1_line_annual_arrivals` | Line chart | Annual arrivals by year |
| `Page1_bar_top10_destinations` | Bar chart | Top destinations by arrivals |
| `Page1_slicer_country` | Slicer | Country |
| `Page1_slicer_year` | Slicer | Year |
| `Page1_slicer_source` | Slicer | Source system |
| `Page1_slicer_visitor_category` | Slicer | Visitor category |

#### Page2 — Country Comparison

| Visual | Type | Content |
|---|---|---|
| `Page2_bar_ranking` | Bar chart | Country ranking by arrivals |
| `Page2_table_country_arrivals` | Table | Country arrivals table |
| `Page2_line_growth_by_country` | Line chart | YoY growth by country/year |
| `Page2_slicer_country` | Slicer | Country |
| `Page2_slicer_year` | Slicer | Year |

#### Page3 — Monthly Trends

| Visual | Type | Content |
|---|---|---|
| `Page3_line_monthly_arrivals` | Line chart | Monthly arrivals by year |
| `Page3_bar_seasonality` | Bar chart | Average arrivals by month |
| `Page3_slicer_month` | Slicer | Month |
| `Page3_slicer_country` | Slicer | Country |
| `Page3_slicer_year` | Slicer | Year |

#### Page4 — Hotel Performance

| Visual | Type | Content |
|---|---|---|
| `Page4_kpi_hotel_establishments` | Card | Hotel Establishments |
| `Page4_kpi_hotel_rooms` | Card | Hotel Rooms |
| `Page4_kpi_bed_places` | Card | Bed Places |
| `Page4_line_occupancy` | Line chart | Occupancy rate by year/month |
| `Page4_table_occupancy_units` | Table | Occupancy by accommodation unit |
| `Page4_bar_occupancy_comparison` | Bar chart | Occupancy by accommodation metric |
| `Page4_slicer_country` | Slicer | Country |
| `Page4_slicer_year` | Slicer | Year |

#### Page5 — Data Quality Monitoring

| Visual | Type | Content |
|---|---|---|
| `Page5_table_source_counts` | Table | Source-wise record counts |
| `Page5_table_missing_values` | Table | Missing-value indicators |
| `Page5_table_nights_spent_nulls` | Table | Nights-spent nulls |
| `Page5_kpi_total_arrivals_quality` | Card | Total arrivals (quality page) |
| `Page5_slicer_year` | Slicer | Year |

#### Visual layout polish

- Premium tourism analytics theme applied: `TourismPulse_Gold.Report/RegisteredResources/Themes/tourism_pulse_theme.json` (deep navy, teal, light neutrals; Segoe UI; card/table styling).
- Report-level theme set in `definition/report.json` via `themeCollection` and `resourcePackages`.
- All 34 visual positions adjusted for clean page layouts: KPIs in rows, charts/tables in main areas, slicers at page bottom.
- Updated by `scripts/powerbi/polish_report.py`.

### Validation results

- `scripts/powerbi/validate_report.py`:
  - Visual reference validation: **None** (all 34 visuals reference fields/measures that exist in the semantic model).
  - Semantic model: 160 fields, 9 measures, 20 tables.
  - DAX checks:
    - `Tourism Growth % (Yearly)`: present and uses `DATEADD(dim_date[date], -1, YEAR)`.
    - `Tourism Growth % (Monthly)`: present and uses `DATEADD(dim_date[date], -1, YEAR)`.
- All `visual.json` files valid JSON (34 files).
- Power BI Desktop restarted with the updated PBIP.

### What is still required

- Formatted theme (colors, typography) and page navigation.
- Bookmarks/drill-throughs.
- Final screenshots to `docs/powerbi_screenshots/`.
- Manual verification in Power BI Desktop that visuals render and slicers filter correctly.

---

## 2. Open the report in Power BI Desktop

```powershell
Start-Process -FilePath "C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe" `
  -ArgumentList "C:\Users\Kaashvi\OneDrive\Documents\Default Project\tourism-analytics\TourismPulse_Gold.pbip"
```

The PBIP has been generated and Power BI Desktop has been launched with it. Verification: `Get-CimInstance Win32_Process` shows `PBIDesktop.exe` with the PBIP path in the command line:

```text
C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe
C:\Users\Kaashvi\OneDrive\Documents\Default Project\tourism-analytics\TourismPulse_Gold.pbip
```

If the project fails to open, see §5.

---

## 3. Connect to Databricks

If the semantic model is not already connected to Databricks:

1. In Power BI Desktop, click **File** > **Get Data** > **More**.
2. Select **Databricks** > **Databricks SQL Warehouse**.
3. Enter:
   - Server: `https://dbc-8409e0b7-429a.cloud.databricks.com`
   - Warehouse ID: `699426b61c5cd41b`
   - Authentication: **Personal Access Token (PAT)**.
4. Select schema: `workspace.gold_layer`.
5. Confirm the tables in the model.

**Do not paste the PAT into this document or chat.**

---

## 4. Build the five dashboard pages

Use `docs/powerbi_dashboard_specs.md` as the visual specification. For each page:

1. Open the page from the report page tabs.
2. Add visuals from the visualizations pane.
3. Drag fields from the field list to the visual.
4. Use the DAX measures in `docs/powerbi_measures.md` for calculations.
5. Apply slicers for Country, Year, Source, and Visitor Category.

### Recommended manual steps

- **Page 1 — Tourism Overview:** Add KPI cards (Total Arrivals, YoY Growth, Top Destination), trend charts, and a map.
- **Page 2 — Country Comparison:** Add rankings, growth by country, and source comparisons.
- **Page 3 — Monthly Trends:** Add monthly arrivals/nights line charts and seasonality.
- **Page 4 — Hotel Performance:** Add establishments, rooms, bed places, occupancy, and stay metrics.
- **Page 5 — Data Quality Monitoring:** Add counts, nulls, duplicates, and coverage metrics.

---

## 5. Validation checklist before reporting complete

1. All 5 pages exist and are visible in Power BI Desktop.
2. All visuals reference correct Gold tables/measures.
3. DAX measures return sensible values (run against connected Databricks).
4. Slicers work (Country, Year, Source, Visitor Category).
5. No incompatible data is being combined (annual vs monthly, percentages vs counts).
6. Save the report as `TourismPulse_Gold.pbix` in the repo.
7. Take screenshots to `docs/powerbi_screenshots/`.
8. Verify `TourismPulse_Gold.pbip` opens in Power BI Desktop without errors.

---

## 6. What is still required

The following are **not** in the PBIP yet:

- Visuals on the 5 pages.
- Data model connection to Databricks (if not connected).
- Formatted theme (colors, typography).
- Navigation between pages.
- Bookmarks/drill-throughs.
- Final screenshots.

---

## 7. Troubleshooting

If Power BI Desktop cannot open the project:

1. Check that the `TourismPulse_Gold.pbip` file and folders exist.
2. Restart Power BI Desktop.
3. Verify the file encodings are UTF-8 without BOM.
4. Ask for assistance; do not delete the project files.

---

*End of Power BI build report.*
