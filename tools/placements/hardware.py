"""Bolts in the 3D view: where each bolt of a unit goes, measured on the assembled unit (numpy, no Blender).

  python -I hardware.py <stl-placements.json> <report.json> [unit key regex]

Reads the placements, rebuilds every unit from the decimated copy ($VAULT_RENDER, same coordinates as the
download), finds the holes that take a bolt and writes, per unit, `hardware`: [[spec, group, m, {part, why}], ...]
back into the placements (other keys untouched). Run it again after any change to the parts (it reads the parts'
final matrices). The report lists every bolt with its seat, the hole it goes into and how much room is left at the
tip, plus the units where a rule found nothing; coverage.py turns it into COVERAGE.md's hardware table.

The bolts themselves are not in the Vault download: the page draws them from their standard sizes
(`hardware_sizes`, written here too), so nothing of USSA's geometry is involved.

Bolt frame (the matrix m maps it to the unit frame): +Y along the bolt from its tip to its head, origin on the axis
at the plane the head bears on (the underside of a button or socket head; the top face of a countersunk head, which
sits flush). The shank runs from y = 0 down to y = -length (ISO lengths: under the head, or overall for countersunk).

Rules (manual p. 3 "Hardware List", p. 17 "Required Hardware - Sustainers", p. 18 "- Drawers"; Drawer Assembly 6/8):
  - drawer front to box: M4 x 14 button head, from the front through each bolt hole of the facade's counterbores
    into the box's front wall (the facade cap closes the counterbore over it);
  - case front panel to body: M4 x 20 button head, from the front through the panel into the body's side walls
    (and floor rib on L and XL);
  - case hinge leaves: M4 x 10, from inside the case through each leaf into the back wall;
  - case hinge tops: M4 x 14, from under the lid's back through each top into the lid (they turn with the lid);
  - case lock holders: M4 x 14, from inside through the holder into the front panel's blind holes;
  - grid roof top handle: M6 x 50 countersunk, from under the roof up through its 45 deg holes into the handle.
"""
import json, os, re, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vault_geom as vg  # noqa: E402
import hw_geom as hg  # noqa: E402

# Standard sizes (mm). button: ISO 7380-1, countersunk: ISO 10642, socket: ISO 4762, hex: ISO 4017 head,
# nut: ISO 4032. d: thread, dk: head diameter (hex: across flats), k: head height, s: hex key, t: key depth.
SIZES = {
    "button": {"M3": {"d": 3, "dk": 5.7, "k": 1.65, "s": 2, "t": 1.04}, "M4": {"d": 4, "dk": 7.6, "k": 2.2, "s": 2.5, "t": 1.3},
               "M5": {"d": 5, "dk": 9.5, "k": 2.75, "s": 3, "t": 1.56}, "M6": {"d": 6, "dk": 10.5, "k": 3.3, "s": 4, "t": 2.08},
               "M8": {"d": 8, "dk": 14, "k": 4.4, "s": 5, "t": 2.6}},
    "countersunk": {"M3": {"d": 3, "dk": 6.72, "k": 1.86, "s": 2, "t": 1.1}, "M4": {"d": 4, "dk": 8.96, "k": 2.48, "s": 2.5, "t": 1.5},
                    "M5": {"d": 5, "dk": 11.2, "k": 3.1, "s": 3, "t": 1.9}, "M6": {"d": 6, "dk": 13.44, "k": 3.72, "s": 4, "t": 2.2},
                    "M8": {"d": 8, "dk": 17.92, "k": 4.96, "s": 5, "t": 3.0}},
    "socket": {"M3": {"d": 3, "dk": 5.5, "k": 3, "s": 2.5, "t": 1.3}, "M4": {"d": 4, "dk": 7, "k": 4, "s": 3, "t": 2},
               "M5": {"d": 5, "dk": 8.5, "k": 5, "s": 4, "t": 2.5}, "M6": {"d": 6, "dk": 10, "k": 6, "s": 5, "t": 3},
               "M8": {"d": 8, "dk": 13, "k": 8, "s": 6, "t": 4}},
    "hex": {"M4": {"d": 4, "dk": 7, "k": 2.8}, "M5": {"d": 5, "dk": 8, "k": 3.5}, "M6": {"d": 6, "dk": 10, "k": 4},
            "M8": {"d": 8, "dk": 13, "k": 5.3}},
    "nut": {"M3": {"d": 3, "dk": 5.5, "k": 2.4}, "M4": {"d": 4, "dk": 7, "k": 3.2}, "M5": {"d": 5, "dk": 8, "k": 4.7},
            "M6": {"d": 6, "dk": 10, "k": 5.2}, "M8": {"d": 8, "dk": 13, "k": 6.8}},
}
SIZES_NOTE = ("Standard sizes the page draws hardware from (mm): button ISO 7380-1, countersunk ISO 10642, socket ISO 4762, "
              "hex ISO 4017 (dk across flats), nut ISO 4032. A spec reads '<thread>x<length> <kind>', e.g. 'M4x14 button'; "
              "threads are not drawn. Bolt frame: +Y from tip to head, origin on the axis where the head bears (top face of a "
              "countersunk head), shank from y = 0 to y = -length.")


def spec_of(spec):
    m = re.match(r"(M\d+)x(\d+(?:\.\d+)?) (\w+)$", spec)
    th, L, kind = m.group(1), float(m.group(2)), m.group(3)
    return {"thread": th, "L": L, "kind": kind, **SIZES[kind][th]}


# Which part a rule's bolts bear on, from which side (unit axis the head faces), and the bolt.
FACADE = r"/Facades/|/[^/]*Facade(?! Cap)[^/]*\.stl$"   # (the XL fronts are not in a Facades folder)
RULES = [
    {"id": "front", "units": r"^drawer\|", "part": FACADE, "face": "+z", "spec": "M4x14 button",
     "why": "drawer front to box", "hole": (3.6, 5.2)},
    {"id": "case_front", "units": r"^case\|", "part": FACADE, "face": "+z", "spec": "M4x20 button",
     "why": "case front to body", "hole": (3.6, 5.2)},
    {"id": "hinge", "units": r"^case\|", "part": r"/Hinges/[^/]* Hinge\.stl$", "face": "+z", "spec": "M4x10 button",
     "why": "hinge leaf to body", "hole": (3.6, 5.2)},
    {"id": "hinge_top", "units": r"^case\|", "part": r"Hinge Top\.stl$", "face": "-y", "spec": "M4x14 button",
     "why": "hinge top to lid", "hole": (3.6, 5.2)},
    {"id": "lock", "units": r"^case\|", "part": r"/LOCK HOLDER\.stl$", "face": "-z", "spec": "M4x14 button",
     "why": "lock holder to front", "hole": (3.3, 5.2)},
]
HANDLE_SPEC = "M6x50 countersunk"

AXES = {"+x": (0, 1), "-x": (0, -1), "+y": (1, 1), "-y": (1, -1), "+z": (2, 1), "-z": (2, -1)}

# Parts the units hold in several variants: the bolts are measured on the variant that has the holes. Units whose
# part list draws another variant (a hidden key, another baseplate, another case body style) take the same bolts:
# the variants share their bolt holes (the case body styles were checked to give the same bolts).
SKIP = r"Baseplate_With|Hidden Key|Dividers Module|Sealed Module|Gridfinity|Divider"

_HOLES = {}


def local_holes(part, axis, sign, rng):
    """Through holes of a part's file (or piece) seen along a unit axis, cached in the file's own coordinates: the
    same file is placed the same way round in many units."""
    f_u = np.zeros(3)
    f_u[axis] = sign
    f_l = part.R.T @ f_u
    k = int(np.argmax(np.abs(f_l)))
    if abs(abs(f_l[k]) - 1) > 1e-3:
        raise ValueError(f"{part.name}: not turned square to {f_u}")
    key = (part.path, tuple(part.piece) if part.piece else None, k, int(np.sign(f_l[k])), rng)
    if key not in _HOLES:
        src = hg.piece_tris(part.path, part.piece) if part.piece else hg.file_tris(part.path)
        loc = hg.Part.__new__(hg.Part)
        loc.tris = src
        P = src.reshape(-1, 3)
        loc.lo, loc.hi = P.min(0), P.max(0)
        a = np.pi * (np.array(rng) / 2) ** 2
        _HOLES[key] = [h for h in hg.holes_in(loc, k, int(np.sign(f_l[k])), area=(a[0], a[1]))]
    return [{"c": part.R @ h["c"] + part.t, "d": h["d"]} for h in _HOLES[key]]


def near_tris(parts, o, d, r):
    """Each part's triangles that come within r of the line o + s d (by their bounding spheres)."""
    out = []
    for p in parts:
        cen = p.tris.mean(1)
        rad = np.linalg.norm(p.tris - cen[:, None], axis=2).max(1)
        v = cen - o
        dist = np.linalg.norm(v - (v @ d)[:, None] * d, axis=1)
        sel = p.tris[dist < r + rad]
        if len(sel):
            q = hg.Part.__new__(hg.Part)
            q.i, q.path, q.tris, q.group, q.piece = p.i, p.path, sel, p.group, p.piece
            P = sel.reshape(-1, 3)
            q.lo, q.hi = P.min(0), P.max(0)
            out.append(q)
    return out


def axis_fit(parts, o, d, r_guess=2.0, stations=(4.0, 10.0)):
    """Refine a hole's axis: at two depths along d, find the middle of the gap across it in two directions."""
    u, v = hg.ortho(d)
    pts = []
    for st in stations:
        p0 = o + d * st
        c = p0.copy()
        for n in (u, v):
            q = c - n * 12
            hs = sorted((s - 12, f) for p in parts for s, f in hg.ray_hits(p.tris, q, n) if abs(s - 12) < 9)
            gaps = [(a[0], b[0]) for a, b in zip(hs, hs[1:]) if a[1] > 0 and b[1] < 0 and a[0] < 0.6 and b[0] > -0.6]
            if not gaps:
                return None
            g = min(gaps, key=lambda g: abs(g[0] + g[1]))
            c = c + n * (g[0] + g[1]) / 2
        pts.append(c)
    a = pts[1] - pts[0]
    return pts[0], a / np.linalg.norm(a)


def measure(parts, head, o, d, sp):
    """A bolt bearing on `head` along d from outside point o (on the axis, in front of the head part): the seat, the
    receiving part and the room at the tip. Returns a dict, or None when nothing would hold the bolt."""
    r_shank, r_head = sp["d"] / 2, sp["dk"] / 2
    nb = near_tris(parts, o, d, r_head + 1)
    hp = [p for p in nb if p.i == head.i]
    others = [p for p in nb if p.i != head.i]
    if not hp:
        return None
    # seat: the highest point of the head part under the head (rays parallel to the axis between the hole and the
    # head's rim)
    seats = []
    for r in np.linspace(r_shank + 0.45, r_head - 0.15, 4):
        for vals in hg.ring(hp, o, d, r, n=16).values():
            seats += vals
    if not seats:
        return None
    s_seat = min(seats)
    # what the shank goes into: the first part (other than the head part) met by rays just outside the shank
    recv = {}
    for i, vals in hg.ring(others, o, d, r_shank + 0.3, n=12, s_min=s_seat - 0.5).items():
        recv[i] = min(vals)
    if not recv:
        return None
    ri = min(recv, key=recv.get)
    s_recv = recv[ri]
    # the pilot hole's bottom: the first material on the axis (in any part) past the receiving face
    axis_hits = [s for p in others for s, f in hg.ray_hits(p.tris, o, d) if f < 0 and s > s_recv - 0.5]
    s_end = min(axis_hits) if axis_hits else None
    tip = s_seat + sp["L"]
    return {"s_seat": s_seat, "s_recv": s_recv, "recv": ri, "s_end": s_end, "tip": tip,
            "grip": round(s_recv - s_seat, 2), "engage": round(tip - s_recv, 2),
            "room": None if s_end is None else round(s_end - tip, 2)}


def frame(p, y):
    """3x4 row-major matrix of a bolt frame: origin p, +Y = y."""
    y = y / np.linalg.norm(y)
    x = hg.ortho(y)[0]          # any right-handed basis around y (the head is round; its key hole turns with x)
    z = np.cross(x, y)
    M = np.column_stack([x, y, z, p])
    return [round(float(v), 6) if k % 4 < 3 else round(float(v), 3) for k, v in enumerate(M.reshape(-1))]


def unit_bolts(key, entry, report):
    parts = hg.load_unit(entry, only=lambda p: not re.search(SKIP, p))
    out = []
    for rule in RULES:
        if not re.search(rule["units"], key):
            continue
        sp = spec_of(rule["spec"])
        axis, sign = AXES[rule["face"]]
        f = np.zeros(3)
        f[axis] = sign
        d = -f
        heads = [p for p in parts if re.search(rule["part"], p.path)]
        n_rule = 0
        for head in heads:
            for h in local_holes(head, axis, sign, rule["hole"]):
                o = h["c"] + f * 25
                m = measure(parts, head, o, d, sp)
                if not m:
                    continue
                p = o + d * m["s_seat"]
                out.append([rule["spec"], head.group, frame(p, -d), {"part": head.i, "why": rule["why"]}])
                n_rule += 1
                report["bolts"].append({"unit": key, "rule": rule["id"], "spec": rule["spec"], "part": head.name,
                                        "at": [round(float(v), 2) for v in p], "hole_d": h["d"],
                                        "into": parts[[q.i for q in parts].index(m["recv"])].name,
                                        **{k: m[k] for k in ("grip", "engage", "room")}})
        report["counts"].setdefault(key, {})[rule["id"]] = n_rule
    if re.search(r"^roof\|.*\|grid$", key):
        out += handle_bolts(key, parts, report)
    return out


def layout_bolts(key, entry, lid, lay, report):
    """The bolts of a layout's drawers (README "Layouts"): measured on the unit's module parts with the layout's
    drawers in it. `part` is the index in the layout's own `parts`, and drawer (and side) are the part's."""
    base = [p for p in entry["parts"] if p[2] != "drawer"]
    hw = unit_bolts(f"{key}#{lid}", {"parts": base + lay["parts"]}, report)
    out = []
    for spec, group, m, x in hw:
        i = x["part"] - len(base)
        if i < 0:
            continue
        tag = lay["parts"][i][4] if len(lay["parts"][i]) > 4 else {}
        out.append([spec, group, m, {"part": i, **{k: tag[k] for k in ("drawer", "side") if k in tag}, "why": x["why"]}])
    return out


def handle_bolts(key, parts, report):
    """The top handle's two M6 x 50 countersunk bolts: up from under the roof through its 45 deg holes."""
    roof = next((p for p in parts if re.search(r"Grid Roof\.stl$", p.path)), None)
    handle = next((p for p in parts if re.search(r"Top Handle", p.path)), None)
    report["counts"].setdefault(key, {})["top_handle"] = 0
    if not roof or not handle:
        return []
    sp = spec_of(HANDLE_SPEC)
    hz = (handle.lo[2] + handle.hi[2]) / 2
    # the roof's holes, found where they go through the grid (x + y = -+13.86 on L7, the same on every grid roof)
    zs = [z for z in np.arange(hz - 4, hz + 4, 0.25)]
    out = []
    for side in (-1, 1):
        d = np.array([side, 1.0, 0.0]) / np.sqrt(2)          # up and out, towards the handle's end
        best = None
        for z in zs:
            o = np.array([side * 22.43, 8.57, z]) - d * 6
            fit = axis_fit([roof], o, d, stations=(3.0, 8.0))
            if fit:
                c, a = fit
                if best is None or abs(c[2] - z) < abs(best[0][2] - best[2]):
                    best = (c, a, z)
        if best is None:
            continue
        c, a, _ = best
        # the holes are drawn at 45 deg in the x-y plane: keep that direction (a fit over a few mm of a decimated hole
        # tilts it by a degree) and the measured middle of the hole
        a = d
        # where the countersunk head sits: the hole's mouth is a countersink (about 45 deg, read from r = 3.5 to 6 mm)
        # opening on the slope under the grid, so its rim is not square to the bolt; the head's cone goes in it,
        # its top face where the countersink's cone (fitted, then carried on) is as wide as the head
        o = c - a * 40
        nb = near_tris([roof], o, a, sp["dk"] / 2 + 2)
        rs, ss = [], []
        for r in np.arange(sp["d"] / 2 + 0.5, sp["dk"] / 2 - 0.6, 0.25):
            vals = [v for vs in hg.ring(nb, o, a, r, n=16).values() for v in vs]
            if len(vals) >= 12:
                rs.append(r)
                ss.append(float(np.median(vals)))
        if len(rs) < 4:
            continue
        k, b0 = np.polyfit(rs, ss, 1)
        s_top = float(k * sp["dk"] / 2 + b0)
        p = o + a * s_top
        tip = s_top + sp["L"]
        hh = near_tris([handle], o, a, 4)
        ax_h = sorted(s for q in hh for s, f in hg.ray_hits(q.tris, o, a) if f < 0 and s > s_top + 5)
        room = round(ax_h[0] - tip, 2) if ax_h else None
        # how far the handle's channel axis is from the roof's hole axis
        fit_h = axis_fit([handle], o + a * (s_top + 30), a, stations=(0.0, 6.0))
        off = None
        if fit_h:
            q = fit_h[0] - c
            off = round(float(np.linalg.norm(q - (q @ a) * a)), 2)
        out.append([HANDLE_SPEC, handle.group, frame(p, -a), {"part": handle.i, "why": "top handle to grid roof"}])
        report["counts"][key]["top_handle"] += 1
        report["bolts"].append({"unit": key, "rule": "top_handle", "spec": HANDLE_SPEC, "part": roof.name,
                                "at": [round(float(v), 2) for v in p], "axis": [round(float(v), 4) for v in a],
                                "into": handle.name, "room": room, "channel_offset": off})
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    path, rep_path = sys.argv[1], sys.argv[2]
    only = re.compile(sys.argv[3]) if len(sys.argv) > 3 else None
    data = json.load(open(path, encoding="utf-8"))
    report = json.load(open(rep_path, encoding="utf-8")) if only and os.path.exists(rep_path) else {"bolts": [], "counts": {}}
    if only:
        report["bolts"] = [b for b in report["bolts"] if not only.search(b["unit"])]
    done = {}
    for key, entry in data["units"].items():
        if only and not only.search(key):
            continue
        if entry.get("same_as"):
            continue
        hw = unit_bolts(key, entry, report)
        if hw:
            entry["hardware"] = hw
        else:
            entry.pop("hardware", None)
        done[key] = hw
        print(key, len(hw), report["counts"].get(key), flush=True)
        for lid, lay in (entry.get("layouts") or {}).items():
            lhw = layout_bolts(key, entry, lid, lay, report)
            lay["hardware"] = lhw
            done[f"{key}#{lid}"] = lhw
            print(f"{key}#{lid}", len(lhw), report["counts"].get(f"{key}#{lid}"), flush=True)
    for key, entry in data["units"].items():       # L2 / XL2 roofs: copies of the L / XL entries
        if entry.get("same_as") and entry["same_as"] in data["units"]:
            src = data["units"][entry["same_as"]]
            if "hardware" in src:
                entry["hardware"] = src["hardware"]
            else:
                entry.pop("hardware", None)
    data["hardware_sizes"] = {"note": SIZES_NOTE, **SIZES}
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    json.dump(report, open(rep_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("WROTE", path, sum(len(v) for v in done.values()), "bolts in", len(done), "units")
