#!/usr/bin/env python3
"""Check one claimed delivery's files/metadata. Manual media/factual/rights review is still required."""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', required=True, help='Exact ticket ID, e.g. CODE-02.')
    args=parser.parse_args()
    errors: list[str] = []
    try:
        rows=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))['tickets']
        row=next((r for r in rows if r['id']==args.id),None)
        if row is None: raise ValueError('Unknown ticket ID.')
        base=(ROOT/row['asset_dir']).resolve()
        state=json.loads((base/'state.json').read_text(encoding='utf-8'))
        if not (base/'delivery.json').is_file():
            raise ValueError(f"{args.id}: no delivery.json; current production status is {state['production_status']}. Planning scaffolds are not delivered assets.")
        delivery=json.loads((base/'delivery.json').read_text(encoding='utf-8'))
    except (OSError,ValueError,KeyError) as exc:
        print(f'NOT DELIVERED / ERROR: {exc}',file=sys.stderr)
        return 1
    def safe(path: Path) -> bool:
        try: path.resolve().relative_to(base); return True
        except ValueError: return False
    required_keys=['id','title','production_status','release_status','provenance_type','shared_version',
                   'duration_seconds','dimensions','fps','outputs','variants','sources','credits','tests',
                   'unresolved_gates','toolchain','notes']
    for key in required_keys:
        if key not in delivery: errors.append(f'Missing delivery metadata: {key}')
    if delivery.get('id') != row['id']: errors.append('Delivery ID mismatch.')
    for field in ['production_status','release_status']:
        if delivery.get(field) != state.get(field): errors.append(f'State/delivery disagreement: {field}')
    claimed=delivery.get('production_status') in ['produced','reviewed','scouted']
    if not claimed:
        errors.append('This is not a produced/reviewed/scouted delivery; partial work must not be certified complete.')
    declared=delivery.get('outputs',[])
    if not isinstance(declared,list):
        errors.append('outputs must be a list.'); declared=[]
    indexed: dict[str,dict] = {}
    for output in declared:
        if not isinstance(output,dict) or 'path' not in output:
            errors.append('Malformed output record.'); continue
        rel=output['path']
        if not isinstance(rel,str): errors.append('Output path must be a string.'); continue
        path=base/rel
        if Path(rel).is_absolute() or not safe(path):
            errors.append(f'Unsafe output path: {rel}'); continue
        if rel in indexed: errors.append(f'Duplicate output declaration: {rel}')
        indexed[rel]=output
        if not path.is_file(): errors.append(f'Declared output missing: {rel}'); continue
        data=path.read_bytes()
        if output.get('bytes') != len(data): errors.append(f'Byte-size mismatch: {rel}')
        if output.get('sha256') != hashlib.sha256(data).hexdigest(): errors.append(f'Hash mismatch: {rel}')
    for pattern in row['required_outputs']:
        paths=list(base.glob(pattern)) if any(x in pattern for x in '*?[') else [base/pattern]
        files=[p for p in paths if p.is_file() and safe(p)]
        if not files:
            errors.append(f'Required file missing: {pattern}'); continue
        for path in files:
            rel=path.relative_to(base).as_posix()
            if rel!='delivery.json' and rel not in indexed:
                errors.append(f'Required file not in hashed output inventory: {rel}')
            if path.stat().st_size==0 and rel not in ['source/stderr.txt','evidence/project-diff.txt']:
                errors.append(f'Empty required file: {rel}')
            if rel.startswith('exports/') and path.suffix.lower()=='.png' and not rel.endswith('contact-sheet.png'):
                header=path.read_bytes()[:24]
                if len(header)<24 or header[:8]!=b'\x89PNG\r\n\x1a\n':
                    errors.append(f'Not a genuine PNG: {rel}')
                elif struct.unpack('>II',header[16:24])!=(1920,1080):
                    errors.append(f'Export PNG dimensions are not 1920×1080: {rel}')
    if row.get('source_hint')=='literal-program-excerpt':
        refs=[r for r in row['refs'] if r[0]=='Program.vb']
        if len(refs)==1 and (base/'src/excerpt.vb').exists():
            _,lo,hi=refs[0]
            original=(ROOT/'sources/Program.vb').read_text(encoding='utf-8').splitlines()
            if (base/'src/excerpt.vb').read_text(encoding='utf-8').splitlines()!=original[lo-1:hi]:
                errors.append('Literal VB excerpt does not match canonical source range.')
    if (base/'source/Program.vb').is_file():
        if (base/'source/Program.vb').read_bytes() != (ROOT/'sources/Program.vb').read_bytes():
            errors.append('Captured program copy changed from original.')
    if delivery.get('release_status')=='approved':
        if delivery.get('unresolved_gates'): errors.append('Release approved despite unresolved gates.')
        if row['kind']=='scout': errors.append('Scouting-only ticket is not release-approved acquired media.')
        if row['gates']:
            try:
                gate_data=json.loads((base/'evidence/claim-checks.json').read_text(encoding='utf-8'))
                gate_map={g['id']:g for g in gate_data['gates']}
                for gate in row['gates']:
                    info=gate_map.get(gate,{})
                    if info.get('status') not in ['approved','not_applicable'] or not info.get('approver') or not info.get('reason'):
                        errors.append(f'Gate {gate} lacks a documented reviewed decision.')
            except (OSError,ValueError,KeyError,TypeError) as exc:
                errors.append(f'Cannot validate release-gate record: {exc}')
    result={'id':row['id'],'ok':not errors,'errors':errors,
            'limitations':['No OCR or visual quality judgment.','No MP4 decode/frame-rate/codec validation; inspect with ffprobe and playback.',
                           'No historical, semantic, or legal clearance.','Manual 1080p/720p review remains required.']}
    print(json.dumps(result,indent=2))
    return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
