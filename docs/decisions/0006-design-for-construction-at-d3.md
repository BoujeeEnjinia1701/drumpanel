---
doc_id: DMP-DDR-006
title: DrumPanel design for construction at detail level D3
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
  change: Details found while modelling every bolt, pin, weld and bearing of option A (kit 1.9.1); made under STANDARDS section 18; no working principle, pitch, scope or safety case changed
---

# 0006: Design for construction at detail level D3

- **Date:** 2026-10-24
- **Status:** made under STANDARDS section 18 (Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible") while carrying out the kit 1.9.1 rollout (Amish, 2026-10-24: "I want detailed TRL3 CAD"; "Kit 1.9.1 rollout - proceed to rollout across the other repos"). Amish can reverse any item. None changes what the bench set does, its pitch, its scope or its safety case; none changes a calculation in DMP-CAL-001 or the cost.

## Context

Kit 1.9 asks for the model of every option at detail level D3: real stock sections, every bolt, nut, washer, pin and screw with its hole, welds as beads, bearings and bushes, checked for interference (STANDARDS section 24). The station model of 2026-10-03 drew each component as one solid with its main holes. Rebuilding option A part by part in `cad/src/option_a.py` (818 parts, `cad/fidelity.json`) found a few joints that could not be assembled or fastened as drawn or written in the build plan, and several fixings the build plan named but the model did not draw.

## Decision

*Table 1. Changes made to the model, the BOM text and the build plan.*

| # | Problem found | Change made | Why this way |
| --- | --- | --- | --- |
| Q1 | The pivot pin was to take an R-clip below the head plate, but that point is inside the welded drop bar, where no clip can be fitted | The pin is lengthened from 55 to 66 mm and, with the drop bar, cross-drilled 9 mm 15 mm above its lower end, 17 mm below the head plate; an M8 bolt through both holds it; the pin turns in the swivel plate and its collar rides on top | The head hangs from the pin, so the pin must be held below the head plate; a cross bolt is reached from outside the drop bar |
| Q2 | Two M12 foot bolts with washers do not fit on an 80 x 80 mm foot plate round a 50 mm leg | Side frame foot plates 120 x 80 mm, extending inward; both M12 bolts inboard of the leg, their nuts inside the long rail, reached through 24 mm access holes in its bottom wall | Keeps the bolted side frames (DMP-DDR-002, P11) on the same base rails; the rails stand on the floor, so the nuts go inside |
| Q3 | The build plan put the tool shelf bolt holes 550 and 700 mm up from the frame top, above the shelf's back plate | Holes 550 and 700 mm up from the floor, inside the back plate (450 to 760 mm); build plan text corrected | The model's shelf position, which the drawing shows, is kept |
| Q4 | The disc guard's 26 mm shaft hole would not pass the 40 mm disc clamp collar and spacer | 42 mm hole through the front and back faces of the guard hood | The clamp and spacer hold the upper disc on its shaft |
| Q5 | Table legs stopped at the lower edge of a box-section frame; real 40 x 40 x 3 mm angles have no lower face there | Legs run up to the underside of the angle frame's top flange and are welded there; each stands on a 50 x 50 x 3 mm cap plate with a welded M10 nut and an M10 levelling screw, as the build plan already said | Gives the weld a face and the levelling screws a nut |
| Q6 | The nip guard lid had no fixing | Four 20 x 20 x 2 mm angle clips, screwed to the side frames with M5 screws and to the lid with M5 bolts | Guards need a tool to remove (PR-010) |
| Q7 | The slide block keeper plates named in the build plan were not drawn; a round captive collar larger than the screw would not pass the 20 mm side plate | Keeper plates of 3 mm sheet with M5 screws on the inside faces; the captive collars on the four screws are flatted to 18 mm | The collars engage the blocks inside the plate thickness |
| Q8 | The cradle roller end discs sat flush with the tube ends, leaving no corner for a fillet weld | Discs set 4 mm into the tube and welded all round | A fillet weld needs a corner |
| Q9 | The shear head bearings were not drawn | Upper housing bored 60 mm for the eccentric bush (3 mm offset) carrying two 6005-2RS bearings; lower housing bored 47 mm for one; drive case plates bored 42 mm for four 6004-2RS bearings; the case closed by three pillar bolts with spacer tubes, its inner plate held by four M8 screws into the upper housing | As in BOM line 10; the case must come apart to fit the chains |
| Q10 | The slip roll crank housing and guards had no fixings | Crank housing a 50 x 6 mm tube with two 25 x 38 x 20 mm bronze bushes; the chain guard held by two M6 screws into the housing end; the gear guard by a tab and two M6 screws into the side frame | Guards need a tool to remove (PR-010) |

## Consequences

- Design dimensions changed: Q1 (pivot pin 66 mm long, was 55 mm), Q2 (foot plates 120 x 80 mm, were 80 x 80 mm), Q4 (guard hole 42 mm, was 26 mm), Q5 (table legs about 37 mm longer, on levelling screws), Q7 (collars flatted). Masses change by well under 1 kg a station; the calculations in DMP-CAL-001 read the station model and are unchanged.
- Cost: unchanged by these items (USD 3,489 before the second drain stand of STEM fix F2, DMP-DEC-001, which brings it to USD 3,566); the extra fasteners and sheet fall inside BOM line 23 (fasteners, paint and welding consumables, USD 120).
- BOM text updated for lines 9, 12, 13, 15, 18 and 19; build plan DMP-BLD-001 v0.4 updated for Q1, Q2, Q3 and Q6; drawings and build plan pictures regenerated from the D3 model.
