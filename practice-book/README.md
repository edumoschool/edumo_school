# Multilevel Practice Book

The exam is trained part by part. Each part opens with a strategy box, then has 8 practice tests, a "My answers" grid, and an answer key at the back. It uses the Multilevel Mock Tests design with a new cover hero.

- Data: `data/<skill>-part-N.json`. The block format is in `SCHEMA.md` and `SCHEMA_BLOCKS.md`. Images are in `assets/`.
- Answer keys (optional): `data/keys/*.json`, e.g. `{"listening-1-1": "1 A  2 B ..."}`. Missing keys print as blank lines.
- Build: `./build.sh` → `dist/Multilevel_Practice_Book.pdf` and `dist/Practice_Cover_spread_A4.pdf`

Contents now: Listening Parts 1–6, 8 tests each. Answer keys are in for Parts 2–6. Still to add: the Part 1 key and Reading Parts 1–5.
