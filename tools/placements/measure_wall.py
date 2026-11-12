"""The wall mount plates and their wall cleats (wall|<w>|<h>), measured on the files (numpy, no Blender).

  python -I measure_wall.py <stl-placements.json>

Writes `wall|<w>|<h>` (w: S M L XL, h: 1 2 4; XL 1F only) into the placements, other keys untouched. Each entry
holds the plate and its cleats in a frame of its own: three.js axes, x = 0 in the middle of the module's width,
y = 0 at the bottom of the module's flat back face (5 mm above the module's bottom on drawers and cases alike: the
module's lowest 5 mm nest into the one below), z = 0 on that back face, -z away from the module, towards the wall.
The page moves it onto a unit's back (placeParts in src/template.html). The Wall Mount Instructions aren't at hand:
what the files say is used, and what is inferred is said so.

- Plate: as wide as the module, 14 mm thick, 3.1 mm taller than a module's rise (52 / 100 / 196): a band of tabs at
  its bottom and of teeth at its top that interleave with the plates above and below. Its wall side (file -z) is
  flat, with an 8 mm counterbore on each of its holes (2 rows per F): it is screwed onto the module's back through
  them, the heads sunk on the wall side. Its module side (file +z) has a few 3 mm nubs along its top. A trapezoid
  opening per cleat, wide end down, goes through it. So it keeps the file's own turn: file +y up, file +z towards the
  module, its main module-side level on the module's back (z = 0).
  Height on the module (inferred): its holes centred on the module's flat back face (5 to 52 + 48 (h - 1) mm above the
  module's bottom), which puts its bottom 2.13 mm above that face's bottom.
- Cleat ("second part"): a trapezoid 102.5 mm wide at its wide end, 67 at its narrow one, 24.2 tall, flat on its
  wall side, screwed to the wall through 3 holes. It goes into the plate's trapezoid opening, both wide ends down:
  the plate is lowered onto the cleat until the slopes meet (here: pushed up into the opening until it touches).
  Its wall side is flush with the plate's (inferred).
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vault_geom as vg  # noqa: E402
import hw_geom as hg  # noqa: E402
from measure_column import mat, posed  # noqa: E402

WM = "03. MODIFICATIONS/Wall Mounts/"
CLEAT = WM + "Wall Mount Second Part.stl"


def openings(T, band, step=0.25):
    """The plate's through openings bigger than a bolt hole, above its bottom band of tabs (an opening may run out
    through the bottom, as on 1F plates): [(x0, x1, y0, y1)] in T's frame."""
    from scipy import ndimage
    D, u0, w0, _ = vg.depthmap(T, 2, 1, step)
    j0 = int(np.ceil(band / step)) + 1
    D = D[j0:]
    w0 += j0 * step
    lab, n = ndimage.label(np.isnan(D))
    out = []
    for k in range(1, n + 1):
        jj, ii = np.nonzero(lab == k)
        if len(ii) * step * step < 500 or ii.min() == 0 or ii.max() == D.shape[1] - 1 or jj.max() == D.shape[0] - 1:
            continue
        y0 = w0 + step * jj.min()
        out.append((u0 + step * ii.min(), u0 + step * (ii.max() + 1), y0 - (band + step if jj.min() == 0 else 0), w0 + step * (jj.max() + 1)))
    return sorted(out)


def slide(fixed, moving, lo, hi, sign, step=0.25, clear=0.05):
    """How far `moving` can go along y (sign +1 up, -1 down) before it runs into `fixed`. Each part is taken as a slab
    per (x, y) cell between its two faces seen along z, which holds for these plates and cleats."""
    F = [vg.depthmap(fixed, 2, s, step, lo, hi)[0] for s in (1, -1)]
    M = [vg.depthmap(moving, 2, s, step, lo, hi)[0] for s in (1, -1)]
    n = F[0].shape[0]
    for k in range(1, n):
        if sign > 0:
            ft, fb, mt, mb = F[0][k:], F[1][k:], M[0][:n - k], M[1][:n - k]
        else:
            ft, fb, mt, mb = F[0][:n - k], F[1][:n - k], M[0][k:], M[1][k:]
        both = np.isfinite(ft) & np.isfinite(mt)
        if (np.minimum(ft[both], mt[both]) - np.maximum(fb[both], mb[both]) > clear).any():
            return (k - 1) * step
    return None


def wall(w, h):
    f = WM + f"{w}{h}F Wall Mount.stl"
    T = hg.file_tris(f)
    P = T.reshape(-1, 3)
    lo, hi = P.min(0), P.max(0)
    # the module side's main level (the nubs stand 3 mm proud of it)
    D, *_ = vg.depthmap(T, 2, 1, 0.25)
    vals, cnt = np.unique(D[np.isfinite(D)].round(1), return_counts=True)
    face = float(vals[np.argmax(cnt)])
    nubs = float(np.nanmax(D))
    # its holes, centred on the module's back face (5 mm above the unit's bottom, 47 + 48 (h - 1) tall)
    class Part: pass
    pp = Part(); pp.tris, pp.lo, pp.hi = T, lo, hi
    ys = sorted({round(float(c["c"][1] - lo[1]), 2) for c in hg.holes_in(pp, 2, 1, area=(3, 60))})
    b = 5 + (47 + 48 * (h - 1)) / 2 - (ys[0] + ys[-1]) / 2
    t = np.array([-(lo[0] + hi[0]) / 2, -lo[1] + b, -face])
    m = mat(np.eye(3), t)
    Tp = posed(T, m)
    out = {"parts": [[f, "base", "module", m, {"as": "plate"}]]}
    C = hg.file_tris(CLEAT)
    Q = C.reshape(-1, 3)
    clo, chi = Q.min(0), Q.max(0)
    wall_z = float(lo[2] - face)       # the plate's flat (wall) side, in the frame
    cleats = []
    for (x0, x1, y0, y1) in openings(Tp, b + 3.2):
        # cleat: its flat side on the wall, wide end down, centred under the opening, then pushed up into it until
        # it touches the plate
        ct = np.array([(x0 + x1) / 2 - (clo[0] + chi[0]) / 2, y0 + 1.0 - clo[1], wall_z - clo[2]])
        Tc = posed(C, mat(np.eye(3), ct))
        win = (np.array([x0 - 5, y0 - 1, -40]), np.array([x1 + 5, y1 + 40, 40]))
        up = slide(Tp, Tc, *win, +1)
        if up is None:
            raise RuntimeError(f"{f}: the cleat goes through the opening at {x0:.1f}..{x1:.1f}")
        ct[1] += up
        out["parts"].append([CLEAT, "fittings", "module", mat(np.eye(3), ct), {"as": "cleat"}])
        cleats.append({"opening": [round(v, 2) for v in (x0, x1, y0, y1)], "up": round(up, 2), "bottom": round(float(ct[1] + clo[1]), 2)})
    out["wall"] = {"bottom": round(b, 2), "h": round(float(hi[1] - lo[1]), 2), "t": round(face - float(lo[2]), 2),
                   "nubs": round(nubs - face, 2), "cleats": len(cleats)}
    return out, {"holes_y": ys, "cleats": cleats}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    path = sys.argv[1]
    pl = json.load(open(path, encoding="utf-8"))
    for w in ["S", "M", "L", "XL"]:
        for h in ((1,) if w == "XL" else (1, 2, 4)):
            u, notes = wall(w, h)
            pl["units"][f"wall|{w}|{h}"] = {"name": f"{w}{h}F wall mount", **u}
            print(w, h, json.dumps(u["wall"]), json.dumps(notes), flush=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pl, f, ensure_ascii=False, separators=(",", ":"))
