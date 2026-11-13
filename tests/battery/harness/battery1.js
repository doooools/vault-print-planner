// Battery 1 recipes, the same clicks as the first run (printer per id in PRINTER)
window.B1 = (() => {
  const c = T.c, chk = T.check;
  const noRails = () => c('[data-ubool="gearedRails=0"]');
  const lv = async () => T.topLevel();
  const h = async n => { await lv(); await c(`[data-useg="h=${n}"]`); };
  const topHandle = async on => { await T.stackPanel(); if (document.querySelector('[data-sbool^="topHandle="]')) await c(`[data-sbool="topHandle=${on ? 1 : 0}"]`); };
  const st = async (k, on) => { await T.stackPanel(); await c(`[data-sbool="${k}=${on ? 1 : 0}"]`); };
  const roof = async r => { await T.stackPanel(); await c(`[data-roof="${r}"]`); };
  const addTop = async () => { await T.tab(1); await c('[data-addtop]'); await lv(); };
  const C01 = async () => { await T.footprint('S', 4); await lv(); await noRails(); await topHandle(false); };
  const C07 = async () => { await T.footprint('M', 5); await lv(); await c('[data-useg="type=case"]'); await h(2); await topHandle(false); };
  const R = {
    C01, C07,
    C02: async () => { await T.footprint('M', 4); await h(2); await noRails(); await topHandle(true); },
    C03: async () => { await T.footprint('L', 5); await h(4); await c('[data-lay="2,1,1"]'); await topHandle(false); },
    C04: async () => { await T.footprint('S', 4); await h(4); await c('[data-lay="1,1,1,1"]'); await topHandle(false); },
    C05: async () => { await T.footprint('S', 3); await h(2); await c('[data-lay="1,1"]'); await c('[data-useg="lock=hidden"]'); await c('[data-useg="interior=gridfinity"]'); await topHandle(false); },
    C06: async () => { await T.footprint('S', 4); await lv(); await c('[data-useg="type=case"]'); await h(1); await topHandle(false); },
    C08: async () => { await T.footprint('S', 4); await lv(); await noRails(); await addTop(); await h(2); await addTop(); await c('[data-useg="type=case"]'); await h(1); await topHandle(false); },
    C09: async () => { await T.footprint('L', 4); await lv(); await c('[data-across="SS"]'); await lv(); for (const j of [0, 1]) { await c(`[data-umod="${j}"]`); await noRails(); } await topHandle(false); },
    C10: async () => { await T.footprint('M', 4); await h(2); await noRails(); await st('base', true); await st('wheels', true); await st('feet', true); await st('stationaryHandle', true); await st('pullHandle', true); await topHandle(false); },
    C11: async () => { await T.footprint('S', 4); await lv(); await noRails(); await st('base', true); await st('casters', true); await topHandle(false); },
    C12: async () => { await T.footprint('XL', 3); await lv(); await noRails(); await roof('heavycut'); },
    C13: async () => { await T.footprint('L', 4); await lv(); await c('[data-across="L2"]'); await lv(); await noRails(); await roof('table'); },
    C14: async () => { await C01(); await T.c('#dNew'); await T.sleep(400); await C07(); },
    X1_L5_4F_112: async () => { await T.footprint('L', 5); await h(4); await c('[data-lay="1,1,2"]'); await topHandle(false); },
    X2_S4_2x1F: async () => { await C01(); await addTop(); },
  };
  const PRINTER = { C03: 'h2s', C09: 'h2s', C12: 'h2s', C13: 'h2s', X1_L5_4F_112: 'h2s' };
  async function run(id) {
    await T.start(); await R[id](); await T.sleep(1500);
    const brief = towersBrief();
    const cap = await T.capture(id, { cfg: id, printer: PRINTER[id] || 'p1s', towers: brief, rerun: 'after fix' });
    return { id, brief, cap };
  }
  return { R, run, PRINTER };
})();
