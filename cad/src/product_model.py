"""DrumPanel product appearance model (build123d), TRL 3, constructable design (DMP-DDR-002).

Finished look of the bench set for photoreal renders, built from the constructable model: every component of
cad/src/model.py components() is used as it is, with every main dimension from there (drain stand and tray, cradle
frame, rollers, pillow blocks, brake, rail posts and beam, trolley, shear head, end cutter, slip roll stand with
its rolls, blocks, screws and dial adjusters, gears, crank drive, guards and tables, the shear head's drive case,
and the tool shelf with the notching punch, its lever and the ring head). Only the look is added: a #40 roller chain drawn
as a plain band round the two sprockets, a nameplate on the right-hand side frame, a hazard label on the in-feed
guard, painted drums, a workshop floor and a 1.75 m mannequin for scale. A second state, used only by the detail
view, shows a drum with its heads off being slit, the shear head halfway along it.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Groups: "purge" (drain stand and tray), "cradle" (cradle frame, rollers, brake, posts, beam), "head" (trolley and
shear head with its drive case parked at the left end), "cutter" (end cutter on the right chime), "tools" (tool shelf
on the left post with the notching punch, its lever and the ring head), "roll" (slip roll stand), "drums"
(the drum on the cradle with its heads on, the drum on the drain stand), "panels" (three panels being fed),
"slitting" (the opened drum and the shear head halfway along it), "context" (floor and mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Pos, Rot  # noqa: E402
from model import PARAMS, box, comp, components, cylx, drum, levels, notch_boxes, ringx, shear_head_local  # noqa: E402

TITLE = "DrumPanel: hand-powered bench set that opens oil drums into flat sheet without fire"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["purge", "cradle", "head", "cutter", "tools", "roll", "drums", "panels", "context"], "explode": False,
     "el": 28, "az": -38,
     "note": "Product render from the front right and above (about 28 deg elevation): drain and purge stand with a drum "
             "bung end down over its tray (front), cutting cradle with a drum, the end cutter on its right chime, "
             "the shear head parked on the rail and the tool shelf with the notching punch and ring head on the left "
             "post (middle), slip roll stand feeding three panels (back); 1.75 m person for scale"},
    {"name": "exploded", "groups": ["cradle", "head", "cutter", "tools", "roll"], "explode": True, "el": 26, "az": -50,
     "note": "Exploded view from the front right and above (about 26 deg elevation): cradle frame, rollers, brake, "
             "posts and rail beam, trolley and shear head with its drive case, end cutter, tool shelf with the "
             "notching punch and ring head; slip roll base, side frames, rolls, slide blocks, screws and dials, "
             "crank drive, guards and tables; drain stand, drums and panels not shown"},
    {"name": "detail", "groups": ["cradle", "slitting"], "explode": False, "el": 30, "az": -30,
     "note": "Detail from the front right and above (about 30 deg elevation): a purged drum with its heads off on the "
             "cradle rollers, brake on, the hand-cranked shear head halfway along the seam slit, the cut edges "
             "spread round its web, its crank turning high on the drive case; chime rings and hoops notched on the "
             "slit line by the notching punch"},
]

C_STEEL = "#3A4048"
C_TEAL = "#0F766E"
C_ACCENT = "#14B8A6"
C_ZINC = "#B8BEC6"
C_BLACK = "#1C1F24"
C_ORANGE = "#C2410C"
C_YELLOW = "#E8B517"
C_BRONZE = "#B08D57"
C_BLUE_DRUM = "#1F4E9C"
C_RED_DRUM = "#9B2C2C"
C_DRUM_IN = "#8A8F96"
C_PLY = "#CFAE84"
C_GREEN = "#2F6B3A"
C_FLOOR = "#D8D5CF"
C_CLAY = "#B9B4AC"
C_LABEL = "#F4F4F2"
C_INK = "#1F2937"

# key: (display name, colour, material, group, explode offset)
LOOK = {
    "ds_frame": ("Drain stand frame", C_STEEL, "painted", "purge", (0, 0, 0)),
    "ds_chocks": ("Drain stand chocks (hardwood)", "#8B5A2B", "wood", "purge", (0, 0, 0)),
    "tray": ("Drain tray, 60 L", C_GREEN, "plastic", "purge", (0, 0, 0)),
    "frame": ("Cradle frame", C_STEEL, "painted", "cradle", (0, 0, -350)),
    "feet": ("Levelling feet", C_ZINC, "metal", "cradle", (0, 0, -450)),
    "pillow": ("Pillow blocks UCP205", "#2B4C7E", "painted", "cradle", (0, 0, -200)),
    "shafts": ("Roller shafts", C_ZINC, "metal", "cradle", (0, 0, -120)),
    "rollers": ("Cradle rollers", C_ORANGE, "painted", "cradle", (0, 0, -120)),
    "brake": ("Drum brake", "#B91C1C", "painted", "cradle", (0, 350, 0)),
    "posts": ("Rail posts", C_TEAL, "painted", "cradle", (0, 0, 250)),
    "beam": ("Rail beam", C_TEAL, "painted", "cradle", (0, 0, 500)),
    "bolts": ("Post and beam bolts", C_ZINC, "metal", "cradle", (0, 0, 250)),
    "trolley": ("Trolley", C_YELLOW, "painted", "head", (0, 0, 750)),
    "trolley_wheels": ("Trolley wheels", C_BLACK, "metal", "head", (0, 0, 750)),
    "drop": ("Drop bar and head plate", C_YELLOW, "painted", "head", (-250, -350, 500)),
    "pivot": ("Pivot pin", C_ZINC, "metal", "head", (-250, -350, 650)),
    "head_frame": ("Shear head frame", C_TEAL, "painted", "head", (-250, -350, 500)),
    "discs": ("Slitting discs (D2)", "#D5D9DE", "metal", "head", (-250, -650, 500)),
    "head_shafts": ("Head shafts and crank", C_ORANGE, "painted", "head", (-250, -650, 500)),
    "head_guard": ("Disc guard", C_YELLOW, "painted", "head", (-250, -350, 700)),
    "head_case": ("Shear head drive case (chain guard)", C_YELLOW, "painted", "head", (-250, -150, 600)),
    "head_drive": ("Shear head crank and jackshaft", C_ORANGE, "painted", "head", (-250, 50, 650)),
    "shelf": ("Tool shelf", C_STEEL, "painted", "tools", (-300, 0, -100)),
    "punch_frame": ("Notching punch C-frame", "#7C2D12", "painted", "tools", (-500, 0, 250)),
    "punch_parts": ("Notching punch screws and nut blocks", C_ZINC, "metal", "tools", (-500, 0, 300)),
    "punch_lever": ("Notching punch ratchet lever", C_BLACK, "metal", "tools", (-500, 0, 150)),
    "ring_frame": ("Ring head frame", C_TEAL, "painted", "tools", (-700, 0, 350)),
    "ring_parts": ("Ring head discs, shafts and guard", "#D5D9DE", "metal", "tools", (-700, 0, 350)),
    "ring_link": ("Ring head spacer plate and coupling", C_ORANGE, "painted", "tools", (-700, 0, 450)),
    "ec_body": ("End cutter body and torque arm", "#6D28D9", "painted", "cutter", (350, 0, 300)),
    "ec_guide": ("End cutter guide roller", C_BLACK, "metal", "cutter", (350, 0, 300)),
    "ec_drive": ("End cutter drive wheel and crank", C_ORANGE, "painted", "cutter", (350, 0, 300)),
    "ec_cutter": ("End cutter wheel", "#D5D9DE", "metal", "cutter", (350, 0, 300)),
    "rs_base": ("Roll stand base", C_STEEL, "painted", "roll", (0, 0, -500)),
    "rs_sides": ("Side frames", C_TEAL, "painted", "roll", (0, 0, -200)),
    "rs_bushes": ("Bronze bushes", C_BRONZE, "metal", "roll", (0, 0, 150)),
    "rs_blocks": ("Slide blocks", "#6B7280", "metal", "roll", (0, 0, 250)),
    "rs_screws": ("Pinch and bending screws with handwheels", "#B91C1C", "painted", "roll", (0, 0, 350)),
    "rs_dials": ("Bending roll dials, lock nuts and pointers", C_BLACK, "metal", "roll", (0, 0, 300)),
    "roll_lower": ("Lower pinch roll", "#C9CED4", "metal", "roll", (0, 0, 150)),
    "roll_upper": ("Upper pinch roll", "#C9CED4", "metal", "roll", (0, 0, 250)),
    "roll_bend": ("Bending roll", "#C9CED4", "metal", "roll", (0, 200, 150)),
    "gears": ("Pinch gears", "#1D4ED8", "metal", "roll", (-300, 0, 200)),
    "rs_bracket": ("Crank bracket", C_TEAL, "painted", "roll", (300, -150, 0)),
    "rs_crank": ("Crank", C_ORANGE, "painted", "roll", (400, -150, 0)),
    "sprockets": ("Chain sprockets", C_BLACK, "metal", "roll", (300, -150, 0)),
    "rs_guards": ("Roll guards", C_YELLOW, "painted", "roll", (0, 0, 650)),
    "tables": ("In-feed and out-feed tables", C_PLY, "wood", "roll", (0, 0, 0)),
    "table_frames": ("Table frames", C_STEEL, "painted", "roll", (0, 0, 0)),
    "drum": ("Drum on the cradle (painted)", C_BLUE_DRUM, "painted", "drums", (0, 0, 0)),
    "drum_ds": ("Drum being purged (painted)", C_RED_DRUM, "painted", "drums", (0, 0, 0)),
    "sheet": ("Three drum panels being fed", C_BLUE_DRUM, "painted", "panels", (0, 0, 0)),
}


def product_parts():
    P, L = PARAMS, levels()
    cs = {c.key: c for c in components()}
    out = []

    def add(name, shape, color, material, group, bom=None, explode=(0, 0, 0)):
        out.append(dict(name=name, shape=shape, color=color, material=material, group=group, bom=bom, explode=explode))

    for key, (name, color, mat, group, exp) in LOOK.items():
        c = cs[key]
        add(name, c.shape, color, mat, group, c.bom, exp)

    # chain as a plain band round the two sprockets (outside the guard's interior, which is drawn closed)
    ry, lz = P["RS_Y"], P["LOWER_Z"]
    cy0, cz0 = ry + P["CRANK_Y"], P["CRANK_Z"]
    import math
    r1, r2 = P["SPROCKET_BIG_R"] + 4, P["SPROCKET_SMALL_R"] + 4
    dy, dz = ry - cy0, lz - cz0
    d = math.hypot(dy, dz)
    a = math.atan2(dz, dy)
    b = math.acos((r1 - r2) / d)
    pts = []
    for ang in (a + b, a - b):
        pts.append((cy0 + r2 * math.cos(ang), cz0 + r2 * math.sin(ang), ry + r1 * math.cos(ang), lz + r1 * math.sin(ang)))
    x0 = 541.0
    links = []
    for k in range(40):
        t = k / 40.0
        for p_ in pts:
            y_ = p_[0] + (p_[2] - p_[0]) * t
            z_ = p_[1] + (p_[3] - p_[1]) * t
            links.append(box(x0, x0 + 6, y_ - 4, y_ + 4, z_ - 3.5, z_ + 3.5))
    add("Roller chain #40 (drawn as links on the straight runs)", comp(links), C_BLACK, "metal", "roll", 17, (300, -150, 0))

    # nameplate on the right-hand side frame, hazard label on the in-feed guard
    sx = P["SIDE_X"] + P["SIDE_T"]
    add("Nameplate", box(sx, sx + 1.2, ry + 120, ry + 210, 880, 940), C_TEAL, "painted", "roll", None, (0, 0, -200))
    add("Nameplate print", box(sx + 1.2, sx + 1.5, ry + 130, ry + 200, 915, 930) + box(sx + 1.2, sx + 1.5, ry + 130, ry + 175, 895, 905),
        C_LABEL, "paper", "roll", None, (0, 0, -200))
    add("Hazard label (in-running rolls, keep hands clear)", box(-120, 120, ry - 53.2, ry - 52, 935, 985), C_YELLOW, "paper", "roll",
        None, (0, 0, 650))
    add("Hazard label print", box(-100, -60, ry - 53.5, ry - 53.2, 945, 975) + box(-40, 100, ry - 53.5, ry - 53.2, 962, 972)
        + box(-40, 80, ry - 53.5, ry - 53.2, 946, 954), C_INK, "paper", "roll", None, (0, 0, 650))

    # detail state: a drum with its heads off being slit, the shear head halfway along
    zax, znip = L["z_ax"], L["z_nip"]
    half = P["DRUM_L"] / 2
    xn = 0.0
    body = Pos(0, 0, zax) * drum(P, heads=False)
    zt = zax + 200
    for nb in notch_boxes(P, z_top=zt):
        body = body - nb
    body = body - box(-half - 10, xn + P["DISC_R"] * 0.2, -11, 11, zt, zt + 200)
    add("Drum with its heads off, being slit", body, C_BLUE_DRUM, "painted", "slitting")
    hl = shear_head_local(P)
    pl = Pos(xn, 0, znip)
    for k, name, color, mat in (("frame", "Shear head frame", C_TEAL, "painted"), ("guard", "Disc guard", C_YELLOW, "painted"),
                                ("disc_u", "Upper slitting disc", "#D5D9DE", "metal"), ("disc_l", "Lower slitting disc", "#D5D9DE", "metal"),
                                ("shaft_u", "Upper shaft", C_ORANGE, "painted"), ("shaft_l", "Lower shaft", C_ORANGE, "painted"),
                                ("drive_case", "Drive case", C_YELLOW, "painted"), ("crank", "Crank", C_ORANGE, "painted"),
                                ("jack", "Jackshaft", C_ZINC, "metal")):
        add(name + " (slitting)", pl * hl[k], color, mat, "slitting")
    dx = xn - P["HEAD_PARK_X"]
    for key in ("trolley", "trolley_wheels", "drop", "pivot"):
        name, color, mat, _, _ = LOOK[key]
        add(name + " (slitting)", Pos(dx, 0, 0) * cs[key].shape, color, mat, "slitting")

    # context: floor and a 1.75 m person
    add("Workshop floor (concrete)", box(-1700, 2300, -2200, 3200, -20, 0), C_FLOOR, "paper", "context")
    from context_parts import mannequin
    person = Pos(1150, -700, 0) * Rot(0, 0, 160) * mannequin(1750, "stand")
    add("Person, 1.75 m mannequin (scale)", person, C_CLAY, "clay", "context")
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:58s} {p['group']:9s} {p['material']:8s} vol={s.volume / 1000:9.1f} cm3")
