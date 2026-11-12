"""The module connectors ("Connector for Modules 1F / 2F", in the Backbone folder), measured on the files (numpy).

  python -I measure_connectors.py <stl-placements.json>

Writes `connectors` into the placements (other keys untouched):
  { holes: {inset, low, high, pitch, d}, pair: 14.5, files: {"1": [file, m], "2": [file, m]}, t, h: {"1", "2"} }

What the files say (no USSA page about these parts was at hand):
- Every drawer module (measured on S3 1F/2F, M3 1F, L3 2F, XL3 1F, XL3² 1F) has, in its back face, a hole 8.15 mm in
  from each side edge at each level's bottom and top: 9.57 and 47.07 mm above the module's bottom, then every 48 mm up
  (a 5.6 mm mouth 5 mm deep, then a 3.6 mm pilot about 40 mm on). An L² / XL² shell has them at its inner seam too, as
  if it were two modules. A case body (S3 1F) has none, and the base's (19.1 mm from the next module's) don't line up.
- The connector is a bar 16.3 wide, 12 thick, as tall as a 1F or 2F backbone (47.15 / 99.15), flat on one face and
  rounded on the other, with 4.2 mm holes on its centre line: 16.32 and 30.82 mm from its bottom (1F), plus 68.32 and
  82.82 (2F). 14.5 mm is the gap between a module's top corner hole and the next module's bottom one (47.07 against
  52 + 9.57: the rise of a drawer module is 52 + 48 per extra level). So a 1F connector ties a module to the one on it at
  one back corner, flush with their side; a 2F one ties three: its second pair is 52 mm higher, the joint above a 1F
  module.
Frame of `m`: three.js axes, x = 0 on the corner holes' column, y = 0 at the lower module's top corner hole, z = 0 on
the modules' back face, -z away from them (its flat face on the modules, its rounded one out).
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hw_geom as hg  # noqa: E402
from measure_column import mat, circle_fit  # noqa: E402

BB = "03. MODIFICATIONS/Backbone/"
MODULE = ("drawer|S|3|1", "S3 Module 1F.stl")


def corner_holes(pl):
    """The module's back corner holes: inset from the side, height of the lowest and highest, diameter of the pilot."""
    key, name = MODULE
    q = next(p for p in pl["units"][key]["parts"] if p[0].endswith(name))
    M = np.array(q[3]).reshape(3, 4)
    T = hg.file_tris(q[0]) @ M[:, :3].T + M[:, 3]
    P = T.reshape(-1, 3)
    lo, hi = P.min(0), P.max(0)
    out = []
    for z, r in ((lo[2] + 2, (2.0, 3.5)), (lo[2] + 20, (1.2, 2.5))):
        s = hg.section(T, 2, z + 0.013).reshape(-1, 3)[:, :2]
        row = []
        for g in ([hi[0] - 8.15, 9.57], [hi[0] - 8.15, 47.07], [lo[0] + 8.15, 9.57]):
            d = np.linalg.norm(s - g, axis=1)
            c, rad = circle_fit(s[(d > r[0]) & (d < r[1])])
            row.append((c, 2 * rad))
        out.append(row)
    (c0, mouth), (c1, _), (c2, _) = out[0]
    pilot = out[1][0][1]
    return {"inset": round(float(hi[0] - c0[0]), 2), "inset_left": round(float(c2[0] - lo[0]), 2),
            "low": round(float(c0[1] - lo[1]), 2), "high": round(float(c1[1] - lo[1]), 2), "pitch": 48.0,
            "mouth": round(float(mouth), 2), "pilot": round(float(pilot), 2)}


def connector(h):
    f = BB + f"Connector for Modules {h}F.stl"
    T = hg.file_tris(f)
    P = T.reshape(-1, 3)
    lo, hi = P.min(0), P.max(0)
    # the flat face: the z end with the most area facing out
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    area = lambda z, sg: float(np.linalg.norm(n[(np.abs(T[:, :, 2] - z).max(1) < 0.01) & (np.sign(n[:, 2]) == sg)], axis=1).sum() / 2)
    flat_lo = area(lo[2], -1) > area(hi[2], 1)
    # the holes along its centre line: circles in a section through its middle
    s = hg.section(T, 2, (lo[2] + hi[2]) / 2 + 0.013).reshape(-1, 3)[:, :2]
    cx = (lo[0] + hi[0]) / 2
    holes = []
    for y in np.arange(lo[1] + 2, hi[1] - 2, 0.5):
        d = np.linalg.norm(s - [cx, y], axis=1)
        p = s[(d < 3.0)]
        if len(p) >= 12:
            c, r = circle_fit(p)
            if abs(np.linalg.norm(p - c, axis=1) - r).max() < 0.1 and 1.5 < r < 2.5 and not any(abs(c[1] - q[0]) < 1 for q in holes):
                holes.append((float(c[1]), float(c[0]), 2 * r))
    holes.sort()
    first = holes[0][0]
    # its flat face on the modules (z = 0), the rest towards -z; a half turn about y when the flat face is at file +z
    R = np.diag([-1.0, 1, -1]) if flat_lo else np.eye(3)
    zface = lo[2] if flat_lo else hi[2]
    t = -R @ np.array([holes[0][1], first, zface])
    return {"file": f, "m": mat(R, t), "h": round(float(hi[1] - lo[1]), 2), "t": round(float(hi[2] - lo[2]), 2),
            "w": round(float(hi[0] - lo[0]), 2), "holes": [round(y - first, 2) for y, _, _ in holes],
            "hole_y": [round(y - lo[1], 2) for y, _, _ in holes], "d": round(float(np.mean([d for *_, d in holes])), 2),
            "flat": "file -z" if flat_lo else "file +z"}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    path = sys.argv[1]
    pl = json.load(open(path, encoding="utf-8"))
    ch = corner_holes(pl)
    print("corner holes", json.dumps(ch))
    out = {"holes": ch, "files": {}, "h": {}}
    for h in (1, 2):
        c = connector(h)
        print(f"{h}F", json.dumps({k: v for k, v in c.items() if k not in ("m", "file")}))
        out["files"][str(h)] = [c["file"], c["m"]]
        out["h"][str(h)] = c["h"]
        out["t"] = c["t"]
        out["w"] = c["w"]
        if h == 1:
            out["pair"] = c["holes"][1]
            out["bottom"] = c["hole_y"][0]
    gap = round(ch["low"] + 52.0 - ch["high"], 2)
    print("module top hole to next module's bottom one:", gap, "connector's pair:", out["pair"])
    pl["connectors"] = out
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pl, f, ensure_ascii=False, separators=(",", ":"))
