-- TourismPulse — Gold analytical tables (SQL Warehouse compatible, Unity Catalog naming)
-- Assumes facts and dim_date exist in workspace.gold_layer.

-- 1) gold_yearly_arrivals_by_country
CREATE OR REPLACE TABLE workspace.gold_layer.gold_yearly_arrivals_by_country AS
SELECT
  fa.country_key,
  fa.geo_code,
  fa.country_name,
  fa.year,
  fa.source_system,
  fa.indicator_code,
  fa.visitor_category,
  SUM(fa.standardized_value) AS arrivals,
  MAX(fa.standardized_unit) AS unit,
  MAX(dd.is_primary_period) AS is_primary_period
FROM workspace.gold_layer.fact_tourism_arrivals fa
LEFT JOIN workspace.gold_layer.dim_date dd
  ON dd.year = fa.year AND dd.month IS NULL
WHERE fa.frequency = 'A'
GROUP BY fa.country_key, fa.geo_code, fa.country_name, fa.year, fa.source_system,
         fa.indicator_code, fa.visitor_category;

-- 2) gold_monthly_arrivals_by_country
CREATE OR REPLACE TABLE workspace.gold_layer.gold_monthly_arrivals_by_country AS
SELECT
  fa.country_key,
  fa.geo_code,
  fa.country_name,
  fa.year,
  fa.month,
  fa.source_system,
  fa.indicator_code,
  fa.visitor_category,
  SUM(fa.standardized_value) AS arrivals,
  MAX(fa.standardized_unit) AS unit,
  MAX(dd.is_primary_period) AS is_primary_period
FROM workspace.gold_layer.fact_tourism_arrivals fa
LEFT JOIN workspace.gold_layer.dim_date dd
  ON dd.year = fa.year AND dd.month = fa.month
WHERE fa.frequency = 'M'
GROUP BY fa.country_key, fa.geo_code, fa.country_name, fa.year, fa.month, fa.source_system,
         fa.indicator_code, fa.visitor_category;

-- 3) gold_tourism_growth_yearly
CREATE OR REPLACE TABLE workspace.gold_layer.gold_tourism_growth_yearly AS
SELECT
  cur.country_key,
  cur.year,
  cur.source_system,
  cur.indicator_code,
  cur.visitor_category,
  cur.arrivals,
  prev.arrivals AS prev_arrivals,
  CASE WHEN prev.arrivals > 0 THEN (cur.arrivals - prev.arrivals) / prev.arrivals END AS growth_pct
FROM workspace.gold_layer.gold_yearly_arrivals_by_country cur
JOIN workspace.gold_layer.gold_yearly_arrivals_by_country prev
  ON cur.country_key = prev.country_key
 AND cur.source_system = prev.source_system
 AND cur.indicator_code = prev.indicator_code
 AND cur.visitor_category = prev.visitor_category
 AND cur.year = prev.year + 1;

-- 4) gold_tourism_growth_monthly
CREATE OR REPLACE TABLE workspace.gold_layer.gold_tourism_growth_monthly AS
SELECT
  cur.country_key,
  cur.year,
  cur.month,
  cur.source_system,
  cur.indicator_code,
  cur.visitor_category,
  cur.arrivals,
  prev.arrivals AS prev_arrivals,
  CASE WHEN prev.arrivals > 0 THEN (cur.arrivals - prev.arrivals) / prev.arrivals END AS growth_pct
FROM workspace.gold_layer.gold_monthly_arrivals_by_country cur
JOIN workspace.gold_layer.gold_monthly_arrivals_by_country prev
  ON cur.country_key = prev.country_key
 AND cur.month = prev.month
 AND cur.source_system = prev.source_system
 AND cur.indicator_code = prev.indicator_code
 AND cur.visitor_category = prev.visitor_category
 AND cur.year = prev.year + 1;

-- 5) gold_destination_rankings
CREATE OR REPLACE TABLE workspace.gold_layer.gold_destination_rankings AS
SELECT
  gya.country_key,
  dc.country_name,
  SUM(gya.arrivals) AS total_arrivals
FROM workspace.gold_layer.gold_yearly_arrivals_by_country gya
JOIN workspace.gold_layer.dim_country dc ON dc.country_key = gya.country_key
WHERE gya.is_primary_period = TRUE
GROUP BY gya.country_key, dc.country_name
ORDER BY total_arrivals DESC;

-- 6) gold_tourism_seasonality
CREATE OR REPLACE TABLE workspace.gold_layer.gold_tourism_seasonality AS
SELECT
  gma.month,
  AVG(gma.arrivals) AS avg_arrivals,
  PERCENTILE_APPROX(gma.arrivals, 0.5) AS median_arrivals,
  MAX(gma.arrivals) AS peak_arrivals,
  MIN(gma.arrivals) AS lowest_arrivals,
  STDDEV_POP(gma.arrivals) AS stddev
FROM workspace.gold_layer.gold_monthly_arrivals_by_country gma
GROUP BY gma.month
ORDER BY gma.month;

-- 7) gold_nights_spent_trends
CREATE OR REPLACE TABLE workspace.gold_layer.gold_nights_spent_trends AS
SELECT
  fns.country_key,
  fns.year,
  SUM(fns.standardized_value) AS total_nights
FROM workspace.gold_layer.fact_nights_spent fns
GROUP BY fns.country_key, fns.year
ORDER BY fns.country_key, fns.year;

-- 8) gold_hotel_capacity_trends
CREATE OR REPLACE TABLE workspace.gold_layer.gold_hotel_capacity_trends AS
SELECT
  fhp.country_key,
  fhp.year,
  fhp.accommodation_metric,
  SUM(fhp.standardized_value) AS total_units
FROM workspace.gold_layer.fact_hotel_performance fhp
GROUP BY fhp.country_key, fhp.year, fhp.accommodation_metric
ORDER BY fhp.country_key, fhp.year;

-- 9) gold_hotel_occupancy_trends
CREATE OR REPLACE TABLE workspace.gold_layer.gold_hotel_occupancy_trends AS
SELECT
  fho.country_key,
  fho.year,
  fho.month,
  AVG(fho.occupancy_rate) AS avg_occupancy_rate
FROM workspace.gold_layer.fact_hotel_occupancy fho
GROUP BY fho.country_key, fho.year, fho.month
ORDER BY fho.country_key, fho.year, fho.month;

-- 10) gold_visitor_category_analysis
CREATE OR REPLACE TABLE workspace.gold_layer.gold_visitor_category_analysis AS
SELECT
  fta.country_key,
  fta.year,
  fta.visitor_category,
  SUM(fta.standardized_value) AS arrivals
FROM workspace.gold_layer.fact_tourism_arrivals fta
WHERE fta.frequency = 'A'
GROUP BY fta.country_key, fta.year, fta.visitor_category
ORDER BY fta.country_key, fta.year, fta.visitor_category;

-- 11) gold_country_comparison
CREATE OR REPLACE TABLE workspace.gold_layer.gold_country_comparison AS
SELECT
  gyac.country_key,
  dc.country_name,
  gyac.year,
  SUM(gyac.arrivals) AS total_arrivals
FROM workspace.gold_layer.gold_yearly_arrivals_by_country gyac
JOIN workspace.gold_layer.dim_country dc ON dc.country_key = gyac.country_key
GROUP BY gyac.country_key, dc.country_name, gyac.year
ORDER BY dc.country_name, gyac.year;
