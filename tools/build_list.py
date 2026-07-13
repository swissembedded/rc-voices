"""Merge every text source into one synthesis list (path/filename -> text).

Sources:
  lists/edgetx_full.json   - the complete EdgeTX sound set, exact paths
                             (parsed from the edgetx CSVs, 747 entries)
  lists/inav_new_modes.json- NEW INAV modes from the orientation-hold
                             branch (not yet upstream)
  lists/messages.json      - our humorous start/stop callouts

Usage: python tools/build_list.py [lists/synth.json]
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "lists/synth.json"
synth = {}

synth.update(json.load(open("lists/edgetx_full.json", encoding="utf-8")))
edgetx_n = len(synth)

new = json.load(open("lists/inav_new_modes.json", encoding="utf-8"))["modes"]
synth.update(new)

msgs = json.load(open("lists/messages.json", encoding="utf-8"))
synth.update(msgs)

json.dump(synth, open(OUT, "w", encoding="utf-8"), indent=2, sort_keys=True)
print(f"{edgetx_n} EdgeTX + {len(new)} new INAV modes + {len(msgs)} messages "
      f"-> {len(synth)} total -> {OUT}")
