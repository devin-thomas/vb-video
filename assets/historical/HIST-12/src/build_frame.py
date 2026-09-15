#!/usr/bin/env python3
"""HIST-12 editorial framing: place the UNCROPPED Borland Delphi 1.0 IDE figure in 1920x1080.

The original is a 444x282 16-colour GIF87a. It is upscaled by an exact integer factor with
nearest-neighbour resampling and centred on a flat neutral matte. No pixels are removed, no
text/UI is added, nothing is retouched, and no watermark is removed. The transform is exactly
reversible, which this script verifies: taking every Nth pixel of the placed region restores
the original raster bit for bit.

Run from the repository root:  python assets/historical/HIST-12/src/build_frame.py
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ASSET = HERE.parent
FRAMING = json.loads((HERE / "framing.json").read_text(encoding="utf-8"))


def main() -> None:
    src = Image.open(ASSET / FRAMING["input"])
    ow, oh = src.size
    if FRAMING["crop_box"] != [0, 0, ow, oh]:
        raise SystemExit("framing.json crop_box must be the full original for this variant")
    rgb = src.convert("RGB")

    cw, ch = FRAMING["canvas"]
    x0, y0, x1, y1 = FRAMING["safe_area"]
    n = int(FRAMING["scale_factor"])
    max_fit = int(min((x1 - x0) / ow, (y1 - y0) / oh))
    if n < 1 or n > max_fit:
        raise SystemExit(f"scale_factor {n} does not fit the safe area (max integer fit {max_fit})")

    w, h = ow * n, oh * n
    placed = rgb.resize((w, h), Image.Resampling.NEAREST)
    canvas = Image.new("RGB", (cw, ch), tuple(FRAMING["matte_rgb"]))
    left, top = (cw - w) // 2, (ch - h) // 2
    canvas.paste(placed, (left, top))

    # Reversibility proof: decimate the placed region and compare with the original raster.
    back = canvas.crop((left, top, left + w, top + h)).resize((ow, oh), Image.Resampling.NEAREST)
    reversible = back.tobytes() == rgb.tobytes()
    if not reversible:
        raise SystemExit("framing is not bit-exactly reversible; refusing to write outputs")

    out = ASSET / "exports" / "editorial-frame.png"
    proof = ASSET / "proofs" / "editorial-frame-720.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    proof.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, optimize=True)
    canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(proof, optimize=True)

    record = {
        "original_size": [ow, oh],
        "original_mode": src.mode,
        "original_palette_colors": len(src.getpalette()) // 3 if src.getpalette() else None,
        "scale": n,
        "resample": "NEAREST",
        "placed_size": [w, h],
        "placed_offset": [left, top],
        "aspect_original": ow / oh,
        "aspect_placed": w / h,
        "aspect_error_pct": abs((w / h) / (ow / oh) - 1) * 100,
        "cropped": False,
        "reversible_bit_exact": reversible,
        "outputs": [out.relative_to(ASSET).as_posix(), proof.relative_to(ASSET).as_posix()],
    }
    (HERE / "framing-result.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
