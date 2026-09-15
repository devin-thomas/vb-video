#!/usr/bin/env python3
"""HIST-13 editorial framing: reversible crop + uniform scale of source/original.jpg.

No pixels are redrawn, retouched, recoloured or invented. Two regions of the same
scanned book page are cropped, scaled by one shared factor (no stretching) and
placed side by side on a plain neutral background. Every parameter below is
written to evidence/transform.json so the frame can be reversed or rebuilt.

Run from the repository root:
    python assets/historical/HIST-13/src/build_frame.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parents[1]
ORIGINAL = BASE / "source" / "original.jpg"
FRAME = BASE / "exports" / "editorial-frame.png"
PROOF_720 = BASE / "proofs" / "editorial-frame-720.png"
TRANSFORM = BASE / "evidence" / "transform.json"

CANVAS = (1920, 1080)
BACKGROUND = (42, 42, 42)  # neutral dark grey, authored framing colour
SCALE = 0.87               # single shared scale factor for both panels
GAP = 64                   # px between panels on the canvas

# Crop boxes in original-pixel coordinates (left, top, right, bottom), right/bottom exclusive.
# Measured from the window borders (dark-pixel projections) plus 10 px padding.
PANELS = [
    {
        "name": "fig-2.40-output-and-editor",
        "depicts": "Program output window 'New Window' and CodeWarrior editor window 'OOPexample.cp' (book Figure 2.40)",
        "crop": [457, 411, 1525, 1452],
    },
    {
        "name": "fig-2.41-project-window",
        "depicts": "CodeWarrior project window 'OOPexamplePPC.µ' (book Figure 2.41)",
        "crop": [567, 1608, 1404, 2005],
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    src = Image.open(ORIGINAL)
    src.load()
    canvas = Image.new("RGB", CANVAS, BACKGROUND)

    scaled = []
    for panel in PANELS:
        l, t, r, b = panel["crop"]
        region = src.crop((l, t, r, b)).convert("RGB")
        size = (round(region.width * SCALE), round(region.height * SCALE))
        scaled.append((panel, region.size, region.resize(size, Image.Resampling.LANCZOS)))

    total_w = sum(img.width for _, _, img in scaled) + GAP * (len(scaled) - 1)
    x = (CANVAS[0] - total_w) // 2
    placements = []
    for panel, crop_size, img in scaled:
        y = (CANVAS[1] - img.height) // 2
        canvas.paste(img, (x, y))
        placements.append({
            **panel,
            "crop_size": list(crop_size),
            "scaled_size": [img.width, img.height],
            "canvas_position": [x, y],
            "effective_scale_x": img.width / crop_size[0],
            "effective_scale_y": img.height / crop_size[1],
        })
        x += img.width + GAP

    FRAME.parent.mkdir(parents=True, exist_ok=True)
    PROOF_720.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(FRAME, format="PNG", optimize=True)
    canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(PROOF_720, format="PNG", optimize=True)

    TRANSFORM.write_text(json.dumps({
        "input": {"path": "source/original.jpg", "sha256": sha256(ORIGINAL),
                  "size": list(src.size), "mode": src.mode},
        "operations": [
            "crop each panel box from the original (no rotation, deskew, levels, sharpening or retouching)",
            "convert greyscale L to RGB without tonal change",
            f"resize each crop by the single shared factor {SCALE} with Lanczos resampling (aspect ratio preserved)",
            "paste panels side by side, vertically centred, on a plain neutral background",
        ],
        "canvas": {"size": list(CANVAS), "background_rgb": list(BACKGROUND), "gap_px": GAP},
        "shared_scale": SCALE,
        "panels": placements,
        "arrangement_note": ("In the book the two figures are stacked vertically on page 43 with captions; "
                             "the frame places them side by side and omits captions/body text. "
                             "No text, labels, UI or watermarks were added or removed."),
        "outputs": {
            "exports/editorial-frame.png": sha256(FRAME),
            "proofs/editorial-frame-720.png": sha256(PROOF_720),
        },
        "reproduce": "python assets/historical/HIST-13/src/build_frame.py",
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"frame": str(FRAME), "proof_720": str(PROOF_720),
                      "panels": [(p["name"], p["scaled_size"], p["canvas_position"]) for p in placements]}))


if __name__ == "__main__":
    main()
