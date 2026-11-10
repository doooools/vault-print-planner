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
if (process.argv[3]) fs.writeFileSync(process.argv[3], [...used].sort().join('\n') + '\n');
console.log('ROLE COLOURS:'); roleClash.forEach(m => console.log(' ', m));
console.log('MISSING:'); for (const [m, w] of bad) console.log(' ', m, '<-', w.slice(0, 3).join(', '), w.length > 3 ? `(+${w.length - 3})` : '');
console.log('\nUNUSED FILES:'); list.filter(p => !used.has(p) && !/Grid Dividers\/[^/]+\/\d/.test(p)).forEach(p => console.log(' ', p));
