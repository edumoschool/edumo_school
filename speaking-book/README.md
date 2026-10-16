# Impulse Learning Center — Speaking Books (A1 & A2)

Speaking-question books based on Navigate topics, designed to match the
Impulse vocabulary books.

| Book | Units | Lessons | Questions | Pages |
|------|-------|---------|-----------|-------|
| `dist/Impulse_A1_Speaking_Book.pdf` | 10 | 50 | 250 | 33 |
| `dist/Impulse_A2_Speaking_Book.pdf` | 12 | 60 | 600 | 75 |

Both books share the same bright blue design (`scripts/style.css`).

**A1** — two lesson cards per page, each with five questions and answer
lines, words & phrases (with Uzbek) and answer starters, plus a review card
per unit.

**A2** — ten questions per lesson, so each lesson is a full-width card on
its own page: questions with answer lines, words & phrases (with Uzbek),
answer starters, a notes box and a speaking tip. Each unit opens with a
banner and ends with a review page (two-minute talk, can-do checklist,
new-words lines).

## Files

- `data/questions.json`, `data/helpers.txt` — A1 questions; words (`w: English = Uzbek`) and starters (`s:`)
- `data/a2-questions.json`, `data/a2-helpers.txt` — the same for A2
- `scripts/build.py` + `style.css` (A1), `scripts/build_a2.py` + `style_a2.css` (A2 additions on top of `style.css`)
- `scripts/render.js` — prints a book's HTML to PDF and warns about overflowing pages

## Rebuild

```bash
./build.sh
```
