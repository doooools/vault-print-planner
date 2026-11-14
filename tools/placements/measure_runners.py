"""How far a drawer's runners travel (README "Motion", "Runners"): the runner slide (on the box) in the runner guide,
and the guide in the module until the runner stopper. Horizontal sections (y = const) of the parts as placed in the
unit, in the (x, z) plane; a part is moved along +z (out of the module) until its section overlaps the other's by more
than it does as placed (0.05 mm^2): the first contact on any section is its stop.

  python -I measure_runners.py <placements.json> <vault download> [unit keys...] [--json out.json] [--write]

With no keys: one drawer of each runner file (S and XL, depths 3 to 7); `all`: every drawer unit. --write puts what
it measured into the placements (rerun after every export, like hardware.py):
  units[key].motion.runners = {"slide": s1, "guide": s2}   mm, the smallest over both sides and every level
  each runner guide part gets {"guide": k}, k its level (0 = the module's bottom one, 48 mm a level), and on an L²
  or XL² {"side": "left" | "right"}, the drawer it guides
and the drawer's opening step takes s 1.0 (it was 0.55: the box now goes s1 + s2, about its whole depth), in the
unit's steps and in its layouts' drawers'. --from <results.json> writes a run saved with --json without measuring again.
"""
import json, os, re, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kinematics as K

EPS = 0.05
MAXBASE = 0.5   # mm^2: sections where the parts already overlap more than this as placed are left out


def placed(unit, rx, download):
    """(name, triangles in the unit frame) of the parts whose path matches rx."""
    out = []
    for p in unit["parts"]:
        if re.search(rx, p[0]):
            T = K.load_tris(p[0], download, p[4].get("piece") if len(p) > 4 else None)
            m = np.array(p[3], float).reshape(3, 4)
            out.append((p, T @ m[:, :3].T + m[:, 3]))
    return out


def side(parts, s):
    """The parts on one side (s = +1 right, -1 left)."""
    return [P for p, P in parts if np.sign(P[:, :, 0].mean()) == s]


def sections(Ps, ys):
    """{y: shapely region} of the union of Ps cut at each y."""
    from shapely.ops import unary_union
    out = {}
    for y in ys:
        g = [K.polygon(K.section(P, 1, y), (0, 2)) for P in Ps if P[:, :, 1].min() < y < P[:, :, 1].max()]
        g = [x for x in g if not x.is_empty]
        if g:
            out[y] = unary_union(g)
    return out


def free_travel(A, B, dmax, step=0.5):
    """How far A (sections by y) moves along +z before it overlaps B more than as placed: (d, y, x where)."""
    from shapely.affinity import translate
    best = (dmax, None, None)
    for y, a in A.items():
        b = B.get(y)
        if b is None or b.is_empty:
            continue
        base = a.intersection(b).area
        if base > MAXBASE:
            continue   # a section through a face the parts share as placed (a stopper's rounded bottom on the guide's slot floor)
        hit = lambda d: translate(a, 0, d).intersection(b).area > base + EPS
        d = step
        while d <= best[0] and not hit(d):
            d += step
        if d > best[0]:
            continue
        lo, hi = d - step, d
        for _ in range(12):
            mid = (lo + hi) / 2
            lo, hi = (lo, mid) if hit(mid) else (mid, hi)
        where = translate(a, 0, hi).intersection(b)
        best = (hi, y, round(where.centroid.x, 2) if not where.is_empty else None)
    return best


def level_of(P):
    """A guide's level in its module: its bottom is 14.8 mm above the level's (48 mm a level)."""
    return int(round((P[:, :, 1].min() - 14.8) / 48))


def write(pl, download, res):
    """Put the travels into the placements, and tag each guide with its level."""
    for r in res:
        unit = pl["units"][r["key"]]
        mo = unit.setdefault("motion", {})
        mo["runners"] = {"slide": r["slide"], "guide": r["guide"]}
        opens = [mo.get("open", [])] + [d["open"] for lay in (unit.get("layouts") or {}).values() for d in lay["drawers"]]
        for st in (st for o in opens for st in o):
            if st["joints"] == ["drawer"]:
                st["s"] = 1.0
        # an L² or XL² holds two drawers side by side: each guide is its side's (nearest key, left one first)
        keys = sorted(j["turn"]["origin"][0] for jid, j in mo.get("joints", {}).items() if jid.startswith("key_") and "turn" in j)
        for p in unit["parts"]:
            if re.search(r"Runner Guide", p[0]):
                m = np.array(p[3], float).reshape(3, 4)
                T = K.load_tris(p[0], download)
                P = T @ m[:, :3].T + m[:, 3]
                if len(p) < 5:
                    p.append({})
                p[4]["guide"] = level_of(P)
                if len(keys) == 2:
                    x = P[:, :, 0].mean()
                    p[4]["side"] = "left" if abs(x - keys[0]) < abs(x - keys[1]) else "right"


def measure(pl, download, key, quiet=False):
    unit = pl["units"][key]
    guide = placed(unit, r"Runner Guide", download)
    slide = placed(unit, r"Runner Slide", download)
    stop = placed(unit, r"Runner Stopper", download)
    zlo = min(P[:, :, 2].min() for _, P in guide)
    depth = -zlo
    res = {"key": key, "file": os.path.basename(guide[0][0][0]), "count": {"guide": len(guide), "slide": len(slide), "stopper": len(stop)}}
    per = []
    for s in (1, -1):
        G, S, St = side(guide, s), side(slide, s), side(stop, s)
        ys = np.arange(min(P[:, :, 1].min() for P in G + S) + 0.13, max(P[:, :, 1].max() for P in G + S), 0.5)
        sg, ss, sst = sections(G, ys), sections(S, ys), sections(St, ys)
        s1 = free_travel(ss, sg, depth)              # the slide in the guide
        s2 = free_travel(sg, sst, depth)             # the guide in the module, to the stopper
        s3 = free_travel(ss, sst, depth)             # the slide to the stopper (it shouldn't reach it)
        per.append({"side": "right" if s > 0 else "left", "slide_in_guide": [round(s1[0], 2), s1[1] and round(s1[1], 2), s1[2]],
                    "guide_to_stopper": [round(s2[0], 2), s2[1] and round(s2[1], 2), s2[2]],
                    "slide_to_stopper": [round(s3[0], 2), s3[1] and round(s3[1], 2), s3[2]]})
    res["sides"] = per
    res["slide"] = round(min(p["slide_in_guide"][0] for p in per), 2)
    res["guide"] = round(min(p["guide_to_stopper"][0] for p in per), 2)
    res["travel"] = round(res["slide"] + res["guide"], 2)
    res["depth"] = round(depth, 2)
    res["levels"] = sorted({level_of(P) for _, P in guide})
    if not quiet:
        print(json.dumps(res))
    return res


def _one(args):
    path, download, key = args
    return measure(json.load(open(path, encoding="utf-8")), download, key)


if __name__ == "__main__":
    a = sys.argv[1:]
    out = a[a.index("--json") + 1] if "--json" in a else None
    wr = "--write" in a
    jobs = int(a[a.index("--jobs") + 1]) if "--jobs" in a else 1
    a = [x for i, x in enumerate(a) if x not in ("--json", "--write", "--jobs", "--from") and x != out and (i == 0 or a[i - 1] not in ("--jobs", "--from"))]
    pl = json.load(open(a[0], encoding="utf-8"))
    keys = a[2:] or [f"drawer|{w}|{d}|1" for w in ("S", "XL") for d in range(3, 8)]
    if "--from" in sys.argv:
        res = json.load(open(sys.argv[sys.argv.index("--from") + 1], encoding="utf-8"))
        write(pl, a[1], res)
        with open(a[0], "w", encoding="utf-8", newline="\n") as f:
            json.dump(pl, f, ensure_ascii=False, separators=(",", ":"))
        sys.exit(0)
    if keys == ["all"]:
        keys = [k for k, u in pl["units"].items() if k.startswith("drawer|") and any("Runner Guide" in p[0] for p in u["parts"])]
    res = []
    from multiprocessing import Pool
    with Pool(jobs) as pool:
        for r in pool.imap(_one, [(a[0], a[1], k) for k in keys]):
            res.append(r)
            if out:
                json.dump(res, open(out, "w", encoding="utf-8"), indent=1)   # as it goes: a long run can be cut
    if wr:
        write(pl, a[1], res)
        with open(a[0], "w", encoding="utf-8", newline="\n") as f:
            json.dump(pl, f, ensure_ascii=False, separators=(",", ":"))
