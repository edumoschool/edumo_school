// Print dist/writing.html (A4, page numbers in the footer) and dist/cover.html (front + back) to PDF.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const dist = path.resolve(__dirname, '..', 'dist');

(async () => {
  const exe = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  for (const [src, out, footer] of [['writing.html', 'interior.pdf', true], ['cover.html', 'cover.pdf', false]]) {
    const page = await browser.newPage();
    await page.goto('file://' + path.join(dist, src), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(400);
    const opts = { path: path.join(dist, out), format: 'A4', printBackground: true, preferCSSPageSize: true };
    if (footer) Object.assign(opts, {
      displayHeaderFooter: true, headerTemplate: '<span></span>',
      footerTemplate: '<div style="width:100%;font-family:Nunito,sans-serif;font-size:8px;color:#6B7690;font-weight:700;display:flex;justify-content:space-between;padding:0 13mm">'
        + '<span>✏️ Write it Right! · Multilevel Writing</span><span style="background:#14215A;color:#fff;border-radius:99px;padding:1px 8px;-webkit-print-color-adjust:exact"><span class="pageNumber"></span></span></div>' });
    await page.pdf(opts);
    await page.close();
  }
  await browser.close();
  console.log('Done: dist/interior.pdf, dist/cover.pdf');
})();
