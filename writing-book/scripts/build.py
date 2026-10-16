"""Build an Impulse Learning Center writing book (A2 or B1) as HTML.

Usage: python3 build.py [A2|B1]  ->  dist/<level>-writing-book.html

Uses the speaking books' design (speaking-book/scripts/style.css) plus style.css here.
Content comes from data/<level>-writing.txt; level settings are in LEVELS below. Pages:
  cover · how to use · contents
  per unit (4 pages): model text + language focus · vocabulary + practice + plan ·
                      writing task · IELTS-style opinion paragraph
  writing bank (2) · common mistakes · answer key · model answers (1 per unit)
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEAKING = ROOT.parent / "speaking-book" / "scripts"
sys.path.insert(0, str(SPEAKING))
from build import ICONS, icon, logo  # noqa: E402  (shared icons and logo)

e = html.escape
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
    "doc": "M6 3h9l4 4v14H6zM15 3v4h4M9 12h7M9 16h7",
    "puzzle": "M4 8h4a2 2 0 114 0h4v4a2 2 0 110 4v4H4v-4a2 2 0 100-4z",
    "layers": "M12 3l9 5-9 5-9-5zM3 13l9 5 9-5",
    "scale": "M12 3v18M5 21h14M4 8h16M4 8l-2 6a3 3 0 006 0zM20 8l-2 6a3 3 0 006 0z",
    "alert": "M12 3l10 18H2zM12 10v5M12 18v.5",
    "key": "M8 15a4 4 0 100-8 4 4 0 000 8zM11 11h10M17 11v4M20 11v3",
    "award": "M12 15a6 6 0 100-12 6 6 0 000 12zM8.5 14L7 22l5-3 5 3-1.5-8",
})
UNIT_ICONS = ["globe", "sun", "briefcase", "building", "bag", "history",
              "heart", "compass", "cup", "leaf", "users", "film"]

A2_STEPS = [("Your opinion", "In my opinion, … / I think …"),
            ("Reason 1 + example", "Firstly, … For example, …"),
            ("Reason 2 or the other side", "Secondly, … / On the other hand, … However, …"),
            ("Conclusion", "To sum up, … / Overall, I believe …")]
B1_STEPS = [("Introduction", "Rewrite the question in your own words + give your opinion or say what you will discuss."),
            ("Body paragraph 1", "Firstly, … / The main advantage is … For example, …"),
            ("Body paragraph 2", "On the other hand, … / However, … Moreover, …"),
            ("Conclusion", "In conclusion, … / To sum up, I believe …")]
LEVELS = {
    "A2": {
        "kicker": "LEVEL A2 · ELEMENTARY", "source": "Topics from Navigate Elementary A2",
        "icons": UNIT_ICONS, "essay": "Opinion paragraph", "short": "OPINION", "lines": 17,
        "instr": "Write an opinion paragraph of 80–120 words. Give reasons and examples.",
        "plan_title": "Paragraph plan", "steps": A2_STEPS,
        "lead": "Model texts, useful vocabulary with Uzbek translations, real-life writing tasks and IELTS-style opinion paragraphs in 12 units.",
        "feat": ["12 units", "24 writing tasks", "120 words & phrases", "Model answers"],
        "sample": ("UNIT 4.7 · IELTS-STYLE TASK", "Is it better to live in a city or in the countryside?",
                   ["In my opinion", "Firstly", "On the other hand", "To sum up"],
                   "I think it is better to live in a city, especially for young people."),
        "part7": "An opinion paragraph with ideas and a plan.",
        "good": ("A good paragraph", [("Topic", "In my opinion, it is important to learn a foreign language."),
                                      ("Support", "Firstly, it gives you more job opportunities. For example, many companies want workers who speak English."),
                                      ("End", "To sum up, I believe everyone should learn at least one foreign language.")]),
    },
    "B1": {
        "kicker": "LEVEL B1 · INTERMEDIATE · IELTS STYLE", "source": "Topics from Navigate Pre-intermediate B1",
        "icons": ["clock", "building", "heart", "history", "bag", "users", "compass", "book", "star", "cup", "globe", "briefcase"],
        "essay": "Essay", "short": "ESSAY", "lines": 19,
        "instr": "Write an essay of 120–160 words in four paragraphs. Give reasons and examples.",
        "plan_title": "Essay plan", "steps": B1_STEPS,
        "lead": "Model texts, B1 collocations with Uzbek translations, IELTS General Training-style letters and IELTS Task 2-style essays in 12 units.",
        "feat": ["12 units", "12 letters & texts", "12 essays", "120 words & phrases", "Model answers"],
        "sample": ("UNIT 2.7 · IELTS-STYLE ESSAY",
                   "More and more people are moving to big cities. What are the advantages and disadvantages?",
                   ["The main advantage is", "Moreover", "However", "In conclusion"],
                   "Nowadays, a growing number of people are leaving the countryside to live in big cities."),
        "part7": "An IELTS Task 2-style essay with ideas and a four-paragraph plan.",
        "good": ("A good essay", [("Introduction", "Nowadays, many people move to big cities. This trend has both advantages and disadvantages."),
                                  ("Body 1", "The main advantage is that cities offer more jobs. For example, …"),
                                  ("Body 2", "However, cities can become crowded and expensive. Moreover, …"),
                                  ("Conclusion", "In conclusion, moving to a city can improve people’s lives, but …")]),
    },
}
LEVEL = sys.argv[1].upper() if len(sys.argv) > 1 else "A2"
CFG = LEVELS[LEVEL]
BOOK = f"{LEVEL} Writing Book"
UNIT_ICONS = CFG["icons"]


def load_units():
    units, cur = [], None
    for line in (ROOT / "data" / f"{LEVEL.lower()}-writing.txt").read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            cur = {"n": int(line[4:])}
            units.append(cur)
        elif line and not line.startswith("#") and cur is not None:
            key, val = line.split(": ", 1)
            cur.setdefault(key, []).append(val)
    for u in units:
        for key in ("title", "type", "model_title", "model", "focus", "focus_text", "task_title", "task",
                    "words", "ielts", "model_task", "model_ielts", "ielts_type"):
            if key in u:
                u[key] = u[key][0]
        u["w"] = [tuple(x.split(" = ", 1)) for x in u["w"]]
        u["gap"] = [tuple(x.split(" || ", 1)) for x in u["gap"]]
    return units


UNITS = load_units()


def rich(text):
    """Escape text and turn [[phrase]] into a highlighted phrase."""
    return re.sub(r"\[\[(.+?)\]\]", r"<mark>\1</mark>", e(text))


def paragraphs(text, cls="ptext"):
    return f'<div class="{cls}">' + "".join(f"<p>{rich(p.strip())}</p>" for p in text.split(" | ")) + "</div>"


def label_line(text):
    """'Label: example' -> bold label + example."""
    label, _, rest = text.partition(": ")
    return f"<b>{e(label)}</b>{e(rest)}" if rest else e(text)


def lines(n):
    return '<i class="line"></i>' * n


def frame(inner, page_no):
    return f"""<section class="page">
 <header class="run"><span class="brand">{logo(18)}<b>IMPULSE</b><span>LEARNING CENTER</span></span>
  <span class="tag"><b>{LEVEL}</b> WRITING BOOK</span></header>
 <div class="content">{inner}</div>
 <footer class="run"><span>© {SCHOOL} · {CFG["source"]}</span>
  <span class="pg">Page {page_no}</span></footer>
</section>"""


def card(ico, small, title, body, cls="", extra=""):
    return f"""<article class="lesson {cls}">
 <div class="lh"><span class="lico">{icon(ico)}</span><div><small>{small}</small><h3>{title}</h3></div>{extra}</div>
 {body}
</article>"""


def essay_type(u):
    return u.get("ielts_type", CFG["essay"])


def unit_banner(u):
    return f"""<div class="ubanner"><div class="uno"><small>UNIT</small><span>{u["n"]}</span></div>
 <span class="uico">{icon(UNIT_ICONS[u["n"] - 1])}</span>
 <div class="ut"><h1>{e(u["title"])}</h1><p>Text type: {e(u["type"])} · {e(essay_type(u))}</p></div>
 <div class="ustat"><b>4</b><small>pages</small></div></div>"""


def page_model(u):
    ex = "".join(f"<li>{label_line(x)}</li>" for x in u["ex"])
    model = card("doc", f"UNIT {u['n']}.1 · MODEL TEXT · {u['type'].upper()}", e(u["model_title"]),
                 paragraphs(u["model"], "ptext model") +
                 '<p class="hint">Find the highlighted phrases. Which ones can you use in your own writing?</p>',
                 "kind-chat grow")
    focus = card("puzzle", f"UNIT {u['n']}.2 · LANGUAGE FOCUS", e(u["focus"]),
                 f'<div class="fbody"><p class="lead2">{e(u["focus_text"])}</p><ul class="flist">{ex}</ul></div>',
                 "kind-abc grow")
    return unit_banner(u) + f'<div class="two first">{model}{focus}</div>'


def page_practice(u):
    words = "".join(f'<li><b>{e(en)}</b><span>{e(uz)}</span></li>' for en, uz in u["w"])
    box = "".join(f"<span>{e(a)}</span>" for _, a in sorted(u["gap"], key=lambda g: g[1].lower()))
    gaps = "".join(f'<li><span class="qn">{i}</span><p>{e(q).replace("___", "<i class=gapline></i>")}</p></li>'
                   for i, (q, _) in enumerate(u["gap"], 1))
    vocab = card("book", f"UNIT {u['n']}.3 · USEFUL VOCABULARY", "Words &amp; phrases",
                 f'<div class="words big"><ul>{words}</ul></div>', "kind-chat")
    practice = card("pen", f"UNIT {u['n']}.4 · PRACTICE", "Complete the sentences",
                    f'<div class="wordbox">{box}</div><ol class="qs gaps">{gaps}</ol>', "kind-pen")
    plan = "".join(f'<div class="pbox"><b>Paragraph {i}</b><p>{e(b)}</p>{lines(2)}</div>'
                   for i, b in enumerate(u["b"], 1))
    plan_card = card("layers", f"UNIT {u['n']}.5 · PLAN YOUR WRITING", f"Plan: {e(u['task_title'])}",
                     f'<p class="hint">Make notes for each paragraph before you write on the next page.</p><div class="plan">{plan}</div>',
                     "kind-play wide-card")
    return f'<div class="two half">{vocab}{practice}</div>{plan_card}'


def checklist(u):
    items = [f"I wrote {u['words']} words.", "I answered every point in the task.",
             "I used at least three phrases from the Vocabulary box."] + u["check"] + \
            ["I checked spelling, capital letters and full stops."]
    return "".join(f'<li><i class="cbox"></i>{e(x)}</li>' for x in items)


def page_task(u):
    bullets = "".join(f"<li>{e(b)}</li>" for b in u["b"])
    body = f"""<div class="tgrid">
  <div class="tleft"><p class="task">{e(u["task"])}</p><p class="incl">In your {e(u["type"].split(":")[0].lower())}:</p>
   <ul class="bul">{bullets}</ul><span class="wcount">{icon("doc")}Write {e(u["words"])} words</span>
   <div class="rbox"><h4>{icon("puzzle")}Remember: {e(u["focus"].lower())}</h4><ul class="mini">{"".join(f"<li>{label_line(x)}</li>" for x in u["ex"][:4])}</ul></div>
   <div class="rbox chk"><h4>{icon("check")}Self-check</h4><ul class="checks">{checklist(u)}</ul></div></div>
  <div class="tright">{lines(CFG["lines"])}</div>
 </div>"""
    return card("pen", f"UNIT {u['n']}.6 · WRITING TASK · {u['type'].upper()}", e(u["task_title"]), body, "kind-pen wide-card")


def page_ielts(u):
    ideas = "".join(f"<li>{e(i)}</li>" for i in u["idea"])
    steps = CFG["steps"]
    plan = "".join(f'<li><span class="qn">{i}</span><div><b>{a}</b><p>{e(b)}</p></div></li>'
                   for i, (a, b) in enumerate(steps, 1))
    body = f"""<div class="tgrid">
  <div class="tleft"><p class="question">“{e(u["ielts"])}”</p>
   <p class="incl">{e(CFG["instr"])}</p>
   <div class="rbox ideas"><h4>{icon("bulb")}Ideas to help you</h4><ul class="talk">{ideas}</ul></div>
   <div class="rbox"><h4>{icon("layers")}{CFG["plan_title"]}</h4><ol class="steps4">{plan}</ol></div>
   <div class="rbox"><h4>{icon("book")}Try to use</h4><div class="chips2">{"".join(f"<span>{e(en)}</span>" for en, _ in u["w"][:8])}</div></div></div>
  <div class="tright">{lines(CFG["lines"])}</div>
 </div>"""
    return card("scale", f"UNIT {u['n']}.7 · IELTS-STYLE TASK · {essay_type(u).upper()}",
                "Give your opinion" if LEVEL == "A2" else e(essay_type(u)), body, "kind-play wide-card")


# ---------- back matter ----------
BANK = [
    ("Informal emails", "chat", ["Hi … , / Dear … ,", "Thanks for your email.", "It was great to hear from you.",
                                  "Let me tell you about …", "What about you?", "Write back soon!", "Best wishes, / Take care,"]),
    ("Formal emails & letters", "briefcase", ["Dear Sir or Madam, / Dear Mr … ,", "I am writing to apply for / complain about / suggest …",
                                               "I would like to …", "Could you please … ?", "In addition, … / As a result, …",
                                               "I look forward to hearing from you.", "Yours faithfully, / Yours sincerely,"]),
    ("Stories", "history", ["Last summer, … / A few years ago, …", "When we arrived, …", "At first, …",
                             "Then … / After that, …", "Suddenly, …", "In the end, …", "It was one of the best days of my life."]),
    ("Descriptions", "building", ["It’s in … / It’s about … km from …", "It’s surrounded by …", "There is … / There are …",
                                   "You can see / hear / smell …", "It’s much … than …", "The best thing about it is …",
                                   "All in all, it’s a … place."]),
    ("Reviews", "award", ["Last … I went to / watched …", "It’s a … (type) about …", "What I liked most was …",
                           "The … was absolutely delicious / amazing.", "However, … / The only problem was …",
                           "Overall, … / I’d give it … stars.", "I’d recommend it to …"]),
    ("Opinion paragraphs", "scale", ["In my opinion, … / I think …", "Firstly, … / Secondly, …", "For example, … / such as …",
                                      "This is because …", "On the other hand, … / However, …", "Some people say … , but …",
                                      "To sum up, … / Overall, I believe …"]),
    ("Advice", "heart", ["I’m sorry to hear that …", "You should / shouldn’t …", "Why don’t you … ?", "If I were you, I’d …",
                          "It’s a good idea to …", "Try to …", "I hope you feel better soon!"]),
    ("Recommending", "compass", ["You must see / try …", "It’s definitely worth visiting.", "The best time to visit is …",
                                  "The best way to … is …", "Don’t forget to …", "I highly recommend it!", "You won’t regret it!"]),
]

MISTAKES = [
    ("I am agree with you.", "I agree with you.", "agree is a verb — no am"),
    ("He go to work every day.", "He goes to work every day.", "he / she / it + -s"),
    ("I have 20 years.", "I am 20 (years old).", "use be for age"),
    ("She is teacher.", "She is a teacher.", "a / an before jobs"),
    ("People is very friendly.", "People are very friendly.", "people is plural"),
    ("Yesterday I go to the cinema.", "Yesterday I went to the cinema.", "past simple for finished time"),
    ("I went to home.", "I went home.", "no to before home"),
    ("I can to swim.", "I can swim.", "can + verb (no to)"),
    ("I very like football.", "I really like football.", "very doesn’t go before verbs"),
    ("It was very interesting film.", "It was a very interesting film.", "a / an before singular nouns"),
    ("He explained me the rule.", "He explained the rule to me.", "explain something to someone"),
    ("I need some informations / advices.", "I need some information / advice.", "uncountable: no -s"),
    ("I am living in Tashkent since 2015.", "I have lived in Tashkent since 2015.", "present perfect with since / for"),
    ("I married with Aziz.", "I am married to Aziz.", "married to"),
    ("I listen music every day.", "I listen to music every day.", "listen to"),
    ("dear sir or madam, i am writing …", "Dear Sir or Madam, I am writing …", "capital letters: names, I, start of sentences"),
]


B1_BANK = [
    ("Informal letters", "chat", ["Thanks a lot for your letter.", "It was lovely to hear from you.", "You asked me about …",
                                   "Anyway, … / By the way, …", "Why don’t you … ? / How about … -ing?",
                                   "Hope to hear from you soon.", "All the best, / Take care,"]),
    ("Formal letters", "briefcase", ["Dear Sir or Madam, → Yours faithfully,", "Dear Ms Davis, → Yours sincerely,",
                                      "I am writing to complain about / enquire about / apply for …",
                                      "I would be grateful if you could …", "Could you tell me whether … ?",
                                      "I have attached …", "I look forward to hearing from you."]),
    ("Semi-formal letters", "users", ["Dear Mr / Ms … ,", "I hope you don’t mind me writing …", "I’m sure you don’t realise …",
                                       "I wonder if you could … ?", "Would you mind … -ing?", "I would really appreciate it.",
                                       "Kind regards,"]),
    ("Stories", "history", ["It was a … afternoon in … and I was …", "While I was … -ing, …", "I had already … , so …",
                             "Suddenly, … / Luckily, … / Eventually, …", "At first I felt … , but …", "To my surprise, …",
                             "I’ll never forget that day."]),
    ("Articles", "doc", ["Do you often … ? You are not alone.", "If you are looking for … , … is the place for you.",
                          "First of all, … / Another tip is to …", "It’s a good idea to … instead of … -ing.",
                          "Of course, it isn’t perfect.", "All in all, …", "Follow these tips and you’ll …"]),
    ("Reviews", "award", ["I stayed at / watched / visited … in …", "Overall, I was very impressed.", "What I liked most was …",
                           "The highlight was …", "The only downside was …", "All things considered, …",
                           "I would highly recommend it to …"]),
    ("Opinion essays", "scale", ["It is often said that … In my opinion, …", "I partly agree with this view.",
                                  "Firstly, … For example, …", "Furthermore, … / Moreover, …", "It is true that … However, …",
                                  "As a result, … / Therefore, …", "In conclusion, I believe …"]),
    ("Other essays", "layers", ["Discussion: On the one hand, … On the other hand, …",
                                 "Adv. / disadv.: The main advantage is … A major drawback is …",
                                 "Problem / solution: The main cause is … One solution would be to …",
                                 "This essay will look at …", "There are several ways to …", "Both views have some truth in them.",
                                 "In conclusion, … should …"]),
]

B1_MISTAKES = [
    ("I have seen him yesterday.", "I saw him yesterday.", "past simple with finished time"),
    ("I live here since 2018.", "I have lived here since 2018.", "present perfect with since / for"),
    ("If I will have time, I will call you.", "If I have time, I will call you.", "no will after if"),
    ("Although it was late, but we went out.", "Although it was late, we went out.", "although OR but, not both"),
    ("Despite of the rain, we played.", "Despite the rain, we played.", "despite (no of) / in spite of"),
    ("I look forward to hear from you.", "I look forward to hearing from you.", "look forward to + -ing"),
    ("The people which live here are friendly.", "The people who live here are friendly.", "who for people, which for things"),
    ("Could you tell me where is the station?", "Could you tell me where the station is?", "indirect questions: normal word order"),
    ("I’m interesting in history.", "I’m interested in history.", "-ed = feelings, -ing = things"),
    ("It depends of the weather.", "It depends on the weather.", "depend on"),
    ("In the other hand, …", "On the other hand, …", "fixed phrase"),
    ("The most of people agree.", "Most people agree.", "no the before most + noun"),
    ("I suggest you to take a taxi.", "I suggest taking a taxi. / I suggest (that) you take …", "suggest + -ing / that"),
    ("Everybody have their own opinion.", "Everybody has their own opinion.", "everybody + singular verb"),
    ("Dear Mr Brown, … Yours faithfully,", "Dear Mr Brown, … Yours sincerely,", "name known → sincerely"),
    ("Nowadays people is very busy.", "Nowadays people are very busy.", "people is plural"),
]
if LEVEL == "B1":
    BANK, MISTAKES = B1_BANK, B1_MISTAKES


def bank_pages(start):
    def col(items):
        return "".join(card(ic, "WRITING BANK", e(t), '<ul class="bank">' + "".join(f"<li>{e(p)}</li>" for p in ph) + "</ul>",
                            "kind-chat") for t, ic, ph in items)
    p1 = f'<h2 class="btitle">{icon("book")}Writing bank</h2><div class="grid4">{col(BANK[:4])}</div>'
    p2 = f'<h2 class="btitle">{icon("book")}Writing bank</h2><div class="grid4">{col(BANK[4:])}</div>'
    return [frame(p1, start), frame(p2, start + 1)]


def mistakes_page(n):
    rows = "".join(f'<tr><td class="bad">✗ {e(a)}</td><td class="good">✓ {e(b)}</td><td>{e(c)}</td></tr>' for a, b, c in MISTAKES)
    body = f'<table class="mist"><tr><th>Don’t write</th><th>Write</th><th>Why?</th></tr>{rows}</table>'
    return frame(card("alert", "COMMON MISTAKES", "Ten-second checks before you finish", body, "kind-abc wide-card"), n)


def key_page(n):
    blocks = "".join(f'<div class="kunit"><b>Unit {u["n"]}</b><ol>' + "".join(f"<li>{e(a)}</li>" for _, a in u["gap"]) + "</ol></div>"
                     for u in UNITS)
    return frame(card("key", "ANSWER KEY", "Practice: complete the sentences", f'<div class="kgrid">{blocks}</div>',
                      "kind-pen wide-card"), n)


def model_answer_page(pair, n):
    rows = ""
    for u in pair:
        task = card("pen", f"UNIT {u['n']} · WRITING TASK", e(u["task_title"]), paragraphs(u["model_task"], "ptext small"), "kind-pen")
        ielts = card("scale", f"UNIT {u['n']} · {CFG['short']}", e(u["ielts"]), paragraphs(u["model_ielts"], "ptext small"), "kind-play")
        rows += f'<div class="two mrow">{task}{ielts}</div>'
    head = f'<h2 class="btitle">{icon("award")}Model answers · Units {pair[0]["n"]}–{pair[-1]["n"]}</h2>'
    return frame(head + rows, n)


# ---------- front matter ----------
def cover():
    dots = "".join(f"<span>{u['n']}</span>" for u in UNITS)
    sample = CFG["sample"]
    return f"""<section class="page cover"><div class="grid"></div><div class="blob b1"></div><div class="blob b2"></div>
 <div class="cbrand">{logo(64, ring=True)}<div><b>IMPULSE</b><small>LEARNING CENTER</small></div></div>
 <div class="main"><span class="kicker">{CFG["kicker"]}</span>
  <h1>Writing<br><span>Book</span></h1>
  <p class="lead">{e(CFG["lead"])}</p>
  <div class="feat">{"".join(f"<span>{e(f)}</span>" for f in CFG["feat"])}</div></div>
 <div class="card"><div class="top">{icon("scale")}<b>{sample[0]}</b></div>
  <div class="cb"><div class="q">{e(sample[1])}</div>
   <div class="chips">{"".join(f"<span>{e(c)}</span>" for c in sample[2])}</div>
   <div class="st">{icon("bulb")}<span>{e(sample[3])}</span></div></div></div>
 <div class="cfoot"><div><b>{SCHOOL}</b> · {CFG["source"]}</div><div class="units">{dots}</div></div>
</section>"""


def how_to():
    steps = [("doc", "Read the model", "Read the model text. Find the <b>highlighted phrases</b> and notice how the text is organised."),
             ("puzzle", "Learn the language", "Study the <b>Language focus</b> and the <b>Words &amp; phrases</b>, then do the practice."),
             ("layers", "Plan", "Make short notes for each paragraph before you start writing."),
             ("pen", "Write and check", "Write your text, then use the <b>Self-check</b> list. Compare with the model answers.")]
    step_html = "".join(f'<div class="step"><span class="sico">{icon(i)}</span><b>{n}. {t}</b><p>{d}</p></div>'
                        for n, (i, t, d) in enumerate(steps, 1))
    parts = [("doc", "1 · Model text", "A real example of the unit’s text type."),
             ("puzzle", "2 · Language focus", "One writing skill with examples."),
             ("book", "3 · Words & phrases", "Ten useful collocations with Uzbek."),
             ("pen", "4 · Practice", "Use the new words in sentences."),
             ("layers", "5 · Plan", "Notes for each paragraph."),
             ("pen", "6 · Writing task", "A real-life task with lines to write on."),
             ("scale", "7 · IELTS-style task", CFG["part7"])]
    part_html = "".join(f'<div class="kind"><span class="lico">{icon(i)}</span><div><b>{t}</b><p>{e(d)}</p></div></div>' for i, t, d in parts)
    return f"""<section class="page"><div class="inner">
 <div class="ptitle">{logo(30)}<h2>How to use this book</h2><div class="bar"></div><small>{SCHOOL.upper()}</small></div>
 <div class="steps">{step_html}</div>
 <div class="hgrid">
  <div class="stack"><div class="box"><h3>Each unit has seven parts</h3><div class="parts">{part_html}</div></div></div>
  <div class="stack">
   <div class="box"><h3>{CFG["good"][0]}</h3>
    <table class="ext">{"".join(f"<tr><td>{a}</td><td>{e(b)}</td></tr>" for a, b in CFG["good"][1])}</table></div>
   <div class="box"><h3>At the back of the book</h3><ul class="checks big plainlist">
    <li>Writing bank — useful phrases for every text type</li><li>Common mistakes — check before you finish</li>
    <li>Answer key — practice exercises</li><li>Model answers — for every writing task</li></ul></div>
  </div>
 </div>
</div><div class="pfoot"><span><b>{SCHOOL}</b> · {BOOK}</span><span>{CFG["source"]}</span></div></section>"""


def contents(unit_pages, back):
    cards = "".join(f"""<a><div class="h"><span class="tico">{icon(UNIT_ICONS[u["n"] - 1])}</span><span><small>UNIT</small><b>{u["n"]}</b></span></div>
  <div class="c"><h4>{e(u["title"])}</h4><ul><li>{e(u["type"])}</li><li>{e(u["focus"])}</li><li>{e(essay_type(u))}</li></ul>
  <div class="meta"><span>Writing</span><span class="pg">p. {unit_pages[u["n"]]}</span></div></div></a>""" for u in UNITS)
    backs = " · ".join(f"{t} p. {p}" for t, p in back)
    return f"""<section class="page"><div class="inner">
 <div class="ptitle">{logo(30)}<h2>Contents</h2><div class="bar"></div><small>12 UNITS · 24 TASKS</small></div>
 <div class="toc six">{cards}</div><p class="backlist">{e(backs)}</p>
</div><div class="pfoot"><span><b>{SCHOOL}</b> · {BOOK}</span><span>{CFG["source"]}</span></div></section>"""


def build():
    front = [cover(), how_to()]
    p = len(front) + 2
    body, unit_pages = [], {}
    for u in UNITS:
        unit_pages[u["n"]] = p
        for make in (page_model, page_practice, page_task, page_ielts):
            body.append(frame(make(u), p))
            p += 1
    back_index = [("Writing bank", p), ("Common mistakes", p + 2), ("Answer key", p + 3), ("Model answers", p + 4)]
    body += bank_pages(p)
    body.append(mistakes_page(p + 2))
    body.append(key_page(p + 3))
    p += 4
    for i in range(0, len(UNITS), 2):
        body.append(model_answer_page(UNITS[i:i + 2], p))
        p += 1
    pages = front + [contents(unit_pages, back_index)] + body
    css = (SPEAKING / "style.css").read_text(encoding="utf-8") + (ROOT / "scripts" / "style.css").read_text(encoding="utf-8")
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{SCHOOL} — {BOOK}</title><style>{css}</style></head><body class="lvl-{LEVEL.lower()}">{''.join(pages)}</body></html>"""
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / f"{LEVEL.lower()}-writing-book.html").write_text(doc, encoding="utf-8")
    print("pages:", len(pages))


if __name__ == "__main__":
    build()
