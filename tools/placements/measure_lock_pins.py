"""A case lock's pins (02. SUSTAINERS/05. Universal/Locks/1 SET OF PINS FOR 1 LOCK.stl), measured on the files
(numpy, no Blender).

  python -I measure_lock_pins.py <stl-placements.json>

Adds the pins to every case|<w>|<d>|<h> that has latches (its `motion` joints latch_1, latch_2), other parts
untouched (an earlier run's pins are replaced). The file holds four pins, each its own `piece`: two plain ones,
17.9 mm long, and two longer ones, 21.4 mm, with a thicker third (r 3.0 for 9 mm, then r 2.75). The latch has two
axles across it, both along x: pin A (the link turns about it in the holder) and pin B (the link carries it, the lever
hangs on it). Measured on the posed parts:
- on A, the link's two ears and the holder between them make one bore 39.6 mm long (holder r 2.94, link ears r 2.84:
  the pins grip the link and turn in the holder), closed at both ends by the lever's sides (40.0 mm between them):
  two long pins (42.8) can't go in, two plain ones (35.8) can. So A takes the plain pins, one from each end, flush with
  the link's outer faces (inferred: they could sit anywhere in the 3.8 mm left over).
- on B, the lever's two ears and the link between them make a 50 mm bore (r 2.94 / 2.91 / 2.94): the long pins, one
  from each end, flush with the lever's outer faces, thick end outwards (inferred: 7.2 mm left over in the middle).
Each pin turns with the link (`latch_<k>.link`): A is the link's own axis, B is carried by it. The planner counts one
file per lock; the page draws one set per latch, as the case has.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vault_geom as vg  # noqa: E402
import hw_geom as hg  # noqa: E402
from measure_column import mat  # noqa: E402

PINS = "02. SUSTAINERS/05. Universal/Locks/1 SET OF PINS FOR 1 LOCK.stl"


def pin_shapes():
    """The file's four pins: [{c (bbox centre, file), ax (unit axis, towards the thin end), len}], short ones first."""
    out = []
    for t in vg.pieces(hg.file_tris(PINS)):
        P = t.reshape(-1, 3)
        c = vg.piece_centre(t)
        _, V = np.linalg.eigh(np.cov((P - P.mean(0)).T))
        ax = V[:, -1]
        s = (P - c) @ ax
        r = np.linalg.norm(P - c - np.outer(s, ax), axis=1)
        lo, hi = s.min(), s.max()
        # the thick third is where the radius is largest: make ax point away from it
        if np.percentile(r[s < lo + 6], 99) < np.percentile(r[s > hi - 6], 99):
            ax = -ax
        out.append({"c": c, "ax": ax, "len": float(hi - lo)})
    return sorted(out, key=lambda p: (round(p["len"]), p["c"][1]))


def rot(ax, d):
    """Turns the file's pin axis `ax` onto the unit's direction `d` (±x), the file's z (the bed) onto the unit's y."""
    a = ax / np.linalg.norm(ax)
    z = np.array([0.0, 0, 1]) - a * a[2]
    z /= np.linalg.norm(z)
    F = np.stack([a, z, np.cross(a, z)], 1)            # file basis (columns)
    dd = np.array(d, float)
    y = np.array([0.0, 1, 0])
    G = np.stack([dd, y, np.cross(dd, y)], 1)          # unit basis
    return G @ F.T


def x_span(u, joint, P):
    """x extent of the posed parts of `joint` (latch_k.link / .lever) within 4 mm of the axle P (y, z)."""
    xs = []
    for p in u["parts"]:
        o = p[4] if len(p) > 4 else {}
        if o.get("joint") != joint:
            continue
        m = np.array(p[3]).reshape(3, 4)
        X = hg.file_tris(p[0]).reshape(-1, 3) @ m[:, :3].T + m[:, 3]
        near = np.hypot(X[:, 1] - P[1], X[:, 2] - P[2]) < 4
        xs.append(X[near, 0])
    xs = np.concatenate(xs)
    return float(xs.min()), float(xs.max())


def case_pins(u, pins):
    short, long_ = pins[:2], pins[2:]
    parts = []
    for k, j in sorted(u["motion"]["joints"].items()):
        if "latch" not in j:
            continue
        L = j["latch"]
        for P, sel, who in ((L["A"], short, f"{k}.link"), (L["B"], long_, f"{k}.lever")):
            x0, x1 = x_span(u, who, P)
            for pin, end, inward in ((sel[0], x0, 1.0), (sel[1], x1, -1.0)):
                R = rot(pin["ax"], [inward, 0, 0])
                at = np.array([end + inward * pin["len"] / 2, P[1], P[2]])
                parts.append([PINS, "mech", "module", mat(R, at - R @ pin["c"]),
                              {"piece": [round(float(v), 3) for v in pin["c"]], "joint": f"{k}.link", "as": "pin"}])
    return parts


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    path = sys.argv[1]
    pl = json.load(open(path, encoding="utf-8"))
    pins = pin_shapes()
    print("pins", [(round(p["len"], 2), p["c"].round(2).tolist()) for p in pins])
    n = 0
    for key, u in pl["units"].items():
        if not key.startswith("case|") or "motion" not in u:
            continue
        u["parts"] = [p for p in u["parts"] if p[0] != PINS]
        add = case_pins(u, pins)
        u["parts"] += add
        n += 1
        if key.endswith("|3|1") or key.endswith("|3|2"):
            print(key, len(add), "pins")
    print(n, "cases")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pl, f, ensure_ascii=False, separators=(",", ":"))
