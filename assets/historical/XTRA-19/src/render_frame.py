#!/usr/bin/env python3
"""XTRA-19 editorial frame: integer 2x nearest-neighbour scale of the untouched 640x480 capture.

Reversible: reads source/original.png read-only, never writes it. Integer scale only
(no stretch, no crop, no retouch, no smoothing). Writes exports/editorial-frame.png,
the 720p review proof, and evidence/framing.json with the exact geometry.

Run from the repository root:
    python assets/historical/XTRA-19/src/render_frame.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, __version__ as PIL_VERSION

HERE = Path(__file__).resolve().parents[1]
SRC = HERE / "source" / "original.png"
EXPORT = HERE / "exports" / "editorial-frame.png"
PROOF = HERE / "proofs" / "editorial-frame-720.png"
FRAMING = HERE / "evidence" / "framing.json"

CANVAS = (1920, 1080)
SCALE = 2  # largest integer factor whose height (960) fits the 1080 canvas
BG = (0x11, 0x13, 0x18)  # studio.py BG token #111318


def main() -> None:
    before = hashlib.sha256(SRC.read_bytes()).hexdigest()
    with Image.open(SRC) as im:
        im.load()
        native = im.size
        mode = im.mode
        capture = im.convert("RGB")  # palette -> RGB, exact colour values, no dithering
    scaled_w, scaled_h = native[0] * SCALE, native[1] * SCALE
    assert scaled_w <= CANVAS[0] and scaled_h <= CANVAS[1], "integer scale does not fit canvas"
    scaled = capture.resize((scaled_w, scaled_h), Image.Resampling.NEAREST)
    x = (CANVAS[0] - scaled_w) // 2
    y = (CANVAS[1] - scaled_h) // 2
    frame = Image.new("RGB", CANVAS, BG)
    frame.paste(scaled, (x, y))

    # Self-check: every scaled pixel block equals its source pixel; background untouched.
    src_px = capture.load()
    out_px = frame.load()
    for sy in range(native[1]):
        for sx in range(native[0]):
            p = src_px[sx, sy]
            for dy in range(SCALE):
                for dx in range(SCALE):
                    assert out_px[x + sx * SCALE + dx, y + sy * SCALE + dy] == p
    for (bx, by) in [(0, 0), (x - 1, 540), (x + scaled_w, 540), (960, y - 1), (960, y + scaled_h), (1919, 1079)]:
        assert out_px[bx, by] == BG

    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    PROOF.parent.mkdir(parents=True, exist_ok=True)
    frame.save(EXPORT, optimize=True)
    frame.resize((1280, 720), Image.Resampling.LANCZOS).save(PROOF, optimize=True)
    after = hashlib.sha256(SRC.read_bytes()).hexdigest()
    assert before == after, "source/original.png changed during render"
    FRAMING.write_text(json.dumps({
        "id": "XTRA-19",
        "input": "source/original.png",
        "input_sha256": before,
        "input_dimensions": list(native),
        "input_mode": mode,
        "output": "exports/editorial-frame.png",
        "canvas": list(CANVAS),
        "operation": "palette-to-RGB conversion (exact colours) + integer 2x nearest-neighbour scale + centered paste on solid background; no crop, no stretch, no smoothing, no retouch, no added text",
        "scale": SCALE,
        "scaled_dimensions": [scaled_w, scaled_h],
        "placement": {"x": x, "y": y},
        "aspect_input": round(native[0] / native[1], 5),
        "aspect_scaled": round(scaled_w / scaled_h, 5),
        "safe_area_note": "Image spans y=60..1020, 12 px beyond the y=72..1008 essential-text band at top and bottom. The top 6 source rows (Tut's Tomb title-bar border) and bottom 6 rows (File Manager icon area, Time/row edge) fall there; no essential text is in those rows. Chosen to keep an integer scale instead of a non-integer 1.95x.",
        "pixel_block_self_check": "passed (every 2x2 block equals its source pixel; sampled background pixels equal #111318)",
        "background": "#111318",
        "proof_720": "proofs/editorial-frame-720.png",
        "proof_720_resample": "Lanczos downscale of the export (review proof only)",
        "pillow_version": PIL_VERSION,
    }, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"scale": SCALE, "scaled": [scaled_w, scaled_h], "x": x, "y": y, "sha256": before}))


if __name__ == "__main__":
    main()
