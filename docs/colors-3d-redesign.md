# Colours and 3D view: redesign brief

Mockups (interactive, press Play): https://claude.ai/artifact/40d863dc-76fe-4420-b13b-42b99025f5c8
Artboards: "1 · Colors" (Main), "2 · Le sélecteur unique" (Picker), "3 · Atelier 3D" (Studio).
Approved by the user. Talk to the user in French. Work on `feat/3d-stack-viewer` or a branch off it; commit only when asked.

## Problems with what is there now (src/template.html)
- Colour is chosen in four places (Colors panel, part preview `filamentMenu`, 3D bubble `rolePicker`, per-unit
  `unitColors` folded in the 3D side list), each opening the same ~80-row list (`filamentList`).
- 14 roles (`R.ROLES`), each with its own drop-down: no overview of which part gets which filament.
- Picking a Bambu colour silently adds it to the palette (`addPaletteColor`), though each new colour means one more
  filament and its own plates.
- Two 3D behaviours: opened from step 1 (`mode.global`) a click picks a colour; from step 2 a click opens a drawer.

## Target, in three steps (each one testable on its own)

### 1. One filament picker, used everywhere
Replaces `filamentList` / `filamentMenu` / the `rolePicker` list / `unitColors`' menus.
- Header: the role's label and where it was opened from (e.g. "L7 · 2F, clicked in 3D").
- Scope switch when a unit is known: "Whole project" / "Only this <unit>" (writes `colorPrefs.roles` or `cfg.colors`).
- "In your tray": the palette as chips.
- Bambu Lab: search by name or colour code, filter chips (All, PLA Basic, PLA Matte, PETG Basic, PETG Matte), a swatch
  grid sorted by shade (neutrals light→dark, then hue).
- Footer: the chosen colour with its line and code, and a button that says what happens: "Use it" (already in the tray)
  or "Add as slot N" (new filament), plus "Your own color…".
- Opens as a popover; inside dialogs (part preview, 3D side column) it opens in place as today.

### 2. Colors panel = filament tray + colour map
Same data (`colorPrefs.palette`, `colorPrefs.roles`, units' `cfg.colors`); saved choices stay valid.
- Tray: one card per palette colour, numbered like the Bambu project's filament slots (slot 1 first, TPU fixed in 2,
  others from 3), with name, line/code and how many roles use it; an "Add a filament" card (opens the picker).
- "Start from" presets: USSA render (today's reset), Two-tone, One color.
- Colour map: roles × slots as radio dots, grouped Outside (shell, facade, roof, base), Inside (box, interior,
  dividers, label), Mechanics (runners, lock, hinge, accent, fittings), Other (aids). A tag on a role when some units
  have their own colour for it ("1 unit").

### 3. One 3D view with three tools
Merge `open3d`'s global and stack modes.
- Toolbar: Turn / Paint / Drawers; views Front / ¾ / Side; toggles "Spread units" (explode vertically) and "Hide roof".
- Paint: a brush bar with the tray's colours (+ "More…" opens the picker) and a scope switch "Same part everywhere" /
  "This unit only"; a click paints the clicked part's role. Hover highlights every part the click would change.
- Drawers: a click opens or closes a drawer. Turn: a click selects.
- Side column: "Selected" card (role, colour, project or this unit only, "Back to the project color"), then units top
  to bottom with load status and progress, their role swatches (ringed when the unit has its own), and
  "Not placed yet: …".

## Keep
- Hard rules in CLAUDE.md (one HTML file, three.js only on open, no USSA geometry, rebuild after any `src/` change).
- `paintLines`, plate grouping, filament totals and the Bambu project must keep following the choices.
- Test with real files in Chrome or Firefox (Claude's built-in browser can't pick a folder).
