"""
Pyrolysis Model — Temperature/yield modeling for plastic pyrolysis.

Predicts oil, gas, and char yields based on plastic type, temperature,
and heating rate. Helps tune your microwave pyrolysis reactor.

Usage:
    python -m models.design.pyrolysis_model --plastic PE --temp 450
    python -m models.design.pyrolysis_model --plastic PP --temp-range 350 550 --step 25
"""

import argparse

# Pyrolysis yield data (weight % at optimal temperature)
# Based on published literature for batch pyrolysis
PLASTIC_DATA = {
    "PE": {
        "name": "Polyethylene (HDPE/LDPE)",
        "optimal_temp": 450,
        "melt_temp": 130,
        "yields": {  # At optimal temp
            "oil": 80, "gas": 15, "char": 5,
        },
        "oil_quality": "Diesel-like; C10-C25 hydrocarbons",
        "notes": "Best oil yield. Avoid >500C (excess gas).",
    },
    "PP": {
        "name": "Polypropylene",
        "optimal_temp": 450,
        "melt_temp": 160,
        "yields": {
            "oil": 82, "gas": 14, "char": 4,
        },
        "oil_quality": "Gasoline-like; lighter fractions than PE",
        "notes": "Similar to PE. Slightly lower viscosity oil.",
    },
    "PS": {
        "name": "Polystyrene",
        "optimal_temp": 425,
        "melt_temp": 240,
        "yields": {
            "oil": 90, "gas": 8, "char": 2,
        },
        "oil_quality": "Styrene monomer (valuable); aromatic-rich",
        "notes": "Highest oil yield. Styrene recovery possible.",
    },
    "PET": {
        "name": "PET (Polyethylene Terephthalate)",
        "optimal_temp": 500,
        "melt_temp": 260,
        "yields": {
            "oil": 40, "gas": 50, "char": 10,
        },
        "oil_quality": "Benzoic acid + terephthalic acid; waxy",
        "notes": "Low oil yield. Chemical recovery preferred (see chemical unit).",
    },
    "PVC": {
        "name": "PVC (DO NOT PYROLYZE)",
        "optimal_temp": 0,
        "melt_temp": 100,
        "yields": {
            "oil": 0, "gas": 0, "char": 0,
        },
        "oil_quality": "TOXIC — releases HCl gas",
        "notes": "NEVER process PVC in pyrolysis. Releases hydrochloric acid.",
    },
    "MIXED": {
        "name": "Mixed plastics (no PVC)",
        "optimal_temp": 450,
        "melt_temp": 160,
        "yields": {
            "oil": 65, "gas": 25, "char": 10,
        },
        "oil_quality": "Variable; blend of hydrocarbon fractions",
        "notes": "Sort out PVC first. Lower yield than pure streams.",
    },
}


def yield_at_temp(plastic_id, temp_c):
    """Estimate yields at a given temperature using a simple bell-curve model.

    Oil yield peaks at optimal_temp and drops off at lower/higher temps.
    Gas yield increases with temperature. Char yield decreases.
    """
    data = PLASTIC_DATA[plastic_id]
    if plastic_id == "PVC":
        return {"oil": 0, "gas": 0, "char": 0, "warning": "TOXIC — DO NOT PROCESS"}

    optimal = data["optimal_temp"]
    base_oil = data["yields"]["oil"]
    base_gas = data["yields"]["gas"]
    base_char = data["yields"]["char"]

    # Temperature deviation factor
    deviation = abs(temp_c - optimal) / optimal
    oil_factor = max(0, 1 - deviation * 2)  # Drops off away from optimal

    oil = base_oil * oil_factor
    # Excess goes to gas at high temp, char at low temp
    remainder = base_oil - oil
    if temp_c > optimal:
        gas = base_gas + remainder * 0.8
        char = base_char + remainder * 0.2
    else:
        gas = base_gas + remainder * 0.3
        char = base_char + remainder * 0.7

    return {"oil": round(oil, 1), "gas": round(gas, 1), "char": round(char, 1)}


def estimate_fuel_value(oil_kg, plastic_id):
    """Estimate fuel value of pyrolysis oil in USD."""
    # Rough diesel-equivalent pricing
    prices = {"PE": 0.80, "PP": 0.85, "PS": 2.50, "PET": 0.30, "MIXED": 0.60}
    price = prices.get(plastic_id, 0.60)
    return oil_kg * price


def simulate(plastic_id, temp_c, batch_kg=1.0):
    """Run pyrolysis simulation for a single temperature."""
    data = PLASTIC_DATA[plastic_id]

    if plastic_id == "PVC":
        print(f"\n  DANGER: {data['name']}")
        print(f"  {data['notes']}")
        print(f"  This model refuses to simulate PVC pyrolysis.")
        return

    yields = yield_at_temp(plastic_id, temp_c)

    oil_kg = batch_kg * yields["oil"] / 100
    gas_kg = batch_kg * yields["gas"] / 100
    char_kg = batch_kg * yields["char"] / 100
    oil_liters = oil_kg / 0.85  # Approximate density
    fuel_value = estimate_fuel_value(oil_kg, plastic_id)

    print(f"\n  Pyrolysis Simulation: {data['name']}")
    print(f"  Temperature: {temp_c}C  (Optimal: {data['optimal_temp']}C)")
    print(f"  Batch size:  {batch_kg} kg")

    print(f"\n  Predicted Yields:")
    print(f"    Oil:   {yields['oil']:5.1f}%  ({oil_kg:.2f} kg / {oil_liters:.2f} L)")
    print(f"    Gas:   {yields['gas']:5.1f}%  ({gas_kg:.2f} kg)")
    print(f"    Char:  {yields['char']:5.1f}%  ({char_kg:.2f} kg)")

    print(f"\n  Oil quality: {data['oil_quality']}")
    print(f"  Est. value:  ${fuel_value:.2f}")

    if abs(temp_c - data["optimal_temp"]) > 50:
        print(f"\n  NOTE: Temperature is {abs(temp_c - data['optimal_temp'])}C"
              f" from optimal ({data['optimal_temp']}C)")
    print(f"  {data['notes']}")


def sweep(plastic_id, temp_low, temp_high, step, batch_kg=1.0):
    """Run simulation across a temperature range."""
    data = PLASTIC_DATA[plastic_id]
    if plastic_id == "PVC":
        print("  DANGER: Will not simulate PVC pyrolysis.")
        return

    print(f"\n  Temperature Sweep: {data['name']} ({batch_kg} kg batch)")
    print(f"\n  {'Temp (C)':>8s}  {'Oil %':>6s}  {'Gas %':>6s}  {'Char %':>7s}  {'Oil (L)':>7s}  {'Value $':>8s}")
    print(f"  {'-' * 50}")

    temps = range(int(temp_low), int(temp_high) + 1, int(step))
    for t in temps:
        y = yield_at_temp(plastic_id, t)
        oil_l = (batch_kg * y["oil"] / 100) / 0.85
        val = estimate_fuel_value(batch_kg * y["oil"] / 100, plastic_id)
        marker = " <-- optimal" if t == data["optimal_temp"] else ""
        print(f"  {t:>7}C  {y['oil']:>5.1f}%  {y['gas']:>5.1f}%  {y['char']:>6.1f}%  {oil_l:>6.2f}L  ${val:>7.2f}{marker}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Model pyrolysis yields")
    parser.add_argument("--plastic", required=True, choices=list(PLASTIC_DATA.keys()),
                        help="Plastic type")
    parser.add_argument("--batch", type=float, default=1.0, help="Batch size in kg (default: 1)")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--temp", type=float, help="Single temperature (C)")
    group.add_argument("--temp-range", type=float, nargs=2, metavar=("LOW", "HIGH"),
                       help="Temperature range for sweep")

    parser.add_argument("--step", type=float, default=25, help="Step size for temp sweep (default: 25)")
    args = parser.parse_args()

    if args.temp:
        simulate(args.plastic, args.temp, args.batch)
    else:
        sweep(args.plastic, args.temp_range[0], args.temp_range[1], args.step, args.batch)
