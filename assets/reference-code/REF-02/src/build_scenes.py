#!/usr/bin/env python3
"""REF-02 revision 2: regenerate this asset's scene SVGs, variants, build.json, timeline.json
and index.html from src/excerpt.c and src/hello.def, using tools/render/studio.py read-only.

  python assets/reference-code/REF-02/src/build_scenes.py              # scenes, build.json, timeline.json, index.html
  python tools/render/render_assets.py --id REF-02                     # PNG/MP4/keyframes/contact sheet (CairoSVG + ffmpeg)
  python tools/render/qa_browser.py --id REF-02                        # evidence/browser-tests.json
  python assets/reference-code/REF-02/src/build_scenes.py --inventory  # delivery.json from the finished files

This script replaces tools/render/build_assets.py for REF-02 only: that script still reads the
revision-1 fixture in tools/fixtures and would overwrite these sources if run with --id REF-02.
"""
from __future__ import annotations
import argparse, hashlib, html, json, math, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # .../assets/reference-code/REF-02/src
BASE = HERE.parent
ROOT = BASE.parents[2]
sys.path.insert(0, str(ROOT / 'tools/render'))
from studio import SVG, BG, FG, MUTED, LINE, BLUE, GOLD, GREEN, code_line, width  # noqa: E402

ID = 'REF-02'
LABEL = 'Representative Windows 3.x C (Win16)'
NOTE = 'The message loop: get a message, translate it, dispatch it to WndProc.'
FOCUS = ('while (GetMessage', 'DispatchMessage')   # the focus band runs from the first to one row past the second
VISIBLE = 16          # whole rows in the code panel
SIZE = 30             # code font size; 25 for line numbers
PITCH = SIZE * 1.27   # 38.1 px per row
SUB = 3               # scroll sub-steps per row (one third of a row per state)
STEP = 0.1            # seconds per sub-step: three 30 fps frames; 0.3 s per row = 3.33 rows/s
HOLD_OPEN = 2.0       # opening hold on the first viewport
HOLD_END = 0.6        # hold on the last viewport before the focus cut
HOLD_FOCUS = 3.5      # closing hold on the message-loop focus
CLIP = (125, 290, 1675, 615)   # x, y, w, h of the scrolling viewport inside the panel


def rows_of(files):
    rows = []
    for k, (name, language, lines) in enumerate(files):
        rows += ([None] if k else []) + [(n, language, line) for n, line in enumerate(lines, 1)]
    return rows


def comment_state(lines):
    """Per line: True when the line starts inside an unclosed /* block comment (studio's tokenizer
    only colours one-line comments, so continuation lines are drawn green here)."""
    out = []; inside = False
    for line in lines:
        out.append(inside)
        i = 0
        while i < len(line):
            if inside:
                j = line.find('*/', i)
                if j < 0: break
                inside = False; i = j + 2
            else:
                j = line.find('/*', i)
                if j < 0: break
                inside = True; i = j + 2
    return out


def draw_code(s, line, x, y, language, cont):
    cw = width('0', SIZE, 'mono')
    if cont:
        s.text(line, x, y, SIZE, GREEN, mono=True); return
    if '/*' in line and '*/' not in line[line.index('/*'):]:
        j = line.index('/*')
        end = code_line(s, line[:j], x, y, SIZE, language) if j else x
        s.text(line[j:], end, y, SIZE, GREEN, mono=True); return
    code_line(s, line, x, y, SIZE, language)


def listing(brief, files, rows, cont, top=0.0, focus=None, note=None):
    s = SVG(BG, brief['title'])
    s.text('   '.join(f'{f[0]} ({len(f[2])} lines)' for f in files), 120, 117, 32, MUTED, mono=True)
    s.text(LABEL, 1800, 117, 28, BLUE, anchor='end')
    s.line(120, 147, 1800, 147, LINE, 2); s.text(brief['copy'], 120, 210, 46, FG, True)
    s.rect(120, 247, 1680, 673, '#151a20'); s.rect(120, 247, 5, 673, BLUE)
    cx, cy, cw, ch = CLIP
    s.raw(f'<clipPath id="view"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}"/></clipPath><g clip-path="url(#view)">')
    first = max(0, math.floor(top))
    for i in range(first, min(len(rows), first + VISIBLE + 2)):
        y = 320 + (i - top) * PITCH
        row = rows[i]
        if row is None:
            s.line(207, y - 11, 1760, y - 11, LINE, 2); continue
        n, language, line = row
        if focus and focus[0] <= i <= focus[1]: s.rect(130, y - SIZE + 1, 1660, PITCH, '#263c58')
        s.text(str(n), 163, y, 25, '#748293', mono=True, anchor='middle')
        if language: draw_code(s, line, 207, y, language, cont[i])
        else: s.text(line, 207, y, SIZE, FG, mono=True)
    s.raw('</g>')
    if note: s.text(note, 150, 982, 34, GOLD)   # the line counts sit in the header so the caption has the footer to itself
    return s.finish()


def build():
    brief = json.loads((HERE / 'brief.json').read_text(encoding='utf-8'))
    old = json.loads((HERE / 'build.json').read_text(encoding='utf-8'))
    hello = (HERE / 'excerpt.c').read_text(encoding='utf-8').splitlines()
    module = (HERE / 'hello.def').read_text(encoding='utf-8').splitlines()
    assert len(hello) == 73, f'hello.c must stay 73 lines as narrated; it is {len(hello)}'
    files = [('hello.c', 'c', hello), ('hello.def', None, module)]
    rows = rows_of(files)
    cont = [False] * len(rows)
    for i, flag in zip(range(len(hello)), comment_state(hello)): cont[i] = flag
    cw = width('0', SIZE, 'mono')
    longest = max(len(r[2]) for r in rows if r)
    assert 207 + longest * cw <= 1760, f'longest line ({longest} chars) leaves the panel'
    last = len(rows) - VISIBLE
    at = lambda text: next(i for i, row in enumerate(rows) if row and text in row[2])
    focus = (at(FOCUS[0]), at(FOCUS[1]) + 1)
    top = min(last, max(0, focus[0] - (VISIBLE - (focus[1] - focus[0] + 1)) // 2))
    clean = listing(brief, files, rows, cont)
    hi = listing(brief, files, rows, cont, top, focus, NOTE)
    frames = [(0, clean)]
    for k in range(1, last * SUB + 1):
        frames.append((round(HOLD_OPEN + k * STEP, 6), listing(brief, files, rows, cont, k / SUB)))
    scroll_end = round(HOLD_OPEN + last * SUB * STEP, 6)
    focus_at = round(scroll_end + HOLD_END, 6)
    duration = round(focus_at + HOLD_FOCUS, 6)
    scroll_seconds = round(last * SUB * STEP, 6)
    frames.append((focus_at, hi))
    notes = [
        'Revision 2 (2026-09-16, Devin review note 5): hello.c is now a complete, agent-authored Windows 3.x (Win16) Hello World of exactly 73 lines, as War/SCRIPT.md narrates; hello.def (11 lines) is shown separately after a rule and is not part of the 73.',
        'API sequence: WinMain(HANDLE, HANDLE, LPSTR, int); WNDCLASS filled field by field and RegisterClass on the first instance only; CreateWindow; ShowWindow; UpdateWindow; the GetMessage/TranslateMessage/DispatchMessage loop; long FAR PASCAL __export WndProc with WM_PAINT (BeginPaint/TextOut/EndPaint), WM_DESTROY (PostQuitMessage) and DefWindowProc. Parameter spellings (UINT message, UINT wParam, LONG lParam) follow the Windows 3.1 SDK windows.h.',
        'Authored in period style for this production; not copied from a book listing or tutorial and not recovered from a historical source.',
        'Not compiled: no 16-bit Windows toolchain (Microsoft C 6/7 + Windows 3.1 SDK) is installed on the production machine. The listing was read line by line against the Windows 3.1 SDK API; see qa.md. Technical and era review stays open under R15; R03 also applies.',
        'Line numbers restart in each file, the rule, the focus band, the caption and the line-count header are display layers; src/excerpt.c and src/hello.def hold the exact text.',
        f'Timing: a {HOLD_OPEN:g} s hold on the first {VISIBLE} rows, then a scroll of one third of a row every {STEP:g} s (0.3 s per row, 3.33 rows/s, under the 4 rows/s ceiling) through all {len(rows)} rows ({last} row steps, {scroll_seconds:g} s, ending at {scroll_end:g} s), a {HOLD_END:g} s hold on the last viewport, then the message-loop focus from {focus_at:g} s to {duration:g} s.',
        'src/build_scenes.py regenerates these sources; tools/render/build_assets.py --id REF-02 would overwrite them with the revision-1 fixture and must not be run for this ticket.',
    ]
    # Dedup identical states, name them in order, write them, and drop the previous revision's scene files.
    for old_scene in HERE.glob('scene-*.svg'): old_scene.unlink()
    names = []; dedup = {}
    for t, svg in frames:
        sha = hashlib.sha256(svg.encode()).hexdigest()
        if sha not in dedup:
            n = f'scene-{len(dedup):04}.svg'; dedup[sha] = n; (HERE / n).write_text(svg, encoding='utf-8', newline='\n')
        names.append({'time': t, 'file': dedup[sha]})
    (HERE / 'scene.svg').write_text(hi, encoding='utf-8', newline='\n')
    vmap = {}
    for name, svg in {'clean': clean, 'teaching-focus': hi}.items():
        path = f'variant-{name}.svg'; (HERE / path).write_text(svg, encoding='utf-8', newline='\n'); vmap[name] = path
    table = {n: (HERE / n).read_text(encoding='utf-8') for n in dedup.values()}
    timeline = {'id': ID, 'durationSeconds': duration, 'fps': 30, 'width': 1920, 'height': 1080, 'beats': brief['beats'], 'frames': names, 'cuts': {}, 'variant_names': list(vmap),
                'motion_model': 'Explicit deterministic step states with readable holds; MP4 encodes the same scene changes at 30 fps.',
                'revision': 2, 'scroll': {'rows': len(rows), 'visible_rows': VISIBLE, 'row_steps': last, 'substeps_per_row': SUB, 'seconds_per_substep': STEP, 'rows_per_second': round(1 / (SUB * STEP), 3), 'start': HOLD_OPEN, 'end': scroll_end, 'focus_at': focus_at}}
    (HERE / 'timeline.json').write_text(json.dumps(timeline, indent=2, ensure_ascii=False), encoding='utf-8', newline='\n')
    # Same offline player as tools/render/build_assets.py: every state inlined, deterministic renderAt(seconds).
    html_doc = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>''' + html.escape(brief['title']) + '''</title><style>html,body{margin:0;background:#000;height:100%;overflow:hidden}#stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center}svg{width:100%;height:100%;object-fit:contain}</style><div id="stage" aria-label="''' + html.escape(brief['title'], quote=True) + '''"></div><script>const timeline=''' + json.dumps(timeline, ensure_ascii=False) + ''';const scenes=''' + json.dumps(table, ensure_ascii=False) + ''';const stage=document.getElementById('stage');window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;else break}stage.innerHTML=scenes[f.file];return f.file}};__ASSET__.renderAt(0);let start=null,playing=false;document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();playing=!playing;start=null;requestAnimationFrame(tick)}if(e.code==='Home'){playing=false;__ASSET__.renderAt(0)}});function tick(ts){if(!playing)return;if(start===null)start=ts;const t=(ts-start)/1000;__ASSET__.renderAt(t);if(t<__ASSET__.durationSeconds)requestAnimationFrame(tick);else playing=false}</script></html>'''
    (HERE / 'index.html').write_text(html_doc, encoding='utf-8', newline='\n')
    build = {'id': ID, 'duration': duration, 'frames': names, 'variants': vmap, 'poster': 'scene.svg', 'cuts': {}, 'notes': notes, 'sources': old['sources'], 'kind': 'motion'}
    (HERE / 'build.json').write_text(json.dumps(build, indent=2, ensure_ascii=False), encoding='utf-8', newline='\n')
    print('AUTHORED', ID, len(dedup), 'states', 'duration', duration, 'scroll', scroll_seconds, 's', 'focus rows', focus, 'top', top, flush=True)


def inventory():
    """delivery.json for the finished package (mirrors tools/render/finish_delivery.py, which is not run
    for a revision because it also rewrites the ticket document and review/ index outside this folder)."""
    from finish_delivery import capabilities, output_inventory, VERSION
    from paths import ROWS
    row = ROWS[ID]
    data = json.loads((HERE / 'build.json').read_text(encoding='utf-8'))
    br = json.loads((BASE / 'evidence/browser-tests.json').read_text(encoding='utf-8')); assert not br['errors'], br['errors']
    rt = json.loads((BASE / 'evidence/render-tests.json').read_text(encoding='utf-8'))
    prov = json.loads((BASE / 'evidence/provenance.json').read_text(encoding='utf-8'))
    state = json.loads((BASE / 'state.json').read_text(encoding='utf-8'))
    manual = json.loads((BASE / 'proofs/manual-review.json').read_text(encoding='utf-8'))
    cap = capabilities(); cap['browser_note'] = 'HTML tested by in-memory content loading.'
    cap['chromium'] = br['browser'].removeprefix('installed ')
    cap['win16_toolchain'] = None
    tests = [
        {'test': 'required outputs and checksums', 'result': 'python tools/validate_delivery.py --id REF-02 run after this inventory; result recorded in qa.md.'},
        {'test': 'line count of src/excerpt.c', 'result': f"{len((HERE / 'excerpt.c').read_text(encoding='utf-8').splitlines())} lines (wc -l and Python splitlines agree); hello.def {len((HERE / 'hello.def').read_text(encoding='utf-8').splitlines())} lines"},
        {'test': 'Win16 API read-through (no compiler)', 'result': 'Read line by line against the Windows 3.1 SDK by the producing agent; the checklist is in qa.md. No 16-bit toolchain is installed, so nothing was compiled or run.'},
        {'test': 'manual visual review', 'result': manual},
        {'test': 'raster dimensions and video codec/fps/duration', 'evidence': 'evidence/render-tests.json', 'result': 'passed: ' + ', '.join(f"{p['file']} {p['probe']['streams'][0]['codec_name']} {p['probe']['streams'][0]['width']}x{p['probe']['streams'][0]['height']} {p['probe']['streams'][0]['r_frame_rate']} {p['probe']['streams'][0]['nb_frames']} frames {p['probe']['format']['duration']} s" for p in rt['video_probes'])},
        {'test': 'offline HTML, deterministic seek, every SVG text bounding box', 'evidence': 'evidence/browser-tests.json', 'result': f"passed: {br['svg_files_checked']} SVG files, {br['text_boxes_checked']} text boxes, offline={br['offline']}, deterministic_seek={br['deterministic_seek']}"},
    ]
    variants = [{'name': name, 'files': [f'exports/{name}.png', f'src/variant-{name}.svg']} for name in data['variants']]
    delivery = {'id': ID, 'title': row['title'], 'production_status': state['production_status'], 'release_status': state['release_status'],
                'provenance_type': prov['classification'], 'shared_version': VERSION, 'duration_seconds': data['duration'],
                'dimensions': {'width': 1920, 'height': 1080}, 'fps': 30, 'outputs': output_inventory(BASE), 'variants': variants,
                'sources': data['sources'], 'credits': [{'type': 'original graphics', 'credit': 'Source-based vector graphics and agent-authored representative code for this production; no third-party images, code listings or font files included.'}],
                'tests': tests, 'unresolved_gates': row['gates'], 'toolchain': cap,
                'notes': data['notes'] + ['Original ticket requirements retained; these exports are not producer publication approval.', 'Revision 2 exports replace the revision-1 package (63-line excerpt) in full; every file in this folder was regenerated on 2026-09-16.']}
    (BASE / 'delivery.json').write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    print('INVENTORIED', ID, len(delivery['outputs']), 'outputs', flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--inventory', action='store_true', help='Write delivery.json from the rendered, browser-checked package instead of building scenes.')
    args = ap.parse_args()
    inventory() if args.inventory else build()
