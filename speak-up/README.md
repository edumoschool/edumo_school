# Impulse Speak Up! A2 — speaking method book (sample: Unit 1)

A5 speaking book built on a 7-step speaking cycle per unit:

1. **Key phrases** — 15 high-frequency chunks with Uzbek (lexical approach)
2. **Listen & shadow** — dialogue audio + shadowing track with pauses, one sound focus
3. **Build it** — substitution tables and a fast question drill (automaticity)
4. **Remember it** — Uzbek → English recall, repeated today / tomorrow / in a week (retrieval + spacing)
5. **Talk together** — information-gap task (Student A / Student B) and a "find things in common" interview
6. **Fluency: 3 rounds** — the same talk to 3 partners in 2:00 / 1:30 / 1:00 (Nation's 4-3-2 technique), listener's card
7. **Record & check** — voice note, self-check, mistakes log, confidence rating, 1-minute challenge before/after, speaking-passport stamp

## Files

- `data/config.json` — book settings, including `audio_base_url` (where the MP3s will be hosted; the QR codes point there)
- `data/units/NN-*.json` — unit content
- `scripts/make_audio.py [unit]` — creates `dist/audio/uNN-1-phrases|2-dialogue|3-shadowing|4-model.mp3` with OpenAI TTS (clips cached in `audio-cache/`, ~$0.03 per unit)
- `scripts/build.py` → `dist/speak-up.html`; `scripts/render.js` → `dist/Impulse_Speak_Up_A2.pdf`

## Rebuild

```bash
python3 scripts/make_audio.py && python3 scripts/build.py && node scripts/render.js
```
