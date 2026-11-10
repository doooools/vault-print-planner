"""Generate assembly recipes (JSON for blender_assemble.py) for the VAULT L family.

  python make_recipe_L.py <size> <out_dir>        e.g.  python make_recipe_L.py 7 pilot/L7

Rules measured on L7 (probes + fits, see README). Every height (1F/2F/4F) is a
stack of 48 mm "levels": level k sits at z = 23.5 + 48 k in the CAD frame.
  - box: already in place in the CAD file (front at y = -145.66, z from 5)
  - module: Rx -90 (1F is printed at 45 deg: Rx -90, Ry -45), x centred on
    the box, front at box front + 0.06, bottom at z = -3.6
  - facade: Rx -90, x centred, back on the box front, bottom at z = 0
  - key (Rx -90) and key cap (Rx +90) on the bottom level, x centred
  - geared rails on the bottom level (z 15.02 / 31.98, the top one Ry 180)
  - per level and per side: runner slide in the box groove, runner guide on
    the module wall, runner stopper in the module side hole
  - 2 latches under the module (x = centre -/+ 82.3)
  - facade caps in every counterbore, label in the slot (bottom right)
Only S (L) sizes 7 were measured; other sizes need their box x/width,
depth and runner length: they are read from the decimation log.
"""
import json, os, sys

ROOT = os.environ.get("VAULT_RENDER", "VAULT_RENDER")  # decimated copy of the Vault download (run_decimate.py)
U = "01. DRAWERS/07. Universal/"


def bbox_of(rel):
    for l in open(os.path.join(ROOT, "_decimate_log.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        if r["file"] == rel:
            return r["bbox_min"], r["bbox_max"]
    raise SystemExit("not decimated yet: " + rel)


def recipe(size, h):
    n = {"1F": 1, "2F": 2, "4F": 4}[h]
    fam = f"01. DRAWERS/03. L Families/L{size}/"
    box = fam + f"Boxes/L{size} Box {h}.stl"
    bmn, bmx = bbox_of(box)
    cx = round((bmn[0] + bmx[0]) / 2, 2)
    yf = bmx[1]                    # box front
    bxmin, bxmax = bmn[0], bmx[0]
    mod_half = 164.8               # module width 329.6 (L)
    mxmin, mxmax = cx - mod_half, cx + mod_half
    name = f"L{size}_{h}"
    P = []

    def part(nm, file, role, group, rot=None, align=None, move=None):
        d = {"name": f"{name}_{nm}", "file": file, "role": role, "group": group}
        if rot:
            d["rot"] = rot
        if align:
            d["align"] = align
        if move:
            d["move"] = move
        P.append(d)

    mrot = [-90, -45, 0] if h == "1F" else [-90, 0, 0]
    part("Module", fam + f"Modules/L{size} Module {h}.stl", "body", "module", mrot,
         {"x": ["center", cx], "y": ["max", yf + 0.06], "z": ["min", -3.6]})
    part("Box", box, "drawer", "drawer")
    # one baseplate file, sitting in the 1F box in the CAD file: reuse its offset to the box
    bp = fam + f"Gridfinity Baseplate/L{size} Baseplate.stl"
    pmn, _ = bbox_of(bp)
    b1mn, _ = bbox_of(fam + f"Boxes/L{size} Box 1F.stl")
    part("Baseplate", bp, "insert", "drawer", None,
         {"x": ["center", cx], "y": ["min", bmn[1] + (pmn[1] - b1mn[1])], "z": ["min", pmn[2]]})
    part("Facade", f"01. DRAWERS/03. L Families/Facades/L{h} (Turn On Supports).stl", "facade", "drawer",
         [-90, 0, 0], {"x": ["center", cx], "y": ["min", yf], "z": ["min", 0.0]})
    part("Key", U + "Key (Turn On Supports).stl", "mech", "drawer", [-90, 0, 0],
         {"x": ["center", cx], "y": ["center", yf + 8.16], "z": ["center", 23.5]})
    part("KeyCap", U + "Key Cap.stl", "facade", "drawer", [90, 0, 0],
         {"x": ["center", cx], "y": ["center", yf + 25.16], "z": ["center", 23.5]})
    part("Rail_bottom", U + "Geared Rails/L Rails.stl", "accent", "drawer", None,
         {"x": ["center", cx], "y": ["center", yf - 7.38], "z": ["center", 15.02]})
    part("Rail_top", U + "Geared Rails/L Rails.stl", "accent", "drawer", [0, 180, 0],
         {"x": ["center", cx], "y": ["center", yf - 7.38], "z": ["center", 31.98]})
    runner = U + f"Runners/x{size} Runner "
    for k in range(n):
        z = 23.5 + 48 * k
        part(f"Slide_L{k+1}", runner + "Slide.stl", "mech", "drawer", [0, 90, 0],
             {"x": ["max", bxmin + 2.2], "y": ["max", yf], "z": ["center", z]})
        part(f"Slide_R{k+1}", runner + "Slide.stl", "mech", "drawer", [0, -90, 0],
             {"x": ["min", bxmax - 2.2], "y": ["max", yf], "z": ["center", z]})
        part(f"Guide_L{k+1}", runner + "Guide.stl", "body", "module", [0, 90, 0],
             {"x": ["min", mxmin + 3.58], "y": ["max", yf], "z": ["center", z]})
        part(f"Guide_R{k+1}", runner + "Guide.stl", "body", "module", [0, -90, 0],
             {"x": ["max", mxmax - 3.58], "y": ["max", yf], "z": ["center", z]})
        # stopper: module side hole at 128.56 mm behind the module front (L), offset calibrated on S3
        part(f"Stopper_R{k+1}", U + "Runners/Runner Stopper.stl", "accent", "module", None,
             {"x": ["max", mxmax - 0.16], "y": ["center", yf + 0.06 - 128.56 - 0.29], "z": ["center", z]})
        part(f"Stopper_L{k+1}", U + "Runners/Runner Stopper.stl", "accent", "module", [0, 0, 180],
             {"x": ["min", mxmin + 0.16], "y": ["center", yf + 0.06 - 128.56 - 0.29], "z": ["center", z]})
    for side, dx in (("L", -82.3), ("R", 82.3)):
        part(f"Latch_{side}", U + "Latch.stl", "accent", "module", None,
             {"x": ["center", cx + dx], "y": ["max", yf + 0.06 - 248.6 - 1.94], "z": ["min", -3.3]})
    part("Label", U + "Label.stl", "insert", "drawer", [-90, 0, 0],
         {"x": ["min", cx + 115.19], "y": ["min", yf + 7.91], "z": ["center", 23.5]})
    caps = [(-130.24, 23.5), (-51.43, 23.5), (51.52, 23.5)]
    if n > 1:
        ztop = 23.5 + 48 * (n - 1)
        caps += [(-130.24, ztop), (130.32, ztop)]
    for i, (dx, z) in enumerate(caps):
        part(f"FacadeCap_{i+1}", U + "Facade Cap.stl", "facade", "drawer", [-90, 0, 0],
             {"x": ["center", cx + dx], "y": ["min", yf + 5.92], "z": ["center", z]})
    return {"name": name, "parts": P, "finalize": {"anchor": f"{name}_Module"}}


ROOFS = {"Bowl": "Bowl Roof", "Grid": "Grid Roof", "Heavyweight": "Heawyweight Roof",
         "Table": "Table Roof", "UnderTable": "Under Table Mount Roof"}


def recipe_roof(size, kind):
    """Roofs: printed on edge at 45 deg like the 1F module, same underside as a
    module (bottom face, latch frames), so they sit on a module exactly like
    another module would, with their own 2 latches."""
    fam = f"01. DRAWERS/03. L Families/L{size}/"
    name = f"L{size}_Roof_{kind}"
    cx, yf = 3001.55, -145.60          # any frame works: the root is recentred
    P = [{"name": f"{name}_Roof", "file": fam + f"Roofs/L{size} {ROOFS[kind]}.stl", "role": "roof", "group": "module",
          "rot": [-90, -45, 0], "align": {"x": ["center", cx], "y": ["max", yf], "z": ["min", -3.6]}}]
    for side, dx in (("L", -82.3), ("R", 82.3)):
        P.append({"name": f"{name}_Latch_{side}", "file": U + "Latch.stl", "role": "accent", "group": "module",
                  "align": {"x": ["center", cx + dx], "y": ["max", yf - 248.6 - 1.94], "z": ["min", -3.3]}})
    return {"name": name, "parts": P, "finalize": {"anchor": f"{name}_Roof"}}


if __name__ == "__main__":
    size, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    jobs = [(f"L{size}_{h}", recipe(size, h)) for h in ("1F", "2F", "4F")]
    jobs += [(f"L{size}_Roof_{k}", recipe_roof(size, k)) for k in ROOFS]
    for nm, r in jobs:
        p = os.path.join(out, f"{nm}_assembly.json")
        json.dump(r, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(p, len(r["parts"]), "parts")
