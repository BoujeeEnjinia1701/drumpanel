---
doc_id: DMP-FEA-001
title: DrumPanel feasibility assessment
project: DrumPanel
doc_type: Feasibility
version: "0.1"
status: Draft
date: 2026-10-24
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: First feasibility assessment (kit 1.8 upgrade of a TRL 3 repo), closed for TRL 3 from DMP-STM-001, DMP-CAL-001, the D3 model and the build plan
---

# DrumPanel feasibility assessment

Feasible on paper and closed for TRL 3: every station is sawn, drilled and stick-welded from square tube and plate, with three rolls turned on a lathe and a handful of bought precision parts, and every crank and lever force is within 150 N. Two things are not settled by paper: throughput (about 2.20 drums an hour against the 2.5 of PR-007) and the screening coefficients behind the hardest forces (the chime notch, the disc traction), which the TRL 4 trial measures. Cost is USD 3,566 against the USD 3,000 value-engineering target. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | The purge, vapour check, end cutter, notching punch, rotary shear head with ring head and slip roll each meet their force and fit checks on paper; the D3 model of 818 parts has no interference; the shear head clears the drum in slit and ring modes | High | Two ring cuts need 136 N against 150 N; the chime notch force (24.3 kN) and the disc traction (1.17) rest on screening values (DMP-STM-001 S6, S7, S13) | DMP-CAL-001 sections 3 to 9; DMP-STM-001; `cad/fidelity.json` |
| Materials | S275 tube and plate, C45 rolls, D2 discs and punches hardened by a tool shop, bronze bushes, hardwood chocks, plywood tables | High | Drum steel varies by batch (yield 200 to 300 MPa, wall 0.8 to 1.2 mm), which is why the bending roll is set by a trial pass for each batch and the first panel of every drum is checked (STEM fix F1) | DMP-CAL-001 Table 1 and section 5.3 |
| Manufacturing and assembly | Welding, drilling, tapping and turning; the rolls need a lathe with 1.1 m between centres; 18 assembly steps; the D3 detailing changed only fixings and small sizes (DMP-DDR-006) | Medium | A long lathe may be in the next town; the punch dies and discs come from a tool shop | DMP-BLD-001; DMP-DWG-001 and DMP-DWG-101 to 123 |
| Power | Human powered: about 20 to 136 N at the handles; no electricity, fuel or compressed air | High | Repetitive cranking over a day (DMP-RSK-001 H7) | DMP-CAL-001 sections 3 to 9; PR-015 |
| Controls | None; the bending roll is set by dials, the shear head by an index pin, the drum by a screw brake | High | A wrong dial reading leaves panels out of flat; the trial pass catches it | DMP-CAL-001 section 5.3 |
| Supply of parts | Steel, fasteners, bearings, bushes, sprockets, chains and gears are commodity parts; the gas detector, its bump-test gas and the discs need specialist suppliers | Medium | Calibration gas and detector service may not be available locally (DMP-RSK-001 P4) | BOM lines 4, 10, 16, 21, 25; DMP-MKT-001 |

Ratings: High, Medium, Low.
