#!/usr/bin/env python3
"""HIST-06: place the untouched Commons original on the 1920x1080 editorial canvas.

The original is enlarged by an exact integer factor with nearest-neighbour sampling
(every source pixel becomes a uniform 2x2 block), centred on a plain canvas, and never
cropped, recoloured, or annotated. The script verifies that the framed pixels map back
to the original exactly, then writes the export, a 720p review proof, and framing.json.
"""
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parents[1]
ORIGINAL = BASE / 'source' / 'original.png'
EXPECTED_SHA256 = '69df4c7f0b3e4271f12311bc0e06e5d61cadffee4b2870875d2034a7cf6bda4e'
CANVAS = (1920, 1080)
BACKGROUND = (0x11, 0x13, 0x18)  # production-bible dark code background
SAFE_AREA = (120, 72, 1800, 1008)
SCALE = 2


def main() -> int:
    data = ORIGINAL.read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        print('source/original.png does not match the acquired file; refusing to frame.', file=sys.stderr)
        return 1
    src = Image.open(ORIGINAL)
    src.load()
    if src.mode == 'RGBA' and src.getchannel('A').getextrema() != (255, 255):
        print('Original has transparency; framing rule does not cover it.', file=sys.stderr)
        return 1
    rgb = src.convert('RGB')
    big = rgb.resize((rgb.width * SCALE, rgb.height * SCALE), Image.NEAREST)
    x = (CANVAS[0] - big.width) // 2
    y = (CANVAS[1] - big.height) // 2
    if not (SAFE_AREA[0] <= x and x + big.width <= SAFE_AREA[2] and SAFE_AREA[1] <= y and y + big.height <= SAFE_AREA[3]):
        print('Enlarged original would leave the safe area.', file=sys.stderr)
        return 1
    canvas = Image.new('RGB', CANVAS, BACKGROUND)
    canvas.paste(big, (x, y))

    # Reversibility: every 2x2 block inside the placed rectangle equals its source pixel.
    placed = canvas.crop((x, y, x + big.width, y + big.height))
    src_px = rgb.load()
    out_px = placed.load()
    for j in range(rgb.height):
        for i in range(rgb.width):
            p = src_px[i, j]
            for dj in range(SCALE):
                for di in range(SCALE):
                    if out_px[i * SCALE + di, j * SCALE + dj] != p:
                        print(f'Framed pixel mismatch at source ({i},{j}).', file=sys.stderr)
                        return 1

    (BASE / 'exports').mkdir(exist_ok=True)
    (BASE / 'proofs').mkdir(exist_ok=True)
    canvas.save(BASE / 'exports' / 'editorial-frame.png', optimize=True)
    canvas.resize((1280, 720), Image.LANCZOS).save(BASE / 'proofs' / 'editorial-frame-720.png', optimize=True)

    framing = {
        'id': 'HIST-06',
        'canvas': list(CANVAS),
        'background': '#111318',
        'safe_area': list(SAFE_AREA),
        'rule': 'Untouched original enlarged by an integer factor with nearest-neighbour sampling, centred, no crop, no annotation, no added UI.',
        'exports': [
            {
                'file': 'exports/editorial-frame.png',
                'from': 'source/original.png',
                'from_sha256': EXPECTED_SHA256,
                'source_size': [rgb.width, rgb.height],
                'scale': SCALE,
                'resampling': 'nearest',
                'placed_size': [big.width, big.height],
                'offset': [x, y],
                'crop': None,
                'alpha': 'source alpha channel is fully opaque (255 everywhere); flattened to RGB',
                'pixels_inside_original_modified': False,
                'reverse': f'crop ({x},{y})-({x + big.width},{y + big.height}), then downsample by {SCALE} with nearest-neighbour sampling to {rgb.width}x{rgb.height} to recover the RGB original exactly',
                'reversibility_check': 'passed (every block compared in this script)',
            },
            {
                'file': 'proofs/editorial-frame-720.png',
                'from': 'exports/editorial-frame.png',
                'scale': 'resize to 1280x720, Lanczos',
                'purpose': '720p review proof only; not a delivery variant',
            },
        ],
    }
    (BASE / 'evidence' / 'framing.json').write_text(json.dumps(framing, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(f'framed at offset ({x},{y}) scale {SCALE}; reversibility check passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
