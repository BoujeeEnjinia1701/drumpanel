# Review note: DrumPanel

## Session 2026-09-30: scaffolded

### What was done

- Repository created from kit 1.6.0 at TRL 1, target TRL 2.
- `docs/01-problem.md` (DMP-PRB-001 v0.1): problem with cited evidence, users, environment, constraints, prior work, open questions.
- `docs/02-concept.md` (DMP-PRC-001 v0.1): how it works, components, patent design-arounds, shared blocks, safety.
- `docs/03-requirements.md` (DMP-REQ-001 v0.1): 9 proposed requirements.
- `README.md` with concept rationale, burning platform, where it could be used, and what sparked the idea.

### Next

- Run `/populate` to bring the repo to a strong TRL 2 with concept media.

## Session 2026-10-03: TRL 2 (populate), kit 1.7.0

Run as the first half of `/to-trl3` under Amish's pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`, `CLAUDE.md`); `.kit/PHASE.yaml` as installed.
- `docs/01-problem.md` (DMP-PRB-001 v0.2): drum facts, the acceptance rule for drum contents, the first co-design candidate and a co-design checklist.
- `docs/03-requirements.md` (DMP-REQ-001 v0.2): targets firmed up; R10 guarding, R11 handling and R12 yield added.
- `docs/02-concept.md` (DMP-PRC-001 v0.2): how it works in three stations, key design choices, first-order numbers, safety.
- Concept media from the model (`cad/src/concept_media.py`): `media/hero.png`, `media/concept-blueprint.png` and `.pdf`, `media/model.glb` and `media/viewer.html`, `media/cutaway.png`, `media/exploded.png`, `media/flow.png` (material flow per drum, estimates).
- `bom/bom.csv` with every line priced.

### Results

- The five open questions of DMP-PRB-001 answered (purge by water, paint left on, steel range, shared set, first partner candidate).

### Requirements not met at TRL 2

- None found at concept level; R7 throughput was flagged for checking at TRL 3.

### Decisions made under the pre-approval (DMP-DDR-001)

- D1 water purge; D2 pumped LEL detector, pass below 5 % LEL; D3 accept only drums labelled for non-volatile oils; D4 panels left painted; D5 end cutter on the chime; D6 one rotary shear head; D7 slip roll; D8 steel range; D9 shared bench set; D10 standard crank and chain; D11 first co-design candidate to approach (not agreed); D12 slit beside the welded seam.

### Safety concerns

- Flammable vapour in "empty" drums is the main hazard; handled by the acceptance rule, the purge and a conservative 5 % LEL pass level (D2, D3).

## Session 2026-10-03: TRL 3 (advance, design for construction, build plan)

### What was done

- `cad/src/model.py`: parametric build123d model of the whole bench set, 42 components; `python cad/src/model.py --check` passes (no overlaps, 49 contacts, shear head clear in all six ring cut positions and at seven slit stations). STEP: `cad/step/drumpanel-bench-set.step`, `drain-stand.step`, `cutting-cradle.step`, `slip-roll-stand.step`, `rotary-shear-head.step`, `end-cutter.step`, `upper-pinch-roll.step`; STL of the shear head and end cutter.
- `docs/04-calcs/01-sizing.md` (DMP-CAL-001 v0.1) and `docs/04-calcs/sizing.py` (writes `results.csv`).
- `cad/drawings/DMP-DWG-001` general arrangement, Rev P1 (`cad/src/sheets.py`).
- `bom/bom.csv`: 24 lines, all priced.
- Design made constructable: `docs/decisions/0002-design-for-construction.md` (DMP-DDR-002); `design_state: constructable`.
- Build plan pictures (`cad/src/build_plan_media.py`): overview, 19 making sketches `cad/drawings/DMP-DWG-101` to `119`, 12 joint close-ups, 17 assembly steps.
- `docs/05-build-plan.md` (DMP-BLD-001 v0.1) and `docs/06-design-decisions.md` (DMP-DEC-001 v0.1).
- Precis DMP-PRC-001 v0.3, requirements DMP-REQ-001 v0.3, problem DMP-PRB-001 v0.3, README (hero render, build section, links), `project.yaml` at TRL 3.
- Appearance model `cad/src/product_model.py` (hero, exploded, detail); scenes exported to `/home/claude/renders/drumpanel` for the photoreal render on Amish's Mac.

### Key results (DMP-CAL-001)

- Output per drum: three panels 233, 234 and 233 x 1,800 mm and two head discs 552 mm.
- Crank forces: end cutter 27 N, shear head 111 N at 1.5 mm wall, slip roll 20 N (limit 150 N).
- Slip roll bending roll setting 13.4 mm nominal, 9.3 to 19.3 mm over likely steel; must be within 0.29 mm for R5.
- Throughput about 2.0 drums an hour for two people.
- Masses: cradle 130 kg, slip roll stand 189 kg, drain stand 15 kg; heaviest lift the 34 kg cradle frame.
- Value-engineering target: USD 3,000. Estimated cost of the constructable design: USD 2,794 (USD 206 under the target).

### Requirements not met

- **R7 not met:** about 2.0 drums an hour against 4. The hacksaw notches and six ring cuts make the cradle the bottleneck. Not redesigned beyond TRL 3; ideas are in the register's value engineering section.
- **R5 at risk:** flatness depends on setting the bending roll by a trial pass for each batch; the last 90 mm of each panel end is set by hand.

### Decisions made under the pre-approval

- DMP-DDR-002, changes P1 to P14 (see build plan findings below). All recorded in DMP-DEC-001 under Decisions made, dated 2026-10-03, decided by Amish with his pre-approval quote. Open decisions: none. Seven items to confirm when parts are bought.

### Build plan findings: design changes made for construction

- P1 fixed drain stand sloping 2.9 degrees; a full drum (240 kg) is never tipped.
- P2 rollers under the rolling hoops and a screw brake.
- P3 end cutter takes the head out inside the chime; the chime ring comes off with the shear head.
- P4 rotary shear head on a trolley and overhead rail; driven upper disc, idle lower disc, web in the cut.
- P5 hacksaw notches through the chime rings and hoops on the slit line.
- P6 slip roll (geared pinch pair, bending roll) instead of a three-roll pyramid, which cannot drive the sheet.
- P7 hoop strips cut out (rolling a hoop flat would stretch it 8.5 %); the body gives three panels, not one sheet.
- P8 head swivels 90 degrees for the six ring cuts.
- P9 guards with 8 mm slots, disc guard skirt, chain and gear guards, cutter cover.
- P10 panel ends set by hand on a bench plate.
- P11 side frames bolted to the base so the lower roll can be fitted.
- P12 rail posts moved out to 712.5 mm.
- P13 end cutter torque arm against a post.
- P14 drum height under the rail set by the levelling feet.

### Appearance model deviations (decided under the pre-approval)

- The chain is drawn as links on its straight runs only; a nameplate, a hazard label, painted drums, a floor and a 1.75 m mannequin are added for the look. The detail view shows a second state (drum with heads off, head halfway along the slit) that is not in `model.py`'s assembled state; its geometry is taken from `model.py`.

### Safety concerns

- Vapour: cut only after a purge and a check below 5 % LEL, with a bump-tested detector; only drums labelled for non-volatile oils. A log of 50 drums reviewed by a competent person could support relaxing the pass level to 10 % LEL.
- In-running nips at the discs, end cutter and rolls: all guarded on paper (ISO 13857 slots); a competent person must check the guards as built.
- Sharp cut edges: cut-resistant gloves and deburring before handling.
- Handling: a full drum is never lifted; two people for the 34 kg cradle frame.
- Oily purge water: settled and skimmed, never poured out.

### Recommended next step

- Photoreal renders on Amish's Mac from `/home/claude/renders/drumpanel` (`media/render-hero.png` is referenced by the README), then `python .kit/cards.py .`.
- When the portfolio phase allows TRL 4: approach the first co-design candidate and build to DMP-BLD-001, starting with the vapour check procedure and the slip roll trial pass.

## 2026-10-03: photoreal renders

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.
