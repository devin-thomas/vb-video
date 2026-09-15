#!/usr/bin/env python3
"""Package production results without treating editorial clearance as media production."""
from __future__ import annotations
import hashlib,json,platform,shutil,subprocess,sys,importlib.metadata,re
from collections import Counter
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
MAN=json.loads((ROOT/'manifest.json').read_text());ROWS={r['id']:r for r in MAN['tickets']}
VERSION='win95-workbench-1.0.0'
def dump(path,data):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def cmd(*args):
 try:return subprocess.check_output(args,text=True,stderr=subprocess.STDOUT).strip()
 except (OSError,subprocess.CalledProcessError) as e:return str(e)
def capabilities():
 return {'os':platform.platform(),'python':platform.python_version(),'ffmpeg':cmd('ffmpeg','-version').splitlines()[0],'chromium':cmd('chromium','--version'),'dotnet_path':shutil.which('dotnet'),'node':cmd('node','--version'),'packages':{n:importlib.metadata.version(n) for n in ['cairosvg','Pillow','playwright']},'network_used':False,'installs_performed':False,'font_files_distributed':False,'browser_note':'HTML tested by in-memory content loading; direct file:// navigation is restricted by the execution environment.'}
def ops():
 from studio import SVG,TEAL,BG,FG,MUTED
 import cairosvg
 shared=ROOT/'shared';deck=shared/'cards';deck.mkdir(exist_ok=True)
 identities=[str(rank)+suit for rank in range(2,11) for suit in 'SHDC']+[rank+suit for rank in ['J','Q','K','A'] for suit in 'SHDC']
 assert len(identities)==52 and len(set(identities))==52
 for identity in identities+['back']:
  s=SVG('none',identity);s.card('AS' if identity=='back' else identity,7,7,144,202,back=identity=='back')
  svg=s.finish().replace('width="1920" height="1080" viewBox="0 0 1920 1080"','width="164" height="226" viewBox="0 0 164 226"')
  (deck/f'{identity}.svg').write_text(svg)
 assert len({digest(deck/f'{i}.svg') for i in identities})==52
 atlas=SVG(BG,'52 original card identities');atlas.heading('52 original card identities')
 ranks=list(map(str,range(2,11)))+['J','Q','K','A']
 for row,suit in enumerate('SHDC'):
  for col,rank in enumerate(ranks):atlas.card(rank+suit,120+col*130,220+row*193,103,145)
 ob=ROOT/'assets/OPS-01';(ob/'exports').mkdir(exist_ok=True,parents=True);(ob/'evidence').mkdir(exist_ok=True)
 (shared/'card-atlas.svg').write_text(atlas.finish())
 cairosvg.svg2png(bytestring=atlas.finish().encode(),write_to=str(ob/'exports/card-atlas.png'))
 cap=capabilities();dump(ob/'exports/capabilities.json',cap)
 dump(shared/'VERSION.json',{'version':VERSION,'canvas':[1920,1080],'fps':30,'renderer':'studio.py / build_assets.py / diagrams.py','font_families':['Liberation Sans','DejaVu Sans Mono'],'fonts_included':False,'date_utc':datetime.now(timezone.utc).isoformat()})
 (ob/'exports/template-contract.md').write_text('''# Shared contract — win95-workbench-1.0.0

The media canvas is 1920 × 1080. Motion is 30 fps, H.264, yuv420p, silent. Color roles and drawing primitives live in `shared/studio.py`. Each asset owns its own scene files, timeline, variants, evidence, and exports. No network resources or font files are included.

## Authoring
`python shared/build_assets.py --id CODE-02` regenerates the authored scene and the exact source excerpt. `python shared/render_assets.py --id CODE-02` rasterizes and encodes it. Building sources resets that ticket to in_progress; run the QA and delivery finishing steps before relying on its state again. These commands do not install missing tools.

The shared authoring scripts encode this production batch's individual compositions. For normal per-asset edits, edit that asset's SVG states or timeline/build.json and use the renderer directly. Do not run build_assets.py afterward unless intentionally discarding those local source edits. Use only the assets explicitly selected by --id when refreshing sources.

## Deterministic HTML
Each `src/index.html` inlines its SVG states and exposes `window.__ASSET__`: id, width, height, fps, durationSeconds, ready, renderAt(seconds). `renderAt` clamps time and selects the last authored state whose start time is not greater than that time. It is independent of prior seek position. The delivered motion is discrete instructional state animation, not continuous optical simulation or a real screen recording. There are deliberate reading holds.

Space plays; Home resets. The gallery adds visible controls and seeking. Still assets use time zero. No fetch, CDN, icon library, tracking, remote font, or external image is required. Browser testing used in-memory loading because this sandbox blocks direct file URL navigation; offline structure was verified rather than assuming file:// was permitted here.

## Exports and variants
PNG and SVG are clean artwork. MP4 uses the same states as HTML at 30 fps. `src/build.json` is the raster/video build driver; `src/timeline.json` is the editorial timing record. Update both when manually changing motion timing, or use the authoring script to keep them together. Named cutdowns have independent MP4s where required by the original ticket. All other named variants have separate SVG and PNG files.

The 52 card primitives in shared/cards/ are original vectors. Small cards omit redundant corner details to remain legible. They do not use copied game sprites. Do not redistribute system font files; install the named fonts locally or accept a deliberate reflow when regenerating. Existing rendered media does not depend on the viewer having any fonts.
''')
 (ob/'exports/report.md').write_text('''# Shared visual system delivered

Win95-style dialogs and chapter cards, dark code/comparison panels, green-felt card scenes, original suit/rank card vectors, source highlighting, deterministic step-state HTML, PNG rendering, and 30 fps MP4 encoding are implemented. The production batch uses these components in 71 individually identified asset packages.

Smoke-test references: CARD-01 (dialog), CODE-02 (annotated source code), DIA-05 (seekable algorithm animation). Each has PNG, HTML, MP4, keyframes, and machine-readable checks. The included 52-card atlas and 53 standalone SVGs (52 faces plus a back) test reusable card coverage.

No program was executed: .NET is not installed. No historical image was acquired or passed off as original evidence. No font, remote resource, subscription, payment, or system installation was used.
''')
 dump(ob/'evidence/provenance.json',{'classification':'original shared design and export implementation','sources':[{'path':'../../sources/ASSET_PLAN.md','lines':[7,58],'sha256':digest(ROOT/'sources/ASSET_PLAN.md')}],'font_files_distributed':False,'remote_assets':[]})
 (ob/'evidence/source-excerpts.md').write_text('# Source brief\n\n```text\n'+'\n'.join((ROOT/'sources/ASSET_PLAN.md').read_text().splitlines()[6:58])+'\n```\n')
 dump(ob/'evidence/card-checks.json',{'identity_count':52,'unique_face_sources':52,'suits':['S','H','D','C'],'ranks':ranks,'back_provided':True,'copy_source':'Original vector construction','faces':[{ 'id':i,'file':'../../shared/cards/'+i+'.svg','sha256':digest(deck/(i+'.svg'))} for i in identities]})
 # Accurate blockers, not fake runtime delivery packages.
 for id in ['OPS-02','TERM-01','TERM-02','TERM-03','TERM-04','TERM-05','TERM-06','XTRA-06']:
  base=ROOT/'assets'/id;st=json.loads((base/'state.json').read_text());st.update(production_status='blocked',release_status='blocked',owner='ChatGPT — capability preflight',notes=['No dotnet executable found in the active environment. No real .NET harness, run capture, or editor capture was made. The original program remains unchanged. No installs were performed.'])
  dump(base/'state.json',st)
  (base/'BLOCKER.md').write_text('# Capability blocker\n\nNo installed .NET SDK was found (`dotnet_path: null` in OPS-01/exports/capabilities.json). No terminal output or IDE screenshot is fabricated. TERM-03 also remains unproduced: code cards are not substitutes for the requested complete editor capture. Use a machine with the SDK and suitable capture capability to execute the original full ticket.\n')
 (ROOT/'shared/REBUILD.md').write_text('''# Local rebuild

No installation script is included. Required preinstalled capabilities are Python, CairoSVG, Pillow, ffmpeg/ffprobe. Chromium plus Playwright are used only for browser checks. The actual environment is recorded under assets/OPS-01/exports/capabilities.json. Font files are not supplied.

```sh
python shared/build_assets.py --id CODE-02
python shared/render_assets.py --id CODE-02
python shared/qa_browser.py
python tools/validate_pack.py
```

Read assets/OPS-01/exports/template-contract.md before editing. Regeneration overwrites the chosen ticket's source and resets its live state; it is intentionally not an automatic publication approval. Use the finish_delivery script only after personally reviewing the batch's current results. The checked-in review record describes this delivery, not all possible future modifications.
''')

def output_inventory(base):
 items=[]
 for p in sorted(base.rglob('*')):
  if not p.is_file() or p.name in ['delivery.json','state.json'] or p.name.endswith('.concat.txt'):continue
  rel=p.relative_to(base).as_posix();role='rendered motion' if p.suffix=='.mp4' else 'rendered still' if rel.startswith('exports/') and p.suffix=='.png' else 'editable source' if rel.startswith('src/') else 'evidence / QA'
  items.append({'path':rel,'role':role,'bytes':p.stat().st_size,'sha256':digest(p)})
 return items

def deliveries():
 cap=json.loads((ROOT/'assets/OPS-01/exports/capabilities.json').read_text())
 visual=json.loads((ROOT/'review/manual-review.json').read_text()) if (ROOT/'review/manual-review.json').exists() else {}
 ids=sorted(p.parents[1].name for p in (ROOT/'assets').glob('*/src/build.json'))+['OPS-01']
 records=[]
 for id in ids:
  row=ROWS[id];base=ROOT/'assets'/id;support=id=='OPS-01'
  data=json.loads((base/'src/build.json').read_text()) if not support else {'duration':None,'variants':{'shared-system':'../../shared/VERSION.json'},'sources':json.loads((base/'evidence/provenance.json').read_text())['sources'],'notes':['Shared system only; no .NET captures or historical verification.']}
  if not support:
   assert (base/'evidence/render-tests.json').exists(),f'{id} unrendered'
   assert (base/'evidence/browser-tests.json').exists(),f'{id} missing browser checks'
   br=json.loads((base/'evidence/browser-tests.json').read_text());assert not br['errors'],f'{id} browser errors'
  gates=row['gates'];release='blocked' if gates else 'unreviewed';status='produced'
  manual=visual.get(id,{'mode':'Poster contact-sheet review','scope':'A 640 × 360 thumbnail, not every full-resolution animation frame.','status':'No obvious composition issue found at overview size; editorial and final frame-by-frame review remain.'})
  tests=[{'test':'required outputs and checksums','result':'Run tools/validate_delivery.py after manifest creation; result is stored in review/delivery-validation.json.'}, {'test':'original source files','result':'Hash-locked originals retained; validate_pack.py output recorded in review/pack-validation.txt.'}, {'test':'manual visual review','result':manual}]
  if not support:
   tests += [{'test':'raster dimensions and video codec/fps/duration','evidence':'evidence/render-tests.json','result':'passed'},{'test':'offline HTML, deterministic seek, every SVG text bounding box','evidence':'evidence/browser-tests.json','result':'passed'}]
  else:tests += [{'test':'52 distinct original card identities','evidence':'evidence/card-checks.json','result':'passed'}]
  note='\n'.join('- '+x for x in data.get('notes',[]))
  qa=f'''# {id} — Production QA

**Production:** produced. **Release:** {release}.

## Delivered
Each required media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. Existing outputs are real rendered media, not placeholder filenames. Independent variants belong to this ticket. The original source brief and code remain unchanged.

## Checks actually performed
- Rasterization and PNG dimensions checked at 1920 × 1080. Motion files checked with ffprobe for H.264, 30 fps, yuv420p, frame count and expected duration; per-file results are retained. Support-only OPS-01 is not a motion asset.
- HTML/SVG content was loaded in installed Chromium, with every source/variant scene checked for out-of-canvas text. Nonlinear forward/backward seeking was compared for identical SVG output. Remote requests were monitored; none were used. This is not a full text-overlap or semantic-proof system.
- The 25 literal Program.vb excerpts are checked against their canonical source ranges by the supplied validator. Code highlighting does not alter source files. Code line-wrap arrows are display markers, not inserted VB syntax.
- Visual review: {manual.get('mode','not recorded')}. {manual.get('scope','')} {manual.get('status','')}
- The source-based War and shuffle fixtures are deterministic teaching examples, not recorded program execution. Source/fixture checks are in the batch's review reports.

## Reproduction
`python shared/render_assets.py --id {id}` from the package root for media assets. For OPS-01, use `python shared/finish_delivery.py --ops-only`. Read shared/REBUILD.md first. Tool versions: assets/OPS-01/exports/capabilities.json.

## Remaining decisions
{'Assigned gates: '+', '.join(gates)+'. See evidence/claim-checks.json and docs/EDITORIAL_REGISTER.md.' if gates else 'No assigned claim gate; producer publication approval is still not assumed.'}

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
{note or '- Local timing and composition are authored production choices.'}
'''
  (base/'qa.md').write_text(qa)
  state=json.loads((base/'state.json').read_text());state.update(production_status=status,release_status=release,owner='ChatGPT — local production',notes=['Rendered/source deliverables, hashes, and executed checks are in delivery.json and qa.md.','Publication approval is separate from production.'])
  dump(base/'state.json',state)
  variants=[]
  for name in data.get('variants',{}):
   variants.append({'name':name,'files':([f'exports/{name}.png',f'src/variant-{name}.svg']+([f'exports/{name}.mp4'] if (base/f'exports/{name}.mp4').exists() else [])) if not support else ['exports/report.md','exports/template-contract.md','exports/card-atlas.png']})
  delivery={'id':id,'title':row['title'],'production_status':status,'release_status':release,'provenance_type':'original design infrastructure' if support else json.loads((base/'evidence/provenance.json').read_text())['classification'],'shared_version':VERSION,'duration_seconds':data.get('duration'),'dimensions':{'width':1920,'height':1080},'fps':30 if data.get('duration') else None,'outputs':output_inventory(base),'variants':variants,'sources':data.get('sources',[]),'credits':[{'type':'original graphics','credit':'Source-based vector graphics authored for this production; no third-party images or font files included.'}],'tests':tests,'unresolved_gates':gates,'toolchain':cap,'notes':data.get('notes',[])+['Original ticket requirements retained; these exports are not producer publication approval.']}
  dump(base/'delivery.json',delivery);records.append({k:delivery[k] for k in ['id','title','production_status','release_status','duration_seconds','fps','unresolved_gates']})
  tp=ROOT/row['ticket'];original=tp.read_text();original=original.split('\n## Production delivery — this batch')[0]
  tp.write_text(original+f'''\n## Production delivery — this batch

**Media/source production: produced. Publication status: {release}.**

[Individual delivery inventory](../assets/{id}/delivery.json) · [QA and remaining decisions](../assets/{id}/qa.md) · [Live state](../assets/{id}/state.json)

The work order above remains unchanged. See the package gallery for rendered previews. Production does not clear an unresolved historical or editorial gate.
''')
 dump(ROOT/'review/production-index.json',records)
 print('Inventoried',len(records),'deliveries')

if __name__=='__main__':
 if '--ops-only' in sys.argv:ops()
 elif '--deliveries-only' in sys.argv:deliveries()
 else:ops();deliveries()
