---
doc_id: DMP-DDR-005
title: DrumPanel concept selection
project: DrumPanel
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: Concept selection between option A (the current bench set) and option B (lever shear and stretch leveller) argued from DMP-OPT-001; proposed, awaiting Amish
---

# 0005: Concept selection

- **Date:** 2026-10-24
- **Status:** proposed, awaiting Amish. Nothing in the repo changes until he decides; the drawing, BOM and build plan describe option A, as they did before (STANDARDS section 21, existing designs).

## Context

Kit 1.8 asks every repo for at least two concept options with different working principles, scored against the user requirements before one is carried forward (STANDARDS section 21). DrumPanel was designed before kit 1.8, so its current design, the bench set of rotary shears and a slip roll taken to TRL 3 on 2026-10-03, is option A. Option B, a deep-throat lever shear with straight blades and a stretch leveller, was added with a different principle for both the cutting (straight blades in short strokes instead of rolling discs) and the flattening (stretching past yield instead of reverse bending). Both are modelled to D3 (Amish, 2026-10-24: "Detail every option") and both pass the STEM check (DMP-STM-001).

## Options considered

*Table 1. Options.*

| Option | What it is | Score (of 230) | For | Against |
| --- | --- | --- | --- | --- |
| A | Bench set: end cutter, notching punch, rail-mounted rotary shear head with ring head, slip roll | 186 | Whole head discs and 1,800 mm panels; continuous cranking at 136 N or less; every nip behind 8 mm slots on paper; already constructable, priced and planned | USD 3,566, USD 566 over the value-engineering target; about 2.20 drums an hour against 2.5 (PR-007 not met); a trial pass per batch for flatness |
| B | Deep-throat lever shear on a stand at the cradle end; wedge-grip stretch leveller with a 15 t hand-pumped cylinder | 165 | About USD 2,800 (estimate); plate and welding work; very flat panels without a per-batch setting | About 1.65 drums an hour; about 380 lever strokes a drum; open blades and link at the cut; 86 mm lost from each panel; slotted head discs; a 62 kg shear head |

## Recommendation

Option A, the current design. It scores 11 % above option B, just outside the 10 % band that would send both to Amish without a pick, and it wins on the needs that carry the safety case (guarding) and the product (full-length panels and whole discs). Graft from option B: keep stretch levelling as a fallback for batches of steel that will not come flat in the slip roll at the TRL 4 trial (a suggestion in DMP-DEC-001, not a design change).

## Decision

Proposed, awaiting Amish. `concept_chosen` in `project.yaml` is "A (proposed)" until he decides.

## Consequences

- If Amish chooses A: no change; option B stays in `cad/src/option_b.py` and DMP-OPT-001 as the documented alternative.
- If Amish chooses B: a new calculation note, product requirement statuses, drawing, BOM and build plan for option B; PR-012 would need restating (panels about 1,714 mm) or longer drums.
