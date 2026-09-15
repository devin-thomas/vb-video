#!/usr/bin/env python3
"""HIST-06: re-run the machine checks, inventory every output, and write delivery.json and state.json."""
import base64
import datetime
import hashlib
import json
import platform
import struct
import sys
from pathlib import Path

import PIL

BASE = Path(__file__).resolve().parents[1]
SKIP = {'delivery.json', 'state.json'}

ROLES = {
    'source/original.png': 'historical original (acquired unmodified from Wikimedia Commons)',
    'exports/editorial-frame.png': 'editorial framing still (derived, reversible)',
    'proofs/editorial-frame-720.png': '720p review proof',
    'src/frame.py': 'framing script',
    'src/bundle.py': 'inventory and state script',
    'qa.md': 'evidence / QA',
}


def role(rel: str) -> str:
    if rel in ROLES:
        return ROLES[rel]
    if rel.startswith('evidence/source-page/'):
        return 'preserved source page / archive record'
    return 'evidence / QA'


def png_size(path: Path):
    head = path.read_bytes()[:24]
    return list(struct.unpack('>II', head[16:24]))


def fail(msg: str) -> int:
    print(f'BUNDLE FAILED: {msg}', file=sys.stderr)
    return 1


def main() -> int:
    original = BASE / 'source/original.png'
    data = original.read_bytes()
    sha1 = hashlib.sha1(data).hexdigest()

    info = json.loads((BASE / 'evidence/source-page/commons-imageinfo.json').read_text(encoding='utf-8'))
    api_sha1 = next(iter(info['query']['pages'].values()))['imageinfo'][0]['sha1']
    if sha1 != api_sha1:
        return fail('original SHA-1 does not match the Commons API record')

    b32 = base64.b32encode(hashlib.sha1(data).digest()).decode()
    cdx = json.loads((BASE / 'evidence/source-page/wayback-cdx-image.json').read_text(encoding='utf-8'))[1:]
    digests = {row[5] for row in cdx if row[4] == '200'}
    if b32 not in digests:
        return fail('original does not match any Wayback 200 capture digest')
    first_capture = min(row[1] for row in cdx)

    framing = json.loads((BASE / 'evidence/framing.json').read_text(encoding='utf-8'))
    if framing['exports'][0]['from_sha256'] != hashlib.sha256(data).hexdigest():
        return fail('framing.json was produced from a different original')

    dims = {
        'source/original.png': png_size(original),
        'exports/editorial-frame.png': png_size(BASE / 'exports/editorial-frame.png'),
        'proofs/editorial-frame-720.png': png_size(BASE / 'proofs/editorial-frame-720.png'),
    }
    if dims != {'source/original.png': [560, 384], 'exports/editorial-frame.png': [1920, 1080], 'proofs/editorial-frame-720.png': [1280, 720]}:
        return fail(f'unexpected PNG dimensions {dims}')

    outputs = []
    for path in sorted(p for p in BASE.rglob('*') if p.is_file()):
        rel = path.relative_to(BASE).as_posix()
        if rel in SKIP or '__pycache__' in rel:
            continue
        blob = path.read_bytes()
        outputs.append({'path': rel, 'role': role(rel), 'bytes': len(blob), 'sha256': hashlib.sha256(blob).hexdigest()})

    production, release = 'produced', 'blocked'
    delivery = {
        'id': 'HIST-06',
        'title': 'Apple II BASIC boot screen',
        'production_status': production,
        'release_status': release,
        'provenance_type': 'historical source',
        'shared_version': 'win95-workbench-1.0.0',
        'duration_seconds': None,
        'dimensions': {'width': 1920, 'height': 1080},
        'fps': None,
        'outputs': outputs,
        'variants': [
            {'name': 'original', 'files': ['source/original.png'],
             'notes': 'Commons File:Applesoft BASIC.png, byte-identical, 560x384.'},
            {'name': 'editorial-frame', 'files': ['exports/editorial-frame.png'], 'derived_from': 'source/original.png',
             'notes': 'Exact 2x nearest-neighbour enlargement centred on 1920x1080 #111318; no crop; reversible (evidence/framing.json). Still; holds for editorial timing.'},
        ],
        'sources': [
            {'path': '../../../sources/ASSET_PLAN.md', 'lines': [91, 91],
             'sha256': '8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7', 'relationship': 'source creative brief'},
            {'path': '../../../sources/SCRIPT.md', 'lines': [73, 75],
             'sha256': '3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb', 'relationship': 'narration and visual brief'},
            {'path': 'source/original.png', 'sha256': hashlib.sha256(data).hexdigest(), 'relationship': 'historical original',
             'url': 'https://commons.wikimedia.org/wiki/File:Applesoft_BASIC.png', 'record': 'evidence/source.json'},
            {'path': 'exports/editorial-frame.png', 'relationship': 'derivative crop (framing only; no pixels removed)', 'record': 'evidence/framing.json'},
        ],
        'credits': [
            {'type': 'historical source (public-domain label, rights review open)',
             'credit': '"Applesoft BASIC" screenshot by Wikimedia Commons user Vadimr, released into the public domain (PD-self). https://commons.wikimedia.org/wiki/File:Applesoft_BASIC.png',
             'license': 'PD-self (Commons); Free screenshot template with empty license parameter',
             'license_url': 'https://commons.wikimedia.org/wiki/Template:PD-self',
             'access_date': '2026-09-15',
             'rights_status': 'unresolved'},
        ],
        'tests': [
            {'test': 'acquisition integrity (local SHA-1 vs Commons API)', 'result': 'passed', 'sha1': sha1},
            {'test': 'archive corroboration (base-32 SHA-1 vs Wayback CDX digest)', 'result': 'passed', 'digest': b32,
             'captures_with_status_200': sum(1 for row in cdx if row[4] == '200'), 'first_capture': first_capture},
            {'test': 'framing reversibility (src/frame.py block-by-block comparison)', 'result': 'passed',
             'detail': framing['exports'][0]['reversibility_check']},
            {'test': 'PNG dimensions', 'result': 'passed', 'sizes': dims, 'placed_rect': [400, 156, 1520, 924], 'safe_area': [120, 72, 1800, 1008]},
            {'test': 'claim checks against primary documents', 'result': 'recorded',
             'detail': 'evidence/claim-checks.json: prompt verified; boot screen not supported; model not established; script sentence qualified.'},
            {'test': 'privacy scan of text outputs', 'result': 'passed', 'hits': [],
             'detail': 'Searched for the local account name, home path, e-mail, and client IP (values not written here). HTTP response headers were not saved.'},
            {'test': 'manual visual inspection', 'result': 'passed',
             'full_size': 'Viewed source/original.png (560x384) and exports/editorial-frame.png (1920x1080): eleven screen lines legible, square pixels, no stretch/blur/clip, no watermark, UI, or private data.',
             'proof_720': 'Viewed proofs/editorial-frame-720.png (1280x720): every line, including CHR$ (7), readable.'},
        ],
        'unresolved_gates': ['R14'],
        'toolchain': {
            'os': platform.platform(),
            'python': platform.python_version(),
            'packages': {'Pillow': PIL.__version__},
            'acquisition': 'curl 8.21.0 (Windows, Schannel), anonymous HTTPS GET',
            'renderer': 'none (Pillow paste of the original; no fonts drawn)',
            'network_used': 'Wikimedia Commons API/file download, Internet Archive metadata/text and Wayback CDX; read-only',
            'installs_performed': False,
            'font_files_distributed': False,
        },
        'notes': [
            'Not a boot screen: shows the Applesoft ] prompt after a typed Hello World was run and listed. Label only as an Applesoft BASIC prompt on an Apple II-family text screen (model and emulator unknown).',
            'Title kept from the ticket for traceability; the ticket title is not a claim this asset supports.',
            'Release blocked on R14 rights review; see qa.md for review questions and the optional boundary need.',
        ],
    }
    (BASE / 'delivery.json').write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

    state = {
        'id': 'HIST-06',
        'production_status': production,
        'release_status': release,
        'assigned_agent': 'Claude Code (Opus 5), worker for Historical Screenshots Manager vb-7a',
        'updated_at': datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
        'blockers': [
            'R14: Commons PD-self label recorded but not cleared (empty Author field; screenshot threshold-of-originality question).',
        ],
        'reviewer': None,
        'notes': [
            'Historical proof delivered: Commons Applesoft BASIC screenshot plus reversible editorial frame; see delivery.json and qa.md.',
            'Image shows the Applesoft ] prompt, not a power-on boot screen; model/ROM/emulator not established.',
            'Review questions: R14 rights; whether the montage accepts a non-boot prompt screen; optional Writing Lead wording on Apple II vs Apple II Plus.',
        ],
    }
    (BASE / 'state.json').write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    print(f'bundled {len(outputs)} outputs; production={production} release={release}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
