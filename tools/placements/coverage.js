// List every unit the planner can build and the files it gives each one, from src/rules.js itself.
//
//   node tools/placements/coverage.js <_stl_index.jsonl> <out.json>
//
// The index (stl_index.py) stands in for the user's folder: the resolver sees the same files the page
// would. Each unit is built with every option turned on, one variant at a time (key lock / hidden key,
// baseplate cut-outs, grid divider heights, mounts...), and the lines are merged per file.
// Unit keys follow the 3D view's: drawer|w|d|h, case|w|d|h, roof|w|d|id, and stack|w|d for a tower's
// base, wheels, feet and handles (sized by the bottom level).
const fs = require('fs'), path = require('path');
const R = require(path.join(__dirname, '../../src/rules.js'));
const [idxPath, out] = process.argv.slice(2);
// Some unzip tools turn the '²' of L²/XL² into '┬▓' (cp437): give the page's spelling
const canon = p => p.replace(/┬▓/g, '²');
const files = fs.readFileSync(idxPath, 'utf8').split('\n').filter(Boolean).map(l => ({ path: canon(JSON.parse(l).file) }));
const resolve = R.makeResolver(files);

const units = {};
function merge(key, res, extra = {}) {
  const u = units[key] || (units[key] = { lines: {}, missing: new Set(), ...extra });
  for (const l of res.lines) {
    const p = l.file.path, cur = u.lines[p];
    if (!cur) u.lines[p] = { label: l.label, group: l.group, qty: l.qty, role: l.role, aid: !!l.aid, alt: l.alt || null };
    else cur.qty = Math.max(cur.qty, l.qty);
  }
  for (const m of res.missing) u.missing.add(m);
}

const drawerVariants = [
  { lock: 'std', gearedRails: true, interior: 'gridfinity', baseplateHandles: '0', manualSupports: true, wallMount: true, pegboard: 'ikea', backbone: 'family' },
  { lock: 'hidden', interior: 'gridfinity', baseplateHandles: '1', pegboard: 'ussa', backbone: 'universal' },
  { interior: 'gridfinity', baseplateHandles: '2' },
  { interior: 'grid', gridAcross: 1, gridAlong: 1, gridHeight: '20', gridEdge: 'straight', gridPin: 'tight' },
  { interior: 'grid', gridAcross: 1, gridAlong: 1, gridHeight: 'full', gridEdge: 'rounded', gridPin: 'loose' },
];
for (const w of ['S', 'M', 'L', 'L2', 'XL', 'XL2']) for (const d of R.DEPTHS) for (const h of R.HEIGHTS.drawer[w]) {
  for (const v of drawerVariants) merge(`drawer|${w}|${d}|${h}`, R.buildUnit({ type: 'drawer', w, d, h, roof: 'none', ...v }, resolve));
  // roofs: the page keys a single unit's roof by the unit's own width (L2, XL2 included)
  for (const rf of R.ROOFS) if (rf.widths.includes(w)) for (const th of [false, true]) {
    const res = R.buildUnit({ type: 'drawer', w, d, h, roof: rf.id, topHandle: th }, resolve);
    merge(`roof|${w}|${d}|${rf.id}`, { lines: res.lines.filter(l => l.group === 'Roof'), missing: [] });
  }
}
for (const w of ['S', 'M', 'L', 'XL']) for (const d of R.DEPTHS) for (const h of R.HEIGHTS.case[w]) {
  for (const ci of (w === 'L' || w === 'XL') ? ['flat', 'dividers', 'sealed'] : ['flat'])
    merge(`case|${w}|${d}|${h}`, R.buildUnit({ type: 'case', w, d, h, caseInterior: ci, caseBaseplate: true,
      dividers: { plain: 1, depth: 1, width: 1, seal: 1 }, wallMount: true, pegboard: 'ikea', backbone: 'family' }, resolve));
  merge(`case|${w}|${d}|${h}`, R.buildUnit({ type: 'case', w, d, h, pegboard: 'ussa', backbone: 'universal' }, resolve));
}
// The handles go with the backbone column (column|w, measure_column.py), the base, wheels and foot with stack|w|d
const handles = res => ({ lines: res.lines.filter(l => l.group === 'Handles'), missing: [] });
const noHandles = res => ({ lines: res.lines.filter(l => l.group !== 'Handles'), missing: res.missing });
for (const w of ['S', 'M', 'L', 'XL']) for (const d of R.DEPTHS) {
  const all = R.buildStack({ w, d, base: true, wheels: true, feet: true, stationaryHandle: true, pullHandle: true }, resolve);
  merge(`stack|${w}|${d}`, noHandles(all));
  merge(`stack|${w}|${d}`, R.buildStack({ w, d, base: true, wheels: false, feet: true, casters: false }, resolve));
  merge(`column|${w}`, handles(all));
}
// The backbone column: family backbones per width, the universal ones (one per rod) on their own
for (const w of ['S', 'M', 'L', 'XL']) for (const heights of [[2, 1], [1, 1, 1]]) {
  merge(`column|${w}`, R.buildBackbones({ w, base: true, heights, upTo: heights.length - 1, universal: false }, resolve));
  merge('column|U', R.buildBackbones({ w, base: true, heights, upTo: heights.length - 1, universal: true }, resolve));
}
const res = {};
for (const [k, u] of Object.entries(units)) res[k] = { lines: u.lines, missing: [...u.missing] };
fs.writeFileSync(out, JSON.stringify(res, null, 1));
console.log(Object.keys(res).length, 'units,', Object.values(res).reduce((n, u) => n + Object.keys(u.lines).length, 0), 'unit-file pairs,',
  Object.values(res).reduce((n, u) => n + u.missing.length, 0), 'missing paths');
