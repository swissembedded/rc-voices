"""Convert raw synthesis output into radio-ready pack files.

- resample 24 kHz XTTS output -> 16 kHz mono 16-bit PCM (the pack's format)
- trim leading/trailing silence (radio announcements must fire instantly)
- loudness-match against the reference pack's median RMS
- restore the SOUNDS/en/<PATH>/ layout from the __-flattened names

Usage:
  python tools/postprocess.py work/raw out/SOUNDS/en C:/tmp/pack_ref/SOUNDS/en
"""
import audioop
import glob
import os
import sys
import wave

RAW, DST, ORIG = sys.argv[1], sys.argv[2], sys.argv[3]
RATE = 16000
SIL = 300            # silence threshold (16-bit RMS) for trim
KEEP_MS = 60         # keep a little air around the speech


def read(p):
    w = wave.open(p)
    d = w.readframes(w.getnframes())
    r = w.getframerate()
    ch = w.getnchannels()
    w.close()
    if ch == 2:
        d = audioop.tomono(d, 2, 0.5, 0.5)
    return d, r


def rms(d):
    return audioop.rms(d, 2) if d else 0


# target loudness = median RMS of the original pack
orig_rms = sorted(rms(read(p)[0]) for p in glob.glob(f"{ORIG}/*.wav")[:200])
target = orig_rms[len(orig_rms) // 2]
print(f"target RMS {target} (original pack median)")

for p in sorted(glob.glob(os.path.join(RAW, "*.wav"))):
    d, r = read(p)
    if r != RATE:
        d, _ = audioop.ratecv(d, 2, 1, r, RATE, None)
    # trim silence
    n = len(d) // 2
    step = RATE // 100                       # 10 ms windows
    lo, hi = 0, n
    while lo < n and rms(d[lo * 2:(lo + step) * 2]) < SIL:
        lo += step
    while hi > lo and rms(d[(hi - step) * 2:hi * 2]) < SIL:
        hi -= step
    pad = int(RATE * KEEP_MS / 1000)
    lo, hi = max(0, lo - pad), min(n, hi + pad)
    d = d[lo * 2:hi * 2]
    # loudness match
    cur = rms(d)
    if cur:
        d = audioop.mul(d, 2, min(4.0, target / cur))
    rel = os.path.basename(p).replace("__", "/")
    out = os.path.join(DST, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    w = wave.open(out, "w")
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(RATE)
    w.writeframes(d)
    w.close()
    print(f"{rel}: {len(d)/2/RATE:.2f}s")
print("done ->", DST)
