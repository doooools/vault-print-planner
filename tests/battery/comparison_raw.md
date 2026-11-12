# Oracle vs planner (raw)

| config | expected copies | planner copies | gaps |
|---|---|---|---|
| C01 | 16 | 16 | 0 |
| C02 | 21 | 27 | 3 |
| C03 | 54 | 60 | 3 |
| C04 | 59 | 59 | 0 |
| C05 | 35 | 33 | 2 |
| C06 | 13 | 13 | 0 |
| C07 | 13 | 13 | 0 |
| C08 | 45 | 51 | 3 |
| C09 | 31 | 31 | 0 |
| C10 | 39 | 45 | 3 |
| C11 | 17 | 17 | 0 |
| C12 | 23 | 23 | 2 |
| C13 | 32 | 32 | 0 |
| C14 | 29 | 29 | 0 |

## C01 (C01)
expected 16 copies / 13 files; planner 16 copies (+ spares) / 13 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S1F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 + p.16 (S1F Facade, Facades folder); M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S4/Boxes/S4 Box 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 p.3-7 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S4/Modules/S4 Module 1f.stl | 1 | 1 |  | ok | high M01 p.11 Drawers Naming (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/01. S Families/S4/Roofs/S4 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; M01 p.11 S3 Grid Roof; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 1 | 1 | 1 | ok | high M02 p.6 step 8 (1 cap on a 1F S facade); count for other facades = exposed 9 mm counterbores measured on the facade STL (the bolt hole under the label slot excluded) S1F facade: 1 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1 (one key lock per facade)  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.11 Label; M02 p.5 + p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | high M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (1 on S and M modules, 2 on L, XL and L2 modules, from the STL)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 2 | 2 | 1 | ok | high M01 p.11 Runner Stopper; M02 p.8 step 11 (2, one per side; the module has one stopper slot per side per floor)  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Guide.stl | 2 | 2 |  | ok | high M01 p.11 x3 Runner Guides (2 shown); M02 p.7 step 9 (2, one per side); depth from file name  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Slide.stl | 2 | 2 |  | ok | high M01 p.11 x3 Runner Slides (2 shown); M02 p.4 step 6 (2, one per side)  |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15 (file Springs highlights both springs); M02 p.2 step 3 (2 springs per facade); file holds 2 springs (2 bodies) One file = the 2 springs of one facade. |

Oracle notes: S4 = S family, depth 4 (folder 01. DRAWERS/01. S Families/S4). Single 1F drawer: no geared rails (optional, M02 p.4 step 5). Grid roof without Top Handle.

## C02 (C02)
expected 21 copies / 14 files; planner 27 copies (+ spares) / 14 files; 3 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/02. M Families/Facades/M2F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 + p.16 (S1F Facade, Facades folder); M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/02. M Families/M4/Boxes/M4 Box 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 p.3-7 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/02. M Families/M4/Modules/M4 Module 2F.stl | 1 | 1 |  | ok | high M01 p.11 Drawers Naming (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/02. M Families/M4/Roofs/M4 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; M01 p.11 S3 Grid Roof; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 5 | 5 | 1 | ok | medium M02 p.6 step 8 (1 cap on a 1F S facade); count for other facades = exposed 9 mm counterbores measured on the facade STL (the bolt hole under the label slot excluded) M2F facade: 5 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1 (one key lock per facade)  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.11 Label; M02 p.5 + p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (1 on S and M modules, 2 on L, XL and L2 modules, from the STL)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 2 | 4 | 1 | **GAP** | high M01 p.11 Runner Stopper; M02 p.8 step 11 (2, one per side; the module has one stopper slot per side per floor)  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Guide.stl | 2 | 4 |  | **GAP** | high M01 p.11 x3 Runner Guides (2 shown); M02 p.7 step 9 (2, one per side); depth from file name  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Slide.stl | 2 | 4 |  | **GAP** | high M01 p.11 x3 Runner Slides (2 shown); M02 p.4 step 6 (2, one per side)  |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15 (file Springs highlights both springs); M02 p.2 step 3 (2 springs per facade); file holds 2 springs (2 bodies) One file = the 2 springs of one facade. |
| 01. DRAWERS/07. Universal/Top Handle (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Top Handle on the S3 Grid Roof; M01 p.18 (M6 50 mm x2 per roof handle); M01 p.3 Only because the config asks for it. |

Oracle notes: One 2F box in a 2F module: geared rails optional, not listed (M Rails would be 1 file if wanted). M2F facade: 5 exposed cap counterbores, so 5 facade caps. Top Handle only because asked.

## C03 (C03)
expected 54 copies / 16 files; planner 60 copies (+ spares) / 16 files; 3 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/03. L Families/Facades/L1F (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11 + p.16 (S1F Facade, Facades folder); M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/03. L Families/Facades/L2F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 + p.16 (S1F Facade, Facades folder); M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/03. L Families/L5/Boxes/L5 Box 1F.stl | 2 | 2 |  | ok | high M01 p.11 (S3 Box 1F); M02 p.3-7 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/03. L Families/L5/Boxes/L5 Box 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 p.3-7 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/03. L Families/L5/Modules/L5 Module 4F.stl | 1 | 1 |  | ok | high M01 p.11 Drawers Naming (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/03. L Families/L5/Roofs/L5 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; M01 p.11 S3 Grid Roof; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 11 | 11 | 2 | ok | medium M02 p.6 step 8 (1 cap on a 1F S facade); count for other facades = exposed 9 mm counterbores measured on the facade STL (the bolt hole under the label slot excluded) L2F facade: 5 cap(s). L1F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Geared Rails/L Rails.stl | 3 | 3 |  | ok | high M02 p.4 step 5: geared rails are optional, but to be used if more than one box per 2F or 4F module; file holds top + bottom rail (2 bodies) Required here: more than one box in one 2F/4F module. |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 3 | 3 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1 (one key lock per facade)  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 3 | 3 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 3 | 3 |  | ok | high M01 p.11 Label; M02 p.5 + p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (1 on S and M modules, 2 on L, XL and L2 modules, from the STL)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 6 | 8 | 1 | **GAP** | high M01 p.11 Runner Stopper; M02 p.8 step 11 (2, one per side; the module has one stopper slot per side per floor)  |
| 01. DRAWERS/07. Universal/Runners/x5 Runner Guide.stl | 6 | 8 |  | **GAP** | high M01 p.11 x3 Runner Guides (2 shown); M02 p.7 step 9 (2, one per side); depth from file name  |
| 01. DRAWERS/07. Universal/Runners/x5 Runner Slide.stl | 6 | 8 |  | **GAP** | high M01 p.11 x3 Runner Slides (2 shown); M02 p.4 step 6 (2, one per side)  |
| 01. DRAWERS/07. Universal/Springs.stl | 3 | 3 | 1 | ok | high M01 p.15 (file Springs highlights both springs); M02 p.2 step 3 (2 springs per facade); file holds 2 springs (2 bodies) One file = the 2 springs of one facade. |

Oracle notes: L5 4F module with 3 drawers (2F + 1F + 1F = 4 floors). Several boxes in one 4F module, so geared rails are needed (M02 p.4 step 5): one "L Rails" file per box. Facade caps: L2F 5 + L1F 3 + L1F 3 = 11. L modules have 2 latch pockets.

## C04 (C04)
expected 59 copies / 14 files; planner 59 copies (+ spares) / 14 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S1F (Turn On Supports).stl | 4 | 4 |  | ok | high M01 p.11 + p.16 (S1F Facade, Facades folder); M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S4/Boxes/S4 Box 1F.stl | 4 | 4 |  | ok | high M01 p.11 (S3 Box 1F); M02 p.3-7 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S4/Modules/S4 Module 4F.stl | 1 | 1 |  | ok | high M01 p.11 Drawers Naming (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/01. S Families/S4/Roofs/S4 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; M01 p.11 S3 Grid Roof; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 4 | 4 | 1 | ok | high M02 p.6 step 8 (1 cap on a 1F S facade); count for other facades = exposed 9 mm counterbores measured on the facade STL (the bolt hole under the label slot excluded) S1F facade: 1 cap(s). |
| 01. DRAWERS/07. Universal/Geared Rails/S Rails.stl | 4 | 4 |  | ok | high M02 p.4 step 5: geared rails are optional, but to be used if more than one box per 2F or 4F module; file holds top + bottom rail (2 bodies) Required here: more than one box in one 2F/4F module. |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 4 | 4 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1 (one key lock per facade)  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 4 | 4 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 4 | 4 |  | ok | high M01 p.11 Label; M02 p.5 + p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | high M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (1 on S and M modules, 2 on L, XL and L2 modules, from the STL)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 8 | 8 | 1 | ok | high M01 p.11 Runner Stopper; M02 p.8 step 11 (2, one per side; the module has one stopper slot per side per floor)  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Guide.stl | 8 | 8 |  | ok | high M01 p.11 x3 Runner Guides (2 shown); M02 p.7 step 9 (2, one per side); depth from file name  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Slide.stl | 8 | 8 |  | ok | high M01 p.11 x3 Runner Slides (2 shown); M02 p.4 step 6 (2, one per side)  |
| 01. DRAWERS/07. Universal/Springs.stl | 4 | 4 | 1 | ok | high M01 p.15 (file Springs highlights both springs); M02 p.2 step 3 (2 springs per facade); file holds 2 springs (2 bodies) One file = the 2 springs of one facade. |

Oracle notes: S4 4F module, four S4 1F drawers (the 4F module has 4 runner levels and 4 stopper slots per side, measured). Geared rails required (more than one box per 4F module): 4 files "S Rails".

## C05 (C05)
expected 35 copies / 16 files; planner 33 copies (+ spares) / 16 files; 2 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S1F (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11 + p.16 (S1F Facade, Facades folder); M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S3/Boxes/S3 Box 1F.stl | 2 | 2 |  | ok | high M01 p.11 (S3 Box 1F); M02 p.3-7 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S3/Gridfinity Baseplate/S3 Baseplate.stl | 2 | 2 |  | ok | high M01 p.9 Interiors (6. gridfinity base); M01 p.11 S3 Baseplate; plain file (not _With 1/2 Handles) One per box. |
| 01. DRAWERS/01. S Families/S3/Modules/S3 Module 2F.stl | 1 | 1 |  | ok | high M01 p.11 Drawers Naming (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/01. S Families/S3/Roofs/S3 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; M01 p.11 S3 Grid Roof; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 2 | 2 | 1 | ok | high M02 p.6 step 8 (1 cap on a 1F S facade); count for other facades = exposed 9 mm counterbores measured on the facade STL (the bolt hole under the label slot excluded) S1F facade: 1 cap(s). |
| 01. DRAWERS/07. Universal/Geared Rails/S Rails.stl | 2 | 2 |  | ok | high M02 p.4 step 5: geared rails are optional, but to be used if more than one box per 2F or 4F module; file holds top + bottom rail (2 bodies) Required here: more than one box in one 2F/4F module. |
| 01. DRAWERS/07. Universal/Hidden Key (Turn On Supports).stl | 2 | 2 |  | ok | medium File names only (Universal folder, listed M01 p.15/p.20); no manual page shows the hidden key. Replaces the Key: same pinion, top is a flush slot. Replaces Key (Turn On Supports). |
| 01. DRAWERS/07. Universal/Hidden Key Part 2 (Turn on Supports).stl | 2 | 1 |  | **GAP** | low File name only. Its tongue fits the Hidden Key slot: it is the removable turning key. Reading A (chosen): one per hidden lock, by the "Part 2" pairing in the name. Reading B: one removable key opens all hidden locks, so 1 per project. |
| 01. DRAWERS/07. Universal/Key Cap.stl | 2 | 1 | 1 | **GAP** | low M02 p.1 step 2 (key cap goes on the key knob). Hidden Key Part 2 has the same knob as the Key (its top matches the Key Cap; the Handle Lock Knob Part 2 is the same size as the Key Cap). Reading A (chosen): the cap goes on each Hidden Key Part 2. Reading B: 0 (hidden lock has no knob). |
| 01. DRAWERS/07. Universal/Label.stl | 2 | 2 |  | ok | high M01 p.11 Label; M02 p.5 + p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | high M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (1 on S and M modules, 2 on L, XL and L2 modules, from the STL)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 4 | 4 | 1 | ok | high M01 p.11 Runner Stopper; M02 p.8 step 11 (2, one per side; the module has one stopper slot per side per floor)  |
| 01. DRAWERS/07. Universal/Runners/x3 Runner Guide.stl | 4 | 4 |  | ok | high M01 p.11 x3 Runner Guides (2 shown); M02 p.7 step 9 (2, one per side); depth from file name  |
| 01. DRAWERS/07. Universal/Runners/x3 Runner Slide.stl | 4 | 4 |  | ok | high M01 p.11 x3 Runner Slides (2 shown); M02 p.4 step 6 (2, one per side)  |
| 01. DRAWERS/07. Universal/Springs.stl | 2 | 2 | 1 | ok | high M01 p.15 (file Springs highlights both springs); M02 p.2 step 3 (2 springs per facade); file holds 2 springs (2 bodies) One file = the 2 springs of one facade. |

Oracle notes: S3 2F module with two 1F drawers, hidden key lock, Gridfinity baseplate in each box. Geared rails required (2 boxes in a 2F module). The hidden key is not documented in the manuals: Hidden Key replaces Key; Hidden Key Part 2 (removable turning key) and its Key Cap are uncertain (see per-part notes). Baseplate = the drawers one (01. DRAWERS/.../S3/Gridfinity Baseplate/S3 Baseplate.stl, 125.8 x 134 x 4), not the sustainers one.

## C06 (C06)
expected 13 copies / 13 files; planner 13 copies (+ spares) / 13 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/S4/Roofs/S4 Grid Roof.stl | 1 | 1 |  | ok | medium Config asks for a grid roof on the case. M01 p.8: sustainers and drawers stack; the case lid top has the same connect features as a module top (M01 p.17). File = the drawers grid roof of the same footprint. Printed in addition to the case lid, which stays. |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | low Not in M01 p.12 (Sustainers Naming lists no latch), but the S/M case module has the same latch pocket underneath as a drawer module (STL); M02 p.8 step 12 for drawers Reading A (chosen): 1 latch per S/M case, like a drawer module. Reading B: 0 (the manual never lists a latch for sustainers). |
| 02. SUSTAINERS/01. S Families/Facades/S1F Facade.stl | 1 | 1 |  | ok | medium M01 p.12 (L1F Facade / L2F Facade on the case front) Equivalent alternative: 02. SUSTAINERS/05. Universal/Facades/S1F.stl (same size and shape; differs only by faint surface detail). Print one of the two. |
| 02. SUSTAINERS/01. S Families/S4/Modules/S4 1F Module.stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 1F Dividers Module, L3 2F Sealed Module); S and M cases only come as one (flat) module per height; file name S/M cases have no Flat/Dividers/Sealed variants: this is the flat one. |
| 02. SUSTAINERS/01. S Families/S4/Roof/S4 Roof.stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 Roof = the hinged lid); M01 p.5 The case lid (sustainer roof). |
| 02. SUSTAINERS/05. Universal/Hinges/S Hinge Top.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL Hinge Top); file name; the S/M file is one piece (the L-XL file holds 2)  |
| 02. SUSTAINERS/05. Universal/Hinges/S-M 1F Hinge.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL 1F Hinge / L 2-4F Hinge); M01 p.17 (2 hinges per case); file holds 2 hinge leaves (2 bodies) One file = both hinge leaves of one case. |
| 02. SUSTAINERS/05. Universal/Label for Sustainers.stl | 1 | 1 |  | ok | medium M01 p.12: the 1F case uses "Label for Sustainers"; the 1F case facade label slot is ~38 mm (measured)  |
| 02. SUSTAINERS/05. Universal/Locks/1 SET OF PINS FOR 1 LOCK.stl | 1 | 1 | 1 | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two; file name says one set per lock (4 pins)  |
| 02. SUSTAINERS/05. Universal/Locks/LOCK HOLDER.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two  |
| 02. SUSTAINERS/05. Universal/Locks/LOCK INNER PART.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two  |
| 02. SUSTAINERS/05. Universal/Locks/LOCK OUTER PART 1F.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two  |
| 02. SUSTAINERS/05. Universal/Rods/S-M Rods.stl | 1 | 1 | 1 | ok | medium M01 p.12 (L-XL Rods, orange pins); file holds 2 rods (2 bodies) One file = both hinge rods. |

Oracle notes: "Case" = Sustainer. S4 1F sustainer, flat interior (the only S module). A case always has its own hinged lid ("S4 Roof" in 02. SUSTAINERS); the grid roof asked for is the drawers S4 Grid Roof on top of it. S/M cases have one lock (M01 p.8); hinge files hold both leaves; rods file holds both rods.

## C07 (C07)
expected 13 copies / 13 files; planner 13 copies (+ spares) / 13 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/02. M Families/M5/Roofs/M5 Grid Roof.stl | 1 | 1 |  | ok | medium Config asks for a grid roof on the case. M01 p.8: sustainers and drawers stack; the case lid top has the same connect features as a module top (M01 p.17). File = the drawers grid roof of the same footprint. Printed in addition to the case lid, which stays. |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | medium M01 p.12: the 2F case uses "Label" (the drawers one); the 2F case facade label slot is ~48 mm (measured)  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | low Not in M01 p.12 (Sustainers Naming lists no latch), but the S/M case module has the same latch pocket underneath as a drawer module (STL); M02 p.8 step 12 for drawers Reading A (chosen): 1 latch per S/M case, like a drawer module. Reading B: 0 (the manual never lists a latch for sustainers). |
| 02. SUSTAINERS/02. M Families/Facades/M2F Facade.stl | 1 | 1 |  | ok | medium M01 p.12 (L1F Facade / L2F Facade on the case front) Equivalent alternative: 02. SUSTAINERS/05. Universal/Facades/M2F.stl (same size and shape; differs only by faint surface detail). Print one of the two. |
| 02. SUSTAINERS/02. M Families/M5/Modules/M5 2F Module .stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 1F Dividers Module, L3 2F Sealed Module); S and M cases only come as one (flat) module per height; file name S/M cases have no Flat/Dividers/Sealed variants: this is the flat one. |
| 02. SUSTAINERS/02. M Families/M5/Roofs/M5 Roof.stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 Roof = the hinged lid); M01 p.5 The case lid (sustainer roof). |
| 02. SUSTAINERS/05. Universal/Hinges/M Hinge Top.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL Hinge Top); file name; the S/M file is one piece (the L-XL file holds 2)  |
| 02. SUSTAINERS/05. Universal/Hinges/S-M 2-4F Hinge.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL 1F Hinge / L 2-4F Hinge); M01 p.17 (2 hinges per case); file holds 2 hinge leaves (2 bodies) One file = both hinge leaves of one case. |
| 02. SUSTAINERS/05. Universal/Locks/1 SET OF PINS FOR 1 LOCK.stl | 1 | 1 | 1 | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two; file name says one set per lock (4 pins)  |
| 02. SUSTAINERS/05. Universal/Locks/LOCK HOLDER.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two  |
| 02. SUSTAINERS/05. Universal/Locks/LOCK INNER PART.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two  |
| 02. SUSTAINERS/05. Universal/Locks/LOCK OUTER PART 2-4F.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two  |
| 02. SUSTAINERS/05. Universal/Rods/S-M Rods.stl | 1 | 1 | 1 | ok | medium M01 p.12 (L-XL Rods, orange pins); file holds 2 rods (2 bodies) One file = both hinge rods. |

Oracle notes: M5 2F sustainer (flat; the only M module; note the on-disk file name has a space before ".stl"). 2F uses "S-M 2-4F Hinge", "LOCK OUTER PART 2-4F" and the drawers "Label" (M01 p.12). Grid roof = drawers M5 Grid Roof on top of the case lid.

## C08 (C08)
expected 45 copies / 27 files; planner 51 copies (+ spares) / 27 files; 3 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S1F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 + p.16 (S1F Facade, Facades folder); M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/Facades/S2F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 + p.16 (S1F Facade, Facades folder); M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S4/Boxes/S4 Box 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 p.3-7 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S4/Boxes/S4 Box 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 p.3-7 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S4/Modules/S4 Module 1f.stl | 1 | 1 |  | ok | high M01 p.11 Drawers Naming (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/01. S Families/S4/Modules/S4 Module 2f.stl | 1 | 1 |  | ok | high M01 p.11 Drawers Naming (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/01. S Families/S4/Roofs/S4 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; M01 p.11 S3 Grid Roof; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 4 | 4 | 1 | ok | medium M02 p.6 step 8 (1 cap on a 1F S facade); count for other facades = exposed 9 mm counterbores measured on the facade STL (the bolt hole under the label slot excluded) S1F facade: 1 cap(s). S2F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1 (one key lock per facade)  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 2 | 2 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 2 | 2 |  | ok | high M01 p.11 Label; M02 p.5 + p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 3 | 3 |  | ok | low M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (1 on S and M modules, 2 on L, XL and L2 modules, from the STL) Reading A (chosen): 1 latch per S/M case, like a drawer module. Reading B: 0 (the manual never lists a latch for sustainers). |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 4 | 6 | 1 | **GAP** | high M01 p.11 Runner Stopper; M02 p.8 step 11 (2, one per side; the module has one stopper slot per side per floor)  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Guide.stl | 4 | 6 |  | **GAP** | high M01 p.11 x3 Runner Guides (2 shown); M02 p.7 step 9 (2, one per side); depth from file name  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Slide.stl | 4 | 6 |  | **GAP** | high M01 p.11 x3 Runner Slides (2 shown); M02 p.4 step 6 (2, one per side)  |
| 01. DRAWERS/07. Universal/Springs.stl | 2 | 2 | 1 | ok | high M01 p.15 (file Springs highlights both springs); M02 p.2 step 3 (2 springs per facade); file holds 2 springs (2 bodies) One file = the 2 springs of one facade. |
| 02. SUSTAINERS/01. S Families/Facades/S1F Facade.stl | 1 | 1 |  | ok | medium M01 p.12 (L1F Facade / L2F Facade on the case front) Equivalent alternative: 02. SUSTAINERS/05. Universal/Facades/S1F.stl (same size and shape; differs only by faint surface detail). Print one of the two. |
| 02. SUSTAINERS/01. S Families/S4/Modules/S4 1F Module.stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 1F Dividers Module, L3 2F Sealed Module); S and M cases only come as one (flat) module per height; file name S/M cases have no Flat/Dividers/Sealed variants: this is the flat one. |
| 02. SUSTAINERS/01. S Families/S4/Roof/S4 Roof.stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 Roof = the hinged lid); M01 p.5 The case lid (sustainer roof). |
| 02. SUSTAINERS/05. Universal/Hinges/S Hinge Top.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL Hinge Top); file name; the S/M file is one piece (the L-XL file holds 2)  |
| 02. SUSTAINERS/05. Universal/Hinges/S-M 1F Hinge.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL 1F Hinge / L 2-4F Hinge); M01 p.17 (2 hinges per case); file holds 2 hinge leaves (2 bodies) One file = both hinge leaves of one case. |
| 02. SUSTAINERS/05. Universal/Label for Sustainers.stl | 1 | 1 |  | ok | medium M01 p.12: the 1F case uses "Label for Sustainers"; the 1F case facade label slot is ~38 mm (measured)  |
| 02. SUSTAINERS/05. Universal/Locks/1 SET OF PINS FOR 1 LOCK.stl | 1 | 1 | 1 | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two; file name says one set per lock (4 pins)  |
| 02. SUSTAINERS/05. Universal/Locks/LOCK HOLDER.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two  |
| 02. SUSTAINERS/05. Universal/Locks/LOCK INNER PART.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two  |
| 02. SUSTAINERS/05. Universal/Locks/LOCK OUTER PART 1F.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two  |
| 02. SUSTAINERS/05. Universal/Rods/S-M Rods.stl | 1 | 1 | 1 | ok | medium M01 p.12 (L-XL Rods, orange pins); file holds 2 rods (2 bodies) One file = both hinge rods. |

Oracle notes: Bottom to top: S4 1F drawer, S4 2F drawer, S4 1F case, S4 Grid Roof. Nothing printed goes between stacked units: each module carries its own latch (M02 p.8 step 12) that locks it to the unit below. Only one roof (on the case lid). Latch total = 1 + 1 + 1 (case latch is low confidence).

## C09 (C09)
expected 31 copies / 13 files; planner 31 copies (+ spares) / 13 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S1F (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11 + p.16 (S1F Facade, Facades folder); M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S4/Boxes/S4 Box 1F.stl | 2 | 2 |  | ok | high M01 p.11 (S3 Box 1F); M02 p.3-7 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S4/Modules/S4 Module 1f.stl | 2 | 2 |  | ok | high M01 p.11 Drawers Naming (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/03. L Families/L4/Roofs/L4 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.8 Stacking Options rule 4 (L = S + S, they stack); file name One L4 roof over both S4 modules. |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 2 | 2 | 1 | ok | high M02 p.6 step 8 (1 cap on a 1F S facade); count for other facades = exposed 9 mm counterbores measured on the facade STL (the bolt hole under the label slot excluded) S1F facade: 1 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1 (one key lock per facade)  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 2 | 2 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 2 | 2 |  | ok | high M01 p.11 Label; M02 p.5 + p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | high M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (1 on S and M modules, 2 on L, XL and L2 modules, from the STL)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 4 | 4 | 1 | ok | high M01 p.11 Runner Stopper; M02 p.8 step 11 (2, one per side; the module has one stopper slot per side per floor)  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Guide.stl | 4 | 4 |  | ok | high M01 p.11 x3 Runner Guides (2 shown); M02 p.7 step 9 (2, one per side); depth from file name  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Slide.stl | 4 | 4 |  | ok | high M01 p.11 x3 Runner Slides (2 shown); M02 p.4 step 6 (2, one per side)  |
| 01. DRAWERS/07. Universal/Springs.stl | 2 | 2 | 1 | ok | high M01 p.15 (file Springs highlights both springs); M02 p.2 step 3 (2 springs per facade); file holds 2 springs (2 bodies) One file = the 2 springs of one facade. |

Oracle notes: Two complete S4 1F drawer units side by side, one L4 Grid Roof across both (M01 p.8 rule 4). No S4 roofs. No printed side-by-side connector is required by the manual ("03. MODIFICATIONS/Backbone/Connector for Modules 1F.stl" exists but belongs to the optional backbone modification).

## C10 (C10)
expected 39 copies / 26 files; planner 45 copies (+ spares) / 26 files; 3 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/02. M Families/Facades/M2F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 + p.16 (S1F Facade, Facades folder); M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/02. M Families/M4/Boxes/M4 Box 2F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 p.3-7 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/02. M Families/M4/Modules/M4 Module 2F.stl | 1 | 1 |  | ok | high M01 p.11 Drawers Naming (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/02. M Families/M4/Roofs/M4 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; M01 p.11 S3 Grid Roof; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 5 | 5 | 1 | ok | medium M02 p.6 step 8 (1 cap on a 1F S facade); count for other facades = exposed 9 mm counterbores measured on the facade STL (the bolt hole under the label slot excluded) M2F facade: 5 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1 (one key lock per facade)  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.11 Label; M02 p.5 + p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (1 on S and M modules, 2 on L, XL and L2 modules, from the STL)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 2 | 4 | 1 | **GAP** | high M01 p.11 Runner Stopper; M02 p.8 step 11 (2, one per side; the module has one stopper slot per side per floor)  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Guide.stl | 2 | 4 |  | **GAP** | high M01 p.11 x3 Runner Guides (2 shown); M02 p.7 step 9 (2, one per side); depth from file name  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Slide.stl | 2 | 4 |  | **GAP** | high M01 p.11 x3 Runner Slides (2 shown); M02 p.4 step 6 (2, one per side)  |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15 (file Springs highlights both springs); M02 p.2 step 3 (2 springs per facade); file holds 2 springs (2 bodies) One file = the 2 springs of one facade. |
| 03. MODIFICATIONS/Backbone/Handle Lock Knob Part 1.stl | 2 | 2 |  | ok | high M01 p.13; M04 p.13 step 16-17 (two knobs on the lock, heat insert in each)  |
| 03. MODIFICATIONS/Backbone/Handle Lock Knob Part 2.stl | 2 | 2 |  | ok | high M01 p.13; M04 p.13 step 16 ("then cap it": one cap per knob)  |
| 03. MODIFICATIONS/Backbone/M Pull-out Handle Lock.stl | 1 | 1 |  | ok | medium M01 p.13 (XL Pull-out Handle Lock); M04 p.13 step 17; file name Alternative: 2 x "Universal Pull-out Handle Lock.stl". |
| 03. MODIFICATIONS/Backbone/M2F Backbone.stl | 1 | 1 |  | ok | low M04 p.7-p.10 steps 10-11 (a 2F backbone ties the base to the first module); M04 p.12 step 15 (the stationary handle is fixed to a backbone) Carries the stationary handle and guides the pull-out rods. Alternative: 2 x "Universal 2F Backbone.stl" (M04 p.1). Count depends on tower height; with base + one 2F module: one 2F backbone (base + lower floor) and the handle lock on the upper floor. |
| 03. MODIFICATIONS/Base/M/M4 Base.stl | 1 | 1 |  | ok | high M04 p.2 step 1 (base + M16 rod, 338 mm for M); M01 p.13 (XL7 Base Whole); file name  |
| 03. MODIFICATIONS/Feet/M Feet.stl | 1 | 1 |  | ok | medium M04 p.6 step 8 ("flip it upside down and attach the necessary size foot", in the wheel sequence); M01 p.13 (wheels + XL Feet) Not named in the config, but the manual's wheel assembly ends with one foot at the other end of the base. Reading B: 0 if feet are treated as a separate option. |
| 03. MODIFICATIONS/Pull-out Handle/M Pull-out Handle.stl | 1 | 1 |  | ok | high M04 p.14 steps 18-19; M01 p.13 (XL Pull-out Handle)  |
| 03. MODIFICATIONS/Stationary Handle/M Stationary Handle.stl | 1 | 1 |  | ok | high M04 p.12 step 15; M01 p.3 (8 x M4 60 per static handle)  |
| 03. MODIFICATIONS/Wheels/Bushing.stl | 2 | 2 |  | ok | high M04 p.2 step 2 (bushings pushed from both sides of the rod), p.3  |
| 03. MODIFICATIONS/Wheels/Cover.stl | 2 | 2 |  | ok | high M04 p.6 step 7 (a cover per wheel, 6 x M4 25)  |
| 03. MODIFICATIONS/Wheels/Disk.stl | 2 | 2 |  | ok | high M04 p.4 step 3 (disks on both sides)  |
| 03. MODIFICATIONS/Wheels/Jig.stl | 1 | 1 |  | ok | medium M04 p.3 (jig used to press the bushings; "here is how to find jig") Assembly tool, not part of the finished stack. Exclude it if the comparison only counts parts that stay in the build. |
| 03. MODIFICATIONS/Wheels/Tyre (TPU).stl | 2 | 2 |  | ok | high M04 p.5 step 6 (2 tyres, TPU); M01 p.1 note 3 Print in TPU. |

Oracle notes: Mobile M4 stack: base with wheels, backbone with stationary handle, pull-out handle with its lock, one M4 2F drawer, M4 Grid Roof. Metal: M16 rod 338 mm for the axle, 2 M16 rods for the pull-out handle, 2 x 6205ZZ, 2 SCSAW collars, M6 heat inserts, bolts. Backbone and handle-lock counts are inferred from the M04 pictures (low/medium).

## C11 (C11)
expected 17 copies / 14 files; planner 17 copies (+ spares) / 14 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S1F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 + p.16 (S1F Facade, Facades folder); M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S4/Boxes/S4 Box 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 p.3-7 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S4/Modules/S4 Module 1f.stl | 1 | 1 |  | ok | high M01 p.11 Drawers Naming (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/01. S Families/S4/Roofs/S4 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; M01 p.11 S3 Grid Roof; file name  |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 1 | 1 | 1 | ok | high M02 p.6 step 8 (1 cap on a 1F S facade); count for other facades = exposed 9 mm counterbores measured on the facade STL (the bolt hole under the label slot excluded) S1F facade: 1 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1 (one key lock per facade)  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.11 Label; M02 p.5 + p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 1 | 1 |  | ok | high M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (1 on S and M modules, 2 on L, XL and L2 modules, from the STL)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 2 | 2 | 1 | ok | high M01 p.11 Runner Stopper; M02 p.8 step 11 (2, one per side; the module has one stopper slot per side per floor)  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Guide.stl | 2 | 2 |  | ok | high M01 p.11 x3 Runner Guides (2 shown); M02 p.7 step 9 (2, one per side); depth from file name  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Slide.stl | 2 | 2 |  | ok | high M01 p.11 x3 Runner Slides (2 shown); M02 p.4 step 6 (2, one per side)  |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15 (file Springs highlights both springs); M02 p.2 step 3 (2 springs per facade); file holds 2 springs (2 bodies) One file = the 2 springs of one facade. |
| 03. MODIFICATIONS/Base/S/S4 Base.stl | 1 | 1 |  | ok | high M04 p.17 Casters Mode (flip the base, 4 casters with M8 bolts); M01 p.1 note 6 (caster holes are M8) Casters are bought, not printed. No rod, no bushings. |

Oracle notes: S4 base in casters mode: 4 bought casters (M8) screwed under the base; nothing else printed for the casters. No wheels, no feet, no backbone. Default grid roof on top.

## C12 (C12)
expected 23 copies / 16 files; planner 23 copies (+ spares) / 16 files; 2 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/05. XL Families/XL Facade 1F.stl | 1 | 1 |  | ok | high M01 p.11 + p.16 (S1F Facade, Facades folder); M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/05. XL Families/XL3/Boxes/XL3 Back Panel.stl | 1 | 1 |  | ok | medium File name / folder (XL3 Boxes folder holds Box 1F + Back Panel; the box is exported open-backed). Not shown in any manual page. One back panel per XL3 box. |
| 01. DRAWERS/05. XL Families/XL3/Boxes/XL3 Box 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 p.3-7 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/05. XL Families/XL3/Modules/XL3 Module 1F.stl | 1 | 1 |  | ok | high M01 p.11 Drawers Naming (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/05. XL Families/XL3/Roofs/XL3 Heavyweight Roof Cut.stl | 0 | 1 |  | **GAP** |    |
| 01. DRAWERS/05. XL Families/XL3/Roofs/XL3 Heawyweight Roof.stl | 1 | 0 |  | **GAP** | medium M01 p.10 Roof Types (3. heavyweight); file name Alternative in the same folder: "XL3 Heavyweight Roof Cut.stl" (corners cut, 337 x 320 mm, fits a 340 x 320 / 350 mm bed; the uncut one, 366 x 348 mm, fits no bed up to 350 x 350). Print one of the two. |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 3 | 3 | 1 | ok | medium M02 p.6 step 8 (1 cap on a 1F S facade); count for other facades = exposed 9 mm counterbores measured on the facade STL (the bolt hole under the label slot excluded) XL1F facade: 3 cap(s). |
| 01. DRAWERS/07. Universal/Heawyweight Roof Handle.stl | 1 | 1 |  | ok | high M01 p.10 (bar between the two bins); file name  |
| 01. DRAWERS/07. Universal/Heawyweight Roof Insert.stl | 2 | 2 |  | ok | low File name only; the bar has two ends, one insert per bin wall No manual page shows the inserts. Reading B: 1. |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1 (one key lock per facade)  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 1 | 1 |  | ok | high M01 p.11 Label; M02 p.5 + p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (1 on S and M modules, 2 on L, XL and L2 modules, from the STL)  |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 2 | 2 | 1 | ok | high M01 p.11 Runner Stopper; M02 p.8 step 11 (2, one per side; the module has one stopper slot per side per floor)  |
| 01. DRAWERS/07. Universal/Runners/XL Runners/x3 Runner Guide XL.stl | 2 | 2 |  | ok | high M01 p.11 x3 Runner Guides (2 shown); M02 p.7 step 9 (2, one per side); depth from file name; XL Runners subfolder for XL  |
| 01. DRAWERS/07. Universal/Runners/XL Runners/x3 Runner Slide XL.stl | 2 | 2 |  | ok | high M01 p.11 x3 Runner Slides (2 shown); M02 p.4 step 6 (2, one per side); XL Runners subfolder for XL  |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15 (file Springs highlights both springs); M02 p.2 step 3 (2 springs per facade); file holds 2 springs (2 bodies) One file = the 2 springs of one facade. |

Oracle notes: XL3 = XL family, depth 3, only made in 1F (no 2F/4F XL). XL box comes with a separate back panel. XL runners are the "XL Runners" ones. XL module has 2 latch pockets; XL facade 3 cap counterbores. Bed fit (as exported, any rotation about Z): see expected.md. Nothing of the module, box, back panel, facade or roof fits 180x180 or 256x256; all the small parts fit both.

## C13 (C13)
expected 32 copies / 15 files; planner 32 copies (+ spares) / 15 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S1F (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11 + p.16 (S1F Facade, Facades folder); M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S4/Boxes/S4 Box 1F.stl | 2 | 2 |  | ok | high M01 p.11 (S3 Box 1F); M02 p.3-7 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/03. L Families/L4/Roofs/L4 Table Roof.stl | 1 | 1 |  | ok | medium M01 p.10 Roof Types (2. table); L2 families have no roofs: the module is L wide, so the L4 roof  |
| 01. DRAWERS/04. L┬▓ Families/L4┬▓/L4┬▓ Module 1F.stl | 1 | 1 |  | ok | medium M01 p.15 folder list (04. L2 Families); file name; module front has two S-width bays (measured: 329.8 mm wide = 2 x 164.8, two openings) The folder name on disk is the mojibake "L┬▓" for "L2". |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 2 | 2 | 1 | ok | high M02 p.6 step 8 (1 cap on a 1F S facade); count for other facades = exposed 9 mm counterbores measured on the facade STL (the bolt hole under the label slot excluded) S1F facade: 1 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 2 | 2 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1 (one key lock per facade)  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 2 | 2 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 2 | 2 |  | ok | high M01 p.11 Label; M02 p.5 + p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | medium M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (1 on S and M modules, 2 on L, XL and L2 modules, from the STL)  |
| 01. DRAWERS/07. Universal/L┬▓ Accessories/x4 Accessory 1st.stl | 1 | 1 |  | ok | low File name/folder only (07. Universal/L2 Accessories, listed M01 p.15); no manual page Purpose not documented (two 6 x 138 x 3 mm strips in one file). Assumed one per L2 module of depth 4. |
| 01. DRAWERS/07. Universal/L┬▓ Accessories/x4 Accessory 2nd.stl | 1 | 1 |  | ok | low File name/folder only; no manual page One 4.2 x 140.8 x 10.5 mm bar. Assumed one per L2 module of depth 4. |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 4 | 4 | 1 | ok | high M01 p.11 Runner Stopper; M02 p.8 step 11 (2, one per side; the module has one stopper slot per side per floor)  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Guide.stl | 4 | 4 |  | ok | high M01 p.11 x3 Runner Guides (2 shown); M02 p.7 step 9 (2, one per side); depth from file name  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Slide.stl | 4 | 4 |  | ok | high M01 p.11 x3 Runner Slides (2 shown); M02 p.4 step 6 (2, one per side)  |
| 01. DRAWERS/07. Universal/Springs.stl | 2 | 2 | 1 | ok | high M01 p.15 (file Springs highlights both springs); M02 p.2 step 3 (2 springs per facade); file holds 2 springs (2 bodies) One file = the 2 springs of one facade. |

Oracle notes: L²4 = L-squared family: an L-wide 1F shell with two S-wide bays; the "04. L2 Families" folders only hold modules, so the drawers are S4 boxes with S1F facades (2 complete S drawer kits) and the roof is the L4 one. Each box sits alone in its bay: no geared rails. L2 accessories counts are guesses (no documentation).

## C14 (C14)
expected 29 copies / 24 files; planner 29 copies (+ spares) / 24 files; 0 gap(s)

| file | expected | planner | spares | | oracle source / note |
|---|---|---|---|---|---|
| 01. DRAWERS/01. S Families/Facades/S1F (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 + p.16 (S1F Facade, Facades folder); M02 p.1 step 1, p.6 step 7; facade height = drawer height  |
| 01. DRAWERS/01. S Families/S4/Boxes/S4 Box 1F.stl | 1 | 1 |  | ok | high M01 p.11 (S3 Box 1F); M02 p.3-7 steps 4-10 (one box per drawer); file name  |
| 01. DRAWERS/01. S Families/S4/Modules/S4 Module 1f.stl | 1 | 1 |  | ok | high M01 p.11 Drawers Naming (S3 1F Module); M02 p.7 step 10; file name  |
| 01. DRAWERS/01. S Families/S4/Roofs/S4 Grid Roof.stl | 1 | 1 |  | ok | high M01 p.10 Roof Types; M01 p.11 S3 Grid Roof; file name  |
| 01. DRAWERS/02. M Families/M5/Roofs/M5 Grid Roof.stl | 1 | 1 |  | ok | medium Config asks for a grid roof on the case. M01 p.8: sustainers and drawers stack; the case lid top has the same connect features as a module top (M01 p.17). File = the drawers grid roof of the same footprint. Printed in addition to the case lid, which stays. |
| 01. DRAWERS/07. Universal/Facade Cap.stl | 1 | 1 | 1 | ok | high M02 p.6 step 8 (1 cap on a 1F S facade); count for other facades = exposed 9 mm counterbores measured on the facade STL (the bolt hole under the label slot excluded) S1F facade: 1 cap(s). |
| 01. DRAWERS/07. Universal/Key (Turn On Supports).stl | 1 | 1 |  | ok | high M01 p.11 Key Lock; M02 p.1 step 1 (one key lock per facade)  |
| 01. DRAWERS/07. Universal/Key Cap.stl | 1 | 1 | 1 | ok | high M01 p.11 Key Cap; M02 p.1 step 2  |
| 01. DRAWERS/07. Universal/Label.stl | 2 | 2 |  | ok | medium M01 p.11 Label; M02 p.5 + p.6 step 8  |
| 01. DRAWERS/07. Universal/Latch.stl | 2 | 2 |  | ok | low M01 p.11 Latch; M02 p.8 step 12; count = latch pockets under the module (1 on S and M modules, 2 on L, XL and L2 modules, from the STL) Reading A (chosen): 1 latch per S/M case, like a drawer module. Reading B: 0 (the manual never lists a latch for sustainers). |
| 01. DRAWERS/07. Universal/Runners/Runner Stopper.stl | 2 | 2 | 1 | ok | high M01 p.11 Runner Stopper; M02 p.8 step 11 (2, one per side; the module has one stopper slot per side per floor)  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Guide.stl | 2 | 2 |  | ok | high M01 p.11 x3 Runner Guides (2 shown); M02 p.7 step 9 (2, one per side); depth from file name  |
| 01. DRAWERS/07. Universal/Runners/x4 Runner Slide.stl | 2 | 2 |  | ok | high M01 p.11 x3 Runner Slides (2 shown); M02 p.4 step 6 (2, one per side)  |
| 01. DRAWERS/07. Universal/Springs.stl | 1 | 1 | 1 | ok | high M01 p.15 (file Springs highlights both springs); M02 p.2 step 3 (2 springs per facade); file holds 2 springs (2 bodies) One file = the 2 springs of one facade. |
| 02. SUSTAINERS/02. M Families/Facades/M2F Facade.stl | 1 | 1 |  | ok | medium M01 p.12 (L1F Facade / L2F Facade on the case front) Equivalent alternative: 02. SUSTAINERS/05. Universal/Facades/M2F.stl (same size and shape; differs only by faint surface detail). Print one of the two. |
| 02. SUSTAINERS/02. M Families/M5/Modules/M5 2F Module .stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 1F Dividers Module, L3 2F Sealed Module); S and M cases only come as one (flat) module per height; file name S/M cases have no Flat/Dividers/Sealed variants: this is the flat one. |
| 02. SUSTAINERS/02. M Families/M5/Roofs/M5 Roof.stl | 1 | 1 |  | ok | high M01 p.12 Sustainers Naming (L3 Roof = the hinged lid); M01 p.5 The case lid (sustainer roof). |
| 02. SUSTAINERS/05. Universal/Hinges/M Hinge Top.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL Hinge Top); file name; the S/M file is one piece (the L-XL file holds 2)  |
| 02. SUSTAINERS/05. Universal/Hinges/S-M 2-4F Hinge.stl | 1 | 1 |  | ok | medium M01 p.12 (L-XL 1F Hinge / L 2-4F Hinge); M01 p.17 (2 hinges per case); file holds 2 hinge leaves (2 bodies) One file = both hinge leaves of one case. |
| 02. SUSTAINERS/05. Universal/Locks/1 SET OF PINS FOR 1 LOCK.stl | 1 | 1 | 1 | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two; file name says one set per lock (4 pins)  |
| 02. SUSTAINERS/05. Universal/Locks/LOCK HOLDER.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two  |
| 02. SUSTAINERS/05. Universal/Locks/LOCK INNER PART.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two  |
| 02. SUSTAINERS/05. Universal/Locks/LOCK OUTER PART 2-4F.stl | 1 | 1 |  | ok | medium M01 p.12 (Lock Holder, Lock Inner Part, Lock Outer Part 1F/2F); M01 p.8 Stacking Options: S and M cases show ONE lock, L and XL cases two  |
| 02. SUSTAINERS/05. Universal/Rods/S-M Rods.stl | 1 | 1 | 1 | ok | medium M01 p.12 (L-XL Rods, orange pins); file holds 2 rods (2 bodies) One file = both hinge rods. |

Oracle notes: Stack A = C01 (S4 1F drawer + S4 Grid Roof), stack B = C07 (M5 2F case + M5 Grid Roof). Combined: Label = 1 (A) + 1 (B, 2F case uses the drawers Label) = 2; Latch = 1 + 1 (case latch low confidence).
