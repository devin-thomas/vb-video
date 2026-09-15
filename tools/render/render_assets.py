#!/usr/bin/env python3
"""Render local SVG scenes and encode exact 30 fps state timelines.
Requires already installed Python cairosvg/Pillow and ffmpeg. Never installs anything.
"""
from __future__ import annotations
import argparse, concurrent.futures, hashlib, json, math, os, shutil, subprocess, sys, tempfile
from pathlib import Path
import cairosvg
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
from paths import asset_dir
def raster(src:Path,dst:Path):
 dst.parent.mkdir(parents=True,exist_ok=True)
 cairosvg.svg2png(url=str(src),write_to=str(dst),output_width=1920,output_height=1080)
 assert Image.open(dst).size==(1920,1080)
def ffprobe(p):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_name,codec_type,width,height,r_frame_rate,pix_fmt,nb_frames','-of','json',str(p)],text=True))
def encode(base,frames,duration,dst,cache):
 # Quantize authored state transitions to frame boundaries, matching renderAt(n/30).
 n=math.ceil(duration*30-1e-8);runs=[]
 for i,frame in enumerate(frames):
  start=math.ceil(frame['time']*30-1e-8)
  end=min(n,math.ceil(frames[i+1]['time']*30-1e-8)) if i+1<len(frames) else n
  count=end-start
  if count<=0:continue
  png=cache[frame['file']];runs.append((png,count/30))
 if not runs:raise ValueError('No video frames')
 concat=dst.with_suffix('.concat.txt')
 lines=[]
 for p,d in runs:lines.extend([f"file '{p.as_posix()}'",f'duration {d:.9f}'])
 lines.append(f"file '{runs[-1][0].as_posix()}'")
 concat.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-vf','fps=30,format=yuv420p','-frames:v',str(n),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','2','-movflags','+faststart',str(dst)]
 subprocess.run(cmd,check=True);concat.unlink()
 info=ffprobe(dst);st=info['streams'][0]
 assert st['width']==1920 and st['height']==1080 and st['r_frame_rate']=='30/1' and st['pix_fmt']=='yuv420p'
 assert abs(float(info['format']['duration'])-duration)<.07
 return {'file':str(dst.relative_to(base)), 'command':' '.join(cmd), 'probe':info}
def render(id):
 base=asset_dir(id);data=json.loads((base/'src/build.json').read_text(encoding='utf-8'));reports=[]
 # SVG keyframes remain sources; temporary raster intermediates are not delivered.
 with tempfile.TemporaryDirectory(prefix='vb-') as td:
  cache={}
  for f in data['frames']:
   if f['file'] not in cache:
    p=Path(td)/Path(f['file']).with_suffix('.png').name;raster(base/'src'/f['file'],p);cache[f['file']]=p
  raster(base/'src'/data['poster'],base/'exports/poster.png')
  for name,src in data['variants'].items():raster(base/'src'/src,base/'exports'/f'{name}.png')
  dur=data['duration']
  if dur:
   for name,t in [('start',0),('middle',dur/2),('end',dur-1/30)]:
    f=next((f for f in reversed(data['frames']) if f['time']<=t),data['frames'][0]);shutil.copyfile(cache[f['file']],base/'exports/keyframes'/f'{name}.png')
   reports.append(encode(base,data['frames'],dur,base/'exports/preview.mp4',cache))
   for name,span in data.get('cuts',{}).items():
    start,end=span
    current=next(f for f in reversed(data['frames']) if f['time']<=start)
    frames=[{'time':0,'file':current['file']}]+[{'time':f['time']-start,'file':f['file']} for f in data['frames'] if start<f['time']<end]
    reports.append(encode(base,frames,end-start,base/'exports'/f'{name}.mp4',cache))
  proof=Image.open(base/'exports/poster.png');proof.resize((1280,720),Image.Resampling.LANCZOS).save(base/'proofs/poster-720.png')
  # Compact contact sheet for this ticket's temporal states and named variants.
  paths=[base/'exports/poster.png']+[base/'exports'/f'{n}.png' for n in data['variants']]
  if dur:paths += [base/'exports/keyframes'/f'{n}.png' for n in ['start','middle','end']]
  thumbs=[]
  from PIL import ImageDraw,ImageFont
  # Pillow also resolves a bare font file name in the Windows font folder.
  linux_font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';font=ImageFont.truetype(linux_font if os.path.exists(linux_font) else 'DejaVuSans.ttf',16)
  for p in paths:
   im=Image.open(p).convert('RGB');im.thumbnail((480,270));cell=Image.new('RGB',(480,300),'#13171c');cell.paste(im,(0,0));ImageDraw.Draw(cell).text((10,277),p.stem,fill='white',font=font);thumbs.append(cell)
  sheet=Image.new('RGB',(960,300*math.ceil(len(thumbs)/2)),'#13171c')
  for i,im in enumerate(thumbs):sheet.paste(im,((i%2)*480,(i//2)*300))
  sheet.save(base/'exports/contact-sheet.png')
 (base/'evidence/render-tests.json').write_text(json.dumps({'renderer':'CairoSVG '+cairosvg.__version__,'png_dimensions':'1920x1080','video_probes':reports,'command':f'python tools/render/render_assets.py --id {id}'},indent=2),encoding='utf-8',newline='\n')
 print('RENDERED',id,flush=True)
 return id
def main():
 # MSYS2's Cairo crashed (access violation) rendering from three threads on Windows; one worker is reliable there.
 ap=argparse.ArgumentParser();ap.add_argument('--id',action='append');ap.add_argument('--workers',type=int,default=1 if os.name=='nt' else 3);ap.add_argument('--skip-existing',action='store_true');args=ap.parse_args()
 ids=args.id or sorted(p.parent.parent.name for p in (ROOT/'assets').glob('*/*/src/build.json'))
 if args.skip_existing:ids=[i for i in ids if not (asset_dir(i)/'evidence/render-tests.json').exists()]
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
  tasks={ex.submit(render,id):id for id in ids}
  for f in concurrent.futures.as_completed(tasks):
   try:f.result()
   except Exception as e:print('FAILED',tasks[f],e,file=sys.stderr);raise
if __name__=='__main__':main()
