"""Drawer grid dividers (01. DRAWERS/07. Universal/Grid Dividers): each drawer box's peg-hole grid, and how each
divider, edge piece and pin file stands. Measured on the files (numpy, no Blender).

  python -I measure_grid.py <stl-placements.json> [files]

files: only the divider files' matrices (the boxes' grids are kept).

USSA's instructions (Grid Dividers/01. INSTRUCTIONS): a box's floor is a grid of peg holes 10.5 mm apart. A divider
is a wall on a wide foot (25.35 mm, filleted up to a ~3 mm wall) that stands on a row or a column of holes, held by
two pins in the holes 1.5 pitches in from each of its ends. Its file number N is how many holes it covers (it is
10.5 x N mm long, N = 5 ... 32). Each end has a 12 mm slot that takes an end piece's tongue:
- "Straight Edge Piece": a 25.35 x 7.5 mm plate that closes against a wall; its tongue slides in the slot, so it
  bridges whatever gap is left to the wall (about 8 to 20 mm).
- "Rounded Edge Piece": an arrow whose underside is the other dividers' fillet: it rides over the foot of a divider
  that runs across, its tip on that divider's middle plane. A partial divider (from a divider to a wall, or between
  two dividers) ends with one at each divider it meets.
A full-span divider is the file named after the box (width 10-S, 18-M, 26-L, 32-XL; depth 10, 14, 18, 22, 26 for
x3 ... x7) with a straight piece at each wall. A partial divider covers the free holes between its ends (a crossing
divider's foot covers its own row and the next one on each side): "N" alone leaves a few mm to the wall, "N - 1"
with a straight piece closes against it (instructions 4-6).

Writes, top level:
  "grid_boxes": {"<box file>": {"m": the box's matrix in the unit it was measured in, "floor": y, "x": [x0, nx],
    "z": [z0, nz], "pitch": 10.5, "walls": [x left, x right, z back, z front]}}
    The grid in that unit's frame: hole centres x0 + i * pitch (i < nx), likewise z (z0 at the back). walls: the
    inner faces 4 mm above the floor (the median over several lines: XL walls lean a few mm). The box is open at the
    front but for a block in its middle, about as far from the last row as the back wall from the first: "z front"
    is that block's face. "as": a 2F or 4F box not measured, given its 1F box's grid (they agree where checked). XL6 and XL7 boxes are printed in two parts: the grid is under Part 1 and holds
    for both. The page moves it with the box: (box's matrix where it is) x inverse(m).
  "grid_files": {"<path>": m}: a 3x4 matrix from the file to the piece's own frame, bottom at y = 0:
    a divider lies along x, centred on x = 0 and z = 0; an edge piece has its face (straight) or tip (rounded) at
    x = 0 and its tongue along +x, centred on z = 0; a pin stands centred on x = z = 0.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hw_geom as hg  # noqa: E402
import vault_geom as vg  # noqa: E402
from measure_baseplates import floor_of  # noqa: E402
from measure_column import mat, posed  # noqa: E402

PITCH = 10.5
GD = "01. DRAWERS/07. Universal/Grid Dividers/"
DIRS = {"20MM": "20MM TALL/", "1F": "34.5MM TALL (full height of 1F drawers)/", "2F": "82.5MM TALL (full height of 2F drawers)/"}
NAMES = {10: "10-S, x3", 14: "14, x4", 18: "18-M, x5", 22: "22, x6", 26: "26-L, x7", 32: "32-XL"}


def grid_files():
    out = []
    for sfx, d in DIRS.items():
        out += [(GD + d + NAMES.get(n, str(n)) + ".stl", "divider") for n in range(5, 33)]
        out += [(GD + d + f"{k} Edge Piece {sfx}.stl", "edge") for k in ("Straight", "Rounded")]
    out += [(GD + f"grid divider pin_{k}.stl", "pin") for k in ("tight", "loose")]
    return out


def file_matrix(path, kind):
    """The files lie as printed: a divider along its X, its width along Y, standing up Z; an edge piece across X,
    face (or tip) at its lowest Y, tongue towards +Y. The pin is printed lying down: its long axis is Y."""
    P = hg.file_tris(path).reshape(-1, 3)
    lo, hi = P.min(0), P.max(0)
    c = (lo + hi) / 2
    if kind == "divider":   # x' = X, y' = Z, z' = -Y
        R = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float)
        t = -R @ np.array([c[0], c[1], lo[2]])
    elif kind == "edge":    # x' = Y, y' = Z, z' = X
        R = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], float)
        t = -R @ np.array([c[0], lo[1], lo[2]])
    else:                   # pin: y' = Y (standing), x' = X, z' = -Z
        R = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]], float)
        t = -R @ np.array([c[0], lo[1], c[2]])
    return mat(R, t), [round(float(v), 2) for v in hi - lo]


def box_units(pl):
    """Each box file and the first single-drawer unit holding it (drawer|w|d|h, w in S M L XL)."""
    out = {}
    for k, u in pl["units"].items():
        p = k.split("|")
        if p[0] != "drawer" or p[1] not in ("S", "M", "L", "XL"):
            continue
        for q in u["parts"]:
            name = q[0].split("/")[-1]
            if " Box " in name and q[0] not in out:
                out[q[0]] = (k, q[3])
    return out


def grid_axis(v):
    """Hole centres along one axis -> (first centre, count), on a 10.5 mm pitch (noise from the rim is dropped:
    every hole must sit within 0.6 mm of the fitted grid, and a run is kept only if it holds most holes)."""
    v = np.sort(v)
    best = None
    for s in v:
        k = np.round((v - s) / PITCH)
        ok = np.abs(v - s - k * PITCH) < 0.6
        if best is None or ok.sum() > best[0]:
            best = (ok.sum(), s, k[ok])
    _, s, ks = best
    ks = np.unique(ks)
    # the longest run of consecutive indices
    runs, cur = [], [ks[0]]
    for a in ks[1:]:
        if a == cur[-1] + 1:
            cur.append(a)
        else:
            runs.append(cur)
            cur = [a]
    runs.append(cur)
    r = max(runs, key=len)
    sel = np.isin(np.round((v - s) / PITCH), r) & (np.abs(v - s - np.round((v - s) / PITCH) * PITCH) < 0.6)
    x0 = float(np.mean(v[sel] - (np.round((v[sel] - s) / PITCH) - r[0]) * PITCH))
    return round(x0, 2), len(r)


def measure(B):
    Q = B.reshape(-1, 3)
    lo, hi = Q.min(0), Q.max(0)
    fl = floor_of(B, lo, hi)
    # the floor and what is sunk in it, seen from above
    T = B[B[:, :, 1].max(1) < fl + 0.5]
    D, u0, w0, _ = vg.depthmap(T, 1, 1, 0.25, lo=lo, hi=hi)
    flat = np.isfinite(D) & (np.abs(D - fl) < 0.2)
    ys, xs = np.where(flat)
    inner = np.zeros_like(flat)
    inner[ys.min():ys.max() + 1, xs.min():xs.max() + 1] = True
    from scipy import ndimage
    hole = ((np.isfinite(D) & (D < fl - 0.5)) | ~np.isfinite(D)) & inner
    lab, n = ndimage.label(hole)
    cs = ndimage.center_of_mass(hole, lab, range(1, n + 1))
    sz = ndimage.sum(hole, lab, range(1, n + 1)) * 0.0625
    pts = np.array([(u0 + c[1] * 0.25, w0 + c[0] * 0.25) for c, s in zip(cs, sz) if 8 < s < 20])
    x0, nx = grid_axis(pts[:, 0])
    z0, nz = grid_axis(pts[:, 1])
    # inner wall faces, seen from above (their tops) along the middle row and column of holes
    W = B[B[:, :, 1].min(1) < fl + 30]
    Dw, u0, w0, _ = vg.depthmap(W, 1, 1, 0.25, lo=lo, hi=hi)

    def face(line, start, step):
        i = start
        while 0 <= i < len(line) and not (np.isfinite(line[i]) and line[i] > fl + 4):
            i += step
        return i - step / 2   # between the last free cell and the wall's first

    def outer(lines, start, step, edge, nearest=False):
        got = [face(ln, start, step) for ln in lines]
        got = [g for g in got if 0 < g < edge - 1] or got   # a line with no wall (a notch, a cut-out) is left out
        if nearest:                                          # the front: the box is open there but in its middle,
            return min(got) if step > 0 else max(got)       # in front of the lock, as far from the holes as the back
        return float(np.median(got))                        # a rib or a joint is outvoted

    rows = [Dw[int(round((z0 + f * (nz - 1) * PITCH - w0) / 0.25))] for f in np.linspace(0.1, 0.9, 9)]
    cols = [Dw[:, int(round((x0 + f * (nx - 1) * PITCH - u0) / 0.25))] for f in np.linspace(0.1, 0.9, 9) if abs(f - 0.5) > 0.15]
    xc = int(round((x0 + (nx - 1) / 2 * PITCH - u0) / 0.25))
    zr = int(round((z0 + (nz - 1) / 2 * PITCH - w0) / 0.25))
    xl = u0 + outer(rows, xc, -1, Dw.shape[1]) * 0.25
    xr = u0 + outer(rows, xc, 1, Dw.shape[1]) * 0.25
    zb = w0 + outer(cols, zr, -1, Dw.shape[0]) * 0.25
    zf = w0 + outer(cols + [Dw[:, xc]], zr, 1, Dw.shape[0], True) * 0.25
    return {"floor": round(fl, 2), "x": [x0, nx], "z": [z0, nz], "pitch": PITCH,
            "walls": [round(float(v), 2) for v in (xl, xr, zb, zf)]}


def main(path, boxes=True):
    pl = json.load(open(path, encoding="utf-8"))
    files = {}
    for f, kind in grid_files():
        files[f], size = file_matrix(f, kind)
        hg._CACHE.pop(f, None)
        print(f.split("/")[-1], size, flush=True)
    pl["grid_files"] = files
    if boxes:
        got, missing = {}, []
        for bf, (k, m) in sorted(box_units(pl).items()):
            if " Part 2" in bf:
                continue
            parts = [bf] + ([bf.replace("Part 1", "Part 2")] if " Part 1" in bf else [])
            ms = [m] + [q[3] for q in pl["units"][k]["parts"] if q[0] in parts[1:]]
            if not all(hg.on_disk(p) for p in parts):
                missing.append((bf, m))
                continue
            B = np.concatenate([posed(hg.file_tris(p), mm) for p, mm in zip(parts, ms)])
            g = measure(B)
            g["m"] = m
            got[bf] = g
            for p in parts:
                hg._CACHE.pop(p, None)
            print(k, bf.split("/")[-1], {a: b for a, b in g.items() if a != "m"}, flush=True)
        # 2F and 4F boxes not on disk: the 1F box of the same family, which gives the same grid in its unit's frame
        # (checked on S3 4F and L7 2F)
        for bf, m in missing:
            one = [b for b in got if b.rsplit("/", 1)[0] == bf.rsplit("/", 1)[0] and " Box 1F" in b]
            if not one:
                print("missing", bf, flush=True)
                continue
            got[bf] = {**got[one[0]], "m": m, "as": one[0]}
            print("as 1F", bf.split("/")[-1], flush=True)
        pl["grid_boxes"] = dict(sorted(got.items()))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pl, f, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1], sys.argv[2:3] != ["files"])
