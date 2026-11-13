// Battery 2 recipes (H2S): each builds one configuration through the page's controls, from a fresh start()
window.B2 = (() => {
  const c = T.c, chk = T.check;
  const noRails = () => c('[data-ubool="gearedRails=0"]');
  const roof = async r => { await T.stackPanel(); await c(`[data-roof="${r}"]`); };
  const topHandle = async on => { await T.stackPanel(); if (document.querySelector('[data-sbool^="topHandle="]')) await c(`[data-sbool="topHandle=${on ? 1 : 0}"]`); };
  const st = async (k, on) => { await T.stackPanel(); await c(`[data-sbool="${k}=${on ? 1 : 0}"]`); };
  const lv = async () => T.topLevel();
  const h = async n => { await lv(); await c(`[data-useg="h=${n}"]`); };
  const lay = async l => { await lv(); await c(`[data-lay="${l}"]`); };
  const type = async t => { await lv(); await c(`[data-useg="type=${t}"]`); };
  const sel = async (k, v) => { await lv(); await c(`[data-useg="${k}=${v}"]`); };
  const addTop = async () => { await T.tab(1); await c('[data-addtop]'); await lv(); };
  const step = async (k, n) => { await lv(); for (let i = 0; i < Math.abs(n); i++) await c(`[data-ustep="${k}"][data-d="${n > 0 ? 1 : -1}"]`); };
  const across = async v => { await lv(); await c(`[data-across="${v}"]`); };
  const mods = async fn => { await lv(); const n = T.$$('[data-umod]').length || 1; for (let j = 0; j < n; j++) { if (n > 1) await c(`[data-umod="${j}"]`); await fn(); } };
  const R = {
    D01: async () => { await T.footprint('S', 3); await h(2); await noRails(); await topHandle(false); },
    D02: async () => { await T.footprint('S', 5); await h(4); await noRails(); await roof('table'); },
    D03: async () => { await T.footprint('M', 3); await lv(); await noRails(); await roof('bowl'); },
    D04: async () => { await T.footprint('M', 6); await h(2); await lay('1,1'); await c('[data-useg="lock=hidden"]'); await topHandle(true); },
    D05: async () => { await T.footprint('M', 7); await h(4); await lay('2,2'); await roof('undertable'); },
    D06: async () => { await T.footprint('L', 3); await lv(); await noRails(); await roof('heavy'); },
    D07: async () => { await T.footprint('L', 6); await h(2); await lay('1,1'); await topHandle(false); },
    D08: async () => { await T.footprint('L', 7); await h(4); await lay('1,2,1'); await c('[data-useg="interior=gridfinity"]'); await topHandle(false); },
    D09: async () => { await T.footprint('XL', 5); await lv(); await noRails(); await roof('table'); },
    D10: async () => { await T.footprint('XL', 6); await lv(); await noRails(); await topHandle(false); },
    D11: async () => { await T.footprint('XL', 4); await across('XL2'); await lv(); await noRails(); await topHandle(false); },
    D12: async () => { await T.footprint('L', 5); await across('L2'); await h(2); await noRails(); await roof('bowl'); },
    D13: async () => { await T.footprint('L', 4); await type('case'); await h(1); await sel('caseInterior', 'flat'); await topHandle(false); },
    D14: async () => { await T.footprint('L', 5); await type('case'); await h(2); await sel('caseInterior', 'dividers'); await roof('table'); },
    D15: async () => { await T.footprint('XL', 3); await type('case'); await h(1); await sel('caseInterior', 'sealed'); await topHandle(false); },
    D16: async () => { await T.footprint('M', 6); await type('case'); await h(2); await topHandle(false); },
    D17: async () => { await T.footprint('S', 4); await type('case'); await h(4); await topHandle(false); },
    D18: async () => { await T.footprint('XL', 4); await h(2); await across('SM'); await mods(noRails); await topHandle(false); },
    D19: async () => { await T.footprint('L', 5); await h(2); await noRails(); await addTop(); await h(1); await addTop(); await type('case'); await h(1); await sel('caseInterior', 'flat');
      await st('base', true); await st('wheels', true); await st('feet', true); await st('pullHandle', true); await roof('table'); },
    D20: async () => { await T.footprint('XL', 3); await lv(); await noRails(); await addTop(); await st('base', true); await st('casters', true); await topHandle(false); },
    D21: async () => { for (let s = 0; s < 2; s++) { if (s) { await T.c('#dNew'); await T.sleep(400); } await T.footprint('M', 4); await h(1); await noRails(); await c('[data-useg="lock=hidden"]'); await addTop(); await addTop(); await topHandle(false); } },
    D22: async () => { await T.footprint('S', 4); await lv(); await noRails(); await c('[data-useg="interior=grid"]'); const a = +T.txt(document.querySelector('[data-ustep="gridAcross"]').parentElement.querySelector('output')); await step('gridAcross', 2 - a);
      const b = +T.txt(document.querySelector('[data-ustep="gridAlong"]').parentElement.querySelector('output')); await step('gridAlong', 1 - b); await sel('gridHeight', '20'); await sel('gridEdge', 'straight'); await topHandle(false); },
    D23: async () => { await T.footprint('S', 4); await h(2); await noRails(); await c('[data-useg="interior=gridfinity"]'); await sel('baseplateHandles', '2'); await topHandle(false); },
    D24: async () => { await T.footprint('M', 5); await lv(); await noRails(); await c('[data-ubool="wallMount=1"]'); await topHandle(false); },
    D25: async () => { await T.footprint('S', 3); await lv(); await noRails(); await sel('pegboard', 'ikea'); await topHandle(false); },
    D26: async () => { await T.footprint('S', 3); await type('case'); await h(2); await chk('[data-ucheck=caseBaseplate]', true); await step('dv_plain', 3); await topHandle(false); },
    D27: async () => { await T.footprint('S', 6); await h(2); await noRails(); await addTop(); await h(1); await st('base', true); await st('wheels', false); await st('stationaryHandle', true); await topHandle(false); },
    D28: async () => { await T.footprint('L', 6); await type('case'); await h(1); await sel('caseInterior', 'flat'); await topHandle(false); },
  };
  async function run(id) {
    await T.start(); await R[id](); await T.sleep(1500);
    const brief = towersBrief();
    const cap = await T.capture(id, { cfg: id, printer: 'h2s', towers: brief });
    return { id, brief, cap, alerts: T.$$('#dInsp .issue').map(T.txt) };
  }
  return { R, run };
})();
