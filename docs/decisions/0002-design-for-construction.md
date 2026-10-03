---
doc_id: DMP-DDR-002
title: DrumPanel design for construction
project: DrumPanel
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each, decided under Amish's pre-approval of 2026-10-03
---

# 0002: Design for construction

- **Date:** 2026-10-03
- **Status:** accepted. Decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

## Context

STANDARDS section 18 asks for the design to be made constructable as the build plan is drawn (Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible"). The TRL 2 concept listed eight components in words only. Drawing every part in `cad/src/model.py`, checking it with build123d, and sizing it in DMP-CAL-001 found the problems below. Every change keeps what DrumPanel does (purge, check, cold cut and roll flat, by hand) and its pitch. P7 changes the output from one sheet to three panels per drum; it is recorded here because the one-sheet output cannot be made, and the safety case is unchanged.

The model now runs its own checks with `python cad/src/model.py --check`: no two of the 42 components overlap, the 49 joints that must touch do touch, the shear head clears the drum at all six ring cut positions and at seven stations along the slit, and its parked position clears the posts and the drum. All pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | A tilting drain stand: a drum full of water (about 240 kg) would have to be tipped | A fixed stand sloping 2.9 degrees to the bung end; the drum is filled and drained in place, never lifted full | Simpler and safer; drains to within 1.4 L (DMP-CAL-001, section 2) |
| P2 | "Cradle and clamps" did not say what the drum sits on or how it is held | Four rollers under the rolling hoops, 380 mm apart, so the drum turns; a screw brake with a rubber pad holds it still | The hoops are the stiffest part of the body; the drum must both turn (ring cuts) and stay still (slit) |
| P3 | The end cutter was to remove each end; a hand wheel cannot cut through the five-layer chime seam | The end cutter cuts the head out just inside the chime; the chime ring stays on the body and is cut off later with the shear head | The head plate is single thickness; the chime's inside wall acts as the die |
| P4 | A "lever or crank-driven slitting tool" with nothing to guide it or react its force | A rotary shear head on a trolley running on an overhead rail between two posts; the upper disc is driven, the lower idles inside the drum, and a 10 mm web in the cut joins them | A gear between the discs would have to pass through the drum wall; the rail keeps the slit straight (R4) |
| P5 | No way to start a cut through the chime rings and hoops | A 40 mm hacksaw notch through each chime ring and each hoop on the slit line before slitting | The discs cannot shear a folded seam or a 12 mm ridge |
| P6 | A three-roll pyramid cannot drive the sheet by friction alone | A slip roll: pinch pair geared 1:1 and pressed together with 2 kN by two M16 screws, bending roll 90 mm behind on two M20 screws | Traction comes from the pinch, bending from the bending roll; crank 20 N (DMP-CAL-001, section 5) |
| P7 | The concept rolled the whole body flat; rolling a hoop flat would stretch its crown about 8.5 % | The shear head also cuts 30 mm each side of each hoop; the body gives three panels about 233 x 1,800 mm and two hoop strips | Only flat panels go through the rolls; matches the three sheets per drum the craft already expects |
| P8 | Rings and hoops cut with a separate tool | The shear head swivels 90 degrees on its pivot (index pin, two positions) for the six ring cuts while the crank turns the drum on its rollers | One tool, already on the rail |
| P9 | No guards drawn | Disc guard with a front skirt 8 mm over the sheet; slip roll nip guards with 8 mm slots, lid, chain and gear guards; a cover over the end cutter wheel; all need a tool to remove | ISO 13857 slot distances met on paper (DMP-CAL-001, section 7); safety additions take the conservative option |
| P10 | Panel ends that no slip roll can bend | The last 90 mm of each panel end is set by hand on a 10 mm bench plate with a dead-blow mallet | A slip roll cannot bend between its pinch line and its bending roll |
| P11 | Lower roll cannot be fitted between two welded side frames | Side frames bolted to the base; the lower roll's bushes go on first, then the frames; upper and bending rolls drop down open slots closed by bolted top bridges | An assembly order that works |
| P12 | Rail posts too close to the drum ends for the end cutter and the parked head | Posts at 712.5 mm each side of the middle, on bases across two cross members; frame 1,550 mm long | Room for the end cutter, its torque arm and the head's lower jaw |
| P13 | Shear head reaction when cutting heads | A torque arm from the end cutter rests against a rail post | The drum turns; the cutter must not |
| P14 | Drum height under the rail fixed | The cradle's levelling feet set the drum top under the shear head; no height adjustment in the drop bar | Fewer parts; drums vary by a few millimetres |

## Consequences

- Cost: the estimated cost of the constructable design is USD 2,794 against the USD 3,000 value-engineering target (USD 206 under).
- R7 (four drums an hour) is not met: the notches and six ring cuts make the cradle the bottleneck at about 2.0 drums an hour.
- R5 (flatness) depends on finding the bending roll setting by trial for each batch of drum steel.
- The drawings DMP-DWG-001 and DMP-DWG-101 to 119, the concept media and the build plan DMP-BLD-001 are drawn from the changed model.
