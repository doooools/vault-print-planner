"""What a stack's outside size needs beyond the units' boxes, measured on the files (numpy, no Blender).

  python -I measure_envelope.py <stl-placements.json>

The page gives a stack's outside size (width x depth x height, drawers closed) as the box around everything on it:
each unit's `bbox` (already in the placements, every part of the unit as placed) where it stands in the stack, the
floor under the base, wheels, foot or casters, and the backbone column. Two of the bboxes hold a part that only some
builds have, and the column's pieces are placed by the page, so this writes:

- `envelope.front`: how far a drawer's front comes out (z) when it has no key lock. A unit's bbox reaches 30.9 mm,
  the key lock's key with its cap, standing 21 mm proud of the front; the hidden key is flush. Measured: the highest
  z of every drawer front (facade), facade cap, label and hidden key on disk.
- `envelope.grid_plate`: a grid roof's height without its carry handle (the bbox, 62.2 mm, holds the handle). The
  highest y of every grid roof file on disk, in its roof unit.
- `box` in every `column|<w>` piece's 5th element: its bounds [x0, y0, z0, x1, y1, z1] in the column frame (x = 0
  between the rods, y = 0 at its bottom, z = 0 on the modules' back), so the page moves them with the pieces
  (stackColumn) and the knobs, handles and pegboards count where they stand.

Every file it can't find is left out and said so; it checks that what it finds is the same on every unit measured.
Needs $VAULT_RENDER (the download or the decimated copy, same coordinates).
"""
import json, os, re, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hw_geom as hg  # noqa: E402

FRONTS = re.compile(r"(?i)/facades?/|facade cap\.stl$|/label\.stl$|hidden key \(turn on supports\)\.stl$|xl facade")


def parts_on_disk(unit):
    out, missing = [], set()
    for i, e in enumerate(unit["parts"]):
        if hg.on_disk(e[0]):
            out.append(hg.Part(i, e))
        else:
            missing.add(e[0])
    return out, missing


def main():
    path = sys.argv[1]
    pl = json.load(open(path, encoding="utf-8"))
    missing = set()

    # Drawer fronts without the key lock
    fronts = []
    for k, u in pl["units"].items():
        if not k.startswith("drawer|"):
            continue
        for e in u["parts"]:
            if FRONTS.search(e[0]) and hg.on_disk(e[0]):
                p = hg.Part(0, e)
                fronts.append((round(float(p.hi[2]), 2), k, p.name))
    fronts.sort()
    print("drawer fronts (no key lock): z max", fronts[0][:2], "...", fronts[-1][:2], f"({len(fronts)} parts)")

    # Grid roofs without their handle
    plates = []
    for k, u in pl["units"].items():
        if re.match(r"roof\|[^|]+\|\d\|grid$", k):
            for e in u["parts"]:
                if re.search(r"(?i)grid roof\.stl$", e[0]):
                    if hg.on_disk(e[0]):
                        plates.append((round(float(hg.Part(0, e).hi[1]), 2), k))
                    else:
                        missing.add(e[0])
    plates.sort()
    print("grid roof plates: y max", plates)

    # Column pieces
    for k, u in pl["units"].items():
        if not k.startswith("column|"):
            continue
        ps, miss = parts_on_disk(u)
        missing |= miss
        for p in ps:
            e = u["parts"][p.i]
            if len(e) < 5 or not isinstance(e[4], dict):
                e[4:] = [{}]
            e[4]["box"] = [round(float(v), 1) for v in [*p.lo, *p.hi]]
            print(f"  {k:10s} {e[4].get('as', ''):16s} {p.name:42s} {e[4]['box']}")

    front = max(f[0] for f in fronts)
    plate = max(p[0] for p in plates)
    if fronts[-1][0] - fronts[0][0] > 1.0 or plates[-1][0] - plates[0][0] > 0.5:
        print("WARNING: not the same on every unit measured")
    pl["envelope"] = {
        "note": "A stack's outside size (the page's stackSize): a drawer's front without a key lock comes out to z = front"
                " (the key lock's key and cap reach the units' bbox, 30.9 mm); a grid roof without its carry handle is"
                " grid_plate tall (the bbox holds the handle). tools/placements/measure_envelope.py",
        "front": round(front, 1), "grid_plate": round(plate, 1),
        "measured_on": {"fronts": len(fronts), "grid_roofs": [p[1] for p in plates]}}
    if missing:
        print("not on disk:", *sorted(missing), sep="\n  ")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pl, f, ensure_ascii=False, separators=(",", ":"))
    print("envelope", json.dumps(pl["envelope"]))


if __name__ == "__main__":
    main()
