"""Generate assembly recipes (JSON for blender_assemble.py) for every Vault unit the planner can build.

  python make_recipes.py <out_dir> [family ...]        families: S M L (default: all known)

Needs (outside the repo, next to the decimated copy):
  $VAULT_ASSEMBLY/_stl_index.jsonl   bbox of every downloaded file (stl_index.py)
  $VAULT_ASSEMBLY/_orient.json       how each module/roof is turned (orient.py)
  $VAULT_RENDER                      decimated copy (features.py reads it)
Measured features (stopper holes, latch frames, counterbores) are cached in $VAULT_ASSEMBLY/_features.json.

Rules (measured on S3 and L7, then checked per family, see README):
  - The box is in place in the CAD file; everything else is set relative to the box's own bbox
    (centre x `cx`, front `yf`, bottom `zb`). The CAD file has S4-S6 boxes 1 mm higher than the
    others; relative to their box the parts are the same.
  - Module: turned as orient.py says, x centred, front at yf + 0.06, bottom at zb - 9.8 (MODULE_UNDER_BOX).
  - Levels: k = 0..h-1 at z = zb + 18.5 + 48 k (runners, stoppers); key, rails and label on level 0.
  - Stopper: centre 0.29 mm behind the module's side hole, 0.16 mm proud of the wall.
  - Latches: in the latch frames under the module (53.5 mm long, back edge 12 mm from the module's
    back), the latch's front edge 1.94 mm behind the frame's.
  - Facade caps: in every counterbore but the one under the label; label at the facade's left end.
  - Motion (recipe "motion", parts' "joint"): the key lock of every drawer and the toggle latches of every case,
    see KEY_* and LATCH_* below and the README ("Motion").
"""
import json, os, re, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vault_geom as vg  # noqa: E402
import features as F  # noqa: E402

ASM = os.environ.get("VAULT_ASSEMBLY", "VAULT_ASSEMBLY")
IDX = vg.Index(os.path.join(ASM, "_stl_index.jsonl"))
# the download's own spelling, found from the planner's: case differs (1F / 1f), and some unzip tools
# turn the '²' of L²/XL² into '┬▓' (cp437). Recipes keep the spelling on disk; the export writes '²'.
def _norm(p):
    """Like the planner's R.norm (case, quotes and spaces don't count: 'M3 1F Module .stl', 'L4F' Facade')."""
    return re.sub(r"['’\s]", "", p.replace("┬▓", "²").lower())


LOWER = {_norm(k): k for k in IDX.rows}
ORIENT = {}
for _f in sorted(os.listdir(ASM)):
    if _f.startswith("_orient") and _f.endswith(".json"):
        ORIENT.update(json.load(open(os.path.join(ASM, _f), encoding="utf-8")))
FEAT_PATH = os.path.join(ASM, "_features.json")
FEAT = json.load(open(FEAT_PATH, encoding="utf-8")) if os.path.exists(FEAT_PATH) else {}

D = "01. DRAWERS/"
U = D + "07. Universal/"
FAM = {"S": "01. S Families", "M": "02. M Families", "L": "03. L Families", "L2": "04. L² Families",
       "XL": "05. XL Families", "XL2": "06. XL² Families"}
WIDTH = {"S": 164.8, "M": 254.0, "L": 329.6, "L2": 329.6, "XL": 418.8, "XL2": 418.8}
LABEL_IN = {"S": 49.75, "M": 49.7, "L": 49.61}   # label's left end, from the module's right edge (CAD x)
ROOFS = {"bowl": "Bowl Roof", "grid": "Grid Roof", "heavy": "Heawyweight Roof", "table": "Table Roof",
         "undertable": "Under Table Mount Roof", "heavycut": "Heavyweight Roof Cut"}


# A drawer's box sits 9.8 mm above its module's bottom (8.6 until the key lock was measured): only there do the
# key's cam lobes (45.0 mm tip to tip) fill the module's two front notches (5.8 and 50.8 mm up) when the key is
# locked, and the racks' tabs enter the module's side pockets (11.3-14.3 mm up; the tabs are 2.7 mm high). The same
# 1.2 mm puts the runner guides in the middle of the module's recesses (0.5 mm each side, they stuck 0.7 mm out),
# the stoppers in the middle of the module's side holes (28.3 mm up) and the facade flush with the module's front
# frame (4.8 and 51.8 mm up). Every drawer family has the same notches (kinematics.py, README "Motion").
MODULE_UNDER_BOX = 9.8
# Key lock (every drawer, manual "Drawer Assembly" 6/8: the key goes in "open"): the key is a 20-tooth pinion
# (4 mm pitch) between the two racks. Placed open (knob across, its dot at the facade's open padlock). Locked:
# a quarter turn anticlockwise seen from the front (dot at the tick above), each rack 20 mm out, the bottom one
# to the right, the top one to the left, their tabs in the module's side pockets, the cam's lobes in its notches.
KEY_UP = MODULE_UNDER_BOX + 18.5     # the key's axis above the module's bottom (unit y)
KEY_TURN = 90.0
RACK_TRAVEL = 20.0                   # 5 teeth: a quarter of 20 teeth of 4 mm


def key_lock(r, t, ux, up=0.0):
    """A drawer's key and racks as joints, in the unit frame (ux: the key's x; up: the drawer's height above the
    module's first level). Each joint goes from 0 (as placed, unlocked) to 1 (locked). A closed drawer is locked:
    opening turns the key back, then pulls the drawer."""
    r.joints[f"key{t}"] = {"turn": {"origin": [round(ux, 3), round(KEY_UP + up, 3), 0.0], "axis": [0, 0, 1], "deg": KEY_TURN}}
    r.joints[f"rack_lo{t}"] = {"slide": [RACK_TRAVEL, 0.0, 0.0]}
    r.joints[f"rack_hi{t}"] = {"slide": [-RACK_TRAVEL, 0.0, 0.0]}
    lock = [j for j in r.joints if j.startswith(("key", "rack_"))]
    r.steps = [{"joints": lock, "from": 1, "to": 0, "s": 0.35}, {"joints": ["drawer"], "from": 0, "to": 1, "s": 0.55}]


def find(rel):
    """The download's own spelling of a path (the files mix 1F / 1f)."""
    return LOWER.get(_norm(rel))


def need(rel):
    f = find(rel)
    if not f:
        raise KeyError(rel)
    return f


def bbox(rel):
    return IDX.bbox(rel)


def rot_of(rel):
    """Best orientation found for a file (lowest score over the references tried)."""
    c = [v for v in ORIENT.values() if v["target"] == rel]
    if not c:
        raise KeyError("no orientation for " + rel)
    return min(c, key=lambda v: v["score"])["rot"]


def rot_checked(rel, check, what):
    """The best-scoring orientation that passes `check(rot)` (e.g. latch frames underneath, at the
    back). orient.py keeps its six best answers; a part turned upside down or back to front fails."""
    c = [v for v in ORIENT.values() if v["target"] == rel]
    if not c:
        raise KeyError("no orientation for " + rel)
    best = min(c, key=lambda v: v["score"])
    for rot, sc in best.get("alts", [[best["rot"], best["score"]]]):
        if check(rot):
            return rot, (None if rot == best["rot"] else f"{what}: orientation #2+ chosen ({rot}, score {sc}) because the best one failed the check")
    return best["rot"], f"{what}: no orientation passed the check, kept the best score (DOUBTFUL)"


def frames_at_back(rel, depth):
    """Check for a module or roof: latch frame(s) under it, their back edge 12 mm from the back.
    (The back edge: on some roofs the rim joins another relief at the front of the frame.)"""
    def ok(rot):
        fr = frames_of(feat("under", rel, rot))
        return bool(fr) and all(abs(f["w_rng"][0] + depth - 12.0) < 2.0 for f in fr)
    return ok


def extents(rel, rot):
    """Size (CAD x, y, z) of a part turned by `rot`, from its real vertices."""
    key = f"ext|{rel}|{rot}"
    if key not in FEAT:
        P = vg.read_stl(os.path.join(F.ROOT, rel)).reshape(-1, 3) @ vg.from_euler_xyz(rot).T
        FEAT[key] = [round(float(v), 3) for v in P.max(0) - P.min(0)]
        json.dump(FEAT, open(FEAT_PATH, "w", encoding="utf-8"), ensure_ascii=False)
    return FEAT[key]


def feat(kind, rel, rot):
    key = f"{kind}|{rel}|{rot}"
    if key not in FEAT:
        FEAT[key] = getattr(F, kind)(rel, rot)
        json.dump(FEAT, open(FEAT_PATH, "w", encoding="utf-8"), ensure_ascii=False)
    return FEAT[key]


class Recipe:
    def __init__(self, name, key):
        self.name, self.key, self.parts, self.notes, self.hinge = name, key, [], [], None
        self.joints, self.steps = {}, None
        self.layout, self.tags = None, None   # a layout recipe: its id and drawers; tags put on the parts made now

    def part(self, nm, file, role, group, rot=None, align=None, move=None, pick=None, joint=None, ref=False):
        d = {"name": f"{self.name}_{nm}", "file": file, "role": role, "group": group}
        if ref:
            d["ref"] = True
        if joint:
            d["joint"] = joint
        if self.tags:
            d["tags"] = dict(self.tags)
        if rot and any(rot):
            d["rot"] = rot
        if align:
            d["align"] = {k: [m, round(v, 3)] for k, (m, v) in align.items()}
        if move:
            d["move"] = move
        if pick is not None:
            d["pick"] = [round(float(v), 3) for v in pick]
        self.parts.append(d)

    def placed(self, nm, file, role, group, R_unit, src, dst, piece=None, origin=(0.0, 0.0, 0.0), joint=None, ref=False):
        """A part (or one piece of its file) turned by R_unit (file axes -> unit axes) with the file
        point `src` on the unit point `dst`. origin: the unit frame's origin in recipe (CAD) coordinates.
        Written as the recipe's rot + align (by the real vertices' bbox, as blender_assemble.py does)."""
        R_unit = np.asarray(R_unit, float)
        T = piece["tris"] if piece else vg.read_stl(os.path.join(F.ROOT, file))
        P = (T.reshape(-1, 3) - np.asarray(src)) @ R_unit.T + np.asarray(dst)
        P = P @ vg.C.T + np.asarray(origin)          # unit -> CAD (C is its own inverse)
        lo = P.min(0)
        self.part(nm, file, role, group, vg.euler_xyz(vg.C @ R_unit), {a: ["min", float(lo[i])] for i, a in enumerate("xyz")},
                  pick=piece["centre"] if piece else None, joint=joint, ref=ref)

    def json(self, anchor="Module"):
        out = {"name": self.name, "key": self.key, "notes": self.notes, "parts": self.parts,
               "finalize": {"anchor": f"{self.name}_{anchor}"}}
        if self.hinge:
            out["hinge"] = self.hinge
        if self.joints:
            out["motion"] = {"joints": self.joints, "open": self.steps}
        if self.layout:
            out["layout"] = self.layout
        if getattr(self, "floor", None):
            out["floor"] = self.floor
        return out


_PIECES = {}


def file_pieces(rel):
    """Connected pieces of a file (vault_geom.pieces), from the decimated copy (same pieces, same
    coordinates): [{"tris", "centre", "min", "max"}], largest first."""
    if rel not in _PIECES:
        out = []
        for t in vg.pieces(vg.read_stl(os.path.join(F.ROOT, rel))):
            P = t.reshape(-1, 3)
            out.append({"tris": t, "centre": vg.piece_centre(t), "min": P.min(0), "max": P.max(0)})
        _PIECES[rel] = out
    return _PIECES[rel]


# Geared rails: each file holds the drawer's two racks, printed side by side. They run in two channels
# inside the box's hollow front wall (both 5.2 mm high, 4.4 mm deep, centred 3.1 mm behind the box's front
# face, 3.2 on XL boxes): the bottom rack in y 10.2-15.4 (unit frame: box bottom at 8.6), teeth up, from
# the channel's closed end left of the key towards the box's right side; the top rack in y 38.8-44.0,
# teeth down, from the closed end right of the key towards the left side. The key's pinion sits between
# them. The top rack is the one with a 1.4 mm fin along its back edge, which runs in a groove of the top
# channel. Racks are set retracted (rounded end against the channel's closed end: unlocked). Closed ends
# (bottom, top), unit x from the drawer's centre, measured on S3, S5 2F, M3, M6 4F, L3, L7 2F, XL3, XL5,
# XL7 and the L2/XL2 boxes (the same on every depth and height):
RAIL_END = {"S": (-65.87, 66.21), "M": (-65.87, 66.57), "L": (-66.77, 66.57), "XL": (-66.77, 66.57)}


def rails(r, w, cx, yf, zb, t="", depth=3.10):
    """Both racks of a drawer, retracted (unlocked); joints rack_lo / rack_hi (+ tag) slide them out to lock."""
    rel = need(U + f"Geared Rails/{w} Rails.stl")
    ps = file_pieces(rel)
    top = max(ps, key=lambda p: p["max"][1] - p["min"][1])   # the fin makes it wider
    bot = next(p for p in ps if p is not top)
    eb, et = RAIL_END[w]
    # bottom rack: file axes = unit axes (teeth up, rounded end at file x min); top rack: turned 180 deg about z
    r.part(f"Rail_bottom{t}", rel, "accent", "drawer", vg.euler_xyz(vg.C),
           {"x": ["max", cx - eb], "y": ["center", yf - depth], "z": ["center", zb + 4.21]}, pick=bot["centre"], joint=f"rack_lo{t}")
    r.part(f"Rail_top{t}", rel, "accent", "drawer", vg.euler_xyz(vg.C @ np.diag([-1.0, -1.0, 1.0])),
           {"x": ["min", cx - et], "y": ["center", yf - depth], "z": ["min", zb + 30.39]}, pick=top["centre"], joint=f"rack_hi{t}")


def hidden_key(r, cx, yf, z0, t=""):
    """The hidden key (lock option 'hidden', "flush"): the key lock without its knob. Same gear, same text,
    printed the same way, so it takes the key's place with the key's turn: its back (the gear) where the key's
    back is, its front flush with the facade's front. Part 2 is the removable key: two half-disc tongues that
    go into the two half-round pockets in the hidden key's front, either side of its bar, and a grip. Shown
    inserted: turned about its axis so its tongues straddle the bar, its tongue root on the hidden key's front.
    A unit's part list has either these two files or the key and its cap, so the page draws one lock only."""
    hk = U + "Hidden Key (Turn On Supports).stl"
    rot = [-90, 0, 0]
    r.part(f"HiddenKey{t}", hk, "mech", "drawer", rot, {"x": ["center", cx], "y": ["min", yf - 8.55], "z": ["center", z0]}, joint=f"key{t}")
    # the same pose by numbers, to carry part 2 along with it
    R = vg.from_euler_xyz(rot)
    H = vg.read_stl(os.path.join(F.ROOT, hk)).reshape(-1, 3)
    Hp = H @ R.T
    lo, hi = Hp.min(0), Hp.max(0)
    th = np.array([cx - (lo[0] + hi[0]) / 2, yf - 8.55 - lo[1], z0 - (lo[2] + hi[2]) / 2])
    hc = np.array([(H[:, 0].min() + H[:, 0].max()) / 2, (H[:, 1].min() + H[:, 1].max()) / 2, H[:, 2].max()])  # front centre
    p2 = U + "Hidden Key Part 2 (Turn on Supports).stl"
    P2 = vg.read_stl(os.path.join(F.ROOT, p2)).reshape(-1, 3)
    c2 = np.array([(P2[:, 0].min() + P2[:, 0].max()) / 2, (P2[:, 1].min() + P2[:, 1].max()) / 2, 0.0])   # tongue root plane z = 0
    # tongues: the two sectors below the root; turn them so they centre on +-90 deg (the pockets, above and below the bar)
    q = P2[(P2[:, 2] < -2) & (P2[:, 2] > -6.5)] - c2
    q = q[np.hypot(q[:, 0], q[:, 1]) > 10]
    a = np.arctan2(q[:, 1], q[:, 0])
    mid = np.degrees(np.arctan2(np.sin(2 * a).mean(), np.cos(2 * a).mean()) / 2)   # the sectors' axis (they are opposite)
    spin = (90 - mid + 90) % 180 - 90
    Rz = vg.rot_axis("z", spin)
    P2p = ((P2 - c2) @ Rz.T + hc) @ R.T + th
    lo2 = P2p.min(0)
    r.part(f"HiddenKey2{t}", p2, "mech", "drawer", vg.euler_xyz(R @ Rz), {k: ["min", float(lo2[i])] for i, k in enumerate("xyz")}, joint=f"key{t}")


def slide_front(rel):
    """XL runner slides are wedges (the XL box's sides narrow towards the back: 0.035 mm/mm on XL3,
    0.038 on XL7, and each slide tapers the same): the slide's thickness at its front end (file y max),
    from a line fitted to its sloped face over the front 30 mm."""
    key = f"slidefront|{rel}"
    if key not in FEAT:
        V = vg.read_stl(os.path.join(F.ROOT, rel)).reshape(-1, 3)
        y1 = V[:, 1].max()
        ys = np.arange(y1 - 30, y1 - 2, 1.0)
        zt = np.array([V[np.abs(V[:, 1] - y) < 0.5][:, 2].max() for y in ys])
        a, b = np.polyfit(ys, zt, 1)
        FEAT[key] = round(float(a * y1 + b - V[:, 2].min()), 3)
        json.dump(FEAT, open(FEAT_PATH, "w", encoding="utf-8"), ensure_ascii=False)
    return FEAT[key]


def insert_sml(r, w, d, h, box, cx, yf, zb, mod_rot, mod_file, tag="", box_rel=None, ux=0.0, up=0.0, module_parts=True):
    """Box, facade, lock, runners, stoppers, latches, caps and label of one S/M/L drawer, relative to
    its box (cx, yf, zb). mod_file/mod_rot: the module whose holes and frames we read.
    up: the box's height above the module's first level (48 mm a level, LEVEL_PITCH), already in zb; the key's
    joint needs it in the unit frame. module_parts=False leaves out the runner guides and stoppers (a layout
    recipe places the shell's own, on every level)."""
    W = WIDTH[w]
    bmn, bmx = bbox(box)
    mxmin, mxmax = cx - W / 2, cx + W / 2
    n = h
    fam = D + FAM[w] + "/"
    t = tag
    # box: in place in x/y; z set so the box bottom is at zb
    r.part(f"Box{t}", box, "drawer", "drawer", None, {"x": ["center", cx], "y": ["max", yf], "z": ["min", zb]})
    # baseplates: one plain file (sitting in the 1F box in the CAD file) and two with handle cut-outs
    b1mn, _ = bbox(need(fam + f"{w}{d}/Boxes/{w}{d} Box 1F.stl"))
    for bp in sorted(k for k in IDX.rows if k.startswith(fam + f"{w}{d}/Gridfinity Baseplate/")):
        pmn, _ = bbox(bp)
        nm = "Baseplate" + ("_H" + re.search(r"With (\d)", bp).group(1) if "With" in bp else "")
        # (a layout puts a box of another height at the shell box's front yf: M3's 2F and 4F boxes are 0.5 mm
        # further forward in the CAD file than its 1F box, so keep the baseplate where it is in its own box)
        dyb = yf - bmx[1] if r.layout else 0.0
        r.part(f"{nm}{t}", bp, "insert", "drawer", None,
               {"x": ["center", cx], "y": ["min", bmn[1] + dyb + (pmn[1] - b1mn[1])], "z": ["min", zb + pmn[2] - 5.0]})
    fac = need(fam + f"Facades/{w}{h}F (Turn On Supports).stl")
    r.part(f"Facade{t}", fac, "facade", "drawer", [-90, 0, 0], {"x": ["center", cx], "y": ["min", yf], "z": ["min", zb - 5]})
    z0 = zb + 18.5
    r.part(f"Key{t}", U + "Key (Turn On Supports).stl", "mech", "drawer", [-90, 0, 0],
           {"x": ["center", cx], "y": ["center", yf + 8.16], "z": ["center", z0]}, joint=f"key{t}")
    r.part(f"KeyCap{t}", U + "Key Cap.stl", "facade", "drawer", [90, 0, 0],
           {"x": ["center", cx], "y": ["center", yf + 25.16], "z": ["center", z0]}, joint=f"key{t}")
    key_lock(r, t, ux, up)
    hidden_key(r, cx, yf, z0, t)
    rails(r, w, cx, yf, zb, t)
    side = feat("side", mod_file, mod_rot)
    holes = [hh for hh in side["holes"] if 20 < hh["u"] < 36 and hh["area"] < 200]
    if not holes:
        raise RuntimeError("no stopper hole found in " + mod_file)
    hole_w = min(holes, key=lambda hh: abs(hh["u"] - 28.26))["w"]
    runner = U + f"Runners/x{d} Runner "
    bw = bmx[0] - bmn[0]   # box width: the slides sit in its side grooves
    for k in range(n):
        z = z0 + 48 * k
        r.part(f"Slide_L{k+1}{t}", runner + "Slide.stl", "mech", "drawer", [0, 90, 0], {"x": ["max", cx - bw / 2 + 2.2], "y": ["max", yf], "z": ["center", z]})
        r.part(f"Slide_R{k+1}{t}", runner + "Slide.stl", "mech", "drawer", [0, -90, 0], {"x": ["min", cx + bw / 2 - 2.2], "y": ["max", yf], "z": ["center", z]})
        if not module_parts:
            continue
        r.part(f"Guide_L{k+1}{t}", runner + "Guide.stl", "body", "module", [0, 90, 0], {"x": ["min", mxmin + 3.58], "y": ["max", yf], "z": ["center", z]})
        r.part(f"Guide_R{k+1}{t}", runner + "Guide.stl", "body", "module", [0, -90, 0], {"x": ["max", mxmax - 3.58], "y": ["max", yf], "z": ["center", z]})
        ys = yf + 0.06 + hole_w - 0.29
        r.part(f"Stopper_R{k+1}{t}", U + "Runners/Runner Stopper.stl", "accent", "module", None, {"x": ["max", mxmax - 0.16], "y": ["center", ys], "z": ["center", z]})
        r.part(f"Stopper_L{k+1}{t}", U + "Runners/Runner Stopper.stl", "accent", "module", [0, 0, 180], {"x": ["min", mxmin + 0.16], "y": ["center", ys], "z": ["center", z]})
    # label at the facade's left end (seen from the front), over the left bolt
    lx = mxmax - LABEL_IN[w]
    r.part(f"Label{t}", U + "Label.stl", "insert", "drawer", [-90, 0, 0], {"x": ["min", lx], "y": ["min", yf + 7.91], "z": ["center", z0]})
    ff = feat("facade", fac, [-90, 0, 0])
    caps = [c for c in ff["counterbores"]]
    under_label = min((c for c in caps if c[1] < 35), key=lambda c: c[0])  # leftmost of the bottom row
    caps = [c for c in caps if c is not under_label]
    for i, (u, wv) in enumerate(caps):
        r.part(f"FacadeCap_{i+1}{t}", U + "Facade Cap.stl", "facade", "drawer", [-90, 0, 0],
               {"x": ["center", cx - u], "y": ["min", yf + 5.92], "z": ["center", zb - 5 + wv]})
    return hole_w


FRAME_LEN = 53.5  # latch frame, back edge to front edge (S3, L7)


def frames_of(fe):
    """Latch frames among the reliefs under a module: about 87 mm across, 53.5 mm long (on roofs
    the rim runs into the next relief, so allow it longer)."""
    def su(f):
        return f["u_rng"][1] - f["u_rng"][0]
    def sw(f):
        return f["w_rng"][1] - f["w_rng"][0]
    return [f for f in fe["frames"] + fe["others"] if 80 < su(f) < 95 and 35 < sw(f)]


def latches(r, mod_file, mod_rot, cx, yf, zb, tag="", depth=None, below=8.6):
    """One latch per frame under the module, whose bottom is `below` under zb."""
    fr = [f for f in frames_of(feat("under", mod_file, mod_rot)) if depth is None or abs(f["w_rng"][0] + depth - 12.0) < 2.0]
    for i, f in enumerate(sorted(fr, key=lambda f: f["u"])):
        u = (f["u_rng"][0] + f["u_rng"][1]) / 2
        r.part(f"Latch_{i+1}{tag}", U + "Latch.stl", "accent", "module", None,
               {"x": ["center", cx - u], "y": ["max", yf + 0.06 + f["w_rng"][0] + FRAME_LEN - 1.94], "z": ["min", zb - below + 0.3]})
    return len(fr)


def drawer_sml(w, d, h):
    fam = D + FAM[w] + f"/{w}{d}/"
    box = need(fam + f"Boxes/{w}{d} Box {h}F.stl")
    bmn, bmx = bbox(box)
    cx, yf, zb = round((bmn[0] + bmx[0]) / 2, 3), bmx[1], 5.0
    mod = need(fam + f"Modules/{w}{d} Module {h}F.stl")
    r = Recipe(f"{w}{d}_{h}F", f"drawer|{w}|{d}|{h}")
    mrot, why = rot_checked(mod, frames_at_back(mod, 146.1 + 42 * (d - 3)), "module")
    if why:
        r.notes.append(why)
    r.part("Module", mod, "body", "module", mrot, {"x": ["center", cx], "y": ["max", yf + 0.06], "z": ["min", zb - MODULE_UNDER_BOX]})
    insert_sml(r, w, d, h, box, cx, yf, zb, mrot, mod)
    nl = latches(r, mod, mrot, cx, yf, zb, depth=146.1 + 42 * (d - 3), below=MODULE_UNDER_BOX)
    r.notes.append(f"{nl} latch frame(s) found under the module")
    return r.json()


def drawer_l2(d, h):
    """L²: an L-wide module holding two S drawers. Its section is two S modules side by side (a double
    wall in the middle, with stopper holes like the outer walls), so each S drawer goes in its half,
    set like in an S module whose centre is the L² module's centre -/+ 82.4."""
    fam = D + FAM["L2"] + f"/L{d}²/"
    mod = need(fam + f"L{d}² Module {h}F.stl")
    box = need(D + FAM["S"] + f"/S{d}/Boxes/S{d} Box {h}F.stl")
    bmn, bmx = bbox(box)
    cx, yf, zb = 0.0, bmx[1], 5.0
    r = Recipe(f"L2-{d}_{h}F", f"drawer|L2|{d}|{h}")
    mrot, why = rot_checked(mod, frames_at_back(mod, 146.1 + 42 * (d - 3)), "module")
    if why:
        r.notes.append(why)
    r.part("Module", mod, "body", "module", mrot, {"x": ["center", cx], "y": ["max", yf + 0.06], "z": ["min", zb - MODULE_UNDER_BOX]})
    for tag, dx in (("_left", 82.4), ("_right", -82.4)):   # CAD +x is the viewer's left
        insert_sml(r, "S", d, h, box, cx + dx, yf, zb, mrot, mod, tag, ux=-dx)
    nl = latches(r, mod, mrot, cx, yf, zb, depth=146.1 + 42 * (d - 3), below=MODULE_UNDER_BOX)
    r.notes.append(f"{nl} latch frame(s) found under the module")
    r.notes.append("L² accessories (x%d Accessory 1st/2nd) not placed: their place is not shown in the manual or the CAD file" % d)
    return r.json()


# Several drawers in one 2F or 4F module (Drawer Assembly 4/8; rules.js LAYOUTS): a 2F shell takes two 1F boxes,
# a 4F shell 2F + 2F, four 1F, or a 2F and two 1F in any order. Each box rides on the runners of the levels it
# spans and locks with its racks in the side pockets of its lowest level. measure_levels.py cut every 2F and 4F
# shell (S, M, L, L², all depths) through the racks' channels and slid the 1F shell's cut over each level: the
# pockets are at 48 k + 0.00 mm on every level of every shell (residual 6-29 mm² of section, 65-115 mm² a mm off).
# So a box on level k is placed as in its own 1F/2F module, 48 k mm higher. The shell's front frame is only at its
# bottom and top (4.8-7.8 mm and the top 3 mm): a key's cam finds its notches on the lowest and the top drawer only,
# the racks lock every drawer (the manual: use the geared rails with more than one box in a 2F/4F module).
LEVEL_PITCH = 48.0
LAYOUTS = {2: [[1, 1]], 4: [[2, 2], [1, 1, 1, 1], [2, 1, 1], [1, 2, 1], [1, 1, 2]]}   # heights, top to bottom


def layout_insert(r, w, d, h, lay, cx, yf, zb, mrot, mod, sides=(("", 0.0),)):
    """The drawers of a layout (heights top to bottom) in a shell of height h; sides: (tag, dx) per column of
    drawers (one, or the two halves of an L²). Sets r.layout: per drawer its index (top to bottom), side,
    height, lowest level and opening steps (its own key and racks, then its slide)."""
    fam = D + FAM[w] + f"/{w}{d}/"
    drawers = []
    for side, dx in sides:
        level = h
        for i, dh in enumerate(lay):
            level -= dh
            up = LEVEL_PITCH * level
            t = f"{side}_d{i}"
            r.tags = {"drawer": i, **({"side": side.strip("_")} if side else {})}
            insert_sml(r, w, d, dh, need(fam + f"Boxes/{w}{d} Box {dh}F.stl"), cx + dx, yf, zb + up, mrot, mod, t,
                       ux=-dx, up=up, module_parts=False)
            r.tags = None
            drawers.append({"drawer": i, **({"side": side.strip("_")} if side else {}), "h": dh, "level": level,
                            "open": [{"joints": [f"key{t}", f"rack_lo{t}", f"rack_hi{t}"], "from": 1, "to": 0, "s": 0.35},
                                     {"joints": ["drawer"], "from": 0, "to": 1, "s": 0.55}]})
    if level != 0:
        raise ValueError(f"layout {lay} doesn't fill a {h}F shell")
    r.steps = None
    r.layout = {"id": ",".join(map(str, lay)), "drawers": drawers}


def shell_runners(r, w, d, h, box, cx, yf, zb, mrot, mod, sides=(("", 0.0),)):
    """The shell's own runner guides and stoppers (every level), as its single-drawer recipe has them."""
    keep = len(r.parts)
    for side, dx in sides:
        insert_sml(r, w, d, h, box, cx + dx, yf, zb, mrot, mod, side, ux=-dx)
    mine = r.parts[keep:]
    r.parts[keep:] = [p for p in mine if re.search(r"_(Guide|Stopper)_", p["name"])]
    r.joints, r.steps = {}, None


def layout_sml(w, d, h, lay):
    fam = D + FAM[w] + f"/{w}{d}/"
    box = need(fam + f"Boxes/{w}{d} Box {h}F.stl")
    bmn, bmx = bbox(box)
    cx, yf, zb = round((bmn[0] + bmx[0]) / 2, 3), bmx[1], 5.0
    mod = need(fam + f"Modules/{w}{d} Module {h}F.stl")
    r = Recipe(f"{w}{d}_{h}F_lay{''.join(map(str, lay))}", f"drawer|{w}|{d}|{h}")
    mrot, why = rot_checked(mod, frames_at_back(mod, 146.1 + 42 * (d - 3)), "module")
    if why:
        r.notes.append(why)
    r.part("Module", mod, "body", "module", mrot, {"x": ["center", cx], "y": ["max", yf + 0.06], "z": ["min", zb - MODULE_UNDER_BOX]})
    shell_runners(r, w, d, h, box, cx, yf, zb, mrot, mod)
    r.layout = True      # (insert_sml reads it)
    layout_insert(r, w, d, h, lay, cx, yf, zb, mrot, mod)
    nl = latches(r, mod, mrot, cx, yf, zb, depth=146.1 + 42 * (d - 3), below=MODULE_UNDER_BOX)
    r.notes.append(f"layout {lay} (top to bottom), {nl} latch frame(s); levels 48 mm apart (measure_levels.py)")
    return r.json()


def layout_l2(d, h, lay):
    fam = D + FAM["L2"] + f"/L{d}²/"
    mod = need(fam + f"L{d}² Module {h}F.stl")
    box = need(D + FAM["S"] + f"/S{d}/Boxes/S{d} Box {h}F.stl")
    bmn, bmx = bbox(box)
    cx, yf, zb = 0.0, bmx[1], 5.0
    r = Recipe(f"L2-{d}_{h}F_lay{''.join(map(str, lay))}", f"drawer|L2|{d}|{h}")
    mrot, why = rot_checked(mod, frames_at_back(mod, 146.1 + 42 * (d - 3)), "module")
    if why:
        r.notes.append(why)
    r.part("Module", mod, "body", "module", mrot, {"x": ["center", cx], "y": ["max", yf + 0.06], "z": ["min", zb - MODULE_UNDER_BOX]})
    sides = (("_left", 82.4), ("_right", -82.4))   # CAD +x is the viewer's left
    shell_runners(r, "S", d, h, box, cx, yf, zb, mrot, mod, sides)
    r.layout = True
    layout_insert(r, "S", d, h, lay, cx, yf, zb, mrot, mod, sides)
    nl = latches(r, mod, mrot, cx, yf, zb, depth=146.1 + 42 * (d - 3), below=MODULE_UNDER_BOX)
    r.notes.append(f"layout {lay} (top to bottom) on both sides, {nl} latch frame(s); levels 48 mm apart (measure_levels.py)")
    return r.json()


def family_layouts():
    out = []
    for w in ("S", "M", "L", "L2"):
        for d in range(3, 8):
            for h, lays in LAYOUTS.items():
                for lay in lays:
                    out.append(layout_l2(d, h, lay) if w == "L2" else layout_sml(w, d, h, lay))
    return out


# A tower's base, wheels and foot: measure_stack.py measures them on the files and writes their matrices (unit frame
# of the tower's first module) to $VAULT_ASSEMBLY/_stack.json; the recipe places them by those matrices, with the
# first module (1F, as in its own entry) as the frame's reference, assembled but not exported.
STACK_JSON = os.path.join(ASM, "_stack.json")


def stack_unit(w, d):
    st = json.load(open(STACK_JSON, encoding="utf-8"))[f"stack|{w}|{d}"]
    pl = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src", "stl-placements.json"), encoding="utf-8"))
    r = Recipe(f"{w}{d}_Stack", f"stack|{w}|{d}")
    mod = next(p for p in pl["units"][f"drawer|{w}|{d}|1"]["parts"] if re.search(r"(?i)Module 1F\.stl$", p[0]))

    def put(nm, f, role, m, ref=False):
        M = np.array(m, float).reshape(3, 4)
        r.placed(nm, f, role, "module", M[:, :3], (0.0, 0.0, 0.0), M[:, 3], ref=ref)
    put("Module", mod[0], "body", mod[3], ref=True)
    put("Base", st["base"]["file"], "body", st["base"]["m"])
    for i, bp in enumerate(st["base_parts"], 1):
        put(f"BasePart_{i}", bp["file"], "body", bp["m"])
    for wp in st["wheels"]:
        put(f"Wheel_{wp['side']}_{os.path.splitext(os.path.basename(wp['file']))[0].split(' ')[0]}", wp["file"], wp["role"], wp["m"])
    put("Foot", st["foot"]["file"], st["foot"]["role"], st["foot"]["m"])
    wn, fn, fe = st["wheel_notes"], st["foot_notes"], st["features"]
    r.floor = {"base": fe["bottom"], "wheels": wn["wheel_bottom"], "foot": fn["foot_bottom"],
               "note": "y of the floor under the base alone, under the wheels (tire bottom) and under the foot, in the first module's frame"}
    r.notes.append("base: top on the module's underside, back flush, 10 mm proud at the front; rod at y %.1f z %.1f; "
                   "wheels %.2f mm clear of the base, rod %.1f mm beyond the bushings; foot on the base's M6 holes (%.2f mm), "
                   "its floor %.2f mm under the tires'" % (fe["rod"][0], fe["rod"][1], wn["clear_of_base"], wn["rod_beyond_bushing"],
                                                          fn["hole_error"], wn["wheel_bottom"] - fn["foot_bottom"]))
    return r.json("Module")


def roof_sml(w, d, kind, ref_mod=None):
    """Roofs are printed on edge at 45 deg, with a module's underside: placed like a module, with a
    latch in each of their own latch frames."""
    rel = find(D + FAM[w] + f"/{w}{d}/Roofs/{w}{d} {ROOFS[kind]}.stl")
    if not rel:
        return None
    cx, yf, zb = 0.0, 0.0, 5.0   # any frame works: the root is recentred
    r = Recipe(f"{w}{d}_Roof_{kind}", f"roof|{w}|{d}|{kind}")
    rr, why = rot_checked(rel, frames_at_back(rel, 146.1 + 42 * (d - 3)), "roof")
    if why:
        r.notes.append(why)
    r.part("Roof", rel, "roof", "module", rr, {"x": ["center", cx], "y": ["max", yf + 0.06], "z": ["min", zb - 8.6]})
    n = latches(r, rel, rr, cx, yf, zb, depth=146.1 + 42 * (d - 3))
    if not n and ref_mod:
        n = latches(r, ref_mod[0], ref_mod[1], cx, yf, zb, depth=146.1 + 42 * (d - 3))
        r.notes.append("no latch frame read under the roof: latches set from the module's frames")
    yc = yf + 0.06 - extents(rel, rr)[1] / 2
    if kind in ("heavy", "heavycut"):
        # A bar from one pocket of the middle slot's walls to the other: the pockets are 156 mm apart, the bar
        # 156.5 long. Its axis is 59.8 mm above the roof's bottom: the middle of the pockets, which run from 44.7 to
        # 74.9 mm on every heavyweight roof (sections at x = +-74 mm; manual p. 10). 45 mm put it a radius too low.
        r.part("Handle", U + "Heawyweight Roof Handle.stl", "roof", "module", [0, 0, 90],
               {"x": ["center", cx], "y": ["center", yc], "z": ["center", zb - 8.6 + 59.8]})
        # Each pocket has an entry groove (a wedge running back on the right, forward on the left) that an insert
        # closes once the bar is in. USSA's CAD scene has the insert against the bar's right end: that is the right
        # one (0.5 mm off the groove's back wall, its peg in the groove's hole); the left one is it turned half a
        # turn about the bar's vertical axis. Offsets are bounding-box centre to the bar's. Right and left are seen
        # from the front: the right one is at CAD -x (CAD +x is the viewer's left), behind the bar; the left one at
        # CAD +x, in front of it. (They were set the other way round, each in the solid wall on the other side of the
        # bar from its groove: hidden, the grooves left open. Sections at x = +-68 mm, roof|L|7|heavy.)
        for i, (sx, rz) in enumerate(((1, 90), (-1, 270)), 1):
            r.part(f"Insert_{i}", U + "Heawyweight Roof Insert.stl", "roof", "module", [0, 0, rz],
                   {"x": ["center", cx - sx * 68.414], "y": ["center", yc - sx * 27.056], "z": ["center", zb - 8.6 + 59.8 - 0.25]})
    if kind == "grid":
        top_handle(r, rel, rr, (cx, yf + 0.06, zb - 8.6))
    r.notes.append(f"{n} latch(es)")
    return {**r.json("Roof")}


# The grid roof's optional top handle (manual p. 18 "Required Hardware - Drawers"): a loop that stands on the grid,
# long side across, its hole running front to back. Its bottom has two notches that take the grid's two pegs at
# x = +-21, and two 6 mm channels that run up and out at 45 deg to its ends; each continues into a 45 deg hole
# through the grid under it, and an M6 x 50 countersunk bolt goes up from under the roof through both. (It was set
# lying flat, which hid all of this.) Measured on every grid roof: the holes are at x = +-22.4 in the middle of
# the roof's depth, except S3 and M3 (10 mm further back); the handle comes down onto the ribs, its pegs inside
# the notches, which leaves its channels 0.4 to 0.7 mm off the axes of the roof's holes (hardware.py measures it).
HANDLE = U + "Top Handle (Turn On Supports).stl"
HANDLE_ROT = [-180.0, 90.0, 0.0]   # CAD Euler of the file, standing


def grid_holes_z(t):
    """z (unit frame) of the middle of the two 45 deg bolt holes under a grid roof's top handle, from the posed
    roof's triangles: rays across each hole's axis (x + y = -13.86 on the left, mirrored on the right)."""
    import hw_geom as hg
    zs = []
    for side in (-1, 1):
        cen = t.mean(1)
        sub = t[(np.abs(cen[:, 0] - side * 22) < 14) & (cen[:, 1] < 17)]
        n = np.array([1, -side, 0.0]) / np.sqrt(2)
        for z in np.arange(t[..., 2].min() + 5, t[..., 2].max() - 5, 0.25):
            o = np.array([side * 22.43, 8.57, z]) - n * 15
            hs = [(s - 15, f) for s, f in hg.ray_hits(sub, o, n) if abs(s - 15) < 8]
            if any(a[1] > 0 and b[1] < 0 and a[0] < 0.5 and b[0] > -0.5 and 5 < b[0] - a[0] < 7 for a, b in zip(hs, hs[1:])):
                zs.append(z)
    if not zs:
        return None
    return float(np.mean(zs))


def _crop(t, lo, hi):
    c = t.mean(1)
    return t[np.all((c > np.asarray(lo) - 3) & (c < np.asarray(hi) + 3), axis=1)]


def top_handle(r, rel, rr, origin):
    """The handle's feet sit between two of the grid's cross ribs, which leaves it one depth only: it is put where it
    comes down furthest (searched 2.5 mm around the holes, 0.1 mm steps), then down onto the ribs."""
    key = f"handle3|{rel}|{rr}"
    if key not in FEAT:
        t = F.posed_fbc(rel, rr)                       # roof in the unit frame (front-bottom-centre at 0)
        hz = grid_holes_z(t)
        R = vg.C @ vg.from_euler_xyz(HANDLE_ROT)
        h = vg.read_stl(os.path.join(F.ROOT, HANDLE))
        P = h.reshape(-1, 3)
        c = (P.min(0) + P.max(0)) / 2
        q = (h - c) @ R.T
        Q = q.reshape(-1, 3)
        y0 = t[..., 1].max() - Q[:, 1].min()           # handle bottom level with the roof's highest point
        z0 = hz if hz is not None else (t[..., 2].min() + t[..., 2].max()) / 2
        st, ext = 0.1, 2.5
        hlo, hhi = Q.min(0), Q.max(0)
        qb = _crop(q, [hlo[0], hlo[1], hlo[2]], [hhi[0], hlo[1] + 8, hhi[2]])
        Dh = vg.depthmap(qb, 1, -1, st, [hlo[0], hlo[1], hlo[2]], [hhi[0], hlo[1] + 8, hhi[2]])[0] + y0
        rlo = [hlo[0], -5, z0 + hlo[2] - ext]
        rhi = [hhi[0], t[..., 1].max() + 1, z0 + hhi[2] + ext]
        Dr = vg.depthmap(_crop(t, rlo, rhi), 1, +1, st, rlo, rhi)[0]
        nz, nx = Dh.shape
        best = None
        for k in range(Dr.shape[0] - nz + 1):
            g = Dh - Dr[k:k + nz, :nx]
            if np.isnan(g).all():
                continue
            dmin = float(np.nanmin(g))
            if best is None or dmin > best[0] + 1e-9:
                best = (dmin, [k])
            elif abs(dmin - best[0]) < 0.02:
                best[1].append(k)
        drop, ks = best
        zc = float(z0 - ext + st * np.mean(ks))
        FEAT[key] = {"holes_z": hz, "centre": [0.0, float(y0 - drop), zc], "drop": round(drop, 3), "src": [float(v) for v in c]}
        json.dump(FEAT, open(FEAT_PATH, "w", encoding="utf-8"), ensure_ascii=False)
    f = FEAT[key]
    if f["holes_z"] is None:
        r.notes.append("top handle: no bolt holes found in the grid")
    r.placed("TopHandle", HANDLE, "roof", "module", vg.C @ vg.from_euler_xyz(HANDLE_ROT), f["src"], f["centre"], origin=origin)
    r.notes.append(f"top handle standing between the cross ribs at z {f['centre'][2]:.2f} (grid holes at "
                   f"{f['holes_z'] and round(f['holes_z'], 2)}), {f['drop']:.2f} mm down onto the ribs")


def drawer_xl2(d):
    """XL²: an XL-wide 1F module holding an S drawer (viewer's left) and an M drawer (right), split by
    a double wall at x = -44.6 mm (unit frame), measured on a section of the XL3² module."""
    fam = D + FAM["XL2"] + f"/XL{d}²/"
    mod = need(fam + f"XL{d}² Module 1F.stl")
    r = Recipe(f"XL2-{d}_1F", f"drawer|XL2|{d}|1")
    depth = 146.1 + 42 * (d - 3)
    mrot, why = rot_checked(mod, frames_at_back(mod, depth), "module")
    if why:
        r.notes.append(why)
    cx, zb = 0.0, 5.0
    sbox = need(D + FAM["S"] + f"/S{d}/Boxes/S{d} Box 1F.stl")
    yf = bbox(sbox)[1][1]
    r.part("Module", mod, "body", "module", mrot, {"x": ["center", cx], "y": ["max", yf + 0.06], "z": ["min", zb - MODULE_UNDER_BOX]})
    insert_sml(r, "S", d, 1, sbox, cx + 127.0, yf, zb, mrot, mod, "_S", ux=-127.0)   # CAD +x is the viewer's left
    mbox = need(D + FAM["M"] + f"/M{d}/Boxes/M{d} Box 1F.stl")
    insert_sml(r, "M", d, 1, mbox, cx - 82.4, yf, zb, mrot, mod, "_M", ux=82.4)
    nl = latches(r, mod, mrot, cx, yf, zb, depth=depth, below=MODULE_UNDER_BOX)
    r.notes.append(f"{nl} latch frame(s) found under the module")
    return r.json()


def openings_of(rel):
    key = f"openings|{rel}"
    if key not in FEAT:
        FEAT[key] = F.openings(rel, 37.5)
        json.dump(FEAT, open(FEAT_PATH, "w", encoding="utf-8"), ensure_ascii=False)
    return FEAT[key]


def tray_rot(rel, want):
    """Pose of a box part: open on top, and open or closed at the back and front as `want` says."""
    for c in openings_of(rel):
        if c["top"] > 20 and all((c[k] > 20) == v for k, v in want.items()):
            return c["rot"]
    raise RuntimeError(f"no pose of {rel} matches {want}")


def drawer_xl(d):
    """XL (1F only): its own box (open at the back and closed by a back panel up to XL5, in two halves
    for XL6/XL7), XL runners and an XL facade; otherwise set like S/M/L."""
    fam = D + FAM["XL"] + f"/XL{d}/"
    mod = need(fam + f"Modules/XL{d} Module 1F.stl")
    r = Recipe(f"XL{d}_1F", f"drawer|XL|{d}|1")
    depth, bdepth = 146.1 + 42 * (d - 3), 143.8 + 42 * (d - 3)
    mrot, why = rot_checked(mod, frames_at_back(mod, depth), "module")
    if why:
        r.notes.append(why)
    cx, yf, zb = 0.0, 0.0, 5.0
    W, BW = WIDTH["XL"], 377.7
    mxmin, mxmax = cx - W / 2, cx + W / 2
    r.part("Module", mod, "body", "module", mrot, {"x": ["center", cx], "y": ["max", yf + 0.06], "z": ["min", zb - MODULE_UNDER_BOX]})
    if d <= 5:
        box = need(fam + f"Boxes/XL{d} Box 1F.stl")
        r.part("Box", box, "drawer", "drawer", tray_rot(box, {"back": True, "front": False}),
               {"x": ["center", cx], "y": ["max", yf], "z": ["min", zb]})
        pan = need(fam + f"Boxes/XL{d} Back Panel.stl")
        pc = [c for c in openings_of(pan) if c["front"] >= c["back"]]
        r.part("BackPanel", pan, "drawer", "drawer", pc[0]["rot"], {"x": ["center", cx], "y": ["min", yf - bdepth], "z": ["min", zb]})
        r.notes.append("back panel: set flush in the box's open back; which face goes inside is a guess (its 1.3 mm relief inwards)")
    else:
        p1 = need(fam + f"Boxes/XL{d} Box 1F Part 1.stl")
        p2 = need(fam + f"Boxes/XL{d} Box 1F Part 2.stl")
        r.part("Box", p1, "drawer", "drawer", tray_rot(p1, {"back": True, "front": False}),
               {"x": ["center", cx], "y": ["max", yf], "z": ["min", zb]})
        r.part("Box2", p2, "drawer", "drawer", tray_rot(p2, {"back": False, "front": True}),
               {"x": ["center", cx], "y": ["min", yf - bdepth], "z": ["min", zb]})
        r.notes.append("box halves: front half from the front, back half to the full box depth (they overlap at the joint)")
    fac = need(D + FAM["XL"] + "/XL Facade 1F.stl")
    r.part("Facade", fac, "facade", "drawer", [-90, 0, 0], {"x": ["center", cx], "y": ["min", yf], "z": ["min", zb - 5]})
    z0 = zb + 18.5
    r.part("Key", U + "Key (Turn On Supports).stl", "mech", "drawer", [-90, 0, 0], {"x": ["center", cx], "y": ["center", yf + 8.16], "z": ["center", z0]}, joint="key")
    r.part("KeyCap", U + "Key Cap.stl", "facade", "drawer", [90, 0, 0], {"x": ["center", cx], "y": ["center", yf + 25.16], "z": ["center", z0]}, joint="key")
    hidden_key(r, cx, yf, z0)
    key_lock(r, "", 0.0)
    rails(r, "XL", cx, yf, zb, depth=3.20)
    side = feat("side", mod, mrot)
    holes = [hh for hh in side["holes"] if 20 < hh["u"] < 36 and hh["area"] < 200]
    if holes:
        hole_w = min(holes, key=lambda hh: abs(hh["u"] - 28.26))["w"]
    else:
        hole_w = -(44.56 + 21 * (d - 3))
        r.notes.append("no stopper hole read in the XL module wall: stopper set by the S/M/L depth rule")
    rn = U + f"Runners/XL Runners/x{d} Runner "
    # the wedge's sloped face lies along the box's tapered side, in its groove (2.2 mm in from the box's
    # face at the front, as on S/M/L); its flat face runs along the guide
    tf = slide_front(need(rn + "Slide XL.stl"))
    r.part("Slide_L", rn + "Slide XL.stl", "mech", "drawer", [0, 90, 0], {"x": ["min", cx - BW / 2 + 2.2 - tf], "y": ["max", yf], "z": ["center", z0]})
    r.part("Slide_R", rn + "Slide XL.stl", "mech", "drawer", [0, -90, 0], {"x": ["max", cx + BW / 2 - 2.2 + tf], "y": ["max", yf], "z": ["center", z0]})
    r.part("Guide_L", rn + "Guide XL.stl", "body", "module", [0, 90, 0], {"x": ["min", mxmin + 3.58], "y": ["max", yf], "z": ["center", z0]})
    r.part("Guide_R", rn + "Guide XL.stl", "body", "module", [0, -90, 0], {"x": ["max", mxmax - 3.58], "y": ["max", yf], "z": ["center", z0]})
    ys = yf + 0.06 + hole_w - 0.29
    r.part("Stopper_R", U + "Runners/Runner Stopper.stl", "accent", "module", None, {"x": ["max", mxmax - 0.16], "y": ["center", ys], "z": ["center", z0]})
    r.part("Stopper_L", U + "Runners/Runner Stopper.stl", "accent", "module", [0, 0, 180], {"x": ["min", mxmin + 0.16], "y": ["center", ys], "z": ["center", z0]})
    r.part("Label", U + "Label.stl", "insert", "drawer", [-90, 0, 0], {"x": ["min", mxmax - 49.7], "y": ["min", yf + 7.91], "z": ["center", z0]})
    ff = feat("facade", fac, [-90, 0, 0])
    caps = ff["counterbores"]
    under_label = min((c for c in caps if c[1] < 35), key=lambda c: c[0])
    for i, (u, wv) in enumerate(c for c in caps if c is not under_label):
        r.part(f"FacadeCap_{i+1}", U + "Facade Cap.stl", "facade", "drawer", [-90, 0, 0],
               {"x": ["center", cx - u], "y": ["min", yf + 5.92], "z": ["center", zb - 5 + wv]})
    nl = latches(r, mod, mrot, cx, yf, zb, depth=depth, below=MODULE_UNDER_BOX)
    r.notes.append(f"{nl} latch frame(s) found under the module")
    return r.json()


SU = "02. SUSTAINERS/"
SUU = SU + "05. Universal/"
CFAM = {"S": "01. S Families", "M": "02. M Families", "L": "03. L Families", "XL": "04. XL Families"}
CASE_H = {1: 50.8, 2: 84.8, 4: 180.8}   # case body height (the sealed L/XL bodies have a 7.5 mm higher rim)
LID_DROP = 6.9                          # the lid comes down over the body's rim (push fit on S3 1F)
# width -> (hinge notch centre |x|, lock seat centre |x| (0: one lock in the middle), case label recess centre x),
# unit frame, measured with features.py on the S3/M3/L3/XL3 1F bodies and S1F/M1F/L1F/XL1F front panels
CASE_SEATS = {"S": (51.8, 0.0, -53.28), "M": (69.3, 0.0, -75.6), "L": (86.8, 82.4, 0.07), "XL": (131.4, 127.05, -0.07)}
# Hinges (manual p. 17). One hinge file holds the two body leaves (mirror images, printed face to face);
# each leaf bolts inside the body's back wall, on the 2 mm pad under a notch in the wall's top (4 holes,
# M4 x 10), its knuckle behind the wall. The hinge top(s) bolt under the lid (4 holes each, M4 x 14): S and
# M have one long top between the two leaves, L and XL a file with two tops, each next to a leaf on its
# inner side. Every knuckle is on one axis along x, level with the body's top and 7.49 mm behind its back
# face (the leaves' and tops' holes against the wall's and lid's: within 0.02 mm on S3/M5/L3/XL3/XL7 1F,
# S3/L7 2F, S7 4F). A rod (one file holds both) goes in from each end, its head against the leaf's end.
CASE_HINGE = {(False, True): "S-M 1F Hinge.stl", (False, False): "S-M 2-4F Hinge.stl",
              (True, True): "L-XL 1F Hinge.stl", (True, False): "L 2-4F Hinge.stl"}
HINGE_X = {"S": 51.9, "M": 69.27, "L": 86.8, "XL": 131.4}                 # leaf centres along the axis (wall holes)
HINGE_TOP_X = {"S": (0.0,), "M": (0.0,), "L": (41.3, -41.3), "XL": (85.9, -85.9)}   # hinge top centres (lid holes)
HINGE_BEHIND = 7.49     # axis behind the body's back face
ROD_HEAD = 5.0          # rod head thickness: the rod's end is this far beyond the leaf's end
# How far the page opens a lid: the manual's open view (p. 17). Swept on the exported parts, neither the lid nor
# the hinge tops meet the body, the leaves or the rods before 180 deg.
LID_OPEN = 105.0
# Toggle latch (a "double throw" latch, manual p. 17), measured on every case (kinematics.py): the same on every
# size and height, relative to the holder's pin A. The link's fork (15.3 mm gap) straddles the holder's lug (30 mm
# wide) on pin A; its solid end sits between the lever's ears on pin B, 15.0 mm below A and 0.99 mm in front (the
# link leans 3.8 deg forward). The lever's tooth tip C is 30.19 mm above B (36.19 on the 6 mm longer 2-4F lever)
# and 10.30 mm behind it, in the lid's groove. Closed, the link is past the toggle's dead centre (about 30 deg forward, where the tooth bites deepest),
# held there by the lever's ears on the front panel's seat; the tooth presses 0.8 mm into the groove's ramp (the
# latch's preload: the parts flex, rigid copies overlap). Opening: phase 1, the link turns forward about A, B
# follows and the tooth slides straight up out of the groove (an inverted slider-crank) until it has risen
# LATCH_OUT mm, clear of the lid's lip; phase 2, the tooth free, the link comes back to LATCH_PHI and the lever
# swings forward to LATCH_THETA: the latch hangs open, leaning 40 deg out in front of the panel, and the lid can turn.
# The link can only turn 0 to 80 deg against the lever (its pocket): LATCH_PHI - LATCH_THETA stays under that.
LATCH_B = (-15.0, 0.99)       # B - A (unit y, z)
LATCH_C = {1: (30.19, -10.30), 2: (36.19, -10.30), 4: (36.19, -10.30)}     # C - B, by height (1F / 2-4F lever)
LATCH_OUT, LATCH_PHI, LATCH_THETA = 4.0, 30.0, -40.0


def case(w, d, h):
    """A case (sustainer): open body with a module's underside, front panel, hinged lid on top.
    Measured on S3 1F: the body has the drawer module's latch frame; the lid (turned like a drawer roof)
    covers the body and the front panel and comes down 6.9 mm over the body's rim (push fit). The body is
    open at the front: the front panel is its front wall, top level with the body's top (bolt holes meet).
    Locks: holder behind the panel on its blind holes, link, lever closed in the seat recess (see below).
    Hinges: leaves, hinge top(s) and rods on one axis behind the back wall (hinges(), CASE_HINGE); the lid and
    the hinge tops are group "lid" and turn about the recipe's "hinge" axis."""
    fam = SU + CFAM[w] + "/"
    big = w in ("L", "XL")
    depth = 146.1 + 42 * (d - 3)
    T = CASE_H[h]
    r = Recipe(f"C{w}{d}_{h}F", f"case|{w}|{d}|{h}")
    variants = ("Flat", "Dividers", "Sealed") if big else ("",)
    first = None
    for v in variants:
        body = need(fam + f"{w}{d}/Modules/{w}{d} {h}F{' ' + v if v else ''} Module.stl")
        rot, why = rot_checked(body, frames_at_back(body, depth), "case body")
        if why:
            r.notes.append(why)
        r.part("Body" + (f"_{v}" if v else ""), body, "body", "module", rot, {"x": ["center", 0], "y": ["max", 0], "z": ["min", 0]})
        first = first or (body, rot)
    if big:
        r.notes.append("the three body styles (flat, dividers, sealed) share one place; the page shows the one in the part list")
    fac = need(fam + ("XL1F Facade.stl" if w == "XL" else f"Facades/{w}{h}F Facade.stl"))
    # The front panel is the body's front wall (the body is open at the front): 4.8 mm lower than the body,
    # its top level with the body's top, so its bolt holes (x = +/-77.4 on S, 19.4 mm apart on 1F) meet the
    # body's (checked on every height: body holes = panel holes + 4.8).
    r.part("Facade", fac, "facade", "module", [-90, 0, 0], {"x": ["center", 0], "y": ["min", 0], "z": ["max", T]})
    lid = find(fam + f"{w}{d}/Roofs/{w}{d} Roof.stl") or find(fam + f"{w}{d}/Roof/{w}{d} Roof.stl") \
        or find(fam + f"{w}{d}/Roofs/{w}{d} Roof Whole.stl") or find(fam + f"{w}{d}/Roof/{w}{d} Roof Whole.stl")
    lrot = [-90, -42.8, 0]   # every case lid is printed like S3's (orient.py: S3-XL5 lids <= 0.17, one-piece S6/L7 lids 0.03 on all corners)
    r.part("Lid", lid, "roof", "lid", lrot, {"x": ["center", 0], "y": ["max", 10.0], "z": ["min", T - LID_DROP]})
    if d >= 6:
        r.notes.append("lid: the one-piece version is placed; the split version's parts are not")
    nl = latches(r, first[0], first[1], 0.0, -0.06, 8.6, depth=depth)
    r.notes.append(f"{nl} latch frame(s) under the body (a latch is placed in each; the planner's case list has no latch)")
    # The outer lock plate hangs from the front panel's top edge, its slot across (manual p. 8 and p. 17):
    # the CAD file has it a quarter turn off and standing higher.
    # Hardware. Seats read on the parts (features: front panel seen from the front, body seen from behind):
    # lock seats 51.3 x 36.8 mm in the front panel's top edge, hinge notches 7 mm deep in the body's back
    # wall, the case label's recess in the front panel. Heights and depths come from the files that sit
    # assembled around one case per height in the CAD file (S 1F, S 2F, S 4F; L 1F, L 2F).
    _, lock_x, label_u = CASE_SEATS[w]
    # Lock (manual p. 17), a toggle latch per seat, closed:
    # - holder: the "UP" plate, lying across behind the front panel, bolted into the 4 blind holes beside the
    #   panel's top notch (61.4 x 9 mm apart; their centre 11.7 mm under the top on 1F, 17.7 mm on 2-4F),
    #   its lug forward through the notch; turned so "UP" reads upright from inside.
    # - link (LOCK INNER PART, holes 15 mm apart): its fork on the lug's pin, in the lever's back pocket (LATCH_*).
    # - lever (LOCK OUTER PART, the 2-4F one is 6 mm longer): pinned to the link's lower hole, lying in the
    #   panel's seat recess, its hook at the top over the lid's front edge (its "UP" reads upright from
    #   inside, as in the manual). Its top comes out at T + 15.0 on every height. 1 mm forward of the
    #   link's plane so it clears the recess floor (an over-centre latch closes slightly tilted).
    # CAD measures: holder bolt holes' centre X 7501.55 / Z 34.27, lug hole X 7498.87 Y 1865.04, plate front
    # Y 1854.84; lever hole 10.29 mm from its end, Y 1865.03; link holes X 7494.05 / 7509.06, Y 1897.22.
    yb = T - (11.7 if h == 1 else 17.7)          # holder bolt centre (unit y)
    lug_y, lug_z = yb + 2.68, 1865.04 - 1854.838  # lug pin (unit y, z)
    for i, x in enumerate([0.0] if not lock_x else [lock_x, -lock_x]):
        r.part(f"LockHolder_{i+1}", SUU + "Locks/LOCK HOLDER.stl", "mech", "module", [0, 90, 0],
               {"x": ["center", x], "y": ["min", 1849.24 - 1854.838], "z": ["min", yb - 11.07]})
        # the link: end for end (the CAD file has its fork down), fork on pin A, leaning forward to pin B
        A = np.array([-x, lug_y, lug_z])                       # unit frame
        B = A + np.array([0.0, *LATCH_B])
        C = B + np.array([0.0, *LATCH_C[h]])
        lk = SUU + "Locks/LOCK INNER PART.stl"
        R0 = vg.from_euler_xyz([0, 90, 0])
        V0 = vg.read_stl(os.path.join(F.ROOT, lk)).reshape(-1, 3)
        P0 = V0 @ R0.T
        lo, hi = P0.min(0), P0.max(0)
        fork = R0.T @ np.array([(lo[0] + hi[0]) / 2, lo[1] + 4.31, lo[2] + 4.30])   # fork hole, file coordinates
        lean = np.degrees(np.arcsin(LATCH_B[1] / 15.0))
        R_cad = vg.rot_axis("x", lean) @ vg.rot_axis("y", 180) @ R0
        r.placed(f"LockLink_{i+1}", lk, "mech", "module", vg.C @ R_cad, fork, A, joint=f"latch_{i+1}.link")
        r.joints[f"latch_{i+1}"] = {"latch": {"axis": [-1, 0, 0], "A": [round(v, 3) for v in A], "B": [round(v, 3) for v in B],
                                              "C": [round(v, 3) for v in C], "slide": [0, 1, 0], "out": LATCH_OUT,
                                              "phi": LATCH_PHI, "theta": LATCH_THETA, "split": 0.5}}
        outer = "LOCK OUTER PART 1F.stl" if h == 1 else "LOCK OUTER PART 2-4F.stl"
        r.part(f"LockOuter_{i+1}", SUU + "Locks/" + outer, "accent", "module", [0, -90, 0],
               {"x": ["center", x], "y": ["min", 1852.14 - 1854.838 + 1.0], "z": ["min", lug_y - 15.0 - 10.29]},
               joint=f"latch_{i+1}.lever")
    r.steps = [{"joints": list(r.joints), "from": 0, "to": 1, "s": 0.45}, {"joints": ["lid"], "from": 0, "to": 1, "s": 0.6}]
    # case label: 1F panels have a closed recess, its centre 10 mm under the panel's top (x from CASE_SEATS);
    # 2F/4F panels a slot open on the left edge, 43.6 mm under the top, closed 50.1 mm in: the label
    # (38.1 mm long) is pushed to its end
    if h == 1:
        label_y = T - 10.0
    else:
        label_y, label_u = T - 43.63, -{"S": 82.4, "M": 127.0, "L": 164.8}[w] + 50.1 - 19.07
    r.part("CaseLabel", SUU + "Label for Sustainers.stl", "insert", "module", [-90, 0, 0],
           {"x": ["center", -label_u], "y": ["min", 7.91], "z": ["center", label_y]})
    r.notes.append("%d lock(s) (lock seats in the front panel; the planner counts 2 for every case)" % (1 if not lock_x else 2))
    hinges(r, w, d, h, T, depth)
    return r.json("Body" + ("_Flat" if big else ""))


def hinges(r, w, d, h, T, depth):
    """Both body leaves, the hinge top(s) (group lid) and both rods, each piece of its file on its own;
    sets the unit's hinge axis (see CASE_HINGE)."""
    big = w in ("L", "XL")
    yA, zA = T, -depth - HINGE_BEHIND
    hx = HINGE_X[w]
    leaf = need(SUU + "Hinges/" + CASE_HINGE[(big, h == 1)])
    leaves = sorted(file_pieces(leaf), key=lambda p: p["centre"][1])
    lleaf = None
    for i, (pc, sx) in enumerate(zip(leaves, (1, -1))):
        lo, hi, V = pc["min"], pc["max"], pc["tris"].reshape(-1, 3)
        # knuckle at the piece's x max end; the plate runs along -x from it, offset 14.5 mm to the side
        # away from the knuckle (+y on the piece whose knuckle is at y min)
        low = V[V[:, 0] > hi[0] - 1.0][:, 1].mean() < pc["centre"][1]
        ring = (hi[0] - 7.0, lo[1] + 7.0 if low else hi[1] - 7.0, (lo[2] + hi[2]) / 2)
        # unit: axis (file z) along x, plate down (file -x -> unit -y), plate in front of the knuckle (inside)
        R = [[0, 0, 1], [1, 0, 0], [0, 1, 0]] if low else [[0, 0, -1], [1, 0, 0], [0, -1, 0]]
        r.placed(f"HingeLeaf_{i+1}", leaf, "mech", "module", R, ring, (sx * hx, yA, zA), piece=pc)
        lleaf = hi[2] - lo[2]
    top = need(SUU + "Hinges/" + ({"S": "S Hinge Top.stl", "M": "M Hinge Top.stl"}.get(w) or "L-XL Hinge Top.stl"))
    tops = sorted(file_pieces(top), key=lambda p: -p["centre"][0])
    for i, (pc, tx) in enumerate(zip(tops, HINGE_TOP_X[w])):
        lo, hi, V = pc["min"], pc["max"], pc["tris"].reshape(-1, 3)
        rx = (lo[0] + hi[0]) / 2 if big else lo[0] + 7.0
        ring = (rx, lo[1] + 7.0, (lo[2] + hi[2]) / 2)
        # the plate runs along file +y from the knuckle (forward, under the lid); its face through the axis
        # is its bottom face, the plate's thickness goes up (file +x, or -x on one of the L/XL tops)
        plus = V[V[:, 1] > lo[1] + 25][:, 0].mean() > rx
        R = [[0, 0, 1], [1, 0, 0], [0, 1, 0]] if plus else [[0, 0, -1], [-1, 0, 0], [0, 1, 0]]
        r.placed(f"HingeTop_{i+1}", top, "mech", "lid", R, ring, (tx, yA, zA), piece=pc)
    rod = need(SUU + "Rods/" + ("L-XL Rods.stl" if big else "S-M Rods.stl"))
    for i, (pc, sx) in enumerate(zip(file_pieces(rod), (1, -1))):
        lo, hi, V = pc["min"], pc["max"], pc["tris"].reshape(-1, 3)
        wide = lambda m: np.ptp(V[m][:, 1])
        head_min = wide(V[:, 0] < lo[0] + 1.0) > wide(V[:, 0] > hi[0] - 1.0)
        # shaft axis: 3.65 above the piece's flat bottom (printed on a flat); the head goes outwards
        end = (lo[0] if head_min else hi[0], pc["centre"][1], lo[2] + 3.65)
        flip = (head_min and sx > 0) or (not head_min and sx < 0)
        R = [[-1, 0, 0], [0, 0, 1], [0, 1, 0]] if flip else [[1, 0, 0], [0, 0, 1], [0, -1, 0]]
        r.placed(f"HingeRod_{i+1}", rod, "accent", "module", R, end, (sx * (hx + lleaf / 2 + ROD_HEAD), yA, zA), piece=pc)
    r.hinge = {"origin": [0.0, round(yA, 3), round(zA, 3)], "axis": [-1, 0, 0], "open_deg": LID_OPEN,
               "note": "the lid and the hinge tops (group lid) turn about this axis (unit frame, right-handed: a "
                       "positive angle lifts the lid's front); 0 = closed"}
    r.notes.append("hinges: 2 leaves, %d top(s), 2 rods on one axis at y %.1f, z %.2f; the hinge tops' plates come "
                   "0.85 mm under the lid's bosses (the lid's push-fit height and the hinge disagree by that much)" % (len(HINGE_TOP_X[w]), yA, zA))


def family_sml(w):
    out = []
    for d in range(3, 8):
        for h in (1, 2, 4):
            out.append(drawer_sml(w, d, h))
        mod1 = need(D + FAM[w] + f"/{w}{d}/Modules/{w}{d} Module 1F.stl")
        for kind in ROOFS:
            rc = roof_sml(w, d, kind, (mod1, rot_checked(mod1, frames_at_back(mod1, 146.1 + 42 * (d - 3)), "module")[0]))
            if rc:
                out.append(rc)
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # paths hold ² (python -I ignores PYTHONIOENCODING)
    out = sys.argv[1]
    fams = sys.argv[2:] or ["S", "M", "L", "L2", "XL", "XL2", "CS", "CM", "CL", "CXL", "LAY"]
    os.makedirs(out, exist_ok=True)
    for w in fams:
        if w in ("S", "M", "L"):
            recs = family_sml(w)
        elif w == "L2":
            recs = [drawer_l2(d, h) for d in range(3, 8) for h in (1, 2, 4)]
        elif w == "XL2":
            recs = [drawer_xl2(d) for d in range(3, 8)]
        elif w == "XL":
            recs = [drawer_xl(d) for d in range(3, 8)]
            for d in range(3, 8):
                mod1 = need(D + FAM["XL"] + f"/XL{d}/Modules/XL{d} Module 1F.stl")
                ref = (mod1, rot_checked(mod1, frames_at_back(mod1, 146.1 + 42 * (d - 3)), "module")[0])
                recs += [rc for kind in ROOFS for rc in [roof_sml("XL", d, kind, ref)] if rc]
        elif w == "STK":          # a tower's base, wheels and foot (measure_stack.py first)
            recs = [stack_unit(sw, d) for sw in ("S", "M", "L", "XL") for d in range(3, 8)]
        elif w == "LAY":          # several drawers in one 2F/4F module (S, M, L, L²)
            recs = family_layouts()
        elif w.startswith("C"):   # cases: CS CM CL CXL
            cw = w[1:]
            recs = [case(cw, d, h) for d in range(3, 8) for h in ((1,) if cw == "XL" else (1, 2, 4))]
        else:
            raise SystemExit("unknown family " + w)
        for rc in recs:
            p = os.path.join(out, f"{rc['name']}_assembly.json")
            txt = json.dumps(rc, indent=1, ensure_ascii=False)
            same = os.path.exists(p) and open(p, encoding="utf-8").read() == txt
            if not same:   # an unchanged recipe keeps its date, so run_assemble.py skips it
                open(p, "w", encoding="utf-8").write(txt)
            print(p, "(same)" if same else "", len(rc["parts"]), "parts", "; ".join(rc["notes"]))
