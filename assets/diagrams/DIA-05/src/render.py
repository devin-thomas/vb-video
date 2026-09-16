#!/usr/bin/env python3
"""DIA-05 render driver. Run from the repository root:  python assets/diagrams/DIA-05/src/render.py

1. tools/render/render_assets.py (imported, unchanged) renders the continuous preview.mp4, poster.png, the seven
   variant stills, keyframes, proofs/poster-720.png, contact-sheet.png and evidence/render-tests.json from build.json.
2. Each entry of build.json "cutdowns" is then encoded as an independent MP4 with the same encode() (identical ffmpeg
   settings: 30 fps, libx264, crf 18, yuv420p): its own frame list starting at its named moment and holding its last
   state to its duration. Their probes are appended to evidence/render-tests.json.
Nothing outside assets/diagrams/DIA-05/ is written; the SVG rasters are temporary.
"""
from __future__ import annotations
import json, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'tools/render'))
import render_assets as ra  # noqa: E402

ID = 'DIA-05'


def main():
    ra.render(ID)
    base = ra.asset_dir(ID)
    data = json.loads((base / 'src/build.json').read_text(encoding='utf-8'))
    tests_path = base / 'evidence/render-tests.json'
    tests = json.loads(tests_path.read_text(encoding='utf-8'))
    with tempfile.TemporaryDirectory(prefix='vb-') as td:
        cache = {}
        for name, cut in data['cutdowns'].items():
            for f in cut['frames']:
                if f['file'] not in cache:
                    p = Path(td) / Path(f['file']).with_suffix('.png').name
                    ra.raster(base / 'src' / f['file'], p); cache[f['file']] = p
            report = ra.encode(base, cut['frames'], cut['duration'], base / 'exports' / f'{name}.mp4', cache)
            report.update(cutdown=name, key_second=cut['key_second'], key_moment=cut['key_moment'], states=len(cut['frames']))
            tests['video_probes'].append(report)
            print('ENCODED', name, cut['duration'], 's, key moment at', cut['key_second'], 's', flush=True)
    tests['command'] = 'python assets/diagrams/DIA-05/src/render.py'
    tests['cutdown_encoder'] = 'tools/render/render_assets.py encode(), called per cutdown from src/render.py'
    tests_path.write_text(json.dumps(tests, indent=2) + '\n', encoding='utf-8', newline='\n')


if __name__ == '__main__':
    main()
