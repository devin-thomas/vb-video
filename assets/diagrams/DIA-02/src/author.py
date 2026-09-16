#!/usr/bin/env python3
"""DIA-02 revision 2: the War rules sequence re-authored as beat-accurate, holdable cutdowns.

Local authoring script for this asset only (Devin's review notes 9 and 11, 2026-09-16). It writes the
deterministic scene states, the named variants, build.json, timeline.json and index.html into this folder,
drawing with the shared primitives in tools/render/studio.py (read only; card faces are the revised
win95-workbench-1.1.0 faces drawn by SVG.card()).

Run from anywhere:   python assets/diagrams/DIA-02/src/author.py
Continuous version:  python tools/render/render_assets.py --id DIA-02      (preview.mp4, full-rules.mp4, stills)
Cutdowns:            python assets/diagrams/DIA-02/src/render_cutdowns.py  (the five named MP4s from build.json)

Every cutdown starts at its named moment and holds its end state to the end of the file. The second at which
its key moment occurs is recorded as key_second so the timeline builder can land it on the narrated word.
All states come from tools/fixtures/war_storyboard.json; they are teaching examples, not a captured game.
"""
from __future__ import annotations
import hashlib, html, json, math, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; BASE=HERE.parent; ROOT=BASE.parents[2]
sys.path.insert(0,str(ROOT/'tools/render'))
from studio import SVG,FELT,GOLD

ID='DIA-02'; TITLE='War rules: shuffle, deal, flip, compare, collect'
WHITE='#ffffff'; PALE='#dfebdf'; MINT='#b9dac3'; EDGE='#7aaa87'
FIX=json.loads((ROOT/'tools/fixtures/war_storyboard.json').read_text(encoding='utf-8'))
NR=FIX['normal_round']; SW=FIX['single_war']
ACE,KING=NR['face_up']                       # AS, KH
EVENTS=SW['events']; ORDER=[c for e in EVENTS[:3] for c in e['cards']]   # ten cards in play order
BURN=set(EVENTS[1]['cards'])
assert NR['start']=={'player1':26,'player2':26,'pot':0} and NR['end']=={'player1':27,'player2':25,'pot':0} and NR['winner']==1
assert EVENTS[3]['winner']==2 and EVENTS[3]['counts']==[21,31,0] and len(ORDER)==10

# Board geometry (shared by every scene so the cutdowns cut together): Player 1 left, Player 2 right, pot centre.
PILE=((190,400),(1580,400)); PW,PH=150,212          # face-down piles
DECK=(875,380); DW,DH=170,239                        # the undealt deck
SLOT=((733,390),(1016,390)); CW,CH=170,239           # face-up pair in the normal round
COLX=[600+170*c for c in range(5)]; ROWY=(300,545)   # war pot: one column per pair, Player 1 above Player 2
FPS=30
def fr(n):return n/FPS                               # exact frame times keep the renderer's quantisation honest

def felt(title,sub=None):
 s=SVG(FELT,title);s.rect(0,0,1920,1080,'url(#felt)');s.heading(title,sub);return s
def outline(s,x,y,w,h):
 s.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="none" stroke="{EDGE}" stroke-width="2" stroke-dasharray="10 8"/>')
def stack(s,x,y,w,h,n,maxl=6,per=9):
 # A face-down pile whose visible thickness grows with its count.
 if n<=0:outline(s,x,y,w,h);return
 for i in range(min(maxl,1+(n-1)//per)):s.card('AS',x+i*2,y-i*3,w,h,back=True)
def players(s,counts):
 for i,(x,y) in enumerate(PILE):
  s.text(f'Player {i+1}',x+PW/2,330,37,WHITE,True,anchor='middle')
  stack(s,x,y,PW,PH,counts[i])
  s.text(str(counts[i]),x+PW/2,722,67,WHITE,True,True,'middle');s.text('cards',x+PW/2,762,27,MINT,anchor='middle')
def caption(s,text,y=880,size=42):s.text(text,960,y,size,WHITE,anchor='middle')
def pot(s,n):s.text(f'Pot: {n}',960,980,39,WHITE,mono=True,anchor='middle')
def lerp(a,b,f):return a+(b-a)*f

def deck_svg():
 s=felt('52 cards')
 stack(s,DECK[0],DECK[1],DW,DH,52,maxl=8,per=7)
 s.text('Deck: 52',960,700,51,WHITE,mono=True,anchor='middle')
 return s.finish()

def deal_svg(k=0,flight=None):
 """k cards have left the deck; flight 'a'/'b' means card k is still in the air (one third / two thirds across)."""
 s=felt('52 cards · 26 each')
 landed=k-1 if flight else k
 players(s,[(landed+1)//2,landed//2])
 remaining=52-k
 if remaining:stack(s,DECK[0],DECK[1],DW,DH,remaining,maxl=8,per=7)
 else:outline(s,DECK[0],DECK[1],DW,DH)
 s.text(f'Deck: {remaining}',960,700,51,WHITE,mono=True,anchor='middle')
 if flight:
  to=PILE[0] if k%2 else PILE[1];f={'a':1/3,'b':2/3}[flight]
  x=lerp(DECK[0]+10,to[0],f);y=lerp(DECK[1]+14,to[1],f)-60*math.sin(math.pi*f)
  s.card('AS',x,y,PW,PH,back=True)
 if landed or flight:caption(s,'Alternate one card at a time' if landed<52 else '26 cards per player')
 return s.finish()

def round_svg(phase,step=0):
 """rest → draw → down → flip → compare → collect(step 0..5) → done."""
 s=felt('Higher rank wins','Aces high')
 counts=[26,26,0] if phase=='rest' else [27,25,0] if phase=='done' else [25,25,2]
 if phase=='collect':
  # The won pair travels first in draw order so it slides under Player 1's pile: won cards go to the bottom.
  f=(step+1)/6;tx,ty=PILE[0][0],PILE[0][1]+36
  for i,(c,(sx,sy)) in enumerate(zip((ACE,KING),SLOT)):
   s.card(c,lerp(sx,tx+i*26,f),lerp(sy,ty,f),lerp(CW,PW,f),lerp(CH,PH,f),back=f>=.5,opacity=1 if f<.9 else .6)
 players(s,counts[:2])
 if phase=='draw':
  for i,(c,(sx,sy)) in enumerate(zip((ACE,KING),SLOT)):
   px,py=PILE[i];s.card(c,lerp(px,sx,.5),lerp(py,sy,.5),lerp(PW,CW,.5),lerp(PH,CH,.5),back=True)
 elif phase=='down':
  for c,(sx,sy) in zip((ACE,KING),SLOT):s.card(c,sx,sy,CW,CH,back=True)
 elif phase in ('flip','compare'):
  s.card(ACE,*SLOT[0],CW,CH,accent=GOLD if phase=='compare' else None);s.card(KING,*SLOT[1],CW,CH)
  if phase=='compare':s.text('>',960,540,84,GOLD,True,anchor='middle');caption(s,'Ace beats King')
 elif phase=='done':
  s.arrow(640,600,352,600,GOLD,5);caption(s,'Won cards go to the bottom')
 pot(s,counts[2])
 return s.finish()

def war_svg(shown=0,up0=False,up4=False,flight=None,awarded=0,moving=None,cap=None):
 """shown: pairs on the table (0..5: the tie, three burns, the deciding pair). flight=(pair, fraction) is a pair in
 the air from the piles. awarded: cards already under Player 2's pile; moving: the card on its way there."""
 s=felt('Tie? War.','A second example · 26 cards each')
 placed=shown*2;drawn=placed+(2 if flight else 0)
 counts=[26-drawn//2,26-drawn//2+awarded,drawn-awarded]
 def face(idx,c):
  col=idx//2;return c in BURN or (col==0 and not up0) or (col==4 and not up4)
 players(s,counts[:2])
 s.rect(460,270,1000,530,'none','#68a07b',2,rx=8)
 s.text('Player 1',480,415,24,MINT);s.text('Player 2',480,660,24,MINT)
 for idx,c in enumerate(ORDER[:placed]):
  if idx<awarded or idx==moving:continue
  col,row=idx//2,idx%2
  s.card(c,COLX[col],ROWY[row],PW,PH,back=face(idx,c),accent=GOLD if (col==4 and up4 and c=='AD') else None)
 if flight:
  pair,f=flight
  for row in (0,1):
   px,py=PILE[row];s.card('AS',lerp(px,COLX[pair],f),lerp(py,ROWY[row],f),PW,PH,back=True)
 if moving is not None:
  # The card in the air is drawn last (above the table); it is only ever shown half-way, clear of the pile.
  c=ORDER[moving];col,row=moving//2,moving%2
  s.card(c,lerp(COLX[col],PILE[1][0],.5),lerp(ROWY[row],PILE[1][1]+36,.5),PW,PH,back=face(moving,c))
 s.text(f'Pot: {counts[2]}',960,870,58,WHITE,True,True,'middle')
 if cap:caption(s,cap,960,36)
 return s.finish()

def end_svg():
 s=felt('Higher rank wins · Aces high')
 s.text('Win all 52 cards.',960,566,97,WHITE,True,anchor='middle')
 s.text('Tie? War.  ·  Won cards go to the bottom',960,724,45,PALE,anchor='middle')
 return s.finish()
def reset_svg():
 s=felt('Tie? War.');s.text('New example · 26 cards each',960,572,56,WHITE,anchor='middle');return s.finish()

# Cutdown frame lists, each relative to its own zero. The last state holds to the cutdown's duration.
def cut_deck():return [(0,deck_svg())]
def cut_deal():
 fs=[(0,deal_svg(0))]
 for k in range(1,53):
  n=18+(k-1)*3      # 0.6 s lead, then one card every 0.1 s: two flight frames, then landed
  fs+=[(fr(n),deal_svg(k,'a')),(fr(n+1),deal_svg(k,'b')),(fr(n+2),deal_svg(k))]
 return fs
def cut_round():
 fs=[(0,round_svg('rest')),(fr(24),round_svg('draw')),(fr(30),round_svg('down')),(fr(36),round_svg('flip')),(fr(57),round_svg('compare'))]
 fs+=[(fr(102+i*3),round_svg('collect',i)) for i in range(6)]
 fs.append((fr(120),round_svg('done')))
 return fs
def cut_war():
 burn='Three face-down each'
 fs=[(0,war_svg()),(fr(21),war_svg(0,flight=(0,.5))),(fr(26),war_svg(1)),(fr(30),war_svg(1,up0=True,cap='Same rank · tie'))]
 for i,n in enumerate((102,117,132)):
  fs+=[(fr(n-5),war_svg(1+i,up0=True,flight=(1+i,.5),cap=burn)),(fr(n),war_svg(2+i,up0=True,cap=burn))]
 fs+=[(fr(180),war_svg(4,up0=True,flight=(4,.5),cap=burn)),(fr(185),war_svg(5,up0=True)),(fr(189),war_svg(5,up0=True,up4=True,cap='Higher rank wins · Aces high'))]
 for n in range(10):
  f0=255+n*6
  fs+=[(fr(f0),war_svg(5,True,True,awarded=n,moving=n,cap='To Player 2’s bottom')),(fr(f0+3),war_svg(5,True,True,awarded=n+1,cap='To Player 2’s bottom'))]
 fs.append((fr(318),war_svg(5,True,True,awarded=10,cap='Won cards go to the bottom')))
 return fs
def cut_end():return [(0,end_svg())]

CUTDOWNS={ # name: (frames, duration s, key_second, what the key moment is, the narrated beat it serves)
 'deck-hold':(cut_deck,30,0.0,'still: the full squared deck at rest (loopable)','S05-B01'),
 'alternating-deal':(cut_deal,20,fr(18),'the first card leaves the deck for Player 1 (0.600 s); it lands at 0.667 s; the 52nd lands at 5.767 s; 26 / 26 holds from there','S05-B02 "Deal it evenly"'),
 'normal-round':(cut_round,16,fr(36),'A♠ and K♥ land face-up at the same instant (1.200 s); gold accent and "Ace beats King" at 1.900 s; the pair travels to Player 1\'s bottom 3.400–3.967 s; 27 / 25, pot 0 from 4.000 s','S05-B03 "Aces are high"'),
 'single-war':(cut_war,20,fr(30),'the tie 4♠ / 4♦ is face-up (1.000 s); burns land 3.400, 3.900, 4.400 s; the deciding 9♦ / A♦ flip at 6.300 s; the ten-card pot travels 8.500–10.400 s; 21 / 31, pot 0 with the closing caption from 10.600 s','S05-B04 "it\'s War"'),
 'final-hold':(cut_end,14,0.0,'still: the rank-only rule card, Win all 52 cards.','S05-B05'),
}
# The continuous version keeps every moment in order with shorter holds and a visible reset before the war example.
SEQUENCE=[('deck-hold',0),('alternating-deal',3),('normal-round',11),('reset',17),('single-war',18.5),('final-hold',31)]
DURATION=35
BEATS=['0–3 s: the full squared deck at rest (deck-hold).',
       '3–11 s: alternating deal, one card at a time from 3.6 s; 26 / 26 from 8.77 s (alternating-deal).',
       '11–17 s: A♠ and K♥ flip at 12.2 s; the pair travels to Player 1\'s bottom; 27 / 25 from 15 s (normal-round).',
       '17–18.5 s: visible reset to the independent single-war fixture, 26 cards each.',
       '18.5–31 s: the tie at 19.5 s, three face-down each by 22.9 s, the deciding flip at 24.8 s, the ten-card pot collected 27–28.9 s; 21 / 31 from 29.1 s (single-war).',
       '31–35 s: the rank-only rule card, Win all 52 cards. (final-hold).']

def write(path,text):path.write_text(text,encoding='utf-8',newline='\n')
def main():
 for old in list(HERE.glob('scene-*.svg'))+list(HERE.glob('variant-*.svg')):old.unlink()
 dedup={}
 def keep(svg):
  sha=hashlib.sha256(svg.encode()).hexdigest()
  if sha not in dedup:n=f'scene-{len(dedup):04}.svg';dedup[sha]=n;write(HERE/n,svg)
  return dedup[sha]
 cut_frames={name:[(t,keep(svg)) for t,svg in fn()] for name,(fn,*_) in CUTDOWNS.items()}
 reset=keep(reset_svg())
 frames=[]
 for name,offset in SEQUENCE:
  part=[(0,reset)] if name=='reset' else cut_frames[name]
  frames+=[{'time':offset+t,'file':f} for t,f in part]   # exact floats: rounding would shift frame-based times past a frame boundary
 assert all(frames[i]['time']<frames[i+1]['time'] for i in range(len(frames)-1)) and frames[-1]['time']<DURATION
 cutdowns={name:{'frames':[{'time':t,'file':f} for t,f in cut_frames[name]],'duration':dur,'key_second':key,'poster':f'variant-{name}.svg','key_moment':what,'serves':beat}
           for name,(fn,dur,key,what,beat) in CUTDOWNS.items()}
 compare=round_svg('compare');write(HERE/'scene.svg',compare)
 variants={'full-rules':compare,'deck-hold':deck_svg(),'alternating-deal':deal_svg(52),'normal-round':round_svg('done'),'single-war':war_svg(5,True,True,awarded=10,cap='Won cards go to the bottom'),'final-hold':end_svg()}
 vmap={}
 for name,svg in variants.items():write(HERE/f'variant-{name}.svg',svg);vmap[name]=f'variant-{name}.svg'
 notes=['Revision 2 (2026-09-16, review notes 9 and 11): re-authored as five named cutdowns (deck-hold, alternating-deal, normal-round, single-war, final-hold) that each start at their named moment and hold their end state; key_second per cutdown marks the moment for placement on the narrated word. Cards use the revised shared faces (win95-workbench-1.1.0).',
        'Shuffle is not animated here (DIA-15 carries the shuffle cue); the deck-hold is the squared deck at rest. Dealing is alternating, one card at a time, with 52 counted transfers.',
        'Normal-round and single-war scenes are independent supplied fixtures (tools/fixtures/war_storyboard.json); the continuous version shows a visible reset between them.',
        'All count states conserve 52; the win-all-52 closing caption is a rule, not an alleged conclusion of the short example. The insufficient-cards ending (R05) is not depicted.',
        'Captions "Ace beats King", "Same rank · tie", "Three face-down each", "Alternate one card at a time", "26 cards per player", "To Player 2’s bottom", "New example · 26 cards each" and the heading "52 cards" are authored production copy; the five ticket copy lines appear verbatim.']
 def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
 sources=[{'path':'../../../sources/ASSET_PLAN.md','lines':[17,17],'sha256':sha('sources/ASSET_PLAN.md'),'relationship':'source creative brief'},
          {'path':'../../../sources/SCRIPT.md','lines':[170,194],'sha256':sha('sources/SCRIPT.md'),'relationship':'source creative brief'},
          {'path':'../../../sources/SCRIPT.md','lines':[399,401],'sha256':sha('sources/SCRIPT.md'),'relationship':'source creative brief'},
          {'path':'../../../sources/Program.vb','lines':[136,152],'sha256':sha('sources/Program.vb'),'relationship':'literal excerpt'},
          {'path':'../../../sources/Program.vb','lines':[234,268],'sha256':sha('sources/Program.vb'),'relationship':'literal excerpt'},
          {'path':'../../../tools/fixtures/war_storyboard.json','lines':[1,1],'sha256':sha('tools/fixtures/war_storyboard.json'),'relationship':'deterministic teaching fixture (normal_round, single_war)'},
          {'path':'../../../review/cut-notes-2026-09-16.md','lines':[16,18],'sha256':sha('review/cut-notes-2026-09-16.md'),'relationship':"Devin's review notes 9 and 11 (revision 2 brief)"}]
 cuts={'full-rules':[0,DURATION]}
 timeline={'id':ID,'durationSeconds':DURATION,'fps':FPS,'width':1920,'height':1080,'beats':BEATS,'frames':frames,'cuts':cuts,'cutdowns':cutdowns,'variant_names':list(vmap),
           'motion_model':'Explicit deterministic step states with readable holds; MP4 encodes the same scene changes at 30 fps. Each cutdown is its own frame list starting at its named moment and holding its end state to its duration.'}
 write(HERE/'timeline.json',json.dumps(timeline,indent=2,ensure_ascii=False)+'\n')
 table={n:(HERE/n).read_text(encoding='utf-8') for n in dedup.values()}
 html_doc='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+html.escape(TITLE)+'''</title><style>html,body{margin:0;background:#000;height:100%;overflow:hidden}#stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center}svg{width:100%;height:100%;object-fit:contain}</style><div id="stage" aria-label="'''+html.escape(TITLE,quote=True)+'''"></div><script>const timeline='''+json.dumps(timeline,ensure_ascii=False)+''';const scenes='''+json.dumps(table,ensure_ascii=False)+''';const stage=document.getElementById('stage');window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;else break}stage.innerHTML=scenes[f.file];return f.file}};__ASSET__.renderAt(0);let start=null,playing=false;document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();playing=!playing;start=null;requestAnimationFrame(tick)}if(e.code==='Home'){playing=false;__ASSET__.renderAt(0)}});function tick(ts){if(!playing)return;if(start===null)start=ts;const t=(ts-start)/1000;__ASSET__.renderAt(t);if(t<__ASSET__.durationSeconds)requestAnimationFrame(tick);else playing=false}</script></html>'''
 write(HERE/'index.html',html_doc)
 build={'id':ID,'duration':DURATION,'frames':frames,'variants':vmap,'poster':'scene.svg','cuts':cuts,'cutdowns':cutdowns,'notes':notes,'sources':sources,'kind':'motion'}
 write(HERE/'build.json',json.dumps(build,indent=2,ensure_ascii=False)+'\n')
 print('AUTHORED',ID,len(dedup),'states',len(frames),'continuous frames',{n:len(c['frames']) for n,c in cutdowns.items()})
if __name__=='__main__':main()
