"""Case dividers (02. SUSTAINERS/05. Universal/Dividers): where they can go in each case body, and how each divider
file stands in one of its slots. Measured on the files (numpy, no Blender).

  python -I measure_dividers.py <stl-placements.json> [files | check]

files: only the divider files' matrices (the bodies' slots are kept); check: the 2F and 4F bodies against the 1F ones.

A divider is a 2 mm sheet that slides into 2 mm slots moulded in the body's walls; there is no other place for it.
- S and M bodies (one style): slots in the two side walls only. The divider runs side to side, full width.
- L and XL "Dividers" bodies: the same side-wall slots for the Width dividers (full width), plus slots in the back
  wall for the Depth dividers (front to back). Width dividers are notched from below and depth dividers from above
  where they cross (an egg crate), so any mix of the two fits.
- L and XL "Sealed" bodies: fixed walls make cells (2 on L, 3 on XL); each cell has its own side slots for the Seal
  dividers, which are as tall as the body's wall.
- "Flat" bodies have no slot: no divider.

Each body is cut at 15 mm above its floor and the cut filled (even-odd) on a 0.25 mm grid. The free runs across a
row away from the slots give the cells; a row where both walls of a cell step out by more than 0.5 mm is a side slot,
a column where the back wall steps back is a back slot. Measured on the 1F bodies of every depth; the 2F and 4F
bodies of the same depth have the same slots and floor (checked on L3 2F/4F Dividers and Sealed, S3 4F).

Every slot runs on down into a 2 mm groove in the floor (and so does a back slot, along the floor to the front): a
divider stands in it, 7.8 mm above the body's bottom where the floor is at 9.8. Plain and seal dividers (49.85 mm on
1F) then reach 57.65, about the lid's underside (a sealed body's rim is at 58.3, a plain one's at 50.8 with the lid
6.9 mm over it); width and depth ones (40.85) stop at 48.65, under the rim.

Writes, per case unit `case|<w>|<d>|<h>` (all heights from the 1F body):
  "dividers": {"<style>": {"floor": y (the grooves' bottom), "body_floor": y, "rows": [z, ...], "cols": [x, ...], "back": z, "cells": [[x0, x1], ...]}}
    style "plain" (S, M), "dividers" or "sealed" (L, XL). rows: side-slot centres (z, unit frame, front at 0); cols
    and back ("dividers" only): back-wall slot centres and the bottom of those slots; cells ("sealed" only): each
    cell's inner faces across. Rows hold for every cell.
and top level "divider_files": {"<path>": m}, a 3x4 matrix from the file to the divider's own frame: standing (its
rounded top corners up), its bottom at y = 0, its middle plane at the slot (z = 0 for one that runs across, x = 0
for a depth divider), centred across (x = 0) or, for a depth divider, its back end at z = 0 running to +z. The page
adds the slot's position.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hw_geom as hg  # noqa: E402
from measure_baseplates import occupancy, floor_of, STEP  # noqa: E402
from measure_column import mat, posed  # noqa: E402

SU = "02. SUSTAINERS/"
DV = SU + "05. Universal/Dividers/"
HEIGHTS = (40.85, 49.85, 74.85, 83.85, 170.85, 179.85)
FAM = {"S": "01. S Families", "M": "02. M Families", "L": "03. L Families", "XL": "04. XL Families"}


def body_file(w, d, style, h=1):
    if w in ("S", "M"):
        return SU + f"{FAM[w]}/{w}{d}/Modules/{w}{d} {h}F Module{' ' if w == 'M' else ''}.stl"
    return SU + f"{FAM[w]}/{w}{d}/Modules/{w}{d} {h}F {style.title()} Module.stl"


def runs(mask):
    """[start, end) index pairs of the True runs of a 1-D mask."""
    m = np.r_[False, mask, False].astype(np.int8)
    d = np.diff(m)
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))


def clusters(v, gap=1.0):
    v = np.sort(np.asarray(v))
    if not len(v):
        return []
    out, cur = [], [v[0]]
    for x in v[1:]:
        if x - cur[-1] > gap:
            out.append(cur)
            cur = []
        cur.append(x)
    out.append(cur)
    return out


def measure(B):
    """The slots of a body posed in its unit frame."""
    Q = B.reshape(-1, 3)
    lo, hi = Q.min(0), Q.max(0)
    fl = floor_of(B, lo, hi)
    g_lo, g_hi = np.array([lo[0] - 1, lo[2] - 1]), np.array([hi[0] + 1, hi[2] + 1])
    G = occupancy(B, fl + 15, g_lo, g_hi)                       # [z, x], True = material
    xs = g_lo[0] + STEP * (np.arange(G.shape[1]) + 0.5)
    zs = g_lo[1] + STEP * (np.arange(G.shape[0]) + 0.5)
    # rows inside the body (between its back wall and its open front), where the free runs are the cells
    free_rows = [(j, [(xs[a], xs[b - 1]) for a, b in runs(~G[j]) if xs[b - 1] - xs[a] > 30 and xs[a] > xs[0] + 1 and xs[b - 1] < xs[-1] - 1])
                 for j in range(len(zs))]
    inside = [(j, r) for j, r in free_rows if r and zs[j] > lo[2] + 15 and zs[j] < hi[2] - 15]
    n = int(np.median([len(r) for _, r in inside]))
    inside = [(j, r) for j, r in inside if len(r) == n]
    cells = [[float(np.median([r[k][0] for _, r in inside])), float(np.median([r[k][1] for _, r in inside]))] for k in range(n)]
    # side slots: rows where every cell is wider on both sides
    # (a slot holds a small nub, so its free space may not join the cell's: look for any free space within 3 mm)
    def open_(j, x0, x1):
        return bool((~G[j, (xs > x0) & (xs < x1)]).any())
    slot_z = [zs[j] for j, r in inside if all(open_(j, c[0] - 3, c[0] - 0.4) and open_(j, c[1] + 0.4, c[1] + 3) for c in cells)]
    rows = [round(float((c[0] + c[-1]) / 2), 2) for c in clusters(slot_z) if c[-1] - c[0] > 1]
    # each slot runs on down into a groove in the floor, where the divider stands: its bottom, under the first slot
    S = hg.section(B, 2, sorted(rows)[0]).reshape(-1, 3)
    c0 = (cells[0][0] + cells[0][1]) / 2
    g = S[(np.abs(S[:, 0] - c0) < 2) & (S[:, 1] > fl - 3.5) & (S[:, 1] < fl - 0.2), 1]
    out = {"floor": round(float(g.min()) if len(g) else fl, 2), "body_floor": round(fl, 2), "rows": sorted(rows), "cells": [[round(a, 2), round(b, 2)] for a, b in cells]}
    # back slots: columns of the cell(s) where the back wall steps back
    back = []
    for i, x in enumerate(xs):
        if not any(c[0] + 10 < x < c[1] - 10 for c in cells):
            continue
        col = ~G[:, i]
        r = [(zs[a], zs[b - 1]) for a, b in runs(col) if zs[b - 1] > hi[2] - 20]
        if r:
            back.append((x, r[0][0]))
    if back:
        bz = np.median([b for _, b in back])
        j0 = np.searchsorted(zs, bz)
        deep = [(x, b) for x, b in back if (~G[max(j0 - 12, 0):max(j0 - 1, 0), np.searchsorted(xs, x)]).any()]
        deep = [(x, min(zs[j] for j in range(max(j0 - 12, 0), j0) if not G[j, np.searchsorted(xs, x)])) for x, _ in deep]
        cols = [c for c in clusters([x for x, _ in deep]) if c[-1] - c[0] > 1]
        out["cols"] = [round(float((c[0] + c[-1]) / 2), 2) for c in cols]
        out["back"] = round(float(min(b for _, b in deep)), 2) if deep else None
        out["back_face"] = round(float(bz), 2)
    return out


def standing(path, along_z=False):
    """The file's matrix to the divider's own frame (see the module's doc)."""
    T = hg.file_tris(path)
    P = T.reshape(-1, 3)
    lo, hi = P.min(0), P.max(0)
    ext = hi - lo
    thin = int(np.argmin(ext))
    a, b = [k for k in range(3) if k != thin]
    # the height is the body's inner wall height less a clearance: 40.85 / 74.85 / 170.85 (width and depth
    # dividers, 1F / 2F / 4F), 49.85 / 83.85 / 179.85 (plain and seal ones); 4F ones are taller than long
    off = lambda k: min(abs(ext[k] - v) for v in HEIGHTS)
    length, height = (a, b) if off(b) < off(a) else (b, a)
    # the top edge has the 2.1 mm rounded corners: no vertex at its two bbox corners
    def corner_gap(sign):
        h = hi[height] if sign > 0 else lo[height]
        return min(np.hypot(P[:, length] - c, P[:, height] - h).min() for c in (lo[length], hi[length]))
    up = 1.0 if corner_gap(1) > corner_gap(-1) else -1.0
    e = np.eye(3)
    X, Y = e[length], up * e[height]
    if along_z:                      # length along +z, thickness along x
        Z = X
        Xn = np.cross(Y, Z)
        R = np.array([Xn, Y, Z])
    else:
        Z = np.cross(X, Y)
        R = np.array([X, Y, Z])
    Q = P @ R.T
    qlo, qhi = Q.min(0), Q.max(0)
    t = -(qlo + qhi) / 2
    t[1] = -qlo[1]
    if along_z:
        t[2] = -qlo[2]
    return mat(R, t), {"length": round(float(ext[length]), 2), "height": round(float(ext[height]), 2), "thick": round(float(ext[thin]), 2)}


def divider_files():
    fs = []
    for w in ("S", "M"):
        fs += [(DV + f"{w} Dividers/{w}{h}F Divider.stl", False) for h in (1, 2, 4)]
    for h in (1, 2, 4):
        fs += [(DV + f"L Width Dividers/L-{h}F Width Divider.stl", False), (DV + f"L Seal Dividers/L-{h}F Seal Divider.stl", False)]
        fs += [(DV + f"L Depth Dividers/L{d}-{h}F Depth Divider.stl", True) for d in range(3, 8)]
    fs += [(DV + "XL Width Divider.stl", False), (DV + "XL Seal Divider (Center).stl", False), (DV + "XL Seal Divider (Sides).stl", False)]
    fs += [(DV + f"XL Depth Dividers/XL{d} Depth Divider.stl", True) for d in range(3, 8)]
    return fs


def main(path, bodies=True):
    pl = json.load(open(path, encoding="utf-8"))
    files = {}
    for f, along in divider_files():
        m, size = standing(f, along)
        files[f] = m
        print(f.split("/")[-1], size, flush=True)
    pl["divider_files"] = files
    for w in (("S", "M", "L", "XL") if bodies else ()):
        for d in range(3, 8):
            got = {}
            for style in (("plain",) if w in ("S", "M") else ("dividers", "sealed")):
                bf = body_file(w, d, style)
                q = [q for q in pl["units"][f"case|{w}|{d}|1"]["parts"] if q[0] == bf]
                if not q:
                    raise KeyError(bf)
                got[style] = measure(posed(hg.file_tris(bf), q[0][3]))
                print(w, d, style, got[style], flush=True)
            for h in (1, 2, 4):
                k = f"case|{w}|{d}|{h}"
                if k in pl["units"]:
                    pl["units"][k]["dividers"] = got
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pl, f, ensure_ascii=False, separators=(",", ":"))


def check_heights(pl):
    """The 2F and 4F bodies give the same slots as the 1F one."""
    for w, d, style, h in (("L", 3, "dividers", 2), ("L", 3, "dividers", 4), ("L", 3, "sealed", 2), ("L", 3, "sealed", 4), ("S", 3, "plain", 4)):
        bf = body_file(w, d, style, h)
        q = [q for q in pl["units"][f"case|{w}|{d}|{h}"]["parts"] if q[0] == bf][0]
        print("check", w, d, style, f"{h}F", measure(posed(hg.file_tris(bf), q[3])), flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[2:3] == ["check"]:
        check_heights(json.load(open(sys.argv[1], encoding="utf-8")))
    else:
        main(sys.argv[1], sys.argv[2:3] != ["files"])
