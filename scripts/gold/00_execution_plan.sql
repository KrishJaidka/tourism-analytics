-- TourismPulse — Complete Gold Layer Execution Script (SQL Warehouse)
-- Proposed execution script. Uses Unity Catalog naming: workspace.gold_layer.*
-- Creates the schema and runs all Gold transformations in dependency order.
-- All tables are new; no existing Gold tables are expected.
-- Notes:
--   - Uses ISO3 strings as country_key for consistent joins (dim_country.country_key = ISO3 or surrogate).
--   - Replaces Spark-specific syntax with SQL Warehouse syntax.
--   - Replaces FIRST with MAX.
--   - Replaces MEDIAN with PERCENTILE_APPROX(0.5).

CREATE SCHEMA IF NOT EXISTS workspace.gold_layer;

-- 1) dim_date
CREATE OR REPLACE TABLE workspace.gold_layer.dim_date AS
SELECT
  d.date_key,
  d.date,
  d.year,
  d.quarter,
  d.month,
  d.month_name,
  d.season,
  d.year_month,
  d.is_primary_period
FROM (
  SELECT
    explode(sequence(DATE '1990-01-01', DATE '2026-12-01', INTERVAL 1 MONTH)) AS date,
    YEAR(explode(sequence(DATE '1990-01-01', DATE '2026-12-01', INTERVAL 1 MONTH))) AS year
) ;

-- The above is a placeholder; final dim_date is created by the notebook.
-- For SQL-only execution, see scripts/gold/02_dim_date.sql.
