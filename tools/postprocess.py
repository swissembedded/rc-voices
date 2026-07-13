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
                     # or a quiet word-final decay is NOT read as silence
MAX_LEAD_MS = 90     # cap on how much may be trimmed from the FRONT ...
MAX_TAIL_MS = 150    # ... and from the END, so neither can eat a syllable
BACK_MS = 30         # back off the detected onset/offset a hair so the
                     # attack and the release stay fully inside
LEAD_MS = 40         # fixed clean pause prepended to every clip
TAIL_MS = 90         # fixed clean pause appended to every clip
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
    # find the speech bounds, but cap how far each edge may move so a soft
    # onset or a quiet word-final decay can never be trimmed off
    n = len(d) // 2
    step = RATE // 100                       # 10 ms windows
    lead_cap = int(RATE * MAX_LEAD_MS / 1000)
    tail_cap = int(RATE * MAX_TAIL_MS / 1000)
    lo, hi = 0, n
    while lo < lead_cap and rms(d[lo * 2:(lo + step) * 2]) < SIL:
        lo += step
    while (n - hi) < tail_cap and hi > lo and rms(d[(hi - step) * 2:hi * 2]) < SIL:
        hi -= step
    back = int(RATE * BACK_MS / 1000)
    lo, hi = max(0, lo - back), min(n, hi + back)
    core = d[lo * 2:hi * 2]
    # normalise both ends to a fixed clean pause, then this is the clip
    d = (b"\x00\x00" * int(RATE * LEAD_MS / 1000)) + core + \
        (b"\x00\x00" * int(RATE * TAIL_MS / 1000))
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
