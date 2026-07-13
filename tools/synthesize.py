"""Synthesize the announcements with Kokoro-82M.

Kokoro is Apache-2.0 (commercial OK), tiny (82M), fast, and built for
clean narration - the best fit for short RC callouts and a distributable
pack. Fixed voice set (no cloning), which is exactly what we want: one
consistent generic voice over the whole pack.

Usage:
  python tools/synthesize.py lists/synth.json work/raw_kokoro [--voice VOICE] [--speed 0.9] [--limit 3]
  python tools/synthesize.py --list-voices

--voice takes a single Kokoro voice (e.g. af_bella) OR a weighted blend
"af_bella:0.6,af_nicole:0.4" (weights optional, default equal). A lower,
warmer voice + a slightly slower speed reads as more confident.

Needs: pip install kokoro soundfile   (CUDA torch for GPU)
Voice codes: a=American, af_*/am_* = US female/male (e.g. af_heart,
af_bella, af_nicole). See lists/voice_target.md.
"""
import json
import os
import sys

import numpy as np
import soundfile as sf
import torch
from kokoro import KPipeline

VOICE = sys.argv[sys.argv.index("--voice") + 1] if "--voice" in sys.argv else "af_nicole"
SPEED = float(sys.argv[sys.argv.index("--speed") + 1]) if "--speed" in sys.argv else 1.0
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
SR = 24000

pipe = KPipeline(lang_code="a", device=DEVICE)   # American English

if "--list-voices" in sys.argv:
    print("US female: af_heart af_bella af_nicole af_sarah af_sky af_alloy af_aoede af_kore")
    print("US male:   am_adam am_michael am_echo am_eric am_liam am_onyx")
    print("blend example: --voice \"af_bella:0.6,af_nicole:0.4\"")
    sys.exit(0)


def resolve_voice(spec):
    """A single name, or a weighted blend of Kokoro voice tensors."""
    if ":" not in spec and "," not in spec:
        return spec
    total, blend = 0.0, None
    for part in spec.split(","):
        name, _, w = part.partition(":")
        w = float(w) if w else 1.0
        t = pipe.load_single_voice(name.strip())
        blend = t * w if blend is None else blend + t * w
        total += w
    return blend / total


VOICE_RESOLVED = resolve_voice(VOICE)

SRC_JSON, OUT_DIR = sys.argv[1], sys.argv[2]
LIMIT = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
os.makedirs(OUT_DIR, exist_ok=True)

items = sorted(json.load(open(SRC_JSON, encoding="utf-8")).items())
if LIMIT:
    items = items[:LIMIT]

print(f"Kokoro on {DEVICE}, voice '{VOICE}', speed {SPEED}, {len(items)} phrases")
for i, (relpath, text) in enumerate(items):
    out = os.path.join(OUT_DIR, relpath.strip("/").replace("/", "__"))
    if os.path.exists(out):
        continue
    print(f"[{i+1}/{len(items)}] {relpath}: '{text}'")
    audio = None
    for _, _, chunk in pipe(text, voice=VOICE_RESOLVED, speed=SPEED):
        audio = chunk if audio is None else np.concatenate([audio, chunk])
    sf.write(out, audio, SR)
print("done ->", OUT_DIR, f"({SR} Hz, postprocess to 16 kHz next)")
