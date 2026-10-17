# Practice book data (`data/listening-part-N.json`, later `data/reading-part-N.json`)

Each file holds all practice tests of ONE exam part. Block types and cleaning rules: see `SCHEMA_BLOCKS.md`
(the same blocks as the mock book: instruction, subtitle, article, text, headings, statements, cards, mcq, notes,
matching, image, lines).

```jsonc
{
  "skill": "listening",
  "part": 1,
  "tests": [
    {"test": 1, "blocks": [ … ]},     // copy the test faithfully, keep its question numbers (e.g. 1–8)
    …                                 // all tests in the source, in order
  ]
}
```
Remove the State Testing Centre cover page (title, "Please write your full name…", booklet notes), watermarks,
page headers/footers. Keep each test's own instruction as an `instruction` block (listening: `"audio": true`).
Images (maps, pictures) go to `assets/` as `lp<part>-t<test>.png` and are used with an `image` block.
