# Complete Forest Plastic Processing Lab - Build Plan

## Your 30-Day Journey: From Zero to Full Production

### Overview: The Integrated System

Building all 7 systems creates a complete plastic processing lab where each system feeds the others:

- **Cleaning station** → prepares all plastics
- **Sorter/shredder** → feeds all other systems
- **Filament maker** → highest value for clean plastics
- **Pyrolysis unit** → handles dirty/mixed plastics
- **Chemical recovery** → processes PET specifically
- **Carbon converter** → uses waste from other processes
- **Mold press** → uses any plastic type

**Total investment:** $1,800-2,750
**Potential daily revenue:** $100-500 — *projected, never measured. See [`Docs/method.md`](./Docs/method.md).*
**Space needed:** Single garage or 200 sq ft

> **Scope.** This is a personal-sufficiency build, not a business plan. The
> growth trajectory this guide originally ended with — 50 kg/day, then a ton,
> then employees — was moved to
> [`legacy/business-scaling-plan.md`](./legacy/business-scaling-plan.md) when
> the project was re-scoped. It is preserved in full, and still a fine starting
> point if you're forking toward a co-op or community shop.
>
> **Every number below is a hypothesis.** Costs, yields, temperatures, and
> revenues are estimates that have not been verified against a working build.
> Treat them as starting points to test, not specifications to trust — and when
> your build disagrees with them, that result is worth more than the estimate
> was. [`legacy/README.md`](./legacy/README.md) is where those results go.

## Week 1: Foundation Systems

### Days 1-2: Build the Ultrasonic Cleaning Station

**Why first:** Every plastic needs cleaning - this multiplies the value of everything you collect.

**Shopping list:**

- 4× 40kHz ultrasonic transducers (eBay/Amazon) - $120
- Stainless steel steam table pan (restaurant supply) - $40
- Aquarium heater (300W) - $25
- Timer outlets - $20
- PVC pipe for drainage - $15
- UV-C germicidal lamp - $30

**Build steps:**

1. Drill holes in pan bottom for transducers (use step bit)
1. Epoxy transducers in place with marine epoxy
1. Wire transducers in parallel to driver board
1. Install heater and temperature controller
1. Add drain valve at lowest point
1. Mount UV lamp above drying area
1. Test with dirty bottles - should see immediate results!

**Pro tip:** Position transducers at calculated points for standing waves - creates intense cleaning zones.

### Days 3-4: Shredding & Sorting Station

**Why second:** All other processes need plastic in small, sorted pieces.

**Shopping list:**

- Heavy-duty paper shredder (thrift store) - $30-50
- Old blender (for fine shredding) - $20
- 5-gallon buckets with lids (7 types) - $35
- Mesh screens (3 sizes) - $30
- Strong magnets (remove metal) - $20

**Build steps:**

1. Modify shredder for larger throat opening
1. Add collection bin with screen bottom
1. Set up bucket station with labels (PET, HDPE, etc.)
1. Install “float/sink” tank for density separation
1. Create workflow: rough shred → sort → fine shred → store

**Pro tip:** Paint buckets in standard recycling colors for quick sorting.

### Days 5-7: Basic Filament Extruder

**Why third:** Highest profit margins and immediate usable product.

**Shopping list:**

- Temperature PID controller kit - $35
- Auger bit (¾” × 12”) - $25
- Black iron pipe (1” × 18”) - $20
- Band heaters (2× 300W) - $60
- DC gear motor (50 RPM) - $40
- Arduino + stepper for puller - $40
- Brass nozzle blanks - $20

**Build steps:**

1. Drill pipe for auger shaft (pillow blocks at ends)
1. Wrap with band heaters and insulation
1. Machine nozzle to 3mm hole (1.75mm later)
1. Build frame from 2×4s or steel angle
1. Add hopper from cut plastic bottle
1. Wire PID controller to heaters
1. Test with clean HDPE first (easiest)

**First success milestone:** Produce your first meter of usable filament!

## Week 2: Value-Adding Systems

### Days 8-10: Microwave Pyrolysis Reactor

**Why fourth:** Handles all the plastics unsuitable for filament.

**Shopping list:**

- Dead microwave (Craigslist free) - $0
- Stainless steel canister - $30
- Copper refrigerator coil - $25
- Mason jars for collection - $10
- High-temp silicone - $15
- Activated carbon - $20
- K-type thermocouple - $25

**Build steps:**

1. Remove microwave transformer (save for plasma unit!)
1. Cut hole in top for reactor vessel
1. Install copper coil condenser in ice bath
1. Add temperature probe through microwave wall
1. Create gas-tight seal on reactor lid
1. Test WITHOUT plastic first (just carbon)
1. Start with 100g batches of PE/PP

**Critical safety:** Work outdoors or with serious ventilation. Never process PVC!

### Days 11-12: Compression Mold Press

**Why fifth:** Uses mixed plastics and makes immediately sellable products.

**Shopping list:**

- 20-ton bottle jack - $60
- Steel plates (½” × 12” × 12”) - $80
- Angle iron for frame - $50
- Cartridge heaters (4× 200W) - $60
- Temperature controller - $30
- Mold release spray - $15

**Build steps:**

1. Weld sturdy H-frame for jack
1. Drill plates for heaters (even pattern)
1. Create first mold (simple tile)
1. Add guide pins for alignment
1. Install temp controllers
1. Test with single plastic type first
1. Document time/temperature/pressure

**First product:** Make coasters or tiles - easy to sell at craft fairs!

### Days 13-14: Rest, Test, and Organize

- Catch up on any delayed steps
- Test each system thoroughly
- Organize workspace for efficiency
- Start processing collected plastics
- Calculate actual yields

## Week 3: Advanced Systems

### Days 15-17: Chemical Recovery Unit

**Why sixth:** Highest value for PET bottles specifically.

**Shopping list:**

- Pressure cooker (thrift store) - $30
- Magnetic stirrer/hotplate - $100
- Glass vessels (various) - $50
- Ethylene glycol (antifreeze) - $30
- Sodium hydroxide - $20
- pH strips and thermometer - $25
- Buchner funnel setup - $40

**Build steps:**

1. Modify pressure cooker for stirrer shaft
1. Add temperature probe port
1. Set up simple distillation apparatus
1. Create fume hood from plastic tote
1. Install washing/crystallization station
1. Test with small batch (100g PET)
1. Refine based on yield/purity

**Value add:** Pure terephthalic acid sells for $2-5/kg to chemical suppliers.

### Days 18-20: Plasma Carbon Converter

**Why last:** Most complex build, uses waste from other processes.

**Shopping list:**

- Microwave oven transformer (from day 8) - $0
- Carbon welding rods - $20
- Quartz tube (or ceramic) - $40
- Variable transformer (variac) - $60
- High voltage insulators - $30
- Cyclone separator (DIY) - $30

**Build steps:**

1. Build high voltage supply (careful!)
1. Create adjustable electrode gap
1. Install quartz reaction tube
1. Add steam injection port
1. Build cyclone collector
1. Test with pure carbon first
1. Process plastic waste gradually

**Safety critical:** This involves 2000V+ - use extreme caution. Consider buying pre-made plasma torch instead.

## Week 4: Integration and Optimization

### Days 21-23: System Integration

- Connect cleaning → shredding → processing flow
- Build unified control panel
- Add data logging (Arduino/Raspberry Pi)
- Create quality control station
- Install ventilation/safety systems

### Days 24-25: Process Optimization

**Test each pathway:**

1. Clean PET → chemicals + filament
1. Clean HDPE/PP → filament + molds
1. Mixed plastics → fuel oil + carbon
1. Contaminated → pyrolysis → carbon
1. Styrofoam → densified → filament

**Document everything:**

- Processing times
- Energy consumption
- Yield percentages
- Product quality
- Optimal parameters

### Days 26-27: Document What Actually Worked

- Create product samples from each pathway
- Photo document everything, including the failures
- Write down measured yields next to the estimates in this guide
- Note where they disagree — that gap is your real data
- File anything falsified in [`legacy/README.md`](./legacy/README.md)

*(The original market-development steps for this stretch — online presence,
contacting buyers, competitive pricing — moved to
[`legacy/business-scaling-plan.md`](./legacy/business-scaling-plan.md) with the
rest of the commercialization plan.)*

### Days 28-30: First Full Batch

- Process one full batch end to end
- Measure real inputs and outputs — weigh every stream
- Identify the bottleneck (`python -m models.design.flow_simulator`)
- Meter actual power draw and rerun `python -m models.build.power_calculator`
- Record the numbers, especially the ones that broke your assumptions

## Integrated Workspace Layout

```
VENTILATION FAN
     ↑
[PYROLYSIS] [PLASMA]     [CHEMICAL]
     ↓         ↓            ↓
[====== WORK BENCH ========]
     ↓         ↓            ↓  
[CLEANING] [SHREDDER] [FILAMENT]
     ↓         ↓            ↓
[STORAGE]  [SORTING]  [MOLD PRESS]
              ↓
         [SHIPPING]
```

## Money-Saving Build Tips

### Source Free/Cheap Materials

- Microwaves: Craigslist “free” section
- Steel: Scrap yards sell by pound
- Motors: Old treadmills have great DC motors
- Heaters: Broken coffee makers, hot plates
- Controllers: Arduino clones from AliExpress
- Insulation: Ceramic fiber from old kilns

### Tool Sharing

- Borrow/rent specialized tools
- Partner with makerspace
- Trade products for services
- Join local builder groups

### Start Small, Scale Smart

- Begin with manual processes
- Automate successful systems
- Reinvest profits immediately
- Document for replication

## Daily Production Schedule (Once Operational)

**Morning (2 hours):**

- Sort previous day’s collection
- Run cleaning station
- Start chemical recovery batch

**Midday (3 hours):**

- Operate filament extruder
- Run pyrolysis batch
- Monitor all processes

**Afternoon (2 hours):**

- Compression molding
- Carbon processing
- Package products

**Evening (1 hour):**

- Equipment maintenance
- Data logging
- Plan next day

**Potential daily output:**

- 2-5kg filament ($40-250)
- 5-10 liters fuel ($5-15)
- 1-2kg chemicals ($2-10)
- 10-20 building units ($50-200)
- 0.5-1kg activated carbon ($5-50)

## Safety Protocols for All Systems

### Essential Safety Gear

- Safety glasses (impact + UV)
- Heat-resistant gloves
- Respirator (organic vapor)
- Fire extinguisher (ABC type)
- First aid kit
- Emergency shower/eyewash

### Ventilation Requirements

- Fume hood for chemical work
- Exhaust fan for pyrolysis
- General air circulation
- Carbon filter on exhaust
- CO detector

### Electrical Safety

- GFCI on all circuits
- Proper grounding
- Insulated tools
- Lockout/tagout procedures
- Regular inspection

## Troubleshooting Guide

### Common Issues & Solutions

**Filament inconsistent diameter:**

- Check temperature stability
- Verify auger speed constant
- Clean die opening
- Adjust pulling speed

**Low pyrolysis oil yield:**

- Increase temperature
- Improve catalyst mixing
- Check for air leaks
- Pre-dry feedstock

**Poor cleaning results:**

- Verify ultrasonic power
- Check transducer placement
- Increase temperature
- Add surfactant

**Weak molded products:**

- Increase pressure
- Extend heating time
- Better material mixing
- Check mold alignment

## Scaling Beyond This Guide

This build plan stops at one working garage lab, because that is what it is
scoped to. The growth trajectory it used to end with — 50 kg/day, 200 kg/day,
1 ton/day, employees, multiple locations — along with the Community Impact
Model projecting acres cleaned and jobs created, now lives in
[`legacy/business-scaling-plan.md`](./legacy/business-scaling-plan.md).

Nothing in it was disproven. It was put out of scope by the project's own
Scope Statement, which prioritizes personal sufficiency and autonomy over
growth. It is kept intact, with notes on what you would need to measure first
if you do want to take it further. See
[L-005](./legacy/README.md#l-005--the-scale-to-business-trajectory).

## Resources and Support

### Online Communities

- r/PreciousPlastic (Reddit)
- Precious Plastic Discord
- RepRap Forums (filament)
- Open Source Ecology

### Technical Resources

- Polymer processing guides
- Safety data sheets
- Equipment manuals
- Process optimization papers

### Funding Opportunities

- EPA waste reduction grants
- State recycling incentives
- Green business loans
- Crowdfunding campaigns

### Certification Programs

- Recycled content verification
- B-Corp certification
- ISO 14001 (environmental)
- Local green business

## Your Next Steps

1. **Today:** Read [`Docs/safety.md`](./Docs/safety.md), then order materials for the cleaning station
1. **This week:** Start collecting forest plastics
1. **Next week:** Complete first 3 systems
1. **This month:** Run your first full batch and *measure* it
1. **Ongoing:** When your numbers disagree with this guide's, write down yours

That last one is not filler. Every figure in this document is an untested
estimate, and the first person to replace one with a measurement makes this
guide permanently better. The method is in [`Docs/method.md`](./Docs/method.md);
the record of what has already been tested and broken is in
[`legacy/README.md`](./legacy/README.md).
