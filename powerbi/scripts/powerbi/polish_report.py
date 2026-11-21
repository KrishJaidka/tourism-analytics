# PolishesPower BI Visuals Layout
# Updates visual.json positions for better alignment on each page.
import json
from pathlib import Path

ROOT = Path(r"C:\Users\Kaashvi\OneDrive\Documents\Default Project\tourism-analytics\TourismPulse_Gold.pbip\TourismPulse_Gold.Report\definition")

LAYOUT = {
    "Page1": {
        "Page1_kpi_total_arrivals": {"x": 0, "y": 0, "width": 190, "height": 100},
        "Page1_kpi_monthly_arrivals": {"x": 230, "y": 0, "width": 190, "height": 100},
        "Page1_kpi_nights_spent": {"x": 460, "y": 0, "width": 190, "height": 100},
        "Page1_kpi_yoy_growth": {"x": 690, "y": 0, "width": 190, "height": 100},
        "Page1_kpi_total_arrivals_yearly": {"x": 920, "y": 0, "width": 190, "height": 100},
        "Page1_line_annual_arrivals": {"x": 0, "y": 120, "width": 900, "height": 380},
        "Page1_bar_top10_destinations": {"x": 920, "y": 120, "width": 270, "height": 380},
        "Page1_slicer_country": {"x": 0, "y": 520, "width": 400, "height": 120},
        "Page1_slicer_year": {"x": 420, "y": 520, "width": 150, "height": 120},
        "Page1_slicer_source": {"x": 580, "y": 520, "width": 250, "height": 120},
        "Page1_slicer_visitor_category": {"x": 850, "y": 520, "width": 330, "height": 120},
    },
    "Page2": {
        "Page2_bar_ranking": {"x": 0, "y": 0, "width": 900, "height": 450},
        "Page2_table_country_arrivals": {"x": 0, "y": 470, "width": 900, "height": 330},
        "Page2_line_growth_by_country": {"x": 920, "y": 0, "width": 270, "height": 730},
        "Page2_slicer_country": {"x": 0, "y": 800, "width": 400, "height": 120},
        "Page2_slicer_year": {"x": 420, "y": 800, "width": 150, "height": 120},
    },
    "Page3": {
        "Page3_line_monthly_arrivals": {"x": 0, "y": 0, "width": 900, "height": 400},
        "Page3_bar_seasonality": {"x": 920, "y": 0, "width": 270, "height": 400},
        "Page3_slicer_month": {"x": 0, "y": 430, "width": 400, "height": 120},
        "Page3_slicer_country": {"x": 420, "y": 430, "width": 400, "height": 120},
        "Page3_slicer_year": {"x": 840, "y": 430, "width": 350, "height": 120},
    },
    "Page4": {
        "Page4_kpi_hotel_establishments": {"x": 0, "y": 0, "width": 280, "height": 90},
        "Page4_kpi_hotel_rooms": {"x": 300, "y": 0, "width": 280, "height": 90},
        "Page4_kpi_bed_places": {"x": 600, "y": 0, "width": 280, "height": 90},
        "Page4_line_occupancy": {"x": 920, "y": 0, "width": 270, "height": 450},
        "Page4_table_occupancy_units": {"x": 0, "y": 110, "width": 900, "height": 350},
        "Page4_bar_occupancy_comparison": {"x": 0, "y": 480, "width": 900, "height": 300},
        "Page4_slicer_country": {"x": 920, "y": 470, "width": 270, "height": 120},
        "Page4_slicer_year": {"x": 920, "y": 600, "width": 270, "height": 120},
    },
    "Page5": {
        "Page5_table_source_counts": {"x": 0, "y": 0, "width": 900, "height": 220},
        "Page5_table_missing_values": {"x": 0, "y": 240, "width": 900, "height": 220},
        "Page5_table_nights_spent_nulls": {"x": 0, "y": 480, "width": 900, "height": 220},
        "Page5_kpi_total_arrivals_quality": {"x": 0, "y": 720, "width": 280, "height": 90},
        "Page5_slicer_year": {"x": 300, "y": 720, "width": 280, "height": 120},
    },
}

def main():
    updated = 0
    for page, visuals in LAYOUT.items():
        for visual, pos in visuals.items():
            vjson = ROOT / "pages" / page / "visuals" / visual / "visual.json"
            if not vjson.exists():
                print(f"MISSING: {vjson}")
                continue
            v = json.loads(vjson.read_text(encoding="utf-8"))
            v["position"] = pos
            vjson.write_text(json.dumps(v, indent=2), encoding="utf-8")
            updated += 1
    print(f"Polished {updated} visuals.")

if __name__ == "__main__":
    main()
