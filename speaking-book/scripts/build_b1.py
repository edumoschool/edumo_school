"""Build the Impulse Learning Center B1 Speaking Book (HTML -> dist/b1-speaking-book.html).

IELTS-style: every topic has Part 1 questions, a Part 2 cue card and Part 3
discussion questions, plus words & phrases (Uzbek), useful language and notes.
Part 1 + Part 2 come from data/b1-questions.json (the B1_Speaking.docx);
Part 3, vocabulary and useful language from data/b1-content.txt.
Same design as the A1/A2 books (style.css + style_a2.css + style_b1.css).
  cover · how to use · contents · per unit: 5 topic pages + mock-test page
"""
import json
import re
from pathlib import Path

from build import e, icon, logo
import build_a2  # noqa: F401  (registers the extra icons)

ROOT = Path(__file__).resolve().parent.parent
SCHOOL = "Impulse Learning Center"
BOOK = "B1 Speaking Book"

UNIT_INFO = [  # title, icon
    ("Everyday Life", "clock"),
    ("My Town", "building"),
    ("Experiences and Memories", "history"),
    ("Changes and the Future", "send"),
    ("Possessions and Money", "bag"),
    ("Health and Wellbeing", "heart"),
]
# Part 1 questions replaced because they only make sense in a classroom
PART1_FIX = {
    ("1.4", 2): "Do you check your phone or emails as soon as you wake up?",
}


def load():
    topics = json.loads((ROOT / "data" / "b1-questions.json").read_text(encoding="utf-8"))
    extra, cur = {}, None
    for line in (ROOT / "data" / "b1-content.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("## "):
            cur = extra.setdefault(line[3:], {"p3": [], "words": [], "starters": []})
        elif line.startswith("p3: "):
            cur["p3"].append(line[4:])
        elif line.startswith("w: "):
            cur["words"].append(tuple(line[3:].split(" = ", 1)))
        elif line.startswith("s: "):
            cur["starters"].append(line[3:])
    units = []
    for t in topics:
        u = int(t["id"].split(".")[0])
        if len(units) < u:
            units.append({"n": u, "title": UNIT_INFO[u - 1][0], "icon": UNIT_INFO[u - 1][1], "topics": []})
        m = re.match(r"(.+?)\s*\((.+)\)$", t["title"])
        title, sub = (m.group(1), m.group(2)) if m else (t["title"], "")
        part1 = [PART1_FIX.get((t["id"], i), q) for i, q in enumerate(t["part1"])]
        units[-1]["topics"].append({**t, **extra[t["id"]], "title": title[0].upper() + title[1:], "sub": sub,
                                    "part1": part1})
    return units


UNITS = load()


def frame(inner, page_no):
    return f"""<section class="page">
 <header class="run"><span class="brand">{logo(18)}<b>IMPULSE</b><span>LEARNING CENTER</span></span>
  <span class="tag"><b>B1</b> SPEAKING BOOK · IELTS STYLE</span></header>
 <div class="content">{inner}</div>
 <footer class="run"><span>© {SCHOOL} · B1 speaking topics in IELTS Speaking format</span>
  <span class="pg">Page {page_no}</span></footer>
</section>"""


def unit_banner(u):
    titles = " · ".join(e(t["title"]) for t in u["topics"])
    return f"""<div class="ubanner"><div class="uno"><small>UNIT</small><span>{u["n"]}</span></div>
 <span class="uico">{icon(u["icon"])}</span>
 <div class="ut"><h1>{e(u["title"])}</h1><p>{titles}</p></div>
 <div class="ustat"><b>5</b><small>topics</small></div></div>"""


def numbered(qs):
    return "".join(f'<li><span class="qn">{i}</span><p>{e(q)}</p></li>' for i, q in enumerate(qs, 1))


def cue_card(t, cls="cue"):
    say = "".join(f"<li>{e(s)}</li>" for s in t["say"])
    return f"""<div class="{cls}"><div class="cuehead"><b>PART 2 · CUE CARD</b><span>1 min to prepare · 1–2 min to speak</span></div>
  <p class="cueq">{e(t["cue"])}</p><p class="say">You should say:</p><ul>{say}</ul><p class="explain">{e(t["explain"])}</p></div>"""


def topic_page(t):
    words = "".join(f'<li><b>{e(en)}</b><span>{e(uz)}</span></li>' for en, uz in t["words"])
    starters = "".join(f"<li>{e(s)}</li>" for s in t["starters"])
    sub = f'<span class="tsub">{e(t["sub"])}</span>' if t["sub"] else ""
    return f"""<article class="lesson wide ielts kind-chat">
 <div class="lh"><span class="lico">{icon("mic")}</span>
  <div><small>TOPIC {t["id"]} · IELTS SPEAKING · PARTS 1–3</small><h3>{e(t["title"])}{sub}</h3></div></div>
 <div class="wbody">
  <div class="parts3">
   <div class="pbox1"><h4>{icon("chat")}Part 1 · Interview</h4><ol class="qs">{numbered(t["part1"])}</ol></div>
   {cue_card(t)}
   <div class="pbox3"><h4>{icon("users")}Part 3 · Discussion</h4><ol class="qs">{numbered(t["p3"])}</ol></div>
  </div>
  <div class="help">
   <div class="words"><h4>{icon("book")}Words &amp; phrases</h4><ul>{words}</ul></div>
   <div class="starters"><h4>{icon("bulb")}Useful language</h4><ul>{starters}</ul></div>
   <div class="mynotes"><h4>{icon("pen")}Cue card notes</h4>{'<i class="line"></i>' * 4}</div>
  </div>
 </div>
</article>"""


def mock_page(u):
    t = u["topics"]
    part1 = [x["part1"][0] for x in t[:4]]
    part3 = [t[1]["p3"][0], t[3]["p3"][0], t[4]["p3"][1]]
    checks = "".join(f'<li><i class="cbox"></i>I can talk about: <b>{e(x["title"])}</b></li>' for x in t)
    return f"""<article class="review wide">
 <div class="lh"><span class="lico">{icon("target")}</span>
  <div><small>UNIT {u["n"]} · REVIEW</small><h3>Mock speaking test</h3></div>
  <span class="qrange">About 11–14 minutes · work in pairs: examiner and candidate</span></div>
 <div class="rgrid">
  <div class="rcol">
   <div class="rbox"><h4>{icon("chat")}Part 1 · 4–5 minutes</h4><ol class="qs mock">{numbered(part1)}</ol></div>
   {cue_card(t[2], "cue mockcue")}
   <div class="rbox"><h4>{icon("users")}Part 3 · 4–5 minutes</h4><ol class="qs mock">{numbered(part3)}</ol></div>
  </div>
  <div class="rcol">
   <div class="rbox"><h4>{icon("check")}Can you do it?</h4><ul class="checks">{checks}</ul></div>
   <div class="rbox notes"><h4>{icon("pen")}Examiner’s feedback / my new words</h4>{'<i class="line"></i>' * 6}</div>
  </div>
 </div>
</article>"""


def cover():
    dots = "".join(f"<span>{u['n']}</span>" for u in UNITS)
    t = UNITS[0]["topics"][0]
    say = "".join(f"<li>{e(s)}</li>" for s in t["say"])
    return f"""<section class="page cover"><div class="grid"></div><div class="blob b1"></div><div class="blob b2"></div>
 <div class="cbrand">{logo(64, ring=True)}<div><b>IMPULSE</b><small>LEARNING CENTER</small></div></div>
 <div class="main"><span class="kicker">LEVEL B1 · INTERMEDIATE · IELTS STYLE</span>
  <h1>Speaking<br><span>Book</span></h1>
  <p class="lead">30 IELTS-style speaking topics with Part 1 questions, Part 2 cue cards and Part 3
  discussions, plus useful vocabulary with Uzbek translations.</p>
  <div class="feat"><span>30 topics</span><span>30 cue cards</span><span>240 questions</span><span>240 words &amp; phrases</span><span>6 mock tests</span></div></div>
 <div class="card"><div class="top">{icon("mic")}<b>PART 2 · CUE CARD</b></div>
  <div class="cb"><div class="q">{e(t["cue"])}</div><p class="csay">You should say:</p><ul class="csl">{say}</ul>
   <div class="st">{icon("bulb")}<span>{e(t["explain"])}</span></div></div></div>
 <div class="cfoot"><div><b>{SCHOOL}</b> · B1 speaking topics in IELTS Speaking format</div><div class="units">{dots}</div></div>
</section>"""


def how_to():
    parts = [("chat", "Part 1 · Interview", "4–5 minutes",
              "Short questions about you, your home, work, study and interests. Answer in 2–3 sentences."),
             ("mic", "Part 2 · Cue card", "3–4 minutes",
              "You get a card with a topic. Prepare for 1 minute, then speak for 1–2 minutes. Cover every point."),
             ("users", "Part 3 · Discussion", "4–5 minutes",
              "More general, abstract questions linked to Part 2. Give opinions, reasons and examples.")]
    part_html = "".join(f'<div class="step"><span class="sico">{icon(i)}</span><b>{t}</b><em>{d}</em><p>{e(x)}</p></div>'
                        for i, t, d, x in parts)
    criteria = [("Fluency & coherence", "Speak without long pauses and link your ideas (firstly, however, so)."),
                ("Vocabulary", "Use topic words and collocations from the Words & phrases box."),
                ("Grammar", "Use a mix of tenses and some longer sentences (because, when, if)."),
                ("Pronunciation", "Speak clearly, stress key words and use natural intonation.")]
    crit = "".join(f'<tr><td>{a}</td><td>{e(b)}</td></tr>' for a, b in criteria)
    return f"""<section class="page"><div class="inner">
 <div class="ptitle">{logo(30)}<h2>The IELTS Speaking test</h2><div class="bar"></div><small>{SCHOOL.upper()}</small></div>
 <div class="steps three">{part_html}</div>
 <div class="hgrid">
  <div class="stack">
   <div class="box"><h3>How you are assessed</h3><table class="ext crit">{crit}</table></div>
  </div>
  <div class="stack">
   <div class="box"><h3>Part 2: plan in one minute</h3><ul class="checks big plain2">
    <li>Write 3–5 key words for each point on the card, not full sentences.</li>
    <li>Start with: “I’m going to talk about …”</li>
    <li>Add details: who, where, when, how, why.</li>
    <li>Finish with the “explain” point — your feelings and reasons.</li></ul></div>
   <div class="box"><h3>Part 3: give a full answer</h3>
    <div class="links"><span>Opinion</span><span>Reason</span><span>Example</span><span>Other side</span></div>
    <p class="model">“I think so, yes. <b>The main reason is that</b> people work longer hours now. <b>For example,</b> my father often works until eight. <b>On the other hand,</b> technology saves us a lot of time.”</p></div>
  </div>
 </div>
</div><div class="pfoot"><span><b>{SCHOOL}</b> · {BOOK}</span><span>IELTS Speaking format</span></div></section>"""


def contents(unit_pages):
    cards = "".join(f"""<a><div class="h"><span class="tico">{icon(u["icon"])}</span><span><small>UNIT</small><b>{u["n"]}</b></span></div>
  <div class="c"><h4>{e(u["title"])}</h4><ul>{"".join(f"<li>{t['id']} {e(t['title'])}</li>" for t in u["topics"])}<li><b>Mock speaking test</b></li></ul>
  <div class="meta"><span>5 topics</span><span class="pg">p. {unit_pages[u["n"]]}</span></div></div></a>""" for u in UNITS)
    return f"""<section class="page"><div class="inner">
 <div class="ptitle">{logo(30)}<h2>Contents</h2><div class="bar"></div><small>6 UNITS · 30 TOPICS</small></div>
 <div class="toc three">{cards}</div>
</div><div class="pfoot"><span><b>{SCHOOL}</b> · {BOOK}</span><span>IELTS Speaking format</span></div></section>"""


def build():
    front = [cover(), how_to()]
    p = len(front) + 2
    body, unit_pages = [], {}
    for u in UNITS:
        unit_pages[u["n"]] = p
        for i, t in enumerate(u["topics"]):
            body.append(frame((unit_banner(u) if i == 0 else "") + topic_page(t), p))
            p += 1
        body.append(frame(mock_page(u), p))
        p += 1
    pages = front + [contents(unit_pages)] + body
    css = "".join((ROOT / "scripts" / f).read_text(encoding="utf-8") for f in ("style.css", "style_a2.css", "style_b1.css"))
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{SCHOOL} — {BOOK}</title><style>{css}</style></head><body>{''.join(pages)}</body></html>"""
    (ROOT / "dist" / "b1-speaking-book.html").write_text(doc, encoding="utf-8")
    print("pages:", len(pages))


if __name__ == "__main__":
    build()
