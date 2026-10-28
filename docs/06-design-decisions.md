---
doc_id: DMP-DEC-001
title: DrumPanel design decisions register
project: DrumPanel
doc_type: Design decisions register
version: "0.4"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened at TRL 3; every decision made under Amish's pre-approval of 2026-10-03
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: Amish's requirement decisions 5A (R7) and 8A (R5) of 2026-10-03 moved to Decisions made (DMP-DDR-003); new open decision on the remaining R7 gap; value engineering updated
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Open decision 1 (R7 gap) decided, round 2, 5A (DMP-DDR-004); no open decisions"
- version: "0.4"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: STEM fixes F1 to F5 decided under the standing instruction of 2026-10-23; concept selection (DMP-OPT-001, DMP-DDR-005) and the drum acceptance flash point added as open decisions, proposed, awaiting Amish; design for construction at D3 (DMP-DDR-006) recorded as made under STANDARDS section 18"
---

# DrumPanel design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Open decisions, each proposed, awaiting Amish.*

| # | To decide | Options | Recommendation | What it affects in the build | Record |
| --- | --- | --- | --- | --- | --- |
| 1 | Concept carried forward | A: the current bench set, rotary shears and slip roll (186 of 230); B: lever shear and stretch leveller (165 of 230) | A: 11 % ahead; whole heads, full-length panels, guarded nips; already constructable and planned | Nothing if A; with B a new calculation note, drawing, BOM and build plan | DMP-OPT-001, DMP-DDR-005 |
| 2 | Flash point limit for accepting a drum | A: keep "non-volatile oil, flash point above 60 °C" (the upper bound of GHS flammable liquid category 3) with the vapour check on every drum; B: raise it to above 93 °C (GHS unclassified), which turns away the few non-fuel oils with flash points of 60 to 93 °C | A: the vapour check below 5 % LEL is the safeguard, fuels are already rejected by name, and lubricating, hydraulic and vegetable oils have flash points well above 93 °C | Only the acceptance pictogram sheet and PR-013 | DMP-STM-001, S4 |

## STEM fixes made under Amish's standing instruction of 2026-10-23

The independent review of the STEM check (DMP-STM-001) refuted or weakened several rows. Five details failed and were fixed in the design under Amish's standing instruction of 2026-10-23 ("when a STEM check row fails, propose and implement the best fix for the design and its constructability in the same session and record it in DEC as decided under that instruction"). None changes the working principle, the pitch or the scope; Amish can reverse any of them.

*Table 1a. STEM fixes, decided under the standing instruction of 2026-10-23.*

| # | Row failed | Options weighed | Fix made | Cost | Where |
| --- | --- | --- | --- | --- | --- |
| F1 | S10: a bending roll reading found once per batch does not hold from drum to drum (0.02 mm of wall or 5 MPa of yield uses up the 0.29 mm allowance) | A trial pass on every drum; an automatic gauge; a straightedge check of the first panel of every drum with a dial trim and a second pass for any panel out of tolerance | The per-drum straightedge check and trim, with a second pass (turned over if over-bent); 1.5 minutes a drum more | None; throughput 2.26 to 2.20 drums an hour | DMP-CAL-001 sections 5.3 and 8; PR-005; DMP-BLD-001 first checks |
| F2 | S25 (new): one drain stand holds each drum about 35 minutes, so it could purge only about 1.7 drums an hour | A faster fill (second hose); a second drain stand; accepting the lower rate | A second drain stand and tray beside the first; the purge kit is shared | USD 77 (BOM lines 1 and 2, quantity 2) | DMP-CAL-001 section 8 [H10 to H13]; model; BOM |
| F3 | S4: a catalytic LEL sensor calibrated on methane under-reads heavy hydrocarbon vapour, so a true 10 to 15 % LEL could read 5 % | Alarm at a lower reading; pentane calibration or the maker's correction factor; an infrared sensor | The LEL channel calibrated on pentane, or set with the maker's correction factor for heavy hydrocarbons | None expected (to confirm when bought) | BOM line 4; PR-002 |
| F4 | S16: the 8 mm guard slots sit at the boundary of ISO 13857 Table 4; at 8.1 mm the distance needed jumps from 20 to 80 mm | Narrower slots in the model; a tolerance on the slots as made | Slots toleranced 7 to 8 mm as made; drawn at 8 mm | None | PR-010; DMP-CAL-001 section 7; DMP-BLD-001 section 3.21 |
| F5 | S19: fire-resistant hydraulic fluids (phosphate esters, water glycols, polyalkylene glycols) sink in or mix with water, so they do not settle out of the purge water | Treat the water; refuse those drums | Refused at acceptance | None | PR-013; acceptance pictogram sheet |

The review also weakened rows without a failure (S6, S7, S13: screening coefficients; S11: a design rationale; S14: lift limits; S17: not a bound); those rows were reworded, S14 and S17 tightened, and the measurements are listed in Table 2 and in DMP-STM-001.

## To confirm when parts are bought

*Table 2. Items to confirm when parts are bought.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The slitting discs bought: 101 mm outside, 10 mm thick, 25 mm bore, hardness 58 to 60 HRC | The 1.0 mm overlap, the shaft shoulders and the guard clearance are drawn to these sizes | DMP-DDR-002, P4 |
| 2 | The end cutter wheel bought: 50 mm across, 6 mm thick, and its bore | Sets the cutter arm and the cut line 4 mm inside the chime wall | DMP-DDR-002, P3 |
| 3 | Real drums from the first supplier: chime inside radius, hoop positions and height, wall and head thickness | Hoop cut lines (30 mm each side of each hoop), roller positions and the steel range of the calculations | DMP-CAL-001, Table 1 |
| 4 | The gas detector bought: pumped sampling, a 1 m probe that fits a 20 mm bung, an alarm that can be set at 5 % LEL, and its calibration gas | The vapour check procedure depends on it | DMP-DDR-001, D2 |
| 5 | Pinch gear mesh at 61 to 61.5 mm centres with the module 3 gears bought | The pinch opens as the sheet thickens | DMP-CAL-001, section 5.5 |
| 6 | The bending roll setting for the first batch of drums, found by a trial pass | R5 depends on it; the calculation gives only a range (9.3 to 19.3 mm) | DMP-CAL-001, section 5.3 |
| 7 | The driven disc's grip on a 1.5 mm wall | Traction margin is only 1.17 at 1.5 mm | DMP-CAL-001, section 4 |
| 8 | The notching punch on a scrap chime and a scrap hoop: force and a clean cut | The chime notch force (24.3 kN) is the least certain number and sets the lever force (131 N against 150 N); the 35 mm side edges are shorter than the 42.5 mm the raked-edge estimate assumes for a 7.5 mm stack (DMP-STM-001 review) | DMP-CAL-001, section 9 |
| 10 | The edge spreading force round the shear head web on a scrap drum | Half the 1.5 mm feed resistance is this unmeasured estimate; doubled, two ring cuts would need about 208 N and the driven disc would slip (DMP-STM-001 S6, S13) | DMP-CAL-001, section 4 |
| 11 | The end cutter drive wheel's grip on a painted, oily chime | At friction 0.15 the clamp must pinch about 1,040 N, not 520 N | DMP-CAL-001, section 3 |
| 9 | The #35 sprockets bought (12, 28 and two of 15 teeth) bored to 20 and 25 mm, and their chains' centre distances in the drive case | The drive case bores are drawn to these sprockets | DMP-DDR-003, Q3 |

## Value engineering

Value-engineering target: USD 3,000 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 3,566 (USD 566 over the target). Amish's decisions of 2026-10-03 added USD 695 (DMP-DDR-003); the second drain stand and tray of STEM fix F2 (2026-10-24) added USD 77. Main cost drivers and savings worth trying:

- The vapour check kit (USD 600) is the largest line. It is a safety item; a shared detector across a cooperative's workshops spreads its cost, but the bench set never runs without one.
- The shear head (USD 340) and the ring head (USD 255), mostly their four D2 discs: standard slitter knives from a cutting tool supplier are cheaper than custom-ground discs, and four bought together cost less each.
- The notching punch (USD 330), mostly its two ground punch and die sets: punch and die blanks from a press tooling supplier, finished locally, could save about USD 60.
- The three rolls (USD 285) and their turning: buying ground shafting of the right length and turning only the journals could save about USD 60.
- The side frames (USD 150): plasma-cut plate from a local shop is cheaper than sawn and drilled plate.
- Throughput still limits the design more than cost (R7, now PR-007, not met; decided by Amish to leave to the TRL 4 trial, DMP-DDR-004). Ideas worth trying at TRL 4: set stops on the rail for the three ring passes, and notching a batch of drums ahead of time while another is cut.
- From the runner-up concept (DMP-OPT-001, option B): if a batch of drum steel will not come flat in the slip roll at the TRL 4 trial, a simple stretch frame with two wedge grips can finish the worst panels. A suggestion only; not in the design or the BOM.

## Decisions made

*Table 3. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | Purge by water fill with detergent, soak 10 min, drain; water reused through a settling drum | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-DDR-001, D1 |
| 2026-10-03 | Vapour check with a bought pumped LEL detector; pass only below 5 % LEL (conservative; a reviewed log of 50 drums could support 10 %) | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-DDR-001, D2 |
| 2026-10-03 | Accept only drums labelled for non-volatile oils; reject fuel, solvent, chemical, unknown and unlabelled drums (conservative) | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-DDR-001, D3 |
| 2026-10-03 | Panels leave painted; paint removal is a separate cold step outside the design | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-DDR-001, D4 |
| 2026-10-03 | End cutter: wheel cutter on the chime, after expired US3161952A | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-DDR-001, D5 |
| 2026-10-03 | One rotary shear head for the slit and all ring cuts | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-DDR-001, D6 |
| 2026-10-03 | Flatten with a hand slip roll | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-DDR-001, D7 |
| 2026-10-03 | Steel range: body 0.8 to 1.5 mm, heads 1.0 to 1.5 mm | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-DDR-001, D8 |
| 2026-10-03 | One shared bench set per cooperative or cluster | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-DDR-001, D9 |
| 2026-10-03 | Standard 300 mm crank and #40 chain, drawn to accept the proposed hand capstan block later | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-DDR-001, D10 |
| 2026-10-03 | First co-design candidate to approach: Haitian metal artists through a fair trade partner (Singing Rooster first); not agreed | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-DDR-001, D11 |
| 2026-10-03 | Slit 50 mm beside the drum's welded seam | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-DDR-001, D12 |
| 2026-10-03 | Design for construction, changes P1 to P14: fixed sloping drain stand, rollers under the hoops and a screw brake, end cutter on the head only, rail-mounted shear head with a web in the cut, hacksaw notches, slip roll, hoop strips cut out (three panels per drum), swivelling head, guards, hand-set panel ends, bolted side frames, posts moved out, torque arm, height set by the levelling feet | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-DDR-002 |
| 2026-10-03 | Guards: every nip slot 8 mm or less and at least 20 mm from its nip; guards need a tool to remove (conservative) | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-DDR-002, P9 |
| 2026-10-03 | Two-person rule for any lift over 25 kg; a drum full of water is never lifted (conservative) | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-DDR-002, P1 |
| 2026-10-03 | Requirements R10 (guarding), R11 (handling) and R12 (yield) added; R7 reported as not met and R5 as at risk, with no redesign beyond TRL 3 | Amish, pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | DMP-REQ-001 v0.3 |
| 2026-10-03 | R7 throughput (5A): a lever notching punch replaces the four hacksaw notches (chime notch widened to 60 mm), and a ring head bolted to the shear head makes two ring cuts a pass; R7 restated from 4 to 2.5 drums an hour. Result: about 2.26 drums an hour, not met (open decision 1) | Amish: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A" | DMP-DDR-003, Q1 and Q2; DMP-REQ-001 v0.4 |
| 2026-10-03 | R5 flatness (8A): fine-pitch M20 x 1.5 bending screws with 60-division dials (0.025 mm) and lock nuts. Result: the 0.29 mm allowance is 11.8 divisions; R5 met on paper with a trial pass for each batch | Amish: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A" | DMP-DDR-003, Q4 |
| 2026-10-03 | Design for construction while carrying out 5A: the shear head crank moved onto a raised crank shaft in a closed 2.33 to 1 chain drive case (the former crank swept through the drum wall), and a tool shelf on the left rail post | Made under STANDARDS section 18 (Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible") to carry out Amish's 5A: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A" | DMP-DDR-003, Q3 and Q5 |
| 2026-10-03 | 5A (round 2): R7 kept at 2.5 drums an hour (paper estimate 2.26, not met on paper); the TRL 4 timed half-day trial decides; no design change | Amish: "i agree with all the 46 recommendations you provided. please proceed." | DMP-DDR-004 |
| 2026-10-24 | STEM fixes F1 to F5: per-drum flatness check; second drain stand and tray; pentane-calibrated LEL channel; guard slots 7 to 8 mm; fire-resistant hydraulic fluids refused | Decided under Amish's standing instruction of 2026-10-23: "when a STEM check row fails, propose and implement the best fix for the design and its constructability in the same session and record it in DEC as decided under that instruction" | DMP-STM-001; Table 1a |
| 2026-10-24 | Design for construction at detail level D3, Q1 to Q10: pivot pin held by an M8 cross bolt through the drop bar; side frame foot plates 120 x 80 mm with nuts inside the long rails; tool shelf bolt holes 550 and 700 mm from the floor; 42 mm disc guard hole; table legs on levelling screws up to the angle frame; lid clips; keeper plates and flatted screw collars; recessed roller discs; shear head and slip roll bearings, bushes and guard fixings drawn | Made under STANDARDS section 18 (Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible") while carrying out Amish's kit 1.9.1 rollout (2026-10-24: "I want detailed TRL3 CAD"); Amish can reverse any item | DMP-DDR-006 |
