# TourismPulse — Power BI Measures

**Date:** 2026-11-21  
**Gold tables:** `workspace.gold_layer.*`  
**Semantic model:** `docs/powerbi_semantic_model.md`

All measures below are null-safe and respect the source, frequency, unit, and category filters. Separate measures are defined for annual vs. monthly and for different visitor categories.

---

## 1. Global Overview Measures

### 1.1 Total International Arrivals (Annual)

```dax
Total International Arrivals :=
CALCULATE(
    SUM(fact_tourism_arrivals[standardized_value]),
    fact_tourism_arrivals[frequency] = "A",
    fact_tourism_arrivals[source_system] = SELECTEDVALUE(gold_yearly_arrivals_by_country[source_system], fact_tourism_arrivals[source_system])
)
```

Or simpler for use with `gold_yearly_arrivals_by_country`:

```dax
Total Annual Arrivals :=
SUM(gold_yearly_arrivals_by_country[arrivals])
```

### 1.2 Total International Arrivals (Monthly)

```dax
Total Monthly Arrivals :=
CALCULATE(
    SUM(fact_tourism_arrivals[standardized_value]),
    fact_tourism_arrivals[frequency] = "M",
    USERELATIONSHIP(fact_tourism_arrivals[country_key], dim_country[country_key])
)
```

### 1.3 Total Overnight Stays (Monthly)

```dax
Total Overnight Stays :=
CALCULATE(
    SUM(fact_tourism_arrivals[standardized_value]),
    fact_tourism_arrivals[frequency] = "M",
    fact_tourism_arrivals[visitor_category] = "Overnight visitors (tourists)"
)
```

### 1.4 Tourism Growth % (Yearly)

```dax
Tourism Growth % (Yearly) :=
VAR Curr = [Total Annual Arrivals]
VAR Prev =
    CALCULATE(
        [Total Annual Arrivals],
        DATEADD(dim_date[date], -1, YEAR)
    )
RETURN
    DIVIDE(Curr - Prev, Prev)
```

### 1.5 Tourism Growth % (Monthly)

```dax
Tourism Growth % (Monthly) :=
VAR Curr = [Total Monthly Arrivals]
VAR Prev =
    CALCULATE(
        [Total Monthly Arrivals],
        DATEADD(dim_date[date], -1, YEAR)
    )
RETURN
    DIVIDE(Curr - Prev, Prev)
```

---

## 2. Hotel Performance Measures

### 2.1 Hotel Establishments

```dax
Hotel Establishments :=
SUMX(
    FILTER(fact_hotel_performance, fact_hotel_performance[accommodation_metric] = "Establishments"),
    fact_hotel_performance[standardized_value]
)
```

### 2.2 Hotel Rooms

```dax
Hotel Rooms :=
SUMX(
    FILTER(fact_hotel_performance, fact_hotel_performance[accommodation_metric] = "Rooms"),
    fact_hotel_performance[standardized_value]
)
```

### 2.3 Bed Places

```dax
Bed Places :=
SUMX(
    FILTER(fact_hotel_performance, fact_hotel_performance[accommodation_metric] = "Bed places"),
    fact_hotel_performance[standardized_value]
)
```

### 2.4 Average Occupancy Rate (Average)

```dax
Average Occupancy Rate (Average) :=
AVERAGEX(fact_hotel_occupancy, fact_hotel_occupancy[occupancy_rate])
```

### 2.5 Average Occupancy Rate (Weighted)

```dax
Average Occupancy Rate (Weighted) :=
DIVIDE(
    SUMX(fact_hotel_occupancy, fact_hotel_occupancy[occupancy_rate] * [Bed Places]),
    SUM([Bed Places])
)
```

### 2.6 Night Time Stays (Total)

```dax
Night Time Stays (Total) :=
SUM(fact_nights_spent[standardized_value])
```

---

## 3. Ranking and Comparison Measures

### 3.1 Country Rank

```dax
Country Rank :=
RANKX(ALL(dim_country), [Total Annual Arrivals], , DESC, DENSE)
```

### 3.2 Country-wise Arrivals

```dax
Country Arrivals :=
SUM(gold_yearly_arrivals_by_country[arrivals])
```

### 3.3 Source-wise Arrivals

```dax
Source Arrivals (WB) :=
SUM(gold_source_comparison[world_bank_arrivals])
Source Arrivals (UN) :=
SUM(gold_source_comparison[un_arrivals])
Source Arrivals (Eurostat) :=
SUM(gold_source_comparison[estat_arrivals])
```

---

## 4. Data Quality Monitoring Measures

### 4.1 Row Counts

```dax
Fact Tourist Arrivals Count := COUNTROWS(fact_tourism_arrivals)
Fact Hotel Occupancy Count := COUNTROWS(fact_hotel_occupancy)
```

### 4.2 Missing Values

```dax
Missing Arrivals :=
CALCULATE(
    COUNTROWS(fact_tourism_arrivals),
    fact_tourism_arrivals[standardized_value] = BLANK()
)
Missing Occupancy :=
CALCULATE(
    COUNTROWS(fact_hotel_occupancy),
    fact_hotel_occupancy[occupancy_rate] = BLANK()
)
```

### 4.3 Coverage

```dax
Countries Covered :=
COUNTROWS(
    FILTER(dim_country, [Country Rank] <= 50)
)
```

---

## 5. Number Formatting

- **Arrivals / Nights / Rooms / Beds:** 0 decimals, millions/billions auto-scaled.
- **Occupancy Rate:** 2 decimals with `%`.
- **Growth %:** 2 decimals with `%`.
- **Country Rank:** integer.

## 6. General Rules

- Do not sum `Visitors (total)` with `Overnight visitors (tourists)` or `Same-day visitors (excursionists)`.
- Do not mix annual and monthly values in the same measure unless split.
- Do not sum occupancy percentages; use averages or weighted averages.
- Use `dim_date[is_primary_period]` to filter 2012–2019 by default.
- Respect `source_system`, `indicator_code`, and `unit` filters.
