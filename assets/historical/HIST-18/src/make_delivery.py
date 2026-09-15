"""Generate assets/historical/HIST-18/delivery.json: hashed inventory of every delivered file plus metadata.
Run from the repository root after capture.py and frame.py:  python assets/historical/HIST-18/src/make_delivery.py
"""
import hashlib
import json
from pathlib import Path

A = Path(__file__).resolve().parents[1]
EXCLUDE = {'delivery.json', 'state.json'}


def role(rel):
    if rel == 'source/original.html': return 'native original (archived HTML, byte-exact)'
    if rel.startswith('source/embeds/'): return 'native original (archived embedded image, byte-exact)'
    if rel.startswith('source/raw/'): return 'uncropped raw capture (offline render of archived bytes)'
    if rel == 'exports/editorial-frame.png': return 'variant editorial-frame (1920x1080 reversible crop)'
    if rel == 'exports/original.png': return 'variant original (1920x1080 uncropped framing)'
    if rel.startswith('evidence/proofs/'): return '720p inspection proof'
    if rel.startswith('evidence/'): return 'evidence'
    if rel.startswith('src/'): return 'reproduction script'
    if rel == 'qa.md': return 'qa report'
    return 'other'


outputs = []
for p in sorted(A.rglob('*')):
    if not p.is_file() or '__pycache__' in p.parts:
        continue
    rel = p.relative_to(A).as_posix()
    if rel in EXCLUDE:
        continue
    data = p.read_bytes()
    outputs.append({'path': rel, 'role': role(rel), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})

state = json.loads((A / 'state.json').read_text(encoding='utf-8'))
delivery = {
    'id': 'HIST-18',
    'title': 'Download.com archived site circa 1996',
    'production_status': state['production_status'],
    'release_status': state['release_status'],
    'provenance_type': 'historical original (Wayback Machine capture 19961221110042 of http://www.download.com/) with offline real capture and derivative crop',
    'shared_version': 'win95-workbench-1.0.0 (canvas/timing contract only; no shared renderer primitives used)',
    'duration_seconds': None,
    'dimensions': {'width': 1920, 'height': 1080},
    'fps': None,
    'outputs': outputs,
    'variants': [
        {'name': 'original', 'paths': ['source/original.html', 'source/raw/capture-800w-2x.png', 'source/raw/capture-800w-1x.png', 'exports/original.png'],
         'timeline': None, 'note': 'Still; holds for editorial timing. exports/original.png is the uncropped page framed at 1920x1080.'},
        {'name': 'editorial-frame', 'paths': ['exports/editorial-frame.png'], 'timeline': None,
         'note': 'Still; holds for editorial timing. Crop CSS [0,0,800,706] of source/raw/capture-800w-2x.png (evidence/transforms.json).'}
    ],
    'sources': [
        {'path': '../../../sources/SCRIPT.md', 'lines': [595, 597], 'sha256': '3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb', 'relationship': 'visual cue served (not excerpted into media)'},
        {'path': '../../../sources/ASSET_PLAN.md', 'lines': [100, 100], 'sha256': '8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7', 'relationship': 'plan lead'},
        {'path': 'source/original.html', 'url': 'http://web.archive.org/web/19961221110042id_/http://www.download.com:80/', 'relationship': 'historical original', 'record': 'evidence/source.json'},
        {'path': 'source/embeds/', 'relationship': 'historical original', 'record': 'evidence/embeds.json'},
        {'path': 'source/raw/capture-800w-2x.png', 'relationship': 'real capture', 'record': 'evidence/capture-log.json'},
        {'path': 'exports/editorial-frame.png', 'relationship': 'derivative crop', 'record': 'evidence/transforms.json'}
    ],
    'credits': [
        {'text': 'download.com home page, © 1996 CNET Inc. Archived by the Internet Archive Wayback Machine, 21 December 1996.',
         'rights_status': 'unresolved', 'license': None, 'record': 'evidence/rights.json'}
    ],
    'tests': [
        {'name': 'offline render integrity', 'command': 'python assets/historical/HIST-18/src/capture.py --replay', 'result': '28 images, 0 broken, 0 aborted requests at scale 1 and 2; Wayback replay 0 HTTP errors', 'log': 'evidence/capture-log.json'},
        {'name': 'export PNG size', 'command': 'Pillow Image.open size check', 'result': 'both exports 1920x1080 RGB'},
        {'name': 'manual inspection full size', 'result': 'both exports viewed as 1:1 tiles; pass (see qa.md)'},
        {'name': 'manual inspection 720p', 'result': 'evidence/proofs/*-720p.png viewed; pass, uncropped footer text small (see qa.md)'},
        {'name': 'delivery validator', 'command': 'python tools/validate_delivery.py --id HIST-18', 'result': 'run after generation; output in state.json notes'}
    ],
    'unresolved_gates': ['R14'],
    'toolchain': {'python': '3.14.0', 'playwright': '1.63.0', 'chromium': '153.0.8010.12', 'pillow': '12.3.0',
                  'font': 'Segoe UI (system, C:/Windows/Fonts/segoeui.ttf, not bundled)', 'os': 'Windows 11 Pro 10.0.26200'},
    'notes': [
        'Capture is a modern Chromium render of archived 1996 bytes, not a period Netscape screenshot.',
        'Release blocked: no license; rights review question in evidence/rights.json.',
        'Caption line, background and crop are authored additions (evidence/provenance.json).'
    ]
}
(A / 'delivery.json').write_text(json.dumps(delivery, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
print(f'{len(outputs)} outputs inventoried')
