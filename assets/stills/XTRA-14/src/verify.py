#!/usr/bin/env python3
"""XTRA-14 post-render checks. Run after tools/render/render_assets.py --id XTRA-14:
    python assets/stills/XTRA-14/src/verify.py

For every rendered variant it proves from pixels, not from intent, that each placed screenshot is
the whole upstream original, uniformly scaled, and that nothing was painted over it:
  1. the upstream original still has the SHA-256 recorded in its own delivery.json and src/layout.json;
  2. the PNG embedded in the variant SVG decodes to exactly the resample of that original;
  3. the rectangle x/y/w/h of the export equals that resample pixel for pixel (any overlap,
     crop, shift, rotation or stretch would change at least one pixel);
  4. the placed rectangle has the source aspect ratio (whole-pixel rounding error only);
  5. the 5 px mat ring just outside every image edge is the uniform mat colour (frame drawn outside);
  6. layout boxes: no label/credit/frame intersects any image, all inside the safe area;
  7. every variant showing XTRA-12 has the Microsoft statement in its SVG text;
  8. no year or date-like string appears in on-screen text except the ones listed.
It also writes the 720p proofs for every variant and 1:1 crops of the collage.
"""
from __future__ import annotations
import base64, hashlib, io, json, re, sys
from pathlib import Path
from PIL import Image, ImageChops

HERE = Path(__file__).resolve().parent
ASSET = HERE.parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
import build  # noqa: E402  (module import has no side effects; main() is not run)

DATE = re.compile(r'\b(1[89]\d\d|20\d\d)\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b')


def hex2rgb(c: str) -> tuple[int, int, int]:
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def main() -> int:
    layout = json.loads((HERE / 'layout.json').read_text(encoding='utf-8'))
    mat = hex2rgb(layout['frame']['mat_fill'])
    ring = layout['frame']['mat_px'] - layout['frame']['stroke_px'] // 2   # pure-mat pixels between image edge and stroke
    report = {'id': build.ID, 'command': 'python assets/stills/XTRA-14/src/verify.py', 'variants': {}, 'errors': []}
    originals: dict = {}
    for name, v in layout['variants'].items():
        svg = (ASSET / v['svg']).read_text(encoding='utf-8')
        uris = re.findall(r'<image [^>]*href="data:image/png;base64,([^"]+)"', svg)
        pngs = [ASSET / v['png']] + ([ASSET / v['also_rendered_as']] if 'also_rendered_as' in v else [])
        texts = re.findall(r'<text [^>]*>([^<]*)</text>', svg)
        vrep = {'exports_checked': [p.relative_to(ASSET).as_posix() for p in pngs], 'panels': []}
        exports = [Image.open(p).convert('RGB') for p in pngs]
        for e in exports:
            if e.size != (1920, 1080):
                report['errors'].append(f'{name}: export size {e.size}')
        if len(uris) != len(v['panels']):
            report['errors'].append(f'{name}: {len(uris)} embedded images for {len(v["panels"])} panels')
        for q, uri in zip(v['panels'], uris):
            src = ROOT / q['source_file']
            raw = src.read_bytes()
            sha = hashlib.sha256(raw).hexdigest()
            up = json.loads((ROOT / 'assets/historical' / q['asset'] / 'delivery.json').read_text(encoding='utf-8'))
            up_sha = next(o['sha256'] for o in up['outputs'] if o['path'] == q['source_file'].split(q['asset'] + '/', 1)[1])
            if q['asset'] not in originals:
                originals[q['asset']] = Image.open(io.BytesIO(raw)).convert('RGB')
            expect, method = build.resample(originals[q['asset']], q['w'], q['h'])
            embedded = base64.b64decode(uri)
            emb_img = Image.open(io.BytesIO(embedded)).convert('RGB')
            x, y, w, h = q['x'], q['y'], q['w'], q['h']
            per_export = []
            for e in exports:
                region = e.crop((x, y, x + w, y + h))
                if region.tobytes() == expect.tobytes():
                    diff = 0
                else:   # count pixels where any channel differs
                    chans = [c.point(lambda v: 255 if v else 0) for c in ImageChops.difference(region, expect).split()]
                    diff = ImageChops.lighter(ImageChops.lighter(chans[0], chans[1]), chans[2]).histogram()[255]
                ring_bad = 0
                for k in range(1, ring + 1):
                    for xx in range(x - k, x + w + k):
                        ring_bad += e.getpixel((xx, y - k)) != mat
                        ring_bad += e.getpixel((xx, y + h - 1 + k)) != mat
                    for yy in range(y - k, y + h + k):
                        ring_bad += e.getpixel((x - k, yy)) != mat
                        ring_bad += e.getpixel((x + w - 1 + k, yy)) != mat
                per_export.append({'differing_pixels_in_placed_rect': diff, 'pixels_checked': w * h, 'mat_ring_px': ring, 'mat_ring_nonmatching_pixels': ring_bad})
            sw, sh = q['source_size']
            rel = abs((w / h) / (sw / sh) - 1)
            row = {'asset': q['asset'], 'label': q['label'], 'role': q['role'], 'source_file': q['source_file'],
                   'source_sha256_now': sha, 'matches_layout': sha == q['source_sha256'], 'matches_upstream_delivery': sha == up_sha,
                   'placed_rect_xywh': [x, y, w, h], 'source_size': [sw, sh], 'scale_x': w / sw, 'scale_y': h / sh,
                   'aspect_rel_error': rel, 'aspect_max_rounding_px': abs(w - h * sw / sh), 'resampling': method,
                   'embedded_png_sha256_matches_layout': hashlib.sha256(embedded).hexdigest() == q['embedded_png_sha256'],
                   'embedded_png_equals_resample': emb_img.size == expect.size and emb_img.tobytes() == expect.tobytes(),
                   'exports': per_export}
            ok = (row['matches_layout'] and row['matches_upstream_delivery'] and row['embedded_png_sha256_matches_layout'] and row['embedded_png_equals_resample']
                  and all(p['differing_pixels_in_placed_rect'] == 0 and p['mat_ring_nonmatching_pixels'] == 0 for p in per_export)
                  and row['aspect_max_rounding_px'] <= 0.5 and q['crop'] is None and q['rotation_deg'] == 0)
            row['pass'] = ok
            if not ok:
                report['errors'].append(f'{name}: {q["asset"]} placement check failed')
            vrep['panels'].append(row)
        try:
            build.check([dict(q, texts=q['texts']) for q in v['panels']])
            vrep['layout_boxes'] = 'pass: no label, credit or frame intersects any image; no text intersects text; all frames and text inside safe area 120-1800 x 72-1008'
        except AssertionError as exc:
            report['errors'].append(f'{name}: layout {exc}')
        has12 = any(q['asset'] == 'XTRA-12' for q in v['panels'])
        vrep['microsoft_statement_in_svg_text'] = (build.MS_STATEMENT in texts) if has12 else None
        if has12 and build.MS_STATEMENT not in texts:
            report['errors'].append(f'{name}: Microsoft statement missing')
        vrep['labels_in_svg_text'] = [t for t in texts if t in build.LABELS]
        vrep['date_like_strings_in_on_screen_text'] = sorted({m.group(0) for t in texts for m in DATE.finditer(t)})
        report['variants'][name] = vrep
        img = exports[0]
        img.resize((1280, 720), Image.Resampling.LANCZOS).save(ASSET / 'proofs' / f'{name}-720.png')
        if name == 'collage':
            img.crop((0, 0, 960, 1080)).save(ASSET / 'proofs' / 'collage-1to1-left.png')
            img.crop((960, 0, 1920, 1080)).save(ASSET / 'proofs' / 'collage-1to1-right.png')
    poster, collage = (ASSET / 'exports/poster.png').read_bytes(), (ASSET / 'exports/collage.png').read_bytes()
    report['poster_equals_collage_bytes'] = poster == collage
    report['proofs_written'] = sorted(p.relative_to(ASSET).as_posix() for p in (ASSET / 'proofs').glob('*.png'))
    report['ok'] = not report['errors']
    (ASSET / 'evidence/placement-checks.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'ok': report['ok'], 'errors': report['errors'], 'dates': {n: v['date_like_strings_in_on_screen_text'] for n, v in report['variants'].items()},
                      'diffs': {n: [(p['asset'], [e['differing_pixels_in_placed_rect'] for e in p['exports']], [e['mat_ring_nonmatching_pixels'] for e in p['exports']]) for p in v['panels']] for n, v in report['variants'].items()}}, indent=1))
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
