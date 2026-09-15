"""Individually composed algorithm explainers. All fixtures are teaching data."""
from __future__ import annotations
import math
from studio import *
from build_assets import ROOT, ROWS, WAR, SHUF, scene, simple

def event_svg(active=-1):
 s=SVG(BG,'Event-Driven Programming');s.heading('Event-Driven Programming')
 cols=[176,645,1302]
 for x,label in zip(cols,['Action','Handler','Response']):s.text(label,x,254,30,MUTED)
 for i,(action,handler,response) in enumerate([('Click','Command1_Click','You clicked me!'),('Type','Text-change handler','Hello'),('Resize','Resize handler','')]):
  y=305+i*211;col=BLUE if active in [-1,i] else LINE
  s.bevel(176,y+40,290, ninety:=90);s.text(action,321,y+98,38,'#111',True,anchor='middle')
  s.arrow(490,y+84,594,y+84,col,4)
  s.rect(616,y,582,174,PANEL,col,3)
  if i==0:
   for j,line in enumerate(['Sub Command1_Click()','    MsgBox "You clicked me!"','End Sub']):code_line(s,line,638,y+44+j*46,29,focus='MsgBox' if active==0 else None)
  else:s.text(handler,907,y+97,35,FG,True,anchor='middle')
  s.arrow(1220,y+84,1300,y+84,col,4)
  if i==0:
   s.window(1325,y+8,425,148,'',titleh=35);s.text(response,1537,y+106,31,'#111',anchor='middle')
  elif i==1:
   s.bevel(1325,y+39,425,91,'#fff',True);s.text(response if active in [-1,1] else '',1350,y+98,36,'#111')
  else:
   width_=425 if active in [-1,2] else 290;s.bevel(1325,y+22,width_,128);s.rect(1333,y+30,width_-16,28,NAVY)
 return s.finish()
def event():
 scene('DIA-01',12,[(0,event_svg(3)),(2,event_svg(0)),(6,event_svg(1)),(8,event_svg(2)),(10,event_svg(-1))],{'overview':event_svg(-1),'click-handler':event_svg(0)},event_svg(-1),notes=['Original GUI concept illustration. Type and Resize use descriptive handler labels rather than fabricated classic-VB identifiers.','Click handler is verbatim SCRIPT.md; these forms do not exist in Program.vb.'])

def rankchart():
 s=SVG(BG,'Card → Stored rank');s.heading('Card → Stored rank')
 ranks=[str(x) for x in range(2,11)]+['J','Q','K','A']
 for i,rank in enumerate(ranks):
  row=0 if i<7 else 1;col=i if i<7 else i-7;n=7 if row==0 else 6
  x=120+(1680-n*176-(n-1)*53)/2+col*229;y=239+row*339
  s.card(rank+'S',x+25,y,126,179,accent=GOLD if rank=='A' else None)
  s.arrow(x+88,y+192,x+88,y+218,GOLD if rank=='A' else MUTED,2)
  s.text(str(i+2),x+88,y+270,49,GOLD if rank=='A' else FG,True,True,'middle')
 s.text('Suits do not decide the winner.',960,983,34,MUTED,anchor='middle')
 simple('DIA-03',s.finish())

def byref_svg(phase=0):
 s=SVG(BG,'Integer example: ByRef / ByVal');s.heading('ByRef versus ByVal','Integer example')
 for col,label in enumerate(['ByRef','ByVal']):
  x=120+870*col;s.rect(x,274,810,599,PANEL);s.text(label,x+44,359,64,BLUE,True,mono=True)
  s.text('Caller',x+58,470,31,MUTED);s.text('Parameter',x+467,470,31,MUTED)
  left=9 if col==0 and phase>=1 else 7;right=9 if (col==0 and phase>=1) or phase>=2 else 7
  s.rect(x+43,509,275,144,'#111820',BLUE,2);s.rect(x+454,509,310,144,'#111820',BLUE,2)
  s.text(f'x = {left}',x+180,602,51,FG,True,True,'middle');s.text(f'p = {right}',x+609,602,51,FG,True,True,'middle')
  if col==0:
   s.arrow(x+444,581,x+335,581,BLUE,4);s.text('Same variable',x+405,744,35,FG,anchor='middle')
  else:
   s.arrow(x+329,581,x+436,581,GOLD,4);s.text('Value copied into p',x+405,744,35,FG,anchor='middle')
  s.text('Caller changes to 9' if col==0 else 'Caller stays 7',x+405,818,34,GOLD if phase==2 else MUTED,anchor='middle')
 return s.finish()
def byref():
 scene('DIA-04',12,[(0,byref_svg()),(4,byref_svg(1)),(8,byref_svg(2))],{},byref_svg(2),notes=['Scoped authored Integer example only; no claim of automatic deep copying for arrays.','No .NET SDK is installed; the separate VB validation harness requested by R04a was not executed. This is a produced internal proof, not a closed semantic gate.'])

def queue_svg(step=0):
 s=SVG(BG,'Arrays as queues');s.heading('Arrays as queues')
 if step==0:
  s.text('Capacity: 52',120,266,38,FG,True)
  x0=126;cell=25;gap=7
  for i in range(52):s.rect(x0+i*(cell+gap),472,cell,108,BLUE if i<4 else PANEL,BLUE if i<4 else LINE,2)
  for i in [0,3,4,51]:s.text(str(i),x0+i*32+12,634,28,MUTED,mono=True,anchor='middle')
  boundary=x0+4*32-3;s.line(boundary,404,boundary,653,GOLD,3);s.text('Count = 4',max(160,boundary),354,46,GOLD,mono=True,anchor='middle')
  s.text('Live: 0 … Count − 1',120,764,37,FG);s.text('Inactive: Count … 51',990,764,37,MUTED)
  s.text('Cards(0): next to draw',120,940,36,FG)
  return s.finish()
 vals=['2S','5H','9D','KC',None,None];count=4
 # Save top, then perform exactly the three increasing-i assignments.
 if step>=2:vals[0]='5H'
 if step>=3:vals[1]='9D'
 if step>=4:vals[2]='KC'
 if step>=5:count=3
 if step>=6:vals[3]='AS'
 if step>=7:count=4
 s.text('Cards(0): next to draw',120,247,33,MUTED)
 s.text(f'Count = {count}',1780,245,46,GOLD,mono=True,anchor='end')
 x0=145;pitch=259;y=471
 for i,value in enumerate(vals):
  x=x0+i*pitch;s.rect(x,y,220,252,PANEL,BLUE if i<count else LINE,2)
  s.text(str(i),x+110,y+301,34,MUTED,mono=True,anchor='middle')
  if value:s.card(value,x+40,y+29,140,196,opacity=1 if i<count else .25)
 if step>=1:
  s.text('Saved top card' if step<6 else 'Returned card',1375,300,29,MUTED);s.card('2S',1585,285,90,126)
 if step in [2,3,4]:
  index=step-1;x_from=x0+index*pitch+110;x_to=x_from-pitch
  s.arrow(x_from,445,x_to,445,GOLD,4)
  s.text(f'H.Cards({index-1}) = H.Cards({index})',120,352,37,GOLD,mono=True)
 elif step==1:s.text('Top = H.Cards(0)',120,353,40,GOLD,mono=True)
 elif step==5:s.text('H.Count = H.Count - 1',120,353,37,GOLD,mono=True)
 elif step==6:s.text('H.Cards(H.Count) = C',120,353,37,GOLD,mono=True)
 else:s.text('H.Count = H.Count + 1',120,353,37,GOLD,mono=True)
 boundary=x0+count*pitch-20;s.line(boundary,829,boundary,886,GOLD,3);s.text('Live boundary',boundary,932,32,GOLD,anchor='middle')
 if step in [5,6]:s.text('Inactive slot',x0+3*pitch+110,832,27,MUTED,anchor='middle')
 return s.finish()
def queue():
 fs=[(0,queue_svg(0)),(3,queue_svg(1)),(6,queue_svg(2)),(7.5,queue_svg(3)),(9,queue_svg(4)),(11,queue_svg(5)),(14,queue_svg(6)),(16,queue_svg(7))]
 scene('DIA-05',18,fs,{'52-slot-overview':fs[0][1],'draw-and-shift':fs[3][1],'append-at-count':fs[-1][1]},fs[3][1],notes=['Authored queue demonstration with exact assignment order. Temporary duplicate memory values during copying are intentional; Count distinguishes the live range from stale storage.'])

def shuffle_svg(step=-1,after=False,real=False):
 s=SVG(BG,'Fisher–Yates shuffle');s.heading('Fisher–Yates shuffle','Small example: 8 cards')
 data=SHUF['swaps'][step] if step>=0 else None;order=data['after'] if after and data else data['before'] if data else SHUF['initial']
 if real:order=SHUF['final']
 i=data['i'] if data else 7;j=data['j'] if data else None
 x0=127;pitch=211
 for idx,c in enumerate(order):
  x=x0+idx*pitch;fixed=(idx>i or (after and idx==i)) if data else False
  s.card(c,x+17,383,151,212,accent=GOLD if data and idx==j and not after else BLUE if data and idx==i else None)
  s.text(str(idx),x+92,651,34,MUTED,mono=True,anchor='middle')
  if fixed or real:s.line(x+17,691,x+168,691,GREEN,5)
 if not real:
  s.line(x0+20,317,x0+i*pitch+166,317,BLUE,3);s.text(f'j ∈ 0 … {i}',x0+15,284,34,BLUE,mono=True)
  if data:
   s.text(f'i = {i}    j = {j}',120,794,44,FG,mono=True)
   s.rect(752,738,449,95,PANEL);s.text('Temp = '+data['before'][i],974,801,37,GOLD,mono=True,anchor='middle')
   s.text('Self-swap: unchanged' if i==j else ('Swap complete' if after else 'Save Deck(i) in Temp'),1265,795,32,MUTED)
  s.text('Choose j from 0 through i',120,974,34,FG);s.text('Fixed suffix',1770,976,31,GREEN,anchor='end')
 else:
  code_line(s,'For i = 51 To 1 Step -1',120,812,45,focus='Step -1');code_line(s,'    j = Rnd.Next(0, i + 1)',120,879,42,focus='i + 1')
  s.text('Real deck: i = 51 down to 1',120,977,34,MUTED)
 return s.finish()
def shuffle():
 fs=[(0,shuffle_svg())]
 # Seven saved swaps, including both allowed self-swaps.
 for n in range(7):
  st=3+n*(12/7);fs += [(st,shuffle_svg(n)),(st+.82,shuffle_svg(n,True))]
 fs += [(15,shuffle_svg(6,True)),(18,shuffle_svg(6,True,True))]
 scene('DIA-06',21,fs,{'miniature-trace':shuffle_svg(0),'real-code-bounds':shuffle_svg(6,True,True)},shuffle_svg(0),notes=['All seven swaps come from the supplied deterministic miniature fixture. This is not randomness testing, a benchmark, or a captured program run.','Historical 1938 wording is omitted; R15 remains visible in metadata.'])

def grid_svg(n=0,close=False):
 s=SVG(BG,'Building the deck');s.heading('Building the deck')
 if close:
  s.text('Rank = 2',120,275,47,GOLD,mono=True)
  for i,suit in enumerate(['S','H','D','C']):
   x=291+i*360;s.card('2'+suit,x,365,186,260);s.text(f'Index = {i}',x+93,722,36,FG,mono=True,anchor='middle');s.text(f'SuitIndex = {i}',x+93,800,30,MUTED,mono=True,anchor='middle')
  s.text('The inner loop walks all four suits.',120,976,35,MUTED)
  return s.finish()
 # Code scaffolding on the left; the right side is a literal rank-major matrix.
 lines=['For Rank = 2 To 14','    For SuitIndex = 0 To 3','        Index = Index + 1','    Next SuitIndex','Next Rank']
 for j,line in enumerate(lines):code_line(s,line,122,351+j*64,37,focus='Next SuitIndex' if n==52 else None)
 current=min(n,51);rank=2+current//4;si=current%4
 s.text('Next card to fill' if n<52 else 'Last card filled',120,704,30,MUTED)
 s.text(f'Rank      {rank if n<52 else 14}',120,778,42,FG,mono=True);s.text(f'SuitIndex {si if n<52 else 3}',120,842,42,FG,mono=True);s.text(f'Index     {n}',120,918,54,GOLD,mono=True)
 x0=1180;y0=286;cw=134;rh=45
 for col,su in enumerate(['S ♠','H ♥','D ♦','C ♣']):s.text(su,x0+col*cw+59,250,33,FG,anchor='middle')
 for row in range(13):
  label=str(row+2) if row<9 else ['J','Q','K','A'][row-9];s.text(label,x0-44,y0+row*rh+31,29,MUTED,mono=True,anchor='middle')
  for col in range(4):
   idx=row*4+col;fill='#244237' if idx<n else PANEL
   s.rect(x0+col*cw,y0+row*rh,cw-10,rh-7,fill,GOLD if idx==n-1 else LINE,2)
   if idx<n:s.text(str(idx),x0+col*cw+62,y0+row*rh+28,26,FG,mono=True,anchor='middle')
 s.text('52 cards = 13 ranks × 4 suits',1170,965,34,FG,anchor='middle')
 return s.finish()
def grid():
 fs=[(0,grid_svg(0))]
 for n in range(1,53):
  t=3+(n-1)*1.25 if n<=4 else 8+(n-5)*(6/43) if n<=48 else 14+(n-49)*.65
  fs.append((t,grid_svg(n)))
 scene('DIA-07',18,fs,{'full-grid':grid_svg(52),'first-rank-closeup':grid_svg(4,True)},grid_svg(52),notes=['Grid cells show the Deck array index, not a shuffled order.','Rank-major order is S,H,D,C within each rank. Final populated index is 51, followed by Index = 52.'])

def war_board(kind='single',stage=0,awarded=0,moving=None,caption=None,milestones=False):
 fixture=WAR['single_war' if kind=='single' else 'double_war'];ev=fixture['events']
 # stage means number of fixture add events already shown; final award uses a prefix of stored order.
 maxstage=3 if kind=='single' else 5
 stage=min(stage,maxstage)
 allcards=[];backs=[]
 for event in ev[:stage]:
  for c in event.get('cards',[]):allcards.append(c);backs.append(event['action']=='burn_pairs')
 perplayer=len(allcards)//2;counts=[26-perplayer,26-perplayer+awarded,len(allcards)-awarded]
 s=SVG(FELT,'War: tie, burn, flip, collect');s.rect(0,0,1920,1080,'url(#felt)')
 title='The pot grows with every tie' if kind=='double' else 'Tie. Burn. Flip. Collect.'
 s.heading(title)
 s.text('Player 1',252,291,38,'#eff4ee',True,anchor='middle');s.text('Player 2',1668,291,38,'#eff4ee',True,anchor='middle')
 for x in [178,1592]:
  for k in range(3):s.card('AS',x+k*4,383-k*5,143,201,back=True)
 s.text(str(counts[0]),252,678,76,'#fff',True,mono=True,anchor='middle');s.text(str(counts[1]),1668,678,76,'#fff',True,mono=True,anchor='middle');s.text('cards',252,723,29,'#b9dac3',anchor='middle');s.text('cards',1668,723,29,'#b9dac3',anchor='middle')
 s.rect(424,286,1072,533,'none','#68a07b',2,rx=8)
 # Each column is one pair in play order, with P1 contributions above P2.
 ncols=5 if kind=='single' else 9;cw=146 if kind=='single' else 96;cardw=117 if kind=='single' else 78;cardh=162 if kind=='single' else 111;x0=960-(ncols*cw)/2+15
 s.text('Player 1',448,335,26,'#bed5c5');s.text('Player 2',448,774,26,'#bed5c5')
 positions=[]
 for idx,c in enumerate(allcards):
  x=x0+(idx//2)*cw;y=375+(idx%2)*225;positions.append((x,y))
  if idx<awarded:continue
  if moving and idx==awarded:
   q=moving;x=x+(1592-x)*q;y=y+(617-y)*q
  s.card(c,x,y,cardw,cardh,back=backs[idx])
 s.text(f'Pot: {counts[2]}',960,896,58,'#fff',True,mono=True,anchor='middle')
 if awarded or moving:s.text('To Player 2’s bottom',960,958,31,'#e1d7aa',anchor='middle');s.arrow(1515,783,1603,652,'#e1d7aa',3)
 elif caption:s.text(caption,960,976,36,'#e9efea',anchor='middle')
 if kind=='double':
  for i,label in enumerate(['2','10','18']):
   active=(counts[2]==int(label));s.text(label,786+174*i,231,56,'#f4d399' if active else '#a3c5ad',True,mono=True,anchor='middle')
  s.arrow(828,214,900,214,'#a3c5ad',2);s.arrow(1001,214,1074,214,'#a3c5ad',2)
 return s.finish()

def four_panel():
 s=SVG(BG,'War in four steps');s.heading('War in four steps')
 heads=['1. Tie','2. Three face-down each','3. One face-up each','4. Higher rank takes the pot']
 for i,title in enumerate(heads):
  x=120+432*i;s.rect(x,267,384,599,PANEL);s.lines(wrap(title,335,34,'bold'),x+24,326,34,FG,True,leading=1.14)
  if i<3:
   cards=[['4S','4D'],['4S','4D','5S','5H','6S','6H','7S','7H'],['4S','4D','5S','5H','6S','6H','7S','7H','9D','AD']][i]
   for k,c in enumerate(cards):
    col=k//2;row=k%2;xx=x+25+col*66;yy=461+row*138;s.card(c,xx,yy,57,80,back=k in range(2,8))
   s.text(f'Pot: {[2,8,10][i]}',x+24,815,38,GOLD,True,mono=True)
  else:
   s.card('AD',x+128,464,128,180);s.text('Player 2',x+192,740,37,FG,True,anchor='middle');s.text('21 / 31 · pot 0',x+192,814,29,GOLD,mono=True,anchor='middle')
 s.text('The deciding pair is additional to the six burns.',120,980,35,MUTED)
 return s.finish()

def war_motion_frames():
 fs=[(0,war_board(stage=1,caption='Two equal ranks. Pot: 2.')),(3,war_board(stage=2,caption='Three face-down each. Pot: 8.')),(6,war_board(stage=3,caption='9♦ versus A♦. Pot: 10.'))]
 # Each card appends in exact P1/P2 play order; counters move only on arrival.
 for n in range(10):
  t=9+n*.22
  fs.append((t,war_board(stage=3,awarded=n,moving=.45)))
  fs.append((t+.11,war_board(stage=3,awarded=n+1)))
 fs.append((11.4,war_board(stage=3,awarded=10)))
 return fs

def war_mechanic():
 fs=war_motion_frames();scene('DIA-08',12,fs,{'four-panel-poster':four_panel(),'single-war-motion':war_board(stage=3),'award-to-bottom':war_board(stage=3,awarded=5,moving=.45)},four_panel(),cuts={'single-war-motion':[0,12],'award-to-bottom':[8,12]},notes=['Uses the supplied single-war fixture; burns conceal their faces. This is not an actual Program.vb run.','The ten-card award moves individually in stored play order. The final counts are 21 / 31 / pot 0.','No insufficient-card case or recursive function is illustrated.'])

def normal_svg(phase=0):
 s=SVG(FELT,'Higher rank wins');s.rect(0,0,1920,1080,'url(#felt)');s.heading('Higher rank wins','Aces high')
 count=[26,26,0] if phase==0 else [25,25,2] if phase==1 else [27,25,0]
 for i,x in enumerate([205,1535]):
  s.text(f'Player {i+1}',x+76,320,37,'#fff',True,anchor='middle');s.card('AS',x,397,152,215,back=True);s.text(str(count[i]),x+76,722,67,'#fff',True,mono=True,anchor='middle')
 if phase==1:
  s.card('AS',733,397,170,239,accent=GOLD);s.card('KH',1016,397,170,239);s.text('14',818,748,48,'#fff',mono=True,anchor='middle');s.text('>',960,526,61,'#fff',True,anchor='middle');s.text('13',1101,748,48,'#fff',mono=True,anchor='middle')
 elif phase==2:
  s.arrow(990,530,438,630,GOLD,5);s.text('Won cards go to the bottom',960,847,42,'#fff',anchor='middle')
 s.text(f'Pot: {count[2]}',960,966,39,'#fff',mono=True,anchor='middle')
 return s.finish()

def deal_svg(k=0,shuffling=False,final=False):
 s=SVG(FELT,'52 cards · 26 each');s.rect(0,0,1920,1080,'url(#felt)');s.heading('52 cards · 26 each')
 p1=(k+1)//2;p2=k//2;remaining=52-k
 for i,x in enumerate([215,1535]):
  s.text(f'Player {i+1}',x+76,324,37,'#fff',True,anchor='middle')
  if [p1,p2][i]:s.card('AS',x,414,152,213,back=True)
  else:s.rect(x,414,152,213,'none','#7aaa87',2,rx=6)
  s.text(str([p1,p2][i]),x+76,760,77,'#fff',True,mono=True,anchor='middle')
 if remaining:
  for j in range(4):s.card('AS',884+(j*18 if shuffling else j*4),414-j*5,152,213,back=True)
 s.text(f'Deck: {remaining}',960,766,51,'#fff',mono=True,anchor='middle')
 if k>0 and k<52:
  to=430 if k%2 else 1500;s.arrow(830 if k%2 else 1090,537,to,537,'#d8dcb4',3)
 s.text('Shuffle' if shuffling else 'Alternate one card at a time' if k<52 else '26 cards per player',960,956,38,'#fff',anchor='middle')
 return s.finish()
def full_rules():
 fs=[(0,deal_svg()),(1,deal_svg(shuffling=True)),(3,deal_svg())]
 fs += [(4+k*(5/52),deal_svg(k)) for k in range(1,53)]
 fs += [(10,normal_svg()),(11,normal_svg(1)),(14,normal_svg(2))]
 # A visible reset into the independent fixture avoids pretending it continues the A/K round.
 reset=SVG(FELT,'New example');reset.heading('Tie? War.');reset.text('New example · 26 cards each',960,572,56,'#fff',anchor='middle')
 fs.append((16,reset.finish()));fs.append((17,war_board(stage=1)));fs.append((19,war_board(stage=2)));fs.append((22,war_board(stage=3)))
 for n in range(10):fs.append((24+n*.18,war_board(stage=3,awarded=n+1)))
 end=SVG(FELT,'Win all 52 cards');end.heading('Higher rank wins · Aces high');end.text('Win all 52 cards.',960,566,97,'#fff',True,anchor='middle');end.text('Won cards go to the bottom',960,724,45,'#dfebdf',anchor='middle')
 fs.append((26,end.finish()))
 scene('DIA-02',28,fs,{'full-rules':normal_svg(1),'alternating-deal':deal_svg(52),'normal-round':normal_svg(1),'single-war':war_board(stage=3)},normal_svg(1),cuts={'full-rules':[0,28],'alternating-deal':[3,10],'normal-round':[10,16],'single-war':[16,28]},notes=['Shuffle is an abstraction; dealing is alternating, one card at a time, with 52 counted transfers.','Normal-round and single-war scenes reset to independent supplied fixtures.','All count states conserve 52; the win-all-52 closing caption is a rule, not an alleged conclusion of the short example.'])

def pot_poster():
 s=SVG(BG,'2 → 10 → 18');s.heading('Every full war adds eight cards')
 for i,(label,n) in enumerate([('Normal round',2),('One war',10),('Double war',18)]):
  x=145+i*581;s.text(label,x,321,38,MUTED);s.text(str(n),x,528,156,GOLD if n==18 else FG,True,mono=True)
  for k in range(n):s.rect(x+(k%6)*59,600+(k//6)*70,46,58,BLUE if k<2 else '#455d76')
  if i<2:s.arrow(x+368,454,x+471,454,MUTED,4)
 s.text('One original pair + 8 per fully supplied war',120,969,36,MUTED)
 return s.finish()
def pot():
 fs=[(0,war_board('double',1,caption='Initial pair: 2')),(3,war_board('double',2,caption='+6 face-down: 8')),(5,war_board('double',3,caption='+2 face-up: 10. Tie again.')),(7,war_board('double',4,caption='+6 face-down: 16')),(9,war_board('double',5,caption='+2 face-up: 18'))]
 for n in range(18):fs.append((11.4+n*.12,war_board('double',5,awarded=n+1)))
 fs.append((13.7,war_board('double',5,awarded=18)))
 scene('DIA-09',15,fs,{'2-10-18-poster':pot_poster(),'double-war-growth':war_board('double',5)},pot_poster(),notes=['The double-war fixture produces live pot milestones 2, 8, 10, 16, 18 and final counts 17 / 35 / 0.','104 is allocation capacity in the supplied code, not the size of the physical deck. No 104-card graphic is used.'])

def flow_box(s,text,x,y,w=450,h=84,accent=BLUE):
 s.rect(x,y,w,h,PANEL,accent,2,rx=2)
 ls=wrap(text,w-36,32,'sans');s.lines(ls,x+w/2,y+h/2-(len(ls)-1)*19+11,32,FG,leading=1.18,anchor='middle')
def main_flow():
 s=SVG(BG,'Game flow');s.heading('The game loop')
 for i,label in enumerate(['Build','Shuffle','New hands','Deal']):
  x=120+i*441;flow_box(s,label,x,246,357,88)
  if i<3:s.arrow(x+365,290,x+424,290,BLUE,3)
 s.path('M1621 346V386H960V426',BLUE,3);s.arrow(960,410,960,429,BLUE)
 flow_box(s,'Both have cards?',735,445,450,88)
 s.arrow(1198,489,1398,489,MUTED);s.text('No',1300,466,29,MUTED,anchor='middle');flow_box(s,'Check counts → winner',1417,444,383,92)
 s.arrow(960,547,960,598,BLUE);s.text('Yes',990,584,29,BLUE)
 flow_box(s,'RoundNumber += 1',735,614,450,85)
 s.arrow(960,711,960,755,BLUE)
 flow_box(s,'Above 20,000?',735,773,450,88,accent=GOLD)
 s.arrow(1198,817,1411,817,GOLD);s.text('Yes',1300,790,29,GOLD,anchor='middle');flow_box(s,'Draw',1430,773,370,88,accent=GOLD)
 s.arrow(725,817,604,817,BLUE);s.text('No',665,789,29,BLUE,anchor='middle');flow_box(s,'Play round',180,773,412,88)
 s.path('M180 817H134V489H723',BLUE,3);s.arrow(707,489,723,489,BLUE)
 s.text('The cap is a safety limit, not a saved-state cycle detector.',120,980,32,MUTED)
 return s.finish()
def detail_flow():
 s=SVG(BG,'PlayRound: the inner loop');s.heading('PlayRound: the inner loop')
 stages=[('Player 1 empty?',246),('Player 2 empty?',382),('Draw pair → append to pot',518),('Compare ranks',654),('Tie → burn equal counts',790)]
 for text,y in stages:flow_box(s,text,404,y,780,82,accent=GOLD if y==790 else BLUE)
 for y in [328,464,600,736]:s.arrow(795,y+9,795,y+40,BLUE)
 for y,label in [(246,'Player 2 takes pot'),(382,'Player 1 takes pot'),(654,'Higher rank takes pot')]:
  s.arrow(1199,y+41,1377,y+41,GOLD);s.text('Yes' if y!=654 else 'Unequal',1285,y+17,27,GOLD,anchor='middle');flow_box(s,label,1394,y,405,82,accent=GOLD)
 for y in [360,496]:s.text('No',825,y,27,BLUE)
 s.path('M404 831H194V287H392',BLUE,3);s.arrow(375,287,392,287,BLUE)
 s.text('Repeat Do…Loop',200,968,35,MUTED);s.text('Award → Exit Sub',1440,968,33,GOLD)
 return s.finish()
def flows():
 simple('DIA-10',main_flow(),{'main-flow':main_flow(),'playround-detail':detail_flow()},notes=['Overview and inner-loop detail are separate readable diagrams.','The main graphic abbreviates the source increment as RoundNumber += 1 in prose only; it is not presented as a literal VB line.','Source behavior retained: first empty-hand guard, second guard, draw, compare, tie/burn, repeat. R04/R05/R06 remain editorial gates.'])

def build_diagrams():
 event();rankchart();byref();queue();shuffle();grid();war_mechanic();full_rules();pot();flows()
