# Oracle vs planner (raw)

| config | expected copies | planner copies | gaps |
|---|---|---|---|
| D01 | 24 | 24 | 0 |
| D02 | 36 | 36 | 0 |
| D03 | 18 | 18 | 0 |
| D04 | 36 | 36 | 0 |
| D05 | 51 | 51 | 0 |
| D06 | 22 | 22 | 0 |
| D07 | 36 | 36 | 0 |
| D08 | 63 | 63 | 0 |
| D09 | 20 | 20 | 0 |
| D10 | 20 | 20 | 0 |
| D11 | 32 | 32 | 0 |
| D12 | 48 | 48 | 0 |
| D13 | 18 | 18 | 0 |
| D14 | 18 | 18 | 0 |
| D15 | 19 | 18 | 3 |
| D16 | 13 | 13 | 0 |
| D17 | 13 | 13 | 0 |
| D18 | 49 | 49 | 0 |
| D19 | 81 | 81 | 0 |
| D20 | 40 | 40 | 0 |
| D21 | 102 | 102 | 0 |
| D22 | 31 | 31 | 0 |
| D23 | 25 | 25 | 0 |
| D24 | 20 | 20 | 0 |
| D25 | 18 | 18 | 0 |
| D26 | 17 | 17 | 0 |
| D27 | 43 | 43 | 0 |
| D28 | 18 | 18 | 0 |

## D01 (D01)
expected 24 copies / 13 files; planner 24 copies (+ spares) / 13 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S2F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S3/Boxes/S3 Box 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S3/Modules/S3 Module 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/01. S Families/S3/Roofs/S3 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 3 | 3 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL S2F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | high M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 4 | 4 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x3 Runner Guide.stl | 4 | 4 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x3 Runner Slide.stl | 4 | 4 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |

Oracle notes: S3 2F module, one S3 2F box. Runners per F of the module: 2 packs (4 guides, 4 slides, 4 stoppers). Single drawer: no geared rails. S2F facade: 3 caps.

## D02 (D02)
expected 36 copies / 13 files; planner 36 copies (+ spares) / 13 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S4F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S5/Boxes/S5 Box 4F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S5/Modules/S5 Module 4F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/01. S Families/S5/Roofs/S5 Table Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 3 | 3 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL S4F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | high M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 8 | 8 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 4F module: 4 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x5 Runner Guide.stl | 8 | 8 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 4F module: 4 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x5 Runner Slide.stl | 8 | 8 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 4F module: 4 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |

Oracle notes: S5 4F module, one S5 4F box, 4 runner packs (8/8/8). S4F facade: 3 caps. S5 Table Roof.

## D03 (D03)
expected 18 copies / 13 files; planner 18 copies (+ spares) / 13 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/02. M Families/Facades/M1F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/02. M Families/M3/Boxes/M3 Box 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/02. M Families/M3/Modules/M3 Module 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/02. M Families/M3/Roofs/M3 Bowl Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 3 | 3 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL M1F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 2 | 2 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x3 Runner Guide.stl | 2 | 2 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x3 Runner Slide.stl | 2 | 2 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |

Oracle notes: M3 1F drawer, M1F facade 3 caps, M3 Bowl Roof.

## D04 (D04)
expected 36 copies / 16 files; planner 36 copies (+ spares) / 16 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/02. M Families/Facades/M1F (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/02. M Families/M6/Boxes/M6 Box 1F.stl | 2 | 2 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/02. M Families/M6/Modules/M6 Module 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/02. M Families/M6/Roofs/M6 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 6 | 6 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL M1F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Geared Rails/M Rails.stl | 2 | 2 |  | ok | high M02 p.4 step 5: geared rails required when more than one box shares a 2F/4F module; one file (top + bottom rail) per box  |
| 01. DRAWERS/07. Universal/Hidden Key (Turn On Supports).stl | 2 | 2 |  | ok | high User rule: the hidden key facade part is one per drawer (replaces Key). File name; no manual page. Replaces Key (Turn On Supports). |
| 01. DRAWERS/07. Universal/Hidden Key Part 2 (Turn on Supports).stl | 1 | 1 |  | ok | high User rule: the removable hidden key is one per stack, shared by all hidden-key drawers of the stack  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | medium Evidence from the STLs: the top tab of Hidden Key Part 2 (27.7 x 9.8 mm) is identical to the tab of "Handle Lock Knob Part 1", which M04 p.13 step 16 caps with "Handle Lock Knob Part 2"; that cap has the same size and mesh as "Key Cap" (37.8 x 13.2 x 11.7). So the removable hidden key takes one Key Cap. Reading A (chosen): 1 Key Cap per Hidden Key Part 2. Reading B (coordinator default): 0. |
| 01. DRAWERS/07. Universal/Label.stl | 2 | 2 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 4 | 4 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x6 Runner Guide.stl | 4 | 4 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x6 Runner Slide.stl | 4 | 4 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 2 | 2 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |
| 01. DRAWERS/07. Universal/Top Handle (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Top Handle on the grid roof; M01 p.18 Asked for by the config. |

Oracle notes: M6 2F module with two M6 1F boxes: geared rails required (2 x M Rails). Hidden key: 2 x Hidden Key (one per drawer), 1 x Hidden Key Part 2 (one per stack), 1 Key Cap on that removable key (evidence: see the part note; alternative 0). Runners: 2 packs. Caps 3 + 3.

## D05 (D05)
expected 51 copies / 14 files; planner 51 copies (+ spares) / 14 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/02. M Families/Facades/M2F (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/02. M Families/M7/Boxes/M7 Box 2F.stl | 2 | 2 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/02. M Families/M7/Modules/M7 Module 4F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/02. M Families/M7/Roofs/M7 Under Table Mount Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 10 | 10 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL M2F facade: 5 cap(s). |
| 01. DRAWERS/07. Universal/Geared Rails/M Rails.stl | 2 | 2 |  | ok | high M02 p.4 step 5: geared rails required when more than one box shares a 2F/4F module; one file (top + bottom rail) per box  |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 2 | 2 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 2 | 2 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 8 | 8 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 4F module: 4 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x7 Runner Guide.stl | 8 | 8 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 4F module: 4 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x7 Runner Slide.stl | 8 | 8 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 4F module: 4 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 2 | 2 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |

Oracle notes: M7 4F module, two M7 2F boxes: geared rails required (2 x M Rails). 4 runner packs (8/8/8, x7). M2F facades 5 + 5 caps. M7 Under Table Mount Roof.

## D06 (D06)
expected 22 copies / 15 files; planner 22 copies (+ spares) / 15 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/03. L Families/Facades/L1F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/03. L Families/L3/Boxes/L3 Box 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/03. L Families/L3/Modules/L3 Module 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/03. L Families/L3/Roofs/L3 Heawyweight Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 3 | 3 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL L1F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Heawyweight Roof Handle.stl | 1 | 1 |  | ok | high M01 p.10 (bar between the two bins); file name  |
| 01. DRAWERS/07. Universal/Heawyweight Roof Insert.stl | 2 | 2 |  | ok | low File name only; one insert per bar end (2 bin walls) Undocumented. Reading B: 1. |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 2 | 2 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x3 Runner Guide.stl | 2 | 2 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x3 Runner Slide.stl | 2 | 2 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |

Oracle notes: L3 1F drawer (L module: 2 latches), L1F facade 3 caps, L3 Heawyweight Roof (no "Cut" variant for L) + 1 roof handle bar + 2 inserts (low).

## D07 (D07)
expected 36 copies / 14 files; planner 36 copies (+ spares) / 14 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/03. L Families/Facades/L1F (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/03. L Families/L6/Boxes/L6 Box 1F.stl | 2 | 2 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/03. L Families/L6/Modules/L6 Module 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/03. L Families/L6/Roofs/L6 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 6 | 6 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL L1F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Geared Rails/L Rails.stl | 2 | 2 |  | ok | high M02 p.4 step 5: geared rails required when more than one box shares a 2F/4F module; one file (top + bottom rail) per box  |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 2 | 2 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 2 | 2 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 4 | 4 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x6 Runner Guide.stl | 4 | 4 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x6 Runner Slide.stl | 4 | 4 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 2 | 2 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |

Oracle notes: L6 2F module, two L6 1F boxes: 2 x L Rails. 2 runner packs (x6). Caps 3 + 3. 2 latches.

## D08 (D08)
expected 63 copies / 17 files; planner 63 copies (+ spares) / 17 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/03. L Families/Facades/L1F (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/03. L Families/Facades/L2F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/03. L Families/L7/Boxes/L7 Box 1F.stl | 2 | 2 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/03. L Families/L7/Boxes/L7 Box 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/03. L Families/L7/Gridfinity Baseplate/L7 Baseplate.stl | 3 | 3 |  | ok | medium M01 p.9 Interiors (gridfinity base); M01 p.11 S3 Baseplate; one per box One per box. The L7 folder has a single baseplate file (no "_With Handles" variants as in S/M); it is 25.85 mm tall like the S/M "_With Handles" files, so the "no handle cut-outs" choice is not offered for L. |
| 01. DRAWERS/03. L Families/L7/Modules/L7 Module 4F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/03. L Families/L7/Roofs/L7 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 11 | 11 | 2 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL L1F facade: 3 cap(s). L2F facade: 5 cap(s). |
| 01. DRAWERS/07. Universal/Geared Rails/L Rails.stl | 3 | 3 |  | ok | high M02 p.4 step 5: geared rails required when more than one box shares a 2F/4F module; one file (top + bottom rail) per box  |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 3 | 3 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 3 | 3 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 3 | 3 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 8 | 8 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 4F module: 4 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x7 Runner Guide.stl | 8 | 8 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 4F module: 4 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x7 Runner Slide.stl | 8 | 8 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 4F module: 4 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 3 | 3 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |

Oracle notes: L7 4F module holding 1F + 2F + 1F: 3 boxes, 3 x L Rails, 4 runner packs (8/8/8, x7), caps 3 + 5 + 3 = 11, 3 baseplates (one per box), 2 latches.

## D09 (D09)
expected 20 copies / 14 files; planner 20 copies (+ spares) / 14 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/05. XL Families/XL Facade 1F.stl | 1 | 1 |  | ok | high M02 p.1 step 1, p.6 step 7; only XL drawer facade  |
| 01. DRAWERS/05. XL Families/XL5/Boxes/XL5 Back Panel.stl | 1 | 1 |  | ok | medium File name / folder: the XL3-XL5 Boxes folders hold Box 1F + Back Panel (the box is exported open-backed). Not shown in the manuals. One back panel per XL box (XL3-XL5). |
| 01. DRAWERS/05. XL Families/XL5/Boxes/XL5 Box 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10; file name  |
| 01. DRAWERS/05. XL Families/XL5/Modules/XL5 Module 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/05. XL Families/XL5/Roofs/XL5 Table Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 3 | 3 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL XL1F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 2 | 2 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/XL Runners/x5 Runner Guide XL.stl | 2 | 2 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F); XL Runners subfolder for XL 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/XL Runners/x5 Runner Slide XL.stl | 2 | 2 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |

Oracle notes: XL5 1F: box + back panel, XL Facade 1F (3 caps), XL runners x5 (1 pack), 2 latches, XL5 Table Roof.

## D10 (D10)
expected 20 copies / 14 files; planner 20 copies (+ spares) / 14 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/05. XL Families/XL Facade 1F.stl | 1 | 1 |  | ok | high M02 p.1 step 1, p.6 step 7; only XL drawer facade  |
| 01. DRAWERS/05. XL Families/XL6/Boxes/XL6 Box 1F Part 1.stl | 1 | 1 |  | ok | high File names: the XL6 box only comes split (Part 1 + Part 2); no whole file exists  |
| 01. DRAWERS/05. XL Families/XL6/Boxes/XL6 Box 1F Part 2.stl | 1 | 1 |  | ok | high File names (split box)  |
| 01. DRAWERS/05. XL Families/XL6/Modules/XL6 Module 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/05. XL Families/XL6/Roofs/XL6 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 3 | 3 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL XL1F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 2 | 2 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/XL Runners/x6 Runner Guide XL.stl | 2 | 2 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F); XL Runners subfolder for XL 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/XL Runners/x6 Runner Slide XL.stl | 2 | 2 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |

Oracle notes: XL6 1F: the box only exists split (Part 1 + Part 2, no back panel file in XL6). XL runners x6 (1 pack), 2 latches, XL6 Grid Roof.

## D11 (D11)
expected 32 copies / 15 files; planner 32 copies (+ spares) / 15 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S1F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S4/Boxes/S4 Box 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/02. M Families/Facades/M1F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/02. M Families/M4/Boxes/M4 Box 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/05. XL Families/XL4/Roofs/XL4 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/06. XL┬▓ Families/XL4┬▓/XL4┬▓ Module 1F.stl | 1 | 1 |  | ok | high File name / folder (06. XL2 Families); front measured: two bays, 246 mm (M) and 157 mm (S) wide Folder spelt "XL┬▓" on disk. |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 4 | 4 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL S1F facade: 1 cap(s). M1F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 2 | 2 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 2 | 2 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | medium Latch pockets under the XL2 module counted on the STL (2, like XL)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 4 | 4 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Guide.stl | 4 | 4 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Slide.stl | 4 | 4 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 2 | 2 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |

Oracle notes: XL²4 1F: one XL-wide shell with an S bay and an M bay; the XL2 folders hold only modules, so each bay takes the S4 / M4 drawer kit (box, facade, key...). One runner pack per bay (x4 runners are the same for S and M). No geared rails (one box per bay). No accessories exist for XL2. XL4 Grid Roof.

## D12 (D12)
expected 48 copies / 15 files; planner 48 copies (+ spares) / 15 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S2F (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S5/Boxes/S5 Box 2F.stl | 2 | 2 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/03. L Families/L5/Roofs/L5 Bowl Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/04. L┬▓ Families/L5┬▓/L5┬▓ Module 2F.stl | 1 | 1 |  | ok | high File name / folder (04. L2 Families); front measured: two S-wide bays Folder spelt "L┬▓" on disk. |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 6 | 6 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL S2F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 2 | 2 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 2 | 2 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | medium Latch pockets under the L2 module counted on the STL (2)  |
| 01. DRAWERS/07. Universal/L┬▓ Accessories/x5 Accessory 1st.stl | 1 | 1 |  | ok | low File name/folder only (07. Universal/L2 Accessories); no manual page Purpose undocumented; assumed one per L2 module of depth 5. Reading B: 0. |
| 01. DRAWERS/07. Universal/L┬▓ Accessories/x5 Accessory 2nd.stl | 1 | 1 |  | ok | low File name/folder only; no manual page Purpose undocumented; assumed one per L2 module of depth 5. Reading B: 0. |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 8 | 8 | 1 | ok | medium User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module, 2 bays: 4 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x5 Runner Guide.stl | 8 | 8 |  | ok | medium User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module, 2 bays: 4 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x5 Runner Slide.stl | 8 | 8 |  | ok | medium User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module, 2 bays: 4 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 2 | 2 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |

Oracle notes: L²5 2F: L-wide shell with two S bays; two S5 2F drawer kits (S2F facades 3 + 3 caps). Runners: per F per bay = 2 bays x 2F = 4 packs (8/8/8, x5), medium (the rule was given per module; an L2 module has a runner column per bay). No rails (one box per bay). L2 accessories low. L5 Bowl Roof (no L2 roofs exist).

## D13 (D13)
expected 18 copies / 13 files; planner 18 copies (+ spares) / 13 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/03. L Families/L4/Roofs/L4 Grid Roof.stl | 1 | 1 |  | ok | high Config: stated roof on top of the case; the case keeps its own lid (coordinator convention). Drawers roof of the same footprint.  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | low Not in M01 p.12, but the case module carries the same latch pocket(s) as a drawer module of its width (STL) Reading A (chosen): 2 per L case, like a drawer module. Reading B: 0. |
| 02. SUSTAINERS/03. L Families/Facades/L1F Facade.stl | 1 | 1 |  | ok | medium M01 p.12 (L1F / L2F Facade on the case front) Equivalent alternative: 02. SUSTAINERS/05. Universal/Facades/L1F.stl (same size and outline). Print one of the two. |
| 02. SUSTAINERS/03. L Families/L4/Modules/L4 1F Flat Module.stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 1F Dividers Module, L3 2F Sealed Module); file name Flat variant. |
| 02. SUSTAINERS/03. L Families/L4/Roof/L4 Roof.stl | 1 | 1 |  | ok | high M01 p.12 (L3 Roof = the hinged lid); M01 p.5 The case lid (sustainer roof). |
| 02. SUSTAINERS/05. Universal/Hinges/L-XL 1F Hinge.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL 1F Hinge / L 2-4F Hinge); M01 p.17; file holds the 2 hinges of one case (2 bodies)  |
| 02. SUSTAINERS/05. Universal/Hinges/L-XL Hinge Top.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL Hinge Top); file name (S/M: one long piece; L-XL: 2 pieces in one file)  |
| 02. SUSTAINERS/05. Universal/Label for Sustainers.stl | 1 | 1 |  | ok | high M01 p.12: 1F case uses "Label for Sustainers"; one label per case (coordinator convention)  |
| 02. SUSTAINERS/05. Universal/Locks/1 SET OF PINS FOR 1 LOCK.stl | 2 | 2 | 1 | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK HOLDER.stl | 2 | 2 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK INNER PART.stl | 2 | 2 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK OUTER PART 1F.stl | 2 | 2 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Rods/L-XL Rods.stl | 1 | 1 | 1 | ok | medium M01 p.12 (L-XL Rods); file holds 2 rods (2 bodies)  |

Oracle notes: L4 1F Flat case: lid L4 Roof, L1F case facade, L-XL 1F Hinge, L-XL Hinge Top, L-XL Rods, 2 lock sets (L/XL cases have two locks, M01 p.8 and the naming page p.12), Label for Sustainers, 2 latches (low), L4 Grid Roof on top.

## D14 (D14)
expected 18 copies / 13 files; planner 18 copies (+ spares) / 13 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/03. L Families/L5/Roofs/L5 Table Roof.stl | 1 | 1 |  | ok | high Config: stated roof on top of the case; the case keeps its own lid (coordinator convention). Drawers roof of the same footprint.  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.12: 2F/4F case uses the drawers "Label"; one label per case  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | low Not in M01 p.12, but the case module carries the same latch pocket(s) as a drawer module of its width (STL) Reading A (chosen): 2 per L case, like a drawer module. Reading B: 0. |
| 02. SUSTAINERS/03. L Families/Facades/L2F Facade.stl | 1 | 1 |  | ok | medium M01 p.12 (L1F / L2F Facade on the case front) Equivalent alternative: 02. SUSTAINERS/05. Universal/Facades/L2F.stl (same size and outline). Print one of the two. |
| 02. SUSTAINERS/03. L Families/L5/Modules/L5 2F Dividers Module.stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 1F Dividers Module, L3 2F Sealed Module); file name Dividers variant. |
| 02. SUSTAINERS/03. L Families/L5/Roofs/L5 Roof.stl | 1 | 1 |  | ok | high M01 p.12 (L3 Roof = the hinged lid); M01 p.5 The case lid (sustainer roof). |
| 02. SUSTAINERS/05. Universal/Hinges/L 2-4F Hinge.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL 1F Hinge / L 2-4F Hinge); M01 p.17; file holds the 2 hinges of one case (2 bodies)  |
| 02. SUSTAINERS/05. Universal/Hinges/L-XL Hinge Top.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL Hinge Top); file name (S/M: one long piece; L-XL: 2 pieces in one file)  |
| 02. SUSTAINERS/05. Universal/Locks/1 SET OF PINS FOR 1 LOCK.stl | 2 | 2 | 1 | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK HOLDER.stl | 2 | 2 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK INNER PART.stl | 2 | 2 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK OUTER PART 2-4F.stl | 2 | 2 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Rods/L-XL Rods.stl | 1 | 1 | 1 | ok | medium M01 p.12 (L-XL Rods); file holds 2 rods (2 bodies)  |

Oracle notes: L5 2F Dividers case module (slotted walls), no divider pieces. 2F: L 2-4F Hinge, LOCK OUTER PART 2-4F x2, the drawers Label. L5 Table Roof on top of the L5 Roof lid.

## D15 (D15)
expected 19 copies / 14 files; planner 18 copies (+ spares) / 13 files; 3 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/05. XL Families/XL3/Roofs/XL3 Grid Roof.stl | 1 | 1 |  | ok | high Config: stated roof on top of the case; the case keeps its own lid (coordinator convention). Drawers roof of the same footprint.  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | low Not in M01 p.12, but the case module carries the same latch pocket(s) as a drawer module of its width (STL) Reading A (chosen): 2 per XL case, like a drawer module. Reading B: 0. |
| 02. SUSTAINERS/01. S Families/Facades/S1F Facade.stl | 1 | 0 |  | **GAP** | low No XL case facade exists in the download; XL width (418.8 mm) = S facade (164.8) + M facade (254.0) exactly, as XL = S + M (M01 p.8) Reading A (chosen): S1F + M1F case facades side by side. Reading B: a missing XL facade file (report as not available). |
| 02. SUSTAINERS/02. M Families/Facades/M1F Facade.stl | 1 | 0 |  | **GAP** | low No XL case facade exists in the download; XL width (418.8 mm) = S facade (164.8) + M facade (254.0) exactly, as XL = S + M (M01 p.8) Reading A (chosen): S1F + M1F case facades side by side. Reading B: a missing XL facade file (report as not available). |
| 02. SUSTAINERS/04. XL Families/XL1F Facade.stl | 0 | 1 |  | **GAP** |    |
| 02. SUSTAINERS/04. XL Families/XL3/Modules/XL3 1F Sealed Module.stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 1F Dividers Module, L3 2F Sealed Module); file name Sealed variant. |
| 02. SUSTAINERS/04. XL Families/XL3/Roofs/XL3  Roof.stl | 1 | 1 |  | ok | high M01 p.12 (L3 Roof = the hinged lid); M01 p.5 The case lid (sustainer roof). |
| 02. SUSTAINERS/05. Universal/Hinges/L-XL 1F Hinge.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL 1F Hinge / L 2-4F Hinge); M01 p.17; file holds the 2 hinges of one case (2 bodies)  |
| 02. SUSTAINERS/05. Universal/Hinges/L-XL Hinge Top.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL Hinge Top); file name (S/M: one long piece; L-XL: 2 pieces in one file)  |
| 02. SUSTAINERS/05. Universal/Label for Sustainers.stl | 1 | 1 |  | ok | high M01 p.12: 1F case uses "Label for Sustainers"; one label per case (coordinator convention)  |
| 02. SUSTAINERS/05. Universal/Locks/1 SET OF PINS FOR 1 LOCK.stl | 2 | 2 | 1 | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per XL case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK HOLDER.stl | 2 | 2 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per XL case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK INNER PART.stl | 2 | 2 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per XL case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK OUTER PART 1F.stl | 2 | 2 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per XL case. |
| 02. SUSTAINERS/05. Universal/Rods/L-XL Rods.stl | 1 | 1 | 1 | ok | medium M01 p.12 (L-XL Rods); file holds 2 rods (2 bodies)  |

Oracle notes: XL3 1F Sealed case module, no seal dividers. Lid "XL3  Roof.stl" (two spaces in the name). No XL case facade exists: S1F + M1F case facades (low). L-XL hinge set, 2 locks, Label for Sustainers, 2 latches (low), XL3 Grid Roof.

## D16 (D16)
expected 13 copies / 13 files; planner 13 copies (+ spares) / 13 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/02. M Families/M6/Roofs/M6 Grid Roof.stl | 1 | 1 |  | ok | high Config: stated roof on top of the case; the case keeps its own lid (coordinator convention). Drawers roof of the same footprint.  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.12: 2F/4F case uses the drawers "Label"; one label per case  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | low Not in M01 p.12, but the case module carries the same latch pocket(s) as a drawer module of its width (STL) Reading A (chosen): 1 per M case, like a drawer module. Reading B: 0. |
| 02. SUSTAINERS/02. M Families/Facades/M2F Facade.stl | 1 | 1 |  | ok | medium M01 p.12 (L1F / L2F Facade on the case front) Equivalent alternative: 02. SUSTAINERS/05. Universal/Facades/M2F.stl (same size and outline). Print one of the two. |
| 02. SUSTAINERS/02. M Families/M6/Modules/M6 2F Module .stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 1F Dividers Module, L3 2F Sealed Module); file name S/M cases come only as one (flat) module per height. |
| 02. SUSTAINERS/02. M Families/M6/Roofs/M6 Roof Whole.stl | 1 | 1 |  | ok | high M01 p.12 (L3 Roof = the lid); "Whole" file chosen because it fits the H2S bed (340 x 320 x 340) in some rotation (measured) Split alternative: Part 1 + Part 2 + Connector For Split Roof. |
| 02. SUSTAINERS/05. Universal/Hinges/M Hinge Top.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL Hinge Top); file name (S/M: one long piece; L-XL: 2 pieces in one file)  |
| 02. SUSTAINERS/05. Universal/Hinges/S-M 2-4F Hinge.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL 1F Hinge / L 2-4F Hinge); M01 p.17; file holds the 2 hinges of one case (2 bodies)  |
| 02. SUSTAINERS/05. Universal/Locks/1 SET OF PINS FOR 1 LOCK.stl | 1 | 1 | 1 | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 1 lock(s) per M case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK HOLDER.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 1 lock(s) per M case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK INNER PART.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 1 lock(s) per M case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK OUTER PART 2-4F.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 1 lock(s) per M case. |
| 02. SUSTAINERS/05. Universal/Rods/S-M Rods.stl | 1 | 1 | 1 | ok | medium M01 p.12 (L-XL Rods); file holds 2 rods (2 bodies)  |

Oracle notes: M6 2F case (the only M module). Lid: M6 Roof Whole or split, chosen by H2S fit (see part). S-M 2-4F Hinge, M Hinge Top, S-M Rods, 1 lock (outer 2-4F), drawers Label, 1 latch (low), M6 Grid Roof.

## D17 (D17)
expected 13 copies / 13 files; planner 13 copies (+ spares) / 13 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/S4/Roofs/S4 Grid Roof.stl | 1 | 1 |  | ok | high Config: stated roof on top of the case; the case keeps its own lid (coordinator convention). Drawers roof of the same footprint.  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.12: 2F/4F case uses the drawers "Label"; one label per case  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | low Not in M01 p.12, but the case module carries the same latch pocket(s) as a drawer module of its width (STL) Reading A (chosen): 1 per S case, like a drawer module. Reading B: 0. |
| 02. SUSTAINERS/01. S Families/Facades/S4F Facade.stl | 1 | 1 |  | ok | medium M01 p.12 (L1F / L2F Facade on the case front) Equivalent alternative: 02. SUSTAINERS/05. Universal/Facades/S4F.stl (same size and outline). Print one of the two. |
| 02. SUSTAINERS/01. S Families/S4/Modules/S4 4F Module.stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 1F Dividers Module, L3 2F Sealed Module); file name S/M cases come only as one (flat) module per height. |
| 02. SUSTAINERS/01. S Families/S4/Roof/S4 Roof.stl | 1 | 1 |  | ok | high M01 p.12 (L3 Roof = the hinged lid); M01 p.5 The case lid (sustainer roof). |
| 02. SUSTAINERS/05. Universal/Hinges/S Hinge Top.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL Hinge Top); file name (S/M: one long piece; L-XL: 2 pieces in one file)  |
| 02. SUSTAINERS/05. Universal/Hinges/S-M 2-4F Hinge.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL 1F Hinge / L 2-4F Hinge); M01 p.17; file holds the 2 hinges of one case (2 bodies)  |
| 02. SUSTAINERS/05. Universal/Locks/1 SET OF PINS FOR 1 LOCK.stl | 1 | 1 | 1 | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 1 lock(s) per S case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK HOLDER.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 1 lock(s) per S case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK INNER PART.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 1 lock(s) per S case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK OUTER PART 2-4F.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 1 lock(s) per S case. |
| 02. SUSTAINERS/05. Universal/Rods/S-M Rods.stl | 1 | 1 | 1 | ok | medium M01 p.12 (L-XL Rods); file holds 2 rods (2 bodies)  |

Oracle notes: S4 4F case: S4 Roof lid, S4F Facade, S-M 2-4F Hinge, S Hinge Top, S-M Rods, 1 lock (outer 2-4F), drawers Label, 1 latch (low), S4 Grid Roof.

## D18 (D18)
expected 49 copies / 16 files; planner 49 copies (+ spares) / 16 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S2F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S4/Boxes/S4 Box 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S4/Modules/S4 Module 2f.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/02. M Families/Facades/M2F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/02. M Families/M4/Boxes/M4 Box 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/02. M Families/M4/Modules/M4 Module 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/05. XL Families/XL4/Roofs/XL4 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.8 Stacking Options rule (XL = S + M side by side); file name One roof over both units. |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 8 | 8 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL S2F facade: 3 cap(s). M2F facade: 5 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 2 | 2 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 2 | 2 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 8 | 8 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Guide.stl | 8 | 8 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Slide.stl | 8 | 8 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 2 | 2 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |

Oracle notes: S4 2F + M4 2F side by side, one XL4 Grid Roof. Each unit: its module, its latch, its box/facade kit and 2 runner packs (x4 for both). Caps 3 (S2F) + 5 (M2F).

## D19 (D19)
expected 81 copies / 39 files; planner 81 copies (+ spares) / 39 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/03. L Families/Facades/L1F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/03. L Families/Facades/L2F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/03. L Families/L5/Boxes/L5 Box 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/03. L Families/L5/Boxes/L5 Box 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/03. L Families/L5/Modules/L5 Module 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/03. L Families/L5/Modules/L5 Module 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/03. L Families/L5/Roofs/L5 Table Roof.stl | 1 | 1 |  | ok | high Config: stated roof on top of the case; the case keeps its own lid (coordinator convention). Drawers roof of the same footprint.  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 8 | 8 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL L2F facade: 5 cap(s). L1F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 2 | 2 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 2 | 2 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 6 | 6 |  | ok | low M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs) Reading A (chosen): 2 per L case, like a drawer module. Reading B: 0. |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 6 | 6 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x5 Runner Guide.stl | 6 | 6 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x5 Runner Slide.stl | 6 | 6 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 2 | 2 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |
| 02. SUSTAINERS/03. L Families/Facades/L1F Facade.stl | 1 | 1 |  | ok | medium M01 p.12 (L1F / L2F Facade on the case front) Equivalent alternative: 02. SUSTAINERS/05. Universal/Facades/L1F.stl (same size and outline). Print one of the two. |
| 02. SUSTAINERS/03. L Families/L5/Modules/L5 1F Flat Module.stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 1F Dividers Module, L3 2F Sealed Module); file name Flat variant. |
| 02. SUSTAINERS/03. L Families/L5/Roofs/L5 Roof.stl | 1 | 1 |  | ok | high M01 p.12 (L3 Roof = the hinged lid); M01 p.5 The case lid (sustainer roof). |
| 02. SUSTAINERS/05. Universal/Hinges/L-XL 1F Hinge.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL 1F Hinge / L 2-4F Hinge); M01 p.17; file holds the 2 hinges of one case (2 bodies)  |
| 02. SUSTAINERS/05. Universal/Hinges/L-XL Hinge Top.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL Hinge Top); file name (S/M: one long piece; L-XL: 2 pieces in one file)  |
| 02. SUSTAINERS/05. Universal/Label for Sustainers.stl | 1 | 1 |  | ok | high M01 p.12: 1F case uses "Label for Sustainers"; one label per case (coordinator convention)  |
| 02. SUSTAINERS/05. Universal/Locks/1 SET OF PINS FOR 1 LOCK.stl | 2 | 2 | 1 | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK HOLDER.stl | 2 | 2 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK INNER PART.stl | 2 | 2 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK OUTER PART 1F.stl | 2 | 2 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Rods/L-XL Rods.stl | 1 | 1 | 1 | ok | medium M01 p.12 (L-XL Rods); file holds 2 rods (2 bodies)  |
| 03. MODIFICATIONS/Backbone/Handle Lock Knob Part 1.stl | 2 | 2 |  | ok | high M01 p.13; M04 p.13 steps 16-17 (two knobs on the lock)  |
| 03. MODIFICATIONS/Backbone/Handle Lock Knob Part 2.stl | 2 | 2 |  | ok | high M04 p.13 step 16 (one cap per knob)  |
| 03. MODIFICATIONS/Backbone/L Pull-out Handle Lock.stl | 1 | 1 |  | ok | high M01 p.13 (XL Pull-out Handle Lock); M04 p.13 step 17: the pull-out handle needs the lock Alternative: 2 x "Universal Pull-out Handle Lock.stl" (M04 p.1 right). |
| 03. MODIFICATIONS/Backbone/L2F Backbone.stl | 2 | 2 |  | ok | low M04 p.7-p.11 steps 10-14: backbones tie the base and the modules and carry the pull-out rods (M04 p.14) up to the handle lock on the top level. Tower = base (1 level) + 2F + 1F + 1F = 5 levels; the lock takes the top level, so 4 levels of backbone = 2 x 2F. Readings: 2 x L2F Backbone (chosen), or L2F + 2 x L1F, or the Universal backbones (2 per level pair). Count depends on how far down the rods are guided. |
| 03. MODIFICATIONS/Base/L/L5 Base.stl | 1 | 1 |  | ok | high M04 p.2 step 1; file name (depth 5 has only one whole file)  |
| 03. MODIFICATIONS/Feet/L Feet.stl | 1 | 1 |  | ok | high Config (foot); M04 p.6 step 8  |
| 03. MODIFICATIONS/Pull-out Handle/L Pull-out Handle.stl | 1 | 1 |  | ok | high M04 p.14 steps 18-19; M01 p.13  |
| 03. MODIFICATIONS/Wheels/Bushing.stl | 2 | 2 |  | ok | high M04 p.2 step 2, p.3 (2 bushings)  |
| 03. MODIFICATIONS/Wheels/Cover.stl | 2 | 2 |  | ok | high M04 p.6 step 7 (a cover per wheel)  |
| 03. MODIFICATIONS/Wheels/Disk.stl | 2 | 2 |  | ok | high M04 p.4 step 3 (2 disks)  |
| 03. MODIFICATIONS/Wheels/Jig.stl | 1 | 1 |  | ok | medium M04 p.3 (jig to press the bushings) Printed assembly tool, does not stay in the stack. Drop it if only parts that stay in the build are counted. |
| 03. MODIFICATIONS/Wheels/Tyre (TPU).stl | 2 | 2 |  | ok | high M04 p.5 step 6 (2 TPU tyres) Print in TPU. |

Oracle notes: L5 mobile stack: L5 Base, 2 wheels (bushings, disks, TPU tyres, covers, jig), L Feet, pull-out handle + its lock + 2 knobs (part 1 + cap), backbones (low), drawer L5 2F (2 runner packs), drawer L5 1F (1 pack), case L5 1F Flat (lid, L1F case facade, L-XL 1F hinge set, 2 locks, Label for Sustainers), L5 Table Roof on top. Latches: 2 + 2 + 2 (case, low). Bought: M16 axle rod 414 mm, 2 M16 handle rods, bearings, collars, heat inserts.

## D20 (D20)
expected 40 copies / 15 files; planner 40 copies (+ spares) / 15 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/05. XL Families/XL Facade 1F.stl | 2 | 2 |  | ok | high M02 p.1 step 1, p.6 step 7; only XL drawer facade  |
| 01. DRAWERS/05. XL Families/XL3/Boxes/XL3 Back Panel.stl | 2 | 2 |  | ok | medium File name / folder: the XL3-XL5 Boxes folders hold Box 1F + Back Panel (the box is exported open-backed). Not shown in the manuals. One back panel per XL box (XL3-XL5). |
| 01. DRAWERS/05. XL Families/XL3/Boxes/XL3 Box 1F.stl | 2 | 2 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10; file name  |
| 01. DRAWERS/05. XL Families/XL3/Modules/XL3 Module 1F.stl | 2 | 2 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/05. XL Families/XL3/Roofs/XL3 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 6 | 6 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL XL1F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 2 | 2 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 2 | 2 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 4 | 4 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 4 | 4 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/XL Runners/x3 Runner Guide XL.stl | 4 | 4 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F); XL Runners subfolder for XL 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/XL Runners/x3 Runner Slide XL.stl | 4 | 4 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 2 | 2 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |
| 03. MODIFICATIONS/Base/XL/XL3 Base.stl | 1 | 1 |  | ok | high M04 p.17 Casters Mode (4 bought casters, M8) Casters are bought. |

Oracle notes: XL3 base on 4 bought casters, two XL3 1F drawers (each: module, 2 latches, box + back panel, XL facade, 1 XL x3 runner pack), XL3 Grid Roof.

## D21 (D21)
expected 102 copies / 14 files; planner 102 copies (+ spares) / 14 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/02. M Families/Facades/M1F (Turn On Supports).stl | 6 | 6 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/02. M Families/M4/Boxes/M4 Box 1F.stl | 6 | 6 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/02. M Families/M4/Modules/M4 Module 1F.stl | 6 | 6 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/02. M Families/M4/Roofs/M4 Grid Roof.stl | 2 | 2 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 18 | 18 | 2 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL M1F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Hidden Key (Turn On Supports).stl | 6 | 6 |  | ok | high User rule: the hidden key facade part is one per drawer (replaces Key). File name; no manual page. Replaces Key (Turn On Supports). |
| 01. DRAWERS/07. Universal/Hidden Key Part 2 (Turn on Supports).stl | 2 | 2 |  | ok | high User rule: the removable hidden key is one per stack, shared by all hidden-key drawers of the stack  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 2 | 2 | 1 | ok | medium Evidence from the STLs: the top tab of Hidden Key Part 2 (27.7 x 9.8 mm) is identical to the tab of "Handle Lock Knob Part 1", which M04 p.13 step 16 caps with "Handle Lock Knob Part 2"; that cap has the same size and mesh as "Key Cap" (37.8 x 13.2 x 11.7). So the removable hidden key takes one Key Cap. Reading A (chosen): 1 Key Cap per Hidden Key Part 2. Reading B (coordinator default): 0. |
| 01. DRAWERS/07. Universal/Label.stl | 6 | 6 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 6 | 6 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 12 | 12 | 2 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Guide.stl | 12 | 12 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Slide.stl | 12 | 12 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 6 | 6 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |

Oracle notes: Two M4 stacks of three 1F hidden-key drawers. Per stack: 3 complete M4 1F drawers (Hidden Key on each facade) + 1 Hidden Key Part 2 + 1 Key Cap for it (medium) + M4 Grid Roof. Project total = 2 stacks.

## D22 (D22)
expected 31 copies / 17 files; planner 31 copies (+ spares) / 17 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S1F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S4/Boxes/S4 Box 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S4/Modules/S4 Module 1f.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/01. S Families/S4/Roofs/S4 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 1 | 1 | 1 | ok | high M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL S1F facade: 1 cap(s). |
| 01. DRAWERS/07. Universal/Grid Dividers/20MM TALL/10-S, x3.stl | 2 | 2 |  | ok | high Grid Dividers/01. INSTRUCTIONS/01. instructions.jpg step 1 ("10-S" is the full width of S boxes) and widths.jpg  |
| 01. DRAWERS/07. Universal/Grid Dividers/20MM TALL/14, x4.stl | 1 | 1 |  | ok | high depth.jpg: "14-x4" is the full depth of x4 boxes  |
| 01. DRAWERS/07. Universal/Grid Dividers/20MM TALL/Straight Edge Piece 20MM.stl | 6 | 6 |  | ok | medium instructions.jpg step 2: a full-length divider needs two border parts 2 per divider x 3. If the full-depth divider stops at a full-width one (instructions step 3-6), it needs only 1 border part: 5. |
| 01. DRAWERS/07. Universal/Grid Dividers/grid divider pin_tight.stl | 6 | 6 | 1 | ok | low instructions.jpg steps 2 and 5: each divider is pinned at two holes (two pin circles per divider) Reading A (chosen): 2 per divider. Reading B: the pin count depends on divider length (pins in more holes). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | high M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 2 | 2 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Guide.stl | 2 | 2 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Slide.stl | 2 | 2 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |

Oracle notes: S4 1F drawer + 20 mm grid dividers: 2 x "10-S, x3" (full width), 1 x "14, x4" (full depth), straight edge pieces and tight pins. Default grid roof.

## D23 (D23)
expected 25 copies / 14 files; planner 25 copies (+ spares) / 14 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S2F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S4/Boxes/S4 Box 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S4/Gridfinity Baseplate/S4 Baseplate_With 2 Handles.stl | 1 | 1 |  | ok | high M01 p.9 Interiors (gridfinity base); M01 p.11 S3 Baseplate; one per box  |
| 01. DRAWERS/01. S Families/S4/Modules/S4 Module 2f.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/01. S Families/S4/Roofs/S4 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 3 | 3 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL S2F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | high M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 4 | 4 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Guide.stl | 4 | 4 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Slide.stl | 4 | 4 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |

Oracle notes: S4 2F drawer (2 runner packs, S2F facade 3 caps) with "S4 Baseplate_With 2 Handles". Default grid roof.

## D24 (D24)
expected 20 copies / 15 files; planner 20 copies (+ spares) / 15 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/02. M Families/Facades/M1F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/02. M Families/M5/Boxes/M5 Box 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/02. M Families/M5/Modules/M5 Module 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/02. M Families/M5/Roofs/M5 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 3 | 3 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL M1F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 2 | 2 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x5 Runner Guide.stl | 2 | 2 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x5 Runner Slide.stl | 2 | 2 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |
| 03. MODIFICATIONS/Wall Mounts/M1F Wall Mount.stl | 1 | 1 |  | ok | high M05 p.1-p.10 Wall Mount Instructions; file name (each module size has its own wall mount)  |
| 03. MODIFICATIONS/Wall Mounts/Wall Mount Second Part.stl | 1 | 1 |  | ok | medium M05 steps 4-5 and 9: one "second part" (wall cleat) goes in each trapezoid opening of a wall mount; the M1F wall mount has one opening (measured) A 2F/4F wall mount has two openings, so two second parts. |

Oracle notes: M5 1F drawer + M1F Wall Mount (plate on the module) + 1 Wall Mount Second Part (cleat on the wall). Default grid roof.

## D25 (D25)
expected 18 copies / 15 files; planner 18 copies (+ spares) / 15 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S1F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S3/Boxes/S3 Box 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S3/Modules/S3 Module 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/01. S Families/S3/Roofs/S3 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 1 | 1 | 1 | ok | high M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL S1F facade: 1 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | high M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 2 | 2 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x3 Runner Guide.stl | 2 | 2 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x3 Runner Slide.stl | 2 | 2 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |
| 03. MODIFICATIONS/Backbone/S1F Backbone.stl | 1 | 1 |  | ok | medium M04 p.15 step 20: pegboards are attached on backbones Alternative: 2 x "Universal 1F Backbone.stl" (M04 p.1 right tower). |
| 03. MODIFICATIONS/Pegboard Attachment/IKEA Skadis Pegboard/S1F.stl | 1 | 1 |  | ok | high M04 p.15 step 20; file name  |

Oracle notes: S3 1F drawer + IKEA Skadis S1F pegboard attachment, which mounts on a backbone: 1 S1F Backbone (medium). Default grid roof.

## D26 (D26)
expected 17 copies / 15 files; planner 17 copies (+ spares) / 15 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/S3/Roofs/S3 Grid Roof.stl | 1 | 1 |  | ok | low Battery default: grid roof on the top unit; no roof was stated for D26 Reading A (chosen, battery default): S3 Grid Roof on the case lid. Reading B: no extra roof, the case lid closes the stack. |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.12: 2F/4F case uses the drawers "Label"; one label per case  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | low Not in M01 p.12, but the case module carries the same latch pocket(s) as a drawer module of its width (STL) Reading A (chosen): 1 per S case, like a drawer module. Reading B: 0. |
| 02. SUSTAINERS/01. S Families/Facades/S2F Facade.stl | 1 | 1 |  | ok | medium M01 p.12 (L1F / L2F Facade on the case front) Equivalent alternative: 02. SUSTAINERS/05. Universal/Facades/S2F.stl (same size and outline). Print one of the two. |
| 02. SUSTAINERS/01. S Families/S3/Modules/S3 2F Module.stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 1F Dividers Module, L3 2F Sealed Module); file name S/M cases come only as one (flat) module per height. |
| 02. SUSTAINERS/01. S Families/S3/Roofs/S3 Roof.stl | 1 | 1 |  | ok | high M01 p.12 (L3 Roof = the hinged lid); M01 p.5 The case lid (sustainer roof). |
| 02. SUSTAINERS/05. Universal/Baseplates/01. S/S3 Baseplate.stl | 1 | 1 |  | ok | high M01 p.9 (sustainers gridfinity interior); sustainers Baseplates folder  |
| 02. SUSTAINERS/05. Universal/Dividers/S Dividers/S2F Divider.stl | 3 | 3 |  | ok | high Config (3 dividers); S Dividers folder, 2F height  |
| 02. SUSTAINERS/05. Universal/Hinges/S Hinge Top.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL Hinge Top); file name (S/M: one long piece; L-XL: 2 pieces in one file)  |
| 02. SUSTAINERS/05. Universal/Hinges/S-M 2-4F Hinge.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL 1F Hinge / L 2-4F Hinge); M01 p.17; file holds the 2 hinges of one case (2 bodies)  |
| 02. SUSTAINERS/05. Universal/Locks/1 SET OF PINS FOR 1 LOCK.stl | 1 | 1 | 1 | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 1 lock(s) per S case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK HOLDER.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 1 lock(s) per S case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK INNER PART.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 1 lock(s) per S case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK OUTER PART 2-4F.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 1 lock(s) per S case. |
| 02. SUSTAINERS/05. Universal/Rods/S-M Rods.stl | 1 | 1 | 1 | ok | medium M01 p.12 (L-XL Rods); file holds 2 rods (2 bodies)  |

Oracle notes: S3 2F case (lid S3 Roof, S2F case facade, S-M 2-4F hinge set, 1 lock outer 2-4F, drawers Label, latch low) with the sustainers S3 Baseplate and 3 x S2F Divider. Roof not stated: S3 Grid Roof listed as the default (low).

## D27 (D27)
expected 43 copies / 20 files; planner 43 copies (+ spares) / 20 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S1F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/Facades/S2F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11/p.16; M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S6/Boxes/S6 Box 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S6/Boxes/S6 Box 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S6/Modules/S6 Module 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/01. S Families/S6/Modules/S6 Module 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/01. S Families/S6/Roofs/S6 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 4 | 4 | 1 | ok | medium M02 p.6 step 8 (1 cap on an S1F facade); other facades: exposed 9 mm counterbores measured on the facade STL S2F facade: 3 cap(s). S1F facade: 1 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 2 | 2 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 2 | 2 |  | ok | high M01 p.11 Label; M02 p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | high M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (S/M 1, L/XL 2, measured on the STLs)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 6 | 6 | 1 | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x6 Runner Guide.stl | 6 | 6 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Runners/x6 Runner Slide.stl | 6 | 6 |  | ok | high User rule (owner of the Vault): one pack of 2 runner guides + 2 runner slides + 2 runner stoppers per F (48 mm level) of the module, whatever the drawers in it; consistent with M02 p.4 step 6, p.7 step 9, p.8 step 11 and the module STLs (one runner level and one stopper slot per side per F) 2F module: 2 pack(s) of 2. 1F module: 1 pack(s) of 2. |
| 01. DRAWERS/07. Universal/Springs.stl | 2 | 2 | 1 | ok | high M01 p.15; M02 p.2 step 3; one file = the 2 springs of one facade  |
| 03. MODIFICATIONS/Backbone/S1F Backbone.stl | 1 | 1 |  | ok | medium user rule: backbone column per the manual (base + 2F = 3F: 2F + 1F)  |
| 03. MODIFICATIONS/Backbone/S2F Backbone.stl | 1 | 1 |  | ok | low M04 p.12 step 15: the stationary handle is fixed from the back of a backbone part; M04 p.7-p.10: the first backbone is a 2F one tying the base and the first (2F) module Reading A (chosen): 1 x S2F Backbone carrying the handle. Reading B: backbones on the whole height (base + 2F + 1F = 4 levels = 2 x S2F). Universal backbones are another alternative. |
| 03. MODIFICATIONS/Base/S/S6 Base Whole.stl | 1 | 1 |  | ok | high File names (Whole / Part 1 + Part 2); Whole fits the H2S bed (measured) Split alternative: S6 Base Part 1 + Part 2 (+ Base Connector). |
| 03. MODIFICATIONS/Stationary Handle/S Stationary Handle.stl | 1 | 1 |  | ok | high M04 p.12 step 15  |

Oracle notes: S6 base (no wheels, no foot) + stationary handle on a backbone, drawer S6 2F (2 runner packs) + drawer S6 1F (1 pack), S6 Grid Roof.

## D28 (D28)
expected 18 copies / 13 files; planner 18 copies (+ spares) / 13 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/03. L Families/L6/Roofs/L6 Grid Roof.stl | 1 | 1 |  | ok | high Config: stated roof on top of the case; the case keeps its own lid (coordinator convention). Drawers roof of the same footprint.  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | low Not in M01 p.12, but the case module carries the same latch pocket(s) as a drawer module of its width (STL) Reading A (chosen): 2 per L case, like a drawer module. Reading B: 0. |
| 02. SUSTAINERS/03. L Families/Facades/L1F Facade.stl | 1 | 1 |  | ok | medium M01 p.12 (L1F / L2F Facade on the case front) Equivalent alternative: 02. SUSTAINERS/05. Universal/Facades/L1F.stl (same size and outline). Print one of the two. |
| 02. SUSTAINERS/03. L Families/L6/Modules/L6 1F Flat Module.stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 1F Dividers Module, L3 2F Sealed Module); file name Flat variant. |
| 02. SUSTAINERS/03. L Families/L6/Roofs/L6 Roof Whole.stl | 1 | 1 |  | ok | high M01 p.12 (L3 Roof = the lid); "Whole" file chosen because it fits the H2S bed (340 x 320 x 340) in some rotation (measured) Split alternative: Part 1 + Part 2 + Connector For Split Roof. |
| 02. SUSTAINERS/05. Universal/Hinges/L-XL 1F Hinge.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL 1F Hinge / L 2-4F Hinge); M01 p.17; file holds the 2 hinges of one case (2 bodies)  |
| 02. SUSTAINERS/05. Universal/Hinges/L-XL Hinge Top.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL Hinge Top); file name (S/M: one long piece; L-XL: 2 pieces in one file)  |
| 02. SUSTAINERS/05. Universal/Label for Sustainers.stl | 1 | 1 |  | ok | high M01 p.12: 1F case uses "Label for Sustainers"; one label per case (coordinator convention)  |
| 02. SUSTAINERS/05. Universal/Locks/1 SET OF PINS FOR 1 LOCK.stl | 2 | 2 | 1 | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK HOLDER.stl | 2 | 2 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK INNER PART.stl | 2 | 2 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Locks/LOCK OUTER PART 1F.stl | 2 | 2 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8: S/M cases one lock, L/XL cases two 2 lock(s) per L case. |
| 02. SUSTAINERS/05. Universal/Rods/L-XL Rods.stl | 1 | 1 | 1 | ok | medium M01 p.12 (L-XL Rods); file holds 2 rods (2 bodies)  |

Oracle notes: L6 1F Flat case: lid L6 Roof Whole or split by H2S fit (see part), L1F case facade, L-XL 1F hinge set, 2 locks, Label for Sustainers, 2 latches (low), L6 Grid Roof.
