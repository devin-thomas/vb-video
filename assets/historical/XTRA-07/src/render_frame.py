#!/usr/bin/env python3
"""XTRA-07 editorial framing: reversible, uniform-scale presentation copy of the acquired disc scan.

Inputs : source/original.png (byte-identical copy of the Internet Archive file; never modified)
Outputs: exports/editorial-frame.png (1920x1080), proofs/editorial-frame-720.png (1280x720),
         evidence/label-crop.png (1:1 crop of the printed label text), evidence/framing.json

Transformations (presentation copy only):
  1. Rim detection ignores isolated dust specks on the scanner bed: a 9 px max filter (lightens small dark
     specks) runs before thresholding, then the non-white bounding box plus 10 px padding defines an ellipse.
  2. That anti-aliased ellipse masks out the blank scanner bed in the corners. The check in framing.json
     reports every non-white pixel removed and how far it lies from the rim.
  3. Uniform (aspect-preserving) LANCZOS scale so the disc's height fills the safe area (y=72..1008).
  4. Centered on the production-bible dark ground #111318. No text, logo, colour grade or retouching.
Run from the repository root: python assets/historical/XTRA-07/src/render_frame.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, __version__ as PIL_VERSION

BASE = Path(__file__).resolve().parents[1]
W, H = 1920, 1080
SAFE_TOP, SAFE_BOTTOM = 72, 1008
GROUND = (0x11, 0x13, 0x18)
WHITE_THRESHOLD = 235  # luminance at or above this counts as blank scanner bed when finding the rim
SPECK_FILTER = 9       # max-filter size; removes dark specks smaller than this from rim detection only
PAD = 10  # chosen by inspecting rim crops: 3 px shaved the rim edge, 6 px was the minimum with no dark rim pixels outside; 10 px keeps the soft outer falloff
SUPERSAMPLE = 4


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pixels(img: Image.Image) -> list:
    getter = getattr(img, "get_flattened_data", None) or img.getdata
    return list(getter())


def main() -> None:
    src = BASE / "source/original.png"
    original = Image.open(src)
    original.load()
    rgb = original.convert("RGB")
    ow, oh = rgb.size
    lum = rgb.convert("L")

    despeckled = lum.filter(ImageFilter.MaxFilter(SPECK_FILTER))
    nonwhite = despeckled.point(lambda v: 255 if v < WHITE_THRESHOLD else 0)
    bbox = nonwhite.getbbox()
    raw_bbox = lum.point(lambda v: 255 if v < WHITE_THRESHOLD else 0).getbbox()
    assert bbox is not None
    x0, y0, x1, y1 = max(0, bbox[0] - PAD), max(0, bbox[1] - PAD), min(ow, bbox[2] + PAD), min(oh, bbox[3] + PAD)
    disc = rgb.crop((x0, y0, x1, y1))
    dw, dh = disc.size

    mask_big = Image.new("L", (dw * SUPERSAMPLE, dh * SUPERSAMPLE), 0)
    ImageDraw.Draw(mask_big).ellipse((0, 0, dw * SUPERSAMPLE - 1, dh * SUPERSAMPLE - 1), fill=255)
    mask = mask_big.resize((dw, dh), Image.Resampling.LANCZOS)

    target_h = SAFE_BOTTOM - SAFE_TOP
    scale = target_h / dh
    tw, th = round(dw * scale), target_h
    disc_s = disc.resize((tw, th), Image.Resampling.LANCZOS)
    mask_s = mask.resize((tw, th), Image.Resampling.LANCZOS)

    frame = Image.new("RGB", (W, H), GROUND)
    left = (W - tw) // 2
    frame.paste(disc_s, (left, SAFE_TOP), mask_s)

    (BASE / "exports").mkdir(exist_ok=True)
    (BASE / "proofs").mkdir(exist_ok=True)
    out = BASE / "exports/editorial-frame.png"
    frame.save(out, optimize=True)
    proof = BASE / "proofs/editorial-frame-720.png"
    frame.resize((1280, 720), Image.Resampling.LANCZOS).save(proof, optimize=True)

    label_box = (1900, 850, 2500, 1250)
    crop = BASE / "evidence/label-crop.png"
    rgb.crop(label_box).save(crop, optimize=True)

    # Reversibility check: list non-white original pixels that the mask hides (alpha < 128).
    full_mask = Image.new("L", (ow, oh), 0)
    full_mask.paste(mask, (x0, y0))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    removed = []
    for i, (v, m) in enumerate(zip(pixels(lum), pixels(full_mask))):
        if m < 128 and v < WHITE_THRESHOLD:
            x, y = i % ow, i // ow
            removed.append((x, y, v, ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2))
    near_rim = [r for r in removed if r[3] <= 1.02]

    record = {
        "input": {"path": "source/original.png", "sha256": sha256(src), "size": [ow, oh], "mode": original.mode},
        "rim_detection": {"white_threshold": WHITE_THRESHOLD, "speck_max_filter_px": SPECK_FILTER,
                          "raw_nonwhite_bbox_including_specks": list(raw_bbox) if raw_bbox else None,
                          "despeckled_bbox": list(bbox), "padding_px": PAD,
                          "disc_crop_box": [x0, y0, x1, y1], "disc_crop_size": [dw, dh]},
        "masked_out_nonwhite_pixels": {
            "count": len(removed),
            "within_2pct_of_rim": len(near_rim),
            "min_normalized_distance": min((r[3] for r in removed), default=None),
            "darkest_luminance": min((r[2] for r in removed), default=None),
            "interpretation": "Pixels far outside the rim (normalized distance > 1.02) are dust specks on the scanner bed; any pixel within 2% of the rim is reported so a clipped disc edge cannot pass unnoticed.",
        },
        "scale": {"uniform_factor": scale, "resized_to": [tw, th], "x_over_y_factor_ratio": (tw / dw) / (th / dh),
                  "resample": "LANCZOS"},
        "placement": {"canvas": [W, H], "left": left, "top": SAFE_TOP, "ground_rgb": "#111318",
                      "safe_area": {"x": [120, 1800], "y": [SAFE_TOP, SAFE_BOTTOM]}},
        "outputs": {
            "exports/editorial-frame.png": {"size": list(frame.size), "sha256": sha256(out)},
            "proofs/editorial-frame-720.png": {"size": [1280, 720], "sha256": sha256(proof)},
            "evidence/label-crop.png": {"source_box": list(label_box), "sha256": sha256(crop)},
        },
        "not_done": ["no stretching", "no colour grading", "no retouching or dust removal on the disc",
                     "no text or logo overlay", "no watermark removal (none present)"],
        "pillow": PIL_VERSION,
    }
    (BASE / "evidence/framing.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
