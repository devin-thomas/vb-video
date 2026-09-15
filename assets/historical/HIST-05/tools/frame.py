"""Reversible 16:9 editorial framing of an archival still.

Integer nearest-neighbour upscale (no resampling blur, no stretch), centred on a flat
pillarbox/letterbox. No crop, no retouch, no added text or UI. Writes the exact
transform to a JSON record so the original pixel grid can be recovered.

usage: python frame.py INPUT OUTPUT_PNG RECORD_JSON [--frame N] [--bg #RRGGBB] [--max-h 936]
"""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageSequence
import PIL

W, H = 1920, 1080


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("record")
    ap.add_argument("--frame", type=int, default=0)
    ap.add_argument("--bg", default="#000000")
    ap.add_argument("--max-h", type=int, default=936, help="keep inside the y=72..1008 safe band")
    a = ap.parse_args()

    src = Image.open(a.input)
    frames = [f.copy() for f in ImageSequence.Iterator(src)]
    img = frames[a.frame].convert("RGB")
    w, h = img.size
    scale = max(1, min((1800 - 120) // w, a.max_h // h))
    sw, sh = w * scale, h * scale
    scaled = img.resize((sw, sh), Image.NEAREST)
    canvas = Image.new("RGB", (W, H), a.bg)
    x, y = (W - sw) // 2, (H - sh) // 2
    canvas.paste(scaled, (x, y))
    canvas.save(a.output, format="PNG", optimize=True)

    inp = Path(a.input).read_bytes()
    record = {
        "input": Path(a.input).name,
        "input_sha256": hashlib.sha256(inp).hexdigest(),
        "input_format": src.format,
        "input_size": [w, h],
        "input_frame_count": len(frames),
        "frame_used": a.frame,
        "crop": None,
        "scale": scale,
        "resample": "nearest",
        "scaled_size": [sw, sh],
        "placement": {"x": x, "y": y},
        "canvas": [W, H],
        "background": a.bg,
        "added_elements": [],
        "reverse": f"crop box ({x},{y},{x + sw},{y + sh}) then downscale by {scale} with nearest to recover frame {a.frame}",
        "pillow": PIL.__version__,
    }
    Path(a.record).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
