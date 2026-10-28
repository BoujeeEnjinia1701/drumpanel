---
doc_id: DMP-RSK-001
title: DrumPanel risk register and hazard analysis
project: DrumPanel
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: 2026-10-24
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: First risk register, preliminary hazard analysis and first-pass design FMEA (kit 1.8 upgrade of a TRL 3 repo, stage P3), for option A, the current bench set
---

# DrumPanel risk register and hazard analysis

The top hazard is an explosion when a drum that still holds flammable vapour is cut; it is controlled by the acceptance rule, the water purge and a pumped LEL reading below 5 % at both bungs on the day of cutting, and it stays the first safety stop of the build plan. The next hazards are fingers in the in-running nips of the discs, rolls and chains (controlled by guards with 8 mm slots that need a tool to remove), cut edges, and a drum full of water (never lifted). The top project risk is that no co-design partner is found, so nothing is built or measured; the highest design FMEA scores are a drum passed by a detector that was not bump-tested and a bending roll set to the wrong dial reading. Method: STANDARDS section 23 and ISO 12100 (as guidance for a non-certified hand tool). Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 (sure to be found) to 5 (unlikely to be found).

> **Safety:** DrumPanel works on used oil drums, which can hold flammable vapour until they are purged and checked, and its hand-cranked tools have in-running nips at the slitting discs, the end cutter, the slip roll and three chain drives. Cut drum steel has sharp edges. A drum full of water weighs about 240 kg. Nothing in this register replaces a hazard review of the built prototype at TRL 4.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | No co-design partner | Candidates named (a fair trade partner of Haitian metal artists, a vocational welding school), none approached; security in Croix-des-Bouquets | URS and PRS stay desk drafts; no TRL 4 | 3 | 5 | Amish | Approach when TRL 4 opens; the design does not depend on one site |
| P2 | Throughput short of PR-007 | Task times are estimates; ring passes and handling dominate | About 2.20 drums an hour against 2.5 | 3 | 3 | Design lead | Timed half-day trial decides (DMP-DDR-004); rail stops and batch notching as ideas (DMP-DEC-001) |
| P3 | Chime notch force higher than estimated | The five-layer chime seam varies; 24.3 kN is a screening estimate | Lever force above 150 N | 3 | 3 | Design lead | Scrap-chime test before the punch dies are hardened (DMP-DEC-001, item 8); a longer ratchet lever as fallback |
| P4 | Detector support not available locally | Calibration gas and service need a specialist supplier | Bump tests skipped; the safety case weakens | 3 | 5 | Partner | One detector shared by a cooperative with a service plan; no cutting without a bump test that day (safety stop) |
| P5 | Drum supply mixed or unlabelled | Drums come from many sources | Many drums rejected; pressure to accept unknown drums | 3 | 4 | Partner | Acceptance rule held without exception (PR-013); record of drums turned away |
| P6 | Cost over the value-engineering target | Detector, discs and punch dies dominate | USD 3,566 against USD 3,000 | 4 | 2 | Amish | A hypothetical target; savings listed in DMP-DEC-001 (shared detector, stock slitter knives, ground shafting) |
| P7 | No lathe with 1.1 m between centres nearby | Rolls are 1,092 mm long | Rolls bought in or made away | 2 | 2 | Partner | Buy ground shafting and turn only the journals (DMP-DEC-001) |

## Preliminary hazard analysis

Table 2. Hazards (residual after the controls in the design).

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Explosion or flash fire in a drum | Residual vapour from a drum that held fuel, solvent or an unknown liquid, or an oil drum not purged; friction at the cut | Burns, blast injury, death | 5 | 3 | Acceptance by label (PR-013; fire-resistant hydraulic fluids refused); water purge; LEL channel calibrated for heavy vapour (fix F3); pumped LEL reading below 5 % at both bungs on the day of cutting (PR-002); no grinder, torch or welder near a drum; the cut stays far below autoignition (DMP-STM-001 S17) | 2 |
| H2 | Fingers drawn into the slip roll nip | Feeding panels by hand | Crushed fingers | 4 | 3 | Nip guards with 8 mm slots 45 mm from the nip (PR-010); guards need a tool to remove; one person on the crank, nobody else at the in-feed | 2 |
| H3 | Fingers at the slitting discs or the end cutter wheel | Steadying the drum or the cut edge while cranking | Cuts, crushing | 4 | 3 | Disc guard with a front skirt 8 mm over the sheet; wheel cover; crank 155 mm and 150 mm from the cut; one person cranks, the other keeps hands on the drum away from the head | 2 |
| H4 | Fingers in a chain drive | Reaching into the drive while cranking | Crushed fingers | 4 | 2 | Shear head chains inside the closed drive case; slip roll chain and gears in guard boxes held by screws (DMP-DDR-006, Q10) | 1 |
| H5 | Cut edges | Handling panels, rings, hoop strips and head discs | Lacerations | 3 | 4 | Cut-resistant gloves EN 388 level C for every task with cut steel (BOM line 24); deburr every edge before stacking | 2 |
| H6 | Back injury | Lifting the 33.7 kg cradle frame, the shear head or ring head, or a drum; tipping a water-filled drum | Back strain | 3 | 3 | Two-person rule over 25 kg, and for lifting either head to the rail (PR-011); a full drum is filled and drained in place, never lifted | 2 |
| H7 | Repetitive strain | Cranking and levering for a working day | Shoulder and wrist strain | 3 | 3 | Forces at or below 150 N (PR-006); two people swap stations; an EN 1005-3 assessment at TRL 4 | 2 |
| H8 | Skin contact with oil residue and detergent | Draining and purging | Dermatitis | 2 | 3 | Nitrile gloves and aprons (BOM line 24); detergent biodegradable | 1 |
| H9 | Purge water or oil on the ground | Spills, overflowing tray, settling drum not emptied | Soil and water pollution | 3 | 3 | 60 L tray under the bung; settling drum with a tap; skimmed oil to a recycler (PR-014); disposal route to agree with the partner (DMP-REG-001 G11) | 2 |
| H10 | Noise | Setting panel ends with a mallet | Hearing damage over years | 2 | 2 | Dead-blow mallet; ear defenders (BOM line 24) | 1 |
| H11 | Drum rolls off the cradle | Side push while slitting | Crushed feet, falling drum | 3 | 2 | Screw brake on for the slit; a side push of 122 N rolls an empty drum, so the brake is always on for the slit (DMP-CAL-001 section 6) | 1 |
| H12 | Ring head or shear head drops while being bolted on | Heavy head held at arm's length | Struck hands or feet | 3 | 2 | Second person steadies it; spacer plate bolts tight before cranking (build plan safety stop S7) | 1 |
| H13 | Welding fume and burns while building the set | Building the frames | Fume, burns, eye injury | 3 | 2 | No drum in the workshop while welding or grinding; ventilation; welding PPE (build plan safety stop S1) | 1 |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Vapour check kit | Flag a drum with vapour before cutting | Reads low | A drum with vapour is passed (H1) | Detector not bump-tested; sensor poisoned; probe not deep enough in the bung; a methane-calibrated catalytic sensor under-reading heavy vapour | 5 | 2 | 4 | 40 | LEL channel calibrated on pentane or corrected for heavy hydrocarbons (STEM fix F3); bump test every day of use, logged; 1 m probe to the bottom of each bung; read both bungs; repeat if a drum stands overnight |
| F2 | Bending roll setting | Leave panels flat within 10 mm over 1 m | Set to the wrong dial reading | Panels bowed; rework | The right reading changes from drum to drum (STEM fix F1); dials slipped; screws not locked | 2 | 3 | 2 | 12 | Check the first panel of every drum with a straightedge and trim the dial; pass a bowed panel again, turned over if over-bent; lock nuts |
| F3 | Slitting discs | Shear the wall cleanly | Chipped or blunt edge | Torn cut, high crank force | Hitting a hoop ridge or chime not notched; wear | 3 | 3 | 2 | 18 | Notch all four points before slitting (build plan); inspect the discs daily; regrind or replace |
| F4 | Driven disc traction | Pull the head along the cut | Slips on a thick drum | Slow slit; operator pushes the trolley | 1.5 mm wall; traction margin 1.17 (DMP-STM-001 S13) | 2 | 3 | 1 | 6 | Push the trolley by hand while cranking; confirm the margin at TRL 4 (DMP-DEC-001 item 7) |
| F5 | Lever notching punch | Cut the chime notch and hoop slot | Punch does not get through the chime | Notch incomplete; lever force rises | Chime thicker or harder than assumed | 3 | 3 | 1 | 9 | Scrap-chime test before hardening (DMP-DEC-001 item 8); longer lever as fallback |
| F6 | Pivot pin and cross bolt (DMP-DDR-006, Q1) | Hang the shear head from the trolley | Cross bolt loosens | Head drops onto the drum (H12) | Vibration of the crank; nut not tight | 4 | 2 | 2 | 16 | Nyloc or double nut; check the bolt with the index pin before each shift |
| F7 | Guards | Keep fingers from nips | Guard left off | Fingers reach a nip (H2 to H4) | Removed for cleaning and not refitted | 4 | 2 | 2 | 16 | Screws need a tool; the crank stays off until the guard is back (safety stop); daily check list |
| F8 | Drain stand chocks | Hold a full drum sloping to the bung | Chock splits | Drum shifts on the stand | Wet timber, coach screw loose | 3 | 2 | 2 | 12 | Hardwood, oiled; screws checked; drum filled and drained in place only |
| F9 | Slip roll pinch gears | Keep the pinch rolls turning together | Teeth jump | Panel skews | Pinch opened beyond 61.5 mm centres | 2 | 2 | 2 | 8 | Set the pinch with a 1 mm sheet strip; gear centres checked when bought (DMP-DEC-001 item 5) |
| F10 | Shear head chains | Drive the upper disc from the raised crank | Chain jumps or breaks | Crank spins free; slit stops | Slack chain; wear | 2 | 2 | 3 | 12 | 3 mm slack at assembly; inspect through the case at each service |
| F11 | Coupling to the ring head | Drive both upper discs together | Dog disengages | Ring head disc idles; one cut of the pair incomplete | Spacer plate bolts loose; 233 or 234 mm slot set wrong | 2 | 2 | 2 | 8 | All four spacer bolts tight before cranking (safety stop S7); both discs seen turning |
| F12 | Drum brake | Hold the drum still for the slit | Pad slips | Drum turns; slit wanders (PR-004) | Worn pad; oil on the drum | 2 | 2 | 2 | 8 | Wipe the pad seat; replace the pad when hard |
