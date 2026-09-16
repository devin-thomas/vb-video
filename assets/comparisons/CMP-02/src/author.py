#!/usr/bin/env python3
"""CMP-02 revision 2: Sub versus Function, animated.

Local authoring script for this asset only. It writes the deterministic scene
states, named variants, build.json, timeline.json and index.html into this
folder using the shared primitives in tools/render/studio.py (read only).
Run from anywhere:  python assets/comparisons/CMP-02/src/author.py
Then render with:   python tools/render/render_assets.py --id CMP-02
"""
from __future__ import annotations
import hashlib, html, json, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; BASE=HERE.parent; ROOT=BASE.parents[2]
sys.path.insert(0,str(ROOT/'tools/render'))
from studio import SVG,BG,FG,MUTED,LINE,BLUE,GOLD,width,code_line

ID='CMP-02'; TITLE='Sub versus Function'
SUB='A Sub, like void, gives nothing back. A Function gives back a value.'
SIZE=30                      # same code size in both columns
CW=width('0',SIZE,'mono')    # monospace advance
LEAD=42
PANEL_Y,PANEL_W,PANEL_H=248,810,652
LEFT_X,RIGHT_X=120,990

# Devin's pairing (review note 14). The VB Function signature is soft-wrapped
# for display; the wrap is not a source line break and inserts no VB syntax.
C_ROWS=[['void HelloWorld() { ... }'],['int Add(int a, int b) { return a + b; }']]
VB_ROWS=[['Sub HelloWorld()','    ...','End Sub'],
         ['Function Add(a As Integer, b As Integer)','        As Integer','    ...','End Function']]
FOCUS={'c':['void','int'],'vb':['Sub','Function']}
CALLS=[('HelloWorld()',None),('Add(3, 4)','7')]

ROW1_MID,ROW2_MID=470,667          # baselines of the single C lines
SEP_Y=552
STRIP_Y,STRIP_H=764,116
CALL_BASE=848; SLOT_Y,SLOT_H,SLOT_W=814,44,100
VALUE_W,VALUE_H=48,44
VALUE_START_Y=712                   # centre of the value box before it moves
TRAVEL_STEPS=12

def slot_x(x0,i):
 # Cell A (HelloWorld) and cell B (Add) share one strip line.
 return x0+312 if i==0 else x0+666
def value_box(s,cx,cy,value):
 s.rect(cx-VALUE_W/2,cy-VALUE_H/2,VALUE_W,VALUE_H,GOLD,rx=4)
 s.text(value,cx,cy+11,SIZE,'#111',True,True,'middle')

def panel(s,x0,label,lang,rows,state,focus=False):
 s.rect(x0,PANEL_Y,PANEL_W,PANEL_H,'#171c23');s.rect(x0,PANEL_Y,PANEL_W,6,BLUE if lang=='vb' else '#738192')
 s.text(label,x0+44,335,53,FG,True)
 x=x0+44
 for r,(lines,mid) in enumerate(zip(rows,[ROW1_MID,ROW2_MID])):
  if state['rows']<=r:continue
  y=mid-(len(lines)-1)*LEAD/2
  for j,line in enumerate(lines):
   f=FOCUS[lang][r] if focus and j==0 else None
   code_line(s,line,x,y+j*LEAD,SIZE,'cs' if lang=='c' else 'vb',f)
  if r==0 and state['rows']>1:s.line(x,SEP_Y,x0+PANEL_W-44,SEP_Y,LINE,2)
 if not state['strip']:return
 s.rect(x0+24,STRIP_Y,PANEL_W-48,STRIP_H,'#10141a')
 s.text('When called',x,STRIP_Y+30,22,MUTED)
 for i,(call,value) in enumerate(CALLS):
  cx=x if i==0 else x0+452
  end=code_line(s,call,cx,CALL_BASE,SIZE,'cs' if lang=='c' else 'vb')
  s.arrow(end+12,CALL_BASE-11,end+42,CALL_BASE-11,MUTED,2.5)
  sx=slot_x(x0,i);centre=sx+SLOT_W/2
  if i==1 and state['value']=='done':
   value_box(s,centre,SLOT_Y+SLOT_H/2,value)
  else:
   s.raw(f'<rect x="{sx:.2f}" y="{SLOT_Y:.2f}" width="{SLOT_W}" height="{SLOT_H}" rx="4" fill="none" stroke="{LINE}" stroke-width="2" stroke-dasharray="6 6"/>')
   if i==0 and state['nothing']:s.text('nothing',centre,CALL_BASE-1,24,MUTED,anchor='middle')
 # The returned value leaves the Function / int row and drops into the call slot.
 if isinstance(state['value'],int):
  step=state['value'];centre=slot_x(x0,1)+SLOT_W/2;end_y=SLOT_Y+SLOT_H/2
  cy=VALUE_START_Y+(end_y-VALUE_START_Y)*step/TRAVEL_STEPS
  value_box(s,centre,cy,'7')

def scene(state,focus=False):
 s=SVG(BG,TITLE);s.heading(TITLE,SUB if state['sub'] else None)
 panel(s,LEFT_X,'C / C++ / C#','c',C_ROWS,state,focus)
 panel(s,RIGHT_X,'VB','vb',VB_ROWS,state,focus)
 s.text('Syntax comparison',120,978,30,MUTED)
 return s.finish()

def st(rows=2,strip=True,value='done',nothing=True,sub=True):
 return {'rows':rows,'strip':strip,'value':value,'nothing':nothing,'sub':sub}

DURATION=8
frames=[(0.0,st(0,False,None,False,False)),(0.4,st(1,False,None,False,False)),(1.4,st(2,False,None,False,False)),(2.6,st(2,True,None,False,False)),(3.4,st(2,True,0,False,False))]
for k in range(1,TRAVEL_STEPS+1):frames.append((round(3.4+0.1*k,6),st(2,True,k,False,False)))
frames+=[(4.8,st(2,True,'done',False,False)),(5.4,st(2,True,'done',True,False)),(6.0,st())]
END=st()
BEATS=['0–2.6 s: heading, both columns, then the HelloWorld / Sub row and the Add / Function row appear.',
       '2.6–3.4 s: the call strip appears: HelloWorld() and Add(3, 4) with empty result slots.',
       '3.4–4.8 s: the returned value 7 leaves the Function / int row and drops into the Add(3, 4) slot; the Sub / void slot stays empty.',
       '4.8–6.0 s: the Sub / void slot is labelled "nothing"; the summary line appears.',
       '6.0–8 s: hold on the end state (poster).']

def write(path,text):path.write_text(text,encoding='utf-8',newline='\n')
def main():
 for old in HERE.glob('scene-*.svg'):old.unlink()
 names=[];dedup={}
 for t,state in frames:
  svg=scene(state);sha=hashlib.sha256(svg.encode()).hexdigest()
  if sha not in dedup:n=f'scene-{len(dedup):04}.svg';dedup[sha]=n;write(HERE/n,svg)
  names.append({'time':t,'file':dedup[sha]})
 poster=scene(END);write(HERE/'scene.svg',poster)
 variants={'comparison':scene(END),'token-focus':scene(END,True)}
 vmap={}
 for name,svg in variants.items():write(HERE/f'variant-{name}.svg',svg);vmap[name]=f'variant-{name}.svg'
 # The script's literal BuildDeck pair survives as a still note, no longer the poster.
 if (HERE/'variant-byref-note.svg').exists():vmap['byref-note']='variant-byref-note.svg'
 notes=['Revision 2 (2026-09-16, review notes 13 and 14): Sub versus Function, animated. Left header lists C / C++ / C# because both left-hand snippets are valid in all three.',
        'HelloWorld and Add are agent-authored teaching snippets, not Program.vb excerpts; Add(3, 4) → 7 is an illustration of a returned value, not recorded program output. No compile/run is claimed.',
        'The VB Function signature is soft-wrapped for display (As Integer on a second visual line); the wrap is not a source line break and inserts no line-continuation syntax.',
        'Syntax comparison only: the HelloWorld pair shows that a Sub, like void, returns nothing; the Add pair shows that a Function, like int, returns a value. No other equivalence is claimed.',
        'byref-note keeps the script\'s literal BuildDeck pair (void BuildDeck(Card[] deck) versus Sub BuildDeck(ByRef Deck() As Card)) as a still; the C# snippet has no ref keyword, and it makes no parameter-rebinding claim.']
 sources=[{'path':'../../../sources/ASSET_PLAN.md','lines':[38,38],'sha256':hashlib.sha256((ROOT/'sources/ASSET_PLAN.md').read_bytes()).hexdigest(),'relationship':'source creative brief'},
          {'path':'../../../sources/SCRIPT.md','lines':[265,270],'sha256':hashlib.sha256((ROOT/'sources/SCRIPT.md').read_bytes()).hexdigest(),'relationship':'source creative brief'},
          {'path':'../../../review/cut-notes-2026-09-16.md','lines':[20,21],'sha256':hashlib.sha256((ROOT/'review/cut-notes-2026-09-16.md').read_bytes()).hexdigest(),'relationship':"Devin's review notes 13 and 14 (revision 2 brief)"}]
 timeline={'id':ID,'durationSeconds':DURATION,'fps':30,'width':1920,'height':1080,'beats':BEATS,'frames':names,'cuts':{},'variant_names':list(vmap),'motion_model':'Explicit deterministic step states with readable holds; MP4 encodes the same scene changes at 30 fps. The value travel is 12 authored positions at 0.1 s each.'}
 write(HERE/'timeline.json',json.dumps(timeline,indent=2,ensure_ascii=False)+'\n')
 table={n:(HERE/n).read_text(encoding='utf-8') for n in dedup.values()}
 html_doc='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+html.escape(TITLE)+'''</title><style>html,body{margin:0;background:#000;height:100%;overflow:hidden}#stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center}svg{width:100%;height:100%;object-fit:contain}</style><div id="stage" aria-label="'''+html.escape(TITLE,quote=True)+'''"></div><script>const timeline='''+json.dumps(timeline,ensure_ascii=False)+''';const scenes='''+json.dumps(table,ensure_ascii=False)+''';const stage=document.getElementById('stage');window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;else break}stage.innerHTML=scenes[f.file];return f.file}};__ASSET__.renderAt(0);let start=null,playing=false;document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();playing=!playing;start=null;requestAnimationFrame(tick)}if(e.code==='Home'){playing=false;__ASSET__.renderAt(0)}});function tick(ts){if(!playing)return;if(start===null)start=ts;const t=(ts-start)/1000;__ASSET__.renderAt(t);if(t<__ASSET__.durationSeconds)requestAnimationFrame(tick);else playing=false}</script></html>'''
 write(HERE/'index.html',html_doc)
 build={'id':ID,'duration':DURATION,'frames':names,'variants':vmap,'poster':'scene.svg','cuts':{},'notes':notes,'sources':sources,'kind':'motion'}
 write(HERE/'build.json',json.dumps(build,indent=2,ensure_ascii=False)+'\n')
 print('AUTHORED',ID,len(dedup),'states',len(names),'frames')
if __name__=='__main__':main()
