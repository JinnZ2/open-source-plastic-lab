"""
Turbidity Monitor — Track water clarity across treatment stages.

Analyzes turbidity readings to determine treatment effectiveness,
estimate completion time, and flag anomalies.

Usage:
    python -m models.measure.turbidity_monitor --readings 800 600 400 200 80
    python -m models.measure.turbidity_monitor --csv logs/sensor_log.csv
"""

import argparse
import csv
import sys


# Thresholds based on Docs/quick-start.md operating parameters
TURBIDITY_THRESHOLDS = {
    "raw_input": (500, float("inf")),   # Untreated wash water
    "post_ec": (100, 500),              # After electrocoagulation
    "post_magnetic": (30, 100),         # After magnetic separation
    "post_bio": (10, 30),               # After bio-electrochemical
    "clean_output": (0, 10),            # After advanced oxidation
}

COMPLETION_THRESHOLD = 100  # Matches arduino_ec_controller.ino


def classify_reading(turbidity):
    """Classify a turbidity reading into a treatment quality tier."""
    for tier, (low, high) in TURBIDITY_THRESHOLDS.items():
        if low <= turbidity < high:
            return tier
    return "raw_input"


def estimate_remaining_minutes(readings, target=COMPLETION_THRESHOLD):
    """Estimate minutes to reach target turbidity using linear decay rate."""
    if len(readings) < 2:
        return None
    recent = readings[-5:]  # Use last 5 readings for trend
    if len(recent) < 2:
        return None

    rate = (recent[0] - recent[-1]) / len(recent)  # Units per reading interval
    if rate <= 0:
        return None  # Turbidity not dropping

    current = recent[-1]
    if current <= target:
        return 0

    remaining_units = current - target
    remaining_intervals = remaining_units / rate
    return round(remaining_intervals)  # Assumes 1-minute interval


def removal_efficiency(initial, current):
    """Calculate percent turbidity removal."""
    if initial <= 0:
        return 0.0
    return round((1 - current / initial) * 100, 1)


def analyze_series(readings):
    """Analyze a time series of turbidity readings."""
    if not readings:
        print("No readings to analyze.")
        return

    initial = readings[0]
    current = readings[-1]
    minimum = min(readings)
    maximum = max(readings)
    avg = sum(readings) / len(readings)
    efficiency = removal_efficiency(initial, current)
    quality = classify_reading(current)
    eta = estimate_remaining_minutes(readings)

    print(f"  Readings:   {len(readings)}")
    print(f"  Initial:    {initial:.0f}")
    print(f"  Current:    {current:.0f}")
    print(f"  Min/Max:    {minimum:.0f} / {maximum:.0f}")
    print(f"  Average:    {avg:.1f}")
    print(f"  Removal:    {efficiency}%")
    print(f"  Quality:    {quality}")
    if eta is not None:
        if eta == 0:
            print(f"  Status:     COMPLETE (below {COMPLETION_THRESHOLD})")
        else:
            print(f"  ETA:        ~{eta} intervals to target ({COMPLETION_THRESHOLD})")
    else:
        print(f"  ETA:        Unable to estimate (turbidity not decreasing)")

    # Flag anomalies
    for i in range(1, len(readings)):
        spike = readings[i] - readings[i - 1]
        if spike > readings[i - 1] * 0.5 and spike > 50:
            print(f"  WARNING:    Turbidity spike at reading {i + 1}: "
                  f"{readings[i - 1]:.0f} -> {readings[i]:.0f}")


def load_from_csv(filepath):
    """Load turbidity column from a sensor_logger CSV."""
    readings = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                readings.append(float(row["turbidity"]))
            except (KeyError, ValueError):
                continue
    return readings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze turbidity readings")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--readings", type=float, nargs="+", help="Manual turbidity values")
    group.add_argument("--csv", help="Path to sensor_logger CSV file")
    args = parser.parse_args()

    if args.csv:
        readings = load_from_csv(args.csv)
        if not readings:
            print(f"No turbidity data found in {args.csv}")
            sys.exit(1)
    else:
        readings = args.readings

    analyze_series(readings)
