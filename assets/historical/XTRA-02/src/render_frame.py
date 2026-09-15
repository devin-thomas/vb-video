#!/usr/bin/env python3
"""XTRA-02 editorial frame: pillarbox the untouched native scan leaf onto a 1920x1080 canvas.

Reads source/original.jp2 (never modified). Writes:
  exports/editorial-frame.png        1920x1080 editorial framing copy
  proofs/editorial-frame-720p.png    1280x720 downscale for 720p inspection
  evidence/folio-showthrough.png     mirrored footer crop (page-number evidence)
  evidence/framing.json              exact geometry and transformations

Run from the repository root:
  python assets/historical/XTRA-02/src/render_frame.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "source" / "original.jp2"
W, H = 1920, 1080
SAFE_X0, SAFE_X1, SAFE_Y0, SAFE_Y1 = 120, 1800, 72, 1008
BG = (17, 19, 24)          # bible dark background #111318
FG = (241, 243, 245)       # bible light foreground #F1F3F5
MUTED = (170, 176, 184)
FONT_REG = Path(r"C:\Windows\Fonts\segoeui.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\segoeuib.ttf")

# Authored caption (production addition, not source text). Facts are from the
# evidence records: magazine title/date from the scan's own footer, page 97 from
# neighbouring folios (leaf 95 = p.96, leaf 97 = p.98).
CAPTION = [
    ("Microsoft Developer", FONT_BOLD, 34, FG),
    ("Network advertisement", FONT_BOLD, 34, FG),
    ("Boardwatch Magazine", FONT_REG, 30, FG),
    ("June 1996, page 97", FONT_REG, 30, FG),
    ("Scan: Internet Archive", FONT_REG, 26, MUTED),
    ("item boardwatch-1996-06", FONT_REG, 26, MUTED),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    before = sha256(SRC)
    page = Image.open(SRC)
    page.load()
    src_w, src_h = page.size
    page = page.convert("RGB")

    # Fit the whole page inside the safe-area height; preserve aspect ratio exactly.
    target_h = SAFE_Y1 - SAFE_Y0
    scale = target_h / src_h
    target_w = round(src_w * scale)
    fitted = page.resize((target_w, target_h), Image.Resampling.LANCZOS)
    px = (W - target_w) // 2
    py = SAFE_Y0

    canvas = Image.new("RGB", (W, H), BG)
    canvas.paste(fitted, (px, py))
    draw = ImageDraw.Draw(canvas)
    # Thin neutral keyline so the page edge reads against the dark ground.
    draw.rectangle((px - 1, py - 1, px + target_w, py + target_h), outline=(70, 74, 82), width=1)

    # Caption column: left of the page, bottom-aligned in the safe area.
    col_x0, col_x1 = SAFE_X0, px - 48
    lines = []
    for text, font_path, size, color in CAPTION:
        font = ImageFont.truetype(str(font_path), size)
        while draw.textlength(text, font=font) > (col_x1 - col_x0) and size > 26:
            size -= 1
            font = ImageFont.truetype(str(font_path), size)
        lines.append((text, font, size, color))
    # Uniform leading from font metrics (not per-glyph ink boxes), with a group gap
    # before the title/issue block's end and before the scan credit.
    leading = 1.25
    group_gap = {2: 10, 4: 22}
    advances = [round(size * leading) for _, _, size, _ in lines]
    total = sum(advances) + sum(group_gap.values())
    y = SAFE_Y1 - total
    for i, ((text, font, size, color), adv) in enumerate(zip(lines, advances)):
        y += group_gap.get(i, 0)
        draw.text((col_x0, y), text, font=font, fill=color)
        y += adv

    exports = BASE / "exports"; exports.mkdir(exist_ok=True)
    proofs = BASE / "proofs"; proofs.mkdir(exist_ok=True)
    evidence = BASE / "evidence"; evidence.mkdir(exist_ok=True)
    frame_path = exports / "editorial-frame.png"
    canvas.save(frame_path, optimize=True)
    canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(proofs / "editorial-frame-720p.png", optimize=True)

    # Page-number evidence: the ad has no folio of its own; the footer shows mirrored
    # show-through of the reverse side's folio. Mirror and auto-contrast to read it.
    foot = page.crop((1500, 3080, src_w, src_h))
    foot = ImageOps.autocontrast(ImageOps.grayscale(ImageOps.mirror(foot)), cutoff=2)
    foot.save(evidence / "folio-showthrough.png", optimize=True)

    after = sha256(SRC)
    assert before == after, "source/original.jp2 changed during render"
    framing = {
        "source": "source/original.jp2",
        "source_sha256": before,
        "source_dimensions": {"width": src_w, "height": src_h},
        "canvas": {"width": W, "height": H, "background": "#111318"},
        "safe_area": {"x0": SAFE_X0, "x1": SAFE_X1, "y0": SAFE_Y0, "y1": SAFE_Y1},
        "page_placement": {"x": px, "y": py, "width": target_w, "height": target_h},
        "scale": scale,
        "aspect_ratio_source": src_w / src_h,
        "aspect_ratio_placed": target_w / target_h,
        "transformations": [
            "JPEG 2000 decoded to RGB (Pillow/OpenJPEG)",
            "uniform Lanczos downscale to the safe-area height; width rounded to nearest pixel",
            "no crop, rotation, colour correction, retouching or watermark removal of the page",
            "pillarboxed on #111318 with a 1px #464A52 keyline",
            "authored caption set in Segoe UI (system font, not bundled) in the left column",
        ],
        "caption_authored": [t for t, *_ in CAPTION],
        "fonts_resolved": [str(FONT_REG), str(FONT_BOLD)],
        "folio_evidence_crop": {"box": [1500, 3080, src_w, src_h], "ops": ["mirror", "grayscale", "autocontrast 2%"],
                                "path": "evidence/folio-showthrough.png"},
    }
    (evidence / "framing.json").write_text(json.dumps(framing, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(framing["page_placement"]), f"scale={scale:.6f}", f"source_unchanged={before == after}")


if __name__ == "__main__":
    main()
