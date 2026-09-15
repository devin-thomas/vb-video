#!/usr/bin/env python3
"""Silent editor preview, not a narration-synchronized final episode."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,tempfile
ROOT=Path(__file__).resolve().parents[2]
from paths import asset_dir
SHOTS=[('CARD-01',0,7,'preview.mp4'),('MOCK-01',0,3,'poster.png'),('CH-07',.2,3,'preview.mp4'),('DIA-07',0,18,'preview.mp4'),('CODE-03',3,4,'preview.mp4'),('CMP-03',0,3,'token-focus.png'),('DIA-06',3,6,'preview.mp4'),('DIA-05',0,18,'preview.mp4'),('DIA-08',0,12,'preview.mp4'),('DIA-09',0,15,'preview.mp4'),('MOCK-02',0,3,'preview.mp4'),('CARD-02',.6,5,'preview.mp4')]
with tempfile.TemporaryDirectory(prefix='vb-reel-') as tmp:
 tmp=Path(tmp)
 def shot(item):
  n,(id,start,duration,name)=item;src=asset_dir(id)/'exports'/name;out=tmp/f'{n:02}.mp4'
  cmd=['ffmpeg','-v','error','-y']
  if name.endswith('.png'):cmd+=['-loop','1','-framerate','30']
  else:cmd+=['-ss',str(start)]
  cmd+=['-i',str(src),'-t',str(duration),'-an','-vf','fps=30,format=yuv420p,setsar=1','-c:v','libx264','-preset','veryfast','-crf','19','-threads','1','-movflags','+faststart',str(out)]
  subprocess.run(cmd,check=True);return out
 with ThreadPoolExecutor(max_workers=4) as e:segments=list(e.map(shot,enumerate(SHOTS)))
 concat=tmp/'concat.txt';concat.write_text('\n'.join(f"file '{p}'" for p in segments)+'\n')
 output=ROOT/'review/PREVIEW_REEL.mp4';subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(output)],check=True)
 t=0;edl=[]
 for id,start,dur,name in SHOTS:edl.append({'ticket':id,'source':f'{asset_dir(id).relative_to(ROOT).as_posix()}/exports/{name}','source_start':start,'reel_start':t,'duration':dur});t+=dur
 (ROOT/'review/reel-edit.json').write_text(json.dumps({'type':'silent production proof, not final episode','duration_seconds':t,'shots':edl},indent=2))
 print(output,t,flush=True)
