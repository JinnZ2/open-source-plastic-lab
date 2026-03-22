"""
Yield Tracker — Track daily production output against targets.

Logs what you produce each day (filament, fuel, molded goods, chemicals,
carbon) and compares against the targets from the 30-day build plan.

Usage:
    python -m models.measure.yield_tracker log --filament 3.2 --fuel 7 --molded 15
    python -m models.measure.yield_tracker summary
    python -m models.measure.yield_tracker summary --days 7
"""

import argparse
import csv
import json
from datetime import datetime, date
from pathlib import Path

DATA_DIR = Path("logs")
YIELD_FILE = DATA_DIR / "daily_yields.csv"

# Daily targets from forest_plastic_lab.md
DAILY_TARGETS = {
    "filament_kg": {"target": 3.5, "unit": "kg", "price_range": (20, 50)},
    "fuel_liters": {"target": 7.5, "unit": "L", "price_range": (1, 1.5)},
    "molded_units": {"target": 15, "unit": "pcs", "price_range": (5, 10)},
    "chemicals_kg": {"target": 1.5, "unit": "kg", "price_range": (2, 5)},
    "carbon_kg": {"target": 0.75, "unit": "kg", "price_range": (10, 50)},
}

FIELDS = ["date"] + list(DAILY_TARGETS.keys()) + ["notes"]


def log_yield(filament=0, fuel=0, molded=0, chemicals=0, carbon=0, notes=""):
    """Log a single day's production output."""
    DATA_DIR.mkdir(exist_ok=True)
    file_exists = YIELD_FILE.exists()

    row = {
        "date": date.today().isoformat(),
        "filament_kg": filament,
        "fuel_liters": fuel,
        "molded_units": molded,
        "chemicals_kg": chemicals,
        "carbon_kg": carbon,
        "notes": notes,
    }

    with open(YIELD_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print(f"Logged production for {row['date']}:")
    for key, meta in DAILY_TARGETS.items():
        val = row[key]
        target = meta["target"]
        pct = (val / target * 100) if target else 0
        bar = "#" * int(pct / 5) + "-" * max(0, 20 - int(pct / 5))
        print(f"  {key:18s} {val:6.1f} / {target:.1f} {meta['unit']:4s}  [{bar}] {pct:.0f}%")


def load_yields():
    """Load all yield records from CSV."""
    if not YIELD_FILE.exists():
        return []
    rows = []
    with open(YIELD_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key in DAILY_TARGETS:
                row[key] = float(row.get(key, 0) or 0)
            rows.append(row)
    return rows


def estimate_revenue(row):
    """Estimate revenue range for a single day's output."""
    low = 0
    high = 0
    for key, meta in DAILY_TARGETS.items():
        val = row.get(key, 0)
        if isinstance(val, str):
            val = float(val or 0)
        lo, hi = meta["price_range"]
        low += val * lo
        high += val * hi
    return low, high


def summary(last_n_days=None):
    """Print a summary of production history."""
    rows = load_yields()
    if not rows:
        print("No yield data found. Use 'log' command first.")
        return

    if last_n_days:
        rows = rows[-last_n_days:]

    print(f"Production Summary ({len(rows)} day(s))\n")

    totals = {key: 0 for key in DAILY_TARGETS}
    total_rev_low = 0
    total_rev_high = 0

    for row in rows:
        for key in DAILY_TARGETS:
            totals[key] += row[key]
        lo, hi = estimate_revenue(row)
        total_rev_low += lo
        total_rev_high += hi

    days = len(rows)
    print(f"  {'Product':18s} {'Total':>8s}  {'Daily Avg':>9s}  {'Target':>7s}  {'% Hit':>6s}")
    print(f"  {'-' * 55}")
    for key, meta in DAILY_TARGETS.items():
        total = totals[key]
        avg = total / days
        target = meta["target"]
        pct = (avg / target * 100) if target else 0
        print(f"  {key:18s} {total:8.1f}  {avg:9.1f}  {target:7.1f}  {pct:5.0f}%")

    print(f"\n  Est. Revenue:  ${total_rev_low:,.0f} - ${total_rev_high:,.0f} total")
    print(f"  Est. Daily:    ${total_rev_low / days:,.0f} - ${total_rev_high / days:,.0f} avg/day")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Track daily production yields")
    sub = parser.add_subparsers(dest="command")

    log_p = sub.add_parser("log", help="Log today's production")
    log_p.add_argument("--filament", type=float, default=0, help="Filament produced (kg)")
    log_p.add_argument("--fuel", type=float, default=0, help="Fuel oil produced (liters)")
    log_p.add_argument("--molded", type=float, default=0, help="Molded units produced")
    log_p.add_argument("--chemicals", type=float, default=0, help="Chemicals recovered (kg)")
    log_p.add_argument("--carbon", type=float, default=0, help="Carbon produced (kg)")
    log_p.add_argument("--notes", default="", help="Optional notes")

    sum_p = sub.add_parser("summary", help="Show production summary")
    sum_p.add_argument("--days", type=int, help="Show last N days only")

    args = parser.parse_args()
    if args.command == "log":
        log_yield(args.filament, args.fuel, args.molded, args.chemicals, args.carbon, args.notes)
    elif args.command == "summary":
        summary(args.days)
    else:
        parser.print_help()
