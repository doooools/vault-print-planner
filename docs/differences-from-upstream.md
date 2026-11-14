# Differences from the original planner

This fork holds all of [Romy Macasieb's Vault Print Planner](https://github.com/rmacasieb/vault-print-planner) as it stands today, plus its own work: nothing from the original is missing, and everything below was added or changed.

## Compared versions

| | Repository | Commit | Date |
| --- | --- | --- | --- |
| Original | [rmacasieb/vault-print-planner](https://github.com/rmacasieb/vault-print-planner), `main` | `1ea73cd` (`README: drop "as is"`) | 2026-11-10 |
| This fork | [doooools/vault-print-planner](https://github.com/doooools/vault-print-planner), `main` | `31c34ff` (merge of PR #18) | 2026-11-12 |

- The fork is up to date with the original: the 8 commits Romy made after the fork came in through PR #1, and the original has had no commit since 2026-11-10.
- This page describes what you see and what the page does, not the code line by line.
- In numbers: 544 files differ, and the published page grows from 0.59 MB to 2.0 MB (mostly the embedded 3D placements).

## At a glance

| Area | Original | This fork |
| --- | --- | --- |
| 3D view | None | Every stack in 3D from your own Vault files, with its bolts, drawers and cases that open |
| Colours | 4 fixed colours (body, inner, accent, TPU) | A filament per part role, per stack or per module, a Paint tool, Bambu Lab's colours |
| Page layout | Design a unit, then Build, Print, Assemble | Design, Print, Hardware and Assemble tabs; stacks on the left, 3D in the middle, inspector on the right |
| Drawers in a 2F/4F module | 1+1, 2+2, 1+1+2, 1+1+1+1; each half of an L² on its own | The same plus 2+1+1 and 1+2+1, counted per drawer; both halves of an L² take the same layout |
| Dividers | Counts (how many across, how many along) | A clickable plan of the slots (cases) and of the peg holes (drawer grids) |
| Quantities | +10% spares | Exactly what the build needs, checked against the manuals and the files' holes |
| Hardware | Inside Assemble, Amazon US affiliate links | Its own tab, no affiliate links, store picked by continent, M4 × 80 for backbones |
| New options | None | Universal handle lock, module connectors, manual supports in Print |
| Saving | In the browser | Also to a file, written straight into the Vault folder (Chrome, Edge) |
| Site | vault.romy.io, Ko-fi, YouTube | doooools.github.io, Romy credited, "Report a bug or an idea" link |

## 3D stack view

The original has no 3D view (only small pictures of each part). The fork shows the selected stack in the middle of the Design tab.

**What it shows**

- Boxes of the right size until the Vault folder is picked, then the real parts read from your files, simplified in the browser (0.15 mm) and cached for your next visit. Nothing is uploaded; three.js and meshoptimizer load only when the view is shown.
- Every part where the assembled unit puts it: drawers, cases, roofs (including the heavyweight roof's handle and its two inserts), base, wheels, foot bar, casters.
- The backbone column and the stationary or pull-out handles, with the handle lock and its knobs.
- Pegboards, wall mounts and their cleats, the Gridfinity baseplates of XL drawers and cases, the latches' lock pins.
- Case dividers in their slots and the drawers' grid dividers.
- Bolts, drawn from their ISO size, always shown, in raw steel (black) or zinc-plated / stainless (grey): the toolbar button switches the finish, which also names the bolts and rods in the Hardware list and its store searches.

**What you can do in it**

- Turn (rotate, select), Paint and Drawers (open) tools.
- Front, ¾ and Side views; "Spread units" pulls the modules apart, "Hide roof" hides the roof.
- Open a drawer or a case with a double click, or Ctrl/Shift + click. A drawer follows the real mechanism: the key turns a quarter turn, the racks move back 20 mm, then it slides out. A case opens its latches, then its lid, roof included.
- A case with a module on top opens differently: latches, hinge rods slid out sideways, then everything above rises by 196 mm (a 4F module's height).
- In an L², or a 2F/4F with several drawers, each drawer opens on its own.
- When the stack changes (an option, a divider, a level), the camera, the open drawers and the selection stay as they were.
- Right-hand column: the selected part with "Change color…", and the list of modules from top to bottom.

**Not in 3D yet** (on purpose or still to do): the key lock's springs and the L²/XL² accessories, left out for now. The full list: [`tools/placements/COVERAGE.md`](../tools/placements/COVERAGE.md).

## Colours

The original puts every part in one of 4 fixed colours (body, inner, accent, TPU) that can't be chosen. The fork lets you pick the filament of each kind of part, and changes nothing if you pick nothing: by default each part keeps the colour the original gave it.

- **14 part roles** instead of 4: shells, fronts, drawer boxes, roofs, runner slides, locks, hinges, accents, Gridfinity interiors, dividers, labels, base and handles, fittings (backbones, connectors, feet, knobs), print aids. TPU tires stay on their own.
- **Three levels:** the whole project, one stack, or one module ("Only this …"). Each stack keeps its own colours.
- **Paint tool** in the 3D view: a brush bar with your colours, "Same part everywhere" or "This unit only", and the part under the pointer is tinted before you click.
- **Colors panel:** your filament tray (each colour with what uses it), the roles grouped Outside / Inside, "Paint all", presets, and the modules that have colours of their own.
- **One filament picker** everywhere: your tray, then the PLA Basic/Matte and PETG Basic/Matte colours Bambu Lab sells in Europe, with their real colour codes, a search and filters.
- **What colours change:** plates are grouped by colour, filament totals are given per colour, and the Bambu Studio project gets one filament per colour (slot 1, TPU in 2, the others from 3). A part in another colour than usual becomes its own line.
- PETG still gets PLA settings in the Bambu project for now.

## Page layout

The original reads as steps: design a unit, put it in a stack (Build), then Print and Assemble, with the hardware list in Assemble. The fork reorganises the whole page into four tabs, following [`docs/ux-redesign.md`](ux-redesign.md).

| Tab | What it holds in the fork |
| --- | --- |
| 1 · Design | On the left the stacks ("New stack", templates, design file, loose parts); in the middle the selected stack (name, Stack settings, Footprint, "Add a level on top", the 3D view); on the right the inspector of the level or the stack, or Colors while painting |
| 2 · Print | Tick the stacks and loose parts to print; the plates follow every change made in Design |
| 3 · Hardware | One shopping list for the whole project, "bought" ticks, copy or CSV, the bolts' finish |
| 4 · Assemble | The assembly checklist, stack by stack |

Other visible changes:

- **Build level by level** instead of "design a unit, then stack it": a level is set in place, as L, L² or two modules side by side (S+S, S+M).
- **Base and roof per stack**, in the stack's settings. A roof can sit on a top-opening case. A base without wheels stands on its own (no more feet option).
- **Start screen** "Start your build": printer, Vault folder, templates. Tabs 2 to 4 stay greyed out while there is nothing to make.
- **Lost folder, said plainly:** when the page can no longer read the folder (a reload, a moved folder, Firefox or Safari not keeping it), a popup offers to reconnect it. Chrome and Edge reconnect on their own when "Allow on every visit" was chosen. "Later" or "Not now" keeps it away for the rest of the visit.
- **Save and open a design:** "Save" writes the file into your Vault folder (Chrome, Edge), "Save as…" and "Open…" work everywhere; other browsers download the file.
- **Small comforts:** the inspector keeps its scroll position and open sections when an option changes; a tip shows how to open a drawer until the first try; a stack is deleted by holding its cross.
- **Linux, macOS, Windows:** file names are compared without regard to case or folder separators, and the files macOS adds (`__MACOSX`, `._name`) are ignored.

## Parts and options

| Topic | Original | This fork |
| --- | --- | --- |
| Several drawers in a 2F/4F | 2F: 1+1. 4F: 2+2, 1+1+2, 1+1+1+1. Each half of an L² can have its own layout | 4F: also 2+1+1 and 1+2+1. Parts, bolts and geared rails counted per drawer. Mixed layouts are marked "Inferred". Both halves of an L² take the same layout |
| Case dividers | A count across, along and for seals, whatever the case body | A top-view plan: a click fills or empties a slot measured in the file. A "Flat" body takes none; XL cases have their own side seal dividers |
| Drawer grid dividers | Counts across and along, an "Edge pieces: Rounded" option | A plan of the floor's peg holes (10.5 mm pitch): a click adds or removes a divider. Rounded pieces go where a divider meets another; "Close against the walls" picks N − 1 + straight piece or N alone. The old option is gone |
| Manual supports | An option on each unit, one support per drawer box | A Print option (Plate options, Print's right column), one support per drawer roof, packed next to its roof on the plate |
| L² / XL² accessories | One set per L² module, none for XL² | One set (1st + 2nd) per F, for L² and XL² |
| Universal handle lock | Not offered | An option for M, L and XL stacks with the pull-out handle: two small locks, one per rod, instead of the one-piece lock (up to 419 mm) |
| Module connectors | Not offered | A "Module connectors" option: a small bar at each joint between drawer modules, at the back corners; a 2F one spans a 1F module. Skipped where a backbone, lock or wall plate covers the holes |
| Backbones | Ticked per unit | A column on the back of the stack, from the base to the module under the top one, in 2F pieces (1F for the remainder, XL in 1F); a pegboard extends it |

The universal case fronts are not offered: the maintainer decided against them.

## Quantities, printing and hardware

The fork counts exactly what the build needs, where the original added 10% and sometimes used one manual page for every size.

**Part counts**

- No more 10% spares (at least one) on small parts and hardware: the part list, the plates and the hardware list give the exact count. For extras, "Loose parts" takes any single part.
- Quantities follow the measured assembly: 2 latches on L and XL drawers; one cap per front counterbore (1, 3 or 5 depending on the module) instead of one; runner guides, slides and stoppers in pairs on every 48 mm level (4 or 8 on a 2F/4F); 1 case lock on S and M, 2 on L and XL; one geared-rails file per drawer and one hinge file per case (each file holds both pieces).
- Checked against the manuals with a battery of 44 configurations ([`tests/battery`](../tests/battery/)): one label per case; the removable hidden key and its cap once per stack, not per drawer; one wall cleat per opening of the plate; on L² and XL², shared parts listed once, with the same totals in Design and Print.

**Hardware**

| Bolts | Original | This fork |
| --- | --- | --- |
| Case front, M4 × 20 | 7 on every case (the manual's L 4F) | From the files' holes: S/M 4 (1F, 2F) or 6 (4F), L 5 or 7, XL 5 |
| Hinge tops and locks, M4 × 14 | 16 on every case | 8 on S and M, 16 on L and XL |
| Backbones | "60–100 mm (to fit)" | M4 × 80, measured on the holes of the modules and the base |
| Connectors and universal locks | None | M4 × 25 and M4 × 30 (inferred, no USSA page) |

- **Store links:** the original links to Amazon US with affiliate links. The fork gives plain product pages and a "Where you buy" choice by continent (Americas, Europe, Asia, Oceania, Africa), guessed from your browser the first time. Outside Amazon.com, the link searches for the same size, head shape and ISO standard. The CSV carries these links.
- "Bought" ticks and the bolts' finish (black or zinc), also shown in 3D.

**Printing and the Bambu Studio project**

- Plates grouped by chosen colour, one filament per colour in the project (see Colours).
- A plate of labels weighs "< 5 g" instead of "≈ 0 g".
- Fixed: the heavyweight roof's handle no longer drops out of the list when the roof is swapped for a grid roof (too wide for the printer, on an H2S for example).

## Site, bug reports and what stayed the same

**The site**

- Address: [doooools.github.io/vault-print-planner](https://doooools.github.io/vault-print-planner/) (GitHub Pages, republished on every merge) instead of vault.romy.io. Romy's `CNAME` file was removed.
- Removed: the Ko-fi button, Romy's byline in the header, the YouTube link, the README's "No support" paragraph. Romy's planner is credited in the page, the README and "What's new".
- README rewritten for the fork (browser table, "Your files stay on your computer"); "What's new" opens with a "Draft, not released yet: the Dols fork" section above Romy's history.

**Report a bug or an idea**

- A "Report a bug or an idea" link next to "What's new" opens two GitHub forms (bug, improvement) on the fork. The bug form comes filled in with the browser, screen, printer and tab. The dialog warns that reports are public and not to attach Vault's files.

**The same in both**

- The Bambu Studio settings per printer (P1S to H3C), the bed-fit check, one 3MF per plate and STL folders for other slicers.
- Supports only where USSA says "Turn On Supports" (and on the XL drawer front): Romy did it on 2026-11-10, the fork took it in PR #1.
- The MIT license, the expected Vault release 261021, and the principle: everything runs in the browser and no Vault file is uploaded.

## Under the hood

None of this shows on the page, but it is what keeps the fork maintainable.

- **The build works:** in the original, `src/build.py` read three files missing from the repository and broke on Windows. `src/printer-beds.tsv` and `src/bambu-reach.tsv` were recovered from the published page, everything is read and written in UTF-8, and `src/` rebuilds `index.html` exactly.
- **New embedded data:** `src/stl-placements.json` (where each part goes, how it moves, its bolts, the measured slots and holes) and `src/bambu-colors.tsv` (Bambu Lab's colours). They are numbers only: no USSA geometry is in the repository.
- **Automatic check:** every pull request and every push to `main` runs `tools/check.py` (`.github/workflows/check.yml`): `index.html` is the build of `src/`, `validate.js` finds no problem, the page's scripts parse, no mesh file is committed.
- **`validate.js` checks much more:** quantities against the placements, roof handles, colour roles, case bolts against the measured holes, backbone rules.
- **Measuring tools** ([`tools/placements/`](../tools/placements/), 42 Python, Blender and Node scripts): placements, opening kinematics, bolts, backbone column, wall mounts, baseplates, dividers, grids, connectors. Explained in [`tools/placements/README.md`](../tools/placements/README.md); what is missing is in `COVERAGE.md`.
- **Test battery** ([`tests/battery/`](../tests/battery/)): 44 configurations compared with an oracle written from the manuals and USSA's file tree, plus a check of every plate.
- **Documents:** `CLAUDE.md` (the fork's rules and state), [`docs/ux-redesign.md`](ux-redesign.md) and [`docs/colors-3d-redesign.md`](colors-3d-redesign.md), issue forms, `.gitattributes` (LF line endings), `.gitignore`.
- **A heavier page:** 2.0 MB instead of 0.59 MB, because of the 3D placements (already packed: over 3 MB without that). three.js and meshoptimizer come from jsDelivr (pinned versions), only when the 3D view is shown.

## Pull request history

Before pull requests, most of the work (3D, colours, page redesign, several drawers per module, bases, saving, quantities, removing the 10% spares) went straight to `main` between 2026-11-10 and 2026-11-12. Since then, one pull request per topic, all merged on 2026-11-12:

| PR | What it changed |
| --- | --- |
| [#18](https://github.com/doooools/vault-print-planner/pull/18) | Backbone bolts: M4 × 80, measured on the files |
| [#17](https://github.com/doooools/vault-print-planner/pull/17) | Universal handle lock and module connectors |
| [#16](https://github.com/doooools/vault-print-planner/pull/16) | Automatic check of every pull request |
| [#15](https://github.com/doooools/vault-print-planner/pull/15) | Folder popup stays away after "Later"; stores by continent |
| [#14](https://github.com/doooools/vault-print-planner/pull/14) | Case bolts from the files' holes; "< 5 g" for labels |
| [#13](https://github.com/doooools/vault-print-planner/pull/13) | Drawer grid dividers: plan, list, 3D |
| [#12](https://github.com/doooools/vault-print-planner/pull/12) | "Report a bug or an idea" link; double click to open in 3D |
| [#11](https://github.com/doooools/vault-print-planner/pull/11) | Open a case that has a module on top |
| [#10](https://github.com/doooools/vault-print-planner/pull/10) | The 3D view keeps camera, open drawers and selection when the stack changes |
| [#9](https://github.com/doooools/vault-print-planner/pull/9) | Case dividers: slot plan, list, 3D |
| [#8](https://github.com/doooools/vault-print-planner/pull/8) | The inspector keeps its scroll and open sections |
| [#7](https://github.com/doooools/vault-print-planner/pull/7) | 3D level outline fixed; L² drawers open one at a time |
| [#6](https://github.com/doooools/vault-print-planner/pull/6) | Manual supports in Print; L²/XL² accessories per F |
| [#5](https://github.com/doooools/vault-print-planner/pull/5) | Pegboards, wall mounts, baseplates, lock pins in 3D |
| [#4](https://github.com/doooools/vault-print-planner/pull/4) | Backbone column and handles in 3D |
| [#3](https://github.com/doooools/vault-print-planner/pull/3) | Folder popup shows even when no folder was ever chosen |
| [#2](https://github.com/doooools/vault-print-planner/pull/2) | Say when the Vault folder is no longer linked, with a button to reconnect it |
| [#1](https://github.com/doooools/vault-print-planner/pull/1) | Romy's 8 later commits (supports only where USSA asks for them) |
