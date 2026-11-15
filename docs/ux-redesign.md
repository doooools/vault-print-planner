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
- Colours expose the Bambu project's logic: a role × N slot matrix, slots numbered 1, 3, 4. Step 2 has its own plate colour modes (`plateColors`) on top.
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
- **Theme**: follows the system setting (`prefers-color-scheme`) until the header's Light / Dark buttons are used;
  then the theme picked stays, saved in the browser (changed 2026-11-14 at the user's request; it was "No switch").
- **Phones**: not a target. Do not spend time on touch layouts.
- **Branding**: one credit line "A fork of Romy's Vault Print Planner" linking to the original. Remove the Ko-fi and YouTube buttons. The store links must stop being upstream's affiliate links (see "Open points"); the "As an Amazon Associate…" line goes with them. (Changed 2026-11-13 at the user's request: Amazon.com links are upstream's affiliate links again, other stores take the fork's own tags; see CLAUDE.md.)
- **Opening drawers and cases**: no "Drawers" tool. A double-click on a drawer or a case opens or closes it, in both tools, and so do O and the level's menu. A plain click selects (Select tool) or paints (Paint tool). (Ctrl / Shift / Cmd + click opened them until 2026-11-14; they now select several levels, see "Several levels selected".)
- **Several levels selected** (Dols, 2026-11-14): with Select, Ctrl + click (Cmd on a Mac) on a level in the 3D view adds it to the selection or takes it out, Shift + click selects the levels from the anchor (the last one clicked alone or with Ctrl) to it, Ctrl + Shift + click adds that range. Levels of the stack shown only (the view shows one stack). In Paint a click with Ctrl or Shift paints as a plain one. Each selected level is outlined in the view. The panel (`multiInspector`) says "3 levels of 5 selected", "Levels 1, 3 and 4", the modules, parts and grams together, the levels as small buttons (top first; one picks that level alone) and one line on what it does; then only the settings every module of every selected level has (Module: across the width, type, height; Inside or Drawers: the layout, inside, cut-outs, divider height, at a wall, lock, geared rails for drawers, every drawer of a module holding several; body style and floor for cases; Back: wall mount, pegboard, backbone), each offering only the options every one of them can take. Drawers mixed with cases share the Module and Back sections only. A setting set differently on them has no button pressed and a grey "Mixed" pill beside its name (the fold's summary says "mixed heights", "mixed locks"…). A change goes to every module of every selected level at once and says so with "Undo" ("Lock: Key lock, levels 1, 3 and 4 · Undo"): one Undo takes it all back. What is set per drawer box, per front or per module (divider plans, the fronts' labels, the drawer tabs, one side of a pair) stays in the one-level panel, as the panel's line says; copies made with D, Shift + D or Ctrl/Cmd + V keep their labels, as one level's do. The "⋯" and a right-click on one of the selected levels open their menu: Open / Close their drawers and cases (O), Add copies of the N above (D) / below (Shift + D: the copies are then selected), Copy N levels, Paste above the top one, Move up / down (each one step, Alt + ↑ ↓), Remove N levels (one click, Delete, "Levels 1, 3 and 4 removed · Undo"). Ctrl/Cmd + C copies them all and Ctrl/Cmd + V pastes them all, the pasted levels then selected. A plain click, ↑ ↓, Esc, the level panel's buttons or another stack go back to one level (or none). Not kept over a reload.

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
Logo and name, the four steps (Design, Print, Hardware, Assemble), then "File", the Light / Dark buttons, the printer (name and bed size, opens the printer picker with the custom bed fields of `renderPrinter`), the Vault folder (file count when connected, "Choose…" when not) and "Support me" (Ko-fi; the cup alone from 1240 to 1599 px). The folder is asked for here and in the first launch only: remove `renderFolderHero`, `unitFolderBar` and step 2's folder row.
One row from 1420 px, so at 1440 (UX audit A10, 2026-11-14); below, the buttons go on a second row. Under the name, two small links, "What's new" and "Report a bug or an idea" (Dols, 2026-11-14: back at the top after session 8 had put them in the footer). They are not file actions, so they stay out of "File", and as a second line under the name they take no width of their own on the row (12 px, no wider than the name). The fork's credit to Romy's planner is the first section of What's new, "About this fork" (framed): who made the original, its link and its MIT licence, what the fork adds, and that Amazon.com links stay Romy's affiliate links. The footer has no credit line any more; its "Store links" still names Romy's original planner, and the page's source starts with the upstream MIT notice.
- **File** (UX audit A9, session 8): a menu on every step, the same `role="menu"` list as the 3D view's. Its head: "Design file", the file's name (the last one saved or opened, "Not saved to a file yet" before), and how it stands: "Kept in this browser. The file has every change." / "… The file is 3 changes behind." Then Save (where it goes on the right: "in the Vault folder", "to downloads"), Save as…, Open…. Design's rail no longer has a "Design file" group; the first launch keeps "Open a saved design…".
- **Tab counters** (UX audit A10): none on Design; Print in % printed; Hardware "11 to buy" (lines not ticked, following Hardware's rail); Assemble in % assembled.

### 0 · First launch
Shown when there is no stack. Three rows: printer, Vault folder (same text and "Later: plan without the files" as today), first stack (empty, or one of the presets of `presetsBlock`, filtered by `presetFits`). Print, Hardware and Assemble are disabled until a stack exists.

### 1 · Design
- Left rail: one card per stack (width letter, name, footprint, level count), "New stack", "Start from a template…", then "Loose parts", an entry like the stacks (solid border, "spares, single parts", its part count or "none yet" on the right; UX audit A9). Print's "Already printed" has the same look.
- Centre: the 3D view of the selected stack, always shown. Toolbar: tools "Select" and "Paint", then "Spread levels", "Hide roof", "Bolts" (two swatches, raw steel or zinc / stainless, the same setting as Hardware's "Bolt finish") and "?" (how to move the view: drag, scroll, right-drag). Over the view's header: the stack's name as the big title, with a pencil button that turns it into the name field (Enter or leaving the field keeps it, Esc puts it back; UX audit B3); "Add a level on top" (`title` "Adds a level like the top one"); a "Stack settings" button, which opens them and does not toggle (A8). No "Footprint" button nor strip (UX audit A8, B2, 2026-11-14): width and depth are in Stack settings.
- In the view (UX audit 2026-11, session 3): with Select, the level under the pointer is outlined and named beside it ("Level 3 · M5 · 1F drawer", "Click to set it up · right-click for actions"). A right-click on a level (let go less than 5 px from where it was pressed; a right-drag still pans) selects it and opens its menu: Open or Close drawer / case (the drawer under the pointer in a module holding several), Add a level above, Add a level below (copies of the level), Move up, Move down, Remove level (a plain click, then "Level 3 removed · Undo"). A right-click on the background, the roof or the base opens the stack's: Fit the stack in the view, Add a level on top, Stack settings. Both are `role="menu"` lists (arrow keys, Home, End, Enter, Esc) that close on a click outside, a scroll or the camera moving. The hint under the view is one line: "Click a level to set it up · right-click for its actions · double-click opens a drawer"; the first-visit tip about opening a drawer stays. Double-click keeps opening drawers and cases (Ctrl / Shift + click did too until 2026-11-14: they now select several levels). The hint reads "Click a level to set it up · Ctrl+click for several · right-click for actions · double-click opens a drawer", the label beside a level "Click to set it up · Ctrl+click to select several · right-click for actions".
- The "Paint" tool button carries the stack's filaments as small swatches (up to four, then "+N"; the names in its `title`), so the toolbar says where colours are set (UX audit C7, 2026-11-14).
- Right: the inspector.
  - Both panels are cut into foldable sections (UX audit A7, 2026-11-14): each header gives the section's name and, on the right, what is set in a few words ("Drawer · 1F", "Empty · key lock · geared rails", "nothing on the back", "18 parts · ≈ 570 g"). A section stays open or folded as the user left it, for the page's life.
  - A level selected: position ("Level 3 of 4"), then "Level below" and "Level above" (they move the selection) and "⋯", which opens the level's menu under itself, the same as the right-click (level actions are in that menu, not in the panel's header; "Duplicate" went, "Add a level above" does it). Sections: **Module** (open: "Across the width" on L and XL stacks, type, module height), **Inside** (open; named **Drawers** when the module can hold several: "Drawers in this module" as small diagrams, inside, lock, geared rails, or a case's body and floor), **Back of this module** (folded: wall mount, pegboard, backbone), **Parts and bolts** (folded: the part list and hardware). A new case starts with its floor "Empty" (UX audit X3, decided 2026-11-14).
  - Labels (Dols, 2026-11-14): the first field of **Inside** / **Drawers** is "Label", a text field ("on the drawer front", "on the case front", "on this drawer's front"; placeholder "e.g. M6 bolts", 24 characters). It is each front's own: in a module holding several drawers it sits in the drawer's frame. The text shows on the Label part in the 3D view as it is typed (dark letters on a light label, light on a dark one), opens the section's summary in quotes ("“M6 bolts” · Empty · key lock"), replaces a drawer tab's second line, and is named under the level in the view's hover tip. It is saved, as one Undo step, when the field is left or Enter pressed; Esc puts the text back. Copies of a level (Add a level above / below, copy and paste) keep their labels; "Add a level on top" starts without. A new piece of free text: escaped wherever it is shown.
  - Several drawers in one module (UX audit X4): one tab per drawer ("Top", "2F · dividers", or its label in quotes) over a frame holding what is the drawer's own (label, inside, baseplate and divider settings, lock, geared rails) and, at its foot, "Same settings in every drawer". Under it: "In the frame: this drawer only. Outside it: the whole module." A click on a drawer in the view picks its tab too.
  - The stack selected: name as plain text (it is renamed at the centre) and a button to the top level, the stack's alerts (`stackAlerts`) or "Everything in this stack fits together" at the top, each alert that names a level with a "Show level N" link (UX audit B1). Sections: **Size and roof** (open: width and depth as segmented buttons, "For every level. Sizes too big for the <printer> aren't offered.", roof — None, Grid, Table, Bowl, Under-table, Heavyweight where it exists — and the grid roof's carry handle), **Under the stack** (folded: base, wheels, casters, foot bar), **Back of the stack** (folded: the two handles, the handle lock, module connectors). An option that needs another stays in place, greyed, its reason on the right of its name: Wheels and Casters "needs a base" (Casters "not with wheels"), Foot bar "needs wheels", Handle lock "needs the trolley handle", Carry handle "needs the grid roof" (UX audit B4); sizes the printer can't make stay hidden. A new empty stack opens on its settings, like a template (B6).
  - A stack that needs attention shows a dot on its letter badge in the rail.
- With two modules side by side (S + S, S + M) each module is selected and set up on its own; with L² or XL² both drawers share the module's settings.

### 1b · Paint tool
Replaces `colorsPanel`, the brush bar of `v3tools` and the "Selected" card's colour actions. Reworked by UX audit session 5 (2026-11-14, mockups `5-design-paint.png` and `6-details.png` column 3).
- **One rule: the Paint tool shows Colors** in the right panel (C1). Picking a stack in the rail, "Stack settings" or the background menu's "Stack settings" goes back to Select, and the panel then shows what was asked for. There is no "Paint is on in the view · Show the colors" strip any more. While painting, "Stack settings" is not shown pressed.
- **Brush bar** under the stack, in the view (C3): "Brush", one swatch button per filament (its name in `title` and `aria-label`; the brush in use is wider and says its name, without its Bambu line), a dashed "+" that opens the catalogue; on the right "A click paints" and "Whole stack" / "This module only". A click in the view paints the clicked part's role, for the whole stack or only that module (UX audit C2; writes the unit's `cfg.colors`, as `v3owner` decides). A double-click still opens a drawer, to paint its box.
- **Colors panel** (C5): "Colors", the stack's name, one line of help ("Pick a brush under the view, then click a part there or a line here…"), "Start from" (USSA render, Two-tone, One color). Then the roles of `R.ROLES` in foldable groups (`ROLE_GROUPS`: Outside open at first, Inside, Mechanics, Other), each header with the group's colours as swatches and "N part types"; inside, "Paint these N <brush>" and one line per role (a click paints it with the brush). Then "Modules with their own color" (open, with its count), each with "Back to the stack color". Then "Your filaments", folded ("N in use · add, remove"): one card per palette colour, which is also the brush, with how many part types and modules use it; a small cross removes it with press and hold (parts go back to their role's colour, per-module colours using it are dropped, the last filament cannot be removed), and "Add a filament". TPU is fixed, for the tires.
- **The catalogue opens in the right panel**, in place of Colors (C4): "‹ Colors" to go back, "Add a filament", the Bambu catalogue (`bambu-colors.tsv`: search, line filters, swatches by shade), the colour picked with its line and code, "Add it and paint with it" (a colour already in your filaments: "Paint with it"), "Your own color…". Nothing opens under the view any more.
- Every stroke, part type, group, preset, filament removed and "Back to the stack color" says what it did, with "Undo" (C5, C6).
- The filament's cross shows its press-and-hold progress as the stack cross does, a ring that fills (Dols, 2026-11-14: with a mouse the red fill didn't show over its red hover).
- Slot numbers are not shown here. `trayUse` and `buildProject` keep assigning them for the export.

### 1d · Loose parts
Today's "Extra parts" (`extrasPanel`), as an entry of the rail: search among the 733 parts, quantity steppers, "Print only these" (`printScope`), "Clear".

### 2 · Print
- Top: progress (parts, plates left, grams) of the stacks picked in the rail, and one export button. Parts that no longer fit the printer are on no plate and in none of these figures; the warning about them counts pieces (UX audit D8). On a Bambu printer "Download the Bambu Studio project" (`buildProject`); otherwise "Download the plate files" (`buildPlateFiles`). "STL folders (.zip)" (`buildFolders`) sits beside it, "for any other slicer" under its name (UX audit D5).
- Filter pills on one line (All, one per filament, Printed) filter the sheet. Each shows its plate count only; the
  weight and "N left" are in each group's header (UX audit D2). A pill names the colour without its line ("Cobalt
  Blue") unless two colours share that name.
- The plate sheet: one small card per plate with its nesting (`plateSvg` data: bed, no-print corner, parts, front edge), its number, part count, grams, a checkbox that ticks it for the download, and "Up next" on the first unprinted plate. Grouped by filament.
- Ticked plates (Dols, 2026-11-13): a bar above the sheet counts them, shown only while a plate is ticked (UX audit D3,
  D4: the card's two targets say what they do in their `title`, "Show this plate" and "Tick it for the download"); the Bambu project and the STL folders hold only them (every plate left when none is ticked), and its "Mark as printed" / "Put back on the list" acts on them all. A tick never marks a plate printed.
- Printed plates leave their filament group and move to a "Printed" group at the end, dimmed. "Printed. Undo" (or ticking it and "Put back on the list") puts it back. Plate numbers never change (`stablePlates`).
- The selected plate, at the top of the right column (UX audit D1): its title with previous and next, "Mark as printed"
  right under it (then selects the next unprinted plate), its tags, the large nesting with numbered parts, the numbered
  part list with file name and settings (walls, supports).
- Plate options, under the selected plate in the right column (Dols, 2026-11-14, "double bandeau" like Design: a rail on the left, a column of settings on the right), always shown: one folded line per setting with its value (`popt`: "Parts with supports · plates of their own"), which opens on its segmented buttons: "Parts with supports" (`mixSupports`), "Manual supports" (`printAids`), "Labels" (`labelsApart`); then the folded "How plates are laid out" text and "Reset all progress" on one row (no clear button since UX audit D7). It was a "Plate options…" popover before.
- Already printed (Dols, 2026-11-14): under the rail's stacks, a dashed button "Already printed" (like Design's
  "Loose parts") shows, in place of the filters and the sheet, a list of parts printed before: search among the parts
  on these plates only (the picked stacks' lines that fit the printer), "Add" or "All N" on each, then "Your parts
  already printed" with a stepper per part (no more than the plates need), "Back to the plates" and "Clear" (press and
  hold, with "Undo"). They count as printed and come off the plates, which are laid out again without them. Kept per
  part like the plates' progress (`onHand`, apart from `printed`); "Reset all progress" clears them too.
- States in `PrintStates.dc.html`: printer without a Bambu preset, folder not chosen, parts missing from the folder (today's "not found in" errors, shown before the download starts), parts that no longer fit after a change of printer.

### 3 · Hardware
A step of its own, fed by the same data as `hwTable` for the whole build.
- Lines grouped by what is bought: M4 bolts, M6 bolts and inserts, axle rods and bearings.
- Per line: a "bought" checkbox, quantity, head shape drawing, name, spare note, what it is for, which stack, store link. A click anywhere on the line ticks it, the store link excepted (UX audit E1).
- What holds for every line is said once, in two pills under the title: the bolt finish ("Every bolt and rod:
  zinc-plated or stainless") and the store ("Links open Amazon.fr"). Names on the lines are short, without the
  finish; Copy and CSV keep the full name (UX audit E2). The store link says what it opens, "Product page" or
  "Search"; the store and the search are in its `title` (E3). Group headers say "1 of 3 bought".
- Laid out like Print (Dols, 2026-11-14, "double bandeau"): a left rail "Hardware for" with each stack as a button
  (dark = in the list, a click leaves it out or puts it back; its line count under it; saved as `hwSkip`). Nothing
  picked is allowed, as in Print: "Nothing picked" in the middle, no Copy or CSV (Dols, 2026-11-14). Then "Jump to",
  always shown, even with one group: the groups as plain links with "1 of 3" bought on the right, a click scrolls to
  the group (UX audit E6). Centre:
  the title, progress, "Copy the list" (orange) and "Export as CSV", then the list. Right column, a "List options"
  panel titled with the list's line count ("12 lines", UX audit E4): "Where you buy", "Bolt finish", the head shape
  legend. Copy and CSV hold what the list shows, and so does the tab's count (it follows Hardware's rail, `hwSkip`,
  not Print's: UX audit E5).

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
- **The stack colour**: blue (`--stack`, `--stack-soft`, light and dark) means *the whole stack* in Design (Dols,
  2026-11-14): the stack picked in the rail (card and badge), the "Stack settings" button while it is on, and the
  inspector while it shows the stack's settings (`.dinsp.istack`: blue panel and border). A level's settings, or
  Colors, stay on the plain panel, so the panel's colour says at a glance whether the whole stack or one level is being
  edited. Blue is for that only: not an action (orange), not a selection elsewhere (dark).
- **Controls**: a setting is a row of segmented buttons (`.seg`: `useg`/`ubool` for a module, `sbool` for the stack,
  `pbool` for plate options), with sublabels in `<small>`. A dropdown only where the choices don't fit (printers,
  stores). A tick box marks an item of a list (plates, hardware bought, assembly steps), never a
  setting (Dols, 2026-11-14: "on enlève tout ce qui se coche"). What to print is a choice, not a list to tick: each
  stack (and the loose parts) is a button in Print's rail, dark when it is in the plates, plain when it is left out,
  a click toggles it, and the button says its state in words: "In the plates" / "Left out" (Hardware's: "In the list"
  / "Left out"; UX audit D6, `railState`). Nothing picked is allowed: no plates, "Nothing picked to print" in the middle (Dols,
  2026-11-14). Print removes nothing: stacks and loose parts are removed in Design (UX audit D7, 2026-11-14; the
  plate options' "Remove <stack>" and "Clear loose parts" went). A case's floor is Empty / Dividers / Gridfinity
  (`caseFloor`; Empty sets `caseEmpty`, which keeps the dividers placed but counts none); a drawer's grid dividers
  "At a wall": Divider alone / Closed (recommended).
- **Headings**: each step's main title is 28 px display (`.dtitle`, `.ptop-prog`, `.hwtitle`, `.asm-title`, `.xtitle`);
  a side panel has an eyebrow saying what it is (`.v3-sec`: Stack settings, Level 2 of 4, Colors, Selected plate)
  over a 22 px title naming which one. Inside a panel: foldable sections (`fold`, `.ifold`: a chevron, the name in bold,
  what is set on the right, a rule above), then field labels (`.field > .lbl`, small capitals). The stack's sections:
  Size and roof, Under the stack, Back of the stack; the level's: Module, Inside (or Drawers), Back of this module,
  Parts and bolts.
- **Type**: the mono font for figures (sizes, counts, grams), never for names or sentences.
- **Words**: "Remove" (not "Delete") for stacks, levels and filaments.
- **Removing or clearing** is pressed and held for half a second (`holdButton`, `HOLD_MS`), the button filling in red;
  let go sooner and a toast says to hold it: a stack (its cross and "Remove stack"), a filament, the loose
  parts, a divider plan, the plates, the print progress, an assembly count (Dols, 2026-11-14). A click that comes from
  no pointer and no key (a screen reader, voice control: `detail` 0) can't be held, so it asks for a confirmation
  instead.
- **Undo** (UX audit 2026-11, session 1): every change to the stacks, the colours or the loose parts can be taken back
  with Ctrl/Cmd + Z, and put back with Ctrl/Cmd + Y or Ctrl/Cmd + Shift + Z (not while typing in a field: the field
  keeps its own undo). A gesture that overwrites or removes says what it did with an "Undo" button for about 6 s
  ("Level 3 removed · Undo", "Two-tone applied to Rolling tool cart · Undo", "Footprint M5 → S3, 2 levels changed ·
  Undo"); other changes show nothing but are undone the same way. The selection comes back with what is undone; the
  camera stays where it is. A gesture that overwrites asks no question first: the colour presets apply, then offer
  "Undo" (the "USSA render" confirmation is gone). Print's "Reset all progress" and "Clear" keep press and hold and
  offer "Undo" too. Undo lives in memory only: a reload or a design file opened starts with nothing to undo.
- **Keyboard shortcuts** (Dols, 2026-11-14): `?` or the header's "Shortcuts" link (beside What's new and Report a bug
  or an idea) opens the list ("Keyboard shortcuts", `#keys`). Everywhere: 1 to 4 go to the steps (by the key's place,
  so AZERTY works with or without Shift), Ctrl/Cmd + S saves the design (Save), Ctrl/Cmd + O opens one, Ctrl/Cmd + Z /
  Y undo and redo. In Design: ↑ ↓ the level above or below (from Stack settings, ↓ picks the top level and ↑ the
  bottom one), Esc back to Stack settings (or from Paint back to Select), Shift + ↑ ↓ the stack above or below in the
  rail, Alt (Option on a Mac) + ↑ ↓ move the level, D a copy of the level above it, Shift + D below it, A a level on top, Delete (or
  Backspace) removes the level, one press with "Undo" like the menu's "Remove level"; Ctrl/Cmd + C copies the selected
  level, or the stack when its settings are shown, and Ctrl/Cmd + V pastes a level above the selected level (on top
  from Stack settings) or a stack right after the selected one in the rail, named "… copy" (Dols, 2026-11-14; the copy
  is taken when copied and kept for the page's life, in this page only; a level pasted into a stack of another
  footprint is made to it; a paste says what it did, with "Undo"; text selected on the page is copied as usual; the
  level menu has "Copy level" / "Paste a level above", the stack menu "Copy stack" / "Paste …"); in the 3D view O opens or closes
  the level's drawer or case, P Paint on or off, F fits the stack in the view (the one reframing, asked for), E Spread
  levels, H Hide roof; Ctrl/Cmd + click and Shift + click select several levels (listed in the 3D view's group, "click" not drawn as a key), and with several selected Alt + ↑ ↓, D, Shift + D, Delete, O, Ctrl/Cmd + C and V act on all of them. Rules: never while typing in a field or with a menu, a dialog, the filament picker or the
  printer list open; bare keys take no Ctrl, Cmd or Alt, so the browser's own shortcuts stay theirs (only Ctrl/Cmd + S
  and O are taken, for the design file); a key held down acts once (but the arrows repeat); no shortcut removes
  anything that is pressed and held with the mouse. Discoverable where the action is: the menus show the key on the
  right ("Remove level · Delete", "Save · Ctrl+S"), the buttons say it in their tooltip ("Spread levels (E)") and
  `aria-keyshortcuts`, the view's "?" names the main ones.
  "Remove level" is a plain click with "Undo" in the level's menu (right-click in the 3D view, or "⋯" in the level
  panel: UX audit session 3); every other removal keeps press and hold.
- **Rails**: Design, Print and Hardware also have a right column (Design's inspector; Print's selected plate over the
  plate options, `.pside`; Hardware's list options, `.hwside`). Design, Print, Hardware and Assemble each have a left
  rail with an eyebrow naming its items (Stacks, What to print, Hardware for, Sections). Every tab past Design shows its progress (Print and Assemble in %, Hardware the lines to buy).
- The 3D view has no Front / ¾ / Side buttons any more (Dols, 2026-11-14): a stack opens from three quarters, then
  one drags to turn it. The camera never reframes by itself (a level added, the footprint changed, "Spread levels",
  "Hide roof": it stays where it is); "Fit the stack in the view", on a right-click on the background, reframes it when
  asked (UX audit 2026-11, decisions 1 and 3).

## Steps, each testable on its own

1. **Hardware**: new tab, list moved out of step 2, bought ticks, copy and CSV. Branding changes in the header.
2. **Print**: plate sheet with nesting, selected plate, Printed group, single export button, plate options menu, export states. Remove `plateColors`.
3. **Assemble**: section rail, per-unit counter, section hardware.
4. **Design model**: stack-level footprint and roof, level inspector, no draft unit, migration of saved builds, first launch, hide what does not fit, backbones from the handles.
5. **Wide levels and loose parts**: "Across the width", footprint strip, loose parts in the rail.
6. **Paint tool**: filaments as brushes, role list, catalogue under the view, exceptions list, double-click to open.
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
