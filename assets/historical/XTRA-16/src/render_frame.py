#!/usr/bin/env python3
"""XTRA-16 editorial frame: place the untouched Microsoft Upgrade Report figure on a 1920x1080 canvas.

Reversible framing only. The screenshot is resized uniformly (one scale factor, no crop, no
annotation, no recolouring) and centred; a small factual source line sits below it inside the
safe area. source/original.gif is opened read-only and never rewritten.

Run from the repository root:
    python assets/historical/XTRA-16/src/render_frame.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parents[1]
ORIGINAL = BASE / "source" / "original.gif"
EXPORT = BASE / "exports" / "editorial-frame.png"
PROOF = BASE / "qa" / "editorial-frame-720p.png"
FRAMING = BASE / "evidence" / "framing.json"

EXPECTED_SHA256 = "139f1c1a1f785ea0688aa96ce6a04b079136601006d530463504987b23267ad0"
CANVAS = (1920, 1080)
SAFE = (120, 72, 1800, 1008)  # production bible safe area (x0, y0, x1, y1)
BACKGROUND = "#111318"  # bible token: dark code background
RULE = "#C0C0C0"  # bible token: window gray, 2 px hairline around the screenshot
CAPTION_COLOUR = "#F1F3F5"  # bible token: light foreground
SCALE = 1.65
FONT_PATH = Path(r"C:\Windows\Fonts\segoeui.ttf")  # installed system font; not bundled
CAPTION_PX = 28
LINE_GAP = 8
CAPTION_LINES = (
    "Visual Basic Upgrade Wizard report \u00b7 Visual Studio 2005 \u00b7 Microsoft",
    "\u201cDeconstructing the Visual Basic Upgrade Wizard,\u201d Bill Sempf, MSDN, March 2006 \u00b7 Figure 1",
)
CAPTION = "\n".join(CAPTION_LINES)


def main() -> None:
    data = ORIGINAL.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"source/original.gif changed: {digest}")

    with Image.open(ORIGINAL) as im:
        native = im.size
        rgb = im.convert("RGB")

    width = round(native[0] * SCALE)
    height = round(native[1] * SCALE)
    shot = rgb.resize((width, height), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", CANVAS, BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(str(FONT_PATH), CAPTION_PX)

    gap = 20
    ascent, descent = font.getmetrics()
    line_h = ascent + descent
    caption_h = line_h * len(CAPTION_LINES) + LINE_GAP * (len(CAPTION_LINES) - 1)
    block_h = height + gap + caption_h
    top = SAFE[1] + ((SAFE[3] - SAFE[1]) - block_h) // 2
    left = (CANVAS[0] - width) // 2

    draw.rectangle((left - 2, top - 2, left + width + 1, top + height + 1), fill=RULE)
    canvas.paste(shot, (left, top))

    extents = {"screenshot": (left - 2, top - 2, left + width + 2, top + height + 2)}
    y = top + height + gap
    for index, line in enumerate(CAPTION_LINES):
        box = draw.textbbox((0, 0), line, font=font)
        x = (CANVAS[0] - (box[2] - box[0])) // 2 - box[0]
        draw.text((x, y), line, font=font, fill=CAPTION_COLOUR)
        extents[f"caption_line_{index + 1}"] = (x + box[0], y + box[1], x + box[2], y + box[3])
        y += line_h + LINE_GAP

    for name, (x0, y0, x1, y1) in extents.items():
        if x0 < SAFE[0] or y0 < SAFE[1] or x1 > SAFE[2] or y1 > SAFE[3]:
            raise SystemExit(f"{name} leaves the safe area: {(x0, y0, x1, y1)}")
    image_extent = (left, top, left + width, top + height)
    cap_extent = [list(extents[k]) for k in extents if k.startswith("caption")]

    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    PROOF.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(EXPORT, "PNG", optimize=True)
    canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(PROOF, "PNG", optimize=True)

    framing = {
        "source": "source/original.gif",
        "source_sha256": digest,
        "native_size": list(native),
        "scale": SCALE,
        "resampling": "Pillow LANCZOS, applied once to the whole screenshot",
        "placed_size": [width, height],
        "horizontal_scale": round(width / native[0], 5),
        "vertical_scale": round(height / native[1], 5),
        "aspect_error_percent": round(abs((width / height) / (native[0] / native[1]) - 1) * 100, 4),
        "placed_box_xyxy": list(image_extent),
        "crop": None,
        "annotations": None,
        "border": "2 px #C0C0C0 hairline outside the screenshot; no pixels of the screenshot covered",
        "background": BACKGROUND,
        "caption": CAPTION,
        "caption_font": str(FONT_PATH),
        "caption_px": CAPTION_PX,
        "caption_box_xyxy": list(cap_extent),
        "safe_area_xyxy": list(SAFE),
        "canvas": list(CANVAS),
        "exports": {"editorial-frame": "exports/editorial-frame.png", "proof_720p": "qa/editorial-frame-720p.png"},
    }
    FRAMING.write_text(json.dumps(framing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(framing, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
