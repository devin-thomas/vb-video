"""Build the renderer-neutral editorial timeline (pipeline stage 09, step 3; ASM-03 rules since 2026-09-16).

Reads narration/beats.json and the synthesized takes' durations, maps each beat's cues and code blocks to approved assets,
applies the producer's placement map, and writes narration/timeline.json: an ordered list of segments with start time,
duration, audio file, and the visuals shown during it. A report of every decision goes to assets/ops/ASM-03/exports/report.md.

Rules (Devin's review of the first cut, review/cut-notes-2026-09-16.md):
- One visual per beat. A beat with several cued assets shows the first; the rest carry over one per following cue-less
  beat (a progression, never a rotation). A beat may show two visuals only when it is at least MIN_SPLIT_S long and the
  placement map says so.
- A beat without a cue holds only the LAST visual of the previous beat.
- No return trips: a visual shown within NO_RETURN_S is not shown again unless the placement map or a cue names it.
- Cutdowns land on words: a placement can name a cutdown of a motion asset and the word it must land on; the cutdown's
  key moment (delivery.json variant `key_second`) is aligned to that word using proportional word timing. Until the
  reworked asset exists the current export is used and the slot is marked pending in the report.
- A stock clip never freezes: archive clips loop inside their slot (render.py); motion assets play and hold their poster.
- A section opens with its chapter card; the end card closes; the cold open shows the code scroll-through.

  python tools/assembly/build_timeline.py          # writes narration/timeline.json and the report, prints coverage
"""
from __future__ import annotations
import csv, json, re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BEATS = ROOT / "narration/beats.json"
TAKES = ROOT / "narration/takes"
OUT = ROOT / "narration/timeline.json"
REPORT = ROOT / "assets/ops/ASM-03/exports/report.md"
LF = "\n"
GAP_BEAT, GAP_SECTION, END_HOLD = 0.45, 0.9, 8.0
NO_RETURN_S, MIN_SPLIT_S, MIN_SLOT_S = 60.0, 12.0, 4.0

manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8")); rows = manifest["tickets"]; by_id = {r["id"]: r for r in rows}
orig = (ROOT / "sources/SCRIPT.md").read_text(encoding="utf-8").split("\n")
inv = {r["id"]: r for r in csv.DictReader((ROOT / "assets/ops/OPS-04/exports/editor-inventory.csv").open(encoding="utf-8"))}

def norm(s: str) -> str: return re.sub(r"\s+", " ", re.sub(r"[`*_\[\]]", "", s)).strip().lower()

cue_text_to_ids = defaultdict(list)
for r in rows:
    for ln in r.get("cues") or []:
        if 0 < ln <= len(orig): cue_text_to_ids[norm(orig[ln - 1])].append(r["id"])
ID_RE = re.compile(r"(?<![A-Z])(?:TERM|CODE|DIA|HIST|XTRA|BROLL|CH|CARD|CMP|FACT|MOCK|REF)-\d{2}(?!\d)")
OVERRIDES = [("73-line C", ["REF-02"]), ("Windows 95 launch footage", ["BROLL-04", "HIST-08"]), ("line 264 highlighted", ["CODE-20"]),
             ("Step-by-step diagram, four panels", ["DIA-08"]), ("Card games that shipped with Windows", ["HIST-19", "HIST-20", "XTRA-18", "XTRA-19"]),
             ("Visual Basic for Mac was never released", ["XTRA-10"]), ("classicvb.org petition", ["XTRA-17"]),
             ("Terminal output scrolling", ["TERM-03"]), ("Title card", ["CARD-01"]), ("Cut to black. End card", ["CARD-02"]),
             ("Side-by-side comparison: TERM-04", ["FACT-08"])]

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

# ------------------------------------------------------------------ the placement map (beat id -> visuals)
# A visual is "ID", ("ID", cutdown, "word or phrase the key moment lands on"), or ("ID", cutdown, None) to start at the beat.
# "hold" keeps the previous beat's last visual. Two visuals in a list split the beat (only when it is long enough).
HOLD = "hold"
PLACE: dict[str, list] = {
    # cold open and rules (Devin: the code scrolling, and the animations at the words)
    "S01-B01": ["TERM-03", ("CARD-01", None, "It was the single most popular")], "S01-B02": [HOLD],
    "S05-B01": [("DIA-02", "deck-hold", None)],
    "S05-B02": [("DIA-15", "riffle", "shuffle it"), ("DIA-02", "alternating-deal", "Deal it evenly")],
    "S05-B03": [("DIA-02", "normal-round", "flip their top card")],
    "S05-B04": [("DIA-02", "single-war", "it's War")],
    "S05-B05": [("DIA-02", "final-hold", None)],
    "S05-B06": ["BROLL-02"],
    # section 4: the Variant and the typo
    "S04-B04": ["CODE-01"], "S04-B06": ["XTRA-06", ("CODE-26", None, "You could just start using")],
    "S04-B07": ["CODE-27"],
    # section 7: ByRef/ByVal demo, the i-to-Rank loop, declarations at the top
    "S07-B05": ["DIA-04"], "S07-B06": [HOLD], "S07-B07": [("CMP-03", "transform", None)], "S07-B08": [HOLD],
    "S07-B12": [("DIA-06", None, None)], "S07-B13": ["CODE-28", ("REF-05", None, "like writing C89")],
    # section 8: queue in three languages, the array-as-queue moments, code on its sentences
    "S08-B01": [("DIA-05", "live-slots", None)], "S08-B02": ["CMP-09"], "S08-B03": [HOLD], "S08-B04": ["CODE-06", "CODE-07"],
    "S08-B05": [("DIA-05", "append", "position Count")], "S08-B06": ["CODE-08"],
    "S08-B07": [("DIA-05", "draw-shift", None), ("DIA-05", "cost", "every card in the hand moves")], "S08-B08": ["CODE-09"], "S08-B09": [HOLD],
    "S08-B10": ["CODE-10", "CMP-05"], "S08-B11": [HOLD], "S08-B12": ["FACT-05"],
    # section 9: no flash, concatenation on its sentence, continuation alone
    "S09-B01": ["DIA-10"], "S09-B02": ["CODE-11", "CODE-12"], "S09-B03": [HOLD], "S09-B04": ["CMP-07"], "S09-B05": ["CODE-14"], "S09-B06": [HOLD],
    "S09-B07": ["CMP-06"], "S09-B08": [HOLD], "S09-B09": ["CMP-08"],
    # section 10: one card at a time, One / Two / Three on their words
    "S10-B01": ["CODE-15"], "S10-B02": [HOLD], "S10-B03": ["CODE-16"], "S10-B04": [("DIA-09", None, "In a normal round")],
    "S10-B05": [HOLD], "S10-B06": ["CODE-17"], "S10-B07": ["CODE-18"], "S10-B08": ["CODE-19"],
    "S10-B09": [("DIA-08", None, "burns up to three")], "S10-B10": [HOLD], "S10-B11": ["CODE-21"], "S10-B12": ["CODE-22"], "S10-B13": [HOLD],
    # section 11: the double war, then the four runs
    "S11-B01": ["TERM-04"], "S11-B02": [("TERM-02", "first-war", None)], "S11-B03": ["FACT-07"], "S11-B04": [HOLD],
    # section 12 (ids after NAR-01 removed the two stage directions): the ending, the endgame panels, the two endgames
    "S12-B01": [("TERM-04", "end", None)], "S12-B02": [HOLD], "S12-B03": [("DIA-08", "endgame", "tie, war")], "S12-B04": ["CODE-20", ("DIA-08", "endgame@27.36", "so both players burned")],
    "S12-B05": [("TERM-02", "end", None)], "S12-B06": [HOLD], "S12-B07": ["FACT-08"], "S12-B08": [HOLD], "S12-B09": [HOLD],
    # section 13: the GUI mockup when the GUI is discussed, games where games are named, no frozen dialog
    "S13-B01": ["HIST-19"], "S13-B02": ["MOCK-01"], "S13-B03": [HOLD], "S13-B04": [HOLD], "S13-B05": [HOLD],
    "S13-B06": ["HIST-20", "XTRA-18"], "S13-B07": ["XTRA-20", "HIST-17"], "S13-B08": ["FACT-06"], "S13-B09": ["MOCK-02", "MOCK-01"],
    "S13-B10": [HOLD], "S13-B11": [HOLD],
    # section 14: each tool on its own name
    "S14-B01": ["XTRA-08"], "S14-B02": ["REF-01"], "S14-B03": [HOLD], "S14-B04": ["HIST-12"], "S14-B05": [HOLD], "S14-B06": [HOLD],
    "S14-B07": [HOLD], "S14-B08": ["HIST-15"], "S14-B09": ["HIST-16"], "S14-B10": [HOLD], "S14-B11": ["DIA-11"],
    # section 15: the Mac, each picture on its sentence, the table row by row
    "S15-B01": ["HIST-21"], "S15-B02": ["XTRA-10"], "S15-B03": ["XTRA-09"], "S15-B04": ["HIST-13"], "S15-B05": [HOLD], "S15-B06": [HOLD],
    "S15-B07": [("HIST-14", None, "NeXT")], "S15-B08": [HOLD], "S15-B09": [HOLD], "S15-B10": [("DIA-12", "row-console", None)],
    "S15-B11": [("DIA-12", "row-gui", None)], "S15-B12": [HOLD], "S15-B13": [("DIA-12", "full", None)],
    # section 16: the quoted lines as code, the petition on "petition"
    "S16-B01": ["DIA-14"], "S16-B02": ["XTRA-14"], "S16-B03": ["CODE-29"], "S16-B04": [HOLD], "S16-B05": ["HIST-03"], "S16-B06": ["BROLL-03"],
    "S16-B07": ["XTRA-15"], "S16-B08": [HOLD], "S16-B09": ["XTRA-16"], "S16-B10": [HOLD], "S16-B11": ["XTRA-17"], "S16-B12": ["DIA-14"],
    "S16-B13": [HOLD], "S16-B14": ["DIA-13"],
    # outro
    "S17-B01": [("TERM-04", "end", None)], "S17-B02": ["TERM-03"], "S17-B03": ["TERM-01"], "S17-B04": ["TERM-03"], "S17-B05": ["CARD-02"], "S17-B06": [HOLD],
}
PLACEMENTS = [  # (asset, section, pattern on the beat's written text) for assets the script discusses without a [VISUAL] line
    ("CMP-01", 6, r"int rank;"), ("FACT-02", 6, r"Dimension"), ("CODE-23", 6, r"Eleven is Jack"), ("CODE-24", 6, r"suit is a single character"),
    ("CMP-02", 7, r"`Sub`"), ("CMP-04", 7, r"Fisher-Yates|Step -1"), ("CODE-07", 8, r"ReDim|NewHand"),
    ("CODE-25", 11, r"Every run is different|final summary"), ("DIA-13", 16, r"ideas it pioneered"),
    ("FACT-01", 2, r"it's an acronym"), ("FACT-04", 2, r"Jet engine"), ("FACT-03", 3, r"Rapid Application Development"),
    ("HIST-09", 3, r"You went to a store"), ("HIST-10", 3, r"Egghead"), ("BROLL-05", 3, r"floppy disks"), ("CODE-01", 4, r"Option Explicit On"),
    ("BROLL-06", 3, r"ran the installer"),
]
def placements_for(beat: dict) -> list[str]:
    return [tid for tid, sec, pat in PLACEMENTS if beat["section"] == sec and re.search(pat, beat["written"])]

RECORDINGS = {"TERM-01": "R1", "TERM-02": "R2", "TERM-05": "R3a", "TERM-06": "R3b", "TERM-03": "R5", "XTRA-06": "R6"}
STILL_CUTDOWNS = {("TERM-04", "end"): "exports/framed-end.png", ("TERM-02", "end"): "exports/framed.png", ("TERM-02", "first-war"): "exports/framed-first-war.png"}

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

def delivery(tid: str) -> dict:
    p = ROOT / by_id[tid]["asset_dir"] / "delivery.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

def visual_record(tid: str, cutdown: str | None = None) -> dict | None:
    r = inv.get(tid)
    if not r or r["release_eligibility"] != "cleared": return None
    d = ROOT / by_id[tid]["asset_dir"]; pending = None
    if cutdown == "poster" and (d / "exports/poster.png").is_file():
        return {"id": tid, "kind": r["kind"], "file": f"{by_id[tid]['asset_dir']}/exports/poster.png", "duration": None, "segment": "", "still": True, "in_out": None, "poster": None, "cutdown": "poster", "key_second": 0.0, "pending": None}
    if cutdown and (tid, cutdown) in STILL_CUTDOWNS:
        f = f"{by_id[tid]['asset_dir']}/{STILL_CUTDOWNS[(tid, cutdown)]}"
        if not (ROOT / f).is_file(): pending = f"{tid}:{cutdown} (missing {f})"; f = r["primary_file"]
        return {"id": tid, "kind": r["kind"], "file": f, "duration": None, "segment": "", "still": f.endswith(".png"), "in_out": None, "poster": None,
                "cutdown": cutdown, "key_second": 0.0, "pending": pending}
    offset = 0.0
    if cutdown and "@" in cutdown: cutdown, off = cutdown.split("@", 1); offset = float(off)
    rec = recording_for(tid)
    if rec and not cutdown: return rec
    if rec: rec.update({"cutdown": cutdown, "key_second": 0.0}); return rec
    f = r["primary_file"]; dl = delivery(tid); dur = None; key = 0.0
    if cutdown:
        cf = d / "exports" / f"{cutdown}.mp4"; cp = d / "exports" / f"{cutdown}.png"
        var = next((v for v in dl.get("variants", []) if v.get("name") == cutdown), None)
        if cf.is_file(): f = f"{by_id[tid]['asset_dir']}/exports/{cutdown}.mp4"; key = float((var or {}).get("key_second") or 0.0)
        elif cp.is_file(): f = f"{by_id[tid]['asset_dir']}/exports/{cutdown}.png"
        else: pending = f"{tid}:{cutdown} (not delivered yet; using {f.split('/')[-1]})"
    if f.endswith(".mp4") and "/exports/" in f:
        if f.endswith("preview.mp4"): dur = float(dl.get("duration_seconds") or 0) or None
        else:
            var = next((v for v in dl.get("variants", []) if v.get("name") == cutdown), None)
            dur = float((var or {}).get("duration_seconds") or 0) or probe(ROOT / f)
    seg = r.get("segment") or ""
    m = re.findall(r"(\d+:\d\d(?:\.\d+)?|\d+\.\d+)", seg)
    poster = f"{by_id[tid]['asset_dir']}/exports/poster.png" if (d / "exports/poster.png").is_file() else None
    if offset: key = 0.0; dur = (dur - offset) if dur else dur
    return {"id": tid, "kind": r["kind"], "file": f, "duration": dur, "segment": seg, "still": f.endswith(".png"),
            "in_out": m[:2] if f.endswith(".mp4") and "/source/" in f else None, "poster": poster, "cutdown": cutdown, "key_second": key, "offset": offset, "pending": pending}

def probe(path: Path) -> float | None:
    import subprocess
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except ValueError: return None

SELECTION = json.loads((ROOT / "narration/selection.json").read_text(encoding="utf-8")) if (ROOT / "narration/selection.json").exists() else {}
def take_attempt(beat_id: str) -> str:
    return f"{SELECTION.get(beat_id, {}).get('attempt', 1):02d}"
def take_duration(beat_id: str) -> float | None:
    p = TAKES / beat_id / take_attempt(beat_id) / "metadata.json"
    return json.loads(p.read_text(encoding="utf-8"))["duration_s"] if p.exists() else None

def hold_of(v: dict) -> dict:
    """What a following beat shows when it holds `v`: a still stays; a motion asset or recording shows its end state (the poster)
    rather than replaying from the start (Devin: animations must not repeat)."""
    h = dict(v); h.pop("slot", None)
    if not v.get("still") and v.get("kind") != "archive":
        still = visual_record(v["id"], "poster") if v.get("cutdown") != "poster" else None
        if still: return still
        if v.get("poster"): return dict(h, file=v["poster"], still=True, duration=None, in_out=None, cutdown="poster", key_second=0.0)
    return h

def word_time(beat: dict, dur: float, phrase: str | None) -> float:
    """Seconds into the beat at which `phrase` is spoken (proportional word timing, as captions.py uses)."""
    if not phrase: return 0.0
    words = re.sub(r"\*\*|`", "", beat["written"]).split(); n = len(words)
    target = re.sub(r"\*\*|`", "", phrase).split()
    for i in range(n - len(target) + 1):
        if [re.sub(r"[^\w']", "", w).lower() for w in words[i:i + len(target)]] == [re.sub(r"[^\w']", "", w).lower() for w in target]:
            return dur * i / n
    return 0.0

def main() -> int:
    beats = json.loads(BEATS.read_text(encoding="utf-8"))["beats"]
    segments, t, last_section, last_visual = [], 0.0, None, None
    missing_audio, unmapped, report, pending, overflow = [], [], [], [], []
    last_seen: dict[str, float] = {}
    for b in beats:
        if b["section"] != last_section:
            ch = f"CH-{b['section']:02d}"; overflow = []
            if ch in inv and b["section"] <= 16:
                v = visual_record(ch)
                segments.append({"kind": "chapter", "id": ch, "start": round(t, 3), "duration": round(v["duration"] or 3.0, 3), "audio": None, "visuals": [v]})
                t += (v["duration"] or 3.0); last_seen[ch] = t
            elif last_section is not None:
                t += GAP_SECTION
            last_section = b["section"]
        dur = take_duration(b["id"])
        if dur is None: missing_audio.append(b["id"]); dur = b["words"] / 2.6
        specs: list[tuple] = []; source = ""
        if b["id"] in PLACE:
            source = "placement map"
            for item in PLACE[b["id"]]:
                if item == HOLD: specs.append((HOLD, None, None))
                elif isinstance(item, str): specs.append((item, None, None))
                else: specs.append(tuple(item))
        else:
            ids = []
            for cue in b["cues"]:
                got = ids_for_cue(cue)
                if not got: unmapped.append((b["id"], cue[:80]))
                ids += got
            for block in b["code"]: ids += ids_for_code(block)
            ids += placements_for(b)
            seen, ordered = set(), []
            for i in ids:
                if i not in seen and visual_record(i): seen.add(i); ordered.append(i)
            if ordered:
                source = "cue"; specs = [(ordered[0], None, None)]; overflow = ordered[1:] + overflow
            elif overflow:
                source = "cue overflow"; specs = [(overflow.pop(0), None, None)]
            else:
                source = "hold"; specs = [(HOLD, None, None)]
        # resolve specs into visuals with slots
        visuals = []
        for tid, cutdown, phrase in specs:
            if tid == HOLD:
                v = hold_of(last_visual) if last_visual else visual_record("CARD-01"); visuals.append((v, 0.0)); continue
            v = visual_record(tid, cutdown)
            if not v: report.append(f"- {b['id']}: {tid} is not cleared or has no record; skipped"); continue
            if v.get("pending"): pending.append(f"{b['id']}: {v['pending']}")
            start_at = max(0.0, word_time(b, dur, phrase) - float(v.get("key_second") or 0.0)) if phrase else 0.0
            visuals.append((v, start_at))
        if not visuals: visuals = [(hold_of(last_visual) if last_visual else visual_record("CARD-01"), 0.0)]
        # no-return guard for cue-derived choices (the placement map may name anything)
        if source == "cue overflow":
            v, s = visuals[0]
            if v["id"] in last_seen and t - last_seen[v["id"]] < NO_RETURN_S and last_visual and v["id"] != last_visual["id"]:
                report.append(f"- {b['id']}: {v['id']} shown {t - last_seen[v['id']]:.0f} s ago without a cue naming it; holding {last_visual['id']} instead")
                visuals = [(hold_of(last_visual), 0.0)]; source = "hold (no-return guard)"
        # a second visual needs room; a word-timed first visual starts where the word is, the previous visual fills the lead
        if len(visuals) > 1 and dur < MIN_SPLIT_S and source != "placement map":
            report.append(f"- {b['id']}: {dur:.1f} s is too short for two visuals; keeping {visuals[0][0]['id']} only"); visuals = visuals[:1]
        out = []
        if visuals[0][1] > MIN_SLOT_S / 2 and last_visual:
            out.append((hold_of(last_visual), 0.0))
        else:
            visuals[0] = (visuals[0][0], 0.0)  # a key moment within 2 s of the beat start just starts with the beat
        out += visuals
        # slots: each visual runs from its start to the next visual's start; unstarted visuals split the remainder equally
        starts = [s for _, s in out]; n = len(out)
        for i in range(1, n):
            if starts[i] <= starts[i - 1]: starts[i] = starts[i - 1] + (dur - starts[i - 1]) / (n - i + 1)
        slots = [round((starts[i + 1] if i + 1 < n else dur) - starts[i], 3) for i in range(n)]
        vis_out = [dict(v, slot=slots[i]) for i, (v, _) in enumerate(out)]
        for v in vis_out: v.pop("pending", None)
        segments.append({"kind": "beat", "id": b["id"], "section": b["section"], "start": round(t, 3), "duration": round(dur, 3),
                         "audio": f"narration/takes/{b['id']}/{take_attempt(b['id'])}/native-audio.wav" if take_duration(b["id"]) else None,
                         "written": b["written"], "visuals": vis_out, "held": source.startswith("hold")})
        report.append(f"| {int(t // 60)}:{int(t % 60):02d} | {b['id']} | {dur:.1f} | {source} | " + ", ".join(f"{v['id']}{':' + v['cutdown'] if v.get('cutdown') else ''} ({v['slot']:.1f} s)" for v in vis_out) + " |")
        for v in vis_out: last_seen[v["id"]] = t + dur
        t += dur + GAP_BEAT; last_visual = vis_out[-1]
    end = visual_record("CARD-02")
    segments.append({"kind": "end", "id": "CARD-02", "start": round(t, 3), "duration": END_HOLD, "audio": None, "visuals": [end]})
    t += END_HOLD
    used = sorted({v["id"] for s in segments for v in s["visuals"] if v})
    cleared = sorted(i for i, r in inv.items() if r["release_eligibility"] == "cleared")
    unused = [i for i in cleared if i not in used]
    data = {"generated": "2026-09-16", "total_seconds": round(t, 1), "fps_review": 60, "size_review": [1920, 1080], "size_master": [3840, 2160],
            "segments": segments, "assets_used": used, "assets_unused": unused, "beats_without_audio": missing_audio, "unmapped_cues": unmapped, "pending_cutdowns": pending}
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + LF, encoding="utf-8", newline=LF)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    notes = [l for l in report if l.startswith("- ")]; table = [l for l in report if l.startswith("| ")]
    REPORT.write_text("# ASM-03 timeline report" + LF + LF + f"{len(segments)} segments, {t/60:.1f} min, assets used {len(used)}/{len(cleared)}, beats without audio {len(missing_audio)}, unmapped cues {len(unmapped)}." + LF + LF
                      + "## Pending cutdowns (asset not delivered yet; current export used)" + LF + LF + (LF.join(f"- {p}" for p in pending) or "- none") + LF + LF
                      + "## Decisions and guards" + LF + LF + (LF.join(notes) or "- none") + LF + LF + "## Every beat" + LF + LF + "| time | beat | s | source | visuals |" + LF + "|---|---|---|---|---|" + LF + LF.join(table) + LF
                      + LF + "## Unused cleared assets" + LF + LF + (", ".join(unused) or "none") + LF, encoding="utf-8", newline=LF)
    print(f"segments {len(segments)}, running time {t/60:.1f} min, assets used {len(used)}/{len(cleared)}, beats without audio {len(missing_audio)}, unmapped cues {len(unmapped)}, pending cutdowns {len(pending)}")
    if unused: print("unused:", ", ".join(unused))
    for u in unmapped[:10]: print("unmapped:", u)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
