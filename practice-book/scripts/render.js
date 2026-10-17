// Paginate dist/mock.html into two-column A4 pages and print dist/mock_interior.pdf.
// Each flowing section is broken into atoms (paragraphs, questions, cards, boxes…); atoms fill the columns
// in order, re-creating their wrapper elements (.part, .split …) in every column they continue into.
const fs = require('fs');
const path = require('path');
const { chromium } = require(fs.existsSync('/opt/node22/lib/node_modules/playwright') ? '/opt/node22/lib/node_modules/playwright' : 'playwright');

(async () => {
  const dist = path.join(__dirname, '..', 'dist');
  const startPage = parseInt(process.env.START_PAGE || '1', 10);
  const exe = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  await page.goto('file://' + path.join(dist, 'mock.html'), { waitUntil: 'networkidle', timeout: 120000 });
  await page.emulateMedia({ media: 'print' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);

  const report = await page.evaluate((startPage) => {
    const over = (c) => c.scrollHeight > c.clientHeight + 1;
    const isWrap = (el) => el.classList.contains('split') || el.classList.contains('part');
    const isHead = (el) => /^H[2-5]$/.test(el.tagName) || ['phead', 'ins', 'subt', 'atitle'].some((k) => el.classList.contains(k));
    let sid = 0;

    // flatten: atoms = [{node, path: [wrapperSource…]}]
    function flatten(el, pathArr, out) {
      for (const ch of [...el.children]) {
        if (isWrap(ch) && ch.children.length) {
          ch.dataset.src = ch.dataset.src || 's' + (++sid);
          flatten(ch, [...pathArr, ch], out);
        } else out.push({ node: ch, path: pathArr });
      }
      return out;
    }
    function newPage(after) {
      const nx = document.createElement('section');
      const one = after.querySelector('.cols').classList.contains('one');
      nx.className = 'page flow cont';
      nx.innerHTML = `<div class="cols${one ? ' one' : ''}"><div class="col"></div>${one ? '' : '<div class="col"></div>'}</div>` + after.querySelector('footer').outerHTML;
      after.after(nx);
      return nx;
    }
    // ensure the wrapper chain for `pathArr` exists at the end of `col`; return the innermost wrapper
    function holder(col, chain, pathArr) {
      let parent = col, i = 0;
      while (i < pathArr.length && i < chain.length && chain[i].src === pathArr[i].dataset.src) { parent = chain[i].el; i++; }
      chain.length = i;
      for (; i < pathArr.length; i++) {
        const w = pathArr[i].cloneNode(false);
        if (chain.length || parent !== col || true) {}
        parent.appendChild(w);
        chain.push({ src: pathArr[i].dataset.src, el: w });
        parent = w;
      }
      return parent;
    }
    function prune(el) {      // remove empty wrappers left behind
      for (const w of [...el.querySelectorAll('.split,.part')].reverse()) if (!w.children.length) w.remove();
    }

    const problems = [];
    for (const first of [...document.querySelectorAll('.page.flow')]) {
      const src = first.querySelector('.col');
      const atoms = flatten(src, [], []);
      first.querySelectorAll('.col').forEach((c) => { c.innerHTML = ''; });
      let pg = first, cols = [...pg.querySelectorAll('.col')], ci = 0, col = cols[0], chain = [], placed = [];
      const nextCol = () => {
        ci += 1;
        if (ci >= cols.length) { pg = newPage(pg); cols = [...pg.querySelectorAll('.col')]; ci = 0; }
        col = cols[ci]; chain = []; placed = [];
      };
      let k = 0, guard = 0;
      while (k < atoms.length && guard++ < 20000) {
        const a = atoms[k];
        const h = holder(col, chain, a.path);
        h.appendChild(a.node);
        if (!over(col) || placed.length === 0) {
          if (over(col)) problems.push(`atom too tall on a column: ${a.node.className}`);
          placed.push(k); k++; continue;
        }
        // does not fit: take it out, also pull back trailing headings, then continue in the next column
        a.node.remove();
        let back = k;
        while (placed.length > 1 && isHead(atoms[placed[placed.length - 1]].node)) { atoms[placed.pop()].node.remove(); back--; }
        prune(col);
        k = back;
        nextCol();
      }
    }
    const pages = [...document.querySelectorAll('.page')];
    pages.forEach((p, i) => { const f = p.querySelector('.pno'); if (f) f.textContent = i + startPage; });
    const still = [];
    pages.forEach((p, i) => p.querySelectorAll('.col').forEach((c) => { if (over(c)) still.push(`page ${i + 1}: +${c.scrollHeight - c.clientHeight}px`); }));
    return { pages: pages.length, still, problems };
  }, startPage);
  console.log(`pages: ${report.pages}`);
  if (report.problems.length) console.warn(report.problems.join('\n'));
  if (report.still.length) console.warn('OVERFLOW\n' + report.still.join('\n'));
  await page.pdf({ path: path.join(dist, 'mock_interior.pdf'), width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('Done: dist/mock_interior.pdf');
})();
