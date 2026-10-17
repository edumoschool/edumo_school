# Read Time! 1 — kids reading book: unit data (`data/units/NN-name.json`)

A1 readers, ages 10–13, Uzbek learners. Same 12 topics as Teen2Teen 1 / "Talk Time! 1"
(see `../kids-speaking/src/teen2teen1.txt` for each unit's grammar and vocabulary — use that grammar in the text).
Very simple English: short sentences, present simple (+ the unit's grammar), common words. Uzbek in Latin script (o‘, g‘).
Markup: `**word**` = highlighted key word in the text (highlight exactly the 6 "before" words where they appear).

```jsonc
{
  "n": 1,
  "title": "Hello, new friends!",       // fun reading title for the unit (not the Teen2Teen title)
  "topic": "Greetings",                   // Teen2Teen topic in 1–3 words
  "emoji": "👋",
  "color": "green",                       // given to you
  "text_type": "email",                   // given to you: email | blog | story | poster | diary | chat | interview | letter | quiz | article
  "before": {
    "words": [["hello", "salom", "👋"], …],                    // EXACTLY 6 key words from the text: English, Uzbek, one colourful emoji
    "predict": "Look at the picture and the title. Who is Laylo writing to?"   // 1 short warm-up question
  },
  "text": {
    "title": "A message from Laylo",
    "meta": "From: Laylo · To: Emma",      // small line above the text that fits the text type ("" if none)
    "paragraphs": ["Hi Emma! …", …],       // 130–170 words in total, 3–5 short paragraphs; chat: each paragraph "Name: line"
    "picture": "📧"                         // 1–3 emoji shown as the text's "picture"
  },
  "tf": [["Laylo is from Samarkand.", true], …],              // EXACTLY 5 true/false sentences
  "mcq": [{"q": "How old is Laylo?", "options": ["10", "11", "12"], "answer": 1}, …],   // EXACTLY 4, 3 options, answer = index
  "match": [["happy", "😊"], …],             // EXACTLY 5 words from the text matched to ONE clear emoji each (shuffled when printed)
  "gaps": [["Laylo’s ___ is Emma.", "friend"], …],           // EXACTLY 5 sentences about the text, one ___ each; answers are single words from the text
  "wordsearch": ["HELLO", "FRIEND", …],     // EXACTLY 8 words from the text, A–Z only, 3–8 letters, no spaces
  "about_you": ["What is your name?", …],    // EXACTLY 3 personal questions (pupils write 1 sentence each)
  "draw": "Draw you and your best friend. Write two sentences.",   // 1 draw-and-write task
  "fun_fact": "In English, people often say “Hi!” to friends and “Hello!” to teachers."   // 1 short fun fact on the topic
}
```
