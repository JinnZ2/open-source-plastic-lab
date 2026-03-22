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

- Microplastics: 10-50kg @ $100-500/kg = **$1,000-25,000**
- Metal sludge: 5-10kg @ $0.50-2/kg = **$2.50-20**
- Bioelectricity: 0.5-2 kWh = **$0.05-0.20**
- Water savings: 1000L = **$1-5**
- **Total daily value: $1,003-25,025**

### Control Integration

**Arduino Mega Water Treatment Controller**

See [`controller_code/master_water_controller.ino`](controller_code/master_water_controller.ino) for the full 6-stage treatment controller. It sequences filling, electrocoagulation, settling, magnetic separation, bio-electrochemical treatment, and advanced oxidation with sensor monitoring over I2C.


## The Complete Value Chain

**Forest → Cleaning → Processing → Water Treatment → Products**

1. **Collect** 100kg forest plastics
1. **Clean** using 1000L water
1. **Process** into:
- 80kg filament ($1,600-4,000)
- 10kg unsuitable → pyrolysis oil ($5-15)
- 10kg microplastics from wash → concentrate ($1,000-5,000)
1. **Treat** water for reuse + recover materials
1. **Total value:** $2,605-9,015 from 100kg “trash”

## Key Insights

**Water treatment isn’t a cost - it’s another profit center!** By adding these systems:

1. **Close the loop** - No waste water discharge
1. **Capture microplastics** - Highest value per kg
1. **Generate power** - Offset energy costs
1. **Meet regulations** - Often required anyway
1. **Marketing advantage** - “Zero discharge facility”
