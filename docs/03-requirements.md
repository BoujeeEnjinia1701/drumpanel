---
doc_id: DMP-REQ-001
title: DrumPanel requirements
project: DrumPanel
doc_type: Requirements
version: "0.4"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2; targets firmed up; R10 guarding, R11 handling and R12 yield added; concept status for each requirement
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 3; status of every requirement from DMP-CAL-001 on the constructable design (DMP-DDR-002); R9 worded against the value-engineering target; R12 changed to three panels per drum
- version: "0.4"
  date: '2026-10-03'
  author: Amish Chadha
  change: 'R7 restated to 2.5 drums an hour by Amish on 2026-10-03 (decision 5A, DMP-DDR-003); status of R5, R6, R7, R9 and R11 from DMP-CAL-001 v0.2 after the notching punch, ring head and dial adjuster'
---

# DrumPanel requirements

On paper, the constructable design meets ten of the twelve requirements, misses one, and is over the value-engineering target of R9. On 2026-10-03 Amish chose option A on every requirement decision put to him ("1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A"); for DrumPanel that added a lever notching punch and a ring head and restated R7 from 4 to 2.5 drums an hour (5A), and added a fine-pitch dial adjuster to the bending roll (8A) (DMP-DDR-003). R7 is still not met: the estimate is about 2.26 drums an hour, up from 2.0. R5 is now met on paper with a trial pass for each batch of drum steel: the dial sets the bending roll to 0.025 mm against a 0.29 mm allowance. Every figure is from DMP-CAL-001 v0.2 (`docs/04-calcs/sizing.py`); the tag in brackets is the line of its output.

*Table 1. Requirements and their status at TRL 3.*

| ID | Requirement | Target | Verification (TRL 4) | Status at TRL 3 |
| --- | --- | --- | --- | --- |
| R1 | No open flame in the process | Zero heat or flame steps from drum to flat sheet | Procedure review and observed trial | Met by design: purge, check, cut and roll are all cold; no grinder or torch touches a drum |
| R2 | Vapour check before cutting | Check reliably flags a drum with flammable vapour at or above 10 % of the lower explosive limit (LEL) | Bump test of the bought detector with 50 % LEL gas; bench test with a calibrated gas | Met by design: a bought pumped LEL detector with its alarm set at 5 % LEL, half the target (DMP-DDR-001, D2) |
| R3 | Remove ends cold | Both heads off a 208 L drum in under 10 minutes by one person | Timed trials on a batch of drums | Met on paper: about 3.9 min [H7]; crank force 12 to 27 N [C10 to C15] |
| R4 | Open the side | Straight slit along the full body length, edge deviation at or below 5 mm | Measure the cut line on trial drums | Met by design: the shear head runs on a rail straight within 1 mm |
| R5 | Flat sheet | Panels flat within 10 mm over 1 m after rolling | Straightedge and feeler check | Met on paper, with a trial pass for each batch: needs the bending roll within 0.29 mm of the right height [E13], which is 11.8 divisions of the new 0.025 mm dial [E14d], held by a lock nut; a fixed setting can leave 188 mm of sag on other steel [E12], so the reading is found by a trial pass on the first drum of each batch; the last 90 mm of each panel end is set by hand [E15, E16] |
| R6 | Manageable effort | Crank force at or below 150 N at the handle | Spring scale on the handle during trials | Met on paper: end cutter 27 N, shear head 68 N for the slit and 136 N for two ring cuts at 1.5 mm wall, notching punch lever 131 N, slip roll 20 N [C15, D15, D15r, K3, E23] |
| R7 | Throughput | At least 2.5 drums to flat sheet per hour for a two-person team (restated 2026-10-03, was 4) | Timed half-day workshop trial | Not met: about 2.26 drums an hour [H5], 53.1 hands-on minutes a drum against 48.0 [H4, H9] |
| R8 | Local build | All parts made or bought in a town with a welder and a lathe | Build by a partner fabricator from the drawings | Met by design: welding, drilling and turning only; the rolls need a lathe with 1.1 m between centres; discs, cutter wheel, bearings, gears and chain are bought |
| R9 | Value engineering | Bench set parts cost at or below the USD 3,000 value-engineering target | Costed bill of materials | Over the target: estimated USD 3,489, USD 489 over the value-engineering target [J1 to J3] |
| R10 | Guarding | No finger reaches a roll nip, disc nip, gear or chain in normal use; guards need a tool to remove | ISO 13857 check of the guards as built | Met on paper: every slot 8 mm or less and 45 mm or more from its nip [G1 to G3]; the shear head's chains run inside its closed drive case and the ring head coupling turns inside a guard sleeve |
| R11 | Handling | No lift over 25 kg by one person; a drum full of water is never lifted | Weigh parts; procedure review | Met with a two-person rule: heaviest piece the 34 kg cradle frame [I4]; shear head 23.7 kg, ring head 20.4 kg, notching punch 18.7 kg [I5, I7, I9]; a full drum (about 240 kg) is filled and drained in place [B2] |
| R12 | Yield | Per drum: three flat panels about 233 x 1,800 mm and two head discs about 550 mm across | Measure the output of trial drums | Met by design: panels 233, 234 and 233 x 1,800 mm; heads 552 mm [A1 to A3] |

## Requirement restated on 2026-10-03

R7 was "at least 4 drums to flat sheet per hour for a two-person team". Amish restated it to 2.5 drums an hour when he chose option 5A on 2026-10-03 ("1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A"): add a lever notching punch and a second shear head so two ring cuts are made per pass, and restate R7 to 2.5 drums an hour. The record is DMP-DDR-003.

## Assumptions

- Most drums reaching artisans held oils or similar contents that a water purge can clear enough to cut cold. Drums that did not are rejected at the door (DMP-PRB-001, Constraints).
- Artists accept painted panels, with paint removal as a separate cold step (DMP-DDR-001, D4).
- Drum body steel has a yield strength of 200 to 300 MPa and a wall of 0.8 to 1.2 mm; heads are 1.0 to 1.5 mm.
- The rolling hoops are cut out as two strips, so the slip roll never has to straighten them (DMP-DDR-002, P7).
- A pumped LEL detector, bump-tested each day, is good enough for a pass or fail check before cold cutting.

## Safety

> **Safety:** R1, R2, R10 and R11 are safety requirements. They are not traded against cost or throughput: where a cheaper or faster option would weaken them, the conservative option was taken (DMP-DEC-001). The bench set is an open engineering reference, never certified equipment.
