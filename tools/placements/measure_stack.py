"""A tower's base, wheels and feet (stack|<w>|<d>), measured on the files (numpy, no Blender).

  python -I measure_stack.py <stl-placements.json> <out.json> [w ...]

Frame: the unit frame of the tower's first module (three.js axes, origin at the middle of the module's front bottom
edge, +Y up, +Z to the front). The base and what hangs under it have y < 0.

- Base (manual "Modifications Assembly" 1-7/15): its top is the top of a module (the same latch pockets and
  "align to connect" ribs), so the first module latches onto it like onto a module below. Pose: the file's 45 deg
  print tilt removed (L, XL), then of the quarter turns that put the base's 52.2 mm along y, the one whose top's
  pockets match a 1F module's top (depth maps from above, pockets = more than 1 mm under the top face); x centred,
  top at y = 0, and slid front to back until the pockets line up (best overlap, 0.25 mm steps).
  The split bases (6 and 7 deep: Part 1 + Part 2) are exported assembled to each other in the CAD file: they take the
  whole base's turn and fill its box.
"""
import json, os, re, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vault_geom as vg  # noqa: E402
import hw_geom as hg  # noqa: E402

MO = "03. MODIFICATIONS/"
STEP = 0.25


def proper_turns():
    out = []
    for p in ([0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]):
        for s in np.array(np.meshgrid([1, -1], [1, -1], [1, -1])).T.reshape(-1, 3):
            R = np.zeros((3, 3))
            for i in range(3):
                R[i, p[i]] = s[i]
            if np.linalg.det(R) > 0:
                out.append(R)
    return out


def top_mask(T, lo, hi):
    D, *_ = vg.depthmap(T, 1, 1, step=STEP, lo=lo, hi=hi)
    return (D < np.nanmax(D) - 1.0) & ~np.isnan(D), ~np.isnan(D)


def base_files(w, d):
    b = f"{MO}Base/{w}/{w}{d} Base"
    return {"whole": b + (" Whole" if d >= 6 else "") + ".stl", "parts": [b + " Part 1.stl", b + " Part 2.stl"] if d >= 6 else []}


def base_pose(pl, w, d):
    """R (file -> unit) and t for the base, with the score of the best and next turn."""
    mod = next(p for p in hg.load_unit(pl["units"][f"drawer|{w}|{d}|1"]) if re.search(r"(?i)Module 1F\.stl$", p.path))
    f = base_files(w, d)["whole"]
    T0 = hg.file_tris(f)
    P0 = T0.reshape(-1, 3)
    Rt, ax, deg = vg.best_tilt(P0)
    W = mod.hi[0] + 20
    lo, hi = [-W, -500, mod.lo[2] - 40], [W, 500, 40]
    Mm, Mo = top_mask(mod.tris - [0, mod.hi[1], 0], lo, hi)
    res = []
    for R in proper_turns():
        RR = R @ Rt
        T = T0 @ RR.T
        P = T.reshape(-1, 3)
        e = np.ptp(P, 0)
        if not (abs(e[1] - 52.2) < 1.0 and abs(e[0] - 2 * mod.hi[0]) < 15):
            continue
        c = np.array([(P[:, 0].min() + P[:, 0].max()) / 2, P[:, 1].max(), P[:, 2].max()])
        Bm, _ = top_mask(T - c, lo, hi)
        best = None
        for k in range(-120, 121):
            B = np.roll(Bm, k, axis=0)
            s = (Mm & B).sum() - 0.5 * (Mm ^ (B & Mo)).sum()
            if best is None or s > best[1]:
                best = (k, s)
        dz = best[0] * STEP
        res.append((best[1], RR, c - [0, 0, dz], dz, float(e[2])))
    res.sort(key=lambda r: -r[0])
    s, RR, c, dz, depth = res[0]
    return {"file": f, "R": RR, "t": -c, "front": dz, "back": dz - depth, "tilt": [ax, float(deg)],
            "score": float(s), "next": float(res[1][0]) if len(res) > 1 else None, "module_back": float(mod.lo[2])}


def mat(R, t):
    M = np.column_stack([R, t])
    return [round(float(v), 6) if k % 4 < 3 else round(float(v), 3) for k, v in enumerate(M.reshape(-1))]


def split_parts(base, w, d):
    """The split base's two parts: the whole base's turn, and moved so that both together fill its box."""
    fs = base_files(w, d)
    if not fs["parts"]:
        return []
    R = base["R"]
    W = (hg.file_tris(fs["whole"]).reshape(-1, 3) @ R.T) + base["t"]
    PP = np.vstack([hg.file_tris(p).reshape(-1, 3) for p in fs["parts"]]) @ R.T
    t = W.min(0) - PP.min(0)
    gap = (W.max(0) - W.min(0)) - (PP.max(0) - PP.min(0))
    return [{"file": p, "m": mat(R, t), "box_diff": [round(float(v), 2) for v in gap]} for p in fs["parts"]]


def regions_of(D, u0, w0, area, mask=None):
    from scipy import ndimage
    lab, n = ndimage.label(np.isnan(D) if mask is None else mask)
    out = []
    for k in range(1, n + 1):
        jj, ii = np.nonzero(lab == k)
        a = len(ii) * STEP * STEP
        if area[0] < a < area[1] and ii.min() > 0 and jj.min() > 0 and ii.max() < D.shape[1] - 1 and jj.max() < D.shape[0] - 1:
            out.append((u0 + STEP * ii.mean(), w0 + STEP * jj.mean(), a))
    return out


def base_features(base, parts=()):
    """In the unit frame: the rod's through hole (axis along x: y, z, radius), the base's side faces around it, and
    the holes in its underside (M6 for the foot, M8 for casters). Read on the whole base, or on its two parts where
    the whole one's decimated copy has lost the hole (XL6)."""
    try:
        return _features([base])
    except RuntimeError:
        if not parts:
            raise
        return {**_features(parts), "from_parts": True}


def _features(items):
    T = np.concatenate([hg.file_tris(b["file"]) @ np.array(b["m"]).reshape(3, 4)[:, :3].T + np.array(b["m"]).reshape(3, 4)[:, 3] for b in items])
    base = items[0]
    P = T.reshape(-1, 3)
    D, u0, w0, (u, w) = vg.depthmap(T, 0, 1, step=STEP)          # along x: u = y, w = z
    # the rod's hole: through, or at least 20 mm deep from the side (the XL6 base's hole is closed by a skin 21 mm in)
    rod = [r for r in regions_of(D, u0, w0, (120, 400), mask=np.isnan(D) | (D < np.nanmax(D) - 20))]
    if len(rod) != 1:
        raise RuntimeError(f"{base['file']}: {len(rod)} rod holes")
    ry, rz, ra = rod[0]
    near = (np.abs(P[:, 1] - ry) < 25) & (np.abs(P[:, 2] - rz) < 25)
    sides = (float(P[near, 0].min()), float(P[near, 0].max()))
    Du, u0, w0, _ = vg.depthmap(T, 1, -1, step=STEP)              # from below: u = x, w = z
    face = np.nanmin(Du)
    holes = regions_of(Du, u0, w0, (15, 120), mask=np.isnan(Du) | (Du > face + 3))   # blind holes, 3 mm deep or more
    return {"rod": [round(ry, 3), round(rz, 3), round(float(np.sqrt(ra / np.pi)), 2)], "sides": [round(s, 2) for s in sides],
            "under": [[round(h[0], 2), round(h[1], 2), round(float(np.sqrt(h[2] / np.pi)), 2)] for h in holes],
            "bottom": round(float(P[:, 1].min()), 3)}


# Wheels (Modifications Assembly 2-7/15): an M16 rod through the base's hole, cut to 248 / 338 / 414 / 504 mm (S, M, L,
# XL) and centred; on each end a printed bushing pushed on with the jig so that 10 mm of rod stays out (a 10 mm thick
# SCSAW collar goes there), a 6205ZZ bearing (25 x 52 x 15) on the bushing's 15 mm seat against its shoulder, the
# disk over the bearing (the bearing against the disk's shoulder, 5 mm into its bore), the cover bolted onto the disk
# from inside with 6 M4 x 25 (its bore takes the rest of the bearing), the TPU tire on both rims. Every wheel part
# is printed flat with its axis along the file's z.
ROD = {"S": 248.0, "M": 338.0, "L": 414.0, "XL": 504.0}
WH = MO + "Wheels/"
# file -> unit, axis along unit +x (the right wheel, outwards): (unit x, unit y, unit z) from the file's (x, y, z).
# The same in-plane map up to a mirror, so that the disk's bolt holes, the cover's bosses and the tire's lobes, at
# 30 + 60 k deg in every file, line up.
OUT_PLUS = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]], float)    # file +z outwards
OUT_MINUS = np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]], float)   # file -z outwards


def centred(f):
    T = hg.file_tris(f)
    P = T.reshape(-1, 3)
    return T, (P.min(0) + P.max(0)) / 2


def place(f, R, src, dst):
    """Matrix putting the file point src on the unit point dst, turned by R."""
    return R, np.asarray(dst, float) - R @ np.asarray(src, float)


def posed(f, R, t):
    return hg.file_tris(f) @ R.T + t


def disk_shoulder(T, c):
    """The disk's bearing shoulder: lowest file z of its material between r 17 and 25 (relative to c)."""
    from kinematics import polygon
    g = polygon(hg.section(T - c, 1, 0.013), (0, 2))
    from shapely.geometry import box
    h = g.intersection(box(17, -50, 25, 50))
    return float(h.bounds[1])


def touch_along_x(fixed, moving, ry, rz, rad, outwards=True):
    """How far to move `moving` along +x (outwards: towards -x) until it touches `fixed`: depth maps along x over a
    disc of radius rad around the axis."""
    lo, hi = [-1e4, ry - rad, rz - rad], [1e4, ry + rad, rz + rad]
    Df, *_ = vg.depthmap(fixed, 0, 1, step=0.5, lo=lo, hi=hi)       # the fixed part's outermost x per ray
    Dm, *_ = vg.depthmap(moving, 0, -1, step=0.5, lo=lo, hi=hi)     # the moving part's innermost x per ray
    gap = Dm - Df
    return float(np.nanmin(gap))


def tire_fit(rims, tire_f, R, src, ry, rz, x0):
    """Axial place of the tire on the rims: least overlap of their cuts through the axis (planes y = ry and z = rz),
    the middle of the best range."""
    from kinematics import polygon
    def cut(T):
        return [polygon(hg.section(T, 1, ry + 0.013), (0, 2)), polygon(hg.section(T, 2, rz + 0.013), (0, 1))]
    rc = cut(rims)
    best = []
    for dx in np.arange(-12, 12.001, 0.1):
        Rt, t = place(tire_f, R, src, (x0 + dx, ry, rz))
        tc = cut(posed(tire_f, Rt, t))
        ov = sum(a.intersection(b).area for a, b in zip(rc, tc))
        best.append((ov, dx))
    m = min(b[0] for b in best)
    ok = [dx for ov, dx in best if ov <= m + 0.5]
    return (ok[0] + ok[-1]) / 2, m


def wheels(w, feats):
    ry, rz, _ = feats["rod"]
    xe = ROD[w] / 2
    parts, notes = [], {}
    # bushing: seat outwards, its flange against the base's side (flat there, no counterbore round the rod's hole).
    # The manual's rod lengths leave 8.6 (S), 9.0 (M), 9.2 (L), 9.6 (XL) mm of rod beyond it for the collar, not
    # the jig's 10: they are rounded.
    fb = WH + "Bushing.stl"
    Tb, cb = centred(fb)
    Pb = Tb.reshape(-1, 3)
    side = feats["sides"][1]
    Rb, tb = place(fb, OUT_PLUS, (cb[0], cb[1], Pb[:, 2].min()), (side, ry, rz))
    xs = side + float(np.ptp(Pb[:, 2])) - 15.0              # bearing's inner face = the bushing's shoulder (15 mm seat)
    # disk: its shoulder on the bearing's inner face, file -z outwards
    fd = WH + "Disk.stl"
    Td, cd = centred(fd)
    zs = disk_shoulder(Td, cd)
    Rd, td = place(fd, OUT_MINUS, (cd[0], cd[1], cd[2] + zs), (xs, ry, rz))
    disk = posed(fd, Rd, td)
    # cover: file +z outwards, pushed in until it touches the disk
    fc = WH + "Cover.stl"
    Tc, cc = centred(fc)
    Pc = Tc.reshape(-1, 3)
    x_out = float(disk.reshape(-1, 3)[:, 0].max())
    Rc, tc = place(fc, OUT_PLUS, (cc[0], cc[1], Pc[:, 2].min()), (x_out + 5, ry, rz))
    gap = touch_along_x(disk, posed(fc, Rc, tc), ry, rz, 72)
    tc = tc - [gap, 0, 0]
    cover = posed(fc, Rc, tc)
    # tire: either way round, on both rims
    ft = WH + "Tyre (TPU).stl"
    Tt, ct = centred(ft)
    rims = np.concatenate([disk, cover])
    x0 = float((rims.reshape(-1, 3)[:, 0].min() + rims.reshape(-1, 3)[:, 0].max()) / 2)
    fits = []
    for nm, R in (("+", OUT_PLUS), ("-", OUT_MINUS)):
        dx, ov = tire_fit(rims, ft, R, ct, ry, rz, x0)
        fits.append((ov, nm, R, dx))
    ov, nm, Rt_, dx = min(fits, key=lambda f: f[0])
    Rt, tt = place(ft, Rt_, ct, (x0 + dx, ry, rz))
    right = [(fb, "mech", Rb, tb), (fd, "body", Rd, td), (fc, "body", Rc, tc), (ft, "accent", Rt, tt)]
    # the left wheel: the right one turned half a turn about the vertical through the base's middle
    H = np.diag([-1.0, 1, -1])
    zc = rz            # turn about the vertical through (0, *, rz): the axis maps onto itself
    for f, role, R, t in right:
        parts.append({"file": f, "role": role, "m": mat(R, t), "side": "right"})
        t2 = H @ (t - [0, 0, zc]) + [0, 0, zc]
        parts.append({"file": f, "role": role, "m": mat(H @ R, t2), "side": "left"})
    inner = float(min(posed(f, R, t).reshape(-1, 3)[:, 0].min() for f, _, R, t in right))
    notes.update({"rod_end": xe, "rod_beyond_bushing": round(xe - side - float(np.ptp(Pb[:, 2])), 2), "bearing_inner_face": xs, "cover_push": round(gap, 3), "tire_way": nm, "tire_overlap_mm2": round(ov, 2),
                  "tire_dx": round(dx, 2), "wheel_inner_x": round(inner, 2), "base_side": feats["sides"][1],
                  "clear_of_base": round(inner - feats["sides"][1], 2), "wheel_bottom": round(ry - 80.0, 2)})
    return parts, notes


# Foot (Modifications Assembly 6/15, step 8): under the base's front, bolted up through its two holes with M6 x 90
# into the base's two blind holes. Its flat full face against the base, its rounded end to the front (the outline
# drawn under the base), the floor face with the bolt heads down.
FOOT_R = np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]], float)     # file -z up, file -y to the front


def foot(w, feats):
    ff = f"{MO}Feet/{w} Feet.stl"
    T, c = centred(ff)
    D, u0, w0, _ = vg.depthmap(T, 2, 1, step=STEP)
    hs = regions_of(D, u0, w0, (10, 80))
    if len(hs) != 2:
        raise RuntimeError(f"{ff}: {len(hs)} holes")
    fh = np.array([[h[0], h[1], T.reshape(-1, 3)[:, 2].min()] for h in hs]).mean(0)    # file: holes' middle, top face
    bh = [h for h in feats["under"] if h[2] < 3.2]                                     # the base's M6 holes
    if len(bh) != 2:
        raise RuntimeError(f"{w}: {len(bh)} foot holes under the base")
    dst = (float(np.mean([h[0] for h in bh])), feats["bottom"], float(np.mean([h[1] for h in bh])))
    R, t = place(ff, FOOT_R, fh, dst)
    P = posed(ff, R, t).reshape(-1, 3)
    # check: each foot hole under a base hole
    fhs = sorted(((R @ [h[0], h[1], 0.0] + t)[[0, 2]] for h in hs), key=lambda v: v[0])
    bhs = sorted((np.array([h[0], h[1]]) for h in bh), key=lambda v: v[0])
    err = max(float(np.linalg.norm(a - b)) for a, b in zip(fhs, bhs))
    return {"file": ff, "role": "mech", "m": mat(R, t)}, {"foot_bottom": round(float(P[:, 1].min()), 2), "hole_error": round(err, 2),
                                                          "foot_front": round(float(P[:, 2].max()), 2), "foot_back": round(float(P[:, 2].min()), 2)}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    pl = json.load(open(sys.argv[1], encoding="utf-8"))
    out = json.load(open(sys.argv[2], encoding="utf-8")) if os.path.exists(sys.argv[2]) else {}
    for w in sys.argv[3:] or ["S", "M", "L", "XL"]:
        for d in range(3, 8):
            b = base_pose(pl, w, d)
            parts = split_parts(b, w, d)
            base = {"file": b["file"], "m": mat(b["R"], b["t"]), "front": b["front"], "back": round(b["back"], 2),
                    "module_back": b["module_back"], "tilt": b["tilt"], "score": b["score"], "next": b["next"]}
            feats = base_features(base, parts)
            wp, wn = wheels(w, feats)
            fp, fn = foot(w, feats)
            out[f"stack|{w}|{d}"] = {"base": base, "base_parts": parts, "features": feats, "wheels": wp, "wheel_notes": wn,
                                     "foot": fp, "foot_notes": fn}
            print("   ", feats["rod"], wn, fn, flush=True)
            print(w, d, "front %.2f back %.2f (module back %.1f) tilt %s score %.0f next %s" % (b["front"], b["back"], b["module_back"], b["tilt"], b["score"], b["next"]),
                  [p["box_diff"] for p in parts], flush=True)
    json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), indent=1)
