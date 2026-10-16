"""Build the Impulse Learning Center A2 Speaking Book (HTML -> dist/a2-speaking-book.html).

A more formal companion to the A1 book: navy and white, serif headings,
one lesson per page and a full opener page for each unit.
  cover · how to use · contents · per unit: opener + 5 lesson pages
"""
import json
from pathlib import Path

from build import ICONS, e, icon, logo

ROOT = Path(__file__).resolve().parent.parent
UNITS = json.loads((ROOT / "data" / "a2-questions.json").read_text(encoding="utf-8"))
SCHOOL = "Impulse Learning Center"
BOOK = "A2 Speaking Book"

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
    "quote": "M7 7h4v4c0 3-1.5 5-4 6M15 7h4v4c0 3-1.5 5-4 6",
    "flag": "M5 21V4M5 4h11l-2 4 2 4H5",
    "list": "M9 6h11M9 12h11M9 18h11M4 6h.5M4 12h.5M4 18h.5",
})
UNIT_ICONS = ["globe", "sun", "briefcase", "building", "bag", "history",
              "heart", "compass", "cup", "leaf", "users", "film"]

KINDS = {
    "speaking": ("chat", "Speaking", "Give a full answer: say what, then add a reason with because or so."),
    "vocabulary": ("abc", "Vocabulary & Skills", "Use each new word in a sentence about your own life."),
    "writing": ("pen", "Speaking & Writing", "Plan your answer in note form first, then say it without reading."),
    "video": ("play", "Video", "Before you answer, say two things you already know about the topic."),
}


def kind_of(lesson):
    t = lesson["title"]
    if t.startswith("Video"):
        return "video", t.split(":", 1)[1].strip()
    if t.startswith("Vocabulary"):
        return "vocabulary", "Vocabulary & Skills Development"
    if t.startswith("Speaking & Writing"):
        return "writing", "Speaking & Writing"
    return "speaking", t


def load_helpers():
    helpers, cur = {}, None
    for line in (ROOT / "data" / "a2-helpers.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("## "):
            cur = helpers.setdefault(line[3:], {"words": [], "starters": []})
        elif line.startswith("w: "):
            cur["words"].append(tuple(line[3:].split(" = ", 1)))
        elif line.startswith("s: "):
            cur["starters"].append(line[3:])
    return helpers


HELPERS = load_helpers()


def frame(inner, page_no, unit=None):
    left = (f'<span class="crumb">UNIT {unit["n"]} <i>·</i> {e(unit["title"].upper())}</span>' if unit
            else '<span class="crumb">A2 SPEAKING BOOK</span>')
    return f"""<section class="page">
 <header class="run"><span class="brand">{logo(17)}<b>IMPULSE</b> LEARNING CENTER</span>{left}</header>
 <div class="content">{inner}</div>
 <footer class="run"><span>{SCHOOL} · Navigate A2 Elementary speaking topics</span><span class="pg">{page_no}</span></footer>
</section>"""


def lesson_page(unit, lesson, page_no):
    kind, title = kind_of(lesson)
    ico, label, tip = KINDS[kind]
    h = HELPERS[lesson["id"]]
    qs = "".join(f'<li><span class="qn">{q["n"]}</span><p>{e(q["q"])}</p></li>' for q in lesson["questions"])
    words = "".join(f"<tr><td>{e(en)}</td><td>{e(uz)}</td></tr>" for en, uz in h["words"])
    starters = "".join(f"<li>{e(s)}</li>" for s in h["starters"])
    inner = f"""<div class="lhead kind-{kind}">
  <div class="lid"><small>LESSON</small><b>{lesson["id"]}</b></div>
  <div class="ltitle"><span class="kind">{icon(ico)}{label}</span><h2>{e(title)}</h2></div>
  <div class="lrange">Questions {lesson["questions"][0]["n"]}–{lesson["questions"][-1]["n"]}</div>
 </div>
 <div class="lbody">
  <ol class="qs">{qs}</ol>
  <aside>
   <div class="panel"><h4>{icon("book")}Key vocabulary</h4><table class="vocab">{words}</table></div>
   <div class="panel"><h4>{icon("quote")}Useful language</h4><ul class="lang">{starters}</ul></div>
   <div class="tip">{icon("bulb")}<p><b>Speaking tip.</b> {e(tip)}</p></div>
  </aside>
 </div>"""
    return frame(inner, page_no, unit)


def opener_page(unit, page_no, first_lesson_page):
    rows = []
    for i, l in enumerate(unit["lessons"]):
        kind, title = kind_of(l)
        ico, label, _ = KINDS[kind]
        rows.append(f"""<tr><td class="oid">{l["id"]}</td><td class="oico kind-{kind}">{icon(ico)}</td>
   <td><b>{e(title)}</b><small>{label}</small></td>
   <td class="oq">Q {l["questions"][0]["n"]}–{l["questions"][-1]["n"]}</td><td class="opg">p. {first_lesson_page + i}</td></tr>""")
    topics = [kind_of(l)[1] for l in unit["lessons"] if kind_of(l)[0] in ("speaking", "video")]
    goals = "".join(f'<li><i class="cbox"></i>talk about <b>{e(t)}</b></li>' for t in topics)
    inner = f"""<div class="opener">
  <div class="oleft">
   <span class="ounit">UNIT</span><span class="onum">{unit["n"]:02d}</span>
   <span class="oico-big">{icon(UNIT_ICONS[unit["n"] - 1])}</span>
   <h1>{e(unit["title"])}</h1>
   <p>5 lessons · 50 questions</p>
  </div>
  <div class="oright">
   <h3>{icon("list")}In this unit</h3>
   <table class="olist">{''.join(rows)}</table>
   <div class="ogrid">
    <div class="obox"><h3>{icon("flag")}Unit goals</h3><p>By the end of this unit I can:</p><ul class="goals">{goals}</ul></div>
    <div class="obox"><h3>{icon("mic")}Two-minute talk</h3>
     <p>Choose one topic from this unit. Prepare for one minute, then speak for two minutes without stopping.</p>
     <ul class="steps"><li>Introduce the topic</li><li>Give two or three details</li><li>Give your opinion and a reason</li><li>Finish with a short conclusion</li></ul></div>
   </div>
  </div>
 </div>"""
    return frame(inner, page_no, unit)


def cover():
    return f"""<section class="page cover">
 <div class="stripe"></div><div class="lines"></div>
 <div class="cbrand">{logo(58, ring=True)}<div><b>IMPULSE</b><small>LEARNING CENTER</small></div></div>
 <div class="ctext">
  <span class="kicker">LEVEL A2 · ELEMENTARY</span>
  <h1>Speaking<br>Book</h1>
  <div class="rule"></div>
  <p>600 discussion questions in 12 units, with key vocabulary,
  Uzbek translations and useful language for every lesson.</p>
 </div>
 <div class="cstats"><div><b>600</b><span>questions</span></div><div><b>60</b><span>lessons</span></div>
  <div><b>480</b><span>key words</span></div><div><b>12</b><span>units</span></div></div>
 <div class="cfoot"><span>{SCHOOL}</span><span>Based on Navigate A2 Elementary</span></div>
</section>"""


def how_to():
    kinds = "".join(f"""<div class="krow kind-{k}"><span class="kico">{icon(i)}</span><div><b>{l}</b><p>{e(t)}</p></div></div>"""
                    for k, (i, l, t) in KINDS.items())
    return f"""<section class="page plain"><div class="inner">
 <div class="ptitle"><h2>How to use this book</h2><span class="sub">{SCHOOL}</span></div>
 <div class="hcols">
  <div>
   <h3 class="sec">Each lesson page</h3>
   <ol class="anat">
    <li><b>Ten questions</b> on one topic. Work in pairs: one person asks, the other answers, then swap.</li>
    <li><b>Key vocabulary</b> with Uzbek translations. Check these words before you start speaking.</li>
    <li><b>Useful language</b> — sentence frames to start and organise your answers.</li>
    <li><b>Speaking tip</b> — one strategy to make your answer better.</li>
   </ol>
   <h3 class="sec">Four kinds of lessons</h3>
   <div class="kinds">{kinds}</div>
  </div>
  <div>
   <h3 class="sec">Build a better answer</h3>
   <table class="ladder">
    <tr><td>A1</td><td>I like my city.</td></tr>
    <tr><td>A2</td><td>I like my city because it’s friendly and there’s a lot to do.</td></tr>
    <tr><td>A2+</td><td>I really like my city because it’s friendly and there’s a lot to do. For example, at weekends I often go to the park with my friends. However, the traffic can be terrible.</td></tr>
   </table>
   <h3 class="sec">Linking words</h3>
   <table class="links">
    <tr><td>Adding</td><td>and · also · as well</td></tr>
    <tr><td>Contrast</td><td>but · however · although</td></tr>
    <tr><td>Reason / result</td><td>because · so</td></tr>
    <tr><td>Example</td><td>for example · such as</td></tr>
    <tr><td>Opinion</td><td>I think … · In my opinion …</td></tr>
    <tr><td>Sequence</td><td>first · then · after that · finally</td></tr>
   </table>
   <h3 class="sec">When you need time to think</h3>
   <p class="fill">“That’s a good question.” · “Let me think …” · “Well, I’m not sure, but …”</p>
  </div>
 </div>
</div><div class="pfoot"><span>{SCHOOL} · {BOOK}</span><span>Navigate A2 Elementary</span></div></section>"""


def contents(unit_pages):
    rows = "".join(f"""<a class="tunit"><span class="tn">{u["n"]:02d}</span><span class="ti">{icon(UNIT_ICONS[u["n"] - 1])}</span>
  <span class="tt"><b>{e(u["title"])}</b><small>{" · ".join(e(kind_of(l)[1]) for l in u["lessons"] if kind_of(l)[0] in ("speaking", "video"))}</small></span>
  <span class="tp">{unit_pages[u["n"]]}</span></a>""" for u in UNITS)
    return f"""<section class="page plain"><div class="inner">
 <div class="ptitle"><h2>Contents</h2><span class="sub">12 units · 60 lessons · 600 questions</span></div>
 <div class="toc">{rows}</div>
</div><div class="pfoot"><span>{SCHOOL} · {BOOK}</span><span>Navigate A2 Elementary</span></div></section>"""


def build():
    front = [cover(), how_to()]
    p = len(front) + 2
    body, unit_pages = [], {}
    for u in UNITS:
        unit_pages[u["n"]] = p
        body.append(opener_page(u, p, p + 1))
        p += 1
        for l in u["lessons"]:
            body.append(lesson_page(u, l, p))
            p += 1
    pages = front + [contents(unit_pages)] + body
    css = (ROOT / "scripts" / "style_a2.css").read_text(encoding="utf-8")
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{SCHOOL} — {BOOK}</title><style>{css}</style></head><body>{''.join(pages)}</body></html>"""
    (ROOT / "dist" / "a2-speaking-book.html").write_text(doc, encoding="utf-8")
    print("pages:", len(pages))


if __name__ == "__main__":
    build()
