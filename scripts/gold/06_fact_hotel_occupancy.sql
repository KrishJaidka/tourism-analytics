-- TourismPulse — fact_hotel_occupancy (SQL Warehouse compatible, Unity Catalog naming)
CREATE OR REPLACE TABLE workspace.gold_layer.fact_hotel_occupancy AS
SELECT
  es.country_iso3 AS country_key,
  es.geo_code AS geo_code,
  YEAR(es.period) AS year,
  MONTH(es.period) AS month,
  YEAR(es.period) * 100 + MONTH(es.period) AS date_key,
  es.accommodation_unit AS accommodation_unit,
  es.occupancy_rate AS occupancy_rate,
  'PC' AS unit,
  'EUROSTAT' AS source_system,
  es.observation_flag AS observation_status,
  (YEAR(es.period) BETWEEN 2012 AND 2019) AS is_primary_period
FROM delta.`/Volumes/workspace/default/tourismdata/silver_layer/estat_tour_occ_mnor` es
WHERE es.country_iso3 IS NOT NULL
ORDER BY country_key, year, month;
