# UX audit brief, November 2026

Audit of the user journey through Design, Print and Hardware, made on `main` at `0b558cd` (2026-11-14), and the
changes Dols validated the same day on eight mockups. Talk to the user in French. Every line number below is in
`src/template.html` at `0b558cd`: find the function by name if the file has moved since.

Put this file in `docs/` next to `ux-redesign.md`. That brief still holds for everything this one doesn't change;
where the two disagree, this one wins, and "Rules of `ux-redesign.md` this brief changes" (at the end) lists the lines
to edit there. The mockups are PNG files in `ux-audit-mockups/` (flat drawings and captures of boxes, no Vault
geometry); the interactive canvas link goes in `CLAUDE.local.md`, like the previous one.

## How to use this brief

- The work is cut into **eight sessions**, one branch and one pull request each (`claude/<name>`, merging stays with
  the user). Each session is testable on its own and says what it depends on.
- Verdict of the audit: **no full redesign**. The frame (rail, view, panel on every step; stack, level, module,
  drawer; orange = action, dark = selected, blue = whole stack) stays. Three areas are reworked: Design's 3D view,
  Design's panels, Print's right column. The rest is alignment.
- **No customisation is removed.** If a session finds it has to drop a setting to follow a mockup, stop and ask.
- Hard rules of `CLAUDE.md` apply as always: one HTML file, rebuild `index.html` after any change in `src/`, run
  `tools/check.py`, test with real files in Chrome or Firefox, no USSA geometry in the repository.

## Decisions taken with the user (2026-11-14)

1. **The camera never reframes by itself.** Kept on purpose: adding a level or changing the footprint leaves the
   camera where it is (`v3keep`). The only reframing is the one the user asks for (decision 3).
2. **Level actions move to a right-click menu** in the 3D view. No action bar under the stack.
3. **Right-click on the background** offers "Fit the stack in the view", the one way to reframe.
4. **A "⋯" button in the level panel's header** opens the same menu as the right-click, for the keyboard and
   touchpads.
5. **"Duplicate" goes away**: "Add a level above" does the same thing (a copy of the level, placed above it).
6. **Undo everywhere in Design** where a gesture overwrites or removes. A confirmation is the fallback only where
   undo turns out impossible; none is expected.
7. **"Remove level" in the menu is a plain click**, followed by "Level 3 removed · Undo". Condition set by the user:
   only if undo works; otherwise it stays press-and-hold. Every other removal keeps press-and-hold (stack, filament,
   divider plan, loose parts, print progress).
8. **"Remove <stack>" leaves Print's plate options.** A stack is removed in Design.
9. **The Footprint button and its strip go away**: width and depth are edited in Stack settings.
10. **The design file moves to the header** (a "File" menu on all four steps).

## Sessions

Order: 1 first (2 can go in parallel, it touches other code). 3 and 5 need 1. 4, 6, 7, 8 are independent.

### Session 1 · Undo

Goal: any change to the stacks, the colours or the loose parts can be taken back.

- State to cover: `towers` + `seq` (`save()`, l. 1143), `colorPrefs` (`saveColors()`, l. 1093), `extras`
  (`saveExtras()`, l. 1172), and `dsel` so the selection comes back with the stack. All plain JSON.
- One way to do it without touching every handler: keep the last saved state as a string; when a save function
  runs and the state differs, push the previous string on an undo stack. One gesture often calls two save functions
  (`save()` then `saveColors()`): group what is saved in the same task into one entry. A handler names the entry
  for the message (`undoLabel = 'Two-tone applied to Rolling tool cart'`); with no name, a generic "Change undone".
- Stack in memory only (about 50 entries), dropped on reload and when a design file is opened. Redo stack cleared
  by any new change.
- Applying an entry: restore the four objects, write them through `store.set`, `renderAll()`. The 3D view rebuilds
  through `v3sync` as for any change; the camera stays (decision 1).
- Message: `toast()` (l. 1928) only takes text and `.toast` has `pointer-events: none` (l. 412). It needs a variant
  with an "Undo" button, shown about 6 s, `role="status"`.
- Keys: Ctrl/Cmd + Z undoes, Ctrl/Cmd + Y and Ctrl/Cmd + Shift + Z redo. Not while the focus is in an `input`,
  `select` or `textarea` (the browser's own undo must keep working in the stack's name and the search fields).
- Gestures that get a named message: painting a part type or "Paint all" (`paintRole`, l. 2148), a click with the
  brush (`v3paint`, l. 4865), a "Start from" preset (`applyColorPreset`, l. 2122), removing a filament, a footprint
  change (`setFootprint`, l. 2278, say how many levels changed), a type or height change that drops settings,
  removing a level or a stack, clearing a divider plan, clearing the loose parts.
- With undo in place, remove the `confirm()` in front of "USSA render" (l. 2203): the three presets behave the same,
  apply then "Undo".
- Print: "Reset all progress" keeps press-and-hold and gets the same "Undo" (`printed`, `plateState`).
- Mockup: `6-details.png`, column 4.

Done when: each gesture above can be undone and redone with the button and the keys; undoing a removed stack brings
back its levels, colours and selection; a reload starts with an empty undo stack; `validate.js` and `check.py` pass.

### Session 2 · Fixes that need no mockup

Each is a few lines. Findings in brackets.

- "Spread units" becomes "Spread levels" (l. 4892) [A6].
- Paint's scope reads "Whole stack" / "This module only" (l. 4901), the words the filament picker already uses [C2].
- Stack settings: the alerts (`.ialerts`, l. 3142) move to the top of the panel, each with a "Show level N" link
  when it names a level (`stackAlerts` gives `l`) [B1].
- A new empty stack opens on Stack settings, like a template: `newStack` sets `dsel = { l: null }` (l. 2318) [B6].
- Print: remove the `clearPlates` button for stacks (l. 3564-3574, 3646-3655). See "Open points" for
  "Clear loose parts" [D7].
- Print: the top line's grams leave out the parts left out of the plates (`gramsStr(s.g)`, l. 3585), and "N parts
  no longer fit" counts pieces, not lines (`skipped`, l. 3513) [D8].
- Hardware: a click anywhere on a row ticks it, the store link excepted (`.hwrow`, l. 5580-5586) [E1].
- Hardware: the panel's title is the line count ("12 lines"), not the store's name (l. 5599) [E4].
- Hardware's tab counter follows Hardware's own rail (`hwSkip`), not Print's: `renderTabs` reads
  `computeBuild(true)` (l. 5799-5804). Checked: leaving a stack out in Print moved "Hardware (11)" to (1); leaving it
  out in Hardware left (11) over a 2-line list [E5].
- Until session 3 replaces them: `title` on the level header's up, down and duplicate buttons (l. 2650) [A4].

### Session 3 · The 3D view: hover, right-click, one-line hint

Needs session 1 for the plain-click "Remove level".

- **Hover with the Select tool**: the level under the pointer lights up and a label names it, "Level 3 · M5 1F
  drawer" over "Click to set it up · right-click for actions". Today only Paint highlights (`setHot`, l. 4839-4848).
  The label is DOM over the canvas, placed from the level's projected box.
- **Right-click on a level** (button 2, released less than 5 px from where it was pressed, as the left click
  already tests at l. 4821-4823; a right-drag keeps panning): selects the level, then opens a menu at the pointer:
  - header: "Level 3 of 4", "M5 · 1F drawer";
  - Open drawer / Close drawer (Open case / Close case on a case; hint "double-click" on the right);
  - Add a level above, Add a level below (a copy of this level, as `levelOp('dup')` makes, l. 2333; below = insert
    at the same index);
  - Move up, Move down (disabled at the ends);
  - Remove level (plain click, then the undo message).
  In a module holding several drawers, "Open drawer" acts on the drawer under the pointer (`moverAt`).
- **Right-click on the background, the roof or the base**: "Whole stack", the stack's name; Fit the stack in the
  view (`v.aim`); Add a level on top; Stack settings.
- The menu is a `role="menu"` list: arrow keys, Enter, Esc; it closes on a click outside, on a scroll and when the
  view redraws. Suppress the browser's own menu on the canvas only.
- **Level panel header** (`.ihead`, l. 2649-2651): "Level 2 of 4", then three buttons: level below, level above
  (they move the selection, so a level can be reached without the mouse), and "⋯" (`aria-haspopup="menu"`), which
  opens the level menu under itself. The four icon buttons (up, down, duplicate, remove) go.
- **Hint bar**: one line, "Click a level to set it up · right-click for its actions · double-click opens a drawer"
  (l. 4905-4906). The first-visit tip stays. Drag, scroll and right-drag move behind a "?" button in the toolbar.
- **Toolbar**: Select | Paint, then "Spread levels", "Hide roof", a "Bolts" control with two swatches (raw steel,
  zinc or stainless: `aria-pressed` on the one in use, same setting as Hardware's "Bolt finish") instead of the
  cycling button (l. 4894), then "?". No Fit button there (decision 3).
- "Add a level on top" keeps its place and gets `title="Adds a level like the top one"`.
- Double-click and Ctrl / Shift + click keep opening drawers and cases.
- Mockups: `1-design-level.png`, `2-right-click-level.png`, `3-right-click-background.png`.

Done when: every level action can be reached by right-click, by "⋯" and by keyboard; no gesture reframes the camera
except "Fit the stack in the view"; a right-drag still pans.

### Session 4 · Design's panels

- **Foldable sections** in the level panel and in Stack settings. A section's header shows its name and a summary
  of what is set ("Drawer · 1F", "Empty · key lock · geared rails", "nothing on the back", "18 parts · ≈ 570 g";
  for the stack "M5 · table roof", "base · wheels · foot bar", "trolley handle"). Level: Module and Inside open,
  the two others folded. Stack: Size and roof open. `inspSave` / `inspRestore` (l. 2573-2582) already keep
  `details` open or closed across redraws: build the sections so they are covered. Measured today at 1440 × 900:
  792 px visible for 1131 px (level), 1312 px (stack), 1629 px (Colors) [A7].
- The level's last section is named **"Back of this module"** (it is "Back of the stack" in both panels today).
- **Footprint in Stack settings**: Width and Depth as segmented buttons, first in "Size and roof", with the note
  "For every level. Sizes too big for the <printer> aren't offered." Remove the Footprint button, the strip and
  `fpStrip` (l. 2227, 2544-2548, 2561-2563, 3128, 3146) [A8, B2].
- **"Stack settings" opens and does not toggle**: a second click no longer jumps to the top level (l. 2560).
- **Rename at the centre**: a pencil button next to the stack's big title turns it into the name field; the panel
  shows the name as plain text (`.tname`, l. 3125, 3145) [B3].
- **Options that depend on another stay visible**, greyed, with the reason in the label's hint: Wheels and Casters
  "needs a base", Foot bar "needs wheels", Handle lock "needs the trolley handle", Carry handle "needs the grid
  roof" (l. 3130-3138). Sizes the printer can't make stay hidden: that rule is unchanged [B4].
- **Several drawers in one module**: "Drawer to set up" becomes tabs on a frame that holds Inside, the baseplate and
  divider settings, Lock, Geared rails and, at its foot, "Same settings in every drawer". Under the frame: "In the
  frame: this drawer only. Outside it: the whole module." The note at the bottom of the panel goes (l. 2666) [X4].
- The stack's warning dot sits on the stack's letter badge in the rail (it overlaps the name today).
- Mockups: `1-design-level.png`, `4-design-stack.png`, `6-details.png` columns 1 and 2.

### Session 5 · Paint

Needs session 1.

- **One rule**: the Paint tool shows Colors. Clicking a stack in the rail or "Stack settings" while painting goes
  back to Select. Remove `inspPaint` and the "Paint is on in the view. Show the colors" strip (l. 2147, 2560,
  2587-2590) [C1].
- **Brush bar** under the stack: "Brush", one swatch button per filament (name in `title` and `aria-label`; the
  brush in use shows its name), a "+" that adds a filament; then "A click paints" and the scope, "Whole stack" /
  "This module only" [C3].
- **The catalogue opens in the right panel**, in place of Colors, with a "‹ Colors" return, the search, the line
  filters, the swatches and "Add it and paint with it". No more block under the view (`#dCat`, `fpAdding`,
  l. 2206, 2550) [C4].
- **Colors panel**: "Start from", then the part types in foldable groups (Outside open; each header shows the
  group's swatches and count), "Paint these 5 <brush>" instead of "Paint all", "Modules with their own color",
  then "Your filaments" folded (use, remove) [C5].
- The Paint button carries the stack's filament swatches, so the tool announces where colours are set [C7].
- Each stroke and each preset shows the undo message (session 1) [C5, C6].
- Mockups: `5-design-paint.png`, `6-details.png` column 3.

### Session 6 · Print

- **Right column**: the selected plate first, "Mark as printed" right under its title, then its tags, layout and
  part list; plate options below, one folded line per setting with its value ("Parts with supports · plates of
  their own"), which opens on its segmented buttons; then "How plates are laid out" and "Reset all progress". Today
  "Mark as printed" sits 1335 px down a 876 px column [D1].
- **Filter on one line**: All, one pill per filament, Printed, each with its plate count; the weight and "N left"
  stay in each group's header (l. 3525-3538) [D2].
- **The selection bar shows only when a plate is ticked.** The plate card gets `title` on both targets ("Show this
  plate", "Tick it for the download") [D3, D4].
- **Export**: the two buttons side by side, "STL folders (.zip)" with "for any other slicer" under it [D5].
- **Rail**: each stack says its state in words, "In the plates" / "Left out" (same in Hardware: "In the list" /
  "Left out") [D6].
- Mockup: `7-print.png`.

### Session 7 · Hardware

- **Short names**: the finish is said once, in the list's header ("Every bolt and rod: zinc-plated or stainless"),
  not on each line (`hwItem`, l. 1813). Copy and CSV keep the full name [E2].
- **The link says what it opens**: "Product page" or "Search" (it is in `title` only today, l. 5586), and the
  store is said once in the header ("Links open Amazon.fr") [E3].
- Group headers say "1 of 3 bought". "In this list" becomes "Jump to", plain links with their count (l. 5595) [E6].
- Mockup: `8-hardware.png`.

### Session 8 · Header, file, tabs

- **"File" menu** in the header, on every step: the file's name, the save state ("Kept in this browser", and how
  the file stands against it), Save, Save as…, Open…. Remove the "Design file" group from Design's rail
  (l. 2484-2485) [A9].
- **Loose parts** in the rail is an entry like the stacks (solid border, its count on the right), not a dashed
  box (`.dloose`, l. 488) [A9].
- **Tab counters**: none on Design; Print in %; Hardware "11 to buy"; Assemble in % (`renderTabs`, l. 5786-5810)
  [A10].
- **Credit line** moves to the footer, so the header is one row at 1440 px (l. 78, 833) [A10].
- Mockup: the header of every screen, `6-details.png` column 5.

## Open points: decided with the user (2026-11-14)

They came from the audit but were on no mockup. Dols answered them on 2026-11-14.

- **"Clear loose parts" in Print's plate options** (the same button as "Remove <stack>", l. 3564): **removed too**.
  Loose parts keep their "Clear" in Design. Done in session 2 with D7: Print's plate options have no clear button.
- **The folder dialog on every visit** [X1]: "Later: plan without the files" is kept for the visit only
  (`sessionStorage`, l. 1998-2001). **Kept as it is**: almost nobody will use the planner without the files. No change.
- **A new case shows Floor = "Dividers" with 0 dividers** [X3] (`caseFloor`, l. 2736): **yes, a new case starts on
  "Empty"**. For session 4 (Design's panels).
- **Print's top line after a stack is left out**: "15% printed · 28 of 28 plates left". **The print percentage
  counts only the stacks picked in Print's rail**, and the figures keep their order (percentage, then parts, plates,
  grams). Checked in session 2: it already did (`computeBuild(true)` holds only the picked stacks); since session 2
  the parts and grams also leave out what no longer fits the printer (`printProgress`, D8). What made the line look
  wrong: progress is kept per part file, not per stack (`printed`, keyed by `pkey`), so a part printed while every
  stack was picked counts for any picked stack that uses that file, and the plates of the selection are planned for
  what is still missing. Measured on "Workbench stack" + "Rolling tool cart": 22 of 184 parts printed with both
  picked (6 plates); the Workbench alone then reads 16 of 75 parts and "10 of 10 plates left", the cart alone 15 of
  109 (16 + 15 > 22: their shared M5 files count for both). Keeping progress per stack would change what `printed`
  stores; asked to Dols on 2026-11-14, not done in session 2.

## Rules of `ux-redesign.md` this brief changes

- "1 · Design": no "Footprint" button nor strip; level actions are in the right-click menu and behind "⋯", not in
  the panel's header; the hint is one line.
- "One look for each kind of thing", removing: "Remove level" in the menu is a plain click with undo; the rest
  keeps press-and-hold.
- "One look for each kind of thing", rails: Print's and Hardware's rails write the state on each stack.
- "The 3D view has no Front / ¾ / Side buttons": still true. Add: the camera never reframes by itself; "Fit the
  stack in the view" is on the background's right-click.
- `CLAUDE.md`: "Where the work stands", and the entries on the bolt finish button, "Design file", `inspPaint`,
  `fpStrip`.

## Findings (for reference)

Majeur = the user searches or gets it wrong; Moyen = hesitates; Mineur = consistency.

| Id | Finding | Where |
|---|---|---|
| A1 | Nothing says a level is picked in the view; no hover with Select; not reachable by keyboard | l. 4839-4848 |
| A2 | A permanent two-line manual instead of buttons; no button opens a drawer | l. 4905-4906 |
| A3 | "Add a level on top" is the only named way to add | l. 2333-2335 |
| A4 | Four icons without tooltips, on the settings side | l. 2650 |
| A5 | The stack leaves the frame and nothing reframes (kept on purpose; "Fit" on request) | l. 5211 |
| A6 | Three look-alike toolbar buttons, two kinds; "units" used only there | l. 4892-4894 |
| A7 | A third of a level's settings is below the screen | measured |
| A8 | Two buttons for the stack's settings; "Stack settings" toggles | l. 2560-2561 |
| A9 | Loose parts looks disabled; the file lives in Design's rail | l. 488, 2484 |
| A10 | Four tabs, three units of count; the credit line takes 30 px | l. 5786-5810, 78 |
| B1 | The stack's alerts are 1183 px down a 1312 px panel | l. 3142 |
| B2 | "Change…" opens a strip at the other end of the screen | l. 3146 |
| B3 | Renaming is a field that doesn't look like one | l. 540 |
| B4 | Options that don't exist until their parent is on | l. 3130-3138 |
| B5 | Press-and-hold is learnt after a failed click; no undo anywhere | l. 2511 |
| B6 | An empty stack opens on level 1, a template on the stack | l. 2318, 2325 |
| C1 | The tool drives the right panel, except when it doesn't | l. 2587-2590 |
| C2 | "Same part everywhere" paints this stack only | l. 4979-4983, 4901 |
| C3 | One gesture, three areas | l. 2175, 4899-4901 |
| C4 | "Add a filament" opens the catalogue off screen | l. 2206, 2550 |
| C5 | 1629 px of panel; painting can't be taken back | l. 2148-2154 |
| C6 | Two presets out of three overwrite without warning | l. 2202-2204 |
| C7 | Nothing announces where colours are | l. 515 |
| D1 | The most frequent action is the furthest | measured |
| D2 | The same figures twice (chips, group headers) | l. 3525-3538 |
| D3 | Two selections on one card | l. 3521-3523 |
| D4 | An explanation that stays on screen | l. 3543 |
| D5 | "STL folders (.zip)": for whom? | l. 3587 |
| D6 | The same rail, another rule | `.dstack`, `.pchip` |
| D7 | A stack can be removed from the plate options | l. 3646-3654 |
| D8 | Figures that contradict each other | l. 3585, 3513 |
| E1 | Only the box ticks | l. 5581 |
| E2 | The finish repeated on every line | l. 1813 |
| E3 | A button named after the store | l. 5586 |
| E4 | The panel's title is a setting's value | l. 5599 |
| E5 | The tab counter follows Print's rail | l. 5799-5804 |
| E6 | Scroll links dressed as stack cards | l. 369, 5595 |
| X1 | The folder dialog comes back on every visit | l. 1998-2001 |
| X2 | No undo in the whole page | n/a |
| X3 | A new case: Floor = "Dividers" with none | l. 2736 |
| X4 | The per-drawer note is at the very bottom of the panel | l. 2666 |

## What the audit did not cover

- It ran without a Vault folder: the 3D view showed boxes. Loading real parts, their progress and what the hidden
  side column says about them were not looked at.
- Assemble, the first-launch screen and the dark theme were not audited. The dark theme should follow from the
  existing tokens.
- Mockups are static and the stack is a flat drawing: it stands in for the three.js view, which stays as it is.
