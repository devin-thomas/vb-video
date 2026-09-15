#!/usr/bin/env python3
"""XTRA-10 authoring script: VB-for-Mac claim visual (composed text card).

Run from the repository root:  python -B assets/stills/XTRA-10/src/build.py
Writes editable SVG source, offline HTML, timeline, and build driver.
Rendering, browser checks and delivery finishing use tools/render with --id XTRA-10.
build_assets.py has no XTRA-10 composition, so this script replaces it here.

Editorial decision (project owner approved):
  "Visual Basic for Mac" was proven fictional. This card shows a neutral
  text composition acknowledging the product was never released and naming
  QuickBASIC for Macintosh as the closest real Microsoft BASIC for Mac.
"""
from __future__ import annotations
import hashlib, html as htmlmod, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSET = HERE.parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'tools' / 'render'))
from studio import (SVG, BG, PANEL, FG, MUTED, LINE, BLUE, GOLD, GREEN,
                    TEAL, GRAY, NAVY, SANS, MONO, width, wrap)

ID = 'XTRA-10'
ROW = next(r for r in json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))['tickets'] if r['id'] == ID)
W, H = 1920, 1080
SAFE = (120, 72, 1800, 1008)

# -- The approved copy for this composed text card --
# This is an authored production choice, approved by the project owner via
# the editorial decision that "VB for Mac" was fictional. The script
# (sources/SCRIPT.md) is NOT changed.
TITLE_TEXT = '"Visual Basic for Mac"'
SUBTITLE = 'Product Not Found'
BODY_LINES = [
    'Microsoft never released a standalone product',
    'called "Visual Basic" for the Macintosh.',
]
CLOSEST_HEADING = 'The closest Microsoft BASIC for Macintosh:'
PRODUCT_NAME = 'Microsoft QuickBASIC 1.00'
PRODUCT_PLATFORM = 'for Apple Macintosh'
PRODUCT_DETAILS = [
    'Released 1988  |  Last update: 1.00e (April 1992)',
    'Platform: Classic Mac OS, 68K (System 4.10+)',
]
ALSO_LINES = [
    'Also on Mac:  BASIC Interpreter 1.0–3.0 (1984–1986)',
    '  BASIC Compiler 1.0  |  VBA in Office for Mac (from ~1994)',
]
SOURCE_NOTE = 'Evidence: Microsoft KB, MacWEEK 1996, period sources  —  see provenance.json'


def question_icon(s, cx, cy, r=48):
    """Draw a Win95-style question-mark circle icon."""
    s.circle(cx, cy, r, fill=NAVY, stroke='#4060a0', sw=3)
    s.text('?', cx, cy + 18, 56, '#ffffff', bold=True, anchor='middle')


def build_card_svg():
    """Compose the XTRA-10 text card as an SVG using studio.py primitives."""
    s = SVG(BG, 'Visual Basic for Mac: Product Not Found')

    # -- Win95-style window --
    wx, wy, ww, wh = 260, 100, 1400, 880
    s.bevel(wx, wy, ww, wh)
    # Title bar
    s.rect(wx + 6, wy + 6, ww - 12, 54, NAVY)
    s.text('Microsoft Product Library', wx + 22, wy + 50, 30, '#ffffff', bold=True)
    # Close button
    s.bevel(wx + ww - 47, wy + 14, 31, 30)
    s.path(f'M{wx+ww-39} {wy+21}l15 15m-15 0l15-15', '#111', 2.4)

    content_top = wy + 76

    # -- Question icon --
    question_icon(s, wx + 80, content_top + 62)

    # -- Title: "Visual Basic for Mac" --
    s.text(TITLE_TEXT, wx + 140, content_top + 42, 52, '#111318', bold=True)

    # -- Subtitle: Product Not Found --
    s.text(SUBTITLE, wx + 140, content_top + 86, 36, '#b53b34', bold=True)

    # -- Separator --
    sy = content_top + 116
    s.line(wx + 40, sy, wx + ww - 40, sy, '#858585', 2)
    s.line(wx + 40, sy + 2, wx + ww - 40, sy + 2, '#eeeeee', 2)

    # -- Body text --
    by = content_top + 165
    for i, line in enumerate(BODY_LINES):
        s.text(line, wx + 60, by + i * 44, 34, '#333333')

    # -- "Closest product" heading --
    hy = by + len(BODY_LINES) * 44 + 30
    s.text(CLOSEST_HEADING, wx + 60, hy, 30, '#555555')

    # -- Product info panel (sunken bevel) --
    py = hy + 24
    pw, ph = ww - 120, 190
    s.bevel(wx + 60, py, pw, ph, '#f0f0f0', pressed=True)

    # Product name (two lines to avoid clipping)
    s.text(PRODUCT_NAME, wx + 84, py + 42, 40, NAVY, bold=True)
    s.text(PRODUCT_PLATFORM, wx + 84, py + 80, 36, '#333333')

    # Product details
    for i, detail in enumerate(PRODUCT_DETAILS):
        s.text(detail, wx + 84, py + 118 + i * 34, 27, '#555555')

    # -- Also on Mac line --
    ay = py + ph + 30
    for i, line in enumerate(ALSO_LINES):
        s.text(line, wx + 60, ay + i * 34, 26, '#555555')

    # -- Source note at bottom --
    s.text(SOURCE_NOTE, wx + 60, wy + wh - 76, 22, '#888888')

    # -- OK button --
    bw, bh = 180, 58
    bx = wx + ww // 2 - bw // 2
    by_btn = wy + wh - 50 - bh
    # Only show button if it fits; it does at these coords
    # Actually place it at bottom-right of the window
    bx = wx + ww - 60 - bw
    by_btn = wy + wh - 30 - bh
    s.button('OK', bx, by_btn, bw, bh)

    return s.finish()


def main():
    svg = build_card_svg()

    # Write the poster/scene SVG
    (HERE / 'scene.svg').write_text(svg, encoding='utf-8', newline='\n')

    # Write the variant SVG (approved-visual is the same as the poster for this still)
    (HERE / 'variant-approved-visual.svg').write_text(svg, encoding='utf-8', newline='\n')

    # Write timeline.json
    timeline = {
        'id': ID,
        'durationSeconds': None,
        'fps': None,
        'width': W,
        'height': H,
        'beats': ROW['beats'],
        'frames': [{'time': 0, 'file': 'scene.svg'}],
        'cuts': {},
        'variant_names': ['approved-visual'],
        'motion_model': 'Still asset: one state held for editorial timing.'
    }
    (HERE / 'timeline.json').write_text(
        json.dumps(timeline, indent=2, ensure_ascii=False),
        encoding='utf-8', newline='\n'
    )

    # Write build.json (render driver)
    script_path = ROOT / 'sources' / 'SCRIPT.md'
    script_hash = hashlib.sha256(script_path.read_bytes()).hexdigest()
    build = {
        'id': ID,
        'duration': None,
        'frames': [{'time': 0, 'file': 'scene.svg'}],
        'variants': {'approved-visual': 'variant-approved-visual.svg'},
        'poster': 'scene.svg',
        'cuts': {},
        'notes': [
            'Composed text card: "Visual Basic for Mac" was never released.',
            'QuickBASIC 1.00 for Apple Macintosh (1988) shown as closest real product.',
            'Editorial decision approved by project owner; script unchanged.',
            'No external images: all content is authored text using studio.py primitives.',
        ],
        'sources': [
            {
                'path': '../../../sources/SCRIPT.md',
                'lines': [645, 647],
                'sha256': script_hash,
                'relationship': 'source creative brief (narration claim under review)',
            }
        ],
        'kind': 'still',
    }
    (HERE / 'build.json').write_text(
        json.dumps(build, indent=2, ensure_ascii=False),
        encoding='utf-8', newline='\n'
    )

    # Write brief.json (ticket data snapshot)
    brief = {k: ROW[k] for k in ['id', 'title', 'requirements', 'beats', 'checks', 'copy', 'refs', 'gates']}
    (HERE / 'brief.json').write_text(
        json.dumps(brief, indent=2, ensure_ascii=False),
        encoding='utf-8', newline='\n'
    )

    # Write the exact on-screen copy for traceability
    copy_text = '\n'.join([
        '# XTRA-10 on-screen copy (authored production text, not from sources/)',
        '',
        f'Title: {TITLE_TEXT}',
        f'Subtitle: {SUBTITLE}',
        '',
        *BODY_LINES,
        '',
        CLOSEST_HEADING,
        f'  {PRODUCT_NAME} {PRODUCT_PLATFORM}',
        *[f'  {d}' for d in PRODUCT_DETAILS],
        '',
        *ALSO_LINES,
        '',
        SOURCE_NOTE,
    ])
    (HERE / 'copy.txt').write_text(copy_text, encoding='utf-8', newline='\n')

    # Write inline HTML (same pattern as build_assets.py save_assets)
    table = {'scene.svg': svg}
    html_doc = (
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>' + htmlmod.escape(ROW['title']) + '</title>'
        '<style>html,body{margin:0;background:#000;height:100%;overflow:hidden}'
        '#stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center}'
        'svg{width:100%;height:100%;object-fit:contain}</style>'
        '<div id="stage" aria-label="' + htmlmod.escape(ROW['title'], quote=True) + '"></div>'
        '<script>'
        'const timeline=' + json.dumps(timeline, ensure_ascii=False) + ';'
        'const scenes=' + json.dumps(table, ensure_ascii=False) + ';'
        'const stage=document.getElementById(\'stage\');'
        'window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,'
        'fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,'
        'renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));'
        'let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;'
        'else break}stage.innerHTML=scenes[f.file];return f.file}};'
        '__ASSET__.renderAt(0);'
        'document.addEventListener(\'keydown\',e=>'
        '{if(e.code===\'Home\')__ASSET__.renderAt(0)});'
        '</script></html>'
    )
    (HERE / 'index.html').write_text(html_doc, encoding='utf-8', newline='\n')

    print(f'AUTHORED {ID}: scene.svg, variant-approved-visual.svg, index.html, build.json, timeline.json')


if __name__ == '__main__':
    main()
