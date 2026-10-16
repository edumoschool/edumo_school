# Impulse Learning Center — Writing Books (A2 & B1)

| Book | Units | Pages |
|------|-------|-------|
| `dist/Impulse_A2_Writing_Book.pdf` | 12 (opinion paragraphs) | 61 |
| `dist/Impulse_B1_Writing_Book.pdf` | 12 (IELTS GT-style letters + Task 2-style essays) | 61 |

The B1 book follows the Navigate Pre-intermediate B1 unit topics and vocabulary:
informal, semi-formal and formal letters (complaint, enquiry, covering letter),
an article, a story, a review and a description, plus opinion, discussion,
advantages/disadvantages and problem/solution essays of 120–160 words.

## A2 Writing Book

A 61-page writing book (A4 landscape) on the Navigate Elementary A2 unit
topics, in the same blue design as the speaking books. It reuses the
vocabulary and IELTS-style topics from the A2 vocabulary and speaking books.

**Each unit (4 pages)**
1. Model text with highlighted useful phrases
2. Language focus (one writing skill with examples)
3. Words & phrases — 10 collocations with Uzbek
4. Practice — gap-fill with a word box
5. Plan — one box of notes per paragraph
6. Writing task — real-life task, word count, self-check and lined space
7. IELTS-style task — opinion paragraph with ideas, a 4-step plan and lined space

**At the back:** writing bank (8 text types), common mistakes, answer key,
model answers for all 24 tasks.

| Unit | Text type | Opinion question |
|------|-----------|------------------|
| 1 Your World | Informal email | Is it important to learn a foreign language? |
| 2 My Day | Blog post: a typical day | Do people have enough free time? |
| 3 Work | Formal email: job application | Interesting job or well-paid job? |
| 4 Places and Things | Description of a place | City or countryside? |
| 5 Clothes and Shopping | Email of complaint | Online shopping or shops? |
| 6 Past Times | Story: a memorable day | Was life better in the past? |
| 7 Health and Sport | Message giving advice | More time for sport at school? |
| 8 Travel and Adventure | Travel blog: recommending a place | Travel alone or with friends? |
| 9 Food and Drink | Restaurant review | Should children learn to cook at school? |
| 10 The Natural World | Description of a natural place | How can we protect the environment? |
| 11 Communities | Formal letter: making a suggestion | Should young people volunteer? |
| 12 Arts and Entertainment | Film review | Films at home or at the cinema? |

## Files

- `data/a2-writing.txt`, `data/b1-writing.txt` — all unit content (edit here)
- `scripts/build.py LEVEL` — builds `dist/<level>-writing-book.html` (level settings, writing banks and common mistakes are in this file)
- `scripts/style.css` — writing-book styles, loaded after `../speaking-book/scripts/style.css`
- `scripts/render.js LEVEL` — prints `dist/Impulse_<LEVEL>_Writing_Book.pdf` and warns about overflowing pages

## Rebuild

```bash
./build.sh        # both books
./build.sh B1     # one book
```
