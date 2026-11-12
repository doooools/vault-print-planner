"""The backbone column and the tower handles (column|<w>), measured on the files (numpy, no Blender).

  python -I measure_column.py <stl-placements.json> [w ...]      (w: S M L XL U; U = the universal backbones)

Writes `column|<w>` into the placements (other keys untouched). Each piece is placed in a column frame of its own:
three.js axes, x = 0 midway between the two M16 rods, y = 0 at the piece's bottom, z = 0 on the modules' back face,
-z away from the stack (the back of a stack faces -z). The page (stackLayout in src/template.html) stacks the pieces
up the back of the tower and moves them onto the back face of its first unit. Modifications Assembly 7-19/15 isn't
at hand: what the files say is used, and what is inferred is said so.

- Backbone (S, M, L 1F and 2F; XL 1F only; universal 1F and 2F): a plate as wide as the module, its flat side on the
  module's back, with a raised pad over each rod. Each pad has an 17.3 mm channel for an M16 rod (vertical, 16.0 mm
  out from the module's back on every size) and, per F, 3 holes 13 mm apart in two columns 26 mm apart (the
  "three spots" drilled through the module). A 2F is two 1F sections 52 mm apart (99 = 47 + 52). Printed flat, the
  plate on the bed: file +y up the stack, file +z away from the module.
- Universal backbone: one pad and its flange, 63 mm wide: one per rod, the flange outwards (the family backbone's
  ends have the same notch), the left one the right one turned half a turn about the depth axis.
- Universal pull-out handle lock (in `column|U`, with its knob): one per rod, see ulock().
- Pull-out handle lock: a backbone-like block 47 tall and 35 deep, its rods' channels split by a slot that a knob
  (M6 x 35 hex bolt from the module side, head in its pocket, into the knob's insert) clamps. Printed on its end:
  file +z up, file +y towards the module. Its rod channels sit 16.0 mm out from its module face, like the
  backbone's: it goes on the module's back like a backbone.
- Knob (part 1 a disc with the insert's hole underneath, part 2 the grip in its slot) and the S lock's part 2:
  exported assembled to their partner in the CAD scene (none of their material inside it): they take its matrix.
  The knob sits on the lock's outer face over its bolt hole (its seat: 33.5 mm, 6 deep on M, L, XL; on S the
  clamp bar, part 2).
- Stationary handle: a U, its two legs' ends on the backbone's pads (2 holes per column, 26 mm apart, under the
  pads' outer holes: M4 x 60 from the module side), the bar 50 mm out. Its legs are 47 tall: one backbone section.
- Pull-out handle: a U, legs down, a 15 mm blind hole 56.5 deep in each leg's end for the rod. Its rods' axis is
  14.4 mm from its module-side face: 1.6 mm clear of the modules' back, so it slides down past the roof. At rest
  its legs stand on the lock's top.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vault_geom as vg  # noqa: E402
import hw_geom as hg  # noqa: E402

MO = "03. MODIFICATIONS/"
BB = MO + "Backbone/"
ROD_Z = -16.0          # rods' axis, from the modules' back (checked on every backbone and lock below)


def mat(R, t):
    M = np.column_stack([R, t])
    return [round(float(v), 6) if k % 4 < 3 else round(float(v), 3) for k, v in enumerate(M.reshape(-1))]


def circle_fit(p):
    x, y = p[:, 0], p[:, 1]
    A = np.c_[2 * x, 2 * y, np.ones(len(x))]
    cx, cy, k = np.linalg.lstsq(A, x * x + y * y, rcond=None)[0]
    return np.array([cx, cy]), float(np.sqrt(k + cx * cx + cy * cy))


def circles(T, axis, value, uv, guesses, r=(5.5, 10.0)):
    """Circles cut by the plane coord[axis] = value near each guessed centre (u, v): [(centre, radius)]."""
    s = hg.section(T, axis, value).reshape(-1, 3)[:, uv]
    out = []
    for g in guesses:
        d = np.linalg.norm(s - g, axis=1)
        p = s[(d > r[0]) & (d < r[1])]
        if len(p) < 12:
            raise RuntimeError(f"no circle near {g}")
        c, rad = circle_fit(p)
        p = s[np.abs(np.linalg.norm(s - c, axis=1) - rad) < 0.3]   # refit on the circle's own points
        out.append(circle_fit(p))
    return out


def posed(T, m):
    M = np.array(m).reshape(3, 4)
    return T @ M[:, :3].T + M[:, 3]


def touch(fixed, moving, axis, sign, window, step=0.25):
    """How far `moving` must go along `axis` (towards -sign) to touch `fixed`: the smallest gap between the fixed
    part's surface nearest the + side (sign +1: largest coordinate) and the moving part's surface facing it."""
    lo, hi = window
    Df, *_ = vg.depthmap(fixed, axis, sign, step=step, lo=lo, hi=hi)
    Dm, *_ = vg.depthmap(moving, axis, -sign, step=step, lo=lo, hi=hi)
    gap = (Dm - Df) * sign
    return float(np.nanmin(gap))


# ---------------------------------------------------------------------------------------------------------- backbone
BB_R = np.diag([-1.0, 1, -1])        # file +z (the pads) away from the module, file +y up


def backbone(f, universal=False):
    T = hg.file_tris(f)
    P = T.reshape(-1, 3)
    lo, hi = P.min(0), P.max(0)
    c = (lo + hi) / 2
    zr = lo[2] - ROD_Z   # expected rod axis in the file (16 mm off the plate face)
    if universal:
        # one channel: try both sides of the middle
        for g in ([c[0] + 10.4, zr], [c[0] - 10.4, zr]):
            try:
                (rc, rr), = circles(T, 1, c[1] + 0.013, [0, 2], [np.array(g)])
                break
            except RuntimeError:
                continue
        mid = rc[0]
        rods = [rc]
    else:
        half = (hi[0] - lo[0]) / 2 - 42.0
        rods = [x[0] for x in circles(T, 1, c[1] + 0.013, [0, 2], [np.array([c[0] - half, zr]), np.array([c[0] + half, zr])])]
        mid = (rods[0][0] + rods[1][0]) / 2
        rr = None
    t = np.array([mid, -lo[1], lo[2]])
    m = mat(BB_R, t)
    rz = [float(-r[1] + lo[2]) for r in rods]
    rx = [float(-r[0] + mid) for r in rods]
    # flange side of a universal piece, in the column frame (+1: the flange is towards +x of its rod)
    flange = None
    if universal:
        xs = sorted([-(lo[0]) + mid, -(hi[0]) + mid])
        flange = 1 if abs(xs[1]) > abs(xs[0]) else -1
    return {"file": f, "m": m, "h": round(float(hi[1] - lo[1]), 2), "depth": round(float(hi[2] - lo[2]), 2),
            "rods_x": [round(x, 2) for x in rx], "rods_z": [round(z, 2) for z in rz], "flange": flange,
            "x": [round(float(-(hi[0]) + mid), 2), round(float(-(lo[0]) + mid), 2)]}


# -------------------------------------------------------------------------------------------------------------- lock
LOCK_R = np.array([[-1.0, 0, 0], [0, 0, 1], [0, 1, 0]])   # file +z up, file +y towards the module


def lock(w):
    f = BB + f"{w} Pull-out Handle Lock.stl"
    T = hg.file_tris(f)
    P = T.reshape(-1, 3)
    lo, hi = P.min(0), P.max(0)
    c = (lo + hi) / 2
    half = (hi[0] - lo[0]) / 2 - 42.0
    yr = hi[1] + ROD_Z
    rods = [x[0] for x in circles(T, 2, c[2] + 0.013, [0, 1], [np.array([c[0] - half, yr]), np.array([c[0] + half, yr])])]
    mid = (rods[0][0] + rods[1][0]) / 2
    t = np.array([mid, -lo[2], -hi[1]])
    m = mat(LOCK_R, t)
    # its M6 bolt holes: through along file y, at mid height (depth map along y)
    D, u0, w0, _ = vg.depthmap(T, 1, 1, step=0.25)
    from scipy import ndimage
    lab, n = ndimage.label(np.isnan(D))
    bolts = []
    for k in range(1, n + 1):
        jj, ii = np.nonzero(lab == k)
        a = len(ii) * 0.0625
        if 20 < a < 45 and ii.min() > 0 and jj.min() > 0 and ii.max() < D.shape[1] - 1 and jj.max() < D.shape[0] - 1:
            fx, fz = u0 + 0.25 * ii.mean(), w0 + 0.25 * jj.mean()
            bolts.append([round(float(-fx + mid), 2), round(float(fz - lo[2]), 2)])
    parts = [{"file": f, "m": m}]
    if w == "S":
        parts.append({"file": BB + "S Pull-out Handle Lock Part 2.stl", "m": m})
    return {"parts": parts, "h": round(float(hi[2] - lo[2]), 2), "depth": round(float(hi[1] - lo[1]), 2),
            "rods_x": [round(float(-r[0] + mid), 2) for r in rods], "rods_z": [round(float(r[1] - hi[1]), 2) for r in rods],
            "bolts": sorted(bolts)}


def ulock():
    """The universal pull-out handle lock: one rod's share of a lock, 89 wide (two per stack, one per rod). Its rod
    channel and knob bolt are the family lock's (16.0 mm out from its module face, an M6 bolt 17.5 mm from the rod,
    clamping a slot); on its other side a flange 14 mm thick runs out to the module's side edge, with 4 holes (4.2 mm,
    a 1 mm membrane on their outer end) in a column 8.15 mm from that edge, 4.75 / 16.25 / 30.75 / 42.25 mm above its
    bottom: the module's back corner holes (8.15 mm from its side, 9.57 and 47.07 mm above its bottom, measure_connectors.py)
    take the outer two, so it is screwed onto a module's back at one level, like the family lock stands on one. Printed
    on its end like the family lock: file +z up, file +y towards the module. In the column frame of the right rod:
    x = 0 on the rod, the flange towards +x (outwards); the left one is turned half a turn about z (its holes are
    symmetric top to bottom), like the universal backbones."""
    f = BB + "Universal Pull-out Handle Lock.stl"
    T = hg.file_tris(f)
    P = T.reshape(-1, 3)
    lo, hi = P.min(0), P.max(0)
    (rc, rr), = circles(T, 2, (lo[2] + hi[2]) / 2 + 0.013, [0, 1], [np.array([lo[0] + 42.0, hi[1] + ROD_Z])])
    t = np.array([rc[0], -lo[2], -hi[1]])
    m = mat(LOCK_R, t)
    D, u0, w0, _ = vg.depthmap(T, 1, 1, step=0.25)
    from scipy import ndimage
    lab, n = ndimage.label(np.isnan(D))
    bolts = []
    for k in range(1, n + 1):
        jj, ii = np.nonzero(lab == k)
        a = len(ii) * 0.0625
        if 20 < a < 45 and ii.min() > 0 and jj.min() > 0 and ii.max() < D.shape[1] - 1 and jj.max() < D.shape[0] - 1:
            fx, fz = u0 + 0.25 * ii.mean(), w0 + 0.25 * jj.mean()
            bolts.append([round(float(-fx + rc[0]), 2), round(float(fz - lo[2]), 2)])
    # the flange's holes: circles in a section through the flange, near its outer edge
    sec = float(hi[1] - 5)
    edge = float(-lo[0] + rc[0])
    fl = circles(T, 1, sec + 0.013, [0, 2], [np.array([lo[0] + 8.15, lo[2] + z]) for z in (4.75, 16.25, 30.75, 42.25)], r=(1.0, 3.0))
    holes = [[round(float(-c[0] + rc[0]), 2), round(float(c[1] - lo[2]), 2), round(2 * r, 2)] for c, r in fl]
    return {"parts": [{"file": f, "m": m}], "h": round(float(hi[2] - lo[2]), 2), "depth": round(float(hi[1] - lo[1]), 2),
            "rod_z": round(float(rc[1] - hi[1]), 2), "rod_d": round(2 * rr, 2), "edge": round(edge, 2), "bolts": sorted(bolts),
            "flange_holes": holes}


KNOB_R = np.diag([-1.0, 1, -1])      # file +z (the grip) away from the module


def knobs(lk):
    """Knob part 1 on the lock's outer face over each bolt hole; part 2 with part 1's matrix."""
    f1, f2 = BB + "Handle Lock Knob Part 1.stl", BB + "Handle Lock Knob Part 2.stl"
    K = hg.file_tris(f1)
    P = K.reshape(-1, 3)
    lo, hi = P.min(0), P.max(0)
    c = (lo + hi) / 2
    L = np.concatenate([posed(hg.file_tris(p["file"]), p["m"]) for p in lk["parts"]])
    out, notes = [], []
    for bx, by in lk["bolts"]:
        # the seat: the outermost surface of the lock (and its part 2) in a ring 9-15 mm round the bolt (inside the knob's 17 mm radius)
        D, u0, w0, _ = vg.depthmap(L, 2, -1, step=0.25, lo=[bx - 15, by - 15, -200], hi=[bx + 15, by + 15, 50])
        jj, ii = np.mgrid[0:D.shape[0], 0:D.shape[1]]
        r = np.hypot(u0 + 0.25 * ii - bx, w0 + 0.25 * jj - by)
        ring = D[(r > 9) & (r < 15)]
        seat = float(np.nanmin(ring))   # the outermost: the seat on M, L, XL; the clamp bar (part 2) on S
        t = np.array([bx + c[0], by - c[1], seat + lo[2]])
        m = mat(KNOB_R, t)
        out += [{"file": f1, "m": m}, {"file": f2, "m": m}]
        notes.append({"at": [bx, by], "seat_z": round(seat, 2), "ring_spread": round(float(np.nanmax(ring) - np.nanmin(ring)), 2)})
    return out, notes


# ------------------------------------------------------------------------------------------------------------ handles
def stationary(w, bb1):
    f = MO + f"Stationary Handle/{w} Stationary Handle.stl"
    T = hg.file_tris(f)
    P = T.reshape(-1, 3)
    lo, hi = P.min(0), P.max(0)
    c = (lo + hi) / 2
    # legs' ends (file +z) on the pads; push it in along z until it touches the backbone
    t = np.array([-c[0], -lo[1], -100.0 - hi[2]])
    B = posed(hg.file_tris(bb1["file"]), bb1["m"])
    H = T + t
    W = (hi[0] - lo[0]) / 2 + 2
    gap = touch(B, H, 2, -1, ([-W, 0, -150], [W, 47, 10]))
    t = t + [0, 0, gap]
    return {"file": f, "m": mat(np.eye(3), t), "face_z": round(float(-100 + gap), 2), "out": round(float(-100 + gap - (hi[2] - lo[2])), 2)}


PULL_R = np.array([[-1.0, 0, 0], [0, 0, -1], [0, -1, 0]])   # legs down (file +z), file -y towards the module


def pullout(w, lk):
    f = MO + f"Pull-out Handle/{w} Pull-out Handle.stl"
    T = hg.file_tris(f)
    P = T.reshape(-1, 3)
    lo, hi = P.min(0), P.max(0)
    c = (lo + hi) / 2
    # the rods' blind holes, 10 mm into the legs' ends
    zc = hi[2] - 10
    gy = lo[1] + 14.4
    rods = [x[0] for x in circles(T, 2, zc + 0.013, [0, 1], [np.array([c[0] - (hi[0] - lo[0]) / 2 + 15.9, gy]), np.array([c[0] + (hi[0] - lo[0]) / 2 - 15.9, gy])], r=(5.0, 9.0))]
    mid = (rods[0][0] + rods[1][0]) / 2
    ry = rods[0][1]
    # hole depth: a ray up the hole from below the leg's end
    hits = hg.ray_hits(T, np.array([rods[0][0], ry, hi[2] + 5]), np.array([0, 0, -1.0]))
    depth = round(float(min(s for s, _ in hits if s > 0) - 5), 2)
    t = np.array([mid, hi[2], ry + ROD_Z])
    m = mat(PULL_R, t)
    # at rest: its legs on the lock's top
    Lk = np.concatenate([posed(hg.file_tris(p["file"]), p["m"]) for p in lk["parts"]])
    Hd = posed(T, m) + [0, 200, 0]
    W = (hi[0] - lo[0]) / 2 + 2
    gap = touch(Lk, Hd, 1, 1, ([-W, -10, -60], [W, 400, 10]))
    return {"file": f, "m": m, "rods_x": [round(float(-r[0] + mid), 2) for r in rods], "rod_in": depth,
            "rest": round(200 - gap, 2), "clear": round(float(-ROD_Z - (ry - lo[1])), 2)}


# ---------------------------------------------------------------------------------------------------------- pegboard
PEG = MO + "Pegboard Attachment/"
PEG_KINDS = {"ussa": "USSA Pegboard", "ikea": "IKEA Skadis Pegboard"}


def pegboard(w, kind, h, bb):
    """A pegboard attachment on its backbone (bb: backbone(), same width and height): a plate 42 mm narrower than the
    backbone, as tall, with one row of 4 holes per section, over the backbone's middle (3.2 mm pilot) holes. Its side
    with two 3 mm pockets goes on the pads, the pockets over the pads' keys. Printed flat, the pockets up: file +z
    towards the module, file +y up (it is symmetric both ways). Placed far out, then moved in until it touches."""
    f = PEG + f"{PEG_KINDS[kind]}/{w}{h}F.stl"
    T = hg.file_tris(f)
    P = T.reshape(-1, 3)
    lo, hi = P.min(0), P.max(0)
    t = np.array([-(lo[0] + hi[0]) / 2, -lo[1], -hi[2] - 60.0])
    m = mat(np.eye(3), t)
    Tb = posed(hg.file_tris(bb["file"]), bb["m"])
    Tp = posed(T, m)
    win = (np.minimum(Tb.reshape(-1, 3).min(0), Tp.reshape(-1, 3).min(0)), np.maximum(Tb.reshape(-1, 3).max(0), Tp.reshape(-1, 3).max(0)))
    gap = touch(Tb, Tp, 2, -1, win)
    t[2] += gap
    m = mat(np.eye(3), t)
    # its holes against the backbone's pilot holes (x, y in the column frame)
    class Part: pass
    pp = Part(); pp.tris = posed(T, m); pp.lo, pp.hi = pp.tris.reshape(-1, 3).min(0), pp.tris.reshape(-1, 3).max(0)
    holes = sorted((round(float(c["c"][0]), 2), round(float(c["c"][1]), 2)) for c in hg.holes_in(pp, 2, -1, area=(3, 60)))
    return {"file": f, "m": m, "face": round(float(t[2] + hi[2]), 2), "t": round(float(hi[2] - lo[2]), 2),
            "w": round(float(hi[0] - lo[0]), 2), "h": round(float(hi[1] - lo[1]), 2), "holes": holes}


def column(w):
    out = {"parts": [], "column": {}}
    notes = {}
    add = lambda f, role, m, what: out["parts"].append([f, role, "module", m, {"as": what}])
    if w == "U":
        for h in (1, 2):
            b = backbone(BB + f"Universal {h}F Backbone.stl", universal=True)
            add(b["file"], "fittings", b["m"], f"backbone{h}")
            out["column"][f"h{h}"] = b["h"]
            notes[f"backbone{h}"] = b
        out["column"].update({"rod_z": notes["backbone1"]["rods_z"][0], "flange": notes["backbone1"]["flange"]})
        lk = ulock()
        for p in lk["parts"]:
            add(p["file"], "fittings", p["m"], "lock")
        kn, kn_notes = knobs(lk)
        for p in kn:
            add(p["file"], "fittings", p["m"], "lock")
        out["column"].update({"lock_h": lk["h"], "lock_edge": lk["edge"]})
        notes.update({"lock": {k: v for k, v in lk.items() if k != "parts"}, "knobs": kn_notes})
        return out, notes
    hs = (1,) if w == "XL" else (1, 2)
    for h in hs:
        b = backbone(BB + f"{w}{h}F Backbone.stl")
        add(b["file"], "fittings", b["m"], f"backbone{h}")
        out["column"][f"h{h}"] = b["h"]
        notes[f"backbone{h}"] = b
    lk = lock(w)
    for p in lk["parts"]:
        add(p["file"], "fittings", p["m"], "lock")
    kn, kn_notes = knobs(lk)
    for p in kn:
        add(p["file"], "fittings", p["m"], "lock")
    st = stationary(w, notes["backbone1"])
    add(st["file"], "body", st["m"], "stationary")
    pu = pullout(w, lk)
    add(pu["file"], "body", pu["m"], "pullout")
    for kind in PEG_KINDS:
        for h in hs:
            pg = pegboard(w, kind, h, notes[f"backbone{h}"])
            add(pg["file"], "base", pg["m"], f"pegboard-{kind}{h}")
            notes[f"pegboard-{kind}{h}"] = pg
            out["column"][f"peg_{kind}"] = {"face": pg["face"], "t": pg["t"], "w": pg["w"]}
    b1 = notes["backbone1"]
    out["column"].update({"rod_x": round(abs(b1["rods_x"][0]), 2), "rod_z": b1["rods_z"][0], "rod_d": 16, "lock_h": lk["h"],
                          "rest": pu["rest"], "rod_in": pu["rod_in"], "section": 52.0})
    notes.update({"lock": {k: v for k, v in lk.items() if k != "parts"}, "knobs": kn_notes, "stationary": st, "pullout": pu})
    return out, notes


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    path = sys.argv[1]
    pl = json.load(open(path, encoding="utf-8"))
    for w in sys.argv[2:] or ["S", "M", "L", "XL", "U"]:
        u, notes = column(w)
        u = {"name": f"{w} backbone column", **u}
        pl["units"][f"column|{w}"] = u
        print(w, json.dumps(u["column"]), flush=True)
        for k, v in notes.items():
            print("   ", k, json.dumps({a: b for a, b in v.items() if a not in ("m", "file")} if isinstance(v, dict) else v), flush=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pl, f, ensure_ascii=False, separators=(",", ":"))
