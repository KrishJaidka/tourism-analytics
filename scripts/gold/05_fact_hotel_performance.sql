-- TourismPulse — fact_hotel_performance (SQL Warehouse compatible, Unity Catalog naming)
CREATE OR REPLACE TABLE workspace.gold_layer.fact_hotel_performance AS
SELECT
  un.reporter_country_iso3 AS country_key,
  un.reporter_area AS geo_code,
  un.year AS year,
  NULL AS month,
  un.year AS date_key,
  'UN_TOURISM' AS source_system,
  un.indicator_code AS indicator_code,
  un.indicator_label AS indicator_label,
  un.indicator_label AS accommodation_metric,
  un.hotel_capacity AS original_value,
  un.unit AS original_unit,
  un.hotel_capacity AS standardized_value,
  un.unit AS standardized_unit,
  un.observation_flag AS observation_status,
  (un.year BETWEEN 2012 AND 2019) AS is_primary_period
FROM delta.`/Volumes/workspace/default/tourismdata/silver_layer/un_tourism_accommodation_hotels` un
WHERE un.reporter_country_iso3 IS NOT NULL
ORDER BY country_key, year;
