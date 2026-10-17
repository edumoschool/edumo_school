# Talk Time! 1 — Teen2Teen 1 speaking book for kids

A5, playful design in the style of "Speak Up! A2" (colour emoji, sticker headers). 12 units, 120 questions from
`src/teen2teen1.txt` (Teen2Teen 1 speaking questions).

Each unit has 4 pages and 7 steps:
1. **Word Bank** – 12 picture cards (emoji, English, Uzbek) + "Point & say" pair game
2. **Grammar Helper** – the unit's grammar pattern with examples and a tip
3. **Talk Time** – questions 1–5 with answer starters
4. **More Talk** – questions 6–10 with starters + 3 example answers
5. **Class Survey** – ask 4 classmates
6. **Game Time** – find someone who / dice / board game / spinner / guess who / bingo
7. **My Mini Talk** – a 4-step plan, a model and 3 tries, then "Now I can" stars

## Build
```
python3 scripts/build.py      # data/units/*.json -> dist/talk-time.html
node scripts/render.js        # -> dist/Talk_Time_1.pdf (A5, warns about overflowing pages)
```
Unit data format: `SCHEMA.md`. Styles: `scripts/style.css` (shared with Speak Up!) + `scripts/kids.css`.
