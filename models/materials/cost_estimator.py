"""
Cost Estimator — Calculate total lab cost with salvage discounts.

Estimates costs for building the complete plastic lab, with adjustable
salvage percentages to model how much you can scavenge vs buy new.

Usage:
    python -m models.materials.cost_estimator
    python -m models.materials.cost_estimator --salvage 60
    python -m models.materials.cost_estimator --systems cleaner extruder water_ec
"""

import argparse

# Bill of materials derived from Docs/build-out-materials.md and forest_plastic_lab.md
SYSTEM_BOMS = {
    "cleaner": {
        "name": "Ultrasonic Cleaning Station",
        "items": [
            ("40kHz ultrasonic transducers (x4)", 120, 0.3),
            ("Stainless steel steam table pan", 40, 0.7),
            ("Aquarium heater (300W)", 25, 0.5),
            ("Timer outlets", 20, 0.4),
            ("PVC pipe for drainage", 15, 0.6),
            ("UV-C germicidal lamp", 30, 0.2),
        ],
    },
    "shredder": {
        "name": "Shredder & Sorting Station",
        "items": [
            ("Heavy-duty paper shredder", 40, 0.9),  # Easy to find used
            ("Old blender", 20, 0.9),
            ("5-gallon buckets with lids (x7)", 35, 0.5),
            ("Mesh screens (3 sizes)", 30, 0.4),
            ("Strong magnets", 20, 0.3),
        ],
    },
    "extruder": {
        "name": "Filament Extruder",
        "items": [
            ("Temperature PID controller kit", 35, 0.2),
            ("Auger bit (3/4\" x 12\")", 25, 0.3),
            ("Black iron pipe (1\" x 18\")", 20, 0.5),
            ("Band heaters (2x 300W)", 60, 0.3),
            ("DC gear motor (50 RPM)", 40, 0.6),
            ("Arduino + stepper for puller", 40, 0.2),
            ("Brass nozzle blanks", 20, 0.2),
        ],
    },
    "pyrolysis": {
        "name": "Microwave Pyrolysis Reactor",
        "items": [
            ("Dead microwave", 0, 1.0),  # Free!
            ("Stainless steel canister", 30, 0.5),
            ("Copper refrigerator coil", 25, 0.7),
            ("Mason jars for collection", 10, 0.5),
            ("High-temp silicone", 15, 0.1),
            ("Activated carbon", 20, 0.1),
            ("K-type thermocouple", 25, 0.2),
        ],
    },
    "mold_press": {
        "name": "Compression Mold Press",
        "items": [
            ("20-ton bottle jack", 60, 0.5),
            ("Steel plates (1/2\" x 12\" x 12\")", 80, 0.6),
            ("Angle iron for frame", 50, 0.7),
            ("Cartridge heaters (4x 200W)", 60, 0.2),
            ("Temperature controller", 30, 0.2),
            ("Mold release spray", 15, 0.0),
        ],
    },
    "chemical": {
        "name": "Chemical Recovery Unit",
        "items": [
            ("Pressure cooker", 30, 0.8),
            ("Magnetic stirrer/hotplate", 100, 0.4),
            ("Glass vessels (various)", 50, 0.5),
            ("Ethylene glycol (antifreeze)", 30, 0.1),
            ("Sodium hydroxide", 20, 0.0),
            ("pH strips and thermometer", 25, 0.1),
            ("Buchner funnel setup", 40, 0.3),
        ],
    },
    "plasma": {
        "name": "Plasma Carbon Converter",
        "items": [
            ("Microwave oven transformer", 0, 1.0),  # Salvaged from pyrolysis build
            ("Carbon welding rods", 20, 0.1),
            ("Quartz tube (or ceramic)", 40, 0.3),
            ("Variable transformer (variac)", 60, 0.4),
            ("High voltage insulators", 30, 0.3),
            ("Cyclone separator (DIY)", 30, 0.5),
        ],
    },
    "water_ec": {
        "name": "Electrocoagulation Unit",
        "items": [
            ("10L clear tank (glass/acrylic)", 40, 0.5),
            ("Aluminum plates 6x8\" (x6)", 30, 0.3),
            ("DC power supply (0-30V, 10A)", 60, 0.3),
            ("Air pump + stone diffuser", 20, 0.5),
            ("PVC pipe, elbows", 20, 0.5),
            ("pH meter", 20, 0.2),
            ("Timer relay", 15, 0.2),
        ],
    },
    "water_mag": {
        "name": "Magnetic Microplastic Separator",
        "items": [
            ("Neodymium magnets N52 (x20)", 50, 0.1),
            ("Peristaltic pump", 40, 0.3),
            ("Iron sulfate (FeSO4) 1kg", 20, 0.0),
            ("PVC tubing & fittings", 30, 0.5),
            ("Drum (plastic/metal roller)", 25, 0.8),
        ],
    },
    "water_uv": {
        "name": "Advanced Oxidation Reactor",
        "items": [
            ("UV-C LEDs (275nm) 10-20pcs", 100, 0.1),
            ("Quartz flow tube", 50, 0.2),
            ("H2O2 dosing pump", 40, 0.3),
            ("Titanium dioxide (powder)", 20, 0.0),
            ("Reflective chamber lining", 20, 0.5),
        ],
    },
    "water_bio": {
        "name": "Bioelectrochemical Cell",
        "items": [
            ("Acrylic tank (split)", 50, 0.5),
            ("Carbon felt sheets 12x12\" (x2)", 40, 0.1),
            ("Proton exchange membrane", 30, 0.0),
            ("Resistor box / multimeter", 20, 0.3),
            ("Activated sludge", 0, 1.0),  # Free from wastewater plant
        ],
    },
}


def estimate(system_ids, salvage_pct=0):
    """Estimate costs for selected systems with salvage discount."""
    salvage_factor = salvage_pct / 100.0

    print(f"Cost Estimate (salvage effort: {salvage_pct}%)\n")

    grand_new = 0
    grand_salvaged = 0

    for sid in system_ids:
        if sid not in SYSTEM_BOMS:
            print(f"  Unknown system: {sid}")
            continue

        bom = SYSTEM_BOMS[sid]
        system_new = 0
        system_salvaged = 0

        print(f"  {bom['name']}:")
        for item_name, new_price, salvage_chance in bom["items"]:
            # Probability of successfully salvaging this item
            effective_salvage = salvage_factor * salvage_chance
            salvaged_price = new_price * (1 - effective_salvage)
            system_new += new_price
            system_salvaged += salvaged_price

            if effective_salvage > 0.5:
                tag = " (likely salvageable)"
            elif effective_salvage > 0.2:
                tag = " (maybe salvageable)"
            else:
                tag = ""
            print(f"    {item_name:40s} ${new_price:>6}  -> ${salvaged_price:>6.0f}{tag}")

        savings = system_new - system_salvaged
        print(f"    {'':40s} ${system_new:>6}     ${system_salvaged:>6.0f}  (save ${savings:.0f})")
        print()

        grand_new += system_new
        grand_salvaged += system_salvaged

    grand_savings = grand_new - grand_salvaged
    pct_saved = (grand_savings / grand_new * 100) if grand_new else 0

    print(f"  {'Total (new):':<30s} ${grand_new:,}")
    print(f"  {'Total (with salvage):':<30s} ${grand_salvaged:,.0f}")
    print(f"  {'Savings:':<30s} ${grand_savings:,.0f} ({pct_saved:.0f}%)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate lab build costs")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--systems", nargs="+", choices=list(SYSTEM_BOMS.keys()),
                       help="Systems to estimate")
    group.add_argument("--all", action="store_true", default=True,
                       help="Estimate all systems (default)")
    parser.add_argument("--salvage", type=int, default=0,
                        help="Salvage effort %% (0=buy all new, 100=max scavenging)")
    args = parser.parse_args()

    ids = args.systems if args.systems else list(SYSTEM_BOMS.keys())
    estimate(ids, args.salvage)
