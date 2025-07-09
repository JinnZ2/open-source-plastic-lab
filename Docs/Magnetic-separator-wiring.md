# Magnetic Microplastic Separator — Wiring + Flow Design

---

## 🧲 System Overview

Goal: Use magnetically tagged microplastics to isolate them with a rotating magnetic drum.

[WASH WATER]
↓
[IRON DOSING CHAMBER]  ← peristaltic pump + FeSO₄ tank
↓
[MIXER TUBE]           ← PVC spiral, 5 min dwell time
↓
[MAGNETIC DRUM]
↓             ↓
[CLEAN WATER]   [SCRAPED MICROPLASTICS]

---

## 🔌 Wiring Schematic

**Components:**
- Peristaltic pump (12V DC)
- Magnetic drum motor (6-12V DC)
- Drum scraper servo (optional)
- Arduino Nano (for timing + sensor control)

- [12V DC IN] ─────────────┐
│
┌──────▼───────┐
│Peristaltic   │
│Pump Motor    │
└──────┬───────┘
│
┌──────▼───────┐
│Mag Drum Motor│
└──────┬───────┘
│
(Optional)
┌──────▼───────┐
│Servo Scraper │
└──────────────┘

- Use **PWM pins** from Arduino to control pump + motor speed
- Scraper can be servo or just a static blade
- Add **Hall sensor** or encoder to monitor drum RPM

---

## ⚙️ Arduino Logic (Simple Version)

```cpp
// Turn on FeSO4 dosing pump
digitalWrite(pumpPin, HIGH); delay(5000); digitalWrite(pumpPin, LOW);

// Run mixer & drum for 10 mins
analogWrite(motorPin, 120); delay(600000); analogWrite(motorPin, 0);

// Optional: scrape microplastic off drum
servo.write(90); delay(3000); servo.write(0);

optimization tips

Component
Hack
FeSO₄ dosing
Use inkjet refill syringe setup
Mixing
Use coiled garden hose in tank
Drum
Repurpose old printer roller
Scraping
Ice scraper blade + spring mount
Yield
Add dilute HCl rinse after scrape


---

### 📂 `docs/oxidation_system_wiring.md`

```markdown
# Advanced Oxidation Reactor — Wiring & Flow Schematic

---

## ☣️ System Purpose

Destroy persistent organic pollutants (POPs), PFAS, and dyes in wash water using hydroxyl radicals (·OH) from UV-C and H₂O₂.

---

## 🔬 System Flow

[POST-TREATMENT WATER]
↓
[H₂O₂ DOSER] → [UV-C TUBE COIL]
↓
[FINAL OUTPUT]

- TiO₂ coating inside quartz tube = radical generation boost
- UV-C LEDs (275nm) surround tube
- Arduino controls H₂O₂ pump + UV timing

---

## ⚡ Wiring Schematic

**Hardware:**
- UV-C LED Array (12V or 24V)
- Peroxide peristaltic pump (5V or 12V)
- Arduino Nano
- Relay Module (or N-MOSFETs)
- Flow sensor (optional)

[12V] ─────────────┐
│
┌────────▼────────┐
│ UV-C LED Array  │
└────────┬────────┘
│
┌────────▼────────┐
│ H₂O₂ Pump Motor │
└─────────────────┘

**Control:**

- Turn both on for **15 minutes per batch**
- Use relay or MOSFET for each load
- Optional: Flow sensor ensures tube is filled

---

## 🧪 Arduino Timing Sketch (Ultra Simple)

```cpp
// Run UV + H2O2 pump for 15 min
digitalWrite(uvPin, HIGH);
digitalWrite(pumpPin, HIGH);
delay(900000);
digitalWrite(uvPin, LOW);
digitalWrite(pumpPin, LOW);

