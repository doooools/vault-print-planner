"""Render quick Workbench previews of STL files side by side (QA tool).

  blender -b --factory-startup --python blender_preview.py -- <out.png> <view: iso|top|bottom|front> <a.stl> [b.stl ...]

Each STL is centred on its own bbox and laid out along X so originals and
decimated versions can be compared in one image.
"""
import bpy, sys, math, mathutils

argv = sys.argv[sys.argv.index("--") + 1:]
out, view, files = argv[0], argv[1], argv[2:]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
x = 0.0
objs = []
for p in files:
    bpy.ops.wm.stl_import(filepath=p)
    o = bpy.context.selected_objects[0]
    bb = [o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    mn = mathutils.Vector([min(c[i] for c in bb) for i in range(3)])
    mx = mathutils.Vector([max(c[i] for c in bb) for i in range(3)])
    size = mx - mn
    o.location -= (mn + mx) / 2
    o.location.x += x + size.x / 2
    x += size.x * 1.15
    objs.append(o)
for o in objs:
    o.select_set(True)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
sc.collection.objects.link(cam)
sc.camera = cam
cam.data.type = "ORTHO"
dirs = {"iso": (1, -1, 0.8), "top": (0, 0, 1), "bottom": (0, 0, -1), "front": (0, -1, 0)}
d = mathutils.Vector(dirs[view]).normalized()
cam.location = d * 5000
cam.rotation_euler = (-d).to_track_quat("-Z", "Y" if view in ("top", "bottom") else "Z").to_euler()
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"
sc.display.shading.show_cavity = True
sc.display.shading.show_object_outline = True
sc.render.resolution_x, sc.render.resolution_y = 1600, 900
sc.render.film_transparent = False
bpy.context.view_layer.update()
bpy.ops.object.select_all(action="SELECT")
cam.select_set(False)
# fit ortho camera on the selection
ctx = {}
pts = []
for o in objs:
    pts += [o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
inv = cam.matrix_world.inverted()
loc = [inv @ p for p in pts]
w = max(p.x for p in loc) - min(p.x for p in loc)
h = max(p.y for p in loc) - min(p.y for p in loc)
cx = (max(p.x for p in loc) + min(p.x for p in loc)) / 2
cy = (max(p.y for p in loc) + min(p.y for p in loc)) / 2
cam.location = cam.matrix_world @ mathutils.Vector((cx, cy, 0))
cam.data.ortho_scale = max(w, h * 16 / 9) * 1.08
cam.data.clip_end = 20000
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
