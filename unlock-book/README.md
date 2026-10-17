# Unlock 5 (Reading & Writing) — Units 4–10

C1 units in the same A3 design as the original Unit 2 / Unit 3, with Uzbek Multilevel (CEFR) exam practice.

| Unit | Topic | Reading practice | Listening practice | Writing | Speaking |
|---|---|---|---|---|---|
| 4 | Risk — Taking chances | Part 5, Test 1 | Part 5, Test 1 | Part 2 essay | Part 3 |
| 5 | Manufacturing — The future of making things | Part 1, Tests 1–2 | Part 6, Test 1 | Part 1.1 + 1.2 letters | Part 1.1 |
| 6 | Environment — A changing planet | Part 2, Test 1 | Parts 1 + 2, Test 1 | Part 2 essay | Part 2 |
| 7 | Architecture — Cities of tomorrow | Part 3, Test 2 | Part 3, Test 1 | Part 1.1 + 1.2 letters | Part 3 |
| 8 | Energy — Powering the future | Part 4, Test 2 | Part 4, Test 2 (map) | Part 2 essay | Part 2 |
| 9 | Medicine — Health & science | Part 5, Test 2 | Part 5, Test 2 | Part 1.1 + 1.2 letters | Part 1.1 |
| 10 | Ageing — Living longer | Part 3, Test 3 | Part 6, Test 2 | Part 2 essay | Part 3 |

Units 2–3 used Reading Part 3/4 Test 1 and Listening Part 3 Test 4 / Part 4 Test 1, so none are repeated.
An answer key for all units is at the end of the book.

## Build
```
python3 scripts/build.py          # data/units/*.json -> dist/units.html
node scripts/render.js            # paginates and prints dist/Unlock5_Units_4-10.pdf (A3)
```
- `SCHEMA.md` — the unit data format.
- `src/*.txt` — text extracted from the exam question papers and the original Units 2–3.
- `assets/covers/uNN.png` — cover illustrations; `assets/u08-map.png` — Listening Part 4 map.
