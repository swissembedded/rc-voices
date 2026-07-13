#!/usr/bin/env bash
# Render a text list in EVERY Kokoro voice, one folder per voice, so a
# user can pick their voice. Output: <outdir>/<voice>/<file>.wav
#
# Usage: scripts/render_all_voices.sh lists/messages.json work/messages [--speed 1.0]
set -e
cd "$(dirname "$0")/.."
LIST="$1"; OUT="$2"; shift 2 || true

FEMALE="af_heart af_bella af_nicole af_sarah af_sky af_kore af_aoede af_alloy"
MALE="am_adam am_michael am_echo am_eric am_liam am_onyx am_fenrir am_puck"

for v in $FEMALE $MALE; do
  echo "=== $v ==="
  venv/Scripts/python tools/synthesize.py "$LIST" "$OUT/$v" --voice "$v" "$@" \
    2>&1 | grep -E "^\[|done ->" | tail -1 || echo "  $v failed"
done
echo "ALL VOICES DONE -> $OUT/<voice>/"
