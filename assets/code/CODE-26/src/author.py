#!/usr/bin/env python3
"""CODE-26 scene author: an undeclared variable created on first use as a Variant.

Authored teaching example (VB4 style, Option Explicit off), not a Program.vb excerpt.
Writes only into this asset's src/: scene-NNNN.svg, variant-*.svg, scene.svg,
build.json, timeline.json, index.html. Uses the frozen drawing primitives in
tools/render/studio.py read-only. Run from the repository root:

    python assets/code/CODE-26/src/author.py
    python tools/render/render_assets.py --id CODE-26
"""
from __future__ import annotations
import html, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'tools' / 'render'))
from studio import SVG, width, segments, BG, FG, MUTED, BLUE, GOLD, GREEN, LINE  # noqa: E402

ID = 'CODE-26'
TITLE = 'Undeclared variable: created on first use as a Variant'
HEADER = 'Visual Basic 4 · Option Explicit off'
LABEL = 'Teaching example'
DURATION = 6
SIZE = 46                       # code size, as CODE-02
CW = width('0', SIZE, 'mono')   # monospace advance
PITCH = SIZE * 1.27
CODE_X = 207
PANEL = (120, 247, 1680, 673)
LINES = ['x = 42', 'Print x        \' 42']   # exact ticket copy (header line carried by the card header)
EXTRA_KEYWORDS = {'Print'}
CALLOUT = ['x was never declared.', 'VB creates it here as a ', 'Variant', '.']


def frame_row_y(i: int) -> float:
    # Two rows, vertically centred in the panel like the CODE-02 excerpt.
    top = PANEL[1] + PANEL[3] / 2 - PITCH * len(LINES) / 2
    return top + SIZE * 0.85 + i * PITCH


def code_line(s: SVG, text: str, row: int, focus: str | None = None):
    y = frame_row_y(row)
    x = CODE_X
    if focus and focus in text:
        j = text.index(focus)
        s.rect(x + j * CW - 3, y - SIZE - 2, len(focus) * CW + 6, SIZE + 10, '#263c58', rx=2)
    for part, col in segments(text, 'vb'):
        if part in EXTRA_KEYWORDS:
            col = BLUE
        s.text(part, x, y, SIZE, col, mono=True)
        x += len(part) * CW
    return x


def scene(rows: list[str], cursor_row: int | None, callout: int, focus: bool):
    """rows: text shown per row; cursor_row: row with a typing caret; callout: 0 none, 1 stub, 2 arrow, 3 text."""
    s = SVG(BG, TITLE)
    s.text(HEADER, 120, 117, 32, MUTED, mono=True)
    s.text(LABEL, 1800, 117, 28, BLUE, anchor='end')
    s.line(120, 147, 1800, 147, LINE, 2)
    s.text(TITLE, 120, 210, 46, FG, bold=True)
    s.rect(*PANEL, '#151a20')
    s.rect(PANEL[0], PANEL[1], 5, PANEL[3], BLUE)
    ends = []
    for i, text in enumerate(rows):
        if i < len(rows) and (text or i < len(LINES)):
            s.text(str(i + 1), 163, frame_row_y(i), 25, '#748293', mono=True, anchor='middle')
        ends.append(code_line(s, text, i, 'x' if (focus and i == 0) else None))
    if cursor_row is not None:
        y = frame_row_y(cursor_row)
        s.rect(ends[cursor_row] + 2, y - SIZE + 4, CW * 0.85, SIZE + 4, FG, opacity=.85)
    if callout:
        # Enters from the right margin toward the end of line 1; never crosses code text.
        yc = frame_row_y(0) - SIZE * 0.36
        tip = ends[0] + 26
        text_x = 940
        if callout == 1:
            s.line(1770, yc, text_x - 30, yc, GOLD, 2)
        else:
            s.arrow(text_x - 30, yc, tip, yc, GOLD, 2)
        if callout >= 3:
            s.text(CALLOUT[0], text_x, yc - 12, 31, GOLD)
            x = text_x
            s.text(CALLOUT[1], x, yc + 30, 31, GOLD); x += width(CALLOUT[1], 31, 'sans')
            s.text(CALLOUT[2], x, yc + 30, 31, GOLD, bold=True); x += width(CALLOUT[2], 31, 'bold')
            s.text(CALLOUT[3], x, yc + 30, 31, GOLD)
    return s.finish()


def main():
    typed = ['x', 'x ', 'x =', 'x = ', 'x = 4', 'x = 42']
    states = [(0.0, scene(['', ''], 0, 0, False))]
    t = 1.0
    for txt in typed:
        states.append((round(t, 2), scene([txt, ''], 0, 0, False))); t += 0.2
    states.append((2.2, scene([LINES[0], 'Print x'], 1, 0, False)))
    states.append((2.35, scene(LINES, None, 0, False)))
    states.append((2.5, scene(LINES, None, 1, False)))
    states.append((2.7, scene(LINES, None, 2, True)))
    states.append((2.9, scene(LINES, None, 3, True)))
    frames = []
    for i, (time, svg) in enumerate(states):
        name = f'scene-{i:04d}.svg'
        (HERE / name).write_text(svg, encoding='utf-8', newline='\n')
        frames.append({'time': time, 'file': name})
    variants = {'clean': scene(LINES, None, 0, False), 'callout': states[-1][1]}
    for name, svg in variants.items():
        (HERE / f'variant-{name}.svg').write_text(svg, encoding='utf-8', newline='\n')
    (HERE / 'scene.svg').write_text(states[-1][1], encoding='utf-8', newline='\n')
    notes = [
        'Authored teaching example in classic VB4 style with Option Explicit off; not an excerpt of Program.vb.',
        'The ticket\'s header comment line is carried by the card header ("Visual Basic 4 · Option Explicit off"); the two code lines are the exact ticket copy.',
        'Callout enters from the right margin and stops at the end of line 1; no annotation crosses code text.',
        'Discrete deterministic step states: typing 1–2.35 s, callout 2.5–2.9 s, hold to 6 s (loop-safe; last state is the poster).',
    ]
    def digest(p: Path):
        import hashlib; return hashlib.sha256(p.read_bytes()).hexdigest()
    sources = [
        {'path': '../../../sources/SCRIPT.md', 'lines': [166, 166], 'sha256': digest(ROOT / 'sources/SCRIPT.md'), 'relationship': 'source creative brief (beat S04-B06 narration)'},
        {'path': '../../../docs/tickets/CODE-26.md', 'lines': [36, 38], 'sha256': digest(ROOT / 'docs/tickets/CODE-26.md'), 'relationship': 'teaching illustration (authored copy from the ticket)'},
        {'path': '../../../review/cut-notes-2026-09-16.md', 'lines': [12, 12], 'sha256': digest(ROOT / 'review/cut-notes-2026-09-16.md'), 'relationship': 'source creative brief (Devin\'s review note 6)'},
    ]
    build = {'id': ID, 'duration': DURATION, 'frames': frames, 'variants': {k: f'variant-{k}.svg' for k in variants}, 'poster': 'scene.svg', 'cuts': {}, 'notes': notes, 'sources': sources, 'kind': 'code'}
    (HERE / 'build.json').write_text(json.dumps(build, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    timeline = {'id': ID, 'durationSeconds': DURATION, 'fps': 30, 'width': 1920, 'height': 1080,
                'beats': ['0–1 s: header and empty editor.', '1–2.35 s: `x = 42` types in, then `Print x` with its comment.', '2.5–2.9 s: callout enters from the right margin: x was never declared; VB creates it here as a Variant.', '2.9–6 s: hold (poster state, loop-safe).'],
                'frames': frames, 'cuts': {}, 'variant_names': list(variants), 'motion_model': 'Explicit deterministic step states with readable holds; MP4 encodes the same scene changes at 30 fps.'}
    (HERE / 'timeline.json').write_text(json.dumps(timeline, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    scenes = {f['file']: (HERE / f['file']).read_text(encoding='utf-8') for f in frames}
    page = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(TITLE)}</title><style>html,body{{margin:0;background:#000;height:100%;overflow:hidden}}#stage{{width:100%;height:100%;display:flex;align-items:center;justify-content:center}}svg{{width:100%;height:100%;object-fit:contain}}</style>'
            f'<div id="stage" aria-label="{html.escape(TITLE)}"></div><script>const timeline={json.dumps(timeline, ensure_ascii=False)};const scenes={json.dumps(scenes, ensure_ascii=False)};'
            "const stage=document.getElementById('stage');window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;else break}stage.innerHTML=scenes[f.file];return f.file}};__ASSET__.renderAt(0);let start=null,playing=false;document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();playing=!playing;start=null;requestAnimationFrame(tick)}if(e.code==='Home'){playing=false;__ASSET__.renderAt(0)}});function tick(ts){if(!playing)return;if(start===null)start=ts;const t=(ts-start)/1000;__ASSET__.renderAt(t);if(t<__ASSET__.durationSeconds)requestAnimationFrame(tick);else playing=false}</script></html>")
    (HERE / 'index.html').write_text(page, encoding='utf-8', newline='\n')
    (HERE / 'example.vb').write_text('\n'.join(["' " + HEADER] + LINES) + '\n', encoding='utf-8', newline='\n')
    print('AUTHORED', ID, len(frames), 'states')


if __name__ == '__main__':
    main()
