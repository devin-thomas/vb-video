#!/usr/bin/env bash
# Finish the episode once narration synthesis is complete: QA, second attempts for flagged beats, selection,
# timeline, captions, music plan, effects, review render with the mix, metadata, and the 4K60 master.
# Run from the repository root:  bash tools/assembly/finish.sh
set -euo pipefail
cd "$(dirname "$0")/../.."
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
python tools/assembly/music_plan.py | head -1
python tools/assembly/sfx_cues.py | head -1

echo "== review render with mix"
python tools/assembly/render.py --profile review --music narration/music-plan.json --sfx narration/sfx.json,narration/sfx-music.json | tail -3
python tools/assembly/metadata.py

echo "== master"
python tools/assembly/render.py --profile master --music narration/music-plan.json --sfx narration/sfx.json,narration/sfx-music.json | tail -2
ls -la build/*.mp4
echo "finished"
