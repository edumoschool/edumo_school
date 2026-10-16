"""Build the Impulse Learning Center A1 Speaking Book (HTML -> dist/speaking-book.html).

Every page is laid out explicitly (A4 landscape), so page numbers in the
contents are known without a second rendering pass:
  cover · how to use · contents · then 3 pages per unit
  (lessons x.1+x.2, x.3+x.4, x.5 + unit review).
"""
import base64
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UNITS = json.loads((ROOT / "data" / "questions.json").read_text(encoding="utf-8"))
LOGO = "data:image/png;base64," + base64.b64encode(
    (ROOT.parent / "vocabulary-book" / "assets" / "impulse-logo.png").read_bytes()).decode()
SCHOOL = "Impulse Learning Center"
e = html.escape


def load_helpers():
    helpers, cur = {}, None
    for line in (ROOT / "data" / "helpers.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("## "):
            cur = helpers.setdefault(line[3:], {"words": [], "starters": []})
        elif line.startswith("w: "):
            en, uz = line[3:].split(" = ", 1)
            cur["words"].append((en, uz))
        elif line.startswith("s: "):
            cur["starters"].append(line[3:])
    return helpers


HELPERS = load_helpers()

ICONS = {
    "user": "M12 12a4 4 0 100-8 4 4 0 000 8zM4 21c0-4 4-6 8-6s8 2 8 6",
    "help": "M12 21a9 9 0 100-18 9 9 0 000 18zM9.5 9a2.5 2.5 0 115 0c0 2-2.5 2-2.5 4M12 17v.5",
    "family": "M9 11a3 3 0 100-6 3 3 0 000 6zM17 12a2.5 2.5 0 100-5 2.5 2.5 0 000 5zM3 20c0-3 3-5 6-5s6 2 6 5M15.5 15.2c3 0 5.5 1.6 5.5 4.8",
    "clock": "M12 21a9 9 0 100-18 9 9 0 000 18zM12 7v5l3 2",
    "shirt": "M8 3L3 6l2 5 3-1v11h8V10l3 1 2-5-5-3c-1 2-2.5 3-4 3S9 5 8 3z",
    "home": "M3 11l9-7 9 7M5 10v10h14V10M10 20v-6h4v6",
    "star": "M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.6 6.6 19.5l1.2-6L3.3 9.3l6.1-.7z",
    "hourglass": "M6 3h12M6 21h12M7 3v3l5 6-5 6v3M17 3v3l-5 6 5 6v3",
    "cloud": "M7 18h10a4 4 0 00.5-8 6 6 0 00-11.5 1.5A3.5 3.5 0 007 18z",
    "send": "M22 2L11 13M22 2l-7 20-4-9-9-4z",
    "chat": "M4 5h16v11H9l-5 4z",
    "pen": "M4 20l4-1 11-11-3-3L5 16zM14 6l3 3",
    "play": "M12 21a9 9 0 100-18 9 9 0 000 18zM10 8.5v7l6-3.5z",
    "book": "M4 5a2 2 0 012-2h13v16H6a2 2 0 00-2 2zM4 5v16M8 7h7",
    "bulb": "M9 18h6M10 21h4M12 3a6 6 0 00-3.5 10.9V16h7v-2.1A6 6 0 0012 3z",
    "mic": "M12 3a3 3 0 00-3 3v6a3 3 0 006 0V6a3 3 0 00-3-3zM5 11a7 7 0 0014 0M12 18v3",
    "check": "M4 12l5 5L20 6",
    "target": "M12 21a9 9 0 100-18 9 9 0 000 18zM12 17a5 5 0 100-10 5 5 0 000 10zM12 13a1 1 0 100-2 1 1 0 000 2z",
}
UNIT_ICONS = ["user", "help", "family", "clock", "shirt", "home", "star", "hourglass", "cloud", "send"]


def icon(name, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true"><path d="{ICONS[name]}" fill="none" '
            'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def lesson_kind(title):
    if title.startswith("Video"):
        return "play", "Video", title.split("–", 1)[1].strip() if "–" in title else title
    if title.startswith("Speaking and Writing"):
        return "pen", "Speaking & Writing", title.split("–", 1)[1].strip() if "–" in title else "Speaking and Writing"
    return "chat", "Speaking", title


def logo(size, ring=False):
    style = "border:2px solid #fff;" if ring else ""
    return f'<img class="logo" src="{LOGO}" width="{size}" height="{size}" alt="" style="{style}">'


def frame(inner, page_no, cls=""):
    return f"""<section class="page {cls}">
 <header class="run"><span class="brand">{logo(18)}<b>IMPULSE</b><span>LEARNING CENTER</span></span>
  <span class="tag"><b>A1</b> SPEAKING BOOK</span></header>
 <div class="content">{inner}</div>
 <footer class="run"><span>© {SCHOOL} · Based on Navigate Beginner A1 speaking topics</span>
  <span class="pg">Page {page_no}</span></footer>
</section>"""


def lesson_card(lesson):
    ico, kind, title = lesson_kind(lesson["title"])
    h = HELPERS[lesson["id"]]
    qs = "".join(
        f'<li><span class="qn">{q["n"]}</span><div><p>{e(q["q"])}</p><i class="line"></i></div></li>'
        for q in lesson["questions"])
    words = "".join(f'<li><b>{e(en)}</b><span>{e(uz)}</span></li>' for en, uz in h["words"])
    starters = "".join(f"<li>{e(s)}</li>" for s in h["starters"])
    return f"""<article class="lesson kind-{ico}">
 <div class="lh"><span class="lico">{icon(ico)}</span>
  <div><small>LESSON {lesson["id"]} · {kind.upper()}</small><h3>{e(title)}</h3></div></div>
 <ol class="qs">{qs}</ol>
 <div class="help">
  <div class="words"><h4>{icon("book")}Words &amp; phrases</h4><ul>{words}</ul></div>
  <div class="starters"><h4>{icon("bulb")}Answer starters</h4><ul>{starters}</ul></div>
 </div>
</article>"""


def unit_banner(u):
    n = u["n"]
    titles = [lesson_kind(l["title"])[2] for l in u["lessons"]]
    return f"""<div class="ubanner"><div class="uno"><small>UNIT</small><span>{n}</span></div>
 <span class="uico">{icon(UNIT_ICONS[n - 1])}</span>
 <div class="ut"><h1>{e(u["title"])}</h1><p>{" · ".join(e(t) for t in titles)}</p></div>
 <div class="ustat"><b>25</b><small>questions</small></div></div>"""


def review_card(u):
    checks = "".join(f'<li><i class="cbox"></i>I can talk about: <b>{e(lesson_kind(l["title"])[2])}</b></li>'
                     for l in u["lessons"])
    first_q = [l["questions"][0]["q"] for l in u["lessons"]]
    talk = "".join(f"<li>{e(q)}</li>" for q in first_q[:3])
    return f"""<article class="review">
 <div class="lh"><span class="lico">{icon("target")}</span>
  <div><small>UNIT {u["n"]} · REVIEW</small><h3>Check your speaking</h3></div></div>
 <div class="rbox"><h4>{icon("mic")}1-minute talk</h4>
  <p>Talk for one minute without stopping. Use these questions to help you:</p><ul class="talk">{talk}</ul></div>
 <div class="rbox"><h4>{icon("check")}Can you do it?</h4><ul class="checks">{checks}</ul></div>
 <div class="rbox notes"><h4>{icon("pen")}My new words</h4><i class="line"></i><i class="line"></i><i class="line"></i><i class="line"></i></div>
</article>"""


def body_pages(start):
    pages, unit_pages, p = [], {}, start
    for u in UNITS:
        L = u["lessons"]
        unit_pages[u["n"]] = p
        pages.append(frame(unit_banner(u) + f'<div class="two first">{lesson_card(L[0])}{lesson_card(L[1])}</div>', p))
        p += 1
        pages.append(frame(f'<div class="two">{lesson_card(L[2])}{lesson_card(L[3])}</div>', p))
        p += 1
        pages.append(frame(f'<div class="two">{lesson_card(L[4])}{review_card(u)}</div>', p))
        p += 1
    return pages, unit_pages


def cover():
    dots = "".join(f"<span>{u['n']}</span>" for u in UNITS)
    return f"""<section class="page cover"><div class="grid"></div><div class="blob b1"></div><div class="blob b2"></div>
 <div class="cbrand">{logo(64, ring=True)}<div><b>IMPULSE</b><small>LEARNING CENTER</small></div></div>
 <div class="main"><span class="kicker">LEVEL A1 · BEGINNER</span>
  <h1>Speaking<br><span>Book</span></h1>
  <p class="lead">250 speaking questions in 10 units, with useful words &amp; phrases,
  Uzbek translations and answer starters for every lesson.</p>
  <div class="feat"><span>250 questions</span><span>50 lessons</span><span>400 words &amp; phrases</span><span>Answer starters</span></div></div>
 <div class="card"><div class="top">{icon("chat")}<b>LESSON 1.2 · SPEAKING</b></div>
  <div class="cb"><div class="q"><span class="qn">6</span>Where are you from?</div>
   <div class="chips"><span>I’m from …</span><span>capital</span><span>small town</span></div>
   <div class="st">{icon("bulb")}<span>I’m from Tashkent. It’s the capital of Uzbekistan.</span></div></div></div>
 <div class="cfoot"><div><b>{SCHOOL}</b> · Based on Navigate Beginner A1 speaking topics</div>
  <div class="units">{dots}</div></div>
</section>"""


def how_to():
    steps = [
        ("chat", "Read the question", "Read each question aloud. Check new words in the <b>Words &amp; phrases</b> box."),
        ("bulb", "Use a starter", "Begin your answer with an <b>answer starter</b>, then add your own idea."),
        ("mic", "Say more", "Give 2–3 sentences: answer + reason (<i>because…</i>) + example."),
        ("pen", "Write it down", "Write a short answer on the line under each question."),
    ]
    step_html = "".join(f'<div class="step"><span class="sico">{icon(i)}</span><b>{n}. {t}</b><p>{d}</p></div>'
                        for n, (i, t, d) in enumerate(steps, 1))
    kinds = "".join(f'<div class="kind kind-{i}"><span class="lico">{icon(i)}</span><div><b>{t}</b><p>{d}</p></div></div>'
                    for i, t, d in [
                        ("chat", "Speaking", "Everyday questions about you, your life and your country."),
                        ("pen", "Speaking & Writing", "Real-life language: greetings, shops, travel, reviews."),
                        ("play", "Video", "Questions connected to the unit video topic."),
                    ])
    return f"""<section class="page"><div class="inner">
 <div class="ptitle">{logo(30)}<h2>How to use this book</h2><div class="bar"></div><small>{SCHOOL.upper()}</small></div>
 <div class="steps">{step_html}</div>
 <div class="hgrid">
  <div class="stack">
   <div class="box"><h3>Three kinds of lessons</h3>{kinds}</div>
   <div class="box"><h3>Classroom phrases</h3><table class="ext cls">
    <tr><td>Can you repeat that, please?</td><td>Takrorlay olasizmi?</td></tr>
    <tr><td>How do you say … in English?</td><td>… inglizcha qanday bo‘ladi?</td></tr>
    <tr><td>What does … mean?</td><td>… nimani anglatadi?</td></tr>
    <tr><td>Can you speak more slowly, please?</td><td>Sekinroq gapira olasizmi?</td></tr>
    <tr><td>Sorry, I don’t know.</td><td>Kechirasiz, bilmayman.</td></tr></table></div>
  </div>
  <div class="stack">
   <div class="box"><h3>Make your answer longer</h3>
    <table class="ext"><tr><td>Short</td><td>Yes, I have.</td></tr>
    <tr><td>Better</td><td>Yes, I’ve got a cat.</td></tr>
    <tr><td>Best</td><td>Yes, I’ve got a cat. Her name is Mimi and she’s very friendly. I play with her every evening.</td></tr></table>
    <h3 style="margin-top:12px">Linking words</h3>
    <div class="links"><span>and</span><span>but</span><span>because</span><span>so</span><span>also</span><span>usually</span><span>for example</span><span>I think…</span></div></div>
   <div class="box"><h3>Speaking checklist</h3><ul class="checks big">
    <li><i class="cbox"></i>I speak in full sentences.</li>
    <li><i class="cbox"></i>I give a reason with <b>because</b>.</li>
    <li><i class="cbox"></i>I look at the person and speak clearly.</li>
    <li><i class="cbox"></i>I don’t stop when I make a mistake.</li></ul></div>
  </div>
 </div>
</div><div class="pfoot"><span><b>{SCHOOL}</b> · A1 Speaking Book</span><span>Navigate Beginner A1</span></div></section>"""


def contents(unit_pages):
    cards = "".join(f"""<a><div class="h"><span class="tico">{icon(UNIT_ICONS[u["n"] - 1])}</span><span><small>UNIT</small><b>{u["n"]}</b></span></div>
  <div class="c"><h4>{e(u["title"])}</h4><ul>{"".join(f"<li>{e(lesson_kind(l['title'])[2])}</li>" for l in u["lessons"])}</ul>
  <div class="meta"><span>Q {u["lessons"][0]["questions"][0]["n"]}–{u["lessons"][-1]["questions"][-1]["n"]}</span><span class="pg">p. {unit_pages[u["n"]]}</span></div></div></a>"""
                    for u in UNITS)
    return f"""<section class="page"><div class="inner">
 <div class="ptitle">{logo(30)}<h2>Contents</h2><div class="bar"></div><small>10 UNITS · 50 LESSONS</small></div>
 <div class="toc">{cards}</div>
</div><div class="pfoot"><span><b>{SCHOOL}</b> · A1 Speaking Book</span><span>Navigate Beginner A1</span></div></section>"""


CSS = (ROOT / "scripts" / "style.css").read_text(encoding="utf-8")


def build():
    front = [cover(), how_to()]
    body, unit_pages = body_pages(start=len(front) + 2)
    pages = front + [contents(unit_pages)] + body
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{SCHOOL} — A1 Speaking Book</title><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"""
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / "speaking-book.html").write_text(doc, encoding="utf-8")
    print("pages:", len(pages))


if __name__ == "__main__":
    build()
