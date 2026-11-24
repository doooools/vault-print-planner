"""A later Vault delivery against the first one: which files the page reads moved, turned or got renamed, and the
matrix that brings each back into the first delivery's coordinates (src/stl-revisions.json).

    python -I tools/placements/revisions.py <first download> <new download> <delivery date> [--write]

Every measurement and placement in src/ was taken on the first delivery (2026-10-21). USSA re-exports some files in a
later one from elsewhere in their CAD scene, often turned (L 1F modules flat instead of at 45 degrees…), and renames a
few. For each file src/ names (stl-measurements.tsv, stl-placements.json) that differs in the new download, this fits
the new file onto the old one (area-weighted surface samples; every axis turn and 45-degree turn as a start; trimmed
point-to-plane ICP) and records { file (new path, when the page wouldn't find it by the old one), size (its bytes),
fix (3x4, new -> old, mm) }. The page applies fix to a file of that size as it reads it (partFile in template.html).

How good a fit is: `ratio` = median distance from the new samples to the old ones over the same for two halves of the
old sample. Two samples of one surface give ~0.71 (1/sqrt 2); clearly above, the part changed shape (a retouch) or the
fit is wrong: look at it. Needs numpy and scipy. Writes numbers only, never geometry (CLAUDE.md "Hard rules").
"""
import itertools, json, os, re, sys, unicodedata
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Rot

ROOT = Path(__file__).resolve().parents[2] / "src"
# Renames the page's own lookup (findFile: exact, end of path, letters and digits only, same name elsewhere) misses
RENAMES = [(r" 1F Module \.stl$", " 1F Module_Sustainer.stl"), (r"/(M2F|M4f) Facade\.stl$", lambda m: f"/{m[1].upper()} Facade_Sustainer.stl"),
           (r"Heavyweight Roof Cut\.stl$", "Heawyweight Roof (Cut to fit on a plate).stl")]
REC = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])

def listing(root):
    out = {}
    for r, _, fs in os.walk(root):
        for f in fs:
            if f.lower().endswith(".stl") and not f.startswith("._"):
                p = os.path.join(r, f); out[os.path.relpath(p, root).replace(os.sep, "/").replace("┬▓", "²")] = p
    return out
loose = lambda s: re.sub(r"[^a-z0-9/]+", "", unicodedata.normalize("NFC", s).lower())
same = lambda s: re.sub(r" ?\.stl$", "", re.sub(r"\s+", " ", unicodedata.normalize("NFC", s.split("/")[-1]).lower()))
def finder(files):
    names = {}
    for f in files: names[same(f)] = None if same(f) in names else f
    lp = [("/" + loose(f), f) for f in files]
    def find(p):  # the page's findFile, on relative paths
        if p in files: return p
        for f in files:
            if f.endswith("/" + p): return f
        tail = "/".join(p.split("/")[1:])
        if tail in files: return tail
        for q in (loose(p), loose(tail)):
            if q:
                for k, f in lp:
                    if k.endswith("/" + q): return f
        return names.get(same(p))
    return find
def tris(p):
    size = os.path.getsize(p); n = int.from_bytes(open(p, "rb").read(84)[80:84], "little")
    if 84 + 50 * n != size: raise SystemExit(f"not a binary STL: {p}")
    return np.fromfile(p, dtype=REC, offset=84)["v"].astype(np.float64)
def sample(t, k=80000, seed=7):
    rng = np.random.default_rng(seed)
    a = np.linalg.norm(np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]), axis=1) / 2
    i = rng.choice(len(t), size=k, p=a / a.sum()); u, w = rng.random(k), rng.random(k); m = u + w > 1; u[m], w[m] = 1 - u[m], 1 - w[m]
    return t[i, 0] + u[:, None] * (t[i, 1] - t[i, 0]) + w[:, None] * (t[i, 2] - t[i, 0])

def _starts():
    sp = []
    for perm in itertools.permutations(range(3)):
        for s in itertools.product([1, -1], repeat=3):
            M = np.zeros((3, 3))
            for i, j in enumerate(perm): M[i, j] = s[i]
            if np.linalg.det(M) > 0: sp.append(M)
    ex = [np.eye(3)] + [Rot.from_euler(ax, d, degrees=True).as_matrix() for ax in "xyz" for d in (45, -45)]
    out = {}
    for B in sp:
        for E in ex:
            for F in ex:
                R = F @ B @ E; q = Rot.from_matrix(R).as_quat(); q = q if q[3] >= 0 else -q
                out[tuple(np.round(q, 6))] = R
    return sp, list(out.values())
SP, AX = _starts()
def _pca(P):
    V = np.linalg.eigh(np.cov((P - P.mean(0)).T))[1]
    if np.linalg.det(V) < 0: V[:, 0] *= -1
    return V
def fit(new, old):
    """R, t with old ~ R new + t"""
    rng = np.random.default_rng(1); tree = cKDTree(old)
    _, j = tree.query(old, 12); Q = old[j] - old[j].mean(1, keepdims=True)
    w, V = np.linalg.eigh(np.einsum('nki,nkj->nij', Q, Q)); nrm, flat = V[:, :, 0], w[:, 0] / np.maximum(w.sum(1), 1e-12)
    cn, co = new.mean(0), old.mean(0); sn = new[rng.choice(len(new), 3000, replace=False)]
    sc = []
    for R in AX + [_pca(old) @ S @ _pca(new).T for S in SP]:
        t = co - R @ cn; d, _ = tree.query(sn @ R.T + t, distance_upper_bound=20); sc.append((np.mean(np.minimum(d, 20)), R, t))
    sc.sort(key=lambda x: x[0]); best = None
    for _, R, t in sc[:8]:
        s0 = new[rng.choice(len(new), 25000, replace=False)]
        for _ in range(80):
            q = s0 @ R.T + t; dd, j = tree.query(q)
            k = (dd < max(np.percentile(dd, 85), 0.3)) & (flat[j] < 0.02); n = nrm[j[k]]
            x = np.linalg.lstsq(np.c_[np.cross(q[k], n), n], np.einsum('ij,ij->i', n, old[j[k]] - q[k]), rcond=None)[0]
            dR = Rot.from_rotvec(x[:3]).as_matrix(); R, t = dR @ R, dR @ t + x[3:]
            if np.linalg.norm(x) < 1e-8: break
        U, _, Vt = np.linalg.svd(R); R = U @ Vt
        d = float(np.median(tree.query(new @ R.T + t)[0]))
        if best is None or d < best[0]: best = (d, R, t)
    h = len(old) // 2; base = float(np.median(cKDTree(old[:h]).query(old[h:])[0]))
    return best[1], best[2], best[0] / base

def main(a, b, date, write):
    paths = {l.split("\t")[0] for l in (ROOT / "stl-measurements.tsv").read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")}
    def walk(x):
        if isinstance(x, str) and x.lower().endswith(".stl"): paths.add(x)
        elif isinstance(x, dict): [walk(v) for v in x.values()]; [walk(k) for k in x]
        elif isinstance(x, list): [walk(v) for v in x]
    walk(json.loads((ROOT / "stl-placements.json").read_text(encoding="utf-8")))
    old, new = listing(a), listing(b); fo, fn = finder(old), finder(new)
    out_f = ROOT / "stl-revisions.json"
    doc = json.loads(out_f.read_text(encoding="utf-8")) if out_f.exists() else {"note": "", "deliveries": {}, "files": {}}
    doc["deliveries"][date] = os.path.basename(os.path.normpath(b))
    for p in sorted(paths):
        o = fo(p)
        if not o: print("not in the first download:", p); continue
        n = fn(p); renamed = False
        if not n:
            for pat, rep in RENAMES:
                q = re.sub(pat, rep, p)
                if q != p and fn(q): n, renamed = fn(q), True; break
        if not n: print("GONE:", p); continue
        po, pn = old[o], new[n]
        if os.path.getsize(po) == os.path.getsize(pn) and open(po, "rb").read()[84:] == open(pn, "rb").read()[84:]:
            entry = {}
        else:
            so = sample(tris(po)); R, t, ratio = fit(sample(tris(pn)), so)
            if ratio > 0.8:  # not the same part: USSA swapped names (XL6/XL7 Box 1F Part 1 and 2, 2026-11-18)? try its neighbours
                for q in sorted(f for f in new if f.rsplit("/", 1)[0] == n.rsplit("/", 1)[0] and f != n):
                    R2, t2, r2 = fit(sample(tris(new[q])), so)
                    if r2 < ratio: n, pn, R, t, ratio, renamed = q, new[q], R2, t2, r2, True
            ang = float(np.degrees(np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1))))
            print(f"{p.split('/')[-1][:40]:40s} turned {ang:5.1f}  moved {np.linalg.norm(t):8.1f}  ratio {ratio:.2f}" + ("  CHECK" if ratio > 0.8 else ""), flush=True)
            entry = {"size": os.path.getsize(pn), "ratio": round(ratio, 2)}
            if ang > 0.01 or np.linalg.norm(t) > 0.15:  # closer than that is the fit's own scatter: the same place
                entry["fix"] = [round(float(v), 7 if c < 3 else 4) for r in np.c_[R, t] for c, v in enumerate(r)]
        if renamed: entry["file"] = n
        if entry.get("fix") or entry.get("file"):
            rs = [r for r in doc["files"].get(p, []) if r.get("delivery") != date]
            doc["files"][p] = rs + [{"delivery": date, **entry}]
    if write: out_f.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
if __name__ == "__main__":
    args = [x for x in sys.argv[1:] if x != "--write"]
    if len(args) != 3: raise SystemExit(__doc__)
    main(*args, "--write" in sys.argv)
