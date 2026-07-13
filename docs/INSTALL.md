# Installing a pack on the radio

The build produces one ready-to-use pack per voice under
`out/<voice>/SOUNDS/en/`, with the exact filenames EdgeTX expects.

## Copy to the SD card

1. Pick a voice, e.g. `af_nicole` (the default) - browse `out/<voice>/`
   and listen first.
2. Copy the `SOUNDS/en` folder to your radio's SD card under `SOUNDS/`,
   so the card has `SOUNDS/en/…`.
3. On the radio, select language **en** (Radio Setup -> Voice).

Files land in the folders the firmware plays from:
`SYSTEM/` (numbers, units, the startup greeting), the root (function
callouts: gear, flaps, spoiler, timers…), and `INAV/` `BETAFLIGHT/`
`YAAPU/` for the flight-controller / telemetry callouts.

## Startup greeting

EdgeTX plays `SYSTEM/hello.wav` on power-on. The build sets it to the
humorous line ("try not to break your little toy today"). To use a
different one, copy any `start1..4.wav` over `SYSTEM/hello.wav`.

## Shutdown line (optional)

EdgeTX has no built-in power-off sound. To play one of the `stop1..4.wav`
lines when you switch off, add a Special Function on the radio:

- Trigger: a switch or the shutdown confirm
- Action: Play Track -> `stop2` ("it's not a crash, it's a kit again")

Or drive it from a model Lua script on the shutdown event.

## New INAV aerobatic callouts

`INAV/invrtd.wav`, `knifel/knifer.wav`, `prpang.wav`, `fltspn.wav`,
`3dlock.wav`, `altflr.wav`, `figrol/figlop/fig4pt/figseq.wav` are the
orientation-hold modes. Assign them to a logical switch -> Play Track in
your INAV model so the radio announces the mode as you select it.
