#!/usr/bin/env python3
"""XTRA-09 editorial frame: fit source/original.jpg inside the shared safe area without stretching.

Reversible and non-destructive: reads source/original.jpg (never modified), writes
exports/editorial-frame.png (1920x1080) and proofs/editorial-frame-720.png (1280x720).
Uniform scale only (aspect preserved), no crop, no retouch, no burned-in text.
Run from the repository root:  python assets/historical/XTRA-09/src/make_frame.py
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from PIL import Image

BASE = Path(__file__).resolve().parents[1]
W, H = 1920, 1080
SAFE = (120, 72, 1800, 1008)  # x0, y0, x1, y1 from docs/PRODUCTION_BIBLE.md
BACKGROUND = (17, 19, 24)  # #111318, bible dark background token


def main() -> None:
    src = BASE / 'source/original.jpg'
    before = hashlib.sha256(src.read_bytes()).hexdigest()
    im = Image.open(src)
    im.load()
    ow, oh = im.size
    sw, sh = SAFE[2] - SAFE[0], SAFE[3] - SAFE[1]
    scale = min(sw / ow, sh / oh)
    nw, nh = round(ow * scale), round(oh * scale)
    fitted = im.convert('RGB').resize((nw, nh), Image.Resampling.LANCZOS)
    x = SAFE[0] + (sw - nw) // 2
    y = SAFE[1] + (sh - nh) // 2
    canvas = Image.new('RGB', (W, H), BACKGROUND)
    canvas.paste(fitted, (x, y))
    (BASE / 'exports').mkdir(exist_ok=True)
    (BASE / 'proofs').mkdir(exist_ok=True)
    canvas.save(BASE / 'exports/editorial-frame.png', optimize=True)
    canvas.resize((1280, 720), Image.Resampling.LANCZOS).save(BASE / 'proofs/editorial-frame-720.png', optimize=True)
    after = hashlib.sha256(src.read_bytes()).hexdigest()
    assert before == after, 'source/original.jpg changed during framing'
    record = {
        'input': 'source/original.jpg',
        'input_sha256': before,
        'input_size': [ow, oh],
        'canvas': [W, H],
        'safe_area': list(SAFE),
        'background': '#111318',
        'uniform_scale': scale,
        'scaled_size': [nw, nh],
        'offset': [x, y],
        'aspect_in': ow / oh,
        'aspect_out': nw / nh,
        'resample': 'LANCZOS',
        'crop': None,
        'retouch': None,
        'burned_text': None,
        'outputs': ['exports/editorial-frame.png', 'proofs/editorial-frame-720.png'],
    }
    (BASE / 'evidence/framing.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
