# Unit file: `data/units/NN.json` (one per EXERCISE of the source guide)

Source: `src/guide.pdf` (pages listed per exercise), text in `src/ex-NN.txt` (pdftotext, plain). The lined "TASK:" pages
are empty writing pages: ignore them. Fix extraction artifacts (missing spaces like "Newcolleagues-Yangihamkasblar"
→ "New colleagues – Yangi hamkasblar", broken line wraps, two-column vocab lists mixed together). Check the page images
(`pdftoppm -r 70 -f P -l P src/guide.pdf /tmp/x` then view) whenever the text is unclear. Keep the source wording of the
situation, email, tasks and sample answers (only fix obvious typos that would confuse students, and list them in your report).

```jsonc
{
  "n": 1,
  "topic": "Library closure",              // 1–3 words, for the unit banner
  "emoji": "📚",                           // one emoji for the topic
  "situation": "You are a member of a local community library. You received an email from the head librarian.",
  "email": {
    "kind": "email",                       // email | flyer | letter | complaint | announcement …  (what the source calls it)
    "greeting": "Dear Member,",
    "body": ["paragraph 1", "paragraph 2"],
    "signoff": "Best regards,",
    "from": "The Head Librarian"
  },
  "task11": "Write a letter to your friend, … Write about 50 words.",
  "task12": "Write a letter to the head librarian. … Write about 120-150 words.",
  "part2": {
    "context": "You are participating in an online discussion for language learners.",
    "question": "What are the advantages and disadvantages of online learning compared to traditional classroom learning?",
    "instruction": "Post your response, giving reasons and examples. Write 180-200 words."
  },

  // ---------- NEW EXERCISES (you write these; B1–B2 level, clear and short) ----------
  "read_qs": [                             // 4 comprehension questions on the email/situation, with short answers
    {"q": "Why is the library closing?", "a": "For renovations and upgrades to its facilities."}
  ],
  "plan": {                                // idea prompts for a planning page; specific to THIS topic
    "t11": ["How do you feel about the news?", "What should the library do?", "Suggest something to do together"],   // 3
    "t12": ["Paragraph 1 – why you are writing + your feelings", "Paragraph 2 – …", "Paragraph 3 – …", "Closing – …"], // 4
    "p2":  ["Your opinion in one sentence", "Advantage + example", "Disadvantage + example", "Conclusion – …"]          // 4
  },
  "register": [                            // 8 phrases taken from THIS unit's sample answers (4 informal, 4 formal), mixed order
    {"phrase": "I'm a bit gutted", "type": "informal"},
    {"phrase": "I must admit to feeling a degree of disappointment", "type": "formal"}
  ],
  "p2_gaps": ["On the plus side", "For instance", "Furthermore", "However", "The lack of", "Ultimately"],
       // 6 linking words/phrases that occur EXACTLY (case-sensitive) in samples.p2; first occurrence of each is gapped,
       // order = order of appearance in the text
  "samples": {
    "t11": "Hi Alex,\nCan you believe … \nBest,\nAlex",       // \n = new line, blank line \n\n = new paragraph
    "t12": "Dear Head Librarian,\n\nThank you for …\n\nSincerely,\nAlex",
    "p2":  "That's a really pertinent question. …\n\nOn the plus side, …"
  },
  "vocab": [["library", "kutubxona"], ["renovations", "ta'mirlash"]]
       // ALL vocabulary/phrase lists of this exercise from the source, in order (English, Uzbek), clean spacing,
       // English in lower case unless a proper noun; merge several lists (e.g. Part 1 list + Part 2 list) into one
}
```
`read_qs` exactly 4, `register` exactly 8, `p2_gaps` exactly 6 (all must be found in `samples.p2`).
Validate with `python3 -c "import json;json.load(open('data/units/NN.json'))"`.
