"""
Electrocoagulation Simulator — Model plate sizing, current, and treatment time.

Physics-based estimator for the EC unit based on Faraday's law
and empirical removal curves.

Usage:
    python -m models.design.ec_simulator
    python -m models.design.ec_simulator --plates 8 --voltage 18 --volume 15
"""

import argparse
import math

# Constants
FARADAY = 96485        # C/mol
AL_MOLAR_MASS = 26.98  # g/mol (aluminum)
AL_VALENCE = 3          # Al -> Al3+
WATER_DENSITY = 1.0     # kg/L


def plate_surface_area(width_cm, height_cm):
    """Active surface area of one plate face in cm²."""
    return width_cm * height_cm


def total_electrode_area(n_plates, width_cm, height_cm):
    """Total active anode area (every other plate is anode)."""
    n_anodes = n_plates // 2
    # Both faces of interior plates are active
    active_faces = n_anodes * 2
    return active_faces * plate_surface_area(width_cm, height_cm)


def current_density(current_a, area_cm2):
    """Current density in mA/cm²."""
    return (current_a * 1000) / area_cm2


def aluminum_dissolved(current_a, time_s):
    """Mass of aluminum dissolved (grams) via Faraday's law."""
    return (current_a * time_s * AL_MOLAR_MASS) / (AL_VALENCE * FARADAY)


def energy_consumption(voltage, current_a, time_s, volume_l):
    """Energy consumption in kWh per cubic meter."""
    energy_kwh = (voltage * current_a * time_s) / 3_600_000
    volume_m3 = volume_l / 1000
    return energy_kwh / volume_m3 if volume_m3 > 0 else 0


def estimate_removal(current_density_ma, time_min):
    """Empirical turbidity removal % based on current density and time.

    Based on published EC removal curves for suspended solids.
    Higher current density and longer time = better removal, with diminishing returns.
    """
    # Sigmoid-like model: removal approaches 98% asymptotically
    cd_factor = 1 - math.exp(-current_density_ma / 30)
    time_factor = 1 - math.exp(-time_min / 15)
    return min(98.0, cd_factor * time_factor * 98)


def simulate(n_plates=6, plate_w=15.24, plate_h=20.32,
             spacing_cm=1.5, voltage=12, volume_l=10, time_min=30):
    """Run a full EC simulation with the given parameters."""
    area_cm2 = total_electrode_area(n_plates, plate_w, plate_h)

    # Estimate resistance and current (simplified)
    # Conductivity of typical wash water ~500 uS/cm
    conductivity = 0.0005  # S/cm
    cell_resistance = spacing_cm / (conductivity * plate_surface_area(plate_w, plate_h))
    n_cells = n_plates - 1
    total_resistance = cell_resistance / n_cells  # Cells in parallel-ish
    estimated_current = min(voltage / max(total_resistance, 0.1), 10)  # Cap at 10A

    cd = current_density(estimated_current, area_cm2)
    al_dissolved_g = aluminum_dissolved(estimated_current, time_min * 60)
    energy_kwh_m3 = energy_consumption(voltage, estimated_current, time_min * 60, volume_l)
    removal = estimate_removal(cd, time_min)

    print("Electrocoagulation Simulation\n")
    print(f"  Configuration:")
    print(f"    Plates:           {n_plates} (aluminum, {plate_w:.1f} x {plate_h:.1f} cm)")
    print(f"    Spacing:          {spacing_cm} cm")
    print(f"    Volume:           {volume_l} L")
    print(f"    Voltage:          {voltage} V")
    print(f"    Treatment time:   {time_min} min")

    print(f"\n  Calculated:")
    print(f"    Total anode area: {area_cm2:.0f} cm²")
    print(f"    Est. current:     {estimated_current:.1f} A")
    print(f"    Current density:  {cd:.1f} mA/cm²")

    if cd < 10:
        print(f"    WARNING: Current density below 10 mA/cm² — may be too low")
    elif cd > 50:
        print(f"    WARNING: Current density above 50 mA/cm² — excessive wear")

    print(f"\n  Results:")
    print(f"    Al dissolved:     {al_dissolved_g:.1f} g")
    print(f"    Energy use:       {energy_kwh_m3:.2f} kWh/m³")
    print(f"    Est. removal:     {removal:.0f}%")
    print(f"    Plate life:       ~{200 / max(al_dissolved_g, 0.01):.0f} batches"
          f" (per plate, ~200g each)")

    # Recommendations
    print(f"\n  Recommendations:")
    if removal < 70:
        print(f"    - Increase voltage or treatment time for better removal")
    if cd < 10:
        print(f"    - Add more plates or increase voltage")
    if cd > 50:
        print(f"    - Reduce voltage or add plates to spread current")
    if energy_kwh_m3 > 5:
        print(f"    - High energy use; consider reducing voltage after initial phase")
    if removal >= 90:
        print(f"    - Excellent removal — system is well-sized")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate electrocoagulation performance")
    parser.add_argument("--plates", type=int, default=6, help="Number of plates (default: 6)")
    parser.add_argument("--plate-width", type=float, default=15.24, help="Plate width in cm (default: 15.24 / 6in)")
    parser.add_argument("--plate-height", type=float, default=20.32, help="Plate height in cm (default: 20.32 / 8in)")
    parser.add_argument("--spacing", type=float, default=1.5, help="Plate spacing in cm (default: 1.5)")
    parser.add_argument("--voltage", type=float, default=12, help="Applied voltage (default: 12)")
    parser.add_argument("--volume", type=float, default=10, help="Tank volume in liters (default: 10)")
    parser.add_argument("--time", type=float, default=30, help="Treatment time in minutes (default: 30)")
    args = parser.parse_args()

    simulate(args.plates, args.plate_width, args.plate_height,
             args.spacing, args.voltage, args.volume, args.time)
