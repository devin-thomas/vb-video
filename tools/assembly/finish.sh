#!/usr/bin/env bash
# Finish the episode once narration synthesis is complete: QA, second attempts for flagged beats, selection,
# timeline, captions, music plan, effects, review render with the mix, metadata, and the 4K60 master.
# Run from the repository root:  bash tools/assembly/finish.sh
set -euo pipefail
cd "$(dirname "$0")/../.."

# Guard: one run at a time, and no accidental repeat. A second invocation while build/.finish.lock names a live
# process exits quietly; once build/master-2160p60.mp4 exists and is newer than narration/selection.json the chain is
# considered finished and exits unless called with --force (or the master is deleted).
LOCK="build/.finish.lock"; FORCE=0; [ "${1:-}" = "--force" ] && FORCE=1
if [ -f "$LOCK/pid" ]; then
  p=$(cat "$LOCK/pid")
  if tasklist //FI "PID eq $p" 2>/dev/null | grep -q " $p "; then echo "finish.sh: another run (pid $p) holds $LOCK; not starting"; exit 0; fi
  rm -rf "$LOCK"
fi
if [ "$FORCE" = 0 ] && [ -f build/master-2160p60.mp4 ] && [ build/master-2160p60.mp4 -nt narration/selection.json ]; then
  echo "finish.sh: already finished (build/master-2160p60.mp4 is newer than narration/selection.json); pass --force to redo"; exit 0
fi
mkdir -p "$LOCK"; echo $$ > "$LOCK/pid"; trap 'rm -rf "$LOCK"' EXIT
ASR="E:/local-llm/models/narration-tts/envs/asr/Scripts/python.exe"
export PYTHONIOENCODING=utf-8

echo "== QA on every take"
"$ASR" tools/narration/qa.py 2>&1 | grep -v -i warning | tail -3
python tools/narration/select.py | tail -4

echo "== second attempts for flagged beats"
FLAGGED=$(python -c "
import json; s=json.load(open('narration/selection.json',encoding='utf-8'))
print(','.join(b for b,v in s.items() if v['flags']))")
if [ -n "$FLAGGED" ]; then
  echo "regenerating: $FLAGGED"
  python tools/narration/synth.py --attempt 2 --only "$FLAGGED" | tail -2
  "$ASR" tools/narration/qa.py --attempt 2 --only "$FLAGGED" 2>&1 | grep -v -i warning | tail -2
  python tools/narration/select.py | tail -6
fi

echo "== timeline, captions, music, effects"
python tools/assembly/build_timeline.py
python tools/assembly/captions.py
python tools/assembly/music_plan.py
python tools/assembly/sfx_cues.py

echo "== review render with mix"
python tools/assembly/render.py --profile review --music narration/music-plan.json --sfx narration/sfx.json,narration/sfx-music.json | tail -3
python tools/assembly/metadata.py

echo "== master"
python tools/assembly/render.py --profile master --music narration/music-plan.json --sfx narration/sfx.json,narration/sfx-music.json | tail -2
ls -la build/*.mp4
echo "finished"
