"""DrumPanel prototype build plan pictures (DMP-BLD-001, STANDARDS section 18).

Run from the repo root:
    python cad/src/build_plan_media.py                       everything (heavy: better one group per process)
    python cad/src/build_plan_media.py overview
    python cad/src/build_plan_media.py sheets [101 102 ...]
    python cad/src/build_plan_media.py joints [1 2 ...]
    python cad/src/build_plan_media.py steps [1 2 ...]
Every picture is drawn from cad/src/model.py (components(), shear_head_local()), so the pictures and the model
never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/DMP-DWG-101 to 119        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model as m  # noqa: E402
from model import PARAMS as P, levels, box, comp  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-03"
L = levels()
ZAX, ZNIP, FT = L["z_ax"], L["z_nip"], L["frame_top"]
RY = P["RS_Y"]
XN = P["HEAD_PARK_X"]
_C = None


def comps():
    global _C
    if _C is None:
        _C = {c.key: c for c in m.components()}
    return _C


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def K(key, name=None, color=None, explode=(0, 0, 0)):
    c = comps()[key]
    return part(name or c.name, c.shape, color or c.color, explode)


def fuse(*keys):
    return comp([comps()[k].shape for k in keys])


def win(shape, x0, x1, y0, y1, z0, z1):
    """The part of a shape inside a box (for close-ups and cut-open views)."""
    w = box(x0, x1, y0, y1, z0, z1)
    try:
        sols = list(shape.solids()) or [shape]
    except Exception:
        sols = [shape]
    kept = []
    for s_ in sols:
        bb = s_.bounding_box()
        if bb.max.X < x0 or bb.min.X > x1 or bb.max.Y < y0 or bb.min.Y > y1 or bb.max.Z < z0 or bb.min.Z > z1:
            continue
        r = s_ & w
        if r is not None and r.volume > 1e-3:
            kept.append(r)
    return comp(kept) if kept else None


def W(key, name, color, bx):
    return part(name, win(comps()[key].shape, *bx), color)


COL = {"ds": "#4B5563", "chock": "#A16207", "tray": "#15803D", "frame": "#374151", "feet": "#9CA3AF",
       "pillow": "#1D4ED8", "shaft": "#6B7280", "roller": "#B45309", "brake": "#DC2626", "posts": "#0F766E",
       "beam": "#0D9488", "bolts": "#111827", "trolley": "#F59E0B", "wheels": "#1F2937", "drop": "#D97706",
       "pivot": "#7C2D12", "hframe": "#0F766E", "discs": "#94A3B8", "hshaft": "#B45309", "guard": "#EAB308",
       "ec": "#7C3AED", "ecdrive": "#B45309", "ecguide": "#111827", "ecwheel": "#94A3B8", "drum": "#1E3A8A",
       "rsbase": "#374151", "sides": "#0F766E", "bush": "#B08D57", "blocks": "#6B7280", "screws": "#DC2626",
       "roll": "#9CA3AF", "gears": "#1D4ED8", "bracket": "#0D9488", "crank": "#B45309", "sprocket": "#111827",
       "rsguard": "#EAB308", "tables": "#D6B98C", "tframes": "#374151", "sheet": "#1E40AF"}


def side_parts():
    """Side frames split into the welded frame (plate and legs) and the bolted-on top bridges."""
    s = comps()["rs_sides"].shape
    z1 = P["SIDE_Z1"]
    bridges = win(s, -2000, 2000, RY - 400, RY + 400, z1, z1 + 40)
    frames = win(s, -2000, 2000, RY - 400, RY + 400, 0, z1)
    return frames, bridges


# ----------------------------------------------------------------- named groups, in build order
def groups():
    return [
        ("ds", "Drain stand frame and chocks", ("ds_frame", "ds_chocks"), COL["ds"]),
        ("tray", "Drain tray (bought)", ("tray",), COL["tray"]),
        ("frame", "Cradle frame and levelling feet", ("frame", "feet"), COL["frame"]),
        ("rollers", "Roller shafts, rollers, pillow blocks", ("shafts", "rollers", "pillow"), COL["roller"]),
        ("brake", "Drum brake", ("brake",), COL["brake"]),
        ("posts", "Rail posts with bolts", ("posts", "bolts"), COL["posts"]),
        ("beam", "Rail beam", ("beam",), COL["beam"]),
        ("trolley", "Trolley with wheels", ("trolley", "trolley_wheels"), COL["trolley"]),
        ("drop", "Drop bar, head plate and pivot pin", ("drop", "pivot"), COL["drop"]),
        ("head", "Shear head frame", ("head_frame",), COL["hframe"]),
        ("hshaft", "Head shafts, crank, discs, guard", ("head_shafts", "discs", "head_guard"), COL["hshaft"]),
        ("ec", "End cutter", ("ec_body", "ec_guide", "ec_drive", "ec_cutter"), COL["ec"]),
        ("rsbase", "Roll stand base", ("rs_base",), COL["rsbase"]),
        ("sides", "Side frames with bridges", ("rs_sides",), COL["sides"]),
        ("rolls", "Rolls (3), bushes and pinch gears", ("roll_lower", "roll_upper", "roll_bend", "rs_bushes", "gears"), COL["roll"]),
        ("blocks", "Slide blocks and screws", ("rs_blocks", "rs_screws"), COL["blocks"]),
        ("drive", "Crank bracket, crank, sprockets", ("rs_bracket", "rs_crank", "sprockets"), COL["crank"]),
        ("guards", "Roll guards", ("rs_guards",), COL["rsguard"]),
        ("tin", "In-feed table", ("tables", "table_frames"), COL["tables"]),
        ("tout", "Out-feed table", ("tables", "table_frames"), COL["tables"]),
    ]


def G(key, explode=(0, 0, 0), color=None, name=None):
    for k, n, keys, c in groups():
        if k == key:
            shape = fuse(*keys)
            if k == "tin":
                shape = win(shape, -2000, 2000, RY - 1000, RY, -10, 1000)
            elif k == "tout":
                shape = win(shape, -2000, 2000, RY, RY + 1000, -10, 1000)
            return part(name or n, shape, color or c, explode)
    raise KeyError(key)


# ----------------------------------------------------------------- overview
def overview():
    off = {"ds": (0, -600, 0), "tray": (500, -900, 0),
           "frame": (0, 0, -500), "rollers": (0, 0, -150), "brake": (0, 550, 0), "posts": (0, 0, 250),
           "beam": (0, 0, 650), "trolley": (0, 0, 950), "drop": (0, 0, 1200), "head": (-700, -650, 900),
           "hshaft": (-700, -1100, 1100), "ec": (650, -500, 600),
           "rsbase": (0, 1000, -650), "sides": (0, 1000, -250), "rolls": (0, 1000, 200), "blocks": (0, 1000, 500),
           "drive": (800, 1000, 0), "guards": (0, 1000, 850),
           "tin": (1700, 1300, -500), "tout": (1700, 700, 300)}
    parts = [G(k, off[k]) for k, *_ in groups()]
    return bv.overview(parts, OUT / "overview.png", "DrumPanel prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Front: drain stand; middle: cutting cradle; back: slip roll. "
                                "Seen from the front right and above",
                       elev=22, azim=-50, size=(13, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
SHEET_REVS = {}


def sheet(n, shape, name, color, neighbours, title, material, notes, view_shape=None, inset=(24, -58)):
    rev, date, revs = SHEET_REVS.get(n, ("P1", DATE, None))
    return bv.component_sheet(part(name, shape, color), neighbours, project="DrumPanel", dwg_no=f"DMP-DWG-{n}",
                              title=f"DrumPanel {title}: making sketch", material=material, notes=notes, date=date,
                              rev=rev, revisions=revs, view_shape=view_shape, inset_view=inset, out_dir=str(DWG))


def sheets(which=None):
    import build123d as b
    c = comps()
    grey = lambda *ks: [G(k) for k in ks]  # noqa: E731
    hl = m.shear_head_local()
    frames, bridges = side_parts()
    S = {}
    S[101] = lambda: sheet(101, fuse("ds_frame", "ds_chocks"), "Drain stand", COL["ds"],
        [K("drum_ds", color="#CBD5E1"), G("tray")], "drain and purge stand",
        "40 x 40 x 3 mm RHS, S275; hardwood chocks 40 x 60 mm",
        ["Two rails 800 mm long, 480 mm apart (centres), on four legs 260 mm",
         "  tall at the rail ends. Weld legs under the rails, square.",
         "Two saddles 560 mm long across the rails, 500 mm apart (centres),",
         "  welded on top of the rails. Top of the saddles 340 mm from the floor.",
         "Chocks: four hardwood blocks 40 x 60 mm, inner faces 300 mm apart.",
         "  70 mm tall on the far saddle, 45 mm tall on the bung-end saddle,",
         "  so the drum falls 2.9 degrees toward its bungs. Screw them down.",
         "Fit: the drum body rests on the four inner top edges of the chocks,",
         "  bung end low and over the tray. Nothing else holds it.",
         "Loads: a drum full of water is about 240 kg; 691 N on each chock.",
         "Check: frame stands level without rocking; the drum, rolled on,",
         "  sits on all four chocks and does not roll off sideways."], inset=(22, -55))
    S[102] = lambda: sheet(102, c["frame"].shape, "Cradle frame", COL["frame"], grey("rollers", "posts", "brake"),
        "cradle frame", "50 x 50 x 3 mm RHS, S275; 6 mm foot plates; M12 nuts",
        ["Two side rails 1,550 mm long, outer faces 700 mm apart.",
         "Six cross members 600 mm long between the rails, centred 520, 675",
         "  and 750 mm each side of the middle (the last one flush with the ends).",
         "Four legs 192 mm long under the corners, each with a 60 x 60 x 6 mm",
         "  foot plate and an M12 nut welded on it for a levelling foot.",
         "Top of the frame 273.5 mm from the floor with the feet screwed in",
         "  13 mm. Weld on a flat table; check the diagonals agree within 2 mm.",
         "Holes, 11 mm: two for each pillow block on the 520 mm members,",
         "  137.5 and 242.5 mm each side of the centre line; four for each post",
         "  base, 70 mm each side of the centre line on the 675 and 750 members.",
         "Fit: pillow blocks and post bases bolt on top with M10; the brake",
         "  post bolts to the outer face of a side rail at the middle.",
         "Check: frame top flat within 2 mm when the feet are set."], inset=(26, -50))
    S[103] = lambda: sheet(103, comp([win(c["shafts"].shape, -600, 600, -300, 0, 0, 500),
                                       win(c["rollers"].shape, -600, 600, -300, 0, 0, 500)]),
        "Roller shaft with rollers", COL["roller"], grey("frame") + [K("pillow", color="#CBD5E1")],
        "roller shaft with two rollers (make 2)", "25 mm bright steel bar; 101.6 x 4 mm tube; 10 mm plate discs",
        ["Make two. Shaft: 25 mm bright bar, 1,120 mm long, ends chamfered.",
         "Rollers: 101.6 x 4 mm tube cut 100 mm long; two 10 mm discs",
         "  93 mm across, bored 25 mm, welded into each end of the tube.",
         "Slide two rollers on, centred 147 mm each side of the middle of the",
         "  shaft (294 mm apart, under the drum's rolling hoops).",
         "Weld each disc to the shaft all round; skim the roller faces true",
         "  in a lathe if they run out more than 0.5 mm.",
         "Fit: the shaft runs in two UCP205 pillow blocks, 1,040 mm apart,",
         "  grub screws tightened on the shaft. Shaft centres 380 mm apart.",
         "Check: the shaft turns freely by hand in its blocks; the rollers",
         "  run true within 0.5 mm."], inset=(24, -58))
    S[104] = lambda: sheet(104, c["brake"].shape, "Drum brake", COL["brake"], grey("frame", "rollers") + [K("drum", color="#CBD5E1")],
        "drum brake", "40 x 40 x 3 mm RHS; M16 x 200 screw; 16 mm bar; rubber pad",
        ["Post: 40 x 40 x 3 mm RHS, 460 mm long. Two 11 mm holes through it,",
         "  25 mm apart, 56 and 81 mm up from its foot, to bolt it to the rail.",
         "An 18 mm hole through both walls 423 mm up from its foot; weld an",
         "  M16 nut over the hole on the outer face (away from the drum).",
         "Screw: M16 x 200; weld a 16 mm bar 160 mm long across its head as",
         "  a T-handle. A 60 mm rubber pad 15 mm thick on a swivel plate at",
         "  its tip faces the drum.",
         "Fit: post bolted with 2 x M10 to the outer face of the right side",
         "  rail at the middle of the frame. Screwed in, the pad presses on",
         "  the drum side between the hoops at the height of the drum axis.",
         "Check: with the screw tight the drum cannot be turned by hand."], inset=(20, -35))
    S[105] = lambda: sheet(105, win(c["posts"].shape, 0, 2000, -200, 200, 0, 2000), "Rail post", COL["posts"],
        grey("frame", "beam"), "rail post (make 2)", "60 x 60 x 4 mm RHS; 10 mm plate; S275",
        ["Make two. Post: 60 x 60 x 4 mm RHS, 926.5 mm long, square ends.",
         "Base plate 200 x 100 x 10 mm: four 11 mm holes on a 75 x 140 mm",
         "  rectangle (75 mm along the frame, 140 mm across it).",
         "Cap plate 120 x 80 x 10 mm: two 11 mm holes on the centre line,",
         "  80 mm apart (40 mm each side of the post).",
         "Weld the post to the middle of both plates, square both ways;",
         "  check with a square before the welds cool.",
         "Fit: the base bolts across the two end cross members of the frame",
         "  with 4 x M10 x 80; the rail beam sits on the cap and is held by",
         "  two M10 through-bolts. Post centre 712.5 mm from the middle.",
         "Check: post upright within 1 mm over its height when bolted."], inset=(22, -50))
    S[106] = lambda: sheet(106, c["beam"].shape, "Rail beam", COL["beam"], grey("posts", "trolley"),
        "rail beam", "80 x 40 x 3 mm RHS, S275; 14 mm tube",
        ["Rail beam: 80 x 40 x 3 mm RHS, 1,540 mm long, stood on its narrow",
         "  edge (80 mm tall). The top face is the trolley track: keep it",
         "  clean and free of weld spatter; file any seam bead flat.",
         "Holes: two 11 mm vertical holes through both walls at each end,",
         "  17.5 and 97.5 mm from the end, on the centre line.",
         "Crush tubes: 14 mm tube 74 mm long inside the beam at each hole",
         "  so the through-bolts do not crush it.",
         "Fit: each end sits on a post cap, held by two M10 x 110 bolts;",
         "  the bolt heads on top stop the trolley at the ends.",
         "Check: the top face is straight within 1 mm over its length",
         "  (a taut string or a straightedge)."], inset=(22, -50))
    S[107] = lambda: sheet(107, c["trolley"].shape, "Trolley", COL["trolley"], grey("beam") + [K("trolley_wheels", color="#CBD5E1")],
        "trolley with swivel plate", "6 mm and 12 mm plate, S275; four 6202-2RS bearings; 15 mm bar",
        ["Two side plates 180 x 164 x 6 mm. Four 15.5 mm axle holes in each,",
         "  60 mm each side of the middle, 141.5 and 25.5 mm up from the",
         "  bottom edge. Drill the two plates clamped together.",
         "Swivel plate 180 x 58 x 12 mm, welded under both side plates so",
         "  their inner faces are 46 mm apart (beam 40 mm, 3 mm each side).",
         "Pivot hole 31 mm in the middle of the swivel plate; two 10.5 mm",
         "  index holes 45 mm from it, at 0 and 90 degrees.",
         "Wheels: 6202-2RS bearings on 15 mm axles with spacers; two ride on",
         "  top of the beam and two run 1 mm under it (anti-lift).",
         "Fit: slide on from the beam end before the end bolts go in, or",
         "  drop on from above and fit the lower axles after.",
         "Check: rolls the full length by hand, no tight spots."], inset=(24, -50))
    S[108] = lambda: sheet(108, fuse("drop", "pivot"), "Drop bar and head plate", COL["drop"],
        grey("trolley", "head"), "drop bar, head plate and pivot pin", "50 x 50 x 4 mm RHS; 12 mm plate; 30 mm bar",
        ["Head plate 120 x 120 x 12 mm: a 31 mm hole in the middle for the",
         "  pivot pin and a 10.5 mm hole 45 mm from it for the index pin.",
         "Drop bar: 50 x 50 x 4 mm RHS, 126 mm long, welded square under",
         "  the head plate, centred, and at its lower end to the middle of",
         "  the shear head's top plate (over the nip line).",
         "Pivot pin: 30 mm bar 55 mm long with a 40 mm collar welded at its",
         "  top; a 6 mm hole for an R-clip under the swivel plate.",
         "Index pin: 10 mm, on a lanyard, through the head plate into one",
         "  of the two holes in the swivel plate: slit or ring position.",
         "Fit: the head hangs from the trolley on the pivot pin and turns",
         "  through 90 degrees when the index pin is out.",
         "Check: the head swings freely; the index pin drops in at both",
         "  positions."], inset=(24, -50))
    S[109] = lambda: sheet(109, hl["frame"], "Shear head frame", COL["hframe"],
        [part("Discs and shafts", comp([hl["disc_u"], hl["disc_l"], hl["shaft_u"], hl["shaft_l"]]), "#CBD5E1")],
        "rotary shear head frame", "10 mm and 20 mm plate, S275; 6005-2RS bearings; eccentric bush",
        ["Web: 10 mm plate 92 x 232 mm. It runs in the cut, behind the discs.",
         "Top plate 195 x 99 x 20 mm and lower plate 195 x 79 x 20 mm,",
         "  welded across the top and bottom ends of the web.",
         "Upper housing 90 x 60 x 101 mm on the top plate, beside the web;",
         "  bore 57 mm on a line 49.5 mm above the nip for the eccentric bush",
         "  (57 mm outside, 47 mm bore offset 3 mm) and one 6005 bearing.",
         "Lower housing 90 x 60 x 96 mm under the lower plate; bore 47 mm",
         "  on a line 49.5 mm below the nip for two 6005 bearings.",
         "Bore both housings in one setting so the shafts are parallel",
         "  within 0.05 mm over 60 mm; the disc faces must meet on one plane.",
         "Fit: the drop bar is welded to the top plate over the nip line.",
         "Check: turning the eccentric moves the upper shaft 6 mm."],
        inset=(20, -40))
    S[110] = lambda: sheet(110, comp([hl["shaft_u"], hl["shaft_l"]]), "Head shafts and crank", COL["hshaft"],
        [part("Head frame", hl["frame"], "#CBD5E1"), part("Discs", comp([hl["disc_u"], hl["disc_l"]]), "#E5E7EB")],
        "head shafts and crank", "25 mm bright bar; 20 x 12 mm flat; 16 mm pin; bought D2 discs",
        ["Upper shaft: 25 mm, 78 mm long, with a 35 mm shoulder 10 mm from",
         "  the disc end and a 6 mm keyway at the crank end.",
         "Crank: 40 mm boss 12 mm thick, arm 20 x 12 mm, 200 mm between",
         "  centres; 24 mm grip 100 mm long, free to spin on a 16 mm pin.",
         "Lower shaft: 25 mm, 74 mm long, same shoulder; no crank.",
         "Discs (bought): 101 x 10 mm D2, hardened 58 to 60 HRC, 25 mm bore.",
         "  Each is clamped against its shoulder by a countersunk M8 end screw",
         "  and washer that sit below the cutting face.",
         "Fit: cutting faces meet on the cut plane with no gap and no rub;",
         "  shim behind a disc with 0.05 mm shims to get there.",
         "Set the overlap to 1.0 mm with the eccentric and lock it.",
         "Check: turning the crank turns the upper disc; a strip of",
         "  1 mm sheet cuts cleanly by hand."], inset=(20, -40))
    S[111] = lambda: sheet(111, hl["guard"], "Disc guard", COL["guard"],
        [part("Head frame and discs", comp([hl["frame"], hl["disc_u"], hl["disc_l"]]), "#CBD5E1")],
        "disc guard", "1.5 mm steel sheet, folded and welded",
        ["A hood over the upper disc: 1.5 mm sheet, 118 mm long, 18 mm wide",
         "  outside, 64 mm tall, with a 108 mm arched opening for the disc.",
         "Front skirt: a 10 mm deep plate down the front of the hood, ending",
         "  8 mm above the sheet line and 52 mm ahead of the nip, so a",
         "  finger cannot reach the nip from the front.",
         "A 26 mm hole in the back face for the upper shaft.",
         "Fit: two M5 screws into the upper housing; it does not touch the",
         "  disc (at least 2 mm clear all round).",
         "Check: with the head on a drum, nothing thicker than 8 mm passes",
         "  under the skirt; the guard is on before the crank is turned."],
        inset=(20, -40))
    S[112] = lambda: sheet(112, fuse("ec_body", "ec_guide", "ec_drive"), "End cutter", COL["ec"],
        [K("drum", color="#CBD5E1"), K("ec_cutter", color="#E5E7EB")] + grey("posts"),
        "end cutter", "12 mm plate; 16 and 12 mm bar; 30 x 8 mm flat; bought 50 mm cutter wheel",
        ["Body: 12 mm plate 160 x 120 mm, standing across the drum end.",
         "Drive shaft 16 mm in a 17 mm hole 20 mm up from the body's bottom",
         "  edge; on it a 40 mm knurled wheel 8 mm wide that bears on the",
         "  inside of the chime, and a 150 mm crank outside the body.",
         "Guide roller 30 mm on a 12 mm axle, 53.5 mm above the drive shaft,",
         "  runs on the outside of the chime: chime pinched between the two.",
         "Cutter arm: 12 mm rod from a link block on the body, 12 degrees",
         "  round from the top, carrying the 50 mm hardened wheel square to",
         "  the head, 4 mm inside the chime wall. An M12 clamp screw presses",
         "  it into the head; a 1.5 mm cover sits over the wheel.",
         "Torque arm: 30 x 8 mm flat, riser 88 mm, then 170 mm to the post.",
         "Check: on a drum the wheel cuts the head just inside the chime;",
         "  the torque arm rests on the post as the crank turns."], inset=(25, -40))
    S[113] = lambda: sheet(113, c["rs_base"].shape, "Roll stand base", COL["rsbase"], grey("sides", "tin", "tout"),
        "roll stand base", "60 x 60 x 3 mm RHS, S275",
        ["Two cross rails 800 mm long, 1,060 mm apart (centres).",
         "Two long rails 1,000 mm between them, at 120 mm in front of and",
         "  190 mm behind the pinch line (centres), flush on top.",
         "Weld on a flat floor or table; diagonals within 2 mm.",
         "Holes: four 13 mm holes in each long rail for the side frame feet",
         "  (two per foot, 50 mm apart), 467.5 mm each side of the middle.",
         "Fit: the side frame legs stand on foot plates bolted to the long",
         "  rails with 2 x M12 each. The cross rails stick out 400 mm each",
         "  way so the stand cannot tip.",
         "Check: rocks on no corner on a flat floor; shim if needed."], inset=(24, -50))
    S[114] = lambda: sheet(114, win(frames, 0, 2000, RY - 400, RY + 400, 0, 2000), "Side frame", COL["sides"],
        [part("Lower roll", comps()["roll_lower"].shape, "#CBD5E1")] + grey("rsbase"),
        "side frame (make 2, mirror pair)", "20 mm plate 370 x 250; 50 x 50 x 3 RHS legs; 6 mm foot plates; S275",
        ["Make two (mirror pair). Plate 20 mm, 370 x 250 mm.",
         "Bore 40 mm for the lower roll bush: 110 mm up from the plate's",
         "  bottom edge, 150 mm from its front edge.",
         "Pinch slot 60 mm wide from 140 mm up to the top, centred over the",
         "  bore. Bending slot 60 mm wide from 80 mm up to the top, centred",
         "  90 mm behind the bore. File both slots smooth and parallel.",
         "Legs: 50 x 50 x 3 RHS 694 mm long under the plate at 30 mm and",
         "  340 mm from the front edge, with 80 x 80 x 6 mm foot plates.",
         "Top bridge (bolted, not welded): 25 x 25 mm bar 370 mm long with",
         "  M16 and M20 threaded holes over the slots; 2 x M10 into the plate.",
         "Fit: plate inner faces 920 mm apart; legs bolted to the base.",
         "Check: both bores line up within 0.5 mm (a 30 mm bar through)."],
        inset=(22, -55))
    S[115] = lambda: sheet(115, c["roll_lower"].shape, "Lower pinch roll", COL["roll"],
        [K("rs_bushes", color="#CBD5E1"), part("Side frames", frames, "#E5E7EB")],
        "rolls (make 3; the lower pinch roll drawn)", "60 mm bright bar C45 (EN8)",
        ["All three rolls: 60 mm bright bar, 900 mm face, ends faced square.",
         "Journals turned to 30 mm, a sliding fit in the bronze bushes",
         "  (0.05 to 0.10 mm clear). Small fillet at each shoulder.",
         "Lower pinch roll (drawn): 1,092 mm overall; gear-end journal 90 mm,",
         "  sprocket-end journal 102 mm; keyways for the gear and sprocket.",
         "Upper pinch roll: 1,032 mm; gear-end journal 90 mm, other 42 mm;",
         "  keyway for the gear.",
         "Bending roll: 984 mm; both journals 42 mm; no keyways.",
         "Turn between centres; run-out of the face within 0.05 mm.",
         "Fit: pinch rolls one above the other at 61 mm centres (1 mm",
         "  sheet); bending roll 90 mm behind, set by its screws.",
         "Check: each roll turns freely in its bushes by hand."], inset=(22, -55))
    S[116] = lambda: sheet(116, fuse("rs_blocks", "rs_screws", "rs_bushes"), "Slide blocks, bushes and screws", COL["blocks"],
        [part("Side frames", frames, "#E5E7EB"), part("Rolls", fuse("roll_lower", "roll_upper", "roll_bend"), "#CBD5E1")],
        "slide blocks, bushes and screws", "20 mm steel plate; bronze bushes; M16 and M20 screws",
        ["Four slide blocks, 60 x 60 x 20 mm (20 mm thick = the side plate),",
         "  bored 40 mm in the middle for a flanged bronze bush.",
         "  Fit in the 60 mm slots with 0.2 mm clearance; break the edges.",
         "Six flanged bronze bushes 30 x 40 x 20 mm, 52 mm flange 6 mm",
         "  thick, pressed in from the outside; a grease hole in each.",
         "A 3 mm keeper plate on the inside face holds each block in.",
         "Pinch screws M16 x 120 (two), bending screws M20 x 150 (two),",
         "  each with a collar captured in the top of its block so it can",
         "  push and pull; handwheels 90 mm (pinch) and 110 mm (bending)",
         "  marked in 12 divisions.",
         "Fit: the screws run in the threaded holes of the top bridges.",
         "Check: each block slides its full travel by turning its screw."],
        inset=(22, -55))
    S[117] = lambda: sheet(117, fuse("rs_bracket", "rs_crank"), "Crank bracket and crank", COL["bracket"],
        [part("Side frame", frames, "#E5E7EB"), K("sprockets", color="#CBD5E1")],
        "crank bracket and crank", "10 mm plate; 50 mm bar; 25 mm shaft; 24 x 12 mm flat",
        ["Bracket: 10 mm plate 190 x 120 mm, bolted to the outer face of the",
         "  right-hand side frame (front prong) with 4 x M10.",
         "Housing: 50 mm round bar 40 mm long bored 26 mm for two bronze",
         "  bushes, welded square to the bracket, 230 mm in front of the",
         "  pinch line and 50 mm below the lower roll centre.",
         "Crank shaft: 25 mm, 90 mm long; keyway for the 13 tooth sprocket.",
         "Crank: arm 24 x 12 mm, 300 mm between centres; 28 mm grip 88 mm",
         "  long, free to spin.",
         "Sprockets #40: 13 teeth on the crank shaft, 39 teeth on the lower",
         "  roll; line them up with a straightedge; chain slack 5 mm.",
         "Fit: the chain guard bolts over both sprockets.",
         "Check: one crank turn moves the sheet 63 mm."], inset=(22, -40))
    S[118] = lambda: sheet(118, c["rs_guards"].shape, "Roll guards", COL["rsguard"],
        [part("Side frames, rolls", comp([frames, fuse("roll_lower", "roll_upper", "roll_bend")]), "#CBD5E1")],
        "roll guards", "1.5 mm steel sheet, folded; M6 screws",
        ["In-feed guard: 920 x 92 mm, 50 mm in front of the pinch line; its",
         "  lower edge 8 mm above the in-feed table, rolled to a 4 mm radius.",
         "Out-feed guard: 920 x 79 mm, 150 mm behind the pinch line, lower",
         "  edge 8 mm above the out-feed table.",
         "Lid: 920 x 204 mm, joining the two guards over the rolls.",
         "Chain guard: a box 30 x 355 x 180 mm round both sprockets, with",
         "  holes for the shafts; bolted to the crank bracket housing.",
         "Gear guard: a box 65 x 90 x 145 mm over the pinch gears, bolted",
         "  to the left-hand side frame.",
         "All guards held by M6 screws: a tool is needed to take them off.",
         "Check: a 10 mm rod cannot reach any nip, gear or sprocket."],
        inset=(22, -55))
    S[119] = lambda: sheet(119, fuse("tables", "table_frames"), "Tables", COL["tables"], grey("sides", "rsbase"),
        "in-feed and out-feed tables", "18 mm exterior plywood; 40 x 40 x 3 mm angle and RHS",
        ["In-feed table: plywood 900 x 815 mm on an angle frame, four RHS",
         "  legs; top 900 mm from the floor, level with the top of the",
         "  lower roll; front edge 35 mm short of the roll.",
         "Out-feed table: plywood 900 x 810 mm on a similar frame; top",
         "  913 mm from the floor, level with the top of the bending roll at",
         "  its usual setting; starts 125 mm behind the pinch line.",
         "Legs: 40 x 40 x 3 RHS with M10 levelling screws.",
         "Seal the plywood; countersink the screws so the panels do not",
         "  catch.",
         "Check: a straightedge from each table to its roll shows no step",
         "  over 1 mm."], inset=(22, -55))
    keys = sorted(S) if not which else [int(w) for w in which]
    out = []
    for k in keys:
        out.append(S[k]())
        print("sheet", k, "->", out[-1], flush=True)
    return out


# ----------------------------------------------------------------- joints
def joints(which=None):
    import build123d as b
    c = comps()
    hl = m.shear_head_local()
    frames, bridges = side_parts()
    J = {}
    bx = None
    J[1] = lambda bx=bx: bv.joint([W("ds_frame", "Saddle (40 x 40 RHS)", COL["ds"], (-290, -210, -1800, -1200, 250, 420)),
                             W("ds_chocks", "Chocks: drum rests on the inner top edges", COL["chock"], (-290, -210, -1800, -1200, 250, 420)),
                             W("drum_ds", "Drum body", "#93C5FD", (-290, -210, -1800, -1200, 250, 520))],
                            OUT / "joint-01.png", "Joint 1: drum on the drain stand chocks",
                            "Cut through the far saddle; the drum touches only the chocks' inner top edges", elev=10, azim=180)
    bx = (440, 600, 60, 320, 200, 380)
    J[2] = lambda bx=bx: bv.joint([W("frame", "Cross member", COL["frame"], bx), W("pillow", "Pillow block UCP205", COL["pillow"], bx),
                             W("shafts", "Roller shaft 25 mm", COL["shaft"], bx)],
                            OUT / "joint-02.png", "Joint 2: pillow block on the cradle frame",
                            "Two M10 bolts through the cross member; grub screws on the shaft", elev=26, azim=-50)
    bx = (640, 790, -130, 130, 200, 420)
    J[3] = lambda bx=bx: bv.joint([W("frame", "End cross members (2)", COL["frame"], bx), W("posts", "Post base plate and post", COL["posts"], bx),
                             W("bolts", "M10 x 80 bolts (4)", COL["bolts"], bx)],
                            OUT / "joint-03.png", "Joint 3: rail post base on the cradle frame",
                            "Cut open at the post centre line; four bolts through two cross members", cut="+Y", elev=22, azim=-60)
    bx = (630, 790, -60, 60, 1150, 1330)
    J[4] = lambda bx=bx: bv.joint([W("posts", "Post and cap plate", COL["posts"], bx), W("beam", "Rail beam", COL["beam"], bx),
                             W("bolts", "M10 through-bolts (2)", COL["bolts"], bx)],
                            OUT / "joint-04.png", "Joint 4: rail beam on a post cap",
                            "Cut open along the beam; bolt heads on top stop the trolley", cut="+Y", elev=20, azim=-60)
    bx = (XN - 120, XN + 120, -60, 60, 1130, 1360)
    J[5] = lambda bx=bx: bv.joint([W("beam", "Rail beam", COL["beam"], bx), W("trolley", "Trolley side plates and swivel plate", COL["trolley"], bx),
                             W("trolley_wheels", "Wheels: two on top, two underneath", COL["wheels"], bx),
                             W("drop", "Head plate", COL["drop"], bx), W("pivot", "Pivot pin", COL["pivot"], bx)],
                            OUT / "joint-05.png", "Joint 5: trolley on the rail beam, head on its pivot",
                            "Cut open across the beam at the wheels", cut="-Y", elev=14, azim=-30)
    dw = b.Pos(0, 0, ZAX) * m.drum(P, heads=False)
    dw = dw - box(-1000, P["DISC_R"] * 0.2, -11, 11, ZAX, ZAX + 400)
    wall = win(dw, -170, 120, -110, 110, ZNIP - 40, ZNIP + 20)
    pl = b.Pos(0, 0, ZNIP)
    J[6] = lambda bx=bx: bv.joint([part("Head frame: web in the cut", pl * hl["frame"], COL["hframe"]),
                             part("Discs: upper driven, lower idle", comp([pl * hl["disc_u"], pl * hl["disc_l"]]), COL["discs"]),
                             part("Shafts and crank", comp([pl * hl["shaft_u"], pl * hl["shaft_l"]]), COL["hshaft"]),
                             part("Drum wall, cut behind the nip", wall, "#93C5FD")],
                            OUT / "joint-06.png", "Joint 6: shear head on the drum wall, slitting",
                            "Guard left off; the cut edges spread round the 10 mm web", elev=20, azim=-35)
    bx = (390, 560, -120, 120, ZAX + 200, ZAX + 470)
    J[7] = lambda bx=bx: bv.joint([W("drum", "Drum chime and head", "#93C5FD", bx), W("ec_body", "Body, cutter arm, cover, torque arm", COL["ec"], bx),
                             W("ec_guide", "Guide roller", COL["ecguide"], bx), W("ec_drive", "Drive wheel, shaft, crank", COL["ecdrive"], bx),
                             W("ec_cutter", "Cutter wheel", COL["ecwheel"], bx)],
                            OUT / "joint-07.png", "Joint 7: end cutter on the chime",
                            "Cut open at the top of the drum, seen from the right; the chime is pinched between the drive wheel and the guide roller",
                            cut="-Y", elev=15, azim=60)
    bx = (60, 240, -320, 80, 240, 700)
    J[8] = lambda bx=bx: bv.joint([W("rollers", "Roller under the hoop", COL["roller"], bx), W("shafts", "Shaft", COL["shaft"], bx),
                             W("drum", "Drum hoop and body", "#93C5FD", (60, 240, -320, 80, 240, 700))],
                            OUT / "joint-08.png", "Joint 8: drum hoop on a cradle roller",
                            "Cut through the hoop; contact 33 degrees from vertical on each side",
                            elev=10, azim=-20)
    bx = (420, 520, RY - 160, RY + 230, 750, 1040)
    J[9] = lambda bx=bx: bv.joint([part("Side frame plate and leg", win(frames, *bx), COL["sides"]),
                             part("Top bridge (bolted)", win(bridges, *bx), "#0D9488"),
                             W("rs_bushes", "Bronze bushes", COL["bush"], bx), W("rs_blocks", "Slide blocks", COL["blocks"], bx),
                             W("rs_screws", "Pinch and bending screws", COL["screws"], bx),
                             W("roll_lower", "Lower roll", COL["roll"], bx), W("roll_upper", "Upper roll", "#A3A3A3", bx),
                             W("roll_bend", "Bending roll", COL["roll"], bx)],
                            OUT / "joint-09.png", "Joint 9: rolls in a side frame",
                            "Right-hand frame from outside: fixed lower bush, upper and bending blocks in their slots", elev=8, azim=-8)
    bx = (-560, -440, RY - 60, RY + 130, 820, 990)
    J[10] = lambda bx=bx: bv.joint([W("gears", "Pinch gears m3 x 20 teeth", COL["gears"], bx), W("roll_lower", "Lower roll", COL["roll"], bx),
                              W("roll_upper", "Upper roll", "#A3A3A3", bx), W("roll_bend", "Bending roll (no gear)", COL["roll"], bx),
                              part("Left side frame", win(frames, *bx), COL["sides"])],
                             OUT / "joint-10.png", "Joint 10: pinch gears at the left-hand end",
                             "Gear guard off; the gears keep the pinch rolls turning together", elev=12, azim=-150)
    bx = (470, 680, RY - 300, RY + 100, 760, 1140)
    J[11] = lambda bx=bx: bv.joint([W("rs_bracket", "Crank bracket and housing", COL["bracket"], bx), W("rs_crank", "Crank shaft and crank", COL["crank"], bx),
                              W("sprockets", "Sprockets 13 and 39 teeth", COL["sprocket"], bx), W("roll_lower", "Lower roll journal", COL["roll"], bx),
                              part("Side frame", win(frames, *bx), COL["sides"])],
                             OUT / "joint-11.png", "Joint 11: crank and chain drive",
                             "Chain guard off; chain not drawn; 3 to 1 reduction", elev=12, azim=-20)
    bx = (-40, 40, RY - 200, RY + 260, 840, 1010)
    J[12] = lambda bx=bx: bv.joint([W("rs_guards", "In-feed guard, lid, out-feed guard", COL["rsguard"], bx),
                              W("roll_lower", "Lower roll", COL["roll"], bx), W("roll_upper", "Upper roll", "#A3A3A3", bx),
                              W("roll_bend", "Bending roll", COL["roll"], bx), W("tables", "Tables", COL["tables"], bx),
                              W("sheet", "Panel being fed", COL["sheet"], bx)],
                             OUT / "joint-12.png", "Joint 12: nip guards over the rolls",
                             "Cut at the middle of the rolls, seen from the right; 8 mm slots over the tables", elev=4, azim=0)
    keys = sorted(J) if not which else [int(w) for w in which]
    out = []
    for k in keys:
        out.append(J[k]())
        print("joint", k, "->", out[-1], flush=True)
    return out


# ----------------------------------------------------------------- assembly steps
def steps(which=None):
    import build123d as b
    frames, bridges = side_parts()
    out = []
    E = {}

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))
        print("step", n, "->", out[-1], flush=True)

    def mv(p, e, name=None):
        return part(name or p.name, p.shape, p.color, e)

    dsf = K("ds_frame", "Drain stand frame", COL["ds"])
    E[1] = lambda: st(1, [dsf], [mv(K("ds_chocks", "Chocks (4)", COL["chock"]), (0, 0, 250)), mv(K("tray", "Drain tray", COL["tray"]), (300, 0, 0))],
                      "drain stand chocks and tray", "Screw the chocks to the saddles, tall pair at the far end; tray under the bung end",
                      elev=26, azim=-50)
    frame = K("frame", "Cradle frame", COL["frame"])
    feet = K("feet", "Levelling feet", COL["feet"])
    E[2] = lambda: st(2, [], [mv(frame, (0, 0, 300)), mv(feet, (0, 0, -150))], "cradle frame on its levelling feet",
                      "Screw the feet in 13 mm; level the frame both ways within 1 mm", elev=24, azim=-50)
    rol = G("rollers")
    E[3] = lambda: st(3, [frame, feet], [mv(K("pillow", "Pillow blocks (4)", COL["pillow"]), (0, 0, 200)),
                                         mv(part("Roller shafts with rollers (2)", fuse("shafts", "rollers"), COL["roller"]), (0, 0, 400))],
                      "pillow blocks and roller shafts", "Bolt the blocks on loosely, drop the shafts in, align, then tighten and lock the grub screws",
                      elev=26, azim=-50, label_done=False)
    brake = K("brake", "Drum brake", COL["brake"])
    E[4] = lambda: st(4, [frame, feet, rol], [mv(brake, (0, 300, 0))], "drum brake",
                      "Bolt the post to the outer face of the right side rail at the middle; screw backed off", elev=24, azim=-40,
                      label_done=False)
    posts = G("posts")
    E[5] = lambda: st(5, [frame, feet, rol, brake], [mv(posts, (0, 0, 500))], "rail posts",
                      "Each post base across the two end cross members, four M10 bolts; check upright", elev=22, azim=-50,
                      label_done=False)
    beam = K("beam", "Rail beam", COL["beam"])
    trol = G("trolley")
    cradle0 = [frame, feet, rol, brake, posts]
    E[6] = lambda: st(6, cradle0, [mv(beam, (0, 0, 450)), mv(trol, (-900, 0, 450), "Trolley, slid on from the end")],
                      "rail beam and trolley", "Slide the trolley onto the beam end, then lift the beam onto the caps and bolt it",
                      elev=22, azim=-50, label_done=False)
    drop = G("drop")
    head = K("head_frame", "Shear head frame", COL["hframe"])
    E[7] = lambda: st(7, cradle0 + [beam, trol], [mv(part("Shear head with drop bar and pivot pin", fuse("drop", "pivot", "head_frame"),
                                                           COL["hframe"]), (0, -450, -150))],
                      "shear head onto the trolley", "Two people: lift the head, pivot pin up through the swivel plate, R-clip; index pin in",
                      elev=20, azim=-40, label_done=False)
    hs = G("hshaft")
    E[8] = lambda: st(8, cradle0 + [beam, trol, drop, head], [mv(hs, (0, -300, 0))], "shafts, discs and guard",
                      "Fit the shafts in their bearings, discs on, set 1.0 mm overlap with the eccentric; guard on",
                      elev=20, azim=-40, label_done=False)
    drum = K("drum", "Drum (heads on)", "#CBD5E1")
    ec = G("ec")
    E[9] = lambda: st(9, cradle0 + [beam, trol, drop, head, hs, drum], [mv(ec, (300, 0, 200))], "drum on, end cutter on the chime",
                      "Roll a purged drum onto the rollers; hook the cutter over the right chime, torque arm against the post",
                      elev=20, azim=-40, label_done=False)
    base = K("rs_base", "Roll stand base", COL["rsbase"])
    E[10] = lambda: st(10, [], [mv(base, (0, 0, -200))], "roll stand base", "Set it where the panels can be fed and taken off; level it",
                       elev=24, azim=-50)
    lower = part("Lower roll with its bushes", comp([comps()["roll_lower"].shape,
                                                     win(comps()["rs_bushes"].shape, -2000, 2000, RY - 20, RY + 20, 840, 900)]), COL["roll"])
    side = part("Side frames (2)", frames, COL["sides"])
    E[11] = lambda: st(11, [base], [mv(lower, (0, 0, 500)), mv(side, (0, 0, 250))], "side frames on the lower roll",
                       "Bushes on the journals, offer both frames onto them, then bolt the feet to the base (2 x M12 each)",
                       elev=22, azim=-50, label_done=False)
    upper = part("Upper roll, blocks, bushes", comp([comps()["roll_upper"].shape,
                                                     win(comps()["rs_blocks"].shape, -2000, 2000, RY - 40, RY + 40, 890, 970),
                                                     win(comps()["rs_bushes"].shape, -2000, 2000, RY - 40, RY + 40, 890, 970)]), "#A3A3A3")
    bend = part("Bending roll, blocks, bushes", comp([comps()["roll_bend"].shape,
                                                      win(comps()["rs_blocks"].shape, -2000, 2000, RY + 50, RY + 130, 840, 930),
                                                      win(comps()["rs_bushes"].shape, -2000, 2000, RY + 50, RY + 130, 840, 930)]), COL["roll"])
    E[12] = lambda: st(12, [base, side, lower], [mv(upper, (0, 0, 350)), mv(bend, (0, 250, 350))], "upper and bending rolls into the slots",
                       "Lower each roll with its blocks down its pair of slots; keeper plates on the inside faces",
                       elev=22, azim=-50, label_done=False)
    br = part("Top bridges with screws", comp([bridges, comps()["rs_screws"].shape]), COL["screws"])
    E[13] = lambda: st(13, [base, side, lower, upper, bend], [mv(br, (0, 0, 250))], "top bridges and screws",
                       "Bolt the bridges across the slot tops; engage the screw collars in the blocks", elev=22, azim=-50,
                       label_done=False)
    rolls = [base, side, lower, upper, bend, br]
    gears = K("gears", "Pinch gears", COL["gears"])
    E[14] = lambda: st(14, rolls, [mv(gears, (-250, 0, 0))], "pinch gears", "Key both gears on at the left-hand end; set the mesh with 1 mm sheet in the pinch",
                       elev=18, azim=-130, label_done=False)
    drv = G("drive")
    E[15] = lambda: st(15, rolls + [gears], [mv(drv, (300, -150, 0))], "crank, sprockets and chain",
                       "Bolt the bracket to the right-hand frame; sprockets in line; chain on with 5 mm slack", elev=18, azim=-30,
                       label_done=False)
    grd = K("rs_guards", "Guards: nip guards, lid, chain and gear guards", COL["rsguard"])
    E[16] = lambda: st(16, rolls + [gears, drv], [mv(grd, (0, 0, 300))], "guards", "Screw all guards on; check the 8 mm slots over the tables",
                       elev=22, azim=-50, label_done=False)
    tab = part("In-feed and out-feed tables", fuse("tables", "table_frames"), COL["tables"])
    E[17] = lambda: st(17, rolls + [gears, drv, grd], [mv(tab, (0, 0, 300))], "in-feed and out-feed tables",
                       "Stand the tables at each side, tops level with the rolls; screw the legs to the floor or the base",
                       elev=24, azim=-50, label_done=False)
    keys = sorted(E) if not which else [int(w) for w in which]
    for k in keys:
        E[k]()
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        overview(); sheets(); joints(); steps()
    elif a[0] == "overview":
        print(overview())
    elif a[0] == "sheets":
        sheets(a[1:])
    elif a[0] == "joints":
        joints(a[1:])
    elif a[0] == "steps":
        steps(a[1:])
