#!/usr/bin/env python3
"""HIST-04 reversible framing. Reads the untouched archive file and writes framed copies.

Nothing is painted over, retouched, sharpened, recolored, or stretched. The only
transformations are a rectangular crop (editorial-frame only), a uniform resize,
and placement on a flat 1920x1080 ground. Parameters are written to
evidence/framing.json so the framing can be inverted or redone differently.

Run from the repository root:
    python assets/historical/HIST-04/src/make_frame.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, __version__ as PIL_VERSION

BASE = Path(__file__).resolve().parents[1]
ORIGINAL = BASE / "source" / "original.jpg"
CANVAS = (1920, 1080)
GROUND = (17, 19, 24)  # #111318, production-bible dark background
SAFE_TOP, SAFE_BOTTOM = 72, 1008  # production-bible safe area (y)
TARGET_H = SAFE_BOTTOM - SAFE_TOP  # 936 px

# Photographic image area inside the mounted print, measured from column/row
# luminance profiles of source/original.jpg (mount edge at x=93/908, y=51/668).
# Inset so no mount-edge fringe remains. The top edge is y=56 because the red
# printer's crop-mark tick at top right (x~893-896) carries ink to row 53 and a
# faint JPEG tint to row 55. Only the mount border, crop marks, and a 4-pixel
# sliver of ceiling at the top edge are removed; no meaningful content is cut.
PRINT_BOX = (95, 56, 907, 667)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frame(img: Image.Image, crop_box):
    src = img.crop(crop_box) if crop_box else img
    scale = TARGET_H / src.height
    size = (round(src.width * scale), TARGET_H)
    resized = src.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", CANVAS, GROUND)
    offset = ((CANVAS[0] - size[0]) // 2, SAFE_TOP)
    canvas.paste(resized, offset)
    return canvas, {
        "crop_box_ltrb_in_original_px": list(crop_box) if crop_box else None,
        "cropped_size": [src.width, src.height],
        "uniform_scale": round(scale, 6),
        "placed_size": list(size),
        "placed_offset_xy": list(offset),
    }


def main() -> None:
    img = Image.open(ORIGINAL).convert("RGB")
    out = BASE / "exports"
    out.mkdir(exist_ok=True)
    records = {}
    for name, box in [("original", None), ("editorial-frame", PRINT_BOX)]:
        canvas, rec = frame(img, box)
        path = out / f"{name}.png"
        canvas.save(path, optimize=False)
        proof = BASE / "evidence" / f"proof-720p-{name}.png"
        canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(proof, optimize=False)
        rec.update(export=f"exports/{name}.png", proof_720p=f"evidence/proof-720p-{name}.png")
        records[name] = rec
    framing = {
        "input": "source/original.jpg",
        "input_sha256": sha(ORIGINAL),
        "input_size": list(img.size),
        "canvas": list(CANVAS),
        "ground_rgb": list(GROUND),
        "resample": "Pillow LANCZOS, uniform (aspect ratio preserved)",
        "pillow_version": PIL_VERSION,
        "variants": records,
        "not_done": ["no stretching", "no retouching or dust removal", "no sharpening or tonal change",
                     "no watermark present or removed", "no text, captions, labels or UI added"],
        "upscale_note": "Both variants enlarge the 1000x724 web derivative (about 1.29x for original, 1.52x for editorial-frame). "
                        "Softness at 1080p is expected; a publication-quality scan from Rauner would remove it.",
    }
    (BASE / "evidence" / "framing.json").write_text(json.dumps(framing, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
