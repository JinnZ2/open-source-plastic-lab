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
│   ├── quick-start.md                     # 1-day electrocoagulation build
│   ├── process-flow-diagram.md            # ASCII process flow diagram
│   ├── full-systems-flow.md               # Complete system overview with sensor stack
│   ├── safety.md                          # Critical safety protocols
│   ├── ec-wiring.md                       # Electrocoagulation wiring diagram
│   ├── magnetic-separator-wiring.md       # Magnetic separator design
│   ├── oxidation-reactor-wiring.md        # Advanced oxidation reactor wiring
│   ├── overview.md                        # Water recovery system summary
│   └── build-out-materials.md             # Bill of materials with costs
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
- **Language:** Arduino C++ (`.ino` files)
- **Communication:** I2C (address `0x16` for master controller)
- **Sensors:** Turbidity (A0), pH (A1), conductivity (A2), temperature (A3), flow (pin 2)
- **IDE:** Arduino IDE for compiling and flashing
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

## File Naming Convention

- All documentation files use **lowercase kebab-case** with `.md` extension
- Arduino sketches use **snake_case** with `.ino` extension
- Directory names use **lowercase** (`Docs/`, `water_treatment/`)

## Key Entry Points

- **Start here:** `README.md` then `forest_plastic_lab.md` (30-day build guide)
- **Quick build:** `Docs/quick-start.md` (electrocoagulation in 1 day)
- **Water treatment:** `water_treatment/README.md`
- **Safety:** `Docs/safety.md` (read before any build work)

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
- **Off-grid compatibility.** All systems should remain compatible with solar/wind power.
- **File naming:** Use lowercase kebab-case for docs, snake_case for Arduino sketches.
- **Always add timeout fallbacks** for sensor-gated stage transitions in controller code.
