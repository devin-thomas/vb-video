#!/usr/bin/env python3
"""XTRA-03 editorial frame: fit the untouched archive original inside 1920x1080.

Uniform scale only (no stretch), centred, pillarboxed on a flat dark ground.
No crop, no retouching, no text. The source file is hash-checked and never
written. Run from the repository root:

    python assets/historical/XTRA-03/src/render_frame.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps, __version__ as PIL_VERSION

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "source" / "original.jpg"
FRAME = BASE / "exports" / "editorial-frame.png"
PROOF_720 = BASE / "evidence" / "proof-720p.png"
RECORD = BASE / "evidence" / "framing.json"

W, H = 1920, 1080
GROUND = (0x11, 0x13, 0x18)  # production-bible dark background token #111318
EXPECTED_SHA256 = "8bfd08bf3a77e1632d6ec43c5b5f566b0719b2e8a3b7524c14736b5a3f5fcc16"


def main() -> int:
    data = SRC.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        print(f"source/original.jpg does not match the acquired file ({digest})", file=sys.stderr)
        return 1

    with Image.open(SRC) as raw:
        exif_orientation = raw.getexif().get(274)
        image = ImageOps.exif_transpose(raw).convert("RGB")
    sw, sh = image.size
    scale = min(W / sw, H / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    # Aspect must survive rounding to within one pixel.
    if abs(nw / nh - sw / sh) > 1 / min(nw, nh):
        print("aspect drift after rounding", file=sys.stderr)
        return 1
    x, y = (W - nw) // 2, (H - nh) // 2

    fitted = image.resize((nw, nh), Image.Resampling.LANCZOS)
    frame = Image.new("RGB", (W, H), GROUND)
    frame.paste(fitted, (x, y))
    FRAME.parent.mkdir(parents=True, exist_ok=True)
    frame.save(FRAME, format="PNG", optimize=False)

    proof = frame.resize((1280, 720), Image.Resampling.LANCZOS)
    PROOF_720.parent.mkdir(parents=True, exist_ok=True)
    proof.save(PROOF_720, format="PNG", optimize=False)

    record = {
        "asset": "XTRA-03",
        "operation": "uniform scale to fit, centre, pillarbox; no crop, no stretch, no retouch, no overlay text",
        "source": {"path": "source/original.jpg", "sha256": digest, "width": sw, "height": sh,
                   "exif_orientation": exif_orientation},
        "scale": round(scale, 6),
        "placed_image": {"x": x, "y": y, "width": nw, "height": nh},
        "ground_rgb_hex": "#111318",
        "resample": "Pillow LANCZOS",
        "outputs": {"editorial_frame": "exports/editorial-frame.png", "proof_720p": "evidence/proof-720p.png"},
        "reversal": (f"Crop exports/editorial-frame.png to box ({x},{y},{x + nw},{y + nh}) to recover the "
                     f"whole picture at {nw}x{nh}; the full-resolution original is source/original.jpg."),
        "metadata_note": "EXIF (including any camera location tags) is not written into the PNG exports; the original keeps it unchanged.",
        "pillow": PIL_VERSION,
    }
    RECORD.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(record["placed_image"]), "scale", record["scale"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
