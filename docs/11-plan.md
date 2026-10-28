---
doc_id: DMP-PLN-001
title: DrumPanel project plan
project: DrumPanel
doc_type: Project plan
version: "0.1"
status: Draft
date: 2026-10-24
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: First project plan (kit 1.8 and 1.9.1 upgrade of a TRL 3 repo); stage P3 reached; workstreams, gates, decision requests and references
---

# DrumPanel project plan

DrumPanel reached TRL 3 on 2026-10-03 and stage P3 (design outputs) on 2026-10-24 with the kit 1.9.1 upgrade: pipeline documents, two concept options both modelled to D3, and the chosen design's model detailed part by part. The next gate, P4 (verification, TRL 4), is on hold while the portfolio cap is P3. Two decisions are requested from Amish: the concept carried forward (option A recommended) and the flash point limit for accepting drums (keep 60 °C recommended). Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| STEM check | Design lead | DMP-STM-001 | Pass (2026-10-24); independent review recorded; five fixes made under the standing instruction (F1 to F5) |
| Concept options | Amish Chadha | DMP-OPT-001, DMP-DDR-005 | Option A recommended; proposed, awaiting Amish |
| Requirements | Design lead | DMP-URS-001, DMP-PRS-001, DMP-RTM-001 | Done on paper; partner review to do |
| Calculations | Design lead | DMP-CAL-001 | Done (v0.3) |
| Detailed CAD | Design lead | `cad/src/model.py`, both options at D3, STEP, drawings | Done (`cad/fidelity.json`) |
| Build plan and BOM | Design lead | DMP-BLD-001, `bom/bom.csv` | Done (plan, not yet built) |
| Regulatory, risk, market | Design lead | DMP-REG-001, DMP-RSK-001, DMP-MKT-001 | First pass done; country rules to assess with a partner |
| Photoreal renders and options picture | Portfolio coordinator | `media/options.png`, `media/render-*.png` from the D3 models | Queued (rendered on Amish's Mac) |
| Co-design partner | Amish Chadha | A cooperative of drum artists and a vocational welding school | Not started (candidates in DMP-PRB-001) |
| Verification (TRL 4) | Design lead with a partner | Test plan and trials: vapour check procedure, slip roll trial pass, scrap-chime punch test, timed half-day trial | On hold (stage cap P3) |

## Resources needed

Table 2. Resources.

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Design lead (Claude with Amish's review) | P0 to P3 documents, model, drawings, build plan | Done | 0 |
| Prototype parts (TRL 4, on hold) | One bench set | A town fabricator, about two weeks (estimate) | 3,566 (BOM) |
| Gas detector training and calibration gas (TRL 4) | A person trained for each session | One day with the supplier (estimate) | Included in BOM line 4 |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB with users and stakeholders, STM, OPT, REG, FEA, PLN | Done 2026-10-24 (the design itself dates from 2026-10-03) |
| P1 Definition | URS, PRS draft, RSK, MKT, REG complete | Done 2026-10-24 |
| P2 Design inputs | PRS targets, CAL, RTM, DDR, STEM check closed, FEA closed | Done 2026-10-24 |
| P3 Design outputs | Model at D3 for both options, STEP, DWG, priced BOM, BLD, DEC, design FMEA, RTM | Done 2026-10-24 |
| P4 to P6 | Tests, field trials, launch | On hold |

## Next steps and decisions requested

- Amish: decide the concept carried forward (DMP-DEC-001, open decision 1; option A recommended) and the drum acceptance flash point (open decision 2; keep 60 °C with the vapour check recommended).
- Portfolio coordinator: render `media/options.png` and the photoreal views from the D3 models, then the storefront cards.
- When the portfolio cap allows TRL 4: approach the first co-design candidate, build to DMP-BLD-001 and run the first checks, starting with the vapour check procedure and the slip roll trial pass.

## References

American Welding Society. *F4.1:2017 Safe Practices for the Preparation of Containers and Piping for Welding, Cutting, and Allied Processes.* Accessed October 25, 2026. https://pubs.aws.org/p/1759/f412017-safe-practices-for-the-preparation-of-containers-and-piping-for-welding-cutting-and-allied-processes.

Global Exchange. "Haiti Oil Drum Art." https://globalexchange.org/tag/haiti-oil-drum-art/.

Global Industrial. "Wizard WIZ-Kid Manual Drum Opener 13073, Non-Ferrous Cutting Wheel." Accessed October 25, 2026. https://www.globalindustrial.com/p/wizard-174-wiz-kid-174-manual-drum-opener-13073-non-ferrous-cutting-wheel.

Grizzly Industrial. "T21318 36 in Slip Roll, 22-Gauge." Accessed October 25, 2026. https://www.grizzly.com/products/t21318.

Haiti Hub. "The Story of Haitian Metal Art." https://haitihub.com/the-story-of-haitian-metal-art/.

Instrumart. "Honeywell BW MicroClip X3 Gas Detector." Accessed October 25, 2026. https://www.instrumart.com/products/42331.

International Organization for Standardization. ISO 13857:2019, *Safety of Machinery: Safety Distances to Prevent Hazard Zones Being Reached by Upper and Lower Limbs.* Accessed October 25, 2026. https://www.iso.org/standard/69569.html.

Legal Information Institute. 29 CFR 1910.252, Welding, Cutting and Brazing. Accessed October 25, 2026. https://www.law.cornell.edu/cfr/text/29/1910.252.

Legal Information Institute. 29 CFR 1915.14, Hot Work. Accessed October 25, 2026. https://www.law.cornell.edu/cfr/text/29/1915.14.

Legal Information Institute. 29 CFR 1926.352, Fire Prevention. Accessed October 25, 2026. https://www.law.cornell.edu/cfr/text/29/1926.352.

Roots of Development. "About Haitian Metal Art." https://store.rootsofdevelopment.org/wp-content/uploads/2023/12/About-Haitian-Metal-Art.pdf.

SFO Museum. "Haitian Metal Sculpture." https://www.sfomuseum.org/exhibitions/haitian-metal-sculpture.

Singing Rooster. "About Haitian Art." https://singingrooster.org/about-haitian-art/.

Transcat. "Enerpac SCR-106H 10 Ton Hydraulic Cylinder and Hand Pump Set." Accessed October 25, 2026. https://transcat.com/enerpac-scr106h-hydraulic-cylinder-and-hand-pump-set.

Trick-Tools. "Beverly B-1 Throatless Shear, 14 Gauge Capacity." Accessed October 25, 2026. https://www.trick-tools.com/Beverly_B_1_Throatless_Shear_14_gauge_capacity_B_1_1116.

United States Patent US3161952A, drum head cutter (expired), as cited in DMP-PRC-001.

Workplace Health and Safety Queensland. "Flammable and Combustible Liquids." Accessed October 25, 2026. https://worksafe.qld.gov.au/safety-and-prevention/hazards/hazardous-chemicals/specific-hazardous-chemicals/flammable-and-combustible-liquids.
