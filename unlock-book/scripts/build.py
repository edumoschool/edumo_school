"""Build the Unlock-5-based C1 units (A3, same design as the original Unit 2 / Unit 3) -> dist/units.html.

Usage: python3 scripts/build.py [unit numbers…]      (default: every file in data/units)
Then:  node scripts/render.js                        (paginates flowing sections and prints the PDF)
"""
import base64
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "units"
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"

_split_id = 0


# ---------------- helpers ----------------
def md(s):
    """Inline markup: [[kw]] red bold, **b**, *i*, \\n -> <br>."""
    s = html.escape(str(s), quote=False)
    s = re.sub(r"\[\[(.+?)\]\]", r'<b class="kw">\1</b>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    return s.replace("\n", "<br>")


def paras(text, cls=""):
    """Split a multi-paragraph string on newlines into <p>."""
    c = f' class="{cls}"' if cls else ""
    return "".join(f"<p{c}>{md(p)}</p>" for p in str(text).split("\n") if p.strip())


def split(inner, cls="", tag="div"):
    """A container whose children may be distributed over several pages by render.js."""
    global _split_id
    _split_id += 1
    return f'<{tag} class="split {cls}" data-split="s{_split_id}">{inner}</{tag}>'


def blk(inner, label=None, cls=""):
    lab = f'<span class="lbl">{label}</span>' if label else ""
    return f'<div class="blk {cls}">{lab}{inner}</div>'


def data_uri(path):
    mime = "image/png" if path.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def letters(n):
    return "abcdefghijklmnopqrstuvwxyz"[n]


def lighten(hex_color, f):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (round(c + (255 - c) * f) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


SPEAKER = ('<svg class="audio" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#E4E7EC"/>'
           '<path d="M6 10h3l4-3v10l-4-3H6z" fill="#7B8494"/><path d="M15 9.5a3.5 3.5 0 0 1 0 5" stroke="#7B8494" '
           'stroke-width="1.4" fill="none" stroke-linecap="round"/></svg>')


# ---------------- pages ----------------
def section(tab, body, cls="", first_strip="sl"):
    """A flowing section: first page gets the blue tab; overflow continues on extra pages (render.js)."""
    tab_html = f'<div class="tab"><i></i><span>{tab}</span></div>' if tab else ""
    tabcls = " hastab" if tab else ""
    return (f'<section class="page {first_strip}{tabcls} {cls}"><div class="strip"></div>{tab_html}'
            f'<div class="content">{body}</div><footer class="pno"></footer></section>')


def cover(u):
    img = ASSETS / "covers" / f"u{u['n']:02d}.png"
    bg = f'<img class="cimg" src="{data_uri(img)}" alt="">' if img.exists() else ""
    dark, light = u["cover_color"], lighten(u["cover_color"], .45)
    qs = "".join(f"<li><b>{i}.</b> {md(q)}</li>" for i, q in enumerate(u["warmup"], 1))
    return f"""<section class="page cover" style="--cdark:{dark};--clight:{light}">{bg}
 <div class="cband"><div class="ctitle"><h1>{md(u['title'])}</h1><small>{md(u['subtitle'])}</small></div>
  <div class="cunit">UNIT {u['n']}</div></div>
 <div class="warm"><div class="whead"><h2>WARM-UP SPEAKING</h2>
  <p>Discuss the questions below with a partner, or answer each one in about 30 seconds.</p></div>
  <ol>{qs}</ol></div></section>"""


def p_article1_vocab(u):
    a = u["article1"]
    sents = "".join(f"<li><span>{i}</span> {md(s)}</li>" for i, s in enumerate(a["vocab"], 1))
    defs = "".join(f"<li><span>{letters(i)}</span> {md(d)}</li>" for i, d in enumerate(a["definitions"]))
    wf = "".join(f"<li><b>{i}.</b> {md(s)} ({md(w)})</li>" for i, (s, w) in enumerate(u["word_forms"], 1))
    body = (blk(f'<h2 class="art">Article 1</h2><p class="ins">Read the sentences. Match each word in bold to its '
                f'definition (a–{letters(len(a["definitions"]) - 1)}).</p><ol class="vsent">{sents}</ol>'
                f'<ol class="defs">{defs}</ol>', "UNDERSTANDING<br>KEY VOCABULARY")
            + blk(f'<p class="ins">Complete the sentences with the correct form of a word from either article.</p>'
                  f'<ol class="wforms">{wf}</ol>', cls="gap-top"))
    return section("Article &amp; Vocabulary", body, "serif")


def p_article1(u):
    a = u["article1"]
    ps = "".join(f"<p><span class='pn'>{i}</span> {md(p)}</p>" for i, p in enumerate(a["paragraphs"], 1))
    return section(None, f'<div class="green"><h2>{md(a["title"])}</h2><div class="cols2">{ps}</div></div>', "serif artpage")


def p_headings(u):
    a, ld = u["article1"], u["language_dev"]
    hs = "".join(f"<li><span>{chr(65 + i)}</span> {md(h)}</li>" for i, h in enumerate(a["headings"]))
    rows = "".join(f"<tr><th>{md(k)}</th><td>{md(v)}</td></tr>" for k, v in ld["table"])
    sents = "".join(f"<li><b>{i}.</b> {md(s)}</li>" for i, s in enumerate(ld["sentences"], 1))
    body = (blk(f'<p class="ins">Match headings A–{chr(64 + len(a["headings"]))} to paragraphs 1–{len(a["paragraphs"])} '
                f'of Article 1. There is one extra heading you do not need.</p><ol class="heads">{hs}</ol>',
                "MATCH THE HEADING")
            + blk(f'<h3 class="ld">LANGUAGE DEVELOPMENT - {md(ld["title"])}</h3>'
                  f'<div class="skill"><small>VOCABULARY SKILL</small><b>{md(ld["skill_name"])}</b>'
                  f'<p>{md(ld["skill_text"])}</p></div><table class="coll">{rows}</table>'
                  f'<p class="ins">{md(ld["instruction"])}</p><ol class="wforms">{sents}</ol>', cls="gap-top"))
    return section(None, body, "serif", first_strip="sr")


def p_article2_vocab(u):
    a = u["article2"]
    items = "".join(
        f'<li><p><b>{i}.</b> {md(v["q"])}</p><ol class="abc">'
        + "".join(f"<li><span>{letters(j)}</span> {md(o)}</li>" for j, o in enumerate(v["options"]))
        + "</ol></li>" for i, v in enumerate(a["vocab"], 1))
    body = blk(f'<h2 class="art">Article 2</h2><p class="ins"><b>2</b> {md(a["intro"])}</p>'
               f'<ol class="a2v">{items}</ol>', "UNDERSTANDING<br>KEY VOCABULARY")
    return section("Article &amp; Vocabulary", body, "serif")


def p_article2(u):
    a = u["article2"]
    ps = "".join(f"<p><b>{i}.</b> {md(p)}</p>" for i, p in enumerate(a["paragraphs"], 1))
    disc = "".join(f"<p>{i}&nbsp; {md(q)}</p>" for i, q in enumerate(a["discussion"], 1))
    return section(None, f'<div class="card"><h2>{md(a["title"])}</h2><div class="cols2">{ps}'
                         f'<div class="disc"><h4>DISCUSSION</h4><h5>Work with a partner. Discuss the questions.</h5>{disc}</div>'
                         f'</div></div>', "serif artpage")


def p_grammar(u):
    g = u["grammar"]
    rules = "".join(f'<p class="rule">{i}. {md(r["rule"])}</p><p class="ex">{md(r["example"])}</p>'
                    for i, r in enumerate(g["rules"], 1))
    exb = "".join(f"<li><b>{i}.</b> {md(s)}</li>" for i, s in enumerate(g["exB"]["items"], 1))
    body = (f'<div class="obar"><b>GRAMMAR</b><small>{md(g["title"])}</small></div>'
            f'<p class="gintro">{md(g["intro"])}</p>'
            f'<div class="rules"><p>{md(g["rules_intro"])}</p>{rules}</div>'
            f'<div class="exbox"><p class="exh">{md(g["exA"]["instruction"])}</p><p class="extext">{md(g["exA"]["text"])}</p>'
            f'<p class="exh gap-top">{md(g["exB"]["instruction"])}</p><ol class="exb">{exb}</ol></div>')
    return section("GRAMMAR FOR WRITING", body, "sans")


def p_academic(u):
    a = u["academic"]
    ex = "".join(f'<p class="pe"><b class="{"orig" if k.upper().startswith("ORIG") else "para"}">{md(k)}:</b> '
                 f'<i>{md(v)}</i></p>' for k, v in a.get("example", []))
    items = "".join(f'<li>{i}&nbsp; {md(s)}<i class="wl"></i></li>' for i, s in enumerate(a["items"], 1))
    body = (f'<div class="obar"><b>ACADEMIC WRITING</b><small>{md(a["subtitle"])}</small></div>'
            f'<div class="skill"><small>ACADEMIC WRITING SKILL</small><b>{md(a["skill_name"])}</b><p>{md(a["skill_text"])}</p></div>'
            f'<div class="exbox">{ex}<p class="exh">{md(a["instruction"])}</p><ol class="para-items">{items}</ol>'
            f'<h4 class="wt">WRITING TASK</h4><p class="exh">{md(a["task"])}</p><div class="wbox short"></div></div>')
    return section(None, body, "sans", first_strip="sr")


# ---------------- exam blocks ----------------
def exam_block(b):
    t = b["type"]
    if t == "instruction":
        icon = SPEAKER if b.get("audio") else ""
        return f'<div class="xins">{icon}<p>{md(b["text"])}</p></div>'
    if t == "article":
        title = f'<h3 class="xtitle">{md(b["title"])}</h3>' if b.get("title") else ""
        ps = "".join(f"<p>{md(p)}</p>" for p in b["paragraphs"])
        return title + split(ps, "xart" + (" one" if b.get("cols") == 1 else ""))
    if t == "text":
        return split("".join(f"<p>{md(p)}</p>" for p in b["paragraphs"]), "xart one")
    if t == "headings":
        left = "".join(f"<li>{md(i)}</li>" for i in b["items"])
        right = "".join(f"<li>{md(i)}</li>" for i in b.get("right", []))
        return (f'<div class="xheads"><div><b>{md(b.get("title", "List of Headings:"))}</b><ol>{left}</ol></div>'
                f'<ol class="r">{right}</ol></div>')
    if t == "statements":
        return f'<ol class="xstate">{"".join(f"<li>{md(i)}</li>" for i in b["items"])}</ol>'
    if t == "cards":
        title = f'<h3 class="xtitle">{md(b["title"])}</h3>' if b.get("title") else ""
        return title + split("".join(f'<div class="xcard"><b>{md(c["title"])}</b>{paras(c["body"])}</div>'
                                     for c in b["items"]), "xcards")
    if t == "mcq":
        items = "".join(
            f'<div class="q"><p><b>{md(q["q"]) if str(q["q"]).lstrip().startswith(str(q.get("n", ""))) else (str(q["n"]) + ". " + md(q["q"]) if q.get("n") else md(q["q"]))}</b></p>'
            + "".join(f"<p>{md(o)}</p>" for o in q.get("options", [])) + "</div>" for q in b["items"])
        title = f'<h4 class="xsub">{md(b["title"])}</h4>' if b.get("title") else ""
        return title + split(items, "xmcq" + (" two" if b.get("cols", 1) == 2 else ""))
    if t == "notes":
        title = f'<h3 class="xtitle c">{md(b["title"])}</h3>' if b.get("title") else ""
        return f'<div class="xnotes">{title}{"".join(f"<p>{md(l)}</p>" for l in b["lines"])}</div>'
    if t == "matching":
        left = "".join(f"<li>{md(i)}</li>" for i in b["left"])
        right = "".join(f"<li>{md(i)}</li>" for i in b["right"])
        return f'<div class="xmatch"><ol>{left}</ol><ol>{right}</ol></div>'
    if t == "image":
        w = b.get("width", 150)
        cap = f'<h3 class="xtitle c red">{md(b["caption"])}</h3>' if b.get("caption") else ""
        return f'<div class="ximg">{cap}<img src="{data_uri(ASSETS / b["src"])}" style="width:{w}mm" alt=""></div>'
    if t == "lines":
        return f'<ol class="xlines">{"".join(f"<li>{md(i)}</li>" for i in b["items"])}</ol>'
    raise ValueError(f"unknown block type {t}")


def p_reading(u):
    r = u["reading"]
    blocks = "".join(exam_block(b) for b in r["blocks"])
    words = "".join(f"<li>{i}. {md(w)} <i class='chk'></i></li>" for i, w in enumerate(u["wordlist"], 1))
    body = (blk(blocks, f'PART {r["part"]}', "exam")
            + f'<div class="wordlist"><h4>✔ Wordlist</h4><ol>{words}</ol></div>')
    return section("READING PRACTICE", body, "exam-page")


def p_listening(u):
    li = u["listening"]
    blocks = "".join(exam_block(b) for b in li["blocks"])
    idioms = "".join(f"<p><b>{md(k)}:</b> {md(v)}</p>" for k, v in u["idioms"])
    body = blk(blocks, f'PART {li["part"]}', "exam") + split(f'<h4 class="idh">Phrases &amp; Idioms Wordlist</h4>{idioms}', "idioms")
    return section("LISTENING PRACTICE", body, "exam-page")


def useful_table(rows, head=("Function", "Useful phrases")):
    trs = "".join(f"<tr><th>{md(a)}</th><td>{md(b)}</td></tr>" for a, b in rows)
    return f'<table class="useful"><tr><th>{head[0]}</th><td>{head[1]}</td></tr>{trs}</table>'


def checklist(items):
    return "".join(f'<p class="chkl">☐&nbsp; {md(r)}</p>' for r in items)


def p_writing(u):
    w = u["writing"]
    if w["kind"] == "letter":
        body = (f'<h3 class="teal">{md(w["useful_title"])}</h3>{useful_table(w["useful"])}'
                f'<h4 class="tsm">{md(w["practice_title"])}</h4><p class="sit">{md(w["situation"])}</p>'
                f'<div class="email">{paras(w["email"])}</div><p class="task">{md(w["task11"])}</p><div class="wbox"></div>'
                f'<p class="task">{md(w["task12"])}</p>'
                f'<h4 class="tsm">{md(w["rules_title"])}</h4>{checklist(w["rules"])}'
                f'<div class="sample"><h5>{md(w["sample_title"])}</h5>{paras(w["sample"])}</div>'
                f'<h4 class="tsm">{md(w["practice2_title"])}</h4><p class="sit">{md(w["situation2"])}</p>'
                f'<div class="email">{paras(w["email2"])}</div><p class="task">{md(w["task2"])}</p><div class="wbox tall"></div>')
    else:
        plan = "".join(f"<tr><th>{md(a)}</th><td>{md(b)}</td></tr>" for a, b in w["plan"])
        body = (f'<h3 class="teal">{md(w["useful_title"])}</h3>{useful_table(w["useful"])}'
                f'<h4 class="tsm">THE TASK</h4><p class="sit">{md(w["task_intro"])}</p>'
                f'<div class="email"><p><b>{md(w["task"])}</b></p></div>'
                f'<h4 class="tsm">PARAGRAPH PLAN</h4><table class="useful plan">{plan}</table>'
                f'<h4 class="tsm">{md(w["rules_title"])}</h4>{checklist(w["rules"])}'
                f'<div class="sample"><h5>{md(w["sample_title"])}</h5>{paras(w["sample"])}</div>'
                f'<h4 class="tsm">{md(w["practice_title"])}</h4><div class="email"><p><b>{md(w["practice_task"])}</b></p></div>'
                f'<div class="wbox xtall"></div>')
    return section(md(w["title"]), split(body, "wflow"), "sans")


def p_speaking(u):
    s = u["speaking"]
    if s["part"] == "2":
        pts = "".join(f"<p>☐&nbsp; {md(p)}</p>" for p in s["points"])
        box = (f'<div class="qbox"><span class="qv">QUESTIONS</span><div><p class="qt">{md(s["prompt"])}</p>'
               f'<p>You should say:</p>{pts}<p>{md(s["end"])}</p></div></div>')
        sample = f'<div class="ssample"><h5>SAMPLE ANSWER</h5>{paras(s["sample"])}</div>'
    elif s["part"] == "3":
        n = max(len(s["for"]), len(s["against"]))
        rows = "".join(f'<tr><td>{md(s["for"][i]) if i < len(s["for"]) else ""}</td>'
                       f'<td>{md(s["against"][i]) if i < len(s["against"]) else ""}</td></tr>' for i in range(n))
        box = (f'<div class="qbox"><span class="qv">STATEMENT</span><div><p class="qt">{md(s["statement"])}</p>'
               f'<p>Discuss both sides of the statement and give your own opinion. Use the points below to help you.</p></div></div>'
               f'<table class="fa"><tr><th>FOR</th><th>AGAINST</th></tr>{rows}</table>')
        sample = f'<div class="ssample"><h5>SAMPLE ANSWER</h5>{paras(s["sample"])}</div>'
    else:
        qs = "".join(f"<p>{i}.&nbsp; {md(q)}</p>" for i, q in enumerate(s["questions"], 1))
        box = (f'<div class="qbox"><span class="qv">QUESTIONS</span><div><p class="qt">Answer the questions. '
               f'Speak for about 30 seconds for each one.</p>{qs}</div></div>')
        sample = ('<div class="ssample"><h5>SAMPLE ANSWERS</h5>'
                  + "".join(f'<p class="sq">{md(q)}</p>{paras(a)}' for q, a in s["samples"]) + "</div>")
    useful = "".join(f"<tr><th>{md(a)}</th><td>{md(b)}</td></tr>" for a, b in s["useful"])
    body = box + sample + f'<div class="sul"><h5>USEFUL LANGUAGE</h5><table>{useful}</table></div>'
    return section(md(s["title"]), body, "sans")


def unit_pages(u):
    return "".join([cover(u), p_article1_vocab(u), p_article1(u), p_headings(u), p_article2_vocab(u), p_article2(u),
                    p_grammar(u), p_academic(u), p_reading(u), p_listening(u), p_writing(u), p_speaking(u)])


KEY_LABELS = [("article1_vocab", "Article 1 vocabulary"), ("word_forms", "Word forms"), ("headings", "Match the heading"),
              ("language_dev", "Language development"), ("article2_vocab", "Article 2 vocabulary"),
              ("grammar_a", "Grammar – Exercise A"), ("grammar_b", "Grammar – Exercise B"), ("reading", "Reading practice")]


def answer_key(units):
    body = ""
    for u in units:
        k = u.get("key", {})
        rows = "".join(f"<tr><th>{lab}</th><td>{md(k[f])}</td></tr>" for f, lab in KEY_LABELS if k.get(f))
        body += f'<div class="kunit"><h3>Unit {u["n"]} · {md(u["title"].title())}</h3><table>{rows}</table></div>'
    return section("ANSWER KEY", split(body, "keyflow"), "sans")


def load(nums=None):
    units = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(DATA.glob("*.json"))]
    return [u for u in units if not nums or u["n"] in nums]


def build(nums=None):
    units = load(nums)
    css = (ROOT / "scripts" / "style.css").read_text(encoding="utf-8")
    pages = "".join(unit_pages(u) for u in units) + answer_key(units)
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Units {units[0]['n']}–{units[-1]['n']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,600;0,700;0,800;0,900;1,400;1,600&family=Tinos:ital,wght@0,400;0,700;1,400;1,700&family=Open+Sans:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Arimo:wght@400;700&display=block" rel="stylesheet">
<style>{css}</style></head><body>{pages}</body></html>"""
    DIST.mkdir(exist_ok=True)
    (DIST / "units.html").write_text(doc, encoding="utf-8")
    print(f"units: {[u['n'] for u in units]} -> dist/units.html")


if __name__ == "__main__":
    build([int(a) for a in sys.argv[1:]] or None)
