// Print the cover HTML files to PDF: dist/Cover_front_back.pdf (2 A3 pages) and dist/Cover_spread.pdf (print spread).
const path = require('path');
const fs = require('fs');
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }

(async () => {
  const dist = path.join(__dirname, '..', 'dist');
  const exe = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  for (const [src, out] of [['cover_pages.html', 'Cover_front_back.pdf'], ['cover_spread.html', 'Cover_spread.pdf']]) {
    const page = await browser.newPage();
    await page.goto('file://' + path.join(dist, src), { waitUntil: 'networkidle', timeout: 120000 });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(400);
    await page.pdf({ path: path.join(dist, out), printBackground: true, preferCSSPageSize: true });
    console.log('Done: dist/' + out);
  }
  await browser.close();
})();
