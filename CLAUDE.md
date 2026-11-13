# Vault Print Planner — fork with a 3D stack view

Fork of rmacasieb/vault-print-planner (upstream remote: `upstream`; ours: `origin` = doooools/vault-print-planner).
Upstream takes no feature requests ("fork it and change it"), so this fork is ours to maintain.
**Talk to the user in French.**

## Goal of the fork
A **3D view of each stack** built from the user's own Vault STL files, with **colours** per part role (shell, front,
drawer box, accents…), per stack and per unit, that feed what the planner does with colour: plate grouping, filament
per colour and the Bambu project. Both are done (see "What is done"); the fork is now maintained and extended on the
user's requests. Live site: https://doooools.github.io/vault-print-planner/ (GitHub Pages from `main`).

## Where the work stands (2026-11-12)
- The page redesign in `docs/ux-redesign.md` (approved 2026-11-11) shipped, all seven steps: tabs 1 · Design,
  2 · Print, 3 · Hardware, 4 · Assemble; footprint and roof per stack, levels edited in place in an inspector, the
  Paint tool, the plate sheet, several drawers per module. Read the brief before UI work: its layout, tokens and
  wording still hold. Its "Open points" and "Later" are what is left of it (store links, an XL 1F level asked for 2F,
  animated GIFs in Assemble). `docs/colors-3d-redesign.md` is history.
- What the 3D view doesn't place yet: `tools/placements/COVERAGE.md` and the project's Library file
  `3d/stl-absents-de-la-3d.md`.

## Checks
- Every pull request and every push to `main` runs `.github/workflows/check.yml`, i.e. `python -I tools/check.py`:
  `index.html` is the build of `src/`, `validate.js` finds no problem (it exits 1 on any; unused files are only
  listed), the page's scripts parse, no mesh file is committed. Run it before pushing.
- Every merge to `main` publishes the site within a minute. `index.html` is generated: on a merge conflict in it,
  merge `src/` and rebuild, never edit it by hand.

## Hard rules
- The page is **one HTML file** (`index.html`) built from `src/` and runs entirely in the browser. It has no external
  scripts. Load three.js (or similar) **only when the 3D view is shown**, as a dynamic import from a pinned CDN
  version, and keep the rest of the page working without it.
- **Never commit USSA geometry**: no STL (original or decimated), no `.blend`, no renders of the parts. Vault's
  files are commercial and the page must keep reading them from the user's own folder only. Numbers derived from
  them (measurements, placements) are fine, like the existing `src/stl-measurements.tsv`.
- After any change in `src/`, rebuild and check the page:
  `python -I src/build.py --public src/stl-measurements.tsv index.html previews/index.tsv`, then
  `python -I tools/check.py`. `.gitattributes` keeps text files in LF on every system. Keep `build.py` reading and
  writing UTF-8: the user's checkout is on Windows.
- Work on a branch off `main` (`claude/<name>` for Claude's threads), one pull request per piece of work. Claude
  commits, pushes and opens the pull request without asking first (the user's rule since 2026-11-12, confirmed in
  this file's update); **merging stays with the user**.

## What is done
- `src/build.py` fixed, plus `src/printer-beds.tsv` and `src/bambu-reach.tsv` recovered from the published page:
  `src/` now rebuilds the page.
- `src/stl-placements.json`: per unit, each part's file, colour role, group and a 3x4 matrix from the file's own
  coordinates to the unit frame (three.js axes: +X right seen from the front, +Y up, +Z towards the viewer, mm,
  origin at the middle of the module's front bottom edge), plus the stacking rule. Format, method and rules:
  `tools/placements/README.md`.
  - Unit keys: `drawer|S|3|1`, `drawer|L|7|{1,2,4}`, `roof|L|7|{bowl,grid,heavy,table,undertable}`
    (the planner's own ids: `R.ROOFS`, `R.HEIGHTS`).
  - group `drawer` parts slide out along +Z when the drawer opens; `module` parts stay.
  - Stacking: a unit starts `52 + 48 × (levels − 1)` mm above the bottom of the one below. The planner's
    `R.exterior` uses 51.5 / 99.5 / 195.5 (USSA's figures): within 0.5 mm, pick one and say so.
- 3D view (section "3D stack view" in `src/template.html`): three.js 0.186.1 and meshoptimizer 1.3.0 from jsDelivr,
  loaded when the view is first shown; boxes before the folder is picked, then real parts simplified in workers
  (0.15 mm, cached in IndexedDB). Shown in step 1 (Design) in the middle of the stack's card (`designCenter`'s
  `.v3-slot`): `v3sync()` (after every render) moves the one persistent `#v3view` into the shown step's `.v3-slot`, or
  parks it in `#v3home`, and shows the selected stack (`curTower()`) as it is. The model is rebuilt only when
  the stack changes (`v.key`, colours left out), and just repainted otherwise. A rebuild of the same stack (any change: an option, a divider,
  a level added) keeps the camera (position and target), every drawer and lid open or closed, and the selection:
  `close3d` → `v3keep` saves them in `v3ui.keep`; `open3d` matches the new units to them (`v3match`: same `cfg` object
  first, then same kind, level and rank). Another stack is framed afresh. `v3park()` takes the view
  out before step 1 redraws with `innerHTML` (else it goes with the old page and `getElementById` stops finding it). One WebGL renderer (`v3gl`) for the page's life; `close3d`
  drops a model's scene; `v3ui` carries tools and camera direction over. The `#v3d` dialog ("3D view, enlarged") is
  still in the page and `v3sync` still honours it, but nothing opens it any more.
  One view since step 3 of `docs/colors-3d-redesign.md` (`open3d`):
  toolbar `v3tools` (Turn: a click selects; Paint: brush bar with the tray's colours, "More…" adds one, "Same part
  everywhere" / "This unit only", hover tints what a click would paint via `v.hot`; Drawers: a click opens or closes a
  drawer), views Front / ¾ / Side (`v.aim`), "Spread units" and "Hide roof" (`v.arrange`). Side column `v3side`:
  "Selected" card (`v3sel`, "Change color…" opens the picker, "Back to the project color"), units top to bottom
  (`v3list`: progress, role swatches ringed when the unit has its own). `v3paint` writes the colour; `v3owner` says
  whose `cfg.colors` a part's own colour goes in (a roof's parts are its unit's).
  Checked in Chrome: L7 4F + 2F + 1F + grid roof, 16.4M → 151k triangles. `build.py` embeds `window.VAULT_PLACEMENTS`.
- Colours: `R.ROLES` / `roleOf` (rules.js) give every part a colour role whose default is its old `colorOf` colour
  (`validate.js` checks), so a build with no choices plans exactly as before. A part's colour (`colorFor`): the unit's
  own `cfg.colors`, else its stack's `t.roles`, else the project's `colorPrefs.roles` (palette and roles in
  localStorage `vpp.colors`), else the role's default. `paintLines` recolours lines; a non-default colour gets its own line key
  (`path#colour`), so plates and progress keep it apart. The Bambu project gets one filament per plate colour
  (slot 1, TPU in 2, others from 3). Bambu Studio counts filaments by `filament_colour` and refuses a project
  whose `filament_extruder_variant` / `filament_self_index` don't give every filament its rows ("Invalid configuration
  file"): new filaments get copies of filament 1's rows. A project with several colours opened in Bambu Studio
  (after a Bambu Studio update made at the same time).
- Bambu Lab colours: `src/bambu-colors.tsv` (PLA Basic/Matte, PETG Basic/Matte on sale in the EU store, with the
  hex from Bambu's own `filaments_color_codes.json`, matched by colour code), made by `tools/bambu_colors.py`,
  embedded as `window.BAMBU_COLORS`, offered as a swatch grid in the filament picker. PETG colours still get PLA
  settings in the Bambu project.
- Choosing colours: one filament picker everywhere (`filamentPicker`, step 1 of `docs/colors-3d-redesign.md`): header
  (role, where it was opened), "Whole stack" (or "Whole project" with no stack) / "Only this <unit>" when a unit is
  known (writes the stack's `roles`, `colorPrefs.roles` or the unit's `cfg.colors`), your tray, Bambu Lab's colours (search, line
  filters, grid by shade), and a footer button "Use it" / "Add as slot N" (a new colour joins the palette only then).
  `fpButton` + `bindPickers` show a role's colour as a button that opens it: in place inside dialogs, as a popover
  elsewhere. Used by the part preview and the 3D view's "Selected" card; with `role: null` it only adds to the tray
  (the Colors panel's "Add a filament", the brush bar's "More…"). `after(id)` gets the colour applied.
- Colors (`paintPanel`: the inspector while the Paint tool is on): the filament tray with each colour's use, the role
  list (a click paints a role with the brush, `paintRole`), the modules' own colours as exceptions (`ownColors`),
  "Add a filament" (the catalogue under the view, `fpAdding`); presets (`applyColorPreset`) and `ROLE_GROUPS`.
  Slots come from `trayUse()`: one per colour in use, in tray order (1, then 3…), like `buildProject`; labels on their
  own plate (`labelsApart`) don't count.
- Tabs: 1 · Design (`view` 'build'; a saved 'unit' opens it), 2 · Print, 3 · Hardware, 4 · Assemble (`renderTabs`;
  2 to 4 are disabled while there is nothing to make). Design (`renderBuild`) = the stacks' rail (stacks, "New stack",
  templates, design file, loose parts), the selected stack's card (`designCenter`: name, Stack settings, Footprint,
  "Add a level on top", the 3D view) and the inspector (`#dInsp`, `renderInspector`: the selected level, the stack's
  settings, or Colors while painting). Selection: `dsel` = `{t, l, u}` (stack id, level, unit in the level), or
  `{t: 'loose'}`. With no stack yet, `renderStart` ("Start your build": printer, Vault folder, templates; skipping the
  folder sets `folderHeroSkipped`).
  The old `mech` role was split into `runners`, `lock`, `hinge` (saved choices are carried over on load).
- Opening and closing (branch claude/open-close-kinematics-…): every drawer and case has `motion` in the JSON
  (README "Motion"): the key turns a quarter turn and its 20-tooth pinion moves both racks 20 mm (a closed drawer is
  locked: key back, then slide); a case's toggle latch is a linkage (link about pin A, lever on pin B, tooth sliding
  out of the lid's groove through the dead centre, then the lever stands up) before the lid turns. Parts carry
  `{"joint": …}`; the page's `v3joint` / `v3pose` / `latchPose` run the steps (`u.t` 0 closed … 1 open, ~1 s).
  `tools/placements/kinematics.py` (same pose, collision check on sections) and `blender_motion.py` (key frames).
  Measuring it moved every drawer part but the module and latches 1.2 mm up (`MODULE_UNDER_BOX` 9.8) and turned the
  case latch's link end for end.
  A case with a unit on it (not a roof) opens by `motion.release` instead (`measure_rods.py`): latches as usual, then
  the hinge rods (`rod_1`/`rod_2`, slides along x) leave the hinge tops, then the lid and the whole stack above rise
  by a 4F module (`V3_LIFT` 196 mm, joint `lift`, `u.lifted` summed by `liftOf` in `placeUnit`).
- Several drawers in one 2F/4F module (S, M, L, L²; `R.LAYOUTS`): `units[key].layouts["2,1,1"]` = drawers (index top
  to bottom, height, lowest level, opening steps), their parts tagged `{drawer, side}`, per-drawer key/rack joints and
  front bolts. `measure_levels.py` found the shells' levels exactly 48 mm apart; `make_recipes.py LAY` → Blender →
  export; `check_layouts.py` checks each drawer's motion among the others (tools/placements/README.md "Layouts").
  `build.py` embeds them: the page grew from 1.5 to 3.0 MB.
  An L² / XL² with one drawer per side (1F, or 2F with one 2F drawer) has no per-drawer tags: the page's `sideDrawers`
  makes one drawer per side (its `key_<side>` and racks) and `sideOf` sorts the parts by side as they load.
- Checked: `tools/placements/blender_check_placements.py` rebuilt an L7 4F + 2F + 1F + grid roof tower from the
  JSON alone, and an S3 1F from the **original** download files. The matrices apply to the user's files as they are.
- Bolts in 3D (branch `claude/hardware-3d-a9c94c`): `tools/placements/hardware.py` measures, on every assembled unit, the
  holes each bolt goes in and writes `hardware: [[spec, group, m, {part, why}]]` per unit plus `hardware_sizes` (ISO
  sizes) into `stl-placements.json`; rerun it after every export. The page makes the bolts from the sizes
  (`hwProfile`/`hwRevolve`, section "hardware" in `src/template.html`), draws each with the part that holds it (`part`),
  in its group; toolbar toggle "Bolts" (`v3hw`, saved), metal colour in `colorPrefs.hardware` (not a filament role:
  plates and the tray ignore it), set from the "Selected" card (`v3selHw`). The grid roof's top handle now stands
  (it was flat). Counts that differ from the planner: `tools/placements/COVERAGE.md`, "Hardware".
- Backbone column and handles in 3D: `tools/placements/measure_column.py` (numpy, on the files) writes `column|<w>`
  (S, M, L, XL; `column|U` the universal backbones): backbones, pull-out handle lock + knobs, stationary and pull-out
  handles, each in a column frame (x = 0 between the M16 rods, y = 0 at its bottom, z = 0 on the modules' back).
  The page's `columnPlan` (shared with `analyzeStack`) and `stackColumn` turn the stack's backbone and handle lines into
  a unit of its own (`column: true`, `stack: true`) stacked up the back: it shows with or without a base, as boxes
  before the folder is picked, hidden when spread. The base unit no longer carries the handles' lines. Rules and
  what is inferred (the manual's Modifications Assembly 7-19 wasn't at hand): tools/placements/README.md
  "Backbone column and handles". Differences with the part list: 1 knob on S (the planner says 2), 2 universal
  backbones per F pair (one per rod; the planner counts 1).
- Pegboards, wall mounts, baseplates, lock pins in 3D: `measure_column.py` (pegboard attachments in `column|<w>`, hung
  by `stackColumn` on the free backbone sections nearest their unit, 4 M4 × 40 per section), `measure_wall.py`
  (`wall|<w>|<h>`: plate + cleats, added by `placeParts` on the unit's back), `measure_baseplates.py` (XL drawers'
  Gridfinity baseplates into `drawer|XL|<d>|1`, cases' into `casebase|<w>|<d>`, added by `placeParts`) and
  `measure_lock_pins.py` (the case latches' 4 pins, one `piece` each, on pins A and B). The baseplates and pins must be
  rerun after a Blender export. Inferred, not measured: which backbone section a pegboard takes, the wall plate's height,
  the pins' places along their bores (README "Pegboards, wall mounts, baseplates and lock pins"). Still not placed:
  the key lock's springs, the L² accessories, the "Connector for Modules" (never listed by the planner).
- Manual supports are a Print option now ("Plate options…" → "Manual supports", `printAids`, saved as
  `manualSupports`; on at first load if any unit had the old unit option): one `x<d>` prop per drawer roof (`roof()` in
  rules.js, `aids` argument), packed against its roof by `planPlates`. A roof printed diagonally (`care`) can't take one:
  the step says the prop was left out. L² and XL² take one set of accessories (1st + 2nd) per F (the user's rule,
  2026-11-12). The springs are left out of the 3D on purpose for now.
- Case dividers (branch `claude/project-thread-jbhoyd`): a divider only goes in a slot moulded in the body's walls.
  `tools/placements/measure_dividers.py` measures every case body's slots (`dividers` in each `case|*`: S/M "plain" side
  slots; L/XL "dividers" side slots + 2 back slots, an egg crate; L/XL "sealed" cells with their own side slots; flat:
  none) and stands each divider file up (`divider_files`); README "Case dividers". The inspector draws the case from
  above and a click fills or empties a slot (`dividerPlan`, `divToggle`, `divAll`); the unit keeps `cfg.divSlots` per
  style and `syncDividers` (in `fixUnit`, and on load) keeps `cfg.dividers` (the counts `rules.js` reads) in step.
  `rules.js` leaves out dividers the body style can't take; XL's side seal dividers have their own count
  (`dividers.sealSide`). `dividerParts` adds them to the 3D in their slots, standing in the floor grooves.
- Drawer grid dividers (same branch): `tools/placements/measure_grid.py` measures every drawer box's peg-hole grid
  (`grid_boxes`, 10.5 mm pitch; README "Drawer grid dividers") and stands each divider / edge piece / pin file
  (`grid_files`). The inspector's plan (`gridPlan`) keeps one plan
  per box size (`cfg.gridPlans[<w><d>]`: lines `[o, at, a, b]`, a divider on row/column `at` from hole a to hole b).
  Since branch `claude/project-thread-8vupuk` (Dols, 2026-11-13) a divider is placed in two clicks, its start then
  its end (`gpend` holds the first; `gridEnds` lists the holes the second can take, shown on the plan; `gridHover`
  previews it); a click on a divider removes it. `gridLayout` reads the ends: the outermost hole = at the wall
  (straight piece where the gap is 8 to 20 mm, the tongue's reach, else "N" alone), two rows from a divider running
  across = meets it (rounded piece), else open; 5 to 32 holes, longer = two files end to end (`gridSplit`). Plans
  saved as `[o, at, s]` (PR #13: to the walls or the dividers in the way) are read as spans by `gridSpans`.
  `syncGrid` writes `cfg.gridPieces` (files by hole count, straight / rounded edge pieces), which `rules.js`
  `gridDividers` reads; the old counts (`gridAcross`, `gridAlong`) make an even grid (`gridEven`). "Close against the
  walls" (`gridSeal`) picks the straight piece or the file alone at a wall.
  `gridParts` draws them in 3D with the box.

- Each drawer its own inside (branch `claude/project-thread-fvvql3`, Dols 2026-11-13): in a module holding several
  drawers (2F/4F layouts, the two sides of an L² or XL²) each drawer keeps its interior, baseplate cut-outs and grid
  plan in `cfg.inside[<id>]` (`R.drawerIds`: id = side + index top to bottom, the 3D view's mover ids; `R.INSIDE` the
  fields). `syncInside` (in `syncGrid`) gives each drawer a copy of the module's fields when it has none (saved states
  and templates plan as before), prunes gone drawers and folds back to the module's fields at one drawer. The inspector
  picks the drawer (`dsel.d`, "Drawer to set up", or a click on it in the view: `v.sel.mv`), shows it through
  `drawerView` and outlines it in 3D (`v3mark`); "Same inside in every drawer" copies it. `rules.js` `drawerInsert`
  reads each drawer's own; `gridParts` lays out each box's own plan. Lock, rails and the rest stay per module.

- Stack size (branch `claude/project-thread-mam5az`, Dols 2026-11-13): the stack header and the template cards give
  the outside size as it stands, drawers closed (`stackSize`): units' `bbox` placed by `stackLayout`, base, wheels,
  foot, casters (70 mm, a guess), roof and its handle, key locks, latches, hinges, column pieces, wall plates.
  `tools/placements/measure_envelope.py`; README "A stack's outside size". The level header still gives the module.

- Store links and affiliation (Hardware, "Where you buy"): Amazon.com keeps upstream's affiliate short links
  (`link.amazon/…`, Romy's tag inside; `SHOP`, the product each opens in a comment), at the user's request
  (2026-11-13). Every other store's search link takes this fork's tag from `SHOP_TAGS` (one per store, '' = no tag
  and no `tag=` parameter; `shopTag` never gives one to `com`). Disclosure: under the store picker (`shopDisclosure`)
  and in the footer's "Store links" (`footShop`). Affiliate links get `rel="sponsored"`.

## Where things are on this machine
- Local paths (Vault download, decimated copy, pilot, Blender) and the mockup links are in `CLAUDE.local.md` at the
  main checkout's root, which is not committed.
- The tooling reads `VAULT_RENDER` and `BLENDER` from the environment.

## Page internals worth knowing (src/template.html)
- `towers` (~l.928): stacks, each `{ id, name, levels: [[unit, unit?], ...] bottom→top, stack: {base, wheels, feet…},
  roles? }`. A level is one unit or two side by side (S+S = L, S+M = XL).
- `R.buildUnit(c, resolve)` (rules.js) lists a unit's files (`lines[].file.path`, `qty`, `color`); `analyzeStack`
  (~l.1039) plans a whole stack.
- `renderBuild` (~l.1995) is step 1, Design; `renderPrint`, `renderHardware`, `renderAssemble` the others; `renderAll`
  redraws the shown one.
- Reading the user's files: `pickVaultFolder` (~l.3044), `filesFromHandle`; STL parsing with vertex welding: `readStl` (~l.2940).

## How the 3D view was built (all done)
Boxes from `R.exterior` before the folder is picked, then the real parts: read with the STL code, **simplified in the
browser** (a whole tower can top 20M triangles), cached in IndexedDB and placed with the matrices. Some source files
are nasty (S1F facade: ~170k zero-area triangles that wreck naive decimators): weld and drop degenerate faces first.
Placements are matched to the unit's lines by file path; parts with no placement are listed, never guessed. Every
part the planner lists is placed now but a few (springs, L² accessories…): `tools/placements/COVERAGE.md`.

## Gotchas met in the page
- Claude desktop's built-in browser can't hand a folder to a page (`showDirectoryPicker` aborts at once and the
  folder upload field reports a cancel). Test with real files in Chrome or Firefox.
- The biggest STL are ~215 MB (L7 Module 2F, 4.3M triangles). Simplifying several at once in one tab ran it out of
  memory and the workers died silently: keep the byte budget and the timeout in `meshRunner`.
- Bounds of placed parts: `Box3.setFromObject(o)` turns each file's own box, and the parts printed on edge at 45° (L 1F
  modules) then give a box ~380 mm tall. Pass `precise = true` (vertices), as `v3mark` does for the level's outline.
- Roof handles (manual p.10 "Roof Types", p.18 "Required Hardware – Drawers"): only the grid roof (Top Handle, opt-in
  `topHandle`, 2 × M6 × 50) and the heavyweight roofs (a bar + 2 inserts) have one; `validate.js` checks it ("ROOF
  HANDLES"). `normalize()` swaps a heavyweight roof for the grid one when it isn't made in that width or is too big for
  the printer (any XL heavyweight roof on an H2S): it now ticks the top handle so the handle doesn't vanish. A level of
  two units takes its roof from `roofOf(lv)` (the first unit with one), not just the left unit.
  The heavyweight bar's axis is 59.8 mm above the roof's bottom (its wall pockets run 44.7–74.9 mm on all 30 roofs);
  each pocket's entry groove takes one insert (placed from USSA's CAD scene, left one turned half a turn).

## Gotchas met while measuring
- Parts are exported in print orientation, scattered in one CAD scene. Some are printed on edge at 45° (L 1F
  module, L roofs): use real-vertex bounds after rotating, never the local bounding box.
- Blender's "Smooth by Angle" modifier gave star artefacts on decimated flat faces. Smooth + sharp edges above 20°
  + Weighted Normal is clean.
- Appending the same .blend twice renames things (`_Drawer.001`, `VAULT_body.001`): match by prefix.
