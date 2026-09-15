"""HIST-18 framing: build the two 1920x1080 named variants from the uncropped 2x capture.

  exports/original.png         whole uncropped page, uniformly scaled to fit (no crop, no stretch)
  exports/editorial-frame.png  reversible top-of-page crop (CSS px box below), uniformly scaled

Both sit on a flat neutral ground with one authored source line in the lower title-safe margin.
Nothing inside the archived page pixels is retouched, removed, or added. Every transform is written to
evidence/transforms.json so the crop can be reversed against source/raw/capture-800w-2x.png.

Run from the repository root:  python assets/historical/HIST-18/src/frame.py
Font: Segoe UI from the installed Windows font directory (not bundled).
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

A = Path(__file__).resolve().parents[1]
W, H = 1920, 1080
SAFE_TOP, SAFE_BOTTOM = 54, 1026          # 90% title-safe band (5% top/bottom)
IMAGE_BOTTOM = 976                         # image box ends here; caption sits below inside title-safe
BG = (32, 34, 37)
FG = (222, 222, 222)
CSS_WIDTH = 800                            # capture viewport width in CSS px
EDITORIAL_CROP_CSS = (0, 0, 800, 706)      # banner ad, logo, navigation, categories, highlights, special-offer bar;
                                           # ends just below the special-offer bar, above the sidebar 'search yahoo' label
CAPTION = 'download.com front page \u2014 Internet Archive Wayback Machine capture, 21 Dec 1996'
FONT = 'C:/Windows/Fonts/segoeui.ttf'


def place(src, box_css, out_name, label, scale_css):
    k = src.width / CSS_WIDTH                               # device pixels per CSS px in the capture
    box_px = tuple(round(v * k) for v in box_css)
    crop = src.crop(box_px)
    avail_h = IMAGE_BOTTOM - SAFE_TOP
    s = avail_h / crop.height
    size = (round(crop.width * s), avail_h)
    scaled = crop.resize(size, Image.LANCZOS)
    canvas = Image.new('RGB', (W, H), BG)
    x = (W - size[0]) // 2
    canvas.paste(scaled, (x, SAFE_TOP))
    d = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT, 28)
    tw = d.textlength(label, font=font)
    d.text(((W - tw) / 2, SAFE_TOP + avail_h + 14), label, font=font, fill=FG)
    canvas.save(A / 'exports' / out_name, optimize=True)
    return {'output': f'exports/{out_name}', 'source': 'source/raw/capture-800w-2x.png',
            'source_size_px': [src.width, src.height], 'crop_css_px': list(box_css), 'crop_device_px': list(box_px),
            'uniform_scale_from_device_px': round(s, 6), 'effective_scale_from_css_px': round(s * k, 6),
            'placed_size_px': list(size), 'placed_at_px': [x, SAFE_TOP], 'background_rgb': list(BG),
            'authored_caption': label, 'caption_font': 'Segoe UI 28 px (system)',
            'reverse': 'crop exports image at placed_at/placed_size, resize by 1/uniform_scale, '
                       'compare with source crop_device_px'}


def main():
    src = Image.open(A / 'source/raw/capture-800w-2x.png').convert('RGB')
    full_css = (0, 0, CSS_WIDTH, round(src.height / (src.width / CSS_WIDTH)))
    records = [
        place(src, full_css, 'original.png', CAPTION + ' (uncropped)', None),
        place(src, EDITORIAL_CROP_CSS, 'editorial-frame.png', CAPTION, None),
    ]
    (A / 'evidence/transforms.json').write_text(json.dumps(records, indent=1) + '\n', encoding='utf-8')
    print(json.dumps(records, indent=1))


if __name__ == '__main__':
    main()
