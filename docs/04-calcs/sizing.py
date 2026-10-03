"""DrumPanel sizing calculations, DMP-CAL-001.

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every figure used in docs/04-calcs/01-sizing.md, tagged [A1], [B2] and so on, and writes
docs/04-calcs/results.csv. Geometry comes from cad/src/model.py (PARAMS, levels(), components()), costs from
bom/bom.csv and the value-engineering target from project.yaml. First-principles estimates for a paper proof
of concept; CONCEPT, NOT FOR FABRICATION.
"""
from __future__ import annotations

import csv
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
import model as m  # noqa: E402

P, L = m.PARAMS, m.levels()
G = 9.81
E = 200_000.0                 # MPa, steel
SY_NOM, SY_LO, SY_HI = 250.0, 200.0, 300.0   # MPa, drum steel yield (cold-rolled low-carbon sheet)
UTS = 360.0                   # MPa
TAU = 0.8 * UTS               # shear strength
T_NOM, T_LO, T_HI = 1.0, 0.8, 1.2            # body wall; 1.5 mm checked where it governs
RHO_W = 1000.0
OUT = []


def say(tag, text, value=None, unit=""):
    print(f"[{tag}] {text}" + ("" if value is None else f": {value}{(' ' + unit) if unit else ''}"))
    if value is not None:
        OUT.append((tag, text, value, unit))


# ------------------------------------------------------------------ A. drum and what it yields
def drum_yield():
    r_mid = P["DRUM_R_IN"] + P["DRUM_T"] / 2
    circ = 2 * math.pi * r_mid
    panels = L["panels"]
    widths = [x1 - x0 for x0, x1 in panels]
    head_d = L["head_d"]
    body_m = circ * (P["DRUM_L"] - 2 * P["CHIME_L"]) * P["DRUM_T"] * 1e-9 * m.STEEL
    head_m = 2 * math.pi * P["CHIME_R_IN"] ** 2 * P["HEAD_T"] * 1e-9 * m.STEEL
    other = 2.5                                    # chimes, hoops, bungs (kg, estimate)
    drum_m = body_m + head_m + other
    panel_area = sum(widths) * circ * 1e-6
    head_area = 2 * math.pi * (head_d / 2) ** 2 * 1e-6
    panel_m = sum(widths) * circ * P["DRUM_T"] * 1e-9 * m.STEEL
    say("A1", "Panel length (body circumference at mid-wall)", round(circ), "mm")
    say("A2", "Panel widths (outer, middle, outer)", " / ".join(f"{w:.0f}" for w in widths), "mm")
    say("A3", "Head discs, two, diameter", round(head_d), "mm")
    say("A4", "Flat area per drum: three panels", round(panel_area, 2), "m2")
    say("A5", "Flat area per drum: two head discs", round(head_area, 2), "m2")
    say("A6", "Empty drum mass (estimate)", round(drum_m, 1), "kg")
    say("A7", "Mass of the three panels at 1.0 mm", round(panel_m, 1), "kg")
    return dict(circ=circ, widths=widths, drum_m=drum_m, head_d=head_d, panel_area=panel_area)


# ------------------------------------------------------------------ B. drain and purge
def horizontal_volume(h, r, length):
    """Liquid volume (mm3) in a horizontal cylinder filled to depth h."""
    a = r * r * math.acos((r - h) / r) - (r - h) * math.sqrt(max(2 * r * h - h * h, 0.0))
    return a * length


def purge(d):
    r = P["DRUM_R_IN"]
    vol_l = math.pi * r ** 2 * (P["DRUM_L"] - 2 * P["HEAD_RECESS"]) * 1e-6
    full_m = d["drum_m"] + vol_l * RHO_W / 1000
    say("B1", "Drum volume (inside)", round(vol_l), "L")
    say("B2", "Mass of a drum full of water", round(full_m), "kg")
    fill_rate = 20.0                                       # L/min from a 19 mm hose on a mains or tank supply
    say("B3", "Fill time at 20 L/min", round(vol_l / fill_rate, 1), "min")
    # drain through the 2 in bung at the bottom of the low head; Cd 0.6 on a 50 mm opening
    cd, a_b = 0.6, math.pi * 25.0 ** 2 * 1e-6
    bung_r = 230.0
    h_bung = r - bung_r                                     # bung centre above the inside bottom (mm)
    length = P["DRUM_L"] - 2 * P["HEAD_RECESS"]

    def depth(v):                                           # liquid depth (mm) for a volume (mm3)
        lo, hi = 0.0, 2 * r
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if horizontal_volume(mid, r, length) < v else (lo, mid)
        return (lo + hi) / 2

    v, t, dt = horizontal_volume(2 * r, r, length), 0.0, 1.0
    h_edge = h_bung - 25.0                                  # lowest edge of the 50 mm opening
    v_end = horizontal_volume(h_edge + 5, r, length)
    while v > v_end:
        head = max(depth(v) - h_bung, 1.0) / 1000.0
        v -= cd * a_b * math.sqrt(2 * G * head) * dt * 1e9
        t += dt
    slope = (P["DS_TOP_HI"] - P["DS_TOP_LO"]) / (2 * P["DS_SADDLE_X"])
    left, x = 0.0, 0.0
    while h_edge - x * slope > 0 and x < length:            # wedge of water below the opening, stand sloping 2.9 deg
        left += horizontal_volume(h_edge - x * slope, r, 1.0)
        x += 1.0
    say("B4", "Drain time through the 2 in bung at the bottom of the low head, full to nearly empty", round(t / 60, 1), "min")
    say("B5", "Water left below the bung opening, stand sloping 2.9 deg", round(left * 1e-6, 1), "L")
    # saddle check: four chocks, contact 31.5 deg off vertical
    ro = P["DRUM_R_IN"] + P["DRUM_T"]
    alpha = math.asin(P["DS_CHOCK_Y"] / ro)
    w = full_m * G
    n_v = w / 4
    n = n_v / math.cos(alpha)
    span = 480.0
    a = span / 2 - P["DS_CHOCK_Y"]
    mom = n_v * a + n * math.sin(alpha) * 0.0               # horizontal parts balance across each saddle
    z_rhs = (40 ** 4 - 34 ** 4) / (6 * 40)
    say("B6", "Contact angle of the drum on the chocks, from vertical", round(math.degrees(alpha), 1), "deg")
    say("B7", "Normal force on each chock, full drum", round(n), "N")
    say("B8", "Bending stress in a saddle (40 x 40 x 3 RHS), full drum", round(mom / z_rhs, 1), "MPa")
    leg_a = (40 * 40 - 34 * 34)
    say("B9", "Compressive stress in a drain stand leg, full drum", round(w / 4 / leg_a, 1), "MPa")
    return dict(vol_l=vol_l, full_m=full_m, fill=vol_l / fill_rate, drain=t / 60)


# ------------------------------------------------------------------ shear by a wheel or a pair of discs
def disc_shear(t, r, overlap):
    """Rotary shear force (N) and nip angle (rad) for sheet t (mm) between discs of radius r with the given overlap."""
    th = math.acos((r - (t + overlap) / 2) / r)
    f = TAU * t * t / (2 * math.tan(th))
    return f, th


def wheel_shear(t, r, extra=0.3):
    """Single cutter wheel against a fixed edge (the chime's countersink wall)."""
    th = math.acos((r - (t + extra)) / r)
    f = TAU * t * t / (2 * math.tan(th))
    return f, th


# ------------------------------------------------------------------ C. end cutter
def end_cutter():
    rows = []
    for t in (1.0, 1.2, 1.5):
        f, th = wheel_shear(t, P["CUTTER_R"])
        feed = f * math.tan(th / 2)
        torque = feed * P["DRIVE_R"] / 1000 * 1.3          # 30 % for the guide roller and drum rollers
        crank = torque / (P["EC_CRANK_R"] / 1000)
        rows.append((t, f, feed, torque, crank))
    for t, f, feed, torque, crank in rows:
        say(f"C{int(t * 10)}", f"End cutter, head {t:.1f} mm: cut force {f:.0f} N, feed {feed:.0f} N, "
            f"drive torque {torque:.1f} N m, crank force", round(crank), "N")
    mu = 0.3                                               # knurled wheel on the painted chime
    grip = rows[-1][2] / mu
    say("C20", "Pinch needed between drive wheel and guide roller for 1.5 mm heads (knurl, friction 0.3)", round(grip), "N")
    perim = 2 * math.pi * P["CUT_LINE_R"]
    turns = perim / (2 * math.pi * P["DRIVE_R"])
    say("C21", "Crank turns to go once round a head", round(turns, 1))
    say("C22", "Cutting time per head at 30 crank turns a minute", round(turns / 30, 2), "min")
    return dict(crank=max(r_[4] for r_ in rows), turns=turns)


# ------------------------------------------------------------------ D. rotary shear head
def shear_head():
    R, ov = P["DISC_R"], P["DISC_OVERLAP"]
    rows = []
    for t in (0.8, 1.0, 1.2, 1.5):
        f, th = disc_shear(t, R, ov)
        spread = 100.0 * (t / 1.2) ** 3                     # pushing the cut edges round the 10 mm web (estimate)
        trolley = 10.0
        feed = f * math.tan(th / 2) + spread + trolley
        torque = feed * R / 1000 * 1.2                      # 20 % for the bearings and the idle disc
        crank = torque / (P["CRANK_R"] / 1000)
        traction = 0.3 * f                                  # the driven disc's edge bites; effective friction 0.3
        rows.append((t, f, th, feed, torque, crank, traction))
        say(f"D{int(t * 10)}", f"Shear head, wall {t:.1f} mm: separating force {f:.0f} N, nip angle "
            f"{math.degrees(th):.1f} deg, feed resistance {feed:.0f} N, crank force", round(crank), "N")
        say(f"D{int(t * 10)}t", f"Shear head, wall {t:.1f} mm: traction of the driven disc over resistance",
            round(traction / feed, 2))
    f15 = rows[-1][1]
    lever = 104.0                                           # disc line to the web's centre (mm)
    z_web = 10 * 92 ** 2 / 6
    s_web = f15 * lever / z_web + f15 / (10 * 92)
    say("D20", "Stress in the 10 mm web at 1.5 mm wall", round(s_web, 1), "MPa")
    m_sh = f15 * (14 + P["DISC_T"] / 2)
    s_sh = 32 * m_sh / (math.pi * (2 * P["SHAFT_R"]) ** 3)
    say("D21", "Bending stress in a 25 mm head shaft at 1.5 mm wall", round(s_sh, 1), "MPa")
    lin = math.pi * 2 * R / 1000 * 30
    say("D22", "Cutting speed at 30 crank turns a minute", round(lin, 1), "m/min")
    # beam carrying the trolley, drop bar and head
    head_m = 0.0
    for c in m.components():
        if c.bom in (9, 10):
            head_m += c.shape.volume * 1e-9 * m.STEEL
    w = head_m * G
    span = 2 * P["POST_X"]
    I = (40 * 80 ** 3 - 34 * 74 ** 3) / 12
    say("D23", "Mass of the trolley, drop bar and shear head", round(head_m, 1), "kg")
    say("D24", "Rail beam deflection with the head at mid-span", round(w * span ** 3 / (48 * E * I), 2), "mm")
    return dict(crank=max(r_[5] for r_ in rows), speed=lin, head_m=head_m)


# ------------------------------------------------------------------ E. slip roll: reverse bending to flat
def moment_ratio(x):
    """M / M_e for an elastic-perfectly plastic rectangle at curvature x = kappa / kappa_e."""
    return x if x <= 1 else 1.5 * (1 - 1 / (3 * x * x))


def solve_flat(k0, ke):
    """Loaded curvature change x (in units of ke) whose springback leaves the sheet flat: x - M/M_e = k0/ke."""
    target = k0 / ke
    lo, hi = 1.0, 50.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if mid - moment_ratio(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def bend_height(rho, t):
    """Bending roll centre above the lower roll centre for a loaded radius rho (mm), pinch geometry of model.py."""
    r, yr = P["ROLL_R"], P["BEND_Y"]
    zn = r + t / 2
    return zn + rho - math.sqrt((rho + t / 2 + r) ** 2 - yr ** 2)


def residual(dk, sy, t, k0):
    ke = 2 * sy / (E * t)
    x = dk / ke
    return k0 - (dk - moment_ratio(x) * ke)


def feed_work(dk, me, ke, ei):
    """Plastic work per mm of sheet (N): bending from k0 by dk and springing back."""
    if dk <= ke:
        return 0.0
    w_load = me * ke / 2 + 1.5 * me * ((dk - ke) + ke * ke / 3 * (1 / dk - 1 / ke))
    mm_ = moment_ratio(dk / ke) * me
    return w_load - mm_ ** 2 / (2 * ei)


def slip_roll(d):
    r_mid = P["DRUM_R_IN"] + P["DRUM_T"] / 2
    k0 = 1 / r_mid
    b = sum(d["widths"])                                    # three panels fed side by side
    yr = P["BEND_Y"]
    res = {}
    say("E1", "Drum curvature to take out (radius)", round(r_mid, 1), "mm")
    say("E2", "Width fed at once (three panels side by side)", round(b), "mm")
    table = []
    for sy in (SY_LO, SY_NOM, SY_HI):
        for t in (T_LO, T_NOM, T_HI):
            ke = 2 * sy / (E * t)
            x = solve_flat(k0, ke)
            dk = x * ke
            rho = 1 / (dk - k0)
            zb = bend_height(rho, t)
            me = sy * b * t * t / 6
            mo = moment_ratio(x) * me
            fb = mo / yr
            ei = E * b * t ** 3 / 12
            fw = feed_work(dk, me, ke, ei)
            table.append((sy, t, x, rho, zb, mo, fb, fw))
    for sy, t, x, rho, zb, mo, fb, fw in table:
        tag = f"E{int(sy)}-{int(t * 10)}"
        say(tag, f"Yield {sy:.0f} MPa, {t:.1f} mm: bent to reverse radius {rho:.0f} mm, bending roll {zb:.1f} mm above "
            f"the lower roll, moment {mo / 1000:.1f} N m, bending roll force {fb:.0f} N, feed resistance", round(fw), "N")
    nom = [r_ for r_ in table if r_[0] == SY_NOM and r_[1] == T_NOM][0]
    worst = max(table, key=lambda r_: r_[6])
    res["setting"] = nom[4]
    res["rho"] = nom[3]
    say("E10", "Nominal setting (250 MPa, 1.0 mm): bending roll above the lower roll", round(nom[4], 1), "mm")
    say("E11", "Range of settings over 200 to 300 MPa and 0.8 to 1.2 mm",
        f"{min(r_[4] for r_ in table):.1f} to {max(r_[4] for r_ in table):.1f}", "mm")
    # sensitivity: one setting, other material
    dk_nom = k0 + 1 / nom[3]
    worst_sag = 0.0
    for sy in (SY_LO, SY_HI):
        for t in (T_LO, T_HI):
            kr = residual(dk_nom, sy, t, k0)
            sag = abs(kr) * 1000 ** 2 / 8
            worst_sag = max(worst_sag, sag)
    say("E12", "Worst sag over 1 m if the nominal setting is used on other drum steel (no trial pass)", round(worst_sag), "mm")
    # setting precision for R5: 10 mm over 1 m
    k_allow = 8 * 10 / 1000 ** 2
    ke = 2 * SY_NOM / (E * T_NOM)
    x = dk_nom / ke
    h = 1e-6
    dres = (residual(dk_nom + h, SY_NOM, T_NOM, k0) - residual(dk_nom - h, SY_NOM, T_NOM, k0)) / (2 * h)
    dk_allow = k_allow / abs(dres)
    rho1 = 1 / (dk_nom - k0)
    rho2 = 1 / (dk_nom + dk_allow - k0)
    dz = abs(bend_height(rho2, T_NOM) - bend_height(rho1, T_NOM))
    say("E13", "Allowed error in the bending roll height to stay within 10 mm over 1 m", round(dz, 2), "mm")
    turn = dz / 2.5 * 360
    say("E14", "That is this much of a turn of the M20 x 2.5 bending screw", round(turn), "deg")
    res["dz"] = dz
    crown = (P["HOOP_R"] - r_mid) * dk_nom
    say("E29", "Strain at a rolling hoop's crown if the hoop were rolled flat with the panel (why the hoops are cut out)",
        round(100 * crown, 1), "%")
    # ends that the slip roll cannot bend
    lead = yr
    end_dev = lead ** 2 / (2 * r_mid)
    say("E15", "Leading end left unbent (pinch to bending roll)", round(lead), "mm")
    say("E16", "Rise of that unbent end above flat", round(end_dev, 1), "mm")
    # forces, traction and crank
    fb_w, fw_w = worst[6], max(r_[7] for r_ in table)
    mu = 0.15
    np_ = 1.5 * fw_w / (2 * mu)
    say("E17", "Worst bending roll force", round(fb_w), "N")
    say("E18", "Worst feed resistance (plastic work per mm)", round(fw_w), "N")
    say("E19", "Pinch force needed for traction (both pinch rolls driven by the gears, friction 0.15, margin 1.5)",
        round(np_), "N")
    pinch = 2000.0
    say("E20", "Pinch force set with the two M16 screws (1 kN each)", round(pinch), "N")
    t_screw = 0.2 * 1000 * 16 / 1000
    say("E21", "M16 screw torque for 1 kN; force on the 90 mm handwheel rim", f"{t_screw:.1f} N m; {t_screw / 0.045:.0f}", "N")
    jr = P["JOURNAL_R"] / 1000
    rr = P["ROLL_R"] / 1000
    bush_mu = 0.10
    t_roll = fw_w * rr + bush_mu * (pinch + fb_w) * jr * 2 + bush_mu * fb_w * jr
    ratio = 39 / 13
    t_crank = t_roll / ratio / 0.95
    f_crank = t_crank / (P["RS_CRANK_R"] / 1000)
    say("E22", "Torque to turn the pinch rolls (worst)", round(t_roll, 1), "N m")
    say("E23", "Crank force at 300 mm through the 3:1 chain", round(f_crank), "N")
    v = 30 / ratio * 2 * math.pi * rr
    say("E24", "Feed speed at 30 crank turns a minute", round(v, 2), "m/min")
    # roll stress and deflection (upper pinch roll carries pinch and bending reaction)
    span = 2 * (P["SIDE_X"] + P["SIDE_T"] / 2)
    w_up = pinch + fb_w
    I = math.pi * (2 * P["ROLL_R"]) ** 4 / 64
    defl = 5 * (w_up / P["ROLL_FACE"]) * span ** 4 / (384 * E * I)
    mom = w_up * span / 8
    s_roll = 32 * mom / (math.pi * (2 * P["ROLL_R"]) ** 3)
    say("E25", "Upper pinch roll: load, mid-span deflection", f"{w_up:.0f} N; {defl:.2f}", "mm")
    say("E26", "Upper pinch roll bending stress", round(s_roll, 1), "MPa")
    bush_p = (w_up / 2) / (2 * P["JOURNAL_R"] * 20)
    say("E27", "Bronze bush bearing pressure (30 x 20 mm)", round(bush_p, 1), "MPa")
    gear_ft = (t_roll / 2) / 0.030
    lewis = gear_ft / (20 * 3 * 0.32)
    say("E28", "Pinch gear tooth stress (Lewis, module 3, 20 mm face)", round(lewis), "MPa")
    res.update(crank=f_crank, speed=v, end_dev=end_dev, worst_sag=worst_sag, fb=fb_w, fw=fw_w)
    return res


# ------------------------------------------------------------------ F. cradle
def cradle(d):
    alpha = math.radians(L["contact_deg"])
    w_design = 1000.0                                       # drum plus a person leaning on it (N)
    n_shaft = w_design / (2 * math.cos(alpha))
    p_roll = n_shaft / 2
    a = P["PB_X"] - P["HOOP_X"]
    span = 2 * P["PB_X"]
    I = math.pi * (2 * P["SHAFT_R"]) ** 4 / 64
    mom = p_roll * a
    s = 32 * mom / (math.pi * (2 * P["SHAFT_R"]) ** 3)
    defl = p_roll * a * (3 * span ** 2 - 4 * a ** 2) / (24 * E * I)
    say("F1", "Drum axis height; top of the drum", f"{L['z_ax']:.0f}; {L['drum_top']:.0f}", "mm")
    say("F2", "Roller contact on the hoops, from vertical", round(L["contact_deg"], 1), "deg")
    say("F3", "Roller shaft at 1 kN on the drum: stress, deflection", f"{s:.0f} MPa; {defl:.1f}", "mm")
    w = d["drum_m"] * G
    say("F4", "Side push that rolls an empty drum over a roller", round(w * math.tan(alpha)), "N")


# ------------------------------------------------------------------ G. guards (ISO 13857 Table 4, slots)
def guards():
    # (opening, slot width e, distance from the opening to the danger point)
    rows = [
        ("Slip roll in-feed slot under the nip guard", P["GUARD_GAP"], 50.0 - 5.0),
        ("Slip roll out-feed slot", P["GUARD_GAP"], 150.0 - (P["BEND_Y"] - 25.0)),
        ("Shear head front skirt over the sheet", P["GUARD_GAP"] - P["DRUM_T"] / 2, 52.0),
    ]
    need = lambda e: 2 if e <= 4 else 10 if e <= 6 else 20 if e <= 8 else 80 if e <= 10 else 100 if e <= 12 else 120  # noqa: E731
    for i, (name, e, sr) in enumerate(rows, 1):
        ok = sr >= need(e)
        say(f"G{i}", f"{name}: slot {e:.1f} mm, distance to the nip {sr:.0f} mm, needed {need(e)} mm",
            "meets" if ok else "DOES NOT MEET")


# ------------------------------------------------------------------ H. throughput and labour
def throughput(c, d, sr, sh, pg):
    # minutes of work per drum, by station; elapsed waits (filling, draining) overlap other work
    purge_lab = 2 + 3 + 2 + 3 + 1          # load on stand, open bungs and start fill, rock, drain and tip, close
    check = 3
    cut = dict(load=2, heads=2 * (1.5 + c["turns"] / 30), notches=8, slit=2 + 0.9 / (sh["speed"] / 3),
               rings=6 * (1.5 + d["circ"] / 1000 / (sh["speed"] / 3)), unload=1.5)
    roll = dict(set_trial=3, passes=3 * d["circ"] / 1000 / sr["speed"], handling=3, ends=6 * 0.5,
                deburr=(2 * 3 * (d["circ"] + 235) / 1000 + 2 * math.pi * d["head_d"] / 1000) / 3)
    cut_t, roll_t = sum(cut.values()), sum(roll.values())
    total = purge_lab + check + cut_t + roll_t
    say("H1", "Purge and vapour check, hands-on minutes per drum", purge_lab + check)
    say("H2", "Cutting cradle minutes per drum", round(cut_t, 1))
    say("H3", "Slip roll and finishing minutes per drum", round(roll_t, 1))
    say("H4", "Total hands-on minutes per drum", round(total, 1))
    rate = 2 * 60 / total
    say("H5", "Drums per hour for two people, work shared evenly", round(rate, 1))
    say("H6", "Elapsed purge time per drum (fill, soak 10 min, drain), done while the cradle works",
        round(L["sheet_l"] * 0 + 10.4 + 10 + 2.5, 1), "min")
    say("H7", "Heads off a drum, both ends, one person (R3)", round(cut["heads"], 1), "min")
    return dict(rate=rate, heads=cut["heads"], total=total)


# ------------------------------------------------------------------ I. masses and J. cost
def masses():
    dens = {"tables": m.PLY, "ds_chocks": 700.0, "tray": 950.0, "rs_bushes": m.BRONZE}
    st = {"purge": 0.0, "cut": 0.0, "roll": 0.0}
    kg = {}
    for c in m.components():
        if c.group == "context":
            continue
        kg[c.key] = c.shape.volume * 1e-9 * dens.get(c.key, m.STEEL)
        st[c.group] += kg[c.key]
    say("I1", "Drain and purge stand with tray", round(st["purge"]), "kg")
    say("I2", "Cutting cradle with posts, beam, shear head and end cutter", round(st["cut"]), "kg")
    say("I3", "Slip roll stand with tables", round(st["roll"]), "kg")
    lifts = [
        ("Side frame with its legs and bridge, each", kg["rs_sides"] / 2),
        ("Cradle frame, one welded piece", kg["frame"]),
        ("Shear head with its shafts, discs, guard and drop bar", sum(kg[k] for k in ("head_frame", "discs", "head_shafts",
                                                                                     "head_guard", "drop"))),
        ("Lower pinch roll", kg["roll_lower"]),
        ("Table frame, each", kg["table_frames"] / 2),
        ("Roller shaft with its two rollers, each", (kg["shafts"] + kg["rollers"]) / 2),
    ]
    lifts.sort(key=lambda x: -x[1])
    for i, (name, w) in enumerate(lifts, 1):
        say(f"I{3 + i}", f"Lift {i}: {name}", round(w, 1), "kg")
    return st, lifts


def cost():
    rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
    total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
    target = float(re.search(r"^budget_usd:\s*([\d.]+)", (ROOT / "project.yaml").read_text(), re.M).group(1))
    say("J1", "Estimated cost of the constructable design (bom/bom.csv)", f"{total:,.0f}", "USD")
    say("J2", "Value-engineering target (project.yaml)", f"{target:,.0f}", "USD")
    say("J3", "Under (-) or over (+) the target", f"{total - target:+,.0f}", "USD")
    top = sorted(rows, key=lambda r: -float(r["qty"]) * float(r["unit_cost_usd"]))[:4]
    for i, r in enumerate(top, 1):
        say(f"J{3 + i}", f"Cost driver {i}: {r['item']}", f"{float(r['qty']) * float(r['unit_cost_usd']):,.0f}", "USD")
    return total, target


if __name__ == "__main__":
    d = drum_yield()
    pg = purge(d)
    c = end_cutter()
    sh = shear_head()
    sr = slip_roll(d)
    cradle(d)
    guards()
    th = throughput(c, d, sr, sh, pg)
    masses()
    cost()
    with (ROOT / "docs" / "04-calcs" / "results.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tag", "quantity", "value", "unit"])
        for row in OUT:
            w.writerow(row)
    print("wrote docs/04-calcs/results.csv")
