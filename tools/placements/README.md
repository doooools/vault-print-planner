# Part placements for the 3D stack view

`src/stl-placements.json` says where every part of a unit goes, so the page can show a stack in 3D
from the user's own Vault files. It holds numbers only, no geometry, like `src/stl-measurements.tsv`.

## The data

```
units["drawer|L|7|2"] = { name, bbox, parts: [[path, role, group, m], ...] }
units["roof|L|7|grid"] = ...
stack = { first: 52, per_level: 48 }
```

- **key**: `drawer|<width>|<depth>|<height F>` or `roof|<width>|<depth>|<roof id>`, with the planner's ids (`R.ROOFS`).
- **path**: the file in the Vault download, as in `stl-measurements.tsv`. Parts used twice (runners, stoppers, caps…) appear once per copy.
- **role**: colour role (`body`, `roof`, `facade`, `drawer`, `mech`, `accent`, `insert`).
- **group**: `drawer` parts slide out with the drawer (along +Z). `module` parts stay put.
- **m**: a 3×4 row-major matrix that takes the file's own coordinates (as downloaded) to the unit frame. The unit frame uses three.js axes: +X right seen from the front, +Y up, +Z towards the viewer, in mm. Its origin is the middle of the module's front bottom edge.
- **stack**: a unit starts `first + per_level × (levels − 1)` mm above the bottom of the unit below it (52 / 100 / 196 for 1F / 2F / 4F). Roofs sit like a module.

Done so far: drawer S3 1F, drawers L7 1F/2F/4F, the five L7 roofs.

## How it is measured

The files are exported in print orientation (some at 45° to fit the bed) and scattered around one big CAD scene. Some parts are already in their assembled place relative to each other: the box, the baseplate, the stopper and the latch (X/Y). The rest is found by measurement in Blender:

| Script | What it does |
|---|---|
| `run_decimate.py` + `blender_decimate.py` | Decimated copy of the download (≤ 40k faces, same coordinates), with a geometric QA per part. If a part breaks, it is rebuilt with a voxel remesh (some files carry 100k+ zero-area triangles). |
| `blender_probe.py` + `depth_image.py` | Ray-cast depth maps: holes, grooves, counterbores and latch frames, with their centres. |
| `blender_fit.py` | Collision search of a part against parts already placed. Modes: best fit, `push` (slide until contact), `centroid` (middle of the free zone, with clusters), `scan` (contact curve). |
| `make_recipe_L.py` | Turns the rules measured on L7 into recipes (`recipes/*.json`) for every height and roof of an L size. |
| `blender_assemble.py` | Builds a unit from a recipe, renders check views (including sections) and saves a `.blend` with the root and drawer empties. |
| `blender_export_placements.py` | `.blend` files → `src/stl-placements.json`. |
| `blender_check_placements.py` | Rebuilds a stack from the JSON alone, as the page will, and renders it. |
| `blender_tower.py`, `blender_showcase.py`, `blender_render.py`, `blender_check_views.py` | Towers, side-by-side scenes, Cycles renders, section views. |

## Running it

Blender 5.x. The scripts read two environment variables:
- `VAULT_RENDER`: the decimated copy of the download;
- `BLENDER`: the Blender executable.

```bash
export VAULT_RENDER="/path/to/VAULT_RENDER"
python tools/placements/run_decimate.py "/path/to/261021_VAULT_USSA_S" "$VAULT_RENDER" --jobs 8
python tools/placements/make_recipe_L.py 7 tools/placements/recipes
for r in tools/placements/recipes/*_assembly.json; do
  blender -b --factory-startup --python tools/placements/blender_assemble.py -- "$r" "build/$(basename "$r" _assembly.json)" iso
done
blender -b --factory-startup --python tools/placements/blender_export_placements.py -- \
  src/stl-placements.json "$VAULT_RENDER/_decimate_log.jsonl" build/*.blend
blender -b --factory-startup --python tools/placements/blender_check_placements.py -- \
  src/stl-placements.json "/path/to/261021_VAULT_USSA_S" check.png "drawer|L|7|4" "drawer|L|7|2" "roof|L|7|grid"
```

Do not commit the decimated STLs, the `.blend` files or the renders: they are USSA's geometry.

## Rules measured on L7 (CAD frame: X across, +Y to the front, Z up)

- Every height is a stack of 48 mm levels. Level k is at z = 23.5 + 48k. Each level has its runner slides (box groove, 2.2 mm deep), runner guides (on the module wall, + 3.58 mm) and stoppers (module side hole, 128.56 mm behind the front).
- Module: Rx −90°, plus Ry −45° for the 1F, which is printed diagonally. Centred on the box, front at the box front + 0.06, bottom at z −3.6.
- Facade: Rx −90°. Its back is on the box front, its bottom at z 0, and its bolt holes line up with the box's.
- Key: Rx −90°, centre at facade back + 8.16. Key cap: Rx +90°, centre at facade back + 25.16. Both on the bottom level.
- Geared rails: at z 15.02 / 31.98 (the top one Ry 180°), 7.38 mm behind the box front.
- Two latches at x = centre ± 82.3. Facade caps go in every counterbore. The label goes in the slot (starts at centre + 115.19).
- There is only one baseplate file, sitting in the 1F box. It keeps the same offset in the 2F and 4F boxes.
- Roofs are printed on edge at 45° like the 1F module, and their underside is the same as a module's (same latch frames).
- S3 differs: one latch, two facade bolt holes, the stopper 44.85 mm behind the front.
