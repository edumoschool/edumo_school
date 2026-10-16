# Impulse Learning Center — Vocabulary Books (A1 & A2)

Unit-by-unit vocabulary books based on the Navigate word lists, in the style
of the *Vocabulary for IELTS* book, themed in dodger blue for Impulse
Learning Center.

| Book | Units | Words |
|------|-------|-------|
| `dist/Impulse_A1_Vocabulary_Book.pdf` | 10 | 775 |
| `dist/Impulse_A2_Vocabulary_Book.pdf` | 12 | 705 |

Each entry has: word + part of speech · IPA transcription · simple English
definition · example sentence (headword highlighted) · Russian · Uzbek.
Words are grouped by part of speech inside every unit, followed by themed
lists (numbers, countries, days, months).

## Files

- `data/navigate-a1-words.json`, `data/navigate-a2-words.json` — all word data (edit here to fix a translation)
- `dist/a1/`, `dist/a2/` — generated HTML pages
- `assets/impulse-logo.png` — the school logo
- `scripts/parse_wordlist.py` — extracts words from a Navigate wordlist PDF (`pdftotext -raw` output)
- `scripts/build_html.py LEVEL` — generates the HTML; `scripts/render.js LEVEL` prints it to PDF

## Rebuild

Requires Python 3, Node with Playwright (Chromium) and poppler-utils.

```bash
./build.sh          # both books
./build.sh A2       # one book
```
