# rc-voices

Neural **voice packs for EdgeTX** radios, generated locally and free with
[Kokoro-82M](https://github.com/hexgrad/kokoro). One consistent voice
speaks the whole pack, in the exact `SOUNDS/en` filenames EdgeTX plays -
system sounds, function callouts, and flight-controller telemetry.

- 766 announcements per pack: the complete EdgeTX English set + INAV,
  Betaflight and Yaapu telemetry callouts.
- 18 voices to choose from (female, male, blends).
- Apache-2.0, English, offline. No cloud, no API key, nobody's voice
  cloned.

Hear a sample (default voice, the startup greeting): [`samples/af_nicole-start1-startup.wav`](samples/af_nicole-start1-startup.wav)

## Quick start

1. Grab the ZIP for a voice from [Releases](../../releases) (start with
   `af_nicole`).
2. Extract `SOUNDS/` to the root of your radio's SD card, so you have
   `SOUNDS/en/…`.
3. On the radio: **Radio Setup -> Voice -> Language: en**.

Full install notes (startup greeting, shutdown line, assigning the new
INAV modes) are in [docs/INSTALL.md](docs/INSTALL.md).

## Voices

All at a slightly deliberate pace (speed 0.9). Lower pitch = warmer.
**af_nicole** is the recommended default.

| Female | ~F0 | Male | ~F0 |
| --- | --- | --- | --- |
| af_alloy | 156 Hz | am_onyx | 96 Hz |
| **af_nicole** | 161 Hz | am_echo | 117 Hz |
| af_sky | 180 Hz | am_liam | 125 Hz |
| af_kore | 185 Hz | am_adam | 126 Hz |
| af_aoede | 194 Hz | am_michael | 129 Hz |
| af_bella | 204 Hz | am_puck | 133 Hz |
| af_sarah | 205 Hz | am_fenrir | 153 Hz |
| af_heart | 217 Hz | am_eric | 188 Hz |

Plus two blends: `blend_bn` (bella + nicole) and `blend_bs` (bella + sky).

## What's in a pack

- **EdgeTX system + functions** - numbers, units, and every callout
  (gear up/down, flaps, spoiler, snapflap, timers, ...). Verified
  identical to the current EdgeTX en-US definition.
- **Flight controllers** - INAV, Betaflight and Yaapu telemetry callouts.
- **New INAV aerobatic modes** - inverted flight, knife edge L/R, prop
  hang, flat spin, 3D lock, altitude floor, figure roll/loop/4-point/
  sequence (from the quaternion orientation-hold work).
- **A cheeky startup greeting** - `SYSTEM/hello.wav` says "try not to
  break your little toy today"; alternate start/stop lines are included.

## Build it yourself

Everything is reproducible. Python 3.10-3.12, an NVIDIA GPU recommended
(fast on an 8 GB card, works on CPU).

```
scripts/setup.sh                 # venv + Kokoro (installs CUDA torch)
venv/Scripts/python tools/build_list.py    # -> lists/synth.json (766)
scripts/build_pack.sh            # all 18 voices -> out/<voice>/SOUNDS/en
venv/Scripts/python tools/package.py       # -> release/*.zip + SHA256SUMS
```

Pick or tune a single voice directly:

```
venv/Scripts/python tools/synthesize.py lists/synth.json work/raw \
  --voice af_nicole --speed 0.9
venv/Scripts/python tools/postprocess.py work/raw out/af_nicole/SOUNDS/en
```

`--voice` also takes a weighted blend, e.g. `"af_bella:0.6,af_nicole:0.4"`.

## Scope & limits

- **EdgeTX, English only.** OpenTX shares EdgeTX's sound system, so it is
  covered by the same pack.
- Kokoro has **no German** model (nor Korean/Polish/Czech/Danish), so
  those languages are not possible with this engine. Spanish, French,
  Italian, Portuguese and Japanese would be feasible from the matching
  EdgeTX text lists.

## Text sources & filenames

The text lists live in `lists/`:
- `edgetx_full.json` - the complete EdgeTX en set, exact `Path/Filename`,
  parsed from the upstream CSVs (also kept in `lists/`).
- `inav_new_modes.json` - the new INAV aerobatic callouts.
- `messages.json` - the humorous start/stop lines.

The filenames matter: the radio only plays a sound if the file is named
and placed exactly as the firmware expects. These lists carry the
authoritative names, so the pack drops straight in.

## License & credits

Apache-2.0 (see `LICENSE`, `NOTICE`). Voice model:
[Kokoro-82M](https://github.com/hexgrad/kokoro) (Apache-2.0). Sound
definitions and filenames from
[EdgeTX](https://github.com/EdgeTX/edgetx-sdcard-sounds). We synthesize a
generic voice - no real person is cloned; see [NOTES.md](NOTES.md).
