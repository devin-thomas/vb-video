#!/usr/bin/env python3
"""XTRA-18: frame the archived Windows for Workgroups 3.11 Hearts capture on a 1920x1080 editorial canvas.

Reversible framing only: the source GIF is read, never written. The whole 640x480 capture is kept
(no crop), enlarged by an exact integer factor with nearest-neighbour sampling (every source pixel
becomes a 2x2 block), and centred on a flat ground. No text, credit, or annotation is burned in.

Run from the repository root:
    python assets/historical/XTRA-18/src/render_editorial_frame.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / "source" / "original.gif"
EXPORT = BASE / "exports" / "editorial-frame.png"
PROOF = BASE / "proofs" / "editorial-frame-720.png"
FRAMING = BASE / "evidence" / "framing.json"

CANVAS = (1920, 1080)
GROUND = (0x11, 0x13, 0x18)  # production-bible dark background token #111318
EXPECTED_SOURCE_SHA256 = "43aed772b74691983af34bb3c5d1288e8432a5474fe7a057502ff51f948890c5"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if sha256(SOURCE) != EXPECTED_SOURCE_SHA256:
        raise SystemExit("source/original.gif does not match the acquired file; refusing to render.")
    with Image.open(SOURCE) as im:
        src = im.convert("RGB")
    w, h = src.size
    # Largest integer factor that fits the canvas (640x480 -> 2).
    scale = min(CANVAS[0] // w, CANVAS[1] // h)
    if scale < 1:
        raise SystemExit("Source larger than canvas; integer framing impossible.")
    big = src.resize((w * scale, h * scale), Image.Resampling.NEAREST)
    left = (CANVAS[0] - big.width) // 2
    top = (CANVAS[1] - big.height) // 2
    canvas = Image.new("RGB", CANVAS, GROUND)
    canvas.paste(big, (left, top))

    # Pixel-exact check: every placed pixel equals its source pixel.
    px, spx = canvas.load(), src.load()
    for y in range(big.height):
        for x in range(big.width):
            if px[left + x, top + y] != spx[x // scale, y // scale]:
                raise SystemExit(f"Nearest-neighbour check failed at {(x, y)}")

    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    PROOF.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(EXPORT, optimize=True)
    # 720p viewing proof: uniform 16:9 -> 16:9 reduction of the finished frame (review aid only).
    canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(PROOF, optimize=True)

    record = {
        "source": "source/original.gif",
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "source_size": [w, h],
        "crop": None,
        "scale_factor": scale,
        "resample": "nearest-neighbour (PIL Image.Resampling.NEAREST), integer factor",
        "placed_size": [big.width, big.height],
        "placement_top_left": [left, top],
        "canvas": list(CANVAS),
        "ground_rgb_hex": "#111318",
        "aspect_ratio_preserved": True,
        "pixel_exact_check": "passed",
        "burned_in_text": None,
        "export": "exports/editorial-frame.png",
        "proof_720": "proofs/editorial-frame-720.png",
        "proof_720_resample": "LANCZOS 1920x1080 -> 1280x720 (uniform, review proof only)",
        "safe_area_note": "Placed image spans x=320..1599, y=60..1019. The capture's status-bar text (source rows 461..473) "
        "lands at y=982..1007, inside the bible's y<=1008 essential-text line; the window frame itself extends into the "
        "margin. 2x is the only integer scale that fits 1080 lines.",
    }
    FRAMING.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"export": sha256(EXPORT), "proof": sha256(PROOF), "scale": scale, "top_left": [left, top]}))


if __name__ == "__main__":
    main()
