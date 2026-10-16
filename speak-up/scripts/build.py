"""Build the Impulse "Speak Up!" A2 speaking book (A5 portrait, playful design) -> dist/speak-up.html.

Each unit (6 pages): vocabulary → story in context → remember the words +
useful phrases → speaking questions + sample answers → real speaking (model
speech, say it 4 ways) → speaking assistant + 1-minute challenge + I can.
Audio QR codes point to config.audio_base_url + track file name.
"""
import html
import io
import json
import re
from pathlib import Path

import qrcode
import qrcode.image.svg

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "data" / "config.json").read_text(encoding="utf-8"))
UNITS = [json.loads(f.read_text(encoding="utf-8")) for f in sorted((ROOT / "data" / "units").glob("*.json"))]
LOGO = (ROOT.parent / "vocabulary-book" / "assets" / "impulse-logo.png")
SCHOOL = "Impulse Learning Center"
e = html.escape

# section number, title, Uzbek instruction, colour class, emoji
SECTIONS = {
    "words": (1, "Topic Vocabulary", "So‘zlarni tinglang, takrorlang va belgilang.", "c-green", "📚"),
    "story": (2, "Story", "Hikoyani 3 marta o‘qing: avval jim, keyin audio bilan, keyin ovoz chiqarib.", "c-yellow", "📖"),
    "remember": (3, "Remember the Words", "Qaramasdan bo‘sh joylarni to‘ldiring, keyin hikoyadan tekshiring.", "c-blue", "🧠"),
    "phrases": (4, "Useful Phrases", "Bu iboralar bilan gapingiz tabiiy eshitiladi.", "c-pink", "💬"),
    "questions": (5, "Answer the Questions", "Har bir savolga 2–3 gap bilan ovoz chiqarib javob bering.", "c-orange", "❓"),
    "speaking": (6, "Real Speaking", "Bu sizning sahnangiz! Nutqni 4 xil qahramon bo‘lib ayting.", "c-purple", "🎤"),
    "assistant": (7, "Speaking Assistant", "Iboralardan foydalanib o‘z nutqingizni tuzing va 1 daqiqa gapiring.", "c-teal", "🚀"),
}
CHARACTERS = [
    ("🎙️", "News reader", "Yangiliklar boshlovchisidek — rasmiy va aniq."),
    ("😊", "Just me", "O‘zingizdek — tabiiy, kundalik ohangda."),
    ("😎", "Superstar", "Mashhur blogerdek — “men zo‘rman” ohangida."),
    ("🔥", "Coach", "Motivatsion murabbiydek — baland va ilhomli."),
]


def logo(size, ring=False):
    import base64
    uri = "data:image/png;base64," + base64.b64encode(LOGO.read_bytes()).decode()
    style = "border:2px solid #fff;" if ring else ""
    return f'<img class="logo" src="{uri}" width="{size}" height="{size}" alt="" style="{style}">'


def rich(text):
    return re.sub(r"\*\*(.+?)\*\*", r"<mark>\1</mark>", e(text))


def qr(file_name, label):
    img = qrcode.make(CFG["audio_base_url"] + file_name, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=1)
    buf = io.BytesIO()
    img.save(buf)
    svg = re.sub(r"<\?xml[^>]*\?>", "", buf.getvalue().decode())
    svg = re.sub(r'width="[^"]*"\s+height="[^"]*"', 'width="100%" height="100%"', svg, count=1)
    return f'<div class="qr"><div class="qrimg">{svg}</div><div><b>🎧 {e(label)}</b><small>Scan &amp; listen</small></div></div>'


def section(key, extra=""):
    n, title, uz, cls, emo = SECTIONS[key]
    return f"""<div class="sec {cls}"><div class="sechead"><span class="secno">{n}</span><h2>{title}</h2><span class="secemo">{emo}</span>{extra}</div>
  <p class="secuz">{e(uz)}</p></div>"""


def page(inner, n, unit=None, cls=""):
    tab = f'<span class="tab {unit["color"]}">{unit["n"]}</span>' if unit else ""
    return f"""<section class="page {cls}">{tab}
 <div class="content">{inner}</div>
 <footer><span>{logo(12)} Impulse Speak Up! {CFG["level"]}</span><span class="pno">{n}</span></footer>
</section>"""


# ---------------- unit pages ----------------
def p_words(u):
    count = sum(len(g["items"]) for g in u["words"])
    groups = ""
    for g in u["words"]:
        items = "".join(f'<li><b>{e(en)}</b><span>{e(uz)}</span><i class="box"></i></li>' for en, uz in g["items"])
        groups += f'<div class="wgroup"><h3>{g["emoji"]} {e(g["group"])}</h3><ul>{items}</ul></div>'
    tr = f"u{u['n']:02d}"
    return f"""<div class="uhead {u["color"]}"><div class="utitle"><small>UNIT {u["n"]}</small><h1>{e(u["title"])}</h1></div><span class="uemo">{u["emoji"]}</span></div>
 {section("words", f'<span class="count">{count} words</span>')}
 {qr(f"{tr}-1-words.mp3", f"Track {u['n']}.1 · Words")}
 <div class="wgrid">{groups}</div>"""


def p_story(u):
    s, tr = u["story"], f"u{u['n']:02d}"
    paras = "".join(f"<p>{rich(p.strip())}</p>" for p in s["text"].split(" | "))
    tf = "".join(f'<li><span class="q">{i}. {e(t)}</span><span class="tfb"><i>T</i><i>F</i></span></li>' for i, (t, _) in enumerate(s["tf"], 1))
    return f"""{section("story")}
 <div class="storybox"><div class="stitle"><h3>{e(s["title"])}</h3>{qr(f"{tr}-2-story.mp3", f"Track {u['n']}.2 · Story")}</div>{paras}</div>
 <div class="reads">🔁 Read it 3 times: <span>1 · silently</span><span>2 · with the audio</span><span>3 · aloud, alone</span></div>
 <div class="tf"><h3>✅ True or false?</h3><ul>{tf}</ul></div>
 <div class="retell"><h3>🗣️ Retell the story<small>Hikoyani kalit so‘zlar yordamida o‘z so‘zlaringiz bilan qayta aytib bering.</small></h3>
  <div class="keys">{"".join(f"<span>{e(k)}</span>" for k in s["retell"])}</div></div>"""


def p_remember(u):
    bank = "".join(f"<span>{e(a)}</span>" for _, a in sorted(u["gaps"], key=lambda g: g[1]))
    gaps = "".join(f'<li>{e(q).replace("___", "<i class=gapline></i>")}</li>' for q, _ in u["gaps"])
    phr = "".join(f'<li><div class="bubble">{e(en)}</div><span>{e(uz)}</span></li>' for en, uz in u["phrases"])
    return f"""{section("remember")}
 <div class="bank">{bank}</div><ol class="gaps">{gaps}</ol>
 {section("phrases")}
 <ul class="phr">{phr}</ul>
 <div class="mine"><h3>✏️ Make it yours<small>Iboralar bilan O‘ZINGIZ haqingizda 3 ta gap yozing va ayting.</small></h3>{'<i class="line"></i>' * 3}</div>"""


def p_questions(u):
    qs = "".join(f'<li><span class="qn">{i}</span>{e(q)}</li>' for i, q in enumerate(u["questions"], 1))
    ans = "".join(f'<div class="ans"><b>💡 {e(q)}</b><p>{rich(a)}</p></div>' for q, a in u["answers"])
    return f"""{section("questions")}
 <ul class="qlist">{qs}</ul>
 <div class="tipstrip">⭐ Answer + reason + example. <span>Javob + sabab (because…) + misol (for example…).</span></div>
 <h3 class="sub">Sample answers</h3>{ans}
 <div class="survey"><h3>👥 Ask a partner<small>Sherigingizga 3 ta savol bering va javobini yozing.</small></h3>
  <table><tr><th>Question no.</th><th>My partner’s answer</th></tr>{'<tr><td></td><td></td></tr>' * 3}</table></div>"""


def p_speaking(u):
    tr = f"u{u['n']:02d}"
    chars = "".join(f'<li><span class="cemo">{emo}</span><div><b>{name}</b><small>{e(uz)}</small></div><i class="box"></i></li>'
                    for emo, name, uz in CHARACTERS)
    return f"""{section("speaking")}
 <div class="speech"><div class="shead"><b>🎬 Model speech</b>{qr(f"{tr}-3-speech.mp3", f"Track {u['n']}.3 · Speech")}</div><p>{rich(u["speech"])}</p></div>
 <h3 class="sub">🎭 Say it 4 ways — tick each one you do</h3>
 <ul class="chars">{chars}</ul>
 <div class="mine"><h3>✏️ Your version<small>Nutqni o‘zingizga moslab o‘zgartiring: ismlar, kasblar, odatlar.</small></h3>{'<i class="line"></i>' * 4}</div>"""


def p_assistant(u):
    a = u["assistant"]

    def block(title, uz, items, cls):
        li = "".join(f"<li><b>{e(en)}</b><span>{e(t)}</span></li>" for en, t in items)
        return f'<div class="ablock {cls}"><h3>{title}<small>{uz}</small></h3><ul>{li}</ul></div>'
    can = "".join(f"<li><span>⭐</span>I can {e(c)}.</li>" for c in u["cando"])
    return f"""{section("assistant")}
 <p class="atopic">Topic: <b>“{e(a["topic"])}”</b></p>
 {block("▶ Start", "Gapni boshlash", a["start"], "a1")}{block("➕ Continue", "Davom ettirish", a["middle"], "a2")}{block("🏁 Finish", "Tugatish", a["end"], "a3")}
 <div class="challenge"><span>⏱️</span><div><b>1-minute challenge</b><small>Gapiring va vaqtni yozing. Har safar uzoqroq!</small></div>
  <div class="tries"><i></i><i></i><i></i><small>seconds · 3 tries</small></div></div>
 <div class="mine"><h3>📝 My speech plan<small>Faqat kalit so‘zlar yozing.</small></h3>{'<i class="line"></i>' * 4}</div>
 <div class="cando"><h3>🏆 Now I can …</h3><ul>{can}</ul></div>"""


# ---------------- front matter ----------------
def cover():
    stickers = "".join(f'<span class="{cls}">{emo} {title}</span>' for _, title, _, cls, emo in SECTIONS.values())
    return f"""<section class="page cover"><div class="dots"></div><div class="blob b1"></div><div class="blob b2"></div>
 <div class="cbrand">{logo(40, ring=True)}<div><b>IMPULSE</b><small>LEARNING CENTER</small></div></div>
 <div class="ctitle"><span class="kicker">LEVEL {CFG["level"]} · {CFG["level_name"].upper()}</span>
  <h1>Speak<br>Up! <span>🎤</span></h1>
  <p>Learn the words. Read them in a story. <b>Start speaking!</b></p>
  <p class="uz">So‘zlarni o‘rganing, hikoyada ko‘ring va gapirishni boshlang!</p></div>
 <div class="cstick">{stickers}</div>
 <div class="cfoot">🎧 Audio for every unit · 12 topics · 🇺🇿 Uzbek support</div>
</section>"""


def how_page():
    rows = "".join(f'<li class="{cls}"><span class="secno">{n}</span><div><b>{emo} {title}</b><small>{e(uz)}</small></div></li>'
                   for n, title, uz, cls, emo in SECTIONS.values())
    return f"""<section class="page"><div class="content">
 <div class="howhead"><h1>How to use<br>this book</h1><span>🗺️</span></div>
 <p class="howintro">Every unit has 7 sections. Do them in order — 20–30 minutes a day is enough!
  <span>Har bir bo‘lim 7 qismdan iborat. Ketma-ket bajaring — kuniga 20–30 daqiqa yetarli!</span></p>
 <ol class="howlist">{rows}</ol>
 <div class="golden"><b>🥇 Golden rule:</b> always speak <u>out loud</u>. Reading silently is not speaking!
  <span>Har doim ovoz chiqarib gapiring — jim o‘qish gapirish emas!</span></div>
</div><footer><span>{logo(12)} Impulse Speak Up! {CFG["level"]}</span><span class="pno">2</span></footer></section>"""


def build():
    pages, n = [cover(), how_page()], 3
    for u in UNITS:
        for make in (p_words, p_story, p_remember, p_questions, p_speaking, p_assistant):
            pages.append(page(make(u), n, u))
            n += 1
    css = (ROOT / "scripts" / "style.css").read_text(encoding="utf-8")
    fonts = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700'
             '&family=Nunito:ital,wght@0,500;0,700;0,800;0,900;1,500;1,700&display=swap">')
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{SCHOOL} — Speak Up! {CFG["level"]}</title>
{fonts}<style>{css}</style></head><body>{''.join(pages)}</body></html>"""
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / "speak-up.html").write_text(doc, encoding="utf-8")
    print("pages:", len(pages))


if __name__ == "__main__":
    build()
