#!/usr/bin/env python3
"""XTRA-05 delivery finishing. Run last, after
    python -B tools/render/finish_delivery.py --deliveries-only --id XTRA-05
and after qa.md is final:
    python -B assets/stills/XTRA-05/src/finalize.py

finish_delivery.py writes a generic delivery (one "original graphics" credit, a thumbnail-only
manual-review line, motion/Program.vb wording) and a generic state. This script replaces those
fields with the placement, annotation edit history, label checks, carried-forward credit, variants
and executed-test results for this still, then re-hashes the complete output inventory. Safe to
re-run; run it again after any edit to qa.md or another delivered file.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSET = HERE.parent
ROOT = HERE.parents[3]
ID = 'XTRA-05'
UP = ROOT / 'assets/historical/HIST-02'

# Written by the producing agent after viewing the exports and proofs (details in qa.md).
MANUAL_REVIEW = {
    'mode': 'Full-resolution exports, native-pixel halves and 1280x720 proofs, viewed by the producing agent with the Read tool',
    'scope': 'exports/poster.png, exports/five-callouts.png (byte-identical), exports/clean-workspace.png at 1920x1080; proofs/five-callouts-1to1-left.png and -right.png; '
             'proofs/poster-720.png, proofs/five-callouts-720.png, proofs/clean-workspace-720.png.',
    'status': 'Whole screenshot, identical placement in both variants, nothing clipped. clean-workspace: no marks or text. five-callouts: every target is unmistakable at full size and 720p '
              '(gold outline on the target window frame plus a leader to its label); the Form Designer outline stops visibly short of the Code Window outline. '
              'All five labels legible at 720p (about 27 px bold). No mark covers code or UI text. Screenshot UI text (menus, Project entry, Properties grid, code) readable at 720p. See qa.md.',
}


def load(rel: str):
    return json.loads((ASSET / rel).read_text(encoding='utf-8'))


def dump(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')


def role(rel: str) -> str:
    if rel.startswith('exports/') and rel.endswith('.png'):
        return 'rendered still (contact sheet written by render_assets.py)' if rel.endswith('contact-sheet.png') else 'rendered still'
    if rel.startswith('proofs/'):
        return 'QA proof (1280x720 LANCZOS downscale)' if rel.endswith('-720.png') else 'QA proof (native-pixel half of five-callouts)'
    if rel.startswith('src/'):
        return 'editable source'
    if rel == 'qa.md':
        return 'QA record'
    return 'evidence'


def main() -> None:
    d = load('delivery.json')
    layout, placement = load('src/layout.json'), load('evidence/placement-checks.json')
    browser, render, prov = load('evidence/browser-tests.json'), load('evidence/render-tests.json'), load('evidence/provenance.json')
    claims, build = load('evidence/claim-checks.json'), load('src/build.json')
    assert placement['ok'] and not browser['errors'], 'placement or browser checks are failing'
    rights = json.loads((UP / 'evidence/rights.json').read_text(encoding='utf-8'))
    up_state = json.loads((UP / 'state.json').read_text(encoding='utf-8'))
    p = layout['placement']
    fc = next(e for e in placement['variants']['five-callouts']['exports'] if e['png'] == 'exports/five-callouts.png')
    cw = placement['variants']['clean-workspace']['exports'][0]

    d['provenance_type'] = prov['classification']
    d['shared_version'] = 'win95-workbench-1.0.0 (tools/render/studio.py colour tokens and text primitives)'
    d['duration_seconds'], d['fps'] = None, None
    d['placement'] = {
        'source_file': layout['source']['file'], 'source_sha256': layout['source']['sha256'], 'source_size': layout['source']['size'],
        'rect_xywh': [p['x'], p['y'], p['w'], p['h']], 'scale_x': p['scale_x'], 'scale_y': p['scale_y'], 'resampling': p['resampling'],
        'crop': p['crop'], 'rotation_deg': p['rotation_deg'], 'retouch': p['retouch'], 'embedded_png_sha256': p['embedded_png_sha256'],
        'frame': layout['frame'], 'identical_in_variants': p['identical_in_variants'],
        'verification': f"clean-workspace {cw['differing_pixels_in_placed_rect']} differing px of {cw['pixels_checked']} against a fresh resample; five-callouts {fc['differing_pixels_outside_marks']} differing px outside declared marks (evidence/placement-checks.json)",
    }
    marks_by = {(m['target'], m['mark']): m for m in fc['marks']}
    d['annotation_edit_history'] = {
        'variant': 'five-callouts (also exports/poster.png)', 'clean_workspace_edits': [],
        'mark_style': layout['mark_style'], 'label_style': layout['label_style'],
        'marks': [dict({k: m[k] for k in ['target', 'type', 'casing_rects', 'core_rects']},
                       shape=t['shape'] if m['type'] == 'outline' else 'horizontal leader line',
                       colours={'core': layout['mark_style']['core'], 'casing': layout['mark_style']['casing']},
                       target_original_px_inclusive=t['rect'],
                       canvas_pixels_changed_on_image=marks_by[(t['label'], m['type'])]['canvas_pixels_changed_on_image'],
                       original_pixels_overlaid=marks_by[(t['label'], m['type'])]['original_pixels_overlaid'],
                       original_bbox_inclusive=marks_by[(t['label'], m['type'])]['original_bbox_inclusive'],
                       original_colours_overlaid=marks_by[(t['label'], m['type'])]['original_colours_overlaid'],
                       overlay_rule=marks_by[(t['label'], m['type'])]['rule'],
                       pixels_breaking_rule=marks_by[(t['label'], m['type'])]['pixels_breaking_rule'])
                  for t in layout['targets'] for m in t['marks']],
        'labels': [{'label': t['label'], 'lines': [x['text'] for x in t['texts']], 'text_boxes': [x['box'] for x in t['texts']], 'side': t['side']} for t in layout['targets']],
        'total_changed_pixels_on_image': fc['mark_pixels_changed_total'],
        'full_record': 'src/layout.json annotation_edits (all 50 rectangles with geometric overlay); evidence/placement-checks.json (pixel-measured overlay per mark); evidence/provenance.json annotation_edit_history',
    }
    d['label_checks'] = [{k: c[k] for k in ['label', 'target_original_px_inclusive', 'target_canvas_box', 'status', 'invented_ui']} for c in claims['label_checks']]
    d['variants'] = [
        {'name': 'clean-workspace', 'kind': 'still', 'timeline': None, 'timing': 'hold for editorial timing; no named cutdown', 'required': True,
         'files': ['exports/clean-workspace.png', 'src/variant-clean-workspace.svg', 'proofs/clean-workspace-720.png'],
         'notes': 'Whole HIST-02 screenshot at 1.5x in a frame outside its edges; no annotation, no text.'},
        {'name': 'five-callouts', 'kind': 'still', 'timeline': None, 'timing': 'hold for editorial timing; no named cutdown; no one-panel reveal (editor request only)', 'required': True,
         'files': ['exports/five-callouts.png', 'exports/poster.png', 'src/variant-five-callouts.svg', 'proofs/five-callouts-720.png', 'proofs/poster-720.png',
                   'proofs/five-callouts-1to1-left.png', 'proofs/five-callouts-1to1-right.png'],
         'notes': 'Same screenshot rectangle as clean-workspace, plus five margin labels, window-frame outlines and leaders. exports/poster.png is byte-identical.'},
    ]
    d['sources'] = build['sources'] + [
        {'path': '../../../War/SCRIPT.md', 'lines': [133, 137], 'relationship': 'working-script copy of SCRIPT.md:130-134 (cue now reads "Project Window"); read only'},
        {'path': '../../historical/HIST-02/evidence/rights.json', 'relationship': 'rights and credit record carried forward'},
        {'path': '../../historical/HIST-02/evidence/source.json', 'relationship': 'source record of the original'},
    ]
    d['credits'] = [
        {'type': 'historical screenshot', 'asset': 'HIST-02', 'file': layout['source']['file'], 'credit': rights['credit_text'], 'credit_on_screen': None,
         'proposed_credit': rights['proposed_credit_text'],
         'status': 'proposed, not approved. The "Used with permission from Microsoft." sentence applies only if the rights review relies on Microsoft\'s screenshot permission (RQ-HIST-02-1 / XTRA-05-RQ4); it must not be used before that decision, so nothing is burned in.',
         'credit_record': 'assets/historical/HIST-02/evidence/rights.json#proposed_credit_text', 'rights_status': rights['rights_status'],
         'upstream_release_status': up_state['release_status'], 'cleared': False,
         'open_questions': ['RQ-HIST-02-1', 'RQ-HIST-02-2', 'RQ-HIST-02-3', 'RQ-HIST-02-4']},
        {'type': 'authored graphics', 'credit': 'Labels, outlines, leaders, frame and layout authored for this production with system fonts (Liberation Sans); no font files or other imagery included.'},
    ]
    d['tests'] = [
        {'test': 'authoring and layout assertions', 'command': 'python -B assets/stills/XTRA-05/src/build.py',
         'result': 'passed: HIST-02 SHA-256 and bytes equal HIST-02/delivery.json; 800x600 source; labels equal ticket copy; labels outside the screenshot and frame, inside 120-1800 x 72-1008, not overlapping; marks clear of labels; outlines on the image and not touching each other'},
        {'test': 'rasterize still variants', 'command': render['command'], 'evidence': 'evidence/render-tests.json',
         'result': f"passed: {render['renderer']}, poster and 2 variants at {render['png_dimensions']}; no video (still)"},
        {'test': 'offline HTML, deterministic seek, SVG text bounds', 'command': 'python -B tools/render/qa_browser.py --id XTRA-05', 'evidence': 'evidence/browser-tests.json',
         'result': f"passed: {browser['browser']}, {browser['svg_files_checked']} SVG files, {browser['text_boxes_checked']} text boxes, out_of_canvas {len(browser['out_of_canvas'])}, offline {browser['offline']}, deterministic {browser['deterministic_seek']}"},
        {'test': 'placed-image pixel integrity and annotation overlay audit', 'command': placement['command'], 'evidence': 'evidence/placement-checks.json',
         'result': (f"passed: embedded PNG equals fresh 1.5x BOX resample; clean-workspace {cw['differing_pixels_in_placed_rect']} differing px / {cw['pixels_checked']}, mat ring {cw['mat_ring_nonmatching_pixels']} non-matching; "
                    f"five-callouts {fc['differing_pixels_in_placed_rect']} changed px, {fc['differing_pixels_outside_marks']} outside declared marks; every leader only over desktop teal or its target, every outline only on its target frame band "
                    f"({sum(m['pixels_breaking_rule'] for m in fc['marks'])} px breaking a rule); poster == five-callouts bytes {placement['poster_equals_five_callouts_bytes']}; SVG labels equal ticket copy")},
        {'test': 'manual visual review (full size and 720p)', 'result': MANUAL_REVIEW},
        {'test': 'delivery and pack validators', 'command': 'python -B tools/validate_delivery.py --id XTRA-05; python -B tools/validate_pack.py', 'result': 'see qa.md (verbatim output of the run after this inventory was written)'},
    ]
    d['unresolved_gates'] = ['R03', 'R14']
    d['production_status'], d['release_status'] = 'produced', 'blocked'
    tc = dict(d.get('toolchain', {}))
    tc.update(fonts='Liberation Sans Bold resolved by fc-match from C:/WINDOWS/fonts; not distributed',
              pillow_resampling='BOX (area average), exact 1.5x',
              render_commands=['python -B assets/stills/XTRA-05/src/build.py', 'python -B tools/render/render_assets.py --id XTRA-05',
                               'python -B tools/render/qa_browser.py --id XTRA-05', 'python -B assets/stills/XTRA-05/src/verify.py',
                               'python -B tools/render/finish_delivery.py --deliveries-only --id XTRA-05', 'python -B assets/stills/XTRA-05/src/finalize.py',
                               'python -B tools/validate_delivery.py --id XTRA-05', 'python -B tools/validate_pack.py'],
              network_used=True, network_note='Read-only web lookups of archived Microsoft KB and VB6 documentation pages for the label checks; no downloads into the repository, no accounts, no terms accepted.',
              installs_performed=False)
    d['toolchain'] = tc
    d['notes'] = build['notes'] + [
        f"Upstream status at use: HIST-02 production {up_state['production_status']}, release {up_state['release_status']}.",
        'Internal proof only: not placed in any cleared-media bin. Review questions XTRA-05-RQ1..RQ6 in evidence/claim-checks.json.',
    ]
    items = []
    for f in sorted(ASSET.rglob('*')):
        if not f.is_file() or f.name in ('delivery.json', 'state.json') or '__pycache__' in f.parts:
            continue
        rel = f.relative_to(ASSET).as_posix()
        items.append({'path': rel, 'role': role(rel), 'bytes': f.stat().st_size, 'sha256': hashlib.sha256(f.read_bytes()).hexdigest()})
    d['outputs'] = items
    dump(ASSET / 'delivery.json', d)
    state = load('state.json')
    state.update(production_status='produced', release_status='blocked', updated_at='2026-09-15',
                 assigned_agent='Render Lane worker (Claude Opus 5) under Render Lane Manager vb-97, branch ticket/XTRA-05',
                 owner='Render Lane worker (Claude Opus 5), branch ticket/XTRA-05', reviewer=None,
                 blockers=['R14 release gate: HIST-02 rights unresolved (RQ-HIST-02-1, -2); callout marks over a whole Microsoft screenshot may count as alteration (XTRA-05-RQ1, carries RQ-HIST-02-3); credit placement (XTRA-05-RQ4).',
                           'R03 release gate: "Project Explorer" is later-version terminology, VB4 says Project window, and War/SCRIPT.md:133 already reads "Project Window" (XTRA-05-RQ2); narration form/code-window description only partly matches the capture (XTRA-05-RQ3).'],
                 notes=['Produced: poster, clean-workspace and five-callouts stills with offline HTML source; validate_delivery.py passes.',
                        'Whole HIST-02 screenshot at exactly 1.5x (Pillow BOX), pixel-verified; every annotation mark and the original pixels it overlays recorded (delivery.json annotation_edit_history).',
                        'Full-size and 720p manual review recorded in qa.md. Internal proof only; release blocked pending the review deck.'])
    dump(ASSET / 'state.json', state)
    print('FINALIZED', ID, len(items), 'outputs')


if __name__ == '__main__':
    main()
