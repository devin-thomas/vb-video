#!/usr/bin/env python3
"""HIST-02 editorial frame: the complete WinWorld VB4 32-bit capture, uniformly resized, pillarboxed to 1920x1080.

Reversible by construction: source/original.png is never modified; the export is a pure
uniform resize (800x600 -> 1440x1080, factor 1.8, Lanczos) placed at x=240, y=0 on a flat
black canvas. No crop, no retouch, no overlay text, no added UI.
Microsoft's published screenshot terms allow resizing only and forbid using portions of a
screenshot, so the full frame is kept.

Run from the repository root:
    python assets/historical/HIST-02/src/make_editorial_frame.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parents[1]
ORIGINAL = BASE / "source" / "original.png"
EXPORT = BASE / "exports" / "editorial-frame.png"
PROOF_720 = BASE / "proofs" / "editorial-frame-720.png"

CANVAS = (1920, 1080)
PILLARBOX = (0, 0, 0)


def main() -> None:
    src = Image.open(ORIGINAL)
    if src.size != (800, 600):
        raise SystemExit(f"Unexpected original size {src.size}; expected 800x600.")
    rgb = src.convert("RGB")
    scale = CANVAS[1] / rgb.height  # 1.8, uniform on both axes
    target = (round(rgb.width * scale), CANVAS[1])  # (1440, 1080)
    if target[0] * rgb.height != target[1] * rgb.width:
        raise SystemExit("Aspect ratio would change; refusing to stretch.")
    scaled = rgb.resize(target, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", CANVAS, PILLARBOX)
    offset = ((CANVAS[0] - target[0]) // 2, 0)  # (240, 0)
    canvas.paste(scaled, offset)
    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(EXPORT, format="PNG", optimize=True)

    PROOF_720.parent.mkdir(parents=True, exist_ok=True)
    canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(PROOF_720, format="PNG", optimize=True)
    print(f"original {rgb.size} -> scaled {target} at offset {offset} on {CANVAS}")
    print(f"wrote {EXPORT.relative_to(BASE)} and {PROOF_720.relative_to(BASE)}")


if __name__ == "__main__":
    main()
