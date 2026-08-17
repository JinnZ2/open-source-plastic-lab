#  Open-Source Plastic Lab  
*An off-grid-ready, low-cost plastic processing facility designed for innovation, forest tinkerers, and community-scale sustainability.*

> “Don’t wait for the system to fix itself. Build a better one in your garage.”

---

##  What This Is

This repository contains a **complete 30-day build plan** to create your own modular plastic processing lab. All tools, systems, and workflows are open-source and optimized for:

-  **Low cost** ($1,800–$2,750)
-  **Off-grid operation**
-  **Recycling, repurposing, and fuel creation**
-  **Practical empowerment over theory**

Build it in a single garage. Power it with solar. Run it with just your hands and a few scavenged microwaves.

---

##  Included Systems

| System                     | Purpose                                     |
|---------------------------|---------------------------------------------|
|  Ultrasonic Cleaner      | Prepares plastics for high-quality output   |
| Shredder & Sorter       | Converts waste into processable input       |
| Filament Maker          | Turns HDPE/PP into usable 3D printing feed  |
| Pyrolysis Reactor       | Extracts fuel oil from dirty/mixed plastic  |
|  Chemical Recovery Unit  | Deconstructs PET into reusable monomers     |
|  Plasma Carbon Converter | Creates pure carbon from waste stream       |
|  Mold Press              | Molds recycled plastic into products        |

---

##  The 30-Day Build Plan

Each week focuses on a system. Each step is fully documented.

- **Week 1**: Build cleaner, shredder, and extruder
- **Week 2**: Pyrolysis and mold press
- **Week 3**: Chemical + carbon systems
- **Week 4**: Integration, optimization, launch

 Full build guide: [`forest_plastic_lab.md`](./forest_plastic_lab.md)

---

##  Python Models

Planning and simulation tools in `models/`, organized by function:

| Module | Purpose |
|--------|---------|
| `models/measure/` | Sensor logging, turbidity monitoring, yield tracking |
| `models/build/` | 30-day build planner, off-grid power calculator |
| `models/design/` | EC simulator, pyrolysis yield model, flow simulator |
| `models/materials/` | Cost estimator with salvage discounts, BOM generator |
| `models/scrap/` | Plastic classifier, scrap valuator, waste stream analyzer |

Run any model with: `python -m models.<category>.<module> --help`

---

##  How This Repo Handles Being Wrong

Every number here is a claim, and claims get tested. When one breaks, the old
wording doesn't get quietly deleted — it moves to [`legacy/`](./legacy/README.md)
with its cause of death attached, and the live doc gets the correction plus a
link back.

```
hypothesize → run → result → falsified? → edit the claim
                                             ↓
                                   search for the unknowns
                                             ↓
                                          rerun
```

- **[`Docs/method.md`](./Docs/method.md)** — the loop, and how to file an entry
- **[`legacy/README.md`](./legacy/README.md)** — the precedence ledger: what
  was claimed, what killed it, what's still unknown

Seven entries so far. A units error that overstated revenue 10×. A `.gitignore`
pattern that silently ate a whole Python package. An "off-grid" claim nobody
had ever put a number to. **Precedence carries** — a claim that was tested and
failed is worth more than one nobody ever checked, so none of it gets thrown
away.

---

##  Potential Output

**These are projections. None have been measured.** They are honest guesses,
kept because a guess you can test beats no target at all — but do not plan
around them until someone has weighed a real batch.

| Product           | Daily Output | Est. Value | Verified? |
|------------------|--------------|------------|-----------|
| 3D filament       | 2–5 kg       | $40–250    | ✗ price untested ([L-007](./legacy/README.md#l-007--recycled-filament-at-2050kg)) |
| Recycled fuel oil | 5–10 liters  | $5–15      | ✗ |
| Molded goods      | 10–20 units  | $50–200    | ✗ |
| Chemicals         | 1–2 kg       | $2–10      | ✗ |
| Carbon            | 0.5–1 kg     | $5–50      | ✗ |

When your build disagrees with this table, **your numbers win** — write them
down. [`Docs/method.md`](./Docs/method.md) explains how; [`legacy/`](./legacy/README.md)
is where the results that already broke live.

---

##  Power Reality

"Off-grid-ready" now means something specific, because it finally got sized:

| Running | Daily draw | Array needed | Off-grid? |
|---------|-----------|--------------|-----------|
| Water treatment + controls | 0.4 kWh | ~123 W | Yes — one panel |
| All seven systems | 7.8 kWh | ~2.6 kW + 35 kWh battery | Not on this budget |

The thermal systems — extruder, pyrolysis, press, chemical, plasma — are
resistive heat. Run them on grid, generator, or daylight batches. Size your own
site with `python -m models.build.power_calculator --help`.
See [L-006](./legacy/README.md#l-006--off-grid-ready-unquantified).

---

##  Why This Matters

-  *Environmental independence*
-  *Practical circular economy*
-  *Off-grid resilience*
-  *Open-source empowerment*
-  *Flipping off extractive industries*

---

##  Built By

An off-grid mechanical inventor who refuses to let waste stay waste.

Want to contribute? Fork the lab.  
Build your own.  
Upload your mods.  
Change the world, or at least your zip code.

---

##  License

This work is licensed under the [MIT License](./LICENSE).
Use it. Break it. Improve it.

---

##  Join the Revolution

 Hackerspaces  
 Cleanups  
 Truck stops  
 Forests  
 Classrooms  
 Collapse-ready garages

If you can build it, you can change it.


🔍 Scope Statement

This repository is a prototype designed for personal sufficiency, testing, and symbolic exploration.
It is not intended for scaling, commercialization, or mass-production.
	•	Purpose → Serves as a working tool, proof-of-concept, or symbolic framework for local use.
	•	Design Philosophy → Built on principles of fit-for-purpose sufficiency, resilience, and personal autonomy, not corporate scaling.
	•	Usage → Treat this as a seed or example, to be adapted or studied as needed. It is complete in scope for its intended function.
	•	Limitations → It may lack packaging, optimization, or interfaces expected in production software—by design.
	•	Ethos → Prioritizes anonymity, autonomy, and independence over growth or competition.


Yes. I built one. 
