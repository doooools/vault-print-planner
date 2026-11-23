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
- **Name** (Dols, 2026-11-23): **3D Vault Configurator**, in title case, in the tab's title and the header (the
  preprod keeps its "Preprod · " prefix). Page text says "the configurator" for this page; "planner" only for Romy's
  original ("Romy's planner", "the original planner").
- **Branding**: one credit line "A fork of Romy's Vault Print Planner" linking to the original. Remove the Ko-fi and YouTube buttons. The store links must stop being upstream's affiliate links (see "Open points"); the "As an Amazon Associate…" line goes with them. (Changed 2026-11-13 at the user's request: Amazon.com links are upstream's affiliate links again, other stores take the fork's own tags; see CLAUDE.md.)
- **Opening drawers and cases**: no "Drawers" tool. A double-click on a drawer or a case opens or closes it, in both tools, and so do O and the level's menu. A plain click selects (Select tool) or paints (Paint tool). (Ctrl / Shift / Cmd + click opened them until 2026-11-14; they now select several levels, see "Several levels selected".)
- **Several levels selected** (Dols, 2026-11-14): with Select, Ctrl + click (Cmd on a Mac) on a level in the 3D view adds it to the selection or takes it out, Shift + click selects the levels from the anchor (the last one clicked alone or with Ctrl) to it, Ctrl + Shift + click adds that range. Levels of the stack shown only (the view shows one stack). In Paint a click with Ctrl or Shift paints as a plain one. Each selected level is outlined in the view. The panel (`multiInspector`) says "3 levels of 5 selected", "Levels 1, 3 and 4", the modules, parts and grams together, the levels as small buttons (top first; one picks that level alone) and one line on what it does; then only the settings every module of every selected level has (Module: across the width, type, height; Inside or Drawers: the layout, inside, cut-outs, divider height, at a wall, lock, geared rails for drawers, every drawer of a module holding several; body style and floor for cases; Back: wall mount, pegboard, backbone), each offering only the options every one of them can take. Drawers mixed with cases share the Module and Back sections only. A setting set differently on them has no button pressed and a grey "Mixed" pill beside its name (the fold's summary says "mixed heights", "mixed locks"…). A change goes to every module of every selected level at once and says so with "Undo" ("Lock: Key lock, levels 1, 3 and 4 · Undo"): one Undo takes it all back. Labels (Dols, 2026-11-15): a folded "Labels" section, after Inside, with one "Text" field "on all N fronts" (every front of the levels selected: each drawer of a module holding several, each module of a pair). It shows the text when they all read the same; else it is empty, says "Mixed" and its placeholder reads "Mixed: type to give them all one text" (the fold's line: "1 of 4 named, mixed"). Typing draws it on every front in the view; leaving the field (or Enter) saves it with "Label “M6 bolts” on 4 fronts, levels 1, 2, 3 and 4 · Undo"; typed then wiped out, it clears them all ("Labels cleared…"); Esc puts each front's own text back. A module holding several drawers gets the text on each, and a line says to set them up one level at a time to name them apart. The font, letter height and relief (`labelLook`, for the whole project) sit under it as in the one-level panel. What is set per drawer box or per module (divider plans, the drawer tabs, one side of a pair) stays in the one-level panel, as the panel's line says; copies made with D, Shift + D or Ctrl/Cmd + V keep their labels, as one level's do. The "⋯" and a right-click on one of the selected levels open their menu: Open / Close their drawers and cases (O), Add copies of the N above (D) / below (Shift + D: the copies are then selected), Copy N levels, Paste above the top one, Move up / down (each one step, Alt + ↑ ↓), Remove N levels (one click, Delete, "Levels 1, 3 and 4 removed · Undo"). Ctrl/Cmd + C copies them all and Ctrl/Cmd + V pastes them all, the pasted levels then selected. A plain click, ↑ ↓, Esc, the level panel's buttons or another stack go back to one level (or none). Not kept over a reload.

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
One row from 1420 px, so at 1440 (UX audit A10, 2026-11-14); below, the buttons go on a second row. Under the name, small links: "What's new" and "Report a bug or an idea" (Dols, 2026-11-14: back at the top after session 8 had put them in the footer), "Shortcuts", and "About" (Dols, 2026-11-15). They are not file actions, so they stay out of "File", and as a second line under the name they take no width of their own on the row (12 px, no wider than the name). The fork's credit to Romy's planner is the first section of What's new, "About this fork" (framed): who made the original, its link and its MIT licence, what the fork adds, and that Amazon.com links stay Romy's affiliate links. The page has no footer any more (Dols, 2026-11-15: "toute la partie du bas est gênante"): its four notices are in the "About" window, opened by the last link under the name, in this order: Not affiliated with USSA, Store links (who earns from which Amazon store, naming Romy's original planner), Visit count (what GoatCounter gets, and "Don't count this browser"), Where the numbers come from. Hardware keeps its own one-line disclosure under the store picker, where the affiliate links are. The page's source starts with the upstream MIT notice.
- **File** (UX audit A9, session 8): a menu on every step, the same `role="menu"` list as the 3D view's. Its head: "Design file", the file's name (the last one saved or opened, "Not saved to a file yet" before), and how it stands: "Kept in this browser. The file has every change." / "… The file is 3 changes behind." Then Save (where it goes on the right: "in the Vault folder", "to downloads"), Save as…, Open…. The file is the whole project (Dols, 2026-11-15): the design, the printer, Print's options, stacks left out and progress, the label look, Hardware's ticks and stacks left out, Assemble's steps, the step and selection shown; opening it puts all of that back (a file saved before only the design, progress here kept). The person's own settings stay out: theme, store, Vault folder, visit count. The head's "The file has every change" compares all of it, progress included. Save as… opens the browser's save window (Chrome, Edge), started in the Vault folder; a browser without one gets a name prompt, then the download. A save window that won't open, or a file that can't be written, never ends in a silent download: the toast says why ("Saved X to your downloads: the browser didn't open its save window (…)"). Under a line, "Export the stack as STL" and "Export the stack as GLB, with colors" (the 3D export, below). Design's rail no longer has a "Design file" group; the first launch keeps "Open a saved design…".
- **Tab counters** (UX audit A10): none on Design; Print in % printed; Hardware "11 to buy" (lines not ticked, following Hardware's rail); Assemble in % assembled.

### 0 · First launch
Shown when there is no stack. Three rows: printer, Vault folder (same text and "Later: plan without the files" as today), first stack (empty, or one of the presets of `presetsBlock`, filtered by `presetFits`). Print, Hardware and Assemble are disabled until a stack exists.

### 1 · Design
- Left rail: one card per stack (width letter, name, footprint, level count), "New stack", "Start from a template…", then "Loose parts", an entry like the stacks (solid border, "spares, single parts", its part count or "none yet" on the right; UX audit A9). Print's "Already printed" has the same look.
- Centre: the 3D view of the selected stack, always shown. Toolbar: tools "Select" and "Paint", then "Rotate" (a toggle, dark while on: the stack turns slowly, one turn in 24 s, until pressed again; Dols, 2026-11-15), "Spread levels", "Hide roof", "Bolts" (two swatches, raw steel or zinc / stainless, the same setting as Hardware's "Bolt finish") and "?" (how to move the view: drag, scroll, right-drag). Over the view's header: the stack's name as the big title, with a pencil button that turns it into the name field (Enter or leaving the field keeps it, Esc puts it back; UX audit B3); "Add a level on top" (`title` "Adds a level like the top one"); a "Stack settings" button, which opens them and does not toggle (A8). No "Footprint" button nor strip (UX audit A8, B2, 2026-11-14): width and depth are in Stack settings.
- In the view (UX audit 2026-11, session 3): with Select, the level under the pointer is outlined and named beside it ("Level 3 · M5 · 1F drawer", "Click to set it up · right-click for actions"). A right-click on a level (let go less than 5 px from where it was pressed; a right-drag still pans) selects it and opens its menu: Open or Close drawer / case (the drawer under the pointer in a module holding several), Add a level above, Add a level below (copies of the level), Move up, Move down, Remove level (a plain click, then "Level 3 removed · Undo"). A right-click on the background, the roof or the base opens the stack's: Fit the stack in the view, Add a level on top, Stack settings. Under a line: Export as STL, Export as GLB, with colors. Both are `role="menu"` lists (arrow keys, Home, End, Enter, Esc) that close on a click outside, a scroll or the camera moving. The hint under the view is one line: "Click a level to set it up · right-click for its actions · double-click opens a drawer"; the first-visit tip about opening a drawer stays. Double-click keeps opening drawers and cases (Ctrl / Shift + click did too until 2026-11-14: they now select several levels). The hint reads "Click a level to set it up · Ctrl+click for several · right-click for actions · double-click opens a drawer", the label beside a level "Click to set it up · Ctrl+click to select several · right-click for actions".
- **While parts are simplified** (Dols, 2026-11-23): a window over the view, "Making the 3D view lighter", opens as
  soon as a part file is really simplified (after 0.4 s, so a quick one doesn't flash it; never for parts this browser
  already keeps). An ink ring turns beside the title, then "Simplifying part files: 3 of 13 done. The big ones take a
  while." and a striped bar. It says why ("too many triangles for a browser to turn smoothly… a lighter copy of each
  part, within 0.15 mm of the original") and, framed, that what is printed doesn't change: "Print's plates and downloads
  always use your original STL files, as they are. Only Export from the 3D view takes the lighter copies." Then "This
  browser keeps the copies: next time, these parts show at once." It takes no focus and blocks nothing: the view turns
  meanwhile. Done, it says "Done. The view shows 24k triangles, from 1.8M in your files." for a moment, then flies
  into its button in the strip under the view, beside the triangle count ("Simplifying 3 of 13…" with a small ring
  while it works, "Why simplified?" after), which opens it again; × or Esc tucks it away too. The fold is one stroke of
  about two thirds of a second, gathering speed, with no pause nor slowing down (Dols), and stays visible all the way into the button, which then flashes yellow, even with less motion asked (Dols,
  2026-11-23: "c'est important qu'on voit la page se replier dans son encart").
- **Share links and codes** (Dols, 2026-11-23, issue #84): the File menu's "Copy a share link", "Copy the share code" (greyed with nothing to share) and "Open a share link or code…" (asks for it with `prompt()`). The link is the page's address with `#d=<code>`; the code holds the stacks, loose parts, colors, Print's plate options and stacks left out, the print settings by part and the label look, compressed (one stack ≈ 800 characters). Never the printer (whoever opens it keeps theirs), nor what is printed, bought or assembled. Copied: a long toast with its length and what it holds. Opened (the link loaded, pasted in the address bar, or the code pasted): it replaces the project, asked first when there is one ("To keep yours, cancel and save it first"), then "Opened the shared design"; the address loses its `#d=…`; the File menu says "Not saved to a file yet". A code cut short: "This share link or code is cut short or damaged: ask for it again, or copy all of it".
- **The stack in 3D, to a file** (Dols, 2026-11-15: renders in Blender): "Export as STL" and "Export as GLB, with colors", at the end of the stack's right-click menu and of the File menu (there "Export the stack as …"). What the view shows, as it stands: drawers and cases open or closed, levels spread or not, the roof hidden or not, the bolts and casters; never the shadow or the outlines. The parts are the simplified ones the view draws (0.15 mm). STL: one solid, in mm, Z up, the floor at 0 and the footprint centred, no colour nor label. GLB: one object per part named after its file, grouped by level (and roof, base, column), one material per colour named after the filament ("Orange #e8742f", "Bolts, grey (zinc-plated or stainless)"), the labels as textured planes, in metres. Both greyed until the parts are in, with the reason as the tooltip ("Choose your Vault folder first: until then the view shows boxes, not the parts", "Wait until every part is in the view"): boxes are never exported. Made in the browser and downloaded; the toast: "Saved Test stack.glb to your downloads (4.1 MB). USSA's parts: for your own renders, not to share." The GLB's `asset.copyright` and the STL's header say the same.
- The "Paint" tool button carries the stack's filaments as small swatches (up to four, then "+N"; the names in its `title`), so the toolbar says where colours are set (UX audit C7, 2026-11-14).
- Right: the inspector.
  - Both panels are cut into foldable sections (UX audit A7, 2026-11-14): each header gives the section's name and, on the right, what is set in a few words ("Drawer · 1F", "Empty · key lock · geared rails", "nothing on the back", "18 parts · ≈ 570 g"). A section stays open or folded as the user left it, for the page's life.
  - A level selected: position ("Level 3 of 4"), then "Level below" and "Level above" (they move the selection) and "⋯", which opens the level's menu under itself, the same as the right-click (level actions are in that menu, not in the panel's header; "Duplicate" went, "Add a level above" does it). Sections: **Module** (open: "Across the width" on L and XL stacks, type, module height), **Inside** (open; named **Drawers** when the module can hold several: "Drawers in this module" as small diagrams, inside, lock, geared rails, or a case's body and floor), **Back of this module** (folded: wall mount, pegboard, backbone), **Parts and bolts** (folded: the part list and hardware). A new case starts with its floor "Empty" (UX audit X3, decided 2026-11-14).
  - Labels (Dols, 2026-11-14): a section of its own after **Inside** / **Drawers**, folded at first so it doesn't weigh on the panel (Dols, 2026-11-15): "Label", or "Labels" in a module holding several drawers, with one text field per front ("Text, on the drawer front" / "on the case front", or the drawer's name; placeholder "e.g. M6 bolts", 24 characters). Its summary gives the text in quotes ("“M6 bolts”"), "2 of 3 named", or "None". The text shows on the Label part in the 3D view as it is typed (dark letters on a light label, light on a dark one), replaces a drawer tab's second line, and is named under the level in the view's hover tip. It is saved, as one Undo step, when the field is left or Enter pressed; Esc puts the text back. Under the fields, "For every label in the project" (Dols, 2026-11-15): Font (Sans · Inter, Narrow · Roboto Condensed, Rounded · Nunito, Mono · Roboto Mono, Slab · Roboto Slab, Stencil · Stardos Stencil, in 3 columns), "Letter height, mm" (4 to 8, 6 "recommended"), "Raised text, mm" (None "blank", 0.4, 0.6 "recommended", 0.8, 1), and a note that the text's colour is the Label text filament, painted with a click on a text in the view like any part. Copies of a level (Add a level above / below, copy and paste) keep their labels; "Add a level on top" starts without. A new piece of free text: escaped wherever it is shown.
  - Several drawers in one module (UX audit X4): one tab per drawer ("Top", "2F · dividers", or its label in quotes) over a frame holding what is the drawer's own (label, inside, baseplate and divider settings, lock, geared rails) and, at its foot, "Same settings in every drawer". Under it: "In the frame: this drawer only. Outside it: the whole module." A click on a drawer in the view picks its tab too.
  - The stack selected: name as plain text (it is renamed at the centre) and a button to the top level, then "Duplicate stack" and "Remove stack" (press and hold) under its size, at the top of the panel (Dols, 2026-11-23; they were at its bottom), the stack's alerts (`stackAlerts`) or "Everything in this stack fits together" at the top, each alert that names a level with a "Show level N" link (UX audit B1). Sections: **Size and roof** (open: width and depth as segmented buttons, "For every level. Sizes too big for the <printer> aren't offered.", roof — None, Grid, Table, Bowl, Under-table, Heavyweight where it exists — and the grid roof's carry handle), **Under the stack** (folded: base, wheels, casters, foot bar), **Back of the stack** (folded: the two handles, the handle lock, module connectors). An option that needs another stays in place, greyed, its reason on the right of its name: Wheels and Casters "needs a base" (Casters "not with wheels"), Foot bar "needs wheels", Handle lock "needs the trolley handle", Carry handle "needs the grid roof" (UX audit B4); sizes the printer can't make stay hidden. A new empty stack opens on its settings, like a template (B6).
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
- Plate options, under the selected plate in the right column (Dols, 2026-11-14, "double bandeau" like Design: a rail on the left, a column of settings on the right), always shown: one folded line per setting with its value (`popt`: "Parts with supports · plates of their own"), which opens on its segmented buttons: "Parts with supports" (`mixSupports`), "Manual supports" (`printAids`), "Labels" (`labelsApart`; its hint sends the text's settings to Design's Label section, where they moved on 2026-11-15); then the folded "How plates are laid out" text and "Reset all progress" on one row (no clear button since UX audit D7). It was a "Plate options…" popover before.
- A plate's menu (Dols, 2026-11-23, issue #93): a right-click on a plate card (or the context menu key), or the
  selected plate's "⋯" (beside its filament tag), opens the menu the 3D view's levels have: "Plate 03 · Light grey · 2
  parts · ≈ 400 g", then Show this plate, Tick it for the download (Untick it), Tick the N <filament> plates left,
  Untick all (while some are ticked); Download this plate alone (the Bambu Studio project or the plate file, whatever is
  ticked), Download its STL folder (.zip), both greyed with the reason when a part is missing; Mark as printed (Put it
  back on the list); Print settings of its parts… (opens its kinds of part below and scrolls there), Plate options….
- Print settings by part (Dols, 2026-11-23, issue #83), a panel under Plate options: one folded line per kind of part
  on these plates (the colour roles of Paint, and "Tires (TPU)"), its value on the right ("default", or "4 walls ·
  gyroid · supports off"). Open, it says how many parts it holds and what the configurator gives them ("Default: 2 or 3
  walls · 15% infill · supports on some"), then five rows of segmented buttons, each starting with "Default": Walls
  (2 to 6), Infill (10 to 60 %), Infill pattern (grid, gyroid, cubic, lightning), Top and bottom layers (3 to 8),
  Supports (off, on), and "Back to the defaults" once one is set. A kind with parts that bend (latches, springs) warns
  that more than 2 walls can make them crack. Written per object into the Bambu Studio project, the plate files
  (PrusaSlicer and OrcaSlicer keys) and the STL folders' notes; supports also move the part to or off the plates with
  supports. Saved in this browser (`partSettings`) and in the design file.
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

## The look: Giscard Punk "encre" (Dols, 2026-11-22, preprod first)

The page took the look of Claude Design's handoff `vault-giscard-punk-handoff.zip` (brief, design guide, shader notes
and mockups; not committed). It changes how things are drawn, not what they do: every control, setting and gesture
stays. Where this section and the rules below disagree, this section wins.
- **Paper and ink**: the ground is paper (`#f1eee7`) with ink (`#111111`) in light, and the two swap in dark
  (`#070707` / `#f1eee7`). Tokens `--gp-*` at the top of the `<style>`, light by default, dark under
  `prefers-color-scheme` and `[data-theme="dark"]`; the planner's names (`--ground`, `--ink`, `--accent`…) point at
  them. Hex only: three.js can't read `oklch`. The Light / Dark switch, its storage and the system default are as
  before. A faint scanline overlay covers the page (`body::after`, not clickable).
- **Colours and their one meaning each**: yellow (`--accent`, `#f2d935`) = selected or done, a block with ink text
  stuck on a little crooked (tabs, segmented buttons, toggles, filter chips, "Bought", the folder once picked);
  pink (`--accent-btn`, `#fc65b6`) = the screen's one main action, with a hard 4 px black shadow (`--gp-shadow`); red
  block with white text = a problem (`.issue.bad`, `.pflag`); blue = the whole stack (as before: "Stack settings"
  and its inspector). The old orange is gone, and so is the dark "selected" fill.
- **Type**: three fonts, embedded in the page (Dols, 2026-11-22: no request to Google Fonts): Anton for titles, in
  capitals (step titles 48 px, panel titles 36 px, section heads 24 px); Special Elite for labels, buttons and tabs;
  Courier Prime 400/700 for text and figures (tabular). `src/fonts/` holds the woff2 files (Fontsource 5.3.0, latin)
  and their licences (OFL 1.1, Apache 2.0); `build.py` inlines them as `data:` URLs (`/*FONTS*/`). About says so.
- **Shapes**: no rounded corners; borders 2 px in ink; shadows only hard (4, 6, 10 px black), never blurred. Dashed =
  left out, new or disabled ("New stack", disabled buttons and tabs, a plate printed); dotted = separators between
  rows; 45° hatching = progress (Print's and Assemble's bars).
- **The taped card**: one per screen, the key thing on it, on `--raised` (ink in light, paper in dark), turned 1° with
  a strip of tape (`::before`): the inspector's head (`.ihead`, blue for the stack), Print's selected plate (`.psel`),
  Assemble's "Have ready" (`.asm-need`), Hardware's list options. The screen's key figure sits on it big (`kfig`: a
  level's parts, the selected levels' parts, the hardware lines; Assemble's first item; Print's title says "22%
  printed"). In the rail, the stack shown is a taped card too.
- **Design fills the window** from 1200 px (Dols, 2026-11-22): the page doesn't scroll; the 3D view takes all the
  height under the stack's title, and only the rail and the inspector scroll, each in itself. Narrower, the page
  scrolls as before.
- **Header**: one row from 1440 px (the printer's bed is hidden from 1240 to 1599 px, it is in the printer's window),
  the name as a taped label, the four steps two by two on a phone.
- **The 3D view ("encre", `open3d`)**: the canvas is transparent over the stage's plain paper
  (`--gp-vp-bg`; the dot grid went, Dols 2026-11-22). Flat colours in two tones (`MeshToonMaterial`, a 2 × 1 ramp): one light from the
  front, left and above, so fronts and tops are lit and right sides in shade, at about 70 %; the shade hatched at 45°
  in screen space (7 px, ink at 28 %). Every part is outlined in ink, 2.5 px at any zoom (an inverted hull: back faces
  pushed out along normals averaged at the corners, `hullMat`, `inked`; parts are drawn on both sides and the hull is
  pushed behind them, so the hairline gaps of the simplified parts show the part's colour, not ink), plus 1 px ink creases on edges sharper than
  30° between two faces where each face leaves the other's plane by more than 0.2 mm (`creaseLines`, once per shape;
  edges with one face and thin triangles left out: the simplifier fans long thin triangles across flat faces from a
  fillet or a countersink). Keeping the normals while simplifying (`simplifyWithAttributes`, PR #90) was tried and
  undone (Dols, 2026-11-23): slower, and the fronts and backs of the modules kept their lines. A hard shadow of the footprint, back and to the right (`--gp-vp-shadow`). The
  level under the pointer: its ink outline thickens to 4 px (no box any more). The selected level(s): a yellow ring
  (`--gp-vp-select`) around the whole module, drawn over the stack outside the module's own shape (stencil mask), with
  an ink ring outside it in light. What a click would paint is tinted halfway to that yellow. Picking, the camera,
  the tools, the menus and the mesh pipeline are untouched. The theme switch re-reads the shadow and the rings
  (`v.retheme`).

What the handoff changes in the rules below: orange actions became pink, the dark "selected" fill became the yellow
block, step titles went from 28 px to 48 px, the mono font is now the text font too (Courier Prime). Kept against the
handoff: sentence case in the page's words (capitals come from CSS on titles and labels only), the Bolts swatches, no
footer.

## One look for each kind of thing (Dols, 2026-11-13)

The pass of thread "Unifier l'interface de tout le planner" set these rules for every step, popup and panel:
- **Buttons** (orange then, pink since the look of 2026-11-22): a filled button (`.btn.primary`, `--accent-btn`) does the screen's main action (Add a level on
  top, Empty stack, Download, Mark as printed, Copy the list, Drawer done). Dark fill (`--ink`; the yellow block since 2026-11-22) only ever means
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
  levels, H Hide roof, R Rotate; Ctrl/Cmd + click and Shift + click select several levels (listed in the 3D view's group, "click" not drawn as a key), and with several selected Alt + ↑ ↓, D, Shift + D, Delete, O, Ctrl/Cmd + C and V act on all of them. Rules: never while typing in a field or with a menu, a dialog, the filament picker or the
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
  asked (UX audit 2026-11, decisions 1 and 3). "Rotate" (Dols, 2026-11-15) is the one camera motion that goes on by
  itself, and only once asked: the camera goes round the vertical axis (never closer, never another point looked at),
  a drag holds it and it goes on from where it was let go; off at every page load, kept while the stack changes and
  onto another stack.

## What is counted (Dols, 2026-11-16)

Dols wants to know what serves, what doesn't and what to improve, with no cookie, nothing in the way of the person and
nothing that tells a person apart. The page sends GoatCounter (account `dols`) its own requests, with no script
loaded: one per visit (the page, the site the visitor came from, the screen width, the address's query, so
`?utm_source=youtube&utm_campaign=video` or `?ref=reddit` on a shared link shows under Campaigns), then events, each
**at most once per visit** (`use()` in `src/template.html`, section "what is used"). Never from a local copy, a test
browser (`navigator.webdriver`, a headless user agent) or after "Don't count this browser" in About, which says what
is counted. Never a stack, file, folder or design name, a label's text, the person's part counts, nor any id. Never from
the preprod site either (`/vault-print-planner/preprod/`, CLAUDE.md "Preprod"): it sends nothing.

In the dashboard, events are the paths without a leading "/"; type the prefix in the filter to see a group.

- `tab/…`: the step shown (design, print, hardware, assemble), also the one a visit opens on.
- `design/…`: start screen, templates window, `design/template/<name>`, new stack, rail stack, loose parts, rename,
  stack settings, add a level on top, duplicate stack, level below / above, "⋯", drawer tab, "Same settings in every
  drawer", copy (level, stack), paste, part preview, print a part on its own.
- `module/<setting>=<value>`, `stack/<setting>=<value>` (width, depth, roof, handle lock…), `levels/…` (several levels
  selected: how they were selected, the settings changed, up / down / dup / del), `level/<op>` (top, dup, up, del…),
  `label/…` (text typed, relief, letter, font), `dividers/…` (case slot, all, grid click, grid clear).
- `3d/…`: tool (select, paint), rotate, spread levels, hide roof, help, bolts finish, right-click on a level or the
  background, a drawer or case opened, the real parts shown, parts not in the folder or not simplified, the viewer
  not loaded, `3d/simplifying` (the window opened by itself), `3d/why-simplified` (its button under the view),
  `3d/simplifying-hide` (its ×).
- `paint/…`: a click in 3D, brush, "A click paints", add a filament, part type or group painted, module exception,
  the presets ("Start from"), the filament picker (opened, scope, Bambu colour, line filter, tray colour, "Use it"),
  the Selected card's buttons.
- `menu/<item>`: any menu item used (level, levels, stack, File menus), digits as N.
- `key/<key>`: a shortcut that did something (`key/mod+z`, `key/step-number`, `key/r`…).
- `file/…`: menu, save, save as, open, opened (or opened an older file), export STL / GLB, share link or code copied,
  "Open a share link or code…", a shared design opened (`file/opened-share`). The code itself is never sent: it is
  after the `#`, which the visit count leaves out.
- `folder/…`: the Vault folder open during the visit, "later" on the start screen, the header button.
- `print/…`: stacks to print, filter, plate select / tick / previous-next, tick all, mark (un)printed, the downloads
  (Bambu project, plate files, STL folders), choose a folder, already printed (opened, add, stepper), plate options
  (`print/<option>=<value>`), print settings by part (`print/part-settings/<setting>`), a plate's menu opened (`print/plate-menu`, its items as `menu/…`), copy the part list, reset all progress; `printer/<id>` once Print is shown.
- `hardware/…`: stacks in the list, jump to, bolt finish, ticked bought, copy, CSV; `store/<id>` once Hardware is
  shown or a store is picked; `buy/<store>` (each store link opened, as before).
- `assemble/…`: a step ticked, a unit done.
- `link/…`: What's new, Report (bug, idea), Shortcuts, About, the steps' "Go to …" buttons; `kofi` as before.
- What the visit comes with: `theme/dark` or `light` (`-system` when not chosen), `lang/<language>`,
  `window/<width range>` (the page's breakpoints: under 860, 860–1239, 1240–1599, 1600 up), `device/touch`,
  `device/no-folder-window` (a browser without the folder window).
- `error/line-<n>`: an error in the page, the line in `index.html`, its message with quoted names taken out (five per
  visit at most).

A new button gets its rule in `USES` (a selector and a name, or a function of the element), a gesture with no button
a `use('group/name')` where it acts.

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
