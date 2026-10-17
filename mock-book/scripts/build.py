"""Build the Multilevel Mock Tests book interior (A4, two columns) -> dist/mock.html.

Mock test N = data/listening-N.json + data/reading-N.json. Each skill starts on a new page with a banner;
parts flow through two columns (render.js moves overflowing blocks to the next column / page).
After the tests: answer sheets for every mock and the answer key.
"""
import base64
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA, ASSETS, DIST = ROOT / "data", ROOT / "assets", ROOT / "dist"
CHANNEL = "t.me/multilevel_express"
e = html.escape
_sid = 0

SKILL = {
    "listening": {"icon": "🎧", "title": "LISTENING", "time": "approx. 35 minutes", "q": 35,
                  "uz": "Har bir audio ikki marta eshittiriladi. Javoblarni javoblar varaqasiga yozing."},
    "reading": {"icon": "📖", "title": "READING", "time": "60 minutes", "q": 35,
                "uz": "Vaqt: 60 daqiqa. Javoblarni javoblar varaqasiga o‘tkazishni unutmang."},
}
QRANGE = {"listening": {1: "1–8", 2: "9–14", 3: "15–18", 4: "19–23", 5: "24–29", 6: "30–35"},
          "reading": {1: "1–6", 2: "7–14", 3: "15–20", 4: "21–29", 5: "30–35"}}


def md(s):
    s = e(str(s), quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"(\(?\b(?:Q?\d{1,2})\)?\s?)(_{3,}|…{2,}|\.{4,})", r'<span class="gn">\1</span><span class="gap"></span>', s)
    s = re.sub(r"_{3,}|…{3,}|\.{6,}", '<span class="gap"></span>', s)
    return s.replace("\n", "<br>")


def split(inner, cls):
    global _sid
    _sid += 1
    return f'<div class="split {cls}" data-split="s{_sid}">{inner}</div>'


def uri(p):
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()


def block(b):
    t = b["type"]
    if t == "instruction":
        icon = '<span class="aud">🎧</span>' if b.get("audio") else ""
        return f'<div class="ins">{icon}<p>{md(b["text"])}</p></div>'
    if t == "subtitle":
        return f'<h4 class="subt">{md(b["text"])}</h4>'
    if t in ("article", "text"):
        title = f'<h3 class="atitle">{md(b["title"])}</h3>' if b.get("title") else ""
        return title + split("".join(f"<p>{md(p)}</p>" for p in b["paragraphs"]), "art")
    if t == "headings":
        items = "".join(f"<li>{md(i)}</li>" for i in b["items"])
        right = "".join(f"<li>{md(i)}</li>" for i in b.get("right", []))
        return (f'<div class="box heads"><b>{md(b.get("title", "List of Headings"))}</b><ul>{items}</ul>'
                + (f'<ul class="ans">{right}</ul>' if right else "") + "</div>")
    if t == "statements":
        return split("".join(f"<p>{md(i)}</p>" for i in b["items"]), "stmts")
    if t == "cards":
        title = f'<h3 class="atitle">{md(b["title"])}</h3>' if b.get("title") else ""
        return title + split("".join(f'<div class="card"><b>{md(c["title"])}</b><div>{md(c["body"])}</div></div>'
                                     for c in b["items"]), "cards")
    if t == "mcq":
        def q(it):
            qs = str(it.get("q", ""))
            n = it.get("n")
            head = (f'<b class="qn">{n}</b>' if n else "") + (f'<b>{md(qs)}</b>' if qs else "")
            opts = "".join(f"<li>{md(o)}</li>" for o in it.get("options", []))
            return f'<div class="q"><p>{head}</p><ul>{opts}</ul></div>'
        return split("".join(q(it) for it in b["items"]), "mcq")
    if t == "notes":
        title = f'<h3>{md(b["title"])}</h3>' if b.get("title") else ""
        lines = ""
        for ln in b["lines"]:
            m = re.match(r"^([^:]{2,32}):\s+(.*)$", ln)
            lines += (f'<p class="kv"><b>{md(m.group(1))}:</b><span>{md(m.group(2))}</span></p>' if m and not ln.startswith("http")
                      else f"<p>{md(ln)}</p>")
        return f'<div class="box notes">{title}{lines}</div>'
    if t == "matching":
        left = "".join(f"<li>{md(i)}</li>" for i in b["left"])
        right = "".join(f"<li>{md(i)}</li>" for i in b["right"])
        return f'<div class="box match"><ul>{left}</ul><ul>{right}</ul></div>'
    if t == "image":
        w = b.get("width", 100)
        return f'<div class="img"><img src="{uri(ASSETS / b["src"])}" style="width:{w}%" alt=""></div>'
    if t == "lines":
        return f'<ul class="lines">{"".join(f"<li>{md(i)}</li>" for i in b["items"])}</ul>'
    raise ValueError(t)


def part(skill, p):
    head = (f'<div class="phead"><span class="pill">PART {p["part"]}</span>'
            f'<span class="qr">Questions {QRANGE[skill].get(p["part"], "")}</span></div>')
    return f'<div class="part">{head}{"".join(block(b) for b in p["blocks"])}</div>'


def skill_pages(test):
    s, n = SKILL[test["skill"]], test["mock"]
    banner = (f'<div class="banner"><div class="girih"></div><div class="bl"><small>MOCK TEST {n}</small>'
              f'<h1>{s["icon"]} {s["title"]}</h1></div><div class="br"><b>{len(test["parts"])} parts · {s["q"]} questions</b>'
              f'<span>⏱ {s["time"]}</span>' + (f'<span>🎧 Audio: {CHANNEL}</span>' if test["skill"] == "listening" else "")
              + f'</div></div><p class="uzline">{e(s["uz"])}</p>')
    parts = "".join(part(test["skill"], p) for p in test["parts"])
    return (f'<section class="page flow first" data-run="Mock Test {n} · {s["title"].title()}">{banner}'
            f'<div class="cols"><div class="col">{parts}</div><div class="col"></div></div>'
            f'<footer><span>Multilevel Mock Tests · Mock Test {n} · {s["title"].title()}</span><span class="pno"></span></footer></section>')


MAP_LETTERS = {12: "ABCDEFGHI"}      # Mock 12's map has places A–I


def answer_sheet(n):
    """Answer sheet in the official Multilevel layout (bubbles + letter boxes), one after every mock."""
    def bubbles(nums, letters, two=False):
        def row(q):
            return f'<div class="bq"><b>{q}</b>' + "".join(f"<i>{L}</i>" for L in letters) + "</div>"
        if two:
            half = (len(nums) + 1) // 2
            return f'<div class="bcols"><div>{"".join(row(q) for q in nums[:half])}</div><div>{"".join(row(q) for q in nums[half:])}</div></div>'
        return "".join(row(q) for q in nums)

    def boxes(nums, cells=12):
        return "".join(f'<div class="bx"><b>{q}</b>' + "<i></i>" * cells + "</div>" for q in nums)

    def grp(label, inner, cls=""):
        return f'<div class="grp {cls}"><span class="gl">{label}</span><div class="gi">{inner}</div></div>'

    example = ('<div class="ex"><p>LOTIN BOSMA KATTA HARFLARDA YOZING<br>НАПИШИТЕ ЛАТИНСКИМИ<br>БОЛЬШИМИ ПРОПИСНЫМИ БУКВАМИ</p>'
               '<div class="exb">' + "".join(f"<i>{c}</i>" for c in "EXAMPLE") + "<i></i></div></div>")
    abc, r = "ABC", range
    listening = (grp("1-QISM / ЧАСТЬ 1", bubbles(list(r(1, 9)), abc, True), "w")
                 + example + grp("2-QISM / ЧАСТЬ 2", boxes(r(9, 15)))
                 + grp("3-QISM / ЧАСТЬ 3", bubbles(list(r(15, 19)), "ABCDEF"), "w")
                 + grp("4-QISM / ЧАСТЬ 4", bubbles(list(r(19, 24)), MAP_LETTERS.get(n, "ABCDEFGH")), "w")
                 + grp("5-QISM / ЧАСТЬ 5", bubbles(list(r(24, 30)), abc, True), "w")
                 + example + grp("6-QISM / ЧАСТЬ 6", boxes(r(30, 36))))
    reading = (example + grp("1-QISM / ЧАСТЬ 1", boxes(r(1, 7)))
               + grp("2-QISM / ЧАСТЬ 2", bubbles(list(r(7, 15)), "ABCDEFGHIJ"), "w")
               + grp("3-QISM / ЧАСТЬ 3", bubbles(list(r(15, 21)), "ABCDEFGH"), "w")
               + grp("4-QISM / ЧАСТЬ 4", '<div class="bcols"><div>' + bubbles(list(r(21, 25)), "ABCD") + '</div><div>'
                     + bubbles(list(r(25, 30)), abc) + "</div></div>", "w")
               + example + grp("5-QISM / ЧАСТЬ 5", boxes(r(30, 34)) + bubbles([34, 35], "ABCD")))
    code = "".join('<div class="kc"><i class="kh"></i>' + "".join(f"<i>{d}</i>" for d in "1234567890") + "</div>" for _ in range(5))
    marks = '<div class="marks">' + "<i></i>" * 46 + "</div>"
    return (f'<section class="page asheet">{marks}<div class="frame">'
            f'<div class="ahead"><img src="{uri(ASSETS / "brand" / "logo_red.png")}" alt="Impulse"><div><small>JAVOBLAR VARAQASI / ЛИСТ ОТВЕТОВ</small>'
            f'<h1>Multilevel Answersheet</h1></div><span class="mk">MOCK {n}</span></div>'
            f'<div class="atop"><div class="al"><p>DOIRACHANI BO‘YASH NAMUNASI / ОБРАЗЕЦ ЗАКРАШИВАНИЯ КРУЖОЧКОВ</p>'
            f'<p class="c">To‘g‘ri / Правильно <span class="dot"></span></p>'
            f'<p class="warn">DIQQAT! NOMZOD CHETLASHTIRILGANDA NAZORATCHI TOMONIDAN TO‘LDIRILADI.<br>ВНИМАНИЕ! ЗАПОЛНЯЕТСЯ НАБЛЮДАТЕЛЕМ ПРИ ОТСТРАНЕНИИ.</p>'
            f'<i class="ln"></i><i class="ln"></i><p class="cap">(Chetlashtirish sababi / Причина отстранения)</p>'
            f'<i class="ln"></i><p class="cap">Guruh nazoratchisining F.I.O / Ф.И.О наблюдателя группы</p><p class="cap r">Imzo / Подпись</p></div>'
            f'<div class="am"><span class="vl">Maxsus kod / Специальный код</span><div class="code">{code}</div></div>'
            f'<div class="ar"><i class="ln"></i><p class="cap">(Familiyasi / Фамилия)</p><i class="ln"></i><p class="cap">(Ismi / Имя)</p>'
            f'<i class="ln"></i><p class="cap">(Otasining ismi / Отчество)</p><i class="ln s"></i><p class="cap">Imzo / Подпись</p></div></div>'
            f'<div class="abody"><div class="sk"><h2>Tinglab tushunish / Аудирование</h2>{listening}</div>'
            f'<div class="sk"><h2>O‘qish / Чтение</h2>{reading}</div></div></div>'
            f'<p class="handle">@cefr_impulse</p></section>')


OFFICIAL = json.loads((DATA / "keys" / "official.json").read_text(encoding="utf-8"))


def answer_key(tests):
    body = ""
    for n in sorted({t["mock"] for t in tests}):
        off = OFFICIAL.get(str(n))
        rows = ""
        for t in tests:
            if t["mock"] != n:
                continue
            for p in t["parts"]:
                if off:
                    ans = off[t["skill"]].get(str(p["part"]), "")
                elif t["skill"] == "reading":
                    ans = t.get("key", {}).get(str(p["part"]), "")
                else:
                    a, b = QRANGE["listening"][p["part"]].split("–")
                    ans = "  ".join(f"{i} ______" for i in range(int(a), int(b) + 1))
                rows += f'<tr><th>{SKILL[t["skill"]]["title"].title()} · Part {p["part"]}</th><td>{md(ans)}</td></tr>'
        note = ('<span class="kn">official answers</span>' if off else
                '<span class="kn alt">reading: worked out by our teachers · listening: fill in from the audio</span>')
        body += f'<div class="kmock"><h3>Mock Test {n} {note}</h3><table>{rows}</table></div>'
    return (f'<section class="page flow" data-run="Answer key"><div class="banner small"><div class="girih"></div><div class="bl">'
            f'<small>ALL TESTS</small><h1>ANSWER KEY</h1></div><div class="br"><span>Mocks 3–12: official answers</span></div></div>'
            f'<div class="cols"><div class="col">{split(body, "keys")}</div><div class="col"></div></div>'
            f'<footer><span>Multilevel Mock Tests · Answer key</span><span class="pno"></span></footer></section>')


NUM_WORDS = {5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}


SPEAKER = re.compile(r"^(\d{1,2}\.\s|Speaker \d+\.?|Extract \w+|[A-Z][A-Za-z.’' ]{0,18}:)")


def listening_scripts():
    """Audio scripts of the Multilevel Zone tests (src/answers.txt) as a flowing two-column section."""
    src = ROOT / "src" / "answers.txt"
    if not src.exists():
        return ""
    text = src.read_text(encoding="utf-8").split("ANSWERS")[0]
    sections = re.split(r"^\s*TEST (\d+) PART (\d+)\s*$", text, flags=re.M)
    by_test = {}
    for i in range(1, len(sections) - 2, 3):
        test, part, body = int(sections[i]), int(sections[i + 1]), sections[i + 2]
        paras, cur = [], ""
        for raw in body.splitlines():
            ln = raw.strip()
            if ln in ("MULTILEVEL ZONE MOCK EXAM", "AUDIO SCRIPTS") or re.fullmatch(r"\d{1,3}", ln):
                continue
            if not ln:
                if cur:
                    paras.append(cur); cur = ""
                continue
            if SPEAKER.match(ln) and cur:
                paras.append(cur); cur = ln
            else:
                cur = f"{cur} {ln}".strip()
        if cur:
            paras.append(cur)
        by_test.setdefault(test, []).append((part, paras))
    body = ""
    for test, parts in sorted(by_test.items()):
        mock = test + 2
        inner = ""
        for part, paras in parts:
            ps = "".join(f"<p>{bold_label(p)}</p>" for p in paras)
            inner += (f'<div class="part"><div class="phead"><span class="pill">PART {part}</span>'
                      f'<span class="qr">Mock Test {mock}</span></div>{split(ps, "script")}</div>')
        body += f'<div class="part"><h3 class="atitle">Mock Test {mock} · Listening</h3></div>{inner}'
    return (f'<section class="page flow first" data-run="Listening scripts"><div class="banner small"><div class="girih"></div>'
            f'<div class="bl"><small>MOCK TESTS 3–12</small><h1>🎧 LISTENING SCRIPTS</h1></div>'
            f'<div class="br"><span>Read after you check your answers</span></div></div>'
            f'<div class="cols"><div class="col">{body}</div><div class="col"></div></div>'
            f'<footer><span>Multilevel Mock Tests · Listening scripts</span><span class="pno"></span></footer></section>')


def bold_label(p):
    m = SPEAKER.match(p)
    if not m:
        return md(p)
    return f"<b>{e(m.group(1).strip())}</b> {md(p[m.end():].strip())}"


def how_page(count=5):
    tips = [("🎧", "Listening", "6 parts · 35 questions. Scan the QR / open the channel and play the audio for each test. Each recording is played twice."),
            ("📖", "Reading", "5 parts · 35 questions · 60 minutes. Do the test in one sitting, without a dictionary."),
            ("📝", "Answer sheets", "After each test there is a Multilevel answer sheet — write your answers there, just like the real exam."),
            ("🔑", "Answer key & scripts", "Check your answers and count your score out of 35. Then read the listening scripts at the back to see what you missed."),
            ("📈", "Track progress", "Repeat the mocks after a few weeks and compare your scores.")]
    cards = "".join(f'<div class="tip"><span>{i}</span><div><b>{t}</b><p>{d}</p></div></div>' for i, t, d in tips)
    return (f'<section class="page howpage"><div class="banner"><div class="girih"></div><div class="bl"><small>MULTILEVEL · CEFR</small>'
            f'<h1>HOW TO USE THIS BOOK</h1></div><div class="br"><b>{count} mock tests</b><span>Listening + Reading</span></div></div>'
            f'<p class="lead">This book contains <b>{NUM_WORDS.get(count, count)} complete Multilevel mock tests</b> in the real exam format. '
            f'Treat each one like the real exam: keep to the time, write on the answer sheet and check your score.</p>'
            f'<div class="tips">{cards}</div>'
            f'<div class="audio"><div class="qrc">{qr_svg("https://" + CHANNEL)}</div><div><b>🎧 Audio for all listening tests</b>'
            f'<p>Scan the QR code to open our Telegram channel.</p><span>{CHANNEL}</span></div></div>'
            f'<table class="plan"><tr><th>Skill</th><th>Part</th><th>Task</th><th>Questions</th></tr>'
            + "".join(f"<tr><td>{s}</td><td>{p}</td><td>{d}</td><td>{q}</td></tr>" for s, p, d, q in [
                ("🎧", "1", "Choose the correct reply", "1–8"), ("🎧", "2", "Complete the notes", "9–14"),
                ("🎧", "3", "Match speakers to statements", "15–18"), ("🎧", "4", "Label a map / plan", "19–23"),
                ("🎧", "5", "Multiple choice (extracts)", "24–29"), ("🎧", "6", "Complete the lecture notes", "30–35"),
                ("📖", "1", "Gap fill (one word)", "1–6"), ("📖", "2", "Match texts to statements", "7–14"),
                ("📖", "3", "Match headings to paragraphs", "15–20"), ("📖", "4", "Multiple choice + True/False/NI", "21–29"),
                ("📖", "5", "Summary completion + multiple choice", "30–35")])
            + '</table><footer><span>Multilevel Mock Tests</span><span class="pno"></span></footer></section>')


def qr_svg(url):
    import qrcode
    import qrcode.image.svg
    return qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=1).to_string(encoding="unicode")


EMOJI = re.compile("([\U0001F000-\U0001FAFF☀-➿⬀-⯿⌀-⏿](?:️)?)")


def build():
    tests = []
    for f in sorted(DATA.glob("*.json")):
        tests.append(json.loads(f.read_text(encoding="utf-8")))
    tests.sort(key=lambda t: (t["mock"], t["skill"] != "listening"))
    pages = [how_page(len({t['mock'] for t in tests}))]
    for t in tests:                      # listening, reading, then the answer sheet of that mock
        pages.append(skill_pages(t))
        if t["skill"] == "reading":
            pages.append(answer_sheet(t["mock"]))
    pages.append(answer_key(tests))
    pages.append(listening_scripts())
    css = (ROOT / "scripts" / "style.css").read_text(encoding="utf-8")
    fonts = ('<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@400;600;700;800'
             '&family=Open+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400;1,600&display=block" rel="stylesheet">')
    body = EMOJI.sub(r'<span class="em">\1</span>', "".join(pages))
    doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Multilevel Mock Tests</title>{fonts}<style>{css}</style></head><body>{body}</body></html>'
    DIST.mkdir(exist_ok=True)
    (DIST / "mock.html").write_text(doc, encoding="utf-8")
    print("tests:", [(t["mock"], t["skill"]) for t in tests])


if __name__ == "__main__":
    build()
