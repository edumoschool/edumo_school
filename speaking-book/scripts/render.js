// Print dist/speaking-book.html to dist/Impulse_A1_Speaking_Book.pdf and warn about overflowing pages.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const dist = path.resolve(__dirname, '..', 'dist');

(async () => {
  const exe = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  const page = await browser.newPage({ viewport: { width: 1123, height: 794 } });
  await page.goto('file://' + path.join(dist, 'speaking-book.html'), { waitUntil: 'networkidle' });
  await page.emulateMedia({ media: 'print' });
  const overflow = await page.evaluate(() => [...document.querySelectorAll('.lesson, .review, .content, .inner')]
    .filter((el) => el.scrollHeight > el.clientHeight + 1)
    .map((el) => `${el.className}: ${el.scrollHeight - el.clientHeight}px (${el.querySelector('small')?.textContent || ''})`));
  if (overflow.length) console.warn('OVERFLOW\n' + overflow.join('\n'));
  await page.pdf({ path: path.join(dist, 'Impulse_A1_Speaking_Book.pdf'), width: '297mm', height: '210mm',
    printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('Done: dist/Impulse_A1_Speaking_Book.pdf');
})();
