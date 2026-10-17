"""Build the Multilevel Practice Book interior (A4, two columns, Mock-book design) -> dist/mock.html.

Organised by exam part: every part opens with a banner and a strategy box, then all practice tests of that part
(data/<skill>-part-N.json), then an answer grid. Answer key (data/keys/*.json if present, otherwise blanks) at the end.
Uses the block renderer of the mock book (scripts/blocks.py).
"""
import json
import re

from blocks import CHANNEL, DIST, EMOJI, QRANGE, ROOT, block, e, md, qr_svg, split

DATA = ROOT / "data"
SKILL = {"listening": ("🎧", "LISTENING"), "reading": ("📖", "READING")}
TASK = {
    ("listening", 1): ("Choose the correct reply", [
        "Read the three replies before you listen and think about what kind of sentence each one answers (a question, an offer, an apology…).",
        "Listen for the function, not for repeated words — an option that repeats a word you hear is often a trap.",
        "You hear each sentence twice: choose on the first listening, check on the second."]),
    ("listening", 2): ("Complete the notes", [
        "Before you listen, read the notes and predict the kind of word for each gap: a number, a name, a noun…",
        "Write ONE WORD and/or A NUMBER only. Check spelling — names are often spelled out for you.",
        "The answers come in the same order as the notes. Don't stop if you miss one — move on."]),
    ("listening", 3): ("Match the speakers", [
        "Underline the key idea in each option A–F before you listen.",
        "Speakers rarely use the same words as the options — listen for the meaning (paraphrase).",
        "Two options are extra. Use the second listening to check the speakers you were unsure about."]),
    ("listening", 4): ("Label the map / plan", [
        "Find the starting point (entrance, 'You are here') and the compass before the talk starts.",
        "Listen for direction language: opposite, next to, behind, on your left, at the end of…",
        "The places 19–23 come in order. Three letters on the map are extra."]),
    ("listening", 5): ("Multiple choice: three extracts", [
        "Read the context line of each extract — who is speaking and where?",
        "There are two questions per extract and they follow the order of the conversation.",
        "Questions often test opinion, attitude or purpose — listen to the whole idea, not single words."]),
    ("listening", 6): ("Complete the lecture notes", [
        "Read the notes first and predict the missing words.",
        "Write no more than ONE WORD for each answer, spelled correctly.",
        "The lecture is long — keep your place by following the notes line by line."]),
    ("reading", 1): ("Gap fill: one word from the text", [
        "Every missing word appears somewhere else in the text — scan for it.",
        "Check the grammar around the gap: singular/plural, verb form, article.",
        "Read the whole sentence again with your word in it."]),
    ("reading", 2): ("Match texts to statements", [
        "Read the statements first and underline the key requirement in each.",
        "Scan the texts for paraphrases of those requirements.",
        "Two statements are extra — don't force a match."]),
    ("reading", 3): ("Match headings to paragraphs", [
        "Read each paragraph's first and last sentences to find the main idea.",
        "A heading must cover the whole paragraph, not just one detail.",
        "Cross out headings as you use them; some are extra."]),
    ("reading", 4): ("Multiple choice + True / False / No information", [
        "Questions follow the order of the text.",
        "'False' means the text says the opposite; 'No information' means the text doesn't say.",
        "Don't use your own knowledge — only the text counts."]),
    ("reading", 5): ("Summary completion + multiple choice", [
        "Read the summary first to understand what's missing.",
        "Find the matching part of the text and copy the word exactly.",
        "Check the word limit for each answer."]),
}


def load_parts():
    out = []
    for f in sorted(DATA.glob("*-part-*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        out.append(d)
    out.sort(key=lambda d: (d["skill"] != "listening", d["part"]))
    return out


def qnums(skill, part):
    a, b = QRANGE[skill][part].split("–")
    return list(range(int(a), int(b) + 1))


def test_block(skill, part, t):
    head = (f'<div class="phead"><span class="pill">TEST {t["test"]}</span>'
            f'<span class="qr">Questions {QRANGE[skill][part]}</span></div>')
    return f'<div class="part">{head}{"".join(block(b) for b in t["blocks"])}</div>'


def answer_grid(skill, part, tests):
    nums = qnums(skill, part)
    wide = (skill, part) in {("listening", 2), ("listening", 6), ("reading", 1), ("reading", 5)}
    head = "".join(f"<th>{n}</th>" for n in nums)
    rows = "".join(f'<tr><th>Test {t["test"]}</th>' + "<td></td>" * len(nums) + "</tr>" for t in tests)
    return (f'<div class="part"><div class="phead"><span class="pill">MY ANSWERS</span>'
            f'<span class="qr">Part {part} · Tests 1–{len(tests)}</span></div>'
            f'<table class="agrid2{" wide" if wide else ""}"><tr><th></th>{head}</tr>{rows}</table>'
            f'<p class="score">Score: write your total for each test in the margin ( / {len(nums)} ).</p></div>')


def part_section(d):
    skill, part, tests = d["skill"], d["part"], d["tests"]
    icon, title = SKILL[skill]
    task, tips = TASK[(skill, part)]
    tip_html = "".join(f"<li>{e(t)}</li>" for t in tips)
    banner = (f'<div class="banner"><div class="girih"></div><div class="bl"><small>{title} · PART {part}</small>'
              f'<h1>{icon} {e(task.upper())}</h1></div><div class="br"><b>{len(tests)} practice tests</b>'
              f'<span>Questions {QRANGE[skill][part]}</span>'
              + (f'<span>🎧 Audio: {CHANNEL}</span>' if skill == "listening" else "") + "</div></div>")
    guide = f'<div class="part"><div class="box guide"><b>💡 How to do Part {part}</b><ul>{tip_html}</ul></div></div>'
    body = guide + "".join(test_block(skill, part, t) for t in tests) + answer_grid(skill, part, tests)
    return (f'<section class="page flow first" data-run="{title.title()} Part {part}">{banner}'
            f'<div class="cols"><div class="col">{body}</div><div class="col"></div></div>'
            f'<footer><span>Multilevel Practice Book · {title.title()} Part {part}</span><span class="pno"></span></footer></section>')


def answer_key(parts):
    keys = {}
    for f in sorted((DATA / "keys").glob("*.json")) if (DATA / "keys").exists() else []:
        keys.update(json.loads(f.read_text(encoding="utf-8")))
    body = ""
    for d in parts:
        rows = ""
        for t in d["tests"]:
            k = keys.get(f'{d["skill"]}-{d["part"]}-{t["test"]}')
            ans = k or "  ".join(f"{n} ______" for n in qnums(d["skill"], d["part"]))
            rows += f'<tr><th>Test {t["test"]}</th><td>{md(ans)}</td></tr>'
        body += f'<div class="kmock"><h3>{SKILL[d["skill"]][1].title()} · Part {d["part"]}</h3><table>{rows}</table></div>'
    return (f'<section class="page flow" data-run="Answer key"><div class="banner small"><div class="girih"></div><div class="bl">'
            f'<small>ALL PARTS</small><h1>ANSWER KEY</h1></div><div class="br"><span>Fill in the listening answers from the audio</span></div></div>'
            f'<div class="cols"><div class="col">{split(body, "keys")}</div><div class="col"></div></div>'
            f'<footer><span>Multilevel Practice Book · Answer key</span><span class="pno"></span></footer></section>')


def how_page(parts):
    tips = [("🎯", "Part by part", "Each section trains ONE exam part with many practice tests, so you master the task type before the full exam."),
            ("💡", "Strategy first", "Every part starts with a short 'How to do it' box. Read it before the first test."),
            ("🎧", "Audio", "Scan the QR code and play the recording for each test. You hear every recording twice."),
            ("📝", "My answers", "Write your answers in the grid at the end of each part and track your score."),
            ("🔑", "Answer key", "Check your answers at the back of the book.")]
    cards = "".join(f'<div class="tip"><span>{i}</span><div><b>{t}</b><p>{d}</p></div></div>' for i, t, d in tips)
    rows = "".join(f'<tr><td>{SKILL[d["skill"]][0]}</td><td>{d["part"]}</td><td>{e(TASK[(d["skill"], d["part"])][0])}</td>'
                   f'<td>{QRANGE[d["skill"]][d["part"]]}</td><td>{len(d["tests"])}</td></tr>' for d in parts)
    return (f'<section class="page howpage"><div class="banner"><div class="girih"></div><div class="bl"><small>MULTILEVEL · CEFR</small>'
            f'<h1>HOW TO USE THIS BOOK</h1></div><div class="br"><b>Practice Book</b><span>Part by part</span></div></div>'
            f'<p class="lead">This book trains every part of the <b>Multilevel (CEFR)</b> exam separately, with many real-format '
            f'practice tests for each part. Learn the strategy, practise until the task feels easy, then move on.</p>'
            f'<div class="tips">{cards}</div>'
            f'<div class="audio"><div class="qrc">{qr_svg("https://" + CHANNEL)}</div><div><b>🎧 Audio for all listening tests</b>'
            f'<p>Scan the QR code to open our Telegram channel.</p><span>{CHANNEL}</span></div></div>'
            f'<table class="plan"><tr><th>Skill</th><th>Part</th><th>Task</th><th>Questions</th><th>Tests</th></tr>{rows}</table>'
            '<footer><span>Multilevel Practice Book</span><span class="pno"></span></footer></section>')


def build():
    parts = load_parts()
    pages = [how_page(parts)] + [part_section(d) for d in parts] + [answer_key(parts)]
    css = (ROOT / "scripts" / "style.css").read_text(encoding="utf-8") + (ROOT / "scripts" / "practice.css").read_text(encoding="utf-8")
    fonts = ('<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@400;600;700;800'
             '&family=Open+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400;1,600&display=block" rel="stylesheet">')
    body = EMOJI.sub(r'<span class="em">\1</span>', "".join(pages))
    doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Multilevel Practice Book</title>{fonts}<style>{css}</style></head><body>{body}</body></html>'
    DIST.mkdir(exist_ok=True)
    (DIST / "mock.html").write_text(doc, encoding="utf-8")
    print("parts:", [(d["skill"], d["part"], len(d["tests"])) for d in parts])


if __name__ == "__main__":
    build()
