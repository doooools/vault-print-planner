// Test driver: clicks the page's own controls and reads what it shows. Injected after each load.
window.T = (() => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const txt = e => (e ? e.textContent : '').replace(/\s+/g, ' ').trim();
  async function c(sel, root) {
    const e = typeof sel === 'string' ? (root || document).querySelector(sel) : sel;
    if (!e) throw new Error('not found: ' + sel);
    if (e.disabled) throw new Error('disabled: ' + sel);
    e.scrollIntoView({ block: 'center' });
    e.click(); await sleep(250); return e;
  }
  async function check(sel, on) {
    const e = document.querySelector(sel); if (!e) throw new Error('not found: ' + sel);
    if (e.checked !== on) { e.checked = on; e.dispatchEvent(new Event('change', { bubbles: true })); await sleep(250); }
  }
  const tab = async n => c($$('[role=tab]').find(t => txt(t).startsWith(n + ' ·')));
  // Stack settings panel on (level inspector off)
  async function stackPanel() {
    await tab(1);
    const b = document.querySelector('[data-dstack]');
    if (b.getAttribute('aria-pressed') !== 'true') await c(b);
  }
  // Select a unit in the side list of the 3D view: ui = index in v3.units (bottom first); the list is shown top first
  async function pickUnit(name) {
    await tab(1);
    const li = $$('#v3dList li').find(l => txt(l.querySelector('b')) === name);
    if (!li) throw new Error('unit not in list: ' + name + ' / ' + $$('#v3dList li b').map(txt).join(' | '));
    await c(li.querySelector('[data-v3pick]'));
  }
  const units = () => $$('#v3dList li b').map(txt);
  // Plate rectangle corners (SVG user units = mm) after their rotate()
  function corners(r) {
    const x = +r.getAttribute('x'), y = +r.getAttribute('y'), w = +r.getAttribute('width'), h = +r.getAttribute('height');
    let pts = [[x, y], [x + w, y], [x + w, y + h], [x, y + h]];
    const tr = r.getAttribute('transform');
    if (tr) {
      const m = tr.match(/rotate\(([-\d.e]+) ([-\d.e]+) ([-\d.e]+)\)/);
      const a = +m[1] * Math.PI / 180, cx = +m[2], cy = +m[3];
      pts = pts.map(([px, py]) => [cx + (px - cx) * Math.cos(a) - (py - cy) * Math.sin(a), cy + (px - cx) * Math.sin(a) + (py - cy) * Math.cos(a)]);
    }
    return pts;
  }
  function overlap(A, B) { // separating axis for convex quads
    for (const P of [A, B]) for (let i = 0; i < 4; i++) {
      const [x1, y1] = P[i], [x2, y2] = P[(i + 1) % 4], nx = y2 - y1, ny = x1 - x2;
      const pa = A.map(([x, y]) => x * nx + y * ny), pb = B.map(([x, y]) => x * nx + y * ny);
      const len = Math.hypot(nx, ny);
      if (Math.max(...pa) <= Math.min(...pb) + 0.01 * len || Math.max(...pb) <= Math.min(...pa) + 0.01 * len) return false;
    }
    return true;
  }
  async function capture(name, meta) {
    const out = { name, meta, when: new Date().toISOString(), printer: JSON.parse(localStorage.getItem('vpp.printer') || 'null'),
      towers: JSON.parse(localStorage.getItem('vpp.towers') || '[]'), printSkip: JSON.parse(localStorage.getItem('vpp.printSkip') || '[]') };
    // Design: the stack panel's alerts for the shown stack
    await stackPanel();
    out.stackAlerts = $$('#dInsp .ialerts .issue').map(txt);
    out.stackCard = $$('[data-stack]').map(txt);
    // Every level's own list, by picking each module in the side list
    out.levels = [];
    for (const nm of units()) {
      if (/roof|base/i.test(nm)) continue;
      try { await pickUnit(nm); } catch (e) { out.levels.push({ unit: nm, error: String(e) }); continue; }
      const ins = document.querySelector('#dInsp');
      out.levels.push({ unit: nm, head: txt(ins.querySelector('.ihead')), alerts: $$('.alert', ins).map(txt),
        parts: $$('.ilist li', ins).map(li => ({ q: parseInt(txt(li.querySelector('.q'))), label: txt(li.querySelector('.n')), file: li.querySelector('.n').title, bad: !!li.querySelector('.badge.no') })) });
    }
    // Print
    await tab(2);
    const V = document.getElementById('view-print');
    out.scope = $$('[data-pskip]', V).map(b => ({ label: txt(b), on: b.getAttribute('aria-pressed') === 'true' }));
    out.top = txt(V.querySelector('.ptop-prog'));
    out.alerts = $$('.alert', V).map(txt);
    const det = V.querySelector('details.fold'); if (det) det.open = true;
    out.parts = $$('details.fold .row', V).map(r => ({ q: parseInt(txt(r.querySelector('.qty'))), label: txt(r.querySelector('.pname')), file: r.querySelector('.pfile').title,
      tags: $$('.tags > *', r).map(txt), dims: txt(r.querySelector('.dimtxt')), bed: (r.querySelector('.bedcell rect:last-child') || { getAttribute: () => '' }).getAttribute('stroke') }));
    out.groups = $$('details.fold .group h3', V).map(txt);
    // Plates: pick each one and read its list and layout
    const nums = $$('[data-pick]', V).map(b => +b.dataset.pick);
    out.plates = [];
    for (const n of nums) {
      await c(`#view-print [data-pick="${n}"]`);
      const P = document.querySelector('#view-print .psel');
      const svg = P.querySelector('svg.platesvg'), vb = svg.getAttribute('viewBox').split(' ').map(Number), W = vb[2] - 4, H = vb[3] - 38;
      const rects = $$('rect', svg).filter(r => !r.closest('pattern') && r.getAttribute('fill') !== 'none' && !(r.getAttribute('fill') || '').startsWith('url(') && r.getAttribute('fill') !== 'var(--bed)');
      const zone = $$('rect', svg).filter(r => (r.getAttribute('fill') || '').startsWith('url(')).map(corners);
      const quads = rects.map(corners);
      const out_of_bed = quads.map((q, i) => q.some(([x, y]) => x < -0.5 || y < -0.5 || x > W + 0.5 || y > H + 0.5) ? i : -1).filter(i => i >= 0);
      const in_noprint = quads.map((q, i) => zone.some(z => overlap(q, z)) ? i : -1).filter(i => i >= 0);
      const clashes = [];
      for (let i = 0; i < quads.length; i++) for (let j = i + 1; j < quads.length; j++) if (overlap(quads[i], quads[j])) clashes.push([i, j]);
      out.plates.push({ n, head: txt(P.querySelector('.psel-head')), tags: txt(P.querySelector('.ptags')), care: txt(P.querySelector('.alert')),
        rows: $$('.plist .prow', P).map(r => ({ count: parseInt(txt(r.querySelector('.q'))), label: txt(r.querySelector('.lbl b')), file: txt(r.querySelector('.lbl small')) })),
        bed: [W, H], shapes: quads.length, out_of_bed, in_noprint, clashes });
    }
    // Hardware tab text (for the record)
    await tab(3); out.hardware = txt(document.getElementById('view-hardware') || document.body).slice(0, 4000);
    await tab(1);
    const r = await fetch('/save?name=' + encodeURIComponent(name + '.json'), { method: 'POST', body: JSON.stringify(out, null, 1) });
    return { saved: r.ok, parts: out.parts.length, plates: out.plates.length, levels: out.levels.length };
  }
  // After a fresh load: the folder, then an empty stack (S3 1F drawer, grid roof)
  async function start() {
    await __fakeVault();
    const b = $$('button').find(x => /Choose your Vault folder/.test(txt(x)));
    if (b) { b.click(); for (let i = 0; i < 40 && !/733/.test(txt(document.body)); i++) await sleep(250); }
    const e = $$('button').find(x => txt(x) === 'Empty stack' || txt(x) === '+ Empty stack' || /Empty stack$/.test(txt(x)));
    if (e) await c(e);
    return { towers: JSON.parse(localStorage.getItem('vpp.towers') || '[]').length, folder: /733/.test(txt(document.querySelector('header') || document.body)) };
  }
  async function footprint(w, d) {
    await stackPanel();
    await c('#dInsp [data-fp]');
    if (w) await c(`[data-fpw="${w}"]`);
    if (d) await c(`[data-fpd="${d}"]`);
  }
  // The level inspector of the top level (Stack settings off)
  async function topLevel() {
    await tab(1);
    const b = document.querySelector('[data-dstack]');
    if (b.getAttribute('aria-pressed') === 'true') await c(b);
  }
  const insp = () => document.querySelector('#dInsp');
  async function printerTo(id) { const s = document.getElementById('printer'); s.value = id; s.dispatchEvent(new Event('change', { bubbles: true })); await sleep(400); return JSON.parse(localStorage.getItem('vpp.printer')); }
  const towersBrief = () => JSON.stringify(JSON.parse(localStorage.getItem('vpp.towers')).map(t => ({ name: t.name, fp: t.fp, st: Object.entries(t.stack).filter(([k, v]) => v).map(([k]) => k).join(','),
    L: t.levels.map(lv => lv.map(u => [u.type, u.w, u.d, u.h + 'F', 'roof=' + u.roof, u.topHandle ? 'topHandle' : '', u.gearedRails ? 'rails' : '', u.lock, u.interior, u.drawers ? 'drawers=' + u.drawers : '', u.backbone !== 'none' ? 'bb=' + u.backbone : '', u.type === 'case' ? 'ci=' + u.caseInterior : ''].filter(Boolean).join(' '))) })));
  Object.assign(window, { printerTo, towersBrief });
  return { start, footprint, topLevel, insp, sleep, c, check, tab, stackPanel, pickUnit, units, capture, txt, $$ };
})();
