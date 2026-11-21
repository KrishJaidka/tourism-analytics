-- TourismPulse — gold_source_comparison (SQL Warehouse compatible, Unity Catalog naming)
-- Compares World Bank, UN Tourism, and Eurostat by country. Values are standardized to persons.
CREATE OR REPLACE TABLE workspace.gold_layer.gold_source_comparison AS
WITH wb AS (
  SELECT
    country_code AS country_key,
    country_name AS country_name,
    SUM(arrivals / 1000.0) AS world_bank_arrivals,
    COUNT(*) AS world_bank_rows
  FROM delta.`/Volumes/workspace/default/tourismdata/silver_layer/world_bank_international_arrivals`
  WHERE country_iso3 IS NOT NULL
  GROUP BY country_code, country_name
),
un AS (
  SELECT
    reporter_country_iso3 AS country_key,
    reporter_area AS country_name,
    SUM(arrivals / 1000.0) AS un_arrivals,
    COUNT(*) AS un_rows
  FROM delta.`/Volumes/workspace/default/tourismdata/silver_layer/un_tourism_inbound_arrivals`
  WHERE reporter_country_iso3 IS NOT NULL
  GROUP BY reporter_country_iso3, reporter_area
),
estat AS (
  SELECT
    country_iso3 AS country_key,
    NULL AS country_name,
    SUM(tourism_value) AS estat_arrivals,
    COUNT(*) AS estat_rows
  FROM delta.`/Volumes/workspace/default/tourismdata/silver_layer/estat_tour_occ_arm`
  WHERE unit_code = 'NR' AND country_iso3 IS NOT NULL
  GROUP BY country_iso3
),
joined AS (
  SELECT
    COALESCE(w.country_key, u.country_key, e.country_key) AS country_key,
    COALESCE(w.country_name, u.country_name) AS country_name,
    w.world_bank_arrivals,
    w.world_bank_rows,
    u.un_arrivals,
    u.un_rows,
    e.estat_arrivals,
    e.estat_rows
  FROM wb w
  FULL OUTER JOIN un u ON u.country_key = w.country_key
  FULL OUTER JOIN estat e ON e.country_key = COALESCE(w.country_key, u.country_key)
)
SELECT
  country_key,
  country_name,
  world_bank_arrivals,
  world_bank_rows,
  un_arrivals,
  un_rows,
  estat_arrivals,
  estat_rows,
  GREATEST(COALESCE(world_bank_arrivals, 0), COALESCE(un_arrivals, 0), COALESCE(estat_arrivals, 0)) AS discrepancy
FROM joined
ORDER BY discrepancy DESC;
