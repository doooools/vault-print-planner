"""Build an assembly from a JSON config, save a .blend and render check views.

  blender -b --factory-startup --python blender_assemble.py -- <config.json> <out_prefix> [views...]

Config:
{
  "root": "X:/.../VAULT_RENDER",
  "materials": {"body": [r,g,b], ...},
  "parts": [
    {"name": "Module", "file": "rel/path.stl", "role": "body",
     "rot": [rx, ry, rz],          # degrees, XYZ euler, about the part's bbox centre
     "move": [dx, dy, dz],         # mm, applied after rotation
     "align": {...},               # optional, see below
     "pick": [x, y, z]             # optional: keep only the file's connected piece whose bbox centre
                                   # is nearest to this point (file coordinates), see blender_pieces.py
    }, ...
  ],
  "hinge": {...},                  # optional (cases): the lid's hinge axis, written to the root as
                                   # "vault_hinge" for blender_export_placements.py
  "layout": {"id", "drawers"}      # optional: several drawers in one module (README "Layouts"), written to the
                                   # root as "vault_layout"; a part's "tags" ({drawer, side}) go to "vault_tags"
  part "ref": true                 # optional: a part assembled only to set the frame (the export leaves it out)
  "motion": {...}                  # optional: joints and opening steps (README "Motion"), written to the
                                   # root as "vault_motion"; a part's "joint" goes to the object as "vault_joint"
}
Groups: "module" parts stay, "drawer" parts slide out with the drawer, "lid" parts turn with a case lid.
Coordinates stay in the source CAD frame (mm, Blender units = mm), which for
VAULT is: X across, +Y towards the front, Z up.

align (optional) positions the rotated part by its bbox instead of "move":
  {"x": ["min"|"max"|"center", value], "y": [...], "z": [...]}
e.g. {"y": ["max", 1854.3]} puts the part's front face at y=1854.3.

Views: iso, front, back, top, bottom, left, right, secx (section at the
centre plane x = const, seen from +X), secz:<z> (section seen from top).
"""
import bpy, sys, json, math, os, mathutils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blender_pieces import keep_piece  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
cfg_path, out_prefix, views = argv[0], argv[1], argv[2:] or ["iso"]
cfg = json.load(open(cfg_path, encoding="utf-8"))
root = os.environ.get("VAULT_RENDER") or cfg.get("root")  # folder of decimated STLs, same tree as the Vault download

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.unit_settings.system = "METRIC"
sc.unit_settings.scale_length = 0.001
sc.unit_settings.length_unit = "MILLIMETERS"

DEFAULT_MATS = {
    "body": (0.85, 0.85, 0.83), "drawer": (0.08, 0.08, 0.09), "facade": (0.85, 0.85, 0.83),
    "accent": (0.95, 0.35, 0.08), "mech": (0.12, 0.12, 0.13), "roof": (0.85, 0.85, 0.83),
    "insert": (0.9, 0.9, 0.9),
}
mats = {}
for role, col in {**DEFAULT_MATS, **{k: tuple(v) for k, v in cfg.get("materials", {}).items()}}.items():
    m = bpy.data.materials.new("VAULT_" + role)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*col, 1)
    bsdf.inputs["Roughness"].default_value = 0.55
    m.diffuse_color = (*col, 1)
    mats[role] = m

coll_root = bpy.data.collections.new(cfg.get("name", "Assembly"))
sc.collection.children.link(coll_root)


def bbox_world(o):
    # from the real vertices: the local bound_box of a part printed at 45 deg
    # is inflated once rotated back
    mw = o.matrix_world
    pts = [mw @ v.co for v in o.data.vertices] if o.type == "MESH" else [mw @ mathutils.Vector(c) for c in o.bound_box]
    return (mathutils.Vector([min(p[i] for p in pts) for i in range(3)]),
            mathutils.Vector([max(p[i] for p in pts) for i in range(3)]))


objs = []
for part in cfg["parts"]:
    if part.get("skip"):
        continue
    bpy.ops.wm.stl_import(filepath=os.path.join(root, part["file"]))
    o = bpy.context.selected_objects[0]
    o.name = part["name"]
    for c in o.users_collection:
        c.objects.unlink(o)
    coll_root.objects.link(o)
    me = o.data
    # put the object origin at the bbox centre, keep world position
    vs = me.vertices
    c = mathutils.Vector([(min(v.co[i] for v in vs) + max(v.co[i] for v in vs)) / 2 for i in range(3)])
    me.transform(mathutils.Matrix.Translation(-c))
    o.location = c
    if part.get("pick"):
        # one piece of a file holding several; the centre c (and so the exported matrix) stays the whole file's
        n = keep_piece(me, part["pick"], c)
        o["vault_piece"] = [round(float(v), 3) for v in part["pick"]]
        print("PIECE", part["name"], "kept 1 of", n)
    o.rotation_euler = [math.radians(a) for a in part.get("rot", [0, 0, 0])]
    bpy.context.view_layer.update()
    if "align" in part:
        mn, mx = bbox_world(o)
        for ax, (mode, val) in part["align"].items():
            i = "xyz".index(ax)
            cur = {"min": mn[i], "max": mx[i], "center": (mn[i] + mx[i]) / 2}[mode]
            o.location[i] += val - cur
    o.location += mathutils.Vector(part.get("move", [0, 0, 0]))
    me.materials.append(mats[part.get("role", "body")])
    # Shading for decimated CAD meshes: smooth, sharp edges above 20 deg, then
    # weighted normals. (The 'Smooth by Angle' modifier gave star-shaped
    # artefacts on the flat faces; this combination is clean.)
    for p in me.polygons:
        p.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(20))
    wn = o.modifiers.new("WeightedNormal", "WEIGHTED_NORMAL")
    wn.keep_sharp = True
    wn.mode = "FACE_AREA"
    o["vault_file"] = part["file"]
    o["vault_role"] = part.get("role", "body")
    o["vault_group"] = part.get("group", "module")
    if part.get("joint"):
        o["vault_joint"] = part["joint"]
    if part.get("tags"):   # a layout's drawer index (and L² side), written to the part's 5th element
        o["vault_tags"] = json.dumps(part["tags"])
    if part.get("ref"):    # placed only to set the unit frame (a stack's first module): not exported
        o["vault_ref"] = 1
    objs.append(o)

bpy.context.view_layer.update()
info = {}
for o in objs:
    mn, mx = bbox_world(o)
    info[o.name] = {"min": [round(x, 2) for x in mn], "max": [round(x, 2) for x in mx],
                    "loc": [round(x, 3) for x in o.location], "rot": [round(math.degrees(a), 2) for a in o.rotation_euler]}
json.dump(info, open(out_prefix + "_bbox.json", "w"), indent=1)

# ---------- camera / render ----------
allmn = mathutils.Vector([min(info[k]["min"][i] for k in info) for i in range(3)])
allmx = mathutils.Vector([max(info[k]["max"][i] for k in info) for i in range(3)])
ctr = (allmn + allmx) / 2
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
sc.collection.objects.link(cam)
sc.camera = cam
cam.data.type = "ORTHO"
cam.data.clip_end = 100000
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"
sc.display.shading.color_type = "MATERIAL"
sc.display.shading.show_cavity = True
sc.display.shading.show_object_outline = True
sc.display.shading.background_type = "VIEWPORT" if hasattr(sc.display.shading, "background_type") else sc.display.shading.background_type
sc.render.resolution_x, sc.render.resolution_y = 1400, 1000
world = bpy.data.worlds.new("w")
sc.world = world
world.color = (0.35, 0.37, 0.4)

VIEWS = {"iso": (-1, 1.3, 0.9), "isoback": (1, -1.3, 0.9), "front": (0, 1, 0), "back": (0, -1, 0),
         "top": (0, 0, 1), "bottom": (0, 0, -1), "left": (-1, 0, 0), "right": (1, 0, 0),
         "secx": (1, 0, 0)}
for v in views:
    name, _, arg = v.partition(":")
    d = mathutils.Vector(VIEWS.get(name, (0, 0, 1))).normalized()
    if name == "secz":
        d = mathutils.Vector((0, 0, 1))
    dist = 3000
    cam.location = ctr + d * dist
    q = (-d).to_track_quat("-Z", "Y")
    if name in ("top", "secz", "bottom"):
        q = mathutils.Euler((0, 0, 0) if name != "bottom" else (math.pi, 0, 0)).to_quaternion()
    cam.rotation_euler = q.to_euler()
    cam.data.clip_start = 1
    if name == "secx":  # cut at x = arg (default centre), look from +X
        x0 = float(arg) if arg else ctr.x
        cam.data.clip_start = cam.location.x - x0
    if name == "secz":
        z0 = float(arg) if arg else ctr.z
        cam.data.clip_start = cam.location.z - z0
    bpy.context.view_layer.update()
    inv = cam.matrix_world.inverted()
    pts = [inv @ mathutils.Vector((x, y, z)) for x in (allmn.x, allmx.x) for y in (allmn.y, allmx.y) for z in (allmn.z, allmx.z)]
    w = max(p.x for p in pts) - min(p.x for p in pts)
    h = max(p.y for p in pts) - min(p.y for p in pts)
    cam.data.ortho_scale = max(w, h * 1.4) * 1.1
    sc.render.filepath = f"{out_prefix}_{v.replace(':', '_')}.png"
    bpy.ops.render.render(write_still=True)

fin = cfg.get("finalize")
if fin:
    # Hierarchy: <Root> (front-bottom-centre of the anchor part, front facing -Y)
    #              +- <Root>_Drawer  (empty: move it along -Y to open the drawer)
    #              +- module parts
    bpy.data.objects.remove(cam)
    a = bpy.data.objects[fin["anchor"]]
    mn, mx = bbox_world(a)
    anchor = mathutils.Vector(((mn.x + mx.x) / 2, mx.y, mn.z))  # CAD frame: front is +Y
    root = bpy.data.objects.new(cfg.get("name", "Assembly"), None)
    root.empty_display_type = "ARROWS"
    root.empty_display_size = 30
    if cfg.get("key"):
        root["vault_key"] = cfg["key"]  # the planner's unit key, read by blender_export_placements.py
    if cfg.get("hinge"):
        root["vault_hinge"] = json.dumps(cfg["hinge"])
    if cfg.get("motion"):
        root["vault_motion"] = json.dumps(cfg["motion"])
    if cfg.get("layout"):
        root["vault_layout"] = json.dumps(cfg["layout"])
    if cfg.get("floor"):
        root["vault_floor"] = json.dumps(cfg["floor"])
    coll_root.objects.link(root)
    drawer = bpy.data.objects.new(cfg.get("name", "Assembly") + "_Drawer", None)
    drawer.empty_display_type = "SINGLE_ARROW"
    drawer.empty_display_size = 40
    coll_root.objects.link(drawer)
    sub = {}
    for g in ("module", "drawer", "lid"):
        sub[g] = bpy.data.collections.new(cfg.get("name", "Assembly") + "_" + g)
        coll_root.children.link(sub[g])
    root.location = anchor
    drawer.parent = root  # identity parent inverse: drawer sits exactly on the root
    bpy.context.view_layer.update()
    for o in objs:
        par = drawer if o["vault_group"] == "drawer" else root
        mw = o.matrix_world.copy()
        o.parent = par
        o.matrix_parent_inverse = mathutils.Matrix.Identity(4)
        bpy.context.view_layer.update()
        o.matrix_world = mw
        coll_root.objects.unlink(o)
        sub[o["vault_group"]].objects.link(o)
    # bring to world origin and turn so the front faces -Y (Blender front view)
    root.location = (0, 0, 0)
    root.rotation_euler = (0, 0, math.pi)
    # opening the drawer = moving the drawer empty along its local +Y (towards the viewer)
    drawer["open_mm_hint"] = "set location Y (local) between 0 and ~120 to pull the drawer out"
    bpy.context.view_layer.update()

bpy.ops.wm.save_as_mainfile(filepath=out_prefix + ".blend")
print("ASSEMBLED", len(objs), "parts")
