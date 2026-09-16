"""Captions and transcript from the timeline (pipeline stage 09, release package).

Each narration beat becomes caption cues of at most two lines, timed proportionally by word count across the
beat's real audio duration. The written text (with code tokens as written, not the spoken form) is what appears.
Writes build/captions.srt, build/captions.vtt and build/transcript.md.

  python tools/assembly/captions.py
"""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIMELINE = ROOT / "narration/timeline.json"
BUILD = ROOT / "build"
LF = "\n"
MAX_CHARS = 84  # two lines of ~42

def chunks(text: str) -> list[str]:
    text = re.sub(r"\*\*|`", "", text)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out, cur = [], ""
    for s in sentences:
        words = s.split()
        while words:
            take = words[:]
            while len(" ".join(take)) > MAX_CHARS and len(take) > 1:
                take = take[:-1]
            piece = " ".join(take); words = words[len(take):]
            if cur and len(cur) + 1 + len(piece) <= MAX_CHARS: cur = cur + " " + piece
            else:
                if cur: out.append(cur)
                cur = piece
    if cur: out.append(cur)
    return out

def two_lines(s: str) -> str:
    if len(s) <= 42: return s
    words = s.split(); best, best_diff = None, 10**9
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        if len(a) <= 46 and len(b) <= 46 and abs(len(a) - len(b)) < best_diff: best, best_diff = (a, b), abs(len(a) - len(b))
    return f"{best[0]}{LF}{best[1]}" if best else s

def ts(t: float, vtt=False) -> str:
    h, m = int(t // 3600), int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", "," if not vtt else ".")

def main() -> int:
    tl = json.loads(TIMELINE.read_text(encoding="utf-8"))
    cues, transcript = [], ["# Transcript", ""]
    section = None
    for seg in tl["segments"]:
        if seg["kind"] != "beat": continue
        if seg["section"] != section:
            section = seg["section"]; transcript += [f"## Section {section}", ""]
        parts = chunks(seg["written"]); total = sum(len(p.split()) for p in parts) or 1
        t = seg["start"]
        for p in parts:
            d = seg["duration"] * len(p.split()) / total
            cues.append((t, min(t + d, seg["start"] + seg["duration"]) - 0.05, two_lines(p))); t += d
        transcript.append(re.sub(r"\*\*", "", seg["written"])); transcript.append("")
    BUILD.mkdir(exist_ok=True)
    (BUILD / "captions.srt").write_text("".join(f"{i}{LF}{ts(a)} --> {ts(b)}{LF}{txt}{LF}{LF}" for i, (a, b, txt) in enumerate(cues, 1)), encoding="utf-8", newline=LF)
    (BUILD / "captions.vtt").write_text("WEBVTT" + LF + LF + "".join(f"{ts(a, True)} --> {ts(b, True)}{LF}{txt}{LF}{LF}" for a, b, txt in cues), encoding="utf-8", newline=LF)
    (BUILD / "transcript.md").write_text(LF.join(transcript), encoding="utf-8", newline=LF)
    print(f"{len(cues)} caption cues, transcript {sum(len(l.split()) for l in transcript)} words")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
