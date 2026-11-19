# tourism-analytics
Travel Demand and Destination Intelligence. Analysis of tourist arrivals, destination popularity, hotel occupancy and seasonal travel trends.

## Ingestion
### 01_raw_data_ingestion
- Read raw CSV, JSON, NetCDF files.
- Load datasets into Databricks.
- Store original data in the Bronze layer.
- Preserve source columns and raw values.


## Silver
### 02_data_cleaning
- Remove duplicates.
- Handle null values.
- Fix data types.
- Standardize country names and dates.
- Clean individual datasets.


### 03_schema_normalization
- Standardize column names.
- Normalize country identifiers.
- Standardize units of measurement.
- Align time formats across datasets.


## Gold
### 04_data_transformation
- Aggregate tourist arrivals by country and month.
- Aggregate temperature and precipitation by country and month.
- Calculate seasonal travel trends.
- Calculate year-over-year growth.


### 05_data_integration
- Join tourism data with weather data.
- Join hotel occupancy data.
- Join country and regional metadata.
- Create an integrated analytical dataset.


### 06_analytical_tables
Create final analytical Delta tables:
- Monthly tourist arrivals.
- Seasonal tourism trends.
- Destination popularity.
- Weather vs tourism.
- Hotel occupancy trends.


### 07_exploratory_analysis
- Identify peak tourism months.
- Compare destinations.
- Find seasonal patterns.
- Analyze weather and tourism relationships.
- Identify tourism growth and decline.


### 08_powerbi_export
- Select final Gold tables.
- Create Power BI-ready datasets.
- Export or connect Power BI to Databricks.
