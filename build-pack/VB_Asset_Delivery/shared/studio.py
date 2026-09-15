#!/usr/bin/env python3
"""Offline SVG scene primitives. No fonts or network assets are distributed."""
from __future__ import annotations
import html, math, re
from pathlib import Path
from PIL import ImageFont
W,H=1920,1080
BG='#111318'; PANEL='#1b2027'; FG='#f1f3f5'; MUTED='#aeb6bf'; LINE='#343d48'
BLUE='#79adff'; GOLD='#eab676'; GREEN='#8dc48c'; TEAL='#008080'; GRAY='#c0c0c0'; NAVY='#000080'; FELT='#0b6b3a'
SANS='Liberation Sans'; MONO='DejaVu Sans Mono'
FONT_PATHS={'sans':'/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf','bold':'/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf','mono':'/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'}
# Runtime fallback paths are discovered, not copied into the delivery.
for key,p in list(FONT_PATHS.items()):
 if not Path(p).exists():
  import subprocess
  FONT_PATHS[key]=subprocess.check_output(['fc-match','-f','%{file}', MONO if key=='mono' else SANS+(':style=Bold' if key=='bold' else '')],text=True)
_fonts={}
def width(s,size=40,face='sans'):
 k=(size,face)
 if k not in _fonts:_fonts[k]=ImageFont.truetype(FONT_PATHS[face],size)
 return _fonts[k].getlength(s)
def wrap(s,limit,size=40,face='sans'):
 out=[]
 for para in s.split('\n'):
  words=para.split(' '); line=''
  for word in words:
   if line and width(line+' '+word,size,face)>limit:out.append(line);line=word
   else:line=(line+' '+word).lstrip()
  out.append(line)
 return out
class SVG:
 def __init__(self,bg=BG,title=''):
  self.a=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080" role="img"><title>{html.escape(title)}</title>', '<defs><pattern id="back" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M0 6L6 0L12 6L6 12Z" fill="none" stroke="#8fa1c5" stroke-width="1"/></pattern><pattern id="felt" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M1 2h1M6 7h1" stroke="#ffffff" stroke-opacity=".035"/></pattern></defs>']
  self.rect(0,0,W,H,bg)
 def raw(self,s): self.a.append(s)
 def rect(self,x,y,w,h,fill='none',stroke=None,sw=2,rx=0,opacity=1):
  self.a.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+(f' opacity="{opacity}"' if opacity!=1 else '')+'/>')
 def text(self,s,x,y,size=40,fill=FG,bold=False,mono=False,anchor='start',opacity=1):
  self.a.append(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{MONO if mono else SANS}" font-size="{size}" font-weight="{700 if bold else 400}" fill="{fill}" text-anchor="{anchor}" opacity="{opacity}" xml:space="preserve">{html.escape(str(s))}</text>')
 def lines(self,lines,x,y,size=40,fill=FG,bold=False,mono=False,leading=1.24,anchor='start'):
  for i,s in enumerate(lines):self.text(s,x,y+i*size*leading,size,fill,bold,mono,anchor)
 def line(self,x,y,x2,y2,fill=LINE,sw=3,dash=None):
  self.a.append(f'<path d="M{x:.2f} {y:.2f}L{x2:.2f} {y2:.2f}" fill="none" stroke="{fill}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def path(self,d,stroke=FG,sw=3,fill='none'):
  self.a.append(f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}" stroke-linejoin="round"/>')
 def circle(self,x,y,r,fill='none',stroke=None,sw=2):
  self.a.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>')
 def arrow(self,x,y,x2,y2,fill=BLUE,sw=3):
  self.line(x,y,x2,y2,fill,sw);a=math.atan2(y2-y,x2-x)
  self.path(f'M{x2-14*math.cos(a-.45)} {y2-14*math.sin(a-.45)} L{x2} {y2} L{x2-14*math.cos(a+.45)} {y2-14*math.sin(a+.45)}',fill,sw)
 def bevel(self,x,y,w,h,fill=GRAY,pressed=False):
  self.rect(x,y,w,h,fill);a,b=('#505050','#ffffff') if pressed else ('#ffffff','#505050')
  self.path(f'M{x} {y+h}V{y}H{x+w}',a,3);self.path(f'M{x+w} {y}V{y+h}H{x}',b,3)
  self.path(f'M{x+3} {y+h-3}V{y+3}H{x+w-3}', '#dfdfdf' if not pressed else '#808080',1)
 def window(self,x,y,w,h,caption='',titleh=54):
  self.rect(x+10,y+12,w,h,'#002e2e',opacity=.5);self.bevel(x,y,w,h)
  self.rect(x+6,y+6,w-12,titleh,NAVY)
  if caption:self.text(caption,x+22,y+titleh-8,30,'#ffffff',True)
  self.bevel(x+w-47,y+14,31,30);self.path(f'M{x+w-39} {y+21}l15 15m-15 0l15-15','#111',2.4)
 def button(self,label,x,y,w=210,h=68,pressed=False):
  self.bevel(x,y,w,h,pressed=pressed);self.text(label,x+w/2+(2 if pressed else 0),y+h/2+13+(2 if pressed else 0),32,'#111',False,False,'middle')
 def cursor(self,x,y):
  self.path(f'M{x} {y}v42l11-12 10 22 10-5-10-21h17Z','#111',3,'#fff')
 def heading(self,title,sub=None):
  ls=wrap(title,1630,58,'bold');self.lines(ls,120,138,58,FG,True,leading=1.1)
  if sub:self.text(sub,120,196+max(0,len(ls)-1)*60,28,MUTED)
 def card(self,identity,x,y,w=144,h=202,back=False,opacity=1,accent=None):
  # Original vector artwork. Face-down cards have no exposed rank/suit.
  self.raw(f'<g opacity="{opacity}">')
  self.rect(x+5,y+6,w,h,'#001e18',rx=7,opacity=.28)
  self.rect(x,y,w,h,'#fbfaf4',stroke=accent or '#c9c7bd',sw=3 if accent else 1.5,rx=7)
  if back:
   self.rect(x+8,y+8,w-16,h-16,'#223b72',rx=2);self.rect(x+12,y+12,w-24,h-24,'url(#back)');self.rect(x+17,y+17,w-34,h-34,'none','#c5cfdf',1)
  else:
   rank,suit=identity[:-1],identity[-1];sym={'S':'♠','H':'♥','D':'♦','C':'♣'}[suit];col='#b53b34' if suit in 'HD' else '#172128'
   fs=max(18,round(w*.22));self.text(rank,x+13,y+fs+8,fs,col,True)
   if w>=110:self.text(sym,x+13,y+fs*2+9,fs,col)
   self.text(sym,x+w/2,y+h*.63,round(w*.5),col,False,False,'middle')
   if w>=110:
    self.raw(f'<g transform="rotate(180 {x+w/2} {y+h/2})">');self.text(rank,x+13,y+fs+8,fs,col,True);self.raw('</g>')
  self.raw('</g>')
 def finish(self):return ''.join(self.a)+'</svg>'

VB_WORDS=set('Option Explicit Strict On Off Module Structure Dim As Integer Char String Const Sub Function End ByRef ByVal New ReDim For To Step Next If Then Else ElseIf Select Case Do While Loop Exit And Or Return True False'.split())
CS_WORDS=set('int char void for while return if else new string ref'.split())
def segments(line,language='vb'):
 # Preserve every character, including continuation underscores and quote spelling.
 pattern=r'("(?:""|[^"\n])*"[cC]?)|(\'.*$)|([A-Za-z_][A-Za-z_0-9]*)|(\d+)|([^A-Za-z_0-9"\']+)'
 if language=='cs':pattern=r'("(?:\\.|[^"\\])*?")|(//.*$)|([A-Za-z_][A-Za-z_0-9]*)|(\d+)|([^A-Za-z_0-9"]+)'
 parts=[]
 for m in re.finditer(pattern,line):
  token=m.group(0);color=FG
  if m.group(1):color=GOLD
  elif m.group(2):color=GREEN
  elif m.group(3) and token in (VB_WORDS if language=='vb' else CS_WORDS):color=BLUE
  elif m.group(4):color=GOLD
  parts.append((token,color))
 if ''.join(p[0] for p in parts)!=line:return [(line,FG)]
 return parts

def code_line(s,line,x,y,size=34,language='vb',focus=None,dim=False):
 cw=width('0',size,'mono')
 if focus and focus in line:
  j=line.index(focus);s.rect(x+j*cw-3,y-size-2,len(focus)*cw+6,size+10,'#263c58',rx=2)
 xx=x
 for part,col in segments(line,language):
  s.text(part,xx,y,size,MUTED if dim else col,mono=True);xx+=len(part)*cw
 return xx
