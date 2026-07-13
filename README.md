# rc-voices

Generate RC transmitter voice packs (EdgeTX / OpenTX) with
[Kokoro-82M](https://github.com/hexgrad/kokoro) - a small, fast,
Apache-2.0 neural TTS. Driven by plain text lists; one consistent voice
over the whole pack, dropped into the `SOUNDS/<lang>` layout the radio
expects.

## Voice

Default is `af_nicole` (warm, low, steady - F0 ~ 161 Hz, matches
`lists/voice_target.md`). Any Kokoro voice works via `--voice`, single
or a weighted blend (`"af_bella:0.6,af_nicole:0.4"`), plus `--speed`.
US female: af_heart af_bella af_nicole af_sarah af_sky af_kore af_aoede
af_alloy. US male: am_adam am_michael am_echo am_eric am_liam am_onyx
am_fenrir am_puck. Kokoro ships the voices with the model and is
Apache-2.0, so the output is clean to redistribute - a generic voice, no
one is cloned.

## Text lists

Each entry is `filename -> spoken text`. The filenames must match exactly
what the transmitter looks for, or it stays silent.

- `lists/missing_en.json` - announcements the current EdgeTX phrase list
  expects (per SOUNDS/<lang> path).
- `lists/inav_modes.json` - INAV flight-mode callouts, including the
  modes from our quaternion orientation-hold branch.

`tools/build_list.py` merges them into `lists/synth.json`.

## Setup

Python 3.10-3.12, NVIDIA GPU recommended (Kokoro is fast on an 8 GB card,
usable on CPU). One-time:

```
scripts/setup.sh    # venv + kokoro + a 1-phrase smoke test
```

The script installs a CUDA torch wheel (cu124) for the GPU.

## Pipeline

1. `tools/build_list.py` - merge the text lists into `lists/synth.json`.
2. `tools/synthesize.py lists/synth.json work/raw [--voice af_nicole] [--speed 1.0]`
   - one wav per phrase, 24 kHz.
3. `tools/postprocess.py work/raw out/SOUNDS/en <reference-pack>/SOUNDS/en`
   - resample to 16 kHz mono 16-bit, trim silence, loudness-match, write
   the exact `SOUNDS/<lang>` filenames the radio plays.
4. Listen-check, copy to the SD card.

## Status

- [x] Kokoro engine, all voices selectable, af_nicole default
- [ ] full EdgeTX + project text collection with exact filenames
- [ ] gap check (flaps up/down, gear, trims, timers, ...)
- [ ] full batch + postprocess
- [ ] on-radio test

Generated audio stays out of git - this repo carries tooling and lists.
