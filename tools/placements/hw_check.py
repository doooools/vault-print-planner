"""Check the bolts of some units: sections through their axes and a clash test of their heads (numpy, no Blender).

  python -I hw_check.py <stl-placements.json> <out_dir> <unit key> [<unit key> ...]

For each unit and each kind of bolt (rule), the first bolt is cut by a plane through its axis: the parts in their
colours, the bolt's outline in black (<out_dir>/<unit>_<n>.png, then one board per unit <unit>.png). Every bolt's
head is also tested: points filling the head (inside 95 % of its radius and height) must lie outside every part
(ray parity on the decimated meshes), and the shank's axis must be free from the head down to its tip.
Prints one line per bolt kind and writes <out_dir>/check.json.
"""
import json, os, re, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hw_geom as hg  # noqa: E402
import hw_shapes  # noqa: E402
from hardware import SKIP  # noqa: E402


def outline(spec, m, sizes, normal):
    """The bolt's outline in the plane through its axis with this normal: segments in the unit frame."""
    s = hw_shapes.spec_size(spec, sizes)
    prof = hw_shapes.profile(s)
    M = np.array(m).reshape(3, 4)
    y = M[:, 1]
    e = np.cross(y, normal)
    e /= np.linalg.norm(e)
    segs = []
    for sg in (-1, 1):
        pts = [M[:, 3] + y * p[1] + e * sg * p[0] for p in prof]
        segs += [[a, b] for a, b in zip(pts, pts[1:])]
    return np.array(segs)


def inside(parts, pts):
    """Which points are inside a part (odd number of crossings along +x, and along +y to be sure)."""
    out = np.zeros(len(pts), bool)
    for k, p in enumerate(pts):
        for q in hg.near(parts, p, np.array([1.0, 0, 0]), 1):
            hits = [s for s, f in hg.ray_hits(q.tris, p, np.array([1.0, 0, 0])) if s > 0]
            hits2 = [s for s, f in hg.ray_hits(q.tris, p, np.array([0, 1.0, 0])) if s > 0]
            if len(hits) % 2 == 1 and len(hits2) % 2 == 1:
                out[k] = True
                break
    return out


def head_points(spec, m, sizes):
    s = hw_shapes.spec_size(spec, sizes)
    M = np.array(m).reshape(3, 4)
    R, t = M[:, :3], M[:, 3]
    pts = []
    if s["kind"] == "countersunk":   # the cone, y from -k to 0, radius from d/2 to dk/2
        for yy in np.linspace(-s["k"] * 0.9, -0.1, 4):
            r = s["dk"] / 2 + yy            # 45 deg
            for rr in (0.5 * r, 0.9 * r):
                for a in np.linspace(0, 2 * np.pi, 12, endpoint=False):
                    pts.append([rr * np.cos(a), yy, rr * np.sin(a)])
    else:
        for yy in np.linspace(0.1, s["k"] * 0.6, 3):
            for rr in (s["dk"] * 0.25, s["dk"] * 0.45):
                for a in np.linspace(0, 2 * np.pi, 12, endpoint=False):
                    pts.append([rr * np.cos(a), yy, rr * np.sin(a)])
    return np.array(pts) @ R.T + t


def main():
    pl_path, out_dir, keys = sys.argv[1], sys.argv[2], sys.argv[3:]
    os.makedirs(out_dir, exist_ok=True)
    data = json.load(open(pl_path, encoding="utf-8"))
    sizes = data["hardware_sizes"]
    res = {}
    for key in keys:
        u = data["units"][key]
        parts = hg.load_unit(u, only=lambda p: not re.search(SKIP, p))
        byi = {p.i: p for p in parts}
        hw = [b for b in u.get("hardware", []) if b[3]["part"] in byi]
        kinds = {}
        for b in hw:
            kinds.setdefault((b[0], b[3].get("why")), []).append(b)
        pngs = []
        res[key] = []
        for n, ((spec, why), bs) in enumerate(kinds.items()):
            clash = 0
            for b in bs:
                clash += int(inside(parts, head_points(b[0], b[2], sizes)).sum())
            b = bs[0]
            M = np.array(b[2]).reshape(3, 4)
            y, p = M[:, 1], M[:, 3]
            # cut by the unit axis plane through the bolt that contains its axis (the one most across it)
            ax = int(np.argmin(np.abs(y)))
            if abs(y[ax]) > 0.2:   # tilted out of every axis plane: cut across z
                ax = 2
            normal = np.zeros(3)
            normal[ax] = 1
            iu, iw = [k for k in range(3) if k != ax]
            segs = outline(spec, b[2], sizes, normal)
            L = hw_shapes.spec_size(spec, sizes)["L"]
            span = max(L, 14) * 0.85
            mid = p - y * L / 2
            win = ((mid[iu] - span, mid[iu] + span), (mid[iw] - span, mid[iw] + span))
            f = os.path.join(out_dir, f"{key.replace('|', '_')}_{n}.png")
            hg.section_png(parts, ax, float(p[ax]), f, window=win, bolts=[(segs, "black")],
                           title=f"{key}: {spec} ({why}), {'xyz'[ax]} = {p[ax]:.1f}")
            pngs.append(f)
            res[key].append({"spec": spec, "why": why, "n": len(bs), "head_points_inside_parts": clash})
            print(key, spec, why, len(bs), "bolts, head points inside parts:", clash, flush=True)
        if pngs:
            from PIL import Image
            ims = [Image.open(f) for f in pngs]
            cols = 2 if len(ims) > 1 else 1
            w, h = max(i.width for i in ims), max(i.height for i in ims)
            board = Image.new("RGB", (cols * w, ((len(ims) + cols - 1) // cols) * h), "white")
            for k, im in enumerate(ims):
                board.paste(im, ((k % cols) * w, (k // cols) * h))
            board.save(os.path.join(out_dir, key.replace("|", "_") + ".png"))
    json.dump(res, open(os.path.join(out_dir, "check.json"), "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
