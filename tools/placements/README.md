# Part placements for the 3D stack view

`src/stl-placements.json` says where every part of a unit goes, so the page can show a stack in 3D
from the user's own Vault files. It holds numbers only, no geometry, like `src/stl-measurements.tsv`.

## The data

```
units["drawer|L|7|2"] = { name, bbox, parts: [[path, role, group, m], ...] }
units["roof|L|7|grid"] = ...
stack = { first: 52, per_level: 48 }
```

- **key**: the 3D view's own keys, with the planner's ids: `drawer|<w>|<d>|<h>` (w = S, M, L, L2, XL, XL2),
  `case|<w>|<d>|<h>` (w = S, M, L, XL), `roof|<w>|<d>|<roof id>` (`R.ROOFS`; `roof|L2|…` and `roof|XL2|…` are
  copies of the L and XL entries, marked `same_as`, since the planner gives a single L² or XL² unit the L or XL
  roof). A tower's base, wheels, feet and handles would be `stack|<w>|<d>` (none placed yet).
- One entry holds every variant of a unit: both lock options' files, every baseplate, the three L/XL case body
  styles. The page draws the placed files that the unit's part list names, so the variant in the list wins.
- **path**: the file in the Vault download, as in `stl-measurements.tsv` (with `²`; some unzip tools write
  `┬▓` for it, and the tools accept both). Parts used twice (runners, stoppers, caps…) appear once per copy.
- **role**: colour role (`body`, `roof`, `facade`, `drawer`, `mech`, `accent`, `insert`).
- **group**: `drawer` parts slide out with the drawer (along +Z). `module` parts stay put.
- **m**: a 3×4 row-major matrix that takes the file's own coordinates (as downloaded) to the unit frame. The unit frame uses three.js axes: +X right seen from the front, +Y up, +Z towards the viewer, in mm. Its origin is the middle of the module's front bottom edge.
- **stack**: a unit starts `first + per_level × (levels − 1)` mm above the bottom of the unit below it (52 / 100 / 196 for 1F / 2F / 4F). Roofs sit like a module.

  `stack.case.rise` gives the same for a case: body height + 15.6 (66.4 / 100.4 / 196.4).

Done: every drawer (S, M, L, L², XL, XL², all depths and heights), every roof, every case. Not yet: bases,
wheels, feet, handles, the mounts on the back of a unit and a few small or optional parts.
`COVERAGE.md` lists every unit the planner can build, its status and the files left out, with the reason.

## How it is measured

The files are exported in print orientation (some at 45° to fit the bed) and scattered around one big CAD scene. Some parts are already in their assembled place relative to each other: the box, the baseplate, the stopper and the latch (X/Y). The rest is found by measurement in Blender:

| Script | What it does |
|---|---|
| `run_decimate.py` + `blender_decimate.py` | Decimated copy of the download (≤ 40k faces, same coordinates), with a geometric QA per part. If a part breaks, it is rebuilt with a voxel remesh (some files carry 100k+ zero-area triangles). |
| `blender_probe.py` + `depth_image.py` | Ray-cast depth maps: holes, grooves, counterbores and latch frames, with their centres. |
| `blender_fit.py` | Collision search of a part against parts already placed. Modes: best fit, `push` (slide until contact), `centroid` (middle of the free zone, with clusters), `scan` (contact curve). |
| `stl_index.py` | Bounding box and triangle count of every downloaded file (`_stl_index.jsonl`, numpy, a few minutes). |
| `orient.py` + `vault_geom.py` | How a part is turned in the assembly: removes the print tilt (smallest box about one axis: 45° for S/M/L, 47.2° for XL parts and case lids), then tries the 24 quarter turns against a part already placed, comparing their corners (point-to-plane, same-facing normals). Keeps the six best. |
| `features.py` | Depth maps (numpy) of a posed part: a front's bolt holes, counterbores and key hole; a module's latch frames from below; its stopper holes from the side; which sides of a box are open. |
| `make_recipes.py` | Every recipe, from the index, the orientations and the features, by the rules below (`make_recipe_L.py`, from the first session, gives the same L recipes). |
| `run_assemble.py` | `blender_assemble.py` over many recipes, in parallel. |
| `coverage.js` + `coverage.py` | The planner's own unit list (`src/rules.js` run on the download's file list) against the JSON: `COVERAGE.md`. `unplaced_reasons.json` says why files are left out. |
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
export VAULT_ASSEMBLY="/path/to/VAULT_ASSEMBLY"   # index, orientations, features, recipes, .blend, renders
python -I tools/placements/stl_index.py "/path/to/261021_VAULT_USSA_S" "$VAULT_ASSEMBLY/_stl_index.jsonl"
python -I tools/placements/orient.py jobs.json "$VAULT_ASSEMBLY/_orient.json"   # jobs: target, reference, its matrix
python -I tools/placements/make_recipes.py "$VAULT_ASSEMBLY/recipes"              # S M L L2 XL XL2 CS CM CL CXL
python -I tools/placements/run_assemble.py "$VAULT_ASSEMBLY" "$VAULT_ASSEMBLY"/recipes/*_assembly.json --jobs 4
blender -b --factory-startup --python tools/placements/blender_export_placements.py -- \
  src/stl-placements.json "$VAULT_RENDER/_decimate_log.jsonl" $(ls "$VAULT_ASSEMBLY"/*/*.blend | grep -v /towers/)
# (the tower files are not units: given to the export, they stop it before it writes)
blender -b --factory-startup --python tools/placements/blender_check_placements.py -- \
  src/stl-placements.json "/path/to/261021_VAULT_USSA_S" check.png "drawer|L|7|4" "drawer|L|7|2" "roof|L|7|grid"
node tools/placements/coverage.js "$VAULT_ASSEMBLY/_stl_index.jsonl" "$VAULT_ASSEMBLY/_units.json"
python -I tools/placements/coverage.py "$VAULT_ASSEMBLY/_units.json" src/stl-placements.json "$VAULT_ASSEMBLY/_checks.json" "$VAULT_ASSEMBLY/recipes" tools/placements/COVERAGE.md
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

## Rules for every family (from `make_recipes.py`)

- **S, M, L drawers.** The boxes are in place in the CAD file (the S4-S6 boxes 1 mm higher than the others:
  everything is set relative to the box's own bbox, so it doesn't matter). The L7 rules above hold for every
  size, with:
  - the stopper hole (module side wall) 44.56 + 21 × (depth − 3) mm behind the module front, read on every module;
  - latch frames under the module, 53.5 mm long, back edge 12 mm from the module's back: S and M have one, in
    the middle; L has two, at ±82.3. A latch goes in each, its front 1.94 mm behind the frame's front;
  - facade: a cap in every counterbore but the one under the label, which sits at the facade's left end (seen
    from the front) over the left bolt: S1F 1 cap, S2F/S4F 3; M1F 3, M2F/M4F 5; L1F 3, L2F/L4F 5;
  - the three baseplate files of a size (plain, 1 or 2 handle cut-outs) share the plain one's place.
- **Roofs** (S, M, L, XL): turned so their latch frames are underneath, 12 mm from the back (on some roofs the
  frame's rim runs into the next relief, so only its back edge counts); otherwise placed like a module.
  Heavyweight (and cut) roofs: the handle is a bar across the middle slot, in the pockets of its walls (156 mm
  apart for a 156.5 mm bar, 45 mm above the roof's bottom: section of the L7 roof; manual p. 10). Grid roofs: the
  optional top handle lies on the grid, in the middle, long side across (manual p. 18); the page shows it when
  the unit's list has it (option `topHandle`). The handle's insert is not placed.
- **L²**: two S drawers. A section of the L3² module is two S modules side by side, with a double wall in the
  middle that has the same stopper holes, so each S drawer goes in its half (centre ±82.4) as in an S module.
  Two latches, like L.
- **XL²**: an S drawer on the viewer's left and an M drawer on the right, split by a double wall at
  x = −44.6 (unit frame): S centre at −127.0, M at +82.4. Two latches.
- **XL** (1F only): parts printed at 47.2°. The box is turned by its openings (open top, open back); up to XL5 a
  back panel closes it: a section shows a 6.3 mm notch at the back of each box wall, the panel's thickness, so
  the panel sits inside, flush with the box's back, its hooked ends in the notches. XL6/XL7 boxes come in a
  front half and a back half (open front): set from the front and from the full box depth, they overlap by
  6.1 mm on both sizes (144 + 131.9 for 269.8, 165 + 152.9 for 311.8): an interlocking joint. The dark band on
  an XL module's flank in iso views is the module's own side recess. XL runners, XL
  rails and the XL facade, otherwise as S/M/L. Two latches.
- **Cases** (sustainers), measured on S3 1F. The body has a drawer module's underside (same latch frame), so it
  sits and latches like a module; it is open at the top and at the front. The front panel is its front wall:
  4.8 mm lower than the body, its top level with the body's, so its bolt holes meet the body's (S 1F: body
  holes at 25.6 / 45.0 mm, panel holes 20.8 / 40.2 above the panel's bottom; same offset on every case). The
  lid is turned like a drawer roof (every case lid the same way: S3-XL5 lids score ≤ 0.17 against S3's, the
  one-piece S6/L7 lids 0.03), covers body and front panel (its front 10 mm proud of the body) and comes down
  6.9 mm over the body's rim (push fit). A unit stacked on a case starts body height + 15.6 mm above the case's
  bottom: a push fit of a drawer module onto the lid, less the 4.3 mm that the same fit overshoots on two drawer
  modules, whose locked step (52 mm) is known.
  Locks (manual p. 17), one per notch in the front panel's top edge: one in the middle on S and M, two at ±82.4
  on L and ±127.05 on XL (the planner counts 2 for every case). Each is a toggle latch, set closed:
  - the holder (the "UP" plate) lies across behind the panel, bolted into the 4 blind holes beside the notch
    (61.4 × 9 mm apart, their centre 11.7 mm under the top on 1F, 17.7 mm on 2-4F); its lug goes forward
    through the notch; "UP" reads upright from inside, as in the manual;
  - the link (LOCK INNER PART, holes 15 mm apart) hangs from the lug's pin, inside the lever's back pocket;
  - the lever (LOCK OUTER PART; the 2-4F one is 6 mm longer, matching the holes 6 mm lower) is pinned to the
    link's lower hole and lies in the panel's seat recess; its hook comes over the lid's front edge, its top at
    body top + 15.0 mm on every height.
  In the CAD file holder and lever sit at the same depth and across position but the lever is turned end for end
  (hook down): the side sections show the closed lever clearing the recess floor and the hook in the lid's
  groove. The two pins (one file) are not placed.
  Case label: on 1F panels in a closed recess 10 mm under the top; on 2F/4F in a slot open on the panel's left
  edge, 43.6 mm under the top, pushed to its end. Hinges are not placed: each hinge file holds both leaves
  printed side by side with their knuckles apart, so one matrix can't put them on their common pin; their
  notches in the body's back wall are at x = ±51.8 (S), ±69.3 (M), ±86.8 (L), ±131.4 (XL), 7 mm deep.
- **Checks against USSA's renders**: `compare_board.py` puts a crop of a PDF page next to our render, for a phone
  (boards in `VAULT_ASSEMBLY/_compare/`, outside the repo: they hold USSA's renders).
- **Checks**: every unit is assembled with front, iso, side-section, top-section (runner level) and bottom
  views; one tower per family is rebuilt from the JSON and the original files (`blender_check_placements.py`,
  which also writes a side section and a `.blend`): S5, M3, L4, L²+L, XL+XL², XL², and S cases with an S drawer.
  The regenerated S3 1F and L7 entries match the first session's checked ones (within 0.3 mm).

## Findings for the page (src/rules.js, src/template.html)

- On this machine the unzip turned `²` into `┬▓` (`04. L┬▓ Families/L3┬▓/...`). `R.norm` doesn't map it, so the
  planner can't find the L² and XL² files there. Mapping `┬▓` to `²` in `R.norm` would fix it.
- Cases: the measured rise (66.4 / 100.4 / 196.4) is 0.9 mm above `R.exterior` (65.5 / 99.5 / 195.5); it is in
  `stack.case.rise`, which `build.py` does not embed yet.
- A case body latches like a module (it has the latch frame), but the planner lists no latch for a case. The JSON
  places one; the page won't draw it until the list has `Latch.stl`.
- Latches per unit: S and M 1; L, L², XL and XL² 2 (the planner lists 1 per drawer insert).
- Case locks: the planner counts 2 per case; S and M fronts have one lock seat, L and XL two.
- Case hinges can't be drawn from the files as they are (both leaves in one file, printed apart).
- The JSON's roles are the first session's (body, drawer, facade, mech, accent, insert, roof); the page takes each
  part's role from the planner's list instead.
- Decimation: 8 of the 733 files stayed above the 0.15 mm QA after the voxel fallback (M5 Module 2F/4F, S6 1F/2F
  case bodies, L3 1F/2F/4F Dividers case bodies, XL3 Grid Roof; worst 1.2 mm). That only touches the renders and
  the bbox alignment by a fraction of a millimetre; the page reads the original files.
