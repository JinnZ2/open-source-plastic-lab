"""
Power Calculator — Off-grid solar and battery sizing for the lab.

Sums the daily energy of whichever systems you plan to run, then sizes the
array, battery bank, and inverter to carry it.

The point of this tool is to check the "power it with solar" claim against
real numbers before you buy panels. Heaters and magnetrons are resistive
loads; they are honest about what they cost you. Run it, look at the array
size, and decide which systems run on grid, generator, or daylight only.

Usage:
    python -m models.build.power_calculator
    python -m models.build.power_calculator --systems cleaner,shredder,extruder
    python -m models.build.power_calculator --sun-hours 3.5 --autonomy 2
    python -m models.build.power_calculator --list
"""

import argparse

# key: (label, watts, hours per day, notes)
# Wattages are nameplate draw for the parts listed in forest_plastic_lab.md
# and Docs/build-out-materials.md. Hours are from the daily schedule in
# forest_plastic_lab.md. Measure your own build — these are estimates.
SYSTEMS = {
    "cleaner":    ("Ultrasonic cleaning station", 540, 1.5, "4x transducers + 300W heater"),
    "shredder":   ("Shredder & sorter", 200, 1.0, "salvaged shredder motor, intermittent"),
    "extruder":   ("Filament extruder", 700, 3.0, "2x 300W band heaters + gear motor"),
    "pyrolysis":  ("Microwave pyrolysis reactor", 1200, 1.5, "magnetron, biggest single load"),
    "press":      ("Compression mold press", 800, 1.0, "4x 200W cartridge heaters, cycles on thermostat"),
    "chemical":   ("Chemical recovery unit", 600, 2.0, "hotplate + magnetic stirrer"),
    "plasma":     ("Plasma carbon converter", 1000, 0.5, "MOT-driven, short runs only"),
    "ec":         ("Electrocoagulation unit", 55, 1.0, "24V @ 2A + air pump"),
    "magsep":     ("Magnetic separator", 50, 1.0, "peristaltic pump + drum motor"),
    "biocell":    ("Bioelectrochemical cell", 5, 24.0, "cathode air pump; the cell itself generates"),
    "uv":         ("Advanced oxidation reactor", 60, 0.5, "UV-C LED array + dosing pump"),
    "control":    ("Controllers & logging", 5, 24.0, "Arduinos, sensors, always on"),
}

# Derate factors
PANEL_DERATE = 0.75      # dust, heat, wiring, controller losses
INVERTER_EFF = 0.90      # DC to AC conversion
BATTERY_DOD = 0.50       # lead-acid depth of discharge; use 0.80 for LiFePO4
LIFEPO4_DOD = 0.80

PANEL_WATTS = 400        # typical modern panel, for the panel count estimate


def daily_energy(keys):
    """Return (list of per-system rows, total Wh/day, peak W)."""
    rows = []
    total_wh = 0
    peak_w = 0
    for key in keys:
        label, watts, hours, note = SYSTEMS[key]
        wh = watts * hours
        total_wh += wh
        peak_w = max(peak_w, watts)
        rows.append((label, watts, hours, wh, note))
    return rows, total_wh, peak_w


def size_array(total_wh, sun_hours):
    """Solar array watts needed to replace the daily load."""
    if sun_hours <= 0:
        return 0
    return total_wh / (sun_hours * PANEL_DERATE * INVERTER_EFF)


def size_battery(total_wh, autonomy_days, system_voltage, dod):
    """Battery bank amp-hours at the given system voltage."""
    usable_wh = total_wh * autonomy_days
    bank_wh = usable_wh / (dod * INVERTER_EFF)
    return bank_wh / system_voltage, bank_wh


def size_inverter(rows):
    """Continuous inverter watts, with headroom for motor surge."""
    # Assume the two largest loads may overlap, plus 25% headroom.
    watts = sorted((r[1] for r in rows), reverse=True)[:2]
    return sum(watts) * 1.25


def main():
    parser = argparse.ArgumentParser(
        description="Size an off-grid solar system for the plastic lab.")
    parser.add_argument("--systems", default="all",
                        help="comma-separated system keys, or 'all' (default)")
    parser.add_argument("--sun-hours", type=float, default=4.5,
                        help="peak sun hours per day at your site (default 4.5)")
    parser.add_argument("--autonomy", type=float, default=2.0,
                        help="days of battery autonomy with no sun (default 2)")
    parser.add_argument("--voltage", type=int, default=48, choices=[12, 24, 48],
                        help="battery bank nominal voltage (default 48)")
    parser.add_argument("--lithium", action="store_true",
                        help="size the bank for LiFePO4 (80%% DoD) instead of lead-acid (50%%)")
    parser.add_argument("--list", action="store_true",
                        help="list system keys and exit")
    args = parser.parse_args()

    if args.list:
        print("SYSTEM KEYS")
        print("-" * 72)
        for key, (label, watts, hours, note) in SYSTEMS.items():
            print("  %-10s %-32s %5dW x %4.1fh" % (key, label, watts, hours))
            print("  %-10s   %s" % ("", note))
        return

    if args.systems == "all":
        keys = list(SYSTEMS)
    else:
        keys = [k.strip() for k in args.systems.split(",") if k.strip()]
        unknown = [k for k in keys if k not in SYSTEMS]
        if unknown:
            print("Unknown system key(s): %s" % ", ".join(unknown))
            print("Run with --list to see valid keys.")
            return
    if not keys:
        print("No systems selected.")
        return

    rows, total_wh, peak_w = daily_energy(keys)
    dod = LIFEPO4_DOD if args.lithium else BATTERY_DOD

    print("DAILY LOAD")
    print("-" * 72)
    print("%-34s %7s %7s %9s" % ("System", "Watts", "Hours", "Wh/day"))
    for label, watts, hours, wh, note in sorted(rows, key=lambda r: -r[3]):
        print("%-34s %6dW %6.1fh %8d" % (label, watts, hours, wh))
    print("-" * 72)
    print("%-34s %22.2f kWh/day" % ("TOTAL", total_wh / 1000))
    print("%-34s %22.1f kWh/month" % ("", total_wh * 30 / 1000))

    array_w = size_array(total_wh, args.sun_hours)
    bank_ah, bank_wh = size_battery(total_wh, args.autonomy, args.voltage, dod)
    inverter_w = size_inverter(rows)
    chemistry = "LiFePO4" if args.lithium else "lead-acid"

    print("\nSYSTEM SIZING  (%.1f sun-hours, %.1f days autonomy, %dV %s)"
          % (args.sun_hours, args.autonomy, args.voltage, chemistry))
    print("-" * 72)
    print("Solar array:      %6.0f W  (~%d x %dW panels)"
          % (array_w, -(-array_w // PANEL_WATTS), PANEL_WATTS))
    print("Battery bank:     %6.0f Ah at %dV  (%.1f kWh nameplate)"
          % (bank_ah, args.voltage, bank_wh / 1000))
    print("Inverter:         %6.0f W continuous  (largest single load %dW)"
          % (inverter_w, peak_w))
    print("Charge controller:%6.0f A MPPT minimum"
          % (array_w / args.voltage * 1.25))

    print("\nREALITY CHECK")
    print("-" * 72)
    if array_w > 3000:
        print("* %.1f kW of panels is a serious install, not a weekend of scrounging." % (array_w / 1000))
        print("  Heaters and the magnetron dominate. Consider running the hot")
        print("  systems on grid or generator and reserving solar for controls,")
        print("  pumps, and the water treatment train.")
    elif array_w > 1200:
        print("* Mid-size install. Batch the hot systems on sunny days to shrink")
        print("  the battery bank rather than the array.")
    else:
        print("* This is within reach of a modest DIY array.")
    print("* Resistive heat is the expensive part. Insulating the extruder barrel")
    print("  and press platens cuts Wh/day more cheaply than adding panels.")
    print("* Batch scheduling beats storage: run heat loads while the sun is up.")
    print("* These are nameplate estimates. Meter your real build with a")
    print("  clamp meter or plug-in energy monitor and rerun with your numbers.")


if __name__ == "__main__":
    main()
