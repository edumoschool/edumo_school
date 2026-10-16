# Impulse Speak Up! A2 — speaking method book (sample: Unit 1)

A5 speaking book in a playful design (Fredoka + Nunito fonts, emoji, colour stickers).
Each unit has 6 pages and 7 sections:

1. **Topic Vocabulary** — 24 words in groups with Uzbek, audio (listen & repeat)
2. **Story** — the words in context (highlighted), audio, read 3 times, true/false, retell with keywords
3. **Remember the Words** — gap-fill from memory with a word bank
4. **Useful Phrases** — 8 speaking chunks with Uzbek + "make it yours"
5. **Answer the Questions** — 8 questions, answer + reason + example, sample answers, ask a partner
6. **Real Speaking** — model speech (audio), say it 4 ways (news reader / just me / superstar / coach), your version
7. **Speaking Assistant** — start / continue / finish phrases, 1-minute challenge (3 tries), speech plan, "Now I can"

## Files

- `data/config.json` — book settings, including `audio_base_url` (where the MP3s will be hosted; the QR codes point there)
- `data/units/NN-*.json` — unit content
- `scripts/make_audio.py [unit]` — creates `dist/audio/uNN-1-words|2-story|3-speech.mp3` with OpenAI TTS (clips cached in `audio-cache/`, ~$0.03 per unit)
- `scripts/build.py` → `dist/speak-up.html`; `scripts/render.js` → `dist/Impulse_Speak_Up_A2.pdf`

## Rebuild

```bash
python3 scripts/make_audio.py && python3 scripts/build.py && node scripts/render.js
```
