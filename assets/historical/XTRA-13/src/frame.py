#!/usr/bin/env python3
"""XTRA-13 editorial framing: reversible, unstretched placement of source/original.gif.

Reads source/original.gif (never modified), scales it by the largest whole-number
factor that fits the shared safe area (x 120..1800, y 72..1008) using
nearest-neighbour resampling (no aspect change, no interpolation of the screenshot
pixels), and centres it on an opaque 1920x1080 dark ground. No text, credit, or
annotation is burned in. Also writes a 1280x720 review proof and a framing record.

Run from the repository root:
    python assets/historical/XTRA-13/src/frame.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, __version__ as PIL_VERSION

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "source" / "original.gif"
EXPORT = BASE / "exports" / "editorial-frame.png"
PROOF = BASE / "proofs" / "editorial-frame-720.png"
RECORD = BASE / "evidence" / "framing.json"

W, H = 1920, 1080
SAFE = (120, 72, 1800, 1008)  # production bible safe area
GROUND = (0x11, 0x13, 0x18)    # production bible dark background token #111318


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    before = sha256(SRC)
    src = Image.open(SRC)
    sw, sh = src.size
    safe_w, safe_h = SAFE[2] - SAFE[0], SAFE[3] - SAFE[1]
    scale = min(safe_w // sw, safe_h // sh)
    if scale < 1:
        raise SystemExit("Original is larger than the safe area; refusing to downscale silently.")
    tw, th = sw * scale, sh * scale
    rgb = src.convert("RGB")
    scaled = rgb.resize((tw, th), Image.Resampling.NEAREST)
    x, y = (W - tw) // 2, (H - th) // 2
    canvas = Image.new("RGB", (W, H), GROUND)
    canvas.paste(scaled, (x, y))
    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(EXPORT, optimize=True)

    PROOF.parent.mkdir(parents=True, exist_ok=True)
    canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(PROOF, optimize=True)

    # Reversibility check: the placed region downsampled back by the integer factor
    # must equal the original pixels exactly.
    region = Image.open(EXPORT).convert("RGB").crop((x, y, x + tw, y + th))
    restored = region.resize((sw, sh), Image.Resampling.NEAREST)
    lossless = restored.tobytes() == rgb.tobytes()

    after = sha256(SRC)
    record = {
        "source": "source/original.gif",
        "source_sha256_before": before,
        "source_sha256_after": after,
        "source_unmodified": before == after,
        "source_size": [sw, sh],
        "canvas": [W, H],
        "safe_area": list(SAFE),
        "scale_factor": scale,
        "resampling": "nearest-neighbour, whole-number factor (aspect ratio preserved)",
        "placed_rect": [x, y, x + tw, y + th],
        "crop": None,
        "ground_rgb": "#111318",
        "burned_in_text": None,
        "reversible_pixel_check": lossless,
        "proof_720": {"path": "proofs/editorial-frame-720.png", "resampling": "Lanczos 1920x1080 -> 1280x720"},
        "pillow": PIL_VERSION,
    }
    RECORD.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))
    if not (lossless and before == after):
        raise SystemExit("Framing check failed.")


if __name__ == "__main__":
    main()
