# Vault Print Planner, Dols fork

An unofficial, fan-made planner for [Vault by USSA](https://www.ussadesign.com/products/vault), the 3D-printable modular storage system. This is a fork of [Romy Macasieb's Vault Print Planner](https://github.com/rmacasieb/vault-print-planner) ([vault.romy.io](https://vault.romy.io)) that adds a 3D view of your stacks, colours, several drawers per module and a redesigned page.

Open it at **https://doooools.github.io/vault-print-planner/** (nothing to install).

Design your stacks and the planner tells you exactly which STL files to print and how many. It checks every part against your printer's bed, packs the parts onto plates, and makes a Bambu Studio project with one plate per tab (or plate files for other slicers).

> This project is not made, endorsed or supported by USSA. It contains no Vault files: it works only with your own copy of the Vault STL download, [bought from USSA](https://www.ussadesign.com/products/vault). Vault, its designs and its files belong to USSA.

## What it does

1. **Design:** build stacks level by level: drawers or top-opening cases, S to XL, L² and two modules side by side, 1F to 4F, several drawers in one 2F or 4F module, locks, interiors, roofs, a base with wheels, a foot bar or casters, handles. Start from a template or a blank stack.
   - **3D view** of the stack, made from your own Vault files: every part where the assembled unit puts it, with its bolts. Turn it, spread the units apart, hide the roof. **Ctrl** or **Shift** + click opens a drawer (its key turns, the racks slide) or a case (latches, then the lid, with the roof on it).
   - **Colors:** the Paint tool gives each kind of part (shells, fronts, boxes, latches, labels…) a filament, for the whole stack or for one module, from your filaments or Bambu Lab's PLA and PETG colours.
2. **Print:** pick the stacks to print. Parts are packed onto plates by colour, under one 1 kg spool each, kept apart when they need supports. Press **Download the Bambu Studio project**: one `.3mf` with every plate as its own tab, with supports, walls and brims already set where the parts need them. Other printers get a zip with one `.3mf` per plate, or STL folders.
3. **Hardware:** one shopping list for the whole build, each bolt with its head shape, a tick when bought, copy or CSV.
4. **Assemble:** a checklist that follows USSA's manuals, stack by stack.

Save a design to a file and open it again later (Chrome and Edge save it straight into your Vault folder, next to the part files).

## Your files stay on your computer

The page runs entirely in your browser. It reads the part files from your Vault folder on your own computer and never uploads them. Your stacks, colours and progress are saved in your browser; simplified 3D parts are cached there too. The 3D view loads three.js and meshoptimizer from jsDelivr when you open it; nothing else is fetched.

## Requirements

- The Vault STL download, release **261021** (folder `261021_VAULT_USSA_S`). Other releases may rename files: the planner matches names loosely and tells you which parts it can't find.
- A desktop browser:

  | | Chrome, Edge (and other Chromium browsers) | Firefox, Safari |
  |---|---|---|
  | Open the Vault folder | Remembered between visits | Asked each visit (folder upload) |
  | 3D view, Print files | Yes | Yes |
  | Save a design | Into the Vault folder, or anywhere | Downloaded |
  | Open a design | File picker, starting in the Vault folder | File picker |

- Bambu Studio projects come with settings for the P1S, P2S, X1C, X2D, P1P, A1, A1 mini, A2L, H2S, H2D, H2D Pro, H2C and H3C (0.4 mm nozzle, 0.20 mm Standard, PLA Basic; dual-nozzle printers use the left nozzle). Other printers get bed-fit checks, plate plans and plate files.

Linux, macOS and Windows all work: file names are matched without regard to case, Unicode form or folder separators, and the files macOS adds to a copied folder (`__MACOSX`, `._name`) are ignored.

## Changing it

The page is one HTML file, `index.html`, built from `src/` (Python 3, no dependencies):

```bash
python3 src/build.py --public src/stl-measurements.tsv index.html previews/index.tsv
```

| File | What it holds |
|---|---|
| `src/rules.js` | Which files and how many each unit needs, and its bolts |
| `src/template.html` | The page itself |
| `src/stl-measurements.tsv` | Footprint, height, volume and export angle of every STL, measured from the files |
| `src/stl-placements.json` | Where each part goes in an assembled unit, for the 3D view (numbers only, made with `tools/placements/`) |
| `src/bambu-settings/<printer>.json` | The full project settings Bambu Studio saves for each printer |
| `src/bambu-colors.tsv`, `src/printer-beds.tsv` | Bambu Lab's filament colours; bed sizes from OrcaSlicer's printer profiles |
| `previews/` | Small pictures of every part, listed in `previews/index.tsv` |

`node src/validate.js <file with one STL path per line>` checks every unit's files against a list of the download's files. `tools/placements/README.md` explains how the 3D placements are measured and regenerated (Blender).

## Credits and license

The planner is [Romy Macasieb's](https://github.com/rmacasieb/vault-print-planner); this fork is maintained by [Dols](https://github.com/doooools/vault-print-planner). The code is MIT licensed (see `LICENSE`). Vault, its designs and its STL files belong to USSA and are not covered by this license.
