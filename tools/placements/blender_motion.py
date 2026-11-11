"""Key frames of a unit opening, rebuilt from src/stl-placements.json alone (the pose is kinematics.py's, the page's).

  blender -b --factory-startup --python blender_motion.py -- <placements.json> <vault download> <out_prefix> <unit key> \
      <t,t,...> <view> [<view> ...]

t: 0 closed (locked / latched) ... 1 open. Views (three.js unit frame, as in the JSON):
  iso            front right, from above
  front          straight from the front
  secz:<z>[:w[:y[:x]]]   from the front, everything in front of z cut away (a drawer's key and racks: secz:-3.2);
                 w: the width shown (default: the whole unit), centred on (x, y) (default: 0, the unit's middle)
  secx:<x>[:w[:y[:z]]]   from the right, everything right of x cut away (a case's latch: secx:10), centred on (y, z)
  zoom:<x>,<y>,<z>,<w>  iso view of a w mm wide box around a point
Writes <out_prefix>_<view>_<t>.png for every t and view. HIDDEN=1 draws the hidden key instead of the key.
Big files come from $VAULT_RENDER (the decimated copy: same coordinates), small ones from the download.
"""
import bpy, sys, os, json, math, re, mathutils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blender_pieces import keep_piece  # noqa: E402
import kinematics as K  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
pl_path, root, out, key, ts, views = argv[0], argv[1], argv[2], argv[3], [float(t) for t in argv[4].split(",")], argv[5:] or ["iso"]
P = json.load(open(pl_path, encoding="utf-8"))
unit = P["units"][key]
dec = os.environ.get("VAULT_RENDER")
skip = K.SKIP_HIDDEN if os.environ.get("HIDDEN") else K.SKIP_DEFAULT
parts = [p for p in unit["parts"] if not re.search(skip, p[0])]

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
COL = {"body": (0.86, 0.86, 0.84), "roof": (0.80, 0.84, 0.80), "facade": (0.93, 0.93, 0.92), "drawer": (0.12, 0.12, 0.14),
       "accent": (0.95, 0.42, 0.10), "mech": (0.20, 0.20, 0.23), "insert": (0.60, 0.75, 0.90)}
JOINT_COL = {"key": (0.85, 0.15, 0.15), "rack_lo": (0.15, 0.55, 0.95), "rack_hi": (0.10, 0.75, 0.45),
             "link": (0.62, 0.30, 0.85), "lever": (0.95, 0.42, 0.10)}
Y2Z = mathutils.Matrix.Rotation(math.radians(90), 4, "X")     # three.js (Y up) -> Blender (Z up)


def path_of(f):
    for base in ([root] + ([dec] if dec else [])):
        for p in (f, f.replace("²", "┬▓")):
            fp = os.path.join(base, p)
            if os.path.exists(fp):
                if base == root and dec and os.path.getsize(fp) > K.BIG:
                    continue
                return fp
    raise FileNotFoundError(f)


cache, objs = {}, []
for part in parts:
    f, role, group, m = part[:4]
    extra = part[4] if len(part) > 4 else {}
    piece = extra.get("piece")
    ck = (f, tuple(piece) if piece else None)
    if ck not in cache:
        bpy.ops.wm.stl_import(filepath=path_of(f))
        src = bpy.context.selected_objects[0]
        if piece:
            keep_piece(src.data, piece)
        cache[ck] = src.data
        bpy.data.objects.remove(src)
    o = bpy.data.objects.new(os.path.basename(f), cache[ck])
    sc.collection.objects.link(o)
    j = extra.get("joint")
    jc = None
    if j:
        jid, body = (j.split(".") + [None])[:2]
        jc = JOINT_COL.get(body) or JOINT_COL.get(re.sub(r"_(left|right|S|M)$", "", jid))
    o.color = (*(jc or COL.get(role, COL["body"])), 1)
    objs.append((o, part))

sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"
sc.display.shading.color_type = "OBJECT"
sc.display.shading.show_cavity = True
sc.display.shading.show_object_outline = True
sc.render.resolution_x, sc.render.resolution_y = 900, 900
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
sc.collection.objects.link(cam)
sc.camera = cam
cam.data.type = "ORTHO"
cam.data.clip_end = 100000
latches = {jid: K.Latch(j["latch"]) for jid, j in (unit.get("motion") or {}).get("joints", {}).items() if "latch" in j}
travel = K.travel_of(unit)
lo3, hi3 = [mathutils.Vector(v) for v in unit["bbox"]]    # three.js frame


def b(v):   # three.js point -> Blender
    return mathutils.Vector((v[0], -v[2], v[1]))


def aim(d, ctr, scale, clip=None):
    d = mathutils.Vector(d).normalized()
    cam.location = ctr + d * 3000
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    cam.data.ortho_scale = scale
    cam.data.clip_start = clip if clip is not None else 1


for t in ts:
    for o, part in objs:
        M = K.part_matrix(unit, part, t, latches, travel)
        o.matrix_world = Y2Z @ mathutils.Matrix(M.tolist())
    bpy.context.view_layer.update()
    ctr3 = (lo3 + hi3) / 2
    for v in views:
        name, _, arg = v.partition(":")
        a = [float(x) for x in re.split(r"[:,]", arg) if x] if arg else []
        size = max(hi3 - lo3)
        if name == "iso":
            aim((0.9, -1.4, 0.8), b(ctr3), size * 1.6)
        elif name == "front":
            aim((0, -1, 0), b(ctr3), max(hi3.x - lo3.x, hi3.y - lo3.y) * 1.15)
        elif name == "secz":     # from the front (Blender -Y), cut at three z = a[0]
            w = a[1] if len(a) > 1 else (hi3.x - lo3.x) * 1.1
            c = b((a[3] if len(a) > 3 else 0, a[2] if len(a) > 2 else (lo3.y + hi3.y) / 2, a[0]))
            aim((0, -1, 0), c, w, clip=3000)   # the camera is 3000 mm in front of the cut
        elif name == "secx":     # from the right (Blender +X), cut at three x = a[0]
            w = a[1] if len(a) > 1 else (hi3.z - lo3.z) * 1.1
            yc = a[2] if len(a) > 2 else (lo3.y + hi3.y) / 2
            zc = a[3] if len(a) > 3 else (lo3.z + hi3.z) / 2
            c = b((a[0], yc, zc))
            aim((1, 0, 0), c, w, clip=3000)
        elif name == "zoom":
            aim((0.9, -1.4, 0.8), b(a[:3]), a[3])
        sc.render.filepath = f"{out}_{v.replace(':', '_').replace(',', '_')}_{t:.2f}.png"
        bpy.ops.render.render(write_still=True)
print("MOTION", key, len(objs), "parts", len(ts), "poses")
