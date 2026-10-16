// Render dist/front.html and dist/body.html to PDF and merge them.
// Usage: node render.js            -> dist/body.pdf, dist/front.pdf, unit page map
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const dist = path.resolve(__dirname, '..', 'dist');

(async () => {
  const exe = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  const page = await browser.newPage();
  const hf = JSON.parse(fs.readFileSync(path.join(dist, 'header_footer.json'), 'utf8'));

  await page.goto('file://' + path.join(dist, 'body.html'), { waitUntil: 'networkidle' });
  await page.pdf({
    path: path.join(dist, 'body.pdf'), format: 'A4', landscape: true, printBackground: true,
    displayHeaderFooter: true, headerTemplate: hf.header, footerTemplate: hf.footer,
    preferCSSPageSize: true,
  });

  await page.goto('file://' + path.join(dist, 'front.html'), { waitUntil: 'networkidle' });
  await page.pdf({ path: path.join(dist, 'front.pdf'), format: 'A4', landscape: true,
    printBackground: true, preferCSSPageSize: true });
  await browser.close();

  // Find the first page of each unit in body.pdf (the unit banner text starts with "<n> <title>").
  const n = parseInt(execFileSync('pdfinfo', [path.join(dist, 'body.pdf')]).toString()
    .match(/Pages:\s+(\d+)/)[1], 10);
  const titles = JSON.parse(fs.readFileSync(path.join(dist, 'unit_titles.json'), 'utf8'));
  const pages = {};
  for (let p = 1; p <= n; p++) {
    const txt = execFileSync('pdftotext', ['-f', p, '-l', p, '-raw',
      path.join(dist, 'body.pdf'), '-']).toString();
    for (const [u, t] of Object.entries(titles)) {
      if (!pages[u] && txt.replace(/ /g, '').split('\n').some((l) => l.startsWith(`${u}${t.replace(/ /g, '')}`))) pages[u] = p;
    }
  }
  fs.writeFileSync(path.join(dist, 'pages.json'), JSON.stringify(pages));
  console.log('body pages', n, pages);
})();
