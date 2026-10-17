// Paginate dist/units.html (move overflowing blocks onto continuation pages) and print it to an A3 PDF.
// Usage: node scripts/render.js [output.pdf]
const path = require('path');
const fs = require('fs');
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }

(async () => {
  const dist = path.join(__dirname, '..', 'dist');
  const out = process.argv[2] || path.join(dist, 'Unlock5_Units_4-10.pdf');
  const exe = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  const page = await browser.newPage({ viewport: { width: 1123, height: 1588 } });
  await page.goto('file://' + path.join(dist, process.env.INPUT || 'units.html'), { waitUntil: 'networkidle', timeout: 120000 });
  await page.emulateMedia({ media: 'print' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);

  const startPage = parseInt(process.env.START_PAGE || '1', 10);
  const report = await page.evaluate((startPage) => {
    const over = (c) => c.scrollHeight > c.clientHeight + 1;
    const movable = (el) => [...el.children].filter((c) => !c.classList.contains('lbl'));
    const splittable = (el) => el.classList.contains('split') || el.classList.contains('blk');
    let uid = 0;
    const key = (el) => el.dataset.key || (el.dataset.key = 'k' + (++uid));

    function moveOne(src, dst) {
      const kids = movable(src);
      const last = kids[kids.length - 1];
      if (!last) return false;
      if (splittable(last) && movable(last).length > 1) {
        let tgt = dst.firstElementChild;
        if (!(tgt && tgt.dataset.key === key(last))) {
          tgt = last.cloneNode(false);
          tgt.classList.add('contd');
          dst.prepend(tgt);
        }
        return moveOne(last, tgt);
      }
      if (kids.length === 1) return false;          // a single unsplittable block that is too tall
      dst.prepend(last);
      return true;
    }

    const problems = [];
    for (let pg of [...document.querySelectorAll('.page')]) {
      let guard = 0;
      while (pg) {
        const c = pg.querySelector('.content');
        if (!c || !over(c)) break;
        const side = pg.classList.contains('sl') ? 'sr' : 'sl';
        const nx = document.createElement('section');
        nx.className = `page ${side} cont ${[...pg.classList].filter((k) => !['page', 'sl', 'sr', 'hastab', 'cont'].includes(k)).join(' ')}`;
        nx.innerHTML = '<div class="strip"></div><div class="content"></div><footer class="pno"></footer>';
        pg.after(nx);
        const nc = nx.querySelector('.content');
        while (over(c) && guard++ < 2000) if (!moveOne(c, nc)) { problems.push(c.closest('.page')); break; }
        // don't leave a heading alone at the bottom of a page
        let tail = movable(c).pop();
        while (tail && /^H[2-5]$/.test(tail.tagName)) { nc.prepend(tail); tail = movable(c).pop(); }
        pg = nx;
      }
    }
    const pages = [...document.querySelectorAll('.page')];
    pages.forEach((p, i) => { const f = p.querySelector('.pno'); if (f) f.textContent = i + startPage; });
    const still = pages.map((p, i) => [i + 1, p.querySelector('.content')])
      .filter(([, c]) => c && over(c)).map(([i, c]) => `page ${i}: +${c.scrollHeight - c.clientHeight}px`);
    return { pages: pages.length, still };
  }, startPage);
  console.log(`pages: ${report.pages}`);
  if (report.still.length) console.warn('OVERFLOW\n' + report.still.join('\n'));
    await page.pdf({ path: out, width: '297mm', height: '420mm', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('Done: ' + path.relative(process.cwd(), out));
})();
