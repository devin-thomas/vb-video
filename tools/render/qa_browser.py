#!/usr/bin/env python3
"""Offline SVG/HTML checks in installed Chromium. Does not download a browser."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,hashlib,sys,os
ROOT=Path(__file__).resolve().parents[2]
results=[]
# System Chromium on the original Linux build machine; otherwise Playwright's bundled Chromium.
LAUNCH={'executable_path':'/usr/bin/chromium','args':['--no-sandbox']} if os.path.exists('/usr/bin/chromium') else {}
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,**LAUNCH)
 page=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
 for fp in sorted((ROOT/'assets').glob('*/*/src/build.json')):
  data=json.loads(fp.read_text());base=fp.parents[1];id=base.name;errors=[];remote=[]
  def onreq(req):
   if req.url.startswith(('http:','https:')):remote.append(req.url)
  page.on('request',onreq)
  page.set_content((base/'src/index.html').read_text(),wait_until='load');page.evaluate('window.__ASSET__.ready')
  dur=data['duration'] or 0;t=dur*.53
  a=page.evaluate('(t)=>{__ASSET__.renderAt(t);return document.getElementById("stage").innerHTML}',t)
  page.evaluate('(t)=>__ASSET__.renderAt(t)',dur)
  page.evaluate('()=>__ASSET__.renderAt(0)')
  c=page.evaluate('(t)=>{__ASSET__.renderAt(t);return document.getElementById("stage").innerHTML}',t)
  if a!=c:errors.append('Non-deterministic seeking')
  # Test every authored scene AND every named variant, including poster.
  overflow=[];total=0
  files=sorted(set([x['file'] for x in data['frames']]+list(data['variants'].values())+[data['poster']]))
  for name in files:
   txt=(base/'src'/name).read_text()
   page.evaluate('(s)=>document.getElementById("stage").innerHTML=s',txt)
   boxes=page.evaluate('''()=>Array.from(document.querySelectorAll('svg text')).map(el=>{let b=el.getBBox(),m=el.getCTM();let pts=[[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]].map(([x,y])=>({x:m.a*x+m.c*y+m.e,y:m.b*x+m.d*y+m.f}));return {text:el.textContent,x:Math.min(...pts.map(p=>p.x)),y:Math.min(...pts.map(p=>p.y)),right:Math.max(...pts.map(p=>p.x)),bottom:Math.max(...pts.map(p=>p.y))}})''')
   total+=len(boxes)
   for box in boxes:
    if box['x'] < -1 or box['y'] < -1 or box['right']>1921 or box['bottom']>1081:
     overflow.append({'file':name,**box})
  if overflow:errors.append(f'{len(overflow)} out-of-canvas text boxes')
  if remote:errors.append('Unexpected network request')
  row={'id':id,'browser':'installed Chromium '+b.version,'loading_mode':'In-memory HTML (file:// navigation restricted by this browser environment)','offline':not remote,'deterministic_seek':a==c,'svg_files_checked':len(files),'text_boxes_checked':total,'out_of_canvas':overflow,'errors':errors,'limitations':['Checks canvas bounds, not every possible overlap or semantic correctness.','Typography depends on installed fonts for editable sources; rendered media is frozen.']}
  (base/'evidence/browser-tests.json').write_text(json.dumps(row,indent=2));results.append(row)
  page.remove_listener('request',onreq);print(id,len(files),errors,flush=True)
 b.close()
(ROOT/'review/browser-summary.json').write_text(json.dumps(results,indent=2))
