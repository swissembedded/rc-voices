#!/usr/bin/env bash
# Render a text list in EVERY voice, one folder per voice, so a user can
# pick theirs. Output: <outdir>/<voice>/<file>.wav
#
# Female voices get speed 0.9 (warmer, more deliberate - the audition
# favourite) plus two blends; male voices stay at 1.0. Generation is fast
# on GPU, so we keep them all.
#
# Usage: scripts/render_all_voices.sh lists/messages.json work/messages
set -e
cd "$(dirname "$0")/.."
LIST="$1"; OUT="$2"

FEMALE="af_heart af_bella af_nicole af_sarah af_sky af_kore af_aoede af_alloy"
MALE="am_adam am_michael am_echo am_eric am_liam am_onyx am_fenrir am_puck"

gen() {  # voice-spec  folder  speed
  echo "=== $2 (speed $3) ==="
  venv/Scripts/python tools/synthesize.py "$LIST" "$OUT/$2" --voice "$1" --speed "$3" \
    2>&1 | grep -E "done ->" | tail -1 || echo "  $2 failed"
}

for v in $FEMALE; do gen "$v" "$v" 0.9; done
gen "af_bella:0.6,af_nicole:0.4" "blend_bn" 0.9
gen "af_bella:0.5,af_sky:0.5"    "blend_bs" 0.9
for v in $MALE;   do gen "$v" "$v" 0.9; done

echo "ALL VOICES DONE -> $OUT/<voice>/ ($(find "$OUT" -name '*.wav' | wc -l) files)"
