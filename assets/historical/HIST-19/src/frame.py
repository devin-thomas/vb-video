#!/usr/bin/env python3
"""HIST-19 editorial framing: reversible crop + integer upscale + pillarbox. No pixels are invented.

Run from the repository root:
    python assets/historical/HIST-19/src/frame.py

Input : source/original.png  (Internet Archive item solitaire-windows-3.1, byte-identical download)
Output: exports/editorial-frame.png (1920x1080)
        qa/editorial-frame-720p.png (1280x720 downscale, review proof only)

Transform (all recorded in evidence/provenance.json):
  1. Verify the original's SHA-256 so the frame is never built from a different file.
  2. Crop to the VirtualBox guest display only: box (left, top, right, bottom) = (555, 201, 1195, 681),
     exactly 640x480 px. This removes the capturer's modern host desktop (file names, taskbar clock,
     third-party wallpaper artwork) and the VirtualBox Manager window. It keeps the whole Windows 3.1
     guest screen, including the Solitaire window, its green playfield, menu bar and score bar.
  3. Drop the alpha channel (the original's alpha is fully opaque, 255 everywhere; checked below).
  4. Scale 2x with nearest-neighbour (uniform, no stretch, no smoothing) to 1280x960.
  5. Centre on a flat 1920x1080 pillarbox (#111318). No text, labels, watermark removal or added UI.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parents[1]
ORIGINAL = BASE / "source" / "original.png"
EXPECTED_SHA256 = "07fd42480f9bc4f926724703111235cc47ddfdfe479cad1b077db16c10424c1c"
CROP_BOX = (555, 201, 1195, 681)  # left, top, right (exclusive), bottom (exclusive)
SCALE = 2
CANVAS = (1920, 1080)
BACKGROUND = (0x11, 0x13, 0x18)


def main() -> None:
    data = ORIGINAL.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 != "REPLACED_AT_FIRST_RUN" and digest != EXPECTED_SHA256:
        raise SystemExit(f"original.png hash changed: {digest}")
    src = Image.open(ORIGINAL)
    if src.size != (1920, 1080):
        raise SystemExit(f"unexpected original size {src.size}")
    if src.mode == "RGBA":
        lo, hi = src.getchannel("A").getextrema()
        if (lo, hi) != (255, 255):
            raise SystemExit(f"original has real transparency {lo}..{hi}; revisit flattening")
    guest = src.convert("RGB").crop(CROP_BOX)
    assert guest.size == (640, 480), guest.size
    scaled = guest.resize((guest.width * SCALE, guest.height * SCALE), Image.Resampling.NEAREST)
    frame = Image.new("RGB", CANVAS, BACKGROUND)
    offset = ((CANVAS[0] - scaled.width) // 2, (CANVAS[1] - scaled.height) // 2)
    frame.paste(scaled, offset)
    (BASE / "exports").mkdir(exist_ok=True)
    (BASE / "qa").mkdir(exist_ok=True)
    frame.save(BASE / "exports" / "editorial-frame.png", format="PNG", optimize=False)
    frame.resize((1280, 720), Image.Resampling.LANCZOS).save(BASE / "qa" / "editorial-frame-720p.png", format="PNG")
    print(f"original sha256 {digest}")
    print(f"crop {CROP_BOX} -> {guest.size}; scaled {scaled.size} at offset {offset} on {CANVAS}")


if __name__ == "__main__":
    main()
