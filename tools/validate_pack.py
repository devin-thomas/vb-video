#!/usr/bin/env python3
"""Validate planning structure only. Does not certify future media or factual claims."""
from __future__ import annotations
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    errors: list[str] = []
    try:
        manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
        lock = json.loads((ROOT / 'sources/LOCK.json').read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        print(f'ERROR: Cannot load pack: {exc}', file=sys.stderr)
        return 1
    rows = manifest['tickets']
    ids = [r['id'] for r in rows]
    id_set = set(ids)
    if len(ids) != len(id_set): errors.append('Duplicate ticket IDs.')
    lines: dict[str, list[str]] = {}
    for entry in lock['files']:
        path = ROOT / entry['path']
        if not path.is_file():
            errors.append(f'Missing original {path.name}')
            continue
        content = path.read_bytes()
        lines[path.name] = content.decode('utf-8').splitlines()
        if hashlib.sha256(content).hexdigest() != entry['sha256']:
            errors.append(f'Original source changed: {path.name}')
        if len(content) != entry['bytes']: errors.append(f'Original size changed: {path.name}')
    register = (ROOT / 'docs/EDITORIAL_REGISTER.md').read_text(encoding='utf-8')
    defined_gates = set(re.findall(r'^## (R\d+[a-z]?)\b', register, flags=re.M))
    for row in rows:
        path = ROOT / row['ticket']
        if not path.is_file():
            errors.append(f'Missing ticket {row["id"]}')
            continue
        text = path.read_text(encoding='utf-8')
        for heading in ['## Assignment and boundaries', '## Creative and technical requirements',
                        '## Deliverables', '## Acceptance checks', '## Embedded source context']:
            if heading not in text: errors.append(f'{row["id"]}: missing {heading}')
        for ref in row['refs']:
            filename, start, end = ref
            if filename not in lines or not (1 <= start <= end <= len(lines.get(filename, []))):
                errors.append(f'{row["id"]}: invalid source range {ref}')
        for dep in row['deps']:
            if dep not in id_set: errors.append(f'{row["id"]}: unknown dependency {dep}')
        for gate in row['gates']:
            if gate not in defined_gates: errors.append(f'{row["id"]}: unknown gate {gate}')
        if not row['required_outputs']: errors.append(f'{row["id"]}: no output contract')
        if len(row['required_outputs']) != len(set(row['required_outputs'])):
            errors.append(f'{row["id"]}: duplicate output paths')
        state_path = ROOT / row['asset_dir'] / 'state.json'
        try:
            state = json.loads(state_path.read_text(encoding='utf-8'))
            if state['id'] != row['id']: errors.append(f'{row["id"]}: state ID mismatch')
        except (OSError, ValueError, KeyError) as exc:
            errors.append(f'{row["id"]}: invalid state: {exc}')
        if row.get('source_hint') == 'literal-program-excerpt':
            refs = [x for x in row['refs'] if x[0] == 'Program.vb']
            if len(refs) != 1:
                errors.append(f'{row["id"]}: ambiguous literal code source')
            else:
                _, lo, hi = refs[0]
                expected = '\n'.join(lines['Program.vb'][lo-1:hi])
                if row['copy'] != expected or expected not in text:
                    errors.append(f'{row["id"]}: literal code payload differs from original')
    graph = {r['id']: r['deps'] for r in rows}
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str) -> None:
        if node in visiting:
            errors.append(f'Dependency cycle involving {node}')
            return
        if node in visited or node not in graph: return
        visiting.add(node)
        for dep in graph[node]: visit(dep)
        visiting.remove(node)
        visited.add(node)
    for item in ids: visit(item)
    families = manifest['families']
    if len([f for f in families if not f['id'].startswith('R2-')]) != 50: errors.append('Original agent family count is not 50.')  # round-2 families (R2-*) are additions
    for family in families:
        if not family['tickets']: errors.append(f'Uncovered family {family["id"]}')
        real = sorted(r['id'] for r in rows if r['parent'] == family['id'])
        if sorted(family['tickets']) != real: errors.append(f'Family mapping mismatch: {family["id"]}')
    original_cues = {i for i, line in enumerate(lines['SCRIPT.md'], 1) if '[VISUAL:' in line}
    mapped_cues = {c['line'] for c in manifest['visual_cues']}
    if original_cues != mapped_cues: errors.append('Inline visual-cue inventory differs from script.')
    for cue in manifest['visual_cues']:
        real = sorted(r['id'] for r in rows if cue['line'] in r['cues'])
        if not real or sorted(cue['tickets']) != real:
            errors.append(f'Uncovered/incorrect cue mapping: line {cue["line"]}')
    if sorted(r['id'] for r in rows if r['id'].startswith('CH-')) != [f'CH-{i:02d}' for i in range(1,17)]:
        errors.append('Chapter card set is not exactly 01–16.')
    counts = manifest['counts']
    if counts['asset_tickets'] != sum(r['kind'] != 'support' for r in rows): errors.append('Asset count mismatch.')
    if counts['coordination_tickets'] != sum(r['kind'] == 'support' for r in rows): errors.append('OPS count mismatch.')
    for i in range(1,8):
        if not (ROOT / f'docs/handoffs/H{i:02d}.md').is_file(): errors.append(f'Missing human handoff H{i:02d}')
    # Derived deck and illustrative fixture integrity, not a test of Program.vb execution.
    deck = json.loads((ROOT / 'tools/fixtures/deck_order.json').read_text())['cards']
    expected_deck = [(r,s) for r in range(2,15) for s in ['S','H','D','C']]
    if [(c['rank'], c['suit']) for c in deck] != expected_deck: errors.append('Deck-order fixture mismatch.')
    if [c['index'] for c in deck] != list(range(52)): errors.append('Deck fixture indices incorrect.')
    war = json.loads((ROOT / 'tools/fixtures/war_storyboard.json').read_text())
    for name in ['single_war','double_war']:
        cards = []
        for event in war[name]['events']:
            if sum(event['counts']) != 52: errors.append(f'{name}: cards not conserved')
            cards.extend(event.get('cards', []))
        if len(cards) != len(set(cards)): errors.append(f'{name}: duplicate physical card')
    shuffle = json.loads((ROOT / 'tools/fixtures/shuffle_storyboard.json').read_text())
    current = shuffle['initial'][:]
    for step in shuffle['swaps']:
        i, j = step['i'], step['j']
        if not 0 <= j <= i < len(current): errors.append('Illegal shuffle fixture bounds')
        if current != step['before']: errors.append('Shuffle fixture before-state mismatch')
        current[i], current[j] = current[j], current[i]
        if current != step['after']: errors.append('Shuffle fixture after-state mismatch')
    if current != shuffle['final']: errors.append('Shuffle fixture final mismatch')
    report = {'ok': not errors, 'checks': ['source hashes/bytes','ticket IDs/sections/output contracts',
              'source ranges and literal code payloads','dependencies and acyclicity','all 50 original families',
              'all inline script visual cues','16 chapter cards','7 human handoffs','illustrative fixture integrity'],
              'asset_tickets': counts['asset_tickets'], 'coordination_tickets':counts['coordination_tickets'],
              'visual_cues':len(original_cues), 'errors':errors,
              'limitations':'Planning structure only. No media, runtime execution, historical facts, or licenses verified.'}
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1

if __name__ == '__main__':
    raise SystemExit(main())
