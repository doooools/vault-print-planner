# Parts test battery: expected printed parts (independent oracle)

Built only from USSA's own material: the STL tree of the Vault download (names, folders, bounding boxes,
body counts, and shapes measured on the STL), and the four scanned PDF manuals. No planner code, data or
output was read. `expected.json` holds the machine-readable lists (path relative to the Vault root, quantity,
source, confidence, note, bounding box). This file explains the reasoning.

Manual page numbers are PDF page numbers:
- **M01** = `01_Instructions Manual.pdf` (20 p.)
- **M02** = `02_Drawer Assembly.pdf` (8 p., "Drawer Assembly n/8" = page n)
- **M04** = `04_Modifications.pdf` (17 p., "Modifications Assembly n/15" = page n+1)
- **M05** = `05_Mounting Instructions.pdf` (12 p., wall and table mounts; not needed for these configs)

Bounding boxes are the STL's own x × y × z in mm, in the orientation the file is exported in (USSA's print
orientation). Many big parts are exported standing up or turned 45° on the bed, so x × y is not the part's
footprint in the stack.

**Path spelling.** The L² folders are spelt on disk with the mojibake `L┬▓` (U+252C U+2593) instead of `L²`, for
example `01. DRAWERS/04. L┬▓ Families/L4┬▓/L4┬▓ Module 1F.stl`. The JSON keeps that exact spelling. The sustainer
M modules have a space before the extension (`M5 2F Module .stl`), and the S4 drawer modules are spelt
`S4 Module 1f.stl` / `S4 Module 2f.stl` (lower-case f). Several names use USSA's typo "Heawyweight".

## Manual pages used

| Page | What it gives |
|---|---|
| M01 p.1 | Notes: TPU tyres; "2F modules after base and before roof" with modifications; caster holes are M8 (bought casters) |
| M01 p.3 | Hardware list (bolts only: drawers 4 × M4 14 per floor, 2 × M6 50 per roof handle; sustainers 8 × M4 10, 16 × M4 14, 7 × M4 20 per module; modifications) |
| M01 p.5 | Two types: drawers and sustainers (= cases with a hinged lid) |
| M01 p.6 | Sizes: widths S, M, L, XL; depths 3–7 (42 mm Gridfinity units); heights 1F, 2F, 4F |
| M01 p.8 | Stacking options: drawers and sustainers stack; L = S + S, XL = S + M. **S and M sustainers show one lock, L and XL sustainers two** |
| M01 p.9 | Interiors: flat / gridfinity / dividers / sealed sustainers; empty / gridfinity base / grid dividers drawers |
| M01 p.10 | Roof types: gridfinity (grid), table, heavyweight, bowl, under table mount |
| M01 p.11 | **Drawers Naming**: exploded S3 1F drawer: Top Handle, S3 Grid Roof, S3 Baseplate, 2 × x3 Runner Guides, 2 × x3 Runner Slides, 2 × S Geared Rail, Springs (2), Key Lock, S1F Facade, Facade Cap, Key Cap, Label, Latch, Runner Stopper (2), S3 Box 1F, S3 1F Module |
| M01 p.12 | **Sustainers Naming**: L3 Roof (lid), L-XL Rods, L-XL 1F Hinge, L-XL Hinge Top, L 2-4F Hinge, modules (Dividers / Sealed), dividers, Lock Holder, Lock Inner Part, Lock Outer Part 1F / 2F, L1F / L2F Facade, Label for Sustainers (1F case), Label (2F case) |
| M01 p.13 | Modifications naming: pull-out handle, handle lock + knob parts 1 and 2, pegboard, backbone, tyre, cover, disk, base, feet |
| M01 p.14–16, 20 | Folder tree ("Working with archive"); p.15 highlights both springs as the one "Springs" file |
| M01 p.17 | Sustainer hardware (2 hinges, locks) |
| M01 p.18 | Drawer hardware (Top Handle 2 × M6 50; facade M4 14 × 4 for 1F, × 6 for 2F/4F) |
| M01 p.19 | Backbone / wheels hardware (M16 rod 248 / 338 / 414 / 504 mm for S / M / L / XL base) |
| M02 p.1–8 | Drawer assembly steps 1–12 (see rules below) |
| M04 p.2–6 | Wheels: rod, 2 bushings pressed with the jig, 2 disks, bearings, collars, 2 TPU tyres, 2 covers, then one foot |
| M04 p.7–11 | Backbone: a 2F backbone ties base and first module; further backbones tie modules |
| M04 p.12 | Stationary handle: fixed from the back of a backbone part |
| M04 p.13 | Handle lock: 2 knobs (part 1 + heat insert + part 2 cap) |
| M04 p.14 | Pull-out handle with 2 M16 rods |
| M04 p.17 | Casters mode: flip the base, 4 casters with M8 bolts |

## General rules found

**Drawer (one box in its module), per drawer** (M01 p.11, M02 p.1–8):
- 1 box `<W><d> Box <h>F` (width, depth, height of that drawer).
- 1 facade `<W><h>F (Turn On Supports)` from the family's `Facades` folder (XL: `XL Facade 1F`). The facade height is
  the drawer's height (1F 47 mm, 2F 95, 4F 191), not the module's.
- 1 `Key (Turn On Supports)` + 1 `Key Cap` (M02 steps 1–2).
- 1 `Springs` file: it holds both springs of one facade (2 bodies; M02 step 3 uses two).
- 1 `Label` (M02 step 8).
- Facade caps: one per exposed bolt counterbore on the facade (M02 step 8 shows the single one of an S1F facade;
  the others measured on the facade STLs: 9.2 mm counterbores, 4.1 mm deep, the cap is 9.8 × 3.8 mm; the bolt
  hole under the label slot is covered by the label):

  | Facade | S | M | L | XL |
  |---|---|---|---|---|
  | 1F | 1 | 3 | 3 | 3 |
  | 2F | 3 | 5 | 5 | – |
  | 4F | 3 | 5 | 5 | – |

  This matches M01 p.18: the (L) facade takes 4 bolts in 1F and 6 in 2F/4F, one of them under the label.
- 2 runner guides + 2 runner slides of the depth (`x<d> Runner Guide/Slide`; XL uses `XL Runners/x<d> … XL`), the same
  for 1F, 2F and 4F boxes (a 2F box has a single runner groove per side, measured).
- 2 `Runner Stopper` (M02 step 11, one per side).
- Geared rails (`<W> Rails`, one file = top + bottom rail): **optional** for a single box, **required when more than one
  box shares a 2F or 4F module** (M02 p.4 step 5). One file per box.
- Gridfinity baseplate (option): one `<W><d> Baseplate` (plain) per box, from the family's `Gridfinity Baseplate` folder.
- Hidden key lock (option, not documented): `Hidden Key` replaces `Key`; `Hidden Key Part 2` is a removable turning key.

**Module (shell)**: one `<W><d> Module <H>F` per unit, whatever the number of drawers in it. A 4F module has 4 runner
levels and 4 stopper slots per side, a 2F module 2 (measured), so it takes 1F/2F/4F boxes in any combination that adds up.

**Latch**: one per latch pocket under the module (M02 step 12; pockets counted on the STL): S 1, M 1, L 2, XL 2,
L² 2. The latch locks a module to the unit below (or the base). Sustainer modules have the same pocket underneath,
although M01 p.12 lists no latch for them (low confidence).

**Roof**: one roof per stack, on the top unit only, from the top unit's family and depth (`<W><d> Grid Roof`, etc.). A
roof needs no latch. The grid roof's `Top Handle (Turn On Supports)` is optional (1 per roof, 2 × M6 50). Heavyweight
roofs exist only for L and XL; they take 1 `Heawyweight Roof Handle` and (undocumented) inserts. A level of two units
side by side (S + S = L, S + M = XL) takes one roof of the combined width (M01 p.8).

**Between stacked units**: nothing printed beyond each module's own latch. Backbones (`03. MODIFICATIONS/Backbone`)
are an optional modification, needed only for the handles and pegboards.

**Case (sustainer)** per case (M01 p.12, p.17, p.8; body counts of the files):
- 1 module (`<W><d> <H>F Module`; S and M are made only as one flat module; L and XL have Flat / Dividers / Sealed).
- 1 lid = the sustainer's `<W><d> Roof` (always, even when another roof sits on top).
- 1 facade `<W><H>F Facade` (family `Facades` folder; `05. Universal/Facades/<W><H>F.stl` is the same part, an alternative).
- Hinges: 1 hinge file (`S-M 1F Hinge` or `S-M 2-4F Hinge`, L: `L-XL 1F Hinge` / `L 2-4F Hinge`; 2 leaves per file),
  1 `S Hinge Top` / `M Hinge Top` (L-XL: one file with 2 tops), 1 rods file (`S-M Rods` / `L-XL Rods`, 2 rods per file).
- Locks: S and M cases 1 lock, L and XL cases 2 (M01 p.8). Per lock: `LOCK HOLDER`, `LOCK INNER PART`,
  `LOCK OUTER PART 1F` (or `2-4F`), `1 SET OF PINS FOR 1 LOCK`.
- Label: `Label for Sustainers` on a 1F case, the drawers' `Label` on a 2F case (M01 p.12; slot widths measured 38 / 48 mm).
- Latch: 1 (S/M), low confidence (see above).

**Base and modifications** (M04): base `<W><d> Base` (depth 6 and 7 also come as Part 1 + Part 2). Wheels: 2 `Bushing`,
2 `Disk`, 2 `Tyre (TPU)`, 2 `Cover`, plus the `Jig` tool and one `<W> Feet` at the other end. Casters are bought (M8),
nothing printed. Stationary handle: 1 `<W> Stationary Handle` on a backbone part. Pull-out handle: 1 `<W> Pull-out Handle`
+ 1 `<W> Pull-out Handle Lock` + 2 `Handle Lock Knob Part 1` + 2 `Handle Lock Knob Part 2`.

## Per configuration

Counts are "lines / total pieces". Default everywhere: standard key, empty box, no rails unless required, grid roof
without top handle.

### C01 — Drawer S4 1F, grid roof, no top handle (13 lines / 16 pieces)
S4 Module 1f, S4 Box 1F, S1F facade, Key, Key Cap, Springs, Label, 1 Facade Cap, 2 × x4 Runner Guide, 2 × x4 Runner
Slide, 2 × Runner Stopper, 1 Latch, S4 Grid Roof. All high confidence (M01 p.11, M02 p.1–8).

### C02 — Drawer M4 2F, one drawer, grid roof with top handle (14 / 21)
M4 Module 2F, M4 Box 2F, M2F facade, Key, Key Cap, Springs, Label, **5 Facade Caps** (M2F facade, measured), 2 + 2 x4
runners, 2 stoppers, 1 Latch (M module: one pocket), M4 Grid Roof, Top Handle. No geared rails (one box).

### C03 — Drawer L5 4F with a 2F and two 1F drawers (16 / 54)
L5 Module 4F; boxes L5 Box 2F + 2 × L5 Box 1F; facades L2F + 2 × L1F; 3 Keys, 3 Key Caps, 3 Springs, 3 Labels;
Facade Caps 5 + 3 + 3 = **11**; 6 x5 Runner Guides, 6 x5 Runner Slides, 6 stoppers; **3 × L Rails** (required: several
boxes in one 4F module); **2 Latches** (L module); L5 Grid Roof.

### C04 — Drawer S4 4F with four 1F drawers (14 / 59)
S4 Module 4F; 4 × S4 Box 1F, 4 × S1F facade, 4 Keys, 4 Key Caps, 4 Springs, 4 Labels, 4 Facade Caps; 8 + 8 x4 runners,
8 stoppers; **4 × S Rails** (required); 1 Latch; S4 Grid Roof.

### C05 — Drawer S3 2F, two 1F drawers, hidden key, Gridfinity baseplate (16 / 35)
S3 Module 2F; 2 × S3 Box 1F, 2 × S1F facade, 2 Springs, 2 Labels, 2 Facade Caps; 4 + 4 x3 runners, 4 stoppers;
2 × S Rails (required); 1 Latch; **2 × S3 Baseplate** (drawers folder, plain); S3 Grid Roof. Lock:
- `Hidden Key (Turn On Supports)` × 2 instead of `Key` (medium: same pinion as the Key, flush slotted top).
- `Hidden Key Part 2` × 2 (**low**): the removable turning key (its tongue fits the slot). Reading A (chosen): one per
  hidden lock, from the "Part 2" pairing. Reading B: one per project.
- `Key Cap` × 2 (**low**): Part 2 has the same knob as the Key (and the Handle Lock Knob Part 2, a key-cap-sized cap,
  goes on a knob of the same size). Reading B: 0.
No manual page documents the hidden key.

### C06 — Case S4 1F, flat, grid roof on the case (13 / 13)
S4 1F Module (sustainers), S4 Roof (the lid), S1F Facade (sustainers), S-M 1F Hinge, S Hinge Top, S-M Rods, 1 lock set
(LOCK HOLDER, LOCK INNER PART, LOCK OUTER PART 1F, 1 SET OF PINS), Label for Sustainers, Latch (**low**), and the drawers'
**S4 Grid Roof** on top of the lid (medium: M01 never shows a drawer roof on a case, but the lid's top has the module-top
connectors, M01 p.17, and drawers stack on sustainers, M01 p.8 and p.17 casters picture).

### C07 — Case M5 2F, flat, grid roof on the case (13 / 13)
M5 2F Module (sustainers, file `M5 2F Module .stl`), M5 Roof (lid), M2F Facade (sustainers), **S-M 2-4F Hinge**, **M Hinge
Top**, S-M Rods, 1 lock set with **LOCK OUTER PART 2-4F**, drawers **Label** (2F case), Latch (low), drawers M5 Grid Roof.

### C08 — S4 stack: drawer 1F, drawer 2F, case 1F, grid roof on top (27 / 45)
= C01 without its roof + S4 2F drawer (S4 Module 2f, S4 Box 2F, S2F facade, Key, Key Cap, Springs, Label, **3 Facade Caps**,
2 + 2 x4 runners, 2 stoppers, 1 Latch) + C06 without its grid roof + one S4 Grid Roof. Totals: Latch 3 (1 + 1 + 1 for
the case, low), Facade Caps 4, Keys 2, Labels 2 (+ 1 Label for Sustainers). Nothing printed between units.

### C09 — Two S4 1F drawers side by side under one L grid roof (13 / 31)
Two complete S4 1F drawer units (as C01 without roof: 2 modules, 2 boxes, 2 facades, 2 keys, 2 key caps, 2 springs,
2 labels, 2 caps, 4 + 4 runners, 4 stoppers, 2 latches) and **one L4 Grid Roof** (M01 p.8 rule 4: L = S + S). No S4 roof.
`03. MODIFICATIONS/Backbone/Connector for Modules 1F.stl` exists (16 mm wide middle piece of the backbone) but belongs to
the optional backbone modification: not listed.

### C10 — M4 stack: base, wheels, stationary handle, pull-out handle, drawer M4 2F (26 / 39)
- Base: M4 Base. Wheels: 2 Bushing, 2 Disk, 2 Tyre (TPU), 2 Cover (high, M04 p.2–6).
- `Jig` × 1 (medium): assembly tool to press the bushings (M04 p.3). Drop it if the comparison counts only parts that stay
  in the stack.
- `M Feet` × 1 (medium): the manual's wheel sequence ends with "attach the necessary size foot" (M04 p.6 step 8) and every
  wheeled picture has a foot at the other end. Reading B: 0 if feet are a separate option.
- `M2F Backbone` × 1 (**low**): the stationary handle is fixed to a backbone (M04 p.12) and the first backbone is a 2F one
  tying base and module (M04 p.7–10). Alternative: 2 × `Universal 2F Backbone`. The count depends on tower height.
- `M Stationary Handle` × 1, `M Pull-out Handle` × 1 (high); `M Pull-out Handle Lock` × 1 (medium; alternative
  2 × `Universal Pull-out Handle Lock`); `Handle Lock Knob Part 1` × 2 and `Part 2` × 2 (high, M04 p.13).
- Drawer M4 2F as in C02 without the top handle (5 Facade Caps, 1 Latch) and an M4 Grid Roof.
- Bought: M16 rod 338 mm (axle), 2 M16 rods for the handle, 2 × 6205ZZ, 2 SCSAW collars, 2 M6 heat inserts, bolts.

### C11 — S4 stack on a base with 4 casters (14 / 17)
S4 Base + C01 (drawer S4 1F + S4 Grid Roof). Casters are bought and bolted with M8 (M04 p.17, M01 p.1). No rod, bushing,
wheel, foot or backbone.

### C12 — Drawer XL3 1F, heavyweight roof (16 / 23)
XL3 Module 1F, XL3 Box 1F, **XL3 Back Panel** (medium: the XL3–XL5 box folders hold "Box 1F" + "Back Panel"; the box is
exported open-backed), XL Facade 1F, Key, Key Cap, Springs, Label, **3 Facade Caps**, 2 × x3 Runner Guide XL, 2 × x3 Runner
Slide XL, 2 stoppers, **2 Latches**, XL3 Heawyweight Roof (medium, see below), 1 Heawyweight Roof Handle, 2 Heawyweight Roof
Inserts (**low**: undocumented; reading B = 1). XL is made only in 1F.

Roof variants: the XL3 Roofs folder holds `XL3 Heawyweight Roof.stl` (366 × 348 mm as exported) and `XL3 Heavyweight Roof Cut.stl`
(same roof with the outer corners cut, 337 × 320 mm). Print one of them. The uncut one is listed as "the" heavyweight roof
(same name as in the L families); the Cut one is the one that fits a 340 × 320 / 350 mm bed.

Bed fit (STL as exported, any rotation about Z, part must also fit the bed height; A1 mini = 180 × 180 × 180,
256 = 256 × 256 × 256):

| Part | bbox x × y × z | smallest footprint (any Z rotation) | 180 | 256 | 350 × 350 |
|---|---|---|---|---|---|
| XL3 Module 1F | 339.6 × 319.7 × 146.1 | 57.0 × 418.8 | no | no | yes (diagonal) |
| XL3 Box 1F | 299.9 × 281.4 × 143.9 | 37.5 × 377.7 | no | no | yes |
| XL3 Back Panel | 289.3 × 271.3 × 6.3 | 37.5 × 363.7 (L-shaped, as exported) | no | no | yes |
| XL Facade 1F | 418.8 × 47.0 × 10.0 | 47.0 × 418.8 | no | no | yes (at ~38°) |
| XL3 Heawyweight Roof | 366.2 × 348.3 × 146.0 | 88.3 × 418.4 | no | no | **no** |
| XL3 Heavyweight Roof Cut (alt.) | 337.4 × 319.6 × 146.0 | 88.3 × 418.4 | no | no | yes |
| x3 Runner Guide XL | 27.0 × 143.5 × 14.7 | | yes | yes | yes |
| x3 Runner Slide XL | 18.2 × 118.2 × 16.1 | | yes | yes | yes |
| Heawyweight Roof Handle | 30.0 × 156.5 × 29.5 | | yes | yes | yes |
| Heawyweight Roof Insert | 41.8 × 16.8 × 30.1 | | yes | yes | yes |
| Latch | 96.6 × 74.6 × 4.5 | | yes | yes | yes |
| Key (Turn On Supports) | 45.0 × 36.5 × 33.4 | | yes | yes | yes |
| Key Cap | 37.8 × 13.2 × 11.7 | | yes | yes | yes |
| Springs | 47.5 × 75.6 × 5.2 | | yes | yes | yes |
| Label | 47.9 × 20.6 × 2.0 | | yes | yes | yes |
| Facade Cap | 9.8 × 9.8 × 3.8 | | yes | yes | yes |
| Runner Stopper | 7.8 × 17.9 × 8.2 | | yes | yes | yes |

So on a 180 × 180 bed (A1 mini) **and** on a 256 × 256 bed, the five big parts (module, box, back panel, facade, roof)
do not fit; every small part fits both. Not even the 256 bed's diagonal (362 mm) takes the 377–419 mm long parts.
(Not used here: `XL Rails` 248.5 mm fits 256, not 180.)

### C13 — Drawer L²4 1F, table roof (15 / 32)
`L4┬▓ Module 1F` (medium): an L-wide shell (329.8 mm = 2 × 164.8) whose front has two S-wide bays (measured). The L²
folders hold only modules, so each bay takes a full S4 1F drawer kit: 2 × S4 Box 1F, 2 × S1F facade, 2 Keys, 2 Key Caps,
2 Springs, 2 Labels, 2 Facade Caps, 4 + 4 x4 runners, 4 stoppers; **2 Latches** (2 pockets); no geared rails (one box per
bay). `x4 Accessory 1st` × 1 and `x4 Accessory 2nd` × 1 (**low**: from the `L² Accessories` folder, depth 4; no manual page
says what they are or how many). Roof: **L4 Table Roof** (no L² roofs exist; the module is L wide).

### C14 — Two stacks: A = C01, B = C07 (24 / 29)
Sum of C01 and C07. Shared files add up: Latch 2 (B's is low), Label 2 (one drawer label for A, one for the 2F case B).

## Ambiguities and low-confidence items

1. **Latch on a case** (C06, C07, C08, C14): M01 p.12 lists none, but the S4 1F sustainer module has the same latch pocket
   underneath as a drawer module. Chosen: 1 per S/M case. Alternative: 0.
2. **Hidden key** (C05): `Hidden Key Part 2` × 2 (alt. 1 per project) and `Key Cap` × 2 (alt. 0). Undocumented.
3. **Heavyweight roof inserts** (C12): 2 (alt. 1). Undocumented; the uncut vs `Cut` roof file is a choice (one of the two).
4. **L² accessories** (C13): 1 + 1, purpose unknown.
5. **C10 backbone** (low) and the **foot** and **jig** (medium): see C10.
6. **Facade caps above 1 per facade** (all 2F/4F and M/L/XL facades): from the STL geometry, not from a manual count
   (medium). The manual shows only the S1F case (1 cap).
7. **Case facade folder**: `02. SUSTAINERS/<family>/Facades/<W><H>F Facade.stl` and `02. SUSTAINERS/05. Universal/Facades/<W><H>F.stl`
   are the same part (same size and outline). Listed: the family one; either counts.
8. **Grid roof on a case** (C06, C07, C08): listed in addition to the case lid; the manuals never show this combination.
9. **Number of locks on S/M cases**: 1, read from M01 p.8 (the naming page only shows L cases, which have 2).
10. **Top Handle** is never in a default build (only C02 asks for it).

## Not printed (notes only)
Bolts M4 (10/14/20/25/40/60–100 mm), M6 (30/35/50/90 mm), M8 caster bolts, M16 rods, 6205ZZ bearings, SCSAW collars,
M6 heat inserts, casters. Drawers: 4 × M4 14 per 1F facade (L), 6 for 2F/4F; 2 × M6 50 per roof handle (M01 p.3, p.18).
