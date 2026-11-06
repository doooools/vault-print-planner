# Vault Print Planner

An unofficial, fan-made planner for [Vault by USSA](https://www.ussadesign.com/products/vault), the 3D-printable modular storage system.

Pick a unit and the planner tells you exactly which STL files to print and how many. You can stack units into towers and check every part against your printer's bed. It packs the parts onto plates and makes a Bambu Studio project with one plate per tab.

**Use it:** [open the planner](https://rmacasieb.github.io/vault-print-planner/). It runs entirely in your browser.

> This project is not made, endorsed or supported by USSA. It contains no Vault STL files: you need your own copy, [bought from USSA](https://www.ussadesign.com/products/vault).

## What it does

1. **Design a unit:** choose the width, depth, height, drawer or case, lock, roof and so on. You get the exact files and counts, with a flag on any part too big for your printer.
2. **Build:** stack units into towers with a base, feet, wheels and a roof. You can also add single parts, like a spare roof or latch.
3. **Print:** parts are packed onto plates, kept under one 1 kg spool and grouped by color and by whether they need supports. Press **Make Bambu Studio project** and pick your Vault download folder. You get one `.3mf` with every plate as its own tab, with these settings already in place:
   - supports on for the parts whose files ask for them, and for every part Bambu Studio warns about when sliced without supports (each of the 733 files was sliced to check)
   - more walls on parts that carry load or take bolts
   - a brim on tall, thin parts
   - plates clear of the printer's no-print corner

   On other printers, save STL folders instead: a zip with one folder per plate.
4. **Assemble:** a checklist that follows the manuals, plus a hardware shopping list.

Your files are read on your own computer and never uploaded. Your towers and progress are saved in your browser.

## Requirements

- The Vault STL download, release **261021** (folder `261021_VAULT_USSA_S`). Other releases may rename files, and the planner will say which parts it can't find.
- A desktop browser. Chrome or Edge works best and remembers your Vault folder. Safari and Firefox work too, but ask for the folder each time.
- Bambu Studio projects come with settings for these printers: P1S, X1C, P1P, A1, A1 mini, H2S and H2D (single nozzle). Each uses the 0.4 mm nozzle, 0.20 mm Standard and PLA Basic. Other printers still get bed-fit checks and plate plans.

## No support

I built this for my own Vault build and am sharing it as is. I don't plan to maintain it, answer questions or take feature requests. If something's wrong or you want it to work differently, fork it and change it; it's all here.

If it saved you some time, you can [buy me a coffee](https://ko-fi.com/E8R32A64D1).

## Changing it

The page is one HTML file, `index.html`, built from `src/`:

| File | What it holds |
|---|---|
| `src/rules.js` | Which files and how many each unit needs |
| `src/template.html` | The page itself |
| `src/stl-measurements.tsv` | Footprint, height, volume and export angle of every STL, measured from the files |
| `src/bambu-settings/<printer>.json` | The full project settings Bambu Studio saves for each printer |
| `previews/` | Small pictures of every part, 8 per row in each sheet, listed in `previews/index.tsv` |
| `src/build.py` | Puts it all together |

Rebuild after editing:

```bash
python3 src/build.py --public src/stl-measurements.tsv index.html previews/index.tsv
```

`node src/validate.js <list of STL paths>` checks that every unit's files exist in a given file list. To add a Bambu printer, save a one-part project for it in Bambu Studio, copy `Metadata/project_settings.config` out of the `.3mf` into `src/bambu-settings/<id>.json`, and add the printer to `PRINTERS` in `src/template.html`.

## License

The code is MIT licensed (see `LICENSE`). Vault, its designs and its STL files belong to USSA and are not covered by this license.
