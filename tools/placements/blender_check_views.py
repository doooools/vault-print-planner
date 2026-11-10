"""Workbench check views of any .blend (world frame: front faces -Y).

  blender -b <file.blend> --python blender_check_views.py -- <out_prefix> <view> [<view> ...]

Views: iso, front, side, secx[:x] (cut at x, seen from +X), secy[:y] (cut at y, seen from -Y),
       zoom boxes: add @x0,z0,x1,z1 to a sec/side view to crop the ortho frame (world mm).
"""
import bpy, sys, math, mathutils

argv = sys.argv[sys.argv.index("--") + 1:]
pre, views = argv[0], argv[1:]
sc = bpy.context.scene
pts = [o.matrix_world @ mathutils.Vector(c) for o in sc.objects if o.type == "MESH" and o.visible_get() for c in o.bound_box]
mn = mathutils.Vector([min(p[i] for p in pts) for i in range(3)])
mx = mathutils.Vector([max(p[i] for p in pts) for i in range(3)])
ctr = (mn + mx) / 2
cam = bpy.data.objects.new("chk", bpy.data.cameras.new("chk"))
sc.collection.objects.link(cam)
sc.camera = cam
cam.data.type = "ORTHO"
cam.data.clip_end = 100000
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"
sc.display.shading.color_type = "MATERIAL"
sc.display.shading.show_cavity = True
sc.display.shading.show_object_outline = True
sc.render.resolution_x, sc.render.resolution_y = 1400, 1000
for o in [o for o in sc.objects if o.name in ("Floor",)]:
    o.hide_render = True
for v in views:
    spec, _, box = v.partition("@")
    name, _, arg = spec.partition(":")
    d = {"iso": (1, -1.3, 0.9), "front": (0, -1, 0), "side": (1, 0, 0), "secx": (1, 0, 0), "secy": (0, -1, 0)}[name]
    d = mathutils.Vector(d).normalized()
    cam.location = ctr + d * 5000
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    cam.data.clip_start = 1
    if name == "secx":
        cam.data.clip_start = cam.location.x - (float(arg) if arg else ctr.x)
    if name == "secy":
        cam.data.clip_start = (float(arg) if arg else ctr.y) - cam.location.y
    bpy.context.view_layer.update()
    if box:
        x0, z0, x1, z1 = [float(t) for t in box.split(",")]
        # box is in the view plane: (y,z) for side/secx, (x,z) for front/secy
        if name in ("side", "secx"):
            cam.location.y, cam.location.z = (x0 + x1) / 2, (z0 + z1) / 2
        else:
            cam.location.x, cam.location.z = (x0 + x1) / 2, (z0 + z1) / 2
        cam.data.ortho_scale = max(abs(x1 - x0), abs(z1 - z0) * 1.4)
    else:
        inv = cam.matrix_world.inverted()
        q = [inv @ mathutils.Vector((x, y, z)) for x in (mn.x, mx.x) for y in (mn.y, mx.y) for z in (mn.z, mx.z)]
        cam.data.ortho_scale = max(max(p.x for p in q) - min(p.x for p in q), (max(p.y for p in q) - min(p.y for p in q)) * 1.4) * 1.08
    sc.render.filepath = f"{pre}_{v.replace(':', '_').replace('@', '_').replace(',', '_')}.png"
    bpy.ops.render.render(write_still=True)
print("CHECKED", len(views))
