# Power BI Dashboard Visuals Generator
# Creates visual.json files inside the PBIP report definition.
# Usage: python scripts/powerbi/add_visuals.py
import json
from pathlib import Path

REPO = Path(r"C:\Users\Kaashvi\OneDrive\Documents\Default Project\tourism-analytics")
ROOT = REPO / "TourismPulse_Gold.pbip" / "TourismPulse_Gold.Report" / "definition"

def field(table, column, queryRef=None, native=None):
    return {
        "type": "Field",
        "field": {"table": table, "column": column},
        "queryRef": queryRef or f"{table}.{column}",
        "nativeQueryRef": native or f"{table}.{column}",
    }

def visual_container(name, pos, visual_type, query_state):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.6.0/schema.json",
        "name": name,
        "id": name,
        "position": pos,
        "visual": {
            "visualType": visual_type,
            "query": {"queryState": query_state},
        },
    }

def measure_projection(measure):
    return {"field": {"type": "Field", "field": {"table": "", "column": ""}, "queryRef": measure}, "queryRef": measure}

def proj(table, column, queryRef=None, native=None):
    return {"field": field(table, column, queryRef, native), "queryRef": queryRef or f"{table}.{column}"}

def make_visual(vtype, projections, pos, name):
    return visual_container(name, pos, vtype, {"projections": projections})

PAGES = [
    {
        "name": "Page1",
        "displayName": "Tourism Overview",
        "visuals": [
            make_visual("card", [proj("fact_tourism_arrivals", "Total Annual Arrivals")], { "x": 0, "y": 0, "width": 280, "height": 90 }, "kpi_total_arrivals"),
            make_visual("card", [proj("fact_tourism_arrivals", "Total Monthly Arrivals")], { "x": 290, "y": 0, "width": 280, "height": 90 }, "kpi_monthly_arrivals"),
            make_visual("card", [proj("fact_nights_spent", "Total Nights Spent")], { "x": 580, "y": 0, "width": 280, "height": 90 }, "kpi_nights_spent"),
            make_visual("card", [proj("fact_tourism_arrivals", "Tourism Growth % (Yearly)")], { "x": 870, "y": 0, "width": 280, "height": 90 }, "kpi_yoy_growth"),
            make_visual("card", [proj("gold_yearly_arrivals_by_country", "total_arrivals")], { "x": 1160, "y": 0, "width": 200, "height": 90 }, "kpi_total_arrivals_yearly"),
            make_visual("lineChart", [proj("gold_yearly_arrivals_by_country", "year"), proj("gold_yearly_arrivals_by_country", "arrivals")], { "x": 0, "y": 110, "width": 860, "height": 340 }, "line_annual_arrivals"),
            make_visual("clusteredBarChart", [proj("gold_destination_rankings", "country_name"), proj("gold_destination_rankings", "total_arrivals")], { "x": 870, "y": 110, "width": 320, "height": 400 }, "bar_top10_destinations"),
            make_visual("slicer", [proj("dim_country", "country_name")], { "x": 0, "y": 460, "width": 400, "height": 120 }, "slicer_country"),
            make_visual("slicer", [proj("dim_date", "year")], { "x": 420, "y": 460, "width": 150, "height": 120 }, "slicer_year"),
            make_visual("slicer", [proj("fact_tourism_arrivals", "source_system")], { "x": 600, "y": 460, "width": 250, "height": 120 }, "slicer_source"),
            make_visual("slicer", [proj("fact_tourism_arrivals", "visitor_category")], { "x": 860, "y": 460, "width": 320, "height": 120 }, "slicer_visitor_category"),
        ],
    },
    {
        "name": "Page2",
        "displayName": "Country Comparison",
        "visuals": [
            make_visual("clusteredBarChart", [proj("gold_destination_rankings", "country_name"), proj("gold_destination_rankings", "total_arrivals")], { "x": 0, "y": 0, "width": 860, "height": 400 }, "bar_ranking"),
            make_visual("tableEx", [proj("gold_country_comparison", "country_name"), proj("gold_country_comparison", "total_arrivals")], { "x": 0, "y": 420, "width": 860, "height": 360 }, "table_country_arrivals"),
            make_visual("clusteredBarChart", [proj("gold_tourism_growth_yearly", "year"), proj("gold_tourism_growth_yearly", "growth_pct")], { "x": 870, "y": 0, "width": 320, "height": 730 }, "line_growth_by_country"),
            make_visual("slicer", [proj("dim_country", "country_name")], { "x": 0, "y": 800, "width": 400, "height": 120 }, "slicer_country"),
            make_visual("slicer", [proj("dim_date", "year")], { "x": 420, "y": 800, "width": 150, "height": 120 }, "slicer_year"),
        ],
    },
    {
        "name": "Page3",
        "displayName": "Monthly Trends",
        "visuals": [
            make_visual("lineChart", [proj("gold_monthly_arrivals_by_country", "year"), proj("gold_monthly_arrivals_by_country", "arrivals")], { "x": 0, "y": 0, "width": 860, "height": 380 }, "line_monthly_arrivals"),
            make_visual("clusteredBarChart", [proj("gold_tourism_seasonality", "month"), proj("gold_tourism_seasonality", "avg_arrivals")], { "x": 870, "y": 0, "width": 320, "height": 380 }, "bar_seasonality"),
            make_visual("slicer", [proj("dim_date", "month")], { "x": 0, "y": 410, "width": 400, "height": 120 }, "slicer_month"),
            make_visual("slicer", [proj("dim_country", "country_name")], { "x": 420, "y": 410, "width": 400, "height": 120 }, "slicer_country"),
            make_visual("slicer", [proj("dim_date", "year")], { "x": 830, "y": 410, "width": 400, "height": 120 }, "slicer_year"),
        ],
    },
    {
        "name": "Page4",
        "displayName": "Hotel Performance",
        "visuals": [
            make_visual("card", [proj("fact_hotel_performance", "Hotel Establishments")], { "x": 0, "y": 0, "width": 280, "height": 90 }, "kpi_hotel_establishments"),
            make_visual("card", [proj("fact_hotel_performance", "Hotel Rooms")], { "x": 290, "y": 0, "width": 280, "height": 90 }, "kpi_hotel_rooms"),
            make_visual("card", [proj("fact_hotel_performance", "Bed Places")], { "x": 580, "y": 0, "width": 280, "height": 90 }, "kpi_bed_places"),
            make_visual("lineChart", [proj("fact_hotel_occupancy", "year"), proj("fact_hotel_occupancy", "occupancy_rate")], { "x": 870, "y": 0, "width": 320, "height": 350 }, "line_occupancy"),
            make_visual("tableEx", [proj("fact_hotel_performance", "accommodation_metric"), proj("fact_hotel_performance", "standardized_value")], { "x": 0, "y": 110, "width": 860, "height": 350 }, "table_occupancy_units"),
            make_visual("clusteredBarChart", [proj("fact_hotel_performance", "accommodation_metric"), proj("fact_hotel_performance", "standardized_value")], { "x": 0, "y": 470, "width": 860, "height": 300 }, "bar_occupancy_comparison"),
            make_visual("slicer", [proj("dim_country", "country_name")], { "x": 870, "y": 370, "width": 320, "height": 120 }, "slicer_country"),
            make_visual("slicer", [proj("dim_date", "year")], { "x": 870, "y": 500, "width": 320, "height": 120 }, "slicer_year"),
        ],
    },
    {
        "name": "Page5",
        "displayName": "Data Quality Monitoring",
        "visuals": [
            make_visual("tableEx", [proj("fact_tourism_arrivals", "source_system"), proj("fact_tourism_arrivals", "standardized_value")], { "x": 0, "y": 0, "width": 860, "height": 220 }, "table_source_counts"),
            make_visual("tableEx", [proj("fact_tourism_arrivals", "observation_status"), proj("fact_tourism_arrivals", "standardized_value")], { "x": 0, "y": 240, "width": 860, "height": 220 }, "table_missing_values"),
            make_visual("tableEx", [proj("fact_nights_spent", "standardized_value")], { "x": 0, "y": 480, "width": 860, "height": 220 }, "table_nights_spent_nulls"),
            make_visual("card", [proj("fact_tourism_arrivals", "Total Annual Arrivals")], { "x": 0, "y": 720, "width": 280, "height": 90 }, "kpi_total_arrivals_quality"),
            make_visual("slicer", [proj("dim_date", "year")], { "x": 300, "y": 720, "width": 280, "height": 120 }, "slicer_year"),
        ],
    },
]

def main():
    created = []
    for page in PAGES:
        page_dir = ROOT / "pages" / page["name"]
        visuals_dir = page_dir / "visuals"
        visuals_dir.mkdir(exist_ok=True)
        for vis in page["visuals"]:
            vis["name"] = f"{page['name']}_{vis['name']}"
            vis["id"] = vis["name"]
            vdir = visuals_dir / vis["name"]
            vdir.mkdir(exist_ok=True)
            (vdir / "visual.json").write_text(json.dumps(vis, indent=2), encoding="utf-8")
            created.append(vis["name"])
        # Add visual entries to page.json if not present
        page_json_path = page_dir / "page.json"
        if page_json_path.exists():
            page_json = json.loads(page_json_path.read_text(encoding="utf-8"))
        else:
            page_json = {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/1.0.0/schema.json"}
        page_json.setdefault("$schema", "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/1.0.0/schema.json")
        page_json.setdefault("name", page["name"])
        page_json.setdefault("displayName", page["displayName"])
        page_json.setdefault("displayOption", "FitToPage")
        page_json.setdefault("isHidden", False)
        page_json.setdefault("annotations", [])
        # Visuals are stored as separate folders under the page's visuals/ directory.
        # page.json does not list visuals in the PBIR schema.
        page_json_path.write_text(json.dumps(page_json, indent=2), encoding="utf-8")
    print("Created visuals:", len(created))
    for name in created:
        print(" -", name)

if __name__ == "__main__":
    main()
