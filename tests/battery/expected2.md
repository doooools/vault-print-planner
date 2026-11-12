# Parts test battery, round 2: expected printed parts (independent oracle)

Same independence rules as round 1 (`expected.md`): built only from the Vault STL tree (names, folders, bounding
boxes, body counts and shapes measured on the STLs), the four scanned manuals and the instruction pictures shipped
in the download (`01. DRAWERS/07. Universal/Grid Dividers/01. INSTRUCTIONS/*.jpg`). No planner code, data or output
was read. `expected2.json` holds the lists (path relative to the Vault root, qty, source, confidence, note,
`bbox_mm`, and a `total_pieces` per config). Manual page numbers as in `expected.md` (M01 instructions,
M02 drawer assembly, M04 modifications, M05 mounting).

## Rules applied in this round

Rules given by the user (owner of the Vault), they replace round 1's:
- **Runners: one pack per F of the module**: 2 runner guides + 2 runner slides + 2 runner stoppers per 48 mm level of
  the module, whatever the drawers in it (2F module = 4/4/4, 4F = 8/8/8). Guide and slide depth = module depth
  (`x<d> Runner Guide/Slide`, XL: `XL Runners/x<d> … XL`). For L² and XL² shells (two bays side by side) I apply it **per
  bay** (each bay has its own runner column): medium confidence.
- **Hidden key**: `Hidden Key (Turn On Supports)` one per drawer (replaces `Key`); `Hidden Key Part 2 (Turn on Supports)`
  (the removable key) **one per stack**.
  - **Key Cap with the hidden key: I found evidence and list 1 per Hidden Key Part 2 (medium).** The top tab of
    `Hidden Key Part 2` measures 27.7 × 9.8 mm, identical to the tab of `03. MODIFICATIONS/Backbone/Handle Lock Knob Part 1`,
    which M04 p.13 step 16 caps with `Handle Lock Knob Part 2`; that cap has the same size and nearly the same mesh as
    `Key Cap` (37.8 × 13.17 × 11.67 mm both, 78 774 vs 78 502 triangles). The standard `Key` tab is 27.7 × 9.1 and takes the
    Key Cap (M02 step 2). So the removable hidden key is a knob that takes a Key Cap. Reading B (coordinator's default): 0.

Conventions given by the coordinator: no spares, printed parts only; Bambu H2S bed 340 × 320 × 340 mm (whole vs split
chosen by fit, see below); geared rails off for a single drawer, on (one `<W> Rails` file per box) when a module holds
several drawers (M02 p.4 step 5); grid roof without top handle unless stated; only the top level gets a roof, a level of
two units side by side takes one roof of the combined width (M01 p.8); cases keep their own lid and get the stated roof
on top; case label: `Label for Sustainers` on 1F, the drawers' `Label` on 2F/4F, one per case; base without wheels has
no foot.

Rules kept from round 1 (see `expected.md` "General rules found"): per drawer 1 box, 1 facade (drawer height), Key + Key
Cap (or hidden key), 1 `Springs` file (both springs), 1 `Label`, facade caps by facade (S1F 1, S2F/S4F 3, M1F 3, M2F/M4F 5,
L1F 3, L2F/L4F 5, XL 1F 3; measured counterbores, medium except S1F); latches per module: S/M 1, L/XL/L²/XL² 2; XL3–XL5
boxes have a separate `Back Panel`; heavyweight roof = roof + 1 `Heawyweight Roof Handle` + 2 inserts (low); cases:
module + lid + facade + 1 hinge file (2 hinges) + 1 hinge-top file + 1 rods file + 1 lock set per lock (S/M 1 lock,
L/XL 2) + label + latch (low).

### Whole or split on the H2S (340 × 320 × 340)
Measured with the STL as exported, any rotation about Z, and the exported height:
- Every whole file used in this round fits, including `S6 Base Whole` (164.8 × 52.2 × 282.1), `M6 Roof Whole`
  (195.9 × 182.9 × 282.1), `L6 Roof Whole` (251.3 × 234.3 × 282.1) and the XL modules (339.6–339.8 × 319.7–319.9, a
  0.2 mm margin). So the whole lids and bases are listed; the split alternatives (Part 1 + Part 2 + `Connector For Split
  Roof`, or base Part 1 + Part 2) are given in the part notes.
- `XL6 Box 1F` exists **only** split (`Part 1` + `Part 2`, no whole file, no back panel file): both parts are listed.
- Drawer boxes of depth 6–7 in S/M/L are single files (e.g. `L7 Box 2F` 299 × 311.8) and fit.

### New sources in this round
- **Grid dividers** (`Grid Dividers/01. INSTRUCTIONS`): `01. instructions.jpg`: a full-width divider is named after the
  width ("10-S" for S boxes, "18-M" for M); "after we printed and installed a 10-S divider, we need to add two border
  parts"; a divider is pinned at two holes (two pin circles per divider in steps 2 and 5); perpendicular dividers use a
  generic number. `widths.jpg`: full widths 10-S, 18-M, 26-L, 32-XL. `depth.jpg`: full depths x3 = "10-S, x3",
  x4 = "14, x4", x5 = "18-M, x5", x6 = "22, x6", x7 = "26-L, x7".
- **Wall mount** (M05 p.1–10): each module size has its own wall-mount plate; a "second part" (the cleat screwed to
  the wall) goes in each trapezoid opening; the 1F plates have one opening, the 2F/4F plates two (measured on the STLs).
- **Pegboard** (M04 p.15 step 20): pegboards (IKEA or USSA) attach on backbones.
- **L² / XL² shells**: front openings measured: `L5┬▓ Module 2F` two S-wide bays; `XL4┬▓ Module 1F` an M bay (246 mm) and an
  S bay (157 mm). The L² / XL² folders hold only modules, so the drawers are S/M kits, the roofs come from the L / XL folders.
- **XL case facade**: no XL case facade file exists. XL = S + M (M01 p.8) and 164.8 + 254.0 = 418.8 mm = the XL width,
  so I list the S1F + M1F case facades (**low**).

## Per configuration (lines / total pieces)

| Id | Lines | Pieces | Summary |
|---|---|---|---|
| D01 | 13 | 24 | S3 2F, one 2F drawer: 2 runner packs (4/4/4 x3), S2F facade 3 caps, 1 latch, S3 Grid Roof |
| D02 | 13 | 36 | S5 4F, one 4F drawer: 4 packs (8/8/8 x5), S4F facade 3 caps, S5 Table Roof |
| D03 | 13 | 18 | M3 1F: 1 pack x3, M1F 3 caps, M3 Bowl Roof |
| D04 | 16 | 36 | M6 2F, two 1F hidden-key drawers: 2 packs x6, 2 × M Rails, 2 Hidden Key, 1 Hidden Key Part 2, 1 Key Cap (medium), caps 6, M6 Grid Roof + Top Handle |
| D05 | 14 | 51 | M7 4F, two 2F drawers: 4 packs x7, 2 × M Rails, caps 10, M7 Under Table Mount Roof |
| D06 | 15 | 22 | L3 1F: 2 latches, 1 pack x3, L1F 3 caps, L3 Heawyweight Roof + handle bar + 2 inserts (low) |
| D07 | 14 | 36 | L6 2F, two 1F drawers: 2 packs x6, 2 × L Rails, caps 6, 2 latches, L6 Grid Roof |
| D08 | 17 | 63 | L7 4F, 1F + 2F + 1F: 4 packs x7, 3 × L Rails, caps 11, 3 × L7 Baseplate (medium, see below), 2 latches, L7 Grid Roof |
| D09 | 14 | 20 | XL5 1F: box + back panel, XL facade 3 caps, 1 XL pack x5, 2 latches, XL5 Table Roof |
| D10 | 14 | 20 | XL6 1F: box Part 1 + Part 2 (only split exists), 1 XL pack x6, 2 latches, XL6 Grid Roof |
| D11 | 15 | 32 | XL²4 1F shell + S4 1F kit + M4 1F kit, 1 pack per bay (x4), 2 latches (medium), XL4 Grid Roof |
| D12 | 15 | 48 | L²5 2F shell + 2 S5 2F kits, runners 2 bays × 2F = 4 packs (8/8/8 x5, medium), caps 6, L² x5 accessories 1 + 1 (low), L5 Bowl Roof |
| D13 | 13 | 18 | Case L4 1F Flat: L4 Roof lid, L1F case facade, L-XL 1F hinge set, 2 locks (outer 1F), Label for Sustainers, 2 latches (low), L4 Grid Roof |
| D14 | 13 | 18 | Case L5 2F Dividers: L5 Roof lid, L2F facade, L 2-4F Hinge, 2 locks (outer 2-4F), drawers Label, 2 latches (low), L5 Table Roof |
| D15 | 14 | 19 | Case XL3 1F Sealed: `XL3  Roof.stl` lid, S1F + M1F case facades (low), L-XL 1F hinge set, 2 locks, Label for Sustainers, 2 latches (low), XL3 Grid Roof |
| D16 | 13 | 13 | Case M6 2F: M6 Roof Whole (fits H2S), M2F facade, S-M 2-4F Hinge, M Hinge Top, S-M Rods, 1 lock (2-4F), Label, latch (low), M6 Grid Roof |
| D17 | 13 | 13 | Case S4 4F: S4 Roof lid, S4F facade, S-M 2-4F Hinge, S Hinge Top, S-M Rods, 1 lock (2-4F), Label, latch (low), S4 Grid Roof |
| D18 | 16 | 49 | S4 2F + M4 2F drawers side by side (2 packs each, x4), caps 3 + 5, one XL4 Grid Roof |
| D19 | 39 | 81 | L5 mobile stack, see below |
| D20 | 15 | 40 | XL3 Base (4 bought casters) + two XL3 1F drawers (each box + back panel, 1 XL pack x3, 2 latches), XL3 Grid Roof |
| D21 | 14 | 102 | Two M4 stacks × three hidden-key 1F drawers: 6 drawers, 2 Hidden Key Part 2, 2 Key Caps (medium), 2 M4 Grid Roofs |
| D22 | 17 | 31 | S4 1F drawer + 2 × "10-S, x3", 1 × "14, x4", 6 straight edge pieces 20 mm (medium), 6 tight pins (low), S4 Grid Roof |
| D23 | 14 | 25 | S4 2F drawer (2 packs, S2F 3 caps) + `S4 Baseplate_With 2 Handles`, S4 Grid Roof |
| D24 | 15 | 20 | M5 1F drawer + `M1F Wall Mount` + 1 `Wall Mount Second Part` (medium), M5 Grid Roof |
| D25 | 15 | 18 | S3 1F drawer + IKEA Skadis `S1F` + 1 `S1F Backbone` (medium), S3 Grid Roof |
| D26 | 15 | 17 | Case S3 2F + sustainers `S3 Baseplate` + 3 × `S2F Divider`, S3 Grid Roof (low: roof not stated) |
| D27 | 19 | 42 | S6 Base Whole (no wheels, no foot) + S Stationary Handle + 1 S2F Backbone (low) + drawers S6 2F (2 packs) and S6 1F (1 pack), S6 Grid Roof |
| D28 | 13 | 18 | Case L6 1F Flat: L6 Roof Whole (fits H2S), L1F facade, L-XL 1F hinge set, 2 locks, Label for Sustainers, 2 latches (low), L6 Grid Roof |

### Details worth reading

**D04, D21 (hidden key).** One `Hidden Key` per drawer; one `Hidden Key Part 2` per stack (D21: 2 for the project); one
`Key Cap` per `Hidden Key Part 2` (evidence above, medium; alternative 0). No standard `Key` and no per-drawer Key Cap.

**D08 (baseplate).** The L7 folder has one baseplate only, `L7 Baseplate.stl`, 290.4 × 302 × 25.85 mm. In S/M the plain
baseplate is 4 mm thick and the `_With 1/2 Handles` files are 25.85 mm, so the L baseplate looks like the handled kind;
the "no handle cut-outs" option is not offered for L. Listed 3 × `L7 Baseplate` (one per box), medium.

**D11 (XL²).** No accessories exist for XL²; the L² accessories are depth-matched strips for L² shells only. Latches: 2,
read from the module like XL (medium).

**D12 (L²).** `x5 Accessory 1st` (2 strips in one file) and `x5 Accessory 2nd`: purpose undocumented; 1 + 1 per L² shell
(low; alternative 0).

**D15 (XL case).** Facade: S1F + M1F case facades (low; alternative: report the XL case facade as missing from the
download). Locks 2 (one behind each facade). One label (coordinator convention), though each facade has a label slot
(alternative: 2 × Label for Sustainers).

**D19 (L5 mobile stack).** Bottom to top: L5 Base + wheels (2 Bushing, 2 Disk, 2 Tyre (TPU), 2 Cover, 1 Jig, the jig being
an assembly tool, medium) + 1 L Feet; drawer L5 2F (2 packs), drawer L5 1F (1 pack), case L5 1F Flat (lid, L1F case facade,
L-XL 1F hinge set, 2 locks, Label for Sustainers); L5 Table Roof on the case lid. Pull-out handle and what it needs (M04
p.13–14, M01 p.13): `L Pull-out Handle`, `L Pull-out Handle Lock` (alternative 2 × `Universal Pull-out Handle Lock`),
2 × `Handle Lock Knob Part 1`, 2 × `Handle Lock Knob Part 2`, and backbones to carry the M16 rods: **2 × `L2F Backbone`
(low)**: tower = base (1 level) + 2F + 1F + 1F = 5 levels, the lock takes the top level, 4 levels of backbone = 2 × 2F
(alternatives: L2F + 2 × L1F, or Universal backbones). Latches 2 + 2 + 2 (the case's 2 are low; the JSON line shows the
merged confidence "low" for all 6). Facade caps 5 + 3 = 8. Bought: M16 axle rod 414 mm, 2 M16 handle rods, 6205ZZ, SCSAW,
heat inserts.

**D20.** Casters are bought (M8, M04 p.17): nothing printed for them.

**D22 (grid dividers).** Full width S = `10-S, x3`; full depth 4 = `14, x4` (both from the 20MM TALL folder).
Border parts: 2 per divider = 6 `Straight Edge Piece 20MM` (medium; if the full-depth divider butts against a full-width
one it takes one border part, 5). Pins: 2 per divider = 6 `grid divider pin_tight` (low; one pin per file, measured;
the pictures show two pin circles per divider, but a longer divider may take more).

**D24 (wall mount).** `M1F Wall Mount` (the plate on the module back) + 1 `Wall Mount Second Part` (wall cleat, one per
trapezoid opening; the 1F plate has one). Medium. M05 notes that 1F wall mounts work but cannot serve as templates later.

**D25 (pegboard).** `IKEA Skadis Pegboard/S1F.stl` (122.8 × 47 × 5 mm) + the backbone it mounts on: 1 × `S1F Backbone`
(medium; alternative 2 × `Universal 1F Backbone`).

**D26 (case S3 2F).** Sustainer gridfinity baseplate `02. SUSTAINERS/05. Universal/Baseplates/01. S/S3 Baseplate.stl` (not
the drawers one) and 3 × `S Dividers/S2F Divider.stl`. No roof was stated: `S3 Grid Roof` listed from the battery default
(low; alternative: none, the case lid closes the stack).

**D27 (stationary handle).** M04 p.12: the stationary handle is fixed from the back of a backbone part. Listed 1 ×
`S2F Backbone` (low): the first backbone is a 2F one tying base and the first (2F) module (M04 p.7–10). Alternatives:
backbones on the whole height (2 × S2F), or Universal backbones. `S6 Base Whole` fits the H2S (alternative Part 1 + Part 2).

## Low-confidence items
1. Latch on cases (D13–D17, D19, D26, D28): S/M 1, L/XL 2 per case; alternative 0.
2. D15: S1F + M1F case facades for the XL case (no XL case facade exists).
3. D06: heavyweight roof inserts × 2 (alternative 1).
4. D12: L² x5 accessories 1 + 1 (alternative 0).
5. D19: 2 × L2F Backbone; D27: 1 × S2F Backbone (counts depend on how far the backbone runs).
6. D22: 6 tight pins (2 per divider).
7. D26: S3 Grid Roof on the case (roof not stated).

Medium items to keep in mind: Key Cap with the hidden key (D04, D21), runners per bay in L²/XL² (D11, D12), the L7
baseplate variant (D08), edge pieces (D22), wall-mount cleat count (D24), pegboard backbone (D25), Jig (D19), facade caps
other than S1F, case hinge/lock/facade files.
