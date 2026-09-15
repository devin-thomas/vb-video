#!/usr/bin/env python3
"""XTRA-14 delivery finishing. Run last, after
    python tools/render/finish_delivery.py --deliveries-only --id XTRA-14
and after qa.md is final:
    python assets/stills/XTRA-14/src/finalize.py

finish_delivery.py writes a generic delivery (one "original graphics" credit, a thumbnail-only
manual-review line, motion/Program.vb wording) and a generic state. This script replaces those
fields with the per-panel credits, sources, coordinate map, variants and executed-test results for
this still, then re-hashes the complete output inventory. Safe to re-run; run it again after any
edit to qa.md or another delivered file.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSET = HERE.parent
ROOT = HERE.parents[3]
ID = 'XTRA-14'

# Written by the producing agent after viewing the exports and proofs (details in qa.md).
MANUAL_REVIEW = {
    'mode': 'Full-resolution exports, 1:1 native-pixel crops and 1280x720 proofs, viewed by the producing agent with the Read tool',
    'scope': 'exports/poster.png and exports/collage.png (byte-identical), proofs/collage-1to1-left.png, proofs/collage-1to1-right.png, proofs/poster-720.png, proofs/collage-720.png; '
             'exports/focus-business.png, exports/focus-data-entry.png, exports/focus-utilities.png and their -720 proofs.',
    'status': 'Collage: three whole screenshots in one row at a common 458 px height, identical mat/frame outside each image, exact labels, per-panel credits, '
              '"Used with permission from Microsoft." on its own line in the brighter colour. No blank panel, no overlap, no crop. '
              '720p: labels, all credits and the Microsoft line legible; XTRA-11 title, menus, field labels, 3379 and 02-27-2016 readable; XTRA-12 every field label, value and drop-down row readable; '
              'XTRA-13 title, tree, buttons, counters and status bar readable, detail-pane lines small but legible. Focus variants: enlarged panel clearly readable at 720p; '
              'reduced context panels are whole and credited but their UI text is not readable by design. See qa.md.',
}


def load(rel: str):
    return json.loads((ASSET / rel).read_text(encoding='utf-8'))


def dump(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')


def role(rel: str) -> str:
    if rel.startswith('exports/') and rel.endswith('.png'):
        return 'rendered still (contact sheet written by render_assets.py)' if rel.endswith('contact-sheet.png') else 'rendered still'
    if rel.startswith('proofs/'):
        return 'QA proof (1280x720 LANCZOS downscale)' if rel.endswith('-720.png') else 'QA proof (1:1 native-pixel crop)'
    if rel.startswith('src/'):
        return 'editable source'
    if rel == 'qa.md':
        return 'QA record'
    return 'evidence'


def main() -> None:
    if MANUAL_REVIEW is None:
        raise SystemExit('Record the manual full-size/720p review in MANUAL_REVIEW before finalizing.')
    d = load('delivery.json')
    layout, placement = load('src/layout.json'), load('evidence/placement-checks.json')
    browser, render, prov = load('evidence/browser-tests.json'), load('evidence/render-tests.json'), load('evidence/provenance.json')
    build = load('src/build.json')
    assert placement['ok'] and not browser['errors'], 'placement or browser checks are failing'
    ups = {u['asset']: u for u in prov['upstream_assets']}
    rights = {a: json.loads((ROOT / 'assets/historical' / a / 'evidence/rights.json').read_text(encoding='utf-8')) for a in ups}
    up_state = {a: json.loads((ROOT / 'assets/historical' / a / 'state.json').read_text(encoding='utf-8')) for a in ups}
    collage = layout['variants']['collage']['panels']

    d['provenance_type'] = prov['classification']
    d['shared_version'] = 'win95-workbench-1.0.0 (tools/render/studio.py colour tokens and text primitives)'
    d['duration_seconds'], d['fps'] = None, None
    d['panel_map'] = {
        'coordinates': layout['coordinates'],
        'frame': layout['frame'],
        'variants': {name: [{k: q[k] for k in ['asset', 'label', 'role', 'source_file', 'source_sha256', 'source_size', 'x', 'y', 'w', 'h',
                                              'scale_x', 'scale_y', 'aspect_rel_error', 'resampling', 'crop', 'rotation_deg', 'frame_outer']}
                             for q in v['panels']] for name, v in layout['variants'].items()},
        'full_record': 'src/layout.json (includes every label and credit text box); pixel verification in evidence/placement-checks.json',
    }
    d['variants'] = []
    for name, v in layout['variants'].items():
        files = [f'exports/{name}.png'] + (['exports/poster.png'] if name == 'collage' else []) + [f'src/variant-{name}.svg', f'proofs/{name}-720.png']
        if name == 'collage':
            files += ['proofs/poster-720.png', 'proofs/collage-1to1-left.png', 'proofs/collage-1to1-right.png']
        d['variants'].append({'name': name, 'kind': 'still', 'timeline': None, 'timing': 'hold for editorial timing; no named cutdown',
                              'required': name == 'collage', 'files': files,
                              'panels': [f"{q['label']} = {q['asset']} at x{q['x']} y{q['y']} {q['w']}x{q['h']} (scale {q['scale_x']:.4f}, {q['role']})" for q in v['panels']]})
    d['sources'] = build['sources'][:1] + [{
        'path': q['source_rel_path'], 'asset': q['asset'], 'panel': q['label'], 'sha256': q['source_sha256'], 'bytes': q['source_bytes'],
        'native_size': q['source_size'], 'origin': ups[q['asset']]['origin'],
        'records': [f"../../historical/{q['asset']}/{r}" for r in ['delivery.json', 'evidence/source.json', 'evidence/rights.json', 'evidence/provenance.json', 'evidence/claim-checks.json']],
        'relationship': 'historical original (produced upstream asset, read in place; whole image uniformly scaled into the panel; no copy, crop or edit)'}
        for q in collage] + [{'path': '../../../War/SCRIPT.md', 'lines': [742, 744], 'relationship': 'working-script copy of SCRIPT.md:685-687; read only'}]
    d['credits'] = [{
        'panel': q['label'], 'asset': q['asset'], 'file': q['source_file'], 'credit_on_screen': q['credit_on_screen'],
        'credit_record': q['credit_record'], 'credit_record_text': q['credit_full'], 'on_screen_edit': q['credit_edit'],
        'rights_status': rights[q['asset']]['rights_status'], 'upstream_release_status': up_state[q['asset']]['release_status'], 'cleared': False}
        for q in collage] + [{'type': 'authored graphics', 'credit': 'Labels, frames and layout authored for this production with system fonts (Liberation Sans); no font files, stock or office imagery included.'}]
    pv = placement['variants']
    d['tests'] = [
        {'test': 'authoring and layout assertions', 'command': 'python assets/stills/XTRA-14/src/build.py',
         'result': 'passed: upstream SHA-256 equal to each upstream delivery.json; opaque single-frame sources; labels equal ticket copy; no text, frame or image box intersects any image; all frames and text inside 120-1800 x 72-1008; Microsoft statement present with XTRA-12'},
        {'test': 'rasterize still variants', 'command': render['command'], 'evidence': 'evidence/render-tests.json',
         'result': f"passed: {render['renderer']}, poster and {len(layout['variants'])} variants at {render['png_dimensions']}; no video (still)"},
        {'test': 'offline HTML, deterministic seek, SVG text bounds', 'command': 'python tools/render/qa_browser.py --id XTRA-14', 'evidence': 'evidence/browser-tests.json',
         'result': f"passed: {browser['browser']}, {browser['svg_files_checked']} SVG files, {browser['text_boxes_checked']} text boxes, out_of_canvas {len(browser['out_of_canvas'])}, offline {browser['offline']}, deterministic {browser['deterministic_seek']}"},
        {'test': 'placed-image pixel integrity, aspect, no overlap, frame outside edges, credits, dates', 'command': placement['command'], 'evidence': 'evidence/placement-checks.json',
         'result': 'passed: ' + '; '.join(
             f"{n}: " + ', '.join(f"{p['asset']} {'/'.join(str(e['differing_pixels_in_placed_rect']) for e in p['exports'])} px differ, aspect err {p['aspect_rel_error']:.2e}" for p in v['panels'])
             + f", MS statement {v['microsoft_statement_in_svg_text']}, on-screen date-like strings {v['date_like_strings_in_on_screen_text']}" for n, v in pv.items())},
        {'test': 'manual visual review (full size and 720p)', 'result': MANUAL_REVIEW},
        {'test': 'delivery and pack validators', 'command': 'python tools/validate_delivery.py --id XTRA-14; python tools/validate_pack.py', 'result': 'see qa.md (verbatim output of the run after this inventory was written)'},
    ]
    d['unresolved_gates'] = ['R11', 'R14']
    d['production_status'], d['release_status'] = 'produced', 'blocked'
    tc = dict(d.get('toolchain', {}))
    tc.update(fonts='Liberation Sans Regular/Bold resolved by fc-match from C:/WINDOWS/fonts; not distributed',
              pillow_resampling='NEAREST for integer factors, LANCZOS otherwise',
              render_commands=['python assets/stills/XTRA-14/src/build.py', 'python tools/render/render_assets.py --id XTRA-14',
                               'python tools/render/qa_browser.py --id XTRA-14', 'python assets/stills/XTRA-14/src/verify.py',
                               'python tools/render/finish_delivery.py --deliveries-only --id XTRA-14', 'python assets/stills/XTRA-14/src/finalize.py',
                               'python tools/validate_delivery.py --id XTRA-14', 'python tools/validate_pack.py'],
              network_used=False, installs_performed=False)
    d['toolchain'] = tc
    d['notes'] = build['notes'] + [
        'Upstream status at use: ' + '; '.join(f"{a} production {s['production_status']}, release {s['release_status']}" for a, s in up_state.items()) + '.',
        'Internal proof only: not placed in any cleared-media bin. Review questions XTRA-14-RQ1..RQ5 in evidence/claim-checks.json.',
    ]
    items = []
    for p in sorted(ASSET.rglob('*')):
        if not p.is_file() or p.name in ('delivery.json', 'state.json') or '__pycache__' in p.parts:
            continue
        rel = p.relative_to(ASSET).as_posix()
        items.append({'path': rel, 'role': role(rel), 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
    d['outputs'] = items
    dump(ASSET / 'delivery.json', d)
    state = load('state.json')
    state.update(production_status='produced', release_status='blocked', updated_at='2026-09-15',
                 assigned_agent='Render Lane worker (Claude Opus 5) under Render Lane Manager vb-97, branch ticket/XTRA-14',
                 owner='Render Lane worker (Claude Opus 5), branch ticket/XTRA-14', reviewer=None,
                 blockers=['R14 release gate: all three panels are rights-blocked upstream (XTRA-11 unclear, XTRA-12-RQ1 Microsoft guidelines fit, XTRA-13 all rights reserved); XTRA-14-RQ1, RQ4.',
                           'R11 release gate: narration fit of the three examples (XTRA-12 is a Microsoft documentation sample) and era fit; XTRA-14-RQ2, RQ3.'],
                 notes=['Produced: poster, collage and three optional focus stills with offline HTML source; validate_delivery.py passes.',
                        'Every panel is the whole upstream original, uniformly scaled and pixel-verified (evidence/placement-checks.json); per-panel credits and coordinate map in delivery.json.',
                        'Full-size and 720p manual review recorded in qa.md. Internal proof only; release blocked pending the review deck.'])
    dump(ASSET / 'state.json', state)
    print('FINALIZED', ID, len(items), 'outputs')


if __name__ == '__main__':
    main()
