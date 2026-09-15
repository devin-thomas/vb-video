#!/usr/bin/env python3
"""XTRA-05 authoring script: VB4 IDE anatomy, five labeled panels.

Run from the repository root:  python -B assets/stills/XTRA-05/src/build.py
It writes this ticket's editable sources only: one SVG per named variant (the uniformly scaled
HIST-02 screenshot is embedded as a PNG data: URI so CairoSVG and the in-memory browser check need no
file access), offline HTML, timeline, build driver, exact copy, and src/layout.json (placement,
targets, every annotation mark and the original pixels it overlays). Rendering, browser checks and
delivery finishing use tools/render with --id XTRA-05; src/verify.py then checks the rendered pixels.
build_assets.py has no XTRA-05 composition, so this script replaces it here.

The HIST-02 original is read in place (assets/historical/HIST-02/source/original.png) and never
written or copied. Its SHA-256 must equal the value in HIST-02/delivery.json or the build stops.
The whole 800x600 screenshot is placed at a uniform 1.5x scale: no crop, rotation, stretch, retouch
or zoom-in. clean-workspace draws nothing over the image. five-callouts puts the label text in the
side margins; only thin leader lines and outline strokes on window frames cross onto the image.
"""
from __future__ import annotations
import base64, hashlib, html, io, json, math, sys
from pathlib import Path
from PIL import Image, ImageFont

HERE = Path(__file__).resolve().parent
ASSET = HERE.parent
ROOT = HERE.parents[3]   # src -> XTRA-05 -> stills -> assets -> repository root
sys.path.insert(0, str(ROOT / 'tools' / 'render'))
from studio import SVG, BG, PANEL, FG, LINE, GOLD, FONT_PATHS, width  # noqa: E402

ID = 'XTRA-05'
ROW = next(r for r in json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))['tickets'] if r['id'] == ID)
LABELS = ROW['copy'].split('\n')   # exact ticket copy, in ticket order
assert LABELS == ['Form Designer', 'Toolbox', 'Properties Window', 'Code Window', 'Project Explorer'], LABELS

W, H = 1920, 1080
SAFE = (120, 72, 1800, 1008)
UP = ROOT / 'assets' / 'historical' / 'HIST-02'
SRC_REL = 'source/original.png'
SCALE_NUM, SCALE_DEN = 3, 2          # uniform 1.5x: 800x600 -> 1200x900 exactly, no aspect rounding
RESAMPLE = Image.Resampling.BOX      # area-average; see qa.md for the NEAREST/LANCZOS comparison
RESAMPLE_NAME = 'Pillow Image.Resampling.BOX (area average), exact 1.5x on both axes'
PAD, STROKE = 6, 2                   # mat between image edge and frame stroke (same frame as XTRA-14)
OUT = PAD + STROKE // 2              # frame extent outside every image edge (7 px)
LABEL_PX, LEAD = 40, 1.15
TEXT_GAP = 14                        # label text edge to leader start
MIN_LEADER = 28                      # visible leader length outside the image frame
TK = 5                               # mark thickness: 1 px dark casing + 3 px gold core + 1 px casing
CORE = GOLD                          # #eab676, shared accent (studio.py)
CASING = BG                          # #111318
OCCLUSION_GAP = 6                    # Form Designer outline stops this far short of the Code Window outline

# Target windows in ORIGINAL pixel coordinates, inclusive (x0, y0, x1, y1). Edges were measured from
# the Win95 frame lines of the original (light #DFD8DF top/left and black right/bottom runs); see
# evidence/claim-checks.json. leader_y is an original row whose pixels between the image edge and
# the target are all desktop teal (checked again from pixels in verify.py).
TARGETS = [
    {'label': 'Toolbox', 'panel': 'Toolbox window (untitled tool window, vertical strip of control icons)',
     'rect': [4, 78, 67, 400], 'side': 'left', 'leader_y': 240, 'shape': 'closed outline'},
    {'label': 'Form Designer', 'panel': "Form window 'LoanSheet' in design mode (grid dots, controls); lower right covered by the Code window",
     'rect': [76, 76, 554, 462], 'side': 'left', 'leader_y': 430, 'shape': 'open outline along the visible edges, stopping short of the Code Window outline'},
    {'label': 'Code Window', 'panel': "Code window 'LoanSheet' (Object: grdPayments, Proc: Click)",
     'rect': [196, 327, 588, 562], 'side': 'left', 'leader_y': 535, 'shape': 'closed outline'},
    {'label': 'Project Explorer', 'panel': "Project window titled 'Loan' (View Form / View Code, LOAN.FRM LoanSheet)",
     'rect': [600, 77, 797, 187], 'side': 'right', 'leader_y': 150, 'shape': 'closed outline'},
    {'label': 'Properties Window', 'panel': "Properties window 'Properties - LoanSheet' (grdPayments Grid)",
     'rect': [599, 338, 792, 567], 'side': 'right', 'leader_y': 470, 'shape': 'closed outline'},
]
assert sorted(t['label'] for t in TARGETS) == sorted(LABELS)


def load_original() -> dict:
    raw = (UP / SRC_REL).read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    rec = next(o for o in json.loads((UP / 'delivery.json').read_text(encoding='utf-8'))['outputs'] if o['path'] == SRC_REL)
    assert sha == rec['sha256'] and len(raw) == rec['bytes'], 'HIST-02 original differs from its delivery.json record'
    img = Image.open(io.BytesIO(raw))
    img.load()
    assert img.size == (800, 600), img.size
    rgb = img.convert('RGB')
    return {'raw': raw, 'sha256': sha, 'bytes': len(raw), 'mode': img.mode, 'size': list(img.size), 'rgb': rgb}


def resample(rgb: Image.Image) -> Image.Image:
    w, h = rgb.size
    assert (w * SCALE_NUM) % SCALE_DEN == 0 and (h * SCALE_NUM) % SCALE_DEN == 0
    return rgb.resize((w * SCALE_NUM // SCALE_DEN, h * SCALE_NUM // SCALE_DEN), RESAMPLE)


def split_label(label: str) -> list[str]:
    return label.split(' ')   # multi-word labels stack one word per line; words and case unchanged


def metrics() -> tuple[int, int]:
    return ImageFont.truetype(FONT_PATHS['bold'], LABEL_PX).getmetrics()


def ring(L: int, T: int, R: int, B: int, th: int) -> list[list[int]]:
    return [[L, T, R, T + th], [L, B - th, R, B], [L, T, L + th, B], [R - th, T, R, B]]


def layout(orig: dict) -> dict:
    s = SCALE_NUM / SCALE_DEN
    iw, ih = orig['size'][0] * SCALE_NUM // SCALE_DEN, orig['size'][1] * SCALE_NUM // SCALE_DEN
    asc, desc = metrics()
    lines = {t['label']: split_label(t['label']) for t in TARGETS}
    lw = {t['label']: max(width(l, LABEL_PX, 'bold') for l in lines[t['label']]) for t in TARGETS}
    need_l = max(lw[t['label']] for t in TARGETS if t['side'] == 'left') + TEXT_GAP + MIN_LEADER + OUT
    need_r = max(lw[t['label']] for t in TARGETS if t['side'] == 'right') + TEXT_GAP + MIN_LEADER + OUT
    spare = (SAFE[2] - SAFE[0]) - iw - need_l - need_r
    assert spare >= 0, f'labels do not fit beside a {iw} px image (short by {-spare:.1f} px)'
    X = math.ceil(SAFE[0] + need_l + spare / 2)
    Y = SAFE[1] + ((SAFE[3] - SAFE[1]) - ih) // 2
    img_box = [X, Y, X + iw, Y + ih]
    frame_box = [X - OUT, Y - OUT, X + iw + OUT, Y + ih + OUT]
    leader_l_start = X - OUT - MIN_LEADER - math.floor(spare / 2)   # left labels end TEXT_GAP before this x
    leader_r_end = X + iw + OUT + MIN_LEADER + math.floor(spare / 2)

    def canvas_box(r):
        x0, y0, x1, y1 = r
        return [math.ceil(X + x0 * s), math.ceil(Y + y0 * s), math.floor(X + (x1 + 1) * s), math.floor(Y + (y1 + 1) * s)]

    boxes = {t['label']: canvas_box(t['rect']) for t in TARGETS}
    code = boxes['Code Window']
    targets = []
    for t in TARGETS:
        L, T, R, B = boxes[t['label']]
        if t['label'] == 'Form Designer':
            stop_y, stop_x = code[1] - OCCLUSION_GAP, code[0] - OCCLUSION_GAP
            assert R < code[2] and B > code[1] and L < code[0]
            casing = [[L, T, R, T + TK], [L, T, L + TK, B], [R - TK, T, R, stop_y], [L, B - TK, stop_x, B]]
            core = [[L + 1, T + 1, R - 1, T + TK - 1], [L + 1, T + 1, L + TK - 1, B - 1],
                    [R - TK + 1, T + 1, R - 1, stop_y - 1], [L + 1, B - TK + 1, stop_x - 1, B - 1]]
        else:
            casing = ring(L, T, R, B, TK)
            core = ring(L + 1, T + 1, R - 1, B - 1, TK - 2)
        yc = Y + (t['leader_y'] + 0.5) * s
        top = round(yc - TK / 2)
        if t['side'] == 'left':
            xa, xb = leader_l_start, L
            lcasing = [[xa, top, xb, top + TK]]
            lcore = [[xa + 1, top + 1, xb + 1, top + TK - 1]]
            anchor, tx = 'end', xa - TEXT_GAP
        else:
            xa, xb = R, leader_r_end
            lcasing = [[xa, top, xb, top + TK]]
            lcore = [[xa - 1, top + 1, xb - 1, top + TK - 1]]
            anchor, tx = 'start', xb + TEXT_GAP
        ls = lines[t['label']]
        block_h = asc + desc + (len(ls) - 1) * LABEL_PX * LEAD
        first = (top + TK / 2) - block_h / 2 + asc
        texts = []
        for i, line in enumerate(ls):
            base = round(first + i * LABEL_PX * LEAD, 2)
            wdt = width(line, LABEL_PX, 'bold')
            x0 = tx - wdt if anchor == 'end' else tx
            texts.append({'text': line, 'x': tx, 'anchor': anchor, 'baseline': base, 'size': LABEL_PX, 'bold': True,
                          'box': [round(x0, 2), round(base - asc, 2), round(x0 + wdt, 2), round(base + desc, 2)]})
        marks = []
        for kind, cas, cor in (('outline', casing, core), ('leader', lcasing, lcore)):
            marks.append({'target': t['label'], 'type': kind, 'casing_rects': cas, 'core_rects': cor})
        targets.append(dict(t, canvas_box=[L, T, R, B], leader_row_canvas=[top, top + TK], texts=texts, marks=marks))
    return {'X': X, 'Y': Y, 'iw': iw, 'ih': ih, 'scale': s, 'img_box': img_box, 'frame_box': frame_box, 'targets': targets,
            'spare_px': spare, 'label_metrics': {'ascent': asc, 'descent': desc}}


def intersects(a, b) -> bool:   # [x0, y0, x1, y1], half-open
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def overlay_record(rect: list[int], lay: dict, rgb: Image.Image) -> dict | None:
    """Original pixels whose 1.5x footprint the mark rectangle touches, with their colours."""
    X, Y, s = lay['X'], lay['Y'], lay['scale']
    ib = lay['img_box']
    x0, y0, x1, y1 = max(rect[0], ib[0]), max(rect[1], ib[1]), min(rect[2], ib[2]), min(rect[3], ib[3])
    if x0 >= x1 or y0 >= y1:
        return None
    ox0, oy0 = math.floor((x0 - X) / s), math.floor((y0 - Y) / s)
    ox1, oy1 = math.ceil((x1 - X) / s) - 1, math.ceil((y1 - Y) / s) - 1
    hist: dict = {}
    px = rgb.load()
    for yy in range(oy0, oy1 + 1):
        for xx in range(ox0, ox1 + 1):
            c = '#%02x%02x%02x' % px[xx, yy]
            hist[c] = hist.get(c, 0) + 1
    return {'canvas_rect_on_image': [x0, y0, x1, y1], 'original_px_inclusive': [ox0, oy0, ox1, oy1],
            'original_px_count': (ox1 - ox0 + 1) * (oy1 - oy0 + 1), 'original_colours': dict(sorted(hist.items(), key=lambda kv: -kv[1]))}


def check(lay: dict) -> dict:
    problems = []
    texts = [x for t in lay['targets'] for x in t['texts']]
    for x in texts:
        b = x['box']
        if intersects(b, lay['frame_box']):
            problems.append(f'label "{x["text"]}" intersects the screenshot or its frame')
        if not (SAFE[0] <= b[0] and b[2] <= SAFE[2] and SAFE[1] <= b[1] and b[3] <= SAFE[3]):
            problems.append(f'label "{x["text"]}" outside safe area')
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            if intersects(texts[i]['box'], texts[j]['box']):
                problems.append(f'label "{texts[i]["text"]}" intersects "{texts[j]["text"]}"')
    rects = [(t['label'], m['type'], r) for t in lay['targets'] for m in t['marks'] for r in m['casing_rects']]
    for lbl, typ, r in rects:
        if not (0 <= r[0] < r[2] <= W and 0 <= r[1] < r[3] <= H):
            problems.append(f'{lbl} {typ} rect {r} degenerate or off canvas')
        for x in texts:
            if intersects(r, x['box']):
                problems.append(f'{lbl} {typ} mark intersects label "{x["text"]}"')
        if typ == 'outline' and not (lay['img_box'][0] <= r[0] and r[2] <= lay['img_box'][2] and lay['img_box'][1] <= r[1] and r[3] <= lay['img_box'][3]):
            problems.append(f'{lbl} outline leaves the image')
    # Outlines of different targets must not touch (the Form Designer stop gap keeps it off the Code Window outline).
    outl = [(lbl, r) for lbl, typ, r in rects if typ == 'outline']
    for i in range(len(outl)):
        for j in range(i + 1, len(outl)):
            if outl[i][0] != outl[j][0] and intersects(outl[i][1], outl[j][1]):
                problems.append(f'outline of {outl[i][0]} touches outline of {outl[j][0]}')
    assert not problems, problems
    return {'labels_clear_of_screenshot_and_frame': True, 'labels_in_safe_area': True, 'labels_clear_of_each_other': True,
            'marks_clear_of_labels': True, 'outlines_inside_image_and_not_touching': True, 'problems': problems}


def compose(lay: dict, png: bytes, annotated: bool, title: str) -> str:
    sv = SVG(BG, title)
    X, Y, iw, ih = lay['X'], lay['Y'], lay['iw'], lay['ih']
    sv.rect(X - PAD, Y - PAD, iw + 2 * PAD, ih + 2 * PAD, PANEL, LINE, STROKE)   # mat and frame outside the image
    uri = 'data:image/png;base64,' + base64.b64encode(png).decode('ascii')
    sv.raw(f'<image x="{X}" y="{Y}" width="{iw}" height="{ih}" preserveAspectRatio="none" image-rendering="optimizeSpeed" '
           f'href="{uri}"><title>HIST-02: Microsoft Visual Basic 4.0 (32-bit) IDE, whole screenshot at 1.5x</title></image>')
    if annotated:
        for layer, key in (('casing', 'casing_rects'), ('core', 'core_rects')):   # all casings first so gold joints stay continuous
            fill = CASING if layer == 'casing' else CORE
            for t in lay['targets']:
                for m in t['marks']:
                    for r in m[key]:
                        sv.rect(r[0], r[1], r[2] - r[0], r[3] - r[1], fill)
        for t in lay['targets']:
            for x in t['texts']:
                sv.text(x['text'], x['x'], x['baseline'], x['size'], FG, True, anchor=x['anchor'])
    return sv.finish()


def main() -> None:
    orig = load_original()
    scaled = resample(orig['rgb'])
    buf = io.BytesIO()
    scaled.save(buf, 'PNG', optimize=True)
    png = buf.getvalue()
    lay = layout(orig)
    checks = check(lay)
    for name in ('exports', 'evidence', 'proofs'):   # render_assets.py writes into these
        (ASSET / name).mkdir(parents=True, exist_ok=True)
    svgs = {'clean-workspace': compose(lay, png, False, 'VB4 IDE: whole HIST-02 screenshot, framed, no annotation'),
            'five-callouts': compose(lay, png, True, 'VB4 IDE anatomy: ' + ', '.join(LABELS))}
    for name, svg in svgs.items():
        (HERE / f'variant-{name}.svg').write_text(svg, encoding='utf-8', newline='\n')
    edits = []
    n = 0
    for t in lay['targets']:
        for m in t['marks']:
            for layer, key, colour in (('casing', 'casing_rects', CASING), ('core', 'core_rects', CORE)):
                for r in m[key]:
                    n += 1
                    edits.append({'n': n, 'variant': 'five-callouts', 'target': t['label'], 'mark': m['type'], 'layer': layer,
                                  'shape': 'filled rectangle', 'canvas_rect_x0y0x1y1': r, 'colour': colour,
                                  'overlays_original': overlay_record(r, lay, orig['rgb'])})
    record = {
        'id': ID, 'canvas': [W, H], 'safe_area': list(SAFE),
        'coordinates': 'canvas pixels, origin top-left of the 1920x1080 export; rectangles are [x0, y0, x1, y1) half-open. Original pixel ranges are inclusive, origin top-left of the 800x600 original.',
        'source': {'asset': 'HIST-02', 'file': f'assets/historical/HIST-02/{SRC_REL}', 'rel_path': f'../../historical/HIST-02/{SRC_REL}',
                   'sha256': orig['sha256'], 'bytes': orig['bytes'], 'mode': orig['mode'], 'size': orig['size']},
        'placement': {'x': lay['X'], 'y': lay['Y'], 'w': lay['iw'], 'h': lay['ih'], 'scale_x': lay['iw'] / orig['size'][0], 'scale_y': lay['ih'] / orig['size'][1],
                      'resampling': RESAMPLE_NAME, 'crop': None, 'rotation_deg': 0, 'retouch': None,
                      'embedded_png_sha256': hashlib.sha256(png).hexdigest(), 'embedded_png_bytes': len(png),
                      'frame_outer': lay['frame_box'], 'identical_in_variants': ['clean-workspace', 'five-callouts']},
        'frame': {'mat_px': PAD, 'stroke_px': STROKE, 'extent_outside_image_px': OUT, 'mat_fill': PANEL, 'stroke': LINE, 'background': BG},
        'label_style': {'font': 'Liberation Sans Bold', 'size_px': LABEL_PX, 'leading': LEAD, 'fill': FG, 'metrics': lay['label_metrics'],
                        'line_breaks': 'multi-word labels are stacked one word per line; the words, spelling and capitalisation are the ticket copy'},
        'mark_style': {'thickness_px': TK, 'core': CORE, 'core_px': TK - 2, 'casing': CASING, 'casing_px': 1,
                       'outline_position': 'inside each target window outer boundary, so the outline covers only that window\'s outer frame bevel (about 3.3 original px)',
                       'leader_position': 'horizontal, on an original row that is desktop teal between the image edge and the target'},
        'targets': [{k: v for k, v in t.items()} for t in lay['targets']],
        'annotation_edits': edits,
        'build_checks': checks,
        'variants': {'clean-workspace': {'svg': 'src/variant-clean-workspace.svg', 'png': 'exports/clean-workspace.png', 'annotated': False},
                     'five-callouts': {'svg': 'src/variant-five-callouts.svg', 'png': 'exports/five-callouts.png', 'annotated': True,
                                       'also_rendered_as': 'exports/poster.png'}},
    }
    (HERE / 'layout.json').write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    (HERE / 'copy.txt').write_text(ROW['copy'] + '\n', encoding='utf-8', newline='\n')
    (HERE / 'brief.json').write_text(json.dumps({k: ROW[k] for k in ['id', 'title', 'brief', 'requirements', 'beats', 'checks', 'copy', 'refs', 'gates', 'deps', 'variants']}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    script = ROOT / 'sources' / 'SCRIPT.md'
    sources = [{'path': '../../../sources/SCRIPT.md', 'lines': [130, 134], 'sha256': hashlib.sha256(script.read_bytes()).hexdigest(),
                'relationship': 'source creative brief (VISUAL cue at 130, IDE narration at 132)'},
               {'path': record['source']['rel_path'], 'asset': 'HIST-02', 'sha256': orig['sha256'],
                'relationship': 'historical original from a produced upstream asset; read in place, whole image uniformly scaled 1.5x, never cropped or copied'}]
    notes = [
        'Whole HIST-02 screenshot (WinWorld "Microsoft Visual Basic 4.0 32 bit - Edit", 800x600) at a uniform 1.5x (1200x900, Pillow BOX) in both variants; no crop, rotation, stretch, retouch or zoom-in. Mat and frame sit outside the image edges.',
        'clean-workspace: framed screenshot only; nothing is drawn over its pixels.',
        'five-callouts (= poster): the five exact ticket labels sit in the side margins, outside the screenshot. Only 5 px outlines on each target window\'s own frame and horizontal leaders over empty desktop cross onto the image. Every mark and the original pixels it covers: src/layout.json annotation_edits.',
        '"Project Explorer" is kept verbatim as ticket copy; the VB4 window is titled with the project name and Microsoft calls it the Project window. Review question for the Writing Lead in evidence/claim-checks.json.',
        'No on-screen credit: HIST-02 rights.json has credit_text null, and its proposed credit ("... Used with permission from Microsoft.") must not be used before RQ-HIST-02-1 is decided. The proposed credit is carried in delivery.json credits, marked proposed.',
        'Release blocked under R03 and R14 until the review deck decides; internal proof only.',
    ]
    frames = [{'time': 0, 'file': 'variant-five-callouts.svg'}]
    timeline = {'id': ID, 'durationSeconds': None, 'fps': None, 'width': W, 'height': H, 'beats': ROW['beats'], 'frames': frames, 'cuts': {},
                'variant_names': list(svgs), 'motion_model': 'Still asset: each variant is a separate still held for editorial timing. The one-panel-at-a-time reveal is editor-request only and was not built.'}
    (HERE / 'timeline.json').write_text(json.dumps(timeline, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    build = {'id': ID, 'duration': None, 'frames': frames, 'variants': {n: f'variant-{n}.svg' for n in svgs}, 'poster': 'variant-five-callouts.svg',
             'cuts': {}, 'notes': notes, 'sources': sources, 'kind': ROW['kind']}
    (HERE / 'build.json').write_text(json.dumps(build, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    table = {f'variant-{n}.svg': v for n, v in svgs.items()}
    # Same deterministic, offline HTML contract as tools/render/build_assets.py (still: time zero = five-callouts).
    doc = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(ROW['title']) + '</title>'
           '<style>html,body{margin:0;background:#000;height:100%;overflow:hidden}#stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center}svg{width:100%;height:100%;object-fit:contain}</style>'
           '<div id="stage" aria-label="' + html.escape(ROW['title'], quote=True) + '"></div><script>const timeline=' + json.dumps(timeline, ensure_ascii=False) + ';const scenes=' + json.dumps(table, ensure_ascii=False) + ';'
           "const stage=document.getElementById('stage');window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,variants:Object.keys(scenes),"
           'renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;else break}stage.innerHTML=scenes[f.file];return f.file},'
           'showVariant(n){stage.innerHTML=scenes["variant-"+n+".svg"];return n}};'
           "__ASSET__.renderAt(0);document.addEventListener('keydown',e=>{if(e.code==='Home')__ASSET__.renderAt(0)});</script></html>")
    (HERE / 'index.html').write_text(doc, encoding='utf-8', newline='\n')
    for t in lay['targets']:
        print(t['label'], 'target', t['rect'], 'canvas', t['canvas_box'], 'leader row', t['leader_row_canvas'], 'text', [x['box'] for x in t['texts']])
    print('placement', lay['X'], lay['Y'], lay['iw'], lay['ih'], 'spare', round(lay['spare_px'], 1), 'edits', len(edits))
    print('AUTHORED', ID, {n: len(v) for n, v in svgs.items()})


if __name__ == '__main__':
    main()
