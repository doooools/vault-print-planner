"""Geometry helpers for the placement tools (plain Python 3 + numpy + scipy, no Blender).

Frames:
  CAD frame  - the Vault files' own axes: X across, +Y to the front, Z up (mm).
  unit frame - three.js axes used by src/stl-placements.json: +X right seen from the front, +Y up,
               +Z towards the viewer; origin at the middle of the module's front bottom edge.
  C (CAD -> unit): x_u = -x_cad, y_u = z_cad, z_u = y_cad.
"""
import json, os
import numpy as np

C = np.array([[-1.0, 0, 0], [0, 0, 1], [0, 1, 0]])
_REC = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def read_stl(path):
    """Triangles as an (n, 3, 3) float64 array (binary or ASCII STL)."""
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        head = f.read(84)
    n = int.from_bytes(head[80:84], "little")
    if 84 + 50 * n == size:
        return np.fromfile(path, dtype=_REC, offset=84, count=n)["v"].astype(np.float64)
    pts = []
    with open(path, "r", errors="replace") as f:
        for line in f:
            s = line.strip()
            if s.startswith("vertex"):
                pts.append([float(x) for x in s.split()[1:4]])
    return np.array(pts, dtype=np.float64).reshape(-1, 3, 3)


def surface_samples(tris, k=40000, seed=0):
    """Area-weighted random points on the triangles."""
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    area = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)
    keep = area > 1e-9
    a, b, c, area = a[keep], b[keep], c[keep], area[keep]
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(area), size=k, p=area / area.sum())
    u, v = rng.random(k), rng.random(k)
    flip = u + v > 1
    u[flip], v[flip] = 1 - u[flip], 1 - v[flip]
    return a[idx] + (b[idx] - a[idx]) * u[:, None] + (c[idx] - a[idx]) * v[:, None]


def pieces(tris, tol=1e-3):
    """Connected pieces of a mesh (vertices welded at `tol` mm), largest first. Some Vault files
    hold several parts printed side by side (both leaves of a hinge, both racks of a drawer); a
    placement entry with {"piece": [x, y, z]} takes the piece whose bbox centre is nearest to that
    point, in the file's own coordinates (the decimated copy has the same pieces and centres)."""
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    q = np.round(tris.reshape(-1, 3) / tol).astype(np.int64)
    _, inv = np.unique(q, axis=0, return_inverse=True)
    inv = inv.reshape(-1, 3)
    n = int(inv.max()) + 1
    r, c = np.r_[inv[:, 0], inv[:, 1]], np.r_[inv[:, 1], inv[:, 2]]
    _, lab = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(n, n)), directed=False)
    tl = lab[inv[:, 0]]
    return sorted((tris[tl == i] for i in np.unique(tl)), key=len, reverse=True)


def piece_centre(t):
    P = t.reshape(-1, 3)
    return (P.min(0) + P.max(0)) / 2


def rot_axis(axis, deg):
    t = np.radians(deg)
    c, s = np.cos(t), np.sin(t)
    j, k = {"x": (1, 2), "y": (2, 0), "z": (0, 1)}[axis]  # right-handed: x->y->z->x
    R = np.eye(3)
    R[j, j], R[j, k], R[k, j], R[k, k] = c, -s, s, c
    return R


def euler_xyz(R):
    """Blender XYZ Euler (degrees) of a rotation matrix (R = Rz @ Ry @ Rx)."""
    from scipy.spatial.transform import Rotation
    return [round(float(a), 4) for a in Rotation.from_matrix(R).as_euler("xyz", degrees=True)]


def from_euler_xyz(e):
    return rot_axis("z", e[2]) @ rot_axis("y", e[1]) @ rot_axis("x", e[0])


def proper_rotations():
    """The 24 rotations that map the axes onto the axes."""
    out = []
    import itertools
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            M = np.zeros((3, 3))
            for r, (c, s) in enumerate(zip(perm, signs)):
                M[r, c] = s
            if np.linalg.det(M) > 0.5:
                out.append(M)
    return out


def best_tilt(pts):
    """Rotation about one of the file's axes that gives the smallest bounding box (parts printed at 45 deg)."""
    from scipy.spatial import ConvexHull
    try:
        h = pts[ConvexHull(pts).vertices]
    except Exception:
        h = pts
    def vol(P):
        e = P.max(0) - P.min(0)
        return e[0] * e[1] * e[2]
    best = (vol(h), "x", 0.0)
    for ax in "xyz":
        for t in np.arange(0.5, 90, 0.5):
            v = vol(h @ rot_axis(ax, t).T)
            if v < best[0] * 0.999:
                best = (v, ax, t)
    v0, ax, t0 = best
    if t0:
        for t in np.arange(t0 - 0.5, t0 + 0.5, 0.02):
            v = vol(h @ rot_axis(ax, t).T)
            if v < best[0]:
                best = (v, ax, t)
        # the parts are laid at round angles: take the nearest multiple of 15 deg when its box is
        # within 1% of the smallest (a part with a lip can have its smallest box a few degrees off)
        r = 15.0 * round(best[2] / 15.0)
        if r % 90 and vol(h @ rot_axis(ax, r).T) < best[0] * 1.01:
            best = (best[0], ax, r)
        elif abs(best[2] - round(best[2])) < 0.15:
            best = (best[0], ax, float(round(best[2])))
    return rot_axis(best[1], best[2]), best[1], best[2]


class Index:
    """_stl_index.jsonl: bbox and size of every original file."""
    def __init__(self, path):
        self.rows = {}
        for l in open(path, encoding="utf-8"):
            r = json.loads(l)
            self.rows[r["file"]] = r

    def bbox(self, rel):
        r = self.rows[rel]
        return np.array(r["bbox_min"]), np.array(r["bbox_max"])

    def has(self, rel):
        return rel in self.rows


def load_placements(path):
    return json.load(open(path, encoding="utf-8"))


def mat34(m):
    M = np.array(m, dtype=np.float64).reshape(3, 4)
    return M[:, :3], M[:, 3]


def depthmap(tris, axis, sign, step=0.25, lo=None, hi=None):
    """Z-buffer of triangles seen along an axis.

    axis: 0/1/2, the viewing axis; sign=+1 looks from +inf towards -inf along it (keeps the largest
    coordinate: the surface nearest to a viewer on the + side), sign=-1 the opposite.
    Returns (D, u0, w0, (u, w)) with D[j, i] the coordinate along `axis` of the first surface hit at
    u = u0 + i*step, w = w0 + j*step (u < w are the two other axes), NaN where the ray hits nothing.
    """
    u, w = [k for k in range(3) if k != axis]
    P = tris.reshape(-1, 3)
    lo = P.min(0) if lo is None else np.asarray(lo, float)
    hi = P.max(0) if hi is None else np.asarray(hi, float)
    u0, w0 = lo[u], lo[w]
    nu = int((hi[u] - u0) / step) + 1
    nw = int((hi[w] - w0) / step) + 1
    D = np.full((nw, nu), -np.inf)
    for tri in tris:
        a, b, c = tri
        umin, umax = min(a[u], b[u], c[u]), max(a[u], b[u], c[u])
        wmin, wmax = min(a[w], b[w], c[w]), max(a[w], b[w], c[w])
        i0, i1 = int(np.ceil((umin - u0) / step)), int(np.floor((umax - u0) / step))
        j0, j1 = int(np.ceil((wmin - w0) / step)), int(np.floor((wmax - w0) / step))
        i0, j0 = max(i0, 0), max(j0, 0)
        i1, j1 = min(i1, nu - 1), min(j1, nw - 1)
        if i1 < i0 or j1 < j0:
            continue
        uu = u0 + step * np.arange(i0, i1 + 1)
        ww = w0 + step * np.arange(j0, j1 + 1)
        U, W = np.meshgrid(uu, ww)
        x1, y1, x2, y2, x3, y3 = a[u], a[w], b[u], b[w], c[u], c[w]
        den = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        if abs(den) < 1e-12:
            continue
        l1 = ((y2 - y3) * (U - x3) + (x3 - x2) * (W - y3)) / den
        l2 = ((y3 - y1) * (U - x3) + (x1 - x3) * (W - y3)) / den
        l3 = 1 - l1 - l2
        ins = (l1 >= -1e-9) & (l2 >= -1e-9) & (l3 >= -1e-9)
        if not ins.any():
            continue
        z = l1 * a[axis] + l2 * b[axis] + l3 * c[axis]
        z = z if sign > 0 else -z
        blk = D[j0:j1 + 1, i0:i1 + 1]
        np.maximum(blk, np.where(ins, z, -np.inf), out=blk)
    D[np.isinf(D)] = np.nan
    if sign < 0:
        D = -D
    return D, u0, w0, (u, w)


def regions(mask, D, u0, w0, step, min_area=1.0):
    """Connected regions of a boolean grid: centre (u, w), size, area, mean depth."""
    from scipy import ndimage
    lab, n = ndimage.label(mask)
    out = []
    for k in range(1, n + 1):
        jj, ii = np.nonzero(lab == k)
        area = len(ii) * step * step
        if area < min_area:
            continue
        border = ii.min() == 0 or jj.min() == 0 or ii.max() == mask.shape[1] - 1 or jj.max() == mask.shape[0] - 1
        dv = D[jj, ii]
        dv = dv[~np.isnan(dv)]
        out.append({"u": round(u0 + step * ii.mean(), 2), "w": round(w0 + step * jj.mean(), 2),
                    "su": round(step * (ii.max() - ii.min() + 1), 2), "sw": round(step * (jj.max() - jj.min() + 1), 2),
                    "area": round(area, 1), "depth": round(float(dv.mean()), 2) if len(dv) else None,
                    "border": bool(border)})
    return sorted(out, key=lambda r: -r["area"])


def posed(rel, R_unit, root):
    """Triangles of a file turned by R_unit (unit frame) and set with their bbox centre at the origin."""
    t = read_stl(os.path.join(root, rel))
    P = t.reshape(-1, 3)
    c = (P.min(0) + P.max(0)) / 2
    return (t - c) @ np.asarray(R_unit).T


def depth_png(D, path, scale=3, flip=True):
    """Grey depth image (light = near the viewer), red where nothing is hit."""
    from PIL import Image
    v = D[~np.isnan(D)]
    lo, hi = np.percentile(v, 1), np.percentile(v, 99)
    t = np.clip((D - lo) / (hi - lo + 1e-9), 0, 1)
    g = (30 + 225 * np.nan_to_num(t)).astype(np.uint8)
    rgb = np.stack([g, g, g], -1)
    rgb[np.isnan(D)] = (200, 30, 30)
    if flip:
        rgb = rgb[::-1]
    Image.fromarray(rgb).resize((D.shape[1] * scale, D.shape[0] * scale), Image.NEAREST).save(path)
