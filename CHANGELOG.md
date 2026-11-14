# What's new

Changes to the Vault Print Planner, newest first: this fork's first, then Romy's at [vault.romy.io](https://vault.romy.io).

## Draft, not released yet: the Dols fork
- **A fork of Romy's planner,** kept at [github.com/doooools/vault-print-planner](https://github.com/doooools/vault-print-planner). Everything below is new in it.
- **Your stacks in 3D,** made from your own Vault files: every drawer, case, roof, base and wheel where the assembled unit puts it, with its bolts. Turn it, spread the units apart, hide the roof. Parts are simplified in your browser and kept there for next time; nothing is uploaded.
- **Open drawers and cases in 3D:** double-click it, or hold Ctrl or Shift and click. A drawer's key turns and its racks slide before it pulls out; a case's latches flip before the lid opens, with the roof riding on it. A drawer comes out on its telescopic runners, as far as the real ones let it: the box slides alone in its guides for the first half, then takes the guides out with it to the stoppers. Closing, the box goes back in first and pushes the guides home at the end.
- **Several drawers in one module:** a 2F module can hold two 1F drawers, a 4F module two 2F, four 1F, or a 2F and two 1F in any order. Parts, bolts and geared rails are counted per drawer. The mixed ones are marked Inferred: the manuals don't show them.
- **Colors:** the Paint tool gives each kind of part a filament, for a whole stack or a single module, from your own filaments or Bambu Lab's PLA and PETG colours. Each stack keeps its own colours. Plates, filament totals and the Bambu Studio project follow them, one filament slot per colour. The runner guides, which sit in the module, take the module's colour until you paint them on their own.
- **A new layout:** Design, Print, Hardware and Assemble tabs. In Design, your stacks on the left, the 3D view in the middle, the selected level or stack on the right. On a wide screen the page takes the whole width, most of it for the 3D view, and the right-hand panel ends with the view and scrolls on its own. Start from a template or a blank stack, and set a level across the width as L, L² or two modules side by side.
- **Print what you want:** tick the stacks, and the loose parts, to plan. The plates follow every change made in Design.
- **Hardware has its own tab:** one shopping list for the whole build, ticks for what you've bought, copy or CSV, and the bolts' finish (black or zinc) shown in 3D. Store links follow where you buy: pick your store by continent (Amazon in North and South America, Europe, Asia, Oceania and Africa); the page guesses it from your browser the first time. Amazon.com links are the original planner's affiliate links, so US purchases keep supporting Romy's project; the other stores' links carry this fork's affiliate tag where it has one, and the page says so beside them.
- **Save and open designs:** in Chrome and Edge, Save writes your stacks, loose parts and colours into your Vault folder, next to the part files. Save as… and Open… work anywhere; other browsers download the file.
- **Lost folder, said plainly:** when the page can no longer read your Vault folder (the browser asks again after a reload, the folder was moved, or Firefox and Safari don't keep it between visits), a popup says the 3D view needs it, with a button to reconnect it. Chrome and Edge reconnect on their own when you chose "Allow on every visit". "Later: plan without the files" or "Not now" keeps it away for the rest of the visit.
- **Bases in 3D:** the base, wheels, front foot bar and casters are drawn where they go. A base without wheels now stands on its own: no feet. A roof can sit on a top-opening case.
- **Universal handle lock and module connectors:** two parts in the Vault download the planner never offered. On M, L and XL stacks with the pull-out handle, pick the universal lock: two small locks, one per rod, that fit any printer instead of the one-piece lock (up to 419 mm long). "Module connectors", in a stack's settings, screws a small bar over each joint between two drawer modules at the back corners, into the holes every drawer module has there; a 2F one spans a 1F module. Both are drawn in 3D, with their bolts.
- **Dividers where you want them:** a case's plan seen from above fills the slots moulded in its walls with a click. A drawer's grid dividers go in with two clicks on the box's holes: where the divider starts, then where it ends, among the holes the plan marks (a divider covers 5 to 32 holes). It closes against a wall, meets a divider running across, or stops open; the part list and the 3D view count the right file and edge pieces. A click on a divider removes it.
- **Light or dark, your pick:** two buttons at the top of the page switch the theme. The page starts in your system's setting and keeps the one you pick for your next visits, 3D view included.
- **Report a bug or an idea:** the link at the top of the page opens a short form on GitHub. The bug form gets your browser and printer filled in.
- **Fixed:** Bambu Studio projects with several colours no longer fail with "Invalid configuration file". The heavyweight roof's carry handle no longer drops out of the print list when the roof is swapped. Store links are plain product pages.
- **Supports only where USSA asks for them** (from Romy's planner, 2026-11-10): supports go only on the files USSA names "Turn On Supports" and on the XL drawer front. Bambu Studio's overhang warnings no longer turn them on: on drawer boxes they filled the channel the bottom geared rail slides into.
- **No more 10% spares:** the part list, the plates and the hardware list give exactly what the build needs. Print or buy extras yourself if you want them (Loose parts takes any single part).
- **Part counts checked against the manuals:** a case now gets one label (the case label on 1F, the drawer label on 2F and 4F), not both. The removable hidden key and its key cap are printed once per stack, not once per drawer. A wall mount gets one wall cleat per opening in its plate. Backbones follow the manual: a column on the back of the stack, from the base to the module under the top one (where the pull-out handle lock goes), in 2F backbones with a 1F for an odd remainder; a pegboard extends it to its module. On an L² or XL², shared parts are listed once, and Design and Print give the same totals.
- **Works the same on Linux, macOS and Windows:** the files macOS adds to a copied folder are ignored, and Firefox and Safari fall back to a folder upload and downloads.

## 2026-11-10
- **Shorter drawers in taller modules:** a 2F or 4F drawer module can now hold shorter drawers, like two 1F drawers in a 2F, or two 1F drawers above a 2F in a 4F. Pick them under "Drawers inside" in step 1 (each half on its own for L²). The parts list, front bolts and stack picture follow. Thanks to the viewer who pointed out they fit.
- **Supports only where USSA asks for them:** Out of an abundance of caution, supports are now only added if USSA says "Turn On Supports" (plus the XL drawer front, which has the same lock pocket as the fronts USSA labels) since there are some facets that could use supports but aren't mandatory. The onus is on you to think through what makes sense with the part you're building.

## 2026-11-09
- **XL units really fit the H2S now:** the XL drawer and case modules and the XL bases were still marked as too big. They fit at the angle USSA exported them, and the planner now keeps them there. The XL heavyweight roofs are still too big for the H2S.
- **Closer filament estimates:** checked against the weights USSA publishes per module, the planner was reading about 17% high. It's now within a few percent.
- **Stack heights with 1F cases:** the planner listed a 1F case as 71 mm tall instead of about 66, so stack drawings and overall heights came out a little tall. Only the numbers on the page were off; the parts and print files are unchanged.
- **Assembly:** step 4 now also passes on USSA's advice to put a 2F module right under the roof when you use the base, backbones or handles.

## 2026-11-08
- **Filament per color:** step 3 shows roughly how much of each color the whole build needs, so you can check your spools before you start.
- **Labels get their own plate,** so you can add your text and print them in several colors without touching the other plates. Turn it off in step 3 to print them with the rest.
- **Manual supports go where they help:** each one prints standing against the end of a roof of the same depth. Ones with no roof to brace are left out (step 3 says which), and STL folder names say where to stand them.
- **Download names say what's inside:** the build, the printer, and which plates if some are already printed, like "Vault - 3 units in 2 stacks - P1S - plates 4-12.3mf".
- **Printer not listed?** Pick "My printer isn't listed" and type its name: the bed size for about 380 printers fills in, taken from OrcaSlicer's printer profiles. Or enter your bed size yourself. The bed size is all the planner needs.
- **Voron presets:** 2.4 and Trident (250, 300, 350) and the 0.2. Like other non-Bambu printers, they get plate files for OrcaSlicer or PrusaSlicer.

## 2026-11-07
- **More printers:** presets for Prusa (MK4/MK4S, CORE One, MINI+, XL), Creality (K1/K1C, K1 Max, K2 Plus, Ender-3 V3 SE), Elegoo (Centauri Carbon, Neptune 4 Pro and Max), Anycubic (Kobra 3, Kobra S1) and Qidi (Q1 Pro, Plus4), plus Custom size for anything else.
- **Plate files for non-Bambu printers:** step 3 now saves a zip with one standard .3mf per plate. Parts are already laid out, and the parts that need supports or a brim are already marked. Works in OrcaSlicer, PrusaSlicer and the slicers built on them; a settings.txt lists the same settings for any other slicer.
- **STL folders** now name each part's settings in its file name, with a settings.txt per plate.
- **XL units fit the H2S:** facades and backbones that are too long for the bed go on the diagonal, at whatever angle fits.
- **Missing parts are named:** if your Vault folder is missing files, step 3 lists them. File names that an unzip or a newer download changed are still matched.
- **Print and Assemble stay empty** until you add something to your build, with a button to add the unit you picked in step 1.
- **Fewer slicer conflicts:** parts with supports keep clear of neighbouring parts, the rows around them and the bed edge.

## 2026-11-06
- **First public version.**
- **More Bambu printers:** P2S, X2D, A2L, H2D Pro, H2C and H3C; plate spacing fixed on dual-nozzle printers.
- **Stack pictures:** front and side views, overall size with dimension lines, and wheels, feet, casters and handles drawn where USSA's manual puts them.
- **Step 1 checks whether a unit stacks** before adding it and offers a matching size.
- **Hardware list:** bolt head shapes, drawer front bolts counted from the holes in each front, and links to matching products.
- **Choosing the Vault folder** is its own step, with a heads-up about the browser's permission prompt.
- **Plate numbers stay put** when you mark plates as printed.
- **Tree supports** no longer run into the next part.
- **Part pictures** at full size.
