---
doc_id: DMP-DDR-001
title: DrumPanel TRL 2 review decisions
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
  change: TRL 2 review items and the open questions of DMP-PRB-001 decided under Amish's pre-approval of 2026-10-03
---

# 0001: TRL 2 review decisions

- **Date:** 2026-10-03
- **Status:** accepted. Decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

## Context

The TRL 2 review (`docs/REVIEW.md`, session 2026-10-03, TRL 2) found five open questions in DMP-PRB-001 v0.1 and eight key design choices for the precis. Amish pre-approved every recommendation for this batch, so each is recorded here as decided. Choices that touch safety take the conservative option, and each says what evidence would relax it. Partners and regions are the first candidate to approach, not agreed.

## Options considered

*Table 1. Options for each item.*

| # | Item | Options | Chosen |
| --- | --- | --- | --- |
| D1 | Purge method | (a) water fill with detergent, soak and drain; (b) air flush with a blower; (c) steam | (a): no power or fuel; water reused through a settling drum |
| D2 | Vapour check | (a) bought pumped LEL detector, pass below 5 % LEL; (b) pass below 10 % LEL; (c) indicator tubes or a smell test | (a), the conservative threshold |
| D3 | Drums accepted | (a) only drums labelled for non-volatile oils (flash point above 60 °C); (b) any drum after purge | (a), the conservative rule |
| D4 | Paint | (a) panels leave painted, paint removal a separate cold step; (b) a stripping station in the set | (a) |
| D5 | Heads | (a) hand-cranked wheel cutter on the chime, after US3161952A; (b) chisel; (c) bought deheader | (a) |
| D6 | Side and rings | (a) one hand-cranked rotary shear head for the slit and the ring cuts; (b) lever shear; (c) separate tools | (a) |
| D7 | Flattening | (a) hand slip roll; (b) three-roll pyramid; (c) hammering | (a); see DMP-DDR-002, P6 |
| D8 | Steel range | Body 0.8 to 1.5 mm, heads 1.0 to 1.5 mm; forces sized at 1.5 mm | As stated |
| D9 | Ownership | (a) one shared bench set per cooperative or cluster; (b) one per workshop | (a) |
| D10 | Shared blocks | (a) standard 300 mm crank with #40 chain, drawn to accept the proposed hand capstan block later; (b) wait for the block | (a) |
| D11 | First co-design partner | (a) Haitian metal artists reached through a fair trade organisation already working with them (first candidate: Singing Rooster), a vocational welding school second; (b) a vocational school first | (a), first candidate to approach only; nothing agreed |
| D12 | Slit position | (a) 50 mm beside the drum's welded side seam; (b) through it | (a): the shear cannot cut the seam weld cleanly |

## Decision

*Table 2. Decisions.*

| # | Decision | Safety note: evidence that would relax it |
| --- | --- | --- |
| D1 | Water fill with a little detergent through the top bung, soak 10 min, drain through the bottom bung; repeat if the check fails. Water settles in a spare drum; oil is skimmed for a recycler | Not a safety relaxation |
| D2 | Pumped LEL detector, bump-tested each day; a drum passes only below 5 % LEL at both bungs; recheck a drum that stands overnight | A log of at least 50 drums with readings, reviewed by a competent person, could support the 10 % LEL limit used for hot work, since cold cutting is a smaller ignition source |
| D3 | Only drums labelled for non-volatile oils; fuel, solvent, chemical, unknown and unlabelled drums are rejected | A supplier audit and a validated purge for a named product could add it to the accepted list |
| D4 | Panels painted; paint removal outside the design, cold only | None needed |
| D5 | End cutter with a hardened wheel cutting just inside the chime | None needed |
| D6 | One shear head, swivelled 90 degrees between slit and ring position | None needed |
| D7 | Slip roll (pinch pair plus bending roll) | None needed |
| D8 | Steel range as stated | None needed |
| D9 | Shared bench set | None needed |
| D10 | Standard crank and chain now | None needed |
| D11 | First candidate to approach as stated; not agreed | None needed |
| D12 | Slit 50 mm beside the welded seam | None needed |

## Consequences

The purge, vapour check and acceptance rule are written into DMP-PRC-001 and DMP-BLD-001 and into the procedure sheets (BOM line 22). The vapour check kit is the largest cost line (USD 600). D6 and D7 set the shape of the constructable design in DMP-DDR-002.
