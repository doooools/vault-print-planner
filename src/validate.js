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
  const has = f => r.lines.some(l => l.file.path.endsWith('/' + f));
  const want = { top: kind === 'grid' && th, heavy: kind === 'heavy' || kind === 'heavycut', insert: kind === 'heavy' || kind === 'heavycut' };
  for (const k of Object.keys(HANDLE)) if (has(HANDLE[k]) !== want[k]) roofClash.push(`${what} ${kind}${th ? ' + top handle' : ''}: ${HANDLE[k]} ${want[k] ? 'missing' : 'listed but not wanted'}`);
  const bolts = r.hardware.filter(h => /M6 × 50/.test(h.item)).reduce((a, h) => a + h.qty, 0);
  if (bolts !== (want.top ? 2 : 0)) roofClash.push(`${what} ${kind}${th ? ' + top handle' : ''}: ${bolts} M6 × 50 bolts`);
};
for (const w of Object.keys(R.HEIGHTS.drawer)) for (const d of R.DEPTHS) for (const rf of R.ROOFS.filter(x => x.widths.includes(w))) for (const th of [false, true]) {
  const c = { type: 'drawer', w, d, h: R.HEIGHTS.drawer[w][0], lock: 'std', interior: 'empty', roof: rf.id, topHandle: th };
  checkRoof(R.buildUnit(c, resolve), rf.id, th, `drawer ${w}${d}`);
  if (!/2$/.test(w)) checkRoof(R.buildRoof(w, d, rf.id, th, resolve), rf.id, th, `roof over a pair, ${w}${d}`);
}
console.log('ROOF HANDLES:'); roofClash.slice(0, 20).forEach(m => console.log(' ', m)); if (roofClash.length > 20) console.log(`  (+${roofClash.length - 20})`);
if (process.argv[3]) fs.writeFileSync(process.argv[3], [...used].sort().join('\n') + '\n');
console.log('ROLE COLOURS:'); roleClash.forEach(m => console.log(' ', m));
console.log('MISSING:'); for (const [m, w] of bad) console.log(' ', m, '<-', w.slice(0, 3).join(', '), w.length > 3 ? `(+${w.length - 3})` : '');
console.log('\nUNUSED FILES:'); list.filter(p => !used.has(p) && !/Grid Dividers\/[^/]+\/\d/.test(p)).forEach(p => console.log(' ', p));
