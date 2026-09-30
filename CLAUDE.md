# CLAUDE.md

## Project Overview

Open-Source Plastic Lab — a complete, open-source, off-grid-ready plastic processing facility. This is a **hardware/DIY project** (not a traditional software project) providing a 30-day modular build plan for collecting, cleaning, and processing forest plastic waste into valuable products. Licensed under the MIT License.

**Cost:** $1,800-$2,750 (or $200-$400 with scrap salvage)

## Repository Structure

```
open-source-plastic-lab/
├── README.md                              # Project overview and introduction
├── forest_plastic_lab.md                  # Complete 30-day build plan (primary guide)
├── LICENSE                                # MIT License
├── .gitignore
├── Docs/
│   ├── method.md                          # Falsification loop + how to file a legacy entry
│   ├── quick-start.md                     # 1-day electrocoagulation build
│   ├── process-flow-diagram.md            # ASCII process flow diagram
│   ├── full-systems-flow.md               # Complete system overview with sensor stack
│   ├── safety.md                          # Critical safety protocols
│   ├── ec-wiring.md                       # Electrocoagulation wiring diagram
│   ├── magnetic-separator-wiring.md       # Magnetic separator design
│   ├── oxidation-reactor-wiring.md        # Advanced oxidation reactor wiring
│   └── build-out-materials.md             # Bill of materials with costs
├── legacy/                                # Superseded claims — kept, never deleted
│   ├── README.md                          # The precedence ledger (L-001 … L-007)
│   ├── overview-water-recovery.md         # Was Docs/overview.md (L-003)
│   ├── water-value-projections.md         # Original 10x-overstated economics (L-004)
│   └── business-scaling-plan.md           # Scale-to-business plan, out of scope (L-005)
├── models/                                # Python planning & simulation tools
│   ├── measure/
│   │   ├── sensor_logger.py               # Log Arduino sensor data to CSV via serial
│   │   ├── turbidity_monitor.py           # Analyze turbidity trends and removal efficiency
│   │   └── yield_tracker.py               # Track daily production output vs targets
│   ├── build/
│   │   ├── build_planner.py               # 30-day build schedule tracker with progress
│   │   └── power_calculator.py            # Off-grid solar/battery sizing calculator
│   ├── design/
│   │   ├── ec_simulator.py                # Electrocoagulation physics simulation
│   │   ├── pyrolysis_model.py             # Temperature/yield modeling by plastic type
│   │   └── flow_simulator.py              # Water treatment throughput & bottleneck analysis
│   ├── materials/
│   │   ├── cost_estimator.py              # Full BOM cost calculator with salvage discounts
│   │   └── bom_generator.py               # Shopping list generator (text/CSV/markdown)
│   └── scrap/
│       ├── plastic_classifier.py          # Identify plastics by code/density/visual cues
│       ├── scrap_valuator.py              # Estimate value of collected plastic waste
│       └── waste_stream.py                # Model waste composition by collection source
└── water_treatment/
    ├── README.md                          # Detailed water treatment guide
    └── controller_code/
        ├── arduino_ec_controller.ino      # Simple EC controller (Arduino Uno)
        └── master_water_controller.ino    # Full water treatment controller (Arduino Mega)
```

## Systems (7 Main + Water Treatment)

| # | System | Purpose |
|---|--------|---------|
| 1 | Ultrasonic Cleaning Station | Prepares plastics for processing |
| 2 | Shredder & Sorter | Converts waste to processable input |
| 3 | Filament Maker | 3D printing feedstock (HDPE/PP) |
| 4 | Microwave Pyrolysis Reactor | Fuel oil extraction |
| 5 | Compression Mold Press | Molded recycled products |
| 6 | Chemical Recovery Unit | PET decomposition into monomers |
| 7 | Plasma Carbon Converter | Pure carbon from waste stream |

**Water Treatment Sub-Systems:** Electrocoagulation, Magnetic Microplastic Concentrator, Bioelectrochemical Treatment Cell, Advanced Oxidation Reactor (UV + H2O2).

## Tech Stack

- **Hardware:** Arduino Uno, Nano, Mega
- **Language:** Arduino C++ (`.ino` files), Python 3 (`models/`)
- **Communication:** I2C (address `0x16` for master controller)
- **Sensors:** Turbidity (A0), pH (A1), conductivity (A2), temperature (A3), flow (pin 2)
- **IDE:** Arduino IDE for compiling and flashing
- **Python:** Standard library only (no pip dependencies except `pyserial` for sensor_logger)
- **No build system, linting, or testing framework** — this is a hardware project

## Arduino Code Conventions

- Pin constants use `UPPER_SNAKE_CASE`: `const int TURBIDITY_PIN = A0;`
- Pin arrays for grouped hardware: `const int PUMP_PINS[4] = {5, 6, 7, 8};`
- State machine pattern for multi-stage treatment processes
- Interrupt-driven flow rate calculation (`attachInterrupt`)
- I2C slave device pattern with `Wire.onRequest` / `Wire.onReceive`
- Inline comments for calibration values and hardware notes
- Simple, procedural style — avoid unnecessary abstraction
- Always include timeout fallbacks for sensor-based stage transitions

## Python Models

Run any model with: `python -m models.<category>.<module> --help`

| Category | Modules | Purpose |
|----------|---------|---------|
| `measure` | sensor_logger, turbidity_monitor, yield_tracker | Data logging and measurement |
| `build` | build_planner, power_calculator | Build scheduling and power sizing |
| `design` | ec_simulator, pyrolysis_model, flow_simulator | Physics simulations |
| `materials` | cost_estimator, bom_generator | Cost estimation and shopping lists |
| `scrap` | plastic_classifier, scrap_valuator, waste_stream | Plastic sorting and valuation |

### Python Conventions

- All models use **standard library only** (except `pyserial` for serial communication)
- Each module is runnable via `python -m` with `argparse` CLI
- Data files (CSV, JSON) go in `logs/` (gitignored)
- Keep models simple and self-contained — no shared state between modules
- Use `snake_case` for filenames and functions

## File Naming Convention

- All documentation files use **lowercase kebab-case** with `.md` extension
- Arduino sketches use **snake_case** with `.ino` extension
- Python modules use **snake_case** with `.py` extension
- Directory names use **lowercase** (`Docs/`, `water_treatment/`, `models/`)

## Key Entry Points

- **Start here:** `README.md` then `forest_plastic_lab.md` (30-day build guide)
- **Quick build:** `Docs/quick-start.md` (electrocoagulation in 1 day)
- **Water treatment:** `water_treatment/README.md`
- **Safety:** `Docs/safety.md` (read before any build work)
- **Method:** `Docs/method.md` (how claims are tested and retired)
- **Precedence ledger:** `legacy/README.md` (what was falsified, and what's still unknown)
- **Python models:** `python -m models.<category>.<module> --help`

## The Falsification Loop

This repo treats its own documentation as a set of testable claims:

```
hypothesize → run → result → falsified? → edit the claim
                                 ↓
                       search for the unknowns → rerun
```

When a claim breaks, the old wording moves to `legacy/` with an `L-NNN` ledger
entry recording what was claimed, what killed it, what replaced it, and what
remains unknown. The live doc gets the correction and a link back. **Nothing is
deleted — precedence carries.** Full procedure in `Docs/method.md`.

Three statuses: `falsified` (tested, failed), `superseded` (replaced or
re-scoped, not disproven), `unverified` (never tested, demoted from assertion
to assumption).

## Build Plan Structure (30 Days)

- **Week 1:** Cleaner, shredder, and extruder
- **Week 2:** Pyrolysis and mold press
- **Week 3:** Chemical + carbon systems
- **Week 4:** Integration, optimization, launch

## Safety-Critical Notes

This project involves **high voltage, chemicals, and thermal hazards**. Always reference `Docs/safety.md` before suggesting modifications to:
- Electrocoagulation wiring (mains voltage)
- Pyrolysis reactor (high temperatures, flammable gases)
- Chemical recovery (caustic substances)
- UV systems (radiation exposure)

## Guidelines for AI Assistants

- **Read `Docs/safety.md` before suggesting hardware/wiring changes.** Never omit safety warnings.
- **Preserve the DIY/maker tone.** This project prioritizes practical empowerment, not corporate polish.
- **Keep Arduino code simple and procedural.** No unnecessary OOP, libraries, or abstractions.
- **Respect the modular design.** Each system should work independently.
- **Documentation uses ASCII diagrams** — maintain this style rather than introducing images or external tools.
- **Cost-consciousness matters.** Suggestions should favor salvaged/cheap components.
- **Off-grid compatibility.** The water treatment train and controls run off-grid
  (~0.4 kWh/day). The thermal systems do not, at this budget (~7.8 kWh/day total,
  needing ~2.6 kW of array). Don't assert "solar-powered" for the whole lab —
  see `legacy/README.md` L-006. Check sizing with `models/build/power_calculator.py`.
- **File naming:** Use lowercase kebab-case for docs, snake_case for Arduino sketches.
- **Always add timeout fallbacks** for sensor-gated stage transitions in controller code.
- **Scope is personal sufficiency, not business.** The README Scope Statement
  (2025-09-02) rules out scaling, commercialization, and mass production. Don't
  reintroduce growth framing — that material lives in `legacy/business-scaling-plan.md`.

### Claims, numbers, and honesty

- **Verify before asserting.** If a doc says a file exists, `ls` it. L-001 is a
  package that three documents described and no commit contained — including a
  commit message listing files the commit didn't have.
- **Re-derive numbers from their stated premises** before repeating them
  downstream. L-004 is a 10× revenue error that any single multiplication would
  have caught, sitting on the same page as the premise that falsified it.
- **Never silently correct.** File the ledger entry. A quiet fix destroys the
  record, and the record is the point.
- **Distinguish "unsourced" from "wrong."** Mark unverified numbers
  `unverified` rather than deleting them or inventing citations. Do not add
  prices, yields, or efficiencies you cannot source.
- **Consistency is not correctness.** A document can be perfectly self-consistent
  and still rest on a number nobody measured. Ask "who measured this?" separately.

<!-- clone-refspec-note v1 -->
## Cloning and pushing
Shallow clones are single-branch by default.
Before pushing any branch other than main, run:

    git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
    git fetch --depth 1

Or clone with: git clone --depth 1 --no-single-branch <url>
Without this, the first push of a new branch
fails the tracking-ref check even when the
commit landed.
<!-- /clone-refspec-note v1 -->
