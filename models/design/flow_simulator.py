"""
Flow Simulator — Model the water treatment train timing and throughput.

Simulates the 6-stage water treatment process to estimate batch time,
daily throughput, and identify bottlenecks.

Usage:
    python -m models.design.flow_simulator
    python -m models.design.flow_simulator --volume 20 --batches 5
    python -m models.design.flow_simulator --fast-ec 20 --fast-bio 30
"""

import argparse

# Stage definitions (from master_water_controller.ino)
STAGES = [
    {"id": "filling", "name": "Filling", "default_min": 5,
     "description": "Fill tank from wash water collection"},
    {"id": "ec", "name": "Electrocoagulation", "default_min": 30,
     "description": "DC current flocculates contaminants"},
    {"id": "settling", "name": "Settling", "default_min": 10,
     "description": "Gravity separation of flocs"},
    {"id": "magnetic", "name": "Magnetic Separation", "default_min": 15,
     "description": "Extract magnetized microplastics"},
    {"id": "bio", "name": "Bio-electrochemical", "default_min": 60,
     "description": "Bacterial digestion + power generation"},
    {"id": "oxidation", "name": "Advanced Oxidation", "default_min": 15,
     "description": "UV + H2O2 destroy persistent pollutants"},
    {"id": "discharge", "name": "Discharge", "default_min": 5,
     "description": "Output clean water for reuse"},
]

# Recovery estimates per 10L batch
RECOVERY_PER_10L = {
    "microplastics_g": 5.0,      # 0.5 g/L average
    "metal_sludge_g": 10.0,
    "power_mwh": 0.5,
    "clean_water_l": 9.5,        # ~5% lost to sludge
}


def simulate_batch(volume_l, overrides=None):
    """Simulate a single treatment batch and return timing."""
    overrides = overrides or {}
    scale = volume_l / 10.0  # Scale times for larger volumes

    results = []
    for stage in STAGES:
        base_min = overrides.get(stage["id"], stage["default_min"])
        # Filling and discharge scale linearly; treatment stages scale sub-linearly
        if stage["id"] in ("filling", "discharge"):
            adjusted = base_min * scale
        else:
            adjusted = base_min * (scale ** 0.7)  # Sub-linear scaling
        results.append({
            "id": stage["id"],
            "name": stage["name"],
            "minutes": round(adjusted, 1),
            "description": stage["description"],
        })
    return results


def print_batch(batch_results, volume_l, batch_num=1):
    """Print results for a single batch."""
    total_min = sum(s["minutes"] for s in batch_results)
    hours = total_min / 60

    print(f"\n  Batch {batch_num}: {volume_l}L")
    print(f"  {'Stage':25s} {'Time':>7s}  {'Cumulative':>10s}  Description")
    print(f"  {'-' * 75}")

    cumulative = 0
    for stage in batch_results:
        cumulative += stage["minutes"]
        print(f"  {stage['name']:25s} {stage['minutes']:>5.1f}m  {cumulative:>8.1f}m   {stage['description']}")

    print(f"\n  Total batch time: {total_min:.0f} min ({hours:.1f} hours)")
    return total_min


def simulate_day(volume_l, n_batches, overrides=None):
    """Simulate a full day of treatment batches."""
    batch = simulate_batch(volume_l, overrides)
    batch_time = sum(s["minutes"] for s in batch)
    total_time = batch_time * n_batches

    scale = volume_l / 10.0
    daily_recovery = {
        k: v * scale * n_batches for k, v in RECOVERY_PER_10L.items()
    }

    print("Water Treatment Flow Simulation")
    print(f"  Volume per batch: {volume_l}L")
    print(f"  Batches per day:  {n_batches}")

    print_batch(batch, volume_l)

    print(f"\n  Daily Summary ({n_batches} batches):")
    print(f"    Total time:          {total_time:.0f} min ({total_time / 60:.1f} hours)")
    print(f"    Water processed:     {volume_l * n_batches:.0f} L")
    print(f"    Clean water output:  {daily_recovery['clean_water_l']:.0f} L")
    print(f"    Microplastics:       {daily_recovery['microplastics_g']:.0f} g")
    print(f"    Metal sludge:        {daily_recovery['metal_sludge_g']:.0f} g")
    print(f"    Power generated:     {daily_recovery['power_mwh']:.1f} mWh")

    # Bottleneck analysis
    longest = max(batch, key=lambda s: s["minutes"])
    print(f"\n  Bottleneck: {longest['name']} ({longest['minutes']:.0f} min)")
    print(f"  Reducing '{longest['name']}' time has the most impact on throughput.")

    if total_time > 480:  # More than 8 hours
        print(f"\n  WARNING: {total_time / 60:.1f} hours exceeds a standard 8-hour day.")
        max_batches = int(480 / batch_time)
        print(f"  Max batches in 8 hours: {max_batches}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate water treatment throughput")
    parser.add_argument("--volume", type=float, default=10, help="Liters per batch (default: 10)")
    parser.add_argument("--batches", type=int, default=3, help="Batches per day (default: 3)")

    # Allow overriding individual stage times
    parser.add_argument("--fast-ec", type=float, help="Override EC time (minutes)")
    parser.add_argument("--fast-bio", type=float, help="Override bio-electrochemical time (minutes)")
    parser.add_argument("--fast-oxidation", type=float, help="Override oxidation time (minutes)")
    args = parser.parse_args()

    overrides = {}
    if args.fast_ec:
        overrides["ec"] = args.fast_ec
    if args.fast_bio:
        overrides["bio"] = args.fast_bio
    if args.fast_oxidation:
        overrides["oxidation"] = args.fast_oxidation

    simulate_day(args.volume, args.batches, overrides)
