"""DrumPanel concept media from the TRL 3 parametric model (constructable design, DMP-DDR-002).

Run from the repo root:  python cad/src/concept_media.py [hero|cutaway|exploded|flow|web|blueprint ...]
With no argument it draws everything; on a small machine run one picture per process. Geometry comes from
cad/src/model.py; the material flow values come from DMP-CAL-001 (docs/04-calcs/sizing.py). The pictures are
made with the pieces of .kit/concept.py render_all, one at a time, and the web model is exported here with a
coarse tessellation (linear deflection 1.0 mm, angular 0.35 rad) so model.glb stays a few MB.

Layout: the drain and purge stand at the front (-Y) with a drum on it, the cutting cradle in the middle with a
drum, the end cutter on its right-hand chime and the shear head parked at its left end, and the slip roll
stand at the back (+Y) with three panels being fed. The cutaway is cut across the stations at the middle of
the drums (x = 0) and seen from the left.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad/src"))
sys.path.insert(0, str(ROOT / "docs/04-calcs"))
import concept as K  # noqa: E402
from concept import Part  # noqa: E402
from model import build_parts, comp, box  # noqa: E402

PROJECT, TITLE, DWG, DATE = "DrumPanel", "Bench set concept: purge, cold cut and roll flat", "DMP-DWG-010", "2026-10-03"
MD = ROOT / "media"


def parts(context=True):
    return [Part(name, shape, color, bom, explode) for name, shape, color, bom, explode in build_parts(context=context)]


def with_figure(ps, gap=400.0):
    bb = comp([p.shape for p in ps]).bounding_box()
    fig = K.human_figure(1750.0, x=bb.max.X + gap + 230, y=(bb.min.Y + bb.max.Y) / 2, z=0.0)
    return ps + [fig]


def hero():
    return K._render(with_figure(parts()), MD / "hero.png", title=PROJECT,
                     note="Seen from the front right and above, 24 deg elevation. Front: drain and purge stand; middle: "
                          "cutting cradle; back: slip roll. Grey figure: 1.75 m person for scale")


def cutaway():
    ps = []
    cutter = box(0, 5000, -5000, 5000, -100, 3000)
    for p in parts():
        try:
            s = p.shape & cutter
            if s is not None and s.volume > 1e-3:
                ps.append(Part(p.name, s, p.color, p.bom, p.explode))
        except Exception:
            ps.append(p)
    return K._render(ps, MD / "cutaway.png", azim=180, elev=16, title=f"{PROJECT}: cutaway across the three stations",
                     note="Cut at the middle of the drums (x = 0), seen from the left, 16 deg elevation: drum on its chocks "
                          "(left), drum on the cradle rollers with the brake (middle), pinch rolls, bending roll and panels (right)")


def exploded():
    return K._render(parts(context=False), MD / "exploded.png", offsets=True, labels=True, title=f"{PROJECT}: exploded view",
                     note="Seen from the front right and above, 24 deg elevation; numbers match bom/bom.csv; drums and panels not shown")


def web():
    from build123d import Color, export_gltf
    import matplotlib.colors as mc
    kids = []
    for p in parts():
        sh = p.shape
        sh.color = Color(*mc.to_rgb(p.color))
        sh.label = p.name
        kids.append(sh)
    MD.mkdir(exist_ok=True)
    export_gltf(comp(kids), str(MD / "model.glb"), binary=True, linear_deflection=1.0, angular_deflection=0.35)
    (MD / "viewer.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{PROJECT}: {TITLE}</title>
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3/dist/model-viewer.min.js"></script>
<style>body{{margin:0;font-family:system-ui,sans-serif;background:#F9FAFB}}model-viewer{{width:100vw;height:100vh}}
.tag{{position:fixed;left:12px;top:10px;font-size:12px;color:#B45309;letter-spacing:.06em}}</style></head>
<body><div class="tag">CONCEPT, NOT FOR FABRICATION</div>
<model-viewer src="model.glb" poster="hero.png" alt="{PROJECT}: {TITLE}" camera-controls auto-rotate shadow-intensity="0.6"
  exposure="1.0" camera-orbit="-35deg 70deg auto" interaction-prompt="auto"></model-viewer></body></html>
""")
    return MD / "model.glb"


def flow():
    import sizing
    d = sizing.drum_yield()
    import math
    from model import PARAMS as P
    heads = 2 * math.pi * (d["head_d"] / 2) ** 2 * P["HEAD_T"] * 1e-9 * 7850
    panels = sum(d["widths"]) * d["circ"] * P["DRUM_T"] * 1e-9 * 7850
    strips = d["drum_m"] - heads - panels
    return K.flow_diagram(
        [("Empty drum, as received", round(d["drum_m"], 1)), ("Purged, vapour checked", round(d["drum_m"], 1)),
         ("Heads off", round(d["drum_m"] - heads, 1)), ("Three panels, opened", round(panels, 1)),
         ("Flat panels", round(panels, 1))],
        MD / "flow.png", f"{PROJECT}: material flow per drum, steel mass (all values are estimates)", "kg",
        [(0, "Residue and purge water to the settling drum (est.)", 0.5), (1, "Two head discs, kept as sheet (est.)", round(heads, 1)),
         (2, "Chime and hoop strips, kept as strip (est.)", round(strips, 1))])


def blueprint():
    import sizing
    from drawing import Sheet, project_views
    d = sizing.drum_yield()
    ps = parts(context=False)
    shown = with_figure(ps)
    views = project_views(comp([p.shape for p in ps]), MD / "_views")
    views["iso"] = project_views(comp([p.shape for p in shown]), MD / "_views_fig")["iso"]
    s = Sheet(project=PROJECT, title=TITLE, dwg_no=DWG, rev="P1", author="Amish Chadha", date=DATE, theme="blueprint",
              material="Massing model for concept communication",
              revisions=[("P1", "Concept sheet from the constructable TRL 3 model", DATE, "AC")])
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 37, 140, 113, label="Isometric view", sublabel="Not to scale; figure is a 1.75 m person")
    s.add_notes("Key figures", [
        "Three hand-powered stations: drain stand, cradle, slip roll",
        "No flame; cut only after a vapour check below 5 % LEL",
        f"Per drum: 3 flat panels {d['widths'][1]:.0f} x {d['circ']:.0f} mm, 2 heads {d['head_d']:.0f} mm",
        "Crank force 20 to 111 N (shear head at 1.5 mm wall)",
        "Bending roll set by a trial pass; nominal 13.4 mm",
        "About 2 drums an hour for two people (est.)",
        "Cradle about 130 kg; slip roll stand about 189 kg (est.)",
        "Estimated cost USD 2,794; target USD 3,000",
    ], x=276, y=168, width=140)
    s.save(MD / "concept-blueprint")
    import shutil
    shutil.rmtree(MD / "_views", ignore_errors=True)
    shutil.rmtree(MD / "_views_fig", ignore_errors=True)
    return MD / "concept-blueprint.png"


if __name__ == "__main__":
    fns = {"hero": hero, "cutaway": cutaway, "exploded": exploded, "flow": flow, "web": web, "blueprint": blueprint}
    for w in sys.argv[1:] or list(fns):
        print(w, "->", fns[w](), flush=True)
