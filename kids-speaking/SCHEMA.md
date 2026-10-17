# Kids speaking book — unit data (`data/units/NN-name.json`)

Book: **Teen2Teen 1 — Speaking** (A1, ages 10–13, Uzbek learners). 12 units × 10 questions from
`src/teen2teen1.txt`. Playful A5 design like the "Speak Up! A2" book (colour emoji, sticker headers).
Each unit = 4 pages: Word bank → Grammar helper + Talk time (Q1–5) → More talk (Q6–10) + survey → Game + mini talk + I can.

Keep English VERY simple (A1): short sentences, present simple, common words. Uzbek in Latin script (o‘, g‘ with ‘).
Markup: `**text**` = highlighted (use for the target grammar / useful words in sample answers and starters).

```jsonc
{
  "n": 1,
  "title": "Welcome to English class",          // from the docx, without the trailing full stop
  "emoji": "👋",                                // one emoji for the unit
  "color": "green",                              // given to you
  "grammar": "Verb be: affirmative and negative; Subject pronouns",   // from the docx
  "vocab_topic": "Greetings: hellos and goodbyes",                     // from the docx

  "words": [["hello", "salom", "👋"], …],          // EXACTLY 12 topic words/short phrases: English, Uzbek, ONE colourful emoji
  "pair_game": "Point at a picture. Your partner says the word. Then swap!",   // 1 short instruction for a word game
  "grammar_box": {
    "title": "Verb be",                          // short
    "rows": [["I", "am", "I’m Ali."], ["You", "are", "You’re my friend."], …],   // 4–6 rows: subject/word, form, example
    "tip": "Short forms: I am → I’m, you are → you’re"                          // 1 short tip (English), may include Uzbek in brackets
  },
  "questions": ["What is your name? How do you spell it?", …],      // EXACTLY the 10 questions from the docx, in order, unchanged
  "starters": ["My name is … . It’s spelled …", …],                  // EXACTLY 10 answer starters, one per question (with … gaps)
  "samples": [["What is your name? How do you spell it?", "My name is **Madina**. It’s spelled **M-A-D-I-N-A**."], …], // EXACTLY 3, 2–3 short sentences
  "survey": {"title": "Class survey", "question": "What is your favourite greeting?",   // ask 4 classmates, write answers
             "columns": ["Name", "Answer"]},
  "game": { "type": "find" | "dice" | "board" | "spinner" | "bingo" | "guess",  // type given to you
            "title": "Find someone who…", "rules": "Walk around the class. Ask: “Are you …?” Write a name.",
            "items": [ … ] },     // find: 8 short "… is good at English" items; dice: 6 prompts; board: 12 prompts;
                                  // spinner: 8 prompts; bingo: 9 prompts; guess: 6 "secret person" clue cards (2 short sentences each)
  "mini_talk": {"title": "All about me", "plan": ["Say hello and your name", "Say your age", "Say where you are from", "Say goodbye"],  // 3–4 steps
                "model": "Hello! My name is …"},   // 40–60 word model, very simple, **bold** target grammar
  "cando": ["say hello and goodbye", "talk about myself with be", "ask my friends questions"]   // EXACTLY 3, start with a verb
}
```
