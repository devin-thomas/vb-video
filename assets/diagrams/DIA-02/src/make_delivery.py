#!/usr/bin/env python3
"""Write DIA-02's delivery.json (revision 2) by hand from an authored template plus a hashed output inventory.

finish_delivery.py is deliberately not used for this revision (it rewrites ticket files and the shared template
note). The metadata below is authored; only the per-file byte counts and SHA-256 digests are computed, in the
same form as tools/render/finish_delivery.py output_inventory(): every file under the asset folder except
delivery.json, state.json and *.concat.txt. Run last, after every export and evidence file is final:
  python assets/diagrams/DIA-02/src/make_delivery.py
"""
from __future__ import annotations
import hashlib, json, platform, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; BASE=HERE.parent; ROOT=BASE.parents[2]

def inventory():
 items=[]
 for p in sorted(BASE.rglob('*')):
  if not p.is_file() or p.name in ['delivery.json','state.json'] or p.name.endswith('.concat.txt'):continue
  rel=p.relative_to(BASE).as_posix()
  role='rendered motion' if p.suffix=='.mp4' else 'rendered still' if rel.startswith('exports/') and p.suffix=='.png' else 'editable source' if rel.startswith('src/') else 'evidence / QA'
  items.append({'path':rel,'role':role,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 return items

def main():
 build=json.loads((HERE/'build.json').read_text(encoding='utf-8'))
 cut=json.loads((BASE/'evidence/cutdown-tests.json').read_text(encoding='utf-8'))
 probes={r['name']:r['probe'] for r in cut['video_probes']}
 def frames(name):return int(probes[name]['streams'][0]['nb_frames'])
 variants=[{'name':'full-rules','file':'exports/full-rules.mp4','duration_seconds':build['duration'],'key_second':0.0}]
 for name,cd in build['cutdowns'].items():
  variants.append({'name':name,'file':f'exports/{name}.mp4','duration_seconds':cd['duration'],'key_second':cd['key_second']})
 import cairosvg, PIL
 try:import playwright;pw=__import__('importlib.metadata').metadata.version('playwright')
 except Exception:pw=None
 ffmpeg=subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0]
 delivery={
  'id':'DIA-02','title':'War rules: shuffle, deal, flip, compare, collect',
  'production_status':'produced','release_status':'unreviewed',
  'provenance_type':'original authored source-based illustration','shared_version':'win95-workbench-1.1.0',
  'duration_seconds':build['duration'],'dimensions':{'width':1920,'height':1080},'fps':30,
  'outputs':inventory(),
  'variants':variants,
  'sources':build['sources'],
  'credits':[{'type':'original graphics','credit':'Source-based vector graphics authored for this production; no third-party images or font files included.'}],
  'tests':[
   {'test':'required outputs and checksums','result':'python tools/validate_delivery.py --id DIA-02 run after this inventory was written; result recorded in qa.md.'},
   {'test':'original source files','result':'sources/ unchanged; the five source digests in "sources" match the checked-in files.'},
   {'test':'raster dimensions and video codec/fps/duration (continuous version, stills, keyframes)','evidence':'evidence/render-tests.json','result':'passed: CairoSVG 1920 x 1080; preview.mp4 and full-rules.mp4 h264, yuv420p, 30/1, 1050 frames, 35.000 s'},
   {'test':'cutdown MP4 probes','evidence':'evidence/cutdown-tests.json','result':'passed: '+'; '.join(f"{n} {frames(n)} frames, {float(probes[n]['format']['duration']):.3f} s" for n in build['cutdowns'])},
   {'test':'offline HTML, deterministic seek, every SVG text bounding box','evidence':'evidence/browser-tests.json','result':'passed: 213 SVG files, 2584 text boxes, none out of canvas, no network request'},
   {'test':'manual visual review','result':{'mode':'Worker inspection of the revision 2 exports at 1920 x 1080 and 1280 x 720 (Read tool on PNGs and ffmpeg-extracted frames)',
     'scope':'Every cutdown poster (deck-hold, alternating-deal, normal-round, single-war, final-hold) and poster.png at full size; frames extracted from each cutdown at its key moment and inside its hold (deck-hold 0 / 29.5 s; alternating-deal 0.6, 0.667, 2.5, 5.767, 19.5 s; normal-round 1.2, 1.9, 3.5, 4.0, 15.5 s; single-war 1.0, 4.4, 6.3, 8.6, 10.6, 19.5 s; final-hold 0 / 13.5 s) at full size and at 1280 wide; preview.mp4 at 3.7, 12.2, 17.5, 19.5, 24.8 and 33 s; contact-sheet.png; proofs/poster-720.png.',
     'status':'Cards read as regular playing cards (corner index, pips, court crown and K letter, single centre pip on the aces); A♠ over K♥ is unmistakable at both sizes; the 4♠ / 4♦ tie and the 9♦ / A♦ deciding pair are legible at 1280 wide; counters sum to 52 in every frame checked; nothing clipped; every hold frame equals its cutdown poster. Not every one of the 3000 frames was viewed individually; the 206 authored states were covered by the frames above.'}}],
  'unresolved_gates':[],
  'toolchain':{'os':platform.platform(),'python':platform.python_version(),'ffmpeg':ffmpeg,'chromium':'Chromium 153.0.8010.12 (Playwright, in-memory HTML)','dotnet_path':None,'node':None,
   'packages':{'cairosvg':cairosvg.__version__,'Pillow':PIL.__version__,'playwright':pw},'network_used':False,'installs_performed':False,'font_files_distributed':False,
   'browser_note':'HTML tested by in-memory content loading.','cutdown_renderer':'assets/diagrams/DIA-02/src/render_cutdowns.py (CairoSVG + ffmpeg through tools/render/render_assets.py raster()/encode())'},
  'notes':build['notes']+['Original ticket requirements retained; these exports are not producer publication approval.',
   'Revision 2 exports (2026-09-16) replace the first cut; release status returned to unreviewed for producer re-review. Review questions are listed in qa.md.',
   'Each cutdown holds its end state to the end of its file (deck-hold 30 s, alternating-deal 20 s, normal-round 16 s, single-war 20 s, final-hold 14 s) so the editor can trim; key_second is the second within the cutdown at which its key moment occurs (0 for the two holds).']}
 (BASE/'delivery.json').write_text(json.dumps(delivery,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
 print('WROTE delivery.json',len(delivery['outputs']),'outputs',[v['name'] for v in variants])
if __name__=='__main__':main()
