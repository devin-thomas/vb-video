#!/usr/bin/env python3
"""XTRA-05 authoring script: VB4 IDE anatomy, five labeled panels.

Run from the repository root:  python -B assets/stills/XTRA-05/src/build.py
It writes this ticket's editable sources only: one SVG per named variant (screenshots embedded as PNG
data: URIs so CairoSVG and the in-memory browser check need no file access), offline HTML, timeline,
build driver, the rendered label copy, and src/layout.json (placements, targets, every annotation mark
and the original pixels it overlays). Rendering, browser checks and delivery finishing use
tools/render with --id XTRA-05; src/verify.py then checks the rendered pixels. build_assets.py has no
XTRA-05 composition, so this script replaces it here.

Labels come from the VISUAL cue in War/SCRIPT.md (the one line containing "VB4 IDE with labeled
callouts"), because the working script is the narrative authority. The build stops unless there are
exactly five, and each must still name the panel in its cue position, so a reordered cue stops the
build instead of putting a label on the wrong window.

The HIST-02 original is read in place (assets/historical/HIST-02/source/original.png) and never
written or copied. Its SHA-256 must equal the value in HIST-02/delivery.json or the build stops.
Variants:
  clean-workspace  the whole 800x600 screenshot at a uniform 1.5x (Pillow BOX), framed; nothing over it.
  five-callouts    the same placement; labels in the side margins; outlines on each target window's
                   own frame and horizontal leaders over empty desktop are the only marks on the image.
  side-by-side     the clean screenshot on the left and the annotated screenshot on the right, both
                   whole at native 1.0x (the HIST-02 PNG bytes, no resampling). Outlines sit on window
                   frames, leaders cross only desktop teal to rails in the dark gutters, and the labels
                   sit in a strip below the annotated side. No label text touches either screenshot.
"""
from __future__ import annotations
import base64, hashlib, html, io, json, math, re, sys
from pathlib import Path
from PIL import Image, ImageFont

HERE = Path(__file__).resolve().parent
ASSET = HERE.parent
ROOT = HERE.parents[3]   # src -> XTRA-05 -> stills -> assets -> repository root
sys.path.insert(0, str(ROOT / 'tools' / 'render'))
from studio import SVG, BG, PANEL, FG, LINE, GOLD, FONT_PATHS, width  # noqa: E402

ID = 'XTRA-05'
ROW = next(r for r in json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))['tickets'] if r['id'] == ID)
TICKET_COPY = ROW['copy'].split('\n')   # the ticket's exact-copy payload, kept for the record only

# ---- labels: read from the working script's VISUAL cue -------------------------------------------
SCRIPT_REL = 'War/SCRIPT.md'
CUE_MARK = 'VB4 IDE with labeled callouts'
# Panel identity of each cue position and a word the label in that position must contain.
CUE_PANELS = [('form', 'form'), ('toolbox', 'toolbox'), ('properties', 'propert'), ('code', 'code'), ('project', 'project')]


def read_cue(path: Path = ROOT / SCRIPT_REL) -> dict:
    raw = path.read_bytes()
    lines = raw.decode('utf-8').splitlines()
    hits = [(i + 1, line) for i, line in enumerate(lines) if CUE_MARK in line]
    assert len(hits) == 1, f'expected exactly one line containing "{CUE_MARK}" in {SCRIPT_REL}, found {len(hits)}'
    number, line = hits[0]
    m = re.search(r'labeled callouts:\s*(.+?)\.?\]', line)
    assert m, f'{SCRIPT_REL}:{number}: cannot find the callout list in the cue'
    labels = [s.strip() for s in m.group(1).split(',')]
    assert len(labels) == 5 and all(labels), f'{SCRIPT_REL}:{number}: expected exactly five callout labels, got {labels}'
    for label, (key, word) in zip(labels, CUE_PANELS):
        assert word in label.lower(), (f'{SCRIPT_REL}:{number}: callout {label!r} sits in the {key} position; '
                                       'the cue order changed, so update CUE_PANELS before rendering')
    return {'path': SCRIPT_REL, 'line': number, 'text': line, 'sha256': hashlib.sha256(raw).hexdigest(),
            'labels': labels, 'by_panel': {key: label for label, (key, _) in zip(labels, CUE_PANELS)}}


CUE = read_cue()
LABELS = CUE['labels']   # cue order

W, H = 1920, 1080
SAFE = (120, 72, 1800, 1008)
UP = ROOT / 'assets' / 'historical' / 'HIST-02'
SRC_REL = 'source/original.png'
SCALE_NUM, SCALE_DEN = 3, 2          # clean-workspace / five-callouts: uniform 1.5x, 800x600 -> 1200x900 exactly
RESAMPLE = Image.Resampling.BOX      # area-average; see qa.md for the NEAREST/LANCZOS comparison
RESAMPLE_NAME = 'Pillow Image.Resampling.BOX (area average), exact 1.5x on both axes'
NATIVE_NAME = 'none: native 1.0x, the HIST-02 PNG bytes embedded unchanged and drawn 1:1 (no resampling filter applies)'
PAD, STROKE = 6, 2                   # mat between image edge and frame stroke (same frame as XTRA-14)
OUT = PAD + STROKE // 2              # frame extent outside every image edge (7 px)
LABEL_PX, LEAD = 40, 1.15
TEXT_GAP = 14                        # label text edge to leader end
MIN_LEADER = 28                      # five-callouts: visible leader length outside the image frame
TK = 5                               # five-callouts marks: 1 px dark casing + 3 px gold core + 1 px casing
CORE = GOLD                          # #eab676, shared accent (studio.py)
CASING = BG                          # #111318
OCCLUSION_GAP = 6                    # five-callouts: Form Designer outline stops this far short of the Code Window outline

# side-by-side (native 1.0x)
SBS_TK = 4            # 1 px casing + 2 px gold core + 1 px casing: fits inside the 4 px Win95 window frame band at 1.0x
SBS_GAP = 5           # Form Designer outline stops this far short of the Code Window outline
SBS_OFF = 10          # annotated image edge to its innermost rail (clears the 7 px mat and frame)
SBS_SPACING = 10      # rail pitch: 4 px rail, 6 px dark
SBS_CLEAR = 8         # minimum space between the outermost left rail and the clean screenshot's frame
SBS_LABEL_PX = 40
SBS_INSET = 24        # label start (left group) / end (right group) inside the annotated image's edges
SBS_ROW_PAD = 14      # annotated frame bottom to the first label box
SBS_PITCH = 54        # label row pitch

POSTER = 'side-by-side'   # decided after the 720p review; see qa.md

# Target windows in ORIGINAL pixel coordinates, inclusive (x0, y0, x1, y1). Edges were measured from
# the Win95 frame lines of the original (light #DFD8DF top/left and black right/bottom runs); see
# evidence/claim-checks.json. leader_y is an original row whose pixels between the image edge and the
# target are all desktop teal (rows leader_y-2 .. leader_y+2 checked from pixels in verify.py).
PANELS = {
    'toolbox': {'panel': 'Toolbox window (untitled tool window, vertical strip of control icons)',
                'rect': [4, 78, 67, 400], 'side': 'left', 'leader_y': 240, 'shape': 'closed outline'},
    'form': {'panel': "Form window 'LoanSheet' in design mode (grid dots, controls); lower right covered by the Code window",
             'rect': [76, 76, 554, 462], 'side': 'left', 'leader_y': 430, 'shape': 'open outline along the visible edges, stopping short of the Code Window outline'},
    'code': {'panel': "Code window 'LoanSheet' (Object: grdPayments, Proc: Click)",
             'rect': [196, 327, 588, 562], 'side': 'left', 'leader_y': 535, 'shape': 'closed outline'},
    'project': {'panel': "Project window titled 'Loan' (View Form / View Code, LOAN.FRM LoanSheet)",
                'rect': [600, 77, 797, 187], 'side': 'right', 'leader_y': 150, 'shape': 'closed outline'},
    'properties': {'panel': "Properties window 'Properties - LoanSheet' (grdPayments Grid)",
                   'rect': [599, 338, 792, 567], 'side': 'right', 'leader_y': 470, 'shape': 'closed outline'},
}
DRAW_ORDER = ['toolbox', 'form', 'code', 'project', 'properties']
TARGETS = [dict(PANELS[k], key=k, label=CUE['by_panel'][k]) for k in DRAW_ORDER]
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


def resample(rgb: Image.Image, num: int = SCALE_NUM, den: int = SCALE_DEN) -> Image.Image:
    """Fresh uniform resample. At num == den this is Pillow's identity copy (no filter is applied)."""
    w, h = rgb.size
    assert (w * num) % den == 0 and (h * num) % den == 0
    return rgb.resize((w * num // den, h * num // den), RESAMPLE)


def split_label(label: str) -> list[str]:
    return label.split(' ')   # five-callouts: multi-word labels stack one word per line; words and case unchanged


def metrics(size: int = LABEL_PX) -> tuple[int, int]:
    return ImageFont.truetype(FONT_PATHS['bold'], size).getmetrics()


def ring(L: int, T: int, R: int, B: int, th: int) -> list[list[int]]:
    return [[L, T, R, T + th], [L, B - th, R, B], [L, T, L + th, B], [R - th, T, R, B]]


def canvas_box(r, X, Y, s):
    x0, y0, x1, y1 = r
    return [math.ceil(X + x0 * s), math.ceil(Y + y0 * s), math.floor(X + (x1 + 1) * s), math.floor(Y + (y1 + 1) * s)]


def outline_rects(key: str, box, code_box, tk: int, gap: int):
    """Casing and gold-core rectangles of one target outline, inside the target's outer boundary."""
    L, T, R, B = box
    if key == 'form':   # open outline: stop short of the Code window, which covers the form's lower right
        stop_y, stop_x = code_box[1] - gap, code_box[0] - gap
        assert R < code_box[2] and B > code_box[1] and L < code_box[0]
        casing = [[L, T, R, T + tk], [L, T, L + tk, B], [R - tk, T, R, stop_y], [L, B - tk, stop_x, B]]
        core = [[L + 1, T + 1, R - 1, T + tk - 1], [L + 1, T + 1, L + tk - 1, B - 1],
                [R - tk + 1, T + 1, R - 1, stop_y - 1], [L + 1, B - tk + 1, stop_x - 1, B - 1]]
    else:
        casing = ring(L, T, R, B, tk)
        core = ring(L + 1, T + 1, R - 1, B - 1, tk - 2)
    return casing, core


def label_text(line: str, x: float, anchor: str, centre_y: float, size: int, asc: int, desc: int, n_lines: int = 1, i: int = 0) -> dict:
    block_h = asc + desc + (n_lines - 1) * size * LEAD
    base = round(centre_y - block_h / 2 + asc + i * size * LEAD, 2)
    wdt = width(line, size, 'bold')
    x0 = x - wdt if anchor == 'end' else x
    return {'text': line, 'x': x, 'anchor': anchor, 'baseline': base, 'size': size, 'bold': True,
            'box': [round(x0, 2), round(base - asc, 2), round(x0 + wdt, 2), round(base + desc, 2)]}


# ---- five-callouts / clean-workspace (1.5x) --------------------------------------------------------
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
    boxes = {t['key']: canvas_box(t['rect'], X, Y, s) for t in TARGETS}
    targets = []
    for t in TARGETS:
        L, T, R, B = boxes[t['key']]
        casing, core = outline_rects(t['key'], boxes[t['key']], boxes['code'], TK, OCCLUSION_GAP)
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
        texts = [label_text(line, tx, anchor, top + TK / 2, LABEL_PX, asc, desc, len(ls), i) for i, line in enumerate(ls)]
        marks = [{'target': t['label'], 'type': 'outline', 'casing_rects': casing, 'core_rects': core},
                 {'target': t['label'], 'type': 'leader', 'casing_rects': lcasing, 'core_rects': lcore}]
        targets.append(dict(t, canvas_box=[L, T, R, B], leader_row_canvas=[top, top + TK], texts=texts, marks=marks))
    return {'X': X, 'Y': Y, 'iw': iw, 'ih': ih, 'scale': s, 'img_box': img_box, 'frame_box': frame_box, 'targets': targets,
            'spare_px': spare, 'label_metrics': {'ascent': asc, 'descent': desc}}


def intersects(a, b) -> bool:   # [x0, y0, x1, y1], half-open
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def inside(r, box) -> bool:
    return box[0] <= r[0] and r[2] <= box[2] and box[1] <= r[1] and r[3] <= box[3]


def overlay_record(rect: list[int], X: int, Y: int, s: float, img_box, rgb: Image.Image) -> dict | None:
    """Original pixels whose scaled footprint the mark rectangle touches, with their colours."""
    x0, y0, x1, y1 = max(rect[0], img_box[0]), max(rect[1], img_box[1]), min(rect[2], img_box[2]), min(rect[3], img_box[3])
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
    """five-callouts geometry: labels off the screenshot and frame, inside the safe area, no collisions."""
    problems = []
    texts = [x for t in lay['targets'] for x in t['texts']]
    for x in texts:
        b = x['box']
        if intersects(b, lay['frame_box']):
            problems.append(f'label "{x["text"]}" intersects the screenshot or its frame')
        if not inside(b, SAFE):
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
        if typ == 'outline' and not inside(r, lay['img_box']):
            problems.append(f'{lbl} outline leaves the image')
    outl = [(lbl, r) for lbl, typ, r in rects if typ == 'outline']
    for i in range(len(outl)):
        for j in range(i + 1, len(outl)):
            if outl[i][0] != outl[j][0] and intersects(outl[i][1], outl[j][1]):
                problems.append(f'outline of {outl[i][0]} touches outline of {outl[j][0]}')
    assert not problems, problems
    return {'labels_clear_of_screenshot_and_frame': True, 'labels_in_safe_area': True, 'labels_clear_of_each_other': True,
            'marks_clear_of_labels': True, 'outlines_inside_image_and_not_touching': True, 'problems': problems}


# ---- side-by-side (native 1.0x) ---------------------------------------------------------------------
def layout_sbs(orig: dict) -> dict:
    w, h = orig['size']
    asc, desc = metrics(SBS_LABEL_PX)
    hb = asc + desc
    by_side = {side: [t['key'] for t in sorted((t for t in TARGETS if t['side'] == side), key=lambda t: -t['leader_y'])]
               for side in ('left', 'right')}   # innermost rail = lowest exit, so rails never cross
    n_l, n_r = len(by_side['left']), len(by_side['right'])
    Xc = SAFE[0] + OUT                                                   # clean frame starts at the safe-area edge
    Xa = SAFE[2] - w - (SBS_OFF + SBS_TK + (n_r - 1) * SBS_SPACING)     # outer right rail ends at the safe-area edge
    clean_frame_right = Xc + w + OUT
    left_rail_outer = Xa - (SBS_OFF + SBS_TK + (n_l - 1) * SBS_SPACING)
    spare = left_rail_outer - SBS_CLEAR - clean_frame_right
    assert spare >= 0, f'side-by-side does not fit at 1.0x (short by {-spare} px)'
    rows = max(n_l, n_r)
    total_h = (h + 2 * OUT) + SBS_ROW_PAD + hb + (rows - 1) * SBS_PITCH
    top = SAFE[1] + ((SAFE[3] - SAFE[1]) - total_h) // 2
    assert top >= SAFE[1], 'side-by-side is taller than the safe area'
    Y = top + OUT
    clean = {'role': 'clean', 'x': Xc, 'y': Y, 'w': w, 'h': h, 'img_box': [Xc, Y, Xc + w, Y + h], 'frame_box': [Xc - OUT, Y - OUT, Xc + w + OUT, Y + h + OUT]}
    ann = {'role': 'annotated', 'x': Xa, 'y': Y, 'w': w, 'h': h, 'img_box': [Xa, Y, Xa + w, Y + h], 'frame_box': [Xa - OUT, Y - OUT, Xa + w + OUT, Y + h + OUT]}
    fb = Y + h + OUT
    boxes = {t['key']: canvas_box(t['rect'], Xa, Y, 1) for t in TARGETS}
    targets = []
    for t in TARGETS:
        L, T, R, B = boxes[t['key']]
        casing, core = outline_rects(t['key'], boxes[t['key']], boxes['code'], SBS_TK, SBS_GAP)
        k = by_side[t['side']].index(t['key'])
        lt = Y + t['leader_y'] - SBS_TK // 2            # exit leader covers original rows leader_y-2 .. leader_y+1
        rc = fb + SBS_ROW_PAD + hb / 2 + k * SBS_PITCH   # label row centre
        rt = round(rc - SBS_TK / 2)
        if t['side'] == 'left':
            x0 = Xa - SBS_OFF - SBS_TK - k * SBS_SPACING
            x1 = x0 + SBS_TK
            lab_x, anchor = Xa + SBS_INSET, 'start'
            end = lab_x - TEXT_GAP
            parts = [('exit', [x0, lt, L, lt + SBS_TK], [x0 + 1, lt + 1, L + 1, lt + SBS_TK - 1]),
                     ('rail', [x0, lt, x1, rt + SBS_TK], [x0 + 1, lt + 1, x1 - 1, rt + SBS_TK - 1]),
                     ('run', [x0, rt, end, rt + SBS_TK], [x0 + 1, rt + 1, end - 1, rt + SBS_TK - 1])]
        else:
            x0 = Xa + w + SBS_OFF + k * SBS_SPACING
            x1 = x0 + SBS_TK
            lab_x, anchor = Xa + w - SBS_INSET, 'end'
            start = lab_x + TEXT_GAP
            parts = [('exit', [R, lt, x1, lt + SBS_TK], [R - 1, lt + 1, x1 - 1, lt + SBS_TK - 1]),
                     ('rail', [x0, lt, x1, rt + SBS_TK], [x0 + 1, lt + 1, x1 - 1, rt + SBS_TK - 1]),
                     ('run', [start, rt, x1, rt + SBS_TK], [start + 1, rt + 1, x1 - 1, rt + SBS_TK - 1])]
        texts = [label_text(t['label'], lab_x, anchor, rt + SBS_TK / 2, SBS_LABEL_PX, asc, desc)]
        marks = [{'target': t['label'], 'type': 'outline', 'casing_rects': casing, 'core_rects': core},
                 {'target': t['label'], 'type': 'leader', 'parts': [p[0] for p in parts],
                  'casing_rects': [p[1] for p in parts], 'core_rects': [p[2] for p in parts]}]
        targets.append(dict(t, canvas_box=[L, T, R, B], leader_row_canvas=[lt, lt + SBS_TK], rail_index=k, label_row=k,
                            rail_x=[x0, x1], label_row_canvas=[rt, rt + SBS_TK], texts=texts, marks=marks))
    return {'scale': 1.0, 'clean': clean, 'annotated': ann, 'targets': targets, 'spare_px': spare,
            'gap_between_frames_px': ann['frame_box'][0] - clean['frame_box'][2],
            'rails': {'left_inner_to_outer': by_side['left'], 'right_inner_to_outer': by_side['right']},
            'label_metrics': {'ascent': asc, 'descent': desc}}


def check_sbs(lay: dict) -> dict:
    """side-by-side geometry: no overlap between the two screenshots, their frames, marks and labels."""
    problems = []
    cf, af, ai = lay['clean']['frame_box'], lay['annotated']['frame_box'], lay['annotated']['img_box']
    if intersects(cf, af):
        problems.append('clean and annotated screenshot frames overlap')
    for name, b in (('clean frame', cf), ('annotated frame', af)):
        if not inside(b, SAFE):
            problems.append(f'{name} {b} outside the safe area')
    texts = [x for t in lay['targets'] for x in t['texts']]
    for x in texts:
        for name, b in (('clean screenshot/frame', cf), ('annotated screenshot/frame', af)):
            if intersects(x['box'], b):
                problems.append(f'label "{x["text"]}" intersects the {name}')
        if not inside(x['box'], SAFE):
            problems.append(f'label "{x["text"]}" outside safe area')
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            if intersects(texts[i]['box'], texts[j]['box']):
                problems.append(f'label "{texts[i]["text"]}" intersects "{texts[j]["text"]}"')
    rects = [(t['label'], m['type'], r) for t in lay['targets'] for m in t['marks'] for r in m['casing_rects']]
    for lbl, typ, r in rects:
        if not (r[0] < r[2] and r[1] < r[3]) or not inside(r, SAFE):
            problems.append(f'{lbl} {typ} rect {r} degenerate or outside the safe area')
        if intersects(r, cf):
            problems.append(f'{lbl} {typ} mark {r} meets the clean screenshot or its frame')
        for x in texts:
            if intersects(r, x['box']):
                problems.append(f'{lbl} {typ} mark {r} intersects label "{x["text"]}"')
        if typ == 'outline' and not inside(r, ai):
            problems.append(f'{lbl} outline leaves the annotated screenshot')
    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            if rects[i][0] != rects[j][0] and intersects(rects[i][2], rects[j][2]):
                problems.append(f'{rects[i][0]} {rects[i][1]} touches {rects[j][0]} {rects[j][1]}')
    clear = af[0] - cf[2]
    for t in lay['targets']:
        if t['side'] == 'left' and t['rail_x'][0] - cf[2] < SBS_CLEAR:
            problems.append(f'{t["label"]} rail is closer than {SBS_CLEAR} px to the clean frame')
    assert not problems, problems
    return {'frames_do_not_overlap': True, 'frames_in_safe_area': True, 'labels_clear_of_both_screenshots_and_frames': True,
            'labels_in_safe_area': True, 'labels_clear_of_each_other': True, 'marks_clear_of_clean_screenshot_and_frame': True,
            'marks_clear_of_labels': True, 'marks_in_safe_area': True, 'outlines_inside_annotated_screenshot': True,
            'marks_of_different_targets_do_not_touch': True, 'gap_between_frames_px': clear, 'problems': problems}


# ---- composition ------------------------------------------------------------------------------------
def compose(images: list[dict], targets: list[dict], title: str) -> str:
    sv = SVG(BG, title)
    for im in images:
        sv.rect(im['x'] - PAD, im['y'] - PAD, im['w'] + 2 * PAD, im['h'] + 2 * PAD, PANEL, LINE, STROKE)   # mat and frame outside the image
        uri = 'data:image/png;base64,' + base64.b64encode(im['png']).decode('ascii')
        sv.raw(f'<image x="{im["x"]}" y="{im["y"]}" width="{im["w"]}" height="{im["h"]}" preserveAspectRatio="none" image-rendering="optimizeSpeed" '
               f'href="{uri}"><title>{html.escape(im["title"])}</title></image>')
    for layer, key in (('casing', 'casing_rects'), ('core', 'core_rects')):   # all casings first so gold joints stay continuous
        fill = CASING if layer == 'casing' else CORE
        for t in targets:
            for m in t['marks']:
                for r in m[key]:
                    sv.rect(r[0], r[1], r[2] - r[0], r[3] - r[1], fill)
    for t in targets:
        for x in t['texts']:
            sv.text(x['text'], x['x'], x['baseline'], x['size'], FG, True, anchor=x['anchor'])
    return sv.finish()


def image_record(im: dict, orig: dict, num: int, den: int, png: bytes, resampling: str) -> dict:
    return {'role': im['role'], 'x': im['x'], 'y': im['y'], 'w': im['w'], 'h': im['h'], 'scale_num': num, 'scale_den': den,
            'scale_x': im['w'] / orig['size'][0], 'scale_y': im['h'] / orig['size'][1], 'resampling': resampling,
            'crop': None, 'rotation_deg': 0, 'retouch': None, 'embedded_png_sha256': hashlib.sha256(png).hexdigest(),
            'embedded_png_bytes': len(png), 'frame_outer': im['frame_box'], 'annotated': im['role'] == 'annotated'}


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(description='Author the XTRA-05 sources.')
    ap.add_argument('--id', default=ID)
    assert ap.parse_args().id == ID, f'this authoring script belongs to {ID}'
    orig = load_original()
    scaled = resample(orig['rgb'])
    buf = io.BytesIO()
    scaled.save(buf, 'PNG', optimize=True)
    png15 = buf.getvalue()
    native = orig['raw']   # HIST-02 bytes, embedded unchanged at 1.0x
    assert Image.open(io.BytesIO(native)).convert('RGB').tobytes() == resample(orig['rgb'], 1, 1).tobytes()
    lay = layout(orig)
    checks = check(lay)
    sbs = layout_sbs(orig)
    checks_sbs = check_sbs(sbs)
    for name in ('exports', 'evidence', 'proofs'):   # render_assets.py writes into these
        (ASSET / name).mkdir(parents=True, exist_ok=True)

    t15 = 'HIST-02: Microsoft Visual Basic 4.0 (32-bit) IDE, whole screenshot at 1.5x'
    t10 = 'HIST-02: Microsoft Visual Basic 4.0 (32-bit) IDE, whole screenshot at native 1.0x'
    im15 = {'role': 'clean', 'x': lay['X'], 'y': lay['Y'], 'w': lay['iw'], 'h': lay['ih'], 'img_box': lay['img_box'], 'frame_box': lay['frame_box'], 'png': png15, 'title': t15}
    im15a = dict(im15, role='annotated')
    imc = dict(sbs['clean'], png=native, title=t10 + ' (clean)')
    ima = dict(sbs['annotated'], png=native, title=t10 + ' (annotated)')
    svgs = {'clean-workspace': compose([im15], [], 'VB4 IDE: whole HIST-02 screenshot, framed, no annotation'),
            'five-callouts': compose([im15a], lay['targets'], 'VB4 IDE anatomy: ' + ', '.join(LABELS)),
            'side-by-side': compose([imc, ima], sbs['targets'], 'VB4 IDE side by side: clean screenshot and ' + ', '.join(LABELS))}
    assert POSTER in svgs
    for name, svg in svgs.items():
        (HERE / f'variant-{name}.svg').write_text(svg, encoding='utf-8', newline='\n')

    edits = []
    n = 0
    for variant, targets, X, Y, s, ib in (('five-callouts', lay['targets'], lay['X'], lay['Y'], lay['scale'], lay['img_box']),
                                          ('side-by-side', sbs['targets'], sbs['annotated']['x'], sbs['annotated']['y'], 1.0, sbs['annotated']['img_box'])):
        for t in targets:
            for m in t['marks']:
                for layer, key, colour in (('casing', 'casing_rects', CASING), ('core', 'core_rects', CORE)):
                    for i, r in enumerate(m[key]):
                        n += 1
                        e = {'n': n, 'variant': variant, 'target': t['label'], 'mark': m['type'], 'layer': layer,
                             'shape': 'filled rectangle', 'canvas_rect_x0y0x1y1': r, 'colour': colour,
                             'overlays_original': overlay_record(r, X, Y, s, ib, orig['rgb'])}
                        if 'parts' in m:
                            e['part'] = m['parts'][i]
                        edits.append(e)

    rec15 = {k: image_record(dict(im15, role=role), orig, SCALE_NUM, SCALE_DEN, png15, RESAMPLE_NAME) for k, role in (('clean', 'clean'), ('annotated', 'annotated'))}
    rec_sbs = [image_record(imc, orig, 1, 1, native, NATIVE_NAME), image_record(ima, orig, 1, 1, native, NATIVE_NAME)]
    record = {
        'id': ID, 'canvas': [W, H], 'safe_area': list(SAFE),
        'coordinates': 'canvas pixels, origin top-left of the 1920x1080 export; rectangles are [x0, y0, x1, y1) half-open. Original pixel ranges are inclusive, origin top-left of the 800x600 original.',
        'source': {'asset': 'HIST-02', 'file': f'assets/historical/HIST-02/{SRC_REL}', 'rel_path': f'../../historical/HIST-02/{SRC_REL}',
                   'sha256': orig['sha256'], 'bytes': orig['bytes'], 'mode': orig['mode'], 'size': orig['size']},
        'labels': {'authority': 'War/SCRIPT.md VISUAL cue (working script, the narrative authority)', 'path': CUE['path'], 'line': CUE['line'],
                   'cue_text': CUE['text'], 'script_sha256_at_build': CUE['sha256'], 'labels_in_cue_order': LABELS, 'by_panel': CUE['by_panel'],
                   'parse_rule': 'the single line containing "VB4 IDE with labeled callouts"; the comma-separated list after "labeled callouts:"; exactly five; each must contain its panel word (form, toolbox, propert, code, project) in cue order',
                   'ticket_copy': TICKET_COPY, 'differs_from_ticket_copy': [[a, b] for a, b in zip(TICKET_COPY, LABELS) if a != b]},
        'placement': {'x': lay['X'], 'y': lay['Y'], 'w': lay['iw'], 'h': lay['ih'], 'scale_x': lay['iw'] / orig['size'][0], 'scale_y': lay['ih'] / orig['size'][1],
                      'resampling': RESAMPLE_NAME, 'crop': None, 'rotation_deg': 0, 'retouch': None,
                      'embedded_png_sha256': hashlib.sha256(png15).hexdigest(), 'embedded_png_bytes': len(png15),
                      'frame_outer': lay['frame_box'], 'identical_in_variants': ['clean-workspace', 'five-callouts']},
        'side_by_side': {'scale': 1.0, 'resampling': NATIVE_NAME, 'embedded_png_sha256': orig['sha256'],
                         'clean': {k: sbs['clean'][k] for k in ('x', 'y', 'w', 'h', 'img_box', 'frame_box')},
                         'annotated': {k: sbs['annotated'][k] for k in ('x', 'y', 'w', 'h', 'img_box', 'frame_box')},
                         'gap_between_frames_px': sbs['gap_between_frames_px'], 'spare_px': sbs['spare_px'], 'rails': sbs['rails'],
                         'width_used': [sbs['clean']['frame_box'][0], max(t['rail_x'][1] for t in sbs['targets'] if t['side'] == 'right')],
                         'why_1x': 'Two whole 800 px screenshots plus frames, gutters and rails fill the 1680 px safe width at exactly 1.0x; no larger scale fits both, and 1.0x needs no resampling, so every pixel of the pixel fonts is the original.'},
        'frame': {'mat_px': PAD, 'stroke_px': STROKE, 'extent_outside_image_px': OUT, 'mat_fill': PANEL, 'stroke': LINE, 'background': BG},
        'label_style': {'font': 'Liberation Sans Bold', 'size_px': LABEL_PX, 'leading': LEAD, 'fill': FG, 'metrics': lay['label_metrics'],
                        'line_breaks': 'five-callouts: multi-word labels are stacked one word per line; the words, spelling and capitalisation are the War/SCRIPT.md cue'},
        'label_style_side_by_side': {'font': 'Liberation Sans Bold', 'size_px': SBS_LABEL_PX, 'fill': FG, 'metrics': sbs['label_metrics'],
                                     'placement': f'one line each in a strip below the annotated screenshot; left-group labels start {SBS_INSET} px inside its left edge, right-group labels end {SBS_INSET} px inside its right edge; row pitch {SBS_PITCH} px'},
        'mark_style': {'thickness_px': TK, 'core': CORE, 'core_px': TK - 2, 'casing': CASING, 'casing_px': 1,
                       'outline_position': 'inside each target window outer boundary, so the outline covers only that window\'s outer frame bevel (about 3.3 original px)',
                       'leader_position': 'horizontal, on an original row that is desktop teal between the image edge and the target'},
        'mark_style_side_by_side': {'thickness_px': SBS_TK, 'core': CORE, 'core_px': SBS_TK - 2, 'casing': CASING, 'casing_px': 1,
                                    'outline_position': 'inside each target window outer boundary: 4 original px, the Win95 outer frame band',
                                    'leader_position': 'exit: horizontal over desktop teal rows (leader_y-2 .. leader_y+1) from the target to the image edge; rail: vertical in the dark gutter outside the image; run: horizontal below the screenshot to the label',
                                    'rail_offset_px': SBS_OFF, 'rail_pitch_px': SBS_SPACING, 'occlusion_gap_px': SBS_GAP},
        'targets': lay['targets'],
        'targets_side_by_side': sbs['targets'],
        'annotation_edits': edits,
        'build_checks': {'five-callouts': checks, 'side-by-side': checks_sbs},
        'poster': POSTER,
        'variants': {
            'clean-workspace': {'svg': 'src/variant-clean-workspace.svg', 'png': 'exports/clean-workspace.png', 'annotated': False,
                                'images': [rec15['clean']], 'targets': None},
            'five-callouts': {'svg': 'src/variant-five-callouts.svg', 'png': 'exports/five-callouts.png', 'annotated': True,
                              'images': [rec15['annotated']], 'targets': 'targets', 'label_lines': 'split'},
            'side-by-side': {'svg': 'src/variant-side-by-side.svg', 'png': 'exports/side-by-side.png', 'annotated': True,
                             'images': rec_sbs, 'targets': 'targets_side_by_side', 'label_lines': 'whole'},
        },
    }
    record['variants'][POSTER]['also_rendered_as'] = 'exports/poster.png'
    (HERE / 'layout.json').write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    (HERE / 'copy.txt').write_text('\n'.join(LABELS) + '\n', encoding='utf-8', newline='\n')
    (HERE / 'brief.json').write_text(json.dumps({k: ROW[k] for k in ['id', 'title', 'brief', 'requirements', 'beats', 'checks', 'copy', 'refs', 'gates', 'deps', 'variants']}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    script = ROOT / 'sources' / 'SCRIPT.md'
    sources = [{'path': '../../../sources/SCRIPT.md', 'lines': [130, 134], 'sha256': hashlib.sha256(script.read_bytes()).hexdigest(),
                'relationship': 'source creative brief (VISUAL cue at 130, IDE narration at 132); its callout list is superseded by the working script below'},
               {'path': '../../../War/SCRIPT.md', 'lines': [CUE['line'], CUE['line']], 'sha256': CUE['sha256'],
                'relationship': 'label authority: the five callout labels are read from this VISUAL cue at build time (working script, narrative authority)'},
               {'path': record['source']['rel_path'], 'asset': 'HIST-02', 'sha256': orig['sha256'],
                'relationship': 'historical original from a produced upstream asset; read in place; whole image uniformly scaled 1.5x (clean-workspace, five-callouts) or embedded byte-identical at 1.0x (side-by-side); never cropped or copied'}]
    notes = [
        'Whole HIST-02 screenshot (WinWorld "Microsoft Visual Basic 4.0 32 bit - Edit", 800x600) in every variant; no crop, rotation, stretch, retouch or zoom-in. Mat and frame sit outside the image edges.',
        'clean-workspace: framed screenshot at 1.5x (1200x900, Pillow BOX); nothing is drawn over its pixels.',
        'five-callouts: same placement; the five labels sit in the side margins, outside the screenshot. Only 5 px outlines on each target window\'s own frame and horizontal leaders over empty desktop cross onto the image.',
        'side-by-side: clean screenshot left, annotated screenshot right, both whole at native 1.0x (the HIST-02 PNG bytes, no resampling). 4 px outlines on window frames and leaders over desktop teal; rails in the dark gutters lead to a label strip below the annotated side. Every mark and the original pixels it covers: src/layout.json annotation_edits.',
        f'Labels are read from the {SCRIPT_REL}:{CUE["line"]} VISUAL cue ({", ".join(LABELS)}); the ticket copy said "Project Explorer" and was overridden by the working script (writing change, Devin 2026-09-15).',
        f'Poster: {POSTER} (decision and reason in qa.md).',
        'No on-screen credit: HIST-02 rights.json has credit_text null, and its proposed credit ("... Used with permission from Microsoft.") must not be used before RQ-HIST-02-1 is decided. The proposed credit is carried in delivery.json credits, marked proposed.',
        'Release blocked under R03 and R14 until the review deck decides; internal proof only.',
    ]
    frames = [{'time': 0, 'file': f'variant-{POSTER}.svg'}]
    timeline = {'id': ID, 'durationSeconds': None, 'fps': None, 'width': W, 'height': H, 'beats': ROW['beats'], 'frames': frames, 'cuts': {},
                'variant_names': list(svgs), 'poster': POSTER,
                'motion_model': 'Still asset: each variant is a separate still held for editorial timing. The one-panel-at-a-time reveal is editor-request only and was not built.'}
    (HERE / 'timeline.json').write_text(json.dumps(timeline, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    build = {'id': ID, 'duration': None, 'frames': frames, 'variants': {n: f'variant-{n}.svg' for n in svgs}, 'poster': f'variant-{POSTER}.svg',
             'cuts': {}, 'notes': notes, 'sources': sources, 'kind': ROW['kind']}
    (HERE / 'build.json').write_text(json.dumps(build, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    table = {f'variant-{n}.svg': v for n, v in svgs.items()}
    # Same deterministic, offline HTML contract as tools/render/build_assets.py (still: time zero = poster variant).
    doc = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(ROW['title']) + '</title>'
           '<style>html,body{margin:0;background:#000;height:100%;overflow:hidden}#stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center}svg{width:100%;height:100%;object-fit:contain}</style>'
           '<div id="stage" aria-label="' + html.escape(ROW['title'], quote=True) + '"></div><script>const timeline=' + json.dumps(timeline, ensure_ascii=False) + ';const scenes=' + json.dumps(table, ensure_ascii=False) + ';'
           "const stage=document.getElementById('stage');window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,variants:Object.keys(scenes),"
           'renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;else break}stage.innerHTML=scenes[f.file];return f.file},'
           'showVariant(n){stage.innerHTML=scenes["variant-"+n+".svg"];return n}};'
           "__ASSET__.renderAt(0);document.addEventListener('keydown',e=>{if(e.code==='Home')__ASSET__.renderAt(0)});</script></html>")
    (HERE / 'index.html').write_text(doc, encoding='utf-8', newline='\n')
    print('labels from', f'{SCRIPT_REL}:{CUE["line"]}', LABELS)
    for t in lay['targets']:
        print('five-callouts', t['label'], 'canvas', t['canvas_box'], 'leader row', t['leader_row_canvas'], 'text', [x['box'] for x in t['texts']])
    print('five-callouts placement', lay['X'], lay['Y'], lay['iw'], lay['ih'], 'spare', round(lay['spare_px'], 1))
    for t in sbs['targets']:
        print('side-by-side', t['label'], 'canvas', t['canvas_box'], 'rail', t['rail_x'], 'row', t['label_row_canvas'], 'text', [x['box'] for x in t['texts']])
    print('side-by-side clean', sbs['clean']['img_box'], 'annotated', sbs['annotated']['img_box'], 'gap between frames', sbs['gap_between_frames_px'], 'spare', sbs['spare_px'])
    print('edits', len(edits), 'poster', POSTER)
    print('AUTHORED', ID, {n: len(v) for n, v in svgs.items()})


if __name__ == '__main__':
    main()
