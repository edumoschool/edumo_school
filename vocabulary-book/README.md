# Impulse Learning Center — A1 Vocabulary Book

A unit-by-unit vocabulary book (Navigate A1, Units 1–10, 775 words) in the
style of the *Vocabulary for IELTS* book, re-themed in dodger blue for
Impulse Learning Center.

Each entry has: CEFR level · word + part of speech · IPA transcription ·
simple English definition · example sentence (headword highlighted) ·
Russian · Uzbek. Words are grouped by part of speech inside every unit,
followed by themed lists (numbers, countries, days, months).

## Files

- `dist/Impulse_A1_Vocabulary_Book.pdf` — the finished book (A4 landscape)
- `dist/front.html`, `dist/body.html` — the HTML source pages
- `data/navigate-a1-words.json` — all word data (edit here to fix a translation)
- `scripts/parse_wordlist.py` — extracts words from the Navigate wordlist PDF text
- `scripts/build_html.py` — generates the HTML; `scripts/render.js` prints it to PDF

## Rebuild

Requires Python 3, Node with Playwright (Chromium) and poppler-utils.

```bash
./build.sh
```
