# TourismPulse — Power BI Dashboard Specifications

**Date:** 2026-11-21  
**Pages:** 5  
**Data model:** `docs/powerbi_semantic_model.md`  
**Measures:** `docs/powerbi_measures.md`

All visuals use the validated Gold tables. Design follows a professional analytics-dashboard style.

---

## Page 1 — Tourism Overview

**Purpose:** High-level view of TourismPulse performance.

### Visuals
1. **KPI Cards** (4):
   - **Total International Arrivals** (annual, `SUM(gold_yearly_arrivals_by_country[arrivals])`).
   - **Tourism Growth %** (latest year, `Tourism Growth % (Yearly)`).
   - **Countries Covered** (`Country Rank <= 50`, `COUNTROWS(dim_country)`).
   - **Top Destination** (`gold_destination_rankings` sorted desc, top 1).
2. **Top 10 Destinations by Arrivals** (Bar chart, `gold_yearly_arrivals_by_country`).
3. **Arrivals Trend (Line)** (`Total Annual Arrivals` by `dim_date[year]`, annual).
4. **Arrivals by Year and Country** (Matrix or stacked column, `fact_tourism_arrivals`).
5. **Geographic Distribution** (Map, `fact_tourism_arrivals` filtered to `frequency='A'`, values by `dim_country[country_name]`).
6. **Slicers:** Country, Year, Source, Visitor Category.

**Design:** Clean hero section with KPI cards, then trend/map. Use `dim_date[is_primary_period]` default filter to 2012–2019.

---

## Page 2 — Country Comparison

**Purpose:** Compare countries by arrivals, growth, and source-specific measurements.

### Visuals
1. **Country Rankings** (Table/Matrix, `gold_destination_rankings` sorted by `total_arrivals`, columns: Country, Arrivals).
2. **Country Arrivals (Bar, top N)** (`Country Arrivals` by Country).
3. **Year-over-Year Growth by Country (Line/Bar)** (`Tourism Growth % (Yearly)` by Country/Year).
4. **Source Comparison (Waterfall or column chart)** (World Bank / UN / Eurostat arrivals by Country).
5. **Source Comparison Discrepancy** (`gold_source_comparison` columns: Country, WB arrivals, UN arrivals, Eurostat arrivals).
6. **Country Trend by Year (Line)** (`gold_yearly_arrivals_by_country[arrivals]` by Country/Year).

**Design:** Use synchronized slicers: Country, Year, Source, Visitor Category. Avoid mixing percentages and absolute counts in the same visual.

---

## Page 3 — Monthly Trends

**Purpose:** Monthly tourism activity, seasonality, and trend analysis.

### Visuals
1. **Monthly Arrivals (Line)** (`Total Monthly Arrivals` by `dim_date[year_month]`).
2. **Monthly Nights Spent (Line)** (`SUM(fact_nights_spent[standardized_value])` by Year/Month).
3. **Seasonality Heatmap** (`gold_tourism_seasonality[avg_arrivals]` by Month, with month names).
4. **Peak/Lowest Months (Bar)** (`gold_tourism_seasonality[peak_arrivals]` and `[lowest_arrivals]`).
5. **Monthly Growth % (Line)** (`Tourism Growth % (Monthly)` by Year/Month).
6. **Country Filter + Year Filter + Month Slicer.**

**Rules:** Use only monthly data. No derived monthly values from annual sources. Filter to 2012–2019 by default for comparable periods.

---

## Page 4 — Hotel Performance

**Purpose:** Hotel capacity, occupancy, and average stay analysis.

### Visuals
1. **Hotel Establishments (Line/Bar)** (`Hotel Establishments` by Year).
2. **Hotel Rooms (Bar)** (`Hotel Rooms` by Year).
3. **Bed Places (Bar)** (`Bed Places` by Year).
4. **Bed-Place Occupancy Rate (Line)** (`Average Occupancy Rate (Weighted)` for `accommodation_unit='BEDPL'`).
5. **Bedroom Occupancy Rate (Line)** (`Average Occupancy Rate (Weighted)` for `accommodation_unit='BEDRM'`).
6. **Average Length of Stay (Bar)** (`SUM(fact_nights_spent[standardized_value]) / 12` or `AVG(fact_hotel_performance[standardized_value])` filtered to `accommodation_metric='Average length of stay'`).
7. **Country and Year Comparisons** (Stacked bar: establishments/rooms/bed places by Country).

**Design:** Keep occupancy metrics separate. Use clear labels: “Bed-Place Occupancy” vs “Bedroom Occupancy”.

---

## Page 5 — Data Quality Monitoring

**Purpose:** Validate Gold tables and highlight data issues.

### Visuals
1. **Table Row Counts (Table/Matrix)**:
   - `Fact Tourist Arrivals Count`
   - `Fact Hotel Occupancy Count`
   - `Countries Covered`
2. **Missing Values (Table)**:
   - `Missing Arrivals`
   - `Missing Occupancy`
3. **Duplicate Records (Table)**:
   - `dim_country` duplicates (should be 0).
   - `fact_tourism_arrivals` full-grain duplicates (should be 0).
   - `fact_nights_spent` full-grain duplicates (should be 0).
4. **Coverage by Source/Year (Matrix)**:
   - Source: WB/UN/Eurostat.
   - Year range covered by each Gold table.
5. **Validation Status (KPI Cards)**:
   - `dim_country` duplicates: 0.
   - `fact_tourism_arrivals` full-grain duplicates: 0.
   - `fact_nights_spent` full-grain duplicates: 0.
   - `Referential Integrity Errors`: 0.
6. **Growth Table Nulls (Table)**:
   - `gold_tourism_growth_yearly.growth_pct` nulls.
   - `gold_tourism_growth_monthly.growth_pct` nulls.

**Design:** Use red/green status indicators for validation checks. Include tooltips explaining what each metric means.

---

## Visual Design Guidelines

- **Typography:** Use a professional sans-serif (e.g., Segoe UI / Helvetica / Inter).
- **Color palette:** Navy, teal, and gray for a modern professional look; avoid clutter.
- **KPIs:** Large-card format with values and trend arrows where applicable.
- **Slicers:** Keep the number of slicers per page to 5 or fewer.
- **Maps:** Use `dim_country[country_name]` for map visuals.
- **Tooltips:** Add helpful tooltips for less intuitive measures.
- **Drill-through:** Provide drill-through from Country to Year, then to Month.

## Page Navigation

- Tab/Tile navigation across the five pages.
- Breadcrumb: [Tourism Overview] > [Destination Intelligence] > [Tourism Seasonality] > [Hotel Performance] > [Data Quality Monitoring].

---

*End of dashboard specifications.*
