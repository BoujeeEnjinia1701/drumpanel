---
doc_id: DMP-PRB-001
title: DrumPanel problem statement
project: DrumPanel
doc_type: Problem statement
version: "0.3"
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
  change: TRL 2 update; drum facts, constraints and acceptance rule for drum contents added; first co-design candidate named
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 3 update; budget worded as a value-engineering target; open questions answered by the decisions of 2026-10-03 (DMP-DDR-001, DMP-DDR-002)
---

# DrumPanel problem statement

The first step in drum-based metal art, opening a drum into flat sheet, is still done by fire, chisel and body weight.

## The problem

Accounts from Croix-des-Bouquets describe the same sequence: ends removed with chisel and hammer, the drum filled with dried leaves or cane and set on fire, the side split, and the body flattened by people climbing inside and pounding it down ([SFO Museum](https://www.sfomuseum.org/exhibitions/haitian-metal-sculpture); [Roots of Development](https://store.rootsofdevelopment.org/wp-content/uploads/2023/12/About-Haitian-Metal-Art.pdf)). It is apprentices who usually do this stage ([Global Exchange](https://globalexchange.org/tag/haiti-oil-drum-art/)). The fire is there to remove paint and residue; DrumPanel treats the smoke from burning unknown residues, and the noise of chisel work, as the things to design out.

In the preliminary IP screen the closest alternatives were powered drum cutter-flatteners and an expired US patent for a drum-head cutter (US3161952A). The screen found no simple, open, hand-powered bench set that combines a purge, a vapour check, cold cutting of the ends and seam, and rolling flat. The gap is a documented manual method that a workshop can build and trust.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Metal artists and their apprentices | Flat, clean sheet from drums with less smoke, noise and effort | Small family workshops such as those in Croix-des-Bouquets |
| Local fabricators | Drawings for a bench set they can build from commodity steel | Towns with a welder and a lathe but no sheet metal machinery |
| Artisan cooperatives and fair trade buyers | A safer, repeatable preparation step they can fund and document | Export supply chains |
| Drum collectors and recyclers | A way to open drums that cannot be reused whole without burning them | Port and industrial areas |

## Operating environment

- Open-sided workshops or yards, hot and humid, often with no reliable mains power.
- Drums of 55 US gallon (about 208 L) steel, previously holding oils or unknown contents. A tight-head drum is about 572 mm inside diameter and 880 mm long over its rolled end seams (chimes), with two rolling hoops pressed out of the body and two screw bungs (50 mm and 20 mm) in one head. The body wall is usually 0.8 to 1.2 mm and the heads 1.0 to 1.5 mm.
- Workers standing at a bench; dust, rain and salt air near the coast.
- Water from a tap, a tank or a hose is available most days; electricity is not assumed.

## Constraints

- Value-engineering target: USD 3,000 in parts for the full bench set (a hypothetical control target that keeps the design lean, not a spending limit).
- Manual operation only: hand cranks, levers and clamps, no motors.
- No flame, no grinding and no power tools on a drum until it has been purged and has passed the vapour check.
- Only drums whose label shows they held a non-volatile oil (lubricating, hydraulic or vegetable oil, flash point above 60 °C) are accepted. Drums that held fuel, solvent, chemicals or anything unknown, or that have no readable label, are rejected and returned to the supplier.
- Buildable by a local fabricator from commodity steel, bearings and fasteners; hardware under CERN-OHL-S-2.0.
- Purge and vapour check must be simple enough to follow from a printed pictogram sheet.
- Published as an open engineering reference, not as certified equipment.

## Out of scope

- Cleaning drums for reuse as containers.
- Drums that held toxic, corrosive or unknown hazardous contents; these are not processed.
- Paint stripping and surface finishing beyond what the purge step removes (to be a separate question).
- Artistic cutting and embossing tools.

## Prior work

| Prior work | What it does | Gap for these users | Source |
| --- | --- | --- | --- |
| Croix-des-Bouquets burn and chisel method | Chisel off lids, split the side, burn out with dried cane or grass, flatten | Uses open fire and hand chisels | [link](https://www.sfomuseum.org/exhibitions/haitian-metal-sculpture) |
| Banana-leaf burn-out with hammer and chisel | Drum stuffed with banana leaves and burned, then sliced and stretched to a 3 by 6 ft sheet using only hammers and chisels | Same fire step; no purge or vapour check | [link](https://singingrooster.org/about-haitian-art/) |
| Body-weight flattening | Artists climb inside the split drum and use their weight to open it, then pound and sand it flat | Tiring and uneven; no rolling or clamping tool | [link](https://store.rootsofdevelopment.org/wp-content/uploads/2023/12/About-Haitian-Metal-Art.pdf) |

## Co-design

An artisan cooperative or community arts organisation working with drum-based metal artists, paired with a vocational training centre or local fabricator, to test the bench set in a working studio and shape the procedure around how apprentices actually work.

The first candidate to approach is a fair trade organisation that already works with Haitian metal artists, such as Singing Rooster, to reach a cooperative of Croix-des-Bouquets artists wherever they now work; a vocational welding school is the second candidate, for the build. Neither has been approached and nothing is agreed (DMP-DDR-001, D11).

Co-design checklist, to complete with the partner before any trial:

- [ ] Partner and studio agreed, with a named contact.
- [ ] Drum supply described: where drums come from, what they held, how they are labelled.
- [ ] Water supply and disposal route for purge water agreed.
- [ ] Pictogram procedure sheets reviewed with apprentices in their language.
- [ ] Panel sizes (about 233 x 1,800 mm) and head discs accepted by the artists.
- [ ] A person trained in the gas detector named for each session.

## Open questions, answered on 2026-10-03

Each question below was answered by a decision made under Amish's pre-approval of 2026-10-03; the decision records give the reasons.

| Question | Answer | Record |
| --- | --- | --- |
| Burning does two jobs today, clearing residue and stripping paint. What replaces the paint stripping step without fire? | The panels leave the bench set painted. Paint removal is a separate cold step (scraper and wire brush, or a non-flammable stripper outdoors) outside this design; the bench set never heats the steel. | DMP-DDR-001, D4 |
| Which purge method (water fill, air flush or steam) suits workshops with little water or power? | Water fill with a little detergent, soak 10 minutes, drain through the bottom bung; the water settles in a spare drum and is reused. Air flush needs a blower and steam needs fuel, so neither is used. | DMP-DDR-001, D1 |
| What wall thickness range of drum steel must the cutter and rolls handle? | Body 0.8 to 1.5 mm and heads 1.0 to 1.5 mm; forces are sized at 1.5 mm and the slip roll setting is worked out for 0.8 to 1.2 mm. | DMP-DDR-001, D8; DMP-CAL-001 |
| Would a shared bench set per cooperative work better than one per workshop? | One bench set shared by a cooperative or a cluster of workshops. | DMP-DDR-001, D9 |
| Which artisan cooperative would host the first trials, given the security situation in Croix-des-Bouquets? | First candidate to approach: Haitian metal artists reached through a fair trade partner, wherever they now work; nothing agreed. | DMP-DDR-001, D11 |

## Safety

> **Safety:** An empty drum that held oil can still hold flammable vapour, and cutting, grinding or heating it can make it explode. DrumPanel removes the fire from the process, but the vapour hazard stays until each drum is purged and checked. Drums that held fuel, solvent, chemicals or unknown contents are never processed. Cut drum steel has sharp edges, and the hand-cranked tools have in-running nips; the design answers these with guards, gloves and the safety stops in DMP-BLD-001. DrumPanel is published as an open engineering reference, never as certified equipment.
