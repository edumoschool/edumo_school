# Multilevel Mock Tests — Listening & Reading

Two complete Uzbek Multilevel (CEFR) mock tests (Listening Parts 1–6, Reading Parts 1–5) from the
"Multilevel with Halikulov" mock PDFs in `src/`, laid out in a compact **two-column A4** design with the
Impulse / Unlock 5 style cover (white + blue band, 3D illustration, Uzbek girih ornaments).

Contents: cover · how to use (with audio channel QR) · Mock Test 1 (Listening, Reading) · Mock Test 2 (Listening, Reading)
· answer sheet for each mock · answer key (reading solved; listening blanks to fill from the audio) · back cover.

## Build
```
./build.sh     # -> dist/Multilevel_Mock_Tests.pdf (book) and dist/Mock_Cover_spread_A4.pdf (print spread)
```
- `data/listening-N.json`, `data/reading-N.json` — the tests (format in `SCHEMA.md`). Add `listening-3.json` +
  `reading-3.json` to get Mock Test 3 automatically.
- `scripts/render.js` — splits sections into paragraphs/questions and flows them through the two columns.
- `scripts/cover.py` — cover (A3 design, scaled to A4 in `scripts/merge.py`).
- Sources: `src/L1.pdf` (Listening mock 1; its second half equals `R2.pdf`), `src/L2.pdf`, `src/R1.pdf`, `src/R2.pdf`.
