#!/usr/bin/env python3
"""HIST-21 editorial framing: pillarbox the untouched Commons original onto a 1920x1080 canvas.

Reversible transform only: uniform Lanczos downscale (no stretch, no crop, no retouching,
no added text or UI). The clean original in source/original.jpg is never modified.

Run from the repository root:
    python assets/historical/HIST-21/src/render_frame.py
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import PIL
from PIL import Image

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "source" / "original.jpg"
EXPORT = BASE / "exports" / "editorial-frame.png"
PROOF = BASE / "proofs" / "editorial-frame-720.png"
FRAMING = BASE / "evidence" / "framing.json"

CANVAS = (1920, 1080)
PROOF_SIZE = (1280, 720)
# Production-bible token "dark code background"; neutral so the beige case reads true.
BACKGROUND = (0x11, 0x13, 0x18)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    original = Image.open(SRC)
    original.load()
    src_w, src_h = original.size
    rgb = original.convert("RGB")

    # Fit the whole image inside the canvas, preserving aspect ratio.
    scale = min(CANVAS[0] / src_w, CANVAS[1] / src_h)
    out_w, out_h = round(src_w * scale), round(src_h * scale)
    resized = rgb.resize((out_w, out_h), Image.Resampling.LANCZOS)
    left, top = (CANVAS[0] - out_w) // 2, (CANVAS[1] - out_h) // 2

    frame = Image.new("RGB", CANVAS, BACKGROUND)
    frame.paste(resized, (left, top))
    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    frame.save(EXPORT, format="PNG", optimize=False, compress_level=9)

    PROOF.parent.mkdir(parents=True, exist_ok=True)
    frame.resize(PROOF_SIZE, Image.Resampling.LANCZOS).save(
        PROOF, format="PNG", optimize=False, compress_level=9
    )

    record = {
        "id": "HIST-21",
        "transform": "uniform downscale + centered pillarbox; no crop, no stretch, no retouch, no overlay",
        "source": {"path": "source/original.jpg", "width": src_w, "height": src_h, "sha256": sha256(SRC)},
        "crop_box_in_source": [0, 0, src_w, src_h],
        "scale": round(scale, 6),
        "scaled_size": [out_w, out_h],
        "placement_on_canvas": {"left": left, "top": top, "right": left + out_w, "bottom": top + out_h},
        "canvas": list(CANVAS),
        "background_rgb_hex": "#%02X%02X%02X" % BACKGROUND,
        "resampling": "PIL LANCZOS",
        "added_text_or_ui": [],
        "reverse_mapping": "source_xy = ((canvas_x - left) / scale, (canvas_y - top) / scale)",
        "outputs": {
            "exports/editorial-frame.png": {"size": list(CANVAS), "sha256": sha256(EXPORT)},
            "proofs/editorial-frame-720.png": {"size": list(PROOF_SIZE), "sha256": sha256(PROOF)},
        },
        "toolchain": {"python": platform.python_version(), "Pillow": PIL.__version__},
    }
    FRAMING.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
