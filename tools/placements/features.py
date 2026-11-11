"""Measure assembly features on posed parts with depth maps (numpy, no Blender).

Library used by make_recipes.py; run alone to print what it finds:
  python features.py facade <rel.stl> [rot_x rot_y rot_z]
  python features.py under  <rel.stl> rot_x rot_y rot_z      (a module or roof seen from below)
  python features.py side   <rel.stl> rot_x rot_y rot_z      (a module's right wall seen from outside)

Everything is in the unit frame (three.js axes, see vault_geom.py), with the part's bounding box
set so that its front-bottom-centre is the origin (x centred, y from 0 up, front face at z = 0,
so the part runs to negative z). Rotations are the recipes' (Blender XYZ Euler, CAD frame).
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vault_geom as vg  # noqa: E402

ROOT = os.environ.get("VAULT_RENDER", "VAULT_RENDER")
STEP = 0.25


def posed_fbc(rel, rot_cad):
    """Triangles in the unit frame, front-bottom-centre of the bbox at the origin."""
    R = vg.C @ vg.from_euler_xyz(rot_cad)
    t = vg.read_stl(os.path.join(ROOT, rel)) @ R.T
    P = t.reshape(-1, 3)
    lo, hi = P.min(0), P.max(0)
    return t - np.array([(lo[0] + hi[0]) / 2, lo[1], hi[2]])


def _mask_regions(mask, D, u0, w0, min_area):
    """Regions with their exact extents."""
    from scipy import ndimage
    lab, n = ndimage.label(mask)
    out = []
    for k in range(1, n + 1):
        jj, ii = np.nonzero(lab == k)
        area = len(ii) * STEP * STEP
        if area < min_area:
            continue
        dv = D[jj, ii]
        dv = dv[~np.isnan(dv)]
        out.append({"u": round(u0 + STEP * ii.mean(), 2), "w": round(w0 + STEP * jj.mean(), 2),
                    "u_rng": [round(u0 + STEP * ii.min(), 2), round(u0 + STEP * ii.max(), 2)],
                    "w_rng": [round(w0 + STEP * jj.min(), 2), round(w0 + STEP * jj.max(), 2)],
                    "area": round(area, 1), "depth": round(float(dv.mean()), 2) if len(dv) else None,
                    "border": bool(ii.min() == 0 or jj.min() == 0 or ii.max() == mask.shape[1] - 1
                                   or jj.max() == mask.shape[0] - 1)})
    return sorted(out, key=lambda r: -r["area"])


def facade(rel, rot=(-90, 0, 0), png=None):
    """Bolt holes, counterbores (cap seats), the label slot and the key hole on a drawer front.
    u = x (right seen from the front), w = y (up)."""
    t = posed_fbc(rel, rot)
    D, u0, w0, _ = vg.depthmap(t, 2, +1, STEP)
    if png:
        vg.depth_png(D, png, 2)
    med = np.nanmedian(D)
    nan = np.isnan(D)
    holes = [r for r in _mask_regions(nan, D, u0, w0, 4) if not r["border"]]
    key = max(holes, key=lambda r: r["area"]) if holes else None
    bolts = [r for r in holes if 8 < r["area"] < 30]
    cb = [r for r in _mask_regions((D < med - 3.0) & ~nan, D, u0, w0, 30) if 40 < r["area"] < 120 and not r["border"]]
    slots = _mask_regions((D < med - 1.5) & (D > med - 3.6) & ~nan, D, u0, w0, 300)
    return {"file": rel, "front_z": round(float(med), 2), "w": round(float(np.ptp(t[..., 0])), 2),
            "h": round(float(t[..., 1].max()), 2),
            "key": key and {"u": key["u"], "w": key["w"], "d": key["u_rng"][1] - key["u_rng"][0]},
            "bolts": sorted([[b["u"], b["w"]] for b in bolts]),
            "counterbores": sorted([[c["u"], c["w"]] for c in cb]),
            "slots": [{"u": s["u_rng"], "w": s["w_rng"], "depth": s["depth"], "area": s["area"]} for s in slots]}


def under(rel, rot, png=None):
    """A module (or roof) seen from below: what stands out of its bottom face (latch frames, pads).
    u = x, w = z (0 at the front, negative to the back). Latch frames are the U-shaped rims about
    85 x 55 mm near the back."""
    t = posed_fbc(rel, rot)
    D, u0, w0, _ = vg.depthmap(t, 1, -1, STEP)
    if png:
        vg.depth_png(-D, png, 1)
    nan = np.isnan(D)
    base = float(np.nanmedian(D))
    rg = [r for r in _mask_regions((D < base - 1.0) & ~nan, D, u0, w0, 20) if not r["border"]]
    for r in rg:
        r["su"] = round(r["u_rng"][1] - r["u_rng"][0], 2)
        r["sw"] = round(r["w_rng"][1] - r["w_rng"][0], 2)
    frames = [r for r in rg if 60 < r["su"] < 110 and 35 < r["sw"] < 80]
    return {"file": rel, "base_y": round(base, 2), "frames": frames, "others": [r for r in rg if r not in frames][:12]}


def side(rel, rot, png=None):
    """A module's right wall seen from outside (+x): holes through it. u = y (up), w = z."""
    t = posed_fbc(rel, rot)
    P = t.reshape(-1, 3)
    D, u0, w0, _ = vg.depthmap(t, 0, +1, STEP)
    if png:
        vg.depth_png(D, png, 1)
    nan = np.isnan(D)
    wall = np.nanpercentile(D, 95)
    rg = _mask_regions(nan | (D < wall - 6), D, u0, w0, 4)
    return {"file": rel, "wall_x": round(float(wall), 2), "x_max": round(float(P[:, 0].max()), 2),
            "holes": [r for r in rg if not r["border"]][:20]}


def openings(rel, height):
    """For a tray-like part (a drawer box), every quarter-turn pose (after the print tilt) with its
    widest side across and `height` upright, and how deep rays go from the top, bottom, back and front
    (an open side reads deep). Used to tell which way up and which way round a box is."""
    t = vg.read_stl(os.path.join(ROOT, rel))
    T, _, _ = vg.best_tilt(t.reshape(-1, 3)[::5])
    out = []
    for G in vg.proper_rotations():
        R = G @ T
        q = t @ R.T
        P = q.reshape(-1, 3)
        e = P.max(0) - P.min(0)
        if not (e[0] >= e[2] and abs(e[1] - height) < 1.5):
            continue
        q = q - P.min(0)
        med = lambda D: float(np.nanmedian(D)) if np.isfinite(D).any() else 0.0
        out.append({"rot": vg.euler_xyz(vg.C.T @ R),
                    "top": round(e[1] - med(vg.depthmap(q, 1, +1, 1.0)[0]), 1),
                    "bottom": round(med(vg.depthmap(q, 1, -1, 1.0)[0]), 1),
                    "back": round(med(vg.depthmap(q, 2, -1, 1.0)[0]), 1),
                    "front": round(e[2] - med(vg.depthmap(q, 2, +1, 1.0)[0]), 1)})
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # paths hold ² (python -I ignores PYTHONIOENCODING)
    kind, rel = sys.argv[1], sys.argv[2]
    rot = [float(x) for x in sys.argv[3:6]] if len(sys.argv) >= 6 else [-90, 0, 0]
    png = sys.argv[6] if len(sys.argv) > 6 else None
    print(json.dumps({"facade": facade, "under": under, "side": side}[kind](rel, rot, png), ensure_ascii=False))
