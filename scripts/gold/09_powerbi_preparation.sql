-- TourismPulse — Power BI preparation tables (SQL Warehouse compatible, Unity Catalog naming)

-- pbi_total_arrivals: annual total arrivals by country/year.
CREATE OR REPLACE TABLE workspace.gold_layer.pbi_total_arrivals AS
SELECT
  fa.country_key,
  fa.country_name,
  fa.year,
  SUM(fa.standardized_value) AS total_arrivals
FROM workspace.gold_layer.fact_tourism_arrivals fa
WHERE fa.frequency = 'A'
GROUP BY fa.country_key, fa.country_name, fa.year
ORDER BY fa.country_key, fa.year;

-- pbi_avg_occupancy: monthly average occupancy by country/year/month.
CREATE OR REPLACE TABLE workspace.gold_layer.pbi_avg_occupancy AS
SELECT
  fho.country_key,
  fho.year,
  fho.month,
  AVG(fho.occupancy_rate) AS avg_occupancy_rate
FROM workspace.gold_layer.fact_hotel_occupancy fho
GROUP BY fho.country_key, fho.year, fho.month
ORDER BY fho.country_key, fho.year, fho.month;
