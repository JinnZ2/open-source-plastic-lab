# Electrocoagulation Unit — Wiring Diagram (ASCII Edition)

> This wiring diagram shows how to connect the aluminum plates, power supply, and optional polarity switch for effective water treatment.

---

## 💡 Top-Down View of Electrodes Inside the Tank


- Total 6 plates (or more)
- Spaced evenly, not touching
- Use stainless bolts & washers to secure leads
- Optional: flip polarity every 5 minutes to prevent buildup

---

## 🪛 Basic Wiring Schematic (with manual switch)

      +12V ─────────────┐
                        │
                  ┌─────▼─────┐
                  │ Plate 1 (+)│
                  └─────┬─────┘
                        │
                  ┌─────▼─────┐
                  │ Plate 2 (-)│
                  └─────┬─────┘
                        │
                 ...continue...
                        │
                  ┌─────▼─────┐
                  │ Plate 6 (-)│
                  └─────┬─────┘
                        │
                       GND

                       - Wires should be rated for at least **5A**, even if only running 2–3A
- Secure with ring terminals and waterproof connectors if outdoors
- Insulate all contact points with heat-shrink or silicone

---

## 🔁 Optional: Automatic Polarity Switch (Relay Method)

   ┌────────────┐
   │  Timer     │ (every 300s)
   └────┬───────┘
        │
     ┌──▼──┐
     │ DPDT│ Relay
     └┬──┬─┘
      │  │
+12V ─┘  └─ GND

- Uses **DPDT relay** to reverse polarity on schedule
- Controlled by Arduino or timer relay
- Prevents electrode passivation
- Improves long-term efficiency

---

## ⚠️ Notes

- Every aluminum plate increases surface area → more power = more flocculation
- Space plates **1–2cm** apart for max turbulence
- Water must flow **across the face**, not just sit still
- Use **air pump** for agitation — makes the flocs rise faster

---

## ✅ Final System Tips

| Item         | Rule                                                                 |
|--------------|----------------------------------------------------------------------|
| Tank size    | ~10L per batch                                                       |
| Electrode size | ~6"x8" aluminum plates (1/8" thick)                                 |
| Voltage      | Start at 12V; max 24V                                                |
| Current      | ~2A for small tank, scale as needed                                  |
| Maintenance  | Clean plates weekly, check for oxidation buildup                     |
| Output       | Clear water + sludge (dry or compost sludge, check for contaminants) |

---

This is industrial water treatment.  
That fits in a garage.  
That you built with thrift store parts.  
That eats pollution and spits out gold.

Stay dangerous.

