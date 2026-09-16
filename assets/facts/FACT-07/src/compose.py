#!/usr/bin/env python3
"""Author FACT-07 ("Every run is different") from the four captured War runs.

Every figure on the card is parsed out of the recorded program output
(assets/captures/TERM-*/source/stdout.txt); nothing is typed in by hand.
Run from the repository root:

    python assets/facts/FACT-07/src/compose.py
    python tools/render/render_assets.py --id FACT-07

Writes only inside assets/facts/FACT-07/: src/scene.svg, src/scene-0000.svg,
src/variant-table.svg, src/variant-highlight.svg, src/cells.json, src/build.json,
src/timeline.json, src/index.html, evidence/source-excerpts.md, evidence/provenance.json.
"""
from __future__ import annotations
import hashlib, html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = BASE.parents[2]
sys.path.insert(0, str(ROOT / 'tools' / 'render'))
from studio import SVG, FG, MUTED, LINE, BLUE, PANEL, width  # noqa: E402

ID = 'FACT-07'
TITLE = 'Every run is different'
SUBTITLE = 'Four recorded runs of the same program'
# Run numbering follows the producer's proposal (review/cut-notes-2026-09-16.md:90):
# Run 1 is the 617-round game the narration calls "that first run", Run 4 the 2,008-round game.
# Runs 2 and 3 are the two remaining captures in script order (SCRIPT.md:572 lists TERM-05 before TERM-06).
RUNS = [('Run 1', 'TERM-04'), ('Run 2', 'TERM-05'), ('Run 3', 'TERM-06'), ('Run 4', 'TERM-02')]
NARRATED = {617, 2008}  # rounds the narration singles out (SCRIPT.md:586, 612)

RE_ROUND = re.compile(r'^Round (\d+): ')
RE_WINNER = re.compile(r'^PLAYER (\d) WINS THE WAR!$')
RE_ROUNDS = re.compile(r'^Total rounds played : (\d+)$')
RE_WARS = re.compile(r'^Total wars fought\s+: (\d+)$')
RE_OUT = re.compile(r'^Player (\d) has no cards left for the war - Player (\d) takes the pot\.$')
RE_DRAW = re.compile(r'DRAW|No winner after')


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_run(label: str, capture: str) -> dict:
    """Parse one capture's stdout. Line numbers are 1-based, as in the evidence file."""
    rel = f'assets/captures/{capture}/source/stdout.txt'
    path = ROOT / rel
    lines = path.read_text(encoding='utf-8').splitlines()
    found: dict = {}
    last_round_line = None
    for n, line in enumerate(lines, 1):
        if RE_ROUND.match(line):
            last_round_line = n
        for key, rx in (('winner', RE_WINNER), ('rounds', RE_ROUNDS), ('wars', RE_WARS)):
            m = rx.match(line)
            if m:
                assert key not in found, f'{capture}: duplicate {key} line'
                found[key] = (int(m.group(1)), n, line)
        if RE_DRAW.search(line):
            raise SystemExit(f'{capture}: draw/cap message present at line {n}; the card assumes a decided game')
    for key in ('winner', 'rounds', 'wars'):
        assert key in found, f'{capture}: no {key} line in stdout'
    # How the game ended: the lines after the last "Round N:" line, before the summary block.
    tail = [(n, lines[n - 1]) for n in range(last_round_line, found['winner'][1])]
    out = [(n, l, RE_OUT.match(l)) for n, l in tail if RE_OUT.match(l)]
    if out:
        n, line, m = out[-1]
        assert len(out) == 1
        ending = {'text': f'Player {m.group(1)} ran out of cards in a war', 'line': n, 'source': line}
        assert m.group(2) == str(found['winner'][0])
    else:
        n, line = tail[0]
        ending = {'text': 'Normal round win', 'line': n, 'source': line, 'last_round_line': last_round_line,
                  'last_round': lines[last_round_line - 1]}
    return {
        'run': label, 'capture': capture, 'stdout': rel, 'stdout_sha256': sha256(path), 'stdout_lines': len(lines),
        'rounds': found['rounds'][0], 'rounds_line': found['rounds'][1], 'rounds_source': found['rounds'][2],
        'wars': found['wars'][0], 'wars_line': found['wars'][1], 'wars_source': found['wars'][2],
        'winner': f'Player {found["winner"][0]}', 'winner_line': found['winner'][1], 'winner_source': found['winner'][2],
        'ending': ending,
    }


def fmt(n: int) -> str:
    return f'{n:,}'


# Column geometry (canvas 1920 × 1080; essential text within x 120…1800, y 72…1008).
X_RUN, X_ROUNDS, X_WARS, X_WINNER, X_END = 152, 640, 860, 950, 1200
Y_HEAD, Y_RULE, Y0, STEP = 312, 340, 430, 118


def scene(rows: list[dict], highlight: bool) -> str:
    s = SVG(title=TITLE)
    s.text(TITLE, 120, 170, 64, FG, True)
    s.text(SUBTITLE, 120, 222, 30, MUTED)
    for label, x, anchor in (('Run', X_RUN, 'start'), ('Rounds', X_ROUNDS, 'end'), ('Wars', X_WARS, 'end'),
                             ('Winner', X_WINNER, 'start'), ('How it ended', X_END, 'start')):
        s.text(label, x, Y_HEAD, 30, MUTED, anchor=anchor)
    s.line(120, Y_RULE, 1800, Y_RULE, MUTED, 2)
    for i, r in enumerate(rows):
        y = Y0 + i * STEP
        marked = r['rounds'] in NARRATED
        if highlight and marked:
            s.rect(120, y - 72, 1680, STEP - 8, PANEL, rx=4)
            s.rect(120, y - 72, 8, STEP - 8, BLUE, rx=2)
        col = MUTED if (highlight and not marked) else FG
        s.text(r['run'], X_RUN, y, 44, col, True)
        s.text(fmt(r['rounds']), X_ROUNDS, y, 48, col, True, anchor='end')
        s.text(fmt(r['wars']), X_WARS, y, 48, col, True, anchor='end')
        s.text(r['winner'], X_WINNER, y, 44, col, True)
        s.text(r['ending']['text'], X_END, y, 34, MUTED if highlight and not marked else FG)
        if i < len(rows) - 1:
            s.line(120, y + STEP - 58, 1800, y + STEP - 58, LINE, 2)
    s.line(120, Y0 + len(rows) * STEP - 58, 1800, Y0 + len(rows) * STEP - 58, MUTED, 2)
    lo = min(rows, key=lambda r: r['rounds']); hi = max(rows, key=lambda r: r['rounds'])
    footer = f'Shortest run: {fmt(lo["rounds"])} rounds ({lo["run"]})   ·   Longest run: {fmt(hi["rounds"])} rounds ({hi["run"]})'
    s.text(footer, 120, 960, 36, BLUE, True)
    return s.finish()


def check_bounds(svg: str) -> None:
    """Approximate right-edge check with the same font metrics the studio uses."""
    for m in re.finditer(r'<text x="([\d.]+)" y="([\d.]+)" font-family="[^"]+" font-size="(\d+)" font-weight="(\d+)"[^>]*text-anchor="(\w+)"[^>]*>([^<]*)</text>', svg):
        x, y, size, weight, anchor, text = float(m[1]), float(m[2]), int(m[3]), m[4], m[5], html.unescape(m[6])
        w = width(text, size, 'bold' if weight == '700' else 'sans')
        left = x - w if anchor == 'end' else x - w / 2 if anchor == 'middle' else x
        right = left + w
        assert 120 <= left and right <= 1800, f'text outside safe area: {text!r} {left:.0f}-{right:.0f}'
        assert 72 <= y - size <= y <= 1008, f'text outside safe area vertically: {text!r}'


def index_html(timeline: dict, scenes: dict) -> str:
    t = html.escape(TITLE)
    return ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{t}</title><style>html,body{{margin:0;background:#000;height:100%;overflow:hidden}}#stage{{width:100%;height:100%;display:flex;align-items:center;justify-content:center}}svg{{width:100%;height:100%;object-fit:contain}}</style>'
            f'<div id="stage" aria-label="{t}"></div><script>const timeline={json.dumps(timeline)};const scenes={json.dumps(scenes)};'
            "const stage=document.getElementById('stage');window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;else break}stage.innerHTML=scenes[f.file];return f.file}};__ASSET__.renderAt(0);let start=null,playing=false;document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();playing=!playing;start=null;requestAnimationFrame(tick)}if(e.code==='Home'){playing=false;__ASSET__.renderAt(0)}});function tick(ts){if(!playing)return;if(start===null)start=ts;const t=(ts-start)/1000;__ASSET__.renderAt(t);if(t<__ASSET__.durationSeconds)requestAnimationFrame(tick);else playing=false}</script></html>")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')


def dump(path: Path, data) -> None:
    write(path, json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def main() -> None:
    rows = [read_run(label, cap) for label, cap in RUNS]
    assert {r['rounds'] for r in rows} >= NARRATED, 'the two narrated runs (617, 2008 rounds) must be present'
    table = scene(rows, False); hl = scene(rows, True)
    check_bounds(table); check_bounds(hl)
    for name, svg in (('scene.svg', table), ('scene-0000.svg', table), ('variant-table.svg', table), ('variant-highlight.svg', hl)):
        write(HERE / name, svg)
    (BASE / 'proofs').mkdir(exist_ok=True)

    script = ROOT / 'War/SCRIPT.md'; frozen = ROOT / 'sources/SCRIPT.md'
    sources = [{'path': f'../../captures/{r["capture"]}/source/stdout.txt', 'lines': [r['ending']['line'] if r['ending']['text'].startswith('Normal') else r['ending']['line'], r['wars_line']],
                'sha256': r['stdout_sha256'], 'relationship': 'real capture'} for r in rows]
    sources += [{'path': '../../../War/SCRIPT.md', 'lines': [574, 574], 'sha256': sha256(script), 'relationship': 'source creative brief'},
                {'path': '../../../sources/SCRIPT.md', 'lines': [571, 571], 'sha256': sha256(frozen), 'relationship': 'source creative brief'}]
    notes = [
        'Every figure is parsed from the captured stdout of the four recorded runs by src/compose.py; src/cells.json records the file and line of each.',
        'Run numbering is a production choice from the producer\'s proposal (Run 1 = the 617-round game the narration calls "that first run", Run 4 = the 2,008-round game); runs 2 and 3 follow script order.',
        'Fact-card treatment: dark card, one bold line per row, right-aligned tabular figures; highlight marks the two runs the narration singles out and dims the other two.',
        'The recordings under recordings/ (R2, R3a, R3b, R4-01..R4-04) are different games from these four captures and are not on this card.',
    ]
    build = {'id': ID, 'duration': None, 'frames': [{'time': 0, 'file': 'scene-0000.svg'}],
             'variants': {'table': 'variant-table.svg', 'highlight': 'variant-highlight.svg'}, 'poster': 'scene.svg', 'cuts': {},
             'notes': notes, 'sources': sources, 'kind': 'still'}
    dump(HERE / 'build.json', build)
    timeline = {'id': ID, 'durationSeconds': None, 'fps': None, 'width': 1920, 'height': 1080,
                'beats': ['Still: the four-row table.', 'Still: highlight with the two named runs marked.'],
                'frames': build['frames'], 'cuts': {}, 'variant_names': list(build['variants']),
                'motion_model': 'Still asset; renderAt(t) always shows the single authored state.'}
    dump(HERE / 'timeline.json', timeline)
    write(HERE / 'index.html', index_html(timeline, {'scene-0000.svg': table}))
    lo = min(rows, key=lambda r: r['rounds']); hi = max(rows, key=lambda r: r['rounds'])
    dump(HERE / 'cells.json', {'id': ID, 'title': TITLE, 'subtitle': SUBTITLE, 'columns': ['Run', 'Rounds', 'Wars', 'Winner', 'How it ended'],
                               'rows': rows, 'footer': {'shortest': lo['run'], 'shortest_rounds': lo['rounds'], 'longest': hi['run'], 'longest_rounds': hi['rounds']},
                               'highlight_rounds': sorted(NARRATED)})

    ex = ['# FACT-07 — source excerpts', '',
          'Each figure on the card, with the captured stdout line it was read from (1-based line numbers; the stdout files are unchanged captures, hashes below).', '']
    for r in rows:
        ex += [f'## {r["run"]} — {r["capture"]} — `{r["stdout"]}` ({r["stdout_lines"]} lines, sha256 {r["stdout_sha256"]})', '', '| Card cell | Value | Line | Captured text |', '|---|---|---:|---|',
               f'| Rounds | {fmt(r["rounds"])} | {r["rounds_line"]} | `{r["rounds_source"]}` |',
               f'| Wars | {r["wars"]} | {r["wars_line"]} | `{r["wars_source"]}` |',
               f'| Winner | {r["winner"]} | {r["winner_line"]} | `{r["winner_source"]}` |',
               f'| How it ended | {r["ending"]["text"]} | {r["ending"]["line"]} | `{r["ending"]["source"]}` |']
        if 'last_round' in r['ending']:
            ex += ['', f'Normal ending: the last round (line {r["ending"]["last_round_line"]}) is an ordinary win and no "has no cards left for the war" line follows it before the summary (line {r["winner_line"]}).']
        ex += ['']
    ex += ['## Footer', '', f'Shortest run: {fmt(lo["rounds"])} rounds ({lo["run"]}, {lo["capture"]} line {lo["rounds_line"]}); longest run: {fmt(hi["rounds"])} rounds ({hi["run"]}, {hi["capture"]} line {hi["rounds_line"]}).', '',
           '## War/SCRIPT.md:574 (narration this card sits under)', '', '```text', script.read_text(encoding='utf-8').splitlines()[573], '```', '',
           '## sources/SCRIPT.md:571 (frozen source, manifest reference)', '', '```text', frozen.read_text(encoding='utf-8').splitlines()[570], '```', '']
    write(BASE / 'evidence/source-excerpts.md', '\n'.join(ex))
    dump(BASE / 'evidence/provenance.json', {'id': ID, 'classification': 'original authored source-based illustration', 'sources': sources,
                                             'authored_additions': notes, 'source_unchanged': True, 'remote_assets': [], 'font_files_distributed': False, 'producer_decisions': []})
    for r in rows:
        print(f'{r["run"]} {r["capture"]}: rounds {r["rounds"]} (l.{r["rounds_line"]}), wars {r["wars"]} (l.{r["wars_line"]}), {r["winner"]} (l.{r["winner_line"]}), {r["ending"]["text"]} (l.{r["ending"]["line"]})')
    print('AUTHORED', ID)


if __name__ == '__main__':
    main()
