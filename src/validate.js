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
console.log('PLACEMENT COUNTS:'); [...new Set(countClash)].slice(0, 20).forEach(m => console.log(' ', m)); if (countClash.length > 20) console.log(`  (+${countClash.length - 20})`);
console.log('ROOF HANDLES:'); roofClash.slice(0, 20).forEach(m => console.log(' ', m)); if (roofClash.length > 20) console.log(`  (+${roofClash.length - 20})`);
if (process.argv[3]) fs.writeFileSync(process.argv[3], [...used].sort().join('\n') + '\n');
console.log('ROLE COLOURS:'); roleClash.forEach(m => console.log(' ', m));
console.log('MISSING:'); for (const [m, w] of bad) console.log(' ', m, '<-', w.slice(0, 3).join(', '), w.length > 3 ? `(+${w.length - 3})` : '');
console.log('\nUNUSED FILES:'); list.filter(p => !used.has(p) && !/Grid Dividers\/[^/]+\/\d/.test(p)).forEach(p => console.log(' ', p));
