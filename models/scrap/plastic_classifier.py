"""
Plastic Classifier — Identify plastic types and recommend processing paths.

Helps sort collected plastics by resin code, density, and visual cues.
Maps each type to the best processing system in the lab.

Usage:
    python -m models.scrap.plastic_classifier --code 2
    python -m models.scrap.plastic_classifier --density 0.95
    python -m models.scrap.plastic_classifier --all
"""

import argparse

# Plastic classification database
PLASTICS = {
    1: {
        "code": "PET",
        "name": "Polyethylene Terephthalate",
        "density_range": (1.33, 1.45),
        "common_items": "Water bottles, soda bottles, food trays",
        "visual_cues": "Clear, smooth, crinkles when crushed, sinks in water",
        "float_test": "sinks",
        "burn_test": "Sweet smell, black smoke, drips",
        "best_process": "chemical",
        "alt_process": "extruder",
        "process_notes": "Chemical recovery gives highest value (terephthalic acid). Can also extrude but needs drying.",
        "value_per_kg": (0.50, 2.00),
        "warnings": [],
    },
    2: {
        "code": "HDPE",
        "name": "High-Density Polyethylene",
        "density_range": (0.94, 0.97),
        "common_items": "Milk jugs, detergent bottles, pipes",
        "visual_cues": "Opaque/translucent, waxy feel, flexible, floats",
        "float_test": "floats",
        "burn_test": "Candle wax smell, blue flame, drips",
        "best_process": "extruder",
        "alt_process": "mold_press",
        "process_notes": "Easiest to extrude. Best starter material. Great for filament.",
        "value_per_kg": (0.30, 1.50),
        "warnings": [],
    },
    3: {
        "code": "PVC",
        "name": "Polyvinyl Chloride",
        "density_range": (1.30, 1.45),
        "common_items": "Pipes, window frames, cable insulation",
        "visual_cues": "Rigid or flexible, sinks, often grey/white",
        "float_test": "sinks",
        "burn_test": "Acrid chlorine smell, green-tipped flame",
        "best_process": "NONE",
        "alt_process": "NONE",
        "process_notes": "DO NOT PROCESS. Releases HCl gas when heated. Separate and set aside.",
        "value_per_kg": (0.05, 0.15),
        "warnings": [
            "TOXIC when heated — releases hydrochloric acid gas",
            "NEVER pyrolyze, extrude, or melt PVC",
            "Contaminates other plastics — sort carefully",
            "Store separately from all other plastics",
        ],
    },
    4: {
        "code": "LDPE",
        "name": "Low-Density Polyethylene",
        "density_range": (0.91, 0.94),
        "common_items": "Plastic bags, cling wrap, squeeze bottles",
        "visual_cues": "Flexible, stretchy, somewhat transparent, floats",
        "float_test": "floats",
        "burn_test": "Candle wax smell, blue flame, drips slowly",
        "best_process": "mold_press",
        "alt_process": "pyrolysis",
        "process_notes": "Hard to extrude (too soft). Good for mold press or pyrolysis oil.",
        "value_per_kg": (0.10, 0.50),
        "warnings": [],
    },
    5: {
        "code": "PP",
        "name": "Polypropylene",
        "density_range": (0.89, 0.92),
        "common_items": "Yogurt cups, bottle caps, food containers",
        "visual_cues": "Semi-rigid, slightly waxy, floats, hinge-like flex",
        "float_test": "floats",
        "burn_test": "Sweet petroleum smell, blue/yellow flame",
        "best_process": "extruder",
        "alt_process": "mold_press",
        "process_notes": "Excellent for filament. Similar to HDPE but slightly tougher.",
        "value_per_kg": (0.30, 1.50),
        "warnings": [],
    },
    6: {
        "code": "PS",
        "name": "Polystyrene",
        "density_range": (1.04, 1.08),
        "common_items": "Styrofoam, disposable cups, CD cases",
        "visual_cues": "Brittle, snaps clean, white foam or clear rigid",
        "float_test": "foam floats, solid sinks",
        "burn_test": "Sooty black smoke, styrene smell (sweet/chemical)",
        "best_process": "pyrolysis",
        "alt_process": "mold_press",
        "process_notes": "Pyrolysis recovers styrene monomer (highest value). Densify foam first.",
        "value_per_kg": (0.20, 3.00),
        "warnings": ["Styrene fumes are hazardous — use respirator"],
    },
    7: {
        "code": "OTHER",
        "name": "Other (ABS, PC, Nylon, etc.)",
        "density_range": (1.00, 1.40),
        "common_items": "Electronics, auto parts, 3D prints, mixed",
        "visual_cues": "Varies widely; often black or colored",
        "float_test": "usually sinks",
        "burn_test": "Varies; ABS has acrid smell",
        "best_process": "pyrolysis",
        "alt_process": "mold_press",
        "process_notes": "Mixed bag. Pyrolysis is safest bet. Some (ABS) extrude well.",
        "value_per_kg": (0.10, 1.00),
        "warnings": ["Test small batches first — unknown composition"],
    },
}


def classify_by_code(code):
    """Look up plastic by resin identification code (1-7)."""
    if code not in PLASTICS:
        print(f"Unknown resin code: {code}. Valid codes: 1-7")
        return
    _print_plastic(PLASTICS[code], code)


def classify_by_density(density):
    """Identify possible plastic types by measured density."""
    matches = []
    for code, data in PLASTICS.items():
        lo, hi = data["density_range"]
        if lo <= density <= hi:
            matches.append((code, data))

    if not matches:
        print(f"No plastics match density {density} g/cm³")
        print("Possible measurement error, or composite material.")
        return

    print(f"Plastics matching density {density} g/cm³:\n")
    for code, data in matches:
        print(f"  #{code} {data['code']} ({data['name']})")
        print(f"    Density range: {data['density_range'][0]}-{data['density_range'][1]} g/cm³")
        print(f"    Common items:  {data['common_items']}")
        print(f"    Float test:    {data['float_test']}")
        print(f"    Burn test:     {data['burn_test']}")
        print()


def show_all():
    """Show all plastic types with processing recommendations."""
    print("Plastic Classification Guide\n")
    print(f"  {'Code':>4s}  {'Type':6s}  {'Name':35s}  {'Density':>12s}  {'Float':>6s}  {'Best Process':>14s}")
    print(f"  {'-' * 85}")

    for code, data in PLASTICS.items():
        density_str = f"{data['density_range'][0]}-{data['density_range'][1]}"
        print(
            f"  #{code:>3}  {data['code']:6s}  {data['name']:35s}"
            f"  {density_str:>12s}  {data['float_test']:>6s}"
            f"  {data['best_process']:>14s}"
        )

    print("\n  Quick sort: Float test in water separates codes 2,4,5 (float) from 1,3,6 (sink)")


def _print_plastic(data, code):
    """Pretty-print a single plastic type."""
    print(f"\n  #{code} — {data['code']}: {data['name']}")
    print(f"  {'=' * 50}")
    print(f"  Common items:   {data['common_items']}")
    print(f"  Visual cues:    {data['visual_cues']}")
    print(f"  Density:        {data['density_range'][0]}-{data['density_range'][1]} g/cm³")
    print(f"  Float test:     {data['float_test']}")
    print(f"  Burn test:      {data['burn_test']}")
    print(f"  Best process:   {data['best_process']}")
    print(f"  Alt process:    {data['alt_process']}")
    print(f"  Value:          ${data['value_per_kg'][0]:.2f}-${data['value_per_kg'][1]:.2f}/kg")
    print(f"  Notes:          {data['process_notes']}")

    for warning in data["warnings"]:
        print(f"  WARNING:        {warning}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify and route plastics")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--code", type=int, help="Resin identification code (1-7)")
    group.add_argument("--density", type=float, help="Measured density in g/cm³")
    group.add_argument("--all", action="store_true", help="Show all types")
    args = parser.parse_args()

    if args.code:
        classify_by_code(args.code)
    elif args.density:
        classify_by_density(args.density)
    else:
        show_all()
