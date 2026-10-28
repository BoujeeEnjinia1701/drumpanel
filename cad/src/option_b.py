"""DrumPanel option B, lever shear and stretch leveller, detailed to D3 (kit 1.9, STANDARDS section 24).

A concept option with a different working principle from option A (DMP-OPT-001), modelled to the same detail level
(Amish, 2026-10-24: "Detail every option"); it is not carried to the drawing, BOM or build plan.

    Cut by blades: a deep-throat lever shear with straight D2 blades stands at the end of the roller cradle. Its lower
    jaw enters the open drum along the axis; a 1,050 mm hand lever drives the upper blade arm through a crank and link
    (about 22 to 1 at the cut). The heads come out first, cut round inside the chime from the 2 in bung hole; then the
    chime rings, the hoop strips and the slit, the drum rolled or slid on the cradle between strokes.
    Flatten by stretching: each curled panel is gripped 60 mm at each end in self-tightening wedge grips on a channel
    bed and stretched about 2 % past yield by a 15 t hand-pumped hydraulic cylinder, so it comes off flat.

The drain and purge stand, the roller cradle frame, rollers, pillow blocks and drum brake are the same as option A's
(cad/src/option_a.py). Axes and units as in cad/src/model.py. CONCEPT, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Plane, Polygon, Pos, Rot, extrude, Cylinder  # noqa: E402
import cad_parts as cp  # noqa: E402
import dmp_parts as D  # noqa: E402
from dmp_parts import (box, eased, rod, ring, rhs_run, tube_run, bolt_set, tap_screw, weld_line, ring_weld, box_welds,  # noqa: E402
                       hole, washer_at, split_pin_at, split_pin_hole)
import model as M  # noqa: E402
import option_a as A  # noqa: E402

P = M.PARAMS
PS, BRIGHT, YEL = "painted_steel", "mild_steel", "safety_yellow"


def ccw(pts):
    """Order a closed outline counter-clockwise, so that its face extrudes along +Z of its plane."""
    a = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]))
    return pts if a > 0 else list(reversed(pts))


def plate_xz(pts, y0, y1):
    """A plate cut to an outline drawn in the XZ plane, from y0 to y1, edges broken."""
    pl = Plane(origin=(0, y1, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    return cp.break_edges(pl.location * extrude(Polygon(*pts, align=None), y1 - y0), 1.0)


def channel_x(x0, x1, y_web, out, z_top, h=100.0, b=50.0, t=6.0, tf=8.5):
    """UPN channel along X: web vertical at y_web (outer face), flanges pointing 'out' (+1 or -1 in Y), top at z_top."""
    s = cp.channel(h, b, t, x1 - x0, tf)          # web along local Y, flanges toward +X, along +Z
    if out > 0:
        pl = Plane(origin=(x0, y_web, z_top - h / 2), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    else:
        pl = Plane(origin=(x1, y_web, z_top - h / 2), x_dir=(0, -1, 0), z_dir=(-1, 0, 0))
    return pl.location * s


# =================================================================================================================
# Deep-throat lever shear (frame: cut point at the origin, cut line along X, jaws toward -X, shear plane y = 0)
# =================================================================================================================
SIDE = [(-130, -100), (520, -100), (520, 240), (250, 240), (250, 160), (-40, 160), (-40, 25), (450, 25), (450, -3), (-130, -3)]
ARM_PIV, LINK_A, HUB, CRANK = (150.0, 70.0), (290.0, 70.0), (340.0, 190.0), (325.0, 164.0)


def shear_parts():
    o = A.Out()
    g, key = "shear", "b_shear"
    holes = {ARM_PIV: 10.2, HUB: 10.2, LINK_A: 19.0, CRANK: 19.0}
    for sy in (-1, 1):
        y0, y1 = (12.0, 28.0) if sy > 0 else (-28.0, -12.0)
        pl = plate_xz(SIDE, y0, y1)
        for (x, z), r in holes.items():
            pl = pl - hole((x, (y0 + y1) / 2, z), "+y", r, 20)
        for x in (-100.0, -40.0):
            pl = pl - hole((x, (y0 + y1) / 2, -18), "+y", 5.5, 20)
        o.part(f"Shear C-frame side plate, {'back' if sy > 0 else 'front'} (16 mm S355, 450 mm throat)", pl, PS, "made", None, key, g, color="#0F766E")
    o.part("Shear lower spacer bar (24 x 40 bar, welded)", eased(-10, 450, -12, 12, -100, -60, 0.8), PS, "made", None, key, g, color="#0F766E")
    o.part("Shear spine block (60 x 24 bar, welded)", eased(455, 515, -12, 12, -95, 235, 0.8), PS, "made", None, key, g, color="#0F766E")
    o.part("Shear front spacer (35 x 24 bar, welded)", eased(-35, 0, -12, 12, 120, 155, 0.8), PS, "made", None, key, g, color="#0F766E")
    for sy in (-1, 1):
        v = "-y" if sy > 0 else "+y"
        o.append(weld_line((-8, sy * 12, -60), (448, sy * 12, -60), "+z", v, 4, tag=f", lower spacer to side plate ({sy:+d})", key=key, group=g))
        o.append(weld_line((455, sy * 12, -93), (455, sy * 12, 233), "-x", v, 4, tag=f", spine to side plate ({sy:+d})", key=key, group=g))
        o.append(weld_line((-33, sy * 12, 120), (-2, sy * 12, 120), "-z", v, 3, tag=f", front spacer to side plate ({sy:+d})", key=key, group=g))
    filler = eased(-120, -20, -12, 0, -60, -10, 0.5)
    for x in (-100.0, -40.0):
        filler = filler - hole((x, -6, -18), "+y", 5.5, 20)
    o.part("Lower jaw filler (12 mm plate)", filler, PS, "made", None, key, g, color="#0F766E")
    lb = box(-120, -20, 0, 12, -30, -0.5)
    for x in (-100.0, -40.0):
        lb = lb - hole((x, 6, -18), "+y", 5.5, 20)
    o.part("Lower blade, D2 hardened (100 x 30 x 12)", cp.break_edges(lb, 0.3), "stainless", "made", None, key, g)
    for x in (-100.0, -40.0):
        o.many(bolt_set(10, 56, (x, -28, -18), "+y", bom=None, tag=f", lower blade at x {x:.0f}"), key, g)
    # upper blade arm, blade insert, link, lever hub and stem (all in the 24 mm gap between the side plates)
    arm = plate_xz([(-125, 30), (120, 30), (160, 45), (305, 55), (305, 88), (160, 100), (-125, 100)], -12, 0)
    arm = arm + cp.break_edges(box(-120, -20, -12, -6, 0.5, 30.5), 0.3)
    for (x, z), r in ((ARM_PIV, 10.2), (LINK_A, 8.2)):
        arm = arm - hole((x, -6, z), "+y", r, 20)
    for x in (-100.0, -50.0):
        arm = arm - hole((x, -9, 15), "+y", 4.4, 8)
    o.part("Upper blade arm (12 mm S355 plate)", arm, PS, "made", None, key, g, color="#B45309")
    ub = box(-120, -20, -6, 0, 0.5, 30.0)
    for x in (-100.0, -50.0):
        ub = ub - hole((x, -3, 15), "+y", 4.0, 7)
    o.part("Upper blade insert, D2 hardened, raked 8 deg (100 x 30 x 6)", cp.break_edges(ub, 0.3), "stainless", "made", None, key, g)
    for x in (-100.0, -50.0):
        o.many(tap_screw(8, 10, (x, -12, 15), "+y", bom=None, tag=f", upper blade at x {x:.0f}"), key, g)
    link = Polygon(*D._hull_poly(LINK_A, 15, CRANK, 15), align=None)
    lk = Plane(origin=(0, 12, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0)).location * extrude(link, 12)
    for (x, z) in (LINK_A, CRANK):
        lk = lk - hole((x, 6, z), "+y", 8.2, 20)
    o.part("Shear link (12 mm plate, 100 centres)", cp.break_edges(lk, 0.8), PS, "made", None, key, g, color="#B45309")
    hubshape = Polygon(*D._hull_poly(HUB, 40, (440.0, 300.0), 20), align=None)
    hb = Plane(origin=(0, 0, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0)).location * extrude(hubshape, 12)
    hb = hb - hole((HUB[0], -6, HUB[1]), "+y", 10.2, 20) - hole((CRANK[0], -6, CRANK[1]), "+y", 8.2, 20)
    o.part("Lever hub and stem with crank pin hole (12 mm plate)", cp.break_edges(hb, 0.8), PS, "made", None, key, g, color="#B45309")
    for (x, z), nm in ((ARM_PIV, "arm pivot"), (HUB, "lever pivot")):
        pin = rod("y", 10, -41, 41, x, z)
        for yy in (-37.1, 37.1):
            pin = pin - split_pin_hole(20, (x, yy, z), "x")
        o.part(f"Shear {nm} pin (20 mm bright bar, 76)", pin, BRIGHT, "made", None, key, g)
        o.part(f"Shear {nm} spacer (28 x 4 tube, 12)", ring("y", 10.2, 14, 0, 12, x, z), BRIGHT, "made", None, key, g)
        for yy, d in ((28.0, "+y"), (-28.0, "-y")):
            o.append(washer_at(20, (x, yy, z), d, bom=None, key=key, group=g, tag=f", {nm}"))
        for yy in (-37.1, 37.1):
            o.append(split_pin_at(20, (x, yy, z), "x", bom=None, key=key, group=g, tag=f", {nm} {yy:+.0f}"))
    for (x, z), nm in ((LINK_A, "link to arm"), (CRANK, "link to lever hub")):
        pin = rod("y", 8, -20, 20, x, z)
        for yy in (-17.0, 17.0):
            pin = pin - split_pin_hole(16, (x, yy, z), "x")
        o.part(f"Shear {nm} pin (16 mm bright bar, 40)", pin, BRIGHT, "made", None, key, g)
        for yy in (-17.0, 17.0):
            o.append(split_pin_at(16, (x, yy, z), "x", bom=None, key=key, group=g, tag=f", {nm} {yy:+.0f}"))
    # lever tube on the stem, along the stem's line
    d = (100.0, 110.0)
    n = math.hypot(*d)
    u = (d[0] / n, 0.0, d[1] / n)
    base = (440.0 - 10 * u[0], -6.0, 300.0 - 10 * u[2])
    lt = Plane(origin=base, x_dir=(0, 1, 0), z_dir=u).location * cp.round_tube(33.7, 3.2, 890)
    lt = lt - Plane(origin=(0, 1, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0)).location * extrude(hubshape, 14)
    o.part("Shear hand lever, slotted over the stem and welded (33.7 x 3.2 CHS, 890)", lt, PS, "made", None, key, g, color="#B45309")
    gp = Plane(origin=tuple(b + 770 * c for b, c in zip(base, u)), x_dir=(0, 1, 0), z_dir=u).location * \
        cp.break_edges(cp.round_tube(41.0, 3.6, 120), 1.5)
    o.part("Shear lever grip (rubber sleeve, 120)", gp, "epdm", "bought", None, key, g)
    # mount plate on the column cap
    mp = eased(385, 585, -100, 100, -120, -100, 1.0)
    for x in (400.0, 570.0):
        for y in (-80.0, 80.0):
            mp = mp - hole((x, y, -110), "+z", 6.5, 30)
    o.part("Shear mount plate (20 mm, 200 x 200)", mp, PS, "made", None, key, g, color="#0F766E")
    for sy in (-1, 1):
        o.append(weld_line((390, sy * 28, -100), (518, sy * 28, -100), "+y" if sy > 0 else "-y", "+z", 5,
                           tag=f", side plate to mount plate ({sy:+d})", key=key, group=g))
    return o


def shear_stand(o):
    """Shear on its stand at the right-hand end of the cradle, its cut point at x = B_CUT_X on the drum top."""
    L = M.levels(P)
    xc, zc = P["B_CUT_X"], L["z_nip"]
    T = Pos(xc, 0, zc)
    o.extend(A.placed(T, shear_parts()))
    g, key = "shear", "b_stand"
    cap_z1 = zc - 120.0
    cap_z0 = cap_z1 - 20.0
    xcol = xc + 485.0
    cap = eased(xcol - 120, xcol + 120, -120, 120, cap_z0, cap_z1, 1.0)
    for x in (400.0, 570.0):
        for y in (-80.0, 80.0):
            cap = cap - hole((xc + x, y, cap_z0 + 10), "+z", 6.5, 30)
    o.part("Shear stand cap plate (20 mm, 240 x 240)", cap, PS, "made", None, key, g)
    for x in (400.0, 570.0):
        for y in (-80.0, 80.0):
            o.many(bolt_set(12, 40, (xc + x, y, cap_z1 + 20), "-z", bom=None, tag=f", shear mount ({x:.0f}, {y:.0f})"), key, g)
    fz = 62.0
    o.part("Shear stand column (100 x 100 x 5 RHS)", rhs_run("z", (fz, cap_z0), (xcol - 50, xcol + 50), (-50, 50), 5), PS, "made", None, key, g)
    for w in box_welds(xcol - 50, xcol + 50, -50, 50, cap_z0, "-z", 5, margin=10, tag=", column to cap", key=key, group=g):
        o.append(w)
    o.part("Shear stand foot plate (12 mm, 250 x 350)", eased(xcol - 125, xcol + 125, -175, 175, 50, fz, 1.0), PS, "made", None, key, g)
    for a0, a1 in ((-40.0, -8.0), (8.0, 40.0)):
        for sgn in (-1, 1):
            o.append(weld_line((xcol + a0, sgn * 50, fz), (xcol + a1, sgn * 50, fz), "+y" if sgn > 0 else "-y", "+z", 5,
                               tag=f", column to foot plate (y {sgn:+d}, {a0:.0f})", key=key, group=g))
            o.append(weld_line((xcol + sgn * 50, a0, fz), (xcol + sgn * 50, a1, fz), "+x" if sgn > 0 else "-x", "+z", 5,
                               tag=f", column to foot plate (x {sgn:+d}, {a0:.0f})", key=key, group=g))
    for k, (dx, dy, ang) in enumerate(((50, 0, 0), (-50, 0, 180), (0, 50, 90), (0, -50, 270))):
        gs = Pos(xcol + dx, dy, fz) * Rot(0, 0, ang) * Plane(origin=(0, 5, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0)).location * \
            extrude(Polygon((0, 0), (70, 0), (0, 150), align=None), 10)
        o.part(f"Shear stand gusset {k + 1} (10 mm, 70 x 150)", gs, PS, "made", None, key, g)
    for sy in (-1, 1):
        o.part(f"Shear stand base rail, {'back' if sy > 0 else 'front'} (50 x 50 x 3 RHS, 850)",
               rhs_run("x", (450, 1300), tuple(sorted((sy * 125, sy * 175))), (0, 50), 3), PS, "made", None, key, g)
    for x0 in (450.0, 1250.0):
        o.part(f"Shear stand base cross rail at x {x0:.0f} (50 x 50 x 3 RHS, 250)", rhs_run("y", (-125, 125), (x0, x0 + 50), (0, 50), 3), PS, "made",
               None, key, g)
        for sy in (-1, 1):
            for xf, u in ((x0, "-x"), (x0 + 50, "+x")):
                o.append(weld_line((xf, sy * 125, 6), (xf, sy * 125, 44), u, "-y" if sy > 0 else "+y", 4,
                                   tag=f", base cross rail {x0:.0f} ({sy:+d}, {u})", key=key, group=g))
    for sy in (-1, 1):
        o.append(weld_line((xcol - 123, sy * 125, 50), (xcol + 123, sy * 125, 50), "-y" if sy > 0 else "+y", "-z", 4,
                           tag=f", foot plate to base rail ({sy:+d})", key=key, group=g))


# =================================================================================================================
# Stretch leveller
# =================================================================================================================
def wedge_grip(o, x0, x1, tighten, tag, key, g):
    """A wedge grip whose jaws hold the panel between x0 and x1; the housing narrows toward 'tighten' (+1: +X)."""
    ry, zp = P["B_RS_Y"], P["B_PANEL_Z"]
    tz = math.tan(math.radians(P["B_WEDGE_DEG"]))
    w0, w1 = ry - 120.0, ry + 120.0
    t2 = 0.6
    xa, xb = (x0, x1) if tighten > 0 else (x1, x0)          # xa: wide end, xb: narrow end
    hw, hn = 24.0, 24.0 - abs(x1 - x0) * tz                  # wedge height at the wide and the narrow end
    for side, sgn in (("upper", 1), ("lower", -1)):
        zf = zp + sgn * t2                                    # the jaw face on the panel
        wpts = [(xa, zf), (xb, zf), (xb, zf + sgn * hn), (xa, zf + sgn * hw)]
        wedge = D.Plane(origin=(0, w1, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0)).location * extrude(Polygon(*ccw(wpts), align=None), w1 - w0)
        o.part(f"Wedge jaw, {side}, serrated, hardened ({tag})", cp.break_edges(wedge, 0.4), "stainless", "made", None, key, g)
        xe0, xe1 = min(xa, xb) - 20, max(xa, xb) + 20
        k = (hn - hw) / (xb - xa)
        zat = lambda x: zf + sgn * (hw + k * (x - xa))        # noqa: E731
        bpts = [(xe0, zat(xe0)), (xe1, zat(xe1)), (xe1, zp + sgn * 60), (xe0, zp + sgn * 60)]
        bk = D.Plane(origin=(0, w1, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0)).location * extrude(Polygon(*ccw(bpts), align=None), w1 - w0)
        for xh in (xe0 + 25, xe1 - 25):
            bk = bk - hole((xh, ry, zp + (50 if sgn > 0 else -42)), "+y", 6.5, 300)
        o.part(f"Grip backing block, {side} ({tag})", cp.break_edges(bk, 0.8), PS, "made", None, key, g)
    xe0, xe1 = min(x0, x1) - 20, max(x0, x1) + 20
    zb0 = P["B_BED_TOP"] + 20.0
    for sy in (-1, 1):
        yy0, yy1 = (w1, w1 + 25) if sy > 0 else (w0 - 25, w0)
        ch = eased(xe0, xe1, yy0, yy1, zb0, zp + 70, 1.0)
        for xh in (xe0 + 25, xe1 - 25):
            for zz in (zp + 50, zp - 42):
                ch = ch - hole((xh, (yy0 + yy1) / 2, zz), "+y", 6.5, 40)
        o.part(f"Grip cheek, {'back' if sy > 0 else 'front'} (25 mm plate) ({tag})", ch, PS, "made", None, key, g)
        o.append(weld_line((xe0 + 2, yy1 if sy > 0 else yy0, zb0), (xe1 - 2, yy1 if sy > 0 else yy0, zb0), "+y" if sy > 0 else "-y", "+z", 4,
                           tag=f", grip cheek to base ({sy:+d}, {tag})", key=key, group=g))
    for xh in (xe0 + 25, xe1 - 25):
        for zz in (zp + 50, zp - 42):
            o.many(bolt_set(12, 290, (xh, w1 + 25, zz), "-y", bom=None, tag=f", grip {tag} ({xh:.0f}, {zz:.0f})"), key, g)
    return xe0, xe1


def leveller(o):
    g = "leveller"
    ry, X, zt = P["B_RS_Y"], P["B_BED_X"], P["B_BED_TOP"]
    key = "b_bed"
    for sy in (-1, 1):
        ch = channel_x(-X, X, ry + sy * 100, sy, zt)
        for x in (-1265.0, -1055.0):
            ch = ch - hole((x, ry + sy * 125, zt - 4), "+z", 8.5, 20)
        o.part(f"Stretch bed channel, {'back' if sy > 0 else 'front'} (UPN 100, 2,600)", ch, PS, "made", None, key, g)
    ties = (-900.0, -350.0, 200.0, 900.0)
    for xt in ties:
        o.part(f"Bed cross tie at x {xt:+.0f} (10 mm plate, 200 x 80)", eased(xt - 5, xt + 5, ry - 100, ry + 100, zt - 90, zt - 10, 0.8), PS, "made",
               None, key, g)
        for sy in (-1, 1):
            for xf, u in ((xt - 5, "-x"), (xt + 5, "+x")):
                o.append(weld_line((xf, ry + sy * 100, zt - 88), (xf, ry + sy * 100, zt - 12), u, "-y" if sy > 0 else "+y", 4,
                                   tag=f", cross tie {xt:+.0f} ({sy:+d}, {u})", key=key, group=g))
    rt = eased(360, 380, ry - 100, ry + 100, zt - 95, zt - 5, 0.8) - hole((370, ry, 750), "+x", 22, 40)
    for yy in (-48.0, 48.0):
        rt = rt - hole((370, ry + yy, 712), "+x", 5.5, 40)
    o.part("Cylinder reaction tie (20 mm plate, 200 x 90)", rt, PS, "made", None, key, g)
    for sy in (-1, 1):
        for xf, u in ((360, "-x"), (380, "+x")):
            o.append(weld_line((xf, ry + sy * 100, zt - 93), (xf, ry + sy * 100, zt - 7), u, "-y" if sy > 0 else "+y", 5,
                               tag=f", reaction tie ({sy:+d}, {u})", key=key, group=g))
    for sx in (-1, 1):
        for sy in (-1, 1):
            xl = sx * 1150
            yl0, yl1 = sorted((ry + sy * 100, ry + sy * 160))
            o.part(f"Bed leg ({sx:+d}, {sy:+d}) (60 x 60 x 3 RHS, 694)", rhs_run("z", (6, zt - 100), (xl - 30, xl + 30), (yl0, yl1), 3), PS, "made",
                   None, key, g)
            o.part(f"Bed leg foot ({sx:+d}, {sy:+d}) (6 mm, 100 x 100)", eased(xl - 50, xl + 50, (yl0 + yl1) / 2 - 50, (yl0 + yl1) / 2 + 50, 0, 6, 1.0),
                   PS, "made", None, key, g)
            for w in box_welds(xl - 30, xl + 30, yl0, yl1, 6, "+z", 4, margin=6, tag=f", bed leg to foot ({sx:+d}, {sy:+d})", key=key, group=g):
                o.append(w)
            for xf, u in ((xl - 30, "-x"), (xl + 30, "+x")):
                o.append(weld_line((xf, ry + sy * 106, zt - 100), (xf, ry + sy * 144, zt - 100), u, "-z", 4,
                                   tag=f", bed leg to channel ({sx:+d}, {sy:+d}, {u})", key=key, group=g))
    # fixed head
    gl = P["B_GRIP_L"]
    x_fix0 = -1150.0
    base = eased(-1290, -1030, ry - 150, ry + 150, zt, zt + 20, 1.0)
    for x in (-1265.0, -1055.0):
        for sy in (-1, 1):
            base = base - hole((x, ry + sy * 125, zt + 10), "+z", 8.5, 30)
    o.part("Fixed grip base plate (20 mm, 260 x 300)", base, PS, "made", None, "b_fixed", g)
    for x in (-1265.0, -1055.0):
        for sy in (-1, 1):
            o.many(bolt_set(16, 28.5, (x, ry + sy * 125, zt + 20), "-z", bom=None, tag=f", fixed grip ({x:.0f}, {sy:+d})"), "b_fixed", g)
    wedge_grip(o, x_fix0 - gl, x_fix0, 1, "fixed", "b_fixed", g)
    # moving head on a carriage that slides on the channel flanges
    x_mov = 650.0
    cx0, cx1 = x_mov - 20, x_mov + gl + 20
    car = eased(cx0 - 20, cx1 + 20, ry - 160, ry + 160, zt, zt + 20, 1.0)
    o.part("Moving grip carriage plate (20 mm, 180 x 320)", car, PS, "made", None, "b_moving", g)
    lug = eased(cx1 + 0, cx1 + 20, ry - 60, ry + 60, zt - 95, zt, 0.8)
    o.part("Carriage pull lug (20 mm plate, 120 x 95)", lug, PS, "made", None, "b_moving", g)
    for sy in (-1, 1):
        o.append(weld_line((cx1 + 20, ry + sy * 58, zt), (cx1 + 20, ry + sy * 2, zt), "+x", "-z", 5, tag=f", lug to carriage ({sy:+d})",
                           key="b_moving", group=g))
        for xs in (cx0 - 10, cx1 - 10):
            yo0, yo1 = sorted((ry + sy * 150, ry + sy * 156))
            yl0, yl1 = sorted((ry + sy * 140, ry + sy * 150))
            sh = box(xs, xs + 30, yo0, yo1, zt - 14.5, zt) + box(xs, xs + 30, yl0, yl1, zt - 14.5, zt - 8.5)
            o.part(f"Carriage guide shoe ({sy:+d}, x {xs:.0f}) (6 mm plate, welded)", cp.break_edges(sh, 0.4), PS, "made", None, "b_moving", g)
            o.append(weld_line((xs + 1, ry + sy * 156, zt), (xs + 29, ry + sy * 156, zt), "+y" if sy > 0 else "-y", "-z", 3,
                               tag=f", guide shoe to carriage ({sy:+d}, {xs:.0f})", key="b_moving", group=g))
    wedge_grip(o, x_mov, x_mov + gl, -1, "moving", "b_moving", g)
    # hydraulic cylinder between the reaction tie and the lug, under the panel
    zc = 750.0
    o.part("Hydraulic cylinder, 15 t, single acting (bought)", cp.break_edges(Pos(495, ry, zc) * Rot(0, 90, 0) * Cylinder(45, 210), 2.0), "safety_red",
           "bought", None, "b_ram", g)
    o.part("Cylinder plunger (52 mm)", rod("x", 26, 600, cx1, ry, zc, chamfer=1.0), "stainless", "bought", None, "b_ram", g)
    fl = eased(380, 390, ry - 55, ry + 55, zc - 55, zc + 55, 0.8)
    for yy in (-48.0, 48.0):
        fl = fl - hole((385, ry + yy, 712), "+x", 5.5, 20)
    o.part("Cylinder mounting flange (10 mm, 110 x 110)", fl, PS, "made", None, "b_ram", g)
    o.append(ring_weld((390, ry, zc), "x", 45, 4, "+", tag=", cylinder to flange", key="b_ram", group=g))
    for yy in (-48.0, 48.0):
        o.many(bolt_set(10, 30, (390, ry + yy, 712), "-x", bom=None, tag=f", cylinder flange ({yy:+.0f})"), "b_ram", g)
    # hand pump on the floor and its hose
    px, py = 0.0, ry - 450.0
    o.part("Hand pump, 700 bar, single speed, cast body and reservoir (bought)", cp.break_edges(box(px - 150, px + 150, py - 45, py + 45, 0, 110), 4.0), "cast_aluminium", "bought",
           None, "b_ram", g)
    hdl = rod("x", 12.5, 0, 600, 0, 0, chamfer=1.0)
    grp = ring("x", 12.5, 15.5, 480, 600, 0, 0, edge=1.0)
    o.part("Hand pump handle (bought with the pump)", Pos(px + 100, py, 150) * Rot(0, -20, 0) * hdl, "mild_steel", "bought", None, "b_ram", g)
    o.part("Hand pump handle grip", Pos(px + 100, py, 150) * Rot(0, -20, 0) * grp, "epdm", "bought", None, "b_ram", g)
    hose = cp.rope([(px + 150, py, 60), (px + 220, py, 60), (360, ry - 260, 40), (430, ry - 200, 40), (490, ry - 130, 600),
                    (490, ry - 51, zc - 5)], 12)
    o.part("Hydraulic hose, 1.8 m (bought)", hose, "epdm", "bought", None, "b_ram", g)


def context(o):
    L = M.levels(P)
    from build123d import Compound
    body = []
    e = P["DRUM_L"] / 2 - P["RING_CUT"]
    ri, t = P["DRUM_R_IN"], P["DRUM_T"]
    body.append(M.ringx(ri, ri + t, -e, e, 0, 0))
    for s in (-1, 1):
        body.append(M.ringx(ri + t - 0.01, P["HOOP_R"], s * P["HOOP_X"] - P["HOOP_W"] / 2, s * P["HOOP_X"] + P["HOOP_W"] / 2, 0, 0))
    dr = Pos(0, 0, L["z_ax"]) * M.fuse(body)
    o.part("Drum body, heads and chime rings off, being slit (context)", dr, PS, "context", None, "drum", "context", color="#1F4E9C")
    ry, zp = P["B_RS_Y"], P["B_PANEL_Z"]
    o.part("Panel being stretched, 233 x 1,800 x 1.0 (context)", box(-1150 - P["B_GRIP_L"], 650 + P["B_GRIP_L"], ry - 116.5, ry + 116.5, zp - 0.5, zp + 0.5),
           PS, "context", None, "sheet", "context", color="#1F4E9C")


def build(with_context=True):
    L = M.levels(P)
    o = A.Out()
    A.drain_stand(o)
    A.cradle_frame(o, L)
    A.rollers(o, L)
    A.brake(o, L)
    for p in o:
        p["bom"] = None              # option B carries no BOM lines (STANDARDS section 24: BOM for the chosen design only)
    shear_stand(o)
    leveller(o)
    if with_context:
        context(o)
    return list(o)
