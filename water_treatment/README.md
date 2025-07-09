Water Treatment & Recovery Systems for Plastic Processing

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

```cpp
// Electrocoagulation Controller
#include <Wire.h>

const int VOLTAGE_CONTROL = 9;  // PWM for voltage
const int CURRENT_SENSOR = A0;
const int PH_SENSOR = A1;
const int TURBIDITY_SENSOR = A2;
const int RELAY_POLARITY = 7;

float targetCurrent = 2.0; // Amps
float phSetpoint = 7.0;
unsigned long polarityTimer = 0;
bool polarityState = false;

void setup() {
  pinMode(VOLTAGE_CONTROL, OUTPUT);
  pinMode(RELAY_POLARITY, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // Read sensors
  float current = analogRead(CURRENT_SENSOR) * 0.0264; // Calibrated
  float ph = analogRead(PH_SENSOR) * 0.0137 + 3.5;   // Calibrated
  float turbidity = analogRead(TURBIDITY_SENSOR);
  
  // Control current (simple P controller)
  int pwmValue = constrain((targetCurrent - current) * 50 + 128, 0, 255);
  analogWrite(VOLTAGE_CONTROL, pwmValue);
  
  // Switch polarity every 5 minutes to prevent passivation
  if (millis() - polarityTimer > 300000) {
    polarityState = !polarityState;
    digitalWrite(RELAY_POLARITY, polarityState);
    polarityTimer = millis();
  }
  
  // Monitor completion (turbidity drops)
  if (turbidity < 100) { // Calibrate threshold
    Serial.println("Treatment complete!");
  }
  
  delay(1000);
}
```

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

```cpp
// Master water treatment controller
#include <Wire.h>

#define I2C_ADDRESS 0x16

struct WaterData {
  float turbidity;
  float ph;
  float conductivity;
  float temperature;
  float flowRate;
  int treatmentStage;
  float microplasticsRecovered; // grams
  float powerGenerated; // mWh
} waterData;

// Pin definitions
const int PUMP_PINS[4] = {5, 6, 7, 8};
const int VALVE_PINS[6] = {22, 23, 24, 25, 26, 27};
const int UV_LAMP = 9;
const int H2O2_PUMP = 10;

// Sensors
const int TURBIDITY_PIN = A0;
const int PH_PIN = A1;
const int CONDUCTIVITY_PIN = A2;
const int FLOW_PIN = 2; // Interrupt pin

volatile int flowPulses = 0;
unsigned long lastFlowCheck = 0;

void setup() {
  Wire.begin(I2C_ADDRESS);
  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);
  
  // Initialize pins
  for(int i = 0; i < 4; i++) {
    pinMode(PUMP_PINS[i], OUTPUT);
  }
  for(int i = 0; i < 6; i++) {
    pinMode(VALVE_PINS[i], OUTPUT);
  }
  
  pinMode(UV_LAMP, OUTPUT);
  pinMode(H2O2_PUMP, OUTPUT);
  
  // Flow sensor interrupt
  attachInterrupt(digitalPinToInterrupt(FLOW_PIN), flowPulse, RISING);
}

void loop() {
  static int stage = 0;
  static unsigned long stageTimer = 0;
  
  // Update sensors
  updateSensors();
  
  // Treatment stages
  switch(stage) {
    case 0: // Filling
      digitalWrite(VALVE_PINS[0], HIGH); // Inlet open
      if(waterData.flowRate < 0.1 && millis() - stageTimer > 5000) {
        digitalWrite(VALVE_PINS[0], LOW);
        stage = 1;
        stageTimer = millis();
      }
      break;
      
    case 1: // Electrocoagulation
      digitalWrite(PUMP_PINS[0], HIGH);
      if(millis() - stageTimer > 1800000) { // 30 minutes
        digitalWrite(PUMP_PINS[0], LOW);
        stage = 2;
        stageTimer = millis();
      }
      break;
      
    case 2: // Settling
      // All pumps off
      if(millis() - stageTimer > 600000) { // 10 minutes
        stage = 3;
        stageTimer = millis();
      }
      break;
      
    case 3: // Magnetic separation
      digitalWrite(PUMP_PINS[1], HIGH);
      digitalWrite(VALVE_PINS[1], HIGH); // To magnetic drum
      if(waterData.turbidity < 50) {
        digitalWrite(PUMP_PINS[1], LOW);
        digitalWrite(VALVE_PINS[1], LOW);
        stage = 4;
        stageTimer = millis();
      }
      break;
      
    case 4: // Bio-electrochemical
      digitalWrite(PUMP_PINS[2], HIGH);
      digitalWrite(VALVE_PINS[2], HIGH);
      // Monitor power generation
      if(millis() - stageTimer > 3600000) { // 1 hour
        stage = 5;
        stageTimer = millis();
      }
      break;
      
    case 5: // Advanced oxidation
      digitalWrite(UV_LAMP, HIGH);
      digitalWrite(H2O2_PUMP, HIGH);
      digitalWrite(PUMP_PINS[3], HIGH);
      if(millis() - stageTimer > 900000) { // 15 minutes
        digitalWrite(UV_LAMP, LOW);
        digitalWrite(H2O2_PUMP, LOW);
        stage = 6;
        stageTimer = millis();
      }
      break;
      
    case 6: // Discharge clean water
      digitalWrite(VALVE_PINS[5], HIGH); // Outlet
      if(waterData.flowRate < 0.1) {
        digitalWrite(VALVE_PINS[5], LOW);
        stage = 0; // Ready for next batch
        waterData.microplasticsRecovered += 25; // Estimate
      }
      break;
  }
  
  waterData.treatmentStage = stage;
  delay(100);
}

void updateSensors() {
  waterData.turbidity = analogRead(TURBIDITY_PIN);
  waterData.ph = analogRead(PH_PIN) * 0.0137 + 3.5;
  waterData.conductivity = analogRead(CONDUCTIVITY_PIN) * 2.0;
  
  // Calculate flow rate
  if(millis() - lastFlowCheck > 1000) {
    waterData.flowRate = flowPulses * 2.25; // mL/min
    flowPulses = 0;
    lastFlowCheck = millis();
  }
}

void flowPulse() {
  flowPulses++;
}

void requestEvent() {
  Wire.write((byte*)&waterData, sizeof(waterData));
}

void receiveEvent(int numBytes) {
  // Handle commands
}
```

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
