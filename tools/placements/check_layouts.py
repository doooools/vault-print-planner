"""Check the layouts (several drawers in one 2F/4F module) as the page would draw them: kinematics.py's motion
check, one drawer at a time, the others shut and locked in their places.

  python -I check_layouts.py <stl-placements.json> <vault download> <out.json> [unit key regex] [--steps 21] [--hidden]
                            [--layouts "1,1,1,1;2,1,1"]

For each layout of each matching unit and each of its drawers: the unit's module parts (shell, guides, stoppers,
latches) plus every drawer of the layout, the drawer under test with its own key, racks and slide (its `open`
steps), the others as fixed parts. kinematics.check cuts them across the motion (planes z = const through the
keys and racks, and y = const through the drawer under test's key) and reports every pair that overlaps, with the
overlap when closed. So a drawer that meets its neighbour, a rack that misses its level's pocket or a box that
rubs the one above shows up as a pair with a drawer of another index or with the shell.
"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kinematics as K  # noqa: E402


def drawer_unit(entry, lay, d):
    """A unit entry with the layout's drawer d (index, side) moving and the other drawers fixed."""
    def mine(p):
        x = p[4] if len(p) > 4 else {}
        return x.get("drawer") == d["drawer"] and x.get("side") == d.get("side")
    parts = []
    for p in entry["parts"]:
        if p[2] == "drawer":
            continue
        x = p[4] if len(p) > 4 else {}
        if "guide" in x and not (d["level"] <= x["guide"] < d["level"] + d["h"] and (not d.get("side") or x.get("side") == d["side"])):
            p = p[:4] + [{k: v for k, v in x.items() if k not in ("guide", "side")}]   # another drawer's guides stay
        parts.append(p)
    for p in lay["parts"]:
        if mine(p):
            parts.append(p)
        else:
            x = {k: v for k, v in (p[4] if len(p) > 4 else {}).items() if k != "joint"}
            parts.append([p[0], p[1], "module", p[3]] + ([x] if x else []))
    tag = [j for j in d["open"][0]["joints"]]
    joints = {j: lay["motion"]["joints"][j] for j in tag}
    runners = (entry.get("motion") or {}).get("runners")
    return {"bbox": entry["bbox"], "parts": parts, "motion": {"joints": joints, "open": d["open"], **({"runners": runners} if runners else {})}}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    steps = int(a[a.index("--steps") + 1]) if "--steps" in a else 21
    hidden = "--hidden" in a
    lays_only = a[a.index("--layouts") + 1].split(";") if "--layouts" in a else None
    pos = [v for i, v in enumerate(a) if not v.startswith("--") and not (i > 0 and a[i - 1] in ("--steps", "--layouts"))]
    pl = json.load(open(pos[0], encoding="utf-8"))
    only = re.compile(pos[3]) if len(pos) > 3 else None
    out = {}
    for key, entry in pl["units"].items():
        if only and not only.search(key):
            continue
        for lid, lay in (entry.get("layouts") or {}).items():
            if lays_only and lid not in lays_only:
                continue
            for d in lay["drawers"]:
                name = f"{key}#{lid}#{d['drawer']}{'/' + d['side'] if d.get('side') else ''}"
                fake = {"units": {name: drawer_unit(entry, lay, d)}}
                res = K.check(fake, pos[1], name, steps=steps, hidden=hidden, quiet=False)
                out[name] = res
    json.dump(out, open(pos[2], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    new = {k: [r for r in v if r["new"]] for k, v in out.items()}
    print("WROTE", pos[2], len(out), "drawers;", sum(1 for v in new.values() if v), "with something new on the way")
