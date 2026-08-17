# Legacy — The Precedence Ledger

**Nothing in this folder is wrong to have believed. It is wrong to still believe.**

This is where superseded claims live. Not the trash — the record. A claim that
got tested and failed is worth more than a claim nobody ever checked, because
the failure is a measurement. Someone rebuilding this lab in five years should
be able to find out what we already tried, what it cost us, and why we stopped.
That is the whole point of keeping precedence.

The working loop is documented in [`../Docs/method.md`](../Docs/method.md):

```
hypothesize → run → result → falsified? → edit the claim
                                 ↓
                       search for the unknowns
                                 ↓
                              rerun
```

This ledger is the "edit the claim" step made durable. When a claim in the live
docs gets falsified, the old wording moves here with its cause of death
attached, and the live doc gets the corrected version plus a link back.

---

## How to read an entry

| Field | Means |
|-------|-------|
| **Claim** | What the repo asserted, quoted as written |
| **Lived in** | Where it was, before |
| **Status** | `falsified` (tested, failed) · `superseded` (replaced by better) · `unverified` (never tested, demoted) |
| **What ran** | The test. If there wasn't one, say so |
| **Result** | What actually came back |
| **Edited claim** | What the repo says now |
| **Still unknown** | What we'd have to measure to close it properly |

An entry is never deleted. If a legacy claim later turns out to have been right
after all, add a new entry recording *that*, and promote the claim back. The
ledger only grows.

---

## L-001 — The `models/build/` package existed

- **Status:** `falsified` → **fixed**
- **Claim:** "13 CLI tools... `build/` — build_planner: 30-day build schedule
  tracker with progress; power_calculator: Off-grid solar/battery sizing
  calculator." Asserted in three places: commit `826a9e6`'s message,
  `README.md`, and `CLAUDE.md`.
- **Lived in:** README.md model table, CLAUDE.md repository structure.
- **What ran:** `ls models/` and `git log --all -- models/build`.
- **Result:** The directory existed in no commit, ever. Eleven of the thirteen
  advertised tools shipped; two did not.
- **Search for unknowns:** `git check-ignore -v models/build/build_planner.py`
  → `.gitignore:17:build/`. The Python-artifact ignore pattern `build/` is
  unanchored, so it matches a directory named `build` at *any* depth. The files
  were written, `git add` silently skipped them, and the commit message
  described intent rather than contents.
- **Edited claim:** `.gitignore` now uses root-anchored `/build/` and `/dist/`,
  with a comment saying why. Both modules are written and committed. The docs
  are now true.
- **Still unknown:** Whether other intended files were lost the same way. The
  ignore file has no other unanchored directory patterns, so probably not — but
  "probably" is not "checked."
- **Carries precedence:** An unanchored ignore pattern will eat your work
  without a warning. Anchor anything that could collide with a source path.

---

## L-002 — "Building all 6 systems"

- **Status:** `falsified` → **fixed**
- **Claim:** "Building all 6 systems creates a complete plastic processing lab"
  — `forest_plastic_lab.md`, overview section.
- **What ran:** Counted the bullets immediately below the sentence.
- **Result:** Seven. Cleaning, shredder/sorter, filament maker, pyrolysis,
  chemical recovery, carbon converter, mold press. `README.md` and `CLAUDE.md`
  both said seven already; only the build guide said six.
- **Edited claim:** `forest_plastic_lab.md` now says seven.
- **Carries precedence:** The mold press was added late and the intro sentence
  was never re-counted. Counts in prose go stale — prefer counting the list.

---

## L-003 — `Docs/overview.md` as the water-system summary

- **Status:** `superseded`
- **File:** [`overview-water-recovery.md`](./overview-water-recovery.md)
  (was `Docs/overview.md`)
- **Claim:** A one-page summary of the four water recovery modules, ending with
  "Microplastic sales: $1,000–5,000 per 1000L."
- **Superseded by:** [`../water_treatment/README.md`](../water_treatment/README.md),
  which covers the same four modules with build instructions, materials,
  operating parameters, and control code.
- **Why it had to go:** Not because it was thin — because it disagreed. The
  same recovery, from the same 1000 L, was priced at **$1,000–5,000** here and
  **$1,000–25,000** in `water_treatment/README.md`. Two live numbers for one
  quantity means at least one is wrong and the reader can't tell which. See
  L-004 for how that resolved.
- **Still worth reading for:** The framing. "You're not just cleaning water —
  you're mining resources from it" is the clearest one-line statement of the
  idea anywhere in the repo.

---

## L-004 — Microplastic recovery of 10–50 kg per 1000 L

- **Status:** `falsified` → **corrected**
- **File:** [`water-value-projections.md`](./water-value-projections.md)
- **Claim:** "Daily Value Recovery (from 1000L wash water) — Microplastics:
  10-50kg @ $100-500/kg = **$1,000-25,000**." Also "10kg microplastics from
  wash ($1,000-5,000)" in the value chain, and a "**Total daily value:
  $1,003-25,025**."
- **What ran:** Checked the claim against the premise stated at the top of the
  *same document*, and against the mass balance in its own value chain.
- **Result:** Falsified twice over, by its own numbers.
  1. The document opens: "Every kilogram of forest plastic you clean releases
     10-50g microplastics." Its value chain says 1000 L of wash water cleans
     100 kg of plastic. So 100 kg × 10–50 g/kg = **1–5 kg**, not 10–50 kg. The
     figure is overstated by exactly 10× — a decimal slip, most likely.
  2. The value chain has 100 kg in and 80 kg filament + 10 kg pyrolysis feed +
     10 kg recovered microplastics = 100 kg out. Zero loss to dirt, moisture,
     PVC rejects, or extruder purge. Also, at the stated 10–50 g/kg, 100 kg
     cannot shed 10 kg of microplastic — the ceiling is 5 kg.
  3. Cross-check: `forest_plastic_lab.md` puts total daily revenue at
     **$100–500**. The water train alone was claiming up to **$25,025/day**.
     Two orders of magnitude apart, in the same repo, uncontested.
- **Edited claim:** `water_treatment/README.md` now derives the mass from the
  10–50 g/kg premise, shows the arithmetic inline so the next person can check
  it, and labels the price as an untested assumption rather than a rate.
- **Still unknown — and this is the big one:** *Nobody has ever verified that a
  buyer pays $100–500/kg for recovered mixed microplastic concentrate.* No
  source is cited in this repo and none was found. That price is the load-
  bearing number under every revenue figure in the water treatment section, and
  it is unsourced. Until someone gets a real quote, treat the entire water
  revenue case as unmeasured. Fixing the mass arithmetic made the number
  smaller; it did not make it true.
- **Rerun instructions:** Weigh the dried concentrate from one real 1000 L
  batch. That closes the mass question in one afternoon and costs nothing but a
  scale. The price question needs a phone call to an actual buyer, and the
  answer belongs in this ledger either way.

---

## L-005 — The scale-to-business trajectory

- **Status:** `superseded` (by the author's own scope statement)
- **File:** [`business-scaling-plan.md`](./business-scaling-plan.md)
- **Claim:** "Scaling to Business — Month 2-3: Process 50kg/day, hire part-time
  help... Year 1 Vision: 1 ton/day processing, 5-10 employees, multiple
  locations, industry recognition," plus a Community Impact Model projecting
  "Revenue generated: $3k-15k/month" and "Jobs created: 2-10 locally."
- **Lived in:** `forest_plastic_lab.md`, final sections.
- **Superseded by:** The Scope Statement added to `README.md` on 2025-09-02
  (commit `546cd6f`), which states plainly: "This repository is a prototype
  designed for personal sufficiency, testing, and symbolic exploration. It is
  **not** intended for scaling, commercialization, or mass-production...
  Prioritizes anonymity, autonomy, and independence over growth or competition."
- **What ran:** No experiment. This is an author decision, not a measurement —
  and it is filed here precisely because that distinction matters. A claim can
  leave the live docs for two different reasons: the world contradicted it, or
  the goal changed. L-004 is the first kind. This is the second.
- **Edited claim:** The build guide now ends at the first full batch, which is
  where a personal-sufficiency project actually ends. The growth trajectory is
  preserved here in full.
- **Not retracted, just re-scoped:** Nothing in the scaling plan was shown to be
  *false*. If someone forks this lab toward a co-op or a community shop, this
  file is their starting point and it is still good. It simply stopped being
  what *this* repo is for.

---

## L-006 — "Off-grid-ready," unquantified

- **Status:** `unverified` → **now measurable**
- **Claim:** "off-grid-ready" (README subtitle), "Power it with solar"
  (README), "Off-grid compatibility. All systems should remain compatible with
  solar/wind power" (CLAUDE.md).
- **What ran:** Nothing, for the life of the repo. The claim was made in three
  places and sized in none. `models/build/power_calculator.py` was supposed to
  be the check, and it was the module that L-001 lost.
- **Result (first actual run):** All seven systems on the documented daily
  schedule draw **7.8 kWh/day**. At 4.5 peak sun hours with normal derating
  that needs roughly a **2.6 kW array**, a **35 kWh** battery bank for two days
  of autonomy, and a **2.75 kW** inverter. That system costs several times the
  lab's entire $1,800–2,750 budget.
- **The split that survives:** Run the same tool over the water treatment train
  and controls only — EC, magnetic separator, UV oxidation, bio cell, Arduinos
  — and it draws **0.38 kWh/day**, about a **123 W** array. That is genuinely a
  solar project. A single panel runs it.
- **Edited claim:** "Off-grid-ready" now means the water treatment and control
  stack. The thermal systems — extruder, pyrolysis, press, chemical, plasma —
  are resistive heat and want grid, generator, or daylight-only batch
  operation. Stated up front rather than discovered after buying panels.
- **Still unknown:** Nameplate wattage is not measured wattage. Heaters cycle on
  thermostats and rarely draw continuously; the real figure is likely lower,
  possibly much lower. A $20 plug-in energy meter on one real build day would
  replace every estimate in that module with data.

---

## L-007 — Recycled filament at $20–50/kg

- **Status:** `unverified` (demoted, not removed)
- **Claim:** "3D filament: 2–5 kg/day, $40–250" (README) and "80kg filament
  ($1,600-4,000)" (water_treatment/README.md) — both imply $20–50/kg.
- **What ran:** Nothing. No sale has been recorded in this repo.
- **Observation:** $20–50/kg is the retail price of *branded, virgin, spooled,
  diameter-controlled* filament. What this lab produces is unbranded recycled
  filament from mixed forest HDPE with hand-built diameter control. Those are
  not obviously the same product at the same price.
- **Edited claim:** Output tables are now labeled as untested projections
  rather than expected income. The numbers are unchanged — they may well be
  right — but they are marked as what they are.
- **Rerun instructions:** Sell one kilogram. One real transaction settles this
  permanently and belongs in this ledger with the price achieved.

---

## Open unknowns, collected

The falsifications above were the cheap ones — arithmetic and file listings,
findable in an afternoon. These are the ones that need the lab to actually run:

| # | Question | How to close it | Cost |
|---|----------|-----------------|------|
| 1 | Does anyone pay for recovered microplastic concentrate, and how much? | Contact a buyer, get a quote in writing | A phone call |
| 2 | How much microplastic does 1000 L of real wash water actually yield? | Weigh the dried concentrate from one batch | A scale |
| 3 | What does recycled forest-HDPE filament sell for? | Sell 1 kg | One transaction |
| 4 | What is the *measured* daily draw, versus nameplate? | Plug-in energy meter, one full production day | ~$20 |
| 5 | What is the real mass balance from 100 kg collected? | Weigh every output stream for one batch | A scale, one day |
| 6 | Do the EC removal curves in `ec_simulator.py` match this build? | Turbidity before/after, compare to `turbidity_monitor.py` | Already have the sensor |

Every one of these is a day's work or less. None have been done. That is not a
criticism of the project — it is the current, honest state of the experiment,
and writing it down is what makes the next run worth something.
