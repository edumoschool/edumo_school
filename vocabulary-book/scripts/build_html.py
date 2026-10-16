"""Build the Impulse Learning Center A1 vocabulary book as HTML.

Produces two documents in dist/:
  front.html  – cover, how-to-use page and contents (no running header)
  body.html   – unit-by-unit vocabulary tables (rendered with header/footer)

Usage: python3 build_html.py [pages.json]
pages.json (optional) maps unit number -> first page in body.pdf; it is
written by render.js after a first pass so the contents page can show
real page numbers.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "navigate-a1-words.json").read_text(encoding="utf-8"))
DIST = ROOT / "dist"
PAGES = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 else {}

SCHOOL = "Impulse Learning Center"
TITLE = "A1 Vocabulary Book"

UNIT_TOPICS = {
    "1": ("Hello!", "Greetings, names, numbers 1–10 and countries"),
    "2": ("People and places", "Jobs, objects, places in town and numbers 11–100"),
    "3": ("Family and friends", "Family, possessions and describing people"),
    "4": ("Daily life", "Routines, transport, free time and days of the week"),
    "5": ("Clothes and colours", "Clothes, the body, colours and frequency"),
    "6": ("Places to stay", "Hotels, homes, rooms and facilities"),
    "7": ("Abilities and free time", "Skills, hobbies and animals"),
    "8": ("Famous lives", "People from history, ordinal numbers and months"),
    "9": ("Life stories", "Past events, the weather and seasons"),
    "10": ("Food and future plans", "Food, drink and plans for the future"),
}

GROUPS = [
    ("Nouns", {"n", "n pl"}),
    ("Verbs", {"v"}),
    ("Phrasal verbs", {"phr v"}),
    ("Adjectives", {"adj"}),
    ("Adverbs", {"adv"}),
    ("Phrases and expressions", {"phr"}),
    ("Exclamations", {"exclamation"}),
    ("Function words", {"prep", "conj", "pron", "pron, pl", "det", ""}),
]
POS_LABEL = {
    "n": "n", "n pl": "n pl", "v": "v", "phr v": "phr v", "adj": "adj", "adv": "adv",
    "phr": "phr", "exclamation": "excl", "prep": "prep", "conj": "conj", "pron": "pron",
    "pron, pl": "pron pl", "det": "det", "": "",
}
THEME_ICONS = {
    "Countries": "globe", "Numbers 1–10": "hash", "Numbers 11–100": "hash",
    "Days of the week": "calendar", "Months": "calendar", "Ordinal numbers": "hash",
}

e = html.escape


def logo_svg(size=48, light=False):
    """Impulse Learning Center logo: white open book with a flame on a blue circle.

    `light` adds a thin white ring so the logo stands out on blue backgrounds.
    """
    ring = '<circle cx="320" cy="320" r="304" fill="none" stroke="#fff" stroke-width="32"/>' if light else ""
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 640 640" aria-hidden="true">
<circle cx="320" cy="320" r="320" fill="#0057FF"/>{ring}
<g transform="translate(0 14)"><g fill="none" stroke="#fff" stroke-width="22">
<path d="M320 140 C348 168 352 220 320 250 C288 220 292 168 320 140 Z"/>
<path d="M203 241 C248 233 290 247 320 280 C350 247 392 233 437 241 V407 C392 404 350 420 320 456 C290 420 248 404 203 407 Z"/>
</g><path d="M309 280 H331 V364 L320 354 L309 364 Z" fill="#fff"/></g>
</svg>"""


ICONS = {
    "Nouns": "M4 6h16M4 12h16M4 18h10",
    "Verbs": "M5 12h12M13 6l6 6-6 6",
    "Phrasal verbs": "M5 12h12M13 6l6 6-6 6",
    "Adjectives": "M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.6 6.6 19.5l1.2-6L3.3 9.3l6.1-.7z",
    "Adverbs": "M4 17l5-5 4 4 7-8",
    "Phrases and expressions": "M4 5h16v10H9l-5 4z",
    "Exclamations": "M12 4v10M12 19v.5",
    "Function words": "M8 4H5v16h3M16 4h3v16h-3",
    "globe": "M12 3a9 9 0 100 18 9 9 0 000-18zM3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18",
    "hash": "M9 4L7 20M17 4l-2 16M4 9h16M3 15h16",
    "calendar": "M4 6h16v14H4zM4 10h16M8 3v5M16 3v5",
}


def icon(name):
    return (f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="{ICONS[name]}" '
            'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
            'stroke-linejoin="round"/></svg>')


def highlight(example, word):
    """Bold the headword (or a simple inflection of it) inside the example."""
    ex = e(example)
    base = re.sub(r"\s*\(.*?\)", "", word).strip()
    candidates = []
    for part in [base] + [p.strip() for p in re.split(r"[,/]", base)]:
        if part and part not in candidates:
            candidates.append(part)
    if base.lower().startswith(("a ", "an ", "the ")) and len(base.split()) > 1:
        candidates.append(base.split(" ", 1)[1])
    for c in sorted(candidates, key=len, reverse=True):
        stem = re.escape(e(c)).replace(r"\ ", r"\s+")
        if len(c) > 3 and c[-1] == "e":
            stem = re.escape(e(c[:-1])) + "e?"
        pat = re.compile(r"(?<![\w’])(" + stem + r"(?:s|es|d|ed|ing|’s)?)(?![\w])", re.I)
        new, n = pat.subn(r"<b>\1</b>", ex, count=1)
        if n:
            return new
    return ex


def group_words(words):
    groups = []
    themed = {}
    for w in words:
        if w["section"]:
            themed.setdefault(w["section"], []).append(w)
    plain = [w for w in words if not w["section"]]
    for name, poses in GROUPS:
        items = [w for w in plain if w["pos"] in poses]
        if items:
            groups.append((name, name, sorted(items, key=lambda w: w["word"].lower())))
    for name, items in themed.items():
        groups.append((name, THEME_ICONS.get(name, "hash"), items))
    return groups


def unit_table(u, words):
    rows = []
    n = 0
    for name, ico, items in group_words(words):
        rows.append(f'<tr class="grp"><td colspan="7">{icon(ico)}<span>{e(name)}</span>'
                    f'<em>{len(items)} words</em></td></tr>')
        for w in items:
            n += 1
            rows.append(word_row(n, w))
    return "\n".join(rows)


def word_row(n, w):
    pos = POS_LABEL.get(w["pos"], w["pos"])
    ex = highlight(w["ex"], w["word"]) if w["ex"] else '<span class="muted">—</span>'
    return ("<tr>"
            f'<td class="num">{n}</td>'
            f'<td class="word"><strong>{e(w["word"])}</strong>'
            f'{f" <i>{e(pos)}</i>" if pos else ""}</td>'
            f'<td class="ipa">{e(w["ipa"])}</td>'
            f'<td class="def">{e(w["def"])}</td>'
            f'<td class="ex">{ex}</td>'
            f'<td class="ru">{e(w["ru"])}</td>'
            f'<td class="uz">{e(w["uz"])}</td>'
            "</tr>")


def unit_section(u, words):
    title, sub = UNIT_TOPICS[u]
    return f"""
<section class="unit" id="unit-{u}">
  <header class="unit-head">
    <div class="unit-no"><small>UNIT</small><span>{u}</span></div>
    <div class="unit-title"><h1>{e(title)}</h1><p>{e(sub)}</p></div>
    <div class="unit-stats"><div class="total"><b>{len(words)}</b><small>words</small></div></div>
  </header>
  <table class="vocab">
    <colgroup><col class="w-num"><col class="w-word"><col class="w-ipa">
      <col class="w-def"><col class="w-ex"><col class="w-ru"><col class="w-uz"></colgroup>
    <thead><tr><th>№</th><th>WORDS</th><th>TRANSCRIPTION</th><th>DEFINITION</th>
      <th>EXAMPLE</th><th>RUSSIAN</th><th>UZBEK</th></tr></thead>
    <tbody>
{unit_table(u, words)}
    </tbody>
  </table>
</section>"""


CSS = """
:root{--blue:#1E90FF;--blue-d:#0B63CE;--navy:#0A2A5E;--tint:#EAF4FF;--tint2:#F5FAFF;
 --line:#CFE3FB;--ink:#14213D;--muted:#6B7A90;}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:Inter,"DejaVu Sans",sans-serif;color:var(--ink);font-size:8.4pt;line-height:1.32;background:#fff}
.ico{width:12px;height:12px;flex:none}
.muted{color:var(--muted)}
table.vocab{width:100%;border-collapse:separate;border-spacing:0;table-layout:fixed;border:1px solid var(--line);border-radius:8px}
col.w-num{width:3%}col.w-word{width:15%}col.w-ipa{width:11%}
col.w-def{width:21%}col.w-ex{width:24.5%}col.w-ru{width:12.7%}col.w-uz{width:12.8%}
thead{display:table-header-group}
thead th{background:var(--blue);color:#fff;font-size:7.3pt;font-weight:700;letter-spacing:.06em;
 padding:5px 6px;text-align:left;border-right:1px solid rgba(255,255,255,.25)}
thead th:first-child{text-align:center}
thead th:last-child{border-right:0}
tr{break-inside:avoid}
td{padding:3.6px 6px;border-top:1px solid var(--line);border-right:1px solid var(--line);vertical-align:top}
td:last-child{border-right:0}
tbody tr:nth-child(even):not(.grp) td{background:var(--tint2)}
tr.grp td{background:var(--tint);color:var(--blue-d);font-weight:800;font-size:8.6pt;padding:4px 8px;
 border-top:1.5px solid var(--blue)}
tr.grp td{break-after:avoid}
tr.grp td>*{vertical-align:middle}
tr.grp .ico{width:13px;height:13px;margin-right:6px;position:relative;top:-1px}
tr.grp em{font-style:normal;font-weight:600;color:var(--muted);font-size:7.4pt;margin-left:8px}
td.num{text-align:center;color:var(--muted);font-size:7.4pt;font-variant-numeric:tabular-nums}
td.word strong{color:var(--navy);font-weight:700;font-size:8.8pt}
td.word i{color:var(--blue);font-style:italic;font-size:7.6pt;font-weight:600}
td.ipa{font-family:"DejaVu Sans",sans-serif;color:#33476B;font-size:7.9pt}
td.ex b{color:var(--blue-d);font-weight:700}
td.ru,td.uz{color:#1F2D4A}
"""

BODY_CSS = CSS + """
@page{size:A4 landscape;margin:17mm 10mm 13mm 10mm}
.unit{break-before:page}
.unit:first-child{break-before:auto}
.unit-head{display:flex;align-items:stretch;gap:0;border-radius:10px;overflow:hidden;margin-bottom:9px;
 background:linear-gradient(100deg,var(--navy) 0%,var(--blue-d) 45%,var(--blue) 100%);color:#fff}
.unit-no{background:rgba(255,255,255,.12);padding:8px 18px;display:flex;flex-direction:column;
 align-items:center;justify-content:center;min-width:78px}
.unit-no small{font-size:7pt;letter-spacing:.25em;font-weight:600;opacity:.85}
.unit-no span{font-size:28pt;font-weight:800;line-height:1}
.unit-title{flex:1;padding:10px 18px;display:flex;flex-direction:column;justify-content:center}
.unit-title h1{font-family:"Inter Display",Inter,sans-serif;font-size:19pt;font-weight:800;letter-spacing:-.01em}
.unit-title p{font-size:8.6pt;opacity:.88;margin-top:2px}
.unit-stats{display:flex;align-items:center;gap:12px;padding:8px 16px}
.unit-stats .total{text-align:center;line-height:1}
.unit-stats .total b{display:block;font-size:20pt;font-weight:800}
.unit-stats .total small{font-size:7pt;letter-spacing:.12em;text-transform:uppercase;opacity:.85}

"""

FRONT_CSS = CSS + """
@page{size:A4 landscape;margin:0}
.page{width:297mm;height:210mm;position:relative;overflow:hidden;break-after:page}
.page:last-child{break-after:auto}
/* cover */
.cover{background:radial-gradient(120% 140% at 85% 10%,#3DA5FF 0%,var(--blue) 30%,var(--blue-d) 62%,var(--navy) 100%);color:#fff}
.cover .grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.06) 1px,transparent 1px),
 linear-gradient(90deg,rgba(255,255,255,.06) 1px,transparent 1px);background-size:12mm 12mm}
.cover .blob{position:absolute;border-radius:50%;background:rgba(255,255,255,.08)}
.cover .b1{width:150mm;height:150mm;right:-40mm;top:-50mm}
.cover .b2{width:90mm;height:90mm;right:40mm;bottom:-45mm;background:rgba(255,255,255,.06)}
.cover .brand{position:absolute;left:20mm;top:18mm;display:flex;align-items:center;gap:12px}
.cover .brand b{display:block;font-size:15pt;font-weight:800;letter-spacing:.04em}
.cover .brand small{display:block;font-size:8pt;letter-spacing:.32em;opacity:.85;font-weight:600}
.cover .main{position:absolute;left:20mm;top:58mm;width:170mm}
.cover .kicker{display:inline-block;background:#fff;color:var(--blue-d);font-weight:800;font-size:9pt;
 letter-spacing:.18em;padding:5px 12px;border-radius:999px}
.cover h1{font-family:"Inter Display",Inter,sans-serif;font-size:50pt;line-height:.98;font-weight:900;letter-spacing:-.02em;margin-top:12px}
.cover h1 span{color:#BFE0FF}
.cover .lead{font-size:12pt;margin-top:12px;opacity:.92;max-width:150mm}
.cover .feat{display:flex;gap:8px;margin-top:16px;flex-wrap:wrap}
.cover .feat span{border:1px solid rgba(255,255,255,.45);border-radius:6px;padding:4px 9px;font-size:8.4pt;font-weight:600}
.cover .card{position:absolute;right:20mm;top:60mm;width:86mm;background:#fff;color:var(--ink);border-radius:14px;
 box-shadow:0 18px 40px rgba(6,26,64,.35);overflow:hidden}
.cover .card .top{background:var(--tint);padding:10px 14px;display:flex;justify-content:space-between;align-items:center}
.cover .card .top b{color:var(--blue-d);font-size:8pt;letter-spacing:.14em}
.cover .card .body{padding:12px 14px 14px}
.cover .card .w{font-size:22pt;font-weight:800;color:var(--navy)}
.cover .card .w i{font-size:10pt;color:var(--blue);font-weight:600}
.cover .card .ipa{font-family:"DejaVu Sans",sans-serif;color:#33476B;font-size:10pt;margin:2px 0 8px}
.cover .card .row{display:flex;gap:8px;padding:6px 0;border-top:1px solid var(--line);font-size:8.6pt}
.cover .card .row small{width:20mm;flex:none;color:var(--muted);font-weight:700;font-size:7pt;letter-spacing:.1em;padding-top:1px}
.cover .card .row b{color:var(--blue-d)}
.cover .foot{position:absolute;left:20mm;right:20mm;bottom:14mm;display:flex;justify-content:space-between;
 align-items:flex-end;font-size:8.6pt;opacity:.9;border-top:1px solid rgba(255,255,255,.3);padding-top:8px}
.cover .units{display:flex;gap:5px}
.cover .units span{width:7mm;height:7mm;border-radius:5px;background:rgba(255,255,255,.16);display:flex;
 align-items:center;justify-content:center;font-weight:800;font-size:8pt}
/* inner pages */
.inner{padding:14mm 16mm 20mm;height:100%;display:flex;flex-direction:column}
.ptitle{display:flex;align-items:center;gap:10px;margin-bottom:8mm}
.ptitle h2{font-family:"Inter Display",Inter,sans-serif;font-size:22pt;font-weight:900;color:var(--navy);letter-spacing:-.01em}
.ptitle .bar{flex:1;height:3px;background:linear-gradient(90deg,var(--blue),transparent);border-radius:2px}
.ptitle small{color:var(--blue);font-weight:800;letter-spacing:.2em;font-size:8pt}
.cols{display:grid;grid-template-columns:1.25fr 1fr;gap:8mm}
.box{border:1px solid var(--line);border-radius:12px;padding:10px 14px;background:#fff}
.box h3{font-size:10pt;color:var(--blue-d);font-weight:800;letter-spacing:.06em;text-transform:uppercase;margin-bottom:8px}
.anat{width:100%;border-collapse:collapse;font-size:9pt}
.anat td{padding:8px 6px;border-top:1px solid var(--line);vertical-align:top}
.anat td:first-child{width:30mm;font-weight:800;color:var(--navy)}
.anat tr:first-child td{border-top:0}
.abbr{display:grid;grid-template-columns:repeat(3,1fr);gap:6px 10px;font-size:9pt}
.abbr b{color:var(--blue);display:inline-block;min-width:13mm}
.tips{list-style:none;font-size:9pt}
.tips li{padding:6px 0 6px 18px;position:relative}
.tips li:before{content:"";position:absolute;left:2px;top:8px;width:8px;height:8px;border-radius:2px;background:var(--blue)}
.stack{display:flex;flex-direction:column;gap:6mm}
.toc{display:grid;grid-template-columns:repeat(5,1fr);grid-template-rows:1fr 1fr;gap:6mm;flex:1}
.toc a{display:flex;flex-direction:column;text-decoration:none;color:inherit;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff}
.toc .h{background:linear-gradient(120deg,var(--blue-d),var(--blue));color:#fff;padding:8px 10px;display:flex;justify-content:space-between;align-items:baseline}
.toc .h small{font-size:7pt;letter-spacing:.2em;font-weight:700;opacity:.9}
.toc .h b{font-size:22pt;font-weight:900;line-height:1}
.toc .c{padding:10px 12px 12px;flex:1;display:flex;flex-direction:column}
.toc .c h4{font-size:12pt;color:var(--navy);font-weight:800;line-height:1.15}
.toc .c p{font-size:8.2pt;color:var(--muted);margin-top:4px;flex:1}
.toc .meta{display:flex;justify-content:space-between;align-items:center;margin-top:7px;padding-top:6px;border-top:1px dashed var(--line);font-size:7.8pt}
.toc .meta b{color:var(--blue-d)}
.toc .pg{background:var(--tint);color:var(--blue-d);font-weight:800;border-radius:5px;padding:1px 6px}
.summary{display:flex;gap:6mm;margin-top:7mm}
.summary div{flex:1;border-radius:12px;background:var(--tint);padding:9px 12px}
.summary b{display:block;font-size:20pt;font-weight:900;color:var(--blue-d);line-height:1.1}
.summary small{color:var(--navy);font-weight:600;font-size:8pt}
.sample{margin-top:auto}
.sample h3{font-size:10pt;color:var(--blue-d);font-weight:800;letter-spacing:.06em;text-transform:uppercase;margin-bottom:6px}
.sample table.vocab td{font-size:9pt;padding:7px 8px}
.pfoot{position:absolute;left:16mm;right:16mm;bottom:9mm;display:flex;justify-content:space-between;font-size:7.6pt;color:var(--muted)}
.pfoot b{color:var(--blue-d)}
"""


def html_doc(title, css, body):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{e(title)}</title><style>{css}</style></head><body>{body}</body></html>"""


def build_front():
    total = sum(len(ws) for ws in DATA.values())
    units_dots = "".join(f"<span>{u}</span>" for u in DATA)
    cover = f"""
<div class="page cover"><div class="grid"></div><div class="blob b1"></div><div class="blob b2"></div>
 <div class="brand">{logo_svg(64, light=True)}<div><b>IMPULSE</b><small>LEARNING CENTER</small></div></div>
 <div class="main">
  <span class="kicker">LEVEL A1 · BEGINNER</span>
  <h1>Vocabulary<br><span>Book</span></h1>
  <p class="lead">Unit-by-unit word lists with transcription, simple English definitions,
  example sentences and Russian &amp; Uzbek translations.</p>
  <div class="feat"><span>{total} words</span><span>10 units</span><span>Transcription</span>
   <span>Russian</span><span>Uzbek</span></div>
 </div>
 <div class="card"><div class="top"><b>WORD OF THE BOOK</b></div>
  <div class="body"><div class="w">holiday <i>n</i></div><div class="ipa">/ˈhɒlədeɪ/</div>
   <div class="row"><small>MEANING</small><span>a period of time when you do not go to work or school</span></div>
   <div class="row"><small>EXAMPLE</small><span>I’m here on <b>holiday</b>.</span></div>
   <div class="row"><small>RUSSIAN</small><span>отпуск, каникулы</span></div>
   <div class="row"><small>UZBEK</small><span>ta’til</span></div></div></div>
 <div class="foot"><div><b>{SCHOOL}</b> · Based on the Navigate A1 coursebook word lists</div>
  <div class="units">{units_dots}</div></div>
</div>"""

    sample_word = next(w for w in DATA["4"] if w["word"] == "get up")
    sample = f"""<table class="vocab"><colgroup><col class="w-num"><col class="w-word">
      <col class="w-ipa"><col class="w-def"><col class="w-ex"><col class="w-ru"><col class="w-uz"></colgroup>
      <thead><tr><th>№</th><th>WORDS</th><th>TRANSCRIPTION</th><th>DEFINITION</th>
      <th>EXAMPLE</th><th>RUSSIAN</th><th>UZBEK</th></tr></thead><tbody>{word_row(1, sample_word)}</tbody></table>"""
    how = f"""
<div class="page"><div class="inner">
 <div class="ptitle">{logo_svg(30)}<h2>How to use this book</h2><div class="bar"></div><small>{SCHOOL.upper()}</small></div>
 <div class="cols">
  <div class="stack">
   <div class="box"><h3>What each column shows</h3><table class="anat">
    <tr><td>WORDS</td><td>The word or phrase with its part of speech in <i style="color:var(--blue)">blue italics</i>.</td></tr>
    <tr><td>TRANSCRIPTION</td><td>How to say the word (British English IPA). <b>ˈ</b> shows the main stress.</td></tr>
    <tr><td>DEFINITION</td><td>A short, simple meaning in English.</td></tr>
    <tr><td>EXAMPLE</td><td>The word in a real sentence from the unit — the word is in <b style="color:var(--blue-d)">bold blue</b>.</td></tr>
    <tr><td>RUSSIAN · UZBEK</td><td>Translations to check your understanding.</td></tr></table></div>
  </div>
  <div class="stack">
   <div class="box"><h3>Abbreviations</h3><div class="abbr">
    <span><b>n</b>noun</span><span><b>n pl</b>plural noun</span><span><b>v</b>verb</span>
    <span><b>phr v</b>phrasal verb</span><span><b>adj</b>adjective</span><span><b>adv</b>adverb</span>
    <span><b>prep</b>preposition</span><span><b>conj</b>conjunction</span><span><b>pron</b>pronoun</span>
    <span><b>det</b>determiner</span><span><b>phr</b>phrase</span><span><b>excl</b>exclamation</span></div></div>
   <div class="box"><h3>Study tips</h3><ul class="tips">
    <li>Learn 10–15 words a day. Cover the definition and say the meaning.</li>
    <li>Read the transcription aloud and copy the stress.</li>
    <li>Write your own example sentence for every new word.</li>
    <li>Cover the English column and translate back from Russian or Uzbek.</li>
    <li>Review each unit again after 1 day, 1 week and 1 month.</li></ul></div>
  </div>
 </div>
 <div class="sample"><h3>Sample entry</h3>{sample}</div>
</div><div class="pfoot"><span><b>{SCHOOL}</b> · {TITLE}</span><span>Navigate A1 · Units 1–10</span></div></div>"""

    cards = []
    for u, ws in DATA.items():
        t, sub = UNIT_TOPICS[u]
        pg = PAGES.get(u)
        cards.append(f"""<a href="#unit-{u}"><div class="h"><small>UNIT</small><b>{u}</b></div>
  <div class="c"><h4>{e(t)}</h4><p>{e(sub)}</p>
  <div class="meta"><span><b>{len(ws)}</b> words</span>{f'<span class="pg">p. {pg}</span>' if pg else ''}</div></div></a>""")
    toc = f"""
<div class="page"><div class="inner">
 <div class="ptitle">{logo_svg(30)}<h2>Contents</h2><div class="bar"></div><small>10 UNITS</small></div>
 <div class="toc">{''.join(cards)}</div>
 <div class="summary"><div><b>{total}</b><small>words and phrases</small></div>
  <div><b>10</b><small>units</small></div>
  <div><b>2</b><small>translations: Russian &amp; Uzbek</small></div></div>
</div><div class="pfoot"><span><b>{SCHOOL}</b> · {TITLE}</span><span>Navigate A1 · Units 1–10</span></div></div>"""
    return html_doc(f"{SCHOOL} — {TITLE}", FRONT_CSS, cover + how + toc)


def build_body():
    sections = "".join(unit_section(u, ws) for u, ws in DATA.items())
    return html_doc(f"{SCHOOL} — {TITLE}", BODY_CSS, sections)


def build_header_footer():
    header = f"""<div style="width:100%;margin:0 10mm;padding-bottom:5px;border-bottom:1.5px solid #1E90FF;
display:flex;justify-content:space-between;align-items:center;font-family:Inter,sans-serif;font-size:8px;color:#0A2A5E;
-webkit-print-color-adjust:exact">
<span style="display:flex;align-items:center;gap:6px">{logo_svg(14)}<b style="letter-spacing:.12em">IMPULSE</b>
<span style="letter-spacing:.12em;color:#6B7A90">LEARNING CENTER</span></span>
<span style="letter-spacing:.14em"><b style="color:#1E90FF">A1</b> VOCABULARY BOOK</span></div>"""
    footer = f"""<div style="width:100%;margin:0 10mm;display:flex;justify-content:space-between;align-items:center;
font-family:Inter,sans-serif;font-size:7.5px;color:#6B7A90;-webkit-print-color-adjust:exact">
<span>© {SCHOOL} · Based on the Navigate A1 coursebook word lists</span>
<span style="background:#1E90FF;color:#fff;border-radius:4px;padding:2px 7px;font-weight:700">Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>"""
    return {"header": header, "footer": footer}


if __name__ == "__main__":
    DIST.mkdir(exist_ok=True)
    (DIST / "front.html").write_text(build_front(), encoding="utf-8")
    (DIST / "body.html").write_text(build_body(), encoding="utf-8")
    (DIST / "unit_titles.json").write_text(
        json.dumps({u: t for u, (t, _) in UNIT_TOPICS.items()}, ensure_ascii=False), encoding="utf-8")
    (DIST / "header_footer.json").write_text(json.dumps(build_header_footer()), encoding="utf-8")
    print("built", sum(len(w) for w in DATA.values()), "words")
