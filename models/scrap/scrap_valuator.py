"""
Scrap Valuator — Estimate the value of collected plastic waste.

Given a collection of plastics (by type and weight), estimates raw material
value, processed product value, and best processing route.

Usage:
    python -m models.scrap.scrap_valuator --pe 20 --pp 10 --pet 15
    python -m models.scrap.scrap_valuator --mixed 50
    python -m models.scrap.scrap_valuator --pe 20 --pp 10 --pet 15 --detail
"""

import argparse

# Value chains per kg of input plastic
# (raw_value, processed_value, best_product, process)
VALUE_CHAINS = {
    "pe": {
        "name": "HDPE/LDPE",
        "raw_value": 0.30,
        "products": {
            "filament": {"yield_pct": 85, "value_per_kg": 25.00, "process": "extruder"},
            "fuel_oil": {"yield_pct": 75, "value_per_kg": 1.00, "process": "pyrolysis"},
            "molded":   {"yield_pct": 90, "value_per_kg": 8.00, "process": "mold_press"},
        },
    },
    "pp": {
        "name": "Polypropylene",
        "raw_value": 0.35,
        "products": {
            "filament": {"yield_pct": 85, "value_per_kg": 25.00, "process": "extruder"},
            "fuel_oil": {"yield_pct": 78, "value_per_kg": 1.10, "process": "pyrolysis"},
            "molded":   {"yield_pct": 90, "value_per_kg": 8.00, "process": "mold_press"},
        },
    },
    "pet": {
        "name": "PET",
        "raw_value": 0.45,
        "products": {
            "chemicals":{"yield_pct": 70, "value_per_kg": 3.50, "process": "chemical"},
            "filament": {"yield_pct": 75, "value_per_kg": 20.00, "process": "extruder"},
            "fuel_oil": {"yield_pct": 35, "value_per_kg": 0.80, "process": "pyrolysis"},
        },
    },
    "ps": {
        "name": "Polystyrene",
        "raw_value": 0.20,
        "products": {
            "styrene":  {"yield_pct": 80, "value_per_kg": 3.00, "process": "pyrolysis"},
            "molded":   {"yield_pct": 85, "value_per_kg": 6.00, "process": "mold_press"},
        },
    },
    "mixed": {
        "name": "Mixed (no PVC)",
        "raw_value": 0.15,
        "products": {
            "fuel_oil": {"yield_pct": 60, "value_per_kg": 0.80, "process": "pyrolysis"},
            "molded":   {"yield_pct": 75, "value_per_kg": 5.00, "process": "mold_press"},
            "carbon":   {"yield_pct": 20, "value_per_kg": 30.00, "process": "plasma"},
        },
    },
}

# Microplastics recovered from wash water (per kg plastic cleaned)
WASH_WATER_RECOVERY = {
    "microplastics_g_per_kg": 30,       # Average grams per kg cleaned
    "microplastics_value_per_kg": 200,   # $/kg of concentrated microplastics
    "sludge_g_per_kg": 10,
    "sludge_value_per_kg": 1.50,
}


def best_product(plastic_type):
    """Find the highest-value product for a plastic type."""
    chain = VALUE_CHAINS[plastic_type]
    best = None
    best_value = 0
    for product_name, product in chain["products"].items():
        value_per_input_kg = (product["yield_pct"] / 100) * product["value_per_kg"]
        if value_per_input_kg > best_value:
            best_value = value_per_input_kg
            best = (product_name, product, value_per_input_kg)
    return best


def valuate(inputs, detail=False):
    """Estimate total value of a plastic collection."""
    total_raw = 0
    total_processed = 0
    total_kg = 0

    print("Scrap Valuation\n")

    for plastic_type, weight_kg in inputs.items():
        if weight_kg <= 0:
            continue
        if plastic_type not in VALUE_CHAINS:
            print(f"  Unknown type: {plastic_type}")
            continue

        chain = VALUE_CHAINS[plastic_type]
        raw = weight_kg * chain["raw_value"]
        total_raw += raw
        total_kg += weight_kg

        product_name, product, value_per_kg = best_product(plastic_type)
        processed = weight_kg * value_per_kg
        total_processed += processed

        print(f"  {chain['name']:20s}  {weight_kg:>6.1f} kg")
        print(f"    Raw value:          ${raw:>8.2f}")
        print(f"    Best product:       {product_name} via {product['process']}")
        print(f"    Yield:              {product['yield_pct']}% -> "
              f"{weight_kg * product['yield_pct'] / 100:.1f} kg product")
        print(f"    Processed value:    ${processed:>8.2f}")

        if detail:
            print(f"    All options:")
            for pname, p in chain["products"].items():
                v = weight_kg * (p["yield_pct"] / 100) * p["value_per_kg"]
                marker = " <-- best" if pname == product_name else ""
                print(f"      {pname:12s} ({p['process']:10s}): "
                      f"${v:>8.2f}{marker}")
        print()

    # Water treatment recovery
    wash_mp_kg = total_kg * WASH_WATER_RECOVERY["microplastics_g_per_kg"] / 1000
    wash_mp_value = wash_mp_kg * WASH_WATER_RECOVERY["microplastics_value_per_kg"]
    wash_sludge_kg = total_kg * WASH_WATER_RECOVERY["sludge_g_per_kg"] / 1000
    wash_sludge_value = wash_sludge_kg * WASH_WATER_RECOVERY["sludge_value_per_kg"]

    print(f"  Water Treatment Recovery:")
    print(f"    Microplastics:      {wash_mp_kg:.2f} kg -> ${wash_mp_value:.2f}")
    print(f"    Metal sludge:       {wash_sludge_kg:.2f} kg -> ${wash_sludge_value:.2f}")

    total_all = total_processed + wash_mp_value + wash_sludge_value
    multiplier = total_all / total_raw if total_raw > 0 else 0

    print(f"\n  Summary:")
    print(f"    Total input:        {total_kg:.1f} kg")
    print(f"    Raw scrap value:    ${total_raw:>10.2f}")
    print(f"    Processed value:    ${total_processed:>10.2f}")
    print(f"    + Water recovery:   ${wash_mp_value + wash_sludge_value:>10.2f}")
    print(f"    TOTAL value:        ${total_all:>10.2f}")
    print(f"    Value multiplier:   {multiplier:.0f}x vs raw scrap")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate value of collected plastics")
    parser.add_argument("--pe", type=float, default=0, help="HDPE/LDPE weight (kg)")
    parser.add_argument("--pp", type=float, default=0, help="Polypropylene weight (kg)")
    parser.add_argument("--pet", type=float, default=0, help="PET weight (kg)")
    parser.add_argument("--ps", type=float, default=0, help="Polystyrene weight (kg)")
    parser.add_argument("--mixed", type=float, default=0, help="Mixed plastics weight (kg)")
    parser.add_argument("--detail", action="store_true", help="Show all processing options")
    args = parser.parse_args()

    inputs = {
        "pe": args.pe,
        "pp": args.pp,
        "pet": args.pet,
        "ps": args.ps,
        "mixed": args.mixed,
    }

    if not any(v > 0 for v in inputs.values()):
        print("Provide at least one plastic weight. Example: --pe 20 --pp 10")
    else:
        valuate(inputs, args.detail)
