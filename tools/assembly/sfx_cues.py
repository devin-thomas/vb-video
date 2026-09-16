"""Place the three sound effects on the timeline (handoff H04) and write narration/sfx.json for render.py --sfx.

Cues come from the timeline, not from guesses: a shuffle where the shuffle visuals start (DIA-02 rules animation,
DIA-06 Fisher-Yates, BROLL-01), a card slap where a war resolves (DIA-08 first appearance, DIA-09 pot growth, the
war-heavy terminal beat), and the Windows 95 startup sound once, at the launch footage (HIST-08). Files are read
from assets/audio/sfx/ and must exist; missing files are reported and skipped.

  python tools/assembly/sfx_cues.py
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIMELINE = ROOT / "narration/timeline.json"
OUT = ROOT / "narration/sfx.json"
SFX_DIR = ROOT / "assets/audio/sfx"
LF = "\n"
FILES = {"shuffle": "card-shuffle.wav", "slap": "card-slap.wav", "win95": "windows95-startup.wav"}
RULES = [  # (effect, asset ids that trigger it, once-only, gain dB)
    ("shuffle", {"DIA-02", "DIA-06", "BROLL-01"}, False, -8),
    ("slap", {"DIA-08", "DIA-09"}, False, -6),
    ("win95", {"HIST-08"}, True, -10),
]

def main() -> int:
    tl = json.loads(TIMELINE.read_text(encoding="utf-8"))
    cues, fired = [], set()
    for seg in tl["segments"]:
        offset = 0.0
        for v in seg["visuals"]:
            if not v: continue
            for effect, ids, once, gain in RULES:
                if v["id"] in ids and not (once and effect in fired) and (effect, v["id"]) not in fired:
                    f = SFX_DIR / FILES[effect]
                    if f.exists():
                        cues.append({"effect": effect, "at": round(seg["start"] + offset, 3), "file": f"assets/audio/sfx/{FILES[effect]}", "gain_db": gain, "trigger": f"{seg['id']}:{v['id']}"})
                    else:
                        print(f"[missing] {f} for {effect} at {seg['id']}")
                    fired.add((effect, v["id"]))
                    if once: fired.add(effect)
            offset += v.get("slot", seg["duration"])
    OUT.write_text(json.dumps(cues, indent=1) + LF, encoding="utf-8", newline=LF)
    print(f"{len(cues)} cues -> {OUT}")
    for c in cues: print(f"  {c['at']:8.1f}s {c['effect']:8s} {c['trigger']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
