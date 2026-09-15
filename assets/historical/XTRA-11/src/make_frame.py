#!/usr/bin/env python3
"""XTRA-11 editorial frame: place source/original.jpg on a 1920x1080 ground.

Reversible, documented transformation only:
  * uniform integer 2x nearest-neighbour enlargement (no stretching, no aspect change),
  * centred inside the shared safe area (x 120..1800, y 72..1008),
  * no crop, no retouching, no text or overlay added.
The original file is read, never written.

Also writes QA proofs: a 1280x720 downscale and two 1:1 crops of the 1920x1080 export.
Run from the repository root:
  python assets/historical/XTRA-11/src/make_frame.py
"""
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parents[1]
SRC = HERE / "source" / "original.jpg"
OUT = HERE / "exports" / "editorial-frame.png"
QA = HERE / "qa"

W, H = 1920, 1080
SAFE = (120, 72, 1800, 1008)  # x0, y0, x1, y1 from docs/PRODUCTION_BIBLE.md
GROUND = (0x11, 0x13, 0x18)   # dark ground token from the production bible
SCALE = 2


def main() -> None:
    original = Image.open(SRC)
    original.load()
    src = original.convert("RGB")
    w, h = src.size[0] * SCALE, src.size[1] * SCALE
    safe_w, safe_h = SAFE[2] - SAFE[0], SAFE[3] - SAFE[1]
    if w > safe_w or h > safe_h:
        raise SystemExit(f"{SCALE}x image {w}x{h} does not fit safe area {safe_w}x{safe_h}")
    big = src.resize((w, h), Image.NEAREST)
    x = SAFE[0] + (safe_w - w) // 2
    y = SAFE[1] + (safe_h - h) // 2
    frame = Image.new("RGB", (W, H), GROUND)
    frame.paste(big, (x, y))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    frame.save(OUT, format="PNG", optimize=False)

    QA.mkdir(exist_ok=True)
    frame.resize((1280, 720), Image.LANCZOS).save(QA / "editorial-frame-720p.png", format="PNG")
    frame.crop((0, 0, 960, 1080)).save(QA / "editorial-frame-1to1-left.png", format="PNG")
    frame.crop((960, 0, 1920, 1080)).save(QA / "editorial-frame-1to1-right.png", format="PNG")
    print(f"source {src.size} -> placed {w}x{h} at ({x},{y}) on {W}x{H}; wrote {OUT}")


if __name__ == "__main__":
    main()
