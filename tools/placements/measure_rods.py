"""A case's hinge rods (02. SUSTAINERS/05. Universal/Rods/*.stl) slide out sideways to let go of the lid, measured on
the files (numpy + scipy, no Blender).

  python -I measure_rods.py <stl-placements.json>

A case whose lid can't turn up (a unit sits on it: the lid stays latched to that unit) opens another way, its
`motion.release`: the front latches open as before, then each hinge rod slides out along the axis, away from the
middle, until its tip has left the hinge top's knuckle, then the whole stack above, the lid with it, rises by a 4F
module's height (the page's "lift" joint, 196 mm; Dols's rule, 2026-11-12). Each rod gets a joint `rod_<k>`
(`slide`, unit frame, mm) and its part `{"joint": "rod_<k>"}`.

Measured on every case|<w>|<d>|<h>, posed as placed: each rod's shaft and each knuckle are the vertices within 9 mm of
the hinge axis. A rod (head outwards, against the leaf's outer end) goes through its leaf's knuckle into the hinge
top's: it must slide out by (outer end of the top's knuckle on its side) - (rod's inner tip) + CLEAR, and its tip
then stays inside the leaf's knuckle (checked), so the rods stay with the body.

Not from USSA: the case has no such use in the manual (no manual at hand); this is the user's idea for a case under
other units (2026-11-12). The rods do come out this way in real life (they are push-in pins).
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hw_geom as hg  # noqa: E402

CLEAR = 1.0      # mm past the hinge top's knuckle
NEAR = 9.0       # mm from the axis: a knuckle's or a rod shaft's vertices (knuckles r 7, rod heads r ~6)
RELEASE_S = (0.45, 0.4, 0.6)   # step times: latches (as when the lid opens), rods, lift


def placed(p):
    m = np.array(p[3]).reshape(3, 4)
    o = p[4] if len(p) > 4 and p[4] else {}
    t = hg.piece_tris(p[0], o["piece"]) if o.get("piece") else hg.file_tris(p[0])
    return t.reshape(-1, 3) @ m[:, :3].T + m[:, 3]


def x_near_axis(X, O):
    near = np.hypot(X[:, 1] - O[1], X[:, 2] - O[2]) < NEAR
    return float(X[near, 0].min()), float(X[near, 0].max())


def case_rods(key, u):
    O = u["hinge"]["origin"]
    rods, tops, leaves = [], [], []
    for p in u["parts"]:
        if "/Rods/" in p[0]:
            rods.append(p)
        elif "/Hinges/" in p[0]:
            (tops if p[2] == "lid" else leaves).append(x_near_axis(placed(p), O))
    if len(rods) != 2:
        raise ValueError(f"{key}: {len(rods)} rods")
    joints = u["motion"]["joints"]
    for k in [k for k in joints if k.startswith("rod_")]:
        del joints[k]
    out = []
    for i, p in enumerate(sorted(rods, key=lambda p: x_near_axis(placed(p), O)[0]), 1):
        x0, x1 = x_near_axis(placed(p), O)
        sx = 1.0 if x0 + x1 > 0 else -1.0
        tip = x0 if sx > 0 else -x1                                   # |x| of the rod's inner end
        top_out = max(sx * a for t in tops for a in t)                # the hinge top's knuckle, its outer end
        leaf = [t for t in leaves if sx * (t[0] + t[1]) > 0][0]
        leaf_in, leaf_out = sorted(sx * a for a in leaf)
        d = top_out - tip + CLEAR
        if not (leaf_in < tip + d < leaf_out):
            raise ValueError(f"{key}: rod {i} would leave its leaf ({tip + d:.1f} not in {leaf_in:.1f}..{leaf_out:.1f})")
        k = f"rod_{i}"
        joints[k] = {"slide": [round(sx * d, 2), 0, 0]}
        while len(p) < 5:
            p.append({})
        p[4] = {**(p[4] or {}), "joint": k}
        out.append((k, round(tip, 1), round(top_out, 1), (round(leaf_in, 1), round(leaf_out, 1)), round(d, 1)))
    latch = [s for s in u["motion"]["open"] if "lid" not in s["joints"]]
    u["motion"]["release"] = [*({**s, "s": RELEASE_S[0]} for s in latch),
                              {"joints": sorted(k for k in joints if k.startswith("rod_")), "from": 0, "to": 1, "s": RELEASE_S[1]},
                              {"joints": ["lift"], "from": 0, "to": 1, "s": RELEASE_S[2]}]
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    path = sys.argv[1]
    pl = json.load(open(path, encoding="utf-8"))
    n = 0
    for key, u in pl["units"].items():
        if not key.startswith("case|") or "hinge" not in u or "motion" not in u:
            continue
        r = case_rods(key, u)
        n += 1
        if key.endswith("|3|1") or key.endswith("|7|4"):
            print(key, r)
    print(n, "cases")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pl, f, ensure_ascii=False, separators=(",", ":"))
