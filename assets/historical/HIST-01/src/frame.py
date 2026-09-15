#!/usr/bin/env python3
"""HIST-01 editorial framing: reversible, no-crop, integer-scale pillarbox of source/original.png.

Run from the repository root:  python assets/historical/HIST-01/src/frame.py

Writes exports/editorial-frame.png (1920x1080), proofs/editorial-frame-720.png (1280x720)
and evidence/render-tests.json. No text, fonts, network or third-party imagery is added.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import PIL
from PIL import Image

BASE = Path(__file__).resolve().parents[1]
FRAME = json.loads((BASE / "src" / "frame.json").read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    src_path = BASE / FRAME["input"]
    original = Image.open(src_path)
    src_rgb = original.convert("RGB")
    w, h = src_rgb.size
    assert (w, h) == tuple(FRAME["input_size"]), (w, h)

    scale = FRAME["scale"]
    cw, ch = FRAME["canvas"]
    sw, sh = w * scale, h * scale
    ox, oy = (cw - sw) // 2, (ch - sh) // 2
    assert [ox, oy] == FRAME["offset"], (ox, oy)

    canvas = Image.new("RGB", (cw, ch), FRAME["background"])
    canvas.paste(src_rgb.resize((sw, sh), Image.Resampling.NEAREST), (ox, oy))

    export = BASE / "exports" / "editorial-frame.png"
    export.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(export, format="PNG", optimize=True)

    proof = BASE / "proofs" / "editorial-frame-720.png"
    proof.parent.mkdir(parents=True, exist_ok=True)
    canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(proof, format="PNG", optimize=True)

    # Reversibility: recover the original pixels from the export using only frame.json.
    reread = Image.open(export).convert("RGB")
    region = reread.crop((ox, oy, ox + sw, oy + sh))
    recovered = region.resize((w, h), Image.Resampling.NEAREST)
    reversible = recovered.tobytes() == src_rgb.tobytes()

    # Every scaled source pixel is an exact 2x2 block (no interpolation, no alteration).
    blocks_exact = region.tobytes() == src_rgb.resize((sw, sh), Image.Resampling.NEAREST).tobytes()

    # Pillarbox is uniform: nothing but the background outside the image rectangle.
    bg = tuple(int(FRAME["background"][i:i + 2], 16) for i in (1, 3, 5))
    mask = Image.new("L", (cw, ch), 255)
    mask.paste(0, (ox, oy, ox + sw, oy + sh))
    outside = Image.composite(reread, Image.new("RGB", (cw, ch), bg), mask)
    outside_colors = outside.getcolors(maxcolors=4)
    pillarbox_clean = outside_colors is not None and len(outside_colors) == 1 and outside_colors[0][1] == bg

    tests = {
        "id": "HIST-01",
        "command": "python assets/historical/HIST-01/src/frame.py",
        "input": {"path": FRAME["input"], "sha256": sha256(src_path), "size": [w, h], "mode": original.mode},
        "export": {"path": "exports/editorial-frame.png", "size": list(reread.size), "sha256": sha256(export)},
        "proof_720": {"path": "proofs/editorial-frame-720.png", "size": list(Image.open(proof).size), "sha256": sha256(proof)},
        "image_rect": [ox, oy, ox + sw, oy + sh],
        "checks": {
            "export_is_1920x1080": reread.size == (1920, 1080),
            "aspect_ratio_preserved": sw * h == sh * w,
            "whole_screenshot_included_no_crop": region.size == (sw, sh) and (sw, sh) == (w * scale, h * scale),
            "reversible_to_original_pixels": reversible,
            "nearest_neighbour_blocks_exact": blocks_exact,
            "pillarbox_uniform_background_only": pillarbox_clean,
        },
        "toolchain": {"python": platform.python_version(), "Pillow": PIL.__version__, "os": platform.platform()},
    }
    tests["passed"] = all(tests["checks"].values())
    (BASE / "evidence" / "render-tests.json").write_text(json.dumps(tests, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(tests, indent=2))
    if not tests["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
