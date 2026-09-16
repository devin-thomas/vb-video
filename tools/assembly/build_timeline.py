"""Build the renderer-neutral editorial timeline (pipeline stage 09, step 3).

Reads narration/beats.json and the synthesized takes' durations, maps each beat's preceding visual cues and code
blocks to approved assets (the same mapping the H05 assembly plan uses), and writes narration/timeline.json:
an ordered list of segments with start time, duration, audio file, and the visuals shown during it.

Rules: a section opens with its chapter card as a silent segment; a beat with no cue keeps the previous visual;
a beat with several cues splits its time equally between them in order; a motion asset shorter than its slot holds
its last frame; the cold open's terminal cue and the title card come from the script itself; the end card closes.

  python tools/assembly/build_timeline.py          # writes narration/timeline.json and prints coverage
"""
from __future__ import annotations
import csv, json, re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BEATS = ROOT / "narration/beats.json"
TAKES = ROOT / "narration/takes"
OUT = ROOT / "narration/timeline.json"
LF = "\n"
GAP_BEAT, GAP_SECTION, END_HOLD = 0.45, 0.9, 8.0

manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8")); rows = manifest["tickets"]; by_id = {r["id"]: r for r in rows}
orig = (ROOT / "sources/SCRIPT.md").read_text(encoding="utf-8").split("\n")
inv = {r["id"]: r for r in csv.DictReader((ROOT / "assets/ops/OPS-04/exports/editor-inventory.csv").open(encoding="utf-8"))}

def norm(s: str) -> str: return re.sub(r"\s+", " ", re.sub(r"[`*_\[\]]", "", s)).strip().lower()

cue_text_to_ids = defaultdict(list)
for r in rows:
    for ln in r.get("cues") or []:
        if 0 < ln <= len(orig): cue_text_to_ids[norm(orig[ln - 1])].append(r["id"])
ID_RE = re.compile(r"(?<![A-Z])(?:TERM|CODE|DIA|HIST|XTRA|BROLL|CH|CARD|CMP|FACT|MOCK|REF)-\d{2}(?!\d)")
OVERRIDES = [("73-line C", ["REF-02"]), ("Windows 95 launch footage", ["HIST-08", "BROLL-04"]), ("line 264 highlighted", ["CODE-20"]),
             ("Step-by-step diagram, four panels", ["DIA-08"]), ("Card games that shipped with Windows", ["HIST-19", "HIST-20", "XTRA-18", "XTRA-19"]),
             ("Visual Basic for Mac was never released", ["XTRA-10"]), ("classicvb.org petition", ["XTRA-17"]),
             ("Terminal output scrolling", ["TERM-04"]), ("Title card", ["CARD-01"]), ("Cut to black. End card", ["CARD-02"])]

def ids_for_cue(text: str) -> list[str]:
    for key, ids in OVERRIDES:
        if key in text: return ids
    named = sorted(set(ID_RE.findall(text)))
    if named: return named
    ids = cue_text_to_ids.get(norm("**[VISUAL: " + text + "]**"))
    if ids: return sorted(set(ids))
    head = norm(text)[:40]
    hits = [v for k, v in cue_text_to_ids.items() if head and head in k]
    return sorted({i for h in hits for i in h})

code_index = {norm(r["copy"].strip().split("\n")[0]): r["id"] for r in rows if r["kind"] == "code" and r.get("copy")}
def ids_for_code(block: str) -> list[str]:
    first = norm(block.strip().split("\n")[0])
    if first in code_index: return [code_index[first]]
    for k, v in code_index.items():
        if k and (k in norm(block) or first in k): return [v]
    return []

PLACEMENTS = [  # (asset, section, pattern on the beat's written text) for assets the script discusses without a [VISUAL] line
    ("CMP-01", 6, r"int rank;"), ("FACT-02", 6, r"Dimension"), ("CODE-23", 6, r"Eleven is Jack"), ("CODE-24", 6, r"suit is a single character"),
    ("CMP-02", 7, r"`Sub`"), ("CMP-03", 7, r"Next Rank"), ("CMP-04", 7, r"Fisher-Yates|Step -1"),
    ("CODE-07", 8, r"ReDim|NewHand"), ("CMP-05", 8, r"return Top;|assign to the function"), ("FACT-05", 8, r"old-school BASIC heritage"),
    ("CODE-12", 9, r"alternating cards"), ("CMP-07", 9, r"`Do While"), ("CODE-14", 9, r"safety valve"), ("CMP-08", 9, r"line continuation|underscore"),
    ("CODE-25", 11, r"Every run is different|final summary"), ("FACT-06", 13, r"bundle the runtime|megabyte-plus"), ("BROLL-06", 3, r"ran the installer"),
    ("DIA-11", 14, r"sweet spot"), ("DIA-13", 16, r"ideas it pioneered"), ("HIST-03", 16, r"VB6, released in 1998"),
    ("FACT-01", 2, r"it's an acronym"), ("FACT-04", 2, r"Jet engine"), ("FACT-03", 3, r"Rapid Application Development"),
    ("HIST-09", 3, r"You went to a store"), ("HIST-10", 3, r"Egghead"), ("BROLL-05", 3, r"floppy disks"), ("CODE-01", 4, r"Option Explicit On"),
    ("BROLL-01", 5, r"shuffle it"), ("BROLL-02", 5, r"flip their top card"), ("BROLL-03", 16, r"banks, hospitals"), ("TERM-03", 17, r"code is straightforward"),
]
def placements_for(beat: dict) -> list[str]:
    return [tid for tid, sec, pat in PLACEMENTS if beat["section"] == sec and re.search(pat, beat["written"])]

RECORDINGS = {"TERM-01": "R1", "TERM-02": "R2", "TERM-05": "R3a", "TERM-06": "R3b", "TERM-03": "R5", "XTRA-06": "R6"}
def recording_for(tid: str) -> dict | None:
    take = RECORDINGS.get(tid)
    if tid == "TERM-04":
        sel = ROOT / "recordings/R4-selected.json"
        take = json.loads(sel.read_text(encoding="utf-8")).get("selected") if sel.exists() else None
    if not take: return None
    f = ROOT / "recordings" / take / "take.mp4"; meta = ROOT / "recordings" / take / "take.json"
    if not f.exists() or not meta.exists(): return None
    return {"id": tid, "kind": "recording", "file": f"recordings/{take}/take.mp4", "duration": json.loads(meta.read_text(encoding="utf-8"))["seconds"],
            "segment": "", "still": False, "in_out": None, "recording": take, "poster": inv[tid]["primary_file"]}

def visual_record(tid: str) -> dict | None:
    r = inv.get(tid)
    if not r or r["release_eligibility"] != "cleared": return None
    rec = recording_for(tid)
    if rec: return rec
    f = r["primary_file"]; d = ROOT / by_id[tid]["asset_dir"]
    dur = None
    if f.endswith(".mp4") and "/exports/" in f:
        dl = json.loads((d / "delivery.json").read_text(encoding="utf-8")); dur = float(dl.get("duration_seconds") or 0) or None
    seg = r.get("segment") or ""
    m = re.findall(r"(\d+:\d\d(?:\.\d+)?|\d+\.\d+)", seg)
    poster = f"{by_id[tid]['asset_dir']}/exports/poster.png" if (d / "exports/poster.png").is_file() else None
    return {"id": tid, "kind": r["kind"], "file": f, "duration": dur, "segment": seg, "still": f.endswith(".png"),
            "in_out": m[:2] if f.endswith(".mp4") and "/source/" in f else None, "poster": poster}

SELECTION = json.loads((ROOT / "narration/selection.json").read_text(encoding="utf-8")) if (ROOT / "narration/selection.json").exists() else {}
def take_attempt(beat_id: str) -> str:
    return f"{SELECTION.get(beat_id, {}).get('attempt', 1):02d}"
def take_duration(beat_id: str) -> float | None:
    p = TAKES / beat_id / take_attempt(beat_id) / "metadata.json"
    return json.loads(p.read_text(encoding="utf-8"))["duration_s"] if p.exists() else None

def main() -> int:
    beats = json.loads(BEATS.read_text(encoding="utf-8"))["beats"]
    segments, t, last_section, last_visuals = [], 0.0, None, []
    missing_audio, unmapped = [], []
    for b in beats:
        if b["section"] != last_section:
            ch = f"CH-{b['section']:02d}"
            if ch in inv and b["section"] <= 16:
                v = visual_record(ch)
                segments.append({"kind": "chapter", "id": ch, "start": round(t, 3), "duration": round(v["duration"] or 3.0, 3), "audio": None, "visuals": [v]})
                t += (v["duration"] or 3.0)
            elif last_section is not None:
                t += GAP_SECTION
            last_section = b["section"]
        dur = take_duration(b["id"])
        if dur is None: missing_audio.append(b["id"]); dur = b["words"] / 2.6
        ids = []
        for cue in b["cues"]:
            got = ids_for_cue(cue)
            if not got: unmapped.append((b["id"], cue[:80]))
            ids += got
        for block in b["code"]:
            ids += ids_for_code(block)
        ids += placements_for(b)
        seen, ordered = set(), []
        for i in ids:
            if i not in seen and visual_record(i): seen.add(i); ordered.append(i)
        visuals = [visual_record(i) for i in ordered] or list(last_visuals)
        if not visuals: visuals = [visual_record("CARD-01")]
        share = dur / len(visuals)
        segments.append({"kind": "beat", "id": b["id"], "section": b["section"], "start": round(t, 3), "duration": round(dur, 3),
                         "audio": f"narration/takes/{b['id']}/{take_attempt(b['id'])}/native-audio.wav" if take_duration(b["id"]) else None,
                         "written": b["written"], "visuals": [dict(v, slot=round(share, 3)) for v in visuals], "held": not ordered})
        t += dur + GAP_BEAT; last_visuals = visuals
    end = visual_record("CARD-02")
    segments.append({"kind": "end", "id": "CARD-02", "start": round(t, 3), "duration": END_HOLD, "audio": None, "visuals": [end]})
    t += END_HOLD
    used = sorted({v["id"] for s in segments for v in s["visuals"] if v})
    cleared = sorted(i for i, r in inv.items() if r["release_eligibility"] == "cleared")
    unused = [i for i in cleared if i not in used]
    data = {"generated": "2026-09-15", "total_seconds": round(t, 1), "fps_review": 60, "size_review": [1920, 1080], "size_master": [3840, 2160],
            "segments": segments, "assets_used": used, "assets_unused": unused, "beats_without_audio": missing_audio, "unmapped_cues": unmapped}
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + LF, encoding="utf-8", newline=LF)
    print(f"segments {len(segments)}, running time {t/60:.1f} min, assets used {len(used)}/{len(cleared)}, beats without audio {len(missing_audio)}, unmapped cues {len(unmapped)}")
    if unused: print("unused:", ", ".join(unused))
    for u in unmapped[:10]: print("unmapped:", u)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
