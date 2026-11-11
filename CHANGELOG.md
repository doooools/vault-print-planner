# What's new

Changes to the Vault Print Planner at [vault.romy.io](https://vault.romy.io), newest first.

## 2026-11-10
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
