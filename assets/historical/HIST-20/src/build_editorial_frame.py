#!/usr/bin/env python3
"""HIST-20: build the reversible 16:9 editorial frame from the untouched archive original.

Run from the repository root:
    python assets/historical/HIST-20/src/build_editorial_frame.py

Transformations (all recorded in evidence/source.json):
  1. Crop the Solitaire window's outer border box from source/original.png:
     left=602, top=356, right=1199, bottom=790 (exclusive) -> 597 x 434 px.
     This removes the Windows 11 host desktop (private folder names, clock,
     third-party wallpaper), the VirtualBox chrome, and the guest wallpaper.
  2. Scale by exactly 2x with nearest-neighbour sampling (no smoothing, no
     stretching; aspect ratio preserved) -> 1194 x 868 px.
  3. Centre on a flat 1920 x 1080 #111318 background at offset (363, 106),
     inside the shared safe area x=120..1800, y=72..1008.
No pixels inside the window are edited; no text, UI, or watermark is added or removed.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parents[1]
ORIGINAL = HERE / "source" / "original.png"
ORIGINAL_SHA256 = "7bb19b94109cfd09d19fd8240411443b3f98a1e5a76a59b0734bf0652715e4e7"
CROP_BOX = (602, 356, 1199, 790)
SCALE = 2
CANVAS = (1920, 1080)
BACKGROUND = (17, 19, 24)  # production-bible token #111318
OUT = HERE / "exports" / "editorial-frame.png"
PROOF_720 = HERE / "evidence" / "proof-720p.png"


def main() -> None:
    digest = hashlib.sha256(ORIGINAL.read_bytes()).hexdigest()
    if digest != ORIGINAL_SHA256:
        raise SystemExit(f"original.png hash changed: {digest}")
    src = Image.open(ORIGINAL).convert("RGB")
    if src.size != (1920, 1080):
        raise SystemExit(f"unexpected original size {src.size}")
    window = src.crop(CROP_BOX)
    scaled = window.resize((window.width * SCALE, window.height * SCALE), Image.NEAREST)
    canvas = Image.new("RGB", CANVAS, BACKGROUND)
    offset = ((CANVAS[0] - scaled.width) // 2, (CANVAS[1] - scaled.height) // 2)
    canvas.paste(scaled, offset)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT)
    canvas.resize((1280, 720), Image.LANCZOS).save(PROOF_720)
    print(f"window {window.size} -> {scaled.size} at {offset}; wrote {OUT.name}, {PROOF_720.name}")


if __name__ == "__main__":
    main()
