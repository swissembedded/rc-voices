#!/usr/bin/env bash
# Kokoro-82M setup (default engine) with CUDA torch, + smoke test.
set -e
cd "$(dirname "$0")/.."
# find a Python 3.10-3.12 interpreter (the py launcher is not always on
# PATH under Git Bash, so also probe the standard Windows install dirs)
PY=""
for c in "py -3.12" "py -3.11" "py -3.10"          "/c/Users/$USER/AppData/Local/Programs/Python/Python312/python.exe"          "/c/Users/$USER/AppData/Local/Programs/Python/Python311/python.exe"          python3.12 python3.11 python; do
  if $c --version >/dev/null 2>&1; then PY="$c"; break; fi
done
[ -n "$PY" ] || { echo "no Python 3.10-3.12 found"; exit 1; }
echo "python: $PY"; $PY --version

$PY -m venv venv
venv/Scripts/python -m pip install -q --upgrade pip
# GPU torch first (RTX 4060 / Ada = cu124); falls back to whatever pip finds
venv/Scripts/python -m pip install -q torch --index-url https://download.pytorch.org/whl/cu124 || \
  venv/Scripts/python -m pip install -q torch
venv/Scripts/python -m pip install -q -r requirements-kokoro.txt

mkdir -p work
venv/Scripts/python - <<'PY'
import time, soundfile as sf, torch, numpy as np
from kokoro import KPipeline
dev = "cuda" if torch.cuda.is_available() else "cpu"
print("device:", dev, torch.cuda.get_device_name(0) if dev=="cuda" else "")
t0=time.time(); p=KPipeline(lang_code="a", device=dev)
a=None
for _,_,c in p("altitude hold active", voice="af_heart"):
    a = c if a is None else np.concatenate([a,c])
sf.write("work/smoke_kokoro.wav", a, 24000)
print(f"OK -> work/smoke_kokoro.wav ({len(a)/24000:.2f}s), total {time.time()-t0:.0f}s")
PY
echo "SETUP_KOKORO_DONE"
