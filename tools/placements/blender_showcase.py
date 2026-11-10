"""Put several assembled .blend files side by side in one scene.

  blender -b --factory-startup --python blender_showcase.py -- <out.blend> <gap_mm> <a.blend>[:open_mm[:facade_rgb]] ...

Each source .blend's assembly collection is appended (its materials come
along as separate copies, so each assembly can get its own colours), its
root empty is moved along X, its drawer opened by open_mm, and its facade
material recoloured when facade_rgb ("r,g,b") is given.
"""
import bpy, sys, os, mathutils

argv = sys.argv[sys.argv.index("--") + 1:]
out, gap, items = argv[0], float(argv[1]), argv[2:]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.unit_settings.system = "METRIC"
sc.unit_settings.scale_length = 0.001
sc.unit_settings.length_unit = "MILLIMETERS"

x = 0.0
for it in items:
    path, *rest = it.split("|")
    open_mm = float(rest[0]) if rest else 0.0
    face = [float(v) for v in rest[1].split(",")] if len(rest) > 1 else None
    name = os.path.splitext(os.path.basename(path))[0]
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.collections = [c for c in src.collections if c == name]
    coll = dst.collections[0]
    sc.collection.children.link(coll)
    objs = list(coll.all_objects)
    root = next(o for o in objs if o.type == "EMPTY" and o.parent is None)
    drawer = next(o for o in objs if o.type == "EMPTY" and o.name.endswith("_Drawer"))
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ mathutils.Vector(c) for o in objs if o.type == "MESH" for c in o.bound_box]
    w = max(p.x for p in pts) - min(p.x for p in pts)
    root.location.x = x + w / 2
    x += w + gap
    drawer.location.y = open_mm
    if face:
        mats = {s.material for o in objs if o.type == "MESH" for s in o.material_slots if s.material}
        for m in mats:
            if m.name.startswith("VAULT_facade"):
                b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
                b.inputs["Base Color"].default_value = (*face, 1)
                m.diffuse_color = (*face, 1)
    print("ADDED", name, "width", round(w, 1))
bpy.ops.wm.save_as_mainfile(filepath=out)
