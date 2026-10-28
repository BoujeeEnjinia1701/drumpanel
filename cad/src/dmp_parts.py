"""DrumPanel repo-specific CAD helpers (kit 1.9). Built on .kit/cad_parts.py; nothing here belongs in .kit/.

Helpers the parts library does not have (suggested kit additions are listed in docs/REVIEW.md):
    box(x0, x1, y0, y1, z0, z1)       an axis-aligned block by its ranges
    orient(shape, d)                  turn a part built along +Z to point along +x, -x, +y, -y, +z or -z
    tube(axis, ...), rhs_run(...)     real EN 10219 hollow sections placed by their ranges, like the station model
    bolt_set(...), tap_screw(...)     an ISO 4017 bolt with washers and nut, or a bolt into a tapped hole, as part() dicts
    coach(...)                        a DIN 571 coach screw with washer into timber
    weld_line(...)                    a fillet weld bead along an axis-aligned corner
    ring_weld(...)                    a fillet weld bead round a shaft or tube where it meets a plate face
    chain_loop(...)                   a roller chain round two sprockets, drawn as a closed band
    hole(...)                         a drilled hole along any axis (to subtract)
    bearing(...), sprocket(...)       catalogue envelopes of a ball bearing and a plate sprocket with its hub
All sizes in millimetres.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, extrude, revolve, Axis  # noqa: E402
import cad_parts as cp  # noqa: E402

ROT_TO = {"+z": (0, 0, 0), "-z": (180, 0, 0), "+x": (0, 90, 0), "-x": (0, -90, 0), "+y": (-90, 0, 0), "-y": (90, 0, 0)}
VEC = {"+x": (1, 0, 0), "-x": (-1, 0, 0), "+y": (0, 1, 0), "-y": (0, -1, 0), "+z": (0, 0, 1), "-z": (0, 0, -1)}
OPP = {"-z": "+z", "+z": "-z", "+x": "-x", "-x": "+x", "+y": "-y", "-y": "+y"}
ZINC = "zinc_plated"
WELD = "mild_steel"


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def eased(x0, x1, y0, y1, z0, z1, r=1.0):
    """A sawn or flame-cut plate block with its edges broken (not a bare box)."""
    return cp.break_edges(box(x0, x1, y0, y1, z0, z1), r)


def orient(shape, d):
    return Rot(*ROT_TO[d]) * shape


def add(a, b, k=1.0):
    return tuple(x + k * y for x, y in zip(a, b))


def hole(xyz, d, r, length, both=True):
    """A cylinder of radius r along direction d ('+x' ...) from xyz (centred on xyz when both)."""
    c = Pos(0, 0, 0 if both else length / 2) * Cylinder(r, length)
    return Pos(*xyz) * orient(c, d)


def rod(axis, r, a0, a1, p, q, chamfer=0.5):
    """Round bar of radius r along axis 'x', 'y' or 'z' from a0 to a1; (p, q) are the other two coordinates in
    x, y, z order. Ends chamfered, as cut bright bar is."""
    s = cp.round_bar(2 * r, a1 - a0, chamfer_ends=chamfer)
    if axis == "x":
        return Pos(a0, p, q) * orient(s, "+x")
    if axis == "y":
        return Pos(p, a0, q) * orient(s, "+y")
    return Pos(p, q, a0) * s


def ring(axis, ri, ro, a0, a1, p, q, edge=0.3):
    """Thick ring (bush, roller, washer-like part) along an axis."""
    from build123d import Circle, Sketch
    s = extrude(Sketch() + Circle(ro) - Circle(ri), a1 - a0)
    if edge:
        s = cp.break_edges(s, edge)
    if axis == "x":
        return Pos(a0, p, q) * orient(s, "+x")
    if axis == "y":
        return Pos(p, a0, q) * orient(s, "+y")
    return Pos(p, q, a0) * s


def rhs_run(axis, a, r1, r2, t):
    """EN 10219 hollow section along axis 'x', 'y' or 'z' over the range a = (a0, a1); r1 and r2 are the ranges of
    the other two axes in x, y, z order (the section's outer faces), as in the station model's rhs()."""
    (a0, a1), (b0, b1), (c0, c1) = a, r1, r2
    L = a1 - a0
    if axis == "x":            # r1 = y range, r2 = z range; local X (w) -> -Z after along('x'); w = z span, h = y span
        s = cp.along(cp.rhs(c1 - c0, b1 - b0, t, L), "x")
        return Pos(a0, (b0 + b1) / 2, (c0 + c1) / 2) * s
    if axis == "y":            # r1 = x range, r2 = z range; local X stays X, local Y -> -Z
        s = cp.along(cp.rhs(b1 - b0, c1 - c0, t, L), "y")
        return Pos((b0 + b1) / 2, a0, (c0 + c1) / 2) * s
    s = cp.rhs(b1 - b0, c1 - c0, t, L)     # r1 = x range, r2 = y range
    return Pos((b0 + b1) / 2, (c0 + c1) / 2, a0) * s


def tube_run(axis, od, t, a0, a1, p, q):
    s = cp.round_tube(od, t, a1 - a0)
    if axis == "x":
        return Pos(a0, p, q) * orient(s, "+x")
    if axis == "y":
        return Pos(p, a0, q) * orient(s, "+y")
    return Pos(p, q, a0) * s


# ---------------------------------------------------------------------------------------------------------------
# Fasteners as part() dicts
# ---------------------------------------------------------------------------------------------------------------
def _pd(name, shape, material, kind, bom, group, explode, key, tag=""):
    p = cp.part(f"{name}{tag}", shape, material, kind, bom=bom, group=group, explode=explode)
    p["key"] = key
    return p


def bolt_set(d, grip, xyz, shank, bom=23, group="fixings", key="bolts", tag="", explode=(0, 0, 0)):
    """ISO 4017 bolt, two ISO 7089 washers and an ISO 4032 nut through a joint 'grip' thick. xyz is the centre of
    the joint face on the head side; shank is the direction the bolt points into the joint."""
    up = OPP[shank]
    return [_pd(n, Pos(*xyz) * orient(s, up), ZINC, "fastener", bom, group, explode, key, tag) for n, s in cp.hex_bolt_set(d, grip)]


def tap_screw(d, length, xyz, shank, bom=23, group="fixings", key="bolts", tag="", explode=(0, 0, 0), washer=True):
    """ISO 4017 hex screw with an ISO 7089 washer into a tapped hole. xyz is the face the washer sits on."""
    h = cp.ISO[d][4] if washer else 0.0
    up = OPP[shank]
    out = [_pd(f"M{d}x{length} hex screw (ISO 4017)", Pos(*xyz) * orient(Pos(0, 0, h) * cp.hex_bolt(d, length), up), ZINC,
               "fastener", bom, group, explode, key, tag)]
    if washer:
        out.append(_pd(f"M{d} washer (ISO 7089)", Pos(*xyz) * orient(cp.washer(d), up), ZINC, "fastener", bom, group, explode, key, tag))
    return out


def coach(d, length, xyz, shank, bom=23, group="fixings", key="bolts", tag="", explode=(0, 0, 0)):
    h = cp.ISO[d][4]
    up = OPP[shank]
    return [_pd(f"M{d}x{length} coach screw (DIN 571)", Pos(*xyz) * orient(Pos(0, 0, h) * cp.coach_screw(d, length), up), ZINC,
                "fastener", bom, group, explode, key, tag),
            _pd(f"M{d} washer (ISO 7089)", Pos(*xyz) * orient(cp.washer(d), up), ZINC, "fastener", bom, group, explode, key, tag)]


def nut_at(d, xyz, up, bom=23, group="fixings", key="bolts", tag="", explode=(0, 0, 0), name=None):
    """An ISO 4032 nut sitting on a face at xyz, its axis pointing 'up' away from the face."""
    return _pd(name or f"M{d} hex nut (ISO 4032)", Pos(*xyz) * orient(cp.hex_nut(d), up), ZINC, "fastener", bom, group, explode, key, tag)


def washer_at(d, xyz, up, bom=23, group="fixings", key="bolts", tag="", explode=(0, 0, 0)):
    return _pd(f"M{d} washer (ISO 7089)", Pos(*xyz) * orient(cp.washer(d), up), ZINC, "fastener", bom, group, explode, key, tag)


def split_pin_at(d_pin, xyz, along, bom=23, group="fixings", key="bolts", tag="", explode=(0, 0, 0)):
    """ISO 1234 split pin for a pin of diameter d_pin, its legs along 'x', 'y' or 'z', centred at xyz."""
    s = cp.split_pin(d_pin)                    # along X
    s = {"x": s, "y": Rot(0, 0, 90) * s, "z": Rot(0, -90, 0) * s}[along]
    return _pd(f"Split pin for {d_pin:.0f} mm pin (ISO 1234)", Pos(*xyz) * s, ZINC, "fastener", bom, group, explode, key, tag)


def split_pin_hole(d_pin, xyz, along):
    dp = d_pin * 0.32
    return hole(xyz, "+" + along, dp / 2 + 0.2, d_pin * 3)


# ---------------------------------------------------------------------------------------------------------------
# Welds
# ---------------------------------------------------------------------------------------------------------------
def _frame(u, v):
    """Return (x_dir, z_dir) so that local X = u, local Y = v."""
    w = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    return u, w


def weld_line(p0, p1, u, v, leg=4.0, name="Fillet weld", group="welds", key="welds", tag="", explode=(0, 0, 0)):
    """Fillet weld bead from p0 to p1 (an axis-aligned line in a corner), its legs along the unit directions u and v
    ('+x', '-y' ...): the bead fills the corner between a face whose normal is u... (lies on it) and the other.
    In practice: u and v point from the corner line along the two faces it joins."""
    U, V = VEC[u], VEC[v]
    L = math.dist(p0, p1)
    tri = Polygon((0, 0), (leg, 0), (0, leg), align=None)
    prism = extrude(tri, L)                    # legs along local +X and +Y, length along +Z
    xd, zd = _frame(U, V)
    d = tuple((b - a) / L for a, b in zip(p0, p1))
    if all(abs(a - b) < 1e-9 for a, b in zip(zd, d)):
        origin = p0
    else:
        origin = p1
    pl = Plane(origin=origin, x_dir=xd, z_dir=zd)
    p = cp.part(f"{name}{tag}", pl.location * prism, WELD, "weld", group=group, explode=explode)
    p["key"] = key
    return p


def ring_weld(center, axis, r, leg=4.0, outward="+", name="Fillet weld, all round", group="welds", key="welds", tag="",
              explode=(0, 0, 0), inside=False):
    """Fillet weld round a shaft or tube of radius r where it meets a plate face at 'center'. axis 'x', 'y' or 'z';
    outward '+' or '-' is the side of the plate face the bead stands on. inside=True puts the bead inside a bore
    of radius r (a disc welded into a tube)."""
    if inside:
        pts = [(r, 0), (r - leg, 0), (r, leg)]
    else:
        pts = [(r, 0), (r + leg, 0), (r, leg)]
    prof = Plane.XZ * Polygon(*pts, align=None)
    s = revolve(prof, Axis.Z, 360)
    if outward == "-":
        s = Rot(180, 0, 0) * s
    s = {"x": Rot(0, 90, 0), "y": Rot(-90, 0, 0), "z": Rot(0, 0, 0)}[axis] * s
    p = cp.part(f"{name}{tag}", Pos(*center) * s, WELD, "weld", group=group, explode=explode)
    p["key"] = key
    return p


def box_welds(x0, x1, y0, y1, z, up, leg=4.0, sides="nsew", margin=0.0, **kw):
    """Fillet welds round the foot of a rectangular member (outer faces x0..x1, y0..y1) standing on a plate face at
    height z; up '+z' if the member rises from the face, '-z' if it hangs below it."""
    out = []
    vz = up
    m = margin
    if "s" in sides:
        out.append(weld_line((x0 + m, y0, z), (x1 - m, y0, z), "-y", vz, leg, **kw))
    if "n" in sides:
        out.append(weld_line((x0 + m, y1, z), (x1 - m, y1, z), "+y", vz, leg, **kw))
    if "w" in sides:
        out.append(weld_line((x0, y0 + m, z), (x0, y1 - m, z), "-x", vz, leg, **kw))
    if "e" in sides:
        out.append(weld_line((x1, y0 + m, z), (x1, y1 - m, z), "+x", vz, leg, **kw))
    return out


# ---------------------------------------------------------------------------------------------------------------
# Hardware
# ---------------------------------------------------------------------------------------------------------------
def bearing(axis, d, D, B, a0, p, q):
    """Deep groove ball bearing envelope (bore d, outside D, width B) along an axis from a0: outer and inner rings
    with the seal recess between them, drawn as one solid."""
    from build123d import Circle, Sketch
    s = extrude(Sketch() + Circle(D / 2) - Circle(d / 2), B)
    groove = extrude(Sketch() + Circle(D / 2 - (D - d) * 0.12) - Circle(d / 2 + (D - d) * 0.12), 0.6)
    s = s - groove - Pos(0, 0, B - 0.6) * groove
    s = cp.break_edges(s, 0.3)
    if axis == "x":
        return Pos(a0, p, q) * orient(s, "+x")
    if axis == "y":
        return Pos(p, a0, q) * orient(s, "+y")
    return Pos(p, q, a0) * s


def sprocket(axis, r_pitch, bore_r, width, a0, p, q, hub_r=None, hub_l=0.0, hub_side=-1):
    """Plate sprocket drawn to its pitch circle (teeth not drawn) with a hub on one side."""
    s = ring(axis, bore_r, r_pitch, a0, a0 + width, p, q, edge=0.4)
    if hub_r and hub_l:
        h0, h1 = (a0 - hub_l, a0) if hub_side < 0 else (a0 + width, a0 + width + hub_l)
        s = s + ring(axis, bore_r, hub_r, h0, h1, p, q, edge=0.3)
    return s


def _hull(points):
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _hull_poly(c1, r1, c2, r2, n=72):
    pts = []
    for (cx, cy), r in ((c1, r1), (c2, r2)):
        for i in range(n):
            a = 2 * math.pi * i / n
            pts.append((round(cx + r * math.cos(a), 4), round(cy + r * math.sin(a), 4)))
    return _hull(pts)


def chain_loop(plane, c1, r1, c2, r2, a0, a1, clear=0.5, depth=5.0):
    """A roller chain round two sprockets (pitch radii r1, r2 at centres c1, c2 in the plane's two coordinates),
    drawn as a closed band from clear to clear + depth outside the pitch circles, between a0 and a1 along the
    plane's normal. plane 'yz' (normal x) or 'xz' (normal y)."""
    outer = Polygon(*_hull_poly(c1, r1 + clear + depth, c2, r2 + clear + depth), align=None)
    inner = Polygon(*_hull_poly(c1, r1 + clear, c2, r2 + clear), align=None)
    band = extrude(outer, a1 - a0) - extrude(inner, a1 - a0)    # in local XY, along +Z
    if plane == "yz":       # local X -> world Y, local Y -> world Z, local Z -> world X
        pl = Plane(origin=(a0, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    else:                   # 'xz': local X -> world X, local Y -> world Z, local Z -> world -Y; start at y = a1
        pl = Plane(origin=(0, a1, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    return pl.location * band


def cylinder_bare_safe(shape, r=0.5):
    """Break the edges of a turned part so it reads as a real part (and is not taken for massing)."""
    return cp.break_edges(shape, r)
