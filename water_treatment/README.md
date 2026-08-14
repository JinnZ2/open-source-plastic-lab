# Water Treatment & Recovery Systems for Plastic Processing

## The Hidden Value in Wash Water

Every kilogram of forest plastic you clean releases:

- 10-50g microplastics (worth $1-25)
- 0.1-1g heavy metals (worth $0.10-10)
- 5-20g biofilm/organics (compost value)
- Chemical additives (potential recovery)

**Don’t dump it - mine it!**

## System 1: Electrocoagulation Recovery Unit

### How It Works

Low-voltage DC current between sacrificial electrodes causes:

1. Metal ions released from anode
1. Contaminants neutralized and flocculated
1. Bubbles float flocs to surface
1. Clean water exits bottom

### Build Instructions

**Materials List:**

- 10L clear acrylic/glass tank - $40
- Aluminum plates (6” × 8” × 1/8”) × 6 - $30
- DC power supply (0-30V, 10A) - $60
- Air pump + diffuser stone - $20
- PVC for baffles/flow control - $20
- pH meter - $30
- Timer relay - $15

**Construction:**

```
[DIRTY WATER IN]
      ↓
┌─────────────────┐
│ ┌─┐ ┌─┐ ┌─┐   │ ← Aluminum plates
│ │+│ │-│ │+│   │   (alternating polarity)
│ │ │ │ │ │ │   │
│ │ │ │ │ │ │   │ ← Bubble curtain
│ └─┘ └─┘ └─┘   │
│  ○ ○ ○ ○ ○    │ ← Air diffuser
└────┬─────┬─────┘
     ↓     ↓
[SLUDGE] [CLEAN]
```

**Operating Parameters:**

- Voltage: 12-24V DC
- Current density: 10-50 mA/cm²
- Treatment time: 20-45 minutes
- pH adjustment: 6.5-7.5 optimal
- Plate spacing: 1-2cm

**Value Recovery:**

- Aluminum hydroxide sludge: $0.50-2/kg (water treatment coagulant)
- Captured microplastics: Concentrate for processing
- Clean water: Reuse in cleaning station
- Energy use: 0.5-2 kWh/m³

### Arduino Control Code

See [`controller_code/arduino_ec_controller.ino`](controller_code/arduino_ec_controller.ino) for the full controller sketch. It handles PWM voltage control, polarity switching every 5 minutes, and turbidity monitoring.

## System 2: Magnetic Microplastic Concentrator

### Physics Principle

Microplastics develop surface charges in water. Iron ions bind to these sites, making them magnetic. This allows magnetic separation without damaging the plastic structure.

### Build Design

**Materials:**

- Neodymium magnets (N52 grade) × 20 - $50
- Peristaltic pump - $40
- Iron sulfate solution - $20
- PVC pipe + fittings - $30
- Magnetic drum (DIY from printer roller) - $40
- Collection vessels - $20

**Process Flow:**

```
[WASH WATER] → [IRON DOSING] → [MIXING ZONE] → [MAGNETIC DRUM]
                                                        ↓
                                              [MICROPLASTIC SLURRY]
                                                        ↓
                                              [ACID WASH] → [PURE MICROPLASTICS]
```

**Operating Steps:**

1. Dose wash water with 50-100 ppm iron sulfate
1. Mix for 5 minutes at pH 6-7
1. Flow past rotating magnetic drum
1. Scrape magnetic particles into collection
1. Wash with dilute acid to remove iron
1. Result: Concentrated microplastics

**Value Outputs:**

- Microplastic concentrate: $100-500/kg
- Iron recovery: Reuse in process
- Processing rate: 50-100L/hour
- Removal efficiency: 95%+

## System 3: Bioelectrochemical Treatment Cell

### The Living Battery That Cleans Water

Certain bacteria can transfer electrons directly to electrodes while consuming organic contamination. This creates a fuel cell that generates power while cleaning!

**Materials:**

- Glass/acrylic chamber (2 compartments) - $50
- Carbon felt electrodes (12” × 12”) × 2 - $40
- Proton exchange membrane (or salt bridge) - $30
- Resistor box (variable load) - $20
- Activated sludge (seed bacteria) - Free
- Air pump for cathode - $20

**Construction:**

```
┌─────────┬─────────┐
│ ANODE   │ CATHODE │
│         │         │
│ ████░░░ ┊ ░░░████ │  ← Carbon felt
│ ████░░░ ┊ ░░░████ │
│ (bacteria) (air)  │
│         ┊         │
└─────────┴─────────┘
     ↑         ↑
[DIRTY IN] [CLEAN OUT]
     
   [LOAD RESISTOR]
   [POWER OUTPUT!]
```

**Inoculation Process:**

1. Fill anode with wash water + 10% activated sludge
1. Keep anaerobic (no oxygen)
1. Feed cathode with air
1. Connect through 1000Ω resistor initially
1. Monitor voltage (should reach 0.3-0.7V)
1. Decrease resistance as biofilm develops

**Performance:**

- Power density: 10-50 mW/m²
- COD removal: 80-95%
- Heavy metal reduction: 60-80%
- Self-sustaining once established

## System 4: Advanced Oxidation Reactor

### Breaking Down the “Forever Chemicals”

Uses UV + hydrogen peroxide to create hydroxyl radicals that destroy even PFAS compounds.

**Materials:**

- UV-C LED array (275nm) - $100
- Quartz flow tube - $50
- Hydrogen peroxide dosing pump - $40
- Titanium dioxide coating - $30
- Reflective chamber - $20

**Process Chemistry:**

```
H₂O₂ + UV → 2·OH (hydroxyl radicals)
·OH + Contaminants → CO₂ + H₂O + minerals
```

**Design Features:**

- Spiral quartz tube for maximum UV exposure
- TiO₂ coating amplifies radical generation
- Peroxide injection optimized by Arduino
- Real-time monitoring via UV absorbance

## Integrated Water Treatment Train

### Complete System Flow

```
[ULTRASONIC CLEANING TANK]
           ↓
    [SETTLING TANK]
           ↓
[ELECTROCOAGULATION] → [SLUDGE RECOVERY]
           ↓
[MAGNETIC SEPARATION] → [MICROPLASTIC RECOVERY]
           ↓
[BIOELECTROCHEMICAL] → [POWER GENERATION]
           ↓
[ADVANCED OXIDATION] → [FINAL POLISH]
           ↓
   [REUSE OR DISCHARGE]
```

### Daily Value Recovery (from 1000L wash water)

> **Corrected.** The figures that used to sit here were overstated by 10× —
> falsified by this document's own premise. The original numbers, the
> arithmetic that broke them, and why it matters are preserved in
> [`../legacy/water-value-projections.md`](../legacy/water-value-projections.md)
> ([L-004](../legacy/README.md#l-004--microplastic-recovery-of-1050-kg-per-1000-l)).

Derived from the 10–50 g/kg figure at the top of this page, and 1000 L washing
100 kg of plastic. Check the multiplication yourself — the last person didn't:

```
Microplastic mass    100 kg × 10–50 g/kg        =  1 – 5 kg
Microplastic value   1–5 kg × $100–500/kg  [!]  =  $100 – $2,500
Metal sludge         5–10 kg × $0.50–2/kg       =  $2.50 – $20
Bioelectricity       0.5–2 kWh × ~$0.10/kWh     =  $0.05 – $0.20
Water reuse          1000 L                     =  $1 – $5
                                                  ────────────────
Total                                             $104 – $2,525
```

**`[!]` — the price is an assumption, not a rate.** No source anywhere in this
repo establishes that a buyer pays $100–500/kg for recovered mixed microplastic
concentrate, and none was found. That single unsourced number carries almost
the entire total above. Correcting the arithmetic made the figure smaller; it
did not make it true.

**Before you build this for the money, get one quote from one real buyer.** If
no buyer exists, that is the most useful thing anyone could add to this repo —
record it in [`../legacy/README.md`](../legacy/README.md) either way.

The water train still earns its place on non-revenue grounds: closed-loop
water reuse, no discharge, and recovered microplastic that feeds the pyrolysis
and carbon systems instead of the creek. Those benefits are real whether or not
the concentrate ever sells.

### Control Integration

**Arduino Mega Water Treatment Controller**

See [`controller_code/master_water_controller.ino`](controller_code/master_water_controller.ino) for the full 6-stage treatment controller. It sequences filling, electrocoagulation, settling, magnetic separation, bio-electrochemical treatment, and advanced oxidation with sensor monitoring over I2C.


## The Complete Value Chain

**Forest → Cleaning → Processing → Water Treatment → Products**

1. **Collect** 100kg forest plastics
1. **Clean** using 1000L water
1. **Process** into:
- 60-80kg filament ($1,200-4,000 *at unverified prices —* [L-007](../legacy/README.md#l-007--recycled-filament-at-2050kg))
- 10-20kg unsuitable → pyrolysis oil ($5-15)
- 1-5kg microplastics from wash → concentrate ($100-2,500 *at an unsourced price*)
- the remainder: dirt, moisture, PVC rejects, extruder purge — **weigh this**
1. **Treat** water for reuse + recover materials
1. **Projected value:** $1,305-6,515 from 100kg “trash” — *never measured*

> The original version of this chain balanced to exactly 100 kg out, with zero
> loss to contamination, moisture, or purge, and claimed 10 kg of microplastic
> from a premise that caps it at 5 kg. Both are fixed above. What has *not*
> been fixed is that no one has ever weighed a real batch — every number here
> is still arithmetic, not measurement. One scale and one afternoon closes it.

## Key Insights

**Water treatment might not be a cost — it might be another profit center.** The
"might" is load-bearing and it is new. This section used to assert it flatly,
on the strength of a price nobody has checked. What holds up regardless of
whether the concentrate ever sells:

1. **Close the loop** - No waste water discharge. Solid.
1. **Capture microplastics** - They stop going in the creek, and they feed the
   pyrolysis and carbon systems. Whether they *sell* is [open](../legacy/README.md#open-unknowns-collected).
1. **Generate power** - The bio cell is real but small; 10-50 mW/m² runs
   sensors, not heaters. Check it against `python -m models.build.power_calculator`.
1. **Meet regulations** - Often required anyway, and this genuinely does not
   depend on any price holding up.
1. **It runs off-grid** - Measured, not assumed: the whole water train plus
   controls draws ~0.4 kWh/day, about a 123 W array. The thermal systems are
   the ones that don't fit on solar
   ([L-006](../legacy/README.md#l-006--off-grid-ready-unquantified)).

The environmental case for this system never depended on the revenue case. It
is worth building either way — just build it knowing which is which.
