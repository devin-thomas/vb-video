#!/usr/bin/env python3
"""XTRA-12 editorial frame: reversible framing of the untouched Microsoft figure.

Reads source/original.gif (never modified), scales it by an integer factor with
nearest-neighbour sampling (uniform in x and y, so no stretching and no invented
pixels), and centres it on an opaque 1920x1080 desktop-teal ground. No crop, no
text, no retouching. Also writes a 1280x720 downscale used only as a QA proof.

Run from the repository root:
    python assets/historical/XTRA-12/src/frame.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "source" / "original.gif"
OUT = BASE / "exports" / "editorial-frame.png"
PROOF = BASE / "qa" / "editorial-frame-720p.png"

CANVAS = (1920, 1080)
GROUND = (0x00, 0x80, 0x80)  # Production bible desktop teal #008080
SAFE = (120, 72, 1800, 1008)  # Production bible safe area x0, y0, x1, y1


def main() -> None:
    original = Image.open(SRC)
    original.seek(0)
    rgb = original.convert("RGB")
    w, h = rgb.size
    safe_w, safe_h = SAFE[2] - SAFE[0], SAFE[3] - SAFE[1]
    scale = max(1, min(safe_w // w, safe_h // h))  # largest integer factor inside the safe area
    scaled = rgb.resize((w * scale, h * scale), Image.Resampling.NEAREST)
    canvas = Image.new("RGB", CANVAS, GROUND)
    x = (CANVAS[0] - scaled.width) // 2
    y = (CANVAS[1] - scaled.height) // 2
    canvas.paste(scaled, (x, y))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT, format="PNG", optimize=False)
    PROOF.parent.mkdir(parents=True, exist_ok=True)
    canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(PROOF, format="PNG", optimize=False)
    print(f"original {w}x{h}; scale {scale}x -> {scaled.width}x{scaled.height} at ({x},{y}); wrote {OUT.name}, {PROOF.name}")


if __name__ == "__main__":
    main()
