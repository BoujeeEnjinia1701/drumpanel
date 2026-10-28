"""DrumPanel product appearance model for photoreal renders (kit 1.9), TRL 3, constructable design (DMP-DDR-002).

Every part of the chosen design comes from cad/src/model.py components("A") as it is: the drain and purge stand with
its tray, the cutting cradle with its rollers, brake, rail posts, rail beam, trolley and parked shear head, the end
cutter on the right chime, the tool shelf with the notching punch, its lever and the ring head, and the slip roll stand
with its rolls, slide blocks, screws, dial adjusters, chain drive, guards and tables, every bolt, washer, pin and weld.
Only the scene is added as context parts: a stack of finished flat panels on a pallet, the settling drum for the purge
water and a 1.75 m mannequin at the slip roll crank, standing on the yard floor at z = 0. A second state, used only by
the detail view, shows a drum with its heads off being slit, the shear head halfway along it (the same detailed head
parts, moved). APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Groups: "purge" (drain stand and tray), "cradle" (cradle frame, rollers, brake, posts, beam), "head" (trolley and
shear head with its drive case parked at the left end), "cutter" (end cutter on the right chime), "tools" (tool shelf
on the left post with the notching punch, its lever and the ring head), "roll" (slip roll stand), "drums" (the drum on
the cradle with its heads on, the drum on the drain stand), "panels" (three panels being fed), "slitting" (the opened
drum and the shear head halfway along it), "context" (panel stack, settling drum, mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Pos, Rot  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402
import model  # noqa: E402
from model import PARAMS as P, levels, notch_boxes, drum  # noqa: E402
from dmp_parts import box, eased  # noqa: E402

TITLE = "DrumPanel: hand-powered bench set that opens oil drums into flat sheet without fire"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["purge", "cradle", "head", "cutter", "tools", "roll", "drums", "panels", "context"], "explode": False,
     "el": 18, "az": -38,
     "args": ["--scene=outdoor", "--ground=concrete", "--ground-z=0", "--sun=42,-70", "--lens=35"],
     "note": "Site render in an open workshop yard from the front right, about 18 deg elevation: drain and purge stand with a drum "
             "bung end down over its tray and the settling drum beside it (front), cutting cradle with a drum, the end cutter on "
             "its right chime, the shear head parked on the rail and the tool shelf with the notching punch and ring head on the "
             "left post (middle), slip roll stand feeding three panels with the operator at its crank and a stack of flat panels "
             "(back); 1.75 m mannequin for scale"},
    {"name": "studio", "groups": ["purge", "cradle", "head", "cutter", "tools", "roll", "drums", "panels"], "explode": False, "el": 26, "az": -45,
     "note": "Studio render from the front right and above, about 26 deg elevation: the three stations with every bolt, weld, "
             "bearing and guard of the detailed model"},
    {"name": "exploded", "groups": ["cradle", "head", "cutter", "tools", "roll"], "explode": True, "el": 26, "az": -50,
     "note": "Exploded view from the front right and above (about 26 deg elevation): cradle frame, rollers, brake, posts and "
             "rail beam, trolley and shear head with its drive case, end cutter, tool shelf with the notching punch and ring "
             "head; slip roll base, side frames, rolls, slide blocks, screws and dials, crank drive, guards and tables; drain "
             "stand, drums and panels not shown"},
    {"name": "detail", "groups": ["cradle", "slitting"], "explode": False, "el": 30, "az": -30,
     "note": "Detail from the front right and above (about 30 deg elevation): a purged drum with its heads off on the cradle "
             "rollers, brake on, the hand-cranked shear head halfway along the seam slit, the cut edges spread round its web, "
             "its crank turning high on the drive case; chime rings and hoops notched on the slit line by the notching punch"},
]

GROUP_OF_KEY = {"drum": "drums", "drum_ds": "drums", "sheet": "panels"}


def slitting():
    """The detail state: a drum with its heads off, notched and part slit, and the detailed shear head, trolley,
    drop bar and pivot moved from their parked place to halfway along the drum."""
    import option_a as A
    L = levels()
    zax, znip = L["z_ax"], L["z_nip"]
    half = P["DRUM_L"] / 2
    xn = 0.0
    body = Pos(0, 0, zax) * drum(P, heads=False)
    zt = zax + 200
    for nb in notch_boxes(P, z_top=zt):
        body = body - nb
    body = body - box(-half - 10, xn + P["DISC_R"] * 0.2, -11, 11, zt, zt + 200)
    out = [part("Drum with its heads off, being slit", body, "painted_steel", "context", color="#1F4E9C")]
    for p in A.placed(Pos(xn, 0, znip), A.shear_head_parts()):
        q = dict(p)
        q["name"] = p["name"] + " (slitting)"
        out.append(q)
    dx = xn - P["HEAD_PARK_X"]
    for p in model.components("A"):
        if p.get("key") in ("trolley", "trolley_wheels", "drop", "pivot"):
            q = dict(p)
            q["shape"] = Pos(dx, 0, 0) * p["shape"]
            q["name"] = p["name"] + " (slitting)"
            out.append(q)
    for q in out:
        q["group"] = "slitting"
        q["explode"] = (0, 0, 0)
    return out


def scene():
    """Context: a stack of flat panels on a pallet, the settling drum, and the operator at the slip roll crank."""
    out = []
    ry = P["RS_Y"]
    px, py = 1450.0, ry + 700.0
    for i in range(3):
        y = py - 90 + i * 90
        out.append(part(f"Pallet board {i + 1} (timber, 1,000 x 80 x 22)", eased(px - 500, px + 500, y - 40, y + 40, 100, 122, 2.0), "timber", "context"))
    for i, y in enumerate((py - 90, py + 90)):
        out.append(part(f"Pallet runner {i + 1} (timber, 100 x 100)", eased(px - 500, px + 500, y - 40, y + 40, 0, 100, 3.0), "timber", "context"))
    for k in range(12):
        z = 122 + k * 1.2
        out.append(part(f"Flat panel {k + 1}, 233 x 1,800 (product)", box(px - 900, px + 900, py - 116, py + 117, z, z + 1.0),
                        "painted_steel", "context", color=("#1F4E9C", "#9B2C2C", "#2F6B3A")[k % 3]))
    out.append(part("Settling drum with tap for purge water (context)", Pos(1450, P["DS_Y"] - 550, 0) * cp.drum_200l(), "painted_steel", "context",
                    color="#3A4048"))
    from context_parts import mannequin
    cy0 = ry + P["CRANK_Y"]
    person = Pos(1050, cy0, 0) * Rot(0, 0, -90) * mannequin(1750, "stand")
    out.append(part("Operator at the slip roll crank, 1.75 m mannequin (scale)", person, "skin", "context"))
    for q in out:
        q["group"] = "context"
    return out


def product_parts():
    out = []
    for p in model.components(model.CHOSEN):
        q = dict(p)
        if p["kind"] == "context":
            q["group"] = GROUP_OF_KEY.get(p.get("key"), "context")
        out.append(q)
    out += slitting()
    out += scene()
    return out


if __name__ == "__main__":
    ps = product_parts()
    from collections import Counter
    print(Counter(p["group"] for p in ps))
    for p in ps:
        if p["group"] in ("context", "slitting") and p["kind"] == "context":
            s = p["shape"]
            print(f"{p['name']:60s} {p['group']:10s} {p['material']:10s} valid={s.is_valid}")
    print(len(ps), "parts")
