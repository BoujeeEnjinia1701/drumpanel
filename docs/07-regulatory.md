---
doc_id: DMP-REG-001
title: DrumPanel regulatory and standards register
project: DrumPanel
doc_type: Regulatory register
version: "0.1"
status: Draft
date: 2026-10-24
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: First register (kit 1.8 upgrade of a TRL 3 repo); container preparation, hot work, flash point, machinery safety, ergonomics, gas detector and waste oil rows; Haiti rows to assess
---

# DrumPanel regulatory and standards register

The bench set is a hand-powered tool published as an open engineering reference, never as certified equipment. Its design follows the container preparation and machinery safety practice that applies to hot and cold work on used drums; the national rules of the country where a set is first used (Haiti or wherever the partner cooperative works) are still to assess, above all for purge water and waste oil. Not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. Machinery and ergonomics rows shared across the Circular Materials focus area are cited from CRP-REG-001 (CoirPress, checked 2026-10-24). Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | 29 CFR 1926.352(i) and 29 CFR 1910.252(a)(3), welding and cutting of used containers | United States | Drums that held flammable or toxic substances are filled with water or cleaned, ventilated and tested before welding, cutting or heating | The purge (water fill, drain) and the vapour check follow this practice although the bench set never heats a drum (PR-001, PR-002) | Design lead | Applies (as guidance outside the United States) |
| G2 | AWS F4.1:2017, safe practices for the preparation of containers and piping for welding, cutting and allied processes | International practice | Cleaning by water, steam or chemicals, inerting, testing before work | Water cleaning is the method chosen (DMP-DDR-001, D1); the procedure sheets follow its sequence | Design lead | Applies (as guidance); text to read before TRL 4 |
| G3 | 29 CFR 1915.14(b), hot work: no hot work at or above 10 % of the lower explosive limit | United States (shipyards) | The vapour threshold for hot work | The basis of PR-002 (flag at 10 % LEL); the bench set passes a drum only below 5 % LEL, half that | Design lead | Met by design |
| G4 | Globally Harmonized System (GHS) classification of flammable liquids | International | Flash point categories: category 3 up to 60 °C, category 4 above 60 to 93 °C | The drum acceptance rule (PR-013) takes oils with flash points above 60 °C; whether to raise it to 93 °C is open decision 2 in DMP-DEC-001 | Design lead | Applies |
| G5 | IEC 60079-29-1, explosive atmospheres: performance requirements of detectors for flammable gases | International | Performance of portable flammable gas detectors | The bought pumped LEL detector (BOM line 4) should meet it, and be certified for use in hazardous areas | Partner (purchaser) | To assess when the detector is chosen |
| G6 | ISO 12100, safety of machinery: risk assessment and risk reduction | International | Hazard identification and the order of risk reduction | DMP-RSK-001 follows its method for the shears, rolls, punch and chains | Design lead | Applies (as guidance for a non-certified hand tool) |
| G7 | ISO 13857:2019, safety distances to prevent hazard zones being reached by upper and lower limbs | International | Openings in guards and their distance from danger points | Every slip roll and shear head slot is 8 mm or less and at least 45 mm from its nip (PR-010, DMP-CAL-001 section 7) | Design lead | Met by design on paper; guards as built checked at TRL 4 |
| G8 | ISO 11228-1 (manual handling, lifting) and EN 1005-3 (recommended force limits for machinery operation) | International; Europe | Lifting masses and hand forces | Lifts against the 25 kg reference mass (PR-011); crank and lever forces at or below 150 N (PR-006), an EN 1005-3 assessment at TRL 4 | Design lead | To assess (EN 1005-3 at TRL 4) |
| G9 | EU Machinery Directive 2006/42/EC and Machinery Regulation (EU) 2023/1230 | European Union | Machinery placed on the EU market | Machinery is defined as having a drive system other than directly applied human or animal effort (CRP-REG-001); the bench set is worked by hand, so it is probably outside the scope | Design lead | To assess (probably does not apply) |
| G10 | EN 388, protective gloves against mechanical risks | Europe and international buyers | Cut resistance levels of gloves | BOM line 24 asks for EN 388 cut level C or higher for every task with cut edges | Partner (purchaser) | Applies |
| G11 | National rules on waste oil and oily water | Country of use (Haiti first) | Storage, disposal and recycling of used oil and wash water | Purge water is settled and reused; skimmed oil goes to a closed container for a recycler (PR-014); the disposal route must be agreed with the partner | Partner | To assess |
| G12 | National occupational safety rules for workshops | Country of use (Haiti first) | Workshop safety, young workers, protective equipment | Apprentices do this stage of the work today; age and training rules to check with the partner | Partner | To assess |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- 29 CFR 1926.352, Fire prevention, paragraph (i), Legal Information Institute, https://www.law.cornell.edu/cfr/text/29/1926.352, checked 2026-10-25.
- 29 CFR 1910.252, Welding, cutting and brazing, paragraph (a)(3), Legal Information Institute, https://www.law.cornell.edu/cfr/text/29/1910.252, checked 2026-10-25.
- 29 CFR 1915.14, Hot work, paragraph (b), Legal Information Institute, https://www.law.cornell.edu/cfr/text/29/1915.14, checked 2026-10-25.
- American Welding Society, F4.1:2017, https://pubs.aws.org/p/1759/f412017-safe-practices-for-the-preparation-of-containers-and-piping-for-welding-cutting-and-allied-processes, checked 2026-10-25.
- Workplace Health and Safety Queensland, "Flammable and Combustible Liquids" (GHS categories), https://worksafe.qld.gov.au/safety-and-prevention/hazards/hazardous-chemicals/specific-hazardous-chemicals/flammable-and-combustible-liquids, checked 2026-10-25.
- ISO 13857:2019, https://www.iso.org/standard/69569.html, checked 2026-10-25.
- CRP-REG-001 v0.2 (CoirPress, Circular Materials focus area): EU machinery definition, ISO 12100, ISO 13857, EN 1005-3, ISO 11228-1, checked 2026-10-24.
- IEC 60079-29-1 and EN 388: titles as published; clauses to be read with a qualified reviewer before any compliance claim.
