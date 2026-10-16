"""Generate the audio tracks for every unit with the OpenAI text-to-speech API.

Tracks per unit (dist/audio/uNN-*.mp3):
  1-words   topic vocabulary, each word followed by a pause to repeat
  2-story   the story
  3-speech  the model speech

Every clip is cached in audio-cache/ (keyed by voice + text), so re-running only
pays for new or changed sentences. Requests go to api.openai.com through the
environment's proxy, which adds the API key.

Usage: python3 make_audio.py [unit-number ...]
"""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "data" / "config.json").read_text(encoding="utf-8"))
CACHE = ROOT / "audio-cache"
OUT = ROOT / "dist" / "audio"
RATE = "24000"


def speak(text, voice, speed=1.0):
    """Return a cached WAV clip of `text` read by `voice`."""
    key = hashlib.sha1(f"{CFG['tts_model']}|{voice}|{speed}|{text}".encode()).hexdigest()[:16]
    wav = CACHE / f"{key}.wav"
    if wav.exists():
        return wav
    CACHE.mkdir(exist_ok=True)
    mp3 = CACHE / f"{key}.mp3"
    body = json.dumps({"model": CFG["tts_model"], "voice": voice, "input": text, "speed": speed})
    code = subprocess.run(["curl", "-sS", "-o", str(mp3), "-w", "%{http_code}", "https://api.openai.com/v1/audio/speech",
                           "-H", "Content-Type: application/json", "--data-binary", body],
                          capture_output=True, text=True, check=True).stdout
    if code != "200":
        raise SystemExit(f"TTS failed ({code}) for: {text}\n{mp3.read_text(errors='ignore')[:300]}")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(mp3), "-ar", RATE, "-ac", "1", str(wav)], check=True)
    mp3.unlink()
    return wav


def duration(wav):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)],
                         capture_output=True, text=True, check=True).stdout
    return float(out)


def silence(seconds):
    wav = CACHE / f"silence-{seconds:.2f}.wav"
    if not wav.exists():
        CACHE.mkdir(exist_ok=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r={RATE}:cl=mono",
                        "-t", f"{seconds:.2f}", str(wav)], check=True)
    return wav


def join(parts, name):
    """Concatenate WAV parts into one MP3 track."""
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        for p in parts:
            f.write(f"file '{p}'\n")
        listfile = f.name
    out = OUT / name
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
                    "-c:a", "libmp3lame", "-b:a", "96k", str(out)], check=True)
    print(f"  {out.name}  {duration(out):.0f}s")


def spoken(text):
    """Text as it should be read aloud (no ellipses or slashes)."""
    text = text.replace("…", "").replace(" / ", " or ")
    return re.sub(r"\s+", " ", text).strip()


def plain(text):
    return spoken(text.replace("**", "").replace(" | ", " "))


def build_unit(u):
    n = f"u{u['n']:02d}"
    narrator, talker = CFG["narrator_voice"], CFG["model_talk_voice"]
    print(f"Unit {u['n']}: {u['title']}")
    # 1 topic vocabulary: each word, then a pause to repeat it
    parts = [speak(f"Unit {u['n']}. {u['title']}. Topic vocabulary. Listen and repeat.", narrator), silence(1.2)]
    for g in u["words"]:
        for en, _ in g["items"]:
            clip = speak(spoken(en), narrator)
            parts += [clip, silence(1.8)]
    join(parts, f"{n}-1-words.mp3")
    # 2 story
    s = u["story"]
    join([speak(f"{s['title']}.", narrator), silence(0.8), speak(plain(s["text"]), talker)], f"{n}-2-story.mp3")
    # 3 model speech
    join([speak("Model speech.", narrator), silence(0.6), speak(plain(u["speech"]), talker)], f"{n}-3-speech.mp3")


if __name__ == "__main__":
    wanted = {int(a) for a in sys.argv[1:]}
    for f in sorted((ROOT / "data" / "units").glob("*.json")):
        unit = json.loads(f.read_text(encoding="utf-8"))
        if not wanted or unit["n"] in wanted:
            build_unit(unit)
