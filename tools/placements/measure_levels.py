"""Where each drawer level of a 2F or 4F module shell is, measured on the shell itself (numpy + shapely, no Blender).

  python -I measure_levels.py <stl-placements.json> <out.json> [unit key regex]

A 1F drawer locks with its racks' tabs in two pockets of the module's side walls and its key's cam in two notches
of the module's front frame (README "Motion"). A 2F or 4F shell that takes several boxes has the side pockets on
every 48 mm level. For each 2F/4F shell (S, M, L, L², every depth) and each level k, this cuts the shell and the
1F shell of the same width and depth (both as placed in the JSON, unit frame) by planes z = const through the
racks (-2.0 to -4.4 mm, the channels' depth), keeps the side walls (and the L² middle wall), and slides the 1F cut up
by 48 k + dy, dy from -3 to +3 mm in 0.05 mm steps. The dy where the two cuts differ least is where level k's
features are; the residual (mm² of the cuts' symmetric difference over the window) says how alike they are.
Also reported per level: the front frame's notches (cut z = -1.0 at the key's x), which a box above level 0
doesn't find (the frame is only at the shell's bottom and top).
"""
import json, re, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vault_geom as vg  # noqa: E402
import hw_geom as hg  # noqa: E402
from shapely.geometry import box as sbox  # noqa: E402
from shapely import affinity  # noqa: E402

PITCH = 48.0
ZS = (-2.0, -3.2, -4.4)        # through the racks' channels (centred 3.1 mm behind the box front)


def shell(entry):
    p = next(p for p in entry["parts"] if re.search(r"(?i)Module \dF\.stl$", p[0]))
    R, t = vg.mat34(p[3])
    return hg.file_tris(p[0]) @ R.T + t


def cut(T, z):
    from kinematics import polygon
    S = hg.section(T, 2, z)
    return polygon(S, (0, 1))


def walls(W, mid):
    """Window over the side walls (and the middle wall of an L²), 22 mm in from each."""
    xs = [(-W / 2 - 1, -W / 2 + 22), (W / 2 - 22, W / 2 + 1)]
    if mid:
        xs.append((-12, 12))
    return xs


Y0, Y1 = 9.0, 47.0   # the 1F level between its bottom and top walls: both pockets (11.3-14.3 and 38.8-44 mm up)


def level_fit(P1, Ph, k, W, mid):
    """(dy, residual at dy, residual 1 mm either side): the 1F cut slid up by 48 k + dy against the shell's cut."""
    def res(dy):
        sh = affinity.translate(P1, 0, PITCH * k + dy)
        tot = 0.0
        for xa, xb in walls(W, mid):
            win = sbox(xa, PITCH * k + dy + Y0, xb, PITCH * k + dy + Y1)
            tot += sh.intersection(win).symmetric_difference(Ph.intersection(win)).area
        return tot
    rs = [(round(float(dy), 2) + 0.0, res(dy)) for dy in np.arange(-3.0, 3.0001, 0.05)]
    dy, r = min(rs, key=lambda v: v[1])
    return dy, round(r, 1), round(min(res(dy - 1), res(dy + 1)), 1)


def frame_notches(T, ux=0.0):
    """y ranges of the front frame's material at x = ux, cut at z = -1 (the frame's lip)."""
    S = hg.section(T, 2, -1.0)
    ys = []
    for a, b in S:
        if (a[0] - ux) * (b[0] - ux) <= 0 and a[0] != b[0]:
            f = (ux - a[0]) / (b[0] - a[0])
            ys.append(a[1] + f * (b[1] - a[1]))
    return sorted(round(float(y), 2) for y in ys)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    pl = json.load(open(sys.argv[1], encoding="utf-8"))
    only = re.compile(sys.argv[3]) if len(sys.argv) > 3 else None
    out = {}
    for key, entry in pl["units"].items():
        m = re.match(r"drawer\|(S|M|L|L2)\|(\d)\|([24])$", key)
        if not m or (only and not only.search(key)):
            continue
        w, d, h = m.group(1), int(m.group(2)), int(m.group(3))
        T1, Th = shell(pl["units"][f"drawer|{w}|{d}|1"]), shell(entry)
        W = float(np.ptp(Th.reshape(-1, 3)[:, 0]))
        res = {"levels": []}
        C1, Ch = {z: cut(T1, z) for z in ZS}, {z: cut(Th, z) for z in ZS}
        for k in range(h):
            fits = [level_fit(C1[z], Ch[z], k, W, w == "L2") for z in ZS]
            res["levels"].append({"k": k, "dy": [f[0] for f in fits], "residual_mm2": [f[1] for f in fits],
                                  "residual_1mm_off_mm2": [f[2] for f in fits]})
        uxs = [0.0] if w != "L2" else [-82.4, 82.4]
        res["frame_at_key"] = {str(ux): frame_notches(Th, ux) for ux in uxs}
        res["frame_at_key_1F"] = {str(ux): frame_notches(T1, ux) for ux in uxs}
        out[key] = res
        print(key, [(L["k"], L["dy"], L["residual_mm2"]) for L in res["levels"]], res["frame_at_key"], flush=True)
    json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), indent=1)
