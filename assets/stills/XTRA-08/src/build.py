#!/usr/bin/env python3
"""XTRA-08 authoring script: five-tool "class photo" lineup (names only).

Run from the repository root:  python assets/stills/XTRA-08/src/build.py
It writes this ticket's editable sources only (SVG states, offline HTML, timeline, build driver,
exact copy). Rendering, browser checks and delivery finishing use tools/render with --id XTRA-08.
build_assets.py has no XTRA-08 composition, so this script replaces it for this ticket.
"""
from __future__ import annotations
import hashlib, html, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]   # src -> XTRA-08 -> stills -> assets -> repository root
sys.path.insert(0, str(ROOT / 'tools' / 'render'))
from studio import SVG, BG, PANEL, FG, LINE, BLUE, width, wrap  # noqa: E402

ID = 'XTRA-08'
ROW = next(r for r in json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))['tickets'] if r['id'] == ID)
# Exact ticket copy, in script order (SCRIPT.md:609). Order is the script's, not a ranking.
NAMES = ['Visual Basic 4', 'Visual C++ 4', 'Borland Delphi 1.0', 'PowerBuilder', 'Java 1.0']
assert '\n'.join(NAMES) == ROW['copy'], 'tile names must match the ticket copy exactly'

# Geometry. Shared with DIA-11: 1920x1080, content band x 120-1800, BG/PANEL/FG tokens, Liberation Sans bold names.
X0, X1 = 120, 1800
GAP = 24
TW = (X1 - X0 - GAP * (len(NAMES) - 1)) / len(NAMES)   # 316.8 px, identical for every tile
TY, TH = 372, 336                                      # identical height; tiles centred on y = 540
PAD = 24
INNER = TW - 2 * PAD
ACCENT = '#738192'                                     # same neutral strip on every tile
LEADING = 1.2
SAFE = (120, 72, 1800, 1008)


def fit_size() -> tuple[int, list[list[str]]]:
    """Largest single type size (even px, 34-60) at which every name wraps to at most two lines
    inside its tile. One size for all five tiles keeps the visual weighting neutral."""
    for size in range(60, 33, -2):
        blocks = [wrap(n, INNER, size, 'bold') for n in NAMES]
        if all(len(b) <= 2 and all(width(l, size, 'bold') <= INNER for l in b) for b in blocks):
            return size, blocks
    raise SystemExit('No shared type size fits all five names in two lines at >= 34 px')


SIZE, BLOCKS = fit_size()


def compose(focus_vb: bool) -> str:
    s = SVG(BG, 'Development tools lineup: ' + ', '.join(NAMES))
    for i, (name, block) in enumerate(zip(NAMES, BLOCKS)):
        x = X0 + i * (TW + GAP)
        focused = focus_vb and i == 0
        s.rect(x, TY, TW, TH, PANEL, BLUE if focused else LINE, 4 if focused else 2)
        s.rect(x, TY, TW, 8, BLUE if focused else ACCENT)
        # Vertically centre the name block (cap height ~0.72 em) inside the tile.
        block_h = SIZE * 0.72 + (len(block) - 1) * SIZE * LEADING
        first = TY + 8 + (TH - 8) / 2 - block_h / 2 + SIZE * 0.72
        for j, line in enumerate(block):
            y = first + j * SIZE * LEADING
            w = width(line, SIZE, 'bold')
            assert SAFE[0] <= x + TW / 2 - w / 2 and x + TW / 2 + w / 2 <= SAFE[2], line
            assert SAFE[1] <= y - SIZE and y <= SAFE[3], line
            s.text(line, x + TW / 2, y, SIZE, FG, True, anchor='middle')
    return s.finish()


def main() -> None:
    clean, focus = compose(False), compose(True)
    src = HERE
    for name in ('exports', 'evidence', 'proofs'):   # render_assets.py expects these, as build_assets.py would create them
        (HERE.parent / name).mkdir(parents=True, exist_ok=True)
    (src / 'scene-0000.svg').write_text(clean, encoding='utf-8', newline='\n')
    (src / 'scene.svg').write_text(clean, encoding='utf-8', newline='\n')
    (src / 'variant-lineup.svg').write_text(clean, encoding='utf-8', newline='\n')
    (src / 'variant-vb-focus.svg').write_text(focus, encoding='utf-8', newline='\n')
    (src / 'copy.txt').write_text('\n'.join(NAMES) + '\n', encoding='utf-8', newline='\n')
    (src / 'brief.json').write_text(json.dumps({k: ROW[k] for k in ['id', 'title', 'requirements', 'beats', 'checks', 'copy', 'refs', 'gates']}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    script = ROOT / 'sources' / 'SCRIPT.md'
    sources = [{'path': '../../../sources/SCRIPT.md', 'lines': [609, 613], 'sha256': hashlib.sha256(script.read_bytes()).hexdigest(), 'relationship': 'source creative brief'}]
    notes = [
        'Names only: the five tile labels are the exact ticket copy (SCRIPT.md:609) in script order. No year, vendor, logo, box art, price, market share or ranking appears on screen.',
        f'Five tiles of identical size ({TW:g} x {TH} px), fill, border and accent strip; every name is Liberation Sans Bold at one shared size ({SIZE} px), centred. Order follows the script and DIA-11 rows, not a ranking.',
        'No on-screen heading: a "1995" title would assert that all five belong to 1995, which evidence does not support for Java 1.0 (JavaSoft shipped it 23 January 1996). See evidence/claim-checks.json.',
        'The script\'s optional bracket-tournament arrangement was not used, because brackets imply elimination and a winner.',
        'Named variant lineup is the clean class photo (identical to the poster). Optional variant vb-focus adds a blue outline and accent strip to the Visual Basic 4 tile only; the other four tiles are unchanged and fully readable.',
        'Transition-compatible with DIA-11: same canvas, background #111318, panel #1b2027, text #f1f3f5, Liberation Sans, and 120-1800 px content band, with tools in the same order.',
        'Release stays blocked under R15 pending the review questions in evidence/claim-checks.json.',
    ]
    frames = [{'time': 0, 'file': 'scene-0000.svg'}]
    timeline = {'id': ID, 'durationSeconds': None, 'fps': None, 'width': 1920, 'height': 1080, 'beats': ROW['beats'], 'frames': frames, 'cuts': {}, 'variant_names': ['lineup', 'vb-focus'], 'motion_model': 'Still asset: one state held for editorial timing; variants are separate stills with identical geometry, so the edit can dissolve between them.'}
    (src / 'timeline.json').write_text(json.dumps(timeline, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    build = {'id': ID, 'duration': None, 'frames': frames, 'variants': {'lineup': 'variant-lineup.svg', 'vb-focus': 'variant-vb-focus.svg'}, 'poster': 'scene.svg', 'cuts': {}, 'notes': notes, 'sources': sources, 'kind': ROW['kind']}
    (src / 'build.json').write_text(json.dumps(build, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    table = {'scene-0000.svg': clean}
    # Same deterministic, offline HTML contract as tools/render/build_assets.py.
    doc = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(ROW['title']) + '</title>'
           '<style>html,body{margin:0;background:#000;height:100%;overflow:hidden}#stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center}svg{width:100%;height:100%;object-fit:contain}</style>'
           '<div id="stage" aria-label="' + html.escape(ROW['title'], quote=True) + '"></div><script>const timeline=' + json.dumps(timeline, ensure_ascii=False) + ';const scenes=' + json.dumps(table, ensure_ascii=False) + ';'
           "const stage=document.getElementById('stage');window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,"
           'renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;else break}stage.innerHTML=scenes[f.file];return f.file}};'
           "__ASSET__.renderAt(0);document.addEventListener('keydown',e=>{if(e.code==='Home')__ASSET__.renderAt(0)});</script></html>")
    (src / 'index.html').write_text(doc, encoding='utf-8', newline='\n')
    print('AUTHORED', ID, 'name px', SIZE, 'tile', round(TW, 1), 'x', TH, 'lines', [len(b) for b in BLOCKS], BLOCKS)


if __name__ == '__main__':
    main()
