#!/usr/bin/env python3
"""XTRA-04 authoring script: FORTRAN II versus Dartmouth BASIC, same one-line message task.

Run from the repository root:  python assets/reference-code/XTRA-04/src/build.py
It writes this ticket's editable sources only (SVG states, offline HTML, timeline, build driver,
exact code excerpts). Rendering, browser checks and delivery finishing use tools/render with --id XTRA-04.
build_assets.py has no XTRA-04 composition, so this script replaces it for this ticket.
"""
from __future__ import annotations
import hashlib, html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]   # src -> XTRA-04 -> reference-code -> assets -> repository root
sys.path.insert(0, str(ROOT / 'tools' / 'render'))
from studio import SVG, BG, PANEL, FG, MUTED, LINE, BLUE, GOLD, width, wrap  # noqa: E402

ID = 'XTRA-04'
ROW = next(r for r in json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))['tickets'] if r['id'] == ID)
TITLE = 'Same task, different syntax'          # ticket copy, line 2
HEADS = ('FORTRAN', 'BASIC')                   # ticket copy, line 1 ("FORTRAN | BASIC"), one heading per panel
# Authored dialect labels (production addition, see evidence/provenance.json).
DIALECTS = ('FORTRAN II for the IBM 7090/7094', 'Dartmouth BASIC, October 1964')

# Authored illustrative programs. FORTRAN keeps real card columns: statement number in 1-5, statement from 7.
FORTRAN = ['      PRINT 1',
           '    1 FORMAT (6H HELLO)',
           '      CALL EXIT',
           '      END']
BASIC = ['10 PRINT "HELLO"',
         '20 END']
KEYWORDS = {'PRINT', 'FORMAT', 'CALL', 'EXIT', 'END'}
LITERALS = {'fortran': re.compile(r'6H HELLO'), 'basic': re.compile(r'"HELLO"')}

CODE = 48                      # identical code size in both panels (52 px overflowed the 23-column FORMAT line)
PITCH = round(CODE * 1.35)     # identical line pitch in both panels
CW = width('0', CODE, 'mono')
PANELS = ((120, 'fortran', FORTRAN), (980, 'basic', BASIC))
PW, PY, PH = 820, 248, 744     # panel width / top / height (bottom 992, inside the 1008 safe line)
AREA_Y, AREA_H = 414, 352      # code well
FIRST = 520                    # first code baseline, same in both panels


def runs(line: str, lang: str):
    """Yield (column, text, colour) for each non-blank run. Placement by column keeps monospaced
    card columns exact without depending on how a renderer treats leading blanks."""
    lit = LITERALS[lang].search(line)
    spans = []
    for m in re.finditer(r'\S+', line):
        s, e, tok = m.start(), m.end(), m.group(0)
        if lit and lit.start() <= s < lit.end():
            colour = GOLD
        elif tok in KEYWORDS:
            colour = BLUE
        else:
            colour = FG
        spans.append((s, tok, colour))
    return spans


def compose(focus: bool) -> str:
    s = SVG(BG, f'{HEADS[0]} | {HEADS[1]}: {TITLE}')
    s.text(TITLE, 120, 150, 64, FG, True)
    for (x, lang, lines), head, dialect in zip(PANELS, HEADS, DIALECTS):
        s.rect(x, PY, PW, PH, PANEL, LINE, 2)
        s.text(head, x + 40, PY + 78, 56, FG, True)
        assert width(dialect, 30) <= PW - 80, dialect
        s.text(dialect, x + 40, PY + 126, 30, MUTED)
        s.rect(x + 40, AREA_Y, PW - 80, AREA_H, '#151a20')
        x0 = x + 70
        assert max(len(l) for l in lines) * CW <= PW - 140
        if focus:
            # Line-structure overlay: a band per program line. Code size and positions are unchanged.
            for i in range(len(lines)):
                s.rect(x + 50, FIRST + i * PITCH - CODE + 4, PW - 100, PITCH - 8, '#223247', rx=2)
            if lang == 'fortran':
                # Card-column guide above the code (C28-6054-5 p.5-6: number in 1-5, statement from 7).
                s.line(x0, AREA_Y + 34, x0 + 5 * CW, AREA_Y + 34, MUTED, 2)
                s.text('cols 1-5', x0, AREA_Y + 26, 26, MUTED)
                s.line(x0 + 6 * CW, AREA_Y + 34, x0 + 16 * CW, AREA_Y + 34, MUTED, 2)
                s.text('col 7 onward', x0 + 6 * CW, AREA_Y + 26, 26, MUTED)
        for i, line in enumerate(lines):
            y = FIRST + i * PITCH
            for col, tok, colour in runs(line, lang):
                s.text(tok, x0 + col * CW, y, CODE, colour, mono=True)
        if focus:
            count = f'{len(lines)} statements'
            note = ('6H counts the next six characters; the first, a blank, is printer carriage control.'
                    if lang == 'fortran' else
                    'The message sits in quotes; END carries the highest line number.')
            s.text(count, x + 40, AREA_Y + AREA_H + 66, 36, GOLD, True)
            s.lines(wrap(note, PW - 80, 30), x + 40, AREA_Y + AREA_H + 116, 30, FG, leading=1.3)
    return s.finish()


def main() -> None:
    clean, focus = compose(False), compose(True)
    src = HERE
    (src / 'scene-0000.svg').write_text(clean, encoding='utf-8', newline='\n')
    (src / 'scene.svg').write_text(clean, encoding='utf-8', newline='\n')
    (src / 'variant-comparison.svg').write_text(focus, encoding='utf-8', newline='\n')
    (src / 'excerpt-fortran2.f').write_text('\n'.join(FORTRAN) + '\n', encoding='utf-8', newline='\n')
    (src / 'excerpt-dartmouth.bas').write_text('\n'.join(BASIC) + '\n', encoding='utf-8', newline='\n')
    (src / 'brief.json').write_text(json.dumps({k: ROW[k] for k in ['id', 'title', 'requirements', 'beats', 'checks', 'copy', 'refs', 'gates']}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    script = ROOT / 'sources' / 'SCRIPT.md'
    sources = [{'path': '../../../sources/SCRIPT.md', 'lines': [69, 71], 'sha256': hashlib.sha256(script.read_bytes()).hexdigest(), 'relationship': 'source creative brief'}]
    notes = [
        'Agent-authored illustrative programs, not recovered historical source and not run: no IBM 7090 FORTRAN II processor or Dartmouth Time-Sharing System was used.',
        'Dialects checked against the IBM 7090/7094 FORTRAN II Programming manual (form C28-6054-5) and the Dartmouth BASIC manual of 1 October 1964; page citations are in evidence/claim-checks.json.',
        'Both programs print one line, HELLO, and end. FORTRAN II needs 4 statements (PRINT, FORMAT, CALL EXIT, END); BASIC needs 2 (PRINT, END). Nothing was added to lengthen FORTRAN: CALL EXIT is required under the FORTRAN II Monitor (C28-6054-5 p.34).',
        'Same code size (48 px DejaVu Sans Mono) and line pitch in both panels. The comparison variant adds line bands, a card-column guide and two captions; it does not resize or move the code.',
        'Neither program uses the manuals’ slashed letter O; plain O is shown in both. Job control cards (FORTRAN) and terminal commands such as RUN (BASIC) are outside both listings.',
        'Release stays blocked under R15 pending editorial review of the length/readability framing.',
    ]
    frames = [{'time': 0, 'file': 'scene-0000.svg'}]
    timeline = {'id': ID, 'durationSeconds': None, 'fps': None, 'width': 1920, 'height': 1080, 'beats': ROW['beats'], 'frames': frames, 'cuts': {}, 'variant_names': ['comparison'], 'motion_model': 'Still asset: one state held for editorial timing; the comparison variant is a separate still.'}
    (src / 'timeline.json').write_text(json.dumps(timeline, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    build = {'id': ID, 'duration': None, 'frames': frames, 'variants': {'comparison': 'variant-comparison.svg'}, 'poster': 'scene.svg', 'cuts': {}, 'notes': notes, 'sources': sources, 'kind': ROW['kind']}
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
    print('AUTHORED', ID, 'code px', CODE, 'char width', round(CW, 2))


if __name__ == '__main__':
    main()
