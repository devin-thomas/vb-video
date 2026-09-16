#!/usr/bin/env python3
"""Encode DIA-02's named cutdowns (build.json "cutdowns") as independent MP4s in exports/.

Uses the batch renderer's own raster() and encode() from tools/render/render_assets.py (imported, not modified),
so every cutdown is CairoSVG at 1920 x 1080 and the same ffmpeg settings as preview.mp4: 30 fps, H.264, yuv420p,
crf 18, faststart. Each cutdown's frame list starts at its named moment and its last state holds to its duration.
Run after render_assets.py:  python assets/diagrams/DIA-02/src/render_cutdowns.py
Writes evidence/cutdown-tests.json with the ffprobe result and key_second of every file.
"""
from __future__ import annotations
import json, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent; BASE=HERE.parent; ROOT=BASE.parents[2]
sys.path.insert(0,str(ROOT/'tools/render'))
import cairosvg
import render_assets as ra

def main():
 data=json.loads((HERE/'build.json').read_text(encoding='utf-8'));reports=[]
 with tempfile.TemporaryDirectory(prefix='vb-') as td:
  cache={}
  for name,cd in data['cutdowns'].items():
   for f in cd['frames']:
    if f['file'] not in cache:
     p=Path(td)/Path(f['file']).with_suffix('.png').name;ra.raster(HERE/f['file'],p);cache[f['file']]=p
   rep=ra.encode(BASE,cd['frames'],cd['duration'],BASE/'exports'/f'{name}.mp4',cache)
   rep.update(name=name,duration_seconds=cd['duration'],key_second=cd['key_second'],states=len({f['file'] for f in cd['frames']}),key_moment=cd.get('key_moment'))
   reports.append(rep);print('CUTDOWN',name,cd['duration'],'s key',cd['key_second'],flush=True)
 (BASE/'evidence/cutdown-tests.json').write_text(json.dumps({'renderer':'CairoSVG '+cairosvg.__version__+' via tools/render/render_assets.py raster()/encode()','png_dimensions':'1920x1080','video_probes':reports,'command':'python assets/diagrams/DIA-02/src/render_cutdowns.py'},indent=2),encoding='utf-8',newline='\n')
if __name__=='__main__':main()
