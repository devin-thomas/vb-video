#!/usr/bin/env python3
"""XTRA-14 authoring script: three-panel real-world VB application collage.

Run from the repository root:  python assets/stills/XTRA-14/src/build.py
It writes this ticket's editable sources only: one SVG per named variant (the uniformly scaled
screenshots are embedded as PNG data: URIs so CairoSVG and the in-memory browser check need no
file access), offline HTML, timeline, build driver, exact copy, and src/layout.json, the map from
collage coordinates to each upstream source file. Rendering, browser checks and delivery finishing
use tools/render with --id XTRA-14; src/verify.py then checks the rendered pixels against
src/layout.json. build_assets.py has no XTRA-14 composition, so this script replaces it here.

Upstream originals are read in place (assets/historical/XTRA-11..13/source/original.*) and never
written or copied. Each one's SHA-256 must equal the value in that upstream delivery.json or the
build stops. Every image is placed whole: no crop, rotation, overlap, or aspect change.
"""
from __future__ import annotations
import base64, hashlib, html, io, json, math, sys
from pathlib import Path
from PIL import Image, ImageFont

HERE = Path(__file__).resolve().parent
ASSET = HERE.parent
ROOT = HERE.parents[3]   # src -> XTRA-14 -> stills -> assets -> repository root
sys.path.insert(0, str(ROOT / 'tools' / 'render'))
from studio import SVG, BG, PANEL, FG, MUTED, LINE, FONT_PATHS, width, wrap  # noqa: E402

ID = 'XTRA-14'
ROW = next(r for r in json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))['tickets'] if r['id'] == ID)
LABELS = ROW['copy'].split(' · ')   # exact ticket copy, one label per panel
assert len(LABELS) == 3 and ' · '.join(LABELS) == ROW['copy'], 'panel labels must be the exact ticket copy'

W, H = 1920, 1080
SAFE = (120, 72, 1800, 1008)
PAD, STROKE = 6, 2           # mat between image edge and frame stroke; stroke is centred on the mat edge
OUT = PAD + STROKE // 2      # frame extent outside every image edge (7 px); the image itself is never covered
LABEL_PX, SMALL_LABEL_PX, CREDIT_PX, LEAD = 40, 32, 26, 1.25
LABEL_GAP, CREDIT_GAP = 16, 18
MS_STATEMENT = 'Used with permission from Microsoft.'

PANELS = [
    {'key': 'business', 'label': LABELS[0], 'asset': 'XTRA-11', 'file': 'source/original.jpg'},
    {'key': 'data-entry', 'label': LABELS[1], 'asset': 'XTRA-12', 'file': 'source/original.gif'},
    {'key': 'utilities', 'label': LABELS[2], 'asset': 'XTRA-13', 'file': 'source/original.gif'},
]

_fonts: dict = {}


def metrics(size: int, bold: bool) -> tuple[int, int]:
    key = (size, bold)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONT_PATHS['bold' if bold else 'sans'], size)
    return _fonts[key].getmetrics()   # (ascent, descent), conservative line box


def load_panels() -> list[dict]:
    out = []
    for spec in PANELS:
        p = dict(spec)
        up = ROOT / 'assets' / 'historical' / p['asset']
        raw = (up / p['file']).read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        recorded = next(o for o in json.loads((up / 'delivery.json').read_text(encoding='utf-8'))['outputs'] if o['path'] == p['file'])
        assert sha == recorded['sha256'] and len(raw) == recorded['bytes'], f"{p['asset']} original differs from its delivery.json record"
        img = Image.open(io.BytesIO(raw))
        img.load()
        assert getattr(img, 'n_frames', 1) == 1, 'single-frame source expected'
        rgba = img.convert('RGBA')
        assert rgba.getextrema()[3] == (255, 255), 'opaque source expected (a transparent pixel would let the mat show through)'
        rights = json.loads((up / 'evidence/rights.json').read_text(encoding='utf-8'))
        p.update(path=f"assets/historical/{p['asset']}/{p['file']}", rel_path=f"../../historical/{p['asset']}/{p['file']}",
                 sha256=sha, bytes=len(raw), size=list(img.size), mode=img.mode, image=img.convert('RGB'), rights=rights)
        p.update(screen_credit(p))
        out.append(p)
    return out


def screen_credit(p: dict) -> dict:
    """On-screen credit derived from the upstream rights record; any edit is asserted and recorded."""
    r = p['rights']
    if p['asset'] == 'XTRA-11':
        full, field = r['credit_text'], 'credit_text'
        head, tail = full.split(' Screenshot: ')
        assert head == 'INVOICE-IT for Windows (Eastern Digital Resources, 1993).'
        paras = [head.replace(', 1993).', ').'), 'Screenshot: ' + tail]
        edit = ('Verbatim except that the software year ", 1993" is left off screen, so the panel cannot be read as a 1993 '
                'capture (the pictured form shows the 2016 emulator date). The full record text is kept in delivery.json credits.')
    elif p['asset'] == 'XTRA-12':
        full, field = r['credit_text'], 'credit_text'
        assert full.endswith(' ' + MS_STATEMENT)
        paras = [full[:-len(MS_STATEMENT) - 1], MS_STATEMENT]
        edit = 'Verbatim; the required Microsoft statement is set on its own line.'
    else:
        full, field = r['credit_text_proposed'], 'credit_text_proposed'
        paras = [full]
        edit = 'Verbatim. The upstream record marks this credit proposed, not approved (credit_text_approved is null).'
    assert all(x in full.replace(', 1993', '') for x in paras)
    return {'credit_record': f"assets/historical/{p['asset']}/evidence/rights.json#{field}", 'credit_full': full,
            'credit_paras': paras, 'credit_edit': edit}


def resample(img: Image.Image, w: int, h: int) -> tuple[Image.Image, str]:
    sw, sh = img.size
    if w % sw == 0 and h % sh == 0 and w // sw == h // sh:
        return img.resize((w, h), Image.Resampling.NEAREST), f'nearest-neighbour, integer {w // sw}x'
    return img.resize((w, h), Image.Resampling.LANCZOS), 'Pillow LANCZOS (non-integer factor)'


def fit(size: list[int], max_w: float, max_h: float, tol: float = 0.15) -> tuple[int, int]:
    """Largest whole-pixel placement with the source aspect ratio (rounding error <= tol px)."""
    sw, sh = size
    s = min(max_w / sw, max_h / sh)
    k = math.floor(s)
    if k >= 1 and k >= 0.9 * s:
        return k * sw, k * sh
    hmax = math.floor(s * sh)
    best = None
    for h in range(hmax, max(1, math.floor(hmax * 0.97)) - 1, -1):
        exact = h * sw / sh
        w = round(exact)
        if w > max_w:
            continue
        if abs(w - exact) <= tol:
            return w, h
        if best is None or abs(w - exact) < best[0]:
            best = (abs(w - exact), w, h)
    return best[1], best[2]


def common_height(panels: list[dict], budget: int, tol: float = 0.2) -> tuple[int, list[int]]:
    asp = [p['size'][0] / p['size'][1] for p in panels]
    hmax = math.floor(budget / sum(asp))
    for h in range(hmax, hmax - 40, -1):
        ws = [round(h * a) for a in asp]
        if sum(ws) <= budget and all(abs(w - h * a) <= tol for w, a in zip(ws, asp)):
            return h, ws
    raise SystemExit('no common panel height keeps every aspect ratio within tolerance')


def credit_lines(p: dict, limit: float) -> list[str]:
    lines = []
    for para in p['credit_paras']:
        # The Microsoft statement is never broken across lines; check() still guards it against
        # every image, frame, other text box and the safe area.
        lines += [para] if para == MS_STATEMENT else wrap(para, limit, CREDIT_PX, 'sans')
    assert all(width(l, CREDIT_PX, 'sans') <= limit for l in lines if l != MS_STATEMENT), 'credit line wider than its column'
    return lines


def panel_block(p: dict, label_px: int, col_w: float) -> dict:
    la, ld = metrics(label_px, True)
    ca, cd = metrics(CREDIT_PX, False)
    lines = credit_lines(p, col_w)
    above = la + ld + LABEL_GAP + OUT                                        # label top to image top
    below = OUT + CREDIT_GAP + ca + (len(lines) - 1) * CREDIT_PX * LEAD + cd  # image bottom to last credit descent
    return {'lines': lines, 'above': above, 'below': below, 'la': la, 'ca': ca}


def place(p: dict, x: int, y: int, w: int, h: int, label_px: int, lines: list[str], role: str) -> dict:
    sw, sh = p['size']
    img, method = resample(p['image'], w, h)
    buf = io.BytesIO()
    img.save(buf, 'PNG', optimize=True)
    png = buf.getvalue()
    la, ld = metrics(label_px, True)
    ca, cd = metrics(CREDIT_PX, False)
    fx = x - OUT
    label_base = y - OUT - LABEL_GAP - ld
    texts = [{'kind': 'label', 'text': p['label'], 'x': fx, 'baseline': label_base, 'size': label_px, 'bold': True,
              'box': [fx, label_base - la, fx + width(p['label'], label_px, 'bold'), label_base + ld]}]
    base = y + h + OUT + CREDIT_GAP + ca
    for i, line in enumerate(lines):
        b = base + i * CREDIT_PX * LEAD
        texts.append({'kind': 'credit', 'text': line, 'x': fx, 'baseline': b, 'size': CREDIT_PX, 'bold': False,
                      'box': [fx, b - ca, fx + width(line, CREDIT_PX, 'sans'), b + cd]})
    return {'panel': p['key'], 'label': p['label'], 'role': role, 'asset': p['asset'], 'source_file': p['path'],
            'source_rel_path': p['rel_path'], 'source_sha256': p['sha256'], 'source_bytes': p['bytes'], 'source_mode': p['mode'],
            'source_size': [sw, sh], 'x': x, 'y': y, 'w': w, 'h': h, 'scale_x': round(w / sw, 6), 'scale_y': round(h / sh, 6),
            'source_aspect': round(sw / sh, 6), 'placed_aspect': round(w / h, 6), 'aspect_rel_error': abs((w / h) / (sw / sh) - 1),
            'resampling': method, 'crop': None, 'rotation_deg': 0, 'frame_outer': [fx, y - OUT, w + 2 * OUT, h + 2 * OUT],
            'embedded_png_sha256': hashlib.sha256(png).hexdigest(), 'credit_record': p['credit_record'],
            'credit_full': p['credit_full'], 'credit_on_screen': ' '.join(p['credit_paras']), 'credit_edit': p['credit_edit'],
            'texts': texts, '_png': png}


def layout_collage(panels: list[dict]) -> list[dict]:
    gap = 32
    budget = (SAFE[2] - SAFE[0]) - 2 * gap - 3 * 2 * OUT
    # 0.3 px rounding tolerance: a whole-pixel rectangle can never be closer than 0.5 px to a non-integer
    # scale, and a tighter bound forced the height down until XTRA-13 was reduced below native size.
    h, ws = common_height(panels, budget, tol=0.3)
    total = sum(ws) + 3 * 2 * OUT + 2 * gap
    blocks = [panel_block(p, LABEL_PX, w + 2 * OUT) for p, w in zip(panels, ws)]
    above = max(b['above'] for b in blocks)
    below = max(b['below'] for b in blocks)
    top = SAFE[1] + ((SAFE[3] - SAFE[1]) - (above + h + below)) / 2
    y = round(top + above)
    x = SAFE[0] + ((SAFE[2] - SAFE[0]) - total) // 2 + OUT
    placed = []
    for p, w, b in zip(panels, ws, blocks):
        placed.append(place(p, x, y, w, h, LABEL_PX, b['lines'], 'collage panel'))
        x += w + 2 * OUT + gap
    return placed


def layout_focus(panels: list[dict], focus: int) -> list[dict]:
    rw, gap_x, gap_y = 520, 56, 48
    lw = (SAFE[2] - SAFE[0]) - rw - gap_x
    fp = panels[focus]
    col = lw
    for _ in range(4):   # credit wrap width depends on the placed width; iterate to a stable fit
        b = panel_block(fp, LABEL_PX, col)
        w, h = fit(fp['size'], lw - 2 * OUT, (SAFE[3] - SAFE[1]) - b['above'] - b['below'])
        new_col = max(w + 2 * OUT, min(lw, 760))
        if new_col == col:
            break
        col = new_col
    b = panel_block(fp, LABEL_PX, col)
    assert b['above'] + h + b['below'] <= SAFE[3] - SAFE[1]
    x = SAFE[0] + (lw - col) // 2 + OUT
    y = round(SAFE[1] + ((SAFE[3] - SAFE[1]) - (b['above'] + h + b['below'])) / 2 + b['above'])
    placed = [place(fp, x, y, w, h, LABEL_PX, b['lines'], 'focused panel (enlarged)')]
    slot_h = ((SAFE[3] - SAFE[1]) - gap_y) / 2
    for i, p in enumerate(q for j, q in enumerate(panels) if j != focus):
        sb = panel_block(p, SMALL_LABEL_PX, rw)
        sw_, sh_ = fit(p['size'], rw - 2 * OUT, slot_h - sb['above'] - sb['below'])
        slot_top = SAFE[1] + i * (slot_h + gap_y)
        sy = round(slot_top + (slot_h - (sb['above'] + sh_ + sb['below'])) / 2 + sb['above'])
        placed.append(place(p, SAFE[2] - rw + OUT, sy, sw_, sh_, SMALL_LABEL_PX, sb['lines'], 'context panel (reduced)'))
    return placed


def intersects(a: list[float], b: list[float]) -> bool:   # boxes as [x0, y0, x1, y1]
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def check(placed: list[dict]) -> dict:
    img_boxes = [[q['x'], q['y'], q['x'] + q['w'], q['y'] + q['h']] for q in placed]
    frames = [[f[0], f[1], f[0] + f[2], f[1] + f[3]] for f in (q['frame_outer'] for q in placed)]
    texts = [t for q in placed for t in q['texts']]
    problems = []
    for i, a in enumerate(img_boxes):
        for j, fr in enumerate(frames):
            if i != j and intersects(a, fr):
                problems.append(f'{placed[i]["asset"]} image intersects frame of {placed[j]["asset"]}')
        for t in texts:
            if intersects(a, t['box']):
                problems.append(f'{placed[i]["asset"]} image intersects text "{t["text"]}"')
    for i, fr in enumerate(frames):
        for t in texts:
            if intersects(fr, t['box']):
                problems.append(f'frame of {placed[i]["asset"]} intersects text "{t["text"]}"')
        if not (SAFE[0] <= fr[0] and fr[2] <= SAFE[2] and SAFE[1] <= fr[1] and fr[3] <= SAFE[3]):
            problems.append(f'frame of {placed[i]["asset"]} outside safe area')
    for a in range(len(texts)):
        t = texts[a]['box']
        if not (SAFE[0] <= t[0] and t[2] <= SAFE[2] and SAFE[1] <= t[1] and t[3] <= SAFE[3]):
            problems.append(f'text "{texts[a]["text"]}" outside safe area')
        for b in range(a + 1, len(texts)):
            if intersects(t, texts[b]['box']):
                problems.append(f'text "{texts[a]["text"]}" intersects text "{texts[b]["text"]}"')
    ms = [q for q in placed if q['asset'] == 'XTRA-12']
    if ms and not any(t['text'] == MS_STATEMENT for t in ms[0]['texts']):
        problems.append('Microsoft statement missing from the XTRA-12 panel')
    assert not problems, problems
    return {'image_rects_clear_of_all_frames_and_text': True, 'text_clear_of_text': True, 'all_in_safe_area': True,
            'microsoft_statement_with_xtra12': bool(ms), 'problems': problems}


def compose(placed: list[dict], title: str) -> str:
    s = SVG(BG, title)
    for q in placed:   # frames first; images are painted last so nothing can be drawn over them
        s.rect(q['x'] - PAD, q['y'] - PAD, q['w'] + 2 * PAD, q['h'] + 2 * PAD, PANEL, LINE, STROKE)
    for q in placed:
        for t in q['texts']:
            s.text(t['text'], t['x'], t['baseline'], t['size'], FG if t['kind'] == 'label' or t['text'] == MS_STATEMENT else MUTED, t['bold'])
    for q in placed:
        uri = 'data:image/png;base64,' + base64.b64encode(q['_png']).decode('ascii')
        s.raw(f'<image x="{q["x"]}" y="{q["y"]}" width="{q["w"]}" height="{q["h"]}" preserveAspectRatio="none" '
              f'image-rendering="optimizeSpeed" href="{uri}"><title>{html.escape(q["asset"] + ": " + q["label"])}</title></image>')
    return s.finish()


def main() -> None:
    panels = load_panels()
    variants = {'collage': layout_collage(panels)}
    for i, p in enumerate(panels):
        variants[f'focus-{p["key"]}'] = layout_focus(panels, i)
    for name in ('exports', 'evidence', 'proofs'):   # render_assets.py writes into these
        (ASSET / name).mkdir(parents=True, exist_ok=True)
    svgs, layout = {}, {'id': ID, 'canvas': [W, H], 'safe_area': list(SAFE), 'frame': {'mat_px': PAD, 'stroke_px': STROKE, 'extent_outside_image_px': OUT,
              'mat_fill': PANEL, 'stroke': LINE, 'background': BG}, 'coordinates': 'pixels, origin top-left of the 1920x1080 export; x/y/w/h is the exact placed image rectangle', 'variants': {}}
    for name, placed in variants.items():
        checks = check(placed)
        title = 'Real-world VB application collage: ' + ', '.join(q['label'] + ' (' + q['asset'] + ')' for q in placed)
        svgs[name] = compose(placed, title)
        (HERE / f'variant-{name}.svg').write_text(svgs[name], encoding='utf-8', newline='\n')
        layout['variants'][name] = {'svg': f'src/variant-{name}.svg', 'png': f'exports/{name}.png', 'build_checks': checks,
                                    'panels': [{k: v for k, v in q.items() if k != '_png'} for q in placed]}
        print(name, [(q['asset'], q['x'], q['y'], q['w'], q['h'], q['scale_x'], q['resampling'][:7], len([t for t in q['texts'] if t['kind'] == 'credit'])) for q in placed])
    layout['variants']['collage']['also_rendered_as'] = 'exports/poster.png'
    (HERE / 'layout.json').write_text(json.dumps(layout, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    (HERE / 'copy.txt').write_text(ROW['copy'] + '\n', encoding='utf-8', newline='\n')
    (HERE / 'brief.json').write_text(json.dumps({k: ROW[k] for k in ['id', 'title', 'brief', 'requirements', 'beats', 'checks', 'copy', 'refs', 'gates', 'deps', 'variants']}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    script = ROOT / 'sources' / 'SCRIPT.md'
    sources = [{'path': '../../../sources/SCRIPT.md', 'lines': [685, 687], 'sha256': hashlib.sha256(script.read_bytes()).hexdigest(), 'relationship': 'source creative brief (VISUAL cue at 687)'}]
    sources += [{'path': p['rel_path'], 'asset': p['asset'], 'sha256': p['sha256'], 'relationship': 'historical original from a produced upstream asset; read in place, uniformly scaled, never cropped or copied'} for p in panels]
    notes = [
        'Three labeled panels, exact ticket copy as labels in ticket order: Business tools = XTRA-11 (INVOICE-IT for Windows, VB 2.0), Data entry = XTRA-12 (VB6 Data Object Wizard form, Microsoft figure), Utilities = XTRA-13 (Karen\'s Window Watcher, VB6).',
        'Each screenshot is the whole upstream original, uniformly scaled; no crop, rotation, overlap or retouch. A mat and frame sit outside the image edges only. Exact rectangles and scale factors: src/layout.json.',
        'Every panel carries its own credit from the upstream rights record. The XTRA-12 panel carries "Used with permission from Microsoft." on its own line.',
        'No capture date, year caption, statistic, user count, revenue, bank/hospital claim or customer data is added. Dates inside the screenshots (02-27-2016 in XTRA-11, 9/3/2003 in XTRA-13) are original pixels and are not captioned.',
        'Optional focus variants enlarge one panel and keep the other two whole, reduced and credited.',
        'Release stays blocked under R11 and R14 until the review deck decides; internal proof only.',
    ]
    frames = [{'time': 0, 'file': 'variant-collage.svg'}]
    timeline = {'id': ID, 'durationSeconds': None, 'fps': None, 'width': W, 'height': H, 'beats': ROW['beats'], 'frames': frames, 'cuts': {},
                'variant_names': list(variants), 'motion_model': 'Still asset: each variant is a separate still held for editorial timing; no animation or named cutdown.'}
    (HERE / 'timeline.json').write_text(json.dumps(timeline, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    build = {'id': ID, 'duration': None, 'frames': frames, 'variants': {n: f'variant-{n}.svg' for n in variants}, 'poster': 'variant-collage.svg',
             'cuts': {}, 'notes': notes, 'sources': sources, 'kind': ROW['kind']}
    (HERE / 'build.json').write_text(json.dumps(build, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    table = {'variant-collage.svg': svgs['collage']}
    # Same deterministic, offline HTML contract as tools/render/build_assets.py.
    doc = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(ROW['title']) + '</title>'
           '<style>html,body{margin:0;background:#000;height:100%;overflow:hidden}#stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center}svg{width:100%;height:100%;object-fit:contain}</style>'
           '<div id="stage" aria-label="' + html.escape(ROW['title'], quote=True) + '"></div><script>const timeline=' + json.dumps(timeline, ensure_ascii=False) + ';const scenes=' + json.dumps(table, ensure_ascii=False) + ';'
           "const stage=document.getElementById('stage');window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,"
           'renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;else break}stage.innerHTML=scenes[f.file];return f.file}};'
           "__ASSET__.renderAt(0);document.addEventListener('keydown',e=>{if(e.code==='Home')__ASSET__.renderAt(0)});</script></html>")
    (HERE / 'index.html').write_text(doc, encoding='utf-8', newline='\n')
    print('AUTHORED', ID, {n: len(s) for n, s in svgs.items()})


if __name__ == '__main__':
    main()
