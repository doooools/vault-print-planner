"""Find how a part is turned in the assembly, by comparing its corners with a part already placed.

  python orient.py <jobs.json> <out.json>

jobs.json: [{"target": "rel/path.stl", "ref": "rel/path.stl", "ref_m": [12 numbers]}, ...]
  ref_m is the reference's matrix from stl-placements.json (file coordinates -> unit frame).
  Optional per job: "win" (mm, default 30), "corners" ([[cx, cy, cz], ...], 0 = min, 1 = max, unit frame),
  "tilt" (false to skip the 45 deg search).
  Files are read from $VAULT_RENDER (decimated copy, same coordinates as the download).

The parts are exported in print orientation: turned by quarter turns, sometimes also by 45 deg about
one axis. The solver
  1. finds that tilt (smallest bounding box over rotations about the file's x, y or z axis);
  2. tries the 24 quarter-turn orientations of the untilted part;
  3. for each, sets every corner of its bounding box on the same corner of the reference, refines that
     with a few point-to-plane steps, and counts the target's surface samples within `win` mm of the
     corner that lie on the reference's surface (closer than 0.2 mm to its tangent plane, facing the same
     way). Same-design parts of another width, depth or height share their corners, so the right
     orientation matches most samples; a part turned upside down matches its flat walls only.
Output per target: rot (and "alts", the six best with their scores) (Blender XYZ Euler, degrees, CAD frame, as in the recipes), the unit-frame
rotation, the score (share of samples that do not match, 0 = perfect) and the runner-up's. A ratio
next/score under ~1.3 means the answer needs a look.
"""
import json, os, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vault_geom as vg  # noqa: E402

ROOT = os.environ.get("VAULT_RENDER", "VAULT_RENDER")


def samples_n(tris, k, seed):
    """Area-weighted surface samples with their face normals."""
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    n = np.cross(b - a, c - a)
    ar = np.linalg.norm(n, axis=1)
    keep = ar > 1e-9
    a, b, c, n, ar = a[keep], b[keep], c[keep], n[keep] / ar[keep, None], ar[keep]
    r = np.random.default_rng(seed)
    i = r.choice(len(ar), k, p=ar / ar.sum())
    u, v = r.random(k), r.random(k)
    f = u + v > 1
    u[f], v[f] = 1 - u[f], 1 - v[f]
    return a[i] + (b[i] - a[i]) * u[:, None] + (c[i] - a[i]) * v[:, None], n[i]


def corners_score(Q, NQ, ref, NR, tree, win=30.0, tol=0.2, corners=None):
    qlo, qhi = Q.min(0), Q.max(0)
    rlo, rhi = ref.min(0), ref.max(0)
    out = []
    for cx in (0, 1):
        for cy in (0, 1):
            for cz in (0, 1):
                sel = (cx, cy, cz)
                if corners is not None and sel not in corners:
                    continue
                qc = np.array([(qlo, qhi)[s][i] for i, s in enumerate(sel)])
                rc = np.array([(rlo, rhi)[s][i] for i, s in enumerate(sel)])
                Qs = Q - qc + rc
                mq = np.all(np.abs(Qs - rc) < win, axis=1)
                if mq.sum() < 30:
                    continue
                q, nq = Qs[mq], NQ[mq]
                for _ in range(5):
                    d, i = tree.query(q)
                    m = (d < 3) & (np.einsum("ij,ij->i", nq, NR[i]) > 0.8)
                    if m.sum() < 20:
                        break
                    A = NR[i[m]]
                    t = np.linalg.lstsq(A, np.einsum("ij,ij->i", ref[i[m]] - q[m], A), rcond=None)[0]
                    q = q + t
                d, i = tree.query(q)
                pp = np.abs(np.einsum("ij,ij->i", q - ref[i], NR[i]))
                ok = (d < 3) & (pp < tol) & (np.einsum("ij,ij->i", nq, NR[i]) > 0.9)
                out.append(ok.mean())
    return 1 - float(np.mean(out)) if out else 1.0


def solve(target, ref, ref_m, win=30.0, corners=None, tilt=True, n=60000):
    tt = vg.read_stl(os.path.join(ROOT, target))
    P, NP_ = samples_n(tt, n, 1)
    P = P - (P.min(0) + P.max(0)) / 2
    rt = vg.read_stl(os.path.join(ROOT, ref))
    Rr, tr = vg.mat34(ref_m)
    Rp, NR = samples_n(rt, 2 * n, 2)
    Rp, NR = Rp @ Rr.T + tr, NR @ Rr.T
    tree = cKDTree(Rp)
    if tilt:
        T, ax, ang = vg.best_tilt(tt.reshape(-1, 3)[:: max(1, len(tt) * 3 // 200000)])
    else:
        T, ax, ang = np.eye(3), "x", 0.0
    res = []
    for G in vg.proper_rotations():
        R = G @ T
        res.append((corners_score(P @ R.T, NP_ @ R.T, Rp, NR, tree, win, corners=corners), R))
    res.sort(key=lambda r: r[0])
    (s0, R0), (s1, _) = res[0], res[1]
    return {"target": target, "ref": ref, "rot": vg.euler_xyz(vg.C.T @ R0), "R_unit": np.round(R0, 6).tolist(),
            "tilt": [ax, round(float(ang), 2)], "score": round(s0, 3), "next": round(s1, 3),
            "ratio": round(s1 / max(s0, 1e-3), 2),
            "alts": [[vg.euler_xyz(vg.C.T @ R), round(sc, 3)] for sc, R in res[:6]]}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # paths hold ² (python -I ignores PYTHONIOENCODING)
    jobs = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    done = json.load(open(out, encoding="utf-8")) if os.path.exists(out) else {}
    for j in jobs:
        key = j["target"] + "|" + j["ref"]
        if key in done and not j.get("redo"):
            continue
        r = solve(j["target"], j["ref"], j["ref_m"], j.get("win", 30.0),
                  corners=[tuple(c) for c in j["corners"]] if j.get("corners") else None, tilt=j.get("tilt", True))
        done[key] = r
        print("ORIENT", r["target"].split("/")[-1], r["rot"], "tilt", r["tilt"], "score", r["score"],
              "next", r["next"], "ratio", r["ratio"], flush=True)
        json.dump(done, open(out, "w", encoding="utf-8"), indent=0, ensure_ascii=False)
