"""Studio render of an assembled VAULT .blend.

  blender -b <file.blend> --python blender_render.py -- <out.png> [--open MM] [--colors JSON] [--samples N] [--save]

--colors: {"body": [r,g,b], "drawer": [...], ...} overrides the VAULT_<role> materials.
--save:   keep the studio (lights, floor, camera) in the .blend.
"""
import bpy, sys, math, json, mathutils

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]
opt = {"open": 0.0, "colors": None, "samples": 96, "save": False}
i = 1
while i < len(argv):
    k = argv[i].lstrip("-")
    if k == "save":
        opt["save"] = True
        i += 1
        continue
    opt[k] = argv[i + 1]
    i += 2
sc = bpy.context.scene

if opt["colors"]:
    for role, col in json.loads(opt["colors"]).items():
        # also VAULT_body.001 ... (copies brought in by blender_showcase.py)
        for m in bpy.data.materials:
            if m.name == "VAULT_" + role or m.name.startswith("VAULT_" + role + "."):
                b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
                b.inputs["Base Color"].default_value = (*col, 1)
                m.diffuse_color = (*col, 1)

if any(a == "--open" for a in argv):  # only when asked: otherwise keep the drawers as saved
    for o in bpy.data.objects:
        if o.type == "EMPTY" and "_Drawer" in o.name:
            o.location.y = float(opt["open"])
bpy.context.view_layer.update()

# scene bounds (meshes only)
pts = [o.matrix_world @ mathutils.Vector(c) for o in bpy.data.objects if o.type == "MESH" for c in o.bound_box]
mn = mathutils.Vector([min(p[i] for p in pts) for i in range(3)])
mx = mathutils.Vector([max(p[i] for p in pts) for i in range(3)])
ctr = (mn + mx) / 2
size = (mx - mn).length

studio = bpy.data.collections.new("Studio")
sc.collection.children.link(studio)


def add(obj):
    studio.objects.link(obj)
    return obj


# floor (big plane slightly under the part)
me = bpy.data.meshes.new("floor")
s = size * 20
me.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [(0, 1, 2, 3)])
floor = add(bpy.data.objects.new("Floor", me))
floor.location = (ctr.x, ctr.y, mn.z - 0.01)
fm = bpy.data.materials.new("Floor")
fm.use_nodes = True
fb = next(n for n in fm.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
fb.inputs["Base Color"].default_value = (0.42, 0.44, 0.47, 1)
fb.inputs["Roughness"].default_value = 0.8
me.materials.append(fm)


def area(name, loc, energy, sz):
    L = bpy.data.lights.new(name, "AREA")
    L.energy = energy
    L.size = sz
    o = add(bpy.data.objects.new(name, L))
    o.location = loc
    d = ctr - mathutils.Vector(loc)
    o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    return o


k = size / 200.0  # energies tuned for ~200 mm assemblies, scale with area
area("Key", ctr + mathutils.Vector((-1.2, -1.6, 1.8)) * size, 2.2e6 * k * k, size * 1.2)
area("Fill", ctr + mathutils.Vector((1.8, -0.8, 0.9)) * size, 0.7e6 * k * k, size * 1.5)
area("Rim", ctr + mathutils.Vector((0.6, 2.0, 1.4)) * size, 1.3e6 * k * k, size)
w = bpy.data.worlds.get("w") or bpy.data.worlds.new("w")
sc.world = w
w.use_nodes = True
bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
bg.inputs["Color"].default_value = (0.5, 0.52, 0.55, 1)
bg.inputs["Strength"].default_value = 0.35

cam = add(bpy.data.objects.new("RenderCam", bpy.data.cameras.new("RenderCam")))
cam.data.lens = 85
cam.data.clip_start = 1
cam.data.clip_end = size * 100
d = mathutils.Vector((-0.75, -1.35, 0.85)).normalized()  # front (-Y) three-quarter, from above
cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
sc.camera = cam
sc.render.resolution_x, sc.render.resolution_y = 1800, 1200
# distance so the bounds fit the frame
fov = 2 * math.atan(36 / 2 / cam.data.lens)
cam.location = ctr + d * (size * 0.5 / math.tan(fov / 2) * 1.25)

try:
    sc.render.engine = "CYCLES"
except TypeError:
    pass
sc.cycles.samples = int(opt["samples"])
sc.cycles.use_denoising = True
try:
    sc.cycles.device = "GPU"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.refresh_devices()
    if not any(dv.use for dv in prefs.devices if dv.type != "CPU"):
        sc.cycles.device = "CPU"
except Exception:
    sc.cycles.device = "CPU"
sc.view_settings.view_transform = "AgX" if "AgX" in [i.identifier for i in bpy.types.ColorManagedViewSettings.bl_rna.properties["view_transform"].enum_items] else sc.view_settings.view_transform
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print("RENDERED", out)
if opt["save"]:
    bpy.ops.wm.save_mainfile()
