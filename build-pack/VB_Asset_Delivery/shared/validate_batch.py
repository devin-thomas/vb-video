#!/usr/bin/env python3
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import subprocess,json
ROOT=Path(__file__).resolve().parents[1]
def check(id):
 p=subprocess.run(['python',str(ROOT/'tools/validate_delivery.py'),'--id',id],capture_output=True,text=True)
 try:r=json.loads(p.stdout)
 except:r={'id':id,'ok':False,'errors':[p.stdout,p.stderr]}
 print(id,r['ok'],flush=True);return r
ids=[x['id'] for x in json.loads((ROOT/'review/production-index.json').read_text())]
with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(check,ids))
(ROOT/'review/delivery-validation.json').write_text(json.dumps(results,indent=2))
print('COMPLETE',len(results),'failures',sum(not r['ok'] for r in results),flush=True)
