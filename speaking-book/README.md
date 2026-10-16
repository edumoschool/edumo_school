# Impulse Learning Center — Speaking Books (A1, A2 & B1)

Speaking-question books based on Navigate topics, designed to match the
Impulse vocabulary books.

| Book | Units | Lessons | Questions | Pages |
|------|-------|---------|-----------|-------|
| `dist/Impulse_A1_Speaking_Book.pdf` | 10 | 50 | 250 | 33 |
| `dist/Impulse_A2_Speaking_Book.pdf` | 12 | 60 | 600 | 75 |
| `dist/Impulse_B1_Speaking_Book.pdf` | 6 | 30 topics | 240 + 30 cue cards | 39 |

Both books share the same bright blue design (`scripts/style.css`).

**A1** — two lesson cards per page, each with five questions and answer
lines, words & phrases (with Uzbek) and answer starters, plus a review card
per unit.

**A2** — ten questions per lesson, so each lesson is a full-width card on
its own page: questions with answer lines, words & phrases (with Uzbek),
answer starters, a notes box and a speaking tip. Each unit opens with a
banner and ends with a review page (two-minute talk, can-do checklist,
new-words lines).

**B1** — IELTS Speaking format: each topic page has Part 1 interview
questions, a Part 2 cue card and Part 3 discussion questions, with words &
phrases (Uzbek), useful language for the cue card and a notes box. Each unit
ends with a mock speaking test.

## Files

- `data/questions.json`, `data/helpers.txt` — A1 questions; words (`w: English = Uzbek`) and starters (`s:`)
- `data/a2-content.txt` — A2 lessons: real-life, IELTS-style questions (`q:`), words & phrases (`w: English = Uzbek`) and starters (`s:`)
- `data/a2-questions.json`, `data/a2-questions-source.txt` — the original A2 question list (unit titles are read from here)
- `scripts/build.py` + `style.css` (A1), `scripts/build_a2.py` + `style_a2.css` (A2 additions on top of `style.css`)
- `data/b1-questions.json` (from `b1-questions-source.txt`) — B1 Part 1 + Part 2; `data/b1-content.txt` — Part 3, words & phrases, useful language
- `scripts/build_b1.py` + `style_b1.css` (B1, on top of `style.css` + `style_a2.css`)
- `scripts/render.js` — prints a book's HTML to PDF and warns about overflowing pages

## Rebuild

```bash
./build.sh
```
