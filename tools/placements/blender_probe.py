"""Depth probe: cast a grid of rays along an axis at a part, report holes/pockets.

  blender -b --factory-startup --python blender_probe.py -- <part.json> <out_prefix> [axis=-y] [step=0.25]

part.json: one part entry like in the assembly config (+ "root").
Writes <out_prefix>_depth.png (darker = deeper, red = no hit) and prints the
centroids/sizes of regions where rays go through ('through') or hit at least
2 mm deeper than the median surface ('pocket').
"""
import bpy, sys, json, math, os, mathutils
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
part = json.load(open(argv[0], encoding="utf-8"))
out = argv[1]
axis = argv[2] if len(argv) > 2 else "-y"
step = float(argv[3]) if len(argv) > 3 else 0.25
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath=os.path.join(os.environ.get("VAULT_RENDER") or part["root"], part["file"]))
o = bpy.context.selected_objects[0]
me = o.data
vs = me.vertices
c = mathutils.Vector([(min(v.co[i] for v in vs) + max(v.co[i] for v in vs)) / 2 for i in range(3)])
R = mathutils.Euler([math.radians(a) for a in part.get("rot", [0, 0, 0])]).to_matrix()
world = [R @ (v.co - c) for v in vs]
mn = mathutils.Vector([min(p[i] for p in world) for i in range(3)])
mx = mathutils.Vector([max(p[i] for p in world) for i in range(3)])
# place like the assembler does (align min/max/center) or keep centre at original c
loc = c.copy()
for ax, (mode, val) in part.get("align", {}).items():
    i = "xyz".index(ax)
    cur = {"min": mn[i], "max": mx[i], "center": (mn[i] + mx[i]) / 2}[mode]
    loc[i] = val - cur
world = [p + loc for p in world]
mn += loc
mx += loc
bvh = BVHTree.FromPolygons(world, [p.vertices[:] for p in me.polygons])

sgn = -1 if axis[0] == "-" else 1
ai = "xyz".index(axis[-1])
u, w = [k for k in range(3) if k != ai]
d = mathutils.Vector((0, 0, 0))
d[ai] = sgn
start = (mx[ai] + 5) if sgn < 0 else (mn[ai] - 5)
nu = int((mx[u] - mn[u]) / step) + 1
nw = int((mx[w] - mn[w]) / step) + 1
depth = [[None] * nu for _ in range(nw)]
for j in range(nw):
    for i in range(nu):
        p = mathutils.Vector((0, 0, 0))
        p[ai], p[u], p[w] = start, mn[u] + i * step, mn[w] + j * step
        hit, nrm, idx, dist = bvh.ray_cast(p, d, 1000)
        depth[j][i] = None if hit is None else hit[ai]

vals = sorted(v for row in depth for v in row if v is not None)
med = vals[len(vals) // 2]
# label regions
lab = [[0] * nu for _ in range(nw)]


def kind(v):
    if v is None:
        return "through"
    return "pocket" if (med - v) * (-sgn) > 2 else None


regions = []
for j in range(nw):
    for i in range(nu):
        k = kind(depth[j][i])
        if k is None or lab[j][i]:
            continue
        stack = [(j, i)]
        lab[j][i] = len(regions) + 1
        cells = []
        while stack:
            a, b = stack.pop()
            cells.append((a, b))
            for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                aa, bb = a + da, b + db
                if 0 <= aa < nw and 0 <= bb < nu and not lab[aa][bb] and kind(depth[aa][bb]) == k:
                    lab[aa][bb] = len(regions) + 1
                    stack.append((aa, bb))
        border = any(a in (0, nw - 1) or b in (0, nu - 1) for a, b in cells)
        if len(cells) * step * step < 1.0 or border:
            regions.append(None)
            continue
        cu = mn[u] + step * sum(b for a, b in cells) / len(cells)
        cw = mn[w] + step * sum(a for a, b in cells) / len(cells)
        su = step * (max(b for a, b in cells) - min(b for a, b in cells) + 1)
        sw = step * (max(a for a, b in cells) - min(a for a, b in cells) + 1)
        dd = [depth[a][b] for a, b in cells if depth[a][b] is not None]
        regions.append({"kind": k, "xyz"[u]: round(cu, 2), "xyz"[w]: round(cw, 2),
                        "size_" + "xyz"[u]: round(su, 2), "size_" + "xyz"[w]: round(sw, 2),
                        "area": round(len(cells) * step * step, 1),
                        "depth_at": round(sum(dd) / len(dd), 2) if dd else None})
regions = [r for r in regions if r]
print("PROBE surface_median", round(med, 2), "bbox", [round(x, 2) for x in mn], [round(x, 2) for x in mx])
for r in sorted(regions, key=lambda r: -r["area"]):
    print("PROBE", json.dumps(r))
json.dump({"median": med, "regions": regions}, open(out + "_probe.json", "w"), indent=1)

import numpy as np
np.save(out + "_depth.npy", np.array([[np.nan if v is None else v for v in row] for row in depth], dtype=np.float64))
json.dump({"axis": axis, "step": step, "u": "xyz"[u], "w": "xyz"[w], "u0": mn[u], "w0": mn[w]}, open(out + "_depth.json", "w"))
try:
    from PIL import Image
    im = Image.new("RGB", (nu, nw))
    lo, hi = vals[0], vals[-1]
    for j in range(nw):
        for i in range(nu):
            v = depth[j][i]
            if v is None:
                im.putpixel((i, nw - 1 - j), (200, 30, 30))
            else:
                t = (v - lo) / (hi - lo + 1e-9)
                g = int(40 + 200 * (t if sgn < 0 else 1 - t))
                im.putpixel((i, nw - 1 - j), (g, g, g))
    im.save(out + "_depth.png")
except Exception as e:
    print("no image", e)
