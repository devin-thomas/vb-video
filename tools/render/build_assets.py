#!/usr/bin/env python3
"""Build separate deterministic scenes, evidence, and edit metadata per ticket.
Run from any directory: python shared/build_assets.py [--id CODE-02]
"""
from __future__ import annotations
import sys
if __name__ == '__main__': sys.modules['build_assets'] = sys.modules[__name__]
import argparse, bisect, hashlib, html, json, math, re, shutil, textwrap
from pathlib import Path
from studio import *
ROOT=Path(__file__).resolve().parents[2]
MAN=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8')); ROWS={r['id']:r for r in MAN['tickets']}
PROGRAM=(ROOT/'sources/Program.vb').read_text(encoding='utf-8').splitlines()
WAR=json.loads((ROOT/'tools/fixtures/war_storyboard.json').read_text(encoding='utf-8'));SHUF=json.loads((ROOT/'tools/fixtures/shuffle_storyboard.json').read_text(encoding='utf-8'))
VERSION='win95-workbench-1.1.0'
REGISTRY={}
def scene(id,duration,frames,variants,poster=None,notes=None,cuts=None,source_text=None,files=None):
 """frames: sorted (seconds, SVG) pairs. This explicit timeline is seekable and offline.
 files: extra editable sources written to src/, as text or JSON-serializable data."""
 REGISTRY[id]={'id':id,'duration':duration,'frames':frames,'variants':variants,'poster':poster if poster is not None else frames[-1][1], 'notes':notes or [],'cuts':cuts or {},'source_text':source_text,'files':files or {}}
def simple(id,svg,variants=None,notes=None,files=None):
 scene(id,None,[(0,svg)],variants or {v:svg for v in ROWS[id]['variants']},notes=notes,files=files)

def chapter_svg(id,state='hold'):
 r=ROWS[id];number,title=r['copy'].split('\n',1);s=SVG(TEAL,title)
 if state=='blank':return s.finish()
 x,y,w,h=236,238,1448,604
 s.window(x,y,w,h,number)
 s.text(number,x+64,y+228,126,'#777',True)
 ls=wrap(title,1110,68,'bold');s.lines(ls,x+258,y+228,68,'#151515',True,leading=1.15)
 # A system separator, not a second slogan.
 s.line(x+64,y+h-84,x+w-64,y+h-84,'#858585',2);s.line(x+64,y+h-82,x+w-64,y+h-82,'#eee',2)
 return s.finish()

def chapters():
 for id in [f'CH-{n:02}' for n in range(1,17)]:
  hold=chapter_svg(id);blank=chapter_svg(id,'blank')
  scene(id,4,[(0,blank),(.2,hold),(3.9,hold)],{v:hold for v in ROWS[id]['variants']},poster=hold)

def title_card(pressed=False,cursor=False,blank=False):
 s=SVG(TEAL,ROWS['CARD-01']['title'])
 if blank:return s.finish()
 s.window(222,220,1476,632,'')
 # Original, minimal message-box icon: a stack of playing cards.
 s.card('AS',284,355,108,154);s.card('4H',326,383,108,154)
 s.lines(["I Wrote a Card Game in", "1995's Most Controversial",'Programming Language'],490,397,66,'#111',True,leading=1.17)
 s.button('OK',799,724,322,70,pressed)
 if cursor:s.cursor(1022,pressed and 768 or 780)
 return s.finish()
def end_card(blank=False):
 s=SVG('#06080a','Subscribe / Like / Next video')
 if blank:return s.finish()
 s.window(146,214,1628,664,'')
 s.circle(473,481,107,'#008080');s.circle(473,481,89,'none','#a5d0cb',2)
 s.text('Subscribe',473,661,52,'#111',True,anchor='middle');s.button('Like',370,700,206,62)
 # The placeholder is a clean unfilled picture area, not an invented thumbnail.
 s.bevel(820,336,798,449,'#151a20',pressed=True)
 s.text('Next video',1219,818,38,'#111',anchor='middle')
 return s.finish()
def cards():
 hold=title_card();scene('CARD-01',7,[(0,title_card(blank=True)),(.45,hold),(5,title_card(cursor=True)),(5.45,title_card(True,True)),(5.75,title_card(False,True)),(6.1,title_card(blank=True))],{'title-hold':hold,'ok-click':title_card(True,True)},hold)
 end=end_card();scene('CARD-02',12,[(0,end_card(True)),(.6,end)],{v:end for v in ROWS['CARD-02']['variants']},end,notes=['The reserved next-video rectangle and subscribe circle are not functional YouTube controls. No destination, thumbnail or channel identity has been invented.'])

def code_layout(r):
 lines=r['copy'].splitlines();count=len(lines);maxlen=max(map(len,lines));num=int(r['id'].split('-')[1]) if r['id'].startswith('CODE') else 0
 size=46 if count<=4 and maxlen*width('0',46,'mono')<=1490 else 34
 if count>=14:size=32
 # Keep source indentation; long lines soft-wrap visually without mutating the excerpt.
 maxchars=int(1506/width('0',size,'mono'))
 visual=[]
 for i,line in enumerate(lines):
  remaining=line;first=True
  if not remaining:visual.append((i,'',True));continue
  while len(remaining)>maxchars:
   cut=maxchars
   spaces=[m.start() for m in re.finditer(' ',remaining[:maxchars+1]) if m.start()>maxchars*.58]
   if spaces:cut=spaces[-1]+1
   visual.append((i,remaining[:cut],first));remaining=remaining[cut:];first=False
  visual.append((i,remaining,first))
 cap=int(670/(size*1.27));pages=[visual[i:i+cap] for i in range(0,len(visual),cap)]
 return size,pages

def code_svg(r,focus=None,page=0):
 size,pages=code_layout(r);rows=pages[min(page,len(pages)-1)];s=SVG(BG,r['title'])
 # A real source filename and language, not a fabricated editor screenshot.
 s.text('Program.vb' if r['id'].startswith('CODE') else 'Button-click event handler',120,117,32,MUTED,mono=True)
 s.text('VB.NET' if r['id'].startswith('CODE') else 'Classic VB',1800,117,28,BLUE,anchor='end')
 s.line(120,147,1800,147,LINE,2)
 title=r['title'];s.text(title,120,210,46,FG,True)
 s.rect(120,247,1680,673,'#151a20');s.rect(120,247,5,673,BLUE)
 actual_refs=[a for a in r['refs'] if a[0]=='Program.vb'];lo=actual_refs[0][1] if actual_refs else 1
 content_h=len(rows)*size*1.27;yy=282+max(0,(605-content_h)/2)+size
 targets=[]
 offsets={}
 for previous in pages[:page]:
  for ii,ll,_ in previous:offsets[ii]=offsets.get(ii,0)+len(ll)
 originals=r['copy'].splitlines()
 for visual_i,(i,line,first) in enumerate(rows):
  y=yy+visual_i*size*1.27
  if first:s.text(str(lo+i),163,y,25,'#748293',mono=True,anchor='middle')
  else:s.text('↪',163,y,25,'#748293',mono=True,anchor='middle')
  offset=offsets.get(i,0);offsets[i]=offset+len(line)
  if focus and focus not in line and focus in originals[i]:
   start=originals[i].index(focus);left=max(start,offset);right=min(start+len(focus),offset+len(line))
   if right>left:
    cw=width('0',size,'mono');s.rect(207+(left-offset)*cw-3,y-size-2,(right-left)*cw+6,size+10,'#263c58',rx=2)
  code_line(s,line,207,y,size,focus=focus)
  if focus and focus in line:targets.append((207+width(line[:line.index(focus)],size,'mono'),y))
 if len(pages)>1:s.text(f'{page+1} / {len(pages)}',1768,899,26,MUTED,mono=True,anchor='end')
 # Individually authored annotation layer, never part of the source text.
 note=None
 id=r['id']
 if focus:
  specific={
   'CODE-01': {'Option Explicit On':'Declare variables.','Option Strict On':'Keep conversions explicit.'},
   'CODE-02': {'Structure Card':'One card. Two fields.','Rank As Integer':'Rank → comparison','Suit As Char':'Suit → printed name','Dim':'Dimension?'},
   'CODE-04': {'For Rank':'Outer loop: Rank','For SuitIndex':'Inner loop: SuitIndex','Next SuitIndex':'Closes the inner loop','Next Rank':'Closes the outer loop'},
   'CODE-06': {'Cards() As Card':'Array reference → card storage','Count As Integer':'Count → live boundary'},
   'CODE-07': {'ReDim H.Cards(HAND_CAPACITY - 1)':'52 slots · indices 0–51','H.Count = 0':'An empty hand.','NewHand = H':'Return the initialized hand.'},
   'CODE-08': {'H.Cards(H.Count) = C':'Write at Count first.','H.Count = H.Count + 1':'Then extend the live range.'},
   'CODE-09': {'Top = H.Cards(0)':'Save the top card.','H.Cards(i - 1) = H.Cards(i)':'Shift the live cards left.','H.Count = H.Count - 1':'The stale tail is now inactive.','DrawTopCard = Top':'Return the saved card.'},
   'CODE-10': {'DrawTopCard = Top':'wait, what?'},
   'CODE-14': {'RoundNumber > MAX_ROUNDS':'Round cap, not a saved-state cycle detector.','calling it a draw (deck cycle detected).':'Source message retained; the implementation checks a cap.','Exit Do':'Exit the outer loop.'},
   'CODE-15': {'ByVal RoundNumber':'Read: round number','ByRef Player1':'Update: Player 1','ByRef Player2':'Update: Player 2','ByRef WarCount':'Update: war count','_':'The signature continues on the next line.'},
   'CODE-16': {'Pot(HAND_CAPACITY * 2 - 1)':'104 allocated slots ≠ 104 physical cards','PotCount As Integer':'PotCount tracks live cards.'},
   'CODE-17': {'If Player1.Count = 0 Then':'Player 1 is checked first.','If Player2.Count = 0 Then':'Player 2 is checked second.'},
   'CODE-19': {'Card1.Rank > Card2.Rank':'Compare ranks, not suits.','Card2.Rank > Card1.Rank':'The other winning branch.'},
   'CODE-20': {'Math.Min(3, Math.Min(Player1.Count, Player2.Count))':'One shared BurnCount for both players.'},
   'CODE-21': {':':'Two statements on one line.','PotCount = PotCount + 1':'Advance the live pot count.'},
   'CODE-22': {'For i = 0 To PotCount - 1':'Read the pot in play order.','AddCardToBottom(Winner, Pot(i))':'Append each card to the bottom.','PotCount = 0':'Then empty the live pot.'},
  }
  note=specific.get(id,{}).get(focus)
  if note:
   if id=='CODE-02' and targets:
    tx,ty=targets[0];endx=tx+width(focus,size,'mono');s.text(note,1260,ty,31,GOLD);s.arrow(1230,ty-12,max(endx+16,tx+80),ty-12,GOLD,2)
   else:s.text(note,150,982,34,GOLD)
  if id=='CODE-04':
   # Two nested brackets have fixed, separately labeled endpoints.
   for px,start,end,label,col in [(345,0,6,'Rank',BLUE),(425,1,5,'SuitIndex',GOLD)]:
    y1=yy+start*size*1.27-size*.8;y2=yy+end*size*1.27+5
    s.path(f'M{px+15} {y1}H{px}V{y2}H{px+15}',col,3)
   s.text('Rank',1290,982,28,BLUE,mono=True);s.text('SuitIndex',1475,982,28,GOLD,mono=True)
 else:
  if actual_refs:s.text(f'Lines {lo}–{actual_refs[0][2]}',150,981,27,MUTED,mono=True)
 return s.finish()

def codes():
 for id,r in ROWS.items():
  if not id.startswith('CODE'):continue
  # Read the complete ticket separately; manifests are structured inputs, not substitute work orders.
  ticket=(ROOT/r['ticket']).read_text(encoding='utf-8'); assert '## Acceptance checks' in ticket
  focuses=next(q for q in r['requirements'] if q.startswith('Required focus sequence:')).split(': ',1)[1].rstrip('.').split(' → ')
  size,pages=code_layout(r);frames=[];time=0
  for p in range(len(pages)):frames.append((time,code_svg(r,page=p)));time+=2
  for focus in focuses:
   page=next((p for p,rs in enumerate(pages) if any(focus in v[1] for v in rs)),0)
   frames.append((time,code_svg(r,focus,page)));time+=max(1.25,6/len(focuses))
  dur=max(10,time+2)
  clean=code_svg(r);highlight=code_svg(r,focuses[-1],next((p for p,rs in enumerate(pages) if any(focuses[-1] in v[1] for v in rs)),0))
  # Pick a representative poster with a useful, readable focus rather than a tail highlight.
  poster_focus=focuses[min(1,len(focuses)-1)];poster_page=next((p for p,rs in enumerate(pages) if any(poster_focus in v[1] for v in rs)),0)
  variants={'clean':clean,'highlighted':highlight}
  for p in range(1,len(pages)):variants[f'clean-page-{p+1:02}']=code_svg(r,page=p)
  scene(id,dur,frames,variants,code_svg(r,poster_focus,poster_page),notes=['Exact source text, separately stored. Soft visual wraps do not change source line breaks.','Literal modern VB.NET source illustration; not a live IDE or VB4 capture.','All focus targets have individually timed holds.'],source_text=r['copy']+'\n')

CMP_TITLES={'CMP-01':'Declaring a variable','CMP-02':'A procedure without a return value','CMP-03':'The same inclusive range','CMP-04':'Counting backward','CMP-05':'Returning a value','CMP-06':'Joining strings','CMP-07':'Repeating while both have cards','CMP-08':'Continuing a statement'}
CMP_FOCUS={'CMP-01':('int','As Integer'),'CMP-02':('void','Sub'),'CMP-03':('rank <= 14','2 To 14'),'CMP-04':('i--','Step -1'),'CMP-05':('return','DrawTopCard'),'CMP-06':('+','&'),'CMP-07':('while','Do While'),'CMP-08':('+','_')}
def comparison_svg(r,focus=False):
 s=SVG(BG,r['title']);s.heading(CMP_TITLES.get(r['id'],r['title']))
 text=r['copy'];left,right=text.split('\n\nVB\n');left=left.removeprefix('C#\n')
 size={'CMP-01':54,'CMP-02':34,'CMP-03':36,'CMP-04':36,'CMP-05':58,'CMP-06':58,'CMP-07':34,'CMP-08':34}[r['id']];cw=width('0',size,'mono');maxchars=int(722/cw)
 for col,(label,content,lang) in enumerate([('C#',left,'cs'),('VB',right,'vb')]):
  x=120+col*870;s.rect(x,248,810,652,'#171c23');s.rect(x,248,810,6,BLUE if col==1 else '#738192')
  s.text(label,x+44,335,53,FG,True)
  logical=[]
  for line in content.splitlines():
   if len(line)<=maxchars:logical.append(line)
   else:
    while len(line)>maxchars:
     split=line.rfind(' ',int(maxchars*.5),maxchars+1);split=split+1 if split>=0 else maxchars
     logical.append(line[:split]);line=line[split:]
    logical.append(line)
  leading=size*1.42;y=540-(max(1,len(logical))-1)*leading/2
  for j,line in enumerate(logical):code_line(s,line,x+44,y+j*leading,size,lang, CMP_FOCUS[r['id']][col] if focus else None)
 s.text('Syntax comparison',120,978,30,MUTED)
 return s.finish()
def comparisons():
 for id,r in ROWS.items():
  if id.startswith('CMP'):
   simple(id,comparison_svg(r),{'comparison':comparison_svg(r),'token-focus':comparison_svg(r,True)},notes=[r['requirements'][0],'No compile/run is claimed for illustrative counterparts.'])

def fact_svg(id):
 r=ROWS[id];s=SVG(BG,r['title']);parts=r['copy'].split('\n');a,b=parts[0],parts[1] if len(parts)>1 else ''
 # Minimal editorial typography, no boilerplate "Did you know?".
 if id=='FACT-01':
  s.text('BASIC',118,504,240,BLUE,True);s.lines(wrap(b,1360,60),130,689,60,FG,leading=1.18)
 elif id=='FACT-02':
  s.text('Dim',170,614,216,BLUE,True,mono=True);s.bevel(920,368,676,218,'#c0c0c0');s.path('M1010 586L963 638L1082 586','#808080',2,'#c0c0c0');s.text('Dimension?',1258,504,67,'#111',False,False,'middle')
 elif id=='FACT-03':
  s.text('RAD',125,442,224,BLUE,True);s.text(b,137,593,65,FG);s.window(1250,268,492,462,'');s.button('Click Me',1353,477,286,80);s.cursor(1589,549)
 elif id=='FACT-04':
  s.text('VB 3.0',124,510,170,BLUE,True);s.text(b,135,660,62,FG)
 elif id=='FACT-05':
  s.rect(120,307,1680,345,'#171e26');code_line(s,a,186,511,77,focus='DrawTopCard');s.text(b,143,762,52,FG)
 else:
  s.lines(wrap(a,1400,74,'bold'),130,390,74,FG,True);s.lines(wrap(b,1400,54),134,634,54,BLUE)
 return s.finish()
def facts():
 for n in range(1,7):
  id=f'FACT-{n:02}';simple(id,fact_svg(id),notes=['Face copy is taken from the supplied ticket. Historical claims, where assigned, remain producer-review gates; no verification is implied by this design.'])

def mock_gui(annotated=False):
 s=SVG(TEAL,'War — CPU vs CPU');s.window(152, ninety:=90,1616,816,'War — CPU vs CPU')
 s.rect(174,165,1572,592,FELT);s.rect(174,165,1572,592,'url(#felt)')
 s.text('Player 1',440,227,34,'#e9f3eb',True,anchor='middle');s.text('Player 2',1480,227,34,'#e9f3eb',True,anchor='middle')
 for x in [350,1390]:
  for k in range(3):s.card('AS',x+k*5,285-k*5,157,220,back=True)
 s.card('AS',764,322,165,232);s.card('KH',984,322,165,232)
 s.text('25 cards',440,613,34,'#e9f3eb',anchor='middle');s.text('25 cards',1480,613,34,'#e9f3eb',anchor='middle');s.text('Pot: 2',960,641,37,'#e9f3eb',anchor='middle')
 s.button('Deal',228,784,218,72);s.button('Watch',468,784,218,72);s.text('Speed',814,830,31,'#111');s.bevel(937,815,458,9,'#808080',True);s.bevel(1085,792,30,58)
 s.text('This is what you’d build next.',960,986,39,'#fff',anchor='middle')
 if annotated:
  s.rect(671,177,578,67,'#fff7da');s.text('Card PictureBoxes',960,222,31,'#382d1e',anchor='middle');s.arrow(954,250,950,311,GOLD,3)
  s.rect(698,677,650,57,'#fff7da');s.text('Timer → one round at a time',1023,716,30,'#382d1e',anchor='middle')
  s.arrow(358,764,358,750,GOLD);s.text('Deal / Watch',473,712,29,'#fff7da',anchor='middle')
 return s.finish()
def download_svg(progress=.22):
 s=SVG(TEAL,'Download progress mockup');s.window(380,279,1160,514,'')
 s.text('War.zip',440,412,46,'#111',True);s.text('14.4 modem',1470,410,32,'#333',anchor='end')
 s.bevel(440,465,980,61,'#fff',True)
 for i in range(round(progress*41)):
  s.rect(447+i*23.5,473,18,45,NAVY)
 s.text('Estimated time remaining:',444,584,36,'#111');s.text('9 minutes 42 seconds',444,637,47,'#111',True);s.button('Cancel',1190,675,235,66)
 return s.finish()
def mockups():
 simple('MOCK-01',mock_gui(),{'concept':mock_gui(),'annotated':mock_gui(True)},notes=['Conceptual GUI only, not an implemented or captured VB4 application.','Original vector cards. Counts are 25 + 25 + pot 2 = 52.'])
 f=[(0,download_svg(.22)),(3,download_svg(.244)),(6,download_svg(.269))]
 scene('MOCK-02',9,f,{'eta-hold':f[0][1],'slow-progress':f[-1][1]},f[0][1],notes=['War.zip is an authored illustrative filename. ETA and modem context come from the ticket, not measured transfer performance.'])

def references():
 historical_code()
 r=ROWS['REF-03'];base=code_svg(r);hi=code_svg(r,'MsgBox')
 scene('REF-03',10,[(0,base),(2,code_svg(r,'Sub')),(4,hi),(8,hi)],{'clean':base,'teaching-focus':hi},hi,source_text=r['copy']+'\n',notes=['Exact script event handler, not a standalone application and not a VB4 compiler capture.'])
 def basic(n=0):
  s=SVG('#06110a','BASIC / 10 PRINT / 20 GOTO');s.rect(106,146,1708,774,'none','#365342',2)
  full=ROWS['REF-04']['copy'];typed=full[:n] if n else full
  s.lines(typed.split('\n'),177,384,66,'#a3d997',mono=True,leading=1.46)
  return s.finish()
 full=ROWS['REF-04']['copy'];frames=[(0,basic(1))]+[(.4+i*.08,basic(i)) for i in range(2,len(full)+1)]
 clean=basic();scene('REF-04',8,frames,{'clean':clean,'teaching-focus':clean},clean,notes=['Original green-screen illustration; not an emulator or historical hardware capture.'],source_text=full+'\n')

# Representative historical code (REF-01, REF-02): authored fixtures shown as a scrolling listing that ends on a focus.
FIXTURES=ROOT/'tools/fixtures'
def listing_rows(files):
 rows=[]
 for k,(name,language,lines) in enumerate(files):rows+=([None] if k else [])+[(n,language,line) for n,line in enumerate(lines,1)]
 return rows
def listing_svg(r,files,label,top=0,focus=None,note=None,visible=16):
 # Line numbers restart in each file and a rule separates files; both are display layers, not source text.
 size=30;pitch=size*1.27;s=SVG(BG,r['title'])
 s.text(' · '.join(f[0] for f in files),120,117,32,MUTED,mono=True);s.text(label,1800,117,28,BLUE,anchor='end')
 s.line(120,147,1800,147,LINE,2);s.text(r['copy'],120,210,46,FG,True)
 s.rect(120,247,1680,673,'#151a20');s.rect(120,247,5,673,BLUE)
 for i,row in enumerate(listing_rows(files)[top:top+visible]):
  y=320+i*pitch
  if row is None:s.line(207,y-11,1760,y-11,LINE,2);continue
  n,language,line=row
  if focus and focus[0]<=top+i<=focus[1]:s.rect(130,y-size+1,1660,pitch,'#263c58')
  s.text(str(n),163,y,25,'#748293',mono=True,anchor='middle')
  if language:code_line(s,line,207,y,size,language)
  else:s.text(line,207,y,size,FG,mono=True)
 if note:s.text(note,150,982,34,GOLD)
 s.text(f'{sum(len(f[2]) for f in files)} lines',1800,982,27,MUTED,mono=True,anchor='end')
 return s.finish()
def code_scroll(id,label,files,focus_text,note,notes,source_text,extra=None,visible=16):
 r=ROWS[id];rows=listing_rows(files);last=max(0,len(rows)-visible)
 at=lambda text:next(i for i,row in enumerate(rows) if row and text in row[2])
 focus=(at(focus_text[0]),at(focus_text[1]));top=min(last,max(0,focus[0]-(visible-(focus[1]-focus[0]+1))//2))
 clean=listing_svg(r,files,label);hi=listing_svg(r,files,label,top,focus,note)
 # A 2.5 s opening hold, one line every 0.25 s to the end of the listing, then the focus holds 4.5 s.
 end=2.5+last*.25+.5;frames=[(0,clean)]+[(2.5+k*.25,listing_svg(r,files,label,k)) for k in range(1,last+1)]+[(end,hi)]
 scene(id,math.ceil(end+4.5),frames,{'clean':clean,'teaching-focus':hi},hi,notes=notes+[f'Timing: a 2.5 s hold, a one-line scroll every 0.25 s through all {len(rows)} rows, then the focus from {end:g} s to the end.'],source_text=source_text,files=extra)
def historical_code():
 mfc=(FIXTURES/'ref-01-cardview.cpp').read_text(encoding='utf-8')
 code_scroll('REF-01','Representative Visual C++ / MFC',[('cardview.h · cardview.cpp','cpp',mfc.splitlines())],('BEGIN_MESSAGE_MAP','END_MESSAGE_MAP'),'The message map: macros that connect Windows messages and commands to handlers.',
  ['Agent-authored representative MFC code in the style of Visual C++ 4: ClassWizard AFX_MSG blocks and ON_COMMAND(ID, handler) without &Class::. It is not recovered historical source.','Not compiled: Visual Studio 2022 on the production machine has no MFC libraries installed. Technical and era review stays open under R15.','CCardDoc, FlipNextCard, Deal and IsDealt are illustrative names for this card game; their definitions are not shown.','Line numbers and the caption are display layers; src/excerpt.cpp holds the exact text.'],mfc)
 hello=(FIXTURES/'ref-02-hello.c').read_text(encoding='utf-8');module=(FIXTURES/'ref-02-hello.def').read_text(encoding='utf-8')
 c,d=len(hello.splitlines()),len(module.splitlines())
 code_scroll('REF-02','Representative Windows 3.0 C',[('hello.c','c',hello.splitlines()),('hello.def',None,module.splitlines())],('while (GetMessage','DispatchMessage'),'The message loop: get a message, translate it, dispatch it to WndProc.',
  ['Agent-authored representative Windows 3.0-style C: HANDLE hPrevInstance, long FAR PASCAL WndProc with WORD/LONG parameters, and the .DEF file a Win16 program needed to link. It is not copied from a tutorial or recovered from a historical source.','Not compiled for Windows: no 16-bit Windows toolchain is installed on the production machine. Technical and era review stays open under R15; R03 also applies.',f'hello.c is {c} lines and hello.def {d}: {c+d} lines in all. The code was not padded toward the script’s “about 80 lines”; by producer decision (2026-09-15), War/SCRIPT.md now says 73 lines to match.','Line numbers restart in each file and the caption is a display layer; src/excerpt.c and src/hello.def hold the exact text.'],hello,{'hello.def':module})

# Diagram implementations are imported after the shared primitives.
def save_assets(ids=None,owner='ChatGPT — local production'):
 for id,item in REGISTRY.items():
  if ids and id not in ids:continue
  r=ROWS[id];base=ROOT/ROWS[id]['asset_dir']
  for name in ['src','exports','exports/keyframes','evidence','proofs']:(base/name).mkdir(parents=True,exist_ok=True)
  # Each ticket retains its own authored data and complete source context.
  (base/'src/brief.json').write_text(json.dumps({k:r[k] for k in ['id','title','requirements','beats','checks','copy','refs','gates']},indent=2,ensure_ascii=False),encoding='utf-8',newline='\n')
  snippets=[];sources=[]
  for filename,lo,hi in r['refs']:
   path=ROOT/'sources'/filename;text=path.read_text(encoding='utf-8').splitlines();snippets.append(f'## {filename}:{lo}–{hi}\n\n```text\n'+ '\n'.join(text[lo-1:hi])+'\n```\n')
   sources.append({'path':'../../../sources/'+filename,'lines':[lo,hi],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'relationship':'literal excerpt' if filename=='Program.vb' else 'source creative brief'})
  (base/'evidence/source-excerpts.md').write_text('\n'.join(snippets),encoding='utf-8',newline='\n')
  notes=item['notes'];(base/'evidence/provenance.json').write_text(json.dumps({'id':id,'classification':'literal source-code illustration' if id.startswith('CODE') else 'authored teaching illustration: representative code written for this production' if id in ('REF-01','REF-02') else 'original authored source-based illustration','sources':sources,'authored_additions':notes,'source_unchanged':True,'remote_assets':[],'font_files_distributed':False,'producer_decisions':[]},indent=2,ensure_ascii=False),encoding='utf-8',newline='\n')
  gates=[{'id':g,'status':'blocked','reason':'Assigned editorial gate is retained. Artwork does not silently revise the source or imply historical/runtime verification.','evidence_paths':['source-excerpts.md']+[f'../src/{n}' for n in item['files']],'approver':None} for g in r['gates']]
  (base/'evidence/claim-checks.json').write_text(json.dumps({'gates':gates},indent=2),encoding='utf-8',newline='\n')
  frames=item['frames']; names=[];dedup={}
  for t,svg in frames:
   sha=hashlib.sha256(svg.encode()).hexdigest()
   if sha not in dedup:
    n=f'scene-{len(dedup):04}.svg';dedup[sha]=n;(base/'src'/n).write_text(svg,encoding='utf-8',newline='\n')
   names.append({'time':round(t,6),'file':dedup[sha]})
  (base/'src/scene.svg').write_text(item['poster'],encoding='utf-8',newline='\n')
  # Inline all frames: HTML works when double-clicked, even offline and under file://.
  table={n:(base/'src'/n).read_text(encoding='utf-8') for n in dedup.values()}
  timeline={'id':id,'durationSeconds':item['duration'],'fps':30 if item['duration'] else None,'width':1920,'height':1080,'beats':r['beats'],'frames':names,'cuts':item['cuts'],'variant_names':list(item['variants']), 'motion_model':'Explicit deterministic step states with readable holds; MP4 encodes the same scene changes at 30 fps.'}
  (base/'src/timeline.json').write_text(json.dumps(timeline,indent=2,ensure_ascii=False),encoding='utf-8',newline='\n')
  html_doc='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+html.escape(r['title'])+'''</title><style>html,body{margin:0;background:#000;height:100%;overflow:hidden}#stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center}svg{width:100%;height:100%;object-fit:contain}</style><div id="stage" aria-label="'''+html.escape(r['title'],quote=True)+'''"></div><script>const timeline='''+json.dumps(timeline,ensure_ascii=False)+''';const scenes='''+json.dumps(table,ensure_ascii=False)+''';const stage=document.getElementById('stage');window.__ASSET__={id:timeline.id,durationSeconds:timeline.durationSeconds||0,fps:timeline.fps||30,width:1920,height:1080,ready:document.fonts.ready,renderAt(t){t=Math.max(0,Math.min(Number.isFinite(t)?t:0,this.durationSeconds));let f=timeline.frames[0];for(const x of timeline.frames){if(x.time<=t)f=x;else break}stage.innerHTML=scenes[f.file];return f.file}};__ASSET__.renderAt(0);let start=null,playing=false;document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();playing=!playing;start=null;requestAnimationFrame(tick)}if(e.code==='Home'){playing=false;__ASSET__.renderAt(0)}});function tick(ts){if(!playing)return;if(start===null)start=ts;const t=(ts-start)/1000;__ASSET__.renderAt(t);if(t<__ASSET__.durationSeconds)requestAnimationFrame(tick);else playing=false}</script></html>'''
  (base/'src/index.html').write_text(html_doc,encoding='utf-8',newline='\n')
  # All named variants are concrete separate editable SVG files, not renamed PNG copies.
  vmap={}
  for name,svg in item['variants'].items():
   path=f'variant-{name}.svg';(base/'src'/path).write_text(svg,encoding='utf-8',newline='\n');vmap[name]=path
  source=item.get('source_text')
  if source is not None:
   ext={'REF-01':'cpp','REF-02':'c','REF-04':'bas'}.get(id,'vb');(base/'src'/f'excerpt.{ext}').write_text(source,encoding='utf-8',newline='\n')
  for name,content in item['files'].items():
   (base/'src'/name).write_text(content if isinstance(content,str) else json.dumps(content,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
  build={'id':id,'duration':item['duration'],'frames':names,'variants':vmap,'poster':'scene.svg','cuts':item['cuts'],'notes':notes,'sources':sources,'kind':r['kind']}
  (base/'src/build.json').write_text(json.dumps(build,indent=2,ensure_ascii=False),encoding='utf-8',newline='\n')
  state=json.loads((base/'state.json').read_text(encoding='utf-8'));state.update(production_status='in_progress',release_status='blocked' if r['gates'] else 'unreviewed',owner=owner,notes=['Sources and scenes authored; exports and QA pending.'])
  (base/'state.json').write_text(json.dumps(state,indent=2),encoding='utf-8',newline='\n')
  print('AUTHORED',id,len(dedup),'states',flush=True)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--id',action='append');ap.add_argument('--owner',default='ChatGPT — local production',help='Owner written to each rebuilt state.json.');args=ap.parse_args()
 chapters();cards();codes();comparisons();facts();mockups();references()
 try:
  from diagrams import build_diagrams
  build_diagrams()
 except ImportError as e:
  if e.name!='diagrams':raise
 save_assets(set(args.id) if args.id else None,args.owner)
if __name__=='__main__':main()
