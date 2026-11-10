"""Find where a 'moving' part goes, given 'fixed' parts already in place.

  blender -b --factory-startup --python blender_fit.py -- <fit.json> <out.json>

fit.json:
{
  "root": "...",
  "moving": "rel/path.stl",
  "fixed": ["rel/a.stl", ...],          # parts already at their assembled place
  "rotations": {"name": [rx, ry, rz], ...},   # candidate orientations (deg, about bbox centre)
  "fix_axis": {"x": ["center", 9001.55]},    # optional: axes known in advance
  "search": {"y": [lo, hi], "z": [lo, hi]},  # range for the moving part's bbox centre
  "step": 1.0,
  "samples": 4000
}
Cost = fraction of fixed-part surface samples lying inside the moving part's
solid (inside test: nearest-surface normal). Lower is better; the best
translation per rotation is refined down to 0.1 mm.
"""
import bpy, sys, json, math, os, random, mathutils
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
cfg = json.load(open(argv[0], encoding="utf-8"))
out_path = argv[1]
root = os.environ.get("VAULT_RENDER") or cfg.get("root")
bpy.ops.wm.read_factory_settings(use_empty=True)


def load(rel):
    bpy.ops.wm.stl_import(filepath=os.path.join(root, rel))
    o = bpy.context.selected_objects[0]
    return o


def samples(me, k, seed=0):
    rnd = random.Random(seed)
    me.calc_loop_triangles()
    tris = [(lt.area, [me.vertices[i].co.copy() for i in lt.vertices]) for lt in me.loop_triangles if lt.area > 1e-8]
    tot = sum(a for a, _ in tris)
    pts = []
    for a, (p, q, r) in tris:
        m = a / tot * k
        for _ in range(int(m) + (1 if rnd.random() < m - int(m) else 0)):
            u, v = rnd.random(), rnd.random()
            if u + v > 1:
                u, v = 1 - u, 1 - v
            pts.append(p + (q - p) * u + (r - p) * v)
    return pts


mov = load(cfg["moving"])
mme = mov.data
vs = mme.vertices
mn = mathutils.Vector([min(v.co[i] for v in vs) for i in range(3)])
mx = mathutils.Vector([max(v.co[i] for v in vs) for i in range(3)])
c0 = (mn + mx) / 2
bvh = BVHTree.FromPolygons([v.co - c0 for v in vs], [p.vertices[:] for p in mme.polygons])  # centred
half = (mx - mn) / 2

pts = []
per = cfg.get("samples", 4000) // max(1, len(cfg["fixed"]))
for i, fx in enumerate(cfg["fixed"]):
    # a fixed part is a path (already in place) or {"file", "rot", "center"}
    rel = fx if isinstance(fx, str) else fx["file"]
    o = load(rel)
    ps = samples(o.data, per, seed=i)
    if not isinstance(fx, str):
        fv = o.data.vertices
        fc = mathutils.Vector([(min(v.co[k] for v in fv) + max(v.co[k] for v in fv)) / 2 for k in range(3)])
        FR = mathutils.Euler([math.radians(a) for a in fx.get("rot", [0, 0, 0])]).to_matrix()
        tgt = mathutils.Vector(fx.get("center", fc))
        ps = [FR @ (p - fc) + tgt for p in ps]
    pts += ps


def cost(R_inv, ctr, pts_sub):
    inside = 0
    for p in pts_sub:
        q = R_inv @ (p - ctr)
        if abs(q.x) > half.x + 0.01 or abs(q.y) > half.y + 0.01 or abs(q.z) > half.z + 0.01:
            continue
        hit, nrm, _, dist = bvh.find_nearest(q)
        if hit is not None and (q - hit).dot(nrm) < 0 and dist > 0.05:
            inside += 1
    return inside / len(pts_sub)


def frange(lo, hi, st):
    n = int(round((hi - lo) / st))
    return [lo + i * st for i in range(n + 1)]


results = {}
step = cfg.get("step", 1.0)
fixed_ctr = {ax: v[1] for ax, v in cfg.get("fix_axis", {}).items()}
for rname, rot in cfg["rotations"].items():
    R = mathutils.Euler([math.radians(a) for a in rot]).to_matrix()
    R_inv = R.inverted()
    rng = {ax: cfg["search"].get(ax, [fixed_ctr.get(ax, c0["xyz".index(ax)])] * 2) for ax in "xyz"}
    sub = pts[::4]
    push = cfg.get("push")  # {"axis": "y", "dir": -1, "tol": 0.002}: slide as far as possible without collision
    if push:
        pi = "xyz".index(push["axis"])
        tol = push.get("tol", 0.002)
        best = None
        grid = []
        for x in frange(*rng["x"], step) if rng["x"][0] != rng["x"][1] else [rng["x"][0]]:
            for y in frange(*rng["y"], step):
                for z in frange(*rng["z"], step):
                    p = mathutils.Vector((x, y, z))
                    if cost(R_inv, p, sub) <= tol:
                        grid.append(p)
        if not grid:
            results[rname] = {"rot": rot, "center": None, "cost": None}
            print("FIT", rname, "no feasible position", flush=True)
            continue
        cur = min(grid, key=lambda p: p[pi] * push["dir"])
        # refine: step further along push dir while feasible, wiggling the other axes
        for st in (step / 2, step / 4, 0.1):
            moved = True
            while moved:
                moved = False
                for dz in (0, -st, st):
                    for dx in (0, -st, st):
                        t = cur.copy()
                        t[pi] += push["dir"] * st
                        others = [k for k in range(3) if k != pi and rng["xyz"[k]][0] != rng["xyz"[k]][1]]
                        if others:
                            t[others[0]] += dz
                        if len(others) > 1:
                            t[others[1]] += dx
                        if cost(R_inv, t, pts) <= tol:
                            cur, moved = t, True
                            break
                    if moved:
                        break
        results[rname] = {"rot": rot, "center": [round(v, 2) for v in cur], "cost": round(cost(R_inv, cur, pts), 5),
                          "push_value": round(cur[pi], 2)}
        print("FIT", rname, results[rname], flush=True)
        continue
    if cfg.get("mode") == "scan":
        # print the collision cost along the grid (to read a contact curve)
        rows = []
        for x in frange(*rng["x"], step) if rng["x"][0] != rng["x"][1] else [rng["x"][0]]:
            for y in frange(*rng["y"], step) if rng["y"][0] != rng["y"][1] else [rng["y"][0]]:
                for z in frange(*rng["z"], step) if rng["z"][0] != rng["z"][1] else [rng["z"][0]]:
                    rows.append([round(x, 2), round(y, 2), round(z, 2), round(cost(R_inv, mathutils.Vector((x, y, z)), pts), 5)])
        results[rname] = {"rot": rot, "scan": rows}
        for r in rows:
            print("SCAN", rname, *r, flush=True)
        continue
    if cfg.get("mode") == "centroid":
        # the part is trapped in a channel/pocket: return the middle of the collision-free zone
        tol = cfg.get("tol", 0.002)
        feas = []
        for x in frange(*rng["x"], step) if rng["x"][0] != rng["x"][1] else [rng["x"][0]]:
            for y in frange(*rng["y"], step):
                for z in frange(*rng["z"], step):
                    p = mathutils.Vector((x, y, z))
                    if cost(R_inv, p, pts) <= tol:
                        feas.append(p)
        if not feas:
            results[rname] = {"rot": rot, "center": None, "n_feasible": 0}
        else:
            cen = sum(feas, mathutils.Vector()) / len(feas)
            ext = {ax: [round(min(p[k] for p in feas), 2), round(max(p[k] for p in feas), 2)] for k, ax in enumerate("xyz")}
            # split the feasible set into connected clusters (grid neighbours)
            key = lambda p: tuple(int(round(p[k] / step)) for k in range(3))
            left = {key(p): p for p in feas}
            clusters = []
            while left:
                k0, p0 = left.popitem()
                st, cl = [k0], [p0]
                while st:
                    a = st.pop()
                    for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                        b = (a[0] + d[0], a[1] + d[1], a[2] + d[2])
                        if b in left:
                            cl.append(left.pop(b))
                            st.append(b)
                cc = sum(cl, mathutils.Vector()) / len(cl)
                clusters.append({"center": [round(v, 2) for v in cc], "n": len(cl),
                                 "range": {ax: [round(min(p[k] for p in cl), 2), round(max(p[k] for p in cl), 2)] for k, ax in enumerate("xyz")}})
            clusters.sort(key=lambda c: -c["n"])
            results[rname] = {"rot": rot, "center": [round(v, 2) for v in cen], "n_feasible": len(feas),
                              "feasible_range": ext, "cost_at_center": round(cost(R_inv, cen, pts), 5),
                              "clusters": clusters[:6]}
        print("FIT", rname, results[rname], flush=True)
        continue
    best = (9, None)
    for x in frange(*rng["x"], step) if rng["x"][0] != rng["x"][1] else [rng["x"][0]]:
        for y in frange(*rng["y"], step):
            for z in frange(*rng["z"], step):
                c = cost(R_inv, mathutils.Vector((x, y, z)), sub)
                if c < best[0]:
                    best = (c, (x, y, z))
    # refine with all samples
    cur = mathutils.Vector(best[1])
    bc = cost(R_inv, cur, pts)
    for st in (step / 2, step / 4, 0.1):
        improved = True
        while improved:
            improved = False
            for ax in "xyz":
                if rng[ax][0] == rng[ax][1]:
                    continue
                for sgn in (-1, 1):
                    t = cur.copy()
                    t["xyz".index(ax)] += sgn * st
                    c = cost(R_inv, t, pts)
                    if c < bc - 1e-9:
                        bc, cur, improved = c, t, True
    results[rname] = {"rot": rot, "center": [round(v, 2) for v in cur], "cost": round(bc, 5),
                      "coarse_cost": round(best[0], 5)}
    print("FIT", rname, results[rname], flush=True)

json.dump(results, open(out_path, "w"), indent=1)
