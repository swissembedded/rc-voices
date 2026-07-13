# rc-voices v1.0.0 - EdgeTX English voice pack

Neural voice packs for EdgeTX radios, generated locally with
[Kokoro-82M](https://github.com/hexgrad/kokoro) (Apache-2.0). One
consistent voice over the whole pack, in the exact `SOUNDS/en` filenames
EdgeTX expects.

## What's in each pack (766 announcements)

- the complete EdgeTX en-US sound set (verified identical to upstream):
  numbers, units, and every function callout (gear, flaps, spoiler,
  snapflap, timers, ...)
- flight-controller / telemetry callouts: INAV, Betaflight, Yaapu
- 11 new INAV aerobatic-mode callouts (inverted, knife edge L/R, prop
  hang, flat spin, 3D lock, altitude floor, figure roll/loop/4-point/
  sequence)
- a humorous startup greeting (SYSTEM/hello.wav) plus start/stop
  alternates

## Voices

18 to choose from - 8 female, 8 male, 2 blends. **af_nicole** is the
recommended default (warm, low, steady). All at a slightly deliberate
pace (speed 0.9).

Download the ZIP for your voice, extract `SOUNDS/` to the SD-card root,
select language **en**. See docs/INSTALL.md for the startup override and
the optional shutdown Special Function.

## Notes

- English only. Kokoro has no German model, so a German pack is not
  possible with this engine.
- Everything is reproducible: `scripts/setup.sh`, `tools/build_list.py`,
  `scripts/build_pack.sh`, `tools/package.py`.
- SHA-256 checksums in SHA256SUMS.txt.
