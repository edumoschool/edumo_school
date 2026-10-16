// Print dist/<level>-writing-book.html to dist/Impulse_<LEVEL>_Writing_Book.pdf and warn about overflowing pages.
// Usage: node render.js [A2|B1]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const dist = path.resolve(__dirname, '..', 'dist');
const level = (process.argv[2] || 'A2').toUpperCase();
const pdfName = `Impulse_${level}_Writing_Book.pdf`;

(async () => {
  const exe = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  const page = await browser.newPage({ viewport: { width: 1123, height: 794 } });
  await page.goto('file://' + path.join(dist, `${level.toLowerCase()}-writing-book.html`), { waitUntil: 'networkidle' });
  await page.emulateMedia({ media: 'print' });
  const overflow = await page.evaluate(() => [...document.querySelectorAll('.page')]
    .map((pg, i) => [i + 1, [...pg.querySelectorAll('.content, .inner, .lesson, .tleft, .tgrid')]
      .filter((el) => el.scrollHeight > el.clientHeight + 1).map((el) => `${el.className} +${el.scrollHeight - el.clientHeight}px`)])
    .filter(([, list]) => list.length).map(([i, list]) => `page ${i}: ${list.join(', ')}`));
  if (overflow.length) console.warn('OVERFLOW\n' + overflow.join('\n'));
  await page.pdf({ path: path.join(dist, pdfName), width: '297mm', height: '210mm',
    printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log(`Done: dist/${pdfName}`);
})();
