# UX redesign brief

Mockups (interactive, press Play): private link, in `CLAUDE.local.md` (not committed).
Approved by the user on 2026-11-11. Talk to the user in French. Work on `feat/3d-stack-viewer` or a branch off it; commit only when asked.

This brief replaces the UI described in steps 2 and 3 of `docs/colors-3d-redesign.md` (Colors panel, 3D toolbar). Step 1 of that brief (the single filament picker) stays valid as the "Add a filament" catalogue.

## Artboards

| Artboard | File in the canvas | What it shows |
|---|---|---|
| 0 · First launch | `Start.dc.html` | Printer, Vault folder, first stack |
| 1 · Design | `Main.dc.html` | Stacks rail, stack view, inspector of the selected level |
| 1b · Design, Paint tool | `Colors.dc.html` | Filaments as brushes, part list, catalogue |
| 1c · Design, footprint and wide levels | `Wide.dc.html` | Footprint strip, "Across the width" |
| 1d · Design, loose parts | `Loose.dc.html` | Parts outside any stack |
| 2 · Print | `Print.dc.html` | Plate sheet with nesting, selected plate, Printed group |
| 2b · Print, plate options and export states | `PrintStates.dc.html` | Options menu, other printers, folder and fit errors |
| 3 · Hardware | `Hardware.dc.html` | One shopping list |
| 4 · Assemble | `Assemble.dc.html` | One section at a time, cases included |
| Dark variants | `*Dark.dc.html` | The same screens with the dark tokens |

In the mockups the stack is a flat CSS drawing. It stands in for the real three.js view (`open3d`, `v3sync`): keep the real view, with the behaviours below.
Figures in the mockups (plates, grams, hardware, steps, nesting) were read from the current page for two presets, "Rolling tool cart" and "Small-parts stack", on a P1S.

## Problems with what is there now (src/template.html)

- Step 1 holds two objects: a draft unit in the settings column (`c`, `renderUnit`, `renderControls`) and the stacks further down. Hence the destination menu (`currentDest`), the ghost in 3D (`v.ghost`), the "Preview" toggle and the "Won't sit on…" errors (`stackProblem`, `stackMatch`).
- Step 1 is one page of about 6,700 px with ten blocks, and 148 visible controls before anything is built.
- Colours expose the Bambu project's logic: a 14 role × N slot matrix, slots numbered 1, 3, 4. Step 2 has its own plate colour modes (`plateColors`) on top.
- The shopping list sits under all the plates in step 2 (`hwTable` at the end of `renderPrint`); step 3 has no consolidated list.
- Step 2 mixes progress, plate settings, export and a wall of open plate cards.
- The Vault folder is asked for in three places; the header still carries upstream's links.

## Target model

A **stack** owns what is the same for all its levels or exists once:
- footprint: width (S, M, L, XL) and depth (x3 to x7);
- roof, and the top handle of a grid roof;
- base, wheels, foot bar, pull-out handle, stationary handle.

A **level** is what sits across the width at one height:
- on S and M: one module;
- on L: one L module, or one L² module (one shell, two drawers side by side), or two S modules side by side;
- on XL: one XL module (1F only), or one XL² module (1F only, an S and an M drawer in one shell), or an S and an M module side by side.

A **module** has: type (drawer or case), shell height (1F, 2F, 4F), the drawers inside it (see "Drawers per module"), and its options (inside, lock, geared rails, print aid, wall mount, pegboard). Options apply to every drawer of the module.

Storage can stay `towers[].levels[][]`:
- the footprint setter writes `w` and `d` on every unit of the stack;
- the roof stays on the top unit as today (`roofOf`), but is edited in the stack's settings and follows when levels are reordered;
- a unit gains a list of drawer heights, top to bottom, that add up to its shell height. A missing list means one drawer of the shell's height.

There is no draft unit any more. Remove `currentDest`, the Add destination menu, the ghost and the "Preview" toggle. `stackProblem` and `stackMatch` become unnecessary for width and depth, since a stack cannot hold mixed footprints.

## Decisions taken with the user

- **Saved builds**: convert automatically on first load (roof and footprint to the stack, one drawer per module). Keep stacks, colours, printed plates and plate numbers.
- **Backbones**: ticking a handle adds a backbone to every 1F and 2F module of the stack. Backbones do not exist in 4F: show an alert on the stack naming the 4F module that has none.
- **Sizes that do not fit the printer**: never offered. On a P1S this leaves S and M in x3 to x5 (today the page flags L, L², XL, XL², x6 and x7 there). A level added before a change of printer may stop fitting: keep it, and show the alert drawn in `PrintStates.dc.html` and on the level. The "Only show what fits" switch (`onlyFits`) goes away.
- **Plate colour modes** of step 2 (`plateColors`: "Like the renders", "Big & small", "One color"): removed. Plates always follow the colours of Design. "Two-tone" and "One color" remain as colour presets (`applyColorPreset`).
- **Painting a role "everywhere"** clears the per-module colours for that role.
- **Colour exceptions** are per module, not per drawer: in a module with several drawers, all fronts change together.
- **Theme**: follows the system setting, as today (`prefers-color-scheme`). No switch.
- **Phones**: not a target. Do not spend time on touch layouts.
- **Branding**: one credit line "A fork of Romy's Vault Print Planner" linking to the original. Remove the Ko-fi and YouTube buttons. The store links must stop being upstream's affiliate links (see "Open points"); the "As an Amazon Associate…" line goes with them. (Changed 2026-11-13 at the user's request: Amazon.com links are upstream's affiliate links again, other stores take the fork's own tags; see CLAUDE.md.)
- **Opening drawers and cases**: no "Drawers" tool. Ctrl + click, Shift + click or Cmd + click on a drawer or a case opens or closes it, in both tools. A plain click selects (Select tool) or paints (Paint tool).

## Drawers per module

Today `drawerInsert` (rules.js) adds one box and one front of the module's height. The redesign lets a shell hold several drawers:
- 2F shell: one 2F drawer, or two 1F;
- 4F shell: one 4F, two 2F, four 1F, or one 2F with two 1F (the 2F at the top, in the middle or at the bottom).

What USSA's manuals say (folder `261021_VAULT_USSA_S`):
- Drawer Assembly 4/8: geared rails go "into a box", and "you should use them for extra locking force, or if you are using more than one box per 2F or 4F module". So several boxes per module is supported, rails are one pair per box, and they should default to on when a module holds more than one drawer.
- Drawer Assembly 8/8: the latch is pushed into the underside of the module. Count it per module (S and M one, L and XL two, as measured), whatever the number of drawers. Today it is counted inside `drawerInsert`, per insert: move it.
- Instructions Manual, "S, M, L, XL – 50 Size Variants": "no 3F to avoid gaps, everything divides by 2". The mixed layouts (2F + 1F + 1F) are not shown anywhere: mark them `inferred`, like the L² contents.

Counts that follow:
- per module, unchanged: shell, runner guides, runner slides and stoppers (already a pair per 48 mm level), latch;
- per drawer: box and front of the drawer's height, key lock and key cap (or hidden key), springs, label, front bolts and facade caps from `frontBolts(w, h)`, geared rails, interior.

`validate.js` must cover the new layouts. The 3D view needs placements for a 1F or 2F box at each level of a taller shell: `stl-placements.json` has none. The user chose to **measure them with the Blender tooling** (`tools/placements/`) before the feature is switched on, not to compute offsets.

## Screens

### Header (all screens)
Logo and name, the four steps (Design, Print, Hardware, Assemble), then two buttons: the printer (name and bed size, opens the printer picker with the custom bed fields of `renderPrinter`) and the Vault folder (file count when connected, "Choose…" when not). The folder is asked for here and in the first launch only: remove `renderFolderHero`, `unitFolderBar` and step 2's folder row.

### 0 · First launch
Shown when there is no stack. Three rows: printer, Vault folder (same text and "Later: plan without the files" as today), first stack (empty, or one of the presets of `presetsBlock`, filtered by `presetFits`). Print, Hardware and Assemble are disabled until a stack exists.

### 1 · Design
- Left rail: one card per stack (width letter, name, footprint, level count), "New stack", "Start from a template…", then "Loose parts".
- Centre: the 3D view of the selected stack, always shown. Tools "Select" and "Paint"; views Front, ¾, Side; "Add a level on top"; a "Stack settings" button; a "Footprint" button that opens a strip under the toolbar (width and depth as segmented controls, applied to all levels).
- Under the view: a colour summary of five chips (shell and roof, fronts, drawer boxes, mechanics, accents) that opens the Paint tool.
- Right: the inspector.
  - A level selected: position ("Level 3 of 4"), move up, move down, duplicate, remove; type; module height; "Across the width" on L and XL stacks; "Drawers in this module" for 2F and 4F drawers, as small diagrams; inside; lock; geared rails; "More options" (print aid, wall mount, pegboard); "Parts and bolts of this level" (the part list and hardware that `unitSum` folds today).
  - The stack selected: name, footprint, roof (None, Grid, Table, Bowl, Under-table, Heavyweight where it exists), base with wheels and foot bar under it, the two handles, then the stack's alerts (`analyzeTower`) or "Everything in this stack fits together".
- With two modules side by side (S + S, S + M) each module is selected and set up on its own; with L² or XL² both drawers share the module's settings.

### 1b · Paint tool
Replaces `colorsPanel`, the brush bar of `v3tools` and the "Selected" card's colour actions.
- "Your filaments": one card per palette colour, which is also the brush. It shows how many part types use it. A small cross removes it, with today's behaviour (`data-pal-del`): parts go back to their role's colour, per-module colours using it are dropped, the last filament cannot be removed. TPU is fixed, for the tires.
- "Add a filament" opens the Bambu catalogue (`bambu-colors.tsv`, line filters, own colour) under the view. A click adds the colour and takes it as the brush.
- The 14 roles of `R.ROLES`, grouped as today (`ROLE_GROUPS`), one swatch per line. A click paints the line with the brush; "Paint all" paints the group.
- In the view, a click paints the clicked part's role. A switch says what the click covers: "Same part everywhere" or "Only this module" (writes the unit's `cfg.colors`, as `v3owner` decides today).
- "Modules with their own color" lists the exceptions, each with "Back to the project color".
- Slot numbers are not shown here. `trayUse` and `buildProject` keep assigning them for the export.

### 1d · Loose parts
Today's "Extra parts" (`extrasPanel`), as an entry of the rail: search among the 733 parts, quantity steppers, "Print only these" (`printScope`), "Clear".

### 2 · Print
- Top: progress (parts, plates left, grams), and one export button. On a Bambu printer "Download the Bambu Studio project" (`buildProject`); otherwise "Download the plate files" (`buildPlateFiles`). "STL folders (.zip)" (`buildFolders`) and "Plate options…" sit next to it.
- Filament chips (all, one per filament, Printed) filter the sheet. Each shows its plate count and weight.
- The plate sheet: one small card per plate with its nesting (`plateSvg` data: bed, no-print corner, parts, front edge), its number, part count, grams, a checkbox that ticks it for the download, and "Up next" on the first unprinted plate. Grouped by filament.
- Ticked plates (Dols, 2026-11-13): a bar above the sheet counts them; the Bambu project and the STL folders hold only them (every plate left when none is ticked), and its "Mark as printed" / "Put back on the list" acts on them all. A tick never marks a plate printed.
- Printed plates leave their filament group and move to a "Printed" group at the end, dimmed. "Printed. Undo" (or ticking it and "Put back on the list") puts it back. Plate numbers never change (`stablePlates`).
- The selected plate, on the right: large nesting with numbered parts, the numbered part list with file name and settings (walls, supports), "Mark as printed" (then selects the next unprinted plate), previous and next.
- "Plate options…": "Fewer plates" (`mixSupports`), "Labels on their own plate" (`labelsApart`), and the folded "How plates are laid out" text.
- States in `PrintStates.dc.html`: printer without a Bambu preset, folder not chosen, parts missing from the folder (today's "not found in" errors, shown before the download starts), parts that no longer fit after a change of printer.

### 3 · Hardware
A step of its own, fed by the same data as `hwTable` for the whole build.
- Lines grouped by what is bought: M4 bolts, M6 bolts and inserts, axle rods and bearings.
- Per line: a "bought" checkbox, quantity, head shape drawing, name, spare note, what it is for, which stack, store link.
- Side: "Copy the list", "Export as CSV", "Include spares", and the head shape legend.

### 4 · Assemble
`GUIDE` and `stepsDone` as today, shown one section at a time.
- Left: the sections the build needs, each with its progress and the stack it concerns.
- Centre: the steps of the selected section, with a checkbox, the printed parts, the hardware and the manual page.
- Sections repeated per unit (drawers, cases) get a counter: "Drawer 1 of 8", and a button "Drawer done, next one" that clears the ticks and counts one more.
- Right: the hardware this section needs, with a link to Hardware.
- Step texts can use the build: "Cut the M16 rod to 338 mm, the length for an M base" instead of listing the four lengths.
- Cases keep the "Inferred order" badge and its note.

## Colours and theme

Keep the page's tokens and its dark theme. Two additions:
- buttons with white text use `#c2511c` in the light theme: white on the current `--accent` (`#d9622b`) is under 4.5:1. `--accent` stays for outlines and marks;
- a raised surface for selected cards: `#ffffff` light, `#2b3031` dark.

Parts and filament swatches keep their real colour in both themes.

## One look for each kind of thing (Dols, 2026-11-13)

The pass of thread "Unifier l'interface de tout le planner" set these rules for every step, popup and panel:
- **Buttons**: a filled orange button (`.btn.primary`, `--accent-btn`) does the screen's main action (Add a level on
  top, Empty stack, Download, Mark as printed, Copy the list, Drawer done). Dark fill (`--ink`) only ever means
  *selected*: tabs, segmented buttons, toggles of the 3D toolbar. There is no dark action button (`.btn.ink` is gone).
- **Controls**: a setting is a row of segmented buttons (`.seg`: `useg`/`ubool` for a module, `sbool` for the stack,
  `pbool` for plate options), with sublabels in `<small>`. A dropdown only where the choices don't fit (printers,
  stores). A tick box marks an item of a list (plates, hardware bought, assembly steps, stacks to print). Two
  checkboxes are left for Dols to decide: "Close against the walls", "Gridfinity baseplate inside".
- **Headings**: each step's main title is 28 px display (`.dtitle`, `.ptop-prog`, `.hwtitle`, `.asm-title`, `.xtitle`);
  a side panel has an eyebrow saying what it is (`.v3-sec`: Stack settings, Level 2 of 4, Colors, Selected plate)
  over a 22 px title naming which one. Inside a panel: sections (`.isec`, bold, with a hint and a rule above), then field
  labels (`.field > .lbl`, small capitals). The stack's sections: Size and roof, Under the stack, Back of the stack;
  the level's: Module, Front and inside, Back of the stack.
- **Type**: the mono font for figures (sizes, counts, grams), never for names or sentences.
- **Words**: "Remove" (not "Delete") for stacks, levels and filaments.

## Steps, each testable on its own

1. **Hardware**: new tab, list moved out of step 2, bought ticks, copy and CSV. Branding changes in the header.
2. **Print**: plate sheet with nesting, selected plate, Printed group, single export button, plate options menu, export states. Remove `plateColors`.
3. **Assemble**: section rail, per-unit counter, section hardware.
4. **Design model**: stack-level footprint and roof, level inspector, no draft unit, migration of saved builds, first launch, hide what does not fit, backbones from the handles.
5. **Wide levels and loose parts**: "Across the width", footprint strip, loose parts in the rail.
6. **Paint tool**: filaments as brushes, role list, catalogue under the view, exceptions list, Ctrl/Shift click to open.
7. **Drawers per module**: rules, `validate.js`, hardware and assembly counts, then placements measured with Blender, then the 3D view.

Steps 1 to 3 do not depend on the new Design model and can ship first.

## Keep

- The hard rules in CLAUDE.md: one HTML file, three.js only when the 3D view is shown, no USSA geometry in the repository, rebuild after any change in `src/` and check the page.
- `paintLines`, plate grouping, filament totals and the Bambu project keep following the colour choices.
- A build with no colour choices and one drawer per module must plan exactly as before: same files, same counts, same plates.
- Test with real files in Chrome or Firefox (Claude's built-in browser cannot pick a folder).

## Open points

- Store links: the table near l.1507 of `src/template.html` holds upstream's affiliate short links (`link.amazon/…`). There is no tag to strip. Either replace each with the plain product page or drop the links: ask the user which.
- Roof on a pair of side-by-side modules, and the heavyweight roofs' limits by width: keep today's rules (`roofOf`, `normalize`), nothing was redesigned.
- ~~On XL, a level taller than 1F has to become S + M side by side.~~ Settled by the files (2026-11-12): every XL and
  XL² piece exists in 1F only (drawer module, box, front, case body, case front, backbone, wall mount, pegboard
  attachments; there is no XL 2F or 4F file anywhere in the download), so an XL width taller than 1F can only be an S
  and an M side by side, the same height. The page does that: an XL or XL² level set to 2F or 4F becomes S + M with
  the unit's options, and says so (toast); "Across the width" back to XL or XL² makes the level 1F again.
- The mockups do not show the picker for a custom bed size, nor the "What's new" dialog: keep them as they are.

## Later (not now)

- Assemble: a short animated GIF for each action (a drawer slid in, a latch fitted, a bolt driven), next to its step. Asked by the user on 2026-11-11; not started.
