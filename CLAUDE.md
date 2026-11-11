# Vault Print Planner — fork with a 3D stack view

Fork of rmacasieb/vault-print-planner (upstream remote: `upstream`; ours: `origin` = doooools/vault-print-planner).
Upstream takes no feature requests ("fork it and change it"), so this fork is ours to maintain.
**Talk to the user in French.**

## Goal of the fork
Add to the planner a **3D view of each stack** built from the user's own Vault STL files, with a **colour picker**:
colours per role (body, facade, drawer box, accents…) and per unit (e.g. each drawer's facade). The chosen
colours must feed what the planner already does with colour: plate grouping, filament per colour and the
3MF/Bambu export. Today colours are fixed categories in `src/rules.js` (`colorOf`: body / inner / accent / tpu)
and `COLOR_NAME` / `COLOR_FILL` in `src/template.html`.

## Hard rules
- The page is **one HTML file** (`index.html`) built from `src/` and runs entirely in the browser. It has no external
  scripts today. Load three.js (or similar) **only when the 3D view opens**, from a pinned CDN version, and keep the
  rest of the page working without it.
- **Never commit USSA geometry**: no STL (original or decimated), no `.blend`, no renders of the parts. Vault's
  files are commercial and the page must keep reading them from the user's own folder only. Numbers derived from
  them (measurements, placements) are fine, like the existing `src/stl-measurements.tsv`.
- After any change in `src/`, rebuild and check the page:
  `python -I src/build.py --public src/stl-measurements.tsv index.html previews/index.tsv`.
  On this branch's first commit the rebuild was byte-identical to upstream's published `index.html`, ignoring CRLF
  (this checkout has `core.autocrlf=true`). Keep `build.py` reading and writing UTF-8, since this is Windows.
- Commit or push only when the user asks. Work on `feat/3d-stack-viewer` (or a branch off it).

## What is done (branch feat/3d-stack-viewer)
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
- 3D view, milestone 1 (section "3D stack view" in `src/template.html`, dialog `#v3d`, "3D" button on each stack
  card): three.js 0.186.1 and meshoptimizer 1.3.0 from jsDelivr, loaded on open; boxes before the folder is picked,
  then real parts simplified in workers (0.15 mm, cached in IndexedDB); click a drawer to open or close it.
  Checked in Chrome: L7 4F + 2F + 1F + grid roof, 16.4M → 151k triangles. `build.py` embeds `window.VAULT_PLACEMENTS`.
- Colours: `R.ROLES` / `roleOf` (rules.js) give every part a colour role whose default is its old `colorOf` colour
  (`validate.js` checks), so a build with no choices plans exactly as before. Palette + role choices in
  `colorPrefs` (localStorage `vpp.colors`, panel "Colors" in step 2); per-unit choices in the unit's own `cfg.colors`
  (edited in the 3D view's side list). `paintLines` recolours lines; a non-default colour gets its own line key
  (`path#colour`), so plates and progress keep it apart. The Bambu project gets one filament per plate colour
  (slot 1, TPU in 2, others from 3). Bambu Studio counts filaments by `filament_colour` and refuses a project
  whose `filament_extruder_variant` / `filament_self_index` don't give every filament its rows ("Invalid configuration
  file"): new filaments get copies of filament 1's rows. A project with several colours opened in Bambu Studio
  (after a Bambu Studio update made at the same time).
- Bambu Lab colours: `src/bambu-colors.tsv` (PLA Basic/Matte, PETG Basic/Matte on sale in the EU store, with the
  hex from Bambu's own `filaments_color_codes.json`, matched by colour code), made by `tools/bambu_colors.py`,
  embedded as `window.BAMBU_COLORS`, offered as a swatch grid in the Colors panel. PETG colours still get PLA
  settings in the Bambu project.
- Choosing colours: one filament picker everywhere (`filamentPicker`, step 1 of `docs/colors-3d-redesign.md`): header
  (role, where it was opened), "Whole project" / "Only this <unit>" when a unit is known (writes `colorPrefs.roles` or
  the unit's `cfg.colors`; step 1's unit is `c`, via `editorUnit`), your tray, Bambu Lab's colours (search, line
  filters, grid by shade), and a footer button "Use it" / "Add as slot N" (a new colour joins the palette only then).
  `fpButton` + `bindPickers` show a role's colour as a button that opens it: in place inside dialogs, as a popover
  elsewhere. Used by the part preview, the Colors panel, the 3D bubble (`rolePicker`) and the 3D list (`unitColors`).
  Step 1 has a "3D" button: the unit opens with drawers out, a click on a part opens the picker as a bubble, and the
  side column shows the Colors panel. Step 1's tiles (shell, box, front, key lock, roof; case: body, front, lid, hinge)
  each carry a colour square that opens the preview with the picker open. Opening the Vault folder is step 1's first thing: a big card in the middle
  (`renderFolderHero`, "Not now" hides it for the visit), then a one-line status (`unitFolderBar`).
  The old `mech` role was split into `runners`, `lock`, `hinge` (saved choices are carried over on load).
- Checked: `tools/placements/blender_check_placements.py` rebuilt an L7 4F + 2F + 1F + grid roof tower from the
  JSON alone, and an S3 1F from the **original** download files. The matrices apply to the user's files as they are.

## Where things are on this machine
- Vault download: `X:/Download/261021_VAULT_USSA_S/261021_VAULT_USSA_S` (733 STL, 24 GB).
- Decimated copy (≤ 40k faces, same coordinates, for the Blender tooling only): `X:/Download/261021_VAULT_USSA_S/VAULT_RENDER`
  (S3, S facades, universal parts and the L7 family done so far; `_decimate_log.jsonl` has per-file bbox and QA).
- Pilot from the first session (assembled `.blend` files, Cycles renders, its own README): `X:/Download/261021_VAULT_USSA_S/VAULT_PILOT`
  (S3 1F, L7 1F/2F/4F, L7 roofs, `L7_tours.blend` with three stacked towers). Useful as a visual reference for the 3D view.
- Blender 5.2: `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe`.
- The tooling reads `VAULT_RENDER` and `BLENDER` from the environment.

## Page internals worth knowing (src/template.html)
- `towers` (from ~l.685): stacks, each `{ levels: [[unit, unit?], ...] bottom→top, stack: {base, wheels, feet…} }`.
  A level is one unit or two side by side (S+S = L, S+M = XL).
- `R.buildUnit(c, resolve)` (rules.js) lists a unit's files (`lines[].file.path`, `qty`, `color`).
- `stackSvg` (~l.1419): the current 2D stack drawing. `renderBuild` (~l.1654) is the Build step.
- Reading the user's files: `pickVaultFolder` (~l.2220), `filesFromHandle`; STL parsing with vertex welding: `readStl` (~l.2120).

## Viewer plan
1. A "3D" view in the Build step for the selected stack. It draws boxes from `R.exterior` right away (no files
   needed), then the real parts once the Vault folder has been picked.
2. Parts: read with the existing STL code, **simplify in the browser** (a whole tower can top 20M triangles:
   e.g. meshoptimizer's simplifier, WASM), cache the result locally (IndexedDB/OPFS) and place it with the
   matrices. Some source files are nasty (S1F facade: ~170k zero-area triangles that wreck naive decimators),
   so weld and drop degenerate faces first.
3. Match placements to the unit's lines by file path; list the parts that have no placement yet (other families,
   options such as hidden key, handle baseplates, dividers) instead of guessing.
4. Colour picker per role and per unit, wired into plates, filament totals and the 3MF.
5. Later: extend `stl-placements.json` to the other families with the Blender tooling (M, XL, L², XL², other L/S
   sizes via a generator like `make_recipe_L.py`, cases/sustainers, bases, feet, wheels, handles).

## Gotchas met in the page
- Claude desktop's built-in browser can't hand a folder to a page (`showDirectoryPicker` aborts at once and the
  folder upload field reports a cancel). Test with real files in Chrome or Firefox.
- The biggest STL are ~215 MB (L7 Module 2F, 4.3M triangles). Simplifying several at once in one tab ran it out of
  memory and the workers died silently: keep the byte budget and the timeout in `meshRunner`.
- The planner lists 1 latch and 1 facade cap per L7 unit; the measured assembly places 2 latches and a cap in every
  counterbore. Not checked against USSA's docs yet.
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
