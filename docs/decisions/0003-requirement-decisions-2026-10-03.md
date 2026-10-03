---
doc_id: DMP-DDR-003
title: DrumPanel requirement decisions of 2026-10-03
project: DrumPanel
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Amish's choices 5A (R7) and 8A (R5) carried into the model, calculations, drawings and build plan
---

# 0003: Requirement decisions of 2026-10-03

- **Date:** 2026-10-03
- **Status:** accepted. Decided by Amish on 2026-10-03, choosing option A on every requirement decision put to him: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A". For DrumPanel these are 5A (R7) and 8A (R5).

## Context

At TRL 3 the constructable design (DMP-DDR-002) missed R7, four drums an hour for two people, at about 2.0 drums an hour: the four hacksaw notches (8 minutes) and the six single ring cuts (about 12 minutes) made the cutting cradle the bottleneck. R5, flat within 10 mm over 1 m, was at risk: the bending roll must be within 0.29 mm of the right height, which was about 1.4 divisions of the 12-division handwheels on the M20 x 2.5 bending screws.

## Options considered

*Table 1. The two decisions put to Amish.*

| Decision | Option chosen | What it asked for |
| --- | --- | --- |
| 5A, R7 throughput | A | Add a lever notching punch to replace the four hacksaw notches, and a second shear head so two ring cuts are made per pass; recompute hands-on minutes and drums an hour; restate R7 to 2.5 drums an hour |
| 8A, R5 flatness | A | Add a fine-pitch screw adjuster with a dial and a lock to set the bending roll height |

## Decision

*Table 2. Changes made to the model, the BOM and the calculations.*

| # | Change | How it is built | Result |
| --- | --- | --- | --- |
| Q1 | Lever notching punch (5A) | A C-frame punch of S355 plate with two stations, slid into the open drum end: station 1 notches each chime (60 x 35 mm, open-ended) with the frame's back face on the drum end; station 2, 338 mm out, slots each hoop (40 x 32 mm) with the drum end against the station 1 die block. D2 punches with faces raked 10 degrees, each pushed by a Tr24 x 5 screw turned by a 500 mm ratchet lever. The chime notch is widened from 40 to 60 mm so the punch's lower jaw passes in through it to reach the hoop | Chime notch 24.3 kN, lever 131 N; hoop slot 6.6 kN, lever 36 N; four notches in 4.0 minutes, down from 8 (DMP-CAL-001, section 9) |
| Q2 | Ring head (5A) | A second shear head made to the same drawings without a drive, lowered through the slit and bolted to the main head with a 10 mm spacer plate once the main head is swivelled for ring cuts; nips 233 mm apart (234 mm for the middle pass); a coupling shaft in a loose guard sleeve joins the two upper shafts | Six ring cuts in three passes, 9.5 minutes, down from about 12.4; 20.4 kg (DMP-CAL-001, sections 4.1 and 8) |
| Q3 | Raised shear head drive (design for construction, found while carrying out Q2) | The crank moves off the upper shaft onto a raised crank shaft in a closed drive case on the side of the head: 12 to 28 tooth #35 chain to a jackshaft, then 15 to 15 tooth down to the upper shaft, 2.33 to 1; crank 155 mm | The former 200 mm crank on the upper shaft swept through the drum wall (about 13,700 mm³ in the model's sweep check), so it could not make a full turn in either mode. The new crank sweeps clear of the drum, posts, beam and trolley in both modes, and two ring cuts on 1.5 mm steel need 136 N, within R6; the slit needs 68 N but takes 2.7 minutes, up from 2.3 |
| Q4 | Fine-pitch dial adjuster (8A) | Each bending screw becomes an M20 x 1.5 fine-pitch screw with an 80 mm dial of 60 divisions (0.025 mm each) clamped to it, a pointer on the bridge, and a lock nut on the bridge that holds the setting | The 0.29 mm allowance is 11.8 divisions; the trial pass on the first drum of a batch gives a reading that every later drum is set to (DMP-CAL-001, section 5.3) |
| Q5 | Tool shelf | A plate shelf bolted to the outer face of the left rail post holds the notching punch, its lever and the ring head with its spacer plate and coupling | The tools have a place at the cradle; about 40 kg on the shelf |

Q3 is a change made to keep the design constructable under STANDARDS section 18 (Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible"). It keeps what the shear head does and does not change the pitch or the safety case; the closed drive case is also the guard for its two chains.

**R7 restated.** R7 now reads "at least 2.5 drums to flat sheet per hour for a two-person team" (DMP-REQ-001 v0.4), as Amish chose in 5A.

## Consequences

- R7: about 2.26 drums an hour for two people, 53.1 hands-on minutes a drum against the 48.0 that 2.5 drums an hour needs. Up from 2.0, but still not met. What to do about the remaining gap is posed to Amish in the register (DMP-DEC-001, Open decisions).
- R5: met on paper with a trial pass for each batch of drum steel.
- R6: met on paper; the hardest efforts are two ring cuts on 1.5 mm steel (136 N) and the punch lever on a chime (131 N).
- R11: the shear head with its drive is 23.7 kg, the ring head 20.4 kg and the punch 18.7 kg, all under the 25 kg one-person limit; the cradle frame (33.7 kg) is still the only two-person lift.
- Cost: value-engineering target USD 3,000. Estimated cost of the constructable design: USD 3,489 (USD 489 over the target). The changes added USD 695: notching punch USD 330 in place of the USD 45 hacksaw line, ring head USD 255, shear head drive USD 75, dial adjusters USD 40, tool shelf USD 40.
- The chime notch force is the least certain new number: a real chime's layers and clinch vary. It is to be confirmed on a scrap chime at TRL 4 (DMP-DEC-001, To confirm when parts are bought).
- The model (52 components), its checks (now with ring passes for both heads, crank sweeps and the four punch positions), the general arrangement DMP-DWG-001 Rev P2, making sketches DMP-DWG-105, 109, 110 and 116 at Rev P2 and new sketches DMP-DWG-120 to 123, the concept media and the build plan DMP-BLD-001 v0.2 are drawn from the changed model.
