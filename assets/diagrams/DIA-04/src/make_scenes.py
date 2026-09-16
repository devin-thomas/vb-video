#!/usr/bin/env python3
"""DIA-04 revision 2: a code-driven ByVal / ByRef demonstration.

Writes scene-000N.svg, variant-*.svg, scene.svg (poster), build.json, timeline.json
and index.html into this folder. It only reads tools/render/studio.py for the shared
colour roles, fonts and code colouring. Run from the repository root:

    python assets/diagrams/DIA-04/src/make_scenes.py
    python tools/render/render_assets.py --id DIA-04

The Integer example (x = 5, Bump adds one) is an authored teaching example, not
supplied code. Nothing here depicts, or claims anything about, arrays.
"""
from __future__ import annotations
import html, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'tools' / 'render'))
from studio import SVG, BG, PANEL, FG, MUTED, LINE, BLUE, GOLD, GREEN, width, code_line  # noqa: E402

ID = 'DIA-04'
TITLE = 'ByRef versus ByVal: caller variable and local parameter'
DURATION = 10
FPS = 30
# Step start times in seconds; the last state holds to the end.
STEP_TIMES = [0, 1.5, 3.0, 4.5, 6.0, 7.5]
INK = '#111820'      # value-box fill, as the DIA family's inner boxes
HILITE = '#263c58'   # studio's code focus colour

VB_VAL = ['Sub Bump(ByVal n As Integer)', '    n = n + 1', 'End Sub', '', 'x = 5', 'Bump(x)']
VB_REF = ['Sub Bump(ByRef n As Integer)', '    n = n + 1', 'End Sub', '', 'x = 5', 'Bump(x)']
CPP_VAL = ['void bump(int n) {', '    n = n + 1;', '}', '', 'int x = 5;', 'bump(x);']
CPP_REF = ['void bump(int& n) {', '    n = n + 1;', '}', '', 'int x = 5;', 'bump(x);']
# Six-line listings: which line runs at each step.
FOCUS6 = {0: 4, 1: 5, 2: 0, 3: 1, 4: 2, 5: None}
# Compact C++ rows share one `int x = 5;` line above them.
CPP_VAL4 = ['void bump(int n) {', '    n = n + 1;', '}', 'bump(x);']
CPP_REF4 = ['void bump(int& n) {', '    n = n + 1;', '}', 'bump(x);']
FOCUS4 = {0: None, 1: 3, 2: 0, 3: 1, 4: 2, 5: None}

NOTES = {
    'val': ['x holds 5', '{call} is called with x', 'n gets a copy of the value 5',
            'n becomes 6; x is untouched', 'the copy n is thrown away', 'x is still 5'],
    'ref': ['x holds 5', '{call} is called with x', 'n is another name for x',
            'n = n + 1 changes x to 6', 'n goes away; x keeps 6', 'x is now 6'],
}


def box(s, x, y, w, h, value, stroke, vs, color=FG, opacity=1.0, dashed=False):
    if opacity != 1:
        s.raw(f'<g opacity="{opacity}">')
    dash = ' stroke-dasharray="12 9"' if dashed else ''
    s.raw(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="4" fill="{INK}" stroke="{stroke}" stroke-width="3"{dash}/>')
    s.text(value, x + w / 2, y + h / 2 + vs * .36, vs, color, True, True, 'middle')
    if opacity != 1:
        s.raw('</g>')


def pointer(s, x, y, size):
    # Current-line marker in the code block's own left margin; never over text.
    s.path(f'M{x:.2f} {y - size * .78:.2f} L{x + size * .42:.2f} {y - size * .36:.2f} L{x:.2f} {y + size * .06:.2f} Z', GOLD, 2, GOLD)


def code_block(s, lines, x, y, w, cs, lead, lang, focus):
    """Code with a full-line highlight behind the running line. Returns the next free y."""
    cx = x + 30
    for i, line in enumerate(lines):
        yy = y + i * lead
        if line:
            # Text starts 30 px in (after the marker) and keeps 20 px clear of the right edge.
            assert width(line, cs, 'mono') <= w - 50, (line, cs, w)
        if i == focus:
            s.rect(x + 8, yy - cs + 2, w - 16, cs + 14, HILITE, rx=3)
            pointer(s, x + 12, yy, cs)
        if line:
            code_line(s, line, cx, yy, cs, lang)
    return y + (len(lines) - 1) * lead


def values(s, mode, step, bx, nx, by, bw, bh, vs, ls, was=True, short=False):
    """Draw x's box, and n's box (ByVal) or n's back-pointing tag (ByRef) for this step.
    Labels sit above the boxes; the copy / same-variable captions sit in the gap between them."""
    changed = mode == 'ref' and step >= 3
    s.text('x  caller' if short else 'x  (the caller’s variable)', bx, by - 16, ls, MUTED)
    box(s, bx, by, bw, bh, 6 if changed else 5, BLUE, vs, GREEN if changed else FG)
    if changed and was:
        s.text('was 5', bx + bw / 2, by + bh + ls + 14, ls, MUTED, anchor='middle')
    if step < 2:
        return
    dim = step >= 4
    mid = by + bh / 2
    gap_mid = (bx + bw + nx) / 2
    cap = max(18, ls - 4)
    if mode == 'val':
        s.text('n  copy' if short else 'n  (a copy)', nx, by - 16, ls, GOLD if not dim else MUTED)
        box(s, nx, by, bw, bh, 6 if step >= 3 else 5, GOLD, vs, GREEN if step >= 3 else FG, .38 if dim else 1)
        if step == 2:
            s.arrow(bx + bw + 14, mid, nx - 14, mid, GOLD, 5)
            s.text('copy', gap_mid, mid - 16, cap, GOLD, anchor='middle')
        elif step == 3 and was:
            s.text('was 5', nx + bw / 2, by + bh + ls + 14, ls, MUTED, anchor='middle')
        if dim:
            s.line(nx - 6, by + bh + 6, nx + bw + 6, by - 6, GOLD, 4)
            s.text('discarded', nx + bw / 2, by + bh + ls + 14, ls, GOLD, anchor='middle')
    else:
        s.raw(f'<g opacity="{.38 if dim else 1}">')
        s.text('n  reference' if short else 'n  (a reference)', nx, by - 16, ls, GOLD if not dim else MUTED)
        th = round(bh * .62)
        box(s, nx, mid - th / 2, bw, th, 'n', GOLD, round(vs * .72), GOLD, dashed=True)
        s.arrow(nx - 14, mid, bx + bw + 14, mid, GOLD, 5)
        label = 'same x' if short else 'same variable'
        assert width(label, cap, 'sans') <= nx - (bx + bw) - 8, (label, cap)
        s.text(label, gap_mid, mid + cap + 12, cap, GOLD, anchor='middle')
        s.raw('</g>')


def panel(s, x, y, w, h, lines, lang, mode, step, focus_map, *, title=None, sub=None,
          cs=32, bw=180, bh=110, vs=60, rs=42, ls=26, ns=28, side=False, call='Bump(x)', was=True):
    s.rect(x, y, w, h, PANEL)
    cy = y + 60
    if title:
        s.text(title, x + 36, y + 72, 50, BLUE, True, True)
        cy = y + 118
    if sub:
        s.text(sub, x + 36, cy, ls, MUTED)
        cy += 30
    lead = round(cs * 1.32)
    code_y = cy + cs + 8
    code_w = w - 40 if not side else round(w * .47)
    last = code_block(s, lines, x + 20, code_y, code_w, cs, lead, lang, focus_map[step])
    if side:
        bx = x + 20 + code_w + 60
        nx = x + w - 40 - bw
        by = code_y + (last - code_y) / 2 - bh / 2 + 6
    else:
        bx = x + 40
        nx = x + w - 40 - bw
        by = last + 76
    values(s, mode, step, bx, nx, by, bw, bh, vs, ls, was)
    text = NOTES[mode][step].replace('{call}', call)
    ry = by + bh + (ls + 14 if was else 0) + rs + 20
    assert ry <= y + h - 24, ('result line leaves the panel', ry, y + h)
    if step == 5:
        s.text(text, bx, ry, rs, GOLD if mode == 'val' else GREEN, True)
    else:
        s.text(text, bx, ry, ns, MUTED)
    return by, ry


def cpp_column(s, x, y, w, h, step):
    """Compact third column: one shared `int x = 5;` line and two four-line rows."""
    s.rect(x, y, w, h, PANEL)
    s.text('C++', x + 36, y + 72, 50, BLUE, True, True)
    s.text('same idea: int copies, int& refers', x + 36, y + 118, 24, MUTED)
    cs, lead = 24, 30
    yy = y + 150
    if step == 0:
        s.rect(x + 28, yy - cs + 2, w - 56, cs + 14, HILITE, rx=3)
        pointer(s, x + 32, yy, cs)
    code_line(s, 'int x = 5;', x + 50, yy, cs, 'cpp')
    for k, (mode, lines) in enumerate([('val', CPP_VAL4), ('ref', CPP_REF4)]):
        top = y + 184 + k * 280
        last = code_block(s, lines, x + 20, top, w - 40, cs, lead, 'cpp', FOCUS4[step])
        bw, bh = 104, 56
        by = last + 54   # keeps the box labels clear of the running-line highlight
        values(s, mode, step, x + 40, x + w - 40 - bw, by, bw, bh, 36, 20, was=False, short=True)
        text = NOTES[mode][step].replace('{call}', 'bump(x)')
        if mode == 'val' and step == 4:
            text = 'copy thrown away'   # short form: the row is narrow and "discarded" sits under the box
        ry = by + bh + 44
        assert ry <= y + h - 24, ('C++ row leaves the panel', ry, y + h)
        if step == 5:
            s.text(text, x + 40, ry, 26, GOLD if mode == 'val' else GREEN, True)
        else:
            s.text(text, x + 40, ry, 22, MUTED)


SUB = 'One Integer, one Sub: a copy of the value versus the variable itself.'


def main_scene(step):
    s = SVG(BG, 'ByRef versus ByVal: Bump(x) by value and by reference')
    s.heading('ByRef versus ByVal', SUB)
    panel(s, 120, 240, 610, 740, VB_VAL, 'vb', 'val', step, FOCUS6, title='ByVal', sub='the Sub gets a copy of the value', cs=30)
    panel(s, 754, 240, 610, 740, VB_REF, 'vb', 'ref', step, FOCUS6, title='ByRef', sub='the Sub gets the variable itself', cs=30)
    cpp_column(s, 1388, 240, 412, 740, step)
    return s.finish()


def variant_vb(mode):
    s = SVG(BG, f'{"ByVal" if mode == "val" else "ByRef"}: Bump(x) with x = 5')
    if mode == 'val':
        s.heading('ByVal: the Sub gets a copy', SUB)
    else:
        s.heading('ByRef: the Sub gets the variable itself', SUB)
    panel(s, 120, 240, 1680, 740, VB_VAL if mode == 'val' else VB_REF, 'vb', mode, 5, FOCUS6,
          title='ByVal' if mode == 'val' else 'ByRef', cs=44, bw=240, bh=150, vs=86, rs=60, ls=32, ns=36, side=True)
    return s.finish()


def variant_cpp():
    s = SVG(BG, 'C++: bump(x) with int n and int& n')
    s.heading('C++: int n versus int& n', SUB)
    panel(s, 120, 240, 816, 740, CPP_VAL, 'cpp', 'val', 5, FOCUS6, title='int n', sub='by value: the function gets a copy',
          cs=32, bw=200, bh=120, vs=66, rs=48, ls=28, ns=30, call='bump(x)')
    panel(s, 984, 240, 816, 740, CPP_REF, 'cpp', 'ref', 5, FOCUS6, title='int& n', sub='by reference: the function gets x itself',
          cs=32, bw=200, bh=120, vs=66, rs=48, ls=28, ns=30, call='bump(x)')
    return s.finish()


def main():
    frames = []
    for i, t in enumerate(STEP_TIMES):
        name = f'scene-{i:04}.svg'
        (HERE / name).write_text(main_scene(i), encoding='utf-8', newline='\n')
        frames.append({'time': t, 'file': name})
    poster = main_scene(5)
    (HERE / 'scene.svg').write_text(poster, encoding='utf-8', newline='\n')
    variants = {'byval': variant_vb('val'), 'byref': variant_vb('ref'), 'cpp': variant_cpp()}
    vmap = {}
    for name, svg in variants.items():
        fn = f'variant-{name}.svg'
        (HERE / fn).write_text(svg, encoding='utf-8', newline='\n')
        vmap[name] = fn
    notes = [
        'Revision 2 (2026-09-16, Devin’s cut note 16): the diagram is replaced by a code-driven demonstration. Bump adds one to its parameter; x = 5 before the call; ByVal leaves x at 5, ByRef makes it 6. The C++ column shows int n versus int& n with the same outcome.',
        'The Bump / bump example is an authored teaching example, not supplied code. It shows one Integer only: nothing on screen claims or shows what ByVal does with an array (no automatic deep copy is depicted), and no historical default-passing statement appears. This caveat lives here and in qa.md, not on screen (producer decision 2026-09-16).',
        'Timing: steps at 0, 1.5, 3, 4.5, 6 and 7.5 s (x holds 5; the call; the parameter appears; n = n + 1 runs; the Sub ends; the result), and the result holds from 7.5 s to 10 s.',
        'Annotations (current-line marker, copy arrow, back-pointing reference arrow, labels) sit in the margins and value area, never over code text.',
    ]
    old = json.loads((HERE / 'build.json').read_text(encoding='utf-8'))
    build = {'id': ID, 'duration': DURATION, 'frames': frames, 'variants': vmap, 'poster': 'scene.svg', 'cuts': {},
             'notes': notes, 'sources': old['sources'], 'kind': 'motion'}
    (HERE / 'build.json').write_text(json.dumps(build, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    beats = [
        '0–1.5 s: three columns show the code; x holds 5 everywhere.',
        '1.5–3 s: the call line Bump(x) / bump(x) is the running line.',
        '3–4.5 s: entering the Sub: ByVal shows n as a copy of 5 beside x; ByRef shows n as a tag whose arrow points back at x. The C++ rows do the same for int n and int& n.',
        '4.5–6 s: n = n + 1 runs: the ByVal copy becomes 6 while x stays 5; under ByRef x itself becomes 6.',
        '6–7.5 s: End Sub: the ByVal copy is struck through and marked discarded; the ByRef tag fades.',
        '7.5–10 s: held result: "x is still 5" (ByVal) against "x is now 6" (ByRef), and the same pair in the C++ column.',
    ]
    timeline = {'id': ID, 'durationSeconds': DURATION, 'fps': FPS, 'width': 1920, 'height': 1080, 'beats': beats,
                'frames': frames, 'cuts': {}, 'variant_names': list(vmap),
                'motion_model': 'Explicit deterministic step states with readable holds; MP4 encodes the same scene changes at 30 fps.'}
    (HERE / 'timeline.json').write_text(json.dumps(timeline, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    table = {f['file']: (HERE / f['file']).read_text(encoding='utf-8') for f in frames}
    html_doc = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'
                + html.escape(TITLE) + '</title><style>html,body{margin:0;background:#000;height:100%;overflow:hidden}#stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center}svg{width:100%;height:100%;object-fit:contain}</style><div id="stage" aria-label="'
                + html.escape(TITLE, quote=True) + '"></div><script>const timeline=' + json.dumps(timeline, ensure_ascii=False) + ';const scenes=' + json.dumps(table, ensure_ascii=False)
                + ";const stage=document.getElementById('stage');window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;else break}stage.innerHTML=scenes[f.file];return f.file}};__ASSET__.renderAt(0);let start=null,playing=false;document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();playing=!playing;start=null;requestAnimationFrame(tick)}if(e.code==='Home'){playing=false;__ASSET__.renderAt(0)}});function tick(ts){if(!playing)return;if(start===null)start=ts;const t=(ts-start)/1000;__ASSET__.renderAt(t);if(t<__ASSET__.durationSeconds)requestAnimationFrame(tick);else playing=false}</script></html>")
    (HERE / 'index.html').write_text(html_doc, encoding='utf-8', newline='\n')
    print('wrote', len(frames), 'scenes,', len(vmap), 'variants, poster, build.json, timeline.json, index.html')


if __name__ == '__main__':
    main()
