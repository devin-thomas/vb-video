#!/usr/bin/env python3
"""HIST-15 editorial frame: reversible pillarbox of the untouched archival bitmap.

Input : source/original.dib  (640x480, 8-bit BMP, byte-identical to the file on the CD)
Output: exports/editorial-frame.png   1920x1080 delivery frame
        qa/editorial-frame-720p.png   1280x720 proof of the same frame

Transform: uniform scale by 936/480 = 1.95 (Lanczos) so the whole screen fits the
shared safe area height (y 72..1008), centred horizontally (x 336..1584), on a flat
#111318 ground. No crop, no stretch, no retouching, no added text or UI.
Reverse: crop box (336, 72, 1584, 1008) and scale by 480/936 recovers the framing;
the pixel-exact original is source/original.dib itself.
"""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parents[1]
SRC = HERE / "source" / "original.dib"
OUT = HERE / "exports" / "editorial-frame.png"
PROOF = HERE / "qa" / "editorial-frame-720p.png"

CANVAS = (1920, 1080)
GROUND = (0x11, 0x13, 0x18)
SAFE_TOP, SAFE_BOTTOM = 72, 1008


def main() -> None:
    im = Image.open(SRC)
    assert im.size == (640, 480), im.size
    rgb = im.convert("RGB")
    target_h = SAFE_BOTTOM - SAFE_TOP                      # 936
    target_w = round(rgb.width * target_h / rgb.height)    # 1248, aspect preserved
    scaled = rgb.resize((target_w, target_h), Image.Resampling.LANCZOS)
    frame = Image.new("RGB", CANVAS, GROUND)
    x = (CANVAS[0] - target_w) // 2                        # 336
    frame.paste(scaled, (x, SAFE_TOP))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    PROOF.parent.mkdir(parents=True, exist_ok=True)
    frame.save(OUT, format="PNG", optimize=False)
    frame.resize((1280, 720), Image.Resampling.LANCZOS).save(PROOF, format="PNG")
    print(f"placed {target_w}x{target_h} at ({x},{SAFE_TOP}) -> {OUT.name}, {PROOF.name}")


if __name__ == "__main__":
    main()
