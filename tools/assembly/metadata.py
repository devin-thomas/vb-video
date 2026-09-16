"""Publication metadata from the finished timeline (handoff H07, pipeline stage 09 step 8).

Writes build/upload-metadata.md with the title, description (script block plus credits), tags, chapters at the real
chapter-card times from narration/timeline.json, and the checklist. Nothing is uploaded.

  python tools/assembly/metadata.py
"""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIMELINE = ROOT / "narration/timeline.json"
SCRIPT = ROOT / "War/SCRIPT.md"
EXC = ROOT / "assets/ops/OPS-04/exports/exceptions.md"
OUT = ROOT / "build/upload-metadata.md"
LF = "\n"
TITLES = {1: "Intro: What Even Is Visual Basic?", 2: "A Very Brief History of BASIC to Visual Basic", 3: "The Toolchain: What You Actually Installed",
          4: "How We're Doing This Today", 5: "The Card Game War: Rules in 60 Seconds", 6: "Modeling a Card in VB", 7: "Building and Shuffling the Deck",
          8: "The Player's Hand: Arrays as Queues", 9: "The Game Loop", 10: "War! The Recursion Within the Loop", 11: "Running It: Full Simulation",
          12: "When the Cards Run Out", 13: "What This Code Would Have Become", 14: "VB vs. The Competition in 1995", 15: "What If You Were on a Mac?",
          16: "Why VB Mattered (and Why It Died)", 17: "Outro"}

def mmss(t: float) -> str:
    m, s = divmod(int(round(t)), 60); return f"{m}:{s:02d}"

def main() -> int:
    tl = json.loads(TIMELINE.read_text(encoding="utf-8"))
    script = SCRIPT.read_text(encoding="utf-8").split("\n")
    meta = script[next(i for i, l in enumerate(script) if l.startswith("## Video Metadata")): next(i for i, l in enumerate(script) if l.startswith("## SECTION 1"))]
    titles, desc, tags, mode = [], [], "", None
    for l in meta:
        if l.startswith("**Title Options"): mode = "t"; continue
        if l.startswith("**Description"): mode = "d"; continue
        if l.startswith("**Tags"): mode = "g"; continue
        if l.startswith("**Chapters"): mode = "c"; continue
        if mode == "t" and re.match(r"^\d+\. ", l.strip()): titles.append(re.sub(r"^\d+\. ", "", l.strip()))
        elif mode == "d" and l.strip(): desc.append(l.strip())
        elif mode == "g" and l.strip(): tags = l.strip()
    chapters = []
    seen = set()
    for seg in tl["segments"]:
        if seg["kind"] == "chapter":
            n = int(seg["id"][3:]); chapters.append((seg["start"], TITLES[n]))
        elif seg["kind"] == "beat" and seg["section"] == 17 and 17 not in seen:
            seen.add(17); chapters.append((seg["start"], TITLES[17]))
    if chapters and chapters[0][0] > 0: chapters[0] = (0.0, chapters[0][1])
    credits = EXC.read_text(encoding="utf-8").split("## Credits to carry")[1].strip().split("\n") if EXC.exists() else []
    credits = [c for c in credits if c.startswith("- ")]
    out = [f"# Upload metadata (generated from the timeline, {tl['total_seconds']/60:.1f} min)", "", "## Title", "", titles[0] if titles else "", "",
           "## Description", ""] + desc + ["", "Chapters:"] + [f"{mmss(t)} {name}" for t, name in chapters] + ["", "Credits:"] + [re.sub(r"\*\*|—", "", c[2:]).strip() for c in credits] + ["",
           "Narration: synthesized with Qwen3-TTS (speaker Aiden), an open model run locally. The program, script and every production asset are in the public repository linked above.", "",
           "## Tags", "", tags, "", "## Chapters (YouTube format)", ""] + [f"{mmss(t)} {name}" for t, name in chapters] + ["",
           "## Checklist", "", "- [ ] Music credit added if the bed's terms need one", "- [ ] Thumbnail chosen (CARD-01 poster is a usable base)",
           "- [ ] Visibility, audience and disclosure settings chosen deliberately", "- [ ] Captions file build/captions.srt uploaded", ""]
    OUT.parent.mkdir(exist_ok=True); OUT.write_text(LF.join(out), encoding="utf-8", newline=LF)
    print(f"{len(chapters)} chapters -> {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
