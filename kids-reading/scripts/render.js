// Print dist/read-time.html to dist/Read_Time_1.pdf (A5) and warn about overflowing pages.
const fs = require('fs');
const { chromium } = require(fs.existsSync('/opt/node22/lib/node_modules/playwright') ? '/opt/node22/lib/node_modules/playwright' : 'playwright');
const path = require('path');

const dist = path.resolve(__dirname, '..', 'dist');

(async () => {
  const exe = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  const page = await browser.newPage({ viewport: { width: 560, height: 794 } });
  await page.goto('file://' + path.join(dist, 'read-time.html'), { waitUntil: 'networkidle' });
  await page.emulateMedia({ media: 'print' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  const overflow = await page.evaluate(() => [...document.querySelectorAll('.page')]
    .map((pg, i) => [i + 1, [pg, ...pg.querySelectorAll('.content, .opener')]
      .filter((el) => el.scrollHeight > el.clientHeight + 1).map((el) => `${el.className} +${el.scrollHeight - el.clientHeight}px`)])
    .filter(([, l]) => l.length).map(([i, l]) => `page ${i}: ${l.join(', ')}`));
  if (overflow.length) console.warn('OVERFLOW\n' + overflow.join('\n'));
  await page.pdf({ path: path.join(dist, 'Read_Time_1.pdf'), width: '148mm', height: '210mm',
    printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('Done: dist/Read_Time_1.pdf');
})();
