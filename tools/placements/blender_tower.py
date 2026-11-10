"""Stack assembled VAULT modules (and an optional roof) into a tower.

  blender -b --factory-startup --python blender_tower.py -- <out.blend> <x_mm> <item> [<item> ...]

Items go bottom to top:  path.blend|levels|open_mm|facade_rgb
  levels  : 1, 2 or 4 for a 1F/2F/4F module, 0 for a roof (must be last)
  open_mm : drawer opening (optional)
  facade_rgb : "r,g,b" facade colour for this module (optional)
Several towers can go in the same file: call again with the same out.blend
and another x_mm (the file is opened when it exists).

Stacking rule measured on L7: a module's underside reliefs rest on the top
face of the module below, so the next module starts 52 mm + 48 mm per extra
level above the bottom of the one below (52 / 100 / 196 mm for 1F / 2F / 4F).
Roofs have the same underside as a module.
"""
import bpy, sys, os

argv = sys.argv[sys.argv.index("--") + 1:]
out, x0, items = argv[0], float(argv[1]), argv[2:]
if os.path.exists(out):
    bpy.ops.wm.open_mainfile(filepath=out)
else:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = "METRIC"
    sc.unit_settings.scale_length = 0.001
    sc.unit_settings.length_unit = "MILLIMETERS"
sc = bpy.context.scene


def pitch(levels):
    return 52.0 + 48.0 * (levels - 1)


z = 0.0
for it in items:
    path, levels, *rest = it.split("|")
    levels = int(levels)
    open_mm = float(rest[0]) if rest and rest[0] else 0.0
    face = [float(v) for v in rest[1].split(",")] if len(rest) > 1 and rest[1] else None
    name = os.path.splitext(os.path.basename(path))[0]
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.collections = [c for c in src.collections if c == name]
    coll = dst.collections[0]
    sc.collection.children.link(coll)
    objs = list(coll.all_objects)
    root = next(o for o in objs if o.type == "EMPTY" and o.parent is None)
    root.location = (x0, 0.0, z)
    # "_Drawer" or "_Drawer.001" when the same module is used twice
    drawer = next((o for o in objs if o.type == "EMPTY" and "_Drawer" in o.name), None)
    if drawer:
        drawer.location.y = open_mm
    if face:
        for m in {s.material for o in objs if o.type == "MESH" for s in o.material_slots if s.material}:
            if m.name.startswith("VAULT_facade"):
                b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
                b.inputs["Base Color"].default_value = (*face, 1)
                m.diffuse_color = (*face, 1)
    print("STACKED", root.name, "at z", z)
    if levels:
        z += pitch(levels)
bpy.ops.wm.save_as_mainfile(filepath=out)
