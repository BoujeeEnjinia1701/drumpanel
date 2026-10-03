---
doc_id: DMP-CAL-001
title: DrumPanel sizing calculations
project: DrumPanel
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First issue at TRL 3, on the constructable design of DMP-DDR-002
---

# DrumPanel sizing calculations

On paper the DrumPanel bench set meets ten of its twelve requirements, has one at risk and misses one. Every crank force is at or below 111 N against the 150 N limit of R6, the guards meet ISO 13857 on paper, and the estimated cost is USD 2,794, USD 206 under the USD 3,000 value-engineering target. R7 is not met: two people would turn about 2.0 drums an hour into flat panels, not 4. R5 is at risk: the slip roll can leave a panel flat only when its bending roll is within about 0.29 mm of the right height for that batch of drum steel, so the setting is found by a trial pass on the first panel of each batch, and the last 90 mm at each panel end is set by hand. Rolling the hoops flat would stretch their crowns about 8.5 %, which is why the hoops are cut out and the body becomes three panels about 233 x 1,800 mm. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [D15], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that a purged drum is free of vapour, that the guards are safe as built, or that the frames carry their loads in service. The vapour check, the guard openings and the drain stand must be checked on hardware before any drum is cut. See DMP-PRC-001, Safety.

## Scope and method

The note checks every requirement in DMP-REQ-001 v0.3 against the design in DMP-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `levels()` and `components()`, so the drum, rollers, shear head, slip roll and guards used here are the ones in the STEP files and in drawing DMP-DWG-001. It reads `bom/bom.csv` for the cost and `budget_usd` in `project.yaml` for the target. Run it from the repo root with `python docs/04-calcs/sizing.py`; it also writes `docs/04-calcs/results.csv`. The model's own checks (`python cad/src/model.py --check`) show that no two parts overlap, that every joint face touches, and that the shear head clears the drum in all six ring cut positions and at seven stations along the slit.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Drum | 572 mm inside diameter, 880 mm over the chimes, body 1.0 mm (0.8 to 1.2), heads 1.2 mm (1.0 to 1.5), hoops 298.5 mm outside radius at 147 mm each side of the middle | Common 55 US gallon tight-head drums |
| Steel | Yield 250 MPa (200 to 300), tensile strength 360 MPa, shear strength 0.8 of tensile, modulus 200 GPa, elastic and perfectly plastic in bending | Low-carbon drum sheet; screening values |
| Shearing | Force = shear strength x t² / (2 tan of the nip angle); feed resistance = force x tan of half the nip angle; discs overlap 1.0 mm | Standard rotary shear estimate |
| Edge spreading | Pushing the cut edges round the 10 mm web adds 100 N at 1.2 mm, scaling with the cube of the wall | Estimate, to confirm at TRL 4 |
| Traction | Driven shear disc: effective friction 0.3 (the edge bites); knurled end cutter wheel 0.3; steel pinch rolls on painted steel 0.15 | Screening values |
| Losses | 20 % for the shear head bearings and idle disc; 30 % for the end cutter's rollers; bronze bushes friction 0.10; chain 95 % | Screening values |
| Slip roll | Panels fed three side by side (700 mm); pinch rolls 60 mm, bending roll 90 mm behind the pinch line; pinch force 2 kN set by two M16 screws | Model geometry |
| Work rate | 30 crank turns a minute; times for loading, setting up and handling as listed in section 8 | Estimates for a practised two-person team |
| Purge | Hose at 20 L/min; 50 mm bung, discharge coefficient 0.6 | Screening values |

## 1. What a drum yields

After the two heads, the two chime rings and the two hoop strips are cut out, the body gives three panels and the heads give two discs.

*Table 2. Output per drum.*

| Quantity | Value | Tag |
| --- | --- | --- |
| Panel length (body circumference at mid-wall) | 1,800 mm | [A1] |
| Panel widths, outer, middle, outer | 233, 234 and 233 mm | [A2] |
| Head discs, two | 552 mm across | [A3] |
| Flat area: panels; heads | 1.26 m²; 0.48 m² | [A4, A5] |
| Empty drum; three panels at 1.0 mm | 19.2 kg; 9.9 kg | [A6, A7] |

The rest of the steel comes off as two chime rings and two hoop strips, about 4.8 kg, which artisans can use as strip.

## 2. Drain and purge

A full drum is filled and drained on its stand, never lifted. The stand slopes 2.9 degrees toward the bung end so it drains to within about 1.4 L.

*Table 3. Purge and the drain stand.*

| Quantity | Value | Tag |
| --- | --- | --- |
| Inside volume (brimful) | 221 L | [B1] |
| Drum full of water | 240 kg | [B2] |
| Fill time at 20 L/min | 11.0 min | [B3] |
| Drain time through the 2 in bung | 2.3 min | [B4] |
| Water left below the bung opening | 1.4 L | [B5] |
| Contact on the chocks, from vertical | 31.5 deg | [B6] |
| Normal force on each chock, full drum | 691 N | [B7] |
| Bending stress in a saddle, full drum | 10.4 MPa | [B8] |
| Compressive stress in a leg, full drum | 1.3 MPa | [B9] |

The stresses are small against the 275 MPa yield of S275; the stand is sized by handling and welding, not strength. The purge itself is a procedure, not a calculation: fill, soak 10 minutes with detergent, drain, then check (DMP-DDR-001, D1 and D2). Whether one fill is enough for a given drum is what the vapour check decides; a failed check means a second fill.

## 3. End cutter

The end cutter needs little force: the cut is short-stroke shearing of the head against the chime's inside wall.

*Table 4. End cutter, 50 mm cutter wheel, 40 mm drive wheel, 150 mm crank.*

| Head thickness | Cut force | Feed resistance | Drive torque | Crank force | Tag |
| --- | --- | --- | --- | --- | --- |
| 1.0 mm | 429 N | 70 N | 1.8 N·m | 12 N | [C10] |
| 1.2 mm | 571 N | 100 N | 2.6 N·m | 17 N | [C12] |
| 1.5 mm | 807 N | 156 N | 4.1 N·m | 27 N | [C15] |

The drive wheel and guide roller must pinch the chime with about 520 N for the knurl to drive a 1.5 mm head [C20]; the cutter's clamp screw sets this. One trip round a head is 13.8 crank turns, about half a minute [C21, C22].

## 4. Rotary shear head

The shear head is the hardest crank in the set. At the thickest wall it still needs only 111 N, but its traction margin is smallest there.

*Table 5. Shear head, 101 mm discs, 1.0 mm overlap, 200 mm crank.*

| Wall | Separating force | Nip angle | Feed resistance | Crank force | Traction over resistance | Tag |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8 mm | 482 N | 10.8 deg | 85 N | 26 N | 1.69 | [D8] |
| 1.0 mm | 713 N | 11.4 deg | 139 N | 42 N | 1.54 | [D10] |
| 1.2 mm | 977 N | 12.0 deg | 213 N | 64 N | 1.38 | [D12] |
| 1.5 mm | 1,429 N | 12.8 deg | 365 N | 111 N | 1.17 | [D15] |

Only the upper disc is driven, because a gear between the discs would have to pass through the drum wall. At 1.5 mm the driven disc has 17 % more traction than it needs; if it slips on a thick drum, the operator pushes the trolley along by hand while cranking. The separating force is carried round the frame: the 10 mm web sees 12.1 MPa and a 25 mm shaft 17.7 MPa [D20, D21]. At 30 crank turns a minute the discs cut at 9.5 m/min [D22]. The trolley, drop bar and head weigh 24.6 kg and bend the rail beam 0.13 mm at mid-span [D23, D24].

## 5. Slip roll: reverse bending to flat

### 5.1 Why the hoops are cut out

A rolling hoop stands about 12 mm out from the body wall. Bent to the reverse curvature the slip roll needs, its crown would be stretched about 8.5 % [E29], far past what the sheet can take without tearing or buckling. So the hoop strips are cut out with the shear head (DMP-DDR-002, P7) and only flat panels go through the rolls.

### 5.2 The setting that leaves a panel flat

A panel leaves the drum curled to a 286.5 mm radius [E1]. To come out flat, it must be bent the other way past the elastic limit by just the right amount, so that it springs back to flat. For an elastic and perfectly plastic sheet the change of curvature x (in units of the elastic limit curvature) must satisfy x - M(x) / M_e = drum curvature / elastic limit curvature, where M / M_e = 1.5 (1 - 1 / (3 x²)). The script solves this for each steel and wall, then finds the bending roll height that bends the panel to that radius between the pinch line and the bending roll 90 mm behind it.

*Table 6. Settings and forces for the three panels fed together (700 mm).*

| Yield | Wall | Reverse radius | Bending roll above lower roll | Moment | Bending roll force | Feed resistance | Tag |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 200 MPa | 0.8 mm | 278 mm | 13.4 mm | 21.5 N·m | 239 N | 71 N | [E200-8] |
| 200 MPa | 1.0 mm | 345 mm | 11.0 mm | 33.9 N·m | 376 N | 112 N | [E200-10] |
| 200 MPa | 1.2 mm | 411 mm | 9.3 mm | 49.1 N·m | 545 N | 163 N | [E200-12] |
| 250 MPa | 0.8 mm | 225 mm | 16.4 mm | 26.6 N·m | 295 N | 87 N | [E250-8] |
| 250 MPa | 1.0 mm | 278 mm | 13.4 mm | 41.9 N·m | 466 N | 138 N | [E250-10] |
| 250 MPa | 1.2 mm | 331 mm | 11.4 mm | 60.8 N·m | 676 N | 201 N | [E250-12] |
| 300 MPa | 0.8 mm | 189 mm | 19.3 mm | 31.6 N·m | 351 N | 103 N | [E300-8] |
| 300 MPa | 1.0 mm | 234 mm | 15.8 mm | 49.9 N·m | 554 N | 164 N | [E300-10] |
| 300 MPa | 1.2 mm | 278 mm | 13.4 mm | 72.5 N·m | 805 N | 239 N | [E300-12] |

The nominal setting is 13.4 mm [E10]; the range over likely drum steel is 9.3 to 19.3 mm [E11], well inside the 60 mm of slot travel.

### 5.3 Why the setting is found by a trial pass (R5 at risk)

The setting is sensitive. If the nominal setting were used on steel at the edges of the range, a panel could sag up to 188 mm over 1 m [E12]. To stay within the 10 mm over 1 m of R5, the bending roll must be within 0.29 mm of the right height [E13], about 42 degrees of a turn of the M20 bending screws [E14]. That is achievable with marked handwheels and the same setting at both ends, but only by trial: the first panel of each batch of drums is passed, checked with a straightedge, and the screws adjusted by a twelfth of a turn at a time until it comes out flat; a panel that is not flat can be passed again. R5 is therefore at risk until a TRL 4 trial shows how many passes a batch takes.

### 5.4 Panel ends

The slip roll cannot bend the leading 90 mm of a panel (from the pinch line to the bending roll) [E15]; left alone, that end would stand 14.1 mm above flat [E16]. The ends are set flat by hand with a dead-blow mallet over the edge of the bench plate. This is quieter and far shorter work than the hammering it replaces.

### 5.5 Drive, rolls and bushes

*Table 7. Slip roll drive and parts, worst case (300 MPa, 1.2 mm).*

| Quantity | Value | Tag |
| --- | --- | --- |
| Bending roll force | 805 N | [E17] |
| Feed resistance | 239 N | [E18] |
| Pinch force needed (friction 0.15, margin 1.5) | 1,193 N | [E19] |
| Pinch force set by the two M16 screws | 2,000 N | [E20] |
| M16 screw torque for 1 kN; force on the 90 mm handwheel rim | 3.2 N·m; 71 N | [E21] |
| Torque to turn the pinch rolls | 16.8 N·m | [E22] |
| Crank force at 300 mm through the 3:1 chain | 20 N | [E23] |
| Feed speed at 30 crank turns a minute | 1.9 m/min | [E24] |
| Upper pinch roll load; mid-span deflection | 2,805 N; 0.25 mm | [E25] |
| Upper pinch roll bending stress | 15.5 MPa | [E26] |
| Bronze bush pressure | 2.3 MPa | [E27] |
| Pinch gear tooth stress (Lewis) | 15 MPa | [E28] |

Every part runs far below its limits; the rolls are 60 mm because they must stay straight to a fraction of the 0.29 mm setting tolerance, not for strength.

## 6. Cutting cradle

The drum sits on its hoops at 33 degrees from vertical each side [F2], with its axis 603 mm and its top 890 mm from the floor [F1], a comfortable height for the crank work. With 1 kN on the drum (the drum plus a person leaning on it) a roller shaft sees 72 MPa and bends 3.2 mm at mid-span [F3]; under the drum alone it bends about 0.6 mm. A sideways push of 122 N rolls an empty drum over a roller [F4], so the drum brake is used whenever the drum must stay still.

## 7. Guards (ISO 13857, slot openings)

ISO 13857 Table 4 allows a slot opening of up to 8 mm when the danger point is at least 20 mm behind it.

*Table 8. Guard openings.*

| Opening | Slot | Distance to the nip | Needed | Result | Tag |
| --- | --- | --- | --- | --- | --- |
| Slip roll in-feed slot under the nip guard | 8.0 mm | 45 mm | 20 mm | Meets | [G1] |
| Slip roll out-feed slot | 8.0 mm | 85 mm | 20 mm | Meets | [G2] |
| Shear head front skirt over the sheet | 7.5 mm | 52 mm | 20 mm | Meets | [G3] |

The chain, sprockets and pinch gears are fully enclosed. The end cutter's wheel works inside the head recess under a sheet cover. These are desk checks on the model; a competent person checks the guards as built before any trial.

## 8. Throughput

Two people turn about 2.0 drums an hour into flat panels [H5], half the 4 of R7. The cutting cradle is the bottleneck.

*Table 9. Hands-on minutes per drum.*

| Station | Minutes | Tag |
| --- | --- | --- |
| Purge and vapour check | 14 | [H1] |
| Cutting cradle: load, two heads, four notches, slit, six ring cuts, unload | 30.1 | [H2] |
| Slip roll and finishing: trial setting, three passes, handling, panel ends, deburring | 17.1 | [H3] |
| Total | 61.2 | [H4] |

The purge takes about 22.9 minutes elapsed but runs while the cradle works [H6]. Taking both heads off is about 3.9 minutes [H7]. The four hacksaw notches (8 minutes) and the six ring cuts (about 12 minutes) are most of the cradle time; ways to win time back, such as a second shear head or notching drums in a batch ahead of time, are listed in the design decisions register (DMP-DEC-001, Value engineering). Even at 2.0 drums an hour, a two-person team turns a drum into panels in about 30 minutes, against the hours of fire and chisel work the method replaces.

## 9. Masses

*Table 10. Masses (steel at 7,850 kg/m³; chocks, tray, bushes and plywood at their own densities).*

| Item | Mass | Tag |
| --- | --- | --- |
| Drain and purge stand with tray | 15 kg | [I1] |
| Cutting cradle with posts, beam, shear head and end cutter | 130 kg | [I2] |
| Slip roll stand with tables | 189 kg | [I3] |
| Heaviest lift: cradle frame, one welded piece | 33.7 kg | [I4] |
| Lower pinch roll | 21.0 kg | [I5] |
| Shear head with shafts, discs, guard and drop bar | 20.0 kg | [I6] |
| Side frame with legs and bridge, each | 19.6 kg | [I7] |

Only the cradle frame is over the 25 kg one-person limit of R11; it is lifted by two people.

## 10. Cost

Value-engineering target: USD 3,000. Estimated cost of the constructable design: USD 2,794 (USD 206 under the target) [J1 to J3]. The largest lines are the vapour check kit (USD 600), the three rolls (USD 285), the shear head (USD 265) and the two side frames (USD 150) [J4 to J7].

## 11. Results against the requirements

*Table 11. Requirement status at TRL 3.*

| ID | Requirement | Result | Status |
| --- | --- | --- | --- |
| R1 | No open flame | All steps cold | Met by design |
| R2 | Vapour check flags 10 % LEL | Detector alarm at 5 % LEL | Met by design |
| R3 | Both heads off in under 10 min | 3.9 min [H7] | Met on paper |
| R4 | Straight slit, 5 mm | Rail-guided head | Met by design |
| R5 | Flat within 10 mm over 1 m | Needs 0.29 mm setting accuracy [E13]; ends hand-set [E16] | **At risk** |
| R6 | Crank force at or below 150 N | 111 N worst [D15] | Met on paper |
| R7 | 4 drums an hour, two people | 2.0 drums an hour [H5] | **Not met** |
| R8 | Local build | Welding, drilling, turning; bought discs and bearings | Met by design |
| R9 | Value-engineering target USD 3,000 | USD 2,794 [J1] | Met |
| R10 | Guarding | All slots meet ISO 13857 on paper [G1 to G3] | Met on paper |
| R11 | Handling | 33.7 kg frame by two people [I4]; full drum never lifted | Met with a two-person rule |
| R12 | Yield | Three panels 233 to 234 x 1,800 mm, two 552 mm heads [A1 to A3] | Met by design |

## Where the numbers come from

- `docs/04-calcs/sizing.py` (this note's script) and `docs/04-calcs/results.csv`.
- `cad/src/model.py`: geometry, `PARAMS`, `levels()`, fit checks.
- `bom/bom.csv` and `project.yaml`.
- ISO 13857:2019, Safety of machinery: safety distances to prevent hazard zones being reached by upper and lower limbs, Table 4.
