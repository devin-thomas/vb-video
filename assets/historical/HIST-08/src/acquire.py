#!/usr/bin/env python3
"""HIST-08 acquisition: decode one uncropped frame from the Internet Archive native MPEG-2 original.

The native file (CC1301_windows_95.mpeg, 1,991,469,060 bytes) is not downloaded in full.
ffmpeg reads it over HTTP byte ranges, seeks to SEEK seconds, and writes the first decoded
frame at its stored 720x480 raster (sample aspect ratio 8:9, i.e. 4:3 display). No crop,
scale, deinterlace, or colour change is applied.

Usage (from the repository root):
    python assets/historical/HIST-08/src/acquire.py            # writes source/original.png
    python assets/historical/HIST-08/src/acquire.py --records  # also re-fetches IA meta/files XML into a scratch dir
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import urllib.request
from pathlib import Path

ASSET = Path(__file__).resolve().parents[1]
ITEM = "CC1301_windows_95"
NATIVE_URL = f"https://archive.org/download/{ITEM}/{ITEM}.mpeg"
SEEK = "419"  # seconds into the native MPEG-2 file (00:06:59)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(ASSET / "source" / "original.png"))
    parser.add_argument("--records", metavar="DIR", help="Re-fetch IA meta.xml/files.xml into DIR (never overwrites evidence/).")
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-y", "-ss", SEEK, "-i", NATIVE_URL,
           "-frames:v", "1", "-vf", "showinfo", "-bitexact", str(out)]
    print("RUN", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return result.returncode
    for line in result.stderr.splitlines():
        if "Parsed_showinfo" in line and " n:   0 " in line:
            print("FRAME", line.split("] ", 1)[1])
    print("SHA256", hashlib.sha256(out.read_bytes()).hexdigest(), out)

    if args.records:
        dest = Path(args.records)
        dest.mkdir(parents=True, exist_ok=True)
        for name in (f"{ITEM}_meta.xml", f"{ITEM}_files.xml"):
            urllib.request.urlretrieve(f"https://archive.org/download/{ITEM}/{name}", dest / name)
            print("RECORD", dest / name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
