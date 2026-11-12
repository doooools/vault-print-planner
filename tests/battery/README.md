# Part-count test battery

Checks the number of parts the planner tells you to print against an oracle written only from USSA's material (the
STL tree and the four manuals), without looking at the planner. Results, in French: `RESULTATS.md` (battery 1,
14 configurations), `RESULTATS2.md` (battery 2, 28 configurations on an H2S, and the fixes).

- `expected.json` / `expected2.json` (+ `.md`): the oracle's lists, frozen before any comparison (`expected.sha256`).
- `corrections.py` → `expected_corrected.json`, `expected2_corrected.json`, `corrections.md`: the oracle with the
  rules the user confirmed afterwards (runners per F, one removable hidden key and cap per stack, backbone column).
- `planner/*.json`: the page's output for every configuration (print list, every plate, Design lists), after the fixes;
  `before_fix/`: the same before them.
- `check_plates.py` → `plate_checks.md`: copies on plates = list quantity, parts inside the bed, no overlap, oversized
  parts flagged.
- `compare.py [1c|2|2c]` → `comparison*_raw.md`: oracle vs planner, without the planner's +10 % spares.
- `harness/`: the test server (`VAULT_DOWNLOAD=<folder> python -I serve.py 8913`), a stand-in for the folder picker
  (`fakefolder.js`), the page driver (`driver.js`, `T.capture`) and the recipes that build each configuration by clicking
  the page's own controls (`battery1.js`, `battery2.js`). Load the page in a same-origin iframe, eval the three scripts
  in it, then `B1.run('C01')` or `B2.run('D01')`.

No USSA geometry here: only file paths, counts and sizes measured from the files.
