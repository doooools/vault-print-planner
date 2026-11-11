"""Opening and closing a unit, from src/stl-placements.json ("motion", README "Motion"), as the page does it, and a
check that no part goes through another on the way.

  python -I kinematics.py check <placements.json> <vault download> <unit key> [...] [--steps 41] [--hidden]
  python -I kinematics.py pose <placements.json> <unit key> <t>        (prints each moving part's matrix at t)

t runs from 0 (closed: a drawer locked, a case latched) to 1 (open), through the unit's steps. `check` poses the
unit's parts (as a part list would draw them: one baseplate, the key lock or with --hidden the hidden key) at
`steps` values of t, cuts them by planes across the motion (a drawer: planes z = const through the key and racks,
whose motion is in those planes, and y = const through the drawer; a case: planes x = const through each latch),
and reports, for every pair of parts of which one moves, the largest overlap of their sections (mm^2) with where
it happens, next to the overlap when closed (t = 0). An overlap that is there when closed and doesn't grow is how
the parts are placed (a preload, or a small error), not the motion.

The pose maths (no Blender, no shapely) is shared with blender_motion.py; `check` needs numpy, scipy and shapely.
Files are read from the download (small parts) or from $VAULT_RENDER, the decimated copy (modules, boxes, lids).
"""
import json, math, os, re, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------- pose (same as the page's v3pose)
def joint_values(steps, t):
    """Each joint's value at t: every step takes its share of the time ("s"), eased in and out (smoothstep)."""
    total = sum(s.get("s", 0.5) for s in steps)
    out, a = {}, 0.0
    for s in steps:
        b = a + s.get("s", 0.5) / total
        w = min(1.0, max(0.0, (t - a) / (b - a)))
        w = w * w * (3 - 2 * w)
        for j in s["joints"]:
            out[j] = s["from"] + (s["to"] - s["from"]) * w
        a = b
    return out


def _rot2(p, c, deg):
    t = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(t) - y * math.sin(t), c[1] + x * math.sin(t) + y * math.cos(t))


def _ang2(v):
    return math.degrees(math.atan2(v[1], v[0]))


class Latch:
    """A case's toggle latch in its plane (u = z, v = y of the unit frame; angles right-handed about the latch's
    axis, -X). Phase 1: the link turns about A by phi, carrying the pin B; the tooth C slides along `slide`
    (an inverted slider-crank, through the toggle's dead centre) until it has slid `out` mm. Phase 2: the link goes
    on to `phi`, the lever (on B) turns to `theta`, together, linear."""

    def __init__(self, l):
        zy = lambda p: (p[2], p[1])
        self.A, self.B0, self.C0, sl = zy(l["A"]), zy(l["B"]), zy(l["C"]), zy(l["slide"])
        n = math.hypot(*sl)
        self.d = (sl[0] / n, sl[1] / n)
        self.len = math.hypot(self.C0[0] - self.B0[0], self.C0[1] - self.B0[1])
        self.out, self.phi2, self.theta2, self.split = l["out"], l["phi"], l["theta"], l.get("split", 0.5)
        self.x = l["A"][0]
        self.phi1 = 90.0
        phi = 0.05
        while phi < 150:
            s = self.slid(phi)
            if s is None:
                break
            if phi > 1 and s >= self.out:
                self.phi1 = phi
                break
            phi += 0.05
        self.theta1 = self.phase1(self.phi1)[2]

    def slid(self, phi):
        B = _rot2(self.B0, self.A, phi)
        dx, dy = self.C0[0] - B[0], self.C0[1] - B[1]
        du = dx * self.d[0] + dy * self.d[1]
        disc = du * du - dx * dx - dy * dy + self.len ** 2
        return None if disc < 0 else -du + math.sqrt(disc)

    def phase1(self, phi):
        B = _rot2(self.B0, self.A, phi)
        s = self.slid(phi) or 0.0
        C = (self.C0[0] + s * self.d[0], self.C0[1] + s * self.d[1])
        return phi, B, _ang2((C[0] - B[0], C[1] - B[1])) - _ang2((self.C0[0] - self.B0[0], self.C0[1] - self.B0[1]))

    def pose(self, s):
        """(phi, B (z, y), theta) at s in [0, 1]"""
        if s <= self.split:
            return self.phase1(self.phi1 * s / self.split)
        w = (s - self.split) / (1 - self.split)
        phi = self.phi1 + (self.phi2 - self.phi1) * w
        return phi, _rot2(self.B0, self.A, phi), self.theta1 + (self.theta2 - self.theta1) * w


def _T(v):
    M = np.eye(4)
    M[:3, 3] = v
    return M


def _R(axis, deg):
    a = np.asarray(axis, float)
    a = a / np.linalg.norm(a)
    t = math.radians(deg)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    M = np.eye(4)
    M[:3, :3] = np.eye(3) + math.sin(t) * K + (1 - math.cos(t)) * K @ K
    return M


def _about(origin, axis, deg):
    o = np.asarray(origin, float)
    return _T(o) @ _R(axis, deg) @ _T(-o)


def travel_of(unit):
    """How far the page pulls a drawer out: 0.6 x its depth (the page uses the published depth; the bbox's is the
    same within a few mm)."""
    lo, hi = unit["bbox"]
    return round((hi[2] - lo[2]) * 0.6)


def part_matrix(unit, part, t, latches=None, travel=None):
    """4x4 matrix: the file's coordinates -> the unit frame, with the unit opened to t."""
    m = np.array(part[3], float).reshape(3, 4)
    M = np.vstack([m, [0, 0, 0, 1]])
    motion = unit.get("motion") or {}
    steps = motion.get("open") or [{"joints": ["drawer" if part[2] == "drawer" else "lid"], "from": 0, "to": 1, "s": 1}]
    val = joint_values(steps, t)
    joint = part[4].get("joint") if len(part) > 4 else None
    if joint:
        jid, body = (joint.split(".") + [None])[:2]
        j = motion["joints"][jid]
        s = val.get(jid, 0.0)
        if "turn" in j:
            M = _about(j["turn"]["origin"], j["turn"]["axis"], s * j["turn"]["deg"]) @ M
        elif "slide" in j:
            M = _T(np.array(j["slide"], float) * s) @ M
        elif "latch" in j:
            L = (latches or {}).get(jid) or Latch(j["latch"])
            phi, B, theta = L.pose(s)
            ax = j["latch"]["axis"]
            if body == "link":
                M = _about(j["latch"]["A"], ax, phi) @ M
            else:
                B0 = np.array(j["latch"]["B"], float)
                M = _T([B0[0], B[1], B[0]]) @ _R(ax, theta) @ _T(-B0) @ M
    if part[2] == "drawer":
        M = _T([0, 0, (travel if travel is not None else travel_of(unit)) * val.get("drawer", 0.0)]) @ M
    elif part[2] == "lid" and unit.get("hinge"):
        h = unit["hinge"]
        M = _about(h["origin"], h["axis"], h["open_deg"] * val.get("lid", 0.0)) @ M
    return M


def moves(part):
    return part[2] in ("drawer", "lid") or (len(part) > 4 and "joint" in part[4])


# ---------------------------------------------------------------- check
SKIP_DEFAULT = r"Baseplate_With|Hidden Key"      # one baseplate, the key lock (a part list names one variant)
SKIP_HIDDEN = r"Baseplate_With|/Key \(|Key Cap"
BIG = 3e6                                        # bytes: bigger files are read from the decimated copy


def load_tris(path, download, piece=None, _cache={}):
    import vault_geom as vg
    dec = os.environ.get("VAULT_RENDER")
    for p in (path, path.replace("²", "┬▓")):
        f = os.path.join(download, p)
        if os.path.exists(f):
            break
    if dec and os.path.getsize(f) > BIG:
        for p in (path, path.replace("²", "┬▓")):
            g = os.path.join(dec, p)
            if os.path.exists(g):
                f = g
                break
    if f not in _cache:
        _cache[f] = vg.read_stl(f)
    T = _cache[f]
    if piece is not None:
        k = (f, "pieces")
        if k not in _cache:
            _cache[k] = vg.pieces(T)
        T = min(_cache[k], key=lambda q: np.linalg.norm(vg.piece_centre(q) - np.array(piece)))
    return T


def section(T, axis, value):
    """Segments where the plane coord[axis] == value cuts the triangles T (n, 3, 3), as (m, 2, 3). Shared edges
    are cut in one order, so neighbouring triangles give the same point."""
    d = T[:, :, axis] - value
    pos = d > 0
    cross = ~(pos.all(1) | (~pos).all(1))
    T, d = T[cross], d[cross]
    out = []
    for i, j in ((0, 1), (1, 2), (2, 0)):
        a, b, da, db = T[:, i], T[:, j], d[:, i], d[:, j]
        swap = (a[:, 0] > b[:, 0]) | ((a[:, 0] == b[:, 0]) & ((a[:, 1] > b[:, 1]) | ((a[:, 1] == b[:, 1]) & (a[:, 2] > b[:, 2]))))
        a2, b2 = np.where(swap[:, None], b, a), np.where(swap[:, None], a, b)
        da2, db2 = np.where(swap, db, da), np.where(swap, da, db)
        ok = (da2 > 0) != (db2 > 0)
        f = np.where(ok, da2 / np.where(ok, da2 - db2, 1), 0)
        out.append((ok, a2 + f[:, None] * (b2 - a2)))
    segs = []
    oks = np.stack([o for o, _ in out], 1)
    pts = np.stack([p for _, p in out], 1)
    two = oks.sum(1) == 2
    for row_ok, row_p in zip(oks[two], pts[two]):
        segs.append(row_p[row_ok])
    return np.array(segs).reshape(-1, 2, 3)


def polygon(S, uv):
    """Section segments -> the solid region (shapely), even-odd over the closed loops."""
    from shapely.geometry import MultiLineString, Polygon
    from shapely.ops import polygonize, unary_union
    if not len(S):
        return Polygon()
    ml = MultiLineString([[(round(p[uv[0]], 4), round(p[uv[1]], 4)), (round(q[uv[0]], 4), round(q[uv[1]], 4))] for p, q in S])
    out = Polygon()
    for p in sorted(polygonize(unary_union(ml)), key=lambda p: -p.area):
        out = out.symmetric_difference(Polygon(p.exterior))
    return out.buffer(0)


def planes(key, unit):
    """Cutting planes (axis, value, joints it watches: None for all) across the unit's motion."""
    kind = key.split("|")[0]
    js = (unit.get("motion") or {}).get("joints", {})
    if kind == "drawer":
        lock = set(js)
        zs = [(2, z, lock) for z in np.arange(-8.37, 24.8, 0.7)]          # key, racks (their motion is in these)
        keys = [j["turn"]["origin"] for j in js.values() if "turn" in j]
        ys = [(1, y, {"drawer"}) for o in keys[:1] for y in (o[1] - 13.5, o[1], o[1] + 13.5)]   # the drawer's slide
        return zs + ys
    xs = []
    for j in js.values():
        if "latch" in j:
            x0 = j["latch"]["A"][0]
            xs += [(0, x0 + dx + 0.013, None) for dx in np.arange(-25.0, 25.1, 2.5)]
    return xs


def check(pl, download, key, steps=41, hidden=False, quiet=False):
    unit = pl["units"][key]
    skip = SKIP_HIDDEN if hidden else SKIP_DEFAULT
    parts = [p for p in unit["parts"] if not re.search(skip, p[0])]
    tris = [load_tris(p[0], download, p[4].get("piece") if len(p) > 4 else None) for p in parts]
    latches = {jid: Latch(j["latch"]) for jid, j in (unit.get("motion") or {}).get("joints", {}).items() if "latch" in j}
    travel = travel_of(unit)
    names = [os.path.basename(p[0]) + (f" [{p[4]['joint']}]" if len(p) > 4 and "joint" in p[4] else "")
             + (f" <{p[4].get('side', '')}{p[4]['drawer']}>" if len(p) > 4 and "drawer" in p[4] else "") for p in parts]
    mov = [moves(p) for p in parts]
    pls = planes(key, unit)
    worst, base = {}, {}
    static, ssec = {}, {}
    for k, (p, T) in enumerate(zip(parts, tris)):
        if not mov[k]:
            M = part_matrix(unit, p, 0.0)
            static[k] = T @ M[:3, :3].T + M[:3, 3]

    def cut(P, ax, v, uv):
        lo, hi = P[:, :, ax].min(), P[:, :, ax].max()
        return polygon(section(P, ax, v), uv) if lo < v < hi else None

    for ax, v, _ in pls:   # the parts that stay are cut once
        uv = [i for i in range(3) if i != ax]
        ssec[(ax, v)] = {k: g for k, P in static.items() for g in [cut(P, ax, v, uv)] if g is not None and not g.is_empty}
    last, prev = None, None
    msteps = (unit.get("motion") or {}).get("open") or [{"joints": ["drawer", "lid"], "from": 0, "to": 1, "s": 1}]
    for t in np.linspace(0, 1, steps):
        val = joint_values(msteps, t)
        moving = None if prev is None else {j for j in val if abs(val[j] - prev.get(j, 0)) > 1e-9}
        prev = val
        posed, rel = {}, {}
        for k, (p, T) in enumerate(zip(parts, tris)):
            if mov[k]:
                M = part_matrix(unit, p, t, latches, travel)
                posed[k] = T @ M[:3, :3].T + M[:3, 3]
                rel[k] = M @ np.linalg.inv(part_matrix(unit, p, 0.0))   # how it moved since closed
        sig = {k: np.round(P[0, 0], 4).tobytes() for k, P in posed.items()}
        if sig == last:
            continue   # nothing moved since the last step (a step that moves none of these parts)
        last = sig
        for ax, v, watch in pls:
            if moving is not None and watch is not None and not (watch & moving):
                continue
            uv = [i for i in range(3) if i != ax]
            secs = dict(ssec[(ax, v)])
            for k, P in posed.items():
                g = cut(P, ax, v, uv)
                if g is not None and not g.is_empty:
                    secs[k] = g
            ks = sorted(secs)
            for i, a in enumerate(ks):
                for b in ks[i + 1:]:
                    if not (mov[a] or mov[b]) or (a in rel and b in rel and np.allclose(rel[a], rel[b], atol=1e-6)
                                                  and not np.allclose(rel[a], np.eye(4), atol=1e-6)):
                        continue   # neither moves, or both move as one (a key and its cap): the plane, not them
                    if not secs[a].bounds or secs[a].distance(secs[b]) > 0:
                        continue
                    ar = secs[a].intersection(secs[b]).area
                    pair = (names[a], names[b])
                    if t == 0:
                        base[pair] = max(base.get(pair, 0), ar)
                    if ar > worst.get(pair, (0.02,))[0]:
                        worst[pair] = (ar, t, "xyz"[ax], v)
    res = []
    for pair, (ar, t, ax, v) in sorted(worst.items(), key=lambda kv: -kv[1][0]):
        b0 = base.get(pair, 0.0)
        res.append({"pair": pair, "max": round(ar, 2), "t": round(t, 3), "plane": f"{ax}={v:.2f}", "closed": round(b0, 2),
                    "new": ar > b0 + 0.1})
    if not quiet:
        print(key, f"({len(pls)} planes, {steps} steps)")
        for r in res:
            print("  %-4s %6.2f mm2 at t=%.2f %-10s (closed %5.2f)  %s | %s" % ("NEW" if r["new"] else "", r["max"], r["t"], r["plane"], r["closed"], *r["pair"]))
        if not res:
            print("  nothing overlaps")
    return res


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "check":
        st = int(a[a.index("--steps") + 1]) if "--steps" in a else 41
        keys = [k for k in a[3:] if "|" in k]
        pl = json.load(open(a[1], encoding="utf-8"))
        sys.stdout.reconfigure(encoding="utf-8")
        for k in keys:
            check(pl, a[2], k, st, hidden="--hidden" in a)
    elif a and a[0] == "pose":
        pl = json.load(open(a[1], encoding="utf-8"))
        u = pl["units"][a[2]]
        for p in u["parts"]:
            if moves(p):
                print(os.path.basename(p[0]), np.round(part_matrix(u, p, float(a[3]))[:3], 3).tolist())
    else:
        print(__doc__)
