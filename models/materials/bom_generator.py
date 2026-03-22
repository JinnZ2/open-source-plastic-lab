"""
BOM Generator — Generate printable bill-of-materials for selected systems.

Outputs a shopping list grouped by source (hardware store, online, salvage)
with quantities and estimated costs.

Usage:
    python -m models.materials.bom_generator --systems cleaner extruder
    python -m models.materials.bom_generator --all --format csv
    python -m models.materials.bom_generator --all --format markdown
"""

import argparse
import csv
import io

# Categorized BOM with source suggestions
FULL_BOM = {
    "cleaner": {
        "name": "Ultrasonic Cleaning Station",
        "items": [
            ("40kHz ultrasonic transducers", 4, "pcs", 30.00, "online", "eBay/Amazon"),
            ("Stainless steel steam table pan", 1, "pcs", 40.00, "restaurant_supply", "Restaurant supply store"),
            ("Aquarium heater (300W)", 1, "pcs", 25.00, "online", "Amazon / pet store"),
            ("Timer outlets", 2, "pcs", 10.00, "hardware", "Hardware store"),
            ("PVC pipe assorted + elbows", 1, "lot", 15.00, "hardware", "Hardware store"),
            ("UV-C germicidal lamp", 1, "pcs", 30.00, "online", "Amazon"),
            ("Marine epoxy", 1, "tube", 10.00, "hardware", "Hardware store"),
        ],
    },
    "extruder": {
        "name": "Filament Extruder",
        "items": [
            ("Temperature PID controller kit", 1, "pcs", 35.00, "online", "Amazon/AliExpress"),
            ("Auger bit 3/4\" x 12\"", 1, "pcs", 25.00, "hardware", "Hardware store"),
            ("Black iron pipe 1\" x 18\"", 1, "pcs", 20.00, "hardware", "Hardware store"),
            ("Band heaters 300W", 2, "pcs", 30.00, "online", "eBay"),
            ("DC gear motor 50 RPM", 1, "pcs", 40.00, "online", "Amazon"),
            ("Arduino Uno clone", 1, "pcs", 10.00, "online", "AliExpress"),
            ("Stepper motor + driver", 1, "set", 25.00, "online", "Amazon"),
            ("Brass nozzle blanks", 3, "pcs", 7.00, "online", "AliExpress"),
            ("Pillow block bearings", 2, "pcs", 8.00, "hardware", "Hardware store"),
        ],
    },
    "water_ec": {
        "name": "Electrocoagulation Unit",
        "items": [
            ("10L clear tank (glass/acrylic)", 1, "pcs", 40.00, "online", "Amazon / food container"),
            ("Aluminum plates 6\"x8\"x1/8\"", 6, "pcs", 5.00, "hardware", "Metal supply"),
            ("DC power supply 0-30V 10A", 1, "pcs", 60.00, "online", "eBay/Amazon"),
            ("Air pump + stone diffuser", 1, "set", 20.00, "online", "Aquarium supply"),
            ("PVC pipe + elbows", 1, "lot", 20.00, "hardware", "Hardware store"),
            ("Digital pH meter", 1, "pcs", 20.00, "online", "Amazon"),
            ("Timer relay", 1, "pcs", 15.00, "online", "Amazon"),
            ("Ring terminals + wire", 1, "lot", 10.00, "hardware", "Hardware store"),
            ("Heat shrink tubing", 1, "lot", 5.00, "hardware", "Hardware store"),
        ],
    },
    "water_mag": {
        "name": "Magnetic Microplastic Separator",
        "items": [
            ("Neodymium magnets N52", 20, "pcs", 2.50, "online", "Amazon / K&J Magnetics"),
            ("Peristaltic pump 12V", 1, "pcs", 40.00, "online", "Amazon"),
            ("Iron sulfate (FeSO4) 1kg", 1, "bag", 20.00, "online", "Hydroponics store"),
            ("PVC tubing 1/2\"", 10, "ft", 1.00, "hardware", "Hardware store"),
            ("PVC fittings assorted", 1, "lot", 20.00, "hardware", "Hardware store"),
            ("Drum/roller (from old printer)", 1, "pcs", 15.00, "salvage", "Old printer / thrift store"),
        ],
    },
    "water_uv": {
        "name": "Advanced Oxidation Reactor",
        "items": [
            ("UV-C LEDs 275nm", 15, "pcs", 7.00, "online", "Amazon"),
            ("Quartz flow tube", 1, "pcs", 50.00, "online", "Lab supply"),
            ("H2O2 dosing pump", 1, "pcs", 40.00, "online", "Aquarium dosing pump"),
            ("Titanium dioxide powder 100g", 1, "bag", 20.00, "online", "Pigment store"),
            ("Mylar reflective sheet", 1, "sheet", 10.00, "online", "Amazon"),
            ("Aluminum tape", 1, "roll", 10.00, "hardware", "Hardware store"),
        ],
    },
}

# Add remaining systems with simpler BOMs
FULL_BOM["shredder"] = {
    "name": "Shredder & Sorting Station",
    "items": [
        ("Heavy-duty paper shredder", 1, "pcs", 40.00, "salvage", "Thrift store"),
        ("Blender (old)", 1, "pcs", 20.00, "salvage", "Thrift store"),
        ("5-gallon buckets with lids", 7, "pcs", 5.00, "hardware", "Hardware store"),
        ("Mesh screens (3 sizes)", 3, "pcs", 10.00, "hardware", "Hardware store"),
        ("Strong magnets", 5, "pcs", 4.00, "online", "Amazon"),
    ],
}

FULL_BOM["pyrolysis"] = {
    "name": "Microwave Pyrolysis Reactor",
    "items": [
        ("Dead microwave", 1, "pcs", 0.00, "salvage", "Craigslist free section"),
        ("Stainless steel canister", 1, "pcs", 30.00, "hardware", "Kitchen supply"),
        ("Copper refrigerator coil", 1, "pcs", 25.00, "salvage", "Old fridge / HVAC shop"),
        ("Mason jars (quart)", 6, "pcs", 2.00, "hardware", "Hardware store"),
        ("High-temp silicone sealant", 1, "tube", 15.00, "hardware", "Hardware store"),
        ("Activated carbon 1kg", 1, "bag", 20.00, "online", "Amazon"),
        ("K-type thermocouple", 1, "pcs", 25.00, "online", "Amazon"),
    ],
}


def generate_shopping_list(system_ids, fmt="text"):
    """Generate organized shopping list."""
    all_items = []
    for sid in system_ids:
        if sid not in FULL_BOM:
            continue
        bom = FULL_BOM[sid]
        for item in bom["items"]:
            name, qty, unit, unit_price, source, source_detail = item
            all_items.append({
                "system": bom["name"],
                "item": name,
                "qty": qty,
                "unit": unit,
                "unit_price": unit_price,
                "total": qty * unit_price,
                "source": source,
                "source_detail": source_detail,
            })

    if fmt == "csv":
        return _format_csv(all_items)
    elif fmt == "markdown":
        return _format_markdown(all_items, system_ids)
    else:
        return _format_text(all_items)


def _format_text(items):
    """Plain text shopping list grouped by source."""
    sources = {}
    for item in items:
        src = item["source"]
        sources.setdefault(src, []).append(item)

    lines = ["Shopping List\n"]
    grand_total = 0

    source_labels = {
        "hardware": "Hardware Store",
        "online": "Online (Amazon/eBay/AliExpress)",
        "salvage": "Salvage / Thrift",
        "restaurant_supply": "Restaurant Supply",
    }

    for src in ["hardware", "online", "salvage", "restaurant_supply"]:
        if src not in sources:
            continue
        lines.append(f"\n  {source_labels.get(src, src)}:")
        for item in sources[src]:
            total = item["total"]
            grand_total += total
            lines.append(
                f"    [{' ':1}] {item['qty']}x {item['item']:40s}"
                f"  ${total:>6.0f}  ({item['source_detail']})"
            )

    lines.append(f"\n  Grand Total: ${grand_total:,.0f}")
    return "\n".join(lines)


def _format_csv(items):
    """CSV output for spreadsheet import."""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        "system", "item", "qty", "unit", "unit_price", "total", "source", "source_detail"
    ])
    writer.writeheader()
    for item in items:
        writer.writerow(item)
    return output.getvalue()


def _format_markdown(items, system_ids):
    """Markdown table output."""
    lines = ["# Bill of Materials\n"]
    grand_total = 0

    # Group by system
    by_system = {}
    for item in items:
        by_system.setdefault(item["system"], []).append(item)

    for system_name, sys_items in by_system.items():
        sys_total = sum(i["total"] for i in sys_items)
        grand_total += sys_total
        lines.append(f"\n## {system_name} (${sys_total:.0f})\n")
        lines.append("| Item | Qty | Unit Price | Total | Source |")
        lines.append("|------|-----|-----------|-------|--------|")
        for item in sys_items:
            lines.append(
                f"| {item['item']} | {item['qty']} | "
                f"${item['unit_price']:.0f} | ${item['total']:.0f} | "
                f"{item['source_detail']} |"
            )

    lines.append(f"\n**Grand Total: ${grand_total:,.0f}**")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate bill of materials")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--systems", nargs="+", choices=list(FULL_BOM.keys()),
                       help="Systems to include")
    group.add_argument("--all", action="store_true", default=True,
                       help="Include all systems (default)")
    parser.add_argument("--format", choices=["text", "csv", "markdown"],
                        default="text", help="Output format (default: text)")
    args = parser.parse_args()

    ids = args.systems if args.systems else list(FULL_BOM.keys())
    print(generate_shopping_list(ids, args.format))
