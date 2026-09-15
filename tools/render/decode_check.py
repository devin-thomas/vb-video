#!/usr/bin/env python3
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json
ROOT=Path(__file__).resolve().parents[2]
paths=sorted((ROOT/'assets').glob('*/*/exports/*.mp4'))+[ROOT/'review/PREVIEW_REEL.mp4']
def check(path):
 proc=subprocess.run(['ffmpeg','-v','error','-threads','1','-i',str(path),'-an','-f','null','-'],capture_output=True,text=True)
 r={'file':str(path.relative_to(ROOT)),'exit_code':proc.returncode,'decode_errors':proc.stderr,'ok':proc.returncode==0 and not proc.stderr.strip()};print(r['file'],r['ok'],flush=True);return r
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(check,paths))
(ROOT/'review/video-decode-tests.json').write_text(json.dumps(results,indent=2));print('COMPLETE',len(results),sum(not r['ok'] for r in results),flush=True)
