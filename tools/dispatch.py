#!/usr/bin/env python3
"""List ticket readiness. Does not start workers or change shared state."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lane', choices=['orchestrator','motion','design','code','capture','research','qa'])
    parser.add_argument('--all', action='store_true', help='Include tickets waiting on dependencies.')
    args = parser.parse_args()
    try:
        rows = json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))['tickets']
        states = {r['id']:json.loads((ROOT/r['asset_dir']/'state.json').read_text(encoding='utf-8')) for r in rows}
    except (OSError,ValueError,KeyError) as exc:
        print(f'ERROR: Cannot read dispatch state: {exc}',file=sys.stderr)
        return 1
    accepted = {'reviewed','scouted','no_match'}
    shown = 0
    for row in rows:
        if args.lane and row['lane'] != args.lane: continue
        status = states[row['id']]['production_status']
        pending = [dep for dep in row['deps'] if states[dep]['production_status'] not in accepted]
        ready = not pending and status == 'planned'
        if not args.all and not ready: continue
        shown += 1
        flag = 'READY' if ready else status.upper()
        suffix = ' | waiting: '+','.join(pending) if pending else ''
        print(f"{row['id']:8} {flag:12} {row['lane']:12} {row['ticket']} | {row['title']}{suffix}")
    if not shown:
        print('No ready tickets for this filter. Use --all to inspect dependencies. Source research/proof preparation may proceed partially as described in AGENTS.md.')
    print('\nReadiness is an integration aid, not release approval. No workers were started.')
    return 0
if __name__ == '__main__': raise SystemExit(main())
