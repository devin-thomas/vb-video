#!/usr/bin/env python3
"""XTRA-01 editorial frame: pillarbox the untouched cover scan onto a 1920x1080 canvas.

Reversible: reads source/original.jp2 read-only, never writes it. Uniform scale only
(no stretch, no crop, no retouch). Writes exports/editorial-frame.png, the 720p proof,
and evidence/framing.json with the exact geometry.

Run from the repository root:
    python assets/historical/XTRA-01/src/render_frame.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, __version__ as PIL_VERSION

HERE = Path(__file__).resolve().parents[1]
SRC = HERE / "source" / "original.jp2"
EXPORT = HERE / "exports" / "editorial-frame.png"
PROOF = HERE / "proofs" / "editorial-frame-720.png"
FRAMING = HERE / "evidence" / "framing.json"

CANVAS = (1920, 1080)
SAFE_TOP, SAFE_BOTTOM = 72, 1008  # PRODUCTION_BIBLE safe area, y=72..1008
BG = (0x11, 0x13, 0x18)  # studio.py BG token #111318


def main() -> None:
    before = hashlib.sha256(SRC.read_bytes()).hexdigest()
    with Image.open(SRC) as im:
        im.load()
        native = im.size
        cover = im.convert("RGB")
    target_h = SAFE_BOTTOM - SAFE_TOP
    scale = target_h / native[1]
    target_w = round(native[0] * scale)
    resized = cover.resize((target_w, target_h), Image.Resampling.LANCZOS)
    x = (CANVAS[0] - target_w) // 2
    y = SAFE_TOP
    frame = Image.new("RGB", CANVAS, BG)
    frame.paste(resized, (x, y))
    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    PROOF.parent.mkdir(parents=True, exist_ok=True)
    frame.save(EXPORT, optimize=True)
    frame.resize((1280, 720), Image.Resampling.LANCZOS).save(PROOF, optimize=True)
    after = hashlib.sha256(SRC.read_bytes()).hexdigest()
    assert before == after, "source/original.jp2 changed during render"
    FRAMING.write_text(json.dumps({
        "id": "XTRA-01",
        "input": "source/original.jp2",
        "input_sha256": before,
        "input_dimensions": list(native),
        "output": "exports/editorial-frame.png",
        "canvas": list(CANVAS),
        "operation": "uniform scale (Lanczos) + centered paste on solid background; no crop, no stretch, no retouch, no added text",
        "scale": round(scale, 6),
        "scaled_dimensions": [target_w, target_h],
        "placement": {"x": x, "y": y},
        "aspect_input": round(native[0] / native[1], 5),
        "aspect_scaled": round(target_w / target_h, 5),
        "background": "#111318",
        "proof_720": "proofs/editorial-frame-720.png",
        "pillow_version": PIL_VERSION,
    }, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"scale": scale, "scaled": [target_w, target_h], "x": x, "y": y}))


if __name__ == "__main__":
    main()
