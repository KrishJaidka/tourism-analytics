-- TourismPulse — dim_date (SQL Warehouse compatible)
CREATE OR REPLACE TABLE workspace.gold_layer.dim_date AS
WITH monthly AS (
  SELECT
    CAST(date_format(d, 'yyyyMMdd') AS INT) AS date_key,
    d AS date,
    YEAR(d) AS year,
    QUARTER(d) AS quarter,
    MONTH(d) AS month,
    MONTHNAME(d) AS month_name,
    CASE
      WHEN MONTH(d) IN (12, 1, 2) THEN 'Winter'
      WHEN MONTH(d) IN (3, 4, 5) THEN 'Spring'
      WHEN MONTH(d) IN (6, 7, 8) THEN 'Summer'
      ELSE 'Autumn'
    END AS season,
    date_format(d, 'yyyyMM') AS year_month,
    (YEAR(d) BETWEEN 2012 AND 2019) AS is_primary_period
  FROM (
    SELECT explode(sequence(DATE '1990-01-01', DATE '2026-12-01', INTERVAL 1 MONTH)) AS d
  )
),
annual AS (
  SELECT
    y AS date_key,
    to_date(y || '-01-01', 'yyyy-MM-dd') AS date,
    y AS year,
    1 AS quarter,
    NULL AS month,
    NULL AS month_name,
    NULL AS season,
    NULL AS year_month,
    (y BETWEEN 2012 AND 2019) AS is_primary_period
  FROM (
    SELECT explode(sequence(CAST('1990' AS INT), CAST('2027' AS INT))) AS y
  )
)
SELECT * FROM monthly
UNION ALL
SELECT * FROM annual
ORDER BY date_key;
