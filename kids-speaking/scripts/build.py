"""Build "Talk Time! 1" — the Teen2Teen 1 kids' speaking book (A5, playful, like Speak Up! A2) -> dist/talk-time.html.

Each unit (4 pages): Word bank + pair game → Grammar helper + Talk time (Q1-5)
→ More talk (Q6-10) + sample answers + class survey → Game time + My mini talk + I can.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UNITS = [json.loads(f.read_text(encoding="utf-8")) for f in sorted((ROOT / "data" / "units").glob("*.json"))]
BOOK = "Talk Time! 1"
e = html.escape

SECTIONS = {
    "words": (1, "Word Bank", "Rasmlarga qarang, so‘zlarni ovoz chiqarib ayting va belgilang.", "c-green", "📚"),
    "grammar": (2, "Grammar Helper", "Namunaga qarab o‘zingiz haqingizda gap tuzing.", "c-blue", "🧩"),
    "talk": (3, "Talk Time", "Savollarga javob bering. Yordamchi gaplardan foydalaning!", "c-orange", "🗣️"),
    "more": (4, "More Talk", "Sherigingiz bilan navbatma-navbat so‘rang va javob bering.", "c-pink", "💬"),
    "survey": (5, "Class Survey", "4 ta sinfdoshingizdan so‘rang va javoblarini yozing.", "c-purple", "📋"),
    "game": (6, "Game Time", "O‘ynang va faqat ingliz tilida gapiring!", "c-yellow", "🎲"),
    "mini": (7, "My Mini Talk", "Rejaga qarab o‘zingiz haqingizda 30 soniya gapiring.", "c-teal", "🎤"),
}
PALETTE = ["#22C55E", "#FF8A1F", "#2F9BFF", "#F0549A", "#8B5CF6", "#14B8A6", "#F5B800", "#EF4444"]


def rich(text):
    return re.sub(r"\*\*(.+?)\*\*", r"<mark>\1</mark>", e(text)).replace("…", '<i class="gapd">…</i>')


EMOJI = re.compile("([\U0001F000-\U0001FAFF☀-➿⬀-⯿⌀-⏿]"
                   "(?:️|‍[\U0001F000-\U0001FAFF☀-➿]️?|[\U0001F3FB-\U0001F3FF])*"
                   "|[\U0001F1E6-\U0001F1FF]{2})")


def color_emoji(markup):
    """Wrap every emoji in a span that uses the colour emoji font."""
    return EMOJI.sub(r'<span class="em">\1</span>', markup)


def section(key, extra=""):
    n, title, uz, cls, emo = SECTIONS[key]
    return f"""<div class="sec {cls}"><div class="sechead"><span class="secno">{n}</span><h2>{title}</h2><span class="secemo">{emo}</span>{extra}</div>
  <p class="secuz">{e(uz)}</p></div>"""


def page(inner, n, unit=None, cls=""):
    tab = f'<span class="tab {unit["color"]}">{unit["n"]}</span>' if unit else ""
    return f"""<section class="page {cls}">{tab}
 <div class="content">{inner}</div>
 <footer><span>{BOOK} · Teen2Teen 1</span><span class="pno">{n}</span></footer>
</section>"""


def qblock(qs, starters, start):
    return "".join(f'<li><span class="qn">{i}</span><div><p>{e(q)}</p><p class="starter">💡 {rich(s)}</p></div></li>'
                   for i, (q, s) in enumerate(zip(qs, starters), start))


# ---------------- unit pages ----------------
def p_words(u):
    cards = "".join(f'<li><span class="wemo">{emo}</span><b>{e(en)}</b><small>{e(uz)}</small><i class="box"></i></li>'
                    for en, uz, emo in u["words"])
    return f"""<div class="uhead {u["color"]}"><div class="utitle"><small>UNIT {u["n"]}</small><h1>{e(u["title"])}</h1></div><span class="uemo">{u["emoji"]}</span></div>
 <div class="topics"><span>🧩 {e(u["grammar"])}</span><span>📚 {e(u["vocab_topic"])}</span></div>
 {section("words", f'<span class="count">{len(u["words"])} words</span>')}
 <ul class="wcards">{cards}</ul>
 <div class="pairgame"><span>👉</span><div><b>Point &amp; say!</b><small>{e(u["pair_game"])}</small></div><span>👈</span></div>"""


def p_grammar_talk(u):
    g = u["grammar_box"]
    rows = "".join(f"<tr><td><b>{e(a)}</b></td><td><span class='gf'>{e(b)}</span></td><td>{rich(c)}</td></tr>" for a, b, c in g["rows"])
    return f"""{section("grammar")}
 <div class="gbox"><h3>{e(g["title"])}</h3><table>{rows}</table><p class="gtip">⭐ {rich(g["tip"])}</p></div>
 {section("talk")}
 <ol class="klist">{qblock(u["questions"][:5], u["starters"][:5], 1)}</ol>"""


def p_more(u):
    samples = "".join(f'<div class="ans"><b>❓ {e(q)}</b><p>{rich(a)}</p></div>' for q, a in u["samples"])
    s = u["survey"]
    heads = "".join(f"<th>{e(c)}</th>" for c in s["columns"])
    rows = "".join("<tr>" + "<td></td>" * len(s["columns"]) + "</tr>" for _ in range(4))
    return f"""{section("more")}
 <ol class="klist pink">{qblock(u["questions"][5:], u["starters"][5:], 6)}</ol>
 <div class="samples"><h3 class="sub">🌟 Example answers</h3>{samples}</div>
 {section("survey")}
 <div class="survey"><h3>🙋 {e(s["question"])}</h3><table><tr>{heads}</tr>{rows}</table></div>"""


def dice_face(n):
    pos = {1: [(50, 50)], 2: [(28, 28), (72, 72)], 3: [(25, 25), (50, 50), (75, 75)],
           4: [(28, 28), (72, 28), (28, 72), (72, 72)], 5: [(25, 25), (75, 25), (50, 50), (25, 75), (75, 75)],
           6: [(28, 22), (72, 22), (28, 50), (72, 50), (28, 78), (72, 78)]}[n]
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="9"/>' for x, y in pos)
    return f'<svg class="die" viewBox="0 0 100 100"><rect x="4" y="4" width="92" height="92" rx="20"/><g>{dots}</g></svg>'


def spinner(n):
    segs, cx, cy, r = "", 50, 50, 46
    import math
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n - math.pi / 2, 2 * math.pi * (i + 1) / n - math.pi / 2
        x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
        am = (a0 + a1) / 2
        tx, ty = cx + r * .66 * math.cos(am), cy + r * .66 * math.sin(am)
        segs += (f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f} Z" fill="{PALETTE[i % 8]}"/>'
                 f'<text x="{tx:.1f}" y="{ty + 4:.1f}">{i + 1}</text>')
    return (f'<svg class="wheel" viewBox="0 0 100 100"><circle cx="50" cy="50" r="49" fill="#13235B"/>{segs}'
            f'<circle cx="50" cy="50" r="7" fill="#fff" stroke="#13235B" stroke-width="2"/></svg>')


def game_html(gm):
    t, items = gm["type"], gm["items"]
    if t == "find":
        body = "".join(f'<li><span>🔎 …{rich(it)}</span><i class="nameline"></i></li>' for it in items)
        return f'<ul class="gfind">{body}</ul>'
    if t == "dice":
        body = "".join(f'<li>{dice_face(i)}<span>{rich(it)}</span></li>' for i, it in enumerate(items, 1))
        return f'<ul class="gdice">{body}</ul>'
    if t == "board":
        cells = ['<li class="startc">🚀 START</li>'] + [f'<li style="--bc:{PALETTE[i % 8]}"><b>{i + 1}</b>{rich(it)}</li>'
                                                       for i, it in enumerate(items)] + ['<li class="finishc">🏁 FINISH</li>']
        rows, k = [], 0
        for r, size in enumerate([4, 4, 3, 3]):
            row = cells[k:k + size]
            k += size
            rows.append(f'<ul class="brow{" rev" if r % 2 else ""}">{"".join(row)}</ul>')
        return f'<div class="gboard">{"".join(rows)}</div>'
    if t == "spinner":
        lst = "".join(f'<li><b style="background:{PALETTE[i % 8]}">{i + 1}</b>{rich(it)}</li>' for i, it in enumerate(items))
        return (f'<div class="gspin"><div class="wheelbox">{spinner(len(items))}<small>📎 Use a pencil and a paper clip!</small></div>'
                f'<ol>{lst}</ol></div>')
    if t == "bingo":
        cells = "".join(f'<li>{rich(it)}</li>' for it in items)
        return f'<ul class="gbingo">{cells}</ul>'
    if t == "guess":
        cards = "".join(f'<li><span>🕵️</span><p>{rich(it)}</p><i class="nameline"></i></li>' for it in items)
        return f'<ul class="gguess">{cards}</ul>'
    raise ValueError(t)


def p_game(u):
    gm, m = u["game"], u["mini_talk"]
    steps = "".join(f'<li><span>{i}</span>{e(s)}</li>' for i, s in enumerate(m["plan"], 1))
    can = "".join(f'<li><span class="stars">☆☆☆</span>I can {e(c)}.</li>' for c in u["cando"])
    return f"""{section("game")}
 <div class="game"><h3>{e(gm["title"])}</h3><p class="rules">{rich(gm["rules"])}</p>{game_html(gm)}</div>
 {section("mini")}
 <div class="mini"><h3>🎯 {e(m["title"])}</h3><ol class="steps">{steps}</ol>
  <p class="model"><b>Example:</b> {rich(m["model"])}</p>
  <div class="timer">⏱️ Try 3 times: <i></i><i></i><i></i></div></div>
 <div class="cando"><h3>🏆 Now I can … <small>Colour the stars!</small></h3><ul>{can}</ul></div>"""


# ---------------- front matter ----------------
def cover():
    stickers = "".join(f'<span class="{cls}">{emo} {title}</span>' for _, title, _, cls, emo in SECTIONS.values())
    return f"""<section class="page cover"><div class="dots"></div><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
 <div class="floaters"><span>👋</span><span>🎈</span><span>⭐</span><span>🎲</span><span>💬</span></div>
 <div class="ctitle"><span class="kicker">TEEN2TEEN 1 · SPEAKING</span>
  <h1>Talk<br>Time! <span>🗣️</span></h1>
  <p>12 units · 120 questions · <b>games &amp; fun!</b></p>
  <p class="uz">Savollar, o‘yinlar va so‘zlar bilan ingliz tilida gapirishni o‘rganamiz!</p></div>
 <div class="cstick">{stickers}</div>
 <div class="cfoot">🧒 For young learners · A1 · 🇺🇿 Uzbek support</div>
</section>"""


def how_page():
    rows = "".join(f'<li class="{cls}"><span class="secno">{n}</span><div><b>{emo} {title}</b><small>{e(uz)}</small></div></li>'
                   for n, title, uz, cls, emo in SECTIONS.values())
    return f"""<section class="page"><div class="content">
 <div class="howhead"><h1>How to use<br>this book</h1><span>🗺️</span></div>
 <p class="howintro">Every unit has 4 fun pages and 7 steps. Do them in order with a friend!
  <span>Har bir unit 4 sahifa va 7 bosqichdan iborat. Do‘stingiz bilan ketma-ket bajaring!</span></p>
 <ol class="howlist">{rows}</ol>
 <div class="golden"><b>🥇 Golden rule:</b> speak English, speak <u>out loud</u> and have fun!
  <span>Ingliz tilida, ovoz chiqarib gapiring va zavqlaning!</span></div>
</div><footer><span>{BOOK} · Teen2Teen 1</span><span class="pno">2</span></footer></section>"""


def build():
    pages, n = [cover(), how_page()], 3
    for u in UNITS:
        for make in (p_words, p_grammar_talk, p_more, p_game):
            pages.append(page(make(u), n, u))
            n += 1
    css = (ROOT / "scripts" / "style.css").read_text(encoding="utf-8") + (ROOT / "scripts" / "kids.css").read_text(encoding="utf-8")
    fonts = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700'
             '&family=Nunito:ital,wght@0,500;0,700;0,800;0,900;1,500;1,700&display=block">')
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{BOOK}</title>
{fonts}<style>{css}</style></head><body>{color_emoji(''.join(pages))}</body></html>"""
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / "talk-time.html").write_text(doc, encoding="utf-8")
    print("pages:", len(pages))


if __name__ == "__main__":
    build()
