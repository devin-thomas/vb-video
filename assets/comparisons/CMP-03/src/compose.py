#!/usr/bin/env python3
"""CMP-03 revision 2: authored `i` teaching example that transforms into the real Program.vb loop.

Run from anywhere: python assets/comparisons/CMP-03/src/compose.py
Writes only inside assets/comparisons/CMP-03/ (src/, evidence/). Then render with
python tools/render/render_assets.py --id CMP-03. Do not run tools/render/build_assets.py --id CMP-03
afterwards: that would regenerate the revision-1 still and discard these scenes.
"""
from __future__ import annotations
import hashlib, html, json, math, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = BASE.parents[2]
sys.path.insert(0, str(ROOT / 'tools/render'))
from studio import SVG, BG, FG, MUTED, BLUE, width, code_line, segments  # read-only shared primitives

ID = 'CMP-03'
ROW = {r['id']: r for r in json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))['tickets']}[ID]
TITLE = ROW['title']
HEADING = 'The same inclusive range'
LEFT_HEADER = 'C / C++ / C# / Java'
RIGHT_HEADER = 'VB'
SIZE = 36
CW = width('0', SIZE, 'mono')
LEADING = SIZE * 1.42
FOCUS_RECT = '#263c58'
PROGRAM_LINES = (104, 110)  # War/Program.vb: For Rank = 2 To 14 ... Next Rank (the real loop, BuildDeck)

# Authored teaching example (both columns say i). Not a Program.vb excerpt.
LEFT_EXAMPLE = ['for (int i = 2; i <= 14; i++) {', '    ...', '}']
RIGHT_EXAMPLE = ['For i = 2 To 14', '    ...', 'Next i']
# Real loop, display form: lines 104 and 110 of Program.vb with the common 8-space indent removed
# and body lines 105-109 elided as "..." (an intentional excerpt, never complete runnable source).
RIGHT_REAL = ['For Rank = 2 To 14', '    ...', 'Next Rank']
LABEL = 'in the real program the counter is called Rank'
LABEL_SOURCE = 'Program.vb lines 104–110 (body lines 105–109 elided as ...)'


def program_excerpt() -> str:
    src = (ROOT / 'sources/Program.vb').read_text(encoding='utf-8').splitlines()
    lo, hi = PROGRAM_LINES
    lines = src[lo - 1:hi]
    assert lines[0] == '        For Rank = 2 To 14' and lines[-1] == '        Next Rank', lines
    assert [l.strip() for l in (lines[0], lines[-1])] == [RIGHT_REAL[0], RIGHT_REAL[2]]
    return '\n'.join(lines) + '\n'


def panel(s: SVG, col: int, header: str):
    x = 120 + col * 870
    s.rect(x, 248, 810, 652, '#171c23')
    s.rect(x, 248, 810, 6, BLUE if col == 1 else '#738192')
    s.text(header, x + 44, 335, 53, FG, True)
    return x + 44


def baseline(n: int, j: int) -> float:
    return 540 - (n - 1) * LEADING / 2 + j * LEADING


def ident_line(s: SVG, keyword: str, x: float, y: float, p: float, tail: str):
    """`keyword i tail` morphing into `keyword Rank tail`; p in [0,1] is the morph progress."""
    kx = x
    s.text(keyword, kx, y, SIZE, BLUE, mono=True)
    ix = kx + (len(keyword) + 1) * CW
    w = CW * (1 + 3 * p)  # one character growing to four
    s.rect(ix - 3, y - SIZE - 2, w + 6, SIZE + 10, FOCUS_RECT, rx=2)
    if p < 1:
        s.text('i', ix, y, SIZE, FG, mono=True, opacity=round(1 - p, 4))
    if p > 0:
        s.text('Rank', ix, y, SIZE, FG, mono=True, opacity=round(p, 4))
    xx = ix + w
    for part, col in segments(tail, 'vb'):
        s.text(part, xx, y, SIZE, col, mono=True)
        xx += len(part) * CW


def footer(s: SVG, note: str):
    s.text('Syntax comparison · ' + note, 120, 978, 30, MUTED)


def scene(state: str, p: float = 0.0) -> str:
    """state: example | focus | morph (with p) | real | real-label"""
    s = SVG(BG, TITLE)
    s.heading(HEADING)
    lx = panel(s, 0, LEFT_HEADER)
    for j, line in enumerate(LEFT_EXAMPLE):
        code_line(s, line, lx, baseline(3, j), SIZE, 'cs', 'i <= 14' if state == 'focus' else None)
    rx = panel(s, 1, RIGHT_HEADER)
    if state in ('example', 'focus'):
        for j, line in enumerate(RIGHT_EXAMPLE):
            code_line(s, line, rx, baseline(3, j), SIZE, 'vb', '2 To 14' if state == 'focus' else None)
        footer(s, 'authored teaching example, the counter is named i on both sides')
    else:
        q = {'morph': p, 'real': 1.0, 'real-label': 1.0}[state]
        ident_line(s, 'For', rx, baseline(3, 0), q, ' = 2 To 14')
        code_line(s, '    ...', rx, baseline(3, 1), SIZE, 'vb')
        ident_line(s, 'Next', rx, baseline(3, 2), q, '')
        if state == 'real-label':
            # Margin label below the code, inside the VB panel; arrow rises through empty panel space
            # to the Rank token of Next Rank and never crosses a code line.
            cx = rx + (len('Next') + 1) * CW + 2 * CW
            top = baseline(3, 2) - SIZE - 2 + SIZE + 10
            s.arrow(cx, 752, cx, top + 8, BLUE, 3)
            s.text(LABEL, rx, 790, 30, FG)
            s.text(LABEL_SOURCE, rx, 832, 26, MUTED)
            footer(s, 'the VB column now shows the real loop from Program.vb')
        else:
            footer(s, 'the counter is renamed to match the real program')
    return s.finish()


def main():
    fps = 30
    frames = [(0.0, scene('example')), (2.5, scene('focus'))]
    morph_start = 135  # frame index = 4.5 s
    steps = 12
    for k in range(steps):
        t = (k + 1) / (steps + 1)
        p = 0.5 - 0.5 * math.cos(math.pi * t)
        frames.append((round((morph_start + k) / fps, 6), scene('morph', round(p, 4))))
    frames.append((round((morph_start + steps) / fps, 6), scene('real')))
    frames.append((5.4, scene('real-label')))
    duration = 9
    variants = {'comparison': scene('example'), 'token-focus': scene('focus'), 'transform': scene('real-label')}
    poster = scene('real-label')
    beats = [
        '0–2.5 s: authored teaching example, i on both sides (comparison state).',
        '2.5–4.5 s: focus overlay on the compared range tokens i <= 14 and 2 To 14 (token-focus state).',
        '4.5–4.9 s: on the VB side the identifier i morphs in place into Rank on the For and Next lines (12 eased steps, one frame each).',
        '4.9–5.4 s: real loop, Rank highlighted; 5.4–9 s: margin label appears and the real-code state holds to the end (transform state).',
    ]
    notes = [
        'Revision 2: both columns are an authored teaching example with the counter named i (for (int i = 2; i <= 14; i++) / For i = 2 To 14 ... Next i); it is not a Program.vb excerpt. The C-family side is a proposed equivalent-bounds example, not verbatim supplied code; the inclusive upper bound 14 is kept on both sides.',
        'Left header lists the languages the snippet is valid in: C / C++ / C# / Java.',
        'Transform: the VB identifier i morphs into Rank in place; the end state is the real loop from Program.vb lines 104–110 (For Rank = 2 To 14 ... Next Rank) shown as lines 104 and 110 with the common indent removed and body lines 105–109 elided as "...". src/excerpt.vb holds the seven lines byte-exactly.',
        'No compile/run is claimed for illustrative counterparts.',
    ]
    for name in ['src', 'exports', 'exports/keyframes', 'evidence', 'proofs']:
        (BASE / name).mkdir(parents=True, exist_ok=True)

    # Scenes, de-duplicated by content like build_assets.save_assets.
    for old in BASE.glob('src/scene-*.svg'):
        old.unlink()
    names = []
    dedup = {}
    for t, svg in frames:
        sha = hashlib.sha256(svg.encode()).hexdigest()
        if sha not in dedup:
            n = f'scene-{len(dedup):04}.svg'
            dedup[sha] = n
            (BASE / 'src' / n).write_text(svg, encoding='utf-8', newline='\n')
        names.append({'time': round(t, 6), 'file': dedup[sha]})
    (BASE / 'src/scene.svg').write_text(poster, encoding='utf-8', newline='\n')
    table = {n: (BASE / 'src' / n).read_text(encoding='utf-8') for n in dedup.values()}
    timeline = {'id': ID, 'durationSeconds': duration, 'fps': fps, 'width': 1920, 'height': 1080, 'beats': beats,
                'frames': names, 'cuts': {}, 'variant_names': list(variants),
                'motion_model': 'Explicit deterministic step states with readable holds; MP4 encodes the same scene changes at 30 fps.'}
    (BASE / 'src/timeline.json').write_text(json.dumps(timeline, indent=2, ensure_ascii=False), encoding='utf-8', newline='\n')
    html_doc = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'
                + html.escape(TITLE) + '</title><style>html,body{margin:0;background:#000;height:100%;overflow:hidden}#stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center}svg{width:100%;height:100%;object-fit:contain}</style><div id="stage" aria-label="'
                + html.escape(TITLE, quote=True) + '"></div><script>const timeline=' + json.dumps(timeline, ensure_ascii=False) + ';const scenes=' + json.dumps(table, ensure_ascii=False)
                + ";const stage=document.getElementById('stage');window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;else break}stage.innerHTML=scenes[f.file];return f.file}};__ASSET__.renderAt(0);let start=null,playing=false;document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();playing=!playing;start=null;requestAnimationFrame(tick)}if(e.code==='Home'){playing=false;__ASSET__.renderAt(0)}});function tick(ts){if(!playing)return;if(start===null)start=ts;const t=(ts-start)/1000;__ASSET__.renderAt(t);if(t<__ASSET__.durationSeconds)requestAnimationFrame(tick);else playing=false}</script></html>")
    (BASE / 'src/index.html').write_text(html_doc, encoding='utf-8', newline='\n')
    vmap = {}
    for name, svg in variants.items():
        path = f'variant-{name}.svg'
        (BASE / 'src' / path).write_text(svg, encoding='utf-8', newline='\n')
        vmap[name] = path
    excerpt = program_excerpt()
    (BASE / 'src/excerpt.vb').write_text(excerpt, encoding='utf-8', newline='\n')

    # Sources and evidence.
    refs = [tuple(r) for r in ROW['refs']] + [('Program.vb',) + PROGRAM_LINES]
    snippets, sources = [], []
    for filename, lo, hi in refs:
        path = ROOT / 'sources' / filename
        text = path.read_text(encoding='utf-8').splitlines()
        snippets.append(f'## {filename}:{lo}–{hi}\n\n```text\n' + '\n'.join(text[lo - 1:hi]) + '\n```\n')
        sources.append({'path': '../../../sources/' + filename, 'lines': [lo, hi], 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                        'relationship': 'literal excerpt' if filename == 'Program.vb' else 'source creative brief'})
    war = ROOT / 'War/Program.vb'
    war_lines = war.read_text(encoding='utf-8').splitlines()[PROGRAM_LINES[0] - 1:PROGRAM_LINES[1]]
    assert war_lines == excerpt.splitlines(), 'War/Program.vb and sources/Program.vb disagree on the loop lines'
    snippets.append('## Authored teaching example (not a Program.vb excerpt)\n\n```text\nC / C++ / C# / Java\n' + '\n'.join(LEFT_EXAMPLE)
                    + '\n\nVB\n' + '\n'.join(RIGHT_EXAMPLE) + '\n```\n\nThe ticket’s revision 2 renames the counter to `i` on both sides so the screen matches the narration. '
                    'The left snippet is a proposed equivalent-bounds example valid in C, C++, C# and Java; the right snippet is the same loop in VB. Neither was compiled or run.\n\n'
                    f'## Real loop check\n\n`src/excerpt.vb` equals `sources/Program.vb` lines {PROGRAM_LINES[0]}–{PROGRAM_LINES[1]} byte for byte (LF newlines); '
                    f'`War/Program.vb` (CRLF, sha256 {hashlib.sha256(war.read_bytes()).hexdigest()}) has the same seven lines at the same numbers. '
                    'On screen the end state shows lines 104 and 110 with the common eight-space indent removed and lines 105–109 elided as `...`. '
                    'The ticket text cites lines 244–255 for this loop; those lines are the round-resolution `If Card1.Rank > Card2.Rank` block, not a `For` loop. The only `For Rank = 2 To 14 ... Next Rank` in Program.vb is at 104–110 (BuildDeck).\n')
    (BASE / 'evidence/source-excerpts.md').write_text('\n'.join(snippets), encoding='utf-8', newline='\n')
    (BASE / 'evidence/provenance.json').write_text(json.dumps({
        'id': ID, 'classification': 'original authored source-based illustration',
        'sources': sources, 'authored_additions': notes, 'source_unchanged': True, 'remote_assets': [], 'font_files_distributed': False,
        'producer_decisions': [
            'Revision 2 (2026-09-16), from Devin’s review notes 13 and 15: counter named i on screen; left header C / C++ / C# / Java; motion transform into the real Rank loop, held at the end.'],
        'authored_example': {'left_header': LEFT_HEADER, 'left': LEFT_EXAMPLE, 'right_header': RIGHT_HEADER, 'right': RIGHT_EXAMPLE,
                             'status': 'agent-authored teaching example, not a Program.vb excerpt, not compiled'},
        'real_loop': {'file': 'sources/Program.vb', 'lines': list(PROGRAM_LINES), 'excerpt_file': 'src/excerpt.vb',
                      'display': 'lines 104 and 110 with the common indent removed; lines 105–109 elided as ...'},
    }, indent=2, ensure_ascii=False), encoding='utf-8', newline='\n')
    (BASE / 'evidence/claim-checks.json').write_text(json.dumps({'gates': [], 'self_checks': [
        {'check': 'src/excerpt.vb equals sources/Program.vb lines 104–110 and War/Program.vb lines 104–110 (newline-normalized)', 'result': 'passed', 'by': 'src/compose.py assertions'},
        {'check': 'the on-screen For/Next lines of the end state equal the stripped lines 104 and 110', 'result': 'passed', 'by': 'src/compose.py assertions'},
    ]}, indent=2, ensure_ascii=False), encoding='utf-8', newline='\n')
    brief = {k: ROW[k] for k in ['id', 'title', 'requirements', 'beats', 'checks', 'copy', 'refs', 'gates']}
    brief['revision_2'] = {'left_header': LEFT_HEADER, 'left': LEFT_EXAMPLE, 'right': RIGHT_EXAMPLE, 'real_loop_lines': list(PROGRAM_LINES), 'label': LABEL, 'beats': beats}
    (BASE / 'src/brief.json').write_text(json.dumps(brief, indent=2, ensure_ascii=False), encoding='utf-8', newline='\n')
    build = {'id': ID, 'duration': duration, 'frames': names, 'variants': vmap, 'poster': 'scene.svg', 'cuts': {}, 'notes': notes, 'sources': sources, 'kind': ROW['kind']}
    (BASE / 'src/build.json').write_text(json.dumps(build, indent=2, ensure_ascii=False), encoding='utf-8', newline='\n')
    print('AUTHORED', ID, len(dedup), 'states,', len(names), 'frames,', duration, 's')


if __name__ == '__main__':
    main()
