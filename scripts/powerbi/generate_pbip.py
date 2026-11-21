# Power BI Dashboard Builder
# Generates a Power BI Project (.pbip) with semantic model and 5-page report skeleton.
# Usage: python scripts/powerbi/generate_pbip.py
import json
import os
from pathlib import Path

REPO = Path(r"C:\Users\Kaashvi\OneDrive\Documents\Default Project\tourism-analytics")
PBIP_NAME = "TourismPulse_Gold"
PBIP_ROOT = REPO / (PBIP_NAME + ".pbip")
MODEL_DIR = PBIP_ROOT / f"{PBIP_NAME}.SemanticModel" / "definition"
REPORT_DIR = PBIP_ROOT / f"{PBIP_NAME}.Report" / "definition"

# Parse gold_schemas.txt
def parse_schemas(path):
    tables = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        name, rest = line.split(" => ")
        cols = []
        for item in rest.split(", "):
            if not item.strip():
                continue
            col, typ = item.split(":")
            cols.append((col.strip(), typ.strip()))
        tables[name] = cols
    return tables

def to_dax_type(t):
    return {
        "string": "text",
        "double": "double",
        "int": "int64",
        "boolean": "bool",
        "date": "date",
    }.get(t, "text")

def is_hidden_col(name):
    n = name.lower()
    return (
        n.startswith("_")
        or n.startswith("arrival_key")
        or n.startswith("nights_key")
        or n.startswith("hotel_perf_key")
        or n.startswith("occupancy_key")
        or n.startswith("prev_arrivals")
        or n in ("original_value", "original_unit", "standardized_unit", "observation_status", "aggregation_level")
        or n in ("is_primary_period",)
    )

RELATIONSHIPS = [
    ("R01", "dim_country.country_key", "fact_tourism_arrivals.country_key"),
    ("R02", "dim_country.country_key", "fact_nights_spent.country_key"),
    ("R03", "dim_country.country_key", "fact_hotel_performance.country_key"),
    ("R04", "dim_country.country_key", "fact_hotel_occupancy.country_key"),
    ("R05", "dim_date.date_key", "fact_tourism_arrivals.date_key"),
    ("R06", "dim_date.date_key", "fact_nights_spent.date_key"),
    ("R07", "dim_date.date_key", "fact_hotel_occupancy.date_key"),
    ("R08", "fact_tourism_arrivals.country_key", "gold_yearly_arrivals_by_country.country_key"),
    ("R09", "fact_tourism_arrivals.country_key", "gold_monthly_arrivals_by_country.country_key"),
    ("R10", "fact_tourism_arrivals.country_key", "gold_tourism_growth_yearly.country_key"),
    ("R11", "fact_tourism_arrivals.country_key", "gold_tourism_growth_monthly.country_key"),
    ("R12", "fact_tourism_arrivals.country_key", "gold_visitor_category_analysis.country_key"),
    ("R13", "fact_nights_spent.country_key", "gold_nights_spent_trends.country_key"),
    ("R14", "fact_hotel_performance.country_key", "gold_hotel_capacity_trends.country_key"),
    ("R15", "fact_hotel_occupancy.country_key", "gold_hotel_occupancy_trends.country_key"),
    ("R16", "gold_yearly_arrivals_by_country.country_key", "gold_destination_rankings.country_key"),
    ("R17", "gold_yearly_arrivals_by_country.country_key", "gold_country_comparison.country_key"),
    ("R18", "fact_tourism_arrivals.country_key", "pbi_total_arrivals.country_key"),
    ("R19", "fact_hotel_occupancy.country_key", "pbi_avg_occupancy.country_key"),
]

MEASURES = {
    "fact_tourism_arrivals": [
        ("Total Annual Arrivals", "SUMX(fact_tourism_arrivals, standardized_value)"),
        ("Total Monthly Arrivals", "CALCULATE(SUMX(fact_tourism_arrivals, standardized_value), fact_tourism_arrivals[frequency] = \"M\")"),
        ("Tourism Growth % (Yearly)", "VAR Current = CALCULATE(SUMX(fact_tourism_arrivals, standardized_value), fact_tourism_arrivals[frequency] = \"A\") VAR Prev = CALCULATE(SUMX(fact_tourism_arrivals, standardized_value), fact_tourism_arrivals[frequency] = \"A\", DATEADD(dim_date[date], -1, YEAR)) RETURN DIVIDE(Current - Prev, Prev)"),
        ("Tourism Growth % (Monthly)", "VAR Current = CALCULATE(SUMX(fact_tourism_arrivals, standardized_value), fact_tourism_arrivals[frequency] = \"M\") VAR Prev = CALCULATE(SUMX(fact_tourism_arrivals, standardized_value), fact_tourism_arrivals[frequency] = \"M\", DATEADD(dim_date[date], -1, YEAR)) RETURN DIVIDE(Current - Prev, Prev)"),
    ],
    "fact_nights_spent": [
        ("Total Nights Spent", "SUMX(fact_nights_spent, standardized_value)"),
    ],
    "fact_hotel_performance": [
        ("Hotel Establishments", "SUMX(FILTER(fact_hotel_performance, accommodation_metric = \"Establishments\"), standardized_value)"),
        ("Hotel Rooms", "SUMX(FILTER(fact_hotel_performance, accommodation_metric = \"Rooms\"), standardized_value)"),
        ("Bed Places", "SUMX(FILTER(fact_hotel_performance, accommodation_metric = \"Bed places\"), standardized_value)"),
    ],
    "fact_hotel_occupancy": [
        ("Average Occupancy Rate", "AVERAGEX(fact_hotel_occupancy, occupancy_rate)"),
    ],
}

def gen_table_tmdl(name, cols):
    lines = [f"table {name}"]
    for col, typ in cols:
        dax_type = to_dax_type(typ)
        lines.append(f"    column '{col}'")
        lines.append(f"        dataType: {dax_type}")
        if col == "country_key" or col in ("country_key",):
            lines.append("        isKey")
        if is_hidden_col(col):
            lines.append("        isHidden")
        lines.append(f"        sourceColumn: {col}")
    for mname, expr in MEASURES.get(name, []):
        lines.append(f"    measure '{mname}' = {expr}")
        lines.append("        formatString: $ #,##0.00")
    lines.append("")
    return "\n".join(lines)

def main():
    schemas = parse_schemas(r"C:\Users\Kaashvi\AppData\Local\Temp\opencode\gold_schemas.txt")

    # Create directories
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    (MODEL_DIR / "tables").mkdir(exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "pages").mkdir(exist_ok=True)
    (REPORT_DIR / "staticResources").mkdir(exist_ok=True)
    (PBIP_ROOT / ".gitignore").write_text(
        "**/.pbi/localSettings.json\n**/.pbi/cache.abf\n",
        encoding="utf-8",
    )

    # PBIP root file
    pbip = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
        "version": "4.0",
        "artifacts": [
            {"report": {"path": f"{PBIP_NAME}.Report"}},
        ],
    }
    (PBIP_ROOT / f"{PBIP_NAME}.pbip").write_text(json.dumps(pbip, indent=2), encoding="utf-8")

    # Semantic model TMDL
    (MODEL_DIR / "database.tmdl").write_text(
        "database DatabaseName compatibilityLevel: 1700\n",
        encoding="utf-8",
    )
    (MODEL_DIR / "model.tmdl").write_text(
        "model Model\n    culture: en-US\n",
        encoding="utf-8",
    )
    (MODEL_DIR / "dataSources.tmdl").write_text("", encoding="utf-8")
    (MODEL_DIR / "expressions.tmdl").write_text("", encoding="utf-8")
    for t, cols in schemas.items():
        (MODEL_DIR / "tables" / f"{t}.tmdl").write_text(gen_table_tmdl(t, cols), encoding="utf-8")
    rels = "\n".join(f"relationship {rid}\n    fromColumn: {f}\n    toColumn: {t}\n" for rid, f, t in RELATIONSHIPS)
    (MODEL_DIR / "relationships.tmdl").write_text(rels + "\n", encoding="utf-8")

    # Report skeleton
    (REPORT_DIR / "version.json").write_text(
        json.dumps({"version": "1.0"}, indent=2), encoding="utf-8"
    )
    (REPORT_DIR / "report.json").write_text(
        json.dumps({
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.0.0/schema.json",
            "version": "4.0",
            "pages": [],
            "slicers": [],
        }, indent=2), encoding="utf-8",
    )
    (REPORT_DIR / "reportExtensions.json").write_text(
        json.dumps({"version": "1.0"}, indent=2), encoding="utf-8"
    )
    (REPORT_DIR / "semanticModelDiagramLayout.json").write_text(
        json.dumps({"zoomLevel": 1}, indent=2), encoding="utf-8"
    )
    (REPORT_DIR / ".platform").write_text("{}\n", encoding="utf-8")
    (REPORT_DIR / "pages" / "pages.json").write_text(
        json.dumps({
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/2.0.0/schema.json",
            "pageOrder": [],
            "activePageName": None,
        }, indent=2), encoding="utf-8",
    )
    pages = [
        ("Page1", "Tourism Overview", 0),
        ("Page2", "Country Comparison", 1),
        ("Page3", "Monthly Trends", 2),
        ("Page4", "Hotel Performance", 3),
        ("Page5", "Data Quality Monitoring", 4),
    ]
    for name, display, idx in pages:
        page_dir = REPORT_DIR / "pages" / name
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "page.json").write_text(
            json.dumps({
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/1.0.0/schema.json",
                "name": name,
                "displayName": display,
                "position": {"x": 0, "y": 0, "width": 1200, "height": 800},
                "isHidden": False,
                "annotations": [],
            }, indent=2), encoding="utf-8"
        )
    # Update pages.json with pageOrder
    pages_meta = json.loads((REPORT_DIR / "pages" / "pages.json").read_text(encoding="utf-8"))
    pages_meta["pageOrder"] = [p[0] for p in pages]
    pages_meta["activePageName"] = pages[0][0]
    (REPORT_DIR / "pages" / "pages.json").write_text(json.dumps(pages_meta, indent=2), encoding="utf-8")

    # definition.pbir
    (REPORT_DIR / "definition.pbir").write_text(
        json.dumps({
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
            "version": "4.0",
            "datasetReference": {"byPath": {"path": "../TourismPulse_Gold.SemanticModel"}},
        }, indent=2), encoding="utf-8",
    )
    (REPORT_DIR / "staticResources").mkdir(exist_ok=True)

    print(f"PBIP project generated: {PBIP_ROOT}")
    print(f"Semantic model: {MODEL_DIR}")
    print(f"Report skeleton: {REPORT_DIR}")
    print("5 report pages: " + ", ".join(p[1] for p in pages))

if __name__ == "__main__":
    main()
