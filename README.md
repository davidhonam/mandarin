# Mandarin Pinyin SRS

A pinyin-first spaced-repetition study app for the **HSK1 1000 Mandarin words**, with high-quality audio for every example sentence. Single self-contained `index.html` — no build step, no server, no accounts.

**Live:** https://davidhonam.github.io/mandarin/

## Features
- **Pinyin-first cards** — front shows the word in pinyin; flip for the English definition + two example sentences (pinyin + English).
- **Audio** — pre-generated MP3s for every sentence (Microsoft Edge neural voice *Yunyang*), played at an adjustable speed. Word audio uses the browser's built-in voice. Falls back to browser TTS if a clip is missing.
- **Spaced repetition** — Anki-style SM-2 scheduling with Again/Hard/Good/Easy, daily new-card cap, and streaks.
- **Browse / search / cram** — search all 1000 words and drill a filtered set without affecting scheduling.
- **Stats** — retention, reviews-per-day, due forecast, collection maturity, leeches.
- **Mobile-first + installable** — responsive layout and a PWA service worker, so it installs to your home screen and caches audio for offline use.
- **Progress** — auto-saved to the browser; export/import as JSON to back up or move devices.

## Project layout
```
index.html              the app (data embedded inline)
audio/                  1,986 sentence MP3s — s_<cardId>_<sentenceIndex>.mp3
cards.json              source data (also embedded in index.html)
generate_audio.py       resumable edge-tts generator (no API key)
manifest.webmanifest    PWA manifest
sw.js                   service worker (offline + audio caching)
```

## Regenerating audio
```bash
pip install edge-tts
python3 generate_audio.py     # resumable; skips existing files. Change VOICE at the top to switch voices.
```

## Running locally
Open `index.html` directly, or serve the folder (needed for the service worker / if local audio is blocked):
```bash
python3 -m http.server   # then open http://localhost:8000
```
