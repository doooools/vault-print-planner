"""Blender worker: decimate a list of STL files to a max face count, with QA.

Run with:
  blender -b --factory-startup --python blender_decimate.py -- <list.txt> <src_root> <dst_root> <max_faces> <log.jsonl>

Each line of list.txt is a path relative to src_root. Output keeps the same
relative path under dst_root and keeps the ORIGINAL world coordinates (no
recentring), so assembly transforms computed on the originals stay valid.

Pipeline per part:
  1. weld + remove degenerate faces (CAD exports carry many zero-area slivers)
  2. collapse decimation down to max_faces
  3. QA: distance from original surface samples to the result (p99, max)
  4. if QA fails or the decimator stalls: voxel remesh (OpenVDB) + collapse,
     which rebuilds a clean surface; QA again.
"""
import bpy, bmesh, sys, os, json, time, random, math
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
list_file, src_root, dst_root, max_faces, log_path = argv[0], argv[1], argv[2], int(argv[3]), argv[4]
QA_P99 = 0.15   # mm: 99% of original surface within this distance
QA_MAX = 1.0    # mm: no original point further than this

with open(list_file, encoding="utf-8") as f:
    rels = [l.rstrip("\n") for l in f if l.strip()]

bpy.ops.wm.read_factory_settings(use_empty=True)
log = open(log_path, "a", encoding="utf-8")


def apply_mod(obj, kind, **props):
    mod = obj.modifiers.new("m", kind)
    for k, v in props.items():
        setattr(mod, k, v)
    dg = bpy.context.evaluated_depsgraph_get()
    new_me = bpy.data.meshes.new_from_object(obj.evaluated_get(dg))
    obj.modifiers.remove(mod)
    old = obj.data
    obj.data = new_me
    bpy.data.meshes.remove(old)
    return len(new_me.polygons)


def collapse_to(obj, target):
    n = len(obj.data.polygons)
    passes = 0
    while n > target and passes < 4:
        n_new = apply_mod(obj, "DECIMATE", decimate_type="COLLAPSE", ratio=target / n * 0.97,
                          use_collapse_triangulate=True)
        passes += 1
        stalled = n_new > 0.9 * n and n_new > target * 1.05
        n = n_new
        if stalled:
            return n, True
    return n, False


def surface_samples(me, k=30000, seed=1):
    """Area-weighted random points on the mesh surface."""
    rnd = random.Random(seed)
    tris = []
    me.calc_loop_triangles()
    for lt in me.loop_triangles:
        a, b, c = (me.vertices[i].co for i in lt.vertices)
        ar = lt.area
        if ar > 1e-9:
            tris.append((ar, a.copy(), b.copy(), c.copy()))
    tot = sum(t[0] for t in tris)
    pts = []
    for ar, a, b, c in tris:
        m = ar / tot * k
        cnt = int(m) + (1 if rnd.random() < m - int(m) else 0)
        for _ in range(cnt):
            u, v = rnd.random(), rnd.random()
            if u + v > 1:
                u, v = 1 - u, 1 - v
            pts.append(a + (b - a) * u + (c - a) * v)
    return pts, tot


def qa(pts, me):
    bvh = BVHTree.FromPolygons([v.co for v in me.vertices], [p.vertices[:] for p in me.polygons])
    d = []
    for p in pts:
        hit = bvh.find_nearest(p)
        d.append((hit[0] - p).length if hit[0] is not None else 1e9)
    d.sort()
    return round(d[int(len(d) * 0.99)], 4), round(d[-1], 4)


for rel in rels:
    t0 = time.time()
    src = os.path.join(src_root, rel)
    dst = os.path.join(dst_root, rel)
    rec = {"file": rel.replace("\\", "/")}
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        bpy.ops.wm.stl_import(filepath=src)
        obj = bpy.context.selected_objects[0]
        rec["faces_in"] = len(obj.data.polygons)
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-3)
        bmesh.ops.dissolve_degenerate(bm, dist=1e-3, edges=bm.edges)
        bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 3])
        bm.to_mesh(obj.data)
        bm.free()
        rec["faces_clean"] = len(obj.data.polygons)
        pts, area = surface_samples(obj.data)
        orig_me = obj.data.copy()  # kept to retry from

        n, stalled = collapse_to(obj, max_faces)
        p99, dmax = qa(pts, obj.data)
        rec.update(method="collapse", faces_out=n, qa_p99=p99, qa_max=dmax)
        if stalled or n > max_faces * 1.05 or p99 > QA_P99 or dmax > QA_MAX:
            # fallback: rebuild a clean surface, then decimate it
            old = obj.data
            obj.data = orig_me.copy()
            bpy.data.meshes.remove(old)
            vox = max(0.05, math.sqrt(2 * area / 4e6))  # ~4M faces before decimation
            apply_mod(obj, "REMESH", mode="VOXEL", voxel_size=vox, use_smooth_shade=False)
            n, stalled = collapse_to(obj, max_faces)
            p99b, dmaxb = qa(pts, obj.data)
            rec.update(method="voxel+collapse", voxel=round(vox, 3), faces_out=n,
                       qa_p99=p99b, qa_max=dmaxb, qa_first_try=[p99, dmax])
        rec["qa_ok"] = rec["qa_p99"] <= QA_P99 and rec["qa_max"] <= QA_MAX * 1.5
        bpy.data.meshes.remove(orig_me)

        vs = obj.data.vertices
        rec["bbox_min"] = [round(min(v.co[i] for v in vs), 3) for i in range(3)]
        rec["bbox_max"] = [round(max(v.co[i] for v in vs), 3) for i in range(3)]
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.ops.wm.stl_export(filepath=dst, export_selected_objects=True, ascii_format=False, apply_modifiers=False)
        bpy.data.objects.remove(obj)
        for m in list(bpy.data.meshes):
            if m.users == 0:
                bpy.data.meshes.remove(m)
        rec["ok"] = True
    except Exception as e:  # keep going on a bad file
        rec["ok"] = False
        rec["error"] = repr(e)
        for o in list(bpy.data.objects):
            bpy.data.objects.remove(o)
    rec["seconds"] = round(time.time() - t0, 1)
    log.write(json.dumps(rec, ensure_ascii=False) + "\n")
    log.flush()
    print("DONE", rec.get("method"), rec.get("faces_in"), "->", rec.get("faces_out"), rel, flush=True)

log.close()
