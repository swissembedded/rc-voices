"""Convert raw Kokoro output into radio-ready pack files.

- resample 24 kHz Kokoro output -> 16 kHz mono 16-bit PCM (pack format)
- trim leading/trailing silence (radio announcements must fire instantly)
- loudness-normalise to a target RMS (a reference pack, or a fixed value)
- restore the SOUNDS/<lang>/<PATH>/ layout from the __-flattened names

Usage:
  python tools/postprocess.py work/raw out/SOUNDS/en [reference/SOUNDS/en]
"""
import audioop
import glob
import os
import sys
import wave

RAW, DST = sys.argv[1], sys.argv[2]
ORIG = sys.argv[3] if len(sys.argv) > 3 else None
RATE = 16000
SIL = 120            # silence threshold (16-bit RMS): low, so a soft onset
                     # consonant (g/f/s, quiet on low male voices) is NOT
                     # mistaken for silence and trimmed away
KEEP_MS = 60         # keep a little air around the speech
MAX_LEAD_MS = 90     # HARD cap on leading trim: Kokoro's lead-in is short,
                     # so never remove more than this from the front - it
                     # physically cannot eat the first syllable
FIXED_TARGET = 4000  # 16-bit speech RMS when no reference pack is given


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


if ORIG:
    orig_rms = sorted(rms(read(p)[0]) for p in glob.glob(f"{ORIG}/*.wav")[:200])
    target = orig_rms[len(orig_rms) // 2] if orig_rms else FIXED_TARGET
    print(f"target RMS {target} (reference pack median)")
else:
    target = FIXED_TARGET
    print(f"target RMS {target} (fixed)")

for p in sorted(glob.glob(os.path.join(RAW, "*.wav"))):
    d, r = read(p)
    if r != RATE:
        d, _ = audioop.ratecv(d, 2, 1, r, RATE, None)
    # trim silence
    n = len(d) // 2
    step = RATE // 100                       # 10 ms windows
    lead_cap = int(RATE * MAX_LEAD_MS / 1000)
    lo, hi = 0, n
    while lo < lead_cap and rms(d[lo * 2:(lo + step) * 2]) < SIL:
        lo += step                           # capped: never past MAX_LEAD_MS
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
