# 3D Vault Configurator — fork of Vault Print Planner with a 3D stack view

Fork of rmacasieb/vault-print-planner (upstream remote: `upstream`; ours: `origin` = doooools/vault-print-planner).
**Name** (Dols, 2026-11-23): the page is "3D Vault Configurator" wherever a visitor reads it (title, header, About,
What's new, README, issue forms, the STL / GLB exports' header); "Vault Print Planner" stays only as the original's
name in its credit. Kept on purpose: the repository and the address (`vault-print-planner`), the design file's
`app: 'vault-print-planner'`, the `vpp.*` / `vppPre.*` / `vault-planner` storage keys, `.vault.json`, code names.
Upstream takes no feature requests ("fork it and change it"), so this fork is ours to maintain.
**Talk to the user in French.**

## Goal of the fork
A **3D view of each stack** built from the user's own Vault STL files, with **colours** per part role (shell, front,
drawer box, accents…), per stack and per unit, that feed what the planner does with colour: plate grouping, filament
per colour and the Bambu project. Both are done (see "What is done"); the fork is now maintained and extended on the
user's requests. Live site: https://doooools.github.io/vault-print-planner/ (from `main`); preprod:
https://doooools.github.io/vault-print-planner/preprod/ (from `preprod`, see "Preprod").

## Where the work stands (2026-11-12)
- The page redesign in `docs/ux-redesign.md` (approved 2026-11-11) shipped, all seven steps: tabs 1 · Design,
  2 · Print, 3 · Hardware, 4 · Assemble; footprint and roof per stack, levels edited in place in an inspector, the
  Paint tool, the plate sheet, several drawers per module. Read the brief before UI work: its layout, tokens and
  wording still hold. Its "Open points" and "Later" are what is left of it (store links, an XL 1F level asked for 2F,
  animated GIFs in Assemble). `docs/colors-3d-redesign.md` is history.
- UX audit of 2026-11-14: `docs/ux-audit-2026-11.md` (decisions, eight sessions, open points, findings A1…X4) and its
  mockups in `docs/ux-audit-mockups/`. Where it disagrees with `docs/ux-redesign.md`, the audit wins. Its four open
  points were answered by Dols on 2026-11-14 (written in the brief). Session 2 (fixes without a mockup: A4, A6, B1,
  B6, C2, D7, D8, E1, E4, E5) is done on its branch. Session 6 (Print: D1 to D6) on `claude/print`. Session 7 (Hardware: E2, E3, E6) is done on its branch. Session 3 (the 3D
  view: hover, right-click menus, "⋯", one-line hint, "Bolts" swatches, "?"; A1, A2, A3, A4, A5, A6) is done on its branch.
  Session 4 (Design's panels: A7, A8, B2, B3, B4, X3, X4) is done on its branch. Session 8 (header, File menu,
  tabs: A9, A10) is done on its branch. Session 5 (Paint: C1, C3, C4, C5, C6, C7) is done on its branch.
- The look (Dols, 2026-11-22, preprod first): Giscard Punk "encre" from Claude Design's handoff zip (not committed):
  paper and ink swapped by theme, yellow = selected, pink = the one main action, red = a problem, blue = the whole stack,
  Anton / Special Elite / Courier Prime embedded (`src/fonts/`, inlined by `build.py` at `/*FONTS*/`), one taped card
  per screen (`.ihead`, `.psel`, `.asm-need`; key figure `kfig`), no radius, hard shadows. The 3D view is drawn in ink
  (`open3d`: `toon` (both sides: the simplified parts have hairline gaps), `hullMat` (offset behind the part), `inked`,
  `creaseLines`, hard shadow, stencil selection ring `v3mark` → `ring`, `v.retheme`). Three looks for the 3D view (Dols, 2026-11-24):
  `V3_LOOKS` Ink (the above), Plain (the pre-redesign `MeshStandardMaterial`, its lights and soft shadow, no ink
  outline or creases: `hulls.ink` and `creaseMat` hidden, the hover outline and the selection ring kept) and Halftone
  (`halftone`: Lambert lit, flat colour, ink dots at 45° in the shade, paper dots on dark filaments, toner grain, dotted
  shadow `dotShadow`); `v3look` in localStorage `look3d` (this browser's), `setLook`, `v.relook` (no rebuild),
  buttons `#v3dLook` under the view (`v3lookDraw`), `lookItems` in `viewMenu` and `lookMenu` (`ctxRule` '3d-look'),
  key L, counted `3d/look` and `3d/look-in-use`. Rules: `docs/ux-redesign.md` "Three looks for the 3D view". From 1200 px Design fills the
  window and doesn't scroll (`body:has(#view-build … .design)`): only the rail and the inspector scroll.
  Rules: `docs/ux-redesign.md` "The look", which wins over the older rules there.
- What the 3D view doesn't place yet: `tools/placements/COVERAGE.md` and the project's Library file
  `3d/stl-absents-de-la-3d.md`.

## Checks
- Every pull request and every push to `main` or `preprod` runs `.github/workflows/check.yml`, i.e. `python -I tools/check.py`:
  `index.html` is the build of `src/`, `validate.js` finds no problem (it exits 1 on any; unused files are only
  listed), the page's scripts parse, no mesh file is committed. Run it before pushing.
- Once that check passes on a push to `main` or `preprod`, `.github/workflows/pages.yml` ("Publish the site")
  publishes both branches within a couple of minutes (see "Preprod"), as it does when `merge-preprod.yml` merged a
  pull request into `preprod` and started it. `index.html` is generated: on a merge conflict
  in it, merge `src/` and rebuild, never edit it by hand.
- Review subagents (Dols kept them, 2026-11-14, PR #45): `.claude/agents/voltagent/` holds three of VoltAgent's
  (`surgeon-reviewer` for a diff's real bugs, `security-auditor`, `ux-microcopy-reviewer` for page text against
  `docs/ux-redesign.md`), copied unchanged (`SOURCE.txt`). Run them on request, not on every PR. Their long files ask
  for a "context manager" that doesn't exist and show made-up figures: tell them to skip both and cite file:line.

## Hard rules
- The page is **one HTML file** (`index.html`) built from `src/` and runs entirely in the browser. It has no external
  scripts. Load three.js (or similar) **only when the 3D view is shown**, as a dynamic import from a pinned CDN
  version, and keep the rest of the page working without it.
- **Never commit USSA geometry**: no STL (original or decimated), no `.blend`, no renders of the parts. Vault's
  files are commercial and the page must keep reading them from the user's own folder only. Numbers derived from
  them (measurements, placements) are fine, like the existing `src/stl-measurements.tsv`.
  One exception (Dols, 2026-11-14): the README's screenshots in `docs/images/` may show the real parts, as the page
  draws them from the user's folder. Nowhere else.
- After any change in `src/`, rebuild and check the page:
  `python -I src/build.py --public src/stl-measurements.tsv index.html previews/index.tsv`, then
  `python -I tools/check.py`. `.gitattributes` keeps text files in LF on every system. Keep `build.py` reading and
  writing UTF-8: the user's checkout is on Windows.
- Work on a branch off `preprod` (`claude/<name>` for Claude's threads), one pull request per piece of work, **into
  `preprod`** (see "Preprod"). Claude commits, pushes and opens the pull request without asking first (the user's rule
  since 2026-11-12, confirmed in this file's update). **GitHub merges it into `preprod`** once its
  checks pass (Dols, 2026-11-22; `merge-preprod.yml`); **merging into `main` stays with the user** (see "Preprod").

## Preprod (Dols, 2026-11-22)
- Two sites from one repository: `main` at https://doooools.github.io/vault-print-planner/ (live) and the `preprod`
  branch at https://doooools.github.io/vault-print-planner/preprod/. A repository has one Pages site, so
  `.github/workflows/pages.yml` publishes both in one deployment: main's tree at the root, preprod's under `preprod/`,
  each as its branch stands, so a push to one never changes the other. It starts from `workflow_run` once "Check the
  page" passed on a push (a failed check publishes nothing), and by hand (Actions > Publish the site > Run workflow,
  on `main`). `workflow_run` runs on the default branch, so the `github-pages` environment's "main only" rule holds
  for preprod too. Needs Settings > Pages > Source: **GitHub Actions** (the old "Deploy from a branch" is gone).
- The flow: pull requests go into `preprod`; Dols tries them on the preprod site; to go live, a pull request from
  `preprod` into `main`, merged by Dols with **a merge commit** (a squash would part the two histories). A fix made
  straight on `main` is merged back into `preprod` (`git merge origin/main`) in the same thread.
- Merging into `preprod` (Dols, 2026-11-22: "auto merge", now that the preprod is there to test; GitHub does it since
  2026-11-23, PR #97, because the session's permission check refused threads' merges): `.github/workflows/merge-preprod.yml`
  ("Merge into preprod") starts when "Check the page" passed on a pull request and merges it, with a merge commit, if it
  goes into `preprod`, comes from a branch of this repository (never a fork), was opened by an account in `TRUSTED`
  (`doooools`: Claude's threads open theirs with it), isn't a draft, its last commit is the one checked, it changes no
  file in `.github/workflows/` (`GITHUB_TOKEN` may not merge those: Dols does), and its merge with `preprod` as it is
  now passes `tools/check.py` again. Then it starts "Publish the site" itself (a merge made with `GITHUB_TOKEN` starts
  no other workflow). What it leaves alone says why in its run's log. It never touches a pull request into `main`.
  A thread opens its pull request into `preprod` and doesn't merge it: open it as a draft to keep it out until it is
  ready. A conflict (another pull request merged first): merge `origin/preprod` into the branch, rebuild `index.html`
  from `src/`, run `tools/check.py`, push; the new check starts the merge again. The thread then tells Dols the change
  is on the preprod URL, with what to try there. `workflow_run` reads the workflow from `main` only: a change to
  `merge-preprod.yml` works once it is on `main`. The pull request from `preprod` into `main` (going live) is opened
  when Dols asks, and **only Dols merges it**.
- The page knows it is the preprod from its address (`VPP_PRE`: a `preprod` folder in the path, script in `<head>`):
  a striped strip above the header ("Preprod", "Copy the live project again", "Open the live site"), "Preprod · " in
  the tab's title, a robots `noindex`, and **no GoatCounter request at all** (`counting()`). Its saved state is under
  localStorage `vppPre.*` instead of `vpp.*` (`VPP_KEY`, read by `store` and the theme script): on the first visit
  the head script copies every `vpp.*` key over (flag `vppPre.copied`), then the two never meet, so a test can't
  break the live project. "Copy the live project again" (press and hold) drops `vppPre.*` and reloads. IndexedDB
  (`vault-planner`: the Vault folder's handle, the simplified meshes) is shared with the live site on purpose: the
  folder stays picked and the cache serves both; a change to the mesh cache's format needs a new key.
- Test locally under a `preprod/` folder to see the preprod look (e.g. a copy of `index.html` in `x/preprod/`).

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
  (0.15 mm, cached in IndexedDB under `MESH_CACHE` `mesh3d.6:`; simplifying with the normals as attributes, PR #90,
  was undone by Dols on 2026-11-23: slower, and it didn't clear the modules' fronts and backs; so was a finer
  simplification near sharp edges, PR #102: too slow). The ink comes from the file's own triangles (Dols, 2026-11-23,
  "fausses arêtes du shader"): `meshJob` returns `ink` (segments on every edge of the file sharper than 30°), cached
  with the mesh, carried by `meshPieces` / `meshPiece`, read by `geom` (`g.userData.ink`) and `creaseLines`; `creaseMat`
  draws the lines 0.5 mm nearer the eye. No hole, closed stays closed (Dols, 2026-11-24, "même décimé, le maillage soit
  au moins sans grand nouveau trous, et s'il était manifold avant le décimage il doit le rester"; README "Simplifying
  for the 3D view"): corners are welded only where the file writes the same coordinates, and before simplifying
  `tidy` drops only what has no surface (a corner twice, a triangle twice, a triangle and its reverse). The old
  clean-up (5 µm merge, small faces dropped, seams sewn) opened holes up to 22 mm and made non-manifold edges on 7 of
  14 closed parts. After simplifying, `tidy` again, then the faces round each edge of more than two are paired by
  angle (`pair`, union-find on the corners: each group gets its own vertex) and an edge whose pairs still share both
  ends is cut at its middle. `nrm`: each corner's normal from the simplified faces round it within 30° of its own,
  by area; a sliver (under twice the tolerance across) takes the widest neighbour nearest its slope. Measure with
  `tools/mesh_check.mjs` (`MESHOPT=…/meshopt_simplifier.js node tools/mesh_check.mjs [--old old.html] files…`). The
  ink outline (`hullNormals`) pushes a face under 1 mm across in one piece: the fans the simplifier leaves round a
  hole turned over and drew black wedges across fronts. While a file is really
  simplified (a cache miss in `partMesh`: `simpStart` / `simpEnd`, counts per batch in `simp`), the window `#v3dSimp`
  over the stage says why and that Print uses the original files, with a spinner (`.v3-spin`); done, `simpTuck` folds
  it (~0.65 s, always animated: Dols wants to see it go) into `#v3dSimpBtn` in the strip under the view ("Why simplified?"), which reopens it (Dols, 2026-11-23).
  Its "Parts in the 3D view" setting (`data-v3res`, `setMeshLevel`): five levels in `MESH_LEVELS` (Super low 0.15 mm,
  the default and the old cache key; Low; Medium; High; Native = tol 0, which skips the simplifier), `meshLevel` in
  localStorage per browser (the old `meshFull` = Native); `meshJob(buf, MS, tol, most)` loosens tol until a part holds
  `most` triangles; `partMesh` memo key `path|tol`, IndexedDB key ends `|tol`, only `keep` levels are stored. Shown in step 1 (Design) in the middle of the stack's card (`designCenter`'s
  `.v3-slot`): `v3sync()` (after every render) moves the one persistent `#v3view` into the shown step's `.v3-slot`, or
  parks it in `#v3home`, and shows the selected stack (`curTower()`) as it is. The model is rebuilt only when
  the stack changes (`v.key`, colours left out, or the same levels as new objects: an undo), and just repainted otherwise. A rebuild of the same stack (any change: an option, a divider,
  a level added) keeps the camera (position and target), every drawer and lid open or closed, and the selection:
  `close3d` → `v3keep` saves them in `v3ui.keep`; `open3d` matches the new units to them (`v3match`: same `cfg` object
  first, then same kind, level and rank). Another stack is framed afresh. `v3park()` takes the view
  out before step 1 redraws with `innerHTML` (else it goes with the old page and `getElementById` stops finding it). One WebGL renderer (`v3gl`) for the page's life; `close3d`
  drops a model's scene; `v3ui` carries tools and camera direction over. The `#v3d` dialog ("3D view, enlarged") is
  still in the page and `v3sync` still honours it, but nothing opens it any more.
  One view since step 3 of `docs/colors-3d-redesign.md` (`open3d`):
  toolbar `v3tools` (Turn: a click selects; Paint, whose button carries the stack's filaments as swatches
  (`stackFilaments`): brush bar `#v3dBrush` with one swatch per filament (`data-v3brush`), "+" for the catalogue
  (`data-v3add`), "A click paints" "Whole stack" / "This module only", hover tints what a click would paint via `v.hot`;
  Drawers: a click opens or closes a drawer), the first framing from three quarters (`V3_DIR`, `v.aim`; the Front / ¾ / Side buttons went on 2026-11-14), "Rotate" (Dols, 2026-11-15: `data-v3spin`, key R, `v3ui.spin`, off at each page load; `v.spin` runs OrbitControls'
  `autoRotate` one turn in `V3_SPIN` 24 s, round the target, which a drag holds; started again by `open3d`), "Spread levels" and "Hide roof" (`v.arrange`, which no longer reframes: the camera never moves by itself but on Rotate), "Bolts" (two swatches) and "?" (`v3ui.help`: drag, scroll, right-drag).
  UX audit session 3: with Select, `hoverOn` outlines the level under the pointer and names it in `.v3-hover` (placed
  from its projected box, `placeTip`, again on every camera change); a right-click (button 2 let go within 5 px,
  `rightAt`) on a level selects it and opens `levelMenu` (open or close via `v.openable` / `v.toggle`, add a copy
  above / below: `levelOp` 'dup' / 'dupBelow', move, remove in one click with `undoAs`), elsewhere `stackMenu` (Fit
  the stack in the view = `v.aim(null)`, the only reframing; Add a level on top; Stack settings). Menus: `menuOpen` /
  `menuClose`, one `.vmenu[role=menu]` in `<body>`, closed by `v3park`, `close3d`, the panel redrawn, a scroll or the
  camera moving. The level panel's header has Level below / Level above (`data-lgo`, the selection moves) and "⋯"
  (`data-lmenu`, the same menu); its up / down / duplicate / remove buttons went. Side column `v3side`:
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
  (`catalogPanel`, with `bare` (no header, no tray) and `addLabel`). `after(id)` gets the colour applied.
- Colors (`paintPanel`: the inspector whenever the Paint tool is on, UX audit session 5; `inspPaint` and its "Show the
  colors" strip went, and the rail's stacks and Stack settings go back to Select through `leavePaint`): presets
  (`applyColorPreset`), the role groups (`ROLE_GROUPS`) as `fold` sections with their swatches ("Paint these N
  <brush>", a click on a role paints it, `paintRole`), the modules' own colours as exceptions (`ownColors`), then
  "Your filaments" folded (brush, use, the press-and-hold cross `.pdel` with the stack cross's ring, "Add a filament").
  "Add a filament" and the brush bar's "+" show the catalogue in the panel instead (`fpAdding`, `catalogPanel`,
  `openCatalog` / `closeCatalog`); no block under the view any more.
  Slots come from `trayUse()`: one per colour in use, in tray order (1, then 3…), like `buildProject`; labels on their
  own plate (`labelsApart`) don't count.
- Tabs: 1 · Design (`view` 'build'; a saved 'unit' opens it), 2 · Print, 3 · Hardware, 4 · Assemble (`renderTabs`;
  2 to 4 are disabled while there is nothing to make; counters: none on Design, Print and Assemble in %, Hardware
  "N to buy"). The header's "File" menu (`fileBtn`, `menuOpen` with a `note`) saves and opens design files on every
  step (`saveDesign`, `openDesign`); `designMark` (localStorage `vpp.designMark`: name, hash of `undoSnap()`, changes
  since, counted in `undoCommit` / `undoBack` / `undoForth`) says how the file stands. The file (version 4, Dols 2026-11-15) is the whole project: `projectState()` (design + printer, `print`, `labels`, `hardware`, `assemble`) plus `view` and `sel`; `loadProject` rebuilds each part (`counts`, `ids`, `plainPrinter`, `plainPlates`) and saves it here; a file under version 4 restores the design only. A new setting kept in localStorage that belongs to the project goes in both. `designHash` hashes `projectState()`. Save as… (`saveDesign(true)`): the save window (`showSaveFilePicker`, started in the Vault folder, asked again without it if refused); any other failure than a cancel downloads with the reason in a long toast (`toast(m, { long: true })`), never silently; with no save window, `prompt()` for the name, then the download. "What's new" (`newsBtn`) and
  "Report a bug or an idea" (`reportBtn`) are small links under the page's name (`.logo .hlinks`, Dols 2026-11-14); the
  fork's credit to Romy is What's new's first section, "About this fork", written in `CHANGELOG.md` (`build.py`
  `changelog_html`: `## ` a section, `- ` a list line, other lines paragraphs; a section named "About…" is framed).
  The page has no footer (Dols, 2026-11-15): its notices (not affiliated with USSA, store links, visit count, where the numbers
  come from) are in the "About" window (`#about`, `aboutBtn`, the last link under the name; `aboutShop`, `aboutCount`, `aboutNotes`).
  `template.html` opens with the upstream MIT notice in a comment.
  Design (`renderBuild`) = the stacks' rail (stacks, "New stack", templates, loose parts as an entry like
  the stacks, `.dloose`), the selected stack's card (`designCenter`: name with its pencil, `dRename`;
  Stack settings, which opens and does not toggle; "Add a level on top"; the 3D view) and the inspector (`#dInsp`,
  `renderInspector`: the selected level, the stack's settings with width and depth first (`setFootprint`; no Footprint
  button nor strip since UX audit session 4), or Colors while painting, always). Both panels are foldable sections (`fold`,
  `bindFolds`, `.ifold`: name and a summary, `insideLine`, `backLine`; open state in `foldOpen` for the page's life);
  stack options that need another are greyed with the reason (`sbool(…, dis)`, `.field.off`, `.need`). Selection: `dsel` = `{t, l, u}` (stack id, level, unit in the level), or
  `{t: 'loose'}`. With no stack yet, `renderStart` ("Start your build": printer, Vault folder, templates; skipping the
  folder sets `folderHeroSkipped`).
  The old `mech` role was split into `runners`, `lock`, `hinge` (saved choices are carried over on load).
  The old `accent` role was split the same way (Dols, 2026-11-14): `latches` (the latch under each module, "Latches
  between levels"), `stoppers` (runner stoppers), `rods` (hinge rods); `accent` keeps the springs and geared rails. Each
  takes accent's saved colour once (`splitRoles`: localStorage flag `vpp.rolesSplit`, design files under version 3).
  The runner guides left `shell` for a role of their own, `guides` (Dols, 2026-11-14): no carry-over, `follow: 'shell'`
  in `R.ROLES` instead. `colorFor` gives them the shells' colour (unit, stack or project) until a `guides` colour is
  chosen anywhere (`ownPick`, `following`); Paint's row and the "Selected" card say "same as …" meanwhile.
- Opening and closing (branch claude/open-close-kinematics-…): every drawer and case has `motion` in the JSON
  (README "Motion"): the key turns a quarter turn and its 20-tooth pinion moves both racks 20 mm (a closed drawer is
  locked: key back, then slide); a case's toggle latch is a linkage (link about pin A, lever on pin B, tooth sliding
  out of the lid's groove through the dead centre, then the lever stands up) before the lid turns. Parts carry
  `{"joint": …}`; the page's `v3joint` / `v3pose` / `latchPose` run the steps (`u.t` 0 closed … 1 open, ~1 s).
  `tools/placements/kinematics.py` (same pose, collision check on sections) and `blender_motion.py` (key frames).
  Measuring it moved every drawer part but the module and latches 1.2 mm up (`MODULE_UNDER_BOX` 9.8) and turned the
  case latch's link end for end.
  Drawers run on telescopic runners (Dols, 2026-11-14, `tools/placements/measure_runners.py`, README "Runners"): the box
  goes out `motion.runners.slide + .guide` (about the module's depth + 5 mm), its slides alone in the guides first,
  then the guides with it to the stoppers; closing, the slides go home first. Guides carry `{"guide": level, side?}`
  and ride in their drawer's `rail` group (`railOf`); `v3pose` keeps `u.slid` (the guides only move when a slide
  drags them). Rerun `measure_runners.py … all --write` after every export.
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
  in its group; always shown (Dols, 2026-11-13: the old "Bolts" show/hide toggle is gone); the toolbar's "Bolts" swatches
  (`data-v3fin="black"` / `"zinc"`, `aria-pressed` on the one in use; UX audit session 3) set the build's bolt finish, raw steel (black) or zinc-plated / stainless (grey), saved in `colorPrefs.hardware`
  (`hwFinish`/`setHwFinish`; Hardware's "Bolt finish" and the "Selected" card set the same one). It also names the
  bolts and rods in Hardware's copy and CSV (`hwItem`; the list says it once, above the lines) and goes into the store searches (`shopQuery`); Amazon.com product pages stay
  as they are. Not a filament role: plates and the tray ignore it. The grid roof's top handle now stands
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
- Manual supports are a Print option now (Print's right column, Plate options → "Manual supports", `printAids`, saved as
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
  picks the drawer (`dsel.d`: one tab per drawer, `.dtabs` over the `.dframe` holding its own settings, or a click on
  it in the view: `v.sel.mv`), shows it through
  `drawerView` and outlines it in 3D (`v3mark`); "Same settings in every drawer" copies it. `rules.js` `drawerInsert`
  reads each drawer's own; `gridParts` lays out each box's own plan. Since branch `claude/project-thread-fvvql3` #2
  (Dols, 2026-11-13) the lock (key / hidden key) and the geared rails are per drawer too (in `R.INSIDE`;
  `R.anyHidden` says whether a unit needs the stack's removable key); `placeParts` keeps each drawer's own key, key
  cap or hidden key and racks (`mine`: drawer from the tags, else from the joint's side). The rest stays per module.

- Labels (Dols, 2026-11-14, branch `claude/project-thread-760e4t`): each drawer and case front's text in `cfg.labels`
  (key = the drawer's id from `R.drawerIds`, `'0'` for a module holding one drawer and for a case; section "labels" in
  `src/template.html`: `labelOf`, `labelsOf`, `setLabel`, `LABEL_MAX` 24). The level panel's "Label" section
  (`l-label`, folded at first, Dols 2026-11-15; summary `labelSum`; one `data-ulabel` field per drawer front) redraws the 3D on `input` and
  saves on `change` (one undo step). In 3D, `loadParts` collects each Label part (`LABEL_PART`, with the drawer it rides
  in) in `v.labelParts`; `v.relabel` lays a canvas text (`labelText`) on its face towards the viewer, in the part's group.
  `noColors` leaves `labels` out of the view's key, so typing never rebuilds the model. Free text: `plainUnit` keeps it
  apart (`freeText`), escaped where shown. Not shown: boxes before the folder is picked. Every case has its label
  placed (Dols, 2026-11-15): Label for Sustainers in a 1F front's recess, the drawers' Label.stl in a 2F/4F front's edge
  slot (`make_recipes.py`, pushed to the slot's closed end; the JSON was patched from the Sustainers' placement, same
  rotation). `rules.js` doesn't read labels: the Label line is the same. The canvas text is a part for the brush and
  Select (`userData.role` 'labelText', the label's `cfg`; `v.recolor` only tints it, `v.relabel` draws it).
  Raised text in Print's exports (Dols, 2026-11-15, section "label text"): `labelAssign` (run by `renderPrint` over the
  plates left) gives each Label part on the plates its text (`labelTexts`: plate item → `{s, color, hex}`), in the order
  of the stacks' fronts per kind (drawers' Label also on 2F/4F case fronts, 1F cases' Label for Sustainers) and colour,
  the first `have()` ones taken as already printed. `planFor` puts it on the piece (`text`) with `label: {relief,
  letter, font}`. `textKit(font)` loads three.js, opentype.js 1.3.4 and the label font (`LABEL_FONTS`: Fontsource
  latin 700 woff, Inter by default, pinned) from jsDelivr at the first export that needs them; `labelFace` loads the
  same woff as a `FontFace` for the 3D view's canvas text; `textSolid` extrudes the glyphs (ShapePath.toShapes, ExtrudeGeometry,
  welded: closed meshes), `labelSolid` centres it on the label's flat top face (measured on the files: 44.7 × 19.2 and
  37.7 × 19.9 mm), 80 % of its length at most, turned half a turn (the placements turn the file half a turn on the front).
  Bambu project: a second `<component>` / `<part>` of the label's object with its `extruder` (the `labelText` colour's
  slot, added to the filaments when no plate prints in it). Plate files: a second PrusaSlicer volume in the same mesh.
  Settings `labelRelief` (0 = none), `labelLetter` and `labelFont`, one for every label, localStorage, recommended
  `LABEL_REC` (0.6, 6, inter), set in Design's Label section (`labelLook`, `labelSet`; they left Print's plate options,
  Dols 2026-11-15). Colour role
  `labelText` ("Label text", default charcoal) in `R.ROLES`, painted like any other, no part of its own; the 3D view's
  canvas text takes it and the letter height. Not in the STL folders.

- Stack size (branch `claude/project-thread-mam5az`, Dols 2026-11-13): the stack header and the template cards give
  the outside size as it stands, drawers closed (`stackSize`): units' `bbox` placed by `stackLayout`, base, wheels,
  foot, casters (70 mm, a guess), roof and its handle, key locks, latches, hinges, column pieces, wall plates.
  `tools/placements/measure_envelope.py`; README "A stack's outside size". The level header still gives the module.

- Store links and affiliation (Hardware, "Where you buy"): Amazon.com keeps upstream's affiliate short links
  (`link.amazon/…`, Romy's tag inside; `SHOP`, the product each opens in a comment), at the user's request
  (2026-11-13). Every other store's search link takes this fork's tag from `SHOP_TAGS` (one per store, '' = no tag
  and no `tag=` parameter; `shopTag` never gives one to `com`).
  `SHOP_PAGES` (Dols, 2026-11-13): product pages for one store and one bolt finish instead of the search (Amazon.fr's M4
  button-head bolts: B0DCY82LTF black carbon steel, B0FQBX529T stainless), with that store's tag; the row says which
  length to pick on the page. Disclosure: under the store picker (`shopDisclosure`)
  and in About's "Store links" (`aboutShop`). Affiliate links get `rel="sponsored"`.
  First visit: `guessShop` takes the time zone's country first (`SHOP_TZ`: Europe/Paris → fr even with an en-US
  browser), then the browser's region unless it is on another continent than the time zone, then the continent. No IP
  lookup (it would send every visitor's IP to a third party).

- Visit count (Dols, 2026-11-13): GoatCounter account `dols` (https://dols.goatcounter.com), with **no script loaded**
  (the "no external scripts" rule holds): `count()` in `src/template.html` requests `/count` as an image, once per visit
  (page, referrer, screen width; GoatCounter works out the country) and once per store link opened in Hardware (event
  `buy/<store>`, title = the item: which Amazon stores deserve an Associates tag). Only on `doooools.github.io`, never
  with `navigator.webdriver` (Playwright, the video), nor after "Don't count this browser" in About (`noCount`).
  What is used (Dols, 2026-11-16, section "what is used" after it): `use(name)` sends an event at most once per visit;
  `USES` names the buttons by selector (a click capture listener), `use()` calls name the gestures with no button
  (undo, save, open, export, a drawer opened, paint in 3D, a shortcut through `useKey`), `useState` (in `renderTabs`)
  the step shown, the folder open, the printer and the store; errors as `error/line-<n>`. Never a name, a label text,
  a count of the person's parts or an id. A new button adds its rule to `USES`. Full list: `docs/ux-redesign.md`,
  "What is counted"; About's "Visit count" says it in short.

- Print: plate ticks select (Dols, 2026-11-13). A plate card's checkbox ticks it for the download (`plateSel`, kept for
  the page's life per print scope, not saved); the downloads (Bambu project, plate files, STL folders) hold the ticked
  plates (`target`), or every plate left when none is ticked. Marking printed is a button: the selected plate's "Mark as
  printed", or the bar above the sheet for every ticked plate. `printed` and `plateState` are unchanged.
  Since UX audit session 6 (branch `claude/print`): the right column shows the selected plate first, "Mark as printed"
  under its title, then the plate options as folded lines with their value (`popt`, open state kept in `openInfo`);
  the filter is one line of pills with plate counts; the selection bar shows only while a plate is ticked; the two
  exports sit side by side; Print's and Hardware's rails say "In the plates" / "In the list" / "Left out" (`railState`).

- Print: Already printed (Dols, 2026-11-14, branch `claude/project-thread-e6g0mi`). The rail's "Already printed" button
  (`printHave`) shows `havePanel` in place of the sheet: the parts on these plates (`haveLines`: the picked stacks'
  lines that fit), "Add" / "All N", and the list with steppers capped by `haveRoom`. Counts in localStorage `vpp.onHand`
  (progress key → pieces, `plainHave` on load), apart from `printed` so plates marked printed keep their own count.
  `have(k)` = printed + onHand is what `printProgress`, `planPlates` and `stablePlates` read: a change lays the plates
  out again (plates marked printed fold into the plan's `base`). Per part like `printed`; only up to the line's total
  counts; keys no line has (stack left out) stay, shown "Not on these plates". "Reset all progress" and the list's
  "Clear" empty it (undoable: `progSnap` holds it).

- Share links and codes (Dols, 2026-11-23, issue #84): section "share links and codes" before `renderStart`.
  `shareState` (the design file's JSON, `kind: 'share'`, no printer, no progress) → `shareCode` ("V1" + base64url of
  deflate-raw, "V0" plain without CompressionStream) → `#d=<code>`; `shareFrom` finds a code in a pasted link or code;
  `openShareCode` → `loadDesign(text, name, share = true)` (own confirm text, no `markFile`). `shareFromAddress` runs
  after the first render and on `hashchange`, and drops the hash. File menu: "Copy a share link", "Copy the share code",
  "Open a share link or code…" (`copyShare`, `openShare`).
- Right-click menus everywhere (Dols, 2026-11-23, section "right-click menus, everywhere" in `src/template.html`, before
  `segBtns`): one `contextmenu` listener on the document (it leaves alone a handler that called preventDefault: the
  3D view's canvas, a plate card). `ctxFind` walks from the element under the pointer up, matching the step's rules
  (`CTXV[view]`, rebuilt by `renderPrint` / `renderHardware` / `renderAssemble` with their closures, cleared at their
  start) then the page's (`ctxRule(name, selector, (el, ev) => menu)`); a menu with no item goes on to the next; none:
  `pageMenu()` (`ctxUndo`, `CTXP[view]()`, `ctxFile`, shortcuts). Helpers: `ctxJoin` (lists with a line between),
  `ctxMirror` (a block's buttons as items, `b._hold` set by `holdButton` for held ones), `ctxFolds`, `ctxSteps`,
  `linkMenu`, `railStackMenu`, `viewMenu`, `brushMenu`, `roleMenu`, `filamentMenu`, `dupStack` (also Stack settings'
  "Duplicate stack": the copy goes last). `menuOpen` items take `on` (a tick,
  `menuitemcheckbox`), `hold` (`holdButton` on the item) and `u` (the visit count's word for a label holding a name);
  the menu goes into the open modal `<dialog>` when there is one. Browser's menu kept on text fields (`ctxField`) and
  with Shift held at the right press (`ctxRight`); `ctxPress` tells a key (context menu key, Shift + F10: under the
  focus, first item focused) from a press. Counted `right-click/<rule name>`. Full list: `docs/ux-redesign.md`,
  "Right-click menus, everywhere".
- A plate's menu (Dols, 2026-11-23, issue #93): in `renderPrint`, `plateMenu(pl)` / `plateMenuAt` on a `.pcard[data-pn]`'s
  `contextmenu`, the `.psel` panel's and its "⋯" (`data-pmenu`, in `.ptags`); `menuOpen` as in Design. "Download this
  plate alone" is `makeDownload([pl], …)`, whatever is ticked.
- Print settings by part (Dols, 2026-11-23, issue #83): `PS_OPTS` / `PS_ROLES` / `partSet` (localStorage
  `partSettings`, design file `print.parts`, `plainPartSet`), next to `printAids`. `computeBuild` runs `partSetApply` on
  merge's copied lines: walls, infill, `pattern`, `shells`, supports ('off' also `noSupports`, written as supports off);
  the configurator's own values stay in `l.base`. `planFor` passes them; `buildProject` writes `sparse_infill_pattern`,
  `top_shell_layers` / `bottom_shell_layers`, `enable_support` 0; the plate files `fill_pattern`, `top_solid_layers`…
  The panel: `partsPanel` (Print's right column, `#pParts`, folds `ps-<role>` in `openInfo`).
- Module shells' supports (Dols, 2026-11-13): rules.js gives them `supports: 'shell'`, a named set in the page's
  `SUPPORT_SETS` (tree(auto), default style, threshold 80°, on build plate only, critical regions only, remove small
  overhangs), written per object into the Bambu project and the plate files (`supportKeys`; PrusaSlicer: organic, 80°,
  build plate only). A named set doesn't move a part onto the "supports" plates (only `supports: true` does).
  Plates keep 15 mm clear beyond each shell's top and bottom walls for those supports (`room` in the set, Dols
  2026-11-13): `roomOf` adds it on the footprint side that is the module's height (57 / 105 / 201 mm), less if the bed
  is too small; `insetOf` gives the part's place inside its box (brim + room) to the export and the plate drawing.
  Diagonal and as-exported shells (L 1F, L 2F) sit alone on their plate and get no room.

- Hardware in two side columns like Print (Dols, 2026-11-14): left rail "Hardware for" (stacks as buttons, `hwSkip`,
  `computeBuild(false, leaveOut)`) and the groups to jump to; right column "List options" (titled with the line count;
  store, bolt finish, head shapes); Copy and CSV under the title. The tab's count follows `hwSkip` too, and a click
  anywhere on a row but its store link ticks it (UX audit E1, E4, E5). UX audit session 7: short names on the lines,
  the finish and the store said once in pills under the title (`.hwsay`; Copy and CSV keep `hwItem`'s full name), the
  link says "Product page" or "Search" (the store goes in `data-store` for `countBuy`'s GoatCounter event), group
  headers "1 of 3 bought", the rail's "Jump to" as plain links (`.hwjumps`) (E2, E3, E6).

- One look everywhere (thread "Unifier l'interface de tout le planner", Dols 2026-11-13): orange fill = action, dark
  fill = selected, settings as segmented buttons (the stack's too, and the plate options), ticks only for list items,
  the same title and section sizes on every step, removing by press and hold (`holdButton`), a left rail on Print
  too, progress in every tab. Rules: `docs/ux-redesign.md`, "One look for each kind of thing".

- Stack colour (Dols, 2026-11-14): in Design, the stack picked in the rail and the inspector showing its Stack
  settings are blue (`--stack*` tokens, `.dinsp.istack` set by `stackInspector`, cleared by `renderInspector0`); a level's
  settings stay on the plain panel. Rule in `docs/ux-redesign.md`, "One look for each kind of thing".

- Theme switch (Dols, 2026-11-14): the header's Light / Dark segmented buttons (`data-themeset`, `setTheme`) put
  `data-theme` on `<html>` and save it in localStorage `vpp.theme`; a script in `<head>` sets it again before the first
  paint (no flash). With nothing saved the page follows the system and its changes. What JS copies from the CSS tokens
  (the 3D background, highlight and level outline) is redone by `v3.retheme`.

- Keyboard shortcuts (Dols, 2026-11-14, branch `claude/project-thread-ebiohf`): section "keyboard shortcuts" after the
  tabs in `src/template.html`: one `keydown` listener on the window in the capture phase (it sees Esc before the
  handlers that act on it), `keyDesign` for step 1, `KEYS` the list shown by `?` and the header's "Shortcuts" link
  (`#keys`, `keysPop`), `MOD` (⌘ on a Mac, else Ctrl). Rules and the full list: `docs/ux-redesign.md`, "Keyboard
  shortcuts". Bare keys never with Ctrl/Cmd/Alt (the browser's stay theirs; only Ctrl/Cmd + S / O are taken), never in a
  field, a menu (`menuNow`), a dialog, `fpOpen` or the printer list. A new shortcut goes in `KEYS`, in the menu item's
  `key` and in the button's `title` / `aria-keyshortcuts`; a removal by key is only "Remove level" (others are press
  and hold: ask Dols). Copy and paste (Ctrl/Cmd + C / V in Design, Dols 2026-11-14): `clip` (a level or a stack, deep
  copies, page's life), `copySel(t, i)` / `pasteClip(t, i)` (also in the level and stack menus); a pasted level goes
  through `levelTo` (the footprint per level, shared with `setFootprint`).

- Several levels selected (Dols, 2026-11-14, branch `claude/project-thread-jku6bd`): Ctrl/Cmd + click and Shift + click in
  the 3D view no longer open drawers (double-click, O, the menu do); with Select they pick levels of the stack shown
  (`selectLevels`: 'add', 'range', 'addRange'). `dsel.m = { l, a, s }` (last clicked, Shift's anchor, levels);
  `multiSel(t)` gives the levels only while `m.l === dsel.l` and drops a stale one, so any gesture that selects one
  level, the stack's settings or another stack ends it (the sites that set `dsel.l` also `delete dsel.m`); the load's
  sanitizer drops it, undo keeps it. `setLevels`, `selLevels`, `levelsName` ("Levels 1, 3 and 4"). `multiInspector`
  shows only the settings every module of every selected level has, with the options all can take; a value that
  differs: no button pressed and a "Mixed" pill; a change goes to every module (every drawer of a module holding
  several, for `R.INSIDE` keys) with `undoAs`, one Undo. `levelsOp` (up, down, dup, dupBelow, del), `openLevels`,
  `levelsMenu`; `keyDesign`, `copySel` and `pasteClip` (clip `lvs`: several levels) take the selection.
  `v3mark` outlines every selected level. Rules: `docs/ux-redesign.md`, "Several levels selected". Labels too (Dols, 2026-11-15):
  `multiInspector`'s "Labels" fold (`data-mlabel`): one text for every front of the selection (`fronts`: each drawer
  id of a module holding several, `'0'` else), drawn on `input`, saved on `blur` with `undoAs`, Esc restores `was`.

- Stack export (Dols, 2026-11-15, branch `claude/project-thread-cmlav7`): section "the stack in 3D, to a file" in
  `src/template.html` (before "opening and closing"). `exportItemsMenu` puts "Export as STL" / "Export as GLB, with
  colors" at the end of `stackMenu` and the File menu, greyed with `exportWhy`'s reason until the parts are in (no
  folder: never boxes). `exportItems` walks the scene: shown meshes with a `role` (not `own` helpers) and the labels'
  text planes, baked to the stack's frame (footprint centred), mirrored placements rewound, triangles of no area
  dropped. `stlOf`: binary, mm, Z up (x, -z, y), no labels. `glbOf`: hand-written glTF 2.0 (no exporter loaded), a
  node per part (`userData.file`, set in `loadParts`) under a node per unit, materials per colour (`v.mat` without the
  highlight), label PNGs, metres; checked with gltf-validator (0 errors) and imported in Blender 5.3 (bpy). The toast,
  the STL header and `asset.copyright` say the parts are USSA's, for one's own renders.

- Undo (UX audit 2026-11, session 1, branch `claude/undo`): section "undo" next to `store` in `src/template.html`.
  `save()`, `saveColors()`, `saveExtras()` and `saveSel()` call `undoNote()`; at the end of the task `undoCommit`
  compares `[towers, seq, colorPrefs, extras]` as JSON with the last state kept and, when it differs, pushes the state
  before (with `dsel`, `printSkip`, `hwSkip` as they were when the pointer went down or the key was pressed:
  `undoSettle`) on `undo.past` (50 entries, memory only). A handler names a gesture that overwrites or removes with
  `undoAs(label)` before changing anything: `toast(label, { label: 'Undo', fn })` shows it with a button for ~6 s
  (`.toast.act`); `undoAs(label, true)` also keeps Print's `printed` and `plateState` (Reset all progress, Clear).
  `undoApply` restores, writes through `store.set` and calls `renderAll()` with `undo.applying` set (renders that save
  don't make entries). Ctrl/Cmd + Z / Y / Shift + Z, not in `input`, `select`, `textarea`. `undoReset()` after the
  first render and in `loadDesign`. A new handler that saves through those four functions is undoable as it is; give it
  `undoAs` when it overwrites or removes. The "USSA render" preset's `confirm()` went (the audit's C6).

- Later Vault deliveries (Dols, 2026-11-24, "Corriger, garder les deux livraisons"): USSA's download of 2026-11-18
  re-exported 41 of the files the page reads elsewhere in their scene (often turned) and renamed a few (M 1F modules and
  fronts `_Sustainer`, XL heavyweight roofs "Heawyweight Roof (Cut to fit on a plate)", XL6/XL7 Box 1F Part 1 ↔ Part 2
  swapped). Every measurement stays on the first download (2026-10-21): `src/stl-revisions.json` (made by
  `tools/placements/revisions.py`, embedded by `build.py` as `window.VAULT_REVISIONS`) gives per first-delivery path the
  later file (`file` when `findFile` wouldn't find it, its `size`) and `fix` (3x4, that file → first delivery). The
  page's `partFile(map, path)` picks the file (a revision's own file of its size first, else the one `findFile` finds)
  and `reviseStl` moves its triangles as it is read, for `partMesh` (fix in the cache key) and Print's `placedMesh`;
  the STL folders download keeps USSA's bytes. A file of another size is read as it is, so both downloads work.
  New parts of that delivery ("Box … Upd", handles in parts…) aren't offered yet. README "Later deliveries".

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
- Stacks, colours, loose parts and the selection are rebuilt on every load and on opening a design file
  (`plainTowers`, `plainColors`, `plainExtras`, `plainData` near `clean`): a design file is anyone's JSON and once put
  HTML into the page (PR #50). A unit's or stack's string survives only as a plain word (`SAFE_STR`: letters, digits,
  `.,:#+-/()²` and spaces), keys likewise; names are free text, escaped where shown. A new saved field that needs other
  characters needs its own rule there, or it is dropped on the next load.
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
