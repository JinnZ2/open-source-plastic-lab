# Legacy — Original Water Treatment Value Projections

> **Ledger entry:** [L-004](./README.md#l-004--microplastic-recovery-of-1050-kg-per-1000-l)
> **Status:** falsified — internally inconsistent by 10×
> **Removed from:** `water_treatment/README.md`

These are the revenue figures the water treatment guide originally carried.
They are preserved verbatim because the *error* is instructive: the document
contained everything needed to falsify itself, on the same page, and nobody
did the multiplication for a year.

---

## As originally written

### Daily Value Recovery (from 1000L wash water)

- Microplastics: 10-50kg @ $100-500/kg = **$1,000-25,000**
- Metal sludge: 5-10kg @ $0.50-2/kg = **$2.50-20**
- Bioelectricity: 0.5-2 kWh = **$0.05-0.20**
- Water savings: 1000L = **$1-5**
- **Total daily value: $1,003-25,025**

### The Complete Value Chain

1. **Collect** 100kg forest plastics
1. **Clean** using 1000L water
1. **Process** into:
   - 80kg filament ($1,600-4,000)
   - 10kg unsuitable → pyrolysis oil ($5-15)
   - 10kg microplastics from wash → concentrate ($1,000-5,000)
1. **Treat** water for reuse + recover materials
1. **Total value:** $2,605-9,015 from 100kg "trash"

---

## What falsified it

**The premise, from the first paragraph of the same document:**

> "Every kilogram of forest plastic you clean releases: 10-50g microplastics"

**The feedstock, from the value chain in the same document:**

> "Collect 100kg forest plastics · Clean using 1000L water"

**Therefore:**

```
100 kg plastic  ×  10 g/kg   =    1,000 g  =   1 kg microplastic   (low end)
100 kg plastic  ×  50 g/kg   =    5,000 g  =   5 kg microplastic   (high end)

  claimed:  10 – 50 kg
  derived:   1 –  5 kg
  ratio:        10×  overstated
```

A clean factor-of-ten. Almost certainly a units slip — g read as kg somewhere
between the premise and the summary table — which is exactly the kind of error
that survives indefinitely when nobody re-derives the numbers downstream.

**Second failure — the mass balance doesn't close:**

```
in:   100 kg collected
out:   80 kg filament
     + 10 kg pyrolysis feed
     + 10 kg microplastic from wash
     ─────────────────────────────
      100 kg                          → zero loss to dirt, water, PVC
                                        rejects, or extruder purge
```

And the 10 kg microplastic line contradicts the premise a second time: at
50 g/kg, 100 kg of plastic cannot shed more than 5 kg.

**Third failure — cross-document, order of magnitude:**

| Source | Daily revenue claimed |
|--------|----------------------|
| `forest_plastic_lab.md` | $100–500 (whole lab) |
| `README.md` output table | $102–525 (whole lab) |
| `water_treatment/README.md` | $1,003–25,025 (water train alone) |
| `Docs/overview.md` (now [L-003](./README.md#l-003--docsoverviewmd-as-the-water-system-summary)) | $1,000–5,000 per 1000 L |

Four numbers for overlapping quantities, spanning two orders of magnitude, all
live in the repo simultaneously.

---

## Corrected arithmetic

Same method, premises applied consistently:

```
Microplastic mass    100 kg × 10–50 g/kg          =  1 – 5 kg
Microplastic value   1–5 kg × $100–500/kg   [!]   =  $100 – $2,500
Metal sludge         5–10 kg × $0.50–2/kg         =  $2.50 – $20
Bioelectricity       0.5–2 kWh × ~$0.10/kWh       =  $0.05 – $0.20
Water reuse          1000 L                       =  $1 – $5
                                                    ────────────────
Water train total                                   $104 – $2,525
```

Down from $1,003–25,025. That is the honest number **given the stated
assumptions** — and one of those assumptions is still unsourced.

---

## The unknown this exposed, which matters more than the error

Fixing the arithmetic made the number ten times smaller. It did not make it
*true*, because the price was never verified:

> **`$100–500/kg` for recovered mixed microplastic concentrate is cited
> nowhere, sourced to nobody, and has never been quoted by a buyer.**

That single figure is load-bearing under every revenue claim in the water
treatment section. Take it out and the water train's economic case is not
smaller — it is unmeasured. The corrected range above is arithmetic performed
on an assumption, which is a different thing from a result.

This is the general shape of the lesson: an internal-consistency check finds
the decimal slip, but it cannot find the missing citation. Consistency is not
correctness. A document can be perfectly self-consistent and still resting on
a number someone made up.

**To close it:** get one written quote from one real buyer for one real
kilogram of concentrate. Record the answer in
[the ledger](./README.md#open-unknowns-collected) whatever it is — including
"no buyer exists," which would be the single most valuable measurement anyone
could contribute to this repository.
