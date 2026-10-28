"""DrumPanel STEM check calculations (DMP-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv and the claims table in docs/01b-stem-check.md (between the STM_TABLE markers).
Option A rows (S1 to S24) take their numbers from the calculation note DMP-CAL-001 (docs/04-calcs/sizing.py, which reads
the station model of cad/src/model.py); option B rows (B1 to B8) are first-order screens of the lever shear and stretch
leveller from PARAMS (DMP-OPT-001). First-order screens; they never replace the calculation note.
"""
import contextlib
import io
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "docs/04-calcs"), str(ROOT / "cad/src")]
from stem_check import Check, limits, G, WITHIN, PLAUSIBLE, FIX  # noqa: E402,F401
with contextlib.redirect_stdout(io.StringIO()):
    import sizing as S  # noqa: E402
    d = S.drum_yield()
    pg = S.purge(d)
    ec = S.end_cutter()
    sh = S.shear_head()
    sr = S.slip_roll(d)
    S.cradle(d)
    kp = S.notching_punch()
    th = S.throughput(ec, d, sr, sh, pg, kp)
    st, lifts = S.masses()
from model import PARAMS as P, levels  # noqa: E402

R = {r[0]: r for r in S.OUT}           # tag -> (tag, text, value, unit)
L = levels()
c = Check(ROOT / "docs/04-calcs/stem_results.csv")
CAL = "DMP-CAL-001"
R6 = 150.0                               # N, crank and lever force limit (DMP-PRS-001 PR-006)

# ------------------------------------------------------------------------------------------------ option A
r_mid = P["DRUM_R_IN"] + P["DRUM_T"] / 2
body_l = P["DRUM_L"] - 2 * P["RING_CUT"] - 4 * P["HOOP_CUT"]
body_area = 2 * math.pi * r_mid * (P["DRUM_L"] - 2 * P["CHIME_L"]) * 1e-6
c.claim("S1", "Each drum gives three flat panels with about 1.26 m2 of sheet", "Mathematics", "Units and dimensional analysis",
        "Panels = mid-wall circumference x body length left after the chime rings and hoop strips are cut out (0.70 x 1.80 m); it must be "
        "less than the whole body between the chimes; the independent review found the README's three sheets of 460 x 1,830 mm per drum "
        "(2.5 m2) cannot come from one drum, and the README is corrected", round(d["panel_area"], 2), round(body_area, 2), "m2", closed_by=CAL)
vol = math.pi * (P["DRUM_R_IN"] / 1000) ** 2 * (P["DRUM_L"] - 2 * P["HEAD_RECESS"]) / 1000
c.order_of_magnitude("S2", "A drum full of water weighs about 240 kg, so it is filled and drained on its stand and never lifted", "Physics",
                     "Mechanics and statics", claimed=pg["full_m"], estimate=vol * 1000 + d["drum_m"], unit="kg",
                     law="Mass = water volume (pi r2 L) x 1,000 kg/m3 + empty drum", closed_by=CAL)
a_b = math.pi * 0.025 ** 2
ri_m, len_m, hb = P["DRUM_R_IN"] / 1000, (P["DRUM_L"] - 2 * P["HEAD_RECESS"]) / 1000, (P["DRUM_R_IN"] - 230.0) / 1000
r_mm, l_mm = P["DRUM_R_IN"], P["DRUM_L"] - 2 * P["HEAD_RECESS"]
v, t_d = S.horizontal_volume(2 * r_mm, r_mm, l_mm), 0.0
v_b = S.horizontal_volume(hb * 1000, r_mm, l_mm)
while v > v_b:                              # falling level in a horizontal cylinder, down to the bung centre
    lo, hi = 0.0, 2 * r_mm
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if S.horizontal_volume(mid, r_mm, l_mm) < v else (lo, mid)
    v -= 0.6 * a_b * math.sqrt(2 * G * max(lo / 1000 - hb, 1e-4)) * 1e9
    t_d += 1.0
c.order_of_magnitude("S3", "A full drum drains through its 2 in bung in about 2.3 min", "Physics", "Fluid mechanics",
                     claimed=pg["drain"], estimate=t_d / 60, unit="min",
                     law="Torricelli outflow Q = Cd a sqrt(2 g h), Cd 0.6, integrated over the falling level of a horizontal cylinder to the bung "
                         "centre (the CAL adds the slow tail to the lip); the top bung is open as the vent", closed_by=CAL)
c.cited("S4", "A water fill and drain, then a pumped LEL reading below 5 % LEL at both bungs, makes a drum that held a non-volatile oil "
        "safe to cut cold", "Chemistry", "Physical chemistry (flammability)",
        "29 CFR 1926.352(i): containers that held flammable substances are filled with water or cleaned, ventilated and tested before "
        "cutting; 29 CFR 1910.252(a)(3); hot work barred at or above 10 % of the LEL (29 CFR 1915.14(b)); AWS F4.1:2017 water cleaning",
        "Pass level 5 % LEL is half the 10 % hot-work limit; the oils accepted have flash points above 60 C (GHS category 3 upper bound), "
        "so little vapour forms at workshop temperatures; the reading, not the purge, is the safeguard. The independent review found that "
        "a catalytic sensor calibrated on methane under-reads heavy hydrocarbon vapour (relative response about 0.3 to 0.5), so a true 10 to "
        "15 % LEL could read 5 %: fixed by specifying the LEL channel calibrated on pentane or set with the maker's correction factor "
        "(BOM line 4, PR-002)", WITHIN, closed_by="DMP-DEC-001 fix F3")
c.claim("S5", "The end cutter takes a 1.5 mm head out with a crank force of at most 27 N", "Physics", "Strength of materials",
        "Wheel shear F = tau t2 / (2 tan theta) against the chime wall, feed resistance F tan(theta / 2), 30 % roller losses, 150 mm crank",
        round(ec["crank"]), R6, "N", closed_by=CAL)
c.claim("S6", "Two ring cuts at once on a 1.5 mm wall need at most 136 N at the shear head crank", "Physics", "Mechanics and statics",
        "Rotary shear F = tau t2 / (2 tan theta), 1.0 mm overlap; edge spreading round the web 100 N at 1.2 mm (estimate, cubic in t); "
        "20 % bearing losses; 2.33 to 1 drive, chains 95 % each; 155 mm crank (CAL section 4)", round(sh["crank2"]), R6, "N", margin=0.1,
        closed_by=f"{CAL} [D15r]; the spreading force is to measure on a scrap drum at TRL 4")
c.claim("S7", "The lever notching punch cuts the five-layer chime notch with at most 131 N on its 500 mm ratchet lever", "Physics",
        "Strength of materials", "Inclined-edge shear per edge 0.5 tau t2 / tan(rake), rake 10 deg, five layers, 20 % stripping; Tr24 x 5 screw, "
        "friction 0.15 (CAL section 9); a flat punch would need about 177 kN, so the rake does the work", round(kp["lever"]), R6, "N", margin=0.15,
        closed_by=f"{CAL} [K3]; the chime notch force is the least certain number, to confirm on a scrap chime at TRL 4")
c.claim("S8", "The shear head frame and shafts carry the separating force at 1.5 mm with a large margin", "Physics", "Strength of materials",
        "Web in bending and tension, 25 mm shaft in bending at 1,429 N (CAL section 4); S275 yield 275 MPa, used at 0.6 of yield",
        max(float(R["D20"][2]), float(R["D21"][2])), 0.6 * 275, "MPa", closed_by=CAL)
rng = [float(x) for x in str(R["E11"][2]).split(" to ")]
c.claim("S9", "The bending roll setting that leaves a panel flat (9.3 to 19.3 mm above the lower roll) lies inside the 60 mm slot travel",
        "Physics", "Strength of materials", "Elastic and perfectly plastic reverse bending: x - M(x)/Me = k0 / ke, Me = sy b t2 / 6, springback to "
        "flat; yield 200 to 300 MPa, wall 0.8 to 1.2 mm (CAL section 5.2)", rng[1], 60.0, "mm", closed_by=CAL)
c.claim("S10", "With the first panel of every drum checked and the dial trimmed, the slip roll leaves panels flat within 10 mm over 1 m",
        "Engineering and technology", "Manufacturing tolerances", "Setting allowance 0.29 mm from the derivative of the residual curvature (CAL "
        "section 5.3); a change of only 0.02 mm of wall or 5 MPa of yield uses it up, so a setting found once per batch (as first claimed) "
        "does not hold from drum to drum (independent review, recomputed in CAL section 5.3): fixed by a straightedge check of the first panel "
        "of every drum, a dial trim, and a second pass, turned over if over-bent, for a panel out of tolerance; the dial resolution must be at "
        "most a quarter of the allowance", round(P["BEND_PITCH"] / P["DIAL_DIV"], 3), round(sr["dz"] / 4, 3), "mm",
        closed_by=f"DMP-DEC-001 fix F1; {CAL} sections 5.3 and 8")
eps_sheet = 100.0 * 0.5 * P["DRUM_T"] * (1 / r_mid + 1 / sr["rho"])
c.claim("S11", "Cutting the hoop strips out keeps the slip roll to plain sheet; rolled flat, a hoop crown would stretch about 8.5 %", "Physics",
        "Strength of materials", f"Crown strain = hoop height x change of curvature, against the {eps_sheet:.2f} % surface strain of a plain panel in "
        "the slip roll: a strain more than ten times larger cannot be put in evenly by three rolls, so a rolled hoop would leave the panel "
        "buckled (DMP-DDR-002, P7); a design rationale: the check shows the crown strain is above ten times the panel strain", float(R["E29"][2]), 10 * eps_sheet,
        "%", rule="above", closed_by=CAL)
c.claim("S12", "The geared pinch rolls grip three panels with enough force to drive them through the bend", "Physics", "Mechanics and statics",
        "Pinch force needed = 1.5 x feed resistance / (2 x friction 0.15) at the worst steel (300 MPa, 1.2 mm); two M16 screws set 2 kN (CAL "
        "section 5.5)", 2000.0, float(R["E19"][2]), "N", rule="above", closed_by=CAL)
tr15 = float(R["D15t"][2])
c.claim("S13", "The single driven shear disc pulls the head along the cut at 1.5 mm wall", "Physics", "Mechanics and statics",
        "Traction 0.3 x separating force (the edge bites) against the feed resistance (CAL section 4); below 1 the operator pushes the trolley",
        tr15, 1.0, "of the resistance", rule="above", margin=0.2,
        closed_by=f"{CAL} [D15t]; friction 0.3 is a screening value, the fallback is a hand push on the trolley")
lift_one = max(w for n, w in lifts if "Cradle frame" not in n)
c.claim("S14", "Every piece one person lifts from bench height is 25 kg or less; heavier pieces, and the shear head and ring head lifted to the "
        "rail, are two-person lifts", "Biology", "Ergonomics",
        "ISO 11228-1 reference mass 25 kg, which holds only for ideal lifting; the independent review put the recommended limit for lifting the "
        "23.7 kg shear head up to the rail beam at about 10 kg, so the build plan and PR-011 make both heads two-person lifts; masses from the "
        "station model (CAL section 10)", round(lift_one, 1), 25.0, "kg", closed_by=CAL)
c.claim("S15", "Every crank and lever force in normal use is at or below 150 N", "Biology", "Human physiology and biomechanics",
        "Forces from S5 to S7 and the slip roll crank (20 N at 300 mm, CAL section 5.5); 150 N is the requirement PR-006, a conservative screen "
        "for a two-hand crank in a standing posture (EN 1005-3 assessment at TRL 4)", round(max(ec["crank"], sh["crank2"], kp["lever"], sr["crank"])),
        R6, "N", margin=0.1, closed_by=f"{CAL}; EN 1005-3 assessment at TRL 4")
c.claim("S16", "Slots made 7 to 8 mm wide and at least 45 mm from the slip roll nip keep fingers out", "Engineering and technology", "Standards practice",
        "ISO 13857:2019 Table 4: a slot over 6 mm and up to 8 mm needs at least 20 mm to the danger point (CAL section 7); a slot made over 8 mm "
        "would need 80 mm, so the slots are toleranced 7 to 8 mm (fix F4, PR-010)", 20.0, 45.0, "mm", rule="below",
        closed_by=f"{CAL}; DMP-DEC-001 fix F4")
zone = 2e-3 * 1.5e-3 * 1.0 * 7850
q_cut = 288e6 * 1.5e-3 * 1.5e-3 * 1.0 + 365.0 * 1.0
dT = q_cut / (zone * 460)
c.claim("S17", "Cold cutting stays cold: slow shearing of 1.5 mm wall does not heat the cut zone toward an oil's autoignition temperature", "Physics",
        "Thermodynamics", "Plastic work tau t x t per metre plus feed work 365 J, into a 2 mm wide strip (c = 460 J/kg K) with no heat flow "
        "away; the independent review showed this is not a bound, since a narrower shear zone (0.2 to 0.9 mm) gives a higher local rise; the "
        "cut moves at about 4 m/min, so heat spreads into the sheet; lubricating oils autoignite above about 250 C (220 K above a 30 C "
        "workshop); the safeguard is the vapour reading below 5 % LEL (S4), and no grinder or torch is used", round(dT), 220.0, "K", margin=0.6,
        closed_by="DMP-STM-001 S4 (the vapour reading is the safeguard); cut edge temperature to measure at TRL 4")
c.cited("S18", "Hardened D2 discs and a hardened cutter wheel shear 0.8 to 1.5 mm low-carbon drum steel without chipping", "Chemistry",
        "Materials and polymer chemistry", "Slitter knives for low-carbon sheet are commonly D2 tool steel hardened to about 58 to 62 HRC "
        "(cutting tool supplier practice); the drum steel is about 250 MPa yield", "Within practice; the discs bought are to the BOM line 10 "
        "specification (DMP-DEC-001, to confirm when bought, item 1)", WITHIN)
c.cited("S19", "Purge water settles and its oil is skimmed off, so the water can be reused", "Chemistry", "Environmental and atmospheric chemistry",
        "Mineral and vegetable oils are less dense than water (about 850 to 920 kg/m3) and separate by gravity; a biodegradable detergent "
        "emulsifies some oil, so the water settles overnight before it is reused; the independent review found that fire-resistant hydraulic "
        "fluids (phosphate esters, water glycols, polyalkylene glycols) sink or mix with water: they are excluded at acceptance (fix F5, PR-013)",
        "Within known science; disposal of the skimmed oil follows local rules (DMP-REG-001)", WITHIN, closed_by="DMP-DEC-001 fix F5")
c.cited("S20", "The process has no burning step, so it gives off none of the smoke of burning paint and oil residue", "Biology", "Toxicology",
        "Open burning of coated and oily scrap releases smoke, soot and products of incomplete combustion; the bench set never heats the steel "
        "(PR-001)", "Removed by design; the paint stays on the panels and is removed later by a separate cold step (DMP-DDR-001, D4)", WITHIN)
c.cited("S21", "The bench set removes the chisel blows: its cuts and rolling are continuous, and the only impact step is setting the panel ends "
        "with a dead-blow mallet", "Physics", "Acoustics and vibration",
        "Impact noise comes from blows on sheet steel; continuous rotary shearing and rolling at hand speed make no impacts (CAL section 5.4)",
        "Within known science as a mechanism; sound levels are not claimed and are measured at TRL 4", WITHIN)
c.claim("S22", "The eccentric bush sets the 1.0 mm disc overlap within its adjustment range", "Engineering and technology", "Manufacturing tolerances",
        "A 3 mm eccentric moves the upper shaft over a 6 mm range; the overlap is set and locked (DMP-DDR-002, P4)", P["DISC_OVERLAP"], 6.0, "mm",
        closed_by=CAL)
c.claim("S23", "A cradle roller shaft carries the drum and a person leaning on it (1 kN) well below yield", "Physics", "Strength of materials",
        "Simply supported 25 mm shaft, two roller loads (CAL section 6); bright steel taken at S275 yield 275 MPa, used at 0.6 of yield",
        float(str(R["F3"][2]).split(";")[0].split()[0]), 0.6 * 275, "MPa", closed_by=CAL)
c.balance("S24", f"Two people turn about {th['rate']:.2f} drums an hour into flat panels (PR-007 asks 2.5)", "Mathematics", "Orders of magnitude",
          inputs={"two people, minutes an hour": 120.0}, outputs={"hands-on minutes": th["total"] * th["rate"]}, unit="min",
          law=f"Rate = 2 x 60 / hands-on minutes per drum ({th['total']:.1f} min, CAL section 8), with the per-drum flatness check of fix F1; "
              "task times are estimates; checks the arithmetic only, the timed trial measures the times")
c.claim("S25", "Two drain stands purge drums faster than the cradle and slip roll use them", "Mathematics", "Orders of magnitude",
        f"Stand cycle {th['cycle']:.1f} min a drum (load, fill 11 min, soak 10 min, drain, tip, check; CAL section 8); the independent review "
        "found one stand would limit the set to about 1.7 drums an hour: fixed by a second stand and tray (fix F2, BOM lines 1 and 2)",
        round(S.STANDS * 60 / th["cycle"], 2), round(th["rate"], 2), "drums/h", rule="above", closed_by="DMP-DEC-001 fix F2")
fb = float(R["E17"][2])
i_roll = math.pi * (2 * P["ROLL_R"]) ** 4 / 64
span_r = 2 * (P["SIDE_X"] + P["SIDE_T"] / 2)
defl_b = 5 * (fb / span_r) * span_r ** 4 / (384 * S.E * i_roll)
c.claim("S26", "The 60 mm bending roll bends little enough under its worst load that all three panels see the same setting", "Physics",
        "Strength of materials", f"Simply supported roll over {span_r:.0f} mm under {fb:.0f} N spread along it; mid-span deflection against half the "
        "0.29 mm setting allowance (CAL section 5.5)", round(defl_b, 3), round(sr["dz"] / 2, 3), "mm", closed_by=CAL)
c.claim("S27", "The notching punch C-frame jaws stay well below yield", "Physics", "Strength of materials",
        "Cantilever jaw root bending at the hoop station (CAL section 9); S355 yield 355 MPa used at 0.6 of yield",
        float(str(R["K5"][2]).split(";")[0].split()[0]), 0.6 * 355, "MPa", closed_by=CAL)
c.claim("S28", "The rail beam keeps the shear head on a straight line with both heads on it", "Physics", "Strength of materials",
        "Mid-span deflection of the 80 x 40 x 3 RHS beam under the trolley, both heads and drive (CAL section 4.1), against the 1 mm "
        "straightness of PR-004's rail", float(R["D26"][2]), 1.0, "mm", closed_by=CAL)

# ------------------------------------------------------------------------------------------------ option B
tau = S.TAU
t = 1.5
f_cut = 0.5 * tau * t * t / math.tan(math.radians(P["B_RAKE"]))
ma = P["B_LEVER"] / P["B_CRANK"] * P["B_ARM_REAR"] / P["B_ARM_FRONT"]
f_hand = f_cut / ma / 0.85
c.claim("B1", "Option B: one person cuts 1.5 mm drum steel with the 1,050 mm shear lever", "Physics", "Mechanics and statics",
        f"Inclined blade shear 0.5 tau t2 / tan(rake), rake {P['B_RAKE']:.0f} deg: {f_cut / 1000:.2f} kN; lever and link advantage "
        f"{ma:.1f}, efficiency 0.85; lever throatless shears of this class are sold for 14 gauge (1.9 mm) mild steel (Beverly B-1)",
        round(f_hand), R6, "N", closed_by="")
w, tb = 234.0, 1.2
f_st = 300.0 * 1.1 * w * tb
c.claim("B2", "Option B: a 15 t hand-pumped cylinder stretches the widest, thickest panel 2 % past yield", "Physics", "Strength of materials",
        "F = flow stress x area; 300 MPa yield x 1.1 for strain hardening at 2 %, 234 x 1.2 mm", round(f_st / 1000, 1), P["B_RAM_KN"], "kN",
        closed_by="")
k_curl = (tb / 2) / r_mid
eps_y = 300.0 / S.E
c.claim("B3", "Option B: a 2 % stretch takes out the drum's curl", "Physics", "Strength of materials",
        "Stretcher levelling: once the whole section yields in tension the bending stresses that hold the curl are wiped out; needs total "
        f"strain above curl strain t / 2R ({100 * k_curl:.2f} %) plus yield strain ({100 * eps_y:.2f} %); levellers use 1 to 3 %",
        100 * P["B_STRAIN"], 100 * (k_curl + eps_y), "%", rule="above", closed_by="")
a_ram = math.pi * (P["B_RAM_BORE"] / 2) ** 2
p_ram = f_st / a_ram
f_pump = p_ram * math.pi * (P["B_PUMP_PISTON"] / 2) ** 2 / P["B_PUMP_RATIO"] / 0.8
c.claim("B4", "Option B: the hand pump handle needs at most 150 N at the stretch force", "Biology", "Human physiology and biomechanics",
        f"Pressure = force / plunger area ({P['B_RAM_BORE']:.0f} mm): {p_ram:.0f} MPa; pump piston {P['B_PUMP_PISTON']:.0f} mm, handle ratio "
        f"{P['B_PUMP_RATIO']:.0f}, pump efficiency 0.8 (to confirm on the pump bought)", round(f_pump), R6, "N", closed_by="")
s_bed = f_st / (2 * 1350.0)
c.claim("B5", "Option B: the two UPN 100 bed channels carry the stretch force in compression", "Physics", "Strength of materials",
        "Axial stress = F / (2 x 1,350 mm2), ties at 550 to 650 mm keep the channels short against buckling; S275 used at 0.6 of yield",
        round(s_bed, 1), 0.6 * 275, "MPa", closed_by="")
mu_back = 0.10
c.claim("B6", "Option B: the wedge grips tighten as the panel pulls", "Physics", "Mechanics and statics",
        f"A wedge grip holds when the face friction on the panel (serrated, taken as 0.3) exceeds tan(wedge angle) plus the friction on its "
        f"greased back ({mu_back}); the first check (tan(angle) below 0.3, self-locking) was the wrong criterion (independent review), so the wedge "
        f"angle is {P['B_WEDGE_DEG']:.0f} deg; the panel's net section at the serrations is to check if B is chosen",
        round(math.tan(math.radians(P["B_WEDGE_DEG"])) + mu_back, 3), 0.3, "", closed_by="")
c.claim("B7", "Option B: each panel loses its gripped ends", "Mathematics", "Units and dimensional analysis",
        f"Panel length after stretching = 1,800 - 2 x {P['B_GRIP_L']:.0f} mm grip + 2 % (PR-012 asks about 1,800 mm)",
        round(1800 - 2 * P["B_GRIP_L"] + 0.02 * (1800 - 2 * P["B_GRIP_L"])), 1800.0, "mm", closed_by="")
cut_m = 2 * math.pi * L["head_d"] / 2 * 2 / 1000 + 0.82 + 6 * d["circ"] / 1000
strokes = cut_m * 1000 / P["B_BITE"]
t_b = 14 + 2 + strokes * 5 / 60 + 6 + 3 * 4.0 + 3 + 4.4
c.order_of_magnitude("B8", "Option B: two people turn about 1.65 drums an hour into flat panels", "Mathematics", "Orders of magnitude",
                     claimed=1.65, estimate=120 / t_b, unit="drums/h",
                     law=f"{cut_m:.1f} m of cut at a {P['B_BITE']:.0f} mm bite and 5 s a stroke ({strokes:.0f} strokes), plus purge 14, loading 2, "
                         "handling 6, three stretches of 4 min, ends 3 and deburring 4.4 min")


def write_table():
    doc = ROOT / "docs/01b-stem-check.md"
    if not doc.exists():
        return
    rows = ["| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in c.rows:
        rows.append(f"| {r['id']} | {r['claim']} | {r['field']} | {r['branch']} | {r['law']} | {r['check']} | {r['verdict']} | {r['closed_by'] or 'Open'} |")
    txt = doc.read_text(encoding="utf-8")
    new = re.sub(r"<!-- STM_TABLE -->.*?<!-- /STM_TABLE -->", "<!-- STM_TABLE -->\n" + "\n".join(rows) + "\n<!-- /STM_TABLE -->", txt, flags=re.S)
    doc.write_text(new, encoding="utf-8")


if __name__ == "__main__":
    c.write()
    write_table()
    for r in c.rows:
        print(f"{r['id']:4s} {r['verdict']:32s} {r['check']}")
