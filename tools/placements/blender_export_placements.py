"""Export where every part goes, from assembled .blend files, for the planner's 3D view.

  blender -b --factory-startup --python blender_export_placements.py -- <out.json> <decimate_log.jsonl> <a.blend> [<b.blend> ...]

Each .blend is one unit built by blender_assemble.py (with "finalize"): a root empty
at the module's front-bottom-centre and the parts under it. For every part we write
the 3x4 matrix that takes the part's coordinates *as they are in the Vault STL
download* to the unit frame, in three.js axes:
    +X right (seen from the front), +Y up, +Z towards the viewer, mm,
    origin at the middle of the module's front bottom edge.
No geometry is written: the page applies the matrices to the user's own files.

The assembled meshes were recentred on their bounding-box centre c (taken from the
decimated file, whose coordinates are the download's), so
    M = C @ inverse(root) @ object @ translate(-c)
with C the CAD -> three.js axis change (x_cad across, y_cad to the front, z_cad up;
seen from the front the viewer's right is -x_cad).
"""
import bpy, sys, json, os, mathutils

argv = sys.argv[sys.argv.index("--") + 1:]
out, log_path, blends = argv[0], argv[1], argv[2:]

centre = {}
for line in open(log_path, encoding="utf-8"):
    r = json.loads(line)
    if r.get("ok"):
        centre[r["file"]] = mathutils.Vector([(a + b) / 2 for a, b in zip(r["bbox_min"], r["bbox_max"])])

C = mathutils.Matrix(((-1, 0, 0, 0), (0, 0, 1, 0), (0, 1, 0, 0), (0, 0, 0, 1)))
ROOF_IDS = {"Bowl": "bowl", "Grid": "grid", "Heavyweight": "heavy", "Table": "table", "UnderTable": "undertable"}


def canonical(path):
    """The planner's spelling of a path. Some unzip tools decode the '²' of 'L²'/'XL²' as cp437
    ('┬▓'); the page and stl-measurements.tsv use '²'."""
    return path.replace("┬▓", "²")


def unit_key(name):
    # S3_1F -> drawer|S|3|1 ; L7_Roof_Grid -> roof|L|7|grid
    fam_d, rest = name.split("_", 1)
    fam, d = fam_d.rstrip("0123456789"), int(fam_d[len(fam_d.rstrip("0123456789")):])
    if rest.startswith("Roof_"):
        return f"roof|{fam}|{d}|{ROOF_IDS[rest[5:]]}"
    return f"drawer|{fam}|{d}|{int(rest.rstrip('F'))}"


data = json.load(open(out, encoding="utf-8")) if os.path.exists(out) else {}
units = data.get("units", {})
for path in blends:
    bpy.ops.wm.open_mainfile(filepath=path)
    name = os.path.splitext(os.path.basename(path))[0]
    root = next(o for o in bpy.data.objects if o.type == "EMPTY" and o.parent is None)
    inv = root.matrix_world.inverted()
    parts, lo, hi = [], [1e9] * 3, [-1e9] * 3
    for o in sorted((o for o in bpy.data.objects if o.type == "MESH" and "vault_file" in o), key=lambda o: o.name):
        f = o["vault_file"]
        M = C @ inv @ o.matrix_world @ mathutils.Matrix.Translation(-centre[f])
        rows = [[round(M[i][j], 6) for j in range(3)] + [round(M[i][3], 3)] for i in range(3)]
        entry = [canonical(f), o["vault_role"], o["vault_group"], [v for r in rows for v in r]]
        if "vault_piece" in o:   # one connected piece of a file that holds several (blender_pieces.py)
            entry.append({"piece": [round(v, 3) for v in o["vault_piece"]]})
        parts.append(entry)
        # unit bounds from the real vertices
        mw = C @ inv @ o.matrix_world
        vs = o.data.vertices
        for i in range(0, len(vs), 50 if len(vs) > 2000 else 1):
            p = mw @ vs[i].co
            lo = [min(a, b) for a, b in zip(lo, p)]
            hi = [max(a, b) for a, b in zip(hi, p)]
    key = root.get("vault_key") or unit_key(name)
    units[key] = {"name": name, "bbox": [[round(x, 1) for x in lo], [round(x, 1) for x in hi]], "parts": parts}
    if root.get("vault_hinge"):
        units[key]["hinge"] = json.loads(root["vault_hinge"])
    print("EXPORTED", key, len(parts), "parts")

# A single L² or XL² unit on top of a stack gets the L or XL roof (rules.js), keyed by its own width
for k in list(units):
    fam = k.split("|")[1] if k.startswith("roof|") else None
    if fam in ("L", "XL"):
        alias = k.replace(f"roof|{fam}|", f"roof|{fam}2|", 1)
        units[alias] = {**units[k], "same_as": k}

data.update({
    "about": "Where each Vault part goes, per unit, measured from the STL files (tools/placements). "
             "Each part: [path in the Vault download, colour role, group, 3x4 row-major matrix]. "
             "The matrix maps the file's own coordinates to the unit frame: three.js axes, +X right seen from the front, "
             "+Y up, +Z towards the viewer, mm, origin at the middle of the module's front bottom edge. "
             "group 'drawer' parts slide out along +Z when the drawer opens; group 'lid' parts (a case's lid and "
             "hinge tops) turn about the unit's 'hinge' axis (origin, axis, right-handed, 0 to open_deg degrees). "
             "A 5th element {\"piece\": [x, y, z]} means: only the connected piece of the file (vertices welded) "
             "whose bounding-box centre is nearest to that point, in the file's own coordinates.",
    "stack": {"note": "a module's underside rests on the top face of the one below: the next unit starts "
                      "first + per_level * (levels - 1) above the bottom of the one below (measured on L7)",
              "first": 52.0, "per_level": 48.0,
              "case": {"note": "a case (sustainer) is its body plus a lid that comes down 6.9 mm over it; the next unit "
                               "starts body height + 15.6 above the case's bottom (push fits on S3 1F, corrected by the same "
                               "fit run on two drawer modules). R.exterior says 65.5 / 99.5 / 195.5.",
                       "rise": {"1": 66.4, "2": 100.4, "4": 196.4}}},
    "units": dict(sorted(units.items())),
})
json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("WROTE", out, len(units), "units")
