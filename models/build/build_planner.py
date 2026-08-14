"""
Build Planner — 30-day build schedule tracker with progress.

Mirrors the day-by-day plan in forest_plastic_lab.md so you can see what is
done, what is next, and what it costs before you order anything.

Progress is stored in logs/build_progress.json (gitignored). Nothing is
written until you mark a task done.

Usage:
    python -m models.build.build_planner
    python -m models.build.build_planner --week 1
    python -m models.build.build_planner --done 3
    python -m models.build.build_planner --undo 3
    python -m models.build.build_planner --shopping --week 2
"""

import argparse
import json
import os

PROGRESS_FILE = os.path.join("logs", "build_progress.json")

# (id, days, week, system, task, parts cost in USD)
# Costs are the shopping-list totals from forest_plastic_lab.md.
TASKS = [
    (1, "1-2", 1, "Ultrasonic Cleaning Station", "Build cleaning tank, transducers, heater, UV dry rack", 250),
    (2, "3-4", 1, "Shredder & Sorter", "Modify shredder, bucket sort station, float/sink tank", 155),
    (3, "5-7", 1, "Filament Extruder", "Auger barrel, band heaters, PID, puller", 240),
    (4, "8-10", 2, "Microwave Pyrolysis Reactor", "Reactor vessel, condenser coil, thermocouple, seals", 125),
    (5, "11-12", 2, "Compression Mold Press", "H-frame, bottle jack, heated platens, first mold", 295),
    (6, "13-14", 2, "Rest / Test / Organize", "Catch up, test each system, measure real yields", 0),
    (7, "15-17", 3, "Chemical Recovery Unit", "Pressure cooker reactor, stirrer, fume hood, filtration", 295),
    (8, "18-20", 3, "Plasma Carbon Converter", "HV supply from MOT, electrode gap, quartz tube, cyclone", 180),
    (9, "21-23", 4, "System Integration", "Connect the flow, control panel, data logging, ventilation", 0),
    (10, "24-25", 4, "Process Optimization", "Run each pathway, document time/energy/yield", 0),
    (11, "26-27", 4, "Output Documentation", "Sample products, photograph, record what actually worked", 0),
    (12, "28-30", 4, "First Full Batch", "Process a full batch end to end, find the bottleneck", 0),
]

WEEK_THEMES = {
    1: "Foundation systems — cleaner, shredder, extruder",
    2: "Value-adding systems — pyrolysis and mold press",
    3: "Advanced systems — chemical and carbon",
    4: "Integration, optimization, first full batch",
}


def load_progress():
    """Return the set of completed task ids."""
    if not os.path.exists(PROGRESS_FILE):
        return set()
    try:
        with open(PROGRESS_FILE) as f:
            return set(json.load(f).get("completed", []))
    except (ValueError, OSError):
        print("Warning: could not read %s, starting fresh." % PROGRESS_FILE)
        return set()


def save_progress(completed):
    """Write completed task ids to the progress file."""
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"completed": sorted(completed)}, f, indent=2)


def find_task(task_id):
    for task in TASKS:
        if task[0] == task_id:
            return task
    return None


def show_schedule(completed, week=None):
    """Print the schedule, optionally filtered to one week."""
    shown = [t for t in TASKS if week is None or t[2] == week]
    if not shown:
        print("No tasks for week %s (weeks are 1-4)." % week)
        return

    current_week = None
    for task_id, days, wk, system, detail, cost in shown:
        if wk != current_week:
            current_week = wk
            print("\nWEEK %d — %s" % (wk, WEEK_THEMES[wk]))
            print("-" * 66)
        mark = "x" if task_id in completed else " "
        cost_str = "$%d" % cost if cost else "—"
        print("[%s] %2d. Days %-5s %-30s %6s" % (mark, task_id, days, system, cost_str))
        print("           %s" % detail)

    print()
    summarize(completed, shown)


def summarize(completed, shown):
    """Print completion and cost totals for the tasks shown."""
    total = len(shown)
    done = len([t for t in shown if t[0] in completed])
    spent = sum(t[5] for t in shown if t[0] in completed)
    remaining = sum(t[5] for t in shown if t[0] not in completed)

    pct = (done / total * 100) if total else 0
    bar_width = 30
    filled = int(bar_width * pct / 100)
    print("Progress: [%s%s] %d/%d systems (%.0f%%)"
          % ("#" * filled, "." * (bar_width - filled), done, total, pct))
    print("Parts bought:     $%d" % spent)
    print("Parts remaining:  $%d" % remaining)
    print("Total parts cost: $%d" % (spent + remaining))

    pending = [t for t in shown if t[0] not in completed]
    if pending:
        nxt = pending[0]
        print("\nNext up: #%d — %s (days %s)" % (nxt[0], nxt[3], nxt[1]))
    else:
        print("\nAll shown systems complete.")


def show_shopping(completed, week=None):
    """Print parts still to buy."""
    pending = [t for t in TASKS
               if t[0] not in completed and t[5] > 0
               and (week is None or t[2] == week)]
    if not pending:
        print("Nothing left to buy%s." % ("" if week is None else " for week %d" % week))
        return

    print("STILL TO BUY%s" % ("" if week is None else " — WEEK %d" % week))
    print("-" * 50)
    for task_id, days, wk, system, detail, cost in pending:
        print("  %-32s $%d" % (system, cost))
    print("-" * 50)
    print("  %-32s $%d" % ("TOTAL", sum(t[5] for t in pending)))
    print("\nSee models/materials/bom_generator.py for the itemized list.")


def main():
    parser = argparse.ArgumentParser(
        description="Track progress through the 30-day build plan.")
    parser.add_argument("--week", type=int, choices=[1, 2, 3, 4],
                        help="show only one week")
    parser.add_argument("--done", type=int, metavar="ID",
                        help="mark task ID complete")
    parser.add_argument("--undo", type=int, metavar="ID",
                        help="mark task ID incomplete")
    parser.add_argument("--shopping", action="store_true",
                        help="list parts still to buy instead of the schedule")
    parser.add_argument("--reset", action="store_true",
                        help="clear all progress")
    args = parser.parse_args()

    completed = load_progress()

    if args.reset:
        save_progress(set())
        print("Progress cleared.")
        return

    for task_id, add in ((args.done, True), (args.undo, False)):
        if task_id is None:
            continue
        task = find_task(task_id)
        if task is None:
            print("No task %d. Valid ids are 1-%d." % (task_id, len(TASKS)))
            return
        if add:
            completed.add(task_id)
            print("Marked done: #%d %s\n" % (task_id, task[3]))
        else:
            completed.discard(task_id)
            print("Marked not done: #%d %s\n" % (task_id, task[3]))
        save_progress(completed)

    if args.shopping:
        show_shopping(completed, args.week)
    else:
        show_schedule(completed, args.week)


if __name__ == "__main__":
    main()
