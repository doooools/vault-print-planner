// VAULT part rules: turn one configured unit (or a tower's base) into a list of STL files + quantities.
// Sources: 01_Instructions Manual, 02_Drawer Assembly, 04_Modifications, 05_Mounting (PDFs in the download),
// plus USSA's own component data (2 springs, 2 geared rails, 2+2 runners per drawer level; 2 hinges per case).
// Anything not stated in those sources is marked `inferred` with the reason, so the page can flag it.
(function (root) {
  const FAM_DIR = { S: '01. S Families', M: '02. M Families', L: '03. L Families', XL: '04. XL Families' };
  const DRAWER_FAM_DIR = { S: '01. S Families', M: '02. M Families', L: '03. L Families', L2: '04. L² Families', XL: '05. XL Families', XL2: '06. XL² Families' };
  const D = '01. DRAWERS/', SU = '02. SUSTAINERS/', MO = '03. MODIFICATIONS/', U = D + '07. Universal/', SUU = SU + '05. Universal/';

  const norm = p => p.toLowerCase().replace(/['’\s]/g, '');

  function makeResolver(files) {
    const idx = new Map(files.map(f => [norm(f.path), f]));
    return p => idx.get(norm(p)) || null;
  }

  // Which heights / depths exist per width (from the folder structure)
  const HEIGHTS = { drawer: { S: [1, 2, 4], M: [1, 2, 4], L: [1, 2, 4], L2: [1, 2, 4], XL: [1], XL2: [1] },
                    case: { S: [1, 2, 4], M: [1, 2, 4], L: [1, 2, 4], XL: [1] } };
  const DEPTHS = [3, 4, 5, 6, 7];

  // Exterior W x D x H in mm (USSA published dims; depth grows 42 mm per Gridfinity unit)
  const WIDTH_MM = { S: 164.8, M: 254, L: 329.6, L2: 329.6, XL: 418.8, XL2: 418.8 };
  function exterior(type, w, d, h) {
    const depth = Math.round((156.1 + (d - 3) * 42) * 10) / 10;
    // Height each unit adds to a stack. A 1F case is 34 mm shorter than a 2F one (USSA's Kickstarter size chart: 61 vs 95;
    // the case body STLs: 50.8 vs 84.8), so 65.5 here, not the 71 USSA's own fit finder uses.
    const height = h === 1 ? (type === 'drawer' ? 51.5 : 65.5) : h === 2 ? 99.5 : 195.5;
    return [WIDTH_MM[w], depth, height];
  }
  // Width family whose base/roof/backbone matches a total width in mm (S+S = L, S+M = XL)
  function familyForWidth(mm) {
    let best = null;
    for (const f of ['S', 'M', 'L', 'XL']) if (Math.abs(WIDTH_MM[f] - mm) < 2) best = f;
    return best;
  }

  // Suggested filament colour, following USSA's renders: light-grey body, charcoal working parts, orange accents
  function colorOf(label, group) {
    if (/tire|tyre/i.test(label)) return 'tpu';
    if (/spring|latch|geared rail|runner stopper|hinge rods/i.test(label)) return 'accent';
    if (/drawer box|back panel|runner slide|key lock|hidden key|top handle|hinge|lock (holder|inner|outer|pin)|backbone|handle lock|module connector|knob|second part|^divider$|depth divider|width divider|seal divider|heavyweight roof handle|^foot$/i.test(label)) return 'inner';
    return 'body';
  }

  // What a part is, for choosing its colour. Each role has one default colour, the one colorOf gives all its parts
  // (validate.js checks), so a build with no colour choices plans exactly as before.
  const ROLES = [
    { id: 'shell', label: 'Module shells and case bodies', def: 'body' },
    { id: 'facade', label: 'Drawer and case fronts', def: 'body' },
    { id: 'box', label: 'Drawer boxes', def: 'inner' },
    { id: 'roof', label: 'Roofs and lids', def: 'body' },
    { id: 'runners', label: 'Runner slides', def: 'inner' },
    { id: 'lock', label: 'Key locks and case locks', def: 'inner' },
    { id: 'hinge', label: 'Hinges', def: 'inner' },
    { id: 'accent', label: 'Latches, springs, rails and stoppers', def: 'accent' },
    { id: 'interior', label: 'Gridfinity baseplates and grid dividers', def: 'body' },
    { id: 'dividers', label: 'Dividers', def: 'inner' },
    { id: 'label', label: 'Labels', def: 'body' },
    { id: 'base', label: 'Base, wheels, handles, mounts', def: 'body' },
    { id: 'fittings', label: 'Backbones, connectors, feet, knobs, handle locks', def: 'inner' },
    { id: 'aids', label: 'Print aids (manual supports, jigs)', def: 'body' },
  ];
  function roleOf(label, group) {
    if (/tire|tyre/i.test(label)) return 'tpu';
    if (/^springs|^latch|geared rail|runner stopper|hinge rods/i.test(label)) return 'accent';
    if (/manual support|jig/i.test(label)) return 'aids';
    if (/label/i.test(label)) return 'label';
    if (/front \(facade\)|^drawer front|^case front|facade cap|key cap/i.test(label)) return 'facade';
    if (/drawer box|back panel/i.test(label)) return 'box';
    if (/runner slide/i.test(label)) return 'runners';
    if (/^hinge/i.test(label)) return 'hinge';
    if (/key lock|hidden key|^lock (holder|inner|outer|pin)/i.test(label)) return 'lock';
    if (/^divider$|depth divider|width divider|seal divider/i.test(label)) return 'dividers';
    if (/gridfinity baseplate|grid divider|divider edge|divider pin/i.test(label)) return 'interior';
    if (/backbone|handle lock|module connector|knob|^foot$|top handle|heavyweight roof handle|second part/i.test(label)) return 'fittings';
    if (group === 'Roof' || group === 'Lid') return 'roof';
    if (/module shell|case body|accessory|runner guide/i.test(label)) return 'shell';
    if (/^base|wheel|bushing|stationary handle|pull-out handle|pegboard|wall mount plate/i.test(label)) return 'base';
    const c = colorOf(label, group);
    return c === 'inner' ? 'fittings' : c === 'accent' ? 'accent' : 'shell';
  }

  // Print strength per part. The design is tuned for the profile default (2 walls, 15% infill), so most parts stay there;
  // more walls on big thin parts only adds shrink stress (warping, tight drawers). Extra walls go where bolts or wear are,
  // and extra walls + infill where the part carries the tower or takes force. Flexing parts must stay default.
  function strengthOf(label) {
    if (/^springs|^latch|geared rail/i.test(label)) return { flex: true };
    if (/^base|^foot|backbone|module connector|stationary handle|pull-out handle|knob|wheel disk|wheel cover|^bushing(?! jig)|^top handle|heavyweight roof handle|wall mount/i.test(label)) return { walls: 4, infill: 25 };
    if (/front \(facade\)|^hinge(?! rods)|^lock (holder|inner|outer)|runner guide|runner slide|^key lock|^hidden key|pegboard|^heavyweight roof \(/i.test(label)) return { walls: 3 };
    return {};
  }

  // Bolt holes in a drawer front, counted in the STLs (Drawer Assembly 6/8 shows the 2 on an S 1F)
  const frontBolts = (w, h) => w === 'S' ? (h === 1 ? 2 : 4) : w === 'XL' ? 4 : (h === 1 ? 4 : 6);
  // The drawers a module shell holds, as their heights top to bottom (Instructions Manual, "50 Size Variants": no 3F,
  // everything divides by 2). Drawer Assembly 4/8 supports more than one box per 2F or 4F module. A 2F next to two 1F
  // in a 4F shell is not drawn anywhere: those layouts are inferred.
  const LAYOUTS = { 1: [[1]], 2: [[2], [1, 1]], 4: [[4], [2, 2], [1, 1, 1, 1], [2, 1, 1], [1, 2, 1], [1, 1, 2]] };
  const MIXED_WHY = 'The manuals show one box per module or boxes of one height; a 2F with two 1F in one 4F module is inferred ("no 3F, everything divides by 2").';
  // A unit's drawers: its `drawers` list when it is one of its shell's layouts, else one drawer of the shell's height.
  // XL and XL² modules are 1F only.
  function drawersOf(c) {
    const lay = (LAYOUTS[c.h] || [[c.h]]).find(l => Array.isArray(c.drawers) && l.join() === c.drawers.join());
    return c.w === 'XL' || c.w === 'XL2' || !lay ? [c.h] : lay;
  }
  const mixedLayout = lay => new Set(lay).size > 1;
  // Every drawer of a unit, top to bottom (left side first on an L² or XL²): its id (side + index, the 3D view's own),
  // the box width it takes and its height. Each drawer of a module holding more than one keeps its own inside
  // (`c.inside[id]`: interior, baseplate cut-outs, grid dividers); a module holding one drawer keeps it in its own fields.
  function drawerIds(c) {
    if (c.type && c.type !== 'drawer') return [];
    const lay = drawersOf(c), one = (side, w) => lay.map((h, i) => ({ id: side + i, side: side || null, i, w, h }));
    return c.w === 'L2' ? [...one('left', 'S'), ...one('right', 'S')] : c.w === 'XL2' ? [...one('left', 'S'), ...one('right', 'M')] : one('', c.w);
  }
  // The fields a drawer's inside is made of: all of them per drawer, or the module's for all
  const INSIDE = ['interior', 'baseplateHandles', 'gridHeight', 'gridSeal', 'gridAcross', 'gridAlong', 'gridPlans', 'gridPieces', 'lock', 'gearedRails'];
  // Whether any drawer of a unit has a hidden lock (the stack then takes the removable key)
  const anyHidden = c => c.type === 'drawer' && (c.inside && drawerIds(c).length > 1 ? drawerIds(c).some(dr => (c.inside[dr.id] || c).lock === 'hidden') : c.lock === 'hidden');
  const SIDE_ID = { left: 'left', right: 'right', 'S side': 'left', 'M side': 'right' };
  // A drawer's settings: the unit's, with its own inside over them when the module holds more than one drawer
  const insideOf = (c, side, i, many) => many && c.inside && c.inside[side + i] ? { ...c, ...c.inside[side + i] } : c;
  // One "drawer insert": the drawers of one width in a module of height h (S, M, L or XL), with the module's runners and
  // latch. `lay` is the drawers' heights, top to bottom (one drawer of height h unless the module holds several). Per
  // module: runner guides, slides and stoppers (a pair per 48 mm level), latch. Per drawer: box and front of its own
  // height, lock, key cap, springs, label, facade caps, geared rails, interior.
  function drawerInsert(add, w, d, h, o, tag, inferred, lay = [h]) {
    const fam = D + DRAWER_FAM_DIR[w] + '/';
    const t = tag ? ' (' + tag + ')' : '';
    const why = inferred || (mixedLayout(lay) ? MIXED_WHY : '');
    const x = why ? { inferred: why } : {};
    const n = lay.length, side = SIDE_ID[tag] || '', many = n > 1 || !!side;
    // Drawers of the same height share their lines: tallest first
    const byH = [...new Set(lay)].sort((p, q) => q - p).map(dh => [dh, lay.filter(v => v === dh).length]);
    if (w === 'XL') {
      if (d >= 6) {
        add('Drawer', 'Drawer box, part 1' + t, fam + `XL${d}/Boxes/XL${d} Box 1F Part 1.stl`, 1, x);
        add('Drawer', 'Drawer box, part 2' + t, fam + `XL${d}/Boxes/XL${d} Box 1F Part 2.stl`, 1, x);
      } else {
        add('Drawer', 'Drawer box' + t, fam + `XL${d}/Boxes/XL${d} Box 1F.stl`, 1, x);
        add('Drawer', 'Box back panel' + t, fam + `XL${d}/Boxes/XL${d} Back Panel.stl`, 1, x);
      }
      add('Drawer', 'Drawer front (facade)' + t, fam + 'XL Facade 1F.stl', 1, { supports: true, ...x });
      add('Runners', 'Runner guide' + t, U + `Runners/XL Runners/x${d} Runner Guide XL.stl`, 2 * h, x);
      add('Runners', 'Runner slide' + t, U + `Runners/XL Runners/x${d} Runner Slide XL.stl`, 2 * h, x);
    } else {
      byH.forEach(([dh, k]) => add('Drawer', 'Drawer box' + (byH.length > 1 ? ` ${dh}F` : '') + t, fam + `${w}${d}/Boxes/${w}${d} Box ${dh}F.stl`, k, x));
      byH.forEach(([dh, k]) => add('Drawer', 'Drawer front (facade)' + (byH.length > 1 ? ` ${dh}F` : '') + t, fam + `Facades/${w}${dh}F (Turn On Supports).stl`, k, { supports: true, ...x }));
      add('Runners', 'Runner guide' + t, U + `Runners/x${d} Runner Guide.stl`, 2 * h, x);
      add('Runners', 'Runner slide' + t, U + `Runners/x${d} Runner Slide.stl`, 2 * h, x);
    }
    // A pair of guides, slides and stoppers on every 48 mm level of the module (h levels), as the assembly has them:
    // one 2F/4F box rides on all of them, and the same module can take a 1F box per level instead
    add('Runners', 'Runner stopper' + t, U + 'Runners/Runner Stopper.stl', 2 * h, x);
    // Geared rails and lock: each drawer's own when the module holds several (insideOf)
    const own = lay.map((dh, i) => insideOf(o, side, i, many));
    const rails = own.filter(oi => oi.gearedRails).length, hidden = own.filter(oi => oi.lock === 'hidden').length;
    if (rails) add('Runners', 'Geared rails (pair)' + t, U + `Geared Rails/${w} Rails.stl`, rails,
      { note: 'Optional in the manual. Adds locking force; use them if you put more than one box in a 2F/4F module. One file holds both racks, top and bottom.', ...x });
    // A hidden lock has no knob on the front: the removable key (part 2) turns it, and one serves the whole stack
    // (buildHiddenKey, added once per stack by the page)
    if (hidden) add('Lock', 'Hidden key' + t, U + 'Hidden Key (Turn On Supports).stl', hidden, { supports: true, ...x });
    if (n - hidden) {
      add('Lock', 'Key lock' + t, U + 'Key (Turn On Supports).stl', n - hidden, { supports: true, ...x });
      add('Lock', 'Key cap' + t, U + 'Key Cap.stl', n - hidden, x);
    }
    add('Lock', 'Springs (pair)' + t, U + 'Springs.stl', n, { note: 'One file holds both springs. Fit them flat side up.', ...x });
    // One latch per latch frame under the module, whatever the drawers in it: S and M have one, in the middle; L and XL
    // two (measured on the modules). Drawer Assembly 8/8 pushes it into the module's underside.
    add('Lock', 'Latch' + t, U + 'Latch.stl', w === 'L' || w === 'XL' ? 2 : 1, x);
    add('Lock', 'Label' + t, U + 'Label.stl', n, { note: 'Add your own text with the slicer’s text tool.', ...x });
    // One cap per counterbore of a front: every bolt hole but the one the label covers (Drawer Assembly 6/8 shows
    // the one cap of an S 1F; the others are counted on the fronts)
    add('Lock', 'Facade cap' + t, U + 'Facade Cap.stl', lay.reduce((a, dh) => a + frontBolts(w, dh) - 1, 0), x);
    // Each drawer's inside, its own when the module holds several (tallest first, as above; buildUnit merges the
    // lines of drawers that take the same files)
    lay.map((dh, i) => [dh, i]).sort((p, q) => q[0] - p[0]).forEach(([dh, i]) => {
      const oi = insideOf(o, side, i, many);
      if (oi.interior === 'gridfinity') {
        const subdir = fam + `${w}${d}/Gridfinity Baseplate/`;
        if (w === 'XL' && d >= 6) {
          add('Interior', 'Gridfinity baseplate, part 1' + t, subdir + `XL${d} Baseplate Part 1.stl`, 1, x);
          add('Interior', 'Gridfinity baseplate, part 2' + t, subdir + `XL${d} Baseplate Part 2.stl`, 1, x);
        } else {
          const v = oi.baseplateHandles && oi.baseplateHandles !== '0' ? `_With ${oi.baseplateHandles} Handle${oi.baseplateHandles === '1' ? '' : 's'}` : '';
          add('Interior', 'Gridfinity baseplate' + (v ? ` (${oi.baseplateHandles}-handle cut-out)` : '') + t, subdir + `${w}${d} Baseplate${v}.stl`, 1,
            { fallback: subdir + `${w}${d} Baseplate.stl`, ...x });
        }
      }
      if (oi.interior === 'grid') gridDividers(add, w, d, dh, oi, t, 1);
    });
  }

  // Grid dividers (Grid Dividers/01. INSTRUCTIONS; tools/placements/measure_grid.py): a box's floor is a grid of peg
  // holes 10.5 mm apart and a divider's file number is how many holes it covers (5 ... 32). A full-span divider is the
  // file named after the box (width 10-S, 18-M, 26-L, 32-XL; depth 4 x depth - 2: x3 = 10 ... x7 = 26) with a straight
  // edge piece at each wall. A partial one, stopping at another divider, ends there with a rounded edge piece (its arrow
  // rides over that divider's foot); at a wall it ends with a straight piece where the gap is one the piece bridges
  // ("N - 1" + piece) or alone ("N"); past 32 holes it is two files end to end.
  // The page lays out each box's plan and passes the pieces in `o.gridPieces[<w><d>]` ({n: {N: qty}, straight,
  // rounded}); without one (no measured grid), `gridAcross` full-width dividers and `gridAlong` front-to-back ones,
  // the latter cut in two by each full-width one.
  const GRID_DIR = {
    20: U + 'Grid Dividers/20MM TALL/',
    1: U + 'Grid Dividers/34.5MM TALL (full height of 1F drawers)/',
    2: U + 'Grid Dividers/82.5MM TALL (full height of 2F drawers)/',
  };
  const GRID_NAMES = { 10: '10-S, x3', 14: '14, x4', 18: '18-M, x5', 22: '22, x6', 26: '26-L, x7', 32: '32-XL' };
  const GRID_FULL_W = { S: 10, M: 18, L: 26, XL: 32 };
  const gridFull = (w, d) => ({ x: GRID_FULL_W[w], z: 4 * d - 2 });
  // The files of a drawer of height h: the folder (20 mm, or as tall as a 1F / 2F drawer), the edge pieces' suffix
  const gridTall = (h, o) => (o.gridHeight === 'full' ? (h === 1 ? 1 : 2) : 20);
  const gridFile = (h, o, n) => GRID_DIR[gridTall(h, o)] + (GRID_NAMES[n] || String(n)) + '.stl';
  const gridEdgeFile = (h, o, kind) => { const t = gridTall(h, o); return GRID_DIR[t] + `${kind === 'rounded' ? 'Rounded' : 'Straight'} Edge Piece ${t === 20 ? '20MM' : t + 'F'}.stl`; };
  const gridPinFile = o => U + `Grid Dividers/grid divider pin_${o.gridPin === 'loose' ? 'loose' : 'tight'}.stl`;
  function gridDividers(add, w, d, h, o, t, k = 1) {
    const p = o.gridPieces && o.gridPieces[w + d];
    const full = gridFull(w, d), across = +o.gridAcross || 0, along = +o.gridAlong || 0;
    const pc = p || { n: { [full.x]: across, ...(along ? { [full.z]: along * (across + 1) } : {}) }, straight: 2 * across + along * 2, rounded: along * 2 * across };
    let total = 0;
    Object.entries(pc.n).map(([n, q]) => [+n, q]).filter(([, q]) => q > 0).sort((a, b) => b[0] - a[0]).forEach(([n, q]) => {
      const what = n === full.x && n === full.z ? 'full width or depth' : n === full.x ? 'full width' : n === full.z ? 'full depth' : n + ' holes';
      add('Interior', `Grid divider ${(GRID_NAMES[n] || String(n)).split(',')[0]} (${what})` + t, gridFile(h, o, n), q * k);
      total += q;
    });
    if (!total) return;
    if (pc.straight) add('Interior', 'Divider edge piece, straight (at a wall)' + t, gridEdgeFile(h, o, 'straight'), pc.straight * k);
    if (pc.rounded) add('Interior', 'Divider edge piece, rounded (where a divider meets another)' + t, gridEdgeFile(h, o, 'rounded'), pc.rounded * k);
    add('Interior', 'Divider pin' + t, gridPinFile(o), 2 * total * k,
      { inferred: 'The instructions don’t give a pin count. Two per divider is read from the drawings.' });
  }

  const ROOFS = [
    { id: 'grid', label: 'Grid roof (Gridfinity top)', widths: ['S', 'M', 'L', 'L2', 'XL', 'XL2'] },
    { id: 'table', label: 'Table roof (flat top)', widths: ['S', 'M', 'L', 'L2', 'XL', 'XL2'] },
    { id: 'bowl', label: 'Bowl roof (tray top)', widths: ['S', 'M', 'L', 'L2', 'XL', 'XL2'] },
    { id: 'undertable', label: 'Under-table mount roof', widths: ['S', 'M', 'L', 'L2', 'XL', 'XL2'] },
    { id: 'heavy', label: 'Heavyweight roof (carry handle)', widths: ['L', 'L2', 'XL', 'XL2'] },
    { id: 'heavycut', label: 'Heavyweight roof, cut version', widths: ['XL', 'XL2'] },
  ];
  const ROOF_FILE = { grid: 'Grid Roof', table: 'Table Roof', bowl: 'Bowl Roof', undertable: 'Under Table Mount Roof', heavy: 'Heawyweight Roof', heavycut: 'Heavyweight Roof Cut' };

  // Roof for the top of a drawer stack, sized to a width family (S/M/L/XL) and depth
  // aids: USSA's manual support, a prop as tall as the roof printed on its edge, printed standing against its end (the
  // Print step's "Manual supports" option; the plate planner packs each with its roof)
  function roof(add, rw, d, kind, topHandle, aids) {
    if (!kind || kind === 'none') return;
    add('Roof', ROOFS.find(r => r.id === kind).label, D + DRAWER_FAM_DIR[rw] + '/' + `${rw}${d}/Roofs/${rw}${d} ${ROOF_FILE[kind]}.stl`, 1);
    if (aids) add('Roof', 'Manual support', U + `Manual Supports/x${d}.stl`, 1,
      { note: 'Print aid: stands against the end of the roof while both print. Not part of the finished unit.', aid: true });
    if (kind === 'grid' && topHandle) add('Roof', 'Top handle', U + 'Top Handle (Turn On Supports).stl', 1, { supports: true });
    if (kind === 'heavy' || kind === 'heavycut') {
      add('Roof', 'Heavyweight roof handle', U + 'Heawyweight Roof Handle.stl', 1);
      // The bar drops into a pocket at each end, through an entry groove that the insert then closes: two per roof
      add('Roof', 'Heavyweight roof insert', U + 'Heawyweight Roof Insert.stl', 2,
        { inferred: 'The manual doesn’t count them. The roof has two handle pockets, each with an entry groove that one insert closes, so two are listed.' });
    }
  }

  // The L² and XL² modules take one set of accessories (1st + 2nd) per F, in the module's depth
  function l2Accessories(add, name, d, h) {
    add('Module', `${name} accessory, 1st`, U + `L² Accessories/x${d} Accessory 1st.stl`, h, { note: 'One set (1st + 2nd) per F.' });
    add('Module', `${name} accessory, 2nd`, U + `L² Accessories/x${d} Accessory 2nd.stl`, h, { note: 'One set (1st + 2nd) per F.' });
  }

  // Module shells print with Bambu Studio's supports set the way Dols prints them (2026-11-13): the page's SUPPORT_SETS
  // has the settings. A named set, not `true`: these light supports don't move the shells onto plates of their own.
  const SHELL = { supports: 'shell' };

  function drawer(add, c) {
    const { w, d, h } = c;
    const fam = D + DRAWER_FAM_DIR[w] + '/';
    if (w === 'L2') {
      const why = 'The manual doesn’t list L² contents. L = S + S, so this assumes two S drawers side by side.';
      add('Module', 'Module shell', fam + `L${d}²/L${d}² Module ${h}F.stl`, 1, SHELL);
      // Both sides of an L² take the same drawers
      drawerInsert(add, 'S', d, h, c, 'left', why, drawersOf(c));
      drawerInsert(add, 'S', d, h, c, 'right', why, drawersOf(c));
      l2Accessories(add, 'L²', d, h);
    } else if (w === 'XL2') {
      const why = 'The manual doesn’t list XL² contents. XL = S + M, so this assumes an S and an M drawer side by side.';
      add('Module', 'Module shell', fam + `XL${d}²/XL${d}² Module 1F.stl`, 1, SHELL);
      drawerInsert(add, 'S', d, 1, c, 'S side', why);
      drawerInsert(add, 'M', d, 1, c, 'M side', why);
      l2Accessories(add, 'XL²', d, 1);
    } else {
      add('Module', 'Module shell', fam + `${w}${d}/Modules/${w}${d} Module ${h}F.stl`, 1, SHELL);
      drawerInsert(add, w, d, h, c, '', '', drawersOf(c));
    }
    if (c.roof && c.roof !== 'none') roof(add, w === 'L2' ? 'L' : w === 'XL2' ? 'XL' : w, d, c.roof, c.topHandle, c.manualSupports);
  }

  function sustainer(add, c, resolve) {
    const { w, d, h } = c;
    const fam = SU + FAM_DIR[w] + '/';
    const big = w === 'L' || w === 'XL';
    const inner = big ? ' ' + { flat: 'Flat', dividers: 'Dividers', sealed: 'Sealed' }[c.caseInterior || 'flat'] : '';
    add('Module', 'Case body' + (big ? ` (${(c.caseInterior || 'flat')})` : ''), fam + `${w}${d}/Modules/${w}${d} ${h}F${inner} Module.stl`, 1);
    add('Module', 'Case front (facade)', w === 'XL' ? fam + 'XL1F Facade.stl' : fam + `Facades/${w}${h}F Facade.stl`, 1);
    // Lid: 6 and 7 deep come whole or split in two with a connector. The page picks whole if it fits the printer.
    const roofDir = fam + `${w}${d}/` + (resolve(fam + `${w}${d}/Roofs/${w}${d} Roof.stl`) || resolve(fam + `${w}${d}/Roofs/${w}${d} Roof Whole.stl`) ? 'Roofs/' : 'Roof/');
    if (d >= 6) {
      add('Lid', 'Lid (one piece)', roofDir + `${w}${d} Roof Whole.stl`, 1, { alt: 'split' });
      add('Lid', 'Lid, part 1', roofDir + `${w}${d} Roof Part 1.stl`, 1, { alt: 'whole' });
      add('Lid', 'Lid, part 2', roofDir + `${w}${d} Roof Part 2.stl`, 1, { alt: 'whole' });
      add('Lid', 'Split-lid connector', roofDir + 'Connector For Split Roof.stl', 1, { alt: 'whole' });
    } else {
      add('Lid', 'Lid', roofDir + `${w}${d} Roof.stl`, 1);
    }
    const sm = !big;
    add('Hinges & locks', 'Hinge', SUU + 'Hinges/' + (sm ? (h === 1 ? 'S-M 1F Hinge.stl' : 'S-M 2-4F Hinge.stl') : (h === 1 ? 'L-XL 1F Hinge.stl' : 'L 2-4F Hinge.stl')), 1,
      { note: 'One file holds the two leaves that bolt to the case body, one per hinge.' });
    // S and M lids take one long hinge top across both leaves (the lid has 4 holes for one); L and XL two short ones
    if (sm) add('Hinges & locks', 'Hinge top', SUU + 'Hinges/' + (w === 'S' ? 'S Hinge Top.stl' : 'M Hinge Top.stl'), 1,
      { note: 'One long top spans both hinges.' });
    else add('Hinges & locks', 'Hinge tops (pair)', SUU + 'Hinges/L-XL Hinge Top.stl', 1, { note: 'This file already contains two hinge tops.' });
    add('Hinges & locks', 'Hinge rods (pair)', SUU + 'Rods/' + (sm ? 'S-M Rods.stl' : 'L-XL Rods.stl'), 1, { note: 'One file holds both rods.' });
    // One lock per notch in the front's top edge: S and M fronts have one, L and XL two (Sustainers Naming shows two on L)
    const locks = big ? 2 : 1;
    add('Hinges & locks', 'Lock holder', SUU + 'Locks/LOCK HOLDER.stl', locks);
    add('Hinges & locks', 'Lock inner part', SUU + 'Locks/LOCK INNER PART.stl', locks);
    add('Hinges & locks', 'Lock outer part', SUU + 'Locks/' + (h === 1 ? 'LOCK OUTER PART 1F.stl' : 'LOCK OUTER PART 2-4F.stl'), locks);
    add('Hinges & locks', 'Lock pin set', SUU + 'Locks/1 SET OF PINS FOR 1 LOCK.stl', locks, { note: 'Four pins per file, one file per lock.' });
    // The case body has a drawer module's underside, latch frames included, and stacks like one
    add('Hinges & locks', 'Latch', U + 'Latch.stl', big ? 2 : 1,
      { inferred: 'The manual doesn’t show a case from below. Its body has the same latch frames as a drawer module (one on S and M, two on L and XL), so it takes the same latches.' });
    // One label per case, in its front's label slot (Sustainers Naming, manual 01 p.12): the short sustainer label on a
    // 1F front, the drawers' label on a 2F or 4F front
    if (h === 1) add('Hinges & locks', 'Case label', SUU + 'Label for Sustainers.stl', 1);
    else add('Hinges & locks', 'Case label', U + 'Label.stl', 1);
    // A Gridfinity baseplate covers the body's floor wall to wall, and with it the 2 mm floor grooves the dividers stand
    // in (their slots run from those grooves up the walls): a case takes one or the other, the baseplate when both are
    // asked. A sealed body's fixed walls split its floor into cells narrower than the baseplate: it takes none.
    const plate = !!c.caseBaseplate && !(big && c.caseInterior === 'sealed');
    if (plate) {
      if (w === 'XL') {
        if (d >= 6) {
          add('Interior', 'Gridfinity baseplate, part 1', SUU + `Baseplates/04. XL/XL${d} Part 1  Gridfinity Baseplate.stl`, 1);
          add('Interior', 'Gridfinity baseplate, part 2', SUU + `Baseplates/04. XL/XL${d} Part 2  Gridfinity Baseplate.stl`, 1);
        } else add('Interior', 'Gridfinity baseplate', SUU + `Baseplates/04. XL/XL${d}  Gridfinity Baseplate.stl`, 1);
      } else add('Interior', 'Gridfinity baseplate', SUU + `Baseplates/0${'SML'.indexOf(w) + 1}. ${w}/${w}${d} Baseplate.stl`, 1);
    }
    // Dividers slide into slots moulded in the body's walls (tools/placements/measure_dividers.py): S and M bodies
    // take plain ones, an L or XL "Dividers" body width and depth ones (an egg crate), a "Sealed" body seal ones
    // in its cells. A flat body has no slot, so dividers chosen for another style are left out.
    const dv = plate ? {} : c.dividers || {}, style = big ? c.caseInterior || 'flat' : 'plain';
    if (style === 'plain') {
      if (dv.plain) add('Interior', 'Divider', SUU + `Dividers/${w} Dividers/${w}${h}F Divider.stl`, dv.plain);
    } else if (w === 'L') {
      if (style === 'dividers' && dv.depth) add('Interior', 'Depth divider (runs front to back)', SUU + `Dividers/L Depth Dividers/L${d}-${h}F Depth Divider.stl`, dv.depth);
      if (style === 'dividers' && dv.width) add('Interior', 'Width divider (runs side to side)', SUU + `Dividers/L Width Dividers/L-${h}F Width Divider.stl`, dv.width);
      if (style === 'sealed' && dv.seal) add('Interior', 'Seal divider', SUU + `Dividers/L Seal Dividers/L-${h}F Seal Divider.stl`, dv.seal);
    } else if (w === 'XL') {
      if (style === 'dividers' && dv.depth) add('Interior', 'Depth divider (runs front to back)', SUU + `Dividers/XL Depth Dividers/XL${d} Depth Divider.stl`, dv.depth);
      if (style === 'dividers' && dv.width) add('Interior', 'Width divider (runs side to side)', SUU + 'Dividers/XL Width Divider.stl', dv.width);
      // seal: the middle cell's count; sealSide: the two side cells' (one row across all three cells before)
      const side = dv.sealSide != null ? dv.sealSide : (dv.seal || 0) * 2;
      if (style === 'sealed' && dv.seal) add('Interior', 'Seal divider, center', SUU + 'Dividers/XL Seal Divider (Center).stl', dv.seal);
      if (style === 'sealed' && side) add('Interior', 'Seal divider, sides', SUU + 'Dividers/XL Seal Divider (Sides).stl', side);
    }
  }

  // Per-unit mounting add-ons
  function mounts(add, c) {
    const { h } = c;
    const w = c.w === 'L2' ? 'L' : c.w === 'XL2' ? 'XL' : c.w;
    if (c.wallMount) {
      add('Wall mount', 'Wall mount plate', MO + `Wall Mounts/${w}${h}F Wall Mount.stl`, 1,
        { note: 'Use full-height plates: a 1F plate on a taller module can’t serve as the drilling template.' });
      // One cleat per trapezoid opening of the plate (Wall Mount Instructions 4-5), counted on the plates: one on 1F and
      // 2F plates, two on 4F ones, twice that across an L or XL plate
      add('Wall mount', 'Wall mount second part (wall cleat)', MO + 'Wall Mounts/Wall Mount Second Part.stl', (h === 4 ? 2 : 1) * (w === 'L' || w === 'XL' ? 2 : 1),
        { note: 'One per opening of the plate, screwed to the wall.' });
    }
    if (c.pegboard && c.pegboard !== 'none' && h <= 2) {
      add('Pegboard', (c.pegboard === 'ikea' ? 'IKEA Skådis' : 'USSA') + ' pegboard attachment',
        MO + `Pegboard Attachment/${c.pegboard === 'ikea' ? 'IKEA Skadis Pegboard' : 'USSA Pegboard'}/${w}${h}F.stl`, 1);
    }
    // Backbones are a column on the back of the whole stack (buildBackbones), not a part of one module
  }

  // The backbone column on the back of a stack (Modifications Assembly 7-15). Each backbone straddles a joint, bolted
  // to the piece below and the one above: the first, a 2F, ties the base to the first module (steps 10-11), the next
  // ones tie the modules to each other (13), 1F ones also do (14). The column runs from the base up to the module under
  // the top one, where the pull-out handle lock goes (17-19), or higher when a pegboard (20) or a chosen backbone sits
  // there. o = { w, base, heights: [F of each level, bottom to top], upTo: highest level index the column covers,
  // universal }. Counted in F: the base as one, 2F backbones, and a 1F one for an odd remainder.
  // Bolts (Modifications Assembly 7-11, measured on the files): through the sealed holes along the backbone's ends (14 mm
  // of backbone), into the 3.6 mm pilot holes in the back of the modules (100 mm deep) and of the base (74 mm). The manual
  // says 60 to 100 mm; 80 is the longest standard length that fits the base too (14 + 74 = 88).
  function buildBackbones(o, resolve) {
    const k = collector(resolve);
    const covered = o.heights.slice(0, Math.max(0, o.upTo + 1)).reduce((a, h) => a + h, 0);
    let f = (o.base ? 1 : 0) + covered;
    const total = (o.base ? 1 : 0) + o.heights.reduce((a, h) => a + h, 0);
    if (f < 2) f = Math.min(2, total); // at least the first 2F backbone, base to first module
    const name = h => MO + `Backbone/${o.universal ? 'Universal ' + h + 'F' : o.w + h + 'F'} Backbone.stl`;
    const x = { note: 'Backbones come sealed: mark the spots on the modules and drill through with a 4 mm bit.',
      inferred: 'The manual draws the column but gives no count: 2F backbones over the base (as 1F) and the modules it covers, a 1F one for an odd remainder.' };
    // XL backbones only come in 1F (there is no XL2F file): the column is made of those
    const only1 = !o.universal && o.w === 'XL';
    const twos = only1 ? 0 : Math.floor(f / 2), ones = only1 ? f : f % 2;
    if (twos) k.add('Backbone', (o.universal ? 'Universal backbone' : 'Backbone') + ' 2F', name(2), twos, x);
    if (ones) k.add('Backbone', (o.universal ? 'Universal backbone' : 'Backbone') + ' 1F', name(1), ones, x);
    return { f: only1 ? ones : 2 * twos + ones, lines: k.lines, missing: k.missing, hardware: twos + ones ? [{ item: 'M4 × 80 mm button-head bolt', qty: 4 * (twos + ones), why: 'Backbones' }] : [] };
  }

  // Tower base and handles: one set per tower, sized by the bottom level's width family and depth
  function stackParts(add, s) {
    const { w, d } = s;
    if (s.base) {
      if (d >= 6) {
        add('Base', 'Base (one piece)', MO + `Base/${w}/${w}${d} Base Whole.stl`, 1, { alt: 'split' });
        add('Base', 'Base, part 1', MO + `Base/${w}/${w}${d} Base Part 1.stl`, 1, { alt: 'whole' });
        add('Base', 'Base, part 2', MO + `Base/${w}/${w}${d} Base Part 2.stl`, 1, { alt: 'whole' });
        add('Base', 'Base connector', MO + 'Base/Base Connector.stl', 1, { alt: 'whole' });
      } else add('Base', 'Base', MO + `Base/${w}/${w}${d} Base.stl`, 1);
      if (s.wheels) {
        add('Wheels', 'Wheel disk', MO + 'Wheels/Disk.stl', 2);
        add('Wheels', 'Bushing', MO + 'Wheels/Bushing.stl', 2);
        add('Wheels', 'Wheel cover', MO + 'Wheels/Cover.stl', 2);
        add('Wheels', 'Tire', MO + 'Wheels/Tyre (TPU).stl', 2, { tpu: true, note: 'Print in TPU.' });
        add('Wheels', 'Bushing jig (tool)', MO + 'Wheels/Jig.stl', 1, { aid: true, note: 'Tool for pressing bushings onto the rod. Print once.' });
      }
      // One foot, opposite the wheels (Modifications Assembly 6/15), on the base's two M6 holes at the front. Without
      // wheels the base stands on its own flat underside (one plane over 82-95 % of its footprint; there are no holes
      // for a second foot): no foot.
      if (s.feet && s.wheels) add('Base', 'Foot', MO + `Feet/${w} Feet.stl`, 1, { note: 'One foot opposite the wheels.' });
    }
    if (s.stationaryHandle) add('Handles', 'Stationary handle', MO + `Stationary Handle/${w} Stationary Handle.stl`, 1);
    if (s.pullHandle) {
      add('Handles', 'Pull-out handle', MO + `Pull-out Handle/${w} Pull-out Handle.stl`, 1);
      if (s.handleLock === 'universal' && w !== 'S') {
        // Universal Pull-out Handle Lock (tools/placements/measure_column.py, ulock): one rod's share of the lock, 89 mm
        // wide, so it prints on any bed: one per rod, each with its knob, screwed through its flange into the module's
        // back corner holes as well as clamped on the rod. Not on S: two of them (178 mm) are wider than an S stack
        // (164.8), whose own lock is no wider than its modules
        add('Handles', 'Pull-out handle lock (universal, one per rod)', MO + 'Backbone/Universal Pull-out Handle Lock.stl', 2,
          { note: 'One per M16 rod, its flange out to the stack’s side. Fits any printer, instead of the one-piece lock.' });
        add('Handles', 'Handle lock knob, part 1', MO + 'Backbone/Handle Lock Knob Part 1.stl', 2, { note: 'One per lock.' });
        add('Handles', 'Handle lock knob, part 2', MO + 'Backbone/Handle Lock Knob Part 2.stl', 2, { note: 'One per lock.' });
      } else {
        add('Handles', 'Pull-out handle lock', MO + `Backbone/${w} Pull-out Handle Lock.stl`, 1);
        if (w === 'S') add('Handles', 'Pull-out handle lock, part 2', MO + 'Backbone/S Pull-out Handle Lock Part 2.stl', 1);
        add('Handles', 'Handle lock knob, part 1', MO + 'Backbone/Handle Lock Knob Part 1.stl', 2, { inferred: 'Two knobs, read from the trolley drawings.' });
        add('Handles', 'Handle lock knob, part 2', MO + 'Backbone/Handle Lock Knob Part 2.stl', 2, { inferred: 'Two knobs, read from the trolley drawings.' });
      }
    }
  }

  function unitHardware(c) {
    const hw = [];
    const push = (item, qty, why) => qty && hw.push({ item, qty, why });
    if (c.type === 'drawer') {
      // Front to box: one bolt per hole in the drawer front, counted in the STLs (Drawer Assembly 6/8 shows the 2 on an S 1F).
      // S: 2 at 1F, 4 at 2F/4F. M and L: 4 at 1F, 6 at 2F/4F. XL (1F only): 4. L² is two S drawers, XL² an S and an M (both 1F).
      const front = frontBolts;
      const lay = drawersOf(c), per = w => lay.reduce((a, dh) => a + front(w, dh), 0);
      const bolts = c.w === 'L2' ? 2 * per('S') : c.w === 'XL2' ? front('S', 1) + front('M', 1) : per(c.w);
      push('M4 × 14 mm button-head bolt', bolts, 'Drawer front to box');
    } else {
      // Counted on the holes in the STLs (tools/placements/COVERAGE.md "Hardware"; the manual's p. 17 draws an L 4F,
      // with 7 and 16). Case front: S and M 4 (1F, 2F), 6 (4F); L 5 (1F, 2F), 7 (4F); XL (1F only) 5. Hinge tops and
      // locks: 4 + 4 on S and M (one hinge top with 4 holes, one lock), 8 + 8 on L and XL. Hinges: 8 everywhere.
      const big = c.w === 'L' || c.w === 'XL';
      push('M4 × 14 mm button-head bolt', big ? 16 : 8, 'Case hinge tops and locks');
      push('M4 × 10 mm button-head bolt', 8, 'Case hinges');
      push('M4 × 20 mm button-head bolt', (big ? 5 : 4) + (c.h === 4 ? 2 : 0), 'Case front and body');
    }
    if (c.roof === 'grid' && c.topHandle) push('M6 × 50 mm countersunk bolt', 2, 'Roof top handle');
    if (c.pegboard && c.pegboard !== 'none' && c.h <= 2) push('M4 × 40 mm button-head bolt', 4, 'Pegboard attachment');
    return hw;
  }

  function stackHardware(s) {
    const hw = [];
    const push = (item, qty, why) => qty && hw.push({ item, qty, why });
    if (s.base && s.wheels) {
      push('M16 threaded rod, ' + { S: 248, M: 338, L: 414, XL: 504 }[s.w] + ' mm', 1, 'Wheel axle');
      push('M4 × 25 mm button-head bolt', 12, 'Wheel covers (6 per wheel)');
      push('6205ZZ bearing (25 × 52 × 15 mm)', 2, 'Wheels');
      push('SCSAW shaft collar (16 mm bore)', 2, 'Wheels');
    }
    if (s.base && s.feet && s.wheels) push('M6 × 90 mm button-head bolt', 2, 'Feet');
    if (s.base && !s.wheels && s.casters) push('Caster with M8 bolt', 4, 'Casters (instead of wheels)');
    if (s.stationaryHandle) push('M4 × 60 mm button-head bolt', 8, 'Stationary handle');
    if (s.pullHandle) {
      push('M6 × 30 mm countersunk bolt', 4, 'Pull-out handle');
      push('M6 × 35 mm hex bolt', 2, 'Handle lock');
      if (s.handleLock === 'universal' && s.w !== 'S') push('M4 × 30 mm button-head bolt', 4, 'Universal handle locks, into the module’s back corner holes');
      push('M6 × 8 × 8 heat insert', 2, 'Handle lock knobs');
      push('M16 rod, cut to stack height', 2, 'Pull-out handle');
    }
    return hw;
  }

  function collector(resolve) {
    const lines = [], missing = [];
    const add = (group, label, path, qty, extra = {}) => {
      const f = resolve(path) || (extra.fallback && resolve(extra.fallback));
      if (!f) { missing.push(path); return; }
      const l = { group, label, file: f, qty, color: colorOf(label, group), role: roleOf(label, group), ...strengthOf(label), ...extra };
      // Supports follow USSA only: the files they name "(Turn On Supports)" plus the XL drawer front (see drawerInsert).
      // Bambu Studio's overhang warnings (src/bambu-support-audit.tsv) no longer turn supports on: USSA builds break-away
      // supports into parts, Bambu flags those as floating, and its supports then fill spots like the drawer box's
      // geared-rail channel (upstream cdcce17, 2026-11-10).
      lines.push(l);
    };
    return { lines, missing, add };
  }

  // One unit, as configured. Includes its roof when c.roof is set (the page clears it for units that aren't on top).
  function buildUnit(c, resolve) {
    const k = collector(resolve);
    if (c.type === 'drawer') drawer(k.add, c); else sustainer(k.add, c, resolve);
    // A roof latches onto a case's lid as onto a module: the lid's top has the module top's latch frames (manual p. 17)
    if (c.type !== 'drawer' && c.roof && c.roof !== 'none') roof(k.add, c.w, c.d, c.roof, c.topHandle, c.manualSupports);
    mounts(k.add, c);
    return { lines: mergeSame(k.lines), missing: k.missing, hardware: unitHardware(c) };
  }
  // One line per file in a unit: the two bays of an L² or XL² list their shared parts (keys, springs, caps, stoppers…)
  // once, without the bay's tag, so Design and Print list the same totals
  function mergeSame(lines) {
    const out = [], by = new Map();
    for (const l of lines) {
      const key = l.file.path + '|' + (l.alt || '');
      const m = by.get(key);
      if (!m) { const c = { ...l }; by.set(key, c); out.push(c); continue; }
      m.qty += l.qty;
      if (m.label !== l.label) m.label = m.label.replace(/ \((left|right|S side|M side)\)$/, '');
    }
    return out;
  }
  // Module connectors (tools/placements/measure_connectors.py): a bar 12 mm thick screwed over a joint between two drawer
  // modules at a back corner, into the corner holes every drawer module has 8.15 mm in from each side, a level's bottom and
  // top. A 1F one ties a module to the one on it (2 holes), a 2F one the modules on both sides of a 1F module (4 holes).
  // The page works out where they go (connectorPlan in src/template.html). o = { ones, twos }
  function buildConnectors(o, resolve) {
    const k = collector(resolve);
    const x = { note: 'At the back corners, flush with the sides, over the joint between two drawer modules.' };
    if (o.twos) k.add('Connectors', 'Module connector 2F', MO + 'Backbone/Connector for Modules 2F.stl', o.twos, { ...x, note: x.note + ' A 2F one spans a 1F module and the joints above and below it.' });
    if (o.ones) k.add('Connectors', 'Module connector 1F', MO + 'Backbone/Connector for Modules 1F.stl', o.ones, x);
    const bolts = 2 * (o.ones || 0) + 4 * (o.twos || 0);
    return { lines: k.lines, missing: k.missing, hardware: bolts ? [{ item: 'M4 × 25 mm button-head bolt', qty: bolts, why: 'Module connectors, into the modules’ back corner holes' }] : [] };
  }
  // A tower's base, wheels, feet and handles. s = { w: 'S'|'M'|'L'|'XL', d, base, wheels, feet, casters, stationaryHandle, pullHandle,
  // handleLock: 'family' (one piece, as wide as the stack) | 'universal' (one small lock per rod) }
  function buildStack(s, resolve) {
    const k = collector(resolve);
    stackParts(k.add, s);
    return { lines: k.lines, missing: k.missing, hardware: stackHardware(s) };
  }
  // Roof on its own, for a top level made of two units side by side (sized to their combined width)
  function buildRoof(rw, d, kind, topHandle, resolve, aids) {
    const k = collector(resolve);
    roof(k.add, rw, d, kind, topHandle, aids);
    return { lines: k.lines, missing: k.missing, hardware: kind === 'grid' && topHandle ? [{ item: 'M6 × 50 mm countersunk bolt', qty: 2, why: 'Roof top handle' }] : [] };
  }

  // The removable key of the hidden locks: one per stack that has any, with its key cap (its grip has the size of the
  // Key's, and the manual caps the same grip on the handle lock knob, Modifications Assembly 13/15)
  function buildHiddenKey(resolve) {
    const k = collector(resolve);
    k.add('Lock', 'Hidden key, part 2', U + 'Hidden Key Part 2 (Turn on Supports).stl', 1, { supports: true, note: 'One per stack: it turns every hidden lock of the stack.' });
    k.add('Lock', 'Key cap', U + 'Key Cap.stl', 1, { note: 'Goes on the removable key’s grip.' });
    return { lines: k.lines, missing: k.missing, hardware: [] };
  }

  const api = { buildUnit, buildStack, buildRoof, buildHiddenKey, buildBackbones, buildConnectors, makeResolver, exterior, familyForWidth, drawersOf, drawerIds, INSIDE, anyHidden, HEIGHTS, DEPTHS, ROOFS, ROLES, WIDTH_MM, LAYOUTS, norm, gridFull, gridFile, gridEdgeFile, gridPinFile };
  if (typeof module !== 'undefined') module.exports = api; else root.VaultRules = api;
})(this);
