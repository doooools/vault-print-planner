// Measures what the 3D view's simplifier (meshJob in src/template.html) does to part files: open edges and holes,
// edges of more than two faces, triangles and time, for the file as it is and for the simplified mesh.
// Never commit a part file nor anything drawn from one: run it on your own Vault download.
//
//   npm install --prefix <dir> meshoptimizer@1.3.0
//   MESHOPT=<dir>/node_modules/meshoptimizer/meshopt_simplifier.js node tools/mesh_check.mjs [--old <template.html>] [--tol 0.15] <file.stl>...
//
// --old: also run the meshJob of another template.html (e.g. `git show preprod:src/template.html > old.html`).
// Prints one JSON line per file. "open" = edges with one face, "nm" = edges with more than two, "holes" = groups of
// open edges more than 1 mm across, "big" = the largest across (mm).
import fs from 'fs';
import path from 'path';
import { pathToFileURL } from 'url';

const args = process.argv.slice(2), opt = { tol: 0.15, old: null };
const files = [];
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--tol') opt.tol = +args[++i];
  else if (args[i] === '--old') opt.old = args[++i];
  else files.push(args[i]);
}
const here = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const jobOf = file => {
  const t = fs.readFileSync(file, 'utf8');
  const src = t.slice(t.indexOf('  function meshJob('), t.indexOf("  // A file's connected pieces"));
  return new Function('return ' + src.trim())();
};
const { MeshoptSimplifier: MS } = await import(pathToFileURL(process.env.MESHOPT || 'meshopt_simplifier.js').href);
await MS.ready;
const job = jobOf(path.join(here, '..', 'src', 'template.html')), old = opt.old && jobOf(opt.old);

// open edges, edges of more than two faces, and the groups of open edges (holes) with their size
function topo(idx, pos) {
  const E = new Map(), K = pos.length / 3 + 1;
  for (let t = 0; t < idx.length; t += 3) for (let k = 0; k < 3; k++) {
    const a = idx[t + k], b = idx[t + (k + 1) % 3], key = a < b ? a * K + b : b * K + a;
    E.set(key, (E.get(key) || 0) + 1);
  }
  let open = 0, nm = 0;
  const adj = new Map(), link = (a, b) => { let l = adj.get(a); if (!l) adj.set(a, l = []); l.push(b); };
  for (const [key, c] of E) {
    if (c > 2) nm++;
    if (c !== 1) continue;
    open++;
    const a = Math.floor(key / K), b = key % K; link(a, b); link(b, a);
  }
  const seen = new Set(), holes = [];
  for (const v0 of adj.keys()) {
    if (seen.has(v0)) continue;
    const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity], st = [v0]; seen.add(v0);
    while (st.length) {
      const v = st.pop();
      for (let d = 0; d < 3; d++) { lo[d] = Math.min(lo[d], pos[v * 3 + d]); hi[d] = Math.max(hi[d], pos[v * 3 + d]); }
      for (const w of adj.get(v)) if (!seen.has(w)) { seen.add(w); st.push(w); }
    }
    holes.push(Math.hypot(hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]));
  }
  return { tris: idx.length / 3, open, nm, holes: holes.filter(h => h > 1).length, big: +Math.max(0, ...holes).toFixed(2) };
}
const ab = b => b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength);
for (const f of files) {
  const buf = fs.readFileSync(f), row = { file: path.basename(f) };
  try { const r = job(ab(buf), MS, 0, 0); row.asIs = topo(r.idx, r.pos); } catch (e) { row.asIs = String(e.message || e); }
  let t = performance.now(); const r = job(ab(buf), MS, opt.tol, 150000); row.ms = Math.round(performance.now() - t);
  row.now = topo(r.idx, r.pos);
  if (old) { t = performance.now(); const o = old(ab(buf), MS, opt.tol, 150000); row.oldMs = Math.round(performance.now() - t); row.old = topo(o.idx, o.pos); }
  console.log(JSON.stringify(row));
}
