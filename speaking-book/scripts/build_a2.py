"""Build the Impulse Learning Center A2 Speaking Book (HTML -> dist/a2-speaking-book.html).

Same colours and design as the A1 book (style.css + style_a2.css). Questions,
vocabulary and starters come from data/a2-content.txt. A2 lessons have ten questions, so each lesson gets a full-width card on its own page:
  cover · how to use · contents · per unit: 5 lesson pages + review page
"""
import json
from pathlib import Path

from build import ICONS, e, icon, logo

ROOT = Path(__file__).resolve().parent.parent
UNIT_TITLES = [u["title"] for u in json.loads((ROOT / "data" / "a2-questions.json").read_text(encoding="utf-8"))]


def load_content():
    """Read data/a2-content.txt into units -> lessons (questions numbered 1-600) and helper lists."""
    units, helpers, n = [], {}, 0
    for line in (ROOT / "data" / "a2-content.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("## "):
            lid, kind, title = (x.strip() for x in line[3:].split("|"))
            u = int(lid.split(".")[0])
            if len(units) < u:
                units.append({"n": u, "title": UNIT_TITLES[u - 1], "lessons": []})
            lesson = {"id": lid, "kind": kind, "title": title, "questions": []}
            units[-1]["lessons"].append(lesson)
            helpers[lid] = {"words": [], "starters": []}
        elif line.startswith("q: "):
            n += 1
            lesson["questions"].append({"n": n, "q": line[3:]})
        elif line.startswith("w: "):
            helpers[lid]["words"].append(tuple(line[3:].split(" = ", 1)))
        elif line.startswith("s: "):
            helpers[lid]["starters"].append(line[3:])
    return units, helpers


UNITS, HELPERS = load_content()
SCHOOL = "Impulse Learning Center"

ICONS.update({
    "globe": "M12 3a9 9 0 100 18 9 9 0 000-18zM3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18",
    "sun": "M12 16a4 4 0 100-8 4 4 0 000 8zM12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4",
    "briefcase": "M3 8h18v12H3zM8 8V5h8v3M3 13h18",
    "building": "M4 21V5l8-2v18M12 7l8 2v12M7 8h2M7 12h2M7 16h2M15 12h2M15 16h2M2 21h20",
    "bag": "M5 8h14l-1 13H6zM9 8V6a3 3 0 016 0v2",
    "history": "M3 12a9 9 0 103-6.7L3 8M3 3v5h5M12 7v5l3 2",
    "heart": "M12 20s-7-4.4-9-9a5 5 0 019-3 5 5 0 019 3c-2 4.6-9 9-9 9z",
    "compass": "M12 21a9 9 0 100-18 9 9 0 000 18zM15.5 8.5l-2 5-5 2 2-5z",
    "cup": "M4 9h13v5a6 6 0 01-6 6h-1a6 6 0 01-6-6zM17 10h1.5a2.5 2.5 0 010 5H17M8 3v3M12 3v3",
    "leaf": "M5 19C5 10 10 5 20 4c-1 10-6 15-15 15zM5 19l8-8",
    "users": "M9 11a3 3 0 100-6 3 3 0 000 6zM17 12a2.5 2.5 0 100-5 2.5 2.5 0 000 5zM3 20c0-3 3-5 6-5s6 2 6 5M15.5 15.2c3 0 5.5 1.6 5.5 4.8",
    "film": "M3 5h18v14H3zM7 5v14M17 5v14M3 9h4M3 15h4M17 9h4M17 15h4",
    "abc": "M3 17l3.5-10L10 17M4.3 13.5h4.4M13 7v10h3a2.5 2.5 0 000-5h-3h2.5a2.5 2.5 0 000-5z",
})
UNIT_ICONS = ["globe", "sun", "briefcase", "building", "bag", "history",
              "heart", "compass", "cup", "leaf", "users", "film"]

# lesson kind -> (icon, label, speaking tip); the icon name is also the CSS colour class
KINDS = {
    "speaking": ("chat", "Speaking", "Give a full answer: say what, then add a reason with because or so."),
    "vocabulary": ("abc", "Vocabulary & Skills", "Use each new word in a sentence about your own life."),
    "writing": ("pen", "Speaking & Writing", "Plan your answer in note form first, then say it without reading."),
    "video": ("play", "Video", "Before you answer, say two things you already know about the topic."),
}


def kind_of(lesson):
    return lesson["kind"], lesson["title"]


def frame(inner, page_no):
    return f"""<section class="page">
 <header class="run"><span class="brand">{logo(18)}<b>IMPULSE</b><span>LEARNING CENTER</span></span>
  <span class="tag"><b>A2</b> SPEAKING BOOK</span></header>
 <div class="content">{inner}</div>
 <footer class="run"><span>© {SCHOOL} · Based on Navigate Elementary A2 speaking topics</span>
  <span class="pg">Page {page_no}</span></footer>
</section>"""


def unit_banner(u):
    titles = [l["title"] for l in u["lessons"]]
    return f"""<div class="ubanner"><div class="uno"><small>UNIT</small><span>{u["n"]}</span></div>
 <span class="uico">{icon(UNIT_ICONS[u["n"] - 1])}</span>
 <div class="ut"><h1>{e(u["title"])}</h1><p>{" · ".join(e(t) for t in titles)}</p></div>
 <div class="ustat"><b>50</b><small>questions</small></div></div>"""


def lesson_card(lesson):
    kind, title = kind_of(lesson)
    ico, label, tip = KINDS[kind]
    h = HELPERS[lesson["id"]]
    qs = "".join(f'<li><span class="qn">{q["n"]}</span><div><p>{e(q["q"])}</p><i class="line"></i></div></li>'
                 for q in lesson["questions"])
    words = "".join(f'<li><b>{e(en)}</b><span>{e(uz)}</span></li>' for en, uz in h["words"])
    starters = "".join(f"<li>{e(s)}</li>" for s in h["starters"])
    return f"""<article class="lesson wide kind-{ico}">
 <div class="lh"><span class="lico">{icon(ico)}</span>
  <div><small>LESSON {lesson["id"]} · {label.upper()}</small><h3>{e(title)}</h3></div>
  <span class="qrange">Questions {lesson["questions"][0]["n"]}–{lesson["questions"][-1]["n"]}</span></div>
 <div class="wbody">
  <ol class="qs">{qs}</ol>
  <div class="help">
   <div class="words"><h4>{icon("book")}Words &amp; phrases</h4><ul>{words}</ul></div>
   <div class="starters"><h4>{icon("bulb")}Answer starters</h4><ul>{starters}</ul></div>
   <div class="mynotes"><h4>{icon("pen")}My notes</h4>{'<i class="line"></i>' * 4}</div>
   <div class="tipbox">{icon("mic")}<p><b>Speaking tip:</b> {e(tip)}</p></div>
  </div>
 </div>
</article>"""


def review_page(u):
    checks = "".join(f'<li><i class="cbox"></i>I can talk about: <b>{e(kind_of(l)[1])}</b></li>' for l in u["lessons"])
    # IELTS Part 2-style prompts from the unit ("Describe …", "Tell me about …"), else each lesson's first question
    prompts = [q["q"] for l in u["lessons"] for q in l["questions"] if q["q"].startswith(("Describe", "Tell me about"))]
    if len(prompts) < 3:
        prompts += [l["questions"][0]["q"] for l in u["lessons"]]
    talk = "".join(f"<li>{e(q)}</li>" for q in prompts[:4])
    return f"""<article class="review wide">
 <div class="lh"><span class="lico">{icon("target")}</span>
  <div><small>UNIT {u["n"]} · REVIEW</small><h3>Check your speaking</h3></div></div>
 <div class="rgrid">
  <div class="rcol">
   <div class="rbox"><h4>{icon("mic")}Two-minute talk</h4>
    <p>Choose one question. Prepare for one minute, then speak for two minutes without stopping.</p><ul class="talk">{talk}</ul></div>
   <div class="rbox"><h4>{icon("check")}Can you do it?</h4><ul class="checks">{checks}</ul></div>
  </div>
  <div class="rbox notes"><h4>{icon("pen")}My new words and phrases</h4>{'<i class="line"></i>' * 9}</div>
 </div>
</article>"""


def cover():
    dots = "".join(f"<span>{u['n']}</span>" for u in UNITS)
    return f"""<section class="page cover"><div class="grid"></div><div class="blob b1"></div><div class="blob b2"></div>
 <div class="cbrand">{logo(64, ring=True)}<div><b>IMPULSE</b><small>LEARNING CENTER</small></div></div>
 <div class="main"><span class="kicker">LEVEL A2 · ELEMENTARY</span>
  <h1>Speaking<br><span>Book</span></h1>
  <p class="lead">600 speaking questions in 12 units, with useful words &amp; phrases,
  Uzbek translations and answer starters for every lesson.</p>
  <div class="feat"><span>600 questions</span><span>60 lessons</span><span>480 words &amp; phrases</span><span>Answer starters</span></div></div>
 <div class="card"><div class="top">{icon("chat")}<b>LESSON 2.2 · SPEAKING</b></div>
  <div class="cb"><div class="q"><span class="qn">67</span>Do you prefer to spend time alone or with friends?</div>
   <div class="chips"><span>spend time</span><span>hang out with friends</span><span>on my own</span></div>
   <div class="st">{icon("bulb")}<span>I prefer spending time with friends because it’s more fun.</span></div></div></div>
 <div class="cfoot"><div><b>{SCHOOL}</b> · Based on Navigate Elementary A2 speaking topics</div>
  <div class="units">{dots}</div></div>
</section>"""


def how_to():
    steps = [
        ("chat", "Ask and answer", "Work in pairs. One student asks the questions, the other answers. Then swap."),
        ("book", "Check the words", "Look at <b>Words &amp; phrases</b> before you start. Use at least three in your answers."),
        ("bulb", "Use a starter", "Begin with an <b>answer starter</b>, then add your own ideas."),
        ("mic", "Say more", "Answer + reason (<i>because…</i>) + example (<i>for example…</i>)."),
    ]
    step_html = "".join(f'<div class="step"><span class="sico">{icon(i)}</span><b>{n}. {t}</b><p>{d}</p></div>'
                        for n, (i, t, d) in enumerate(steps, 1))
    kinds = "".join(f'<div class="kind kind-{i}"><span class="lico">{icon(i)}</span><div><b>{l}</b><p>{e(t)}</p></div></div>'
                    for i, l, t in KINDS.values())
    return f"""<section class="page"><div class="inner">
 <div class="ptitle">{logo(30)}<h2>How to use this book</h2><div class="bar"></div><small>{SCHOOL.upper()}</small></div>
 <div class="steps">{step_html}</div>
 <div class="hgrid">
  <div class="stack">
   <div class="box"><h3>Four kinds of lessons</h3>{kinds}</div>
  </div>
  <div class="stack">
   <div class="box"><h3>Make your answer longer</h3>
    <table class="ext"><tr><td>A1</td><td>I like my city.</td></tr>
    <tr><td>A2</td><td>I like my city because it’s friendly and there’s a lot to do.</td></tr>
    <tr><td>A2+</td><td>I really like my city because it’s friendly and there’s a lot to do. For example, I often go to the park with my friends. However, the traffic can be terrible.</td></tr></table>
    <h3 style="margin-top:12px">Linking words</h3>
    <div class="links"><span>and</span><span>also</span><span>but</span><span>however</span><span>because</span><span>so</span><span>for example</span><span>first</span><span>then</span><span>finally</span><span>In my opinion…</span></div></div>
   <div class="box"><h3>Need time to think?</h3><ul class="checks big">
    <li>“That’s a good question.”</li><li>“Let me think …”</li><li>“Well, I’m not sure, but I think …”</li></ul></div>
  </div>
 </div>
</div><div class="pfoot"><span><b>{SCHOOL}</b> · A2 Speaking Book</span><span>Navigate Elementary A2</span></div></section>"""


def contents(unit_pages):
    cards = "".join(f"""<a><div class="h"><span class="tico">{icon(UNIT_ICONS[u["n"] - 1])}</span><span><small>UNIT</small><b>{u["n"]}</b></span></div>
  <div class="c"><h4>{e(u["title"])}</h4><ul>{"".join(f"<li>{e(l['title'])}</li>" for l in u["lessons"])}</ul>
  <div class="meta"><span>Q {u["lessons"][0]["questions"][0]["n"]}–{u["lessons"][-1]["questions"][-1]["n"]}</span><span class="pg">p. {unit_pages[u["n"]]}</span></div></div></a>"""
                    for u in UNITS)
    return f"""<section class="page"><div class="inner">
 <div class="ptitle">{logo(30)}<h2>Contents</h2><div class="bar"></div><small>12 UNITS · 60 LESSONS</small></div>
 <div class="toc six">{cards}</div>
</div><div class="pfoot"><span><b>{SCHOOL}</b> · A2 Speaking Book</span><span>Navigate Elementary A2</span></div></section>"""


def build():
    front = [cover(), how_to()]
    p = len(front) + 2
    body, unit_pages = [], {}
    for u in UNITS:
        unit_pages[u["n"]] = p
        for i, l in enumerate(u["lessons"]):
            body.append(frame((unit_banner(u) if i == 0 else "") + lesson_card(l), p))
            p += 1
        body.append(frame(review_page(u), p))
        p += 1
    pages = front + [contents(unit_pages)] + body
    css = "".join((ROOT / "scripts" / f).read_text(encoding="utf-8") for f in ("style.css", "style_a2.css"))
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{SCHOOL} — A2 Speaking Book</title><style>{css}</style></head><body>{''.join(pages)}</body></html>"""
    (ROOT / "dist" / "a2-speaking-book.html").write_text(doc, encoding="utf-8")
    print("pages:", len(pages))


if __name__ == "__main__":
    build()
