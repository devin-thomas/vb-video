#!/usr/bin/env python3
"""Author FACT-08 (two endgames side by side) from the script cue, checked against the captures.

The card copy is the script's own cue text (War/SCRIPT.md:624-626, relabelled Run 1 / Run 4 by the
ticket). Each step is checked against the captured stdout of the two runs: the played rank and the
"no cards left" line are read directly; the hand sizes, burn count and pot size are reconstructed
from the transcript (every "wins the round (N cards)" line moves N/2 cards from loser to winner, and
Program.vb:264 caps the burn at the shorter hand). Run from the repository root:

    python assets/facts/FACT-08/src/compose.py
    python tools/render/render_assets.py --id FACT-08

Writes only inside assets/facts/FACT-08/.
"""
from __future__ import annotations
import hashlib, html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = BASE.parents[2]
sys.path.insert(0, str(ROOT / 'tools' / 'render'))
from studio import SVG, FG, MUTED, LINE, BLUE, PANEL, width  # noqa: E402

ID = 'FACT-08'
TITLE = 'Two endgames side by side'
KICKER = 'When the cards run out'  # section 12 title, War/SCRIPT.md:581
# Verbatim from docs/tickets/FACT-08.md "Exact copy"; the script cue (War/SCRIPT.md:625-626) labels the
# same sequences TERM-04 and TERM-02.
COLUMNS = [
    {'header': 'Run 1 · 617 rounds', 'steps': ['2 cards', 'play 10', 'burn 1', 'empty', '4-card pot'], 'capture': 'TERM-04', 'round': 617, 'script_line': 625},
    {'header': 'Run 4 · 2,008 rounds', 'steps': ['3 cards', 'play 8', 'burn 2', 'empty', '6-card pot'], 'capture': 'TERM-02', 'round': 2008, 'script_line': 626},
]

RE_ROUND = re.compile(r'^Round (\d+): Player 1 plays (\S+) of \w+, Player 2 plays (\S+) of \w+\.$')
RE_WIN = re.compile(r'^\s+Player (\d) wins the round \((\d+) cards\)\.$')
RE_OUT = re.compile(r'^Player (\d) has no cards left for the war - Player (\d) takes the pot\.$')
RE_ROUNDS = re.compile(r'^Total rounds played : (\d+)$')


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check_column(col: dict) -> dict:
    """Reconstruct the final round of one capture from its stdout and compare with the cue."""
    rel = f'assets/captures/{col["capture"]}/source/stdout.txt'
    path = ROOT / rel
    lines = path.read_text(encoding='utf-8').splitlines()
    p1 = p2 = 26
    final = None
    for n, line in enumerate(lines, 1):
        m = RE_ROUND.match(line)
        if m and int(m.group(1)) == col['round']:
            final = {'round_line': n, 'round_text': line, 'p1_before': p1, 'p2_before': p2, 'rank1': m.group(2), 'rank2': m.group(3)}
        m = RE_WIN.match(line)
        if m:
            half = int(m.group(2)) // 2
            if m.group(1) == '1':
                p1 += half; p2 -= half
            else:
                p2 += half; p1 -= half
        m = RE_OUT.match(line)
        if m and final and 'out_line' not in final:
            final.update(out_line=n, out_text=line, loser=int(m.group(1)), winner=int(m.group(2)))
        m = RE_ROUNDS.match(line)
        if m:
            final.update(total_line=n, total_text=line, total=int(m.group(1)))
    assert final and 'out_line' in final, f'{col["capture"]}: round {col["round"]} did not end with a "no cards left" line'
    assert final['total'] == col['round']
    assert final['rank1'] == final['rank2'], 'the final round must be a tie'
    short = min(final['p1_before'], final['p2_before'])
    after_play = short - 1
    burn = min(3, min(final['p1_before'] - 1, final['p2_before'] - 1))  # Program.vb:264 after both played one card
    pot = 2 + 2 * burn
    derived = [f'{short} cards', f'play {final["rank1"]}', f'burn {burn}', 'empty' if after_play - burn == 0 else f'{after_play - burn} left', f'{pot}-card pot']
    loser_hand = final['p1_before'] if final['loser'] == 1 else final['p2_before']
    assert loser_hand == short
    return {**col, 'stdout': rel, 'stdout_sha256': sha256(path), 'stdout_lines': len(lines), 'derived_steps': derived,
            'matches_script': derived == col['steps'], 'hand_before': {'player1': final['p1_before'], 'player2': final['p2_before']},
            'burn': burn, 'pot': pot, 'evidence': final}


# Geometry (canvas 1920 × 1080; essential text within x 120…1800, y 72…1008).
CX = (600, 1320); Y_KICKER, Y_TITLE, Y_HEAD, Y0, STEP = 150, 222, 330, 450, 118


def scene(cols: list[dict], focus: bool) -> str:
    s = SVG(title=TITLE)
    s.text(KICKER, 120, Y_KICKER, 30, MUTED)
    s.text(TITLE, 120, Y_TITLE, 64, FG, True)
    s.line(960, Y_HEAD - 60, 960, Y0 + 4 * STEP + 30, LINE, 3)
    s.line(120, Y_HEAD + 32, 1800, Y_HEAD + 32, MUTED, 2)
    for cx, col in zip(CX, cols):
        s.text(col['header'], cx, Y_HEAD, 48, FG, True, anchor='middle')
        n = len(col['steps'])
        for i, step in enumerate(col['steps']):
            y = Y0 + i * STEP
            last = i == n - 1
            if last:
                w = width(step, 56, 'bold') + 72
                if focus:
                    s.rect(cx - w / 2, y - 58, w, 84, PANEL, stroke=BLUE, sw=3, rx=6)
                s.text(step, cx, y, 56, BLUE, True, anchor='middle')
            else:
                s.text(step, cx, y, 44, MUTED if focus else FG, anchor='middle')
            if not last:
                s.arrow(cx, y + 22, cx, y + STEP - 62, LINE if focus else MUTED, 3)
    return s.finish()


def check_bounds(svg: str) -> None:
    for m in re.finditer(r'<text x="([\d.]+)" y="([\d.]+)" font-family="[^"]+" font-size="(\d+)" font-weight="(\d+)"[^>]*text-anchor="(\w+)"[^>]*>([^<]*)</text>', svg):
        x, y, size, weight, anchor, text = float(m[1]), float(m[2]), int(m[3]), m[4], m[5], html.unescape(m[6])
        w = width(text, size, 'bold' if weight == '700' else 'sans')
        left = x - w if anchor == 'end' else x - w / 2 if anchor == 'middle' else x
        assert 120 <= left and left + w <= 1800, f'text outside safe area: {text!r}'
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
    cols = [check_column(c) for c in COLUMNS]
    comparison = scene(cols, False); focus = scene(cols, True)
    check_bounds(comparison); check_bounds(focus)
    for name, svg in (('scene.svg', comparison), ('scene-0000.svg', comparison), ('variant-comparison.svg', comparison), ('variant-step-focus.svg', focus)):
        write(HERE / name, svg)
    (BASE / 'proofs').mkdir(exist_ok=True)

    script = ROOT / 'War/SCRIPT.md'; frozen = ROOT / 'sources/SCRIPT.md'; program = ROOT / 'sources/Program.vb'
    sources = [{'path': f'../../captures/{c["capture"]}/source/stdout.txt', 'lines': [c['evidence']['round_line'], c['evidence']['total_line']],
                'sha256': c['stdout_sha256'], 'relationship': 'real capture'} for c in cols]
    sources += [{'path': '../../../War/SCRIPT.md', 'lines': [624, 626], 'sha256': sha256(script), 'relationship': 'source creative brief'},
                {'path': '../../../sources/SCRIPT.md', 'lines': [267, 267], 'sha256': sha256(frozen), 'relationship': 'source creative brief'},
                {'path': '../../../sources/Program.vb', 'lines': [264, 264], 'sha256': sha256(program), 'relationship': 'literal excerpt'}]
    agree = all(c['matches_script'] for c in cols)
    notes = [
        'Both columns are the script cue (War/SCRIPT.md:625-626) word for word, with the ticket\'s Run 1 / Run 4 labels in place of the capture IDs; each step on its own line, drawn arrows as connectors, the final step emphasised.',
        'Checked against the captured stdout of both runs by src/compose.py: the played rank and the "no cards left" line are read directly; hand sizes, burn and pot are reconstructed from the transcript (src/cells.json, evidence/endgame-check.json). '
        + ('The reconstruction agrees with the script on every step.' if agree else 'DISAGREEMENT with the script recorded in evidence/endgame-check.json; the card keeps the script wording.'),
        'The two columns share one baseline grid so the steps align row by row; step-focus boxes the final step of each column and dims the earlier steps.',
        'Kicker "When the cards run out" is the script\'s section 12 title (War/SCRIPT.md:581); "Two endgames side by side" is the ticket title.',
    ]
    build = {'id': ID, 'duration': None, 'frames': [{'time': 0, 'file': 'scene-0000.svg'}],
             'variants': {'comparison': 'variant-comparison.svg', 'step-focus': 'variant-step-focus.svg'}, 'poster': 'scene.svg', 'cuts': {},
             'notes': notes, 'sources': sources, 'kind': 'still'}
    dump(HERE / 'build.json', build)
    timeline = {'id': ID, 'durationSeconds': None, 'fps': None, 'width': 1920, 'height': 1080,
                'beats': ['Still: both columns.', 'Still: step-focus with the final step of each column highlighted.'],
                'frames': build['frames'], 'cuts': {}, 'variant_names': list(build['variants']),
                'motion_model': 'Still asset; renderAt(t) always shows the single authored state.'}
    dump(HERE / 'timeline.json', timeline)
    write(HERE / 'index.html', index_html(timeline, {'scene-0000.svg': comparison}))
    dump(HERE / 'cells.json', {'id': ID, 'kicker': KICKER, 'title': TITLE,
                               'columns': [{k: c[k] for k in ('header', 'steps', 'capture', 'round', 'script_line', 'stdout', 'derived_steps', 'matches_script')} for c in cols]})
    dump(BASE / 'evidence/endgame-check.json', {'id': ID, 'method': 'Hand sizes reconstructed from every "wins the round (N cards)" line (N/2 cards move from loser to winner; each side contributes half of any pot because Program.vb:264 burns the same count from both hands). Burn = min(3, shorter hand after both played one card); pot = 2 played + 2 × burn.',
                                                'columns': [{k: c[k] for k in ('header', 'capture', 'round', 'steps', 'derived_steps', 'matches_script', 'hand_before', 'burn', 'pot', 'evidence', 'stdout', 'stdout_sha256')} for c in cols],
                                                'all_match': agree})

    sl = script.read_text(encoding='utf-8').splitlines(); pl = program.read_text(encoding='utf-8').splitlines()
    ex = ['# FACT-08 — source excerpts', '', '## Card copy — War/SCRIPT.md:624–626 (the cue), relabelled per docs/tickets/FACT-08.md', '', '```text', *sl[623:626], '```', '',
          'The ticket\'s exact copy replaces the capture IDs with run labels: "Run 1 · 617 rounds" (TERM-04) and "Run 4 · 2,008 rounds" (TERM-02).', '']
    for c in cols:
        e = c['evidence']
        ex += [f'## {c["header"]} — {c["capture"]} — `{c["stdout"]}` ({c["stdout_lines"]} lines, sha256 {c["stdout_sha256"]})', '',
               '| Step | Card | Check | Evidence |', '|---|---|---|---|',
               f'| hand | {c["steps"][0]} | reconstructed: Player 1 {c["hand_before"]["player1"]}, Player 2 {c["hand_before"]["player2"]} going into round {c["round"]} | every `wins the round (N cards)` line up to line {e["round_line"] - 1} |',
               f'| play | {c["steps"][1]} | both played rank {e["rank1"]} | line {e["round_line"]}: `{e["round_text"]}` |',
               f'| burn | {c["steps"][2]} | min(3, {min(c["hand_before"].values())} − 1) = {c["burn"]} | Program.vb:264 `{pl[263].strip()}` |',
               f'| empty | {c["steps"][3]} | {min(c["hand_before"].values())} − 1 − {c["burn"]} = 0 | line {e["out_line"]}: `{e["out_text"]}` |',
               f'| pot | {c["steps"][4]} | 2 played + 2 × {c["burn"]} burned = {c["pot"]} | same lines; Player {e["winner"]} takes the pot |',
               f'| rounds | {c["header"].split("· ")[1]} | total | line {e["total_line"]}: `{e["total_text"]}` |', '',
               f'Reconstruction: {" → ".join(c["derived_steps"])} — {"matches the script" if c["matches_script"] else "DOES NOT match the script"}.', '']
    ex += ['## War/SCRIPT.md:581 (section title used as the kicker)', '', '```text', sl[580], '```', '',
           '## sources/SCRIPT.md:267 (frozen source, manifest reference)', '', '```text', frozen.read_text(encoding='utf-8').splitlines()[266], '```', '']
    write(BASE / 'evidence/source-excerpts.md', '\n'.join(ex))
    dump(BASE / 'evidence/provenance.json', {'id': ID, 'classification': 'original authored source-based illustration', 'sources': sources,
                                             'authored_additions': notes, 'source_unchanged': True, 'remote_assets': [], 'font_files_distributed': False, 'producer_decisions': []})
    for c in cols:
        print(f'{c["header"]} [{c["capture"]}]: script {c["steps"]} | derived {c["derived_steps"]} | match={c["matches_script"]} | hands before {c["hand_before"]}')
    print('AUTHORED', ID, 'all_match' if agree else 'MISMATCH')


if __name__ == '__main__':
    main()
