"""
Waste Stream Analyzer — Model composition and routing of plastic waste.

Helps plan collection strategy by modeling typical forest/roadside plastic
composition and routing each fraction to the best processing system.

Usage:
    python -m models.scrap.waste_stream --total 100
    python -m models.scrap.waste_stream --total 50 --source forest
    python -m models.scrap.waste_stream --total 200 --source roadside
"""

import argparse

# Typical composition by source (weight percentage)
SOURCE_PROFILES = {
    "forest": {
        "name": "Forest / Trail Cleanup",
        "composition": {
            "pet": 35,     # Water/soda bottles
            "hdpe": 20,    # Detergent, oil containers
            "ldpe": 15,    # Bags, wrap
            "pp": 12,      # Caps, food containers
            "ps": 8,       # Styrofoam
            "pvc": 3,      # Pipe fragments
            "other": 5,    # Mixed, degraded
            "non_plastic": 2,  # Metal, glass, etc.
        },
        "contamination_pct": 30,  # Dirt, organic matter
        "notes": "High UV degradation. Heavy biofilm. Needs thorough cleaning.",
    },
    "roadside": {
        "name": "Roadside / Highway Cleanup",
        "composition": {
            "pet": 40,
            "hdpe": 15,
            "ldpe": 20,
            "pp": 10,
            "ps": 5,
            "pvc": 2,
            "other": 5,
            "non_plastic": 3,
        },
        "contamination_pct": 20,
        "notes": "Less degradation than forest. Often muddy. Watch for auto fluids.",
    },
    "urban": {
        "name": "Urban / Park Cleanup",
        "composition": {
            "pet": 45,
            "hdpe": 10,
            "ldpe": 15,
            "pp": 15,
            "ps": 10,
            "pvc": 1,
            "other": 3,
            "non_plastic": 1,
        },
        "contamination_pct": 15,
        "notes": "Cleaner overall. High PET fraction. Good for chemical recovery.",
    },
    "beach": {
        "name": "Beach / Shoreline Cleanup",
        "composition": {
            "pet": 30,
            "hdpe": 20,
            "ldpe": 25,
            "pp": 10,
            "ps": 8,
            "pvc": 2,
            "other": 3,
            "non_plastic": 2,
        },
        "contamination_pct": 35,
        "notes": "Salt encrustation. Microplastic-rich. Heavy cleaning needed.",
    },
}

# Processing routes for each fraction
ROUTES = {
    "pet":    {"process": "Chemical Recovery", "system": "chemical", "alt": "extruder"},
    "hdpe":   {"process": "Filament Extrusion", "system": "extruder", "alt": "mold_press"},
    "ldpe":   {"process": "Mold Press / Pyrolysis", "system": "mold_press", "alt": "pyrolysis"},
    "pp":     {"process": "Filament Extrusion", "system": "extruder", "alt": "mold_press"},
    "ps":     {"process": "Pyrolysis (Styrene Recovery)", "system": "pyrolysis", "alt": "mold_press"},
    "pvc":    {"process": "REJECT — Set Aside", "system": "none", "alt": "none"},
    "other":  {"process": "Pyrolysis", "system": "pyrolysis", "alt": "plasma"},
    "non_plastic": {"process": "Discard / Recycle Separately", "system": "none", "alt": "none"},
}


def analyze(total_kg, source="forest"):
    """Analyze a waste stream and plan processing routes."""
    if source not in SOURCE_PROFILES:
        print(f"Unknown source: {source}")
        print(f"Available: {', '.join(SOURCE_PROFILES.keys())}")
        return

    profile = SOURCE_PROFILES[source]
    contamination = total_kg * profile["contamination_pct"] / 100
    clean_kg = total_kg - contamination

    print(f"Waste Stream Analysis: {profile['name']}")
    print(f"  Total collected:    {total_kg:.0f} kg")
    print(f"  Contamination:      {contamination:.0f} kg ({profile['contamination_pct']}%)")
    print(f"  Clean plastic:      {clean_kg:.0f} kg")
    print(f"  Notes:              {profile['notes']}")

    print(f"\n  {'Fraction':15s} {'%':>4s}  {'Weight':>7s}  {'Route':30s}")
    print(f"  {'-' * 65}")

    system_loads = {}
    processable_kg = 0

    for fraction, pct in profile["composition"].items():
        weight = clean_kg * pct / 100
        route = ROUTES[fraction]

        print(f"  {fraction:15s} {pct:>3}%  {weight:>5.1f} kg  {route['process']}")

        if route["system"] != "none":
            system_loads.setdefault(route["system"], 0)
            system_loads[route["system"]] += weight
            processable_kg += weight

    reject_kg = clean_kg - processable_kg

    print(f"\n  System Load Distribution:")
    print(f"  {'System':20s} {'Load':>7s}  {'Daily Batches':>14s}")
    print(f"  {'-' * 45}")

    # Estimate batches based on typical throughput
    throughputs = {
        "extruder": 5, "pyrolysis": 3, "mold_press": 8,
        "chemical": 2, "plasma": 1,
    }

    for system, load in sorted(system_loads.items(), key=lambda x: -x[1]):
        daily_cap = throughputs.get(system, 3)
        days_needed = load / daily_cap
        print(f"  {system:20s} {load:>5.1f} kg  {days_needed:>12.1f} days")

    total_days = max(
        (load / throughputs.get(sys, 3)) for sys, load in system_loads.items()
    ) if system_loads else 0

    print(f"\n  Processing Summary:")
    print(f"    Processable:      {processable_kg:.0f} kg ({processable_kg / clean_kg * 100:.0f}%)")
    print(f"    Rejected (PVC+):  {reject_kg:.0f} kg")
    print(f"    Est. processing:  {total_days:.0f} days (bottleneck-limited)")

    # Water treatment load
    wash_water_l = total_kg * 10  # ~10L per kg
    print(f"\n  Water Treatment:")
    print(f"    Wash water needed:  {wash_water_l:.0f} L")
    print(f"    EC batches (10L):   {wash_water_l / 10:.0f}")
    print(f"    Microplastics est:  {total_kg * 0.03:.1f} kg")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze plastic waste stream composition")
    parser.add_argument("--total", type=float, required=True, help="Total collected weight (kg)")
    parser.add_argument("--source", choices=list(SOURCE_PROFILES.keys()),
                        default="forest", help="Collection source (default: forest)")
    args = parser.parse_args()

    analyze(args.total, args.source)
