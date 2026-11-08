// VAULT part rules: turn one configured unit (or a tower's base) into a list of STL files + quantities.
// Sources: 01_Instructions Manual, 02_Drawer Assembly, 04_Modifications, 05_Mounting (PDFs in the download),
// plus USSA's own component data (2 springs, 2 geared rails, 2+2 runners per drawer; 2 locks + 2 hinges per case).
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
    const height = h === 1 ? (type === 'drawer' ? 51.5 : 71) : h === 2 ? 99.5 : 195.5;
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
    if (/drawer box|back panel|runner slide|key lock|hidden key|top handle|hinge|lock (holder|inner|outer|pin)|backbone|handle lock|knob|second part|^divider$|depth divider|width divider|seal divider|heavyweight roof handle|^foot$/i.test(label)) return 'inner';
    return 'body';
  }

  // Print strength per part. The design is tuned for the profile default (2 walls, 15% infill), so most parts stay there;
  // more walls on big thin parts only adds shrink stress (warping, tight drawers). Extra walls go where bolts or wear are,
  // and extra walls + infill where the part carries the tower or takes force. Flexing parts must stay default.
  function strengthOf(label) {
    if (/^springs|^latch|geared rail/i.test(label)) return { flex: true };
    if (/^base|^foot|backbone|stationary handle|pull-out handle|knob|wheel disk|wheel cover|^bushing(?! jig)|^top handle|heavyweight roof handle|wall mount/i.test(label)) return { walls: 4, infill: 25 };
    if (/front \(facade\)|^hinge(?! rods)|^lock (holder|inner|outer)|runner guide|runner slide|^key lock|^hidden key|pegboard|^heavyweight roof \(/i.test(label)) return { walls: 3 };
    return {};
  }

  // One "drawer insert" = box + facade + lock + runners for a single-width drawer (S, M, L or XL)
  function drawerInsert(add, w, d, h, o, tag, inferred) {
    const fam = D + DRAWER_FAM_DIR[w] + '/';
    const t = tag ? ' (' + tag + ')' : '';
    const x = inferred ? { inferred } : {};
    if (w === 'XL') {
      if (d >= 6) {
        add('Drawer', 'Drawer box, part 1' + t, fam + `XL${d}/Boxes/XL${d} Box 1F Part 1.stl`, 1, x);
        add('Drawer', 'Drawer box, part 2' + t, fam + `XL${d}/Boxes/XL${d} Box 1F Part 2.stl`, 1, x);
      } else {
        add('Drawer', 'Drawer box' + t, fam + `XL${d}/Boxes/XL${d} Box 1F.stl`, 1, x);
        add('Drawer', 'Box back panel' + t, fam + `XL${d}/Boxes/XL${d} Back Panel.stl`, 1, x);
      }
      add('Drawer', 'Drawer front (facade)' + t, fam + 'XL Facade 1F.stl', 1, { supports: true, ...x });
      add('Runners', 'Runner guide' + t, U + `Runners/XL Runners/x${d} Runner Guide XL.stl`, 2, x);
      add('Runners', 'Runner slide' + t, U + `Runners/XL Runners/x${d} Runner Slide XL.stl`, 2, x);
    } else {
      add('Drawer', 'Drawer box' + t, fam + `${w}${d}/Boxes/${w}${d} Box ${h}F.stl`, 1, x);
      add('Drawer', 'Drawer front (facade)' + t, fam + `Facades/${w}${h}F (Turn On Supports).stl`, 1, { supports: true, ...x });
      add('Runners', 'Runner guide' + t, U + `Runners/x${d} Runner Guide.stl`, 2, x);
      add('Runners', 'Runner slide' + t, U + `Runners/x${d} Runner Slide.stl`, 2, x);
    }
    add('Runners', 'Runner stopper' + t, U + 'Runners/Runner Stopper.stl', 2, { spare: true, ...x });
    if (o.gearedRails) add('Runners', 'Geared rail' + t, U + `Geared Rails/${w} Rails.stl`, 2,
      { note: 'Optional in the manual. Adds locking force; use them if you put more than one box in a 2F/4F module.', ...x });
    if (o.lock === 'hidden') {
      add('Lock', 'Hidden key' + t, U + 'Hidden Key (Turn On Supports).stl', 1, { supports: true, ...x });
      add('Lock', 'Hidden key, part 2' + t, U + 'Hidden Key Part 2 (Turn on Supports).stl', 1, { supports: true, ...x });
    } else {
      add('Lock', 'Key lock' + t, U + 'Key (Turn On Supports).stl', 1, { supports: true, ...x });
      add('Lock', 'Key cap' + t, U + 'Key Cap.stl', 1, { spare: true, ...x });
    }
    add('Lock', 'Springs (pair)' + t, U + 'Springs.stl', 1, { note: 'One file holds both springs. Fit them flat side up.', spare: true, ...x });
    add('Lock', 'Latch' + t, U + 'Latch.stl', 1, x);
    add('Lock', 'Label' + t, U + 'Label.stl', 1, { note: 'Add your own text with the slicer’s text tool.', ...x });
    add('Lock', 'Facade cap' + t, U + 'Facade Cap.stl', 1, { spare: true, ...x });
    if (o.interior === 'gridfinity') {
      const subdir = fam + `${w}${d}/Gridfinity Baseplate/`;
      if (w === 'XL' && d >= 6) {
        add('Interior', 'Gridfinity baseplate, part 1' + t, subdir + `XL${d} Baseplate Part 1.stl`, 1, x);
        add('Interior', 'Gridfinity baseplate, part 2' + t, subdir + `XL${d} Baseplate Part 2.stl`, 1, x);
      } else {
        const v = o.baseplateHandles && o.baseplateHandles !== '0' ? `_With ${o.baseplateHandles} Handle${o.baseplateHandles === '1' ? '' : 's'}` : '';
        add('Interior', 'Gridfinity baseplate' + (v ? ` (${o.baseplateHandles}-handle cut-out)` : '') + t, subdir + `${w}${d} Baseplate${v}.stl`, 1,
          { fallback: subdir + `${w}${d} Baseplate.stl`, ...x });
      }
    }
    if (o.interior === 'grid') gridDividers(add, w, d, h, o, t);
    if (o.manualSupports) add('Drawer', 'Manual support' + t, U + `Manual Supports/x${d}.stl`, 1,
      { note: 'Optional print aid for tall prints. Not part of the finished drawer.', aid: true, ...x });
  }

  // Grid dividers: the file number is how many peg holes the divider spans.
  // Full width: 10-S, 18-M, 26-L, 32-XL. Full depth: 4 x depth - 2 (x3 = 10 ... x7 = 26).
  const GRID_DIR = {
    20: U + 'Grid Dividers/20MM TALL/',
    1: U + 'Grid Dividers/34.5MM TALL (full height of 1F drawers)/',
    2: U + 'Grid Dividers/82.5MM TALL (full height of 2F drawers)/',
  };
  const GRID_WIDTH_FILE = { S: '10-S, x3', M: '18-M, x5', L: '26-L, x7', XL: '32-XL' };
  const GRID_DEPTH_FILE = { 3: '10-S, x3', 4: '14, x4', 5: '18-M, x5', 6: '22, x6', 7: '26-L, x7' };
  function gridDividers(add, w, d, h, o, t) {
    const tall = o.gridHeight === 'full' ? (h === 1 ? 1 : 2) : 20;
    const dir = GRID_DIR[tall], sfx = tall === 20 ? '20MM' : tall + 'F';
    const across = +o.gridAcross || 0, along = +o.gridAlong || 0;
    if (across) add('Interior', `Grid divider, full width (${GRID_WIDTH_FILE[w].split(',')[0]})` + t, dir + GRID_WIDTH_FILE[w] + '.stl', across);
    if (along) add('Interior', `Grid divider, full depth (${GRID_DEPTH_FILE[d].split(',')[0]})` + t, dir + GRID_DEPTH_FILE[d] + '.stl', along);
    if (across + along) {
      add('Interior', 'Divider edge piece' + t, dir + `${o.gridEdge === 'rounded' ? 'Rounded' : 'Straight'} Edge Piece ${sfx}.stl`, 2 * (across + along),
        { note: 'Two per full-span divider, one at each wall.' });
      add('Interior', 'Divider pin' + t, U + `Grid Dividers/grid divider pin_${o.gridPin === 'loose' ? 'loose' : 'tight'}.stl`, 2 * (across + along),
        { spare: true, inferred: 'The instructions don’t give a pin count. Two per divider is read from the drawings.' });
    }
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
  function roof(add, rw, d, kind, topHandle) {
    if (!kind || kind === 'none') return;
    add('Roof', ROOFS.find(r => r.id === kind).label, D + DRAWER_FAM_DIR[rw] + '/' + `${rw}${d}/Roofs/${rw}${d} ${ROOF_FILE[kind]}.stl`, 1);
    if (kind === 'grid' && topHandle) add('Roof', 'Top handle', U + 'Top Handle (Turn On Supports).stl', 1, { supports: true });
    if (kind === 'heavy' || kind === 'heavycut') {
      add('Roof', 'Heavyweight roof handle', U + 'Heawyweight Roof Handle.stl', 1);
      add('Roof', 'Heavyweight roof insert', U + 'Heawyweight Roof Insert.stl', 1);
    }
  }

  function drawer(add, c) {
    const { w, d, h } = c;
    const fam = D + DRAWER_FAM_DIR[w] + '/';
    if (w === 'L2') {
      const why = 'The manual doesn’t list L² contents. L = S + S, so this assumes two S drawers side by side.';
      add('Module', 'Module shell', fam + `L${d}²/L${d}² Module ${h}F.stl`, 1);
      drawerInsert(add, 'S', d, h, c, 'left', why);
      drawerInsert(add, 'S', d, h, c, 'right', why);
      add('Module', 'L² accessory, 1st', U + `L² Accessories/x${d} Accessory 1st.stl`, 1, { inferred: 'One of each accessory per module is assumed.' });
      add('Module', 'L² accessory, 2nd', U + `L² Accessories/x${d} Accessory 2nd.stl`, 1, { inferred: 'One of each accessory per module is assumed.' });
    } else if (w === 'XL2') {
      const why = 'The manual doesn’t list XL² contents. XL = S + M, so this assumes an S and an M drawer side by side.';
      add('Module', 'Module shell', fam + `XL${d}²/XL${d}² Module 1F.stl`, 1);
      drawerInsert(add, 'S', d, 1, c, 'S side', why);
      drawerInsert(add, 'M', d, 1, c, 'M side', why);
    } else {
      add('Module', 'Module shell', fam + `${w}${d}/Modules/${w}${d} Module ${h}F.stl`, 1);
      drawerInsert(add, w, d, h, c, '');
    }
    if (c.roof && c.roof !== 'none') roof(add, w === 'L2' ? 'L' : w === 'XL2' ? 'XL' : w, d, c.roof, c.topHandle);
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
    add('Hinges & locks', 'Hinge', SUU + 'Hinges/' + (sm ? (h === 1 ? 'S-M 1F Hinge.stl' : 'S-M 2-4F Hinge.stl') : (h === 1 ? 'L-XL 1F Hinge.stl' : 'L 2-4F Hinge.stl')), 2,
      { note: 'Each file is one complete hinge (both leaves).' });
    if (sm) add('Hinges & locks', 'Hinge top', SUU + 'Hinges/' + (w === 'S' ? 'S Hinge Top.stl' : 'M Hinge Top.stl'), 2,
      { inferred: 'One hinge top per hinge is assumed; the S/M files hold a single top.' });
    else add('Hinges & locks', 'Hinge tops (pair)', SUU + 'Hinges/L-XL Hinge Top.stl', 1, { note: 'This file already contains two hinge tops.' });
    add('Hinges & locks', 'Hinge rods (pair)', SUU + 'Rods/' + (sm ? 'S-M Rods.stl' : 'L-XL Rods.stl'), 1, { note: 'One file holds both rods.', spare: true });
    add('Hinges & locks', 'Lock holder', SUU + 'Locks/LOCK HOLDER.stl', 2);
    add('Hinges & locks', 'Lock inner part', SUU + 'Locks/LOCK INNER PART.stl', 2);
    add('Hinges & locks', 'Lock outer part', SUU + 'Locks/' + (h === 1 ? 'LOCK OUTER PART 1F.stl' : 'LOCK OUTER PART 2-4F.stl'), 2);
    add('Hinges & locks', 'Lock pin set', SUU + 'Locks/1 SET OF PINS FOR 1 LOCK.stl', 2, { note: 'Four pins per file, one file per lock.', spare: true });
    add('Hinges & locks', 'Case label', SUU + 'Label for Sustainers.stl', 1);
    add('Hinges & locks', 'Front label', U + 'Label.stl', 1);
    if (c.caseBaseplate) {
      if (w === 'XL') {
        if (d >= 6) {
          add('Interior', 'Gridfinity baseplate, part 1', SUU + `Baseplates/04. XL/XL${d} Part 1  Gridfinity Baseplate.stl`, 1);
          add('Interior', 'Gridfinity baseplate, part 2', SUU + `Baseplates/04. XL/XL${d} Part 2  Gridfinity Baseplate.stl`, 1);
        } else add('Interior', 'Gridfinity baseplate', SUU + `Baseplates/04. XL/XL${d}  Gridfinity Baseplate.stl`, 1);
      } else add('Interior', 'Gridfinity baseplate', SUU + `Baseplates/0${'SML'.indexOf(w) + 1}. ${w}/${w}${d} Baseplate.stl`, 1);
    }
    const dv = c.dividers || {};
    if (w === 'S' || w === 'M') {
      if (dv.plain) add('Interior', 'Divider', SUU + `Dividers/${w} Dividers/${w}${h}F Divider.stl`, dv.plain);
    } else if (w === 'L') {
      if (dv.depth) add('Interior', 'Depth divider (runs front to back)', SUU + `Dividers/L Depth Dividers/L${d}-${h}F Depth Divider.stl`, dv.depth);
      if (dv.width) add('Interior', 'Width divider (runs side to side)', SUU + `Dividers/L Width Dividers/L-${h}F Width Divider.stl`, dv.width);
      if (dv.seal) add('Interior', 'Seal divider', SUU + `Dividers/L Seal Dividers/L-${h}F Seal Divider.stl`, dv.seal);
    } else if (w === 'XL') {
      if (dv.depth) add('Interior', 'Depth divider', SUU + `Dividers/XL Depth Dividers/XL${d} Depth Divider.stl`, dv.depth);
      if (dv.width) add('Interior', 'Width divider', SUU + 'Dividers/XL Width Divider.stl', dv.width);
      if (dv.seal) { add('Interior', 'Seal divider, center', SUU + 'Dividers/XL Seal Divider (Center).stl', dv.seal);
                     add('Interior', 'Seal divider, sides', SUU + 'Dividers/XL Seal Divider (Sides).stl', dv.seal * 2); }
    }
  }

  // Per-unit mounting add-ons
  function mounts(add, c) {
    const { h } = c;
    const w = c.w === 'L2' ? 'L' : c.w === 'XL2' ? 'XL' : c.w;
    if (c.wallMount) {
      add('Wall mount', 'Wall mount plate', MO + `Wall Mounts/${w}${h}F Wall Mount.stl`, 1,
        { note: 'Use full-height plates: a 1F plate on a taller module can’t serve as the drilling template.' });
      add('Wall mount', 'Wall mount second part (wall cleat)', MO + 'Wall Mounts/Wall Mount Second Part.stl', 2,
        { inferred: 'Two cleats per plate, read from the mounting drawings.' });
    }
    if (c.pegboard && c.pegboard !== 'none' && h <= 2) {
      add('Pegboard', (c.pegboard === 'ikea' ? 'IKEA Skådis' : 'USSA') + ' pegboard attachment',
        MO + `Pegboard Attachment/${c.pegboard === 'ikea' ? 'IKEA Skadis Pegboard' : 'USSA Pegboard'}/${w}${h}F.stl`, 1);
    }
    if (c.backbone && c.backbone !== 'none' && h <= 2) {
      add('Backbone', c.backbone === 'universal' ? 'Universal backbone' : 'Backbone',
        MO + `Backbone/${c.backbone === 'universal' ? 'Universal ' + h + 'F' : w + h + 'F'} Backbone.stl`, 1,
        { note: '2F backbones come sealed: mark the three spots on the module and drill through with a 4 mm bit.',
          inferred: 'One backbone per unit is read from the trolley drawings.' });
    }
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
      if (s.feet && (s.wheels || !s.casters)) add('Base', 'Foot', MO + `Feet/${w} Feet.stl`, s.wheels ? 1 : 2,
        s.wheels ? { note: 'One foot opposite the wheels.' } : { inferred: 'Without wheels, two feet are assumed. The manual only shows the wheeled version.' });
    }
    if (s.stationaryHandle) add('Handles', 'Stationary handle', MO + `Stationary Handle/${w} Stationary Handle.stl`, 1);
    if (s.pullHandle) {
      add('Handles', 'Pull-out handle', MO + `Pull-out Handle/${w} Pull-out Handle.stl`, 1);
      add('Handles', 'Pull-out handle lock', MO + `Backbone/${w} Pull-out Handle Lock.stl`, 1);
      if (w === 'S') add('Handles', 'Pull-out handle lock, part 2', MO + 'Backbone/S Pull-out Handle Lock Part 2.stl', 1);
      add('Handles', 'Handle lock knob, part 1', MO + 'Backbone/Handle Lock Knob Part 1.stl', 2, { inferred: 'Two knobs, read from the trolley drawings.' });
      add('Handles', 'Handle lock knob, part 2', MO + 'Backbone/Handle Lock Knob Part 2.stl', 2, { inferred: 'Two knobs, read from the trolley drawings.' });
    }
  }

  function unitHardware(c) {
    const hw = [];
    const push = (item, qty, why) => qty && hw.push({ item, qty, why });
    if (c.type === 'drawer') {
      // Front to box: one bolt per hole in the drawer front, counted in the STLs (Drawer Assembly 6/8 shows the 2 on an S 1F).
      // S: 2 at 1F, 4 at 2F/4F. M and L: 4 at 1F, 6 at 2F/4F. XL (1F only): 4. L² is two S drawers, XL² an S and an M (both 1F).
      const front = (w, h) => w === 'S' ? (h === 1 ? 2 : 4) : w === 'XL' ? 4 : (h === 1 ? 4 : 6);
      const bolts = c.w === 'L2' ? 2 * front('S', c.h) : c.w === 'XL2' ? front('S', 1) + front('M', 1) : front(c.w, c.h);
      push('M4 × 14 mm button-head bolt', bolts, 'Drawer front to box');
      if (c.roof === 'grid' && c.topHandle) push('M6 × 50 mm countersunk bolt', 2, 'Roof top handle');
    } else {
      push('M4 × 14 mm button-head bolt', 16, 'Case hinge tops and locks');
      push('M4 × 10 mm button-head bolt', 8, 'Case hinges');
      push('M4 × 20 mm button-head bolt', 7, 'Case front and body');
    }
    if (c.pegboard && c.pegboard !== 'none' && c.h <= 2) push('M4 × 40 mm button-head bolt', 4, 'Pegboard attachment');
    if (c.backbone && c.backbone !== 'none' && c.h <= 2) push('M4 button-head bolt, 60–100 mm (to fit)', 4, 'Backbone');
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
    if (s.base && s.feet && (s.wheels || !s.casters)) push('M6 × 90 mm button-head bolt', 2 * (s.wheels ? 1 : 2), 'Feet');
    if (s.base && !s.wheels && s.casters) push('Caster with M8 bolt', 4, 'Casters (instead of wheels)');
    if (s.stationaryHandle) push('M4 × 60 mm button-head bolt', 8, 'Stationary handle');
    if (s.pullHandle) {
      push('M6 × 30 mm countersunk bolt', 4, 'Pull-out handle');
      push('M6 × 35 mm hex bolt', 2, 'Handle lock');
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
      const l = { group, label, file: f, qty, color: colorOf(label, group), ...strengthOf(label), ...extra };
      // Bambu Studio's own check says this part has overhangs that need supports (see src/bambu-support-audit.tsv)
      if (f.needsSupport && !l.aid) { l.supports = true; if (!extra.supports) l.supportsWhy = 'bambu'; }
      lines.push(l);
    };
    return { lines, missing, add };
  }

  // One unit, as configured. Includes its roof when c.roof is set (the page clears it for units that aren't on top).
  function buildUnit(c, resolve) {
    const k = collector(resolve);
    if (c.type === 'drawer') drawer(k.add, c); else sustainer(k.add, c, resolve);
    mounts(k.add, c);
    return { lines: k.lines, missing: k.missing, hardware: unitHardware(c) };
  }
  // A tower's base, wheels, feet and handles. s = { w: 'S'|'M'|'L'|'XL', d, base, wheels, feet, casters, stationaryHandle, pullHandle }
  function buildStack(s, resolve) {
    const k = collector(resolve);
    stackParts(k.add, s);
    return { lines: k.lines, missing: k.missing, hardware: stackHardware(s) };
  }
  // Roof on its own, for a top level made of two units side by side (sized to their combined width)
  function buildRoof(rw, d, kind, topHandle, resolve) {
    const k = collector(resolve);
    roof(k.add, rw, d, kind, topHandle);
    return { lines: k.lines, missing: k.missing, hardware: kind === 'grid' && topHandle ? [{ item: 'M6 × 50 mm countersunk bolt', qty: 2, why: 'Roof top handle' }] : [] };
  }

  const api = { buildUnit, buildStack, buildRoof, makeResolver, exterior, familyForWidth, HEIGHTS, DEPTHS, ROOFS, WIDTH_MM, norm };
  if (typeof module !== 'undefined') module.exports = api; else root.VaultRules = api;
})(this);
