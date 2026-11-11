"""Rebuild a stack from src/stl-placements.json alone (as the page will) and render it.

  blender -b --factory-startup --python blender_check_placements.py -- <placements.json> <stl_root> <out.png> <unit key> [<unit key> ...]

Units go bottom to top, e.g.  drawer|L|7|4  drawer|L|7|2  roof|L|7|grid
Also writes <out>_secx.png (the stack cut at x = SEC_X, default 0.3 mm right of the middle, seen from
the right; set SEC_X to cut through an off-centre latch) and <out>.blend.
stl_root: the Vault download (or its decimated copy: same coordinates).
LID_DEG=<deg> opens case lids (group "lid") by that angle about the unit's hinge axis; VIEW="x,y,z" sets
the camera direction (Blender axes, default 0.9,-1.4,0.8: front right, from above). One entry holds every
variant of a unit (key and hidden key, every baseplate, ...): SKIP="text,text" leaves out the parts whose path
contains one of them, as the page does for the files a unit's part list doesn't name.
Bolts (`hardware`, tools/placements/hardware.py) are made from their standard sizes (hw_shapes.py, as the page
does) and drawn with the part that holds them; HW=0 leaves them out. HIDE="text,text" hides parts (not their
bolts) whose path contains one of them, to see bolt heads under caps. FOCUS="x,y,z,size" (three.js frame of the
stack, mm) frames a close-up instead of the whole stack; SEC_X still cuts the side view.
Only reads the JSON and the STL files: this checks the exported matrices and the
stacking rule independently of the .blend files they came from.
"""
import bpy, sys, os, json, math, mathutils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blender_pieces import keep_piece  # noqa: E402
import hw_shapes  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
pl_path, root, out, keys = argv[0], argv[1], argv[2], argv[3:]
P = json.load(open(pl_path, encoding="utf-8"))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
COL = {"body": (0.85, 0.85, 0.83), "roof": (0.85, 0.85, 0.83), "facade": (0.95, 0.45, 0.1), "drawer": (0.1, 0.1, 0.12),
       "accent": (0.95, 0.35, 0.08), "mech": (0.15, 0.15, 0.17), "insert": (0.6, 0.75, 0.9), "hardware": (0.2, 0.75, 0.95)}
mats = {}
for k, c in COL.items():
    m = bpy.data.materials.new(k)
    m.diffuse_color = (*c, 1)
    mats[k] = m
# three.js frame (Y up) -> Blender (Z up): rotate +90 deg about X
Y2Z = mathutils.Matrix.Rotation(math.radians(90), 4, "X")
cache = {}
hw_cache = {}
SIZES = P.get("hardware_sizes", {})
SKIPS = [k for k in os.environ.get("SKIP", "").split(",") if k]
HIDES = [k for k in os.environ.get("HIDE", "").split(",") if k]


def bolt_mesh(spec):
    if spec not in hw_cache:
        s = hw_shapes.spec_size(spec, SIZES)
        v, f = hw_shapes.revolve(hw_shapes.profile(s))
        me = bpy.data.meshes.new(spec)
        me.from_pydata(v, [], f)
        me.update()
        hw_cache[spec] = me
    return hw_cache[spec]


y = 0.0
for key in keys:
    u = P["units"][key]
    if key.startswith("stack|") and not y:   # a base first: its frame is the first module's, lifted by its wheels
        y = -u["floor"]["wheels"]
    lid = mathutils.Matrix.Identity(4)
    if u.get("hinge") and float(os.environ.get("LID_DEG", "0")):
        hg = u["hinge"]
        O = mathutils.Vector(hg["origin"])
        lid = (mathutils.Matrix.Translation(O) @ mathutils.Matrix.Rotation(math.radians(float(os.environ["LID_DEG"])), 4, mathutils.Vector(hg["axis"]))
               @ mathutils.Matrix.Translation(-O))
    for part in u["parts"]:
        f, role, group, m = part[:4]
        if any(k in f for k in SKIPS + HIDES):
            continue
        piece = part[4].get("piece") if len(part) > 4 else None
        ck = (f, tuple(piece) if piece else None)
        if ck not in cache:
            fp = os.path.join(root, f)
            if not os.path.exists(fp):  # some unzip tools turn the '²' of L²/XL² into '┬▓'
                fp = os.path.join(root, f.replace("²", "┬▓"))
            bpy.ops.wm.stl_import(filepath=fp)
            src = bpy.context.selected_objects[0]
            if piece:
                keep_piece(src.data, piece)
            cache[ck] = src.data
            bpy.data.objects.remove(src)
        o = bpy.data.objects.new(os.path.basename(f), cache[ck])
        sc.collection.objects.link(o)
        M = mathutils.Matrix((m[0:4], m[4:8], m[8:12], (0, 0, 0, 1)))
        if group == "lid":
            M = lid @ M
        o.matrix_world = Y2Z @ mathutils.Matrix.Translation((0, y, 0)) @ M
        o.material_slots and None
        if not o.data.materials:
            o.data.materials.append(mats.get(role, mats["body"]))
        o.color = (*COL.get(role, COL["body"]), 1)
    for b in (u.get("hardware", []) if os.environ.get("HW", "1") != "0" else []):
        spec, group, m, o = b
        if any(k in u["parts"][o["part"]][0] for k in SKIPS):
            continue
        ob = bpy.data.objects.new(spec, bolt_mesh(spec))
        sc.collection.objects.link(ob)
        M = mathutils.Matrix((m[0:4], m[4:8], m[8:12], (0, 0, 0, 1)))
        if group == "lid":
            M = lid @ M
        ob.matrix_world = Y2Z @ mathutils.Matrix.Translation((0, y, 0)) @ M
        ob.color = (*COL["hardware"], 1)
    lv = int(key.split("|")[3]) if key.split("|")[0] in ("drawer", "case") else 0
    print("PLACED", key, "at", y)
    if key.startswith("case"):
        y += P["stack"]["case"]["rise"][str(lv)]
    elif lv:
        y += P["stack"]["first"] + P["stack"]["per_level"] * (lv - 1)

sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"
sc.display.shading.color_type = "OBJECT"
sc.display.shading.show_cavity = True
sc.render.resolution_x, sc.render.resolution_y = 1000, 1200
bpy.context.view_layer.update()
pts = [o.matrix_world @ mathutils.Vector(c) for o in sc.objects if o.type == "MESH" for c in o.bound_box]
mn = mathutils.Vector([min(p[i] for p in pts) for i in range(3)])
mx = mathutils.Vector([max(p[i] for p in pts) for i in range(3)])
ctr = (mn + mx) / 2
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
sc.collection.objects.link(cam)
sc.camera = cam
cam.data.type = "ORTHO"
cam.data.clip_end = 100000
d = mathutils.Vector([float(v) for v in os.environ.get("VIEW", "0.9,-1.4,0.8").split(",")]).normalized()   # front (-Y in Blender = +Z three) right, from above
cam.location = ctr + d * 4000
cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
cam.data.ortho_scale = (mx - mn).length * 0.95
if os.environ.get("FOCUS"):
    fx, fy, fz, fs = [float(v) for v in os.environ["FOCUS"].split(",")]
    ctr = Y2Z @ mathutils.Vector((fx, fy, fz))
    cam.location = ctr + d * 4000
    cam.data.ortho_scale = fs
    sc.render.resolution_x = sc.render.resolution_y = 1000
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
# side section: camera on +X (Blender), clipping everything right of x0
x0 = float(os.environ.get("SEC_X", "0.3"))
cam.location = (mx.x + 2000, ctr.y, ctr.z)
cam.rotation_euler = mathutils.Vector((-1, 0, 0)).to_track_quat("-Z", "Y").to_euler()
cam.data.clip_start = cam.location.x - x0
cam.data.ortho_scale = max(mx.y - mn.y, mx.z - mn.z) * 1.1
sc.render.resolution_x, sc.render.resolution_y = 1000, 1200
if os.environ.get("FOCUS"):
    cam.data.ortho_scale = fs
    sc.render.resolution_x = sc.render.resolution_y = 1000
sc.render.filepath = os.path.splitext(out)[0] + "_secx.png"
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.splitext(out)[0] + ".blend")
print("CHECKED", out)
