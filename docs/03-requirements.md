---
doc_id: DMP-PRS-001
title: DrumPanel product requirements and specifications
project: DrumPanel
doc_type: Product requirements and specifications
version: "0.6"
status: Draft
date: '2026-10-24'
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
- version: "0.5"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Round-2 decision 5A (DMP-DDR-004): R7 kept at 2.5 drums an hour; the TRL 4 timed trial decides; no design change"
- version: "0.6"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Kit 1.8 upgrade: requirements migrated from DMP-REQ-001 to product requirements PR-001 to PR-012 (old R number in Was) with tolerance, units, the user requirement each traces to (DMP-URS-001) and the TRL of verification; PR-013 to PR-016 added from the constraints of DMP-PRB-001 (drum acceptance, purge water, hand power only, pictogram procedure); no target changed. STEM fixes F1 to F5 of 2026-10-24 (DMP-DEC-001): per-drum flatness check (PR-005), second drain stand (PR-007 now 2.20), LEL channel calibration (PR-002), slot tolerance (PR-010), two-person head lifts (PR-011), fire-resistant hydraulic fluids refused (PR-013); cost USD 3,566 (PR-009)"
---

# DrumPanel product requirements and specifications

What the bench set must do, each requirement traced to a user need in DMP-URS-001 (links in DMP-RTM-001). The requirements describe option A, the current design (DMP-OPT-001; the concept choice is proposed, awaiting Amish). On paper the constructable design meets 14 of the 16 requirements, misses one and is over the value-engineering target of another: PR-007 (throughput) is **not met**, about 2.20 drums an hour against 2.5, and PR-009 (cost) is over the USD 3,000 target by USD 566. PR-001 to PR-012 are the requirements R1 to R12 of DMP-REQ-001 v0.5 with the same targets, verification and status; PR-013 to PR-016 write down four constraints of DMP-PRB-001 as requirements. On 2026-10-03 Amish chose option A on every requirement decision put to him ("1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A"; DMP-DDR-003) and kept R7 at 2.5 drums an hour in round 2 ("i agree with all the 46 recommendations you provided. please proceed."; DMP-DDR-004). Every figure is from DMP-CAL-001 v0.3 (`docs/04-calcs/sizing.py`); the tag in brackets is the line of its output. Targets remain proposals for review with a co-design partner. Method: STANDARDS section 22.

Table 1. Product requirements and specifications. Status from DMP-CAL-001 v0.3 (2026-10-24).

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Safety | No open flame | No step from drum to flat sheet shall use flame or heat; no grinder or torch touches a drum | 0 | none | heat or flame steps | Inspection of the procedure and build plan, TRL 3; observed trial, TRL 4 | Met by design: purge, check, cut and roll are all cold | R1 |
| PR-002 | UR-002 | Safety | Vapour check before cutting | The vapour check shall flag any drum with flammable vapour at or above 10 % of the lower explosive limit (LEL), at both bungs, before any cut, with the detector's LEL channel calibrated on pentane or set with the maker's correction factor for heavy hydrocarbon vapour | 10 | alarm set at 5 | % LEL | Bump test of the bought detector with 50 % LEL gas, TRL 4; bench test with a calibrated gas, TRL 4 | Met by design: bought pumped LEL detector, alarm at 5 % LEL, half the target (DMP-DDR-001, D2) | R2 |
| PR-003 | UR-003 | Performance | Remove ends cold | One person shall take both heads off a 208 L drum in under 10 minutes | 10 | max | min | Analysis (CAL section 8), TRL 3; timed trials on a batch of drums, TRL 4 | Met on paper: about 3.9 min [H7]; crank force 12 to 27 N [C10 to C15] | R3 |
| PR-004 | UR-004 | Performance | Open the side | The slit shall run straight along the full body length | 5 | max deviation | mm | Inspection of the model (rail straight within 1 mm), TRL 3; measure trial drums, TRL 4 | Met by design: the shear head runs on a rail | R4 |
| PR-005 | UR-005 | Performance | Flat sheet | Panels shall be flat within 10 mm over 1 m after rolling and hand-setting the ends | 10 | max over 1 m | mm | Analysis (CAL section 5), TRL 3; straightedge and feeler check, TRL 4 | Met on paper, with a trial pass for each batch and a straightedge check of the first panel of every drum (fix F1): the bending roll needs 0.29 mm setting accuracy [E13], 11.8 divisions of the 0.025 mm dial [E14d], and 0.02 mm of wall or 5 MPa of yield uses that up, so the dial is trimmed drum by drum and a panel out of tolerance is passed again; panel ends set by hand [E15, E16] | R5 |
| PR-006 | UR-006 | Usability | Manageable effort | Every crank and lever force in normal use shall be at or below 150 N at the handle | 150 | max | N | Analysis (CAL sections 3 to 5, 9), TRL 3; spring scale on each handle, TRL 4 | Met on paper: end cutter 27 N, shear head 68 N (slit) and 136 N (two ring cuts) at 1.5 mm, notching punch 131 N, slip roll 20 N [C15, D15, D15r, K3, E23] | R6 |
| PR-007 | UR-007 | Performance | Throughput | A two-person team shall turn at least 2.5 drums an hour into flat sheet (restated by Amish on 2026-10-03, was 4) | 2.5 | min | drums/h | Analysis (CAL section 8), TRL 3; timed half-day workshop trial, TRL 4 | **Not met** on paper: about 2.20 drums an hour [H5, H13], 54.6 hands-on minutes a drum against 48.0 [H4, H9], with two drain stands so the purge keeps up [H12]; kept at 2.5 by Amish (DMP-DDR-004); the TRL 4 trial decides | R7 |
| PR-008 | UR-008 | Physical architecture | Local build | Every part shall be made by welding, drilling and turning in a town with a welder and a lathe, or bought as a commodity part | All parts | pass or fail | n/a | Inspection of the drawings, BOM and build plan, TRL 3; build by a partner fabricator, TRL 4 | Met by design: the rolls need a lathe with 1.1 m between centres; discs, cutter wheel, bearings, gears and chain are bought | R8 |
| PR-009 | UR-009 | Cost | Value engineering | Bench set parts shall cost at or below the USD 3,000 value-engineering target (a hypothetical control target, not a spending limit) | 3,000 | max | USD | Priced BOM (`bom/bom.csv`), TRL 3 | Over the target: estimated USD 3,566, USD 566 over [J1 to J3] | R9 |
| PR-010 | UR-010 | Safety | Guarding | No finger shall reach a roll nip, disc nip, gear or chain in normal use; guard slots shall be made 7 to 8 mm wide; guards shall need a tool to remove | ISO 13857 Table 4 | slots 7 to 8 mm | n/a | Analysis (CAL section 7), TRL 3; guards as built checked by a competent person, TRL 4 | Met on paper: every slot 8 mm or less and 45 mm or more from its nip [G1 to G3]; chains in closed cases | R10 |
| PR-011 | UR-011 | Safety | Handling | No lift over 25 kg by one person; the shear head and ring head are lifted to the rail by two people; a drum full of water shall never be lifted | 25 | max one person | kg | Model masses (CAL section 10), TRL 3; weigh parts, TRL 4 | Met with a two-person rule: heaviest piece the 33.7 kg cradle frame [I4]; shear head 23.7 kg, ring head 20.4 kg, punch 18.7 kg [I5, I7, I9]; a full drum (about 240 kg) is filled and drained in place [B2] | R11 |
| PR-012 | UR-012 | Performance | Yield | Each drum shall give three flat panels of about 233 x 1,800 mm and two head discs about 550 mm across | 233 x 1,800; 550 | ±5; ±5 | mm | Analysis (CAL section 1), TRL 3; measure trial output, TRL 4 | Met by design: panels 233, 234 and 233 x 1,800 mm; heads 552 mm [A1 to A3] | R12 |
| PR-013 | UR-015 | Safety | Drum acceptance | Only drums whose label shows a non-volatile oil (lubricating, mineral hydraulic or vegetable oil, flash point above 60 °C) shall be accepted; fire-resistant hydraulic fluids (phosphate esters, water glycols, polyalkylene glycols), which do not separate from water, and all others are returned | 60 | min flash point | °C | Inspection of the acceptance procedure sheet, TRL 3; observed intake, TRL 4 | Met by design: acceptance is step 1 of the procedure and the first pictogram sheet (BOM line 22) | new |
| PR-014 | UR-013 | Environment and durability | Purge water | Residue and purge water shall drain into a tray, settle in a spare drum and be reused; skimmed oil shall go to a closed container for a recycler | 0 | none to ground | L | Inspection of the purge kit and procedure, TRL 3; observed purge, TRL 4 | Met by design: drain tray, settling drum with tap and hose kit (BOM lines 2 and 3) | new |
| PR-015 | UR-006 | Usability | Hand power only | Every station shall be worked by hand cranks, levers and screws; no electricity, fuel or compressed air | 0 | none | powered drives | Inspection of the model and BOM, TRL 3 | Met by design | new |
| PR-016 | UR-014 | Usability | Pictogram procedure | Acceptance, purge, vapour check, cutting, rolling and finishing shall each have a laminated pictogram sheet | 6 | min | sheets | Inspection, TRL 3; review with apprentices in their language, TRL 4 | Met by design: BOM line 22; content drafted from DMP-BLD-001 | new |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, environment and durability, cost. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Requirement restated on 2026-10-03

R7 (now PR-007) was "at least 4 drums to flat sheet per hour for a two-person team". Amish restated it to 2.5 drums an hour when he chose option 5A on 2026-10-03 ("1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A"): add a lever notching punch and a second shear head so two ring cuts are made per pass, and restate R7 to 2.5 drums an hour. The record is DMP-DDR-003.

In round 2 Amish kept R7 at 2.5 drums an hour (5A of DMP-DDR-004): "i agree with all the 46 recommendations you provided. please proceed." The paper estimate (2.26 drums an hour then, 2.20 since the STEM fixes of 2026-10-24) was not changed by that decision, and PR-007 is not claimed as met. The gap is about 12 % of the hands-on time, inside the uncertainty of the task-time estimates, so the TRL 4 timed half-day trial decides, and no design change is made at TRL 3.

## Assumptions

- Most drums reaching artisans held oils or similar contents that a water purge can clear enough to cut cold. Drums that did not are rejected at the door (PR-013).
- Artists accept painted panels, with paint removal as a separate cold step (DMP-DDR-001, D4).
- Drum body steel has a yield strength of 200 to 300 MPa and a wall of 0.8 to 1.2 mm; heads are 1.0 to 1.5 mm.
- The rolling hoops are cut out as two strips, so the slip roll never has to straighten them (DMP-DDR-002, P7).
- A pumped LEL detector, bump-tested each day, is good enough for a pass or fail check before cold cutting.
- The 150 N force limit of PR-006 is a conservative screen for a two-hand crank in a standing posture; an EN 1005-3 assessment belongs to TRL 4.

## Safety

> **Safety:** PR-001, PR-002, PR-010, PR-011 and PR-013 are safety requirements. They are not traded against cost or throughput: where a cheaper or faster option would weaken them, the conservative option was taken (DMP-DEC-001). The bench set is an open engineering reference, never certified equipment.
