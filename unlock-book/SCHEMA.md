# Unit data format (`data/units/NN-topic.json`)

One JSON file per unit. The build script (`scripts/build.py`) turns it into ~14 A3 pages that copy
the design of the original Unit 2 / Unit 3 PDFs (Unlock 5 Reading & Writing based, C1 level,
Uzbek Multilevel / CEFR exam practice).

Reference for style, length and register: `src/Unit_2.txt` and `src/Unit_3.txt` (text of the
original units). Match their level (C1), density and length closely.

## Inline markup (allowed in every text string)
- `[[word]]`  → key vocabulary, printed **bold red** (use in articles and vocab sentences)
- `**text**`  → bold
- `*text*`    → italic
- `__` (two or more underscores) → kept as a gap line, e.g. `________`
- `\n` inside a string → line break

## Top-level fields

```jsonc
{
  "n": 4,                                  // unit number
  "title": "RISK",                         // big cover word, UPPERCASE, 1 word ideally
  "subtitle": "TAKING CHANCES",            // small cover line, UPPERCASE
  "cover_color": "#0B3B60",                // dark band colour on the cover (title block)
  "image_prompt": "…",                     // prompt for an illustrated cover picture (no text in image)
  "warmup": ["q1", "q2", "q3", "q4"],      // 4 warm-up speaking questions

  "article1": {
    "title": "WHAT MAKES A LOGO WORK?",    // UPPERCASE
    "vocab": [                             // EXACTLY 8 sentences, each with ONE [[word]] (the word as used in the article)
      "Before choosing a designer, the company drew up a clear list of [[criteria]] the new logo had to meet.", …
    ],
    "definitions": ["(adj) next; happening after something else", …],   // EXACTLY 8, order a–h, SHUFFLED vs. sentences
    "paragraphs": ["A good logo does …", …],   // EXACTLY 7 paragraphs, 60–110 words each; all 8 vocab words appear as [[word]]
    "headings": ["Doing a lot in a small space", …]  // EXACTLY 8 headings A–H (7 match paragraphs, 1 extra), shuffled
  },

  "word_forms": [                          // EXACTLY 5: "Complete the sentences with the correct form of a word from either article."
    ["Environmental ________ has become one more factor designers must consider today.", "sustainable"], …
  ],

  "language_dev": {
    "title": "Describing emotional responses",          // after "LANGUAGE DEVELOPMENT - "
    "skill_name": "Verb + noun collocations",
    "skill_text": "Certain verbs regularly combine with … for example [[evoke memories]], or [[stir up controversy]]. …",
    "table": [["evoke", "feelings, memories, emotions (mixed)"], …],  // EXACTLY 6 rows
    "instruction": "Complete the sentences with the correct collocation from the table above.",
    "sentences": ["The unusual new logo ________ a lot of criticism online within hours of its release.", …] // 5 or 6
  },

  "article2": {
    "title": "WHY DO BRANDS REBRAND?",
    "intro": "The sentences below are about rebranding. Choose the correct meaning (a, b or c) for the word in bold.",
    "vocab": [                             // EXACTLY 8 items; each word also appears as [[word]] in article2 paragraphs
      {"q": "The new packaging design faced strong [[opposition]] to its bright colour scheme from long-time customers.",
       "options": ["support for", "disagreement with", "confusion about"]}, …
    ],
    "paragraphs": ["Every few years, …", …],   // EXACTLY 6 paragraphs, 80–120 words each
    "discussion": ["Think of a logo you dislike. What would you change about it, and why?", "…"] // EXACTLY 2
  },

  "grammar": {
    "title": "Defining relative clauses, omission & reduced clauses",    // small line under orange GRAMMAR bar
    "intro": "Defining relative clauses add essential information …",     // 2–3 sentences, italic paragraph
    "rules_intro": "The rules below explain when …",
    "rules": [ {"rule": "Use **who/that** for people, and **which/that** for things, …", "example": "The designer who created the logo later became famous …"}, … ], // 5 or 6
    "exA": {"instruction": "Exercise A — Complete the paragraph …", "text": "The designer (1) ___________ created our new logo …"},  // 8 gaps
    "exB": {"instruction": "Exercise B — Combine each pair of sentences …", "items": ["The design studio is in the old power station. Our designers create new prototypes there. (where)", …]} // 4–6
  },

  "academic": {
    "subtitle": "Paraphrasing — expressing other people's ideas in your own words",  // under orange ACADEMIC WRITING bar
    "skill_name": "Paraphrasing",
    "skill_text": "Paraphrasing means …",                     // 2–3 sentences
    "example": [["ORIGINAL", "A good logo must …"], ["PARAPHRASE", "For a logo to work well, …"]],  // 0–2 pairs, may be []
    "instruction": "Paraphrase the sentences below in your own words, without copying the original phrasing.",
    "items": ["Logos should be flexible enough …", …],      // 5–8 items (each gets a writing line)
    "task": "Write a short paragraph (80–100 words) …"        // WRITING TASK
  },

  "reading":   { "part": 3, "test": 2, "blocks": [ … ] },   // exam practice, see "Blocks"
  "wordlist":  ["entity", "flourish", "trace back to", …],   // EXACTLY 30 useful C1 words/phrases taken from the READING PRACTICE text, in text order
  "listening": { "part": 3, "test": 1, "blocks": [ … ] },
  "idioms": [["Stretched to the limit", "Pushed as far as possible; almost exhausted."], …],  // EXACTLY 15 phrases & idioms (topic-related, C1)

  "writing":  { … },   // see "Writing"
  "speaking": { … },   // see "Speaking"

  "key": {             // ANSWER KEY (printed at the end of the book)
    "article1_vocab": "1 c  2 d  3 e …",       // sentence → definition letter
    "word_forms": "1 sustainability  2 associated …",
    "headings": "1 A  2 B …",
    "language_dev": "1 provoked  2 inspire …",
    "article2_vocab": "1 b  2 a …",
    "grammar_a": "1 who/that  2 –  3 …",
    "grammar_b": "1 The design studio is in the old power station where our designers …",
    "reading": "15 B  16 D …"                 // solve the exam reading test yourself from the text
  }
}
```

## Blocks (reading / listening)
Copy the exam test **faithfully** from the given `src/*_Questions.txt` file (fix only obvious OCR
junk such as stray watermark words like "BAGDAD 2025", broken hyphenation, page numbers and headers).
Keep the original numbering (e.g. questions 15–20) and instructions.

| type | fields | renders as |
|---|---|---|
| `instruction` | `text`, optional `"audio": true` | bold instruction line (audio icon for listening) |
| `article` | `title`, `paragraphs` [..], optional `"cols": 2` (default 2) | reading text, justified, 2 columns |
| `text` | `paragraphs` [..] | plain paragraphs, 1 column (e.g. Part 1 gapped text) |
| `headings` | `title`, `items` [..], `right` [..] | teal box: list of headings on the left, numbered answer lines on the right |
| `statements` | `items` ["A) …", …] | simple list |
| `cards` | `items` [{"title": "7. Breezy Bean Café", "body": "…"}] | numbered short texts (Reading Part 2) |
| `mcq` | `items` [{"n": 21, "q": "…", "options": ["A) …", "B) …"]}], optional `"cols": 2` | multiple choice |
| `notes` | `title`, `lines` [..] | gap-fill notes (Listening 2 / 6, Reading 5 summary) — keep `9______` style gaps |
| `matching` | `left` [..], `right` [..] | two-column matching (Listening 3) |
| `image` | `src` (relative to `assets/`), `width` (mm, optional) | picture/map |
| `lines` | `items` [..] | plain numbered lines, e.g. "19. Adventure course …" |

## Writing
Two kinds, set by `"kind"`.

**`"kind": "letter"`** (Multilevel Writing Task 1.1 informal + 1.2 formal), like Unit 2:
```jsonc
{"kind": "letter", "title": "WRITING PART 1.2",
 "useful_title": "USEFUL LANGUAGE — Formal letter",
 "useful": [["Opening", "Dear Sir/Madam, / Dear [Title], / I am writing in response to …"], …],  // 5 rows
 "practice_title": "PART 1.1 PRACTICE",
 "situation": "You are a member of a local … You received this email from …",
 "email": "Dear Member,\nI'm writing to let you know …\nBest wishes,\nThe Director",   // 90–130 words
 "task11": "Task 1.1 — Write a letter to your friend … Write about 50 words.",
 "task12": "Task 1.2 — Write a letter to the … Write about 120–150 words.",
 "rules_title": "RULES for Task 1.2 (formal letter)",
 "rules": ["Respond to the SAME message as Task 1.1 — …", …],    // 5–6
 "sample_title": "SAMPLE ANSWER",
 "sample": "Dear Director,\n…\nYours faithfully,\nN. Yusupova",  // a model Task 1.2 answer, 140–170 words
 "practice2_title": "TASK 1.2 PRACTICE — now you try, with a new message",
 "situation2": "…", "email2": "…", "task2": "Task 1.2 — Write a letter … Write about 120–150 words."}
```

**`"kind": "essay"`** (Multilevel Writing Part 2, 180–200 word essay):
```jsonc
{"kind": "essay", "title": "WRITING PART 2",
 "useful_title": "USEFUL LANGUAGE — Opinion essay",
 "useful": [["Introducing the topic", "It is often argued that … / In recent years, …"], …],   // 6 rows
 "task_intro": "You are writing an essay for an academic audience. Write 180–200 words.",
 "task": "Some people believe … To what extent do you agree or disagree?",
 "plan": [["Introduction", "paraphrase the question + your position"], …],      // 4 rows (paragraph plan)
 "rules_title": "RULES for Part 2 (essay)",
 "rules": ["…", …],        // 5–6 checklist items
 "sample_title": "SAMPLE ANSWER",
 "sample": "…",            // model essay 190–210 words, paragraphs separated by \n
 "practice_title": "PART 2 PRACTICE — now you try",
 "practice_task": "…"}     // a second essay prompt on the unit topic
```

## Speaking
`"part"` is one of `"1.1"`, `"2"`, `"3"`.

```jsonc
// Part 2 (like Unit 2):
{"part": "2", "title": "SPEAKING PART 2",
 "prompt": "Describe a product or brand whose design you really admire.",
 "points": ["what the product or brand is", "what you like about its design", "how the design makes you feel or behave"],
 "end": "…and say whether you think design generally influences your own buying decisions.",
 "sample": "I'd like to talk about my phone, which I think has a **genuinely distinctive design**. …",  // 200–250 words, \n between paragraphs
 "useful": [["Introducing the topic:", "I'd like to talk about… / One product whose design I really admire is…"], …]}  // 6 rows

// Part 1.1: personal questions
{"part": "1.1", "title": "SPEAKING PART 1.1",
 "questions": ["…", "…", "…", "…", "…", "…"],               // 6 short questions on the topic
 "samples": [["question", "model answer 40–60 words with **bold** useful phrases"], …],   // 3
 "useful": [[label, phrases], …]}                          // 6 rows

// Part 3: discuss a statement using for/against points
{"part": "3", "title": "SPEAKING PART 3",
 "statement": "Governments should ban extreme sports.",
 "for": ["…", "…", "…"], "against": ["…", "…", "…"],     // short table points
 "sample": "…",              // 200–250 word model answer, \n between paragraphs, **bold** key phrases
 "useful": [[label, phrases], …]}                          // 6 rows
```
