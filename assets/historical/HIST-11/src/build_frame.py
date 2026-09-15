#!/usr/bin/env python3
"""HIST-11 editorial framing: fit the UNCROPPED archival scan into the shared 1920x1080 safe area.

Reversible: no pixels are removed from the original; the scan is uniformly scaled (aspect kept)
and centered on a flat neutral matte. No text, watermark removal, retouching or UI is added.
Run from the repository root:  python assets/historical/HIST-11/src/build_frame.py
"""
from __future__ import annotations
import json
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ASSET = HERE.parent
FRAMING = json.loads((HERE / "framing.json").read_text(encoding="utf-8"))


def main() -> None:
    src = Image.open(ASSET / FRAMING["input"]).convert("RGB")
    ow, oh = src.size
    cw, ch = FRAMING["canvas"]
    x0, y0, x1, y1 = FRAMING["safe_area"]
    crop = FRAMING["crop_box"]  # full image = no crop
    if crop != [0, 0, ow, oh]:
        raise SystemExit("framing.json crop_box must be the full original for this variant")
    scale = min((x1 - x0) / ow, (y1 - y0) / oh)
    w, h = round(ow * scale), round(oh * scale)
    placed = src.resize((w, h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (cw, ch), tuple(FRAMING["matte_rgb"]))
    left, top = (cw - w) // 2, (ch - h) // 2
    canvas.paste(placed, (left, top))
    out = ASSET / "exports" / "editorial-frame.png"
    canvas.save(out, optimize=True)
    proof = ASSET / "proofs" / "editorial-frame-720.png"
    canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(proof, optimize=True)
    record = {
        "original_size": [ow, oh],
        "scale": scale,
        "placed_size": [w, h],
        "placed_offset": [left, top],
        "aspect_original": ow / oh,
        "aspect_placed": w / h,
        "aspect_error_pct": abs((w / h) / (ow / oh) - 1) * 100,
        "outputs": [out.relative_to(ASSET).as_posix(), proof.relative_to(ASSET).as_posix()],
    }
    (HERE / "framing-result.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
