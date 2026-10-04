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

## 2026-10-03: Amish's requirement decisions carried out

Amish chose option A on every requirement decision put to him: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A". For DrumPanel these are 5A (R7) and 8A (R5). Record: `docs/decisions/0003-requirement-decisions-2026-10-03.md` (DMP-DDR-003).

### Changes and new results

- **Lever notching punch (5A).** A two-station C-frame punch replaces the four hacksaw notches (`cad/src/model.py`, BOM line 21, sketch DMP-DWG-121, joint 14). The chime notch is widened from 40 to 60 mm so the punch's lower jaw passes through it to reach the hoop. Chime notch 24.3 kN, lever 131 N; hoop slot 6.6 kN, lever 36 N [K1 to K4]; four notches in 4.0 minutes, down from 8.
- **Ring head (5A).** A second shear head bolted to the main head with a spacer plate and a coupling in a guard sleeve makes two ring cuts a pass (BOM line 25, sketch DMP-DWG-122, joint 13). Six ring cuts in three passes, 9.5 minutes, down from about 12.4; 20.4 kg.
- **R7 restated to 2.5 drums an hour (5A).** DMP-REQ-001 v0.4. New result: about 2.26 drums an hour (53.1 hands-on minutes a drum against 48.0 needed). **R7 not met**, up from 2.0.
- **Fine-pitch dial adjuster (8A).** M20 x 1.5 bending screws, 60-division dials (0.025 mm) and lock nuts (BOM line 15, sketch DMP-DWG-116 Rev P2). The 0.29 mm allowance is 11.8 divisions [E14d]. **R5 met on paper** with a trial pass for each batch (was at risk).
- **Raised shear head drive (design for construction, found while carrying out 5A).** The former 200 mm crank on the upper shaft swept through the drum wall (about 13,700 mm³ in the new sweep check), so it could not turn. The crank now sits on a raised crank shaft in a closed 2.33 to 1 #35 chain drive case, 155 mm (BOM line 10, sketch DMP-DWG-120). Slit crank 68 N, two ring cuts 136 N at 1.5 mm wall. **R6 met on paper** (worst 136 N). Slit time 2.7 minutes, up from 2.3.
- **Tool shelf** on the left rail post for the punch and ring head (BOM line 26, sketch DMP-DWG-123).
- **R11:** shear head with drive 23.7 kg, ring head 20.4 kg, punch 18.7 kg; met with the two-person rule for the 33.7 kg cradle frame.
- **Cost (R9):** Value-engineering target: USD 3,000. Estimated cost of the constructable design: USD 3,489 (USD 489 over the target). The decisions added USD 695; every new BOM line carries its price basis.
- **Masses:** cradle station with its tools 196 kg, slip roll stand 191 kg, drain stand 15 kg.

### Files

- Model and checks: `cad/src/model.py`, 52 components; `--check` passes (no overlaps, all contacts, three ring passes with both heads, crank sweeps in both modes, four punch positions). New STEP: `cad/step/notching-punch.step`, `cad/step/shear-head-with-ring-head.step`; STL `cad/stl/notching-punch.stl`; all others regenerated.
- Calculations: `docs/04-calcs/01-sizing.md` (DMP-CAL-001 v0.2, new section 9) and `sizing.py`, `results.csv`.
- Drawings: DMP-DWG-001 Rev P2; DMP-DWG-105, 109, 110, 116 Rev P2; new DMP-DWG-120 to 123.
- Build plan DMP-BLD-001 v0.2: overview, joints 6, 9, 13 and 14, steps 8 to 18 (new step 10; former steps 10 to 17 renumbered 11 to 18), new sections 3.13 to 3.15.
- Concept media: hero, exploded, cutaway, model.glb, concept blueprint (Rev P2). Precis DMP-PRC-001 v0.4; register DMP-DEC-001 v0.2; README cost and build lines.
- Appearance model `cad/src/product_model.py` (drive case, tool shelf, punch, ring head, dials; new group "tools" in the hero and exploded views); scenes exported to `/home/claude/renders/drumpanel`. Photoreal renders not redone: `media/render-hero.png` and the other renders now predate these changes.

### Decisions proposed and awaiting Amish

- **R7 gap (register, open decision 1).** About 2.26 against 2.5 drums an hour. Options: A keep 2.5 and let the TRL 4 timed trial decide; B restate R7 to 2.25; C add more speed-ups now (rail stops for the ring passes, a second deburring station). Recommendation: A, because the gap is about 10 % of hands-on time, inside the uncertainty of the task-time estimates.

### Safety

- New hazards covered in the build plan: the coupling shaft turns in a guard sleeve; both shear head chains are inside the closed drive case; the punch moves only by its screw, hands on the lever (safety stop S10). The chime punch force is the least certain number and is to be confirmed on a scrap chime (register, item 8).

## 2026-10-03: photoreal renders redone after Amish's requirement decisions

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.

## 2026-10-03: Amish's round-2 requirement decisions carried out

Amish, 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed." For DrumPanel this is decision 5A on R7, recorded in `docs/decisions/0004-r7-kept-at-2-5-drums-an-hour.md` (DMP-DDR-004) and in the register `docs/06-design-decisions.md` (DMP-DEC-001 v0.3). A records and wording change only: no geometry, bill of materials, drawing or picture changed.

| Change | Files | New result |
| --- | --- | --- |
| R7 kept at 2.5 drums an hour; the TRL 4 timed trial decides | `docs/03-requirements.md` v0.5, `docs/05-build-plan.md` (Throughput check wording), `docs/06-design-decisions.md` v0.3, DMP-DDR-004 | **R7 not met on paper: about 2.26 drums an hour, 53.1 hands-on minutes a drum against 48.0**; the gap is about 10 % of hands-on time, inside the estimate's uncertainty; the trial decides |
| Open decision 1 closed | register v0.3 | Open decisions: none |
| Cost | unchanged | Value-engineering target: USD 3,000. Estimated cost of the constructable design: USD 3,489 (USD 489 over the target). `budget_usd` unchanged |

Mass unchanged. Pictures changed: none; the appearance model is unchanged and no views were re-exported.

### Decisions proposed, awaiting Amish

None.

### Cross-repo actions

None.

### Safety

The throughput target never justifies skipping a vapour stop: S4 and S5 apply to every drum.

### Recommended next step

TRL 4 (the timed half-day trial, with each task timed, is the test that decides R7) needs a new instruction from Amish.

