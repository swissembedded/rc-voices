"""Package each built voice pack into a release ZIP.

One ZIP per voice, each containing SOUNDS/en/... at the archive root, so
a user extracts it straight onto the SD card. Also writes a SHA-256
manifest.

Usage: python tools/package.py [out] [release] [version]
"""
import hashlib
import os
import sys
import zipfile

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
REL = sys.argv[2] if len(sys.argv) > 2 else "release"
VER = sys.argv[3] if len(sys.argv) > 3 else "v1.0.0"

os.makedirs(REL, exist_ok=True)
manifest = []

for voice in sorted(os.listdir(OUT)):
    src = os.path.join(OUT, voice, "SOUNDS")
    if not os.path.isdir(src):
        continue
    zpath = os.path.join(REL, f"rc-voices-en-{VER}-{voice}.zip")
    n = 0
    # deterministic: sorted entries, fixed timestamp
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(src):
            for f in sorted(files):
                full = os.path.join(root, f)
                arc = os.path.relpath(full, os.path.join(OUT, voice))
                zi = zipfile.ZipInfo(arc.replace(os.sep, "/"), (2026, 1, 1, 0, 0, 0))
                zi.compress_type = zipfile.ZIP_DEFLATED
                with open(full, "rb") as fh:
                    z.writestr(zi, fh.read())
                n += 1
    h = hashlib.sha256(open(zpath, "rb").read()).hexdigest()
    size = os.path.getsize(zpath)
    manifest.append((os.path.basename(zpath), n, size, h))
    print(f"{voice:12s} {n:4d} files  {size/1e6:5.1f} MB")

with open(os.path.join(REL, "SHA256SUMS.txt"), "w", encoding="utf-8", newline="\n") as m:
    for name, n, size, h in manifest:
        m.write(f"{h}  {name}\n")
print(f"\n{len(manifest)} packs -> {REL}/  (+ SHA256SUMS.txt)")
