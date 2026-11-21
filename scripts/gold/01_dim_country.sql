-- TourismPulse — dim_country (SQL Warehouse compatible, Unity Catalog naming)
-- country_key is the ISO3 code for countries. Aggregates use descriptive surrogate keys.
CREATE OR REPLACE TABLE workspace.gold_layer.dim_country AS
WITH countries AS (
  SELECT reporter_country_iso3 AS country_key,
         reporter_country_iso3 AS iso3,
         NULL AS iso2,
         reporter_area AS country_name,
         'MAPPED_COUNTRY' AS mapping_status,
         TRUE AS is_country
  FROM delta.`/Volumes/workspace/default/tourismdata/silver_layer/un_tourism_inbound_arrivals`
  WHERE reporter_country_iso3 IS NOT NULL
  UNION
  SELECT reporter_country_iso3 AS country_key,
         reporter_country_iso3 AS iso3,
         NULL AS iso2,
         reporter_area AS country_name,
         'MAPPED_COUNTRY' AS mapping_status,
         TRUE AS is_country
  FROM delta.`/Volumes/workspace/default/tourismdata/silver_layer/un_tourism_accommodation_hotels`
  WHERE reporter_country_iso3 IS NOT NULL
  UNION
  SELECT country_iso3 AS country_key,
         country_iso3 AS iso3,
         NULL AS iso2,
         geo_code AS country_name,
         'MAPPED_COUNTRY' AS mapping_status,
         TRUE AS is_country
  FROM delta.`/Volumes/workspace/default/tourismdata/silver_layer/estat_tour_occ_arm`
  WHERE country_iso3 IS NOT NULL
  UNION
  SELECT country_iso3 AS country_key,
         country_iso3 AS iso3,
         NULL AS iso2,
         country_name AS country_name,
         'MAPPED_COUNTRY' AS mapping_status,
         TRUE AS is_country
  FROM delta.`/Volumes/workspace/default/tourismdata/silver_layer/world_bank_international_arrivals`
  WHERE country_iso3 IS NOT NULL
),
aggregates AS (
  SELECT country_code AS country_key,
         NULL AS iso3,
         NULL AS iso2,
         country_name AS country_name,
         'MAPPED_AGGREGATE' AS mapping_status,
         FALSE AS is_country
  FROM delta.`/Volumes/workspace/default/tourismdata/silver_layer/world_bank_international_arrivals`
  WHERE country_iso3 IS NULL AND geography_type = 'regional_aggregate'
  UNION
  SELECT 'WORLD' AS country_key,
         NULL AS iso3,
         NULL AS iso2,
         'World' AS country_name,
         'SPECIAL_GEOGRAPHY' AS mapping_status,
         FALSE AS is_country
)
SELECT DISTINCT
  COALESCE(c.country_key, a.country_key) AS country_key,
  c.iso3,
  c.iso2,
  c.country_name,
  'Country' AS region,
  c.is_country,
  c.mapping_status
FROM countries c
LEFT JOIN aggregates a ON a.country_key = c.country_key
WHERE c.country_key IS NOT NULL
UNION ALL
SELECT
  country_key,
  iso3,
  iso2,
  country_name,
  'Aggregate' AS region,
  is_country,
  mapping_status
FROM aggregates;
