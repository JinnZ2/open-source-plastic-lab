# Method — How Claims Get Made, Broken, and Kept

**This is a lab, not a brochure. Everything in it is a claim, and claims get tested.**

A garage lab and a research lab differ in budget, not in method. The build
guides here are full of numbers — yields, temperatures, prices, throughputs —
and every one of them is a prediction about what will happen when you turn the
thing on. Predictions are testable. Most of the ones in this repo have not been
tested yet, and the honest move is to say so out loud rather than let a
confident table imply otherwise.

---

## The loop

```
   ┌─────────────────────────────────────────────────────────┐
   │                                                         │
   ▼                                                         │
HYPOTHESIZE ──▶ RUN ──▶ RESULT ──▶ falsified? ──no──▶ keep it │
 write the      do the   record             │        (say what│
 claim so it    thing    what               yes      confirmed│
 could be       for      actually            │         it)    │
 wrong          real     happened            ▼                │
                                       EDIT THE CLAIM         │
                                    old wording → legacy/     │
                                    new wording → live doc    │
                                             │                │
                                             ▼                │
                                    SEARCH FOR UNKNOWNS       │
                                    what did the failure      │
                                    reveal that nobody        │
                                    had thought to ask?       │
                                             │                │
                                             └────────────────┘
                                                  RERUN
```

Six steps. The two that get skipped are the last two, and they are the two that
make the loop a loop instead of a straight line.

---

## Step by step

### 1. Hypothesize — write it so it could be wrong

"The pyrolysis reactor works well" cannot fail, so it teaches nothing. "100 g
of clean HDPE at 450 °C yields 60–80 ml of condensable oil in under 40 minutes"
can fail in four distinct ways, each of which tells you something different.

Rule of thumb: **if you can't describe the observation that would embarrass the
claim, it isn't a claim yet.**

Numbers are good. Ranges are good. Units are mandatory —
[L-004](../legacy/README.md#l-004--microplastic-recovery-of-1050-kg-per-1000-l)
is a factor-of-ten revenue error that was, at bottom, grams read as kilograms.

### 2. Run — actually run it

Cheap tests first. Some falsifications cost nothing:

| Test | Cost | Found in this repo |
|------|------|--------------------|
| Count the items in a list | seconds | [L-002](../legacy/README.md#l-002--building-all-6-systems) |
| Re-derive a number from its own stated premise | minutes | [L-004](../legacy/README.md#l-004--microplastic-recovery-of-1050-kg-per-1000-l) |
| `ls` the directory the docs describe | seconds | [L-001](../legacy/README.md#l-001--the-modelsbuild-package-existed) |
| Check whether two docs give the same number | minutes | [L-003](../legacy/README.md#l-003--docsoverviewmd-as-the-water-system-summary) |
| Ask "who told us this price?" | one phone call | [L-007](../legacy/README.md#l-007--recycled-filament-at-2050kg), still open |

Every ledger entry so far came from a test in that table. None required the lab
to be running. Do these before you buy anything.

The `models/` tools exist for the tests that need arithmetic —
`ec_simulator`, `pyrolysis_model`, `flow_simulator`, `power_calculator`,
`cost_estimator`. A simulation is not a result, but it is a cheap way to find
out that a claim was never going to survive contact with a stopwatch.

### 3. Result — write down what happened, not what you wanted

Including the boring runs. Including the ones where you did it wrong. A run
that failed for a stupid reason still eliminates a possibility, and the next
person will make the same stupid mistake if you don't say so.

### 4. Edit the claim — and keep the old one

This is where most projects quietly cheat. The tempting move is to delete the
wrong number and write the right one, leaving a document that looks like it was
always correct. Don't.

**The old claim moves to [`legacy/`](../legacy/README.md) with its cause of
death attached. The live doc gets the corrected claim and a link back.**

Why bother:

- Someone will re-propose the failed idea. The record answers them in seconds.
- *How* it failed is often more useful than what replaced it.
- A repo with no record of being wrong reads as a repo that never checked.
- Being wrong in a recoverable, documented way is the normal state of building
  things. Hiding it teaches beginners that competence means never missing.

**Precedence carries.** A superseded claim still governs anything downstream
that was built on it, until someone re-derives that too. That is why the
entries are numbered and cross-linked rather than summarized in a changelog.

### 5. Search for unknowns — the step that pays

A falsification is not a conclusion, it's a lead. The question is always: *what
else does this failure imply, that nobody thought to ask?*

Worked example, [L-001](../legacy/README.md#l-001--the-modelsbuild-package-existed):

| | |
|---|---|
| **Claim** | `models/build/` ships two tools |
| **Test** | `ls models/` |
| **Result** | Directory does not exist. Never did, in any commit. |
| **Stop here?** | You could. "Docs were wrong, fix the docs." Two minutes. |
| **Kept going** | *Why* did two written files never reach a commit? |
| **Unknown found** | `.gitignore` line 17: `build/`, unanchored, matches at any depth |
| **Real fix** | Anchor the pattern. Otherwise the next `models/build/` vanishes too. |
| **Next unknown** | Are there other unanchored patterns? (Checked: no. Now recorded.) |

Stopping at "fix the docs" would have left a repository that silently eats any
directory named `build`. The unknown was worth more than the falsification.

Same shape in [L-004](../legacy/README.md#l-004--microplastic-recovery-of-1050-kg-per-1000-l):
correcting a 10× arithmetic slip surfaced a much larger problem — the *price*
underneath the corrected figure was never sourced by anyone. The document was
internally consistent after the fix and still resting on an invented number.

> **Consistency is not correctness.** Internal checks find slips. They cannot
> find a missing citation. Ask "who measured this?" separately, every time.

### 6. Rerun — with the unknown closed

Then the loop starts over, one assumption stronger than last time.

---

## Filing a ledger entry

When something gets falsified, add an entry to
[`legacy/README.md`](../legacy/README.md). Next free `L-` number, and these
fields:

```markdown
## L-0NN — Short name of the claim

- **Status:** falsified | superseded | unverified
- **Claim:** quote it as written, don't paraphrase
- **Lived in:** file and section
- **What ran:** the test — or "nothing," if that's the truth
- **Result:** what came back
- **Search for unknowns:** what the failure exposed
- **Edited claim:** what the live docs say now
- **Still unknown:** what would close it properly
- **Rerun instructions:** how the next person tests it
```

Three statuses, and the difference matters:

- **`falsified`** — tested against reality, failed. L-001, L-002, L-004.
- **`superseded`** — replaced by something better, or put out of scope by a
  decision. Not disproven. L-003, L-005. Say which of the two it was; "the goal
  changed" and "the world disagreed" are not the same event.
- **`unverified`** — never tested, demoted from assertion to assumption. L-006,
  L-007. **This is the most useful status in the ledger**, because it is the
  one that marks a number you are currently trusting for no reason.

If a whole file is superseded, `git mv` it into `legacy/` and put the entry
banner at the top. If only a section is, extract that section into a legacy
file. Either way it stays readable — legacy is an archive, not a graveyard.

If a legacy claim later turns out to have been right, **add a new entry saying
so** and promote it back. The ledger only ever grows. Never edit a past entry
to look smarter than it was.

---

## For AI assistants working in this repo

You are unusually good at step 2 and unusually likely to skip steps 4 and 5.

- **Check before you assert.** If a doc says a file exists, `ls` it. Several
  ledger entries exist because generated documentation described intent as if
  it were fact — including a commit message that listed files the commit did
  not contain.
- **Re-derive numbers from their stated premises** before repeating them. Two
  of the entries here are arithmetic that nobody re-checked downstream.
- **Never silently correct.** File the ledger entry. A quiet fix destroys the
  record, and the record is the asset.
- **Distinguish "unsourced" from "wrong."** Prefer marking a number
  `unverified` over deleting it or inventing a citation for it.
- **Preserve the tone.** This project is deliberately profane, funny, and
  unpolished. Rigor and polish are different things — do not sand it down in
  the name of accuracy.

---

## Why this is in a plastics repo at all

Because the alternative is a document that gets more confident as it gets more
wrong. Numbers propagate. A yield figure becomes a revenue figure becomes a
business plan becomes someone spending $2,000 on band heaters. The only thing
standing between an early units error and that outcome is somebody, later,
doing the multiplication and writing down what they found.

**Keep the receipts. Especially for the runs that failed.**
