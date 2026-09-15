#!/usr/bin/env python3
"""XTRA-05 post-render checks. Run after tools/render/render_assets.py --id XTRA-05:
    python -B assets/stills/XTRA-05/src/verify.py --id XTRA-05

Proves from pixels, not from intent:
  1. the HIST-02 original still has the SHA-256 in HIST-02/delivery.json and src/layout.json;
  2. each variant SVG embeds exactly one PNG per declared placement, which decodes to exactly a fresh
     resample at that placement's scale (1.5x BOX, or the native 1.0x identity; at 1.0x the embedded
     bytes must also be the HIST-02 file itself);
  3. every clean placement (clean-workspace; the left screenshot of side-by-side) equals that resample
     pixel for pixel, and the mat ring just outside it is uniform;
  4. every annotated placement (five-callouts; the right screenshot of side-by-side): each pixel that
     differs from the resample lies inside a declared mark rectangle; per mark, the original pixels
     actually changed are recorded; each leader crosses only desktop teal (plus the target's own
     frame edge); each outline covers only its target window's outer frame band; the mat ring changes
     only where a declared mark crosses it;
  5. a gold audit over the whole export: every #eab676 pixel lies in a declared gold core rectangle,
     and every declared core pixel is gold (so nothing gold lands on the clean screenshot);
  6. SVG label text equals the War/SCRIPT.md cue labels, the stored layout passes the build's
     no-overlap checks, and poster.png is byte-identical to the chosen poster variant.
It also writes the 720p proofs and native-pixel halves used for the manual review.
"""
from __future__ import annotations
import argparse, base64, hashlib, io, json, re, sys
from pathlib import Path
from PIL import Image, ImageChops

HERE = Path(__file__).resolve().parent
ASSET = HERE.parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
import build  # noqa: E402  (import reads the script cue and has no other side effects; main() is not run)

TEAL = (0, 120, 127)
FRAME_BAND = 4   # original px: Win95 window outer frame band (offsets 0-3 are frame colours; offset 4 can be title bar or content)


def hex2rgb(c: str) -> tuple[int, int, int]:
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def diff_mask(a: Image.Image, b: Image.Image) -> Image.Image:
    chans = [c.point(lambda v: 255 if v else 0) for c in ImageChops.difference(a, b).split()]
    return ImageChops.lighter(ImageChops.lighter(chans[0], chans[1]), chans[2])


def colour_mask(img: Image.Image, rgb: tuple[int, int, int]) -> Image.Image:
    return diff_mask(img, Image.new('RGB', img.size, rgb)).point(lambda v: 0 if v else 255)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--id', default=build.ID)
    args = ap.parse_args()
    assert args.id == build.ID, f'this verifier belongs to {build.ID}'
    lay = json.loads((HERE / 'layout.json').read_text(encoding='utf-8'))
    errors: list[str] = []
    rep: dict = {'id': build.ID, 'command': 'python -B assets/stills/XTRA-05/src/verify.py --id XTRA-05', 'errors': errors}
    src = ROOT / lay['source']['file']
    raw = src.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    up = next(o for o in json.loads((build.UP / 'delivery.json').read_text(encoding='utf-8'))['outputs'] if o['path'] == build.SRC_REL)
    rep['source'] = {'file': lay['source']['file'], 'sha256_now': sha, 'matches_layout': sha == lay['source']['sha256'],
                     'matches_hist02_delivery': sha == up['sha256'], 'size': list(Image.open(src).size)}
    if not (rep['source']['matches_layout'] and rep['source']['matches_hist02_delivery']):
        errors.append('HIST-02 original hash mismatch')
    orig = Image.open(io.BytesIO(raw)).convert('RGB')
    rep['labels'] = {'authority': f"{lay['labels']['path']}:{lay['labels']['line']}", 'layout_labels': lay['labels']['labels_in_cue_order'],
                     'cue_labels_now': build.LABELS, 'cue_unchanged_since_build': lay['labels']['labels_in_cue_order'] == build.LABELS}
    if not rep['labels']['cue_unchanged_since_build']:
        errors.append('War/SCRIPT.md cue labels changed since build.py ran; rebuild')
    mat = hex2rgb(lay['frame']['mat_fill'])
    ring = lay['frame']['mat_px'] - lay['frame']['stroke_px'] // 2
    exports = {}
    expected_cache: dict = {}

    def expected(num: int, den: int) -> Image.Image:
        if (num, den) not in expected_cache:
            expected_cache[(num, den)] = build.resample(orig, num, den)
        return expected_cache[(num, den)]

    for name, v in lay['variants'].items():
        svg = (ASSET / v['svg']).read_text(encoding='utf-8')
        uris = re.findall(r'<image [^>]*href="data:image/png;base64,([^"]+)"', svg)
        vr: dict = {'svg': v['svg'], 'embedded_images': len(uris), 'declared_placements': len(v['images']), 'images': []}
        if len(uris) != len(v['images']):
            errors.append(f'{name}: {len(uris)} embedded images for {len(v["images"])} placements')
            rep.setdefault('variants', {})[name] = vr
            continue
        targets = lay[v['targets']] if v['targets'] else []
        for im, uri in zip(v['images'], uris):
            emb = base64.b64decode(uri)
            exp = expected(im['scale_num'], im['scale_den'])
            emb_img = Image.open(io.BytesIO(emb)).convert('RGB')
            ir = {'role': im['role'], 'rect_xywh': [im['x'], im['y'], im['w'], im['h']], 'scale_x': im['w'] / 800, 'scale_y': im['h'] / 600,
                  'aspect_error': abs((im['w'] / im['h']) / (800 / 600) - 1), 'resampling': im['resampling'], 'crop': im['crop'], 'rotation_deg': im['rotation_deg'],
                  'embedded_png_sha256_matches_layout': hashlib.sha256(emb).hexdigest() == im['embedded_png_sha256'],
                  'embedded_png_equals_fresh_resample': emb_img.size == exp.size and emb_img.tobytes() == exp.tobytes()}
            if im['scale_num'] == im['scale_den']:
                ir['embedded_png_is_hist02_original_bytes'] = hashlib.sha256(emb).hexdigest() == lay['source']['sha256']
                if not ir['embedded_png_is_hist02_original_bytes']:
                    errors.append(f'{name} {im["role"]}: 1.0x embed is not the HIST-02 file')
            if not (ir['embedded_png_sha256_matches_layout'] and ir['embedded_png_equals_fresh_resample']):
                errors.append(f'{name} {im["role"]}: embedded PNG is not the fresh resample')
            if (im['w'], im['h']) != exp.size or im['crop'] is not None or im['rotation_deg'] != 0 or ir['aspect_error'] > 1e-12:
                errors.append(f'{name} {im["role"]}: placement is not the whole image at a uniform scale')
            vr['images'].append(ir)
        texts = re.findall(r'<text [^>]*>([^<]*)</text>', svg)
        vr['svg_text_strings'] = texts
        pngs = [v['png']] + ([v['also_rendered_as']] if 'also_rendered_as' in v else [])
        vr['exports'] = []
        for rel in pngs:
            img = Image.open(ASSET / rel).convert('RGB')
            exports[rel] = img
            er: dict = {'png': rel, 'size': list(img.size), 'placements': []}
            if img.size != (1920, 1080):
                errors.append(f'{rel}: size {img.size}')
            for im in v['images']:
                X, Y, w, h = im['x'], im['y'], im['w'], im['h']
                exp = expected(im['scale_num'], im['scale_den'])
                region = img.crop((X, Y, X + w, Y + h))
                mask = diff_mask(region, exp)
                pr: dict = {'role': im['role'], 'differing_pixels_in_placed_rect': mask.histogram()[255], 'pixels_checked': w * h, 'mat_ring_px': ring}
                rects = [r for t in targets for m in t['marks'] for r in m['casing_rects']] if im['annotated'] else []
                ring_bad = ring_bad_outside = 0
                for k in range(1, ring + 1):
                    pts = [(xx, Y - k) for xx in range(X - k, X + w + k)] + [(xx, Y + h - 1 + k) for xx in range(X - k, X + w + k)] + \
                          [(X - k, yy) for yy in range(Y - k, Y + h + k)] + [(X + w - 1 + k, yy) for yy in range(Y - k, Y + h + k)]
                    for (xx, yy) in pts:
                        if img.getpixel((xx, yy)) != mat:
                            ring_bad += 1
                            if not any(r[0] <= xx < r[2] and r[1] <= yy < r[3] for r in rects):
                                ring_bad_outside += 1
                if not im['annotated']:
                    pr['mat_ring_nonmatching_pixels'] = ring_bad
                    if pr['differing_pixels_in_placed_rect'] or ring_bad:
                        errors.append(f'{rel} {im["role"]}: clean image region or mat ring altered')
                else:
                    pr['mat_ring_nonmatching_pixels_outside_marks'] = ring_bad_outside
                    if ring_bad_outside:
                        errors.append(f'{rel} {im["role"]}: {ring_bad_outside} mat ring pixels changed outside declared marks')
                    pr.update(check_marks(targets, im, img, region, mask, orig, errors, f'{rel} {im["role"]}'))
                er['placements'].append(pr)
            er['gold_audit'] = gold_audit(img, targets, [im for im in v['images'] if not im['annotated']], errors, rel)
            if not v['annotated'] and texts:
                errors.append(f'{rel}: clean variant has text')
            vr['exports'].append(er)
        if v['annotated']:
            want = [line for t in targets for line in (build.split_label(t['label']) if v['label_lines'] == 'split' else [t['label']])]
            vr['labels_in_svg_equal_script_cue'] = sorted(texts) == sorted(want) and sorted({t['label'] for t in targets}) == sorted(build.LABELS)
            if not vr['labels_in_svg_equal_script_cue']:
                errors.append(f'{name}: SVG text is not the War/SCRIPT.md cue labels')
            try:
                if name == 'side-by-side':
                    sbs = lay['side_by_side']
                    res = build.check_sbs({'clean': sbs['clean'], 'annotated': sbs['annotated'], 'targets': targets})
                    vr['layout_boxes'] = ('pass: clean and annotated frames do not overlap (gap %d px) and sit inside the safe area; no label meets either screenshot or frame; '
                                          'labels inside 120-1800 x 72-1008 and not overlapping; no mark meets the clean screenshot or its frame, a label, or another target\'s mark; '
                                          'outlines stay on the annotated screenshot' % res['gap_between_frames_px'])
                else:
                    p = lay['placement']
                    build.check({'targets': targets, 'frame_box': p['frame_outer'], 'img_box': [p['x'], p['y'], p['x'] + p['w'], p['y'] + p['h']]})
                    vr['layout_boxes'] = 'pass: no label meets the screenshot or its frame; labels inside safe area 120-1800 x 72-1008; labels do not overlap; no mark meets a label; outlines stay on the image and do not touch each other'
            except AssertionError as exc:
                errors.append(f'{name}: layout {exc}')
        rep.setdefault('variants', {})[name] = vr
    poster = lay['poster']
    rep['poster'] = poster
    rep['poster_equals_variant_bytes'] = (ASSET / 'exports/poster.png').read_bytes() == (ASSET / lay['variants'][poster]['png']).read_bytes()
    if not rep['poster_equals_variant_bytes']:
        errors.append(f'poster.png differs from {poster}.png')
    for name, v in lay['variants'].items():
        exports[v['png']].resize((1280, 720), Image.Resampling.LANCZOS).save(ASSET / 'proofs' / f'{name}-720.png')
    for name in ('five-callouts', 'side-by-side'):
        img = exports[lay['variants'][name]['png']]
        img.crop((0, 0, 960, 1080)).save(ASSET / 'proofs' / f'{name}-1to1-left.png')
        img.crop((960, 0, 1920, 1080)).save(ASSET / 'proofs' / f'{name}-1to1-right.png')
    rep['proofs_written'] = sorted(q.relative_to(ASSET).as_posix() for q in (ASSET / 'proofs').glob('*.png'))
    rep['ok'] = not errors
    (ASSET / 'evidence/placement-checks.json').write_text(json.dumps(rep, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    summary: dict = {'ok': rep['ok'], 'errors': errors, 'poster': poster, 'poster_equals_variant_bytes': rep['poster_equals_variant_bytes']}
    for name, vr in rep.get('variants', {}).items():
        for er in vr.get('exports', []):
            summary[er['png']] = {'placements': [{k: pr[k] for k in pr if k in ('role', 'differing_pixels_in_placed_rect', 'mat_ring_nonmatching_pixels',
                                                                              'mat_ring_nonmatching_pixels_outside_marks', 'differing_pixels_outside_marks', 'mark_pixels_changed_total')}
                                                 for pr in er['placements']],
                                  'gold': {k: er['gold_audit'][k] for k in ('gold_pixels_total', 'gold_pixels_outside_declared_cores', 'declared_core_pixels_not_gold', 'gold_pixels_on_clean_placements')}}
        if 'layout_boxes' in vr:
            summary[name + ' layout'] = vr['layout_boxes']
    print(json.dumps(summary, indent=1))
    return 0 if rep['ok'] else 1


def gold_audit(img, targets, clean_images, errors, rel) -> dict:
    gold = colour_mask(img, hex2rgb(build.CORE))
    cores = Image.new('L', img.size, 0)
    for t in targets:
        for m in t['marks']:
            for r in m['core_rects']:
                cores.paste(255, (r[0], r[1], r[2], r[3]))
    on_clean = 0
    for im in clean_images:
        fb = im['frame_outer']
        on_clean += gold.crop((fb[0], fb[1], fb[2], fb[3])).histogram()[255]
    out = {'gold': build.CORE, 'gold_pixels_total': gold.histogram()[255],
           'declared_core_pixels': cores.histogram()[255],
           'gold_pixels_outside_declared_cores': ImageChops.subtract(gold, cores).histogram()[255],
           'declared_core_pixels_not_gold': ImageChops.subtract(cores, gold).histogram()[255],
           'gold_pixels_on_clean_placements': on_clean}
    if out['gold_pixels_outside_declared_cores'] or out['declared_core_pixels_not_gold'] or on_clean:
        errors.append(f'{rel}: gold audit failed {out}')
    return out


def check_marks(targets, im, img, region, mask, orig, errors, tag) -> dict:
    X, Y, s = im['x'], im['y'], im['w'] / 800
    ib = [X, Y, X + im['w'], Y + im['h']]
    core, casing = hex2rgb(build.CORE), hex2rgb(build.CASING)
    declared = Image.new('L', region.size, 0)   # union of declared mark rectangles, in placed-rect coordinates
    for t in targets:
        for m in t['marks']:
            for r in m['casing_rects']:
                x0, y0, x1, y1 = max(r[0], ib[0]), max(r[1], ib[1]), min(r[2], ib[2]), min(r[3], ib[3])
                if x0 < x1 and y0 < y1:
                    declared.paste(255, (x0 - X, y0 - Y, x1 - X, y1 - Y))
    outside = ImageChops.subtract(mask, declared).histogram()[255]
    out: dict = {'differing_pixels_outside_marks': outside}
    if outside:
        errors.append(f'{tag}: {outside} changed image pixels lie outside the declared annotation marks')
    marks = []
    total = 0
    mpx = mask.load()
    opx = orig.load()
    for t in targets:
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
                errors.append(f'{tag}: {t["label"]} {m["type"]} breaks its overlay rule ({off_band} px) or colour check ({colour_ok})')
            marks.append(row)
    out['mark_pixels_changed_total'] = ImageChops.multiply(mask, declared).histogram()[255]
    out['mark_pixels_changed_sum_over_marks'] = total   # larger: rectangle corners and leader/outline joins are counted per mark
    out['marks'] = marks
    return out


if __name__ == '__main__':
    raise SystemExit(main())
