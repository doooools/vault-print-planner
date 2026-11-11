# Part placements for the 3D stack view

`src/stl-placements.json` says where every part of a unit goes, so the page can show a stack in 3D
from the user's own Vault files. It holds numbers only, no geometry, like `src/stl-measurements.tsv`.

## The data

```
units["drawer|L|7|2"] = { name, bbox, parts: [[path, role, group, m], [path, role, group, m, {piece}], ...],
                          hardware: [[spec, group, m, {part, why}], ...] }
units["case|S|3|1"]  = { ..., hinge: { origin: [0, 50.8, -153.59], axis: [-1, 0, 0], open_deg: 105 } }
units["roof|L|7|grid"] = ...
stack = { first: 52, per_level: 48 }
hardware_sizes = { button: { M4: { d, dk, k, s, t }, ... }, countersunk: {...}, socket, hex, nut }
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
- **group**: `drawer` parts slide out with the drawer (along +Z). `module` parts stay put. `lid` parts (a case's
  lid and its hinge tops) turn about the unit's `hinge`.
- **piece** (optional 5th element, `{"piece": [x, y, z]}`): the part is only one connected piece of the file.
  Some files hold several parts printed side by side (a drawer's two racks, a case's two hinge leaves, two hinge
  tops, two rods); each copy is then its own entry with its own matrix. Split the file into connected pieces
  (vertices welded at 0.001 mm: an STL has no shared vertices, so weld first) and take the piece whose
  bounding-box centre is nearest to `[x, y, z]`, in the file's own coordinates (as downloaded; the decimated copy
  has the same pieces and centres, and the pieces are far apart, 6 mm or more, so the choice is never close).
  The matrix applies to the piece's own vertices as they are in the file. `vault_geom.pieces` (numpy) and
  `blender_pieces.py` (Blender) do it.
- **hinge** (cases only): the lid's axis in the unit frame, `origin` a point on it and `axis` its direction.
  The lid opens by turning the `lid` group about it by 0 (closed) to `open_deg` degrees, right-handed about
  `axis` (with `axis` −X a positive angle lifts the lid's front). The axis is the hinge knuckles' own: level
  with the body's top, 7.49 mm behind its back face. `open_deg` is 105, the manual's open view (p. 17).
  Swept in steps on the exported parts, nothing meets the body, the leaves or the rods before 180°.
- **m**: a 3×4 row-major matrix that takes the file's own coordinates (as downloaded) to the unit frame. The unit frame uses three.js axes: +X right seen from the front, +Y up, +Z towards the viewer, in mm. Its origin is the middle of the module's front bottom edge.
- **hardware** (written by `hardware.py`, after the export): the unit's bolts. `spec` reads `<thread>x<length> <kind>`,
  e.g. `"M4x14 button"`, `"M6x50 countersunk"` (kinds: `button` ISO 7380-1, `countersunk` ISO 10642, `socket` ISO 4762,
  `hex` ISO 4017; `nut` ISO 4032 and `rod` are understood too, none placed yet). `m` maps the bolt's own frame to the
  unit frame: +Y along the bolt from its tip to its head, origin on its axis where the head bears (the top face of a
  countersunk head, which sits flush), the shank from y = 0 to y = -length. `part` is the index in `parts` of the part
  whose hole the head bears on, and `group` is that part's: a bolt is drawn with its part (not at all when the unit's
  list doesn't name it) and moves with it (a drawer front's bolts slide out with the drawer, a hinge top's turn with
  the lid). An animation that moves one part on its own should move the bolts whose `part` is that part. `why` says
  what it holds (not embedded in the page).
- **hardware_sizes**: the standard sizes the page and `hw_shapes.py` make the bolts from (mm; d thread, dk head
  diameter or hex across flats, k head height, s hex key, t key depth). No bolt geometry is stored.
- **stack**: a unit starts `first + per_level × (levels − 1)` mm above the bottom of the unit below it (52 / 100 / 196 for 1F / 2F / 4F). Roofs sit like a module.

  `stack.case.rise` gives the same for a case: body height + 15.6 (66.4 / 100.4 / 196.4).

Done: every drawer (S, M, L, L², XL, XL², all depths and heights), every roof, every case, and their bolts
(drawer fronts, case fronts, hinges, hinge tops, lock holders, the grid roof's top handle). Not yet: bases,
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
| `hardware.py` + `hw_geom.py` | The bolts: on every assembled unit (rebuilt from the JSON and the decimated copy), the through holes of the part a bolt's head bears on, seen from its side (depth maps, cached per file); rays along each hole give the seat (highest point under the head), the part the shank goes into and the bottom of its hole. Writes `hardware` and `hardware_sizes` into the JSON and a report (seat, grip, engagement, room at the tip) for `coverage.py`. |
| `hw_shapes.py` | A bolt's shape from its standard sizes (plain Python, as the page makes it): for the Blender check. |
| `hw_check.py` | Sections through the bolts' axes (parts in colour, the bolt's outline in black) and a clash test of every head against the parts. |
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
# the bolts: after every export (the export rewrites a unit without its `hardware`)
python -I tools/placements/hardware.py src/stl-placements.json "$VAULT_ASSEMBLY/_hardware/hardware_report.json"
python -I tools/placements/hw_check.py src/stl-placements.json "$VAULT_ASSEMBLY/_hardware/check" "case|L|7|4" "drawer|S|3|1"
blender -b --factory-startup --python tools/placements/blender_check_placements.py -- \
  src/stl-placements.json "/path/to/261021_VAULT_USSA_S" check.png "drawer|L|7|4" "drawer|L|7|2" "roof|L|7|grid"
node tools/placements/coverage.js "$VAULT_ASSEMBLY/_stl_index.jsonl" "$VAULT_ASSEMBLY/_units.json"
python -I tools/placements/coverage.py "$VAULT_ASSEMBLY/_units.json" src/stl-placements.json "$VAULT_ASSEMBLY/_checks.json" "$VAULT_ASSEMBLY/recipes" tools/placements/COVERAGE.md "$VAULT_ASSEMBLY/_hardware/hardware_report.json"
```

Do not commit the decimated STLs, the `.blend` files or the renders: they are USSA's geometry.

## Rules measured on L7 (CAD frame: X across, +Y to the front, Z up)

- Every height is a stack of 48 mm levels. Level k is at z = 23.5 + 48k. Each level has its runner slides (box groove, 2.2 mm deep), runner guides (on the module wall, + 3.58 mm) and stoppers (module side hole, 128.56 mm behind the front).
- Module: Rx −90°, plus Ry −45° for the 1F, which is printed diagonally. Centred on the box, front at the box front + 0.06, bottom at z −3.6.
- Facade: Rx −90°. Its back is on the box front, its bottom at z 0, and its bolt holes line up with the box's.
- Key: Rx −90°, centre at facade back + 8.16. Key cap: Rx +90°, centre at facade back + 25.16. Both on the bottom level.
- Geared rails: see "Geared rails" below (the first session's rule, both racks of the file at z 15.02 / 31.98
  7.38 mm behind the box front, lying flat, was wrong: it put them through the box's front wall).
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
- **Geared rails** (every drawer, from sections of S3, S5 2F, M3, M6 4F, L3, L7 2F, XL3, XL5, XL7, L² and XL²
  boxes). Each `<w> Rails.stl` holds the drawer's two racks (two pieces). The box's front wall is hollow: two
  channels run inside it, 5.2 mm high and 4.4 mm deep, centred 3.1 mm behind the box's front face (3.2 on the XL
  box, whose face is 0.1 mm behind its bbox). The bottom channel is at y 10.2–15.4 (unit frame, box bottom at 8.6),
  from a closed end left of the key (x −65.87 on S and M, −66.77 on L and XL) to the box's right side. The top
  channel is at y 38.8–44.0, from a closed end right of the key (+66.21 on S, +66.57 on M, L, XL) to the left side,
  with a 1.5 mm groove along its top. The key's pinion is between the two. Each rack lies in its channel on edge,
  in the x-y plane, with its teeth towards the pinion: the plain rack at the bottom, with its teeth up; the rack with a
  1.4 mm fin on its back edge at the top, turned half a turn about z, teeth down, its fin in the groove. Both are
  retracted, rounded end against the channel's closed end (unlocked), so their teeth span the pinion and their
  tabs stay 6 to 12 mm inside the box's sides.
- **Hidden key** (lock option "Hidden key (flush)", every drawer): `Hidden Key` is the key lock without its knob,
  with the same gear, the same text and the same print pose. So it takes the key's place with the key's turn: its
  back (the gear) is where the key's back is, 8.55 mm behind the box front, and its front sits 0.15 mm under the
  facade's front. `Hidden Key Part 2` is the removable key: two half-disc tongues (115° each) that go into the
  two half-round pockets in the hidden key's front, one on each side of its bar, and a grip. It is shown
  inserted, turned 29° about its axis so the tongues sit in the pockets, the root of its tongues against the
  hidden key's front. The manuals don't draw this option. An entry holds both locks; a unit's part list names
  either the key and key cap or these two files, and the page draws only the files the list names.
- **XL runner slides** are wedges: the XL box's sides narrow towards the back (0.035 mm per mm on XL3, 0.038 on
  XL7, from depth maps of both sides), and each XL slide tapers the same way (12.0 mm thick at the front,
  16.0 at the back of x3, 22.6 at the back of x7). The sloped face goes in the box's groove, 2.2 mm in from the
  box's face at the front, as on S/M/L. The flat face runs along the straight guide. (Placed by its bounding box,
  as before, the wedge stood 4 mm out on XL3 and 10.6 mm on XL7, through the module's wall at the back.)
- **Roofs** (S, M, L, XL): turned so their latch frames are underneath, 12 mm from the back (on some roofs the
  frame's rim runs into the next relief, so only its back edge counts); otherwise placed like a module.
  Heavyweight (and cut) roofs: the handle is a bar across the middle slot, in the pockets of its walls (156 mm
  apart for a 156.5 mm bar; its axis 59.8 mm above the roof's bottom, the middle of the pockets, which run from
  44.7 to 74.9 mm on every heavyweight roof, measured on sections of all 30; manual p. 10). Grid roofs: the
  optional top handle (option `topHandle`, manual p. 18) **stands** on the grid, long side across, its hole running
  front to back (it was set lying flat until the bolts showed it). Its bottom has two notches over the grid's pegs at
  x = ±21 and two 6 mm channels that run up and out at 45° to its ends; each continues a 45° hole through the grid
  under it (x = ±22.4, in the middle of the roof's depth; 10 mm further back on S3 and M3, measured on all 20 grid
  roofs). Its feet sit between two cross ribs, which leaves it one depth (the one where it comes down furthest,
  0.05 mm from the holes'), and it comes down 3.54 mm from the roof's highest point onto the ribs (3.21 on XL3,
  whose decimated grid is off by up to 1.2 mm). Its channels are then 0.4 to 0.7 mm off the grid's hole axes. Each pocket has a wedge-shaped entry groove (back on the right,
  front on the left) closed by an insert once the bar is in: two inserts per heavyweight roof. The right one is
  where USSA's CAD scene has it, against the bar's end (0.5 mm off the groove's back wall, its peg in the groove's
  hole); the left one is the same turned half a turn about the bar's vertical axis.
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
  edge, 43.6 mm under the top, pushed to its end.
  Hinges (manual p. 17), each piece of a file on its own (`piece`):
  - the hinge file (`S-M 1F`, `S-M 2-4F`, `L-XL 1F`, `L 2-4F Hinge`) holds the two body leaves, mirror images
    printed face to face. Each leaf bolts inside the back wall, on the 2 mm pad under a notch in the wall's top,
    with 4 M4 × 10 bolts. Its 4 holes (23 × 15.4 mm apart on S/M, 33 × 15.4 on L/XL; 34.6 down the plate on
    2-4F) meet the wall's at x = ±51.9 (S), ±69.27 (M), ±86.8 (L), ±131.4 (XL). The crank goes over the
    lowered wall and the knuckle sits behind it, touching the back face.
  - the hinge top bolts under the lid with 4 M4 × 14 bolts, into the lid's holes 16 and 36 mm in front of the
    body's back face. S and M have one long top (62.8 / 98.8 mm) between the two leaves, at x = 0. L and XL
    have a file with two 40 mm tops, each 0.5 mm inside its leaf, at x = ±41.3 (L) and ±85.9 (XL). The plate's
    face through the knuckle's axis is its bottom face.
  - every knuckle is on one axis along x, level with the body's top and 7.49 mm behind its back face. On every
    case measured (S3, M5, L3, XL3, XL7 1F; S3, L7 2F; S7 4F), the leaves' holes and the wall's agree within
    0.02 mm, and so do the tops' and the lid's.
  - the rods (one file holds both): 7.9 mm shafts in the 8.3 mm bores, one from each end, its head against the
    leaf's outer end.
  The hinge tops' plates stop 0.85 mm under the lid's bosses on every height: the lid's push-fit height and
  the hinge disagree by that much. The lid stays where the push fit puts it, since the locks and the stacking
  height were measured from there.
- **Bolts** (`hardware.py`; manual p. 3 "Hardware List", p. 17 and 18 "Required Hardware", Drawer Assembly 6/8):
  - drawer front to box, M4 × 14 button head: from the front through each bolt hole of the facade, the head on the
    counterbore's floor 4.1 mm under the facade's face (the facade cap closes it, 0.6 mm over the head), into the
    box's front wall; 0.5 mm left at the tip (0.6 on XL);
  - case front to body, M4 × 20 button: through the front panel's holes (its face, no counterbore) into the body's
    side walls (and a floor rib in the middle on L and XL); 3.0 mm left;
  - case hinge leaves, M4 × 10 button: from inside, through each leaf into the back wall; the hole is exactly 10 mm
    deep under the head;
  - case hinge tops, M4 × 14 button: from under the back of the lid, through each top into the lid's bosses; they
    turn with the lid (group `lid`); 0.3 to 0.7 mm left;
  - case lock holders, M4 × 14 button: from inside the case, through the holder into the front panel's blind holes,
    exactly as deep;
  - grid roof top handle, M6 × 50 countersunk: up from under the roof, the head in the 45° hole's countersink (its
    cone fitted from r = 3.5 to 6 mm, carried on to the head's diameter: the hole's mouth opens on a slope, so its
    rim isn't square to the bolt), through the grid into the handle's channel; 0.7 mm left (0.9 on XL3).
  Parts held in several variants (key / hidden key, baseplates, case body styles) take the same bolts: the bolts are
  measured on the default variant and carry the index of the part that holds them, which every variant shares.
- **Checks against USSA's renders**: `compare_board.py` puts a crop of a PDF page next to our render, for a phone
  (boards in `VAULT_ASSEMBLY/_compare/`, outside the repo: they hold USSA's renders).
- **Checks**: every unit is assembled with front, iso, side-section, top-section (runner level) and bottom
  views; one tower per family is rebuilt from the JSON and the original files (`blender_check_placements.py`,
  which also writes a side section and a `.blend`): S5, M3, L4, L²+L, XL+XL², XL², and S cases with an S drawer.
  The regenerated S3 1F and L7 entries match the first session's checked ones (within 0.3 mm).

## Findings for the page (src/rules.js, src/template.html)

- Bolt counts, planner (`unitHardware`) against the files' holes (left as they are, to decide): case fronts take
  7 M4 × 20 in the planner and in the manual (drawn on an L 4F), but the panels have 4 holes on S and M 1F/2F, 6 on S
  and M 4F, 5 on L 1F/2F and XL, 7 only on L 4F. Cases take 16 M4 × 14 in the planner and the manual (an L: 2 hinge
  tops, 2 locks); S and M have one hinge top with 4 holes and one lock, so 8. M4 × 10 (8), drawer fronts and the
  top handle's M6 × 50 agree.

- On this machine the unzip turned `²` into `┬▓` (`04. L┬▓ Families/L3┬▓/...`). `R.norm` doesn't map it, so the
  planner can't find the L² and XL² files there. Mapping `┬▓` to `²` in `R.norm` would fix it.
- Cases: the measured rise (66.4 / 100.4 / 196.4) is 0.9 mm above `R.exterior` (65.5 / 99.5 / 195.5); it is in
  `stack.case.rise`, which `build.py` does not embed yet.
- Now in the planner (`src/rules.js`, checked by `validate.js` "PLACEMENT COUNTS", where a file split into
  pieces counts once per set of its pieces):
  - latches per unit: S and M 1; L, L², XL and XL² 2, cases included (a case body has a module's latch frames);
  - a facade cap per counterbore (S1F 1, S2F/S4F 3, M1F 3, M2F/M4F 5, L1F 3, L2F/L4F 5, XL 3);
  - runner guides, slides and stoppers: a pair on every 48 mm level (2, 4 or 8 of each for 1F, 2F, 4F);
  - case locks: S and M 1, L and XL 2;
  - one geared-rails file per drawer (both racks), one hinge file per case (both leaves), one hinge-top file.
- Roofs have a module's latch frames too and the JSON places latches there (the page gives a roof its unit's
  latch files), but the manual's exploded S3 with a grid roof (Drawers Naming) shows a single latch, so the
  planner lists none for the roof itself.
- Pieces: the page splits a file into its connected pieces (corners welded at 0.001 mm, from the simplified mesh)
  wherever an entry has `piece`, and takes the one whose centre is nearest. Case lids turn about `hinge` with the
  Open tool.
- The JSON's roles are the first session's (body, drawer, facade, mech, accent, insert, roof); the page takes each
  part's role from the planner's list instead.
- Decimation: 8 of the 733 files stayed above the 0.15 mm QA after the voxel fallback (M5 Module 2F/4F, S6 1F/2F
  case bodies, L3 1F/2F/4F Dividers case bodies, XL3 Grid Roof; worst 1.2 mm). That only touches the renders and
  the bbox alignment by a fraction of a millimetre; the page reads the original files.
