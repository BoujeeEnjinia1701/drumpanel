---
doc_id: DMP-DEC-001
title: DrumPanel design decisions register
project: DrumPanel
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened at TRL 3; every decision made under Amish's pre-approval of 2026-10-03
---

# DrumPanel design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All decisions were made under Amish's 2026-10-03 pre-approval.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The slitting discs bought: 101 mm outside, 10 mm thick, 25 mm bore, hardness 58 to 60 HRC | The 1.0 mm overlap, the shaft shoulders and the guard clearance are drawn to these sizes | DMP-DDR-002, P4 |
| 2 | The end cutter wheel bought: 50 mm across, 6 mm thick, and its bore | Sets the cutter arm and the cut line 4 mm inside the chime wall | DMP-DDR-002, P3 |
| 3 | Real drums from the first supplier: chime inside radius, hoop positions and height, wall and head thickness | Hoop cut lines (30 mm each side of each hoop), roller positions and the steel range of the calculations | DMP-CAL-001, Table 1 |
| 4 | The gas detector bought: pumped sampling, a 1 m probe that fits a 20 mm bung, an alarm that can be set at 5 % LEL, and its calibration gas | The vapour check procedure depends on it | DMP-DDR-001, D2 |
| 5 | Pinch gear mesh at 61 to 61.5 mm centres with the module 3 gears bought | The pinch opens as the sheet thickens | DMP-CAL-001, section 5.5 |
| 6 | The bending roll setting for the first batch of drums, found by a trial pass | R5 depends on it; the calculation gives only a range (9.3 to 19.3 mm) | DMP-CAL-001, section 5.3 |
| 7 | The driven disc's grip on a 1.5 mm wall | Traction margin is only 1.17 at 1.5 mm | DMP-CAL-001, section 4 |

## Value engineering

Value-engineering target: USD 3,000 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 2,794 (USD 206 under the target). Main cost drivers and savings worth trying:

- The vapour check kit (USD 600) is the largest line. It is a safety item; a shared detector across a cooperative's workshops spreads its cost, but the bench set never runs without one.
- The three rolls (USD 285) and their turning: buying ground shafting of the right length and turning only the journals could save about USD 60.
- The shear head (USD 265), mostly the two D2 discs: standard slitter knives from a cutting tool supplier are cheaper than custom-ground discs.
- The side frames (USD 150): plasma-cut plate from a local shop is cheaper than sawn and drilled plate.
- Throughput rather than cost limits the design (R7 not met). Ideas worth trying at TRL 4: notch a batch of drums ahead of time, a second shear head so slit and ring cuts can overlap, and pre-set hoop cut stops on the rail.

## Decisions made

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
