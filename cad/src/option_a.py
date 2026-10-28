"""DrumPanel option A, the bench set (CHOSEN), detailed to D3 (kit 1.9, STANDARDS section 24).

Built on the station model of cad/src/model.py (same PARAMS, levels() and positions, so the drawing, the calculations
and the build plan keep their numbers) and on .kit/cad_parts.py through cad/src/dmp_parts.py: real hollow sections with
their corner radii, every bolt, nut, washer, pin and screw with its hole, fillet welds as beads, ball bearings, bushes,
sprockets and chains at their catalogue envelopes, broken edges on every plate and bar.

Each part dict carries, besides the kit fields, "key": the station model component it belongs to (build plan pictures,
masses by component). Called from model.components("A"). CONCEPT, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Plane, Polygon, Pos, Rot, extrude, Torus, Cylinder  # noqa: E402
import cad_parts as cp  # noqa: E402
import dmp_parts as D  # noqa: E402
from dmp_parts import (box, eased, rod, ring, rhs_run, tube_run, bolt_set, tap_screw, coach, weld_line, ring_weld,  # noqa: E402
                       box_welds, hole, bearing, sprocket, chain_loop, nut_at, washer_at, split_pin_at, split_pin_hole)
import model as M  # noqa: E402

P = M.PARAMS
EXPLODE = {bom: exp for bom, (_, _, exp) in M.BOM_NAMES.items()}
PS, PY, HW, BRZ, ZN, YEL, RED, BRIGHT = ("painted_steel", "plywood", "hardwood", "brass", "zinc_plated", "safety_yellow",
                                         "safety_red", "mild_steel")


class Out(list):
    """Collects part dicts with their station key, BOM line and group."""

    def part(self, name, shape, material, kind, bom, key, group, color=None):
        p = cp.part(name, shape, material, kind, bom=bom, group=group, explode=EXPLODE.get(bom, (0, 0, 0)), color=color)
        p["key"] = key
        self.append(p)
        return p

    def many(self, parts, key, group, bom=None):
        for p in parts:
            p["key"] = key
            p["group"] = group
            if bom is not None:
                p["bom"] = bom
            p["explode"] = EXPLODE.get(p.get("bom"), (0, 0, 0))
            self.append(p)


def placed(T, parts):
    """Move a list of part dicts by the location T."""
    out = []
    for p in parts:
        q = dict(p)
        q["shape"] = T * p["shape"]
        out.append(q)
    return out


def tri_plate_y(pts_xz, y0, y1):
    """A plate cut to an outline in the XZ plane, from y0 to y1."""
    pl = Plane(origin=(0, y1, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    return pl.location * extrude(Polygon(*pts_xz, align=None), y1 - y0)


def angle_run(heel, xdir, ydir, run, L, a=40.0, t=3.0):
    """EN 10056 equal angle a x a x t with its heel line starting at 'heel', legs along the unit vectors xdir and ydir,
    running a length L along 'run'."""
    z = (xdir[1] * ydir[2] - xdir[2] * ydir[1], xdir[2] * ydir[0] - xdir[0] * ydir[2], xdir[0] * ydir[1] - xdir[1] * ydir[0])
    origin = heel if all(abs(p - q) < 1e-9 for p, q in zip(z, run)) else tuple(h + L * r for h, r in zip(heel, run))
    return Plane(origin=origin, x_dir=xdir, z_dir=z).location * cp.angle(a, a, t, L)


def handwheel(d, rim_d, hub_r, hub_h, bore_r, spokes=3):
    """Cast handwheel in the XY plane, rim centre at z = 0, hub from z = -rim_d / 2 up, bored for its screw."""
    rim = Torus(d / 2 - rim_d / 2, rim_d / 2)
    hub = ring("z", bore_r, hub_r, -rim_d / 2, -rim_d / 2 + hub_h, 0, 0, edge=0.5)
    from build123d import Compound
    kids = [rim, hub]
    for i in range(spokes):
        a = i * 360 / spokes
        L = d / 2 - rim_d / 2 - hub_r - 0.5
        kids.append(Rot(0, 0, a) * Pos(hub_r + 0.25 + L / 2, 0, 0) * Rot(0, 90, 0) * Cylinder(rim_d * 0.3, L))
    return Compound(kids)


# =================================================================================================================
# Station 1: drain and purge stand
# =================================================================================================================
def drain_stand(o, dx=0.0, n=""):
    """A drain and purge stand with its tray; dx moves it along X, n names the second stand (BOM line 1 has two)."""
    y0 = P["DS_Y"]
    g, key = "purge", "ds_frame" + n
    T = Pos(dx, 0, 0)
    o0 = len(o)
    for sy in (-1, 1):
        yc = y0 + sy * 240
        o.part(f"Drain stand rail, {'front' if sy < 0 else 'back'} (40 x 40 x 3 RHS, 800)",
               rhs_run("x", (-400, 400), (yc - 20, yc + 20), (260, 300), 3), PS, "made", 1, key, g)
        for sx in (-1, 1):
            o.part(f"Drain stand leg, {'left' if sx < 0 else 'right'} {'front' if sy < 0 else 'back'} (40 x 40 x 3 RHS, 260)",
                   rhs_run("z", (0, 260), (sx * 380 - 20, sx * 380 + 20), (yc - 20, yc + 20), 3), PS, "made", 1, key, g)
            xi = sx * 360
            o.append(weld_line((xi, yc - 14, 260), (xi, yc + 14, 260), "-x" if sx > 0 else "+x", "-z", 4,
                               tag=f", drain stand leg to rail ({sx:+d}, {sy:+d})", key=key, group=g))
    tops = {-1: P["DS_TOP_HI"], 1: P["DS_TOP_LO"]}
    for sx in (-1, 1):
        xs = sx * P["DS_SADDLE_X"]
        holes = [hole((xs, y0 + sy * 180, 320), "+z", 4.5, 60) for sy in (-1, 1)]
        sad = rhs_run("y", (y0 - 280, y0 + 280), (xs - 20, xs + 20), (300, 340), 3)
        for h in holes:
            sad = sad - h
        o.part(f"Drain stand saddle, {'left' if sx < 0 else 'right'} (40 x 40 x 3 RHS, 560)", sad, PS, "made", 1, key, g)
        for sy in (-1, 1):
            yc = y0 + sy * 240
            for xf, u in ((xs - 20, "-x"), (xs + 20, "+x")):
                o.append(weld_line((xf, yc - 14, 300), (xf, yc + 14, 300), u, "+z", 4,
                                   tag=f", saddle to rail ({sx:+d}, {sy:+d}, {u})", key=key, group=g))
            yi = y0 + sy * P["DS_CHOCK_Y"]
            yo = y0 + sy * (P["DS_CHOCK_Y"] + 60)
            ya, yb = min(yi, yo), max(yi, yo)
            ys = y0 + sy * 180
            chock = eased(xs - 20, xs + 20, ya, yb, 340, tops[sx], 2.0) - hole((xs, ys, 340), "+z", 4.0, 34, both=False)
            o.part(f"Drain stand chock, {'left' if sx < 0 else 'right'} {'front' if sy < 0 else 'back'} (hardwood 40 x 60, "
                   f"{tops[sx] - 340:.0f} high)", chock, HW, "made", 1, "ds_chocks" + n, g)
            o.many(coach(8, 70, (xs, ys, 300), "+z", bom=1, tag=f", chock ({sx:+d}, {sy:+d})"), "ds_chocks" + n, g)
    tray = box(460, 1060, y0 - 250, y0 + 250, 0, 150) - box(463, 1057, y0 - 247, y0 + 247, 3, 160)
    o.part("Drain tray, 60 L (HDPE, bought)", cp.break_edges(tray, 1.0), "hdpe_recycled", "bought", 2, "tray" + n, g)
    for p in o[o0:]:
        p["shape"] = T * p["shape"]
        if n:
            p["name"] = p["name"] + f" (stand {n})"


# =================================================================================================================
# Station 2: cutting cradle
# =================================================================================================================
def cradle_frame(o, L):
    ft, S, T = L["frame_top"], P["FRAME_RHS"], P["FRAME_T"]
    FX, FY = P["FRAME_X"], P["FRAME_Y"]
    g, key = "cradle", "frame"
    zb = ft - S
    brake_holes = [hole((0, FY - S / 2, z), "+y", 5.5, 60) for z in (236.0, 261.0)]
    for sy in (-1, 1):
        r = rhs_run("x", (-FX, FX), tuple(sorted((sy * FY, sy * (FY - S)))), (zb, ft), T)
        if sy > 0:
            for h in brake_holes:
                r = r - h
        o.part(f"Cradle side rail, {'front' if sy < 0 else 'back'} (50 x 50 x 3 RHS, 1,550)", r, PS, "made", 5, key, g)
    xs = [sx * xc for sx in (-1, 1) for xc in (P["PB_X"], P["POST_X"] - 37.5, P["POST_X"] + 37.5)]
    for xc in xs:
        c = rhs_run("y", (-(FY - S), FY - S), (xc - S / 2, xc + S / 2), (zb, ft), T)
        if abs(abs(xc) - P["PB_X"]) < 1:
            for sy in (-1, 1):
                for dy in (-52.5, 52.5):
                    c = c - hole((xc, sy * P["ROLLER_Y"] + dy, ft - 25), "+z", 5.5, 70)
        else:
            for yy in (-70.0, 70.0):
                c = c - hole((xc, yy, ft - 25), "+z", 5.5, 70)
        o.part(f"Cradle cross member at x {xc:+.0f} (50 x 50 x 3 RHS, 600)", c, PS, "made", 5, key, g)
        for sy in (-1, 1):
            yf = sy * (FY - S)
            for xf, u in ((xc - S / 2, "-x"), (xc + S / 2, "+x")):
                o.append(weld_line((xf, yf, zb + 6), (xf, yf, ft - 6), u, "-y" if sy > 0 else "+y", 4,
                                   tag=f", cross member {xc:+.0f} to side rail ({sy:+d}, {u})", key=key, group=g))
    lx, ly = FX - S / 2, FY - S / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * lx, sy * ly
            nm = f"{'left' if sx < 0 else 'right'} {'front' if sy < 0 else 'back'}"
            o.part(f"Cradle leg, {nm} (50 x 50 x 3 RHS, 192.5)", rhs_run("z", (31, zb), (cx - 25, cx + 25), (cy - 25, cy + 25), T),
                   PS, "made", 5, key, g)
            fp = eased(cx - 30, cx + 30, cy - 30, cy + 30, 25, 31, 1.0) - hole((cx, cy, 28), "+z", 6.5, 10)
            o.part(f"Cradle foot plate, {nm} (60 x 60 x 6)", fp, PS, "made", 5, key, g)
            o.append(nut_at(12, (cx, cy, 25), "-z", bom=5, key=key, group=g, name=f"M12 hex nut welded under the foot plate, {nm}"))
            xi = cx - sx * 25
            o.append(weld_line((xi, cy - 19, zb), (xi, cy + 19, zb), "-x" if sx > 0 else "+x", "-z", 4,
                               tag=f", cradle leg to rail, {nm}", key=key, group=g))
            for w in box_welds(cx - 25, cx + 25, cy - 25, cy + 25, 31, "+z", 4, margin=6, tag=f", leg to foot plate, {nm}",
                               key=key, group=g):
                o.append(w)
            foot = cp.break_edges(Pos(cx, cy, 6) * Cylinder(30, 12), 2.0) + rod("z", 6, 12, 45, cx, cy)
            o.part(f"Levelling foot M12 with 60 mm pad, {nm} (bought)", foot, ZN, "bought", 5, "feet", g)


def rollers(o, L):
    g = "cradle"
    ft, zr, sr = L["frame_top"], P["ROLLER_Z"], P["SHAFT_R"]
    for sy in (-1, 1):
        yr = sy * P["ROLLER_Y"]
        side = "front" if sy < 0 else "back"
        o.part(f"Roller shaft, {side} (25 mm bright bar, 1,120)", rod("x", sr, -560, 560, yr, zr), BRIGHT, "made", 6, "shafts", g)
        for sx in (-1, 1):
            xp = sx * P["PB_X"]
            nm = f"{'left' if sx < 0 else 'right'} {side}"
            hs = eased(xp - 19, xp + 19, yr - 70, yr + 70, ft, ft + 15, 1.0) + cp.break_edges(
                Pos(xp, yr, zr) * Rot(0, 90, 0) * Cylinder(32, 38), 1.0)
            hs = hs - Pos(xp, yr, zr) * Rot(0, 90, 0) * Cylinder(26, 50)
            for dy in (-52.5, 52.5):
                hs = hs - hole((xp, yr + dy, ft + 7), "+z", 6.5, 30)
            o.part(f"Pillow block housing UCP205, {nm} (bought)", hs, PS, "bought", 6, "pillow", g, color="#1D4ED8")
            o.part(f"Insert bearing UC205, {nm} (bought)", ring("x", sr, 26, xp - 15, xp + 15, yr, zr), BRIGHT, "bought", 6, "pillow", g)
            for dy in (-52.5, 52.5):
                o.many(bolt_set(10, 65, (xp, yr + dy, ft + 15), "-z", bom=6, tag=f", pillow block {nm}"), "pillow", g)
            h = sx * P["HOOP_X"]
            o.part(f"Cradle roller tube, {nm} (101.6 x 4 CHS, 100)", tube_run("x", 101.6, 4.0, h - 50, h + 50, yr, zr),
                   PS, "made", 6, "rollers", g, color="#B45309")
            for e in (-1, 1):
                a0 = h + e * 36 if e > 0 else h - 46
                o.part(f"Cradle roller end disc, {nm}, {'outer' if e * sx > 0 else 'inner'} (10 mm plate, 93.6 bored 25)",
                       ring("x", sr, 46.8, a0, a0 + 10, yr, zr), PS, "made", 6, "rollers", g, color="#B45309")
                xf = h + e * 46
                sgn = "+" if e > 0 else "-"
                o.append(ring_weld((xf, yr, zr), "x", sr, 4, sgn, tag=f", roller disc to shaft, {nm} {sgn}", key="rollers", group=g))
                o.append(ring_weld((xf, yr, zr), "x", 46.8, 4, sgn, inside=True, tag=f", roller disc to tube, {nm} {sgn}",
                                   key="rollers", group=g))


def brake(o, L):
    g, key = "cradle", "brake"
    FY, zax = P["FRAME_Y"], L["z_ax"]
    ro = P["DRUM_R_IN"] + P["DRUM_T"]
    post = rhs_run("z", (180, 640), (-20, 20), (FY, FY + 40), 3) - hole((0, FY + 20, zax), "+y", 9, 60)
    for z in (236.0, 261.0):
        post = post - hole((0, FY + 20, z), "+y", 5.5, 60)
    o.part("Drum brake post (40 x 40 x 3 RHS, 460)", post, RED, "made", 7, key, g)
    for z in (236.0, 261.0):
        o.many(bolt_set(10, 90, (0, FY + 40, z), "-y", bom=7, tag=f", brake post at z {z:.0f}"), key, g)
    o.append(nut_at(16, (0, FY + 40, zax), "+y", bom=7, key=key, group=g, name="M16 hex nut welded on the brake post"))
    o.append(ring_weld((0, FY + 40, zax), "y", 13.9, 3, "+", tag=", brake nut to post", key=key, group=g))
    o.part("Brake screw M16 (16 mm bar threaded)", rod("y", 8, 303, 454, 0, zax), BRIGHT, "made", 7, key, g)
    o.part("Brake T-handle (16 mm bar, 160)", rod("x", 8, -80, 80, 462, zax), BRIGHT, "made", 7, key, g)
    o.part("Brake pad swivel plate (6 mm, 60 dia)", cp.break_edges(Pos(0, ro + 13, zax) * Rot(90, 0, 0) * Cylinder(30, 6), 1.0),
           BRIGHT, "made", 7, key, g)
    o.part("Brake pad, rubber (60 dia x 10)", cp.break_edges(Pos(0, ro + 5, zax) * Rot(90, 0, 0) * Cylinder(30, 10), 2.0),
           "epdm", "bought", 7, key, g)


def posts_and_beam(o, L):
    g = "cradle"
    ft = L["frame_top"]
    px, pr, pt = P["POST_X"], P["POST_RHS"], P["POST_T"]
    bz0, bz1 = P["BEAM_Z0"], P["BEAM_Z0"] + P["BEAM_H"]
    beam_bolts_x = [sx * bx for sx in (-1, 1) for bx in (px - 40.0, px + 40.0)]
    for sx in (-1, 1):
        xc = sx * px
        nm = "left" if sx < 0 else "right"
        base = eased(xc - 50, xc + 50, -100, 100, ft, ft + 10, 1.0)
        for bx in (px - 37.5, px + 37.5):
            for by in (-70.0, 70.0):
                base = base - hole((sx * bx, by, ft + 5), "+z", 5.5, 20)
        o.part(f"Rail post base plate, {nm} (200 x 100 x 10)", base, "painted_steel", "made", 8, "posts", g, color="#0F766E")
        col = rhs_run("z", (ft + 10, bz0 - 10), (xc - pr / 2, xc + pr / 2), (-pr / 2, pr / 2), pt)
        if sx < 0:
            for z in (550.0, 700.0):
                col = col - hole((xc, 0, z), "+x", 5.5, 80)
        o.part(f"Rail post, {nm} (60 x 60 x 4 RHS, 927)", col, PS, "made", 8, "posts", g, color="#0F766E")
        cap = eased(xc - 60, xc + 60, -40, 40, bz0 - 10, bz0, 1.0)
        for bx in beam_bolts_x:
            if bx * sx > 0:
                cap = cap - hole((bx, 0, bz0 - 5), "+z", 5.5, 20)
        o.part(f"Rail post cap, {nm} (120 x 80 x 10)", cap, PS, "made", 8, "posts", g, color="#0F766E")
        for w in box_welds(xc - pr / 2, xc + pr / 2, -pr / 2, pr / 2, ft + 10, "+z", 5, margin=8, tag=f", post to base, {nm}",
                           key="posts", group=g):
            o.append(w)
        for w in box_welds(xc - pr / 2, xc + pr / 2, -pr / 2, pr / 2, bz0 - 10, "-z", 5, sides="ns", margin=8, tag=f", post to cap, {nm}",
                           key="posts", group=g):
            o.append(w)
        for bx in (px - 37.5, px + 37.5):
            for by in (-70.0, 70.0):
                o.many(bolt_set(10, 60, (sx * bx, by, ft + 10), "-z", bom=8, tag=f", post base {nm}"), "bolts", g)
    beam = rhs_run("x", (-P["BEAM_X"], P["BEAM_X"]), (-P["BEAM_W"] / 2, P["BEAM_W"] / 2), (bz0, bz1), P["BEAM_T"])
    for bx in beam_bolts_x:
        beam = beam - hole((bx, 0, (bz0 + bz1) / 2), "+z", 5.5, 100)
    o.part("Rail beam (80 x 40 x 3 RHS, 1,540)", beam, PS, "made", 8, "beam", g, color="#0F766E")
    for bx in beam_bolts_x:
        o.part(f"Crush tube at x {bx:+.1f} (14 x 1.75 tube, 74)", tube_run("z", 14, 1.75, bz0 + 3, bz1 - 3, bx, 0), BRIGHT, "made", 8,
               "bolts", g)
        o.many(bolt_set(10, 90, (bx, 0, bz1), "-z", bom=8, tag=f", beam at x {bx:+.1f}"), "bolts", g)


def trolley(o, L):
    g = "head"
    xn = P["HEAD_PARK_X"]
    bz0, bz1 = P["BEAM_Z0"], P["BEAM_Z0"] + P["BEAM_H"]
    tz0, tz1 = 1176.0, 1340.0
    zw = (bz1 + 17.5, bz0 - 18.5)
    axle_holes = [hole((xn + dx, 0, z), "+y", 7.6, 80) for dx in (-60, 60) for z in zw]
    for sy in (-1, 1):
        y0, y1 = (23.0, 29.0) if sy > 0 else (-29.0, -23.0)
        pl = eased(xn - 90, xn + 90, y0, y1, tz0, tz1, 1.0)
        for h in axle_holes:
            pl = pl - h
        o.part(f"Trolley side plate, {'back' if sy > 0 else 'front'} (6 mm, 180 x 164)", pl, YEL, "made", 9, "trolley", g)
        for xa, xb in ((xn - 88, xn - 24), (xn + 24, xn + 88)):
            o.append(weld_line((xa, sy * 23, tz0), (xb, sy * 23, tz0), "-y" if sy > 0 else "+y", "+z", 4,
                               tag=f", trolley plate to swivel plate ({sy:+d}, {xa:.0f})", key="trolley", group=g))
    sw = eased(xn - 90, xn + 90, -29, 29, 1164, tz0, 1.0) - hole((xn, 0, 1170), "+z", 15.5, 20) - hole((xn + 45, 0, 1170), "+z", 5.2, 20)
    o.part("Trolley swivel plate (12 mm, 180 x 58)", sw, YEL, "made", 9, "trolley", g)
    for dx in (-60, 60):
        for z in zw:
            x = xn + dx
            nm = f"{'left' if dx < 0 else 'right'} {'upper' if z > bz1 else 'lower'}"
            o.part(f"Trolley wheel, bearing 6202-2RS, {nm} (bought)", bearing("y", 15, 35, 11, -5.5, x, z), BRIGHT, "bought", 9,
                   "trolley_wheels", g)
            ax = rod("y", 7.5, -41, 41, x, z)
            for yy in (-36.6, 36.6):
                ax = ax - split_pin_hole(15, (x, yy, z), "x")
            o.part(f"Trolley wheel axle, {nm} (15 mm bright bar, 74)", ax, BRIGHT, "made", 9, "trolley_wheels", g)
            for y0, y1 in ((5.5, 23.0), (-23.0, -5.5)):
                o.part(f"Wheel spacer, {nm}, {'back' if y0 > 0 else 'front'} (20 x 2.5 tube, 17.5)", tube_run("y", 20, 2.5, y0, y1, x, z),
                       BRIGHT, "made", 9, "trolley_wheels", g)
            for yy, d in ((29.0, "+y"), (-29.0, "-y")):
                o.append(washer_at(16, (x, yy, z), d, bom=9, key="trolley_wheels", group=g, tag=f", axle {nm}"))
                o.append(split_pin_at(15, (x, 36.6 if yy > 0 else -36.6, z), "x", bom=9, key="trolley_wheels", group=g,
                                      tag=f", axle {nm} {'back' if yy > 0 else 'front'}"))


def drop_and_pivot(o, L):
    g = "head"
    xn, znip = P["HEAD_PARK_X"], L["z_nip"]
    top = znip + 136.0
    db = rhs_run("z", (top, 1152), (xn - 25, xn + 25), (-25, 25), 4) - hole((xn, 0, 1135), "+x", 4.5, 60)
    o.part("Drop bar, cross-drilled for the pivot pin bolt (50 x 50 x 4 RHS, 126)", db, YEL, "made", 9, "drop", g)
    hp = eased(xn - 60, xn + 60, -60, 60, 1152, 1164, 1.0) - hole((xn, 0, 1158), "+z", 15.5, 20)
    for ix, iy in ((45, 0), (0, 45)):
        hp = hp - hole((xn + ix, iy, 1158), "+z", 5.2, 20)
    o.part("Head plate with two index holes at 90 deg (12 mm, 120 x 120)", hp, YEL, "made", 9, "drop", g)
    for w in box_welds(xn - 25, xn + 25, -25, 25, 1152, "-z", 4, margin=8, tag=", drop bar to head plate", key="drop", group=g):
        o.append(w)
    for w in box_welds(xn - 25, xn + 25, -25, 25, top, "+z", 4, sides="new", margin=8, tag=", drop bar to shear head top plate",
                       key="drop", group=g):
        o.append(w)
    pin = rod("z", 15, 1120, 1176, xn, 0) + cp.break_edges(Pos(xn, 0, 1181) * Cylinder(20, 10), 1.0)
    pin = pin - hole((xn, 0, 1135), "+x", 4.5, 40)
    o.part("Pivot pin, 30 mm bar 66 long with 40 mm collar, cross-drilled 9 mm", pin, BRIGHT, "made", 9, "pivot", g)
    o.many(bolt_set(8, 50, (xn - 25, 0, 1135), "+x", bom=9, tag=", pivot pin cross bolt through the drop bar"), "pivot", g)
    ip = rod("z", 5, 1146, 1176, xn + 45, 0) + cp.break_edges(Pos(xn + 45, 0, 1179) * Cylinder(8, 6), 0.8)
    o.part("Index pin, 10 mm with knob", ip, BRIGHT, "made", 9, "pivot", g)


# ----------------------------------------------------------------------------------------------- the shear heads
def shear_head_parts(ring_head=False, tag=""):
    """One rotary shear head in its own frame (nip at the origin, cut plane y = 0, cutting direction +X, disc axes
    along Y, driven disc above), as part dicts. ring_head=True: the ring head, same frame, shafts, discs and guard,
    no drive, its upper shaft slotted at the +Y end for the coupling."""
    R, T, ov = P["DISC_R"], P["DISC_T"], P["DISC_OVERLAP"]
    zc = R - ov / 2
    sr = P["SHAFT_R"]
    o = Out()
    bomh = 25 if ring_head else 10
    kf, kp, kg = ("ring_frame", "ring_parts", "ring_parts") if ring_head else ("head_frame", "head_shafts", "head_guard")
    kd = "ring_parts" if ring_head else "discs"
    g = "tools" if ring_head else "head"
    who = "Ring head" if ring_head else "Shear head"
    # frame: web, top and lower plates, upper and lower bearing housings (20 mm plate), welded
    o.part(f"{who} web (10 mm plate, 92 x 232){tag}", eased(-150, -58, -5, 5, -116, 116, 1.0), PS, "made", bomh, kf, g, color="#0F766E")
    tp = eased(-150, 45, -25, 74, 116, 136, 1.0)
    for x in (-120.0, -60.0):
        tp = tp - hole((x, 0, 128), "+z", 6.0, 16.1)
    o.part(f"{who} top plate with two M12 tapped holes (20 mm, 195 x 99){tag}", tp, PS, "made", bomh, kf, g, color="#0F766E")
    o.part(f"{who} lower plate (20 mm, 195 x 79){tag}", eased(-150, 45, -74, 5, -136, -116, 1.0), PS, "made", bomh, kf, g, color="#0F766E")
    uh = eased(-45, 45, 14, 74, 15, 116, 1.0) - hole((0, 44, zc + 3), "+y", 30, 62) - hole((36, 44, zc + 3), "+x", 4, 21)
    for x in (-35, 35):
        uh = uh - hole((x, 21, 100), "+y", 3, 14.1)
    if not ring_head:
        for x, z in ((-38, 30), (38, 30), (-38, 105), (38, 105)):
            uh = uh - hole((x, 64, z), "+y", 4, 20.1)
    o.part(f"{who} upper bearing housing (20 mm plate, 90 x 60 x 101, bored 60){tag}", uh, PS, "made", bomh, kf, g, color="#0F766E")
    lh = eased(-45, 45, -74, -14, -116, -20, 1.0) - hole((0, -44, -zc), "+y", 13.5, 62) - hole((0, -44, -zc), "+y", 23.5, 12)
    o.part(f"{who} lower bearing housing (20 mm plate, 90 x 60 x 96, bored 47){tag}", lh, PS, "made", bomh, kf, g, color="#0F766E")
    for sy in (-1, 1):
        o.append(weld_line((-148, sy * 5, 116), (-60, sy * 5, 116), "+y" if sy > 0 else "-y", "-z", 4,
                           tag=f", web to top plate ({sy:+d}){tag}", key=kf, group=g))
        o.append(weld_line((-148, sy * 5, -116), (-60, sy * 5, -116), "+y" if sy > 0 else "-y", "+z", 4,
                           tag=f", web to lower plate ({sy:+d}){tag}", key=kf, group=g))
    for sx in (-1, 1):
        o.append(weld_line((sx * 45, 16, 116), (sx * 45, 72, 116), "+x" if sx > 0 else "-x", "-z", 4,
                           tag=f", upper housing to top plate ({sx:+d}){tag}", key=kf, group=g))
        o.append(weld_line((sx * 45, -72, -116), (sx * 45, -16, -116), "+x" if sx > 0 else "-x", "+z", 4,
                           tag=f", lower housing to lower plate ({sx:+d}){tag}", key=kf, group=g))
    # eccentric bush, bearings, shafts, discs and their clamps
    bush = Pos(0, 14, zc + 3) * Rot(-90, 0, 0) * Cylinder(30, 60, align=None) - Pos(0, 13, zc) * Rot(-90, 0, 0) * Cylinder(23.5, 62, align=None)
    o.part(f"{who} eccentric bush, 3 mm offset (60 x 47 bore){tag}", cp.break_edges(bush, 0.4), BRIGHT, "made", bomh, kp, g)
    o.many(tap_screw(8, 12, (45, 44, zc + 3), "-x", bom=bomh, tag=f", eccentric lock{tag}", washer=False), kp, g)
    for y0 in (16.0, 60.0):
        o.part(f"{who} upper bearing 6005-2RS at y {y0:.0f} (bought){tag}", bearing("y", 25, 47, 12, y0, 0, zc), BRIGHT, "bought", bomh, kp, g)
    o.part(f"{who} lower bearing 6005-2RS (bought){tag}", bearing("y", 25, 47, 12, -50, 0, -zc), BRIGHT, "bought", bomh, kp, g)
    yu1 = 74.0 if ring_head else 96.0
    us = rod("y", sr, -24, yu1, 0, zc)
    if ring_head:
        us = us - box(-3.1, 3.1, yu1 - 8, yu1 + 1, zc - 13, zc + 13)
    else:
        us = us - box(-3.1, 3.1, -25, -16, zc - 13, zc + 13)
    o.part(f"{who} upper shaft, slotted for the coupling (25 mm bright bar){tag}", us, BRIGHT, "made", bomh, kp, g)
    ls = rod("y", sr, -74, 0, 0, -zc) - hole((0, -8, -zc), "+y", 4, 16.1)
    o.part(f"{who} lower shaft (25 mm bright bar, 74){tag}", ls, BRIGHT, "made", bomh, kp, g)
    o.part(f"{who} upper slitting disc, D2 101 x 10 (bought){tag}", ring("y", sr, R, 0, T, 0, zc, edge=0.2), "stainless", "bought", bomh, kd, g)
    o.part(f"{who} lower slitting disc, D2 101 x 10 (bought){tag}", ring("y", sr, R, -T, 0, 0, -zc, edge=0.2), "stainless", "bought", bomh, kd, g)
    o.part(f"{who} upper disc spacer (40 x 4){tag}", ring("y", sr, 20, T, 14, 0, zc), BRIGHT, "made", bomh, kp, g)
    o.part(f"{who} upper disc clamp collar (40 x 10){tag}", ring("y", sr, 20, -10, 0, 0, zc), BRIGHT, "made", bomh, kp, g)
    o.part(f"{who} lower disc spacer (40 x 4){tag}", ring("y", sr, 20, -14, -T, 0, -zc), BRIGHT, "made", bomh, kp, g)
    o.part(f"{who} lower disc end washer (30 x 3){tag}", ring("y", 4.3, 15, 0, 3, 0, -zc), BRIGHT, "made", bomh, kp, g)
    o.many(tap_screw(8, 16, (0, 3, -zc), "-y", bom=bomh, tag=f", lower disc{tag}", washer=False), kp, g)
    # disc guard: folded 1.5 mm hood with a front skirt (drawn as in the station model), screwed to the upper housing
    gd = box(-56, 62, -4, 14, zc, zc + 64) - Pos(0, 11.5, zc) * Rot(90, 0, 0) * Cylinder(54, 13.5, align=None)
    gd = gd - hole((0, 5, zc), "+y", 21, 40)
    gd = gd + box(52, 62, -4, 14, P["GUARD_GAP"], zc)
    for x in (-35, 35):
        gd = gd - hole((x, 5, 100), "+y", 3.3, 30)
    o.part(f"{who} disc guard, 1.5 mm sheet hood with front skirt{tag}", gd, YEL, "made", bomh, kg, g)
    for x in (-35, 35):
        o.many(tap_screw(6, 30, (x, -4, 100), "+y", bom=bomh, tag=f", disc guard{tag}"), kg, g)
    if ring_head:
        return o
    # drive case (DMP-DDR-003, Q3): crank shaft 12 T to 28 T, jackshaft 15 T to 15 T to the upper shaft
    jz, kx, kz = P["JACK_Z"], P["KCRANK_X"], P["KCRANK_Z"]
    pillars = ((-82.0, 28.0), (-82.0, 192.0), (40.0, 192.0))
    ip = eased(-90, 50, 74, 82, 18, 200, 0.8) - hole((0, 78, zc), "+y", 13, 20) - hole((0, 78, jz), "+y", 21, 20) - hole((kx, 78, kz), "+y", 21, 20)
    for x, z in ((-38, 30), (38, 30), (-38, 105), (38, 105)) + pillars:
        ip = ip - hole((x, 78, z), "+y", 4.4, 20)
    o.part("Drive case inner plate (8 mm, 140 x 182)", ip, YEL, "made", 10, "head_case", g)
    op = eased(-90, 50, 104, 112, 18, 200, 0.8) - hole((0, 108, jz), "+y", 21, 20) - hole((kx, 108, kz), "+y", 21, 20)
    for x, z in pillars:
        op = op - hole((x, 108, z), "+y", 4.4, 20)
    o.part("Drive case outer plate (8 mm, 140 x 182)", op, YEL, "made", 10, "head_case", g)
    band = box(-90, 50, 82, 104, 18, 200) - box(-88.5, 48.5, 81, 105, 19.5, 198.5)
    o.part("Drive case band, the chain guard (1.5 mm sheet)", band, YEL, "made", 10, "head_case", g)
    for x, z in pillars:
        o.part(f"Drive case pillar at ({x:.0f}, {z:.0f}) (12 x 1.8 tube, 22)", tube_run("y", 12, 1.8, 82, 104, x, z), BRIGHT, "made", 10,
               "head_case", g)
        o.many(bolt_set(8, 38, (x, 112, z), "-y", bom=10, tag=f", drive case pillar ({x:.0f}, {z:.0f})"), "head_case", g)
    for x, z in ((-38, 30), (38, 30), (-38, 105), (38, 105)):
        o.many(tap_screw(8, 25, (x, 82, z), "-y", bom=10, tag=f", drive case to housing ({x}, {z})"), "head_case", g)
    kd2 = "head_drive"
    for (x, z), nm in (((0.0, jz), "jackshaft"), ((kx, kz), "crank shaft")):
        o.part(f"Bearing 6004-2RS, {nm}, inner plate (bought)", bearing("y", 20, 42, 12, 74, x, z), BRIGHT, "bought", 10, kd2, g)
        o.part(f"Bearing 6004-2RS, {nm}, outer plate (bought)", bearing("y", 20, 42, 12, 100, x, z), BRIGHT, "bought", 10, kd2, g)
    o.part("Jackshaft (20 mm bright bar, 38)", rod("y", 10, 74, 112, 0, jz), BRIGHT, "made", 10, kd2, g)
    o.part("Crank shaft (20 mm bright bar, 44)", rod("y", 10, 74, 118, kx, kz), BRIGHT, "made", 10, kd2, g)
    o.part("Sprocket #35, 15 T, on the upper shaft (bought)", sprocket("y", P["SPR_A_R"], sr, 6, 86, 0, zc), BRIGHT, "bought", 10, kd2, g)
    o.part("Sprocket #35, 15 T, on the jackshaft (bought)", sprocket("y", P["SPR_A_R"], 10, 6, 86, 0, jz), BRIGHT, "bought", 10, kd2, g)
    o.part("Sprocket #35, 28 T, on the jackshaft (bought)", sprocket("y", P["SPR_C_R"], 10, 6, 94, 0, jz), BRIGHT, "bought", 10, kd2, g)
    o.part("Sprocket #35, 12 T, on the crank shaft (bought)", sprocket("y", P["SPR_D_R"], 10, 6, 94, kx, kz), BRIGHT, "bought", 10, kd2, g)
    o.part("Roller chain #35, jackshaft to upper shaft (bought)", chain_loop("xz", (0, zc), P["SPR_A_R"], (0, jz), P["SPR_A_R"], 86.5, 91.5),
           BRIGHT, "bought", 10, kd2, g, color="#2B2F33")
    o.part("Roller chain #35, crank shaft to jackshaft (bought)", chain_loop("xz", (kx, kz), P["SPR_D_R"], (0, jz), P["SPR_C_R"], 94.5, 99.5),
           BRIGHT, "bought", 10, kd2, g, color="#2B2F33")
    cr = P["CRANK_R"]
    o.part("Shear head crank arm (20 x 12 bar, 155 centres)", eased(kx - 10, kx + 10, 118, 130, kz - 10, kz + cr, 1.0), PS, "made", 10, kd2, g,
           color="#B45309")
    o.append(ring_weld((kx, 118, kz), "y", 10, 4, "-", tag=", crank arm to crank shaft", key=kd2, group=g))
    gz = kz + cr - 10
    gp = rod("y", 8, 130, 240, kx, gz) - split_pin_hole(16, (kx, 236.9, gz), "x")
    o.part("Shear head crank grip pin (16 mm bar)", gp, BRIGHT, "made", 10, kd2, g)
    o.append(ring_weld((kx, 130, gz), "y", 8, 3, "+", tag=", grip pin to crank arm", key=kd2, group=g))
    o.part("Shear head crank grip, free to spin (24 x 3.5 tube, 95)", tube_run("y", 24, 3.5, 134, 229, kx, gz), "hdpe_black", "made", 10, kd2, g)
    o.append(washer_at(16, (kx, 229, gz), "+y", bom=10, key=kd2, group=g, tag=", crank grip"))
    o.append(split_pin_at(16, (kx, 236.9, gz), "x", bom=10, key=kd2, group=g, tag=", crank grip"))
    return o


def spacer_link_parts(d):
    """Ring head spacer plate, coupling shaft with dogs and its guard sleeve, in the main head's frame (ring head 'd'
    along -Y), as part dicts; plus the two M12 screws that hold the spacer on the ring head's top plate."""
    zc = P["DISC_R"] - P["DISC_OVERLAP"] / 2
    sr = P["SHAFT_R"]
    o = Out()
    sp = eased(-145, -30, -d - 17, 20, 136, 146, 1.0)
    for x in (-120.0, -60.0):
        for yy in (0.0, -d):
            slot = hole((x, yy - 0.5, 141), "+z", 6.5, 12) + hole((x, yy + 0.5, 141), "+z", 6.5, 12) + box(x - 6.5, x + 6.5, yy - 0.5, yy + 0.5, 135, 147)
            sp = sp - slot
    o.part("Ring head spacer plate, slotted for 233 or 234 mm (10 mm, 115 x 270)", sp, PS, "made", 25, "ring_link", "tools", color="#D97706")
    cpl = rod("y", sr, -d + 74, -24, 0, zc) + cp.break_edges(box(-3, 3, -d + 66.5, -d + 74, zc - 12.0, zc + 12.0), 0.5) \
        + cp.break_edges(box(-3, 3, -24, -16.5, zc - 12.0, zc + 12.0), 0.5)
    o.part("Coupling shaft with dog ends (25 mm bar, 135)", cpl, BRIGHT, "made", 25, "ring_link", "tools")
    o.part("Coupling guard sleeve, loose (plastic tube 32 x 3)", ring("y", 13.0, 16.0, -d + 76, -26, 0, zc), "hdpe_natural", "made", 25,
           "ring_link", "tools")
    for x in (-120.0, -60.0):
        o.many(tap_screw(12, 25, (x, -d, 146), "-z", bom=25, tag=f", spacer plate to ring head at x {x:.0f}"), "ring_link", "tools")
    return o


def shear_head(o, L):
    xn, znip = P["HEAD_PARK_X"], L["z_nip"]
    o.extend(placed(Pos(xn, 0, znip), shear_head_parts()))


def tool_shelf(o, L):
    g = "tools"
    px, pr = P["POST_X"], P["POST_RHS"]
    pxo = -(px + pr / 2)
    bp = eased(pxo - 10, pxo, -100, 100, 450, 760, 1.0)
    for z in (550.0, 700.0):
        bp = bp - hole((pxo - 5, 0, z), "+x", 5.5, 20)
    o.part("Tool shelf back plate (10 mm, 200 x 310)", bp, PS, "made", 26, "shelf", g)
    o.part("Tool shelf (6 mm plate, 380 x 600)", eased(pxo - 380, pxo - 10, -300, 300, 600, 608, 1.0), PS, "made", 26, "shelf", g)
    for yc in (-100.0, 100.0):
        gus = tri_plate_y([(pxo - 10, 600), (pxo - 260, 600), (pxo - 10, 520)], yc - 3, yc + 3)
        o.part(f"Tool shelf gusset at y {yc:+.0f} (6 mm, 250 x 80)", gus, PS, "made", 26, "shelf", g)
        fy = "+y" if yc > 0 else "-y"
        o.append(weld_line((pxo - 10, yc + (3 if yc > 0 else -3), 524), (pxo - 10, yc + (3 if yc > 0 else -3), 596), fy, "-x", 4,
                           tag=f", gusset to back plate ({yc:+.0f})", key="shelf", group=g))
        o.append(weld_line((pxo - 254, yc + (3 if yc > 0 else -3), 600), (pxo - 16, yc + (3 if yc > 0 else -3), 600), fy, "-z", 4,
                           tag=f", gusset to shelf ({yc:+.0f})", key="shelf", group=g))
    o.append(weld_line((pxo - 10, -94, 600), (pxo - 10, 94, 600), "-x", "-z", 5, tag=", shelf to back plate, under", key="shelf", group=g))
    o.append(weld_line((pxo - 10, -40, 608), (pxo - 10, 100, 608), "-x", "+z", 5, tag=", shelf to back plate, top", key="shelf", group=g))
    for z in (550.0, 700.0):
        o.many(bolt_set(10, 70, (pxo - 10, 0, z), "+x", bom=26, tag=f", tool shelf at z {z:.0f}"), "shelf", g)
    # notching punch, its lever and the ring head, stored on the shelf as in the station model
    st_top = 608.0
    ppl = Pos(pxo - 48, -95, st_top + 50) * Rot(0, 0, 90)
    o.extend(placed(ppl, punch_parts()))
    o.part("Ratchet lever 500 mm with 24 mm hex socket (bought)", Pos(pxo - 357, -250, st_top) * M.punch_lever(P), "matte_black", "bought", 21,
           "punch_lever", g)
    d = P["RING_PITCH"]
    rpl = Pos(pxo - 180, -20 + d, st_top + 136)
    o.extend(placed(rpl * Pos(0, -d, 0), shear_head_parts(ring_head=True, tag=" (stored)")))
    o.extend(placed(rpl, spacer_link_parts(d)))


def punch_parts():
    """Lever notching punch (DMP-DDR-003, Q1) in its own frame, as part dicts."""
    o = Out()
    g = "tools"
    pl = M.notch_punch_local(P)
    hx, cl, cw = P["PUNCH_HOOP_X"], P["CHIME_NOTCH_L"], P["CHIME_NOTCH_W"] / 2
    hl_, hw = P["HOOP_NOTCH_L"] / 2, P["HOOP_NOTCH_W"] / 2
    stations = ((cl / 2, (-5.5, 40.5)), (hx, (hx - 22, hx + 22)))
    fr = pl["frame"]
    for cx, xs in stations:
        for x in xs:
            for y in (-17.0, 17.0):
                fr = fr - hole((x, y, 90), "+z", 4.0, 20.1)
    o.part("Notching punch C-frame (S355 plate, welded and ground)", fr, PS, "made", 21, "punch_frame", g, color="#7C2D12")
    o.part("Chime notch punch, D2, face raked 10 deg (60 x 35)", cp.break_edges(box(0.1, cl, -cw, cw, 25, 96), 0.5), BRIGHT, "made", 21,
           "punch_parts", g)
    o.part("Hoop slot punch, D2, face raked 10 deg (40 x 32)", cp.break_edges(box(hx - hl_, hx + hl_, -hw, hw, 20, 96), 0.5), BRIGHT, "made", 21,
           "punch_parts", g)
    for (cx, xs), nm in zip(stations, ("chime station", "hoop station")):
        o.part(f"Needle thrust bearing, {nm} (bought)", ring("z", 5, 12, 96, 100, cx, 0), BRIGHT, "bought", 21, "punch_parts", g)
        nb = box(cx - 30, cx + 30, -25, 25, 100, 130) - hole((cx, 0, 115), "+z", 12.2, 40)
        for x in xs:
            for y in (-17.0, 17.0):
                nb = nb - hole((x, y, 115), "+z", 4.4, 40)
        o.part(f"Bronze nut block Tr24 x 5, {nm} (60 x 50 x 30)", cp.break_edges(nb, 0.8), BRZ, "made", 21, "punch_parts", g)
        hexh = Pos(cx, 0, 135) * extrude(__import__("build123d").RegularPolygon(17.3, 6), 15)
        sc = rod("z", 12, 100, 135.5, cx, 0) + cp.break_edges(hexh, 0.8) + rod("z", 5, 96, 100.5, cx, 0, chamfer=0.3)
        o.part(f"Punch screw Tr24 x 5 with hex drive head, {nm}", sc, BRIGHT, "made", 21, "punch_parts", g)
        for x in xs:
            for y in (-17.0, 17.0):
                o.many(tap_screw(8, 40, (x, y, 130), "-z", bom=21, tag=f", nut block {nm} ({x:.0f}, {y:.0f})"), "punch_parts", g)
    return o


def end_cutter(o, L):
    g = "cutter"
    zax = L["z_ax"]
    half = P["DRUM_L"] / 2
    xh = half - P["HEAD_RECESS"]
    gz = zax + P["HOOP_R"] + P["GUIDE_R"]
    dz = zax + P["CHIME_R_IN"] - P["DRIVE_R"]
    px, pr = P["POST_X"], P["POST_RHS"]
    o.part("End cutter guide roller (30 mm, bored 12)", ring("x", 6, P["GUIDE_R"], half - 14, half, 0, gz), BRIGHT, "made", 11, "ec_guide", g)
    ga = rod("x", 6, 416, 500, 0, gz) - split_pin_hole(12, (419.7, 0, gz), "z")
    o.part("End cutter guide axle (12 mm bar)", ga, BRIGHT, "made", 11, "ec_guide", g)
    o.append(washer_at(12, (half - 14, 0, gz), "-x", bom=11, key="ec_guide", group=g, tag=", guide roller"))
    o.append(split_pin_at(12, (419.7, 0, gz), "z", bom=11, key="ec_guide", group=g, tag=", guide axle"))
    o.append(ring_weld((500, 0, gz), "x", 6, 3, "-", tag=", guide axle to body plate", key="ec_guide", group=g))
    o.part("End cutter knurled drive wheel (40 mm, bored 16)", ring("x", 8, P["DRIVE_R"], xh + 1, half - 1, 0, dz), BRIGHT, "made", 11, "ec_drive", g)
    o.part("End cutter drive shaft (16 mm bright bar)", rod("x", 8, xh + 1, 530, 0, dz), BRIGHT, "made", 11, "ec_drive", g)
    for a0 in (492.0, 512.0):
        o.part(f"End cutter shaft collar at x {a0:.0f} (28 x 8)", ring("x", 8, 14, a0, a0 + 8, 0, dz), BRIGHT, "made", 11, "ec_drive", g)
    cr = P["EC_CRANK_R"]
    o.part("End cutter crank arm (20 x 12 bar, 150 centres)", eased(530, 542, -10, 10, dz - 10, dz + cr + 10, 1.0), PS, "made", 11, "ec_drive", g,
           color="#B45309")
    o.append(ring_weld((530, 0, dz), "x", 8, 3, "-", tag=", end cutter crank arm to shaft", key="ec_drive", group=g))
    gzp = dz + cr
    gp = rod("x", 8, 542, 631, 0, gzp) - split_pin_hole(16, (627.9, 0, gzp), "z")
    o.part("End cutter crank grip pin (16 mm bar)", gp, BRIGHT, "made", 11, "ec_drive", g)
    o.append(ring_weld((542, 0, gzp), "x", 8, 3, "+", tag=", end cutter grip pin to arm", key="ec_drive", group=g))
    o.part("End cutter crank grip, free to spin (24 x 3.5 tube, 75)", tube_run("x", 24, 3.5, 545, 620, 0, gzp), "hdpe_black", "made", 11,
           "ec_drive", g)
    o.append(washer_at(16, (620, 0, gzp), "+x", bom=11, key="ec_drive", group=g, tag=", end cutter grip"))
    o.append(split_pin_at(16, (627.9, 0, gzp), "z", bom=11, key="ec_drive", group=g, tag=", end cutter grip"))
    phi = P["CUTTER_PHI"]
    T0 = Pos(0, 0, zax) * Rot(-phi, 0, 0)
    xw = xh + P["CUTTER_R"]
    cut = T0 * Pos(xw, 0, P["CUT_LINE_R"]) * ring("z", 6.1, P["CUTTER_R"], -P["CUTTER_T"] / 2, P["CUTTER_T"] / 2, 0, 0, edge=0.4)
    o.part("End cutter wheel, hardened, 50 x 6 (bought)", cut, "stainless", "bought", 11, "ec_cutter", g)
    stud = T0 * rod("z", 6, P["CUT_LINE_R"] - 3 - 12, 345, xw, 0)
    o.part("End cutter arm, 12 mm bar threaded M12 at the wheel", stud, BRIGHT, "made", 11, "ec_body", g)
    o.append(dict(nut_at(12, (0, 0, 0), "-z", bom=11, key="ec_body", group=g, name="M12 hex nut clamping the cutter wheel"),
                  shape=T0 * Pos(xw, 0, P["CUT_LINE_R"] - P["CUTTER_T"] / 2) * Rot(180, 0, 0) * cp.hex_nut(12)))
    cy_, cz_ = M.polar(phi, 340, 0, zax)[1:]
    link = box(xw - 6, 500, cy_ - 12, cy_ + 12, cz_ - 6, cz_ + 14) - T0 * hole((xw, 0, 330), "+z", 6.0, 60)
    o.part("End cutter arm link (24 x 20 bar, welded to the arm)", link, PS, "made", 11, "ec_body", g,
           color="#7C3AED")
    body = eased(500, 512, -80, 80, zax + 240, zax + 360, 1.0) - hole((506, 0, dz), "+x", 8.5, 20)
    o.part("End cutter body plate (12 mm, 160 x 120)", body, PS, "made", 11, "ec_body", g, color="#7C3AED")
    cov = T0 * box(half + 1, xh + 2 * P["CUTTER_R"] + 3, -30, 30, P["CUT_LINE_R"] + 5, P["CUT_LINE_R"] + 8)
    cov = cov + T0 * box(xh + 2 * P["CUTTER_R"] + 3, 500, -30, 30, P["CUT_LINE_R"] - 20, P["CUT_LINE_R"] + 8)
    cov = cov - T0 * hole((xw, 0, P["CUT_LINE_R"] + 6), "+z", 6.2, 20)
    o.part("End cutter wheel cover (3 mm sheet, welded to the body plate)", cov, YEL, "made", 11, "ec_body", g)
    o.part("Torque arm, upright (30 x 12 bar, 88)", eased(500, 512, -15, 15, zax + 360, zax + 448, 0.8), PS, "made", 11, "ec_body", g, color="#7C3AED")
    o.part("Torque arm, reach to the rail post (30 x 8 bar, 170)", eased(512, px - pr / 2, -15, 15, zax + 440, zax + 448, 0.8), PS, "made", 11,
           "ec_body", g, color="#7C3AED")
    for sy in (-1, 1):
        o.append(weld_line((501, sy * 15, zax + 360), (511, sy * 15, zax + 360), "+y" if sy > 0 else "-y", "+z", 4,
                           tag=f", torque arm to body plate ({sy:+d})", key="ec_body", group=g))
    o.append(weld_line((512, -14, zax + 440), (512, 14, zax + 440), "+x", "-z", 4, tag=", torque arm reach to upright", key="ec_body", group=g))
    for z, v in ((cz_ + 14, "+z"), (cz_ - 6, "-z")):
        o.append(weld_line((500, cy_ - 11, z), (500, cy_ + 11, z), "-x", v, 4, tag=f", arm link to body plate ({v})", key="ec_body", group=g))


# =================================================================================================================
# Station 3: slip roll stand
# =================================================================================================================
def slip_roll(o, L):
    g = "roll"
    ry, sx_, st_ = P["RS_Y"], P["SIDE_X"], P["SIDE_T"]
    lz, uz, bz = P["LOWER_Z"], L["upper_z"], L["bend_z"]
    by_ = ry + P["BEND_Y"]
    jr = P["JOURNAL_R"]
    z1 = P["SIDE_Z1"]
    zb = z1 + 25
    # base: two cross rails along Y and two long rails along X between them (60 x 60 x 3)
    foot_bolts = {}
    for s in (-1, 1):
        for yy in (-120.0, 190.0):
            xm = s * 467.5
            foot_bolts[(s, yy)] = [s * 392.5, s * 427.5]
    for sx in (-1, 1):
        o.part(f"Roll stand cross rail, {'left' if sx < 0 else 'right'} (60 x 60 x 3 RHS, 800)",
               rhs_run("y", (ry - 400, ry + 400), (sx * 530 - 30, sx * 530 + 30), (0, 60), 3), PS, "made", 12, "rs_base", g)
    for y0_ in (-150.0, 160.0):
        r = rhs_run("x", (-500, 500), (ry + y0_, ry + y0_ + 60), (0, 60), 3)
        yy = y0_ + 30
        for s in (-1, 1):
            for bx in foot_bolts[(s, yy)]:
                r = r - hole((bx, ry + yy, 57), "+z", 6.5, 8) - hole((bx, ry + yy, 3), "+z", 12, 8)
        o.part(f"Roll stand long rail at y {y0_ + 30:+.0f} (60 x 60 x 3 RHS, 1,000), with 24 mm access holes", r, PS, "made", 12, "rs_base", g)
        for sx in (-1, 1):
            for yf, u in ((ry + y0_, "-y"), (ry + y0_ + 60, "+y")):
                o.append(weld_line((sx * 500, yf, 6), (sx * 500, yf, 54), u, "-x" if sx > 0 else "+x", 4,
                                   tag=f", long rail to cross rail ({sx:+d}, {y0_:+.0f}, {u})", key="rs_base", group=g))
    # side frames: plate, legs with foot plates, bolted top bridge
    for s in (-1, 1):
        nm = "left" if s < 0 else "right"
        xo0, xo1 = sorted((s * sx_, s * (sx_ + st_)))
        xc = s * (sx_ + st_ / 2)
        plate = box(xo0, xo1, ry + P["SIDE_Y0"], ry + P["SIDE_Y1"], P["SIDE_Z0"], z1)
        plate -= Pos(xc, ry, lz) * Rot(0, 90, 0) * Cylinder(20, 100)
        plate -= box(xo0 - 1, xo1 + 1, ry - 30, ry + 30, 900, z1 + 1)
        plate -= box(xo0 - 1, xo1 + 1, by_ - 30, by_ + 30, 840, z1 + 1)
        for yy in (-90.0, 170.0):
            plate -= hole((xc, ry + yy, z1 - 7.5), "+z", 5.0, 15.1)
        if s > 0:
            for z in (780.0, 830.0):
                plate -= hole((xc, ry - 125, z), "+x", 5.5, 40)
        else:
            for yy in (-40.0, 40.0):
                plate -= hole((-sx_ - st_ + 7, ry + yy, 984), "+x", 3.0, 14.1)
        for yy in (-40.0, 135.0):
            plate -= hole((s * (sx_ + 4), ry + yy, 990), "+x", 2.5, 8.1)
        for yk, zk in ((ry - 35, 940.0), (ry + 35, 940.0), (by_ - 35, 905.0), (by_ + 35, 905.0)):
            plate -= hole((s * (sx_ + 4), yk, zk), "+x", 2.5, 8.1)
        o.part(f"Side frame plate, {nm} (20 mm, 370 x 250, bored 40, two 60 mm slots)", cp.break_edges(plate, 0.8), PS, "made", 13, "rs_sides", g,
               color="#0F766E")
        lx0, lx1 = sorted((s * (sx_ - 17.5), s * (sx_ + 32.5)))
        for yy in (-120.0, 190.0):
            o.part(f"Side frame leg, {nm} at y {yy:+.0f} (50 x 50 x 3 RHS, 694)", rhs_run("z", (66, P["SIDE_Z0"]), (lx0, lx1), (ry + yy - 25, ry + yy + 25), 3),
                   PS, "made", 13, "rs_sides", g, color="#0F766E")
            fx0, fx1 = sorted((s * 377.5, s * 497.5))
            fp = eased(fx0, fx1, ry + yy - 40, ry + yy + 40, 60, 66, 1.0)
            for bx in foot_bolts[(s, yy)]:
                fp = fp - hole((bx, ry + yy, 63), "+z", 6.5, 10)
            o.part(f"Side frame foot plate, {nm} at y {yy:+.0f} (6 mm, 120 x 80)", fp, PS, "made", 13, "rs_sides", g, color="#0F766E")
            for w in box_welds(lx0, lx1, ry + yy - 25, ry + yy + 25, 66, "+z", 4, margin=6, tag=f", side frame leg to foot, {nm} {yy:+.0f}",
                               key="rs_sides", group=g):
                o.append(w)
            for xf, u in ((xo0, "-x"), (xo1, "+x")):
                if s > 0 and yy < 0 and u == "+x":
                    continue          # the crank bracket covers this corner
                o.append(weld_line((xf, ry + yy - 19, P["SIDE_Z0"]), (xf, ry + yy + 19, P["SIDE_Z0"]), u, "+z", 4,
                                   tag=f", side frame leg to plate, {nm} {yy:+.0f} {u}", key="rs_sides", group=g))
            for bx in foot_bolts[(s, yy)]:
                o.many(bolt_set(12, 9, (bx, ry + yy, 66), "-z", bom=13, tag=f", side frame foot {nm} {yy:+.0f}"), "rs_sides", g)
        bx0, bx1 = (xo0 - 5, xo1) if s < 0 else (xo0, xo1 + 5)
        br = box(bx0, bx1, ry - 150, ry + 220, z1, zb) - hole((xc, ry, z1 + 12.5), "+z", 8, 40) - hole((xc, by_, z1 + 12.5), "+z", 10, 40)
        for yy in (-90.0, 170.0):
            br = br - hole((xc, ry + yy, z1 + 12.5), "+z", 5.5, 40)
        br = br - hole((xc, by_ + 56, zb - 6), "+z", 3, 12.1)
        o.part(f"Side frame top bridge, {nm} (25 mm bar, 370), tapped M16 and M20 x 1.5", cp.break_edges(br, 0.8), PS, "made", 13, "rs_sides", g,
               color="#0F766E")
        for yy in (-90.0, 170.0):
            o.many(tap_screw(10, 35, (xc, ry + yy, zb), "-z", bom=13, tag=f", top bridge {nm} {yy:+.0f}"), "rs_sides", g)
        # bushes, slide blocks, screws, dial adjuster
        fl0, fl1 = sorted((s * (sx_ + st_), s * (sx_ + st_ + 6)))
        for (yb, zbz), what in (((ry, lz), "lower roll"), ((ry, uz), "upper roll"), ((by_, bz), "bending roll")):
            bu = ring("x", jr, 20, xo0, xo1, yb, zbz) + ring("x", jr, 26, fl0, fl1, yb, zbz)
            o.part(f"Flanged bronze bush 30 x 40 x 20, {what}, {nm} (bought)", bu, BRZ, "bought", 15, "rs_bushes", g)
        for (yb, zbz), what in (((ry, uz), "upper roll"), ((by_, bz), "bending roll")):
            blk = box(xo0, xo1, yb - 30, yb + 30, zbz - 30, zbz + 30) - Pos(xc, yb, zbz) * Rot(0, 90, 0) * Cylinder(20, 100)
            o.part(f"Slide block, {what}, {nm} (20 x 60 x 60, bored 40)", cp.break_edges(blk, 0.5), BRIGHT, "made", 15, "rs_blocks", g)
        kx0, kx1 = sorted((s * (sx_ - 3), s * sx_))
        for (yk, z0k, zh), what in (((ry, 900.0, uz), "pinch slot"), ((by_, 840.0, bz), "bending slot")):
            kp = eased(kx0, kx1, yk - 40, yk + 40, z0k, 975, 0.8) - hole(((kx0 + kx1) / 2, yk, zh), "+x", 16, 10)
            for dy in (-35.0, 35.0):
                kp = kp - hole(((kx0 + kx1) / 2, yk + dy, 940.0 if what == "pinch slot" else 905.0), "+x", 2.75, 10)
            o.part(f"Slide block keeper plate, {what}, {nm} (3 mm)", kp, "galvanised", "made", 15, "rs_blocks", g)
            for dy in (-35.0, 35.0):
                o.many(tap_screw(5, 10, (s * (sx_ - 3), yk + dy, 940.0 if what == "pinch slot" else 905.0), "+x" if s > 0 else "-x", bom=15,
                                 tag=f", keeper plate {what} {nm} {dy:+.0f}"), "rs_blocks", g)
        slab = box(min(xo0, xo1) + 1, max(xo0, xo1) - 1, -1e4, 1e4, 0, 2000)       # collars flatted to pass the 20 mm plate
        sc = rod("z", 8, uz + 30, z1 + 72, xc, ry) + (ring("z", 8, 12, uz + 30, uz + 38, xc, ry) & slab)
        o.part(f"Pinch screw M16 with flatted captive collar, {nm}", sc, BRIGHT, "made", 15, "rs_screws", g)
        o.part(f"Pinch screw handwheel 90 mm, {nm}", Pos(xc, ry, z1 + 66) * handwheel(90, 10, 15, 16, 8.0), RED, "bought", 15, "rs_screws", g)
        sb = rod("z", 10, bz + 30, z1 + 102, xc, by_) + (ring("z", 10, 14, bz + 30, bz + 38, xc, by_) & slab)
        o.part(f"Bending screw M20 x 1.5 with flatted captive collar, {nm}", sb, BRIGHT, "made", 15, "rs_screws", g)
        o.part(f"Bending screw handwheel 110 mm, {nm}", Pos(xc, by_, z1 + 96) * handwheel(110, 12, 17, 18, 10.0), RED, "bought", 15, "rs_screws", g)
        o.append(nut_at(20, (xc, by_, zb), "+z", bom=15, key="rs_dials", group=g, name=f"M20 x 1.5 lock nut on the bridge, {nm}"))
        o.part(f"Bending dial, 60 divisions (80 dia x 8), {nm}", ring("z", 10.0, 40, zb + 20, zb + 28, xc, by_), "aluminium", "made", 15, "rs_dials", g)
        ptr = box(xc - 5, xc + 5, by_ + 45, by_ + 50, zb + 3, zb + 31) + box(xc - 5, xc + 5, by_ + 36, by_ + 45, zb + 28, zb + 31) \
            + box(xc - 5, xc + 5, by_ + 45, by_ + 62, zb, zb + 3) - hole((xc, by_ + 56, zb + 1.5), "+z", 3.3, 6)
        o.part(f"Dial pointer (3 mm stainless strip), {nm}", ptr, "stainless", "made", 15, "rs_dials", g)
        o.many(tap_screw(6, 12, (xc, by_ + 56, zb + 3), "-z", bom=15, tag=f", dial pointer {nm}"), "rs_dials", g)
    # rolls and pinch gears
    face, rr = P["ROLL_FACE"] / 2, P["ROLL_R"]
    for nm, y, z, j0, j1, key, what in (("Lower pinch roll (driven), C45, 1,092", ry, lz, -540, 552, "roll_lower", "lower"),
                                        ("Upper pinch roll, C45, 1,032", ry, uz, -540, 492, "roll_upper", "upper"),
                                        ("Bending roll, C45, 984", by_, bz, -492, 492, "roll_bend", "bending")):
        shp = Pos(0, y, z) * Rot(0, 90, 0) * Cylinder(rr, 2 * face) + rod("x", jr, j0, j1, y, z, chamfer=0.8)
        o.part(nm, shp, BRIGHT, "made", 14, key, g)
    for z, nm in ((lz, "lower"), (uz, "upper")):
        o.part(f"Pinch gear, module 3, 20 T, {nm} roll (bought)", ring("x", jr, P["GEAR_R"], -530, -510, ry, z, edge=0.5), BRIGHT, "bought", 16, "gears", g,
               color="#1D4ED8")
    # crank bracket and chain drive (+X side)
    cy0, cz0 = ry + P["CRANK_Y"], P["CRANK_Z"]
    xo = sx_ + st_
    brk = eased(xo, xo + 10, ry - 290, ry - 100, 760, 880, 1.0) - hole((xo + 5, cy0, cz0), "+x", 13, 20)
    for z in (780.0, 830.0):
        brk = brk - hole((xo + 5, ry - 125, z), "+x", 5.5, 20)
    o.part("Crank bracket (10 mm plate, 190 x 120)", brk, PS, "made", 17, "rs_bracket", g, color="#0F766E")
    for z in (780.0, 830.0):
        o.many(bolt_set(10, 30, (xo + 10, ry - 125, z), "-x", bom=17, tag=f", crank bracket at z {z:.0f}"), "rs_bracket", g)
    hsg = tube_run("x", 50, 6, xo + 10, 530, cy0, cz0)
    for dz in (-22.0, 22.0):
        hsg = hsg - hole((524, cy0, cz0 + dz), "+x", 3.0, 12.1)
    o.part("Crank bearing housing, two M6 tapped holes in its end (50 x 6 tube, 40)", hsg, PS, "made", 17, "rs_bracket", g, color="#0F766E")
    tube_end = 530.0
    for a0 in (xo + 10, xo + 30):
        o.part(f"Crank shaft bronze bush at x {a0:.0f} (25 x 38 x 20, bought)", ring("x", 12.5, 19, a0, a0 + 20, cy0, cz0), BRZ, "bought", 17,
               "rs_bracket", g)
    o.append(ring_weld((xo + 10, cy0, cz0), "x", 25, 4, "+", tag=", bearing housing to crank bracket", key="rs_bracket", group=g))
    o.part("Slip roll crank shaft (25 mm bright bar, 85)", rod("x", 12.5, xo, 565, cy0, cz0), BRIGHT, "made", 17, "rs_crank", g)
    o.part("Slip roll crank arm (24 x 12 bar, 300 centres)", eased(565, 577, cy0 - 12, cy0 + 12, cz0 - 12, cz0 + P["RS_CRANK_R"] + 12, 1.0), PS,
           "made", 17, "rs_crank", g, color="#B45309")
    o.append(ring_weld((565, cy0, cz0), "x", 12.5, 4, "-", tag=", slip roll crank arm to shaft", key="rs_crank", group=g))
    gz = cz0 + P["RS_CRANK_R"]
    gp = rod("x", 8, 577, 679, cy0, gz) - split_pin_hole(16, (675.9, cy0, gz), "z")
    o.part("Slip roll crank grip pin (16 mm bar)", gp, BRIGHT, "made", 17, "rs_crank", g)
    o.append(ring_weld((577, cy0, gz), "x", 8, 3, "+", tag=", slip roll grip pin to arm", key="rs_crank", group=g))
    o.part("Slip roll crank grip, free to spin (28 x 4 tube, 88)", tube_run("x", 28, 4, 580, 668, cy0, gz), "hdpe_black", "made", 17, "rs_crank", g)
    o.append(washer_at(16, (668, cy0, gz), "+x", bom=17, key="rs_crank", group=g, tag=", slip roll grip"))
    o.append(split_pin_at(16, (675.9, cy0, gz), "z", bom=17, key="rs_crank", group=g, tag=", slip roll grip"))
    o.part("Sprocket #40, 39 T, on the lower roll (bought)", sprocket("x", P["SPROCKET_BIG_R"], jr, 8, 540, ry, lz, hub_r=28, hub_l=10, hub_side=1),
           BRIGHT, "bought", 17, "sprockets", g)
    o.part("Sprocket #40, 13 T, on the crank shaft (bought)", sprocket("x", P["SPROCKET_SMALL_R"], 12.5, 8, 540, cy0, cz0, hub_r=20, hub_l=10, hub_side=1),
           BRIGHT, "bought", 17, "sprockets", g)
    o.part("Roller chain #40, about 1.3 m (bought)", chain_loop("yz", (ry, lz), P["SPROCKET_BIG_R"], (cy0, cz0), P["SPROCKET_SMALL_R"], 541, 547,
                                                                 clear=0.5, depth=6.5), BRIGHT, "bought", 17, "sprockets", g, color="#2B2F33")
    # guards (1.5 mm sheet, every one needs a tool to remove)
    cg = box(530, 560, ry - 265, ry + 90, 780, 960) - box(531.5, 558.5, ry - 263.5, ry + 88.5, 781.5, 958.5)
    cg -= Pos(545, cy0, cz0) * Rot(0, 90, 0) * Cylinder(13, 50)
    cg -= Pos(527.5, ry, lz) * Rot(0, 90, 0) * Cylinder(jr + 1, 15)
    for dz in (-22.0, 22.0):
        cg -= hole((530.75, cy0, cz0 + dz), "+x", 3.3, 4)
    o.part("Chain guard box (1.5 mm sheet)", cg, YEL, "made", 18, "rs_guards", g)
    for dz in (-22.0, 22.0):
        o.many(tap_screw(6, 12, (531.5, cy0, cz0 + dz), "-x", bom=18, tag=f", chain guard {dz:+.0f}"), "rs_guards", g)
    gx = -(sx_ + st_)
    gg = box(-545, gx, ry - 45, ry + 45, 830, 975) - box(-543.5, gx + 5, ry - 43.5, ry + 43.5, 831.5, 973.5)
    gg = gg + box(gx - 1.5, gx, ry - 48, ry + 48, 975, 992)
    for yy in (-40.0, 40.0):
        gg = gg - hole((gx - 0.75, ry + yy, 984), "+x", 3.3, 4)
    o.part("Gear guard box with fixing tab (1.5 mm sheet)", gg, YEL, "made", 18, "rs_guards", g)
    for yy in (-40.0, 40.0):
        o.many(tap_screw(6, 14, (gx - 1.5, ry + yy, 984), "+x", bom=18, tag=f", gear guard {yy:+.0f}"), "rs_guards", g)
    tg = P["TABLE_TOP"] + P["GUARD_GAP"]
    nip = box(-sx_, sx_, ry - 52, ry - 50, tg, 1000) + box(-sx_, sx_, ry - 52, ry + 152, 1000, 1002) \
        + box(-sx_, sx_, ry + 150, ry + 152, P["OUT_TABLE_TOP"] + P["GUARD_GAP"], 1000)
    for s in (-1, 1):
        for yy in (-40.0, 135.0):
            nip = nip - hole((s * 450, ry + yy, 1001), "+z", 2.75, 4)
    o.part("Nip guards and lid, folded (1.5 mm sheet), 8 mm slots", nip, YEL, "made", 18, "rs_guards", g)
    for s in (-1, 1):
        for yy in (-40.0, 135.0):
            y0 = ry + yy - (10 if yy < 0 else 12)
            if s > 0:
                ang = angle_run((sx_, y0, 1000), (-1, 0, 0), (0, 0, -1), (0, 1, 0), 24, a=20, t=2)
            else:
                ang = angle_run((-sx_, y0, 1000), (1, 0, 0), (0, 0, -1), (0, 1, 0), 24, a=20, t=2)
            ang = ang - hole((s * 450, ry + yy, 999), "+z", 2.75, 4) - hole((s * (sx_ - 1), ry + yy, 990), "+x", 2.75, 4)
            o.part(f"Lid clip angle 20 x 20 x 2, {'left' if s < 0 else 'right'} at y {yy:+.0f}", ang, "galvanised", "made", 18, "rs_guards", g)
            o.many(tap_screw(5, 10, (s * (sx_ - 2), ry + yy, 990), "+x" if s > 0 else "-x", bom=18,
                             tag=f", lid clip to side frame ({s:+d}, {yy:+.0f})"), "rs_guards", g)
            o.many(bolt_set(5, 4, (s * 450, ry + yy, 1002), "-z", bom=18, tag=f", lid to clip ({s:+d}, {yy:+.0f})"), "rs_guards", g)
    # in-feed and out-feed tables
    for nm, y0, y1, top, legs in (("In-feed", ry - 850, ry - 35, P["TABLE_TOP"], (-810.0, -420.0)),
                                  ("Out-feed", ry + 125, ry + 935, P["OUT_TABLE_TOP"], (420.0, 895.0))):
        zt = top - 18
        tp = eased(-450, 450, y0, y1, zt, top, 1.0)
        scr = [(sx * 430, y) for sx in (-1, 1) for y in (y0 + 150, y1 - 150)]
        for x, y in scr:
            tp = tp - hole((x, y, zt + 7.5), "+z", 3.0, 15.1)
        o.part(f"{nm} table top (18 mm exterior plywood, 900 x {y1 - y0:.0f})", tp, PY, "made", 19, "tables", g)
        fr = []
        fr.append(angle_run((-450, y0, zt), (0, 1, 0), (0, 0, -1), (1, 0, 0), 900))
        fr.append(angle_run((-450, y1, zt), (0, -1, 0), (0, 0, -1), (1, 0, 0), 900))
        side_l = angle_run((-450, y0 + 40, zt), (1, 0, 0), (0, 0, -1), (0, 1, 0), y1 - y0 - 80)
        side_r = angle_run((450, y0 + 40, zt), (-1, 0, 0), (0, 0, -1), (0, 1, 0), y1 - y0 - 80)
        for x, y in scr:
            if x < 0:
                side_l = side_l - hole((x, y, zt - 1.5), "+z", 3.3, 5)
            else:
                side_r = side_r - hole((x, y, zt - 1.5), "+z", 3.3, 5)
        fr += [side_l, side_r]
        for i, a in enumerate(fr):
            o.part(f"{nm} table frame angle {i + 1} (40 x 40 x 3)", a, PS, "made", 19, "table_frames", g)
        for x, y in scr:
            o.many(coach(6, 16, (x, y, zt - 3), "+z", bom=19, tag=f", {nm.lower()} table top ({x:+.0f}, {y - ry:+.0f})"), "tables", g)
        for sx in (-1, 1):
            for yy in legs:
                xl0, xl1 = sx * 410 - 20, sx * 410 + 20
                yc_ = ry + yy
                lnm = f"{nm.lower()} table leg ({'left' if sx < 0 else 'right'}, y {yy:+.0f})"
                o.part(f"{nm} table leg ({'left' if sx < 0 else 'right'}, y {yy:+.0f}) (40 x 40 x 3 RHS)",
                       rhs_run("z", (25, zt - 3), (xl0, xl1), (yc_ - 20, yc_ + 20), 3), PS, "made", 19, "table_frames", g)
                o.part(f"Leg cap plate, {lnm} (3 mm, 50 x 50)", eased(xl0 - 5, xl1 + 5, yc_ - 25, yc_ + 25, 22, 25, 0.6) - hole((sx * 410, yc_, 23.5), "+z", 5.5, 6),
                       PS, "made", 19, "table_frames", g)
                o.append(nut_at(10, (sx * 410, yc_, 25), "+z", bom=19, key="table_frames", group=g, name=f"M10 hex nut welded in the {lnm}"))
                for w in box_welds(xl0, xl1, yc_ - 20, yc_ + 20, 25, "+z", 3, sides="ew", margin=5, tag=f", {lnm} to cap", key="table_frames", group=g):
                    o.append(w)
                foot = cp.break_edges(Pos(sx * 410, yc_, 4) * Cylinder(15, 8), 1.5) + rod("z", 5, 8, 33, sx * 410, yc_)
                o.part(f"Levelling screw M10 with 30 mm pad, {lnm} (bought)", foot, ZN, "bought", 19, "table_frames", g)
                xf, u = (xl1, "+x") if sx > 0 else (xl0, "-x")
                o.append(weld_line((xf, ry + yy - 14, zt - 3), (xf, ry + yy + 14, zt - 3), u, "-z", 3,
                                   tag=f", {nm.lower()} table leg to frame ({sx:+d}, {yy:+.0f})", key="table_frames", group=g))


# =================================================================================================================
def context(o, L):
    from build123d import Pos as Ps, Rot as Rt
    y0 = P["DS_Y"]
    ro = P["DRUM_R_IN"] + P["DRUM_T"]
    h = math.sqrt(ro ** 2 - P["DS_CHOCK_Y"] ** 2)
    xs = P["DS_SADDLE_X"]
    tilt = math.degrees(math.atan2(P["DS_TOP_HI"] - P["DS_TOP_LO"], 2 * xs))
    zc = (P["DS_TOP_HI"] + P["DS_TOP_LO"]) / 2 + h / math.cos(math.radians(tilt)) + 1.1
    o.part("Drum being purged (context)", Ps(0, y0, zc) * Rt(0, tilt, 0) * M.drum(P), PS, "context", None, "drum_ds", "context", color="#9B2C2C")
    o.part("Drum on the cradle (context)", Ps(0, 0, L["z_ax"]) * M.drum(P, bung_phi=90.0), PS, "context", None, "drum", "context", color="#1F4E9C")
    o.part("Three drum body panels being fed (context)", Ps(0, P["RS_Y"], P["TABLE_TOP"]) * M.curled_sheet(P), PS, "context", None, "sheet",
           "context", color="#1F4E9C")


def build(with_context=True):
    L = M.levels(P)
    o = Out()
    drain_stand(o)
    drain_stand(o, -1600.0, "2")
    cradle_frame(o, L)
    rollers(o, L)
    brake(o, L)
    posts_and_beam(o, L)
    trolley(o, L)
    drop_and_pivot(o, L)
    shear_head(o, L)
    tool_shelf(o, L)
    end_cutter(o, L)
    slip_roll(o, L)
    if with_context:
        context(o, L)
    return list(o)
