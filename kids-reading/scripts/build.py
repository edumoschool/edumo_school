"""Build "Read Time! 1" — kids' reading comprehension book (A5, playful, companion to Talk Time! 1) -> dist/read-time.html.

Each unit (3 pages): Before you read + the text → True/False, Choose, Match, Fill the gaps
→ Word search, About you, Draw & write, fun fact, reading stars. Answer key at the end.
"""
import html
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UNITS = [json.loads(f.read_text(encoding="utf-8")) for f in sorted((ROOT / "data" / "units").glob("*.json"))]
BOOK = "Read Time! 1"
e = html.escape

SECTIONS = {
    "before": (1, "Before You Read", "Rasmlarga qarang va so‘zlarni o‘qing. Matn nima haqida deb o‘ylaysiz?", "c-green", "👀"),
    "read": (2, "Read", "Matnni 2 marta o‘qing: avval jim, keyin ovoz chiqarib.", "c-blue", "📖"),
    "tf": (3, "True or False?", "To‘g‘ri bo‘lsa T, noto‘g‘ri bo‘lsa F ni belgilang.", "c-orange", "✅"),
    "mcq": (4, "Choose the Answer", "To‘g‘ri javobni aylana ichiga oling.", "c-pink", "🔘"),
    "match": (5, "Match", "So‘zni rasm bilan chiziq orqali bog‘lang.", "c-purple", "🔗"),
    "gaps": (6, "Fill the Gaps", "So‘zlar qutisidan foydalanib bo‘sh joylarni to‘ldiring.", "c-teal", "✏️"),
    "search": (7, "Word Search", "Matndagi 8 ta so‘zni toping va belgilang.", "c-yellow", "🔍"),
    "you": (8, "About You", "O‘zingiz haqingizda bitta gap yozing.", "c-blue", "🙋"),
    "draw": (9, "Draw & Write", "Rasm chizing va 2 ta gap yozing.", "c-pink", "🎨"),
}
TYPES = {   # icon + label for the text "window"
    "email": ("📧", "Email"), "blog": ("🌐", "Blog"), "story": ("📖", "Story"), "poster": ("🎉", "Poster"),
    "diary": ("📔", "Diary"), "chat": ("💬", "Chat"), "interview": ("🎤", "Interview"), "letter": ("✉️", "Letter"),
    "quiz": ("🧩", "Magazine quiz"), "article": ("📰", "Article"),
}


def rich(text):
    return re.sub(r"\*\*(.+?)\*\*", r"<mark>\1</mark>", e(text))


EMOJI = re.compile("([\U0001F000-\U0001FAFF☀-➿⬀-⯿⌀-⏿]"
                   "(?:️|‍[\U0001F000-\U0001FAFF☀-➿]️?|[\U0001F3FB-\U0001F3FF])*"
                   "|[\U0001F1E6-\U0001F1FF]{2})")


def color_emoji(markup):
    return EMOJI.sub(r'<span class="em">\1</span>', markup)


def section(key, extra=""):
    n, title, uz, cls, emo = SECTIONS[key]
    return f"""<div class="sec {cls}"><div class="sechead"><span class="secno">{n}</span><h2>{title}</h2><span class="secemo">{emo}</span>{extra}</div>
  <p class="secuz">{e(uz)}</p></div>"""


def page(inner, n, unit=None, cls=""):
    tab = f'<span class="tab {unit["color"]}">{unit["n"]}</span>' if unit else ""
    ucls = unit["color"] if unit else ""
    return f"""<section class="page {ucls} {cls}">{tab}
 <div class="content">{inner}</div>
 <footer><span>{BOOK} · Teen2Teen 1</span><span class="pno">{n}</span></footer>
</section>"""


# ---------------- word search ----------------
def word_search(words, seed, size=10):
    """Place words left→right, top→bottom or diagonally down-right; fill the rest with random letters."""
    rnd = random.Random(seed)
    grid = [[""] * size for _ in range(size)]
    dirs = [(0, 1), (1, 0), (1, 1)]
    for w in sorted(words, key=len, reverse=True):
        for _ in range(500):
            dr, dc = rnd.choice(dirs)
            r = rnd.randrange(size - (len(w) - 1) * dr)
            c = rnd.randrange(size - (len(w) - 1) * dc)
            if all(grid[r + i * dr][c + i * dc] in ("", ch) for i, ch in enumerate(w)):
                for i, ch in enumerate(w):
                    grid[r + i * dr][c + i * dc] = ch
                break
        else:
            raise ValueError(f"cannot place {w}")
    letters = "ABCDEFGHIKLMNOPRSTUWY"
    return [[ch or rnd.choice(letters) for ch in row] for row in grid]


# ---------------- unit pages ----------------
def text_window(u):
    t = u["text"]
    icon, label = TYPES[u["text_type"]]
    kind = u["text_type"]
    if kind == "chat":
        body = ""
        names = []
        for p in t["paragraphs"]:
            who, _, line = p.partition(":")
            if who not in names:
                names.append(who)
            side = "me" if names.index(who) % 2 else "you"
            body += f'<div class="bub {side}"><b>{e(who.strip())}</b>{rich(line.strip())}</div>'
    elif kind in ("interview", "quiz"):
        body = "".join(f"<p>{re.sub(r'^([^:]{1,24}:)', r'<b>\1</b>', rich(p))}</p>" for p in t["paragraphs"])
    else:
        body = "".join(f"<p>{rich(p)}</p>" for p in t["paragraphs"])
    meta = f'<div class="meta">{e(t["meta"])}</div>' if t.get("meta") else ""
    return (f'<div class="twin t-{kind}"><div class="tbar"><span class="dots3"><i></i><i></i><i></i></span>'
            f'<span>{icon} {label}</span></div><div class="tbody"><div class="thead"><h3>{e(t["title"])}</h3>'
            f'<span class="tpic">{t["picture"]}</span></div>{meta}<div class="ttext">{body}</div></div></div>')


def p_read(u):
    b = u["before"]
    cards = "".join(f'<li><span class="wemo">{emo}</span><b>{e(en)}</b><small>{e(uz)}</small></li>' for en, uz, emo in b["words"])
    return f"""<div class="uhead {u["color"]}"><div class="utitle"><small>UNIT {u["n"]} · {e(u["topic"].upper())}</small><h1>{e(u["title"])}</h1></div><span class="uemo">{u["emoji"]}</span></div>
 {section("before")}
 <ul class="wcards six">{cards}</ul>
 <p class="predict">🤔 {e(b["predict"])}</p>
 {section("read")}
 {text_window(u)}"""


def p_check(u):
    tf = "".join(f'<li><span class="qn">{i}</span><span class="q">{e(s)}</span><span class="tfb"><i>T</i><i>F</i></span></li>'
                 for i, (s, _) in enumerate(u["tf"], 1))
    mcq = "".join(f'<li><p><span class="qn">{i}</span>{e(q["q"])}</p><div class="opts">'
                  + "".join(f'<span><b>{"abc"[j]}</b>{e(o)}</span>' for j, o in enumerate(q["options"])) + "</div></li>"
                  for i, q in enumerate(u["mcq"], 1))
    rnd = random.Random(u["n"] * 7)
    pics = [p for _, p in u["match"]]
    order = list(range(len(pics)))
    while order == sorted(order):
        rnd.shuffle(order)
    left = "".join(f'<li><span class="mn">{i}</span>{e(w)}<i class="dot"></i></li>' for i, (w, _) in enumerate(u["match"], 1))
    right = "".join(f'<li><i class="dot"></i><span class="mp">{pics[k]}</span><span class="ml">{"abcde"[j]}</span></li>' for j, k in enumerate(order))
    bank = [a for _, a in u["gaps"]]
    rnd.shuffle(bank)
    gaps = "".join(f'<li>{e(s).replace("___", "<span class=gapline></span>")}</li>' for s, _ in u["gaps"])
    return f"""{section("tf")}
 <ul class="tflist">{tf}</ul>
 {section("mcq")}
 <ol class="mcq">{mcq}</ol>
 {section("match")}
 <div class="matchbox"><ul>{left}</ul><ul class="r">{right}</ul></div>
 {section("gaps")}
 <div class="bank">{''.join(f'<span>{e(w)}</span>' for w in bank)}</div>
 <ol class="gaps">{gaps}</ol>"""


def p_fun(u):
    grid = word_search(u["wordsearch"], u["n"])
    cells = "".join("<tr>" + "".join(f"<td>{ch}</td>" for ch in row) + "</tr>" for row in grid)
    words = "".join(f'<li><i class="box"></i>{w.lower()}</li>' for w in u["wordsearch"])
    you = "".join(f'<li><p>{i}. {e(q)}</p><i class="wline"></i></li>' for i, q in enumerate(u["about_you"], 1))
    return f"""{section("search")}
 <div class="wsearch"><table>{cells}</table><ul>{words}</ul></div>
 {section("you")}
 <ul class="you">{you}</ul>
 {section("draw")}
 <div class="drawbox"><p>{e(u["draw"])}</p><div class="canvas"></div><i class="wline"></i><i class="wline"></i></div>
 <div class="funfact"><span>💡</span><p><b>Fun fact!</b> {e(u["fun_fact"])}</p></div>
 <div class="rstars"><b>How did I do?</b><span>😀 Great!</span><span>🙂 Good</span><span>🤔 I need practice</span></div>"""


# ---------------- answer key ----------------
def answer_key():
    blocks = ""
    for u in UNITS:
        tf = "  ".join(f"{i} {'T' if v else 'F'}" for i, (_, v) in enumerate(u["tf"], 1))
        mcq = "  ".join(f"{i} {'abc'[q['answer']]}" for i, q in enumerate(u["mcq"], 1))
        rnd = random.Random(u["n"] * 7)
        order = list(range(len(u["match"])))
        while order == sorted(order):
            rnd.shuffle(order)
        match = "  ".join(f"{i + 1} {'abcde'[order.index(i)]}" for i in range(len(u["match"])))
        gaps = "  ".join(f"{i} {a}" for i, (_, a) in enumerate(u["gaps"], 1))
        blocks += (f'<div class="kunit {u["color"]}"><h3><span>{u["n"]}</span>{e(u["title"])}</h3>'
                   f'<p><b>True/False:</b> {tf}</p><p><b>Choose:</b> {mcq}</p><p><b>Match:</b> {match}</p><p><b>Gaps:</b> {e(gaps)}</p></div>')
    return blocks


# ---------------- front matter ----------------
def cover():
    stickers = "".join(f'<span class="{cls}">{emo} {title}</span>' for _, title, _, cls, emo in SECTIONS.values())
    return f"""<section class="page cover rcover"><div class="dots"></div><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
 <div class="floaters"><span>📚</span><span>🔍</span><span>⭐</span><span>📖</span><span>✏️</span></div>
 <div class="ctitle"><span class="kicker">TEEN2TEEN 1 · READING</span>
  <h1>Read<br>Time! <span>📖</span></h1>
  <p>12 fun texts · puzzles · <b>games &amp; stars!</b></p>
  <p class="uz">Qiziqarli matnlar, savollar va boshqotirmalar bilan ingliz tilida o‘qishni o‘rganamiz!</p></div>
 <div class="cstick">{stickers}</div>
 <div class="cfoot">🧒 For young learners · A1 · 🇺🇿 Uzbek support · ✅ Answer key</div>
</section>"""


def how_page():
    rows = "".join(f'<li class="{cls}"><span class="secno">{n}</span><div><b>{emo} {title}</b><small>{e(uz)}</small></div></li>'
                   for n, title, uz, cls, emo in SECTIONS.values())
    return f"""<section class="page"><div class="content">
 <div class="howhead"><h1>How to use<br>this book</h1><span>🗺️</span></div>
 <p class="howintro">Every unit has 3 pages and 9 steps: read, check, then play!
  <span>Har bir unit 3 sahifa va 9 bosqichdan iborat: o‘qing, tekshiring, keyin o‘ynang!</span></p>
 <ol class="howlist">{rows}</ol>
 <div class="golden"><b>🥇 Golden rule:</b> read the text <u>two times</u> before you answer!
  <span>Javob berishdan oldin matnni ikki marta o‘qing!</span></div>
</div><footer><span>{BOOK} · Teen2Teen 1</span><span class="pno">2</span></footer></section>"""


def build():
    pages, n = [cover(), how_page()], 3
    for u in UNITS:
        for make in (p_read, p_check, p_fun):
            pages.append(page(make(u), n, u))
            n += 1
    pages.append(page(f'<div class="howhead"><h1>Answer key</h1><span>🔑</span></div><div class="keygrid">{answer_key()}</div>', n, cls="keypage"))
    css = "".join((ROOT / "scripts" / f).read_text(encoding="utf-8") for f in ("style.css", "kids.css", "reading.css"))
    fonts = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700'
             '&family=Nunito:ital,wght@0,500;0,700;0,800;0,900;1,500;1,700&family=Patrick+Hand&display=block">')
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{BOOK}</title>
{fonts}<style>{css}</style></head><body>{color_emoji(''.join(pages))}</body></html>"""
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / "read-time.html").write_text(doc, encoding="utf-8")
    print("pages:", len(pages))


if __name__ == "__main__":
    build()
