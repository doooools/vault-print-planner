// Runs every unit configuration and tower base through the rules and reports file paths that don't resolve.
// usage: node validate.js <file list> [write used paths to this file]
const fs = require('fs');
const R = require('./rules.js');
const list = fs.readFileSync(process.argv[2], 'utf8').trim().split('\n').filter(p => p.endsWith('.stl'));
const resolve = R.makeResolver(list.map(path => ({ path })));
const used = new Set(), bad = new Map();
// Every part of a colour role must default to that role's colour, so choosing nothing plans as before
const roleColor = new Map(), roleClash = new Set();
const note = (r, what) => {
  r.lines.forEach(l => used.add(l.file.path));
  r.lines.forEach(l => {
    const want = l.role === 'tpu' ? 'tpu' : (R.ROLES.find(x => x.id === l.role) || {}).def;
    if (want !== l.color) roleClash.add(`${l.label} (${l.group}): role ${l.role} defaults to ${want}, colorOf says ${l.color}`);
  });
  r.missing.forEach(m => bad.set(m, (bad.get(m) || []).concat(what)));
};
const all = { gearedRails: true, interior: 'gridfinity', gridAcross: 1, gridAlong: 1, manualSupports: true, topHandle: true, wallMount: true,
  pegboard: 'ikea', backbone: 'family', caseBaseplate: true, dividers: { plain: 1, depth: 1, width: 1, seal: 1 } };
const variants = [{ lock: 'std', roof: 'grid', baseplateHandles: '0', caseInterior: 'flat', pegboard: 'ussa', backbone: 'universal' },
  { lock: 'hidden', roof: 'heavy', baseplateHandles: '2', caseInterior: 'dividers' },
  { roof: 'table', baseplateHandles: '1', caseInterior: 'sealed' },
  { roof: 'bowl', interior: 'grid', gridHeight: 'full', gridEdge: 'rounded', gridPin: 'loose' },
  { roof: 'undertable', interior: 'grid' }, { roof: 'heavycut', interior: 'grid', gridEdge: 'rounded' }];
for (const type of ['drawer', 'case']) for (const w of Object.keys(R.HEIGHTS[type])) for (const d of R.DEPTHS) for (const h of R.HEIGHTS[type][w])
  for (const v of variants) {
    const c = { type, w, d, h, ...all, ...v };
    if (!R.ROOFS.find(r => r.id === c.roof).widths.includes(w)) c.roof = 'grid';
    note(R.buildUnit(c, resolve), `${type} ${w}${d} ${h}F`);
  }
for (const w of ['S', 'M', 'L', 'XL']) for (const d of R.DEPTHS)
  for (const s of [{ base: true, wheels: true, feet: true, stationaryHandle: true, pullHandle: true }, { base: true, feet: true }])
    note(R.buildStack({ w, d, ...s }, resolve), `stack ${w}${d}`);
// Roof handles (manual: Roof Types, Required Hardware - Drawers): the grid roof takes the top handle and 2 M6 x 50
// bolts when asked, the heavyweight roofs always come with their handle and insert, and no other roof has one. Checked
// on a unit's own roof and on the wide roof over two units side by side (buildRoof).
const HANDLE = { top: 'Top Handle (Turn On Supports).stl', heavy: 'Heawyweight Roof Handle.stl', insert: 'Heawyweight Roof Insert.stl' };
const roofClash = [];
const checkRoof = (r, kind, th, what) => {
  const qty = f => r.lines.filter(l => l.file.path.endsWith('/' + f)).reduce((a, l) => a + l.qty, 0);
  const heavy = kind === 'heavy' || kind === 'heavycut';
  // one insert per pocket: the bar has a pocket at each end
  const want = { top: kind === 'grid' && th ? 1 : 0, heavy: heavy ? 1 : 0, insert: heavy ? 2 : 0 };
  for (const k of Object.keys(HANDLE)) if (qty(HANDLE[k]) !== want[k]) roofClash.push(`${what} ${kind}${th ? ' + top handle' : ''}: ${qty(HANDLE[k])} × ${HANDLE[k]}, want ${want[k]}`);
  const bolts = r.hardware.filter(h => /M6 × 50/.test(h.item)).reduce((a, h) => a + h.qty, 0);
  if (bolts !== (want.top ? 2 : 0)) roofClash.push(`${what} ${kind}${th ? ' + top handle' : ''}: ${bolts} M6 × 50 bolts`);
};
for (const w of Object.keys(R.HEIGHTS.drawer)) for (const d of R.DEPTHS) for (const rf of R.ROOFS.filter(x => x.widths.includes(w))) for (const th of [false, true]) {
  const c = { type: 'drawer', w, d, h: R.HEIGHTS.drawer[w][0], lock: 'std', interior: 'empty', roof: rf.id, topHandle: th };
  checkRoof(R.buildUnit(c, resolve), rf.id, th, `drawer ${w}${d}`);
  if (!/2$/.test(w)) checkRoof(R.buildRoof(w, d, rf.id, th, resolve), rf.id, th, `roof over a pair, ${w}${d}`);
}
// Quantities against the measured assembly (stl-placements.json, one entry per copy): a file both list and place must
// have as many copies in the list.
const PL = JSON.parse(fs.readFileSync(require('path').join(__dirname, 'stl-placements.json'), 'utf8'));
const countClash = [];
for (const [key, pu] of Object.entries(PL.units)) {
  const [kind, w, d, h] = key.split('|');
  // An entry with `piece` is one piece of its file (a rack, a hinge leaf): a file is printed once per set of its
  // pieces, so its copies are its entries over its distinct pieces
  const placed = {}, pieces = {};
  pu.parts.forEach(([p, , , , o]) => {
    const k = R.norm(p); placed[k] = (placed[k] || 0) + 1;
    if (o && o.piece) (pieces[k] = pieces[k] || new Set()).add(o.piece.join(','));
  });
  for (const k of Object.keys(pieces)) placed[k] /= pieces[k].size;
  for (const lock of ['std', 'hidden']) {
    const c = kind === 'roof' ? { type: 'drawer', w, d: +d, h: R.HEIGHTS.drawer[w][0], roof: h, topHandle: true, lock, interior: 'gridfinity' }
      : { type: kind, w, d: +d, h: +h, roof: 'none', lock, interior: 'gridfinity', gearedRails: true };
    const lines = R.buildUnit(c, resolve).lines.filter(l => (l.group === 'Roof') === (kind === 'roof'));
    // a roof's latches are its unit's (the page gives a roof the files its unit lists)
    const own = kind === 'roof' ? R.buildUnit({ ...c, roof: 'none' }, resolve).lines : [];
    const listed = {};
    for (const l of lines.length && kind === 'roof' ? lines.concat(own.filter(o => !lines.some(x => R.norm(x.file.path) === R.norm(o.file.path)))) : lines)
      listed[R.norm(l.file.path)] = (listed[R.norm(l.file.path)] || 0) + l.qty;
    for (const [p, n] of Object.entries(listed)) {
      if (placed[p] === undefined || placed[p] === n) continue;
      countClash.push(`${key} ${lock}: ${p.split('/').pop()} listed ${n}, placed ${placed[p]}`);
    }
  }
}
// Drawers per module (src/rules.js LAYOUTS): every layout of every drawer shell resolves its files, and is counted as
// the manuals have it. Per module: shell, a pair of runner guides, slides and stoppers per 48 mm level, the latch (S
// and M one, L and XL two; L² is two S sides). Per drawer: box and front of its height, lock, springs, label, geared
// rails, the front's bolts and its caps (every counterbore but the label's).
const layoutClash = [];
const FRONT_BOLTS = (w, h) => w === 'S' ? (h === 1 ? 2 : 4) : w === 'XL' ? 4 : (h === 1 ? 4 : 6);
for (const w of ['S', 'M', 'L', 'L2']) for (const d of R.DEPTHS) for (const h of R.HEIGHTS.drawer[w]) for (const lay of R.LAYOUTS[h])
  for (const lock of ['std', 'hidden']) {
    const c = { type: 'drawer', w, d, h, drawers: lay, lock, interior: 'gridfinity', gearedRails: true, roof: 'none' };
    const what = `drawer ${w}${d} ${h}F [${lay.join(' ')}] ${lock}`;
    const r = R.buildUnit(c, resolve);
    note(r, what);
    if (R.drawersOf(c).join() !== lay.join()) layoutClash.push(`${what}: drawersOf gives ${R.drawersOf(c).join(' ')}`);
    const sides = w === 'L2' ? 2 : 1, fw = w === 'L2' ? 'S' : w;
    const qty = re => r.lines.filter(l => re.test(l.file.path)).reduce((a, l) => a + l.qty, 0);
    const want = {
      shell: [/ Module \dF\.stl$/i, 1],
      boxes: [/ Box \dF\.stl$/i, sides * lay.length],
      fronts: [/Facades\/.*F \(Turn On Supports\)\.stl$/, sides * lay.length],
      guides: [/Runner Guide\.stl$/, sides * 2 * h], slides: [/Runner Slide\.stl$/, sides * 2 * h], stoppers: [/Runner Stopper\.stl$/, sides * 2 * h],
      latches: [/\/Latch\.stl$/, w === 'L' || w === 'L2' ? 2 : 1],
      locks: [lock === 'hidden' ? /\/Hidden Key \(Turn On Supports\)\.stl$/ : /\/Key \(Turn On Supports\)\.stl$/, sides * lay.length],
      springs: [/\/Springs\.stl$/, sides * lay.length], labels: [/\/Label\.stl$/, sides * lay.length], rails: [/ Rails\.stl$/, sides * lay.length],
      caps: [/\/Facade Cap\.stl$/, sides * lay.reduce((a, dh) => a + FRONT_BOLTS(fw, dh) - 1, 0)],
    };
    for (const [k, [re, n]] of Object.entries(want)) if (qty(re) !== n) layoutClash.push(`${what}: ${qty(re)} ${k}, want ${n}`);
    // each drawer's box and front are its own height
    for (const dh of new Set(lay)) {
      const n = sides * lay.filter(x => x === dh).length;
      const re = new RegExp(` Box ${dh}F\\.stl$`, 'i');
      if (qty(re) !== n) layoutClash.push(`${what}: ${dh}F boxes ${qty(re)}, want ${n}`);
    }
    const mixed = new Set(lay).size > 1 || w === 'L2'; // L² contents are inferred anyway
    if (mixed !== r.lines.filter(l => l.group === 'Drawer').every(l => l.inferred)) layoutClash.push(`${what}: ${mixed ? 'mixed layout not marked inferred' : 'marked inferred'}`);
    const bolts = r.hardware.filter(x => /M4 × 14/.test(x.item)).reduce((a, x) => a + x.qty, 0);
    if (bolts !== sides * lay.reduce((a, dh) => a + FRONT_BOLTS(fw, dh), 0)) layoutClash.push(`${what}: ${bolts} front bolts`);
  }
// A list that isn't one of the shell's layouts plans one drawer of the shell's height, and XL is always one 1F drawer
for (const [c, want] of [[{ w: 'S', h: 2, drawers: [1] }, '2'], [{ w: 'M', h: 4, drawers: [3, 1] }, '4'], [{ w: 'XL', h: 1, drawers: [1, 1] }, '1'], [{ w: 'L', h: 2 }, '2']])
  if (R.drawersOf(c).join() !== want) layoutClash.push(`drawersOf(${JSON.stringify(c)}) = ${R.drawersOf(c).join(' ')}, want ${want}`);
// Counts checked by the part-count battery (tests/battery): one label per case (Sustainers Naming), the removable hidden
// key once per stack and not per drawer, one wall cleat per opening of the plate, a backbone under every pegboard, and
// one line per file in a unit (the two bays of L² and XL² merged)
const countRules = [];
const fileQty = (r, re) => r.lines.filter(l => re.test(l.file.path)).reduce((a, l) => a + l.qty, 0);
note(R.buildHiddenKey(resolve), 'hidden key');
for (const w of Object.keys(R.HEIGHTS.case)) for (const d of R.DEPTHS) for (const h of R.HEIGHTS.case[w]) {
  const r = R.buildUnit({ type: 'case', w, d, h, roof: 'none' }, resolve), what = `case ${w}${d} ${h}F`;
  const sus = fileQty(r, /Label for Sustainers\.stl$/), drw = fileQty(r, /07\. Universal\/Label\.stl$/);
  if (sus !== (h === 1 ? 1 : 0) || drw !== (h === 1 ? 0 : 1)) countRules.push(`${what}: ${sus} sustainer label, ${drw} drawer label`);
}
for (const type of ['drawer', 'case']) for (const w of Object.keys(R.HEIGHTS[type])) for (const d of R.DEPTHS) for (const h of R.HEIGHTS[type][w]) {
  const base = { type, w, d, h, roof: 'none', lock: 'hidden' }, what = `${type} ${w}${d} ${h}F`;
  const r = R.buildUnit(base, resolve);
  if (fileQty(r, /Hidden Key Part 2/i)) countRules.push(`${what}: removable hidden key listed in the unit`);
  const paths = r.lines.map(l => l.file.path + '|' + (l.alt || ''));
  if (new Set(paths).size !== paths.length) countRules.push(`${what}: a file listed on two lines`);
  const fw = w === 'L2' ? 'L' : w === 'XL2' ? 'XL' : w;
  const wm = R.buildUnit({ ...base, wallMount: true }, resolve);
  if (fileQty(wm, /Wall Mount Second Part\.stl$/) !== (h === 4 ? 2 : 1) * (fw === 'L' || fw === 'XL' ? 2 : 1)) countRules.push(`${what}: ${fileQty(wm, /Wall Mount Second Part\.stl$/)} wall cleats`);
  if (fileQty(R.buildUnit({ ...base, pegboard: 'ikea', backbone: 'family' }, resolve), /Backbone\.stl$/)) countRules.push(`${what}: a backbone listed in the unit (it belongs to the stack's column)`);
}
// The backbone column (Modifications Assembly 7-15): 2F backbones over the base (as 1F) and the modules it covers, a 1F
// for an odd remainder, at least one 2F from the base; XL has 1F backbones only
const BB = [[{ base: true, heights: [2], upTo: -1 }, 1, 0], [{ base: true, heights: [2, 1, 1], upTo: 1 }, 2, 0], [{ base: true, heights: [2, 1], upTo: 0 }, 1, 1],
  [{ base: true, heights: [2, 4, 1, 2], upTo: 2 }, 4, 0], [{ base: false, heights: [2, 2], upTo: 0 }, 1, 0], [{ base: false, heights: [1], upTo: 0 }, 0, 1]];
for (const w of ['S', 'M', 'L', 'XL']) for (const universal of [false, true]) {
  note(R.buildBackbones({ w, base: true, heights: [2, 1], upTo: 0, universal }, resolve), `backbones ${w}`);
  for (const [o, twos, ones] of BB) {
    const r = R.buildBackbones({ w, universal, ...o }, resolve), f = 2 * twos + ones;
    const want2 = !universal && w === 'XL' ? 0 : twos, want1 = !universal && w === 'XL' ? f : ones;
    const got2 = fileQty(r, /2F Backbone\.stl$/), got1 = fileQty(r, /1F Backbone\.stl$/);
    if (got2 !== want2 || got1 !== want1) countRules.push(`backbones ${w}${universal ? ' universal' : ''} ${JSON.stringify(o)}: ${got2} × 2F + ${got1} × 1F, want ${want2} + ${want1}`);
  }
}
console.log('COUNT RULES:'); countRules.slice(0, 20).forEach(m => console.log(' ', m)); if (countRules.length > 20) console.log(`  (+${countRules.length - 20})`);
console.log('DRAWER LAYOUTS:'); layoutClash.slice(0, 20).forEach(m => console.log(' ', m)); if (layoutClash.length > 20) console.log(`  (+${layoutClash.length - 20})`);
console.log('PLACEMENT COUNTS:'); [...new Set(countClash)].slice(0, 20).forEach(m => console.log(' ', m)); if (countClash.length > 20) console.log(`  (+${countClash.length - 20})`);
console.log('ROOF HANDLES:'); roofClash.slice(0, 20).forEach(m => console.log(' ', m)); if (roofClash.length > 20) console.log(`  (+${roofClash.length - 20})`);
if (process.argv[3]) fs.writeFileSync(process.argv[3], [...used].sort().join('\n') + '\n');
console.log('ROLE COLOURS:'); roleClash.forEach(m => console.log(' ', m));
console.log('MISSING:'); for (const [m, w] of bad) console.log(' ', m, '<-', w.slice(0, 3).join(', '), w.length > 3 ? `(+${w.length - 3})` : '');
console.log('\nUNUSED FILES:'); list.filter(p => !used.has(p) && !/Grid Dividers\/[^/]+\/\d/.test(p)).forEach(p => console.log(' ', p));
