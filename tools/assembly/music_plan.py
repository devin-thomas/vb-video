"""Turn Devin's music keeps into a bed plan over the timeline (handoff H03).

Copies the chosen source files into assets/audio/music/ with a provenance record, then writes narration/music-plan.json
for render.py --music: one bed per section range, with gains, plus the chapter transition sting as extra sfx cues in
narration/sfx-music.json (2038 D.M.G. for at most 8 seconds over each chapter card, per Devin's note).

  python tools/assembly/music_plan.py
"""
from __future__ import annotations
import hashlib, json, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIMELINE = ROOT / "narration/timeline.json"
OUT_DIR = ROOT / "assets/audio/music"; OUT_DIR.mkdir(parents=True, exist_ok=True)
SCRATCH = Path(r"C:\Users\lilgo\AppData\Local\Temp\claude\C--dev-youtube-vb-video-checkout-2\2037dbba-382e-4fa6-be2a-d732946c5260\scratchpad")
LF = "\n"

SOURCES = {  # key -> (source file, title, artist, licence, page)
    "shady": (SCRATCH / "music2/src/ognomo-flac/oGnomo - Chiptune Collection - 03 Shady Business (YM2612).flac", "Shady Business (YM2612)", "ognomo", "CC0 (Bandcamp)", "https://ognomo.bandcamp.com/album/chiptune-collection"),
    "dmg": (SCRATCH / "music2/src/ognomo-flac/oGnomo - Chiptune Collection - 05 2038 D.M.G. (GameBoy).flac", "2038 D.M.G. (Gameboy)", "ognomo", "CC0 (Bandcamp)", "https://ognomo.bandcamp.com/album/chiptune-collection"),
    "crypto": (SCRATCH / "music2/src/ognomo-flac/oGnomo - Chiptune Collection - 06 Cryptosphere (GameBoy).flac", "Cryptosphere (Gameboy)", "ognomo", "CC0 (Bandcamp)", "https://ognomo.bandcamp.com/album/chiptune-collection"),
    "gravebyte": (SCRATCH / "music2/src/ognomo-flac/oGnomo - Chiptune Collection - 07 Gravebyte (GameBoy).flac", "Gravebyte (Gameboy)", "ognomo", "CC0 (Bandcamp)", "https://ognomo.bandcamp.com/album/chiptune-collection"),
    "hexel": (SCRATCH / "music2/src/ognomo-flac/oGnomo - Chiptune Collection - 09 Hexel (GameBoy).flac", "Hexel (Gameboy)", "ognomo", "CC0 (Bandcamp)", "https://ognomo.bandcamp.com/album/chiptune-collection"),
    "auldjack": (SCRATCH / "music2/src/free_vgms/auld_jack.wav", "Auld Jack", "Safety Stoat Studios", "CC0 1.0 (github.com/jerellsworth/free_vgms LICENSE)", "https://safetystoatstudios.itch.io/free-vgms"),
    "chipper": (SCRATCH / "music/src/1-chipper-doodle-v2.mp3", "Chipper Doodle v2", "Kevin MacLeod", "CC BY 4.0 (incompetech.com)", "https://incompetech.com/music/royalty-free/music.html"),
}
# section ranges -> bed key and gain (dB relative to the loudness-matched bed)
PLAN = [
    ((1, 2), "shady", -15, "opening; Devin: let it run a few seconds before the voice, then duck"),
    ((3, 4), "auldjack", -16, "toolchain and setup"),
    ((5, 8), "crypto", -16, "rules, card, deck, hand"),
    ((9, 11), "chipper", -16, "game loop, war, runs"),
    ((12, 13), "gravebyte", -16, "what it would have become, competition"),
    ((14, 15), "crypto", -16, "Mac, why it mattered"),
    ((16, 16), "hexel", -20, "why it died; Devin: spooky, very loud, so 4 dB lower"),
    ((17, 17), "shady", -13, "outro and end card, a touch more forward"),
]

def sha(p: Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> int:
    tl = json.loads(TIMELINE.read_text(encoding="utf-8"))
    starts = {int(s["id"][3:]): s["start"] for s in tl["segments"] if s["kind"] == "chapter"}
    first17 = next(s["start"] for s in tl["segments"] if s["kind"] == "beat" and s["section"] == 17)
    starts[17] = first17; end = tl["total_seconds"]
    def sec_start(n): return starts.get(n, 0.0)
    def sec_end(n): return starts.get(n + 1, end) if n < 17 else end
    prov = {"approved_by": "Devin, from the 16-bit bench ratings, 2026-09-16", "files": {}}
    files = {}
    for key, (src, title, artist, lic, page) in SOURCES.items():
        dst = OUT_DIR / f"{key}{src.suffix}"
        if not dst.exists(): shutil.copyfile(src, dst)
        files[key] = dst; prov["files"][dst.name] = {"title": title, "artist": artist, "licence": lic, "page": page, "bytes": dst.stat().st_size, "sha256": sha(dst),
                                                   "note": "FLAC from Bandcamp free download (no email required)" if src.suffix == ".flac" else "source file"}
    (OUT_DIR / "provenance.json").write_text(json.dumps(prov, indent=1, ensure_ascii=False) + LF, encoding="utf-8")
    plan = []
    for (a, b), key, gain, why in PLAN:
        plan.append({"file": str(files[key]).replace("\\", "/"), "from": round(sec_start(a), 3), "to": round(sec_end(b), 3), "gain_db": gain, "why": why, "title": SOURCES[key][1]})
    (ROOT / "narration/music-plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False) + LF, encoding="utf-8", newline=LF)
    # transition sting: first 8 s of 2038 D.M.G. over every chapter card except the first (the opening bed covers it)
    sting = OUT_DIR / "dmg-sting-8s.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-t", "8", "-i", str(files["dmg"]), "-af", "afade=t=out:st=6.5:d=1.5", "-c:a", "libmp3lame", "-b:a", "192k", str(sting)], check=True)
    cues = [{"effect": "chapter-sting", "at": round(t, 3), "file": "assets/audio/music/dmg-sting-8s.mp3", "gain_db": -12, "trigger": f"CH-{n:02d}"} for n, t in sorted(starts.items()) if n not in (1, 17)]
    (ROOT / "narration/sfx-music.json").write_text(json.dumps(cues, indent=1) + LF, encoding="utf-8", newline=LF)
    print(f"{len(plan)} beds, {len(cues)} chapter stings; plan -> narration/music-plan.json")
    for p in plan: print(f"  {p['from']/60:6.2f}-{p['to']/60:6.2f} min  {p['title']:24s} {p['gain_db']} dB  {p['why']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
