#!/usr/bin/env bash
# Build the full voice pack in EVERY voice: synthesize lists/synth.json
# then postprocess into out/<voice>/SOUNDS/en (the radio layout, exact
# filenames). Females + blends at speed 0.9, males at 0.9 too.
#
# Usage: scripts/build_pack.sh   (run tools/build_list.py first)
set -e
cd "$(dirname "$0")/.."
LIST=lists/synth.json
FEMALE="af_heart af_bella af_nicole af_sarah af_sky af_kore af_aoede af_alloy"
MALE="am_adam am_michael am_echo am_eric am_liam am_onyx am_fenrir am_puck"

one() {  # voice-spec folder
  echo "=== $2 ==="
  venv/Scripts/python tools/synthesize.py "$LIST" "work/raw/$2" --voice "$1" --speed 0.9 >/dev/null 2>&1
  venv/Scripts/python tools/postprocess.py "work/raw/$2" "out/$2/SOUNDS/en" >/dev/null 2>&1
  echo "  $2: $(find "out/$2" -name '*.wav' | wc -l) wav"
}
for v in $FEMALE; do one "$v" "$v"; done
one "af_bella:0.6,af_nicole:0.4" blend_bn
one "af_bella:0.5,af_sky:0.5"    blend_bs
for v in $MALE;   do one "$v" "$v"; done
echo "PACK DONE -> out/<voice>/SOUNDS/en ($(find out -name '*.wav' | wc -l) files, $(ls out | wc -l) voices)"
