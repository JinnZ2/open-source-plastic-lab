# Legacy — Scale-to-Business Plan

> **Ledger entry:** [L-005](./README.md#l-005--the-scale-to-business-trajectory)
> **Status:** superseded — out of scope, not disproven
> **Removed from:** `forest_plastic_lab.md`
> **Superseded by:** the Scope Statement in `README.md` (commit `546cd6f`, 2025-09-02)

This is the growth trajectory the build guide originally ended with. It was
written when the project was aimed at becoming a business. The repository was
later, deliberately, re-scoped to personal sufficiency:

> "This repository is a prototype designed for personal sufficiency, testing,
> and symbolic exploration. It is **not** intended for scaling,
> commercialization, or mass-production... Prioritizes anonymity, autonomy, and
> independence over growth or competition."

Nothing below was tested and found false. It stopped being what this repo is
for. It is kept intact because a fork aimed at a co-op, a makerspace, or a
community shop starts here rather than from nothing — and because the reasoning
in it still holds for anyone who *does* want that.

Read it as a different project's plan, not this one's roadmap.

---

## Days 26-27: Market Development

- Create product samples
- Photo document everything
- Set up online presence
- Contact local buyers
- Price products competitively

---

## Scaling to Business

### Month 2-3 Goals

- Process 50kg/day
- Establish supply chain
- Hire part-time help
- Apply for green grants
- Create brand identity

### Month 4-6 Goals

- Process 200kg/day
- Automated systems
- Retail partnerships
- B2B chemical sales
- Educational workshops

### Year 1 Vision

- 1 ton/day processing
- 5-10 employees
- Multiple locations
- Product certification
- Industry recognition

---

## Community Impact Model

### Environmental Benefits

- Forests cleaned: 10-50 acres/month
- Plastic diverted: 1-5 tons/month
- Carbon offset: 2-10 tons CO2/month
- Wildlife protected: Immeasurable

### Social Benefits

- Jobs created: 2-10 locally
- Skills taught: 50+ people/year
- Youth engaged: School programs
- Community pride: Clean forests

### Economic Benefits

- Revenue generated: $3k-15k/month
- Local spending: 80% of revenue
- Tax contribution: Business + sales
- Property values: Increase with clean environment

---

## Original closing steps

1. **This month:** Process first $100 of products
1. **Next month:** Scale to daily production
1. **This year:** Build thriving green business

---

## If you do fork this toward a business

These figures were never validated and they inherit every unknown in
[the open-unknowns table](./README.md#open-unknowns-collected). Before
committing money to them, note that:

- **Every revenue figure depends on unverified prices.** See
  [L-004](./README.md#l-004--microplastic-recovery-of-1050-kg-per-1000-l) and
  [L-007](./README.md#l-007--recycled-filament-at-2050kg). The single largest
  number in the water treatment case rests on a price nobody has ever quoted.
- **The throughput ladder was never rate-checked.** 50 kg/day, then 200, then
  1000 — against a shredder that is a modified thrift-store paper shredder and
  a pyrolysis reactor documented as running 100 g batches. Run
  `python -m models.design.flow_simulator` before believing any of these.
- **Permitting is absent entirely.** Pyrolysis, chemical recovery, and effluent
  discharge are regulated activities almost everywhere once they leave the
  hobby scale. Nothing in the original plan accounted for that, and at 1 t/day
  it dominates.
- **Power was never sized.** See
  [L-006](./README.md#l-006--off-grid-ready-unquantified). One garage-scale
  lab already needs ~2.6 kW of array. A ton per day is an industrial service.

That is not an argument against scaling. It is the list of things to measure
first, which is exactly the list the original plan skipped.
