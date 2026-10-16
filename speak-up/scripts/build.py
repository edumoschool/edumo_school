"""Build the Impulse "Speak Up!" speaking book (A5 portrait) as HTML -> dist/speak-up.html.

Each unit follows the same 7-step speaking cycle (8 pages):
  opener · 1 key phrases · 2 listen & shadow · 3 build it · 4 remember it ·
  5 talk together · 6 fluency 3 rounds · 7 record & check
Back matter: Student B pages (info-gap cards).
Audio QR codes point to config.audio_base_url + track file name.
"""
import html
import io
import json
import re
import sys
from pathlib import Path

import qrcode
import qrcode.image.svg

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "speaking-book" / "scripts"))
from build import ICONS, icon, logo  # noqa: E402  shared icons + logo
import build_a2  # noqa: E402,F401  registers extra icons

e = html.escape
CFG = json.loads((ROOT / "data" / "config.json").read_text(encoding="utf-8"))
UNITS = [json.loads(f.read_text(encoding="utf-8")) for f in sorted((ROOT / "data" / "units").glob("*.json"))]
SCHOOL = "Impulse Learning Center"
ICONS.update({
    "headphones": "M4 14v-2a8 8 0 0116 0v2M4 14h3v6H5a1 1 0 01-1-1zM20 14h-3v6h2a1 1 0 001-1z",
    "repeat": "M17 2l4 4-4 4M3 11V9a3 3 0 013-3h15M7 22l-4-4 4-4M21 13v2a3 3 0 01-3 3H3",
    "timer": "M12 21a8 8 0 100-16 8 8 0 000 16zM12 9v4l2 2M9 2h6",
    "brain": "M9 4a3 3 0 00-3 3 3 3 0 00-2 5 3 3 0 002 5 3 3 0 006 0V4a3 3 0 00-3 0zM15 4a3 3 0 013 3 3 3 0 012 5 3 3 0 01-2 5 3 3 0 01-6 0",
    "blocks": "M3 3h8v8H3zM13 3h8v8h-8zM3 13h8v8H3zM13 13h8v8h-8z",
    "swap": "M7 4L3 8l4 4M3 8h14M17 20l4-4-4-4M21 16H7",
    "stamp": "M9 3h6v6l3 3v3H6v-3l3-3zM4 19h16v2H4z",
    "tick": "M4 12l5 5L20 6",
})

STEPS = [  # name, Uzbek name, icon, colour class
    ("Key phrases", "Kerakli iboralar", "book", "s1"),
    ("Listen & shadow", "Tinglang va takrorlang", "headphones", "s2"),
    ("Build it", "Gap tuzing", "blocks", "s3"),
    ("Remember it", "Eslab qoling", "brain", "s4"),
    ("Talk together", "Sherik bilan gaplashing", "users", "s5"),
    ("Fluency: 3 rounds", "Ravonlik: 3 bosqich", "timer", "s6"),
    ("Record & check", "Yozib oling va tekshiring", "mic", "s7"),
]


def qr(file_name, label):
    url = CFG["audio_base_url"] + file_name
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=1)
    buf = io.BytesIO()
    img.save(buf)
    svg = re.sub(r"<\?xml[^>]*\?>", "", buf.getvalue().decode())
    svg = re.sub(r'width="[^"]*"\s+height="[^"]*"', 'width="100%" height="100%"', svg, count=1)
    return f'<div class="qr"><div class="qrimg">{svg}</div><div><b>{icon("headphones")}{e(label)}</b><small>Scan to listen</small></div></div>'


def page(inner, n, cls=""):
    return f"""<section class="page {cls}">
 <header class="run"><span class="brand">{logo(14)}<b>IMPULSE</b> SPEAK UP! {CFG["level"]}</span><span>{n}</span></header>
 <div class="content">{inner}</div>
</section>"""


def step_head(i, unit_n, extra=""):
    name, uz, ico, cls = STEPS[i]
    return f"""<div class="stephead {cls}"><span class="sbadge">{i + 1}</span>
  <div><small>UNIT {unit_n} · STEP {i + 1} of 7</small><h2>{icon(ico)}{name}</h2><em>{uz}</em></div>{extra}</div>"""


def how(en, uz):
    return f'<p class="how">{e(en)}<span>{e(uz)}</span></p>'


def confidence(label, uz):
    dots = "".join(f"<span>{i}</span>" for i in range(1, 6))
    return f'''<div class="conf"><div><b>{label}</b><small>{uz}</small></div><div class="dots">{dots}</div>
  <div class="scale"><small>not at all</small><small>very</small></div></div>'''


def ticks(n):
    return '<span class="tk"></span>' * n


# ---------------- unit pages ----------------
def p_opener(u):
    can = "".join(f"<li>{icon('tick')}{e(c)}</li>" for c in u["cando"])
    road = "".join(f'<li class="{c}"><b>{i + 1}</b><span>{n}</span></li>' for i, (n, _, _, c) in enumerate(STEPS))
    warm = "".join(f"<li>{e(q)}</li>" for q in u["warmup"])
    return f"""<div class="opener">
  <div class="ohead"><span class="onum"><small>UNIT</small>{u["n"]}</span><span class="oico">{icon(u["icon"])}</span><h1>{e(u["title"])}</h1></div>
  <div class="obox"><h3>In this unit I will learn to …<span>Bu bo‘limda men … o‘rganaman</span></h3><ul class="can">{can}</ul></div>
  <div class="obox warm"><h3>Warm-up<span>Juftlikda javob bering</span></h3><ol>{warm}</ol></div>
  <div class="challenge"><span class="cico">{icon("timer")}</span><div><b>1-minute challenge · BEFORE</b>
   <p>Talk about the unit topic for 1 minute. How long can you speak without stopping?</p>
   <p class="uz">Mavzu haqida 1 daqiqa gapiring. To‘xtamasdan necha soniya gapira oldingiz?</p></div>
   <div class="secs"><i></i><small>seconds</small></div></div>
  {confidence("How confident do I feel talking about this topic?", "Bu mavzuda gapirishga qanchalik ishonchim bor? (1–5)")}
  <div class="route"><h3>Your speaking route</h3><ol>{road}</ol></div>
 </div>"""


def p_phrases(u):
    rows = "".join(f"""<tr><td class="no">{i}</td><td><b>{e(en)}</b>{f'<i>{e(ex)}</i>' if ex else ''}</td><td class="uz">{e(uz)}</td><td class="ck">{ticks(1)}</td></tr>"""
                   for i, (en, uz, ex) in enumerate(u["phrases"], 1))
    n = f"u{u['n']:02d}"
    return f"""{step_head(0, u["n"], qr(f"{n}-1-phrases.mp3", f"Track {u['n']}.1"))}
 {how("Learn whole phrases, not single words. Listen, repeat each phrase in the pause, then tick the ones you can say without looking.",
      "So‘zlarni emas, tayyor iboralarni o‘rganing. Tinglang, pauzada takrorlang va qaramasdan ayta oladiganlaringizni belgilang.")}
 <table class="phr"><tr><th></th><th>English</th><th>O‘zbekcha</th><th>{icon("tick")}</th></tr>{rows}</table>"""


def p_shadow(u):
    d, n = u["dialogue"], f"u{u['n']:02d}"
    lines = "".join(f'<li class="{"a" if who == d["lines"][0][0] else "b"}"><b>{e(who)}</b><p>{e(t)}</p></li>' for who, t in d["lines"])
    p = u["pron"]
    words = " · ".join(e(w) for w in p["words"])
    return f"""{step_head(1, u["n"])}
 <div class="qrrow">{qr(f"{n}-2-dialogue.mp3", f"Track {u['n']}.2 · Dialogue")}{qr(f"{n}-3-shadowing.mp3", f"Track {u['n']}.3 · Shadowing")}</div>
 <ol class="rounds"><li><b>Listen</b> and read (Track {u['n']}.2).<span>Tinglang va o‘qing.</span></li>
  <li><b>Read aloud</b> together with the audio.<span>Audio bilan birga ovoz chiqarib o‘qing.</span></li>
  <li><b>Repeat</b> in the pauses — try not to look (Track {u['n']}.3).<span>Pauzada qaramasdan takrorlang.</span></li></ol>
 <div class="dlg"><h3>{e(d["title"])}</h3><p class="set">{e(d["setting"])}</p><ul>{lines}</ul></div>
 <div class="pron"><h3>{icon("mic")}Sound focus: {e(p["title"])}</h3><p>{e(p["tip"])}<span>{e(p["tip_uz"])}</span></p>
  <p class="pw">{words}</p><p class="ps">“{e(p["sentence"])}”</p></div>"""


def p_build(u):
    tables = ""
    for t in u["tables"]:
        cols = "".join("<td>" + "".join(f"<span>{e(x)}</span>" for x in c) + "</td>" for c in t["cols"])
        tables += f'<div class="sub"><h3>{e(t["title"])}</h3><table><tr>{cols}</tr></table></div>'
    drill = "".join(f'<tr><td class="no">{i}</td><td>{e(p)}</td><td class="ans">{e(a)}</td></tr>'
                    for i, (p, a) in enumerate(u["drill"]["items"], 1))
    return f"""{step_head(2, u["n"])}
 {how("Make sentences from the tables. Say five TRUE sentences about your family to your partner.",
      "Jadvallardan gap tuzing. Sherigingizga oilangiz haqida 5 ta TO‘G‘RI gap ayting.")}
 {tables}
 <div class="drill"><h3>{icon("timer")}{e(u["drill"]["title"])}<span>Cover the answers. Say each question in 3 seconds.</span></h3>
  <table>{drill}</table></div>"""


def p_recall(u):
    rows = "".join(f'<tr><td class="no">{i}</td><td class="uzq">{e(uz)}</td><td class="ans">{e(en)}</td><td class="ck">{ticks(3)}</td></tr>'
                   for i, (uz, en) in enumerate(u["recall"], 1))
    return f"""{step_head(3, u["n"])}
 {how("Cover the English column. Read the Uzbek sentence and SAY the English aloud. Then check. Do it again tomorrow and in one week.",
      "Inglizcha ustunni yoping. O‘zbekcha gapni o‘qib, inglizchasini OVOZ chiqarib ayting va tekshiring. Ertaga va bir haftadan keyin takrorlang.")}
 <table class="rec"><tr><th></th><th>O‘zbekcha</th><th>English (cover!)</th><th>Today · Tomorrow · Week</th></tr>{rows}</table>
 <p class="why">{icon("brain")}<b>Why?</b> Remembering a phrase from memory makes it stick much better than reading it again.
  <span>Iborani xotiradan eslash uni qayta o‘qishdan ko‘ra ancha yaxshi yodda saqlaydi.</span></p>"""


def gap_table(g, hide):
    hidden = {tuple(h) for h in hide}
    head = "".join(f"<th>{e(c)}</th>" for c in g["cols"])
    body = ""
    for r, row in enumerate(g["rows"]):
        body += "<tr>" + "".join(f'<td class="{"blank" if (r, c) in hidden else ""}">{"" if (r, c) in hidden else e(v)}</td>'
                                 for c, v in enumerate(row)) + "</tr>"
    return f'<table class="gap"><tr>{head}</tr>{body}</table>'


def p_talk(u):
    g, c = u["infogap"], u["common"]
    qs = " · ".join(e(q) for q in g["questions"])
    cq = "".join(f"<li>{e(q)}</li>" for q in c["questions"])
    return f"""{step_head(4, u["n"])}
 <div class="card"><h3><span class="role">Student A</span>{e(g["title"])}</h3>
  {how(g["intro"], g["intro_uz"])}{gap_table(g, g["hide_a"])}
  <p class="qhelp"><b>Ask:</b> {qs}</p><p class="tiny">Student B: turn to page {{B_PAGE}}.</p></div>
 <div class="card"><h3>{e(c["title"])}</h3>{how(c["intro"], "Sherigingizdan so‘rang va oilalaringizdagi 3 ta o‘xshashlikni toping.")}
  <ul class="cq">{cq}</ul><div class="same"><span>1</span><span>2</span><span>3</span></div></div>"""


def p_fluency(u):
    f, n = u["fluency"], f"u{u['n']:02d}"
    prompts = "".join(f'<div class="node"><b>{e(p)}</b><i class="line"></i><i class="line"></i></div>' for p in f["prompts"])
    return f"""{step_head(5, u["n"])}
 <p class="topic">“{e(f["topic"])}”</p>
 <div class="mind"><div class="core">{icon(u["icon"])}<b>ME</b></div>{prompts}</div>
 <p class="tiny center">Write KEY WORDS only — no full sentences. / Faqat kalit so‘zlar yozing.</p>
 <div class="r3"><div><b>2:00</b><span>Partner 1</span></div><div><b>1:30</b><span>Partner 2</span></div><div><b>1:00</b><span>Partner 3</span></div></div>
 {how("Tell the SAME story to three different partners. Each time you have less time, so you speak faster and more smoothly. Listeners: count the key phrases you hear.",
      "Bir xil hikoyani 3 xil sherigingizga ayting. Har safar vaqt kamayadi — siz tezroq va ravonroq gapirasiz. Tinglovchi: eshitgan iboralarni sanang.")}
 <div class="lcard"><h3>{icon("users")}Listener’s card<span>Tinglovchi kartasi</span></h3>
  <div class="lrow"><b>Key phrases I heard</b><span class="tally">{ticks(10)}</span></div>
  <div class="lrow"><b>One thing my partner did well</b><i class="line"></i></div>
  <div class="lrow"><b>New phrase I added in round 3</b><i class="line"></i></div></div>
 {qr(f"{n}-4-model.mp3", f"Track {u['n']}.4 · Model talk — listen AFTER you speak")}"""


def p_check(u):
    checks = "".join(f'<li><span class="tk"></span>{e(c)}</li>' for c in u["checks"])
    return f"""{step_head(6, u["n"])}
 <div class="rec7"><span class="cico">{icon("mic")}</span><div><b>Record a 1-minute voice message</b> about the topic (for example, a Telegram voice note). Listen to it once and check.
  <span>Mavzu bo‘yicha 1 daqiqalik ovozli xabar yozib oling, tinglang va tekshiring.</span></div></div>
 <div class="obox"><h3>Self-check<span>O‘zingizni tekshiring</span></h3><ul class="checks">{checks}</ul></div>
 <div class="obox"><h3>My mistakes<span>Xatolarim — keyingi safar to‘g‘ri ayting</span></h3>
  <table class="mist"><tr><th>I said …</th><th>Correct</th></tr>{'<tr><td></td><td></td></tr>' * 4}</table></div>
 {confidence("How confident do I feel now?", "Endi qanchalik ishonchim bor? (1–5)")}
 <div class="ba"><div class="challenge small"><span class="cico">{icon("timer")}</span><div><b>1-minute challenge · AFTER</b><p>Talk about the topic again. Compare!</p></div><div class="secs"><i></i><small>seconds</small></div></div>
  <div class="stampbox">{icon("stamp")}<b>Speaking passport</b><small>Teacher’s stamp / signature</small></div></div>"""


def student_b(u):
    g = u["infogap"]
    qs = " · ".join(e(q) for q in g["questions"])
    return f"""<div class="bhead"><span class="role">Student B</span><h2>Unit {u["n"]} · {e(g["title"])}</h2></div>
 <div class="card">{how(g["intro"], g["intro_uz"])}{gap_table(g, g["hide_b"])}<p class="qhelp"><b>Ask:</b> {qs}</p></div>"""


# ---------------- front matter ----------------
def cover():
    return f"""<section class="page cover"><div class="grid"></div><div class="blob b1"></div><div class="blob b2"></div>
 <div class="cbrand">{logo(44, ring=True)}<div><b>IMPULSE</b><small>LEARNING CENTER</small></div></div>
 <div class="ctitle"><span class="kicker">LEVEL {CFG["level"]} · {CFG["level_name"].upper()}</span>
  <h1>Speak<br><span>Up!</span></h1>
  <p>A step-by-step method to start speaking English — with audio for every unit.</p>
  <p class="uz">Ingliz tilida gapirishni boshlash uchun bosqichma-bosqich metod — har bir bo‘lim audio bilan.</p></div>
 <div class="csteps">{"".join(f'<span class="{c}"><b>{i + 1}</b>{n}</span>' for i, (n, _, _, c) in enumerate(STEPS))}</div>
 <div class="cfoot">{icon("headphones")}<span>Scan the QR codes to listen</span></div>
</section>"""


def method_page():
    why = [
        ("Key phrases", "Fluent speakers use ready-made phrases. Learning phrases, not single words, lets you speak faster.",
         "Tayyor iboralar bilan tezroq gapirasiz."),
        ("Listen & shadow", "Repeating after native audio trains pronunciation, rhythm and listening together.",
         "Audio ortidan takrorlash talaffuz va ritmni rivojlantiradi."),
        ("Build it", "Short pattern drills make grammar automatic — no translating in your head.",
         "Qisqa mashqlar grammatikani avtomatik qiladi."),
        ("Remember it", "Saying phrases from memory, again after 1 day and 1 week, moves them into long-term memory.",
         "Xotiradan eslash va takrorlash uzoq muddatli xotiraga o‘tkazadi."),
        ("Talk together", "Real tasks where you NEED to ask and answer — like real life, not a memorised speech.",
         "Yodlangan matn emas, haqiqiy muloqot."),
        ("Fluency: 3 rounds", "Telling the same story three times with less time (the 4-3-2 technique) makes you measurably more fluent.",
         "Bir hikoyani 3 marta qisqaroq vaqtda aytish ravonlikni oshiradi."),
        ("Record & check", "Hearing yourself shows your mistakes. Your 1-minute challenge shows your progress.",
         "O‘zingizni eshitish xatolarni ko‘rsatadi, 1 daqiqalik sinov esa o‘sishni."),
    ]
    rows = "".join(f'<li class="{STEPS[i][3]}"><b class="n">{i + 1}</b><div><b>{t}</b><p>{e(en)}</p><span>{e(uz)}</span></div></li>'
                   for i, (t, en, uz) in enumerate(why))
    return f"""<section class="page"><div class="content">
 <div class="ptitle">{logo(26)}<h2>How Speak Up! works</h2></div>
 <p class="intro">Every unit follows the same 7 steps. Each step is based on research into how people really learn to speak a foreign language.
  <span>Har bir bo‘lim 7 bosqichdan iborat. Har bir bosqich til o‘rganish bo‘yicha tadqiqotlarga asoslangan.</span></p>
 <ol class="method">{rows}</ol>
 <div class="tipline">{icon("timer")}<b>Best results:</b> one unit per week · 15 minutes of audio every day · speak with a partner twice a week.</div>
</div></section>"""


def build():
    pages, n = [cover(), method_page()], 3
    b_pages = []
    unit_pages = []
    for u in UNITS:
        for make in (p_opener, p_phrases, p_shadow, p_build, p_recall, p_talk, p_fluency, p_check):
            unit_pages.append((u, make, n))
            n += 1
    b_start = n
    body = []
    for u, make, num in unit_pages:
        html_ = make(u).replace("{B_PAGE}", str(b_start + UNITS.index(u) // 2))
        body.append(page(html_, num, "opener-page" if make is p_opener else ""))
    for i in range(0, len(UNITS), 2):
        b_pages.append(page("".join(student_b(u) for u in UNITS[i:i + 2]), b_start + i // 2))
    css = (ROOT / "scripts" / "style.css").read_text(encoding="utf-8")
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{SCHOOL} — Speak Up! {CFG["level"]}</title>
<style>{css}</style></head><body>{''.join(pages + body + b_pages)}</body></html>"""
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / "speak-up.html").write_text(doc, encoding="utf-8")
    print("pages:", len(pages) + len(body) + len(b_pages))


if __name__ == "__main__":
    build()
