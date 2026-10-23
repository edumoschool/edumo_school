"""Build the playful Multilevel Writing guide (A4) -> dist/writing.html (interior) and dist/cover.html (front + back cover)."""
import base64
import html
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DIST = ROOT / "dist"
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700'
         '&family=Nunito:ital,wght@0,400;0,600;0,700;0,800;0,900;1,600;1,700&display=block" rel="stylesheet">')
COLORS = ["c-blue", "c-pink", "c-green", "c-orange", "c-purple", "c-teal", "c-sky", "c-yellow", "c-pink", "c-green"]
TOTAL = 10


def e(s):
    return html.escape(str(s), quote=False)


def uri(p):
    return "data:image/png;base64," + base64.b64encode(Path(p).read_bytes()).decode()


def paras(text, marker=None):
    """Plain text with \\n (line) and \\n\\n (paragraph) -> <p> blocks; marker(str)->str post-processes escaped text."""
    out = []
    for block in text.split("\n\n"):
        t = "<br>".join(e(l) for l in block.split("\n"))
        out.append(f"<p>{marker(t) if marker else t}</p>")
    return "".join(out)


def sec(no, title, emoji, color, uz=None, count=None):
    c = f'<span class="count">{e(count)}</span>' if count else ""
    u = f'<p class="secuz">{e(uz)}</p>' if uz else ""
    return (f'<div class="sec {color}"><span class="secno">{no}</span><h2>{e(title)}</h2><span class="emo">{emoji}</span>{c}</div>{u}')


def hero(kicker, title, emoji, color, sub=""):
    s = f"<p>{e(sub)}</p>" if sub else ""
    return f'<div class="hero {color}"><div><small>{e(kicker)}</small><h1>{e(title)}</h1>{s}</div><span class="emo">{emoji}</span></div>'


# ---------------------------------------------------------------- front matter
def how_page():
    steps = [("c-blue", "📩", "Read the situation", "Read the email or letter and the three tasks.", "Vaziyat va uchta topshiriqni diqqat bilan o‘qing."),
             ("c-pink", "🔍", "Read & think", "Answer 4 quick questions about the message.", "Xat bo‘yicha 4 ta savolga javob bering."),
             ("c-green", "🔤", "Word power", "Match the key words with their Uzbek meaning.", "Kalit so‘zlarni o‘zbekcha ma’nosi bilan moslang."),
             ("c-orange", "🎭", "Formal or informal?", "Decide which phrases belong in which letter.", "Iboralar qaysi xatga mosligini aniqlang."),
             ("c-purple", "🧠", "Plan it", "Make quick notes for every task before you write.", "Yozishdan oldin har bir topshiriq uchun reja tuzing."),
             ("c-teal", "✍️", "Write", "Write Task 1.1, Task 1.2 and Part 2. Count your words and tick the checklist.", "Uchala topshiriqni yozing, so‘zlarni sanang."),
             ("c-yellow", "⭐", "Model answers", "Compare with the model letters. Highlighted words are worth learning.", "Namunaviy javoblar bilan solishtiring."),
             ("c-sky", "🔗", "Linkers & words", "Complete the model blog post with linkers, then learn the word list.", "Bog‘lovchilarni qo‘ying va lug‘atni yodlang.")]
    cards = "".join(f'<div class="step {c}"><span class="ic">{i}</span><div><b>{n}. {e(t)}</b><p>{e(d)}</p><p class="uz">{e(u)}</p></div></div>'
                    for n, (c, i, t, d, u) in enumerate(steps, 1))
    return (hero("10 exercises · B1 – C1", "How to use this book", "🗺️", "c-blue", "Har bir mashq — 8 qadam. Bir mashq ≈ 2 dars.")
            + f'<div class="steps">{cards}</div>'
            + '<div class="note" style="margin-top:5mm"><b>💡 Tip:</b> Time yourself like in the real exam — about <b>60 minutes</b> for all three tasks: '
              '≈ 10 min for Task 1.1, ≈ 20 min for Task 1.2 and ≈ 30 min for Part 2. Use the <b>score tracker</b> to see your progress.</div>')


def exam_pages(f):
    skills = "".join(f'<span class="chip">{e(s)}</span>' for s in f["skills"])
    out = hero("Multilevel · Yozma ish", "The writing exam", "📝", "c-purple", "Tuzilma, talablar va baholash mezonlari")
    out += f'<p style="font-weight:700;margin-bottom:2mm">{e(f["intro"])}</p><div class="c-purple" style="margin-bottom:3mm">{skills}</div>'
    colors = ["c-green", "c-blue", "c-purple"]
    k = 0
    for p in f["parts"]:
        out += sec(p["level"], p["title"], "✉️" if "1" in p["title"][:2] else "💻", "c-orange") + f'<p class="secuz" style="font-style:normal">{e(p["lead"])}</p><div class="stack">'
        for t in p["tasks"]:
            req = "".join(f"<li>{e(r)}</li>" for r in t["req"])
            out += (f'<div class="task {colors[k]}"><div class="side"><span class="big">{e(t["level"])}</span><small>{e(t["words"])}</small></div>'
                    f'<div><h3>{e(t["name"])}</h3><p class="kv"><b>Uslub:</b> {e(t["style"])} · <b>Maqsad:</b> {e(t["aim"])}</p>'
                    f'<ul class="dots" style="margin-top:2px">{req}</ul></div></div>')
            k += 1
        out += "</div>"
        if p.get("note"):
            out += f'<div class="note" style="margin-top:3mm"><b>Muhim jihat:</b> {e(p["note"])}</div>'
        if p.get("topics"):
            out += '<p style="margin-top:3mm;font-weight:800;color:var(--navy)">Namunaviy mavzular:</p><div class="c-pink">' + "".join(
                f'<span class="chip">{e(t)}</span>' for t in p["topics"]) + "</div>"
    fn = "".join(f'<span class="chip">✔ {e(x)}</span>' for x in f["functions"])
    out += sec("✓", "Til funksiyalari", "🗣️", "c-teal") + f'<p class="secuz" style="font-style:normal">Yozma ishda nomzod quyidagi ko‘nikmalarni namoyish etishi kerak:</p><div class="c-teal">{fn}</div>'
    cards = ""
    for a, c in zip(f["assess"], ["c-green", "c-purple"]):
        pts = "".join(f"<li>{e(x)}</li>" for x in a["points"])
        cr = "".join(f'<span class="chip">{e(x)}</span>' for x in a["criteria"])
        cards += f'<div class="card {c}"><h3>{e(a["title"])} · <span class="badge">{e(a["range"])}</span></h3><ul class="dots">{pts}</ul><p style="font-weight:800;margin-top:3px">Mezonlar:</p>{cr}</div>'
    out += sec("★", "Baholash mezonlari", "🏅", "c-pink") + f'<div class="grid2">{cards}</div>'
    succ = "".join(f'<span class="chip">{e(x)}</span>' for x in f["success"])
    out += (f'<div class="note" style="margin-top:4mm"><b>Xulosa:</b> {e(f["summary"])}<br><b>Muvaffaqiyatli yozma ish uchun:</b> '
            f'<span class="c-yellow">{succ}</span></div>')
    return out


def toolkit_page():
    inf = {"Start": ["Hi Jack, / Hey Sam,", "How are you doing?", "Did you hear about …?", "Guess what!"],
           "Feelings": ["I'm so excited about …", "I'm a bit gutted / upset that …", "Honestly, it's really annoying.", "I can't wait!"],
           "Ideas": ["Maybe we could …", "Why don't we …?", "I think they should …", "How about …?"],
           "Finish": ["Let me know what you think!", "Talk soon, / Take care,", "See you soon,", "Best, + your name"]}
    frm = {"Start": ["Dear Mr Smith, / Dear Manager,", "I am writing regarding …", "Thank you for informing us about …", "I am writing to express my concern about …"],
           "Feelings": ["I must admit I was disappointed to hear …", "I was delighted to learn that …", "I fully understand the need for …", "I am concerned that …"],
           "Ideas": ["I would like to suggest that …", "It would be highly beneficial to …", "I would strongly recommend …", "Perhaps you could consider …"],
           "Finish": ["I look forward to hearing from you.", "Thank you for your attention.", "Sincerely, / Best regards,", "Full name"]}

    def kit(d, title, color, emoji):
        body = "".join(f"<h4>{k}</h4><ul>" + "".join(f"<li>{e(x)}</li>" for x in v) + "</ul>" for k, v in d.items())
        return f'<div class="card kit {color}"><h3>{emoji} {title}</h3>{body}</div>'
    bp = [("Introduction", "Rephrase the question + give your opinion clearly."),
          ("Body 1", "First reason / advantage + a real example."),
          ("Body 2", "Second reason or the other side + example."),
          ("Conclusion", "Sum up and repeat your opinion in new words.")]
    blue = "".join(f"<div><b>{a}</b><span>{e(b)}</span></div>" for a, b in bp)
    linkers = {"Adding": "Furthermore · Moreover · Additionally · What is more", "Contrast": "However · On the other hand · Although · Nevertheless",
               "Examples": "For example · For instance · such as · Take … as an example", "Result": "Therefore · As a result · Consequently · This means that",
"Concluding": "Ultimately · In conclusion · Overall · All things considered"}
    lk = "".join(f'<div><b>{k}</b><span>{e(v)}</span></div>' for k, v in linkers.items())
    return (hero("Your writing toolkit", "Phrase bank", "🧰", "c-teal", "Informal vs formal · Blog post plan · Linkers")
            + f'<div class="grid2">{kit(inf, "Informal (Task 1.1)", "c-green", "😊")}{kit(frm, "Formal (Task 1.2)", "c-blue", "🎩")}</div>'
            + sec("✓", "Part 2 blueprint", "🧱", "c-purple", "Blog post / maqola rejasi — 4 paragraf, 180–200 so‘z")
            + f'<div class="blueprint c-purple">{blue}</div>'
            + sec("✓", "Linkers", "🔗", "c-orange", "Bog‘lovchi so‘zlar — fikrlarni bog‘lash uchun")
            + f'<div class="blueprint c-orange">{lk}</div>')


def sample_page(f):
    out = hero("Examiner's eye", "Real marks, real comments", "🧐", "c-pink", "Read the answer, guess the mark, then check the examiner's comment.")
    for t, c in zip(f["sample"]["tasks"], ["c-green", "c-blue", "c-purple"]):
        out += (f'<div class="samp {c}"><div class="paper"><span class="tag badge">{e(t["task"])}</span>{paras(t["text"])}</div>'
                f'<div class="exam"><b>Guess the mark: ____ / {t["max"]}</b><span class="mark">{t["mark"]}<small>/{t["max"]}</small></span>'
                f'<b>👩‍🏫 Examiner:</b><span>{e(t["comment"])}</span></div></div>')
    s = f["sample"]
    out += (f'<div class="score c-orange"><div><b>{s["overall"]}</b><span>Overall score (out of 17)</span></div>'
            f'<div><b>{s["standard"]}</b><span>Standard score (out of 75)</span></div><div><b>{s["level"]}</b><span>Level</span></div></div>')
    return out


def rubric_pages(f):
    out = ""
    colors = ["c-green", "c-sky", "c-blue", "c-purple", "c-orange", "c-pink", "c-teal"]
    for i, r in enumerate(f["rubrics"]):
        out += '<div class="np"></div>' if i else ""
        out += hero("Band descriptors", f"How {r['part']} is marked", ["📧", "📨", "💻"][i], ["c-green", "c-blue", "c-purple"][i])
        for j, (b, lvl, desc) in enumerate(r["bands"]):
            parts = desc.split("|")
            body = f"<p>{e(parts[0])}</p>" + (('<ul class="dots">' + "".join(f"<li>{e(x)}</li>" for x in parts[1:]) + "</ul>") if len(parts) > 1 else "")
            out += f'<div class="band {colors[j % len(colors)]}"><div class="lv"><span class="big">{b}</span><small>{e(lvl)}</small></div><div class="ds">{body}</div></div>'
    return out


def conversion_page(f):
    cells = "".join(f'<div>{m}<span>→ {s}</span></div>' for m, s in f["conversion"])
    rows = "".join(f"<tr><td>Exercise {i}</td><td></td><td></td><td></td><td></td><td></td></tr>" for i in range(1, TOTAL + 1))
    return (hero("Score", "From marks to score", "📈", "c-orange", "Task 1.1 (0–5) + Task 1.2 (0–6) + Part 2 (0–6) = 0–17")
            + sec("1", "Conversion table", "🔢", "c-orange", "Expert mark → standard score (0–75)") + f'<div class="conv c-orange">{cells}</div>'
            + sec("2", "My score tracker", "🏆", "c-purple", "Har bir mashqdan keyin ballaringizni yozing")
            + '<table class="track"><tr><th>Exercise</th><th>Task 1.1 /5</th><th>Task 1.2 /6</th><th>Part 2 /6</th><th>Total /17</th><th>Score /75</th></tr>'
            + rows + "</table>")


# ---------------------------------------------------------------- units
def mark_vocab(text, vocab):
    words = sorted({w for w, _ in vocab if len(w) > 3}, key=len, reverse=True)
    for w in words:
        text = re.sub(r"(?<![\w>])(" + re.escape(e(w)) + r")(?![\w<])", r"<mark>\1</mark>", text, count=1, flags=re.I)
    return re.sub(r"<mark>([^<]*)<mark>([^<]*)</mark>([^<]*)</mark>", r"<mark>\1\2\3</mark>", text)


def pick_match(u):
    v = [x for x in u["vocab"] if len(x[0]) < 32]
    step = max(1, len(v) // 8)
    sel = [tuple(x) for x in v[::step][:8]]
    rnd = random.Random(u["n"] * 7)
    right = sel[:]
    rnd.shuffle(right)
    letters = "ABCDEFGH"
    key = {w: letters[right.index((w, uz))] for w, uz in sel}
    return sel, right, key


def register_order(u):
    r = u["register"][:]
    random.Random(u["n"] * 13).shuffle(r)
    return r


def gapped_p2(u):
    text = u["samples"]["p2"]
    pieces = []
    for g in u["p2_gaps"]:
        i = text.find(g)
        pieces.append((i, g))
    pieces.sort()
    out, pos = "", 0
    for n, (i, g) in enumerate(pieces, 1):
        out += e(text[pos:i]) + f"\x00{n}\x00"
        pos = i + len(g)
    out += e(text[pos:])
    out = "".join(f"<p>{p.replace(chr(10), '<br>')}</p>" for p in out.split("\n\n"))
    return re.sub("\x00(\\d)\x00", r'<span class="gap">\1</span>', out)


def unit_pages(u):
    n, col = u["n"], COLORS[(u["n"] - 1) % len(COLORS)]
    m = u["email"]
    body = "".join(f"<p>{e(p)}</p>" for p in m["body"])
    sign = "<br>".join(e(x) for x in [m.get("signoff", ""), m.get("from", "")] if x)
    mail = (f'<div class="mail"><div class="bar"><i style="background:#FF6B6B"></i><i style="background:#FFC94D"></i><i style="background:#3DD68C"></i>'
            f'<span class="t">From: <b>{e(m.get("from") or "—")}</b> · To: <b>You</b> · {e(m.get("kind", "email")).title()}</span></div>'
            f'<div class="body">{"<p><b>" + e(m["greeting"]) + "</b></p>" if m.get("greeting") else ""}{body}{"<p>" + sign + "</p>" if sign else ""}</div></div>')

    def tk(c, name, sub, text, words):
        return (f'<div class="tk {c}"><div class="h"><b>{name}</b><span>{sub}</span></div><div class="t"><span class="badge w">{words}</span>{text}</div></div>')
    p2 = u["part2"]
    tasks = ('<div class="tasks">'
             + tk("c-green", "Task 1.1", "Informal · B1", e(u["task11"]), "≈ 50 words")
             + tk("c-blue", "Task 1.2", "Formal · B2", e(u["task12"]), "120–150 words")
             + tk("c-purple", "Part 2", "Blog post · C1", f'{e(p2["context"])} <span class="q">“{e(p2["question"])}”</span> {e(p2["instruction"])}', "180–200 words")
             + "</div>")
    out = (f'<div class="np"></div><div class="unit {col}"><div class="num"><small>EXERCISE</small><span class="big">{n}</span></div>'
           f'<div class="ttl"><div><small>Multilevel writing · Part 1 + Part 2</small><h1>{e(u["topic"])}</h1></div><span class="emo">{u["emoji"]}</span></div></div>'
           f'<div class="situ"><span class="emo">📍</span>{e(u["situation"])}</div>{mail}{tasks}')

    qs = "".join(f'<li>{e(q["q"])}<div class="ln"></div></li>' for q in u["read_qs"])
    out += '<div class="keep">' + sec(1, "Read & think", "🔍", "c-pink", "Xatni o‘qing va savollarga javob bering") + f'<ol class="qs c-pink">{qs}</ol></div>'

    sel, right, _ = pick_match(u)
    rows = "".join(f'<div class="l"><b>{i + 1}</b><span>{e(w)}</span><i></i></div><div class="r"><b>{"ABCDEFGH"[i]}</b>{e(right[i][1])}</div>'
                   for i, (w, _) in enumerate(sel))
    out += '<div class="keep">' + sec(2, "Word power", "🔤", "c-green", "So‘zlarni ma’nosi bilan moslang (1–8 → A–H)") + f'<div class="match c-green">{rows}</div></div>'

    reg = "".join(f'<div><span>“{e(r["phrase"])}”</span><em>F</em><em>I</em></div>' for r in register_order(u))
    out += ('<div class="keep">' + sec(3, "Formal or informal?", "🎭", "c-orange", "Rasmiy (F) yoki norasmiy (I)? Belgilang.")
            + f'<div class="reg c-orange">{reg}</div></div>')

    pl = u["plan"]

    def pbox(title, c, items, k):
        inner = "".join(f'<p class="pr">{e(x)}</p>' + '<div class="ln"></div>' * k for x in items)
        return f'<div class="pl {c}"><h3>{title}</h3>{inner}</div>'
    out += ('<div class="keep">' + sec(4, "Plan it", "🧠", "c-purple", "Yozishdan oldin qisqa reja tuzing")
            + f'<div class="plan">{pbox("Task 1.1 😊", "c-green", pl["t11"], 2)}{pbox("Task 1.2 🎩", "c-blue", pl["t12"], 2)}{pbox("Part 2 💻", "c-purple", pl["p2"], 2)}</div></div>')

    def wbox(c, title, lines, checks, words):
        ch = "".join(f"<span>{e(x)}</span>" for x in checks)
        return (f'<div class="wbox {c}"><div class="top"><span class="badge">{words}</span><h3>{title}</h3><span class="wc">Words: <i></i></span></div>'
                f'<div class="lines">{"<div></div>" * lines}</div><div class="check">{ch}</div></div>')
    out += ('<div class="np"></div>' + sec(5, "Write", "✍️", "c-teal", "Endi yozing! So‘zlarni sanang va tekshiring.")
            + wbox("c-green", "Task 1.1 · Informal letter", 7, ["Friendly greeting", "Feelings", "Suggestion", "Informal ending", "≈ 50 words"], "≈ 50")
            + '<div style="height:4mm"></div>'
            + wbox("c-blue", "Task 1.2 · Formal letter", 17, ["Dear … ,", "Reason for writing", "Clear paragraphs", "Polite suggestions", "Formal ending", "120–150 words"], "120–150"))
    out += ('<div class="np"></div>'
            + wbox("c-purple", f'Part 2 · “{e(p2["question"])}”', 26, ["Clear opinion", "2 reasons + examples", "Other side", "Linkers", "Conclusion", "180–200 words"], "180–200"))

    v = u["vocab"]
    out += ('<div class="np"></div>' + sec(6, "Model answers", "⭐", "c-yellow", "Namunaviy javoblar — belgilangan so‘zlarni o‘rganing")
            + f'<div class="model c-green"><span class="tag badge">Task 1.1 · Informal</span>{paras(u["samples"]["t11"], lambda t: mark_vocab(t, v))}</div>'
            + f'<div class="model c-blue"><span class="tag badge">Task 1.2 · Formal</span>{paras(u["samples"]["t12"], lambda t: mark_vocab(t, v))}</div>')
    bank = list(u["p2_gaps"])
    random.Random(n * 17).shuffle(bank)
    out += (sec(7, "Linkers: complete the model post", "🔗", "c-sky", "Namunaviy blog postini bog‘lovchilar bilan to‘ldiring (1–6)")
            + '<div class="bank">' + "".join(f"<span>{e(b)}</span>" for b in bank) + "</div>"
            + f'<div class="model c-purple gaptext"><span class="tag badge">Part 2 · Model blog post</span>{gapped_p2(u)}</div>')
    vv = "".join(f'<div><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in v)
    out += sec(8, "Word list", "📚", "c-green", "Lug‘at: inglizcha — o‘zbekcha", f"{len(v)} words") + f'<div class="voc">{vv}</div>'
    return out


def answer_key(units):
    out = '<div class="np"></div>' + hero("Check yourself", "Answer key", "🔑", "c-green", "Read & think · Word power · Formal or informal · Linkers")
    for u in units:
        _, _, key = pick_match(u)
        sel, _, _ = pick_match(u)
        rq = "".join(f'<div><b>{i}.</b> {e(q["a"])}</div>' for i, q in enumerate(u["read_qs"], 1))
        mt = "  ".join(f"<b>{i}</b>–{key[w]}" for i, (w, _) in enumerate(sel, 1))
        rg = "  ".join(f'<b>{i}</b> {"F" if r["type"] == "formal" else "I"}' for i, r in enumerate(register_order(u), 1))
        order = sorted(u["p2_gaps"], key=lambda g: u["samples"]["p2"].find(g))
        lk = "  ".join(f"<b>{i}</b> {e(g)}" for i, g in enumerate(order, 1))
        out += (f'<div class="key {COLORS[(u["n"] - 1) % len(COLORS)]}"><h3><span>Exercise {u["n"]} · {e(u["topic"])}</span><span>{u["emoji"]}</span></h3><div class="kb">'
                f'<div class="full"><b>🔍 Read & think</b></div>{rq}'
                f'<div class="full"><b>🔤 Word power:</b> {mt}</div><div class="full"><b>🎭 Formal / informal:</b> {rg}</div>'
                f'<div class="full"><b>🔗 Linkers:</b> {lk}</div></div></div>')
    return out


def cover(units):
    hero_img = uri(ROOT / "assets" / "hero_clean.png")
    topics = "".join(f'<span>{u["emoji"]} {e(u["topic"])}</span>' for u in units)
    front = (f'<section class="cv front"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>'
             f'<div class="kick">Multilevel · CEFR · B1 – C1</div><h1>Write<br>it <span>Right!</span></h1>'
             f'<p class="sub">A complete guide to <b>Multilevel Writing</b></p>'
             f'<img class="hi" src="{hero_img}"><div class="pills"><span class="p1">✉️ Task 1.1</span><span class="p2">📨 Task 1.2</span><span class="p3">💻 Part 2</span></div>'
             f'<div class="foot"><b>10 exercises</b> · model answers · examiner marks · word lists · answer key</div></section>')
    back = (f'<section class="cv back"><div class="blob b1"></div><div class="blob b2"></div><h2>Write it Right!</h2>'
            f'<p>Ten complete Multilevel writing exercises — each with a real exam situation, three tasks, fun warm-up activities, '
            f'planning pages, space to write, model answers and a word list in English and Uzbek.</p>'
            f'<div class="tp">{topics}</div><p class="uzb">Elektron xatlar (B1–B2) va blog posti (C1) — bosqichma-bosqich, namunalar va baholash mezonlari bilan.</p></section>')
    css = """
@page{size:A4;margin:0}*{box-sizing:border-box;margin:0;padding:0}html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:Nunito,sans-serif}
.cv{width:210mm;height:297mm;position:relative;overflow:hidden;break-after:page;color:#fff;
 background:linear-gradient(160deg,#3B6CFF 0%,#2563EB 45%,#5B3DF5 100%)}
.blob{position:absolute;border-radius:50%}
.b1{width:120mm;height:120mm;background:rgba(255,255,255,.10);right:-40mm;top:-40mm}
.b2{width:80mm;height:80mm;background:rgba(255,201,77,.25);left:-25mm;bottom:40mm}
.b3{width:40mm;height:40mm;background:rgba(240,84,154,.35);right:22mm;top:118mm}
.kick{position:absolute;left:18mm;top:20mm;font-family:Fredoka;font-weight:600;letter-spacing:.2em;font-size:12pt;background:rgba(255,255,255,.18);
 border-radius:999px;padding:4px 16px}
.front h1{position:absolute;left:18mm;top:36mm;font-family:Fredoka;font-weight:700;font-size:72pt;line-height:.95;text-shadow:0 6px 0 rgba(0,0,0,.15)}
.front h1 span{color:#FFD84D}
.sub{position:absolute;left:18mm;top:110mm;font-size:16pt;font-weight:700;opacity:.97}
.hi{position:absolute;left:12mm;width:186mm;top:128mm;filter:drop-shadow(0 6mm 8mm rgba(10,20,90,.35))}
.pills{position:absolute;left:18mm;right:18mm;bottom:38mm;display:flex;gap:4mm}
.pills span{font-family:Fredoka;font-weight:600;font-size:15pt;padding:6px 18px;border-radius:999px;color:#14215A;box-shadow:0 4px 0 rgba(0,0,0,.15)}
.p1{background:#7CF2B4}.p2{background:#FFD84D}.p3{background:#FFB3D4}
.foot{position:absolute;left:18mm;right:18mm;bottom:18mm;font-size:12pt;font-weight:700;border-top:2px solid rgba(255,255,255,.35);padding-top:5mm}
.back{padding:40mm 22mm}
.back h2{font-family:Fredoka;font-size:40pt;margin-bottom:8mm;position:relative}
.back p{font-size:13pt;line-height:1.5;font-weight:600;position:relative;margin-bottom:8mm}
.tp{display:flex;flex-wrap:wrap;gap:3mm;position:relative;margin-bottom:10mm}
.tp span{background:#fff;color:#14215A;font-weight:800;border-radius:999px;padding:4px 14px;font-size:12pt}
.uzb{font-style:italic;opacity:.9}
"""
    return f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{css}</style></head><body>{front}{back}</body></html>'


def build():
    f = json.loads((DATA / "front.json").read_text(encoding="utf-8"))
    units = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((DATA / "units").glob("*.json"))]
    body = (how_page() + '<div class="np"></div>' + exam_pages(f) + '<div class="np"></div>' + toolkit_page()
            + '<div class="np"></div>' + sample_page(f) + '<div class="np"></div>' + rubric_pages(f)
            + '<div class="np"></div>' + conversion_page(f) + "".join(unit_pages(u) for u in units) + answer_key(units))
    css = (ROOT / "scripts" / "style.css").read_text(encoding="utf-8")
    DIST.mkdir(exist_ok=True)
    (DIST / "writing.html").write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Write it Right!</title>{FONTS}<style>{css}</style></head>'
                                       f"<body>{body}</body></html>", encoding="utf-8")
    (DIST / "cover.html").write_text(cover(units), encoding="utf-8")
    print("units:", len(units))


if __name__ == "__main__":
    build()
