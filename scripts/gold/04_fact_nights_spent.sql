-- TourismPulse — fact_nights_spent (SQL Warehouse compatible, Unity Catalog naming)
CREATE OR REPLACE TABLE workspace.gold_layer.fact_nights_spent AS
SELECT
  es.country_iso3 AS country_key,
  es.geo_code AS geo_code,
  YEAR(es.period) AS year,
  MONTH(es.period) AS month,
  YEAR(es.period) * 100 + MONTH(es.period) AS date_key,
  es.residence_category AS residence_category,
  es.activity_code AS activity_category,
  'EUROSTAT' AS source_system,
  es.nights_spent AS original_value,
  'nights' AS original_unit,
  es.nights_spent AS standardized_value,
  'nights' AS standardized_unit,
  es.observation_flag AS observation_status,
  (YEAR(es.period) BETWEEN 2012 AND 2019) AS is_primary_period
FROM delta.`/Volumes/workspace/default/tourismdata/silver_layer/estat_tour_occ_nim` es
WHERE es.unit_code = 'NR' AND es.country_iso3 IS NOT NULL
ORDER BY country_key, year, month;
