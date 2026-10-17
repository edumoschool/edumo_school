# Mock book data (`data/listening-N.json`, `data/reading-N.json`)

Copy the exam **faithfully** from the source text (`src/*.txt`, extracted with pdftotext -layout from the PDFs in `src/`).
Remove watermark/header junk only: "Multilevel with Halikulov.", "@Multilevel_Halikulov", "BAGDAD", "BAGDAD 2024/2025",
page numbers, broken hyphenation, stray line breaks inside sentences. Keep the original wording, numbering and instructions.
Fix nothing else (keep the test's own small errors). Markup allowed in strings: `**bold**`, `*italic*`, `\n` line break.

```jsonc
{
  "skill": "listening" | "reading",
  "mock": 1,
  "parts": [
    {"part": 1, "blocks": [ … ]},   // listening: parts 1–6; reading: parts 1–5
    …
  ],
  "key": {"1": "1 game  2 available …", …}   // READING ONLY: solve every question yourself (by part). Listening: omit "key".
}
```

## Blocks
| type | fields | renders as |
|---|---|---|
| `instruction` | `text`, optional `"audio": true` (listening) | bold instruction paragraph |
| `subtitle` | `text` | small bold heading, e.g. "Extract One" or "You hear a university tutor…" (put context lines here, italic) |
| `article` | `title` (may be ""), `paragraphs` [..] | reading text, justified |
| `text` | `paragraphs` [..] | plain paragraphs (gap texts) |
| `headings` | `title`, `items` ["A) …"], `right` ["15. Paragraph I", …] | boxed list of headings |
| `statements` | `items` ["A) …", …] | simple list |
| `cards` | optional `title`, `items` [{"title": "7. …", "body": "…"}] | numbered short texts / adverts in boxes |
| `mcq` | `items` [{"n": 21, "q": "…", "options": ["A) …", "B) …"]}] | multiple choice |
| `notes` | `title`, `lines` [..] (keep gaps like `9…………` or `(30) …………`; for two-column notes use "Label: text") | boxed gap-fill notes |
| `matching` | `left` [..], `right` [..] | two-column matching (Listening Part 3) |
| `image` | `src` (file in `assets/`), optional `width` (% of column, default 100) | picture / map |
| `lines` | `items` [..] | numbered lines, e.g. "19. Newspapers ……" |
