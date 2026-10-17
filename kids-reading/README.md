# Read Time! 1 — kids reading comprehension book (Teen2Teen 1 topics)

A5, playful and colourful, companion to "Talk Time! 1". 12 units, 12 original texts (email, blog, chat, diary,
story, poster, letter, article, interview, quiz), A1 level, Uzbek instructions, answer key at the end.

Each unit has 4 pages and 9 steps:
1. **Before You Read** – 6 picture word cards + a guessing question
2. **Read** – the text in a styled "window" for its text type, key words highlighted
3. **True or False?** · 4. **Choose the Answer** · 5. **Match** (word ↔ picture)
6. **Fill the Gaps** (word bank) · 7. **Word Search** (generated 10×10 puzzle) · fun fact
8. **About You** · 9. **Draw & Write** · "How did I do?" faces

## Build
```
python3 scripts/build.py      # data/units/*.json -> dist/read-time.html
node scripts/render.js        # -> dist/Read_Time_1.pdf (A5, warns about overflowing pages)
```
Unit data format: `SCHEMA.md`. Styles: `scripts/style.css` + `scripts/kids.css` (shared) + `scripts/reading.css`.
