-- TourismPulse — fact_tourism_arrivals (SQL Warehouse compatible, Unity Catalog naming)
CREATE OR REPLACE TABLE workspace.gold_layer.fact_tourism_arrivals AS
WITH wb AS (
  SELECT
    wb.country_iso3 AS country_key,
    wb.country_code AS geo_code,
    wb.country_name AS country_name,
    wb.year AS year,
    NULL AS month,
    wb.year AS date_key,
    'A' AS frequency,
    'WORLD_BANK' AS source_system,
    wb.indicator_code AS indicator_code,
    wb.indicator_name AS indicator_label,
    'International arrivals' AS visitor_category,
    NULL AS residence_category,
    NULL AS accommodation_category,
    wb.arrivals AS original_value,
    'number of arrivals' AS original_unit,
    wb.arrivals AS standardized_value,
    'persons' AS standardized_unit,
    NULL AS observation_status,
    'Country' AS aggregation_level,
    TRUE AS is_country,
    (wb.year BETWEEN 2012 AND 2019) AS is_primary_period
  FROM delta.`/Volumes/workspace/default/tourismdata/silver_layer/world_bank_international_arrivals` wb
  WHERE wb.country_iso3 IS NOT NULL
),
un AS (
  SELECT
    un.reporter_country_iso3 AS country_key,
    un.reporter_area AS geo_code,
    un.reporter_area AS country_name,
    un.year AS year,
    NULL AS month,
    un.year AS date_key,
    'A' AS frequency,
    'UN_TOURISM' AS source_system,
    un.indicator_code AS indicator_code,
    un.indicator_label AS indicator_label,
    un.indicator_label AS visitor_category,
    NULL AS residence_category,
    NULL AS accommodation_category,
    un.arrivals / 1000.0 AS original_value,
    'thousand trips' AS original_unit,
    un.arrivals AS standardized_value,
    'persons' AS standardized_unit,
    un.observation_flag AS observation_status,
    'Country' AS aggregation_level,
    TRUE AS is_country,
    (un.year BETWEEN 2012 AND 2019) AS is_primary_period
  FROM delta.`/Volumes/workspace/default/tourismdata/silver_layer/un_tourism_inbound_arrivals` un
  WHERE un.reporter_country_iso3 IS NOT NULL
),
estat AS (
  SELECT
    es.country_iso3 AS country_key,
    es.geo_code AS geo_code,
    NULL AS country_name,
    YEAR(es.period) AS year,
    MONTH(es.period) AS month,
    YEAR(es.period) * 100 + MONTH(es.period) AS date_key,
    'M' AS frequency,
    'EUROSTAT' AS source_system,
    es.activity_code AS indicator_code,
    es.geo_code AS indicator_label,
    'International arrivals' AS visitor_category,
    es.residence_category AS residence_category,
    es.activity_code AS accommodation_category,
    es.tourism_value AS original_value,
    'number of arrivals' AS original_unit,
    es.tourism_value AS standardized_value,
    'persons' AS standardized_unit,
    es.observation_flag AS observation_status,
    'Country' AS aggregation_level,
    TRUE AS is_country,
    (YEAR(es.period) BETWEEN 2012 AND 2019) AS is_primary_period
  FROM delta.`/Volumes/workspace/default/tourismdata/silver_layer/estat_tour_occ_arm` es
  WHERE es.unit_code = 'NR' AND es.country_iso3 IS NOT NULL
)
SELECT * FROM wb
UNION ALL
SELECT * FROM un
UNION ALL
SELECT * FROM estat
ORDER BY source_system, country_key, year, month;
