"""DrumPanel general arrangement drawing DMP-DWG-001 (Rev P1).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/DMP-DWG-001.svg, .pdf and .png from the parametric model (bench set only; the drums and
panels are left out of the views). The concept sheet in media/ uses DMP-DWG-010. Figures in the notes come
from DMP-CAL-001 (python docs/04-calcs/sizing.py).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, build_parts, comp, levels  # noqa: E402

L = levels()
parts = build_parts(context=False)
bench = comp([p[1] for p in parts])
bb = bench.bounding_box()
work = ROOT / "cad/drawings/_views"
views = project_views(bench, work)

s = Sheet(project="DrumPanel", title="Drum opening bench set: general arrangement of the three stations",
          dwg_no="DMP-DWG-001", rev="P1", author="Amish Chadha", date="2026-10-03", concept=True, scale=None,
          material="S275 RHS and plate; C45 rolls; D2 discs; bronze bushes. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the constructable TRL 3 model (DMP-DDR-002)", "2026-10-03", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 40, 140, 70, label="Isometric view", sublabel="Not to scale; drums and panels not shown")
w = [x1 - x0 for x0, x1 in L["panels"]]
s.add_notes("Key dimensions (mm) and data", [
    f"Layout {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.max.Z:.0f} high (three stations in a row)",
    f"Drain stand at y {P['DS_Y']:.0f}; saddles {2 * P['DS_SADDLE_X']:.0f} apart; 2.9 deg fall to the bung end",
    f"Cradle: rollers {2 * P['ROLLER_Y']:.0f} apart at {P['ROLLER_Z']:.0f} high, under the hoops at +/-{P['HOOP_X']:.0f}",
    f"Drum axis {L['z_ax']:.0f}; drum top {L['drum_top']:.0f}; contact {L['contact_deg']:.0f} deg from vertical",
    f"Rail posts at +/-{P['POST_X']:.1f}; rail beam top {P['BEAM_Z0'] + P['BEAM_H']:.0f}",
    f"Shear discs {2 * P['DISC_R']:.0f} x {P['DISC_T']:.0f}, overlap {P['DISC_OVERLAP']:.1f}; crank {P['CRANK_R']:.0f}",
    f"End cutter wheel {2 * P['CUTTER_R']:.0f}; cut line {2 * P['CUT_LINE_R']:.0f} dia; crank {P['EC_CRANK_R']:.0f}",
    f"Slip roll at y +{P['RS_Y']:.0f}: rolls {2 * P['ROLL_R']:.0f} dia x {P['ROLL_FACE']:.0f} face",
    f"Sheet line {P['TABLE_TOP']:.0f}; bending roll {P['BEND_Y']:.0f} behind, set {P['BEND_SET']:.1f} up (trial)",
    f"Pinch gears m3 x 20 T; chain #40, 13 to 39 T; crank {P['RS_CRANK_R']:.0f}",
    f"Guards: 8 mm slots at the roll nips and the shear head",
    f"Panels {w[0]:.0f} / {w[1]:.0f} / {w[2]:.0f} x {L['sheet_l']:.0f}; heads {L['head_d']:.0f} dia",
    "Masses (est.): cradle 130 kg, slip roll 189 kg, stand 15 kg",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=128, width=140)
s.save(ROOT / "cad/drawings/DMP-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/DMP-DWG-001.svg, .pdf, .png")
