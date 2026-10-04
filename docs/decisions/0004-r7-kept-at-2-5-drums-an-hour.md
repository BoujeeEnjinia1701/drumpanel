---
doc_id: DMP-DDR-004
title: DrumPanel R7 kept at 2.5 drums an hour
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
  change: Amish's round-2 decision 5A on R7 recorded
---

# 0004: R7 kept at 2.5 drums an hour; the TRL 4 timed trial decides

- **Date:** 2026-10-03
- **Status:** decided by Amish, 2026-10-03 (round 2): "i agree with all the 46 recommendations you provided. please proceed." For DrumPanel this is decision 5A, the open decision in DMP-DEC-001 v0.2.

## Context

After the notching punch, the ring head and the dial adjuster (DMP-DDR-003) two people turn about 2.26 drums an hour on paper: 53.1 hands-on minutes a drum against the 48.0 that 2.5 drums an hour needs (DMP-CAL-001 v0.2, section 8). Most of the task times behind the estimate are first estimates, not measurements.

## Options considered

| Option | What it means |
| --- | --- |
| A (chosen) | Keep R7 at 2.5 drums an hour and let the TRL 4 timed half-day trial decide; no more hardware at TRL 3 |
| B | Restate R7 to 2.25 drums an hour, what the design gives on paper |
| C | Keep 2.5 and add more speed-ups now (rail stops, a second deburring station), with no estimate of what they save |

## Decision

Option A. No design change. R7 stays at "at least 2.5 drums to flat sheet per hour for a two-person team" and is reported honestly as not met on paper (about 2.26). The half-day trial in the build plan (section 5, Throughput) records each task's time and the drums an hour, and decides R7. If the trial misses 2.5, options B and C come back to Amish with measured times.

*Table 1. Effects.*

| Item | Result |
| --- | --- |
| R7 | Not met on paper, 2.26 against 2.5 drums an hour; kept; the TRL 4 trial decides |
| Other requirements | None changed |
| Mass and geometry | Unchanged |
| Cost | Unchanged. Value-engineering target: USD 3,000. Estimated cost of the constructable design: USD 3,489 (USD 489 over the target). `budget_usd` unchanged |

## Safety

> **Safety:** An empty oil drum can still hold flammable vapour and explode when cut, ground or heated. No drum is cut until it has been purged and passed the vapour check (build plan, stops S4 and S5), and the throughput target never justifies skipping a stop. The kit has shear heads, a punch and a roller: guards stay on and hands stay clear. It is an open engineering reference, not certified equipment.
