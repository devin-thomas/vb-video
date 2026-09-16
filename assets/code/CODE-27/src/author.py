#!/usr/bin/env python3
"""CODE-27 scene author: Nintendo and Nintendont, the silent typo, then Option Explicit.

Authored teaching example (VB4 style), not a Program.vb excerpt. Two states:
A (Option Explicit off) the misspelled name silently becomes a new empty variable;
B (Option Explicit On) the same line fails with the classic "Variable not defined".
Writes only into this asset's src/. Uses tools/render/studio.py read-only.

    python assets/code/CODE-27/src/author.py
    python tools/render/render_assets.py --id CODE-27
"""
from __future__ import annotations
import hashlib, html, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'tools' / 'render'))
from studio import SVG, width, segments, BG, FG, MUTED, BLUE, GOLD, LINE  # noqa: E402

ID = 'CODE-27'
TITLE = 'Nintendo and Nintendont: the silent typo'
HEADER_A = 'Visual Basic 4 · Option Explicit off'
HEADER_B = 'Visual Basic 4 · Option Explicit on'
LABEL = 'Teaching example'
DURATION = 9
SIZE = 36
CW = width('0', SIZE, 'mono')
PITCH = SIZE * 1.3
CODE_X = 207
PANEL = (120, 247, 1680, 673)
ROW0_Y = 330                    # baseline of row 0 (reserved for Option Explicit On)
RED = '#f28b82'
RED_TINT = '#4a2323'
CORRECT, TYPO = 'Nintendo', 'Nintendont'
LINES = [
    'Dim Nintendo As Integer',
    'Nintendo = 1985',
    "Nintendont = Nintendo + 1   ' typo: creates a NEW empty variable",
    "Print Nintendo              ' still 1985",
]
OPTION = 'Option Explicit On'
EXTRA_KEYWORDS = {'Print'}
CALLOUT_A = ['Nintendont is a new, empty variable.', 'Nintendo is still 1985.', 'Nothing told you.']
ERROR_TEXT = 'Variable not defined'
assert TYPO in LINES[2] and CORRECT in LINES[0] and CORRECT in LINES[1] and CORRECT in LINES[3]
MARGIN_X = 1745                 # right-margin lane for connectors; right of every line end


def row_y(i: int) -> float:
    return ROW0_Y + i * PITCH


def code_line(s: SVG, text: str, row: int, focus: str | None = None, tint: str = '#263c58', squiggle: bool = False):
    y = row_y(row)
    x = CODE_X
    if focus and focus in text:
        j = text.index(focus)
        fx, fw = x + j * CW - 3, len(focus) * CW + 6
        s.rect(fx, y - SIZE - 2, fw, SIZE + 10, tint, rx=2)
        if squiggle:
            d = f'M{fx + 2:.1f} {y + 9:.1f}'
            step, up = 8, True
            px = fx + 2
            while px + step <= fx + fw - 2:
                px += step; d += f' L{px:.1f} {y + (5 if up else 9):.1f}'; up = not up
            s.path(d, RED, 2.5)
    for part, col in segments(text, 'vb'):
        if part in EXTRA_KEYWORDS:
            col = BLUE
        s.text(part, x, y, SIZE, col, mono=True)
        x += len(part) * CW
    return x


def elbow(s: SVG, line_end: float, yc: float, y_bottom: float, color: str, head: bool):
    """Connector that enters from the right-margin lane: up the margin, then left to the line end."""
    s.line(MARGIN_X, y_bottom, MARGIN_X, yc, color, 2)
    if head:
        s.arrow(MARGIN_X, yc, line_end + 24, yc, color, 2)
    else:
        s.line(MARGIN_X, yc, MARGIN_X - 60, yc, color, 2)


def scene(rows, option: str, cursor_row, callout: int, error: int):
    """rows: code rows 1-4 text; option: row 0 text; callout: 0 none/1 stub/2 connector/3 text; error: same steps for state B."""
    header = HEADER_B if option == OPTION else HEADER_A
    s = SVG(BG, TITLE)
    s.text(header, 120, 117, 32, MUTED, mono=True)
    s.text(LABEL, 1800, 117, 28, BLUE, anchor='end')
    s.line(120, 147, 1800, 147, LINE, 2)
    s.text(TITLE, 120, 210, 46, FG, bold=True)
    s.rect(*PANEL, '#151a20')
    s.rect(PANEL[0], PANEL[1], 5, PANEL[3], BLUE)
    number = 1
    ends = [CODE_X]
    if option:
        s.text(str(number), 163, row_y(0), 25, '#748293', mono=True, anchor='middle'); number += 1
        ends[0] = code_line(s, option, 0)
    for i, text in enumerate(rows, start=1):
        s.text(str(number), 163, row_y(i), 25, '#748293', mono=True, anchor='middle'); number += 1
        focus = TYPO if (i == 3 and (callout or error)) else None
        ends.append(code_line(s, text, i, focus, RED_TINT if error else '#263c58', squiggle=bool(error)))
    if cursor_row is not None:
        y = row_y(cursor_row)
        s.rect(ends[cursor_row] + 2 if cursor_row < len(ends) else CODE_X, y - SIZE + 3, CW * 0.85, SIZE + 3, FG, opacity=.85)
    y3 = row_y(3) - SIZE * 0.36
    box_top = 640
    if callout:
        elbow(s, ends[3], y3, box_top, GOLD, callout >= 2)
        if callout >= 3:
            for k, line in enumerate(CALLOUT_A):
                s.text(line, MARGIN_X - 4, box_top + 44 + k * 42, 31, GOLD, anchor='end')
            s.text('Output', MARGIN_X - 4, box_top + 205, 24, MUTED, anchor='end')
            s.text('1985', MARGIN_X - 4, box_top + 248, 36, FG, mono=True, anchor='end')
    if error:
        elbow(s, ends[3], y3, box_top, RED, error >= 2)
        if error >= 3:
            s.text('Compile error', MARGIN_X - 4, box_top + 40, 24, MUTED, anchor='end')
            s.text(ERROR_TEXT, MARGIN_X - 4, box_top + 88, 40, RED, bold=True, anchor='end')
            s.text(TYPO, MARGIN_X - 4, box_top + 140, 36, RED, mono=True, anchor='end')
    return s.finish()


def main():
    states = [(0.0, scene(['', '', '', ''], None, 1, 0, 0))]
    times = [0.4, 0.8, 1.2, 1.6]
    for n, t in enumerate(times, start=1):
        rows = LINES[:n] + [''] * (4 - n)
        states.append((t, scene(rows, None, n + 1 if n < 4 else None, 0, 0)))
    states.append((2.0, scene(LINES, None, None, 1, 0)))
    states.append((2.25, scene(LINES, None, None, 2, 0)))
    states.append((2.5, scene(LINES, None, None, 3, 0)))
    typed = ['Option', 'Option Explicit', OPTION]
    for k, txt in enumerate(typed):
        states.append((round(5.0 + 0.3 * k, 2), scene(LINES, txt, 0, 0, 0)))
    states.append((6.0, scene(LINES, OPTION, None, 0, 1)))
    states.append((6.3, scene(LINES, OPTION, None, 0, 2)))
    states.append((6.6, scene(LINES, OPTION, None, 0, 3)))
    frames = []
    for i, (time, svg) in enumerate(states):
        name = f'scene-{i:04d}.svg'
        (HERE / name).write_text(svg, encoding='utf-8', newline='\n')
        frames.append({'time': time, 'file': name})
    variants = {'typo': scene(LINES, None, None, 3, 0), 'option-explicit': states[-1][1]}
    for name, svg in variants.items():
        (HERE / f'variant-{name}.svg').write_text(svg, encoding='utf-8', newline='\n')
    (HERE / 'scene.svg').write_text(states[-1][1], encoding='utf-8', newline='\n')
    for name, svg in [*variants.items(), ('poster', states[-1][1])]:
        assert TYPO in svg and CORRECT in svg, name
    assert ERROR_TEXT in variants['option-explicit']
    notes = [
        'Authored teaching example in classic VB4 style; not an excerpt of Program.vb. Names are exactly Nintendo (declared) and Nintendont (misspelled).',
        'State A (Option Explicit off): the misspelled line silently creates a new, empty Nintendont; Nintendo stays 1985 and Print Nintendo outputs 1985.',
        'State B (Option Explicit On): the same line is flagged with the classic VB message "Variable not defined", pointing at Nintendont. The card header switches to "Option Explicit on".',
        'The long line 3 leaves no room beside the code, so both callouts sit below the code and their connectors enter from the right-margin lane (x=1745, right of every line end); no annotation crosses code text.',
        'Discrete deterministic step states: lines type in 0.4–1.6 s, State A callout 2–2.5 s, Option Explicit On types in 5–5.6 s, State B error 6–6.6 s, hold to 9 s (poster).',
    ]
    def digest(p: Path):
        return hashlib.sha256(p.read_bytes()).hexdigest()
    sources = [
        {'path': '../../../sources/SCRIPT.md', 'lines': [166, 166], 'sha256': digest(ROOT / 'sources/SCRIPT.md'), 'relationship': 'source creative brief (beat S04-B07 narration)'},
        {'path': '../../../docs/tickets/CODE-27.md', 'lines': [36, 43], 'sha256': digest(ROOT / 'docs/tickets/CODE-27.md'), 'relationship': 'teaching illustration (authored copy from the ticket)'},
        {'path': '../../../review/cut-notes-2026-09-16.md', 'lines': [12, 12], 'sha256': digest(ROOT / 'review/cut-notes-2026-09-16.md'), 'relationship': "source creative brief (Devin's review note 6: the names Nintendo and Nintendont)"},
    ]
    build = {'id': ID, 'duration': DURATION, 'frames': frames, 'variants': {k: f'variant-{k}.svg' for k in variants}, 'poster': 'scene.svg', 'cuts': {}, 'notes': notes, 'sources': sources, 'kind': 'code'}
    (HERE / 'build.json').write_text(json.dumps(build, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    timeline = {'id': ID, 'durationSeconds': DURATION, 'fps': 30, 'width': 1920, 'height': 1080,
                'beats': ['0–2 s: the four lines type in.', '2–5 s: State A callout from the right margin: Nintendont is a new, empty variable; Nintendo is still 1985; nothing told you. Output 1985.', '5–6 s: Option Explicit On types in at the top; header switches to Option Explicit on.', '6–9 s: State B: Nintendont underlined in red, error "Variable not defined" pointing at Nintendont. Hold as poster.'],
                'frames': frames, 'cuts': {}, 'variant_names': list(variants), 'motion_model': 'Explicit deterministic step states with readable holds; MP4 encodes the same scene changes at 30 fps.'}
    (HERE / 'timeline.json').write_text(json.dumps(timeline, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    scenes = {f['file']: (HERE / f['file']).read_text(encoding='utf-8') for f in frames}
    page = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(TITLE)}</title><style>html,body{{margin:0;background:#000;height:100%;overflow:hidden}}#stage{{width:100%;height:100%;display:flex;align-items:center;justify-content:center}}svg{{width:100%;height:100%;object-fit:contain}}</style>'
            f'<div id="stage" aria-label="{html.escape(TITLE)}"></div><script>const timeline={json.dumps(timeline, ensure_ascii=False)};const scenes={json.dumps(scenes, ensure_ascii=False)};'
            "const stage=document.getElementById('stage');window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;else break}stage.innerHTML=scenes[f.file];return f.file}};__ASSET__.renderAt(0);let start=null,playing=false;document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();playing=!playing;start=null;requestAnimationFrame(tick)}if(e.code==='Home'){playing=false;__ASSET__.renderAt(0)}});function tick(ts){if(!playing)return;if(start===null)start=ts;const t=(ts-start)/1000;__ASSET__.renderAt(t);if(t<__ASSET__.durationSeconds)requestAnimationFrame(tick);else playing=false}</script></html>")
    (HERE / 'index.html').write_text(page, encoding='utf-8', newline='\n')
    (HERE / 'example.vb').write_text('\n'.join(["' " + HEADER_A] + LINES + ['', "' with Option Explicit On:", "' Nintendont = Nintendo + 1  → Variable not defined: Nintendont"]) + '\n', encoding='utf-8', newline='\n')
    print('AUTHORED', ID, len(frames), 'states')


if __name__ == '__main__':
    main()
