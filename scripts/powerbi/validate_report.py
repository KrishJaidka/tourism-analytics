# Validates TourismPulse_Gold PBIP visuals against the semantic model and DAX.
import json
from pathlib import Path

ROOT = Path(r"C:\Users\Kaashvi\OneDrive\Documents\Default Project\tourism-analytics\TourismPulse_Gold.pbip")
DEF = ROOT / "TourismPulse_Gold.SemanticModel" / "definition"
REPORT = ROOT / "TourismPulse_Gold.Report" / "definition"

def parse_tmdl(path):
    text = path.read_text(encoding="utf-8")
    table = None
    cols = set()
    measures = set()
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("table "):
            table = line.split()[1].strip("'\"")
        elif line.startswith("column ") and table:
            cols.add((table, line.split()[1].strip("'\"")))
        elif line.startswith("measure ") and table:
            name = line[8:].split("'")[1] if "'" in line else line.split()[1]
            measures.add((table, name))
        elif line.startswith("ref table "):
            table = line[10:].strip()
    return cols, measures

def main():
    cols = set()
    measures = set()
    for t in (DEF / "tables").glob("*.tmdl"):
        c, m = parse_tmdl(t)
        cols.update(c)
        measures.update(m)
    # relationships file for table names
    rel = (DEF / "relationships.tmdl").read_text(encoding="utf-8")
    tables = set()
    for line in rel.splitlines():
        if line.startswith("relationship "):
            pass
    # get all table names from definitions
    for t in (DEF / "tables").glob("*.tmdl"):
        tables.add(t.stem)
    # database/model tables? not needed.

    errors = []
    for page_dir in (REPORT / "pages").iterdir():
        if not page_dir.is_dir():
            continue
        visuals_dir = page_dir / "visuals"
        if not visuals_dir.exists():
            continue
        for v in visuals_dir.iterdir():
            vjson = v / "visual.json"
            if not vjson.exists():
                continue
            try:
                vis = json.loads(vjson.read_text(encoding="utf-8"))
            except Exception as e:
                errors.append(f"{vjson.name}: invalid JSON: {e}")
                continue
            query = vis.get("visual", {}).get("query", {})
            for state_name, state in query.get("queryState", {}).get("projections", []):
                pass
            projs = query.get("queryState", {}).get("projections", [])
            for p in projs:
                f = p.get("field", {})
                tname = f.get("field", {}).get("table")
                cname = f.get("field", {}).get("column")
                qref = p.get("queryRef")
                is_column = (tname, cname) in cols
                is_measure = any(
                    m == qref or m == cname or (tname and m == f"{tname}.{cname}")
                    for _, m in measures
                )
                if not is_column and not is_measure:
                    errors.append(f"{vjson.name}: field {tname}.{cname} not found")
    print("Visual reference validation errors:")
    if errors:
        for e in sorted(set(errors)):
            print(" -", e)
    else:
        print(" None.")
    print(f"Semantic model: {len(cols)} fields, {len(measures)} measures, {len(tables)} tables.")

    # DAX sanity checks on generated measures
    gen = Path(r"C:\Users\Kaashvi\OneDrive\Documents\Default Project\tourism-analytics\scripts\powerbi\generate_pbip.py").read_text(encoding="utf-8")
    checks = [
        ("Tourism Growth % (Yearly)", "DATEADD(dim_date[date], -1, YEAR)"),
        ("Tourism Growth % (Monthly)", "DATEADD(dim_date[date], -1, YEAR)"),
    ]
    print("DAX checks:")
    for name, needle in checks:
        print(f" - {name}: {'present' if name in gen and needle in gen else 'MISSING or incorrect'}")

if __name__ == "__main__":
    main()
