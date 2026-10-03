"""DrumPanel parametric model (build123d), TRL 3, constructable design (DMP-DDR-002).

Run from the repo root:
    python cad/src/model.py            exports cad/step/*.step and cad/stl/*.stl
    python cad/src/model.py --check    fit checks: no two parts overlap, every joint face touches

The bench set has three stations, laid out as in a workshop:

    Drain and purge stand   at y = -1,500   a sloped stand that holds a drum, bung end low, over a tray
    Cutting cradle          at y = 0        rollers under the rolling hoops, a screw brake, an end cutter
                                            on the chime, and a hand-cranked rotary shear head that runs
                                            on an overhead rail (seam slit) or swivels 90 degrees (chime ring cuts)
    Slip roll stand         at y = +1,950   a hand-cranked pinch pair geared 1:1 and an adjustable bending
                                            roll that reverse-bends the opened drum body flat

Axes: X along the drum axis and the roll axes, Y across the workshop (drain stand at -Y, roll stand
at +Y, the operator at the slip roll in-feed stands on the -Y side of it), Z up from the floor.
Units mm. The cradle drum is shown with its heads on, the end cutter clamped on the +X chime and the
shear head parked at the -X end, ready to start. The slip roll holds a drum body being fed in.

components() returns every made or bought component on its own (build plan, checks);
build_parts() groups them by BOM line (concept media, drawing, masses). Context items (drums,
the sheet) carry no BOM line. Sizing is in DMP-CAL-001 (docs/04-calcs/sizing.py), which reads
PARAMS and levels() from here. CONCEPT, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
from pathlib import Path

# ---------------------------------------------------------------------------
# Parameters (mm). Edit these, not the geometry below.
# ---------------------------------------------------------------------------
PARAMS = {
    # 55 US gallon (208 L) tight-head steel drum, as received (DMP-CAL-001, section 2)
    "DRUM_R_IN": 286.0,      # body inside radius (572 mm inside diameter)
    "DRUM_T": 1.0,           # body wall (0.8 to 1.5 mm seen; 1.0 nominal, 1.2 for forces)
    "HEAD_T": 1.2,           # head thickness
    "DRUM_L": 880.0,         # overall length over the chimes
    "HOOP_R": 298.5,         # rolling hoop outside radius
    "HOOP_W": 30.0,          # hoop width
    "HOOP_X": 147.0,         # hoops at +/- this from the drum middle
    "CHIME_R_IN": 280.0,     # chime (rolled seam) inside radius; the head is cut just inside it
    "CHIME_L": 15.0,         # chime length at each end
    "HEAD_RECESS": 10.0,     # head outer face below the drum end
    "RING_CUT": 30.0,        # chime ring cut this far in from each end
    "HOOP_CUT": 30.0,        # hoop strips cut out: cuts this far each side of each hoop centre (DMP-DDR-002, P7)
    # Cutting cradle
    "ROLLER_R": 50.8,        # 101.6 mm tube rollers
    "ROLLER_W": 100.0,
    "ROLLER_Y": 190.0,       # roller shafts at +/- this
    "ROLLER_Z": 310.0,       # roller shaft height
    "SHAFT_R": 12.5,         # 25 mm bright steel shafts
    "PB_X": 520.0,           # pillow blocks at +/- this
    "PB_H": 36.5,            # UCP205 shaft centre height
    "FRAME_RHS": 50.0, "FRAME_T": 3.0,
    "FRAME_X": 775.0,        # frame ends at +/- this
    "FRAME_Y": 350.0,        # side rails' outer faces at +/- this
    "POST_X": 712.5,         # rail posts at +/- this
    "POST_RHS": 60.0, "POST_T": 4.0,
    "BEAM_Z0": 1220.0, "BEAM_H": 80.0, "BEAM_W": 40.0, "BEAM_T": 3.0, "BEAM_X": 770.0,
    # Rotary shear head (DMP-DDR-002, P4)
    "DISC_R": 50.5,          # 101 mm slitting discs, 10 mm thick, D2 hardened
    "DISC_T": 10.0,
    "DISC_OVERLAP": 1.0,     # discs overlap 1.0 mm at the nip (adjustable by the eccentric)
    "HEAD_PARK_X": -520.0,   # nip position when parked at the -X end
    "CRANK_R": 155.0,        # shear head crank radius, on the raised crank shaft of the drive case (DMP-DDR-003, Q3)
    # Shear head drive case (DMP-DDR-003, Q3): crank shaft -> 12 T to 28 T (#35) -> jackshaft -> 15 T to 15 T -> upper shaft
    "JACK_Z": 130.0,         # jackshaft above the nip (head local)
    "KCRANK_X": -60.0, "KCRANK_Z": 170.0,   # crank shaft position (head local)
    "SPR_A_R": 22.9,         # 15 T #35 on the upper shaft and on the jackshaft (pitch radius)
    "SPR_C_R": 42.5,         # 28 T #35 on the jackshaft
    "SPR_D_R": 18.4,         # 12 T #35 on the crank shaft
    # Ring head (DMP-DDR-003, Q2): a second shear head bolted 233 mm along the drum for two ring cuts a pass
    "RING_PITCH": 233.0,
    # Notches on the slit line, made with the lever notching punch (DMP-DDR-003, Q1)
    "CHIME_NOTCH_W": 60.0, "CHIME_NOTCH_L": 35.0,   # open-ended notch at each drum end
    "HOOP_NOTCH_W": 40.0, "HOOP_NOTCH_L": 32.0,     # slot through each hoop
    "PUNCH_HOOP_X": 338.0,   # hoop station of the punch from its back face (45 mm stand-off + 293 mm)
    # End cutter (DMP-DDR-002, P3)
    "CUTTER_R": 25.0, "CUTTER_T": 6.0, "CUT_LINE_R": 276.0, "CUTTER_PHI": -12.0,
    "DRIVE_R": 20.0, "GUIDE_R": 15.0, "EC_CRANK_R": 150.0,
    # Drain and purge stand
    "DS_Y": -1500.0, "DS_SADDLE_X": 250.0, "DS_CHOCK_Y": 150.0, "DS_TOP_HI": 410.0, "DS_TOP_LO": 385.0,
    # Slip roll stand (DMP-DDR-002, P6)
    "RS_Y": 1950.0,
    "ROLL_R": 30.0,          # 60 mm rolls
    "ROLL_FACE": 900.0,      # roll face length
    "JOURNAL_R": 15.0,       # 30 mm journals in bronze bushes
    "LOWER_Z": 870.0,        # lower pinch roll centre; its top (the sheet line) is at 900
    "SHEET_T": 1.0,
    "BEND_Y": 90.0,          # bending roll behind the pinch line
    "BEND_SET": 13.4,        # bending roll above the lower roll, nominal setting (DMP-CAL-001, section 6)
    "BEND_PITCH": 1.5,       # fine-pitch bending screws M20 x 1.5 (DMP-DDR-003, Q4)
    "DIAL_DIV": 60,          # dial divisions per turn: 0.025 mm each
    "SIDE_X": 460.0, "SIDE_T": 20.0, "SIDE_Y0": -150.0, "SIDE_Y1": 220.0, "SIDE_Z0": 760.0, "SIDE_Z1": 1010.0,
    "CRANK_Y": -230.0, "CRANK_Z": 820.0, "RS_CRANK_R": 300.0,
    "SPROCKET_BIG_R": 79.0,  # 39 tooth #40 chain sprocket, pitch radius
    "SPROCKET_SMALL_R": 26.5,  # 13 tooth
    "GEAR_R": 30.0,          # module 3, 20 teeth, pitch radius
    "TABLE_TOP": 900.0, "OUT_TABLE_TOP": 913.0,
    "GUARD_GAP": 8.0,        # in-feed slot under the nip guard
}

STEEL, BRONZE, PLY = 7850.0, 8800.0, 600.0   # kg/m3


def levels(P=PARAMS):
    """Heights and positions that the drawing, the calculations and the pictures share."""
    zr = P["ROLLER_Z"]
    z_ax = zr + math.sqrt((P["HOOP_R"] + P["ROLLER_R"]) ** 2 - P["ROLLER_Y"] ** 2)
    r_mid = P["DRUM_R_IN"] + P["DRUM_T"] / 2
    L = {
        "z_ax": z_ax,                                  # cradle drum axis
        "z_nip": z_ax + r_mid,                          # top of the drum wall, mid-thickness
        "frame_top": zr - P["PB_H"],
        "drum_top": z_ax + P["DRUM_R_IN"] + P["DRUM_T"],
        "contact_deg": math.degrees(math.atan2(P["ROLLER_Y"], z_ax - zr)),
        "upper_z": P["LOWER_Z"] + 2 * P["ROLL_R"] + P["SHEET_T"],
        "bend_z": P["LOWER_Z"] + P["BEND_SET"],
        "sheet_w": P["DRUM_L"] - 2 * P["RING_CUT"],
        "panels": panel_ranges(P),
        "sheet_l": 2 * math.pi * r_mid,
        "head_d": 2 * P["CUT_LINE_R"],
    }
    return L


def panel_ranges(P=PARAMS):
    """The three flat panels across the drum body, as (x0, x1) along the drum axis, after the chime ring cuts
    and the hoop strip cuts (DMP-DDR-002, P7)."""
    e = P["DRUM_L"] / 2 - P["RING_CUT"]
    hi, ho = P["HOOP_X"] - P["HOOP_CUT"], P["HOOP_X"] + P["HOOP_CUT"]
    return [(-e, -ho), (-hi, hi), (ho, e)]


def ring_cut_lines(P=PARAMS):
    """The six circumferential cuts along the drum axis: two chime rings and both sides of both hoops."""
    e = P["DRUM_L"] / 2 - P["RING_CUT"]
    hi, ho = P["HOOP_X"] - P["HOOP_CUT"], P["HOOP_X"] + P["HOOP_CUT"]
    return [-e, -ho, -hi, hi, ho, e]


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------
def _b():
    import build123d as bd
    return bd


def box(x0, x1, y0, y1, z0, z1):
    bd = _b()
    return bd.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * bd.Box(x1 - x0, y1 - y0, z1 - z0)


def cylx(r, x0, x1, y, z):
    bd = _b()
    return bd.Pos((x0 + x1) / 2, y, z) * bd.Rot(0, 90, 0) * bd.Cylinder(r, x1 - x0)


def cyly(r, y0, y1, x, z):
    bd = _b()
    return bd.Pos(x, (y0 + y1) / 2, z) * bd.Rot(90, 0, 0) * bd.Cylinder(r, y1 - y0)


def cylz(r, z0, z1, x, y):
    bd = _b()
    return bd.Pos(x, y, (z0 + z1) / 2) * bd.Cylinder(r, z1 - z0)


def ringx(ri, ro, x0, x1, y, z):
    return cylx(ro, x0, x1, y, z) - cylx(ri, x0 - 1, x1 + 1, y, z)


def ringy(ri, ro, y0, y1, x, z):
    return cyly(ro, y0, y1, x, z) - cyly(ri, y0 - 1, y1 + 1, x, z)


def rhs(axis, a0, a1, b0, b1, c0, c1, t):
    """Hollow rectangular section along axis 'x', 'y' or 'z'. (a0, a1) is the length; (b0, b1) and (c0, c1)
    are the other two ranges in x, y, z order with the length axis removed."""
    if axis == "x":
        return box(a0, a1, b0, b1, c0, c1) - box(a0 - 1, a1 + 1, b0 + t, b1 - t, c0 + t, c1 - t)
    if axis == "y":
        return box(b0, b1, a0, a1, c0, c1) - box(b0 + t, b1 - t, a0 - 1, a1 + 1, c0 + t, c1 - t)
    return box(b0, b1, c0, c1, a0, a1) - box(b0 + t, b1 - t, c0 + t, c1 - t, a0 - 1, a1 + 1)


def comp(shapes):
    bd = _b()
    return bd.Compound(list(shapes))


def fuse(shapes):
    s = shapes[0]
    for x in shapes[1:]:
        s = s + x
    return s


def polar(phi_deg, r, x, z_ax, y0=0.0):
    """Point on a circle about the cradle drum axis: phi from +Z toward +Y."""
    a = math.radians(phi_deg)
    return (x, y0 + r * math.sin(a), z_ax + r * math.cos(a))


# ---------------------------------------------------------------------------
# The drum (context) and the sheet (context)
# ---------------------------------------------------------------------------
def drum(P=PARAMS, heads=True, bung_phi=0.0):
    """A 208 L drum lying along X, centred on the origin. Body, two rolling hoops, two chimes, two heads
    recessed 10 mm, two bung bosses on the +X head (one at the top, one at the bottom)."""
    ri, t, half = P["DRUM_R_IN"], P["DRUM_T"], P["DRUM_L"] / 2
    ro = ri + t
    parts = [ringx(ri, ro, -half + P["CHIME_L"], half - P["CHIME_L"], 0, 0)]
    for s in (-1, 1):
        xh = s * P["HOOP_X"]
        parts.append(ringx(ro - 0.01, P["HOOP_R"], xh - P["HOOP_W"] / 2, xh + P["HOOP_W"] / 2, 0, 0))
        x0, x1 = sorted((s * (half - P["CHIME_L"]), s * half))
        parts.append(ringx(P["CHIME_R_IN"], P["HOOP_R"], x0, x1, 0, 0))
    if heads:
        for s in (-1, 1):
            xo = s * (half - P["HEAD_RECESS"])
            x0, x1 = sorted((xo, xo - s * P["HEAD_T"]))
            parts.append(cylx(P["CHIME_R_IN"], x0, x1, 0, 0))
            # web joining the head to the chime (the countersink seam), so the drum is one closed vessel
            parts.append(ringx(P["CHIME_R_IN"] - 0.01, ri + 0.5, x0, x1, 0, 0))
        xo = half - P["HEAD_RECESS"]
        a = math.radians(bung_phi)
        parts.append(cylx(32, xo, xo + 6, -230 * math.sin(a), -230 * math.cos(a)))   # 2 in bung boss
        parts.append(cylx(20, xo, xo + 6, 230 * math.sin(a), 230 * math.cos(a)))     # 3/4 in bung boss
    return fuse(parts)


def curled_sheet(P=PARAMS):
    """The three panels of an opened drum body as they are fed side by side: a flat lead on the in-feed table
    into the pinch, and the rest still curled in a near-tube lying on the table (paint side up).
    Local: X across, Y feed, sheet bottom z = 0. Orientation: the cylinder sector starts at local +X and runs
    counter-clockwise; after Rot(0, 90, 0) a local angle a points at theta = a - 90 (theta from +Y toward +Z), so
    Rot(100, 0, 0) makes the curl run from theta 10 deg round through +Z and -Y to -90 deg, where it meets the
    flat lead on the table."""
    bd = _b()
    L = levels(P)
    t, r = P["SHEET_T"], P["DRUM_R_IN"] + P["DRUM_T"] / 2
    flat_len = 500.0
    curl_len = L["sheet_l"] - flat_len
    arc = math.degrees(curl_len / r)
    out = []
    for x0, x1 in L["panels"]:
        w = x1 - x0
        flat = box(x0, x1, -flat_len, 0, 0, t)
        cyl_o = bd.Cylinder(r + t / 2, w, arc_size=arc, align=(bd.Align.NONE, bd.Align.NONE, bd.Align.CENTER))
        cyl_i = bd.Cylinder(r - t / 2, w + 2)
        shell = cyl_o - cyl_i
        shell = bd.Rot(0, 90, 0) * shell        # axis to X
        shell = bd.Rot(100, 0, 0) * shell
        shell = bd.Pos((x0 + x1) / 2, -flat_len, r + t / 2) * shell
        out.append(flat + shell)
    return comp(out)




# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------
class C:
    """One component: key, display name, shape, colour, BOM line, how it is made, station, explode offset."""
    def __init__(self, key, name, shape, color, bom, how, group, explode=(0, 0, 0)):
        self.key, self.name, self.shape, self.color = key, name, shape, color
        self.bom, self.how, self.group, self.explode = bom, how, group, explode


def shear_head_local(P=PARAMS):
    """Rotary shear head in its own frame: nip at the origin, cut plane y = 0, cutting direction +X,
    disc axes along Y, outer (driven) disc above. Returns {key: shape}.
    The crank is on a raised crank shaft in a drive case on the +Y side (DMP-DDR-003, Q3): crank shaft, 12 T to
    28 T #35 chain to a jackshaft, 15 T to 15 T chain down to the upper shaft (2.33 to 1), so the crank sweeps
    clear of the drum in both slit and ring modes. The upper shaft has a stub on the -Y side for the coupling
    shaft to the ring head."""
    R, T, ov = P["DISC_R"], P["DISC_T"], P["DISC_OVERLAP"]
    zc = R - ov / 2                                   # disc centres at +/- this
    s = {}
    s["disc_u"] = ringy(P["SHAFT_R"], R, 0, T, 0, zc)
    s["disc_l"] = ringy(P["SHAFT_R"], R, -T, 0, 0, -zc)
    s["shaft_u"] = cyly(P["SHAFT_R"], -24, 96, 0, zc)
    s["shaft_l"] = cyly(P["SHAFT_R"], -74, 0, 0, -zc)
    hole_u = cyly(P["SHAFT_R"], -200, 200, 0, zc)
    hole_l = cyly(P["SHAFT_R"], -200, 200, 0, -zc)
    frame = box(-150, -58, -5, 5, -116, 116)                       # web (spine) in the cut plane, trailing
    frame += box(-45, 45, 14, 74, 15, 116) - hole_u                  # upper bearing housing (eccentric bush)
    frame += box(-150, 45, -25, 74, 116, 136)                        # top plate
    frame += box(-45, 45, -74, -14, -116, -20) - hole_l              # lower bearing housing (inside the drum)
    frame += box(-150, 45, -74, 5, -136, -116)                       # lower plate
    s["frame"] = frame
    g = box(-56, 62, -4, 14, zc, zc + 64) - cyly(54, -2, 11.5, 0, zc) - cyly(P["SHAFT_R"] + 0.5, -10, 20, 0, zc)
    g += box(52, 62, -4, 14, P["GUARD_GAP"], zc)          # front skirt: 8 mm slot over the sheet, 52 mm ahead of the nip
    s["guard"] = g
    # drive case: inner plate bolted to the upper housing and top plate, outer plate, 1.5 mm sheet band between
    jz, kx, kz = P["JACK_Z"], P["KCRANK_X"], P["KCRANK_Z"]
    holes = cyly(P["SHAFT_R"] + 0.5, 60, 120, 0, zc) + cyly(10, 60, 120, 0, jz) + cyly(10, 60, 120, kx, kz)
    inner = box(-90, 50, 74, 82, 18, 200) - holes
    outer = box(-90, 50, 104, 112, 18, 200) - holes
    band = box(-90, 50, 82, 104, 18, 200) - box(-88.5, 48.5, 81, 105, 19.5, 198.5)
    s["drive_case"] = inner + outer + band
    s["jack"] = cyly(10, 74, 112, 0, jz)
    s["sprockets"] = comp([ringy(P["SHAFT_R"], P["SPR_A_R"], 86, 92, 0, zc), ringy(10, P["SPR_A_R"], 86, 92, 0, jz),
                           ringy(10, P["SPR_C_R"], 94, 100, 0, jz), ringy(10, P["SPR_D_R"], 94, 100, kx, kz)])
    cr = P["CRANK_R"]
    s["crank"] = cyly(10, 74, 118, kx, kz) + box(kx - 10, kx + 10, 118, 130, kz - 10, kz + cr) \
        + cyly(12, 130, 230, kx, kz + cr - 10)
    return s


HEAD_KEYS = ("frame", "guard", "shaft_u", "shaft_l", "disc_u", "disc_l", "drive_case", "jack", "sprockets", "crank")


def ring_head_local(P=PARAMS):
    """The ring head in the main head's local frame when bolted on for ring cuts (DMP-DDR-003, Q2): a second
    shear head (same frame, discs, shafts and guard, no drive) 233 mm along the -Y side, a spacer plate on the
    two top plates and a coupling shaft from the main head's upper shaft stub to the ring head's upper shaft.
    Returns {key: shape}."""
    hl = shear_head_local(P)
    zc = P["DISC_R"] - P["DISC_OVERLAP"] / 2
    d = P["RING_PITCH"]
    o = _b().Pos(0, -d, 0)
    s = {k: o * hl[k] for k in ("frame", "guard", "disc_u", "disc_l", "shaft_l")}
    s["shaft_u"] = o * cyly(P["SHAFT_R"], -24, 74, 0, zc)
    s["coupling"] = cyly(P["SHAFT_R"], -d + 74, -24, 0, zc)
    s["sleeve"] = ringy(P["SHAFT_R"], P["SHAFT_R"] + 3, -d + 76, -26, 0, zc)      # loose guard sleeve over the coupling
    s["spacer"] = box(-145, -30, -d - 17, 20, 136, 146)
    return s


RING_KEYS = ("frame", "guard", "disc_u", "disc_l", "shaft_l", "shaft_u", "coupling", "sleeve", "spacer")


def notch_boxes(P=PARAMS, z_top=None, ends=True, hoops=True):
    """The four notches on the slit line (top of the drum, y = 0): open-ended chime notches at the two ends and a
    slot through each hoop. Boxes in drum coordinates (axis along X at z = 0 unless z_top is given)."""
    half = P["DRUM_L"] / 2
    zt = (P["DRUM_R_IN"] - 20) if z_top is None else z_top
    out = []
    cw, cl = P["CHIME_NOTCH_W"] / 2, P["CHIME_NOTCH_L"]
    hw, hl_ = P["HOOP_NOTCH_W"] / 2, P["HOOP_NOTCH_L"] / 2
    if ends:
        out += [box(-half - 1, -half + cl, -cw, cw, zt, zt + 200), box(half - cl, half + 1, -cw, cw, zt, zt + 200)]
    if hoops:
        out += [box(-P["HOOP_X"] - hl_, -P["HOOP_X"] + hl_, -hw, hw, zt, zt + 200),
                box(P["HOOP_X"] - hl_, P["HOOP_X"] + hl_, -hw, hw, zt, zt + 200)]
    return out


def notch_punch_local(P=PARAMS):
    """Lever notching punch (DMP-DDR-003, Q1) in its own frame: back face at x = 0 (the drum end rests against
    it for a chime notch), jaws along +X into the drum, die faces at z = 0, punches moving down (-Z) into the
    drum wall at the slit line (y = 0). Station 1 (x 0 to 35) cuts the open-ended chime notch; station 2 (at
    PUNCH_HOOP_X) cuts the hoop slot with the drum end against the station 1 die block (45 mm stand-off).
    Each punch is pushed by a Tr24 x 5 screw in a nut block, turned by a 500 mm ratchet lever.
    Returns {key: shape}."""
    hx = P["PUNCH_HOOP_X"]
    cl, cw = P["CHIME_NOTCH_L"], P["CHIME_NOTCH_W"] / 2
    hl_, hw = P["HOOP_NOTCH_L"] / 2, P["HOOP_NOTCH_W"] / 2
    s = {}
    die1 = box(0, cl + 0.2, -cw - 0.2, cw + 0.2, -51, 7)
    die2 = box(hx - hl_ - 0.2, hx + hl_ + 0.2, -hw - 0.2, hw + 0.2, -51, 1)
    bore1 = box(0, cl + 0.2, -cw - 0.2, cw + 0.2, 39, 101)
    bore2 = box(hx - hl_ - 0.2, hx + hl_ + 0.2, -hw - 0.2, hw + 0.2, 39, 101)
    ri, rc = P["DRUM_R_IN"], P["CHIME_R_IN"]
    frame = box(-50, 0, -38, 38, -50, 100)                                  # back
    # lower jaw (die arm), its top ground to the inside radius of the drum wall
    frame += box(0, 385, -28, 28, -50, 0) & cylx(ri, -1, 386, 0, -ri)
    # station 1 die block, ground to the inside of the chime (x 0 to 15) and of the wall beyond it (x 15 to 45)
    frame += (box(0, 45, -38, 38, -50, 0) & cylx(rc, -1, 46, 0, -rc)) + (box(15, 45, -38, 38, -50, 6) & cylx(ri, 14, 46, 0, -rc))
    frame += box(0, 385, -20, 20, 40, 100)                                   # upper jaw
    frame += box(0, 45, -38, 38, 40, 100) + box(hx - 28, hx + 28, -28, 28, 40, 100)   # punch guide bosses
    s["frame"] = frame - die1 - die2 - bore1 - bore2
    s["punches"] = comp([box(0.1, cl, -cw, cw, 25, 100), box(hx - hl_, hx + hl_, -hw, hw, 20, 100)])
    nuts, screws = [], []
    for cx in (cl / 2, hx):
        nuts.append(box(cx - 30, cx + 30, -25, 25, 100, 130) - cylz(12, 99, 131, cx, 0))
        screws.append(cylz(12, 100, 135, cx, 0) + cylz(17, 135, 150, cx, 0))
    s["nuts"] = comp(nuts)
    s["screws"] = comp(screws)
    return s


PUNCH_KEYS = ("frame", "punches", "nuts", "screws")


def punch_lever(P=PARAMS):
    """The 500 mm ratchet lever of the notching punch, lying along +Y from its ratchet ring at the origin, on z = 0."""
    return (cylz(22, 0, 16, 0, 0) - cylz(17, -1, 17, 0, 0)) + box(-10, 10, 21.5, 500, 3, 13)


def components(P=PARAMS):
    bd = _b()
    L = levels(P)
    z_ax, z_nip, ft = L["z_ax"], L["z_nip"], L["frame_top"]
    S, Tf = P["FRAME_RHS"], P["FRAME_T"]
    FX, FY = P["FRAME_X"], P["FRAME_Y"]
    out = []

    def add(key, name, shape, color, bom, how, group, explode=(0, 0, 0)):
        out.append(C(key, name, shape, color, bom, how, group, explode))

    # ======================================================== drain and purge stand (station 1)
    y0 = P["DS_Y"]
    rails = [rhs("x", -400, 400, y0 + sy * 240 - 20, y0 + sy * 240 + 20, 260, 300, 3) for sy in (-1, 1)]
    saddles, chocks = [], []
    tops = {-1: P["DS_TOP_HI"], 1: P["DS_TOP_LO"]}
    for sx in (-1, 1):
        xs = sx * P["DS_SADDLE_X"]
        saddles.append(rhs("y", y0 - 280, y0 + 280, xs - 20, xs + 20, 300, 340, 3))
        for sy in (-1, 1):
            yi = y0 + sy * P["DS_CHOCK_Y"]
            yo = y0 + sy * (P["DS_CHOCK_Y"] + 60)
            chocks.append(box(xs - 20, xs + 20, min(yi, yo), max(yi, yo), 340, tops[sx]))
    # legs stop under the rails (the rails sit on the legs)
    legs = [rhs("z", 0, 260, sx * 380 - 20, sx * 380 + 20, y0 + sy * 240 - 20, y0 + sy * 240 + 20, 3)
            for sx in (-1, 1) for sy in (-1, 1)]
    add("ds_frame", "Drain stand frame", comp(rails + legs + saddles), "#4B5563", 1, "make", "purge")
    add("ds_chocks", "Drain stand chocks (hardwood)", comp(chocks), "#A16207", 1, "make", "purge")
    # drum on the drain stand: rests on the four chock inner top edges, bung end (+X) low
    ro = P["DRUM_R_IN"] + P["DRUM_T"]
    h = math.sqrt(ro ** 2 - P["DS_CHOCK_Y"] ** 2)
    xs = P["DS_SADDLE_X"]
    tilt = math.degrees(math.atan2(P["DS_TOP_HI"] - P["DS_TOP_LO"], 2 * xs))
    zc = (P["DS_TOP_HI"] + P["DS_TOP_LO"]) / 2 + h / math.cos(math.radians(tilt)) + 1.1
    d2 = bd.Pos(0, y0, zc) * bd.Rot(0, tilt, 0) * drum(P)
    add("drum_ds", "Drum being purged (context)", d2, "#1E3A8A", None, "context", "context")
    tray = box(460, 1060, y0 - 250, y0 + 250, 0, 150) - box(463, 1057, y0 - 247, y0 + 247, 3, 160)
    add("tray", "Drain tray, 60 L", tray, "#15803D", 2, "buy", "purge")

    # ======================================================== cutting cradle (station 2)
    side = [rhs("x", -FX, FX, *(sorted((sy * FY, sy * (FY - S)))), ft - S, ft, Tf) for sy in (-1, 1)]
    cross_x = []
    for sx in (-1, 1):
        for xc in (P["PB_X"], P["POST_X"] - 37.5, P["POST_X"] + 37.5):
            cross_x.append(xc * sx)
    cross = [rhs("y", -(FY - S), FY - S, xc - S / 2, xc + S / 2, ft - S, ft, Tf) for xc in cross_x]
    leg_x, leg_y = FX - S / 2, FY - S / 2
    legs_c = [rhs("z", 31, ft - S, sx * leg_x - S / 2, sx * leg_x + S / 2, sy * leg_y - S / 2, sy * leg_y + S / 2, Tf)
              + box(sx * leg_x - 30, sx * leg_x + 30, sy * leg_y - 30, sy * leg_y + 30, 25, 31)
              for sx in (-1, 1) for sy in (-1, 1)]
    add("frame", "Cradle frame", comp(side + cross + legs_c), "#374151", 5, "make", "cut")
    feet = [cylz(30, 0, 12, sx * leg_x, sy * leg_y) + cylz(6, 12, 25, sx * leg_x, sy * leg_y)
            for sx in (-1, 1) for sy in (-1, 1)]
    add("feet", "Levelling feet (4)", comp(feet), "#9CA3AF", 5, "buy", "cut")

    zr, sr = P["ROLLER_Z"], P["SHAFT_R"]
    pbs, shafts, rollers = [], [], []
    for sy in (-1, 1):
        yr = sy * P["ROLLER_Y"]
        shafts.append(cylx(sr, -560, 560, yr, zr))
        for sx in (-1, 1):
            xp = sx * P["PB_X"]
            pb = box(xp - 19, xp + 19, yr - 70, yr + 70, ft, ft + 15) + cylx(32, xp - 19, xp + 19, yr, zr)
            pbs.append(pb - cylx(sr, xp - 30, xp + 30, yr, zr))
            rollers.append(ringx(sr, P["ROLLER_R"], sx * P["HOOP_X"] - P["ROLLER_W"] / 2,
                                 sx * P["HOOP_X"] + P["ROLLER_W"] / 2, yr, zr))
    add("pillow", "Pillow block bearings UCP205 (4)", comp(pbs), "#1D4ED8", 6, "buy", "cut")
    add("shafts", "Roller shafts (2)", comp(shafts), "#9CA3AF", 6, "make", "cut")
    add("rollers", "Cradle rollers (4)", comp(rollers), "#B45309", 6, "make", "cut")

    # drum on the cradle (heads on), hoops on the rollers
    d1 = bd.Pos(0, 0, z_ax) * drum(P, bung_phi=90.0)
    add("drum", "Drum on the cradle (context)", d1, "#1E3A8A", None, "context", "context")

    # drum brake on the +Y side rail
    ro = P["DRUM_R_IN"] + P["DRUM_T"]
    bpost = rhs("z", 180, 640, -20, 20, FY, FY + 40, 3) - cyly(9, FY - 10, FY + 50, 0, z_ax)
    screw = cyly(8, ro + 15, 470, 0, z_ax) + cylx(8, -80, 80, 470 - 8, z_ax)
    pad = cyly(30, ro, ro + 15, 0, z_ax)
    add("brake", "Drum brake: post, screw and pad", comp([bpost, screw + pad]), "#DC2626", 7, "make", "cut")

    # rail posts and beam
    px, pr, pt = P["POST_X"], P["POST_RHS"], P["POST_T"]
    bz0, bz1 = P["BEAM_Z0"], P["BEAM_Z0"] + P["BEAM_H"]
    posts, bolts_p = [], []
    for sx in (-1, 1):
        xc = sx * px
        base = box(xc - 50, xc + 50, -100, 100, ft, ft + 10)
        col = rhs("z", ft + 10, bz0 - 10, xc - pr / 2, xc + pr / 2, -pr / 2, pr / 2, pt)
        cap = box(xc - 60, xc + 60, -40, 40, bz0 - 10, bz0)
        holes = []
        for bx_ in (P["POST_X"] - 37.5, P["POST_X"] + 37.5):
            for by_ in (-70.0, 70.0):
                b_ = cylz(5, ft - S - 8, ft + 18, sx * bx_, by_)
                bolts_p.append(b_)
                holes.append(cylz(5.5, ft - S - 10, ft + 20, sx * bx_, by_))
        posts.append((base - fuse(holes)) + col + cap)
    add("posts", "Rail posts (2)", comp(posts), "#0F766E", 8, "make", "cut")
    beam = rhs("x", -P["BEAM_X"], P["BEAM_X"], -P["BEAM_W"] / 2, P["BEAM_W"] / 2, bz0, bz1, P["BEAM_T"])
    bolts_b = []
    for sx in (-1, 1):
        for bx_ in (P["POST_X"] - 40.0, P["POST_X"] + 40.0):
            bolts_b.append(cylz(5, bz0 - 10 - 7, bz1 + 7, sx * bx_, 0))
    hb = fuse([cylz(5.5, bz0 - 20, bz1 + 20, sx * bx_, 0) for sx in (-1, 1) for bx_ in (P["POST_X"] - 40.0, P["POST_X"] + 40.0)])
    add("beam", "Rail beam", beam - hb, "#0F766E", 8, "make", "cut")
    # the post caps need the same holes
    out[-2].shape = comp([p_ - hb for p_ in posts])
    # the cross members under the post bases need bolt holes too
    hp = fuse([cylz(5.5, ft - S - 10, ft + 20, sx * bx_, by_) for sx in (-1, 1) for bx_ in (P["POST_X"] - 37.5, P["POST_X"] + 37.5) for by_ in (-70.0, 70.0)])
    fr_ = [c for c in out if c.key == "frame"][0]
    fr_.shape = comp(side + [c_ - hp for c_ in cross] + legs_c)
    add("bolts", "Post and beam bolts M10", comp(bolts_p + bolts_b), "#111827", 8, "buy", "cut")

    # trolley and swivel, parked at the -X end
    xn = P["HEAD_PARK_X"]
    tz0, tz1 = 1176.0, 1340.0
    plates = [box(xn - 90, xn + 90, sy * 23, sy * 29, tz0, tz1) if sy > 0 else box(xn - 90, xn + 90, -29, -23, tz0, tz1)
              for sy in (-1, 1)]
    axles, wheels = [], []
    for dx in (-60, 60):
        for zc_ in (bz1 + 17.5, bz0 - 17.5 - 1.0):
            axles.append(cyly(7.5, -29, 29, xn + dx, zc_))
            wheels.append(ringy(7.5, 17.5, -5.5, 5.5, xn + dx, zc_))
    swivel = box(xn - 90, xn + 90, -29, 29, 1164, tz0)
    pin_h = cylz(15.5, 1100, 1200, xn, 0)
    trolley = fuse(plates) + swivel - pin_h - fuse([cyly(7.5, -40, 40, xn + dx, zc_) for dx in (-60, 60)
                                                    for zc_ in (bz1 + 17.5, bz0 - 18.5)])
    add("trolley", "Trolley with swivel plate", trolley, "#F59E0B", 9, "make", "cut")
    add("trolley_wheels", "Trolley wheels, 6202 bearings on 15 mm axles (4)", comp(axles + wheels), "#111827", 9, "buy", "cut")

    # shear head
    hl = shear_head_local(P)
    place = bd.Pos(xn, 0, z_nip)
    top_local = 136.0
    drop = rhs("z", z_nip + top_local, 1152, xn - 25, xn + 25, -25, 25, 4)
    tplate = box(xn - 60, xn + 60, -60, 60, 1152, 1164) - pin_h
    pin = cylz(15, 1130, 1185, xn, 0)
    add("drop", "Drop bar and head plate", (drop + tplate), "#F59E0B", 9, "make", "cut")
    add("pivot", "Pivot pin 30 mm with index pin", pin, "#111827", 9, "make", "cut")
    add("head_frame", "Shear head frame", place * hl["frame"], "#0F766E", 10, "make", "cut")
    add("discs", "Slitting discs 101 mm (2)", comp([place * hl["disc_u"], place * hl["disc_l"]]), "#E5E7EB", 10, "buy", "cut")
    add("head_shafts", "Head shafts", comp([place * hl["shaft_u"], place * hl["shaft_l"]]), "#B45309", 10, "make", "cut")
    add("head_guard", "Disc guard", place * hl["guard"], "#EAB308", 10, "make", "cut")
    add("head_case", "Drive case with chain guard", place * hl["drive_case"], "#EAB308", 10, "make", "cut")
    add("head_drive", "Crank, crank shaft, jackshaft and #35 sprockets",
        comp([place * hl["crank"], place * hl["jack"], place * hl["sprockets"]]), "#B45309", 10, "make", "cut")

    # tool shelf on the outer face of the left rail post, holding the notching punch, its lever and the ring head
    pxo = -(px + pr / 2)                                       # outer face of the left post
    back = box(pxo - 10, pxo, -100, 100, 450, 760)
    shelf = box(pxo - 380, pxo - 10, -300, 300, 600, 608)
    brk = [box(pxo - 260, pxo - 10, sy - 5, sy + 5, 520, 600) for sy in (-100, 100)]
    add("shelf", "Tool shelf on the left rail post", fuse([back, shelf] + brk), "#4B5563", 26, "make", "cut")
    st_top = 608.0
    pl_ = notch_punch_local(P)
    ppl = bd.Pos(pxo - 48, -95, st_top + 50) * bd.Rot(0, 0, 90)
    add("punch_frame", "Notching punch C-frame", ppl * pl_["frame"], "#7C2D12", 21, "make", "cut")
    add("punch_parts", "Notching punch: punches, screws and nut blocks",
        comp([ppl * pl_[k] for k in ("punches", "nuts", "screws")]), "#B45309", 21, "make", "cut")
    add("punch_lever", "Ratchet lever 500 mm", bd.Pos(pxo - 357, -250, st_top) * punch_lever(P), "#111827", 21, "buy", "cut")
    rl = ring_head_local(P)
    rpl = bd.Pos(pxo - 180, -20 + P["RING_PITCH"], st_top + 136)
    add("ring_frame", "Ring head frame (stored)", rpl * rl["frame"], "#0F766E", 25, "make", "cut")
    add("ring_parts", "Ring head discs, shafts and guard (stored)",
        comp([rpl * rl[k] for k in ("disc_u", "disc_l", "shaft_l", "shaft_u", "guard")]), "#E5E7EB", 25, "make", "cut")
    add("ring_link", "Ring head spacer plate, coupling shaft and guard sleeve (stored)",
        comp([rpl * rl["spacer"], rpl * rl["coupling"], rpl * rl["sleeve"]]),
        "#D97706", 25, "make", "cut")

    # end cutter on the +X chime (polar positions about the drum axis)
    half = P["DRUM_L"] / 2
    xh = half - P["HEAD_RECESS"]                        # head outer face
    gp = polar(0, P["HOOP_R"] + P["GUIDE_R"], 0, z_ax)
    dp = polar(0, P["CHIME_R_IN"] - P["DRIVE_R"], 0, z_ax)
    guide = ringx(6, P["GUIDE_R"], half - 14, half, 0, gp[2]) + cylx(6, half - 14, 500, 0, gp[2])
    dshaft = cylx(8, xh + 1, 530, 0, dp[2]) + box(530, 542, -10, 10, dp[2] - 10, dp[2] + P["EC_CRANK_R"] + 10) \
        + cylx(12, 542, 620, 0, dp[2] + P["EC_CRANK_R"])
    dwheel = ringx(8, P["DRIVE_R"], xh + 1, half - 1, 0, dp[2])
    phi = P["CUTTER_PHI"]
    cw = bd.Pos(xh + P["CUTTER_R"], 0, 0) * bd.Cylinder(P["CUTTER_R"], P["CUTTER_T"])    # axis Z (radial at top)
    cw = bd.Pos(0, 0, z_ax) * bd.Rot(-phi, 0, 0) * bd.Pos(0, 0, P["CUT_LINE_R"]) * cw
    c_rod = bd.Pos(0, 0, z_ax) * bd.Rot(-phi, 0, 0) * cylz(6, P["CUT_LINE_R"] + P["CUTTER_T"] / 2, 345,
                                                             xh + P["CUTTER_R"], 0)
    cy_, cz_ = polar(phi, 340, 0, z_ax)[1:]
    link = box(xh + P["CUTTER_R"] - 6, 500, cy_ - 12, cy_ + 12, cz_ - 6, cz_ + 14)
    body = box(500, 512, -80, 80, z_ax + 240, z_ax + 360) - cylx(8.5, 495, 520, 0, dp[2])
    cover = bd.Pos(0, 0, z_ax) * bd.Rot(-phi, 0, 0) * box(half + 1, xh + 2 * P["CUTTER_R"] + 3, -30, 30,
                                                           P["CUT_LINE_R"] + 5, P["CUT_LINE_R"] + 8)
    cover += bd.Pos(0, 0, z_ax) * bd.Rot(-phi, 0, 0) * box(xh + 2 * P["CUTTER_R"] + 3, 500, -30, 30,
                                                            P["CUT_LINE_R"] - 20, P["CUT_LINE_R"] + 8)
    body += cover
    tarm = box(500, 512, -15, 15, z_ax + 360, z_ax + 448) + box(512, px - pr / 2, -15, 15, z_ax + 440, z_ax + 448)
    add("ec_body", "End cutter body, cutter arm and torque arm", body + link + c_rod + tarm, "#7C3AED", 11, "make", "cut")
    add("ec_guide", "End cutter guide roller", guide, "#111827", 11, "make", "cut")
    add("ec_drive", "End cutter drive wheel, shaft and crank", comp([dshaft, dwheel]), "#B45309", 11, "make", "cut")
    add("ec_cutter", "End cutter wheel 50 mm (hardened)", cw, "#E5E7EB", 11, "buy", "cut")

    # ======================================================== slip roll stand (station 3)
    ry = P["RS_Y"]
    sx_, st_ = P["SIDE_X"], P["SIDE_T"]
    lz, uz, bz = P["LOWER_Z"], L["upper_z"], L["bend_z"]
    by_ = ry + P["BEND_Y"]
    jr = P["JOURNAL_R"]
    base = [rhs("y", ry - 400, ry + 400, sx * 530 - 30, sx * 530 + 30, 0, 60, 3) for sx in (-1, 1)]
    base += [rhs("x", -500, 500, ry + y0_, ry + y0_ + 60, 0, 60, 3) for y0_ in (-150, 160)]
    add("rs_base", "Roll stand base", comp(base), "#374151", 12, "make", "roll")

    def side_frame(s):
        xo0, xo1 = sorted((s * sx_, s * (sx_ + st_)))
        plate = box(xo0, xo1, ry + P["SIDE_Y0"], ry + P["SIDE_Y1"], P["SIDE_Z0"], P["SIDE_Z1"])
        plate -= cylx(20, xo0 - 1, xo1 + 1, ry, lz)
        plate -= box(xo0 - 1, xo1 + 1, ry - 30, ry + 30, 900, P["SIDE_Z1"] + 1)
        plate -= box(xo0 - 1, xo1 + 1, by_ - 30, by_ + 30, 840, P["SIDE_Z1"] + 1)
        lx0, lx1 = sorted((s * (sx_ - 17.5), s * (sx_ + 32.5)))
        lg = [rhs("z", 66, P["SIDE_Z0"], lx0, lx1, ry + yy - 25, ry + yy + 25, 3)
              + box((lx0 + lx1) / 2 - 40, (lx0 + lx1) / 2 + 40, ry + yy - 40, ry + yy + 40, 60, 66) for yy in (-120, 190)]
        bridge = box(xo0 - 5 if s < 0 else xo0, xo1 if s < 0 else xo1 + 5, ry - 150, ry + 220, P["SIDE_Z1"], P["SIDE_Z1"] + 25) \
            - cylz(8.5, P["SIDE_Z1"] - 5, P["SIDE_Z1"] + 30, s * (sx_ + st_ / 2), ry) \
            - cylz(10.5, P["SIDE_Z1"] - 5, P["SIDE_Z1"] + 30, s * (sx_ + st_ / 2), by_)
        return plate + bridge, lg

    sides, slegs = [], []
    for s in (-1, 1):
        sp, lg = side_frame(s)
        sides.append(sp)
        slegs += lg
    add("rs_sides", "Side frames with top bridges (2)", comp(sides + slegs), "#0F766E", 13, "make", "roll")

    # bushes and slide blocks
    bushes, blocks, screws, dials = [], [], [], []
    for s in (-1, 1):
        xo0, xo1 = sorted((s * sx_, s * (sx_ + st_)))
        xc = s * (sx_ + st_ / 2)
        fl0, fl1 = sorted((s * (sx_ + st_), s * (sx_ + st_ + 6)))
        bushes.append(ringx(jr, 20, xo0, xo1, ry, lz) + ringx(jr, 26, fl0, fl1, ry, lz))
        ub = box(xo0, xo1, ry - 30, ry + 30, uz - 30, uz + 30) - cylx(20, xo0 - 1, xo1 + 1, ry, uz)
        bb = box(xo0, xo1, by_ - 30, by_ + 30, bz - 30, bz + 30) - cylx(20, xo0 - 1, xo1 + 1, by_, bz)
        blocks += [ub, bb]
        bushes.append(ringx(jr, 20, xo0, xo1, ry, uz) + ringx(jr, 26, fl0, fl1, ry, uz))
        bushes.append(ringx(jr, 20, xo0, xo1, by_, bz) + ringx(jr, 26, fl0, fl1, by_, bz))
        screws.append(cylz(8, uz + 30, P["SIDE_Z1"] + 60, xc, ry) + cylz(45, P["SIDE_Z1"] + 60, P["SIDE_Z1"] + 72, xc, ry))
        screws.append(cylz(10, bz + 30, P["SIDE_Z1"] + 90, xc, by_) + cylz(55, P["SIDE_Z1"] + 90, P["SIDE_Z1"] + 102, xc, by_))
        # fine-pitch adjuster (DMP-DDR-003, Q4): lock nut on the bridge, dial clamped to the screw, pointer on the bridge
        zb = P["SIDE_Z1"] + 25
        dials.append(cylz(16, zb, zb + 12, xc, by_) - cylz(10, zb - 1, zb + 13, xc, by_))
        dials.append(cylz(40, zb + 20, zb + 28, xc, by_) - cylz(10, zb + 19, zb + 29, xc, by_))
        dials.append(box(xc - 5, xc + 5, by_ + 45, by_ + 50, zb, zb + 31) + box(xc - 5, xc + 5, by_ + 36, by_ + 45, zb + 28, zb + 31))
    add("rs_bushes", "Bronze bushes 30 mm, flanged (6)", comp(bushes), "#B08D57", 15, "buy", "roll")
    add("rs_blocks", "Slide blocks (4)", comp(blocks), "#6B7280", 15, "make", "roll")
    add("rs_screws", "Pinch screws M16 and fine-pitch bending screws M20 x 1.5 with handwheels", comp(screws), "#DC2626", 15, "make", "roll")
    add("rs_dials", "Bending roll adjusters: lock nuts, dials and pointers (2)", comp(dials), "#1F2937", 15, "make", "roll")

    # rolls
    face = P["ROLL_FACE"] / 2
    rr = P["ROLL_R"]
    lower = cylx(rr, -face, face, ry, lz) + cylx(jr, -540, 552, ry, lz)
    upper = cylx(rr, -face, face, ry, uz) + cylx(jr, -540, 492, ry, uz)
    bend = cylx(rr, -face, face, by_, bz) + cylx(jr, -492, 492, by_, bz)
    add("roll_lower", "Lower pinch roll (driven)", lower, "#9CA3AF", 14, "make", "roll")
    add("roll_upper", "Upper pinch roll", upper, "#A3A3A3", 14, "make", "roll")
    add("roll_bend", "Bending roll", bend, "#9CA3AF", 14, "make", "roll")
    gears = [ringx(jr, P["GEAR_R"], -530, -510, ry, lz), ringx(jr, P["GEAR_R"], -530, -510, ry, uz)]
    add("gears", "Pinch gears, module 3, 20 teeth (2)", comp(gears), "#1D4ED8", 16, "buy", "roll")

    # crank and chain drive (+X side)
    cy0, cz0 = ry + P["CRANK_Y"], P["CRANK_Z"]
    bracket = box(sx_ + st_, sx_ + st_ + 10, ry - 290, ry - 100, 760, 880) - cylx(13, sx_ + st_ - 1, sx_ + st_ + 11, cy0, cz0)
    housing = ringx(13, 25, sx_ + st_ + 10, 530, cy0, cz0)
    big = ringx(jr, P["SPROCKET_BIG_R"], 540, 548, ry, lz)
    small = ringx(12.5, P["SPROCKET_SMALL_R"], 540, 548, cy0, cz0)
    cshaft = cylx(12.5, sx_ + st_ + 0.0, 565, cy0, cz0) + box(565, 577, cy0 - 12, cy0 + 12, cz0 - 12, cz0 + P["RS_CRANK_R"] + 12) \
        + cylx(14, 577, 665, cy0, cz0 + P["RS_CRANK_R"])
    add("rs_bracket", "Crank bracket and bearing housing", bracket + housing, "#0F766E", 17, "make", "roll")
    add("rs_crank", "Crank shaft and crank, 300 mm", cshaft, "#B45309", 17, "make", "roll")
    add("sprockets", "Chain sprockets 13 and 39 teeth, #40 chain", comp([big, small]), "#111827", 17, "buy", "roll")

    # guards
    cg = box(530, 560, ry - 265, ry + 90, 780, 960) - box(531.5, 558.5, ry - 263.5, ry + 88.5, 781.5, 958.5)
    cg -= cylx(13, 520, 570, cy0, cz0)
    cg -= cylx(jr + 1, 520, 535, ry, lz)
    gx = -(sx_ + st_)
    gg = box(-545, gx, ry - 45, ry + 45, 830, 975) - box(-543.5, gx + 5, ry - 43.5, ry + 43.5, 831.5, 973.5)
    tg = P["TABLE_TOP"] + P["GUARD_GAP"]
    nip_in = box(-sx_, sx_, ry - 52, ry - 50, tg, 1000)
    nip_out = box(-sx_, sx_, ry + 150, ry + 152, P["OUT_TABLE_TOP"] + P["GUARD_GAP"], 1000)
    lid = box(-sx_, sx_, ry - 52, ry + 152, 1000, 1002)
    add("rs_guards", "Guards: nip guards and lid, chain guard, gear guard", comp([cg, gg, nip_in + lid + nip_out]), "#EAB308", 18, "make", "roll")

    # tables
    tin = box(-450, 450, ry - 850, ry - 35, 882, 900)
    tin_f = [box(-450, 450, ry - 850, ry - 35, 842, 882) - box(-446, 446, ry - 846, ry - 39, 841, 883)]
    tin_l = [rhs("z", 0, 842, sx * 410 - 20, sx * 410 + 20, ry + yy - 20, ry + yy + 20, 3) for sx in (-1, 1) for yy in (-810, -420)]
    tout_z = P["OUT_TABLE_TOP"]
    tout = box(-450, 450, ry + 125, ry + 935, tout_z - 18, tout_z)
    tout_f = [box(-450, 450, ry + 125, ry + 935, tout_z - 58, tout_z - 18) - box(-446, 446, ry + 129, ry + 931, tout_z - 59, tout_z - 17)]
    tout_l = [rhs("z", 0, tout_z - 58, sx * 410 - 20, sx * 410 + 20, ry + yy - 20, ry + yy + 20, 3) for sx in (-1, 1) for yy in (420, 895)]
    add("tables", "In-feed and out-feed tables", comp([tin, tout]), "#D6B98C", 19, "make", "roll")
    add("table_frames", "Table frames", comp(tin_f + tin_l + tout_f + tout_l), "#374151", 19, "make", "roll")

    # the opened drum body being fed (context)
    sh = bd.Pos(0, ry, P["TABLE_TOP"]) * curled_sheet(P)
    add("sheet", "Three drum body panels being fed (context)", sh, "#1E40AF", None, "context", "context")
    return out


# ---------------------------------------------------------------------------
# Grouping by BOM line
# ---------------------------------------------------------------------------
BOM_NAMES = {
    1: ("Drain and purge stand", "#4B5563", (0, -500, 0)),
    2: ("Drain tray, 60 L", "#15803D", (500, -500, 0)),
    5: ("Cradle frame with levelling feet", "#374151", (0, 0, -350)),
    6: ("Cradle rollers on shafts in pillow blocks", "#B45309", (0, 0, -150)),
    7: ("Drum brake", "#DC2626", (0, 350, 0)),
    8: ("Rail posts and rail beam", "#0F766E", (0, 0, 450)),
    9: ("Trolley, swivel and drop bar", "#F59E0B", (-300, 0, 650)),
    10: ("Rotary shear head", "#0D9488", (-300, -350, 300)),
    11: ("End cutter", "#7C3AED", (400, 0, 250)),
    12: ("Roll stand base", "#374151", (0, 0, -400)),
    13: ("Side frames (2)", "#0F766E", (0, 0, -150)),
    14: ("Rolls (3)", "#9CA3AF", (0, 0, 150)),
    15: ("Bushes, slide blocks and screws", "#B08D57", (0, 0, 350)),
    16: ("Pinch gears", "#1D4ED8", (-350, 0, 150)),
    17: ("Crank and chain drive", "#B45309", (350, -250, 0)),
    18: ("Roll guards", "#EAB308", (0, 0, 600)),
    19: ("In-feed and out-feed tables", "#D6B98C", (0, 0, 0)),
    21: ("Lever notching punch", "#7C2D12", (-500, -500, 200)),
    25: ("Ring head with spacer and coupling", "#0F766E", (-500, 300, 250)),
    26: ("Tool shelf", "#4B5563", (-450, 0, 0)),
}


def build_parts(P=PARAMS, comps=None, context=True):
    """Components grouped by BOM line: list of (name, shape, color, bom, explode). Context items last."""
    comps = comps or components(P)
    parts = []
    for bom, (name, color, exp) in BOM_NAMES.items():
        kids = [c.shape for c in comps if c.bom == bom]
        if kids:
            parts.append((name, comp(kids), color, bom, exp))
    if context:
        for c in comps:
            if c.group == "context":
                parts.append((c.name, c.shape, c.color, None, (0, 0, 0)))
    return parts


def assembly(parts=None):
    parts = parts or build_parts()
    return comp([p[1] for p in parts])


def station(comps, group):
    return comp([c.shape for c in comps if c.group == group])


# ---------------------------------------------------------------------------
# Fit checks
# ---------------------------------------------------------------------------
CONTACTS = [
    ("feet", "frame"), ("pillow", "frame"), ("shafts", "pillow"), ("rollers", "shafts"), ("drum", "rollers"),
    ("brake", "frame"), ("brake", "drum"), ("posts", "frame"), ("beam", "posts"), ("bolts", "posts"), ("bolts", "beam"),
    ("trolley_wheels", "beam"), ("trolley_wheels", "trolley"), ("drop", "trolley"), ("pivot", "trolley"), ("pivot", "drop"),
    ("head_frame", "drop"), ("head_shafts", "head_frame"), ("discs", "head_shafts"), ("head_guard", "head_frame"),
    ("head_case", "head_frame"), ("head_drive", "head_case"), ("head_drive", "head_shafts"),
    ("shelf", "posts"), ("punch_frame", "shelf"), ("punch_parts", "punch_frame"), ("punch_lever", "shelf"),
    ("ring_frame", "shelf"), ("ring_parts", "ring_frame"), ("ring_link", "ring_frame"), ("ring_link", "ring_parts"),
    ("ec_guide", "drum"), ("ec_drive", "drum"), ("ec_cutter", "drum"), ("ec_body", "ec_guide"), ("ec_body", "ec_drive"),
    ("ec_body", "ec_cutter"), ("ec_body", "posts"),
    ("ds_chocks", "ds_frame"), ("drum_ds", "ds_chocks"),
    ("rs_sides", "rs_base"), ("rs_bushes", "rs_sides"), ("rs_blocks", "rs_sides"), ("rs_bushes", "rs_blocks"),
    ("roll_lower", "rs_bushes"), ("roll_upper", "rs_bushes"), ("roll_bend", "rs_bushes"), ("rs_screws", "rs_blocks"),
    ("rs_screws", "rs_sides"), ("rs_dials", "rs_screws"), ("rs_dials", "rs_sides"), ("gears", "roll_lower"), ("gears", "roll_upper"), ("rs_bracket", "rs_sides"),
    ("rs_crank", "rs_bracket"), ("sprockets", "roll_lower"), ("sprockets", "rs_crank"), ("rs_guards", "rs_bracket"),
    ("rs_guards", "rs_sides"), ("tables", "table_frames"), ("sheet", "tables"), ("sheet", "roll_lower"),
]
ALLOWED = set()


def _solids(shape):
    return list(shape.solids()) or [shape]


def _bb_apart(A, B, pad=0.0):
    return (A.min.X > B.max.X + pad or B.min.X > A.max.X + pad or A.min.Y > B.max.Y + pad or B.min.Y > A.max.Y + pad
            or A.min.Z > B.max.Z + pad or B.min.Z > A.max.Z + pad)


def check_fits(comps=None, tol=1.0, verbose=True):
    """No two components may overlap (intersection volume at or above tol mm3); every CONTACTS pair must touch
    (within 1.2 mm: the drum on the sloped drain stand is placed 1.1 mm clear of the chock edges at their middle,
    so the sloping drum just clears the high corner of each 40 mm chock)."""
    comps = comps or components()
    sol = {c.key: [(s_, s_.bounding_box()) for s_ in _solids(c.shape)] for c in comps}
    bbs = {c.key: c.shape.bounding_box() for c in comps}
    overlaps = []
    for i, a in enumerate(comps):
        for b_ in comps[i + 1:]:
            if frozenset((a.key, b_.key)) in ALLOWED or _bb_apart(bbs[a.key], bbs[b_.key]):
                continue
            v = 0.0
            for sa, ba in sol[a.key]:
                if _bb_apart(ba, bbs[b_.key]):
                    continue
                for sb, bb_ in sol[b_.key]:
                    if _bb_apart(ba, bb_):
                        continue
                    r = sa & sb
                    v += r.volume if r is not None else 0.0
            if v >= tol:
                overlaps.append((a.key, b_.key, v))
    gaps = []
    for ka, kb in CONTACTS:
        near = [(sa, sb) for sa, ba in sol[ka] for sb, bb_ in sol[kb] if not _bb_apart(ba, bb_, 1.0)]
        d = min(sa.distance_to(sb) for sa, sb in near) if near else 99.0
        if d > 1.2:
            gaps.append((ka, kb, d))
    if verbose:
        print(f"fit check: {len(comps)} components; {len(overlaps)} overlaps; {len(gaps)} missing contacts")
        for o in overlaps:
            print(f"  OVERLAP {o[0]} / {o[1]}: {o[2]:.1f} mm3")
        for g_ in gaps:
            print(f"  NO CONTACT {g_[0]} / {g_[1]}: {g_[2]:.2f} mm apart")
    return overlaps, gaps


def crank_sweep_local(P=PARAMS):
    """The space the shear head's crank and grip sweep through in one turn (head local)."""
    return cyly(P["CRANK_R"] + 2, 118, 230, P["KCRANK_X"], P["KCRANK_Z"])


def ring_passes(P=PARAMS):
    """The three ring passes: (main head nip x, ring head nip x). Each pass makes two of the six ring cuts."""
    c = ring_cut_lines(P)
    return [(c[0], c[1]), (c[2], c[3]), (c[4], c[5])]


def ring_mode_check(P=PARAMS, verbose=True):
    """The main head swivelled 90 degrees with the ring head bolted on (DMP-DDR-003, Q2), set at each of the three
    ring passes on the opened drum (heads off, slit at the top, hoops still on): the frames, guards, shafts, discs,
    drive case, coupling and spacer must clear the drum wall everywhere except in the two kerfs being cut, and the
    rail posts; the crank's sweep must clear the drum, the posts, the rail beam and the trolley. The ring head sits
    233 or 234 mm from the main head (two holes in the spacer plate)."""
    bd = _b()
    L = levels(P)
    hl = shear_head_local(P)
    half = P["DRUM_L"] / 2
    body = bd.Pos(0, 0, L["z_ax"]) * drum(P, heads=False)
    body = body - box(-half - 5, half + 5, -6, 6, L["z_ax"], L["z_ax"] + 400)      # the slit, edges spread
    cs = {c.key: c.shape for c in components(P)}
    fixed = comp([cs["posts"], cs["beam"]])
    worst = 0.0
    for x1, x2 in ring_passes(P):
        Q = dict(P)
        Q["RING_PITCH"] = x2 - x1
        rl = ring_head_local(Q)
        pl = bd.Pos(x1, 0, L["z_nip"]) * bd.Rot(0, 0, 90)
        head = comp([pl * hl[k] for k in HEAD_KEYS] + [pl * rl[k] for k in RING_KEYS])
        k = P["DISC_T"] + 1.0     # the sheared zone: the cut edges are pushed apart by the discs and the 10 mm web
        kerf = box(x1 - k, x1 + k, -400, 400, L["z_ax"], L["z_ax"] + 400) + box(x2 - k, x2 + k, -400, 400, L["z_ax"], L["z_ax"] + 400)
        v = (head & (body - kerf)).volume + (head & fixed).volume
        dx = x1 - P["HEAD_PARK_X"]
        trol = comp([bd.Pos(dx, 0, 0) * cs[c_] for c_ in ("trolley", "trolley_wheels", "drop", "pivot")])
        sweep = pl * crank_sweep_local(P)
        vs = (sweep & body).volume + (sweep & fixed).volume + (sweep & trol).volume
        worst = max(worst, v, vs)
        if verbose:
            print(f"ring pass at x = {x1:5.0f} and {x2:5.0f}: heads inside the drum wall outside the kerfs or in a post "
                  f"{v:.1f} mm3; crank sweep in the drum, posts, beam or trolley {vs:.1f} mm3 "
                  f"({'clear' if max(v, vs) < 1 else 'CLASH'})")
    return worst


def slit_mode_check(P=PARAMS, verbose=True):
    """The shear head in slit mode at stations along the drum (heads off, chime rings and hoop ridges notched on
    the slit line by the notching punch, DMP-DDR-003 Q1): the frame, guard, shafts, discs and drive case must clear
    the drum wall except in the cut behind the nip and the sheared zone under the discs, and the crank's sweep must
    clear the drum and the rail beam."""
    bd = _b()
    L = levels(P)
    hl = shear_head_local(P)
    half = P["DRUM_L"] / 2
    body = bd.Pos(0, 0, L["z_ax"]) * drum(P, heads=False)
    zt = L["z_ax"] + 200
    for nb in notch_boxes(P, z_top=zt):
        body = body - nb
    beam = [c.shape for c in components(P) if c.key == "beam"][0]
    worst = 0.0
    for xn in (-450.0, -300.0, -147.0, 0.0, 147.0, 300.0, 450.0):
        pl = bd.Pos(xn, 0, L["z_nip"])
        head = pl * comp([hl[k] for k in HEAD_KEYS])
        k = P["DISC_T"] + 1.0
        cut = box(-half - 200, xn + P["DISC_R"] + 1, -k, k, zt, zt + 200)
        sweep = pl * crank_sweep_local(P)
        v = (head & (body - cut)).volume + (sweep & body).volume + (sweep & beam).volume
        worst = max(worst, v)
    if verbose:
        print(f"slit mode, 7 stations from x = -450 to 450: worst head or crank sweep volume inside the drum wall outside "
              f"the cut or in the beam: {worst:.1f} mm3 ({'clear' if worst < 1 else 'CLASH'})")
    return worst


def punch_check(P=PARAMS, verbose=True):
    """The notching punch at each of the four notches (DMP-DDR-003, Q1), in the order they are cut: both chime
    notches first (back face on the drum end, station 1 die on the inside of the chime), then both hoop slots
    (drum end against the station 1 die block, station 2 die on the inside of the wall), each hoop reached through
    the chime notch at its own end. The C-frame, punches, nut blocks and screws must clear the drum except for
    the slug being cut, and the die faces must touch the steel they support."""
    bd = _b()
    L = levels(P)
    pl_ = notch_punch_local(P)
    tool = comp([pl_[k] for k in PUNCH_KEYS])
    half = P["DRUM_L"] / 2
    zax = L["z_ax"]
    body0 = bd.Pos(0, 0, zax) * drum(P, heads=False)
    zt = zax + 200
    chime, hoop = notch_boxes(P, z_top=zt, hoops=False), notch_boxes(P, z_top=zt, ends=False)
    worst, worst_gap = 0.0, 0.0
    cases = []
    for i, sx in enumerate((-1, 1)):
        rot = bd.Rot(0, 0, 0 if sx < 0 else 180)
        cases.append((f"chime notch, {'left' if sx < 0 else 'right'} end", bd.Pos(sx * half, 0, zax + P["CHIME_R_IN"]) * rot,
                      body0, chime[i]))
    body1 = body0 - chime[0] - chime[1]
    for i, sx in enumerate((-1, 1)):
        rot = bd.Rot(0, 0, 0 if sx < 0 else 180)
        cases.append((f"hoop slot, {'left' if sx < 0 else 'right'} hoop", bd.Pos(sx * (half + 45), 0, zax + P["DRUM_R_IN"]) * rot,
                      body1, hoop[i]))
    for name, pl, body, slug in cases:
        t = pl * tool
        v = (t & (body - slug)).volume
        gap = (pl * pl_["frame"]).distance_to(body - slug)
        worst, worst_gap = max(worst, v), max(worst_gap, gap)
        if verbose:
            print(f"punch, {name}: tool inside the drum outside the slug {v:.1f} mm3; die to steel {gap:.2f} mm "
                  f"({'clear' if v < 1 and gap < 0.5 else 'CLASH' if v >= 1 else 'NO CONTACT'})")
    return worst, worst_gap


if __name__ == "__main__":
    import sys
    from build123d import export_step, export_stl
    comps = components()
    if "--check" in sys.argv:
        ov, gp = check_fits(comps)
        v = ring_mode_check()
        v2 = slit_mode_check()
        v3, g3 = punch_check()
        ok = not (ov or gp) and v < 1 and v2 < 1 and v3 < 1 and g3 < 0.5
        print("constructability checks:", "PASS" if ok else "FAIL")
        sys.exit(0 if ok else 1)
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    parts = build_parts(comps=comps, context=False)
    export_step(assembly(parts), str(root / "step" / "drumpanel-bench-set.step"))
    by = {c.key: c.shape for c in comps}
    for grp, stem in (("purge", "drain-stand"), ("cut", "cutting-cradle"), ("roll", "slip-roll-stand")):
        export_step(station(comps, grp), str(root / "step" / f"{stem}.step"))
    hl = shear_head_local()
    head = comp([hl[k] for k in HEAD_KEYS])
    export_step(head, str(root / "step" / "rotary-shear-head.step"))
    export_step(comp([by[k] for k in ("ec_body", "ec_guide", "ec_drive", "ec_cutter")]), str(root / "step" / "end-cutter.step"))
    export_step(by["roll_upper"], str(root / "step" / "upper-pinch-roll.step"))
    pl_ = notch_punch_local()
    punch = comp([pl_[k] for k in PUNCH_KEYS])
    export_step(punch, str(root / "step" / "notching-punch.step"))
    rl = ring_head_local()
    export_step(comp([hl[k] for k in HEAD_KEYS] + [rl[k] for k in RING_KEYS]), str(root / "step" / "shear-head-with-ring-head.step"))
    export_stl(punch, str(root / "stl" / "notching-punch.stl"), tolerance=0.2, angular_tolerance=0.3)
    export_stl(head, str(root / "stl" / "rotary-shear-head.stl"), tolerance=0.2, angular_tolerance=0.3)
    export_stl(comp([by[k] for k in ("ec_body", "ec_guide", "ec_drive", "ec_cutter")]), str(root / "stl" / "end-cutter.stl"),
               tolerance=0.2, angular_tolerance=0.3)
    L = levels()
    print(f"cradle drum axis {L['z_ax']:.1f} mm; drum top {L['drum_top']:.1f} mm; roller contact {L['contact_deg']:.1f} deg "
          f"from vertical; sheet {L['sheet_l']:.0f} x {L['sheet_w']:.0f} mm")
    print("wrote cad/step/*.step and cad/stl/*.stl")
