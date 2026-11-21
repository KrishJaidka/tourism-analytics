# TourismPulse

TourismPulse is an end-to-end analytics pipeline for tourism demand and accommodation data. It ingests multiple public datasets into Databricks, cleans and standardizes them in the Silver layer, builds a country-and-date-based Gold star schema, and prepares analytical outputs for Power BI.

## Contributors

| Name | Roll No |
| --- | --- |
| Krish Jaidka | 2401730188 |
| Kaashvi Gupta | 2401730180 |
| Anirudh Chauhan | 2401730062 |
| Divyam | 2401730000 |

## Pipeline overview

```text
Public tourism sources
        |
        v
Bronze: preserve source files and values
        |
        v
Silver: clean, reshape, normalize countries and units
        |
        v
Gold: dimensions, facts and analytical tables
        |
        v
Power BI: semantic model and report project
```

The primary analytical period is 2012-2019. Full history is retained, and Gold tables expose `is_primary_period` for consistent default filtering.

## Data sources

| Source | Dataset | Link |
| --- | --- | --- |
| World Bank | International Tourism, number of arrivals (`ST.INT.ARVL`) | [World Bank indicator](https://data.worldbank.org/indicator/ST.INT.ARVL) |
| Eurostat | Nights spent at tourist accommodation establishments | [Eurostat tourism database](https://ec.europa.eu/eurostat/web/tourism/database) |
| Eurostat | Arrivals at tourist accommodation establishments | [Eurostat tourism database](https://ec.europa.eu/eurostat/web/tourism/database) |
| Eurostat | Net occupancy rate of bed-places and bedrooms in hotels and similar accommodation | [Eurostat tourism database](https://ec.europa.eu/eurostat/web/tourism/database) |
| UN Tourism | Tourism accommodation and hotels | [UN Tourism statistics database](https://www.untourism.int/tourism-statistics/tourism-statistics-database) |
| UN Tourism | Tourism inbound arrivals | [UN Tourism statistics database](https://www.untourism.int/tourism-statistics/tourism-statistics-database) |

### Source conventions

- World Bank and UN Tourism inbound/accommodation data are annual.
- Eurostat arrival and nights-spent data are monthly; `NR` is the count unit used in the Gold facts.
- Eurostat occupancy data is monthly and distinguishes bed-places (`BEDPL`) from bedrooms (`BEDRM`).
- Observation flags and original units remain in the curated data.
- Cross-source values are not blindly summed. Annual and monthly observations, source definitions, visitor categories and measurement units have different grains.

## Databricks storage layout

The notebooks use Unity Catalog and Databricks volumes configured in [`config/config.py`](config/config.py):

```text
/Volumes/workspace/default/tourismdata/
├── raw/
├── bronze_layer/
├── silver_layer/
└── gold_layer/
```

Gold SQL objects are created in `workspace.gold_layer`.

## Notebook pipeline

Run the notebooks in order from a Databricks environment attached to a Spark cluster.

| Stage | Notebook | Purpose |
| --- | --- | --- |
| 01 - Bronze | [`01 Data Ingestion.ipynb`](01%20Data%20Ingestion.ipynb) | Read the six raw CSV/TSV files and write Bronze Delta tables. |
| 01 - Bronze QA | [`01 Bronze Data Overview.ipynb`](01%20Bronze%20Data%20Overview.ipynb) | Inventory and inspect the Bronze tables. |
| 02 - Silver cleaning | [`02 Dataset Cleaning [estat_tour_occ_arm].ipynb`](02%20Dataset%20Cleaning%20%5Bestat_tour_occ_arm%5D.ipynb) | Clean and reshape Eurostat accommodation arrivals. |
| 02 - Silver cleaning | [`02 Dataset Cleaning [estat_tour_occ_mnor].ipynb`](02%20Dataset%20Cleaning%20%5Bestat_tour_occ_mnor%5D.ipynb) | Clean and reshape Eurostat hotel occupancy. |
| 02 - Silver cleaning | [`02 Dataset Cleaning [estat_tour_occ_nim].ipynb`](02%20Dataset%20Cleaning%20%5Bestat_tour_occ_nim%5D.ipynb) | Clean and reshape Eurostat nights spent. |
| 02 - Silver cleaning | [`02 Dataset Cleaning [un_tourism_accommodation_hotels].ipynb`](02%20Dataset%20Cleaning%20%5Bun_tourism_accommodation_hotels%5D.ipynb) | Clean UN hotel capacity and performance indicators. |
| 02 - Silver cleaning | [`02 Dataset Cleaning [un_tourism_inbound_arrivals].ipynb`](02%20Dataset%20Cleaning%20%5Bun_tourism_inbound_arrivals%5D.ipynb) | Clean UN inbound visitor categories. |
| 02 - Silver cleaning | [`02 Dataset Cleaning [world_bank_internatinal_arrival].ipynb`](02%20Dataset%20Cleaning%20%5Bworld_bank_internatinal_arrival%5D.ipynb) | Cleans and Reshape World Bank annual arrivals. |
| 03 - Normalization | [`03 Country Code Normalization.ipynb`](03%20Country%20Code%20Normalization.ipynb) | Map source geography codes to ISO2/ISO3 identifiers and classify entities. |
| 03 - Quality | [`03 Data Anomaly Detection.ipynb`](03%20Data%20Anomaly%20Detection.ipynb) | Detect nulls, duplicates, negatives and malformed geography values. |
| 03 - Measurements | [`03 Measurement Conversion.ipynb`](03%20Measurement%20Conversion.ipynb) | Inspect source units and document measurement semantics. |
| 04 - Silver QA | [`04 Silver Data Overview.ipynb`](04%20Silver%20Data%20Overview.ipynb) | Inventory and inspect the curated Silver tables. |
| 05 - Gold dimensions | [`05 Gold Dimensions.ipynb`](05%20Gold%20Dimensions.ipynb) | Build `dim_country` and `dim_date`. |
| 06 - Gold facts | [`06 Gold Facts.ipynb`](06%20Gold%20Facts.ipynb) | Build tourism arrivals, nights spent, hotel performance and occupancy facts. |
| 07 - Gold analytics | [`07 Gold Analytics.ipynb`](07%20Gold%20Analytics.ipynb) | Build growth, seasonality, ranking and source-comparison tables. |
| 08 - Validation | [`08 Gold Validation.ipynb`](08%20Gold%20Validation.ipynb) | Check Gold row counts, duplicates, null keys and referential integrity. |
| 09 - Power BI | [`09 Power BI Preparation.ipynb`](09%20Power%20BI%20Preparation.ipynb) | Create Power BI-ready Gold tables and preparation outputs. |

## Gold data model

### Dimensions

- `dim_country`: ISO codes, country names, regions and aggregate/special-geography classification.
- `dim_date`: annual and monthly date keys, year, quarter, month, season and primary-period flag.

### Facts

- `fact_tourism_arrivals`: annual World Bank/UN arrivals and monthly Eurostat arrivals.
- `fact_nights_spent`: monthly Eurostat nights spent.
- `fact_hotel_performance`: annual UN hotel establishments, bed places, rooms and rates.
- `fact_hotel_occupancy`: monthly Eurostat bed-place and bedroom occupancy rates.

### Analytical tables

- `gold_yearly_arrivals_by_country`
- `gold_monthly_arrivals_by_country`
- `gold_tourism_growth_yearly`
- `gold_tourism_growth_monthly`
- `gold_destination_rankings`
- `gold_tourism_seasonality`
- `gold_nights_spent_trends`
- `gold_hotel_capacity_trends`
- `gold_hotel_occupancy_trends`
- `gold_visitor_category_analysis`
- `gold_country_comparison`
- `gold_source_comparison`

See [`powerbi/docs/gold_schema.md`](powerbi/docs/gold_schema.md) for the detailed schema and grain rules.

## Gold SQL alternative

The [`powerbi/scripts/gold`](powerbi/scripts/gold) folder contains SQL and PowerShell implementations that mirror the Gold notebooks.

```powershell
cd powerbi/scripts/gold
.\00_execute_gold.ps1
```

The script creates `workspace.gold_layer` objects through a Databricks SQL warehouse. Review and configure its Databricks profile and warehouse ID before running it.

Key support files:

- [`00_execution_plan.sql`](powerbi/scripts/gold/00_execution_plan.sql)
- [`10_verify_execution.ps1`](powerbi/scripts/gold/10_verify_execution.ps1)
- [`README.md`](powerbi/scripts/gold/README.md)

## Power BI

The [`powerbi`](powerbi) folder contains PBIP report and semantic-model definitions plus scripts for generation and validation:

```text
powerbi/
├── TourismPulse_Gold.pbip
├── TourismPulse_Gold.Report/
├── TourismPulse_Gold.SemanticModel/
├── TourismPulse_Gold_pbip_backup/
├── scripts/powerbi/
└── docs/
```

Open `TourismPulse_Gold.pbip` in Power BI Desktop, or review [`powerbi/docs/powerbi_connection_guide.md`](powerbi/docs/powerbi_connection_guide.md) for connection requirements.

Power BI build, lineage and design references:

- [`powerbi/docs/data_lineage.md`](powerbi/docs/data_lineage.md)
- [`powerbi/docs/powerbi_semantic_model.md`](powerbi/docs/powerbi_semantic_model.md)
- [`powerbi/docs/powerbi_measures.md`](powerbi/docs/powerbi_measures.md)
- [`powerbi/docs/powerbi_dashboard_specs.md`](powerbi/docs/powerbi_dashboard_specs.md)
- [`powerbi/docs/powerbi_build_report.md`](powerbi/docs/powerbi_build_report.md)
- [`powerbi/docs/gold_validation_report.md`](powerbi/docs/gold_validation_report.md)

## Setup

1. Upload the six source files to `/Volumes/workspace/default/tourismdata/raw/`.
2. Configure the volume paths in [`config/config.py`](config/config.py) if the workspace or catalog differs.
3. Attach the notebooks to a Databricks cluster with Spark and required Python packages.
4. Run the notebooks in numbered order.
5. Run Gold validation before consuming the outputs.
6. Open or generate the PBIP project and connect it to the validated Gold tables.

## Repository guide

- `*.ipynb`: numbered Bronze, Silver, Gold and Power BI preparation workflow.
- `config/`: Databricks volume and Gold table paths.
- `powerbi/scripts/gold/`: SQL warehouse implementation of the Gold pipeline.
- `powerbi/scripts/powerbi/`: report generation, visual addition, polishing and validation scripts.
- `powerbi/docs/`: implementation status, lineage, schema, validation and dashboard documentation.
- `TourismPulse_Gold.pbip`: top-level Power BI project entry point.
