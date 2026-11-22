# What's new

Changes to the Vault Print Planner, newest first: this fork's, then those of Romy's original planner.

## About this fork
This page is a fork of [Romy's Vault Print Planner](https://vault.romy.io), made by Romy Macasieb and shared under the MIT licence. Romy's planner does the heart of the work: it lists every file a Vault build needs, checks each part against your printer, lays the parts out on plates and makes the Bambu Studio project. It takes no feature requests and invites forks instead: this one, kept by [Dols](https://github.com/doooools), holds all of Romy's planner and adds:
- **Your stacks in 3D,** made from your own Vault files, with drawers and cases that open and every bolt in place.
- **Colours:** a filament for each kind of part, for a whole stack or a single module, that the plates, the filament totals and the Bambu Studio project follow.
- **More inside a module:** several drawers in one module, each with its own inside, lock and geared rails, and case and drawer dividers placed on a plan.
- **A new layout** in four steps, Design, Print, Hardware and Assemble, with Undo, design files, a dark theme and store links for where you live.
Every difference is listed on [GitHub](https://github.com/doooools/vault-print-planner/blob/main/docs/differences-from-upstream.md). Amazon.com links in Hardware are still Romy's affiliate links, so US purchases keep supporting the original project. Romy's own changes are the ones marked "Romy's planner", from 2026-11-10 back.

## 2026-11-22
- **A new look:** paper and ink, swapped in the dark theme; yellow for what is selected or done, pink for the one main action of each screen, red for a problem. Titles in Anton, labels in Special Elite, text and figures in Courier Prime, all carried inside the page. Each screen puts its key thing on a taped card. Nothing you can do has changed: every button, setting and shortcut is where it was.
- **Flat faces stay flat in 3D:** the parts are now simplified keeping the way their faces turn, so the false lines that ran across flat faces from screw holes and corners are gone. Your parts are simplified again once, the first time you open the 3D view (a little slower, then cached).
- **The 3D view drawn in ink:** flat colours in two tones, the shaded sides hatched, every part outlined, a hard shadow on the ground and the selected level ringed in yellow. Picking, the camera and every tool work as before.

## 2026-11-16
- **What is counted, said in full:** to learn which steps, tools and settings serve and which don't, the visit count now also notes, once per visit, the steps opened, the tools, settings, menu items and shortcuts used, the downloads, the theme, language and window width, and the page's errors. Still no cookie, no IP address kept, no id that follows you, and nothing you name or type (no stack, file or folder names, no label text). "About" lists it all, and "Don't count this browser" there turns all of it off.

## 2026-11-15
- **Rotate:** a new button over the 3D view makes the stack turn slowly on itself, one turn in 24 seconds, until you press it again (or press R). Drag the view while it turns and it waits, then goes on from where you let go. The zoom and the point you look at stay as they are.
- **No more footer:** the notes that sat at the bottom of every page (not affiliated with USSA, the store links, the visit count, where the numbers come from) are now in "About", the last link under the page's name. "Don't count this browser" is there too. Hardware still says who earns from its store links, under the store picker.
- **A saved design keeps the whole project:** File › Save and Save as… now also write your printer, Print's plate options and stacks left out, the plates marked printed and the parts already printed, the label look, the hardware you ticked as bought, the assembly steps done, and the step you were on. Opening the file in any browser brings all of it back as it was. Files saved before still open: they bring back the stacks, loose parts and colors, and leave your progress here as it is. Your theme, store and Vault folder stay your own.
- **Save as… asks where again:** in Chrome and Edge, File › Save as… opens the save window, where you pick the folder and the name. When the browser won't open it (a setting or a company policy can block it) or the file can't be written, the design still goes to your downloads, and the message now says why instead of saying nothing. In browsers that have no save window (Firefox, Safari, Brave), Save as… asks for the file's name, then saves it to your downloads.
- **Labels on several levels at once:** with several levels selected (Ctrl+click, Shift+click), the Labels section gives every front of them the text you type, with one Undo. When their texts differ it says "Mixed"; Esc puts each one's own text back. In a module holding several drawers, each drawer gets it: name them apart one level at a time.
- **Label look:** pick the labels' font (six of them, from sans to stencil), their letter height and how far the text is raised, under the label's text in Design (the Label section of a level). They left Print's plate options. The text's color paints like any part: with Paint, click a text in the 3D view.
- **Labels on every case:** 2F and 4F cases now show their label, the drawers' one, in the slot of their front, with its text, in the 3D view.
- **Labels folded away:** the labels now have their own section in a level's settings, after Inside, folded until you open it. Its line says the label's text, or how many drawers have one.
- **Label text you can print:** the text you give a drawer or case label in Design now comes raised on that label in the Bambu Studio project and the plate files, centred on it, as a part of its own in its own filament. Pick its color under "Label text" in Paint, and its relief (0.6 mm recommended) and letter height (6 mm recommended) in Print's plate options. A text too long for its label gets smaller letters. The 3D view writes it the same size and color.
- **Export a stack for renders:** right-click the background of the 3D view, or open "File", for "Export as STL" and "Export as GLB, with colors". The file holds the stack as the view shows it, made from your own Vault files: drawers open or closed, levels spread, the roof hidden or not, every bolt. The STL is one piece in mm, Z up. The GLB keeps your colours (one material per filament), one object per part grouped by level, and the labels, in metres: in Blender, File › Import › glTF. Both are made in your browser and saved to your downloads. They are USSA's parts: keep the files for your own renders, don't share them.

## 2026-11-14
- **Select several levels:** in the 3D view, Ctrl+click (Cmd+click on a Mac) adds a level to the selection or takes it out, and Shift+click selects every level from the last one clicked. The panel then shows only the settings they all share, a setting set differently on them says "Mixed", and a change goes to all of them at once, with one Undo. Moving, copying, pasting, removing (Delete) and opening (O) work on all of them too. Ctrl and Shift + click no longer open drawers: double-click them, or press O.
- **Labels:** give each drawer and case a label, such as "M6 bolts", in the first field of its settings. In a module holding several drawers, each drawer has its own. The 3D view writes it on the front's label as you type, and the level's settings and the view's tip show it. Undo takes it back, and a copied level keeps its labels.
- **Copy and paste:** in Design, Ctrl+C copies the selected level, or the whole stack when its settings are shown. Ctrl+V pastes the level above the selected one (on top from the stack's settings), or the stack right after the selected one. A level pasted into a stack of another size takes that stack's size. The level and stack menus have Copy and Paste too.
- **Keyboard shortcuts:** press **?** (or "Shortcuts" at the top) for the list. 1 to 4 switch steps, Ctrl+S saves the design and Ctrl+O opens one. In Design, ↑ and ↓ pick the level above or below, Esc goes back to the stack's settings, Alt+↑ / Alt+↓ move the level, D adds a copy of it, A adds a level on top and Delete removes it (with Undo). In the 3D view, O opens the level's drawer or case, P switches Paint on or off, F fits the stack in the view, E spreads the levels and H hides the roof. Menus and tooltips show each key. Shortcuts never fire while you type in a field.
- **What's new and Report a bug or an idea** are back at the top, under the page's name. The story of this fork is here, in What's new.
- **Undo:** Ctrl+Z (Cmd+Z on a Mac) takes back the last change to your stacks, colours or loose parts, and Ctrl+Y or Ctrl+Shift+Z puts it back. Removing a level or a stack, painting, a colour preset, a new footprint, a filament removed or a divider plan cleared says what it did, with an Undo button. "Reset all progress" in Print can be undone too. Undo lasts until you reload the page or open a design file.
- **Right-click in the 3D view:** the level under the pointer lights up and says which it is. Right-click it to open or close its drawer or case, add a copy of it above or below, move it up or down, or remove it (one click, with Undo). Right-click the background for "Fit the stack in the view", "Add a level on top" and the stack's settings. The same level menu opens from "⋯" in the level panel, beside buttons to go to the level below or above, so everything works from the keyboard. Pick a level by clicking it in the view. The camera no longer moves by itself, "?" says how to turn, zoom and move the view, and a soft shadow under the stack replaces the floor grid.
- **Drawers on telescopic runners:** in 3D, a drawer comes out as far as the real runners let it. The box slides alone in its guides for the first half, then takes the guides out with it to the stoppers; closing, the box goes back in first.
- **Design's panels, shorter:** a level's and a stack's settings fold into sections, each saying what is set ("Drawer · 1F", "Empty · key lock · geared rails"), so a level fits on the screen. Width and depth are the first settings of the stack, under "Size and roof". Rename a stack with the pencil next to its name. Options that need another one first stay in sight, greyed, saying what they need. In a module with several drawers, one tab per drawer frames that drawer's own settings. A new case starts with an empty floor. The stack you picked and its settings are blue, so you can tell at a glance whether you are changing the whole stack or one level.
- **Painting, in one place:** with the Paint tool on, the panel on the right always shows the colours. Pick the brush under the view, one swatch per filament, with "+" to add one from Bambu Lab's colours, then "Whole stack" or "This module only". The part types fold into Outside, Inside, Mechanics and Other; "Paint these 5 Orange" paints a group. The latches between levels, the runner stoppers, the hinge rods and the runner guides each have a colour of their own now (the guides take the module's until you paint them).
- **Print, tidied up:** the selected plate comes first on the right, with "Mark as printed" under its name, then the plate options, one line each with their value. The filament filter is one line of pills with their plate counts, the bar of ticked plates shows only once you tick one, and "STL folders (.zip)" sits beside the main download. You can leave every stack out.
- **Parts you already have:** "Already printed", under the stacks in Print, lists the parts you printed before or kept from another build. Pick them among the parts on your plates, with how many: they count as printed and come off the plates.
- **Hardware, like Print:** the stacks in the list on the left, with groups to jump to, and the list options on the right. The bolt finish and the store are said once, above the list, so each line gives just the bolt (the copy and the CSV keep the full name). Each link says what it opens, "Product page" or "Search"; each group says how many of its lines you've bought; a click anywhere on a line ticks it.
- **File menu and a one-row header:** "File", at the top on every step, saves, saves as and opens design files, and says whether the file has your latest changes ("The file is 3 changes behind"). The tabs count what matters to each: Print and Assemble in %, Hardware what is left to buy. Loose parts is an entry like the stacks.
- **Light or dark, your pick:** two buttons at the top of the page switch the theme. The page starts in your system's setting and keeps the one you pick, 3D view included.
- **Support me:** a link at the top right opens this fork's Ko-fi page in a new tab. Nothing is loaded from Ko-fi until you click it.
- **Settings are buttons, not ticks:** a case's floor is Empty, Dividers or Gridfinity, and a grid divider at a wall is "Divider alone" or "Closed". Ticks are left for lists (plates, hardware bought, assembly steps). Removing a stack, a filament or a plan is a press and hold.
- **Smaller fixes:** a stack's warnings come first in its settings, with a link to the level they name; a new empty stack opens on its settings. In Print, the parts and grams at the top leave out what no longer fits your printer. After an undo, painting a single module or right-clicking in the 3D view works again.

## 2026-11-13
- **Each drawer its own inside:** in a module holding several drawers, or the two sides of an L² or XL², each drawer keeps its own interior, baseplate, grid dividers, lock and geared rails. Pick it with its tab or in the 3D view; "Same settings in every drawer" copies one to the others.
- **Grid dividers in two clicks:** click the hole where a divider starts, then where it ends, among the holes the plan marks. A click on a divider removes it.
- **The stack's outside size,** drawers closed, with its base, wheels, casters, roof and handles, in the stack's header and on the templates.
- **Pick the plates to download:** tick plates and the Bambu project, plate files and STL folders hold only those; "Mark as printed" is a button.
- **Room for the shells' supports:** module shells keep 15 mm clear above and below on their plate, for the supports Bambu Studio adds there.
- **Bolt finish:** raw steel (black) or zinc-plated and stainless (grey), shown in 3D and named in the hardware list.
- **Where you buy:** the store is guessed from your time zone first. Amazon.com links are Romy's affiliate links; Amazon.fr and Amazon.it carry this fork's tag, and the page says so beside them.
- **Loose parts** lists every part by family before you search. A case takes a Gridfinity baseplate or dividers, not both.
- **Visit count:** the page counts visits and the store links opened with GoatCounter, without loading its script: no cookie, no IP address kept, nothing about your build. The bottom of the page says what is sent, and "Don't count this browser" turns it off.

## Up to 2026-11-12 · the fork's first version
- **Your stacks in 3D,** made from your own Vault files: every drawer, case, roof, base and wheel where the assembled unit puts it, with its bolts. Turn it, spread the units apart, hide the roof. Parts are simplified in your browser and kept there for next time; nothing is uploaded.
- **Open drawers and cases in 3D:** double-click it (Ctrl and Shift + click did it too until 2026-11-14). A drawer's key turns and its racks slide before it pulls out; a case's latches flip before the lid opens, with the roof riding on it.
- **Several drawers in one module:** a 2F module can hold two 1F drawers, a 4F module two 2F, four 1F, or a 2F and two 1F in any order. Parts, bolts and geared rails are counted per drawer. The mixed ones are marked Inferred: the manuals don't show them.
- **Colors:** the Paint tool gives each kind of part a filament, for a whole stack or a single module, from your own filaments or Bambu Lab's PLA and PETG colours. Each stack keeps its own colours. Plates, filament totals and the Bambu Studio project follow them, one filament slot per colour.
- **A new layout:** Design, Print, Hardware and Assemble tabs. In Design, your stacks on the left, the 3D view in the middle, the selected level or stack on the right. Start from a template or a blank stack, and set a level across the width as L, L² or two modules side by side.
- **Print what you want:** pick the stacks, and the loose parts, to plan. The plates follow every change made in Design.
- **Hardware has its own tab:** one shopping list for the whole build, ticks for what you've bought, copy or CSV. Store links follow where you buy: pick your store by continent.
- **Save and open designs:** in Chrome and Edge, Save writes your stacks, loose parts and colours into your Vault folder, next to the part files. Save as… and Open… work anywhere; other browsers download the file.
- **Lost folder, said plainly:** when the page can no longer read your Vault folder, a popup says the 3D view needs it, with a button to reconnect it. "Later: plan without the files" or "Not now" keeps it away for the rest of the visit.
- **Bases in 3D:** the base, wheels, front foot bar and casters are drawn where they go. A base without wheels now stands on its own: no feet. A roof can sit on a top-opening case.
- **Universal handle lock and module connectors:** two parts in the Vault download the planner never offered. On M, L and XL stacks with the pull-out handle, pick the universal lock: two small locks, one per rod, that fit any printer. "Module connectors", in a stack's settings, screws a small bar over each joint between two drawer modules at the back corners. Both are drawn in 3D, with their bolts.
- **Dividers where you want them:** a case's plan seen from above fills the slots moulded in its walls with a click; a drawer's plan places grid dividers on the box's peg holes. The part list and the 3D view count the right files and edge pieces.
- **Report a bug or an idea** opens a short form on GitHub. The bug form gets your browser and printer filled in.
- **No more 10% spares:** the part list, the plates and the hardware list give exactly what the build needs. Print or buy extras yourself if you want them (Loose parts takes any single part).
- **Part counts checked against the manuals:** one label per case; the removable hidden key and its cap once per stack; one wall cleat per opening; backbones in a column on the back of the stack, as the manual has them; case bolts and backbone bolts (M4 × 80) follow the holes in the files. On an L² or XL², shared parts are listed once.
- **Fixed:** Bambu Studio projects with several colours no longer fail with "Invalid configuration file". The heavyweight roof's carry handle no longer drops out of the print list when the roof is swapped.
- **Works the same on Linux, macOS and Windows:** the files macOS adds to a copied folder are ignored, and Firefox and Safari fall back to a folder upload and downloads.

## 2026-11-10 · Romy's planner
- **Shorter drawers in taller modules:** a 2F or 4F drawer module can now hold shorter drawers, like two 1F drawers in a 2F, or two 1F drawers above a 2F in a 4F. Pick them under "Drawers inside" in step 1 (each half on its own for L²). The parts list, front bolts and stack picture follow. Thanks to the viewer who pointed out they fit.
- **Supports only where USSA asks for them:** Out of an abundance of caution, supports are now only added if USSA says "Turn On Supports" (plus the XL drawer front, which has the same lock pocket as the fronts USSA labels) since there are some facets that could use supports but aren't mandatory. The onus is on you to think through what makes sense with the part you're building.

## 2026-11-09 · Romy's planner
- **XL units really fit the H2S now:** the XL drawer and case modules and the XL bases were still marked as too big. They fit at the angle USSA exported them, and the planner now keeps them there. The XL heavyweight roofs are still too big for the H2S.
- **Closer filament estimates:** checked against the weights USSA publishes per module, the planner was reading about 17% high. It's now within a few percent.
- **Stack heights with 1F cases:** the planner listed a 1F case as 71 mm tall instead of about 66, so stack drawings and overall heights came out a little tall. Only the numbers on the page were off; the parts and print files are unchanged.
- **Assembly:** step 4 now also passes on USSA's advice to put a 2F module right under the roof when you use the base, backbones or handles.

## 2026-11-08 · Romy's planner
- **Filament per color:** step 3 shows roughly how much of each color the whole build needs, so you can check your spools before you start.
- **Labels get their own plate,** so you can add your text and print them in several colors without touching the other plates. Turn it off in step 3 to print them with the rest.
- **Manual supports go where they help:** each one prints standing against the end of a roof of the same depth. Ones with no roof to brace are left out (step 3 says which), and STL folder names say where to stand them.
- **Download names say what's inside:** the build, the printer, and which plates if some are already printed, like "Vault - 3 units in 2 stacks - P1S - plates 4-12.3mf".
- **Printer not listed?** Pick "My printer isn't listed" and type its name: the bed size for about 380 printers fills in, taken from OrcaSlicer's printer profiles. Or enter your bed size yourself. The bed size is all the planner needs.
- **Voron presets:** 2.4 and Trident (250, 300, 350) and the 0.2. Like other non-Bambu printers, they get plate files for OrcaSlicer or PrusaSlicer.

## 2026-11-07 · Romy's planner
- **More printers:** presets for Prusa (MK4/MK4S, CORE One, MINI+, XL), Creality (K1/K1C, K1 Max, K2 Plus, Ender-3 V3 SE), Elegoo (Centauri Carbon, Neptune 4 Pro and Max), Anycubic (Kobra 3, Kobra S1) and Qidi (Q1 Pro, Plus4), plus Custom size for anything else.
- **Plate files for non-Bambu printers:** step 3 now saves a zip with one standard .3mf per plate. Parts are already laid out, and the parts that need supports or a brim are already marked. Works in OrcaSlicer, PrusaSlicer and the slicers built on them; a settings.txt lists the same settings for any other slicer.
- **STL folders** now name each part's settings in its file name, with a settings.txt per plate.
- **XL units fit the H2S:** facades and backbones that are too long for the bed go on the diagonal, at whatever angle fits.
- **Missing parts are named:** if your Vault folder is missing files, step 3 lists them. File names that an unzip or a newer download changed are still matched.
- **Print and Assemble stay empty** until you add something to your build, with a button to add the unit you picked in step 1.
- **Fewer slicer conflicts:** parts with supports keep clear of neighbouring parts, the rows around them and the bed edge.

## 2026-11-06 · Romy's planner
- **First public version.**
- **More Bambu printers:** P2S, X2D, A2L, H2D Pro, H2C and H3C; plate spacing fixed on dual-nozzle printers.
- **Stack pictures:** front and side views, overall size with dimension lines, and wheels, feet, casters and handles drawn where USSA's manual puts them.
- **Step 1 checks whether a unit stacks** before adding it and offers a matching size.
- **Hardware list:** bolt head shapes, drawer front bolts counted from the holes in each front, and links to matching products.
- **Choosing the Vault folder** is its own step, with a heads-up about the browser's permission prompt.
- **Plate numbers stay put** when you mark plates as printed.
- **Tree supports** no longer run into the next part.
- **Part pictures** at full size.
