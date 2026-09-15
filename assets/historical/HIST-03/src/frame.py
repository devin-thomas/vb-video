#!/usr/bin/env python3
"""HIST-03 editorial framing: resize-only, aspect-preserving fit onto a 1920x1080 plate.

Reversible by construction: the acquired original is never modified; the frame is the
whole original, uniformly scaled (no crop, no stretch, no retouch, no added UI or text),
centered inside the shared safe area (x 120..1800, y 72..1008) on a flat neutral plate.
The placement rectangle is printed so the transform can be inverted exactly.

Run from the repository root:
    python assets/historical/HIST-03/src/frame.py
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, __version__ as PIL_VERSION

HERE = Path(__file__).resolve().parents[1]
CANVAS = (1920, 1080)
SAFE = (120, 72, 1800, 1008)          # left, top, right, bottom (shared production bible)
PLATE = (17, 19, 24)                  # #111318, bible dark token; neutral pillarbox only

JOBS = [
    # (source, export, 720p proof)
    ("source/original.gif", "exports/editorial-frame.png", "proofs/editorial-frame-720.png"),
    ("candidates/wikipedia-vb6-on-xp/original.png",
     "candidates/wikipedia-vb6-on-xp/editorial-frame.png",
     "candidates/wikipedia-vb6-on-xp/editorial-frame-720.png"),
]


def frame(src: Path) -> tuple[Image.Image, dict]:
    im = Image.open(src)
    im.seek(0)
    rgb = im.convert("RGB")
    sw, sh = rgb.size
    box_w, box_h = SAFE[2] - SAFE[0], SAFE[3] - SAFE[1]
    scale = min(box_w / sw, box_h / sh)
    dw, dh = round(sw * scale), round(sh * scale)
    scaled = rgb.resize((dw, dh), Image.Resampling.LANCZOS)
    x = SAFE[0] + (box_w - dw) // 2
    y = SAFE[1] + (box_h - dh) // 2
    plate = Image.new("RGB", CANVAS, PLATE)
    plate.paste(scaled, (x, y))
    info = {"source_size": [sw, sh], "scale": round(scale, 6), "placed_size": [dw, dh],
            "placed_at": [x, y], "resample": "LANCZOS", "crop": None, "plate_rgb": list(PLATE)}
    return plate, info


def main() -> None:
    report = {"pillow": PIL_VERSION, "jobs": []}
    for src, out, proof in JOBS:
        img, info = frame(HERE / src)
        (HERE / out).parent.mkdir(parents=True, exist_ok=True)
        (HERE / proof).parent.mkdir(parents=True, exist_ok=True)
        img.save(HERE / out, format="PNG", optimize=False)
        img.resize((1280, 720), Image.Resampling.LANCZOS).save(HERE / proof, format="PNG", optimize=False)
        report["jobs"].append({"source": src, "export": out, "proof_720p": proof, **info})
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
