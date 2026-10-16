// Print dist/speak-up.html to dist/Impulse_Speak_Up_A2.pdf (A5) and warn about overflowing pages.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const dist = path.resolve(__dirname, '..', 'dist');

(async () => {
  const exe = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  const page = await browser.newPage({ viewport: { width: 560, height: 794 } });
  await page.goto('file://' + path.join(dist, 'speak-up.html'), { waitUntil: 'networkidle' });
  await page.emulateMedia({ media: 'print' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  const overflow = await page.evaluate(() => [...document.querySelectorAll('.page')]
    .map((pg, i) => [i + 1, [pg, ...pg.querySelectorAll('.content, .opener')]
      .filter((el) => el.scrollHeight > el.clientHeight + 1).map((el) => `${el.className} +${el.scrollHeight - el.clientHeight}px`)])
    .filter(([, l]) => l.length).map(([i, l]) => `page ${i}: ${l.join(', ')}`));
  if (overflow.length) console.warn('OVERFLOW\n' + overflow.join('\n'));
  await page.pdf({ path: path.join(dist, 'Impulse_Speak_Up_A2.pdf'), width: '148mm', height: '210mm',
    printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('Done: dist/Impulse_Speak_Up_A2.pdf');
})();
