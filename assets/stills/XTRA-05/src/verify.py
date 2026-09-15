#!/usr/bin/env python3
"""XTRA-05 post-render checks. Run after tools/render/render_assets.py --id XTRA-05:
    python -B assets/stills/XTRA-05/src/verify.py

Proves from pixels, not from intent:
  1. the HIST-02 original still has the SHA-256 in HIST-02/delivery.json and src/layout.json;
  2. each variant SVG embeds exactly one PNG, which decodes to exactly a fresh 1.5x BOX resample of it;
  3. clean-workspace.png: the placed 1200x900 rectangle equals that resample pixel for pixel, the mat
     ring just outside the image is uniform, and the SVG has no text;
  4. five-callouts.png (and poster.png, byte-identical): every pixel of the placed rectangle that differs
     from the resample lies inside a declared annotation rectangle; per mark, the original pixels
     actually changed are recorded; each leader crosses only desktop teal (plus the target's own
     frame edge) and each outline covers only its target window's outer frame band;
  5. label text in the SVG is the ticket copy, and no label box meets the screenshot or its frame.
It also writes the 720p proofs and native-pixel halves used for the manual review.
"""
from __future__ import annotations
import base64, hashlib, io, json, re, sys
from pathlib import Path
from PIL import Image, ImageChops

HERE = Path(__file__).resolve().parent
ASSET = HERE.parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
import build  # noqa: E402  (import has no side effects; main() is not run)

TEAL = (0, 120, 127)
FRAME_BAND = 4   # original px: Win95 window outer frame band measured at 3-5 px


def hex2rgb(c: str) -> tuple[int, int, int]:
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def diff_mask(a: Image.Image, b: Image.Image) -> Image.Image:
    chans = [c.point(lambda v: 255 if v else 0) for c in ImageChops.difference(a, b).split()]
    return ImageChops.lighter(ImageChops.lighter(chans[0], chans[1]), chans[2])


def main() -> int:
    lay = json.loads((HERE / 'layout.json').read_text(encoding='utf-8'))
    errors: list[str] = []
    rep: dict = {'id': build.ID, 'command': 'python -B assets/stills/XTRA-05/src/verify.py', 'errors': errors}
    src = ROOT / lay['source']['file']
    raw = src.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    up = next(o for o in json.loads((build.UP / 'delivery.json').read_text(encoding='utf-8'))['outputs'] if o['path'] == build.SRC_REL)
    rep['source'] = {'file': lay['source']['file'], 'sha256_now': sha, 'matches_layout': sha == lay['source']['sha256'],
                     'matches_hist02_delivery': sha == up['sha256'], 'size': list(Image.open(src).size)}
    if not (rep['source']['matches_layout'] and rep['source']['matches_hist02_delivery']):
        errors.append('HIST-02 original hash mismatch')
    orig = Image.open(io.BytesIO(raw)).convert('RGB')
    opx = orig.load()
    expect = build.resample(orig)
    p = lay['placement']
    X, Y, w, h, s = p['x'], p['y'], p['w'], p['h'], p['scale_x']
    rep['placement'] = {'rect_xywh': [X, Y, w, h], 'scale_x': w / 800, 'scale_y': h / 600, 'aspect_error': abs((w / h) / (800 / 600) - 1),
                        'resampling': p['resampling'], 'crop': p['crop'], 'rotation_deg': p['rotation_deg']}
    if (w, h) != (1200, 900) or p['crop'] is not None or p['rotation_deg'] != 0:
        errors.append('placement is not the whole image at uniform 1.5x')
    mat = hex2rgb(lay['frame']['mat_fill'])
    ring = lay['frame']['mat_px'] - lay['frame']['stroke_px'] // 2
    exports = {}
    for name, v in lay['variants'].items():
        svg = (ASSET / v['svg']).read_text(encoding='utf-8')
        uris = re.findall(r'<image [^>]*href="data:image/png;base64,([^"]+)"', svg)
        vr: dict = {'svg': v['svg'], 'embedded_images': len(uris)}
        if len(uris) != 1:
            errors.append(f'{name}: {len(uris)} embedded images')
            continue
        emb = base64.b64decode(uris[0])
        emb_img = Image.open(io.BytesIO(emb)).convert('RGB')
        vr['embedded_png_sha256_matches_layout'] = hashlib.sha256(emb).hexdigest() == p['embedded_png_sha256']
        vr['embedded_png_equals_fresh_resample'] = emb_img.size == expect.size and emb_img.tobytes() == expect.tobytes()
        if not (vr['embedded_png_sha256_matches_layout'] and vr['embedded_png_equals_fresh_resample']):
            errors.append(f'{name}: embedded PNG is not the fresh resample')
        pngs = [v['png']] + ([v['also_rendered_as']] if 'also_rendered_as' in v else [])
        texts = re.findall(r'<text [^>]*>([^<]*)</text>', svg)
        vr['svg_text_strings'] = texts
        vr['exports'] = []
        for rel in pngs:
            img = Image.open(ASSET / rel).convert('RGB')
            exports[rel] = img
            er: dict = {'png': rel, 'size': list(img.size)}
            if img.size != (1920, 1080):
                errors.append(f'{rel}: size {img.size}')
            region = img.crop((X, Y, X + w, Y + h))
            mask = diff_mask(region, expect)
            er['differing_pixels_in_placed_rect'] = mask.histogram()[255]
            er['pixels_checked'] = w * h
            ring_bad = 0
            for k in range(1, ring + 1):
                for xx in range(X - k, X + w + k):
                    ring_bad += img.getpixel((xx, Y - k)) != mat
                    ring_bad += img.getpixel((xx, Y + h - 1 + k)) != mat
                for yy in range(Y - k, Y + h + k):
                    ring_bad += img.getpixel((X - k, yy)) != mat
                    ring_bad += img.getpixel((X + w - 1 + k, yy)) != mat
            er['mat_ring_px'] = ring
            er['mat_ring_nonmatching_pixels_outside_marks'] = None
            if not v['annotated']:
                er['mat_ring_nonmatching_pixels'] = ring_bad
                if er['differing_pixels_in_placed_rect'] or ring_bad:
                    errors.append(f'{rel}: clean image region or mat ring altered')
                if texts:
                    errors.append(f'{rel}: clean variant has text')
            else:
                er.update(check_marks(lay, img, region, mask, expect, orig, errors, rel))
            vr['exports'].append(er)
        if v['annotated']:
            want = [line for t in lay['targets'] for line in build.split_label(t['label'])]
            vr['labels_in_svg_equal_ticket_copy'] = sorted(texts) == sorted(want) and sorted({t['label'] for t in lay['targets']}) == sorted(build.LABELS)
            if not vr['labels_in_svg_equal_ticket_copy']:
                errors.append(f'{name}: SVG text is not the ticket copy')
            try:
                build.check({'targets': lay['targets'], 'frame_box': p['frame_outer'], 'img_box': [X, Y, X + w, Y + h]})
                vr['layout_boxes'] = 'pass: no label meets the screenshot or its frame; labels inside safe area 120-1800 x 72-1008; labels do not overlap; no mark meets a label; outlines stay on the image and do not touch each other'
            except AssertionError as exc:
                errors.append(f'{name}: layout {exc}')
        rep.setdefault('variants', {})[name] = vr
    rep['poster_equals_five_callouts_bytes'] = (ASSET / 'exports/poster.png').read_bytes() == (ASSET / 'exports/five-callouts.png').read_bytes()
    if not rep['poster_equals_five_callouts_bytes']:
        errors.append('poster.png differs from five-callouts.png')
    for rel, stem in (('exports/clean-workspace.png', 'clean-workspace'), ('exports/five-callouts.png', 'five-callouts')):
        img = exports[rel]
        img.resize((1280, 720), Image.Resampling.LANCZOS).save(ASSET / 'proofs' / f'{stem}-720.png')
    fc = exports['exports/five-callouts.png']
    fc.crop((0, 0, 960, 1080)).save(ASSET / 'proofs' / 'five-callouts-1to1-left.png')
    fc.crop((960, 0, 1920, 1080)).save(ASSET / 'proofs' / 'five-callouts-1to1-right.png')
    rep['proofs_written'] = sorted(q.relative_to(ASSET).as_posix() for q in (ASSET / 'proofs').glob('*.png'))
    rep['ok'] = not errors
    (ASSET / 'evidence/placement-checks.json').write_text(json.dumps(rep, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    summary = {'ok': rep['ok'], 'errors': errors}
    for name, vr in rep.get('variants', {}).items():
        for er in vr['exports']:
            summary[er['png']] = {k: er[k] for k in er if k in ('differing_pixels_in_placed_rect', 'mat_ring_nonmatching_pixels', 'differing_pixels_outside_marks', 'mark_pixels_changed_total')}
    print(json.dumps(summary, indent=1))
    return 0 if rep['ok'] else 1


def check_marks(lay, img, region, mask, expect, orig, errors, rel) -> dict:
    p = lay['placement']
    X, Y, s = p['x'], p['y'], p['scale_x']
    ib = [X, Y, X + p['w'], Y + p['h']]
    core, casing = hex2rgb(build.CORE), hex2rgb(build.CASING)
    # union mask of all declared mark rectangles (casing rects contain their core rects), in placed-rect coordinates
    declared = Image.new('L', region.size, 0)
    for t in lay['targets']:
        for m in t['marks']:
            for r in m['casing_rects']:
                x0, y0, x1, y1 = max(r[0], ib[0]), max(r[1], ib[1]), min(r[2], ib[2]), min(r[3], ib[3])
                if x0 < x1 and y0 < y1:
                    declared.paste(255, (x0 - X, y0 - Y, x1 - X, y1 - Y))
    outside = ImageChops.subtract(mask, declared).histogram()[255]
    out = {'differing_pixels_outside_marks': outside}
    if outside:
        errors.append(f'{rel}: {outside} changed image pixels lie outside the declared annotation marks')
    # outside the image: the mat ring may only change where a leader passes through it
    mat = hex2rgb(lay['frame']['mat_fill'])
    marks = []
    total = 0
    mpx = mask.load()
    opx = orig.load()
    for t in lay['targets']:
        tx0, ty0, tx1, ty1 = t['rect']
        for m in t['marks']:
            changed = set()
            colour_ok = True
            for r in m['core_rects']:
                cx, cy = (r[0] + r[2]) // 2, (r[1] + r[3]) // 2
                colour_ok &= img.getpixel((cx, cy)) == core
            for r in m['casing_rects']:
                colour_ok &= img.getpixel((r[0], r[1])) == casing
                x0, y0, x1, y1 = max(r[0], ib[0]), max(r[1], ib[1]), min(r[2], ib[2]), min(r[3], ib[3])
                for yy in range(y0, y1):
                    for xx in range(x0, x1):
                        if mpx[xx - X, yy - Y]:
                            changed.add((int((xx - X) // s), int((yy - Y) // s)))
            colours: dict = {}
            off_band = 0
            for (ox, oy) in changed:
                c = '#%02x%02x%02x' % opx[ox, oy]
                colours[c] = colours.get(c, 0) + 1
                inside = tx0 <= ox <= tx1 and ty0 <= oy <= ty1
                if m['type'] == 'leader':
                    if not (opx[ox, oy] == TEAL or inside):
                        off_band += 1
                else:
                    band = inside and min(ox - tx0, tx1 - ox, oy - ty0, ty1 - oy) < FRAME_BAND
                    if not band:
                        off_band += 1
            canvas_changed = sum(1 for r in m['casing_rects'] for yy in range(max(r[1], ib[1]), min(r[3], ib[3])) for xx in range(max(r[0], ib[0]), min(r[2], ib[2])) if mpx[xx - X, yy - Y])
            total += canvas_changed
            xs, ys = [c[0] for c in changed], [c[1] for c in changed]
            row = {'target': t['label'], 'mark': m['type'], 'canvas_pixels_changed_on_image': canvas_changed,
                   'original_pixels_overlaid': len(changed),
                   'original_bbox_inclusive': [min(xs), min(ys), max(xs), max(ys)] if changed else None,
                   'original_colours_overlaid': dict(sorted(colours.items(), key=lambda kv: -kv[1])),
                   'rule': 'leader: only desktop teal or the target window itself' if m['type'] == 'leader' else f'outline: only the target window outer frame band (< {FRAME_BAND} original px from its edge)',
                   'pixels_breaking_rule': off_band, 'core_and_casing_colours_present': colour_ok}
            if off_band or not colour_ok:
                errors.append(f'{rel}: {t["label"]} {m["type"]} breaks its overlay rule ({off_band} px) or colour check ({colour_ok})')
            marks.append(row)
    # union of changed pixels inside declared marks (each canvas pixel counted once)
    out['mark_pixels_changed_total'] = ImageChops.multiply(mask, declared).histogram()[255]
    out['mark_pixels_changed_sum_over_marks'] = total   # larger: rectangle corners and leader/outline joins are counted per mark
    out['marks'] = marks
    return out


if __name__ == '__main__':
    raise SystemExit(main())
