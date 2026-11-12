"""Gridfinity baseplates that the CAD scene doesn't give in place: the XL drawers' (printed tilted) and the cases'
(02. SUSTAINERS/05. Universal/Baseplates), measured on the files (numpy, no Blender).

  python -I measure_baseplates.py <stl-placements.json> [xl] [case]

xl   : adds each XL drawer's baseplate (one piece on XL3-5, two on XL6-7) to drawer|XL|<d>|1 (other parts untouched).
       Like the L and M ones, they were exported in the drawer box's own pose but somewhere else in the scene, and
       upside down: they take the box's rotation turned half a turn about x (their 22 mm ribs up, the flat slab
       down). XL boxes are tapered (narrower at the back, about 3.5 mm a side over 100 mm) and so are the
       baseplates: each is laid on the box's floor, centred across, and pushed back until it touches (the box, its
       back panel, or the back piece of a two-piece baseplate, which goes in first). Measured the same way, an L3's
       baseplate lands 0.24 mm in front of the back wall, where the CAD scene has it.
case : adds `casebase|<w>|<d>`: the case baseplate in a case's unit frame, laid on the floor of the case body
       (its "Flat" module), centred across, pushed back until it touches. Measured on the S3, M3, L3 and XL3 bodies
       where they are in the download folder (VAULT_RENDER), else from the L3 one: the floor's height and the gap
       to the back wall are the same on every size (the bodies differ by 42 mm a depth step, the baseplates too).
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vault_geom as vg  # noqa: E402
import hw_geom as hg  # noqa: E402
from measure_column import mat, posed  # noqa: E402

XL = "01. DRAWERS/05. XL Families/"
SUU = "02. SUSTAINERS/05. Universal/Baseplates/"
FLIP_X = np.diag([1.0, -1, -1])
STEP = 0.25


def occupancy(T, y, lo, hi):
    """Where the cut y = const of T is inside material, on an (x, z) grid from lo to hi (even-odd fill of the cut's
    crossings, row by row along z)."""
    S = hg.section(T, 1, y)
    a, b = S[:, 0], S[:, 1]
    xs = np.arange(lo[0], hi[0], STEP) + STEP / 2
    zs = np.arange(lo[1], hi[1], STEP) + STEP / 2
    G = np.zeros((len(zs), len(xs)), bool)
    dz = b[:, 2] - a[:, 2]
    for j, z in enumerate(zs):
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (z - a[:, 2]) / dz
        ok = (t >= 0) & (t < 1) & (dz != 0)
        cx = np.sort(a[ok, 0] + t[ok] * (b[ok, 0] - a[ok, 0]))
        G[j] = (np.searchsorted(cx, xs) % 2) == 1
    return G


def floor_of(T, box_lo, box_hi):
    """The box's or body's inner floor: the most common upward-facing level seen from above, in its middle."""
    c = (box_lo + box_hi) / 2
    w = (box_hi - box_lo) / 4
    D, *_ = vg.depthmap(T, 1, 1, 0.5, lo=np.array([c[0] - w[0], box_lo[1], c[2] - w[2]]), hi=np.array([c[0] + w[0], box_hi[1], c[2] + w[2]]))
    v = D[np.isfinite(D)].round(1)
    vals, cnt = np.unique(v, return_counts=True)
    return float(vals[np.argmax(cnt)])


def push_back(walls, plate, floor):
    """Translate `plate` (its slab flat, bottom anywhere) onto `floor`, centred across on x = 0, then back along -z
    from in front of the walls until it touches them. walls: list of triangle sets in the unit frame. Returns the
    translation."""
    P = plate.reshape(-1, 3)
    plo, phi = P.min(0), P.max(0)
    t = np.array([-(plo[0] + phi[0]) / 2, floor - plo[1], 0.0])
    W = np.concatenate(walls)
    Q = W.reshape(-1, 3)
    lo2 = np.array([min(Q[:, 0].min(), plo[0] + t[0]) - 2, Q[:, 2].min() - 2])
    hi2 = np.array([max(Q[:, 0].max(), phi[0] + t[0]) + 2, Q[:, 2].max() + 2])
    G = np.zeros_like(occupancy(W, floor + 1.0, lo2, hi2))
    for y in (floor + 1.0, floor + 2.5):
        G |= occupancy(W, y, lo2, hi2)
    B = occupancy(plate + t, plo[1] + t[1] + 1.5, np.array([lo2[0], plo[2] - 2]), np.array([hi2[0], phi[2] + 2]))
    # the plate's rows, then slide its grid along z (in steps) from its front at the walls' front edge
    rows = np.nonzero(B.any(1))[0]
    B = B[rows.min():rows.max() + 1]
    z_back_plate = plo[2] - 2 + STEP * rows.min()                 # the plate's back edge, on its grid
    # where it overlaps the walls least (no overlap at all for the L and M ones: then the furthest back)
    n = G.shape[0]
    over = np.array([(G[k:k + B.shape[0]] & B).sum() for k in range(n - B.shape[0] + 1)])
    last = int(np.nonzero(over == over.min())[0][0])
    push_back.overlap = float(over.min() * STEP * STEP)
    t[2] = lo2[1] + STEP * last - z_back_plate
    return t


def xl_drawer(pl):
    for d in range(3, 8):
        u = pl["units"][f"drawer|XL|{d}|1"]
        u["parts"] = [q for q in u["parts"] if "/Gridfinity Baseplate/" not in q[0]]
        boxes = [q for q in u["parts"] if "/Boxes/" in q[0]]
        walls = [posed(hg.file_tris(q[0]), q[3]) for q in boxes]
        front = [q for q in boxes if "Box 1F" in q[0]][0]
        B = posed(hg.file_tris(front[0]), front[3])
        Q = B.reshape(-1, 3)
        fl = floor_of(B, Q.min(0), Q.max(0))
        M = np.array(front[3]).reshape(3, 4)
        R = FLIP_X @ M[:, :3]
        names = [f"XL{d} Baseplate.stl"] if d < 6 else [f"XL{d} Baseplate Part 1.stl", f"XL{d} Baseplate Part 2.stl"]
        behind = None
        for nm in names:
            f = XL + f"XL{d}/Gridfinity Baseplate/{nm}"
            T = hg.file_tris(f) @ R.T
            if behind is None:
                t = push_back(walls, T, fl)
            else:
                # the back piece: its front edge on the front piece's back edge (on XL6 the two fill the box to
                # 0.1 mm, front wall to back wall)
                P = T.reshape(-1, 3)
                t = np.array([-(P[:, 0].min() + P[:, 0].max()) / 2, fl - P[:, 1].min(), behind - P[:, 2].max()])
                push_back.overlap = None
            m = mat(R, t)
            u["parts"].append([f, "interior", front[2], m, {}])
            Tp = posed(hg.file_tris(f), m)
            P = Tp.reshape(-1, 3)
            behind = float(P[:, 2].min())
            print(f"XL{d}", nm, "floor", fl, "overlap mm2", push_back.overlap, "x", P[:, 0].min().round(2), P[:, 0].max().round(2), "z", P[:, 2].min().round(2), P[:, 2].max().round(2), flush=True)


CASE_BODY = {"S": "02. SUSTAINERS/01. S Families/S3/Modules/S3 1F Module.stl",
             "M": "02. SUSTAINERS/02. M Families/M3/Modules/M3 1F Module .stl",
             "L": "02. SUSTAINERS/03. L Families/L3/Modules/L3 1F Flat Module.stl",
             "XL": "02. SUSTAINERS/04. XL Families/XL3/Modules/XL3 1F Flat Module.stl"}
UP = np.array([[1.0, 0, 0], [0, 0, 1], [0, -1, 0]])      # file +z up, file +y to the back


def flat_down(T):
    """Is the side facing down flat (the slab), not the ribs?"""
    D = vg.depthmap(T, 1, -1, 0.5)[0]
    lo = T.reshape(-1, 3)[:, 1].min()
    v = (D[np.isfinite(D)] - lo).round(1)
    return (v <= 0.2).mean() > 0.5


def case_files(w, d):
    if w == "XL":
        if d >= 6:
            return [SUU + f"04. XL/XL{d} Part 1  Gridfinity Baseplate.stl", SUU + f"04. XL/XL{d} Part 2  Gridfinity Baseplate.stl"]
        return [SUU + f"04. XL/XL{d}  Gridfinity Baseplate.stl"]
    return [SUU + f"0{'SML'.index(w) + 1}. {w}/{w}{d} Baseplate.stl"]


def back_wall(B, y):
    """The inner face of a body's back wall at height y, in its middle (x = 0)."""
    S = hg.section(B, 1, y)
    a, b = S[:, 0], S[:, 1]
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (0 - a[:, 0]) / (b[:, 0] - a[:, 0])
    ok = (t >= 0) & (t < 1)
    z = np.sort(a[ok, 2] + t[ok] * (b[ok, 2] - a[ok, 2]))
    return float(z[1])                      # [0] the outer face, [1] the inner one


def cases(pl):
    """casebase|<w>|<d>: on the floor of the depth-3 body, centred across, its back on the body's back wall (the
    S ones, pushed back until they touch, land there; the others are as deep, 141.1 mm, from that wall to the
    body's front edge, but meet a lip or fillet on the way). A two-piece XL one: part 2 at the back, part 1 in front
    of it. A deeper body's back wall is 42 mm further back a depth step."""
    for w in ["S", "M", "L", "XL"]:
        body = CASE_BODY[w]
        q = [q for q in pl["units"][f"case|{w}|3|1"]["parts"] if q[0] == body][0]
        B = posed(hg.file_tris(body), q[3])
        Q = B.reshape(-1, 3)
        fl = floor_of(B, Q.min(0), Q.max(0))
        back = back_wall(B, fl + 10)
        # XL's are printed tilted like the XL bodies, and exported in the body's pose: its rotation, or that turned
        # half a turn about the vertical, whichever puts the flat slab down. S, M, L ones are printed flat.
        Rb = np.array(q[3]).reshape(3, 4)[:, :3] if w == "XL" else UP
        for d in range(3, 8):
            parts, z_back = [], back - 42 * (d - 3)
            for f in reversed(case_files(w, d)):
                R = Rb
                T = hg.file_tris(f) @ R.T
                if not flat_down(T):
                    R = np.diag([-1.0, -1, 1]) @ Rb
                    T = hg.file_tris(f) @ R.T
                P = T.reshape(-1, 3)
                t = np.array([-(P[:, 0].min() + P[:, 0].max()) / 2, fl - P[:, 1].min(), z_back - P[:, 2].min()])
                m = mat(R, t)
                z_back = float(P[:, 2].max() + t[2])
                parts.insert(0, [f, "interior", "module", m, {}])
                print(w, d, f.split("/")[-1], "floor", fl, "x", round(float(P[:, 0].min() + t[0]), 2), round(float(P[:, 0].max() + t[0]), 2),
                      "z", round(float(P[:, 2].min() + t[2]), 2), round(z_back, 2), "back wall", round(back - 42 * (d - 3), 2), flush=True)
            pl["units"][f"casebase|{w}|{d}"] = {"name": f"{w}{d} case baseplate", "parts": parts}


def check_L3(pl):
    """The method on a baseplate the CAD scene places: L3's, against its box."""
    u = pl["units"]["drawer|L|3|1"]
    box = [q for q in u["parts"] if "Box 1F" in q[0]][0]
    bp = [q for q in u["parts"] if "Gridfinity Baseplate" in q[0]][0]
    B = posed(hg.file_tris(box[0]), box[3])
    Q = B.reshape(-1, 3)
    fl = floor_of(B, Q.min(0), Q.max(0))
    M = np.array(bp[3]).reshape(3, 4)
    T = hg.file_tris(bp[0]) @ M[:, :3].T
    t = push_back([B], T, fl)
    print("L3 check: scene", M[:, 3].round(2), "measured", t.round(2), flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    path = sys.argv[1]
    what = sys.argv[2:] or ["xl", "case"]
    pl = json.load(open(path, encoding="utf-8"))
    check_L3(pl)
    if "xl" in what:
        xl_drawer(pl)
    if "case" in what:
        cases(pl)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pl, f, ensure_ascii=False, separators=(",", ":"))
