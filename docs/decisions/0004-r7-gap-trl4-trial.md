---
doc_id: DMP-DDR-004
title: DrumPanel R7 gap left to the TRL 4 timed trial
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
  change: Amish's decision on register open decision 1 (portfolio decision 47) recorded
---

# 0004: R7 gap left to the TRL 4 timed trial

- **Date:** 2026-10-03
- **Status:** decided by Amish Chadha, 2026-10-03: "i approve all of the 47 recommendations provided by you. Execute them." For DrumPanel this is portfolio decision 47, the recommendation on open decision 1 of DMP-DEC-001 v0.2, taken exactly as recommended: option A.

## Context

After decision 5A (DMP-DDR-003) the notching punch and the ring head raised the estimate from about 2.0 to about 2.26 drums an hour for two people, against R7 as restated to 2.5. That is 53.1 hands-on minutes a drum against the 48.0 that 2.5 drums an hour needs [H4, H9]: a gap of 5.1 minutes, about 10 % of the hands-on time. Most of the task times behind the estimate are first estimates, not measurements.

## Options considered

*Table 1. Options.*

| Option | What it means |
| --- | --- |
| A (chosen) | Keep R7 at 2.5 drums an hour and let the TRL 4 timed half-day trial decide; no more hardware at TRL 3. No cost or mass stated |
| B | Restate R7 to 2.25 drums an hour, what the design gives on paper |
| C | Keep 2.5 and add more speed-ups now, such as set stops on the rail for the three ring passes and a second deburring station, with no estimate yet of what they save |

## Decision

Option A. R7 stays "at least 2.5 drums to flat sheet per hour for a two-person team" (DMP-REQ-001). The design, the model, the BOM and the cost do not change. The half-day trial at TRL 4 (build plan DMP-BLD-001, section 5, "Throughput") times each task and records drums an hour against the estimate of 2.26 and the target of 2.5; its result decides whether R7 is met, and if it is not, the options to close the gap (B or C above) come back to Amish with measured times.

## Consequences

*Table 2. Results.*

| Item | Result |
| --- | --- |
| R7 | About 2.26 drums an hour on paper against 2.5: **not met on paper**, unchanged. Decided by the TRL 4 timed trial |
| Other requirements | Unchanged: ten of twelve met on paper, R9 over the value-engineering target |
| Cost | USD 3,489, unchanged (USD 489 over the USD 3,000 value-engineering target) |
| Model, drawings, media | Unchanged; no re-render needed |

- The trial needs the times of each task written down, not only the total, so that a miss can be traced to the station that causes it (the cradle at 23.6 minutes a drum is the largest).
- Speed-up ideas stay in the register's value engineering list for TRL 4: rail stops for the ring passes, a second deburring station, notching drums ahead while another is cut.

## Safety

> **Safety:** This decision changes no hardware. The trial is timed, but the guards, the two-person rule for lifts over 25 kg, the vapour check below 5 % LEL and the safety stops of the build plan apply in full; nobody hurries a step to meet the target, and a step skipped to save time voids the trial. DrumPanel cuts sheet steel from drums that may have held flammable liquids; it is an open engineering reference, not certified equipment.
