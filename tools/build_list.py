"""Merge the source-pack gap list and the INAV mode list into one
synthesis list (filename -> spoken text).

The INAV modes go under SOUNDS/en/ (flat), announced on mode change by a
Lua/logical-switch trigger. The gap list keeps its original PATH layout.

Usage:
  python tools/build_list.py lists/synth.json
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "lists/synth.json"

synth = {}

# 1. source-pack gaps (already PATH/file -> text)
gaps = json.load(open("lists/missing_en.json", encoding="utf-8"))
synth.update(gaps)

# 2. INAV flight modes (flat under SOUNDS/en)
modes = json.load(open("lists/inav_modes.json", encoding="utf-8"))["modes"]
ours = 0
for m in modes:
    synth[m["file"]] = m["text"]
    ours += bool(m.get("ours"))

json.dump(synth, open(OUT, "w", encoding="utf-8"), indent=2, sort_keys=True)
print(f"{len(gaps)} gap phrases + {len(modes)} INAV modes "
      f"({ours} of them new in the orientation-hold branch) -> {len(synth)} total")
print(f"-> {OUT}")
