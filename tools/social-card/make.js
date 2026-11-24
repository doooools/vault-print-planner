// Makes docs/images/social.png, the link preview card of the live page (og:image, twitter:image), from card.html.
// Run from anywhere: node tools/social-card/make.js (Playwright and its Chromium, as in the cloud sessions).
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('file://' + path.join(__dirname, 'card.html'));
  await p.evaluate(() => Promise.all(['112px Anton', '27px CP', '22px SE'].map(f => document.fonts.load(f))));
  await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(__dirname, '..', '..', 'docs', 'images', 'social.png') });
  await b.close();
})();
