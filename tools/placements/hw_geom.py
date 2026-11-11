"""Bolt-hole measurement on an assembled unit (numpy + scipy, no Blender).

A unit is rebuilt from src/stl-placements.json and the decimated copy ($VAULT_RENDER, same coordinates as the
download): every part in the unit frame (three.js axes, mm). Holes are then found with depth maps and measured
with rays cast along their axis through the whole assembly. Used by hardware.py.
"""
import os, re
import numpy as np
import vault_geom as vg

ROOT = os.environ.get("VAULT_RENDER", "VAULT_RENDER")
_LOWER = None


def _norm(p):
    return re.sub(r"['’\s]", "", p.replace("┬▓", "²").lower())


def on_disk(rel):
    """The decimated copy keeps the unzip's spelling (┬▓ for ², odd spaces): find the file by the planner's norm."""
    global _LOWER
    if _LOWER is None:
        _LOWER = {}
        for d, _, fs in os.walk(ROOT):
            for f in fs:
                if f.lower().endswith(".stl"):
                    full = os.path.join(d, f)
                    _LOWER[_norm(os.path.relpath(full, ROOT).replace("\\", "/"))] = full
    return _LOWER.get(_norm(rel))


_CACHE = {}


def file_tris(rel):
    if rel not in _CACHE:
        p = on_disk(rel)
        if not p:
            raise FileNotFoundError(rel)
        _CACHE[rel] = vg.read_stl(p)
    return _CACHE[rel]


_PCACHE = {}


def piece_tris(rel, at):
    key = (rel, tuple(np.round(at, 2)))
    if key not in _PCACHE:
        ps = vg.pieces(file_tris(rel))
        _PCACHE[key] = min(ps, key=lambda t: np.linalg.norm(vg.piece_centre(t) - np.asarray(at)))
    return _PCACHE[key]


class Part:
    def __init__(self, i, entry):
        self.i = i
        self.path, self.role, self.group, m = entry[:4]
        self.piece = entry[4]["piece"] if len(entry) > 4 and entry[4] else None
        self.R, self.t = vg.mat34(m)
        src = piece_tris(self.path, self.piece) if self.piece else file_tris(self.path)
        self.tris = src @ self.R.T + self.t
        P = self.tris.reshape(-1, 3)
        self.lo, self.hi = P.min(0), P.max(0)

    @property
    def name(self):
        return self.path.rsplit("/", 1)[-1]


def load_unit(entry, only=None):
    """Parts of a unit in the unit frame. `only`: a function(path) -> bool to skip files (other variants)."""
    out = []
    for i, e in enumerate(entry["parts"]):
        if only and not only(e[0]):
            continue
        out.append(Part(i, e))
    return out


def ray_hits(tris, o, d, eps=1e-9):
    """Every crossing of the ray o + s d (s any sign) with the triangles: sorted list of (s, facing) where facing is
    -1 when the ray enters material (the triangle faces against d) and +1 when it leaves."""
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    e1, e2 = b - a, c - a
    p = np.cross(d, e2)
    det = (e1 * p).sum(1)
    ok = np.abs(det) > eps
    inv = np.where(ok, 1.0 / np.where(ok, det, 1), 0)
    s = o - a
    u = (s * p).sum(1) * inv
    q = np.cross(s, e1)
    v = (q * d).sum(1) * inv
    t = (e2 * q).sum(1) * inv
    hit = ok & (u >= -1e-7) & (v >= -1e-7) & (u + v <= 1 + 1e-7)
    n = np.cross(e1, e2)
    face = np.sign((n * d).sum(1))
    r = sorted(zip(t[hit].tolist(), face[hit].tolist()))
    # merge duplicates (a ray through a shared edge hits both triangles)
    out = []
    for s_, f in r:
        if out and abs(out[-1][0] - s_) < 1e-4 and out[-1][1] == f:
            continue
        out.append((s_, f))
    return out


def near(parts, o, d, r=12.0):
    """Parts whose bbox comes within r of the line o + s d."""
    out = []
    for p in parts:
        lo, hi = p.lo - r, p.hi + r
        # slab test of the infinite line against the inflated box
        t0, t1 = -1e9, 1e9
        ok = True
        for k in range(3):
            if abs(d[k]) < 1e-12:
                if not (lo[k] <= o[k] <= hi[k]):
                    ok = False
                    break
            else:
                a_, b_ = (lo[k] - o[k]) / d[k], (hi[k] - o[k]) / d[k]
                t0, t1 = max(t0, min(a_, b_)), min(t1, max(a_, b_))
        if ok and t0 <= t1:
            out.append(p)
    return out


def ortho(d):
    a = np.array([1.0, 0, 0]) if abs(d[0]) < 0.9 else np.array([0, 1.0, 0])
    u = np.cross(d, a)
    u /= np.linalg.norm(u)
    return u, np.cross(d, u)


def ring(parts, o, d, r, n=12, s_min=-1e9):
    """First hit beyond s_min of rays parallel to d at radius r around o, per part: {part index: [s...]}."""
    u, v = ortho(d)
    out = {}
    for k in range(n):
        a = 2 * np.pi * k / n
        oo = o + r * (np.cos(a) * u + np.sin(a) * v)
        for p in parts:
            h = [s for s, f in ray_hits(p.tris, oo, d) if s > s_min and f < 0]
            if h:
                out.setdefault(p.i, []).append(min(h))
    return out


def profile(parts, o, d, r=0.0, n=1):
    """Material along the axis (and rays at radius r): per part, the [enter, leave] intervals in s."""
    u, v = ortho(d)
    rays = [o] if r == 0 else [o + r * (np.cos(2 * np.pi * k / n) * u + np.sin(2 * np.pi * k / n) * v) for k in range(n)]
    out = {}
    for p in parts:
        ivs = []
        for oo in rays:
            h = ray_hits(p.tris, oo, d)
            cur = None
            for s, f in h:
                if f < 0 and cur is None:
                    cur = s
                elif f > 0 and cur is not None:
                    ivs.append((round(cur, 2), round(s, 2)))
                    cur = None
        if ivs:
            out[p.i] = ivs
    return out


def holes_in(part, axis, sign, step=0.25, area=(8, 40), window=None):
    """Round through holes of a part seen along a unit axis (0 x, 1 y, 2 z) from the sign side: centres in the unit
    frame (the coordinate along the axis is the part's surface there). window: (lo, hi) bounds to look in."""
    lo, hi = (part.lo, part.hi) if window is None else window
    D, u0, w0, (iu, iw) = vg.depthmap(part.tris, axis, sign, step, lo, hi)
    from scipy import ndimage
    nan = np.isnan(D)
    lab, n = ndimage.label(nan)
    out = []
    for k in range(1, n + 1):
        jj, ii = np.nonzero(lab == k)
        a = len(ii) * step * step
        if not (area[0] <= a <= area[1]):
            continue
        if ii.min() == 0 or jj.min() == 0 or ii.max() == D.shape[1] - 1 or jj.max() == D.shape[0] - 1:
            continue
        su, sw = step * (ii.max() - ii.min() + 1), step * (jj.max() - jj.min() + 1)
        if max(su, sw) > 1.6 * min(su, sw):
            continue  # slots, not holes
        c = np.zeros(3)
        c[iu], c[iw] = u0 + step * ii.mean(), w0 + step * jj.mean()
        c[axis] = part.hi[axis] if sign > 0 else part.lo[axis]
        out.append({"c": c, "d": round(2 * np.sqrt(a / np.pi), 2)})
    return out


def section(tris, axis, value):
    """Segments where the plane coord[axis] = value cuts the triangles: (n, 2, 3)."""
    d = tris[..., axis] - value
    out = []
    s = np.sign(d)
    cross = ~((s[:, 0] == s[:, 1]) & (s[:, 1] == s[:, 2]))
    T, D = tris[cross], d[cross]
    for t, dd in zip(T, D):
        pts = []
        for i in range(3):
            j = (i + 1) % 3
            if (dd[i] < 0) != (dd[j] < 0):
                f = dd[i] / (dd[i] - dd[j])
                pts.append(t[i] + f * (t[j] - t[i]))
        if len(pts) == 2:
            out.append(pts)
    return np.array(out).reshape(-1, 2, 3)


def section_png(parts, axis, value, path, window=None, bolts=(), title=""):
    """Cut of the assembly by the plane coord[axis] = value, each part its own colour; bolts drawn as their
    outline (list of (segments, colour)). window: ((u0, u1), (w0, w1)) in the plane's axes (u < w)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    iu, iw = [k for k in range(3) if k != axis]
    fig, ax = plt.subplots(figsize=(8, 8), dpi=110)
    cm = plt.get_cmap("tab10")
    for n, p in enumerate(parts):
        if p.lo[axis] > value or p.hi[axis] < value:
            continue
        S = section(p.tris, axis, value)
        if len(S):
            ax.add_collection(LineCollection(S[..., [iu, iw]], colors=[cm(n % 10)], linewidths=1.0, label=p.name[:28]))
    for segs, col in bolts:
        if len(segs):
            ax.add_collection(LineCollection(segs[..., [iu, iw]], colors=[col], linewidths=1.6))
    if window:
        ax.set_xlim(*window[0]); ax.set_ylim(*window[1])
    else:
        ax.autoscale()
    ax.set_aspect("equal")
    ax.set_xlabel("xyz"[iu]); ax.set_ylabel("xyz"[iw])
    ax.legend(fontsize=7, loc="upper right")
    ax.set_title(title or f"{'xyz'[axis]} = {value}")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
