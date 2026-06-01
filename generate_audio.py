#!/usr/bin/env python3
"""Batch-generate Mandarin sentence audio with edge-tts (no API key).
Resumable: skips files that already exist. Filenames are deterministic:
  audio/s_<cardId>_<sentenceIndex>.mp3
so the web app can derive them without a mapping file.
"""
import asyncio, json, os, sys
import edge_tts

VOICE = "zh-CN-YunyangNeural"
OUTDIR = "audio"
CONCURRENCY = 10
MAX_RETRIES = 4

os.makedirs(OUTDIR, exist_ok=True)
cards = json.load(open("cards.json", encoding="utf-8"))

# build work list: (path, text)
jobs = []
for c in cards:
    for i, ex in enumerate(c["ex"]):
        zh = (ex.get("zh") or "").strip()
        if not zh:
            continue
        path = os.path.join(OUTDIR, f"s_{c['id']}_{i}.mp3")
        if os.path.exists(path) and os.path.getsize(path) > 0:
            continue
        jobs.append((path, zh))

total = len(jobs)
print(f"{total} clips to generate (voice={VOICE}); existing skipped.", flush=True)
if total == 0:
    sys.exit(0)

done = 0
fail = []

async def one(path, text, sem, lock):
    global done
    async with sem:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                tmp = path + ".part"
                comm = edge_tts.Communicate(text, VOICE)
                await comm.save(tmp)
                if os.path.getsize(tmp) == 0:
                    raise RuntimeError("empty file")
                os.replace(tmp, path)
                break
            except Exception as e:
                if attempt == MAX_RETRIES:
                    fail.append((path, text, str(e)))
                else:
                    await asyncio.sleep(0.6 * attempt)
        async with lock:
            global done
            done += 1
            if done % 50 == 0 or done == total:
                print(f"  {done}/{total}", flush=True)

async def main():
    sem = asyncio.Semaphore(CONCURRENCY)
    lock = asyncio.Lock()
    await asyncio.gather(*(one(p, t, sem, lock) for p, t in jobs))

asyncio.run(main())
print(f"Done. generated={total-len(fail)} failed={len(fail)}", flush=True)
if fail:
    print("FAILURES (rerun to retry):", flush=True)
    for p, t, e in fail[:20]:
        print("  ", p, "->", e, flush=True)
