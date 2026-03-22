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
```
