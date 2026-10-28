# DrumPanel

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Stage P3](https://img.shields.io/badge/stage-P3%20design%20outputs-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827) [![REUSE compliant](https://github.com/BoujeeEnjinia1701/drumpanel/actions/workflows/reuse.yml/badge.svg)](https://github.com/BoujeeEnjinia1701/drumpanel/actions/workflows/reuse.yml) [![Archived in Software Heritage](https://archive.softwareheritage.org/badge/origin/https://github.com/BoujeeEnjinia1701/drumpanel/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/BoujeeEnjinia1701/drumpanel) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23128830.svg)](https://doi.org/10.5281/zenodo.23128830)

**Area:** Circular materials · **TRL:** 3 of 9 (proof of concept on paper) · **Value-engineering target:** USD 3,000; parts USD 3,566 · **Difficulty:** 3 of 5

Turns empty oil drums into flat sheet by purging and cold-opening them instead of burning them.

![DrumPanel: hand-powered bench set that opens oil drums into flat sheet without fire](media/render-hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement DMP-DWG-001 (PDF)](cad/drawings/DMP-DWG-001.pdf) · [STEM check DMP-STM-001](docs/01b-stem-check.md) · [Concept options DMP-OPT-001](docs/02a-concept-options.md) · [User requirements](docs/03a-user-requirements.md) · [Product requirements](docs/03-requirements.md) · [Traceability](docs/03b-traceability.md) · [Sizing note DMP-CAL-001](docs/04-calcs/01-sizing.md) · [Prototype build plan](docs/05-build-plan.md) · [Decisions](docs/06-design-decisions.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Used 55 gallon (about 208 L) steel drums are a cheap source of sheet metal for artisans; accounts from Haiti speak of three sheets per drum. DrumPanel gets three flat panels about 233 x 1,800 mm and two head discs about 552 mm across from each drum. Today the common method is to fill the drum with dried leaves and set it on fire to clear paint and residue, then chisel off the ends, split the side and flatten it. DrumPanel keeps the craft and changes the first steps: purge the drum, check it for vapour, cut it cold and roll it flat with hand-cranked tools on a bench.

The design is manual on purpose. The preliminary IP screen found powered drum cutter-flatteners on the market; DrumPanel assumes workshops with little money and no dependable power. A bench set built from commodity steel and bearings, published openly with a written purge and vapour check, can be made by a local fabricator for an estimated USD 3,566 (value-engineering target USD 3,000, so USD 566 over it) and shared across a workshop cluster.

## Burning platform

In Croix-des-Bouquets, Haiti, the centre of Haitian metal sculpture since Georges Liautaud began the form in the 1950s, drum lids are cut open with a chisel and hammer, the side is split, and the interior is filled with dried sugarcane or grass and set on fire to remove grime before the drum is flattened ([SFO Museum](https://www.sfomuseum.org/exhibitions/haitian-metal-sculpture)). Other accounts describe stuffing drums with banana leaves to burn off paint and residue, and cutting with only hammers and chisels ([Singing Rooster](https://singingrooster.org/about-haitian-art/)). Artists then flatten the body by climbing inside and using their weight to open it up ([Roots of Development](https://store.rootsofdevelopment.org/wp-content/uploads/2023/12/About-Haitian-Metal-Art.pdf)).

This first stage is where newcomers begin: new artists usually start by burning out whole 55 gallon drums, cutting them down and pounding the surfaces flat ([Global Exchange](https://globalexchange.org/tag/haiti-oil-drum-art/)). The work is loud enough that a support group tried supplying ear plugs ([Singing Rooster](https://singingrooster.org/about-haitian-art/)). The raw material is plentiful, a byproduct of shipping through the harbour in Port-au-Prince ([Haiti Hub](https://haitihub.com/the-story-of-haitian-metal-art/)), so better tools for this stage would reach many workshops.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Artisan metalwork and crafts | Opening and flattening drums into sheet for sculpture, wall art and homewares |
| Informal fabrication | Sheet for stoves, boxes, roofing patches and small tanks in workshops without sheet stock |
| Drum reconditioning and recycling | Cold, manual opening of drums that cannot be reused whole |
| Vocational training | A documented, safer drum preparation method for apprentices |
| Fair trade and export buyers | A cleaner, repeatable supply chain for drum-based products |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| Haiti, Croix-des-Bouquets | Noailles in Croix-des-Bouquets has long been the centre of Haitian metal art, though gang violence has recently forced artists to relocate ([SFO Museum](https://www.sfomuseum.org/exhibitions/haitian-metal-sculpture)). |
| Haiti, Port-au-Prince | Drums come to artisans as a byproduct of shipping through the harbour, and each 55 gallon drum yields three sheets ([Haiti Hub](https://haitihub.com/the-story-of-haitian-metal-art/)). |
| United States | Fair trade stores sell Haitian oil drum art, giving artisans who export under fair labour conditions a route out of poverty ([Global Exchange](https://globalexchange.org/tag/haiti-oil-drum-art/)). |
| Europe and North America | Croix-des-Bouquets sculpture made with hacksaws, hammers and chisels is shown in galleries, museums and private collections ([Nader Haitian Art](https://www.naderhaitianart.com/blogs/news/a-deep-dive-into-metal-sculptures-from-croix-des-bouquets)). |

## What sparked the idea

Haiti Hub's account of Haitian metal art says it plainly: each drum is first burned to remove all paint and residue, then cut vertically down both sides and flattened into panels ([Haiti Hub](https://haitihub.com/the-story-of-haitian-metal-art/)). Every sheet in the craft starts with a fire and a chisel. DrumPanel asks whether that first step can be done cold, on a bench, with hand tools a local fabricator can make.

## Problem

Metal artisans who turn used oil drums into sheet usually burn each drum out first and then cut and flatten it by hand with chisels and body weight. The work is loud and relies on open fire, and there is no simple, documented bench method to open drums cold.

Full problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

The current design, option A, is a hand-powered bench set in three stations that two people run with no electricity. A drum is accepted only if its label shows a non-volatile oil; it is filled with water and detergent on a sloping drain stand, drained, and passes a pumped LEL reading below 5 % at both bungs before anything touches it. On the cutting cradle a hand-cranked end cutter takes both heads out as flat 552 mm discs, a lever punch notches the chimes and hoops, and a rotary shear head on an overhead rail slits the body and then, swivelled with a ring head bolted on, cuts off the chime rings and hoop strips two at a time. The three curled panels go through a slip roll whose bending roll is set by a dial, and come out flat, about 233 x 1,800 mm. Every crank and lever force is 136 N or less; two people turn about 2.20 drums an hour into panels (DMP-CAL-001).

Full design precis: [docs/02-concept.md](docs/02-concept.md) · Requirements: [docs/03-requirements.md](docs/03-requirements.md)

![Concept overview: drain stand, cutting cradle and slip roll](media/hero.png)

## STEM check

Thirty-six claims are checked (DMP-STM-001): twenty-eight for the bench set and eight first-order screens for option B. Nothing fails. An independent reviewer refuted one claim and weakened others; five details that failed were fixed in the design under Amish's standing instruction: the first panel of every drum is now checked for flatness and the dial trimmed (a reading found once per batch does not hold), a second drain stand keeps the purge ahead of the cutting, the gas detector's LEL channel is calibrated for heavy vapour, the guard slots are toleranced 7 to 8 mm, and fire-resistant hydraulic fluids are refused at the door. Five bench set rows stay plausible on screening values that the TRL 4 trial measures, among them the hardest crank and lever forces (136 N and 131 N against 150 N).

## Concept options

![Two ways to open a drum cold, side by side at one scale](media/options.png)

Option A, the bench set of rotary shears and a slip roll (score 186 of 230), is recommended over option B, a deep-throat lever shear with a stretch leveller (165), which is cheaper but slower, harder to guard and wastes the gripped panel ends. Both are modelled to the same level of detail; the choice is proposed, awaiting Amish (DMP-OPT-001, DMP-DDR-005).

## Key components

- Drain and purge stand, drain tray and purge kit
- Vapour check kit (pumped gas detector)
- Cutting cradle: frame, rollers under the hoops, drum brake
- Rail posts, rail beam, trolley and a swivelling rotary shear head
- End cutter for the heads
- Slip roll: geared pinch rolls, bending roll, 3:1 chain crank, guards and tables
- Bench plate, deburring tools and pictogram procedure sheets

## Building the prototype

The prototype build plan ([docs/05-build-plan.md](docs/05-build-plan.md)) shows how to make each of the 24 groups of parts and put them together, with a making sketch for every made part, close-ups of the joints and a picture for every assembly step, all drawn from the detailed model (818 parts with every bolt, weld and bearing). Almost everything is sawn, drilled and stick-welded from square tube and plate; the rolls are turned on a lathe; the slitting discs, cutter wheel, notching punches and dies, bearings, gears and gas detector are bought or made by a tool shop. It is a plan, not yet built: building and testing it is TRL 4 work.

![Every component, pulled apart and numbered in build order](docs/05-build-plan/overview.png)

## Safety

> Empty drums can still hold flammable vapour. Never cut, grind, weld or heat a drum until the purge is done and the vapour check passes below 5 % LEL.
>
> Do not process drums that held fuel, solvent, chemicals or unknown contents, or that have no readable label.
>
> A drum full of water weighs about 240 kg: fill and drain it on the stand, never lift it.
>
> Cut steel edges are sharp; wear cut-resistant gloves and eye protection, and deburr sheets before handling.
>
> Crank-driven rolls and cutters have pinch points; keep guards fitted and one person on the crank.
>
> This design is published as an open engineering reference. It is not certified equipment. It is a TRL 3 concept, not for fabrication until built and tested at TRL 4.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry: both concept options at detail level D3 |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (DMP-PRC-001 for the precis), a version and a revision history. Run `python .kit/render.py --check` to validate them, `python .kit/cad_check.py --export` for the CAD fidelity check, `python docs/04-calcs/sizing.py` for the calculations and `python docs/04-calcs/stem_check.py` for the STEM check. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `DMP-PRC-001/v1.0`.

## Credits

Designed by Amish Chadha at Design Molecule Labs. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for roles. To cite this design, use [CITATION.cff](CITATION.cff) (GitHub shows it as "Cite this repository").

AI assistance (Claude) was used to accelerate prototype documentation and first-pass research. Design direction and all decisions are Amish Chadha's, recorded in this repository's decision records (`docs/decisions/`).

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab.
