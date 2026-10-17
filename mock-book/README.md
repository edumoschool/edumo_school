# Multilevel Mock Tests — Listening & Reading

Twelve complete Uzbek Multilevel (CEFR) mock tests (Listening Parts 1–6, Reading Parts 1–5) from the
"Multilevel with Halikulov" mock PDFs (mocks 1–2) `src/M3.pdf`, `src/M6.pdf`, `src/M10.pdf` ("Multilevel Zone" tests 1–10 → mocks 3–12) in `src/`, laid out in a compact **two-column A4** design with the
Impulse / Unlock 5 style cover (white + blue band, 3D illustration, Uzbek girih ornaments).

Contents: cover · how to use (with audio channel QR) · Mock Tests 1–12 (Listening, Reading, then a Multilevel answer sheet)
· answer key (reading solved; listening blanks to fill from the audio) · back cover.

## Build
```
./build.sh     # -> dist/Multilevel_Mock_Tests.pdf (book) and dist/Mock_Cover_spread_A4.pdf (print spread)
```
- `data/listening-N.json`, `data/reading-N.json` — the tests (format in `SCHEMA.md`). Add `listening-3.json` +
  `reading-3.json` to get Mock Test 3 automatically.
- `scripts/render.js` — splits sections into paragraphs/questions and flows them through the two columns.
- `scripts/cover.py` — cover (A3 design, scaled to A4 in `scripts/merge.py`).
- Sources: Mock 1 = `src/L1b.pdf` + `src/R1b.pdf` (official answers from the Halikulov answer image); Mock 2 = `src/L2.pdf` + `src/R2.pdf`.
  (`src/L1.pdf`/`R1.pdf` were the earlier Mock 1, now replaced.)

## Answer key
- Mocks 3–12 (Multilevel Zone tests 1–10): **official answers** from `src/answers.pdf`, typed into `data/keys/official.json`
  (Zone test n = mock n+2). `src/answers.pdf` also contains the audio scripts.
- Mock 1 (Halikulov): official answers (from the Halikulov answer image), also in `data/keys/official.json`.
- Mock 2 (Halikulov): reading answers worked out by us (`"key"` in `data/reading-2.json`); listening left blank.

Small source fixes: Mock 4 map places renumbered 16–20 → 19–23; Mock 10 "19. Speaker 4" → "18."; Mock 11 extract
headings (all printed "Extract One"); Mock 12 map instruction A–H → A–I (the map and the official answer use I).
