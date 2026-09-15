#!/usr/bin/env python3
"""HIST-08 editorial framing: reversible 16:9 presentation of source/original.png.

Transformations (and nothing else):
  1. Pixel-aspect correction + uniform scale: stored 720x480 raster with 8:9 sample aspect
     ratio (4:3 display) -> 1440x1080 (x2.0 horizontally after 8:9, x2.25 vertically;
     equivalently 720x480 -> 1440x1080 Lanczos). Full frame kept; no crop.
  2. Pillarbox: centred on a 1920x1080 black canvas at x=240..1680, y=0..1080.
No text, UI, logo, watermark removal, colour grade, or retouching is added.

Also writes a 1280x720 downscale proof for 720p inspection.

Usage (from the repository root):
    python assets/historical/HIST-08/src/render_frame.py
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import PIL
from PIL import Image

ASSET = Path(__file__).resolve().parents[1]
ORIGINAL = ASSET / "source" / "original.png"
EXPORT = ASSET / "exports" / "editorial-frame.png"
PROOF_720 = ASSET / "proofs" / "editorial-frame-720.png"

CANVAS = (1920, 1080)
PICTURE = (1440, 1080)          # 4:3 display at full canvas height
OFFSET = ((CANVAS[0] - PICTURE[0]) // 2, 0)  # (240, 0)


def main() -> int:
    src = Image.open(ORIGINAL)
    if src.size != (720, 480):
        print(f"Unexpected original size {src.size}; expected 720x480 stored raster.", file=sys.stderr)
        return 1
    picture = src.convert("RGB").resize(PICTURE, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", CANVAS, (0, 0, 0))
    canvas.paste(picture, OFFSET)
    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    PROOF_720.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(EXPORT, format="PNG", optimize=False)
    canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(PROOF_720, format="PNG", optimize=False)
    print("Pillow", PIL.__version__, "Python", sys.version.split()[0])
    for path in (EXPORT, PROOF_720):
        data = path.read_bytes()
        print(path.relative_to(ASSET).as_posix(), Image.open(path).size, len(data), hashlib.sha256(data).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
