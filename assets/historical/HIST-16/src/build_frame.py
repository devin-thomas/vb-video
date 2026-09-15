#!/usr/bin/env python3
"""HIST-16 editorial framing: source/original.gif -> exports/editorial-frame.png (+ 720p proof).

Reversible, non-destructive framing only. The full, uncropped original is scaled by an
integer factor with nearest-neighbour sampling (every source pixel becomes a 3x3 block,
no smoothing, no stretch), centred on a neutral ground inside the shared safe area, with
one authored credit line underneath. Nothing inside the screenshot is altered.

Run from the repository root:
    python assets/historical/HIST-16/src/build_frame.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, __version__ as PIL_VERSION

BASE = Path(__file__).resolve().parents[1]
ORIGINAL = BASE / "source" / "original.gif"
EXPORT = BASE / "exports" / "editorial-frame.png"
PROOF = BASE / "proofs" / "editorial-frame-720.png"
FRAMING = BASE / "evidence" / "framing.json"

CANVAS = (1920, 1080)
SAFE = (120, 72, 1800, 1008)          # shared safe area x0, y0, x1, y1
SCALE = 3                              # integer, nearest-neighbour
GROUND = (27, 29, 34)                  # neutral dark ground; deliberately not Win95 teal
CREDIT_COLOR = (200, 204, 210)
CREDIT_SIZE = 30
GAP = 34                               # image bottom to credit top
FONT_CANDIDATES = [
    Path("C:/Windows/Fonts/LiberationSans-Regular.ttf"),
    Path("C:/Windows/Fonts/segoeui.ttf"),
]
# Authored production text (not a quotation from the source). Kept factual and minimal.
CREDIT = ("\u201cThe AWT Components\u201d example window \u2014 The Java Tutorial, "
          "Sun Microsystems (online copy dated Feb. 1996)")


def main() -> None:
    src = Image.open(ORIGINAL)
    src_size = src.size
    rgb = src.convert("RGB")
    scaled = rgb.resize((src_size[0] * SCALE, src_size[1] * SCALE), Image.NEAREST)

    font_path = next(p for p in FONT_CANDIDATES if p.is_file())
    font = ImageFont.truetype(str(font_path), CREDIT_SIZE)

    canvas = Image.new("RGB", CANVAS, GROUND)
    draw = ImageDraw.Draw(canvas)
    tb = draw.textbbox((0, 0), CREDIT, font=font)
    text_w, text_h = tb[2] - tb[0], tb[3] - tb[1]

    block_h = scaled.height + GAP + text_h
    x = (CANVAS[0] - scaled.width) // 2
    y = (CANVAS[1] - block_h) // 2
    canvas.paste(scaled, (x, y))
    tx = (CANVAS[0] - text_w) // 2 - tb[0]
    ty = y + scaled.height + GAP - tb[1]
    draw.text((tx, ty), CREDIT, font=font, fill=CREDIT_COLOR)

    image_box = [x, y, x + scaled.width, y + scaled.height]
    text_box = [tx + tb[0], ty + tb[1], tx + tb[2], ty + tb[3]]
    for box in (image_box, text_box):
        assert SAFE[0] <= box[0] and box[2] <= SAFE[2] and SAFE[1] <= box[1] and box[3] <= SAFE[3], box

    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    PROOF.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(EXPORT, optimize=True)
    canvas.resize((1280, 720), Image.LANCZOS).save(PROOF, optimize=True)

    # Reversibility check: the pasted region, sampled every SCALE pixels, equals the original.
    region = canvas.crop(image_box)
    restored = region.resize(src_size, Image.NEAREST)
    identical = restored.tobytes() == rgb.tobytes()
    assert identical, "framing altered source pixels"

    record = {
        "source": "source/original.gif",
        "source_sha256": hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(),
        "source_size": list(src_size),
        "crop": None,
        "crop_note": "No crop. The whole original, including its window border, is shown.",
        "scale": SCALE,
        "resample": "nearest (integer pixel replication; aspect ratio preserved exactly)",
        "canvas": list(CANVAS),
        "ground_rgb": list(GROUND),
        "image_box_xyxy": image_box,
        "credit_text": CREDIT,
        "credit_text_status": "authored production caption, not a quotation from the source",
        "credit_box_xyxy": text_box,
        "font_file": font_path.name,
        "font_size_px": CREDIT_SIZE,
        "safe_area_xyxy": list(SAFE),
        "reversibility_check": "image region downsampled by nearest to source size is byte-identical to the original's RGB pixels" if identical else "FAILED",
        "outputs": {"export": "exports/editorial-frame.png", "proof_720": "proofs/editorial-frame-720.png"},
        "tool": f"Pillow {PIL_VERSION}",
        "command": "python assets/historical/HIST-16/src/build_frame.py",
    }
    FRAMING.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
