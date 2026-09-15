#!/usr/bin/env python3
"""HIST-07 editorial frame renderer (editable input).

Deterministic: reads source/original.jpg (byte-exact Commons 2019 upload of
File:Trinity77.jpg), takes one axis-aligned crop around the TRS-80 Model I,
scales it uniformly (no stretching), pillarboxes it on a 1920x1080 canvas and
adds a single authored credit line. Also writes the 720p review proof.

Reversibility: the crop box below is in native pixels of source/original.jpg;
the original is kept untouched, so the full uncropped photo is always
recoverable.

Run from the repo root:
    python assets/historical/HIST-07/src/render_editorial_frame.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parents[1]
ORIGINAL = HERE / "source" / "original.jpg"
EXPORT = HERE / "exports" / "editorial-frame.png"
PROOF_720 = HERE / "qa" / "editorial-frame-720p.png"
PROOF_FULL = HERE / "qa" / "editorial-frame-1080p-check.png"
CROP_RECORD = HERE / "evidence" / "crop.json"

EXPECTED_SHA1 = "cbaeec4d22aaefe9ffc0ae7656cb0fa9e3adaf59"
CANVAS = (1920, 1080)
SAFE = (120, 72, 1800, 1008)  # production bible safe area x0, y0, x1, y1
BACKGROUND = (0x11, 0x13, 0x18)  # production bible dark background #111318
CREDIT_COLOR = (0xC8, 0xCC, 0xD2)
# Native-pixel crop (left, top, right, bottom): whole TRS-80 Model I monitor,
# expansion interface and keyboard; excludes the neighbouring Apple II.
CROP_BOX = (2740, 190, 3973, 1430)
IMAGE_TOP = SAFE[1]
IMAGE_BOTTOM = 924  # leaves a credit band inside the safe area
CREDIT_LINES = [
    "TRS-80 Model I, Level II BASIC power-up prompt",
    "Photo: Tim Colegrove (2019), CC BY-SA 4.0, cropped",
]
FONT_PATH = Path(r"C:\Windows\Fonts\LiberationSans-Regular.ttf")  # installed system font, not bundled
FONT_SIZE = 26


def main() -> None:
    data = ORIGINAL.read_bytes()
    sha1 = hashlib.sha1(data).hexdigest()
    if sha1 != EXPECTED_SHA1:
        raise SystemExit(f"source/original.jpg SHA-1 {sha1} != expected {EXPECTED_SHA1}")
    with Image.open(ORIGINAL) as im:
        im.load()
        native_size = im.size
        crop = im.convert("RGB").crop(CROP_BOX)

    target_h = IMAGE_BOTTOM - IMAGE_TOP
    scale = target_h / crop.height
    target_w = round(crop.width * scale)
    scaled = crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
    x = (CANVAS[0] - target_w) // 2
    y = IMAGE_TOP

    canvas = Image.new("RGB", CANVAS, BACKGROUND)
    canvas.paste(scaled, (x, y))

    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)
    line_gap = 6
    heights = [draw.textbbox((0, 0), t, font=font)[3] for t in CREDIT_LINES]
    total = sum(heights) + line_gap * (len(CREDIT_LINES) - 1)
    ty = SAFE[3] - total
    for text, h in zip(CREDIT_LINES, heights):
        w = draw.textlength(text, font=font)
        draw.text(((CANVAS[0] - w) / 2, ty), text, font=font, fill=CREDIT_COLOR)
        ty += h + line_gap

    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    PROOF_720.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(EXPORT, format="PNG", optimize=False)
    canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(PROOF_720, format="PNG")
    # 1:1 native-pixel check of the screen area of the export for full-size inspection
    canvas.crop((x, y, x + target_w, y + 420)).save(PROOF_FULL, format="PNG")

    CROP_RECORD.write_text(json.dumps({
        "source": "source/original.jpg",
        "source_sha1": sha1,
        "source_native_size": list(native_size),
        "crop_box_native_px": {"left": CROP_BOX[0], "top": CROP_BOX[1], "right": CROP_BOX[2], "bottom": CROP_BOX[3]},
        "crop_size_px": [crop.width, crop.height],
        "uniform_scale": round(scale, 6),
        "resample": "LANCZOS",
        "placed_at_px": {"x": x, "y": y, "width": target_w, "height": target_h},
        "canvas": list(CANVAS),
        "background": "#111318",
        "authored_text": CREDIT_LINES,
        "font": {"path": str(FONT_PATH), "family": "Liberation Sans", "size_px": FONT_SIZE, "bundled": False},
        "reverse": "Invert by mapping placed rectangle back through uniform_scale to crop_box_native_px on source/original.jpg; the original file is unmodified.",
    }, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"export": str(EXPORT), "scale": scale, "placed": [x, y, target_w, target_h]}))


if __name__ == "__main__":
    main()
