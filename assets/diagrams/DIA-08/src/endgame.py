#!/usr/bin/env python3
"""DIA-08 revision 2: the `endgame` cutdown, round 617 of the first recorded run (TERM-04).

Numbers come from assets/captures/TERM-04/source/stdout.txt (see evidence/source-excerpts.md): line 5 deals 26 / 26,
lines 7-1288 replayed give Player 1 = 50 and Player 2 = 2 entering round 617, line 1289 has both players play a 10
(10 of Diamonds / 10 of Spades), line 1290 the war, line 1291 "Player 2 has no cards left for the war - Player 1
takes the pot." The burn count is Math.Min(3, Math.Min(Player1.Count, Player2.Count)) = 1 (Program.vb:264). Burn
identities are not printed, so the burns stay face-down.

This script is additive: it writes endgame-*.svg, variant-endgame.svg and endgame.html into src/, merges the
`endgame` block into build.json and timeline.json, and (with `render`) rasterizes the states with CairoSVG and
encodes exports/endgame.mp4 with ffmpeg through the same raster()/encode() functions render_assets.py uses.
tools/render/render_assets.py --id DIA-08 renders the rest of the package; it ignores the `endgame` block except
for the variant still (exports/endgame.png). Run from the package root:

  python assets/diagrams/DIA-08/src/endgame.py author     # SVG states, poster, HTML, build/timeline merge
  python tools/render/render_assets.py --id DIA-08         # preview, cuts, poster, variants, keyframes, sheet
  python assets/diagrams/DIA-08/src/endgame.py render     # exports/endgame.mp4, proofs, render-tests entry
  python assets/diagrams/DIA-08/src/endgame.py inventory  # rehash delivery.json outputs

Stage seconds are word-timed the way tools/assembly/build_timeline.py places cutdowns (proportional word timing over
each beat's selected take, GAP_BEAT 0.45 s): S12-B03 is 21.12 s and S12-B04 21.28 s in narration/timeline.json.
"""
from __future__ import annotations
import argparse, hashlib, html, json, os, shutil, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;ROOT=BASE.parents[2]
sys.path.insert(0,str(ROOT/'tools/render'))
from studio import SVG,FELT,BG,PANEL,FG,MUTED,GOLD,wrap

ID='DIA-08';VARIANT='endgame';FPS=30
# Round 617 as captured (TERM-04/source/stdout.txt:1289-1291) and as replayed from lines 5-1288.
P1_CARD,P2_CARD='10D','10S'
COUNTS={1:(50,2,0),2:(49,1,2),3:(48,0,4),4:(52,0,0)}   # (Player 1, Player 2, pot) at each stage
STDOUT_1291='Player 2 has no cards left for the war - Player 1 takes the pot.'
STDOUT_1294='PLAYER 1 WINS THE WAR!'
# Word timing (seconds into the take) from build_timeline.word_time: duration * word_index / word_count.
B03,B04,GAP=21.12,21.28,0.45
def word_time(dur,i,n):return dur*i/n
KEY=6.5                                         # asset second at which the two tens are face-up (lands on "tie, war")
T_TIE=word_time(B03,20,51)                      # "tie, war" in S12-B03
def b03(i):return round(KEY+word_time(B03,i,51)-T_TIE,2)
def b04(i):return round(KEY+(B03-T_TIE)+GAP+word_time(B04,i,59),2)
STAGES=[0.0,KEY,b04(21),b04(50)]                # 1 hand sizes; 2 tie; 3 "so both players burned 1"; 4 "Player 1 took the four-card pot"
SUBS={'normally':b03(22),'only-one':b03(33),'empty':b04(26),'loop-top':b04(34)}
DURATION=42.0

def dashed(s,x,y,w,h,col,rx=7,sw=2.5):
 s.raw(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-dasharray="10 8"/>')

def pile(s,x,count,accent=None,w=143,h=201,y=383):
 # A hand drawn as a stack of backs: at most eight backs suggest a thick pile; two, one or none are drawn exactly.
 n=min(count,8)
 if n==0:
  dashed(s,x+8,y-10,w,h,accent or '#9cc3a8');s.text('empty',x+w/2+8,y+h/2+2,30,accent or '#cfe3d4',anchor='middle')
  return
 for k in range(n):
  s.card('AS',x+k*4,y-k*5,w,h,back=True,accent=accent if k==n-1 else None)

def board(stage,sub=None,awarded=0,moving=None):
 p1,p2,pot=COUNTS[stage]
 if stage==4:p1=48+awarded;pot=4-awarded
 titles={1:'Round 617: Player 2 has 2 cards left. Player 1 has 50.',2:'Both play a 10. Tie — war.',
  3:'Both burn 1 face-down — all Player 2 can spare.',4:'Player 2 cannot flip. Player 1 takes the 4-card pot.'}
 s=SVG(FELT,'How the 617-round run ended');s.rect(0,0,1920,1080,'url(#felt)')
 s.heading(titles[stage],f'The last round of the first recorded run (TERM-04, 617 rounds) · step {stage} of 4')
 s.text('Player 1',252,291,38,'#eff4ee',True,anchor='middle');s.text('Player 2',1668,291,38,'#eff4ee',True,anchor='middle')
 pile(s,178,p1)
 p2_accent='#f4d399' if sub in ('only-one','empty') else None
 pile(s,1592,p2,p2_accent)
 for x,n in [(252,p1),(1668,p2)]:
  s.text(str(n),x,678,76,'#fff',True,mono=True,anchor='middle');s.text('cards' if n!=1 else 'card',x,723,29,'#b9dac3',anchor='middle')
 s.rect(424,286,1072,533,'none','#68a07b',2,rx=8)
 s.text('Player 1',448,335,26,'#bed5c5');s.text('Player 2',448,774,26,'#bed5c5')
 cw=146;cardw=117;cardh=162;x0=960-(5*cw)/2+15;rows=(375,600)
 def col(i):return x0+i*cw
 def label(i,text,col_='#bed5c5'):s.text(text,col(i)+cardw/2,578,24,col_,anchor='middle')
 # Pot contents in stored play order: 10D, 10S, Player 1's burn, Player 2's burn (Pot(0..3)).
 cards=[]
 if stage>=2:cards+=[(P1_CARD,0,0,False),(P2_CARD,0,1,False)]
 if stage>=3:cards+=[('AS',1,0,True),('AS',1,1,True)]
 for idx,(identity,c,r,back) in enumerate(cards):
  if stage==4 and idx<awarded:continue
  x=col(c);y=rows[r]
  if stage==4 and moving is not None and idx==awarded:
   x=x+(190-x)*moving;y=y+(600-y)*moving
  s.card(identity,x,y,cardw,cardh,back=back)
 if stage>=2 and not (stage==4 and awarded>=2):label(0,'played')
 if stage>=3 and not (stage==4 and awarded>=4):label(1,'burned')
 if sub=='normally':
  for c in (1,2,3):
   for y in rows:dashed(s,col(c),y,cardw,cardh,'#9cc3a8')
  for y in rows:dashed(s,col(4),y,cardw,cardh,'#e1d7aa')
  label(2,'normally: burn 3 face-down');label(4,'then flip 1','#e1d7aa')
 s.text(f'Pot: {pot}',960,896,58,'#fff',True,mono=True,anchor='middle')
 caption={1:'26 / 26 at the deal. 616 rounds later: 50 / 2.',2:'10♦ against 10♠: equal ranks. Player 2 has 1 card left; Player 1 has 49.',
  3:'BurnCount = Math.Min(3, Math.Min(49, 1)) = 1. Each side burns one card face-down.',4:None}[stage]
 if sub=='normally':caption='Normally each player burns three face-down, then flips a fourth.'
 elif sub=='only-one':caption='But Player 2 has only 1 card left after playing that 10.'
 elif sub=='empty':caption='After the burn, Player 2’s hand is empty.'
 elif sub=='loop-top':caption='Back to the top of the loop: If Player2.Count = 0 Then …'
 if stage==4:
  if awarded<4 or moving is not None:
   s.text('To Player 1’s bottom, in pot order',960,958,31,'#e1d7aa',anchor='middle');s.arrow(430,700,330,600,'#e1d7aa',3)
   s.text(STDOUT_1291,960,1010,30,'#f4d399',mono=True,anchor='middle')
  else:
   s.text(STDOUT_1291,960,958,30,'#f4d399',mono=True,anchor='middle')
   s.text(f'Player 1: 52 cards. Player 2: 0. {STDOUT_1294}',960,1010,36,'#e9efea',True,anchor='middle')
 elif caption:s.text(caption,960,976,36,'#e9efea',anchor='middle')
 return s.finish()

def poster():
 s=SVG(BG,'How the 617-round run ended');s.heading('How the 617-round run ended','Round 617 of the first recorded run (TERM-04): both play a 10, the burn is capped at the shorter hand')
 heads=['1. Player 2 has 2 cards. Player 1 has 50.','2. Both play a 10: tie, war.','3. Both burn 1 — all Player 2 can spare.','4. Player 2 cannot flip. Player 1 takes the pot.']
 for i,title in enumerate(heads):
  st=i+1;p1,p2,pot=COUNTS[st];x=120+432*i
  s.rect(x,267,384,599,PANEL);s.lines(wrap(title,335,34,'bold'),x+24,326,34,FG,True,leading=1.14)
  for k,(label,n) in enumerate([('Player 1',p1),('Player 2',p2)]):
   cx=x+110+k*172;s.text(label,cx,455,24,MUTED,anchor='middle');s.text(str(n),cx,530,64,FG,True,mono=True,anchor='middle')
  cards=[] if st==1 else [(P1_CARD,False),(P2_CARD,False)] if st==2 else [(P1_CARD,False),(P2_CARD,False),('AS',True),('AS',True)] if st==3 else []
  if st==4:
   # The four pot cards, already face-down at the bottom of Player 1's hand, with the pot area cleared.
   for k in range(4):s.card('AS',x+238+k*6,612-k*6,57,80,back=True)
   s.arrow(x+226,650,x+110,650,GOLD,3);s.text('4 cards to Player 1’s bottom',x+192,760,24,GOLD,anchor='middle')
  for k,(identity,back) in enumerate(cards):
   col=k//2;row=k%2;s.card(identity,x+120+col*66,575+row*90,57,80,back=back)
  if st==2 or st==3:
   s.text('played',x+148,760,20,MUTED,anchor='middle')
   if st==3:s.text('burned',x+214,760,20,MUTED,anchor='middle')
  s.text(f'Pot: {pot}',x+24,815,38,GOLD,True,mono=True)
 s.lines(wrap('The burn is capped at the shorter hand (Program.vb line 264): one card each. The empty-hand check at the top of the loop then ends the war.',1680,30),120,960,30,MUTED)
 return s.finish()

def frames():
 fs=[(STAGES[0],board(1)),(STAGES[1],board(2)),(SUBS['normally'],board(2,'normally')),(SUBS['only-one'],board(2,'only-one')),
  (STAGES[2],board(3)),(SUBS['empty'],board(3,'empty')),(SUBS['loop-top'],board(3,'loop-top'))]
 t=STAGES[3]
 for n in range(4):
  fs.append((round(t+n*.3,2),board(4,awarded=n,moving=.45)));fs.append((round(t+n*.3+.15,2),board(4,awarded=n+1)))
 fs.append((round(t+1.2,2),board(4,awarded=4)))
 return fs

def author():
 for old in HERE.glob('endgame-*.svg'):old.unlink()
 names=[];dedup={}
 for t,svg in frames():
  sha=hashlib.sha256(svg.encode()).hexdigest()
  if sha not in dedup:
   n=f'endgame-{len(dedup):04}.svg';dedup[sha]=n;(HERE/n).write_text(svg,encoding='utf-8',newline='\n')
  names.append({'time':t,'file':dedup[sha]})
 (HERE/f'variant-{VARIANT}.svg').write_text(poster(),encoding='utf-8',newline='\n')
 block={'duration':DURATION,'fps':FPS,'frames':names,'poster':f'variant-{VARIANT}.svg','html':'endgame.html','key_second':KEY,'stage_seconds':STAGES,
  'sub_states':SUBS,'landing':{'key_second':'S12-B03 "tie, war"','stage_3':'S12-B04 "so both players burned 1"','stage_4':'S12-B04 "Player 1 took the four-card pot"'},
  'render':'assets/diagrams/DIA-08/src/endgame.py render (CairoSVG raster + ffmpeg concat encode, the raster()/encode() functions of tools/render/render_assets.py)'}
 for fn in ('build.json','timeline.json'):
  data=json.loads((HERE/fn).read_text(encoding='utf-8'))
  data.setdefault('variants',{})
  if fn=='build.json':data['variants'][VARIANT]=f'variant-{VARIANT}.svg'
  else:
   data['variant_names']=[v for v in data['variant_names'] if v!=VARIANT]+[VARIANT]
   data['cuts_note']='endgame is a separate word-timed timeline (below), not a window of the 12 s war sequence.'
  data[VARIANT]=block
  (HERE/fn).write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8',newline='\n')
 table={n:(HERE/n).read_text(encoding='utf-8') for n in dedup.values()}
 timeline={'id':ID,'variant':VARIANT,'durationSeconds':DURATION,'fps':FPS,'width':1920,'height':1080,'frames':names,'key_second':KEY,'stage_seconds':STAGES}
 title='War mechanic: the 617-round endgame'
 doc='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+html.escape(title)+'''</title><style>html,body{margin:0;background:#000;height:100%;overflow:hidden}#stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center}svg{width:100%;height:100%;object-fit:contain}</style><div id="stage" aria-label="'''+html.escape(title,quote=True)+'''"></div><script>const timeline='''+json.dumps(timeline,ensure_ascii=False)+''';const scenes='''+json.dumps(table,ensure_ascii=False)+''';const stage=document.getElementById('stage');window.__ASSET__={id:timeline.id,variant:timeline.variant,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;else break}stage.innerHTML=scenes[f.file];return f.file}};__ASSET__.renderAt(0);let start=null,playing=false;document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();playing=!playing;start=null;requestAnimationFrame(tick)}if(e.code==='Home'){playing=false;__ASSET__.renderAt(0)}});function tick(ts){if(!playing)return;if(start===null)start=ts;const t=(ts-start)/1000;__ASSET__.renderAt(t);if(t<__ASSET__.durationSeconds)requestAnimationFrame(tick);else playing=false}</script></html>'''
 (HERE/'endgame.html').write_text(doc,encoding='utf-8',newline='\n')
 print('AUTHORED',ID,VARIANT,len(dedup),'states; stages',STAGES,'subs',SUBS,flush=True)

def render():
 from render_assets import raster,encode
 from PIL import Image
 block=json.loads((HERE/'build.json').read_text(encoding='utf-8'))[VARIANT]
 with tempfile.TemporaryDirectory(prefix='vb-endgame-') as td:
  cache={}
  for f in block['frames']:
   if f['file'] not in cache:
    p=Path(td)/Path(f['file']).with_suffix('.png').name;raster(HERE/f['file'],p);cache[f['file']]=p
  raster(HERE/block['poster'],BASE/'exports'/f'{VARIANT}.png')
  report=encode(BASE,block['frames'],block['duration'],BASE/'exports'/f'{VARIANT}.mp4',cache)
  # Proofs: the poster at 720p and one frame per stage at 1280 x 720 for the manual review record.
  Image.open(BASE/'exports'/f'{VARIANT}.png').resize((1280,720),Image.Resampling.LANCZOS).save(BASE/'proofs'/f'{VARIANT}-720.png')
  for i,t in enumerate(block['stage_seconds'],1):
   f=next(f for f in reversed(block['frames']) if f['time']<=t)
   Image.open(cache[f['file']]).resize((1280,720),Image.Resampling.LANCZOS).save(BASE/'proofs'/f'{VARIANT}-stage{i}-720.png')
 rt=BASE/'evidence/render-tests.json';data=json.loads(rt.read_text(encoding='utf-8'))
 data['video_probes']=[p for p in data['video_probes'] if p['file'].replace('\\','/')!=f'exports/{VARIANT}.mp4']+[report]
 data['endgame_command']=f'python assets/diagrams/DIA-08/src/endgame.py render'
 rt.write_text(json.dumps(data,indent=2),encoding='utf-8',newline='\n')
 print('RENDERED',ID,VARIANT,report['probe']['format']['duration'],'s',flush=True)

def inventory():
 roles={'exports':lambda p:'rendered motion' if p.suffix=='.mp4' else 'rendered still','src':lambda p:'editable source','evidence':lambda p:'evidence / QA','proofs':lambda p:'evidence / QA'}
 outputs=[]
 for p in sorted(BASE.rglob('*')):
  rel=p.relative_to(BASE).as_posix()
  if not p.is_file() or rel in ('delivery.json','state.json') or '__pycache__' in rel or rel.endswith('.concat.txt'):continue
  role=roles.get(rel.split('/')[0],lambda p:'evidence / QA')(p)
  data=p.read_bytes();outputs.append({'path':rel,'role':role,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
 d=json.loads((BASE/'delivery.json').read_text(encoding='utf-8'));d['outputs']=outputs
 (BASE/'delivery.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
 print('INVENTORY',len(outputs),'outputs',flush=True)

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter);ap.add_argument('step',choices=['author','render','inventory'])
 {'author':author,'render':render,'inventory':inventory}[ap.parse_args().step]()
