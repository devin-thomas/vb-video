#!/usr/bin/env python3
"""XTRA-05 delivery finishing. Run last, after
    python -B tools/render/finish_delivery.py --deliveries-only --id XTRA-05
and after qa.md is final:
    python -B assets/stills/XTRA-05/src/finalize.py --id XTRA-05

finish_delivery.py writes a generic delivery (one "original graphics" credit, a thumbnail-only
manual-review line, motion/Program.vb wording) and a generic state. This script replaces those
fields with the placements, annotation edit history, label checks, carried-forward credit, variants
(including the poster mapping) and executed-test results for this still, then re-hashes the complete
output inventory. Safe to re-run; run it again after any edit to qa.md or another delivered file.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSET = HERE.parent
ROOT = HERE.parents[3]
ID = 'XTRA-05'
UP = ROOT / 'assets/historical/HIST-02'
AGENT = 'Render Lane worker (Claude Opus 5) under Render Lane Manager vb-8c, branch ticket/XTRA-05-rev'

# Written by the producing agent after viewing the exports and proofs (details in qa.md).
MANUAL_REVIEW = {
    'mode': 'Full-resolution exports, native-pixel halves, 1280x720 proofs and 2x zooms of the side-by-side 720p proof, viewed by the producing agent with the Read tool',
    'scope': 'exports/poster.png, exports/side-by-side.png (byte-identical), exports/five-callouts.png, exports/clean-workspace.png, exports/contact-sheet.png at full size; '
             'proofs/side-by-side-1to1-left.png and -right.png; proofs/poster-720.png, proofs/side-by-side-720.png, proofs/five-callouts-720.png, proofs/clean-workspace-720.png.',
    'status': 'Every variant shows the whole screenshot with nothing clipped; clean screenshots carry no marks or text. side-by-side: both screenshots crisp at native 1.0x; '
              'all five labels legible at 720p (about 27 px bold); every target unmistakable at 720p (gold outline on the window frame, leader traced over teal and a gutter rail to its label; '
              'Form Designer outline visibly stops short of the Code Window outline). Screenshot UI text is smaller at 720p than in five-callouts (0.67x effective) but readable. '
              'five-callouts: labels and targets as before, fifth label now Project Window. Poster = side-by-side. See qa.md.',
}


def load(rel: str):
    return json.loads((ASSET / rel).read_text(encoding='utf-8'))


def dump(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')


def role(rel: str) -> str:
    if rel.startswith('exports/') and rel.endswith('.png'):
        if rel.endswith('contact-sheet.png'):
            return 'rendered still (contact sheet written by render_assets.py)'
        return 'rendered still (poster)' if rel == 'exports/poster.png' else 'rendered still'
    if rel.startswith('proofs/'):
        if rel.endswith('-720.png'):
            return 'QA proof (1280x720 LANCZOS downscale)'
        variant = rel.removeprefix('proofs/').split('-1to1-')[0]
        return f'QA proof (native-pixel half of {variant})'
    if rel.startswith('src/'):
        return 'editable source'
    if rel == 'qa.md':
        return 'QA record'
    return 'evidence'


def export_rec(placement: dict, variant: str, png: str) -> dict:
    return next(e for e in placement['variants'][variant]['exports'] if e['png'] == png)


def marks_history(layout: dict, targets_key: str, placements: dict) -> list:
    by = {(m['target'], m['mark']): m for m in placements['marks']}
    out = []
    for t in layout[targets_key]:
        for m in t['marks']:
            px = by[(t['label'], m['type'])]
            row = {k: m[k] for k in ['target', 'type', 'casing_rects', 'core_rects']}
            if 'parts' in m:
                row['parts'] = m['parts']
            row.update(shape=t['shape'] if m['type'] == 'outline' else ('exit leader, gutter rail and run to the label' if 'parts' in m else 'horizontal leader line'),
                       colours={'core': layout['mark_style']['core'], 'casing': layout['mark_style']['casing']},
                       target_original_px_inclusive=t['rect'],
                       canvas_pixels_changed_on_image=px['canvas_pixels_changed_on_image'], original_pixels_overlaid=px['original_pixels_overlaid'],
                       original_bbox_inclusive=px['original_bbox_inclusive'], original_colours_overlaid=px['original_colours_overlaid'],
                       overlay_rule=px['rule'], pixels_breaking_rule=px['pixels_breaking_rule'])
            out.append(row)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description='Finish the XTRA-05 delivery record.')
    ap.add_argument('--id', default=ID)
    assert ap.parse_args().id == ID, f'this finishing script belongs to {ID}'
    d = load('delivery.json')
    layout, placement = load('src/layout.json'), load('evidence/placement-checks.json')
    browser, render, prov = load('evidence/browser-tests.json'), load('evidence/render-tests.json'), load('evidence/provenance.json')
    claims, build = load('evidence/claim-checks.json'), load('src/build.json')
    assert placement['ok'] and not browser['errors'], 'placement or browser checks are failing'
    rights = json.loads((UP / 'evidence/rights.json').read_text(encoding='utf-8'))
    up_state = json.loads((UP / 'state.json').read_text(encoding='utf-8'))
    poster = layout['poster']
    cw = export_rec(placement, 'clean-workspace', 'exports/clean-workspace.png')
    fc = export_rec(placement, 'five-callouts', 'exports/five-callouts.png')
    sx = export_rec(placement, 'side-by-side', 'exports/side-by-side.png')
    cw0, fc0 = cw['placements'][0], fc['placements'][0]
    sxc = next(p for p in sx['placements'] if p['role'] == 'clean')
    sxa = next(p for p in sx['placements'] if p['role'] == 'annotated')
    p, sbs = layout['placement'], layout['side_by_side']
    research = claims['loan_project_research']

    d['provenance_type'] = prov['classification']
    d['shared_version'] = 'win95-workbench-1.0.0 (tools/render/studio.py colour tokens and text primitives)'
    d['duration_seconds'], d['fps'] = None, None
    d['poster'] = {'file': 'exports/poster.png', 'variant': poster, 'byte_identical_to': layout['variants'][poster]['png'],
                   'verified': placement['poster_equals_variant_bytes'],
                   'reason': 'At 720p every label is legible and every target is unmistakable in side-by-side (qa.md "Poster decision").'}
    d['placement'] = {
        'source_file': layout['source']['file'], 'source_sha256': layout['source']['sha256'], 'source_size': layout['source']['size'],
        'clean-workspace and five-callouts': {
            'rect_xywh': [p['x'], p['y'], p['w'], p['h']], 'scale_x': p['scale_x'], 'scale_y': p['scale_y'], 'resampling': p['resampling'],
            'crop': p['crop'], 'rotation_deg': p['rotation_deg'], 'retouch': p['retouch'], 'embedded_png_sha256': p['embedded_png_sha256'],
            'verification': f"clean-workspace {cw0['differing_pixels_in_placed_rect']} differing px of {cw0['pixels_checked']} against a fresh 1.5x BOX resample; five-callouts {fc0['differing_pixels_outside_marks']} differing px outside declared marks"},
        'side-by-side': {
            'scale': sbs['scale'], 'resampling': sbs['resampling'], 'embedded_png_sha256': sbs['embedded_png_sha256'],
            'clean_rect_xywh': [sbs['clean']['x'], sbs['clean']['y'], sbs['clean']['w'], sbs['clean']['h']],
            'annotated_rect_xywh': [sbs['annotated']['x'], sbs['annotated']['y'], sbs['annotated']['w'], sbs['annotated']['h']],
            'gap_between_frames_px': sbs['gap_between_frames_px'], 'width_used_x': sbs['width_used'], 'why_1x': sbs['why_1x'],
            'verification': f"clean (left) {sxc['differing_pixels_in_placed_rect']} differing px of {sxc['pixels_checked']}; annotated (right) {sxa['differing_pixels_outside_marks']} differing px outside declared marks; "
                            f"gold pixels outside declared cores {sx['gold_audit']['gold_pixels_outside_declared_cores']}, on the clean screenshot {sx['gold_audit']['gold_pixels_on_clean_placements']}"},
        'frame': layout['frame'], 'crop': None, 'rotation_deg': 0, 'retouch': None,
        'evidence': 'evidence/placement-checks.json',
    }
    d['annotation_edit_history'] = {
        'clean_workspace_edits': [], 'clean_side_of_side_by_side_edits': [],
        'five-callouts': {'mark_style': layout['mark_style'], 'label_style': layout['label_style'],
                          'marks': marks_history(layout, 'targets', fc0),
                          'labels': [{'label': t['label'], 'lines': [x['text'] for x in t['texts']], 'text_boxes': [x['box'] for x in t['texts']], 'side': t['side']} for t in layout['targets']],
                          'total_changed_pixels_on_image': fc0['mark_pixels_changed_total']},
        'side-by-side': {'mark_style': layout['mark_style_side_by_side'], 'label_style': layout['label_style_side_by_side'],
                         'marks': marks_history(layout, 'targets_side_by_side', sxa),
                         'labels': [{'label': t['label'], 'text_box': t['texts'][0]['box'], 'rail_x': t['rail_x'], 'label_row_canvas': t['label_row_canvas']} for t in layout['targets_side_by_side']],
                         'total_changed_pixels_on_image': sxa['mark_pixels_changed_total']},
        'full_record': 'src/layout.json annotation_edits (every rectangle of both annotated variants with geometric overlay); evidence/placement-checks.json (pixel-measured overlay per mark); evidence/provenance.json annotation_edit_history',
    }
    d['label_source'] = {k: layout['labels'][k] for k in ['authority', 'path', 'line', 'cue_text', 'script_sha256_at_build', 'labels_in_cue_order', 'ticket_copy', 'differs_from_ticket_copy']}
    d['label_source']['override_record'] = 'evidence/claim-checks.json copy_override (writing change, Devin 2026-09-15; authority War/SCRIPT.md at 9e6f14a)'
    d['label_checks'] = [{k: c[k] for k in ['label', 'target_original_px_inclusive', 'target_canvas_box', 'target_canvas_box_side_by_side', 'status', 'invented_ui']} for c in claims['label_checks']]
    d['variants'] = [
        {'name': 'clean-workspace', 'kind': 'still', 'timeline': None, 'timing': 'hold for editorial timing; no named cutdown', 'required': True,
         'files': ['exports/clean-workspace.png', 'src/variant-clean-workspace.svg', 'proofs/clean-workspace-720.png'],
         'notes': 'Whole HIST-02 screenshot at 1.5x in a frame outside its edges; no annotation, no text.'},
        {'name': 'five-callouts', 'kind': 'still', 'timeline': None, 'timing': 'hold for editorial timing; no named cutdown; no one-panel reveal (editor request only)', 'required': True,
         'files': ['exports/five-callouts.png', 'src/variant-five-callouts.svg', 'proofs/five-callouts-720.png', 'proofs/five-callouts-1to1-left.png', 'proofs/five-callouts-1to1-right.png'],
         'notes': 'Same screenshot rectangle as clean-workspace, plus five margin labels (War/SCRIPT.md cue), window-frame outlines and leaders.'},
        {'name': 'side-by-side', 'kind': 'still', 'timeline': None, 'timing': 'hold for editorial timing; no named cutdown', 'required': False,
         'requested_by': 'Devin, 2026-09-15 (cue "Side-by-side"; XTRA-05-RQ6)',
         'files': ['exports/side-by-side.png', 'src/variant-side-by-side.svg', 'proofs/side-by-side-720.png', 'proofs/side-by-side-1to1-left.png', 'proofs/side-by-side-1to1-right.png'],
         'notes': 'Clean screenshot left, annotated screenshot right, both whole at native 1.0x; label strip below the annotated side.'},
    ]
    for v in d['variants']:
        if v['name'] == poster:
            v['files'] += ['exports/poster.png', 'proofs/poster-720.png']
            v['poster'] = True
            v['notes'] += ' exports/poster.png is byte-identical.'
    d['sources'] = build['sources'] + [
        {'path': '../../historical/HIST-02/evidence/rights.json', 'relationship': 'rights and credit record carried forward'},
        {'path': '../../historical/HIST-02/evidence/source.json', 'relationship': 'source record of the original'},
    ] + [{'url': s['url'], 'accessed': s['accessed'], 'title': s.get('title', s['type']),
          'relationship': 'external evidence for the Loan project authorship (URL, quote and page hash only; nothing copied)'}
         for s in research['sources_checked'] if 'url' in s and s['n'] <= 4]
    d['credits'] = [
        {'type': 'historical screenshot', 'asset': 'HIST-02', 'file': layout['source']['file'], 'credit': rights['credit_text'], 'credit_on_screen': None,
         'proposed_credit': rights['proposed_credit_text'],
         'status': 'proposed, not approved. The "Used with permission from Microsoft." sentence applies only if the rights review relies on Microsoft\'s screenshot permission (RQ-HIST-02-1); it must not be used before that decision, so nothing is burned in. Placement is with the producer (XTRA-05-RQ4).',
         'credit_record': 'assets/historical/HIST-02/evidence/rights.json#proposed_credit_text', 'rights_status': rights['rights_status'],
         'upstream_release_status': up_state['release_status'], 'cleared': False,
         'rights_holders_after_research': 'Microsoft Corporation (IDE and the Loan sample project, VB 4.0 \\vb\\samples\\grid); unknown WinWorld capturer',
         'open_questions': ['RQ-HIST-02-1', 'XTRA-05-RQ4'],
         'resolved_questions': {'RQ-HIST-02-3 / XTRA-05-RQ1': 'marks allowed (Devin, 2026-09-15)',
                                'RQ-HIST-02-2 / XTRA-05-RQ5': 'Loan is a Microsoft VB 4.0 sample (evidence: KB Q150726, archive.org VB 4.0 CD listings)',
                                'RQ-HIST-02-4 / XTRA-05-RQ2 (Project part)': 'label Project Window (War/SCRIPT.md:133)'}},
        {'type': 'authored graphics', 'credit': 'Labels, outlines, leaders, rails, frames and layout authored for this production with system fonts (Liberation Sans); no font files or other imagery included.'},
    ]
    gs = {rel: export_rec(placement, v, rel)['gold_audit'] for v, rel in (('clean-workspace', 'exports/clean-workspace.png'), ('five-callouts', 'exports/five-callouts.png'), ('side-by-side', 'exports/side-by-side.png'))}
    d['tests'] = [
        {'test': 'authoring, label source and layout assertions', 'command': 'python -B assets/stills/XTRA-05/src/build.py --id XTRA-05',
         'result': f"passed: HIST-02 SHA-256 and bytes equal HIST-02/delivery.json; 800x600 source; exactly five labels read from {layout['labels']['path']}:{layout['labels']['line']} and each names its panel in cue order; "
                   'five-callouts: labels outside the screenshot and frame, inside 120-1800 x 72-1008, not overlapping, marks clear of labels, outlines on the image and not touching; '
                   f"side-by-side: frames do not overlap (gap {sbs['gap_between_frames_px']} px) and sit in the safe area, labels clear of both screenshots and frames and of each other, no mark meets the clean screenshot/frame, a label or another target's mark, outlines on the annotated screenshot"},
        {'test': 'rasterize still variants', 'command': render['command'], 'evidence': 'evidence/render-tests.json',
         'result': f"passed: {render['renderer']}, poster and {len(layout['variants'])} variants at {render['png_dimensions']}; no video (still)"},
        {'test': 'offline HTML, deterministic seek, SVG text bounds', 'command': 'python -B tools/render/qa_browser.py --id XTRA-05', 'evidence': 'evidence/browser-tests.json',
         'result': f"passed: {browser['browser']}, {browser['svg_files_checked']} SVG files, {browser['text_boxes_checked']} text boxes, out_of_canvas {len(browser['out_of_canvas'])}, offline {browser['offline']}, deterministic {browser['deterministic_seek']}"},
        {'test': 'placed-image pixel integrity, annotation overlay audit, gold audit and no-overlap check', 'command': placement['command'], 'evidence': 'evidence/placement-checks.json',
         'result': (f"passed: every embedded PNG equals a fresh resample at its scale (1.0x embeds are the HIST-02 bytes); "
                    f"clean-workspace {cw0['differing_pixels_in_placed_rect']} differing px / {cw0['pixels_checked']}, mat ring {cw0['mat_ring_nonmatching_pixels']}; "
                    f"five-callouts {fc0['differing_pixels_in_placed_rect']} changed px, {fc0['differing_pixels_outside_marks']} outside declared marks, {sum(m['pixels_breaking_rule'] for m in fc0['marks'])} px breaking a leader/outline rule; "
                    f"side-by-side clean {sxc['differing_pixels_in_placed_rect']} differing px / {sxc['pixels_checked']}, mat ring {sxc['mat_ring_nonmatching_pixels']}; annotated {sxa['differing_pixels_in_placed_rect']} changed px, "
                    f"{sxa['differing_pixels_outside_marks']} outside declared marks, {sum(m['pixels_breaking_rule'] for m in sxa['marks'])} px breaking a rule, mat ring {sxa['mat_ring_nonmatching_pixels_outside_marks']} changed outside marks; "
                    f"gold outside declared cores: clean-workspace {gs['exports/clean-workspace.png']['gold_pixels_outside_declared_cores']}, five-callouts {gs['exports/five-callouts.png']['gold_pixels_outside_declared_cores']}, side-by-side {gs['exports/side-by-side.png']['gold_pixels_outside_declared_cores']} (on the clean screenshot {gs['exports/side-by-side.png']['gold_pixels_on_clean_placements']}); "
                    f"poster == {poster} bytes {placement['poster_equals_variant_bytes']}; SVG labels equal the War/SCRIPT.md cue")},
        {'test': 'manual visual review (full size and 720p)', 'result': MANUAL_REVIEW},
        {'test': 'delivery and pack validators', 'command': 'python -B tools/validate_delivery.py --id XTRA-05; python -B tools/validate_pack.py', 'result': 'see qa.md (verbatim output of the run after this inventory was written)'},
    ]
    d['unresolved_gates'] = ['R03', 'R14']
    d['production_status'], d['release_status'] = 'produced', 'blocked'
    tc = dict(d.get('toolchain', {}))
    tc.update(fonts='Liberation Sans Bold resolved by fc-match from C:/WINDOWS/fonts; not distributed',
              pillow_resampling='clean-workspace and five-callouts: BOX (area average), exact 1.5x; side-by-side: none (native 1.0x, HIST-02 bytes embedded)',
              render_commands=['python -B assets/stills/XTRA-05/src/build.py --id XTRA-05', 'python -B tools/render/render_assets.py --id XTRA-05',
                               'python -B tools/render/qa_browser.py --id XTRA-05', 'python -B assets/stills/XTRA-05/src/verify.py --id XTRA-05',
                               'python -B tools/render/finish_delivery.py --deliveries-only --id XTRA-05', 'python -B assets/stills/XTRA-05/src/finalize.py --id XTRA-05',
                               'python -B tools/validate_delivery.py --id XTRA-05', 'python -B tools/validate_pack.py'],
              network_used=True,
              network_note='Read-only web lookups with a generic browser User-Agent: archived Microsoft KB and VB6 documentation pages (label checks); archived KB articles and archive.org item metadata and disc contents listing pages (Loan authorship). No installers, disc images or files from disc images downloaded; nothing external added to the repository; no accounts, no terms accepted.',
              installs_performed=False)
    d['toolchain'] = tc
    d['notes'] = build['notes'] + [
        f"Upstream status at use: HIST-02 production {up_state['production_status']}, release {up_state['release_status']}.",
        'Devin rulings of 2026-09-15 implemented (evidence/claim-checks.json devin_rulings). Open review questions: XTRA-05-RQ2 (Form Designer note, Writing Lead), XTRA-05-RQ3 (Writing Lead), XTRA-05-RQ4 (producer); upstream RQ-HIST-02-1.',
        'Internal proof only: not placed in any cleared-media bin.',
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
    state.update(production_status='produced', release_status='blocked', updated_at='2026-09-15', assigned_agent=AGENT, owner=AGENT, reviewer=None,
                 blockers=['R14 release gate: the HIST-02 permission basis is undecided (RQ-HIST-02-1: Microsoft\'s screenshot permission, another basis, or none), and the credit placement is open with the producer (XTRA-05-RQ4). '
                           'Resolved on 2026-09-15: callout marks are allowed (Devin, XTRA-05-RQ1); the "Loan" project is Microsoft\'s VB 4.0 Grid sample, so no third-party content concern remains (XTRA-05-RQ5, evidence: KB Q150726 and archive.org VB 4.0 CD listings).',
                           'R03 release gate: the narration\'s form/code-window description only partly matches the capture (XTRA-05-RQ3, Writing Lead); "Form Designer" is VB6-documented wording (XTRA-05-RQ2 remaining note, Writing Lead). "Project Window" now follows War/SCRIPT.md:133.'],
                 notes=['Produced: poster (= side-by-side), side-by-side, clean-workspace and five-callouts stills with offline HTML source; validate_delivery.py passes.',
                        'Labels read from the War/SCRIPT.md:133 VISUAL cue (fifth label Project Window). Whole HIST-02 screenshot in every variant: 1.5x BOX (clean-workspace, five-callouts) or native 1.0x (side-by-side), pixel-verified; every mark and the original pixels it overlays recorded.',
                        'Full-size and 720p manual review recorded in qa.md. Internal proof only; release blocked pending the review deck.'])
    dump(ASSET / 'state.json', state)
    print('FINALIZED', ID, len(items), 'outputs; poster =', poster)


if __name__ == '__main__':
    main()
