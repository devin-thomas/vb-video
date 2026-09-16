"""Render the episode from narration/timeline.json with ffmpeg (pipeline stage 09, one reproducible rendering path).

Every timeline segment becomes one intermediate clip (video from the approved asset files, audio from the narration
take), the clips are concatenated, then an optional mix pass adds the music bed (ducked under narration) and sound
effects. The review rendition is 1920x1080 at 60 fps; the master is 3840x2160 at 60 fps, upscaled with Lanczos
from the 1080p sources (the sources are 1080p by contract; diagrams keep their SVG for a later native re-render).

  python tools/assembly/render.py --profile review                 # build/review-1080p60.mp4
  python tools/assembly/render.py --profile review --sections 1,2  # a test cut
  python tools/assembly/render.py --profile master                 # build/master-2160p60.mp4 (needs the review pass)
  python tools/assembly/render.py --profile review --music path/to/bed.wav --sfx narration/sfx.json
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIMELINE = ROOT / "narration/timeline.json"
BUILD = ROOT / "build"
BG = "#1a1917"
LF = "\n"

def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed ({r.returncode}):\n{' '.join(cmd)}\n{r.stderr[-2000:]}")

def fit(w: int, h: int, fps: int) -> str:
    return f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color={BG},setsar=1,fps={fps},format=yuv420p"

def tc_seconds(tc: str) -> float:
    parts = tc.split(":")
    return sum(float(p) * 60 ** i for i, p in enumerate(reversed(parts)))

def visual_inputs(v: dict, slot: float, w: int, h: int, fps: int, idx: int) -> tuple[list[str], str]:
    """ffmpeg input args and a filter chain producing exactly `slot` seconds labelled [v{idx}]."""
    f = ROOT / v["file"]
    if v["still"]:
        args = ["-loop", "1", "-framerate", str(fps), "-t", f"{slot:.3f}", "-i", str(f)]
        chain = f"[{idx}:v]{fit(w, h, fps)},trim=duration={slot:.3f},setpts=PTS-STARTPTS[v{idx}]"
        return args, chain, 1
    elif v.get("in_out"):
        a, b = v["in_out"]; start, end = tc_seconds(a), tc_seconds(b)
        args = ["-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", str(f)]
        chain = f"[{idx}:v]{fit(w, h, fps)},tpad=stop_mode=clone:stop_duration={slot:.3f},trim=duration={slot:.3f},setpts=PTS-STARTPTS[v{idx}]"
        return args, chain, 1
    elif v.get("kind") == "archive" and not v.get("still"):
        # a stock clip never freezes (Devin, 2026-09-16): loop the whole clip inside its slot
        args = ["-stream_loop", "-1", "-i", str(f)]
        chain = f"[{idx}:v]{fit(w, h, fps)},trim=duration={slot:.3f},setpts=PTS-STARTPTS[v{idx}]"
        return args, chain, 1
    elif v.get("kind") == "recording":
        # a screen recording: fill the width, never upscale past 1.6x, hold the last frame after it ends
        args = ["-i", str(f)]
        chain = (f"[{idx}:v]scale=w='min({w},iw*1.6)':h='min({h},ih*1.6)':force_original_aspect_ratio=decrease:flags=lanczos,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color={BG},setsar=1,fps={fps},format=yuv420p,"
                 f"tpad=stop_mode=clone:stop_duration={slot:.3f},trim=duration={slot:.3f},setpts=PTS-STARTPTS[v{idx}]")
    elif v.get("poster") and v.get("duration") and v["duration"] < slot - 0.05:
        # motion preview shorter than its slot: play it, then hold its designed poster frame
        rest = slot - v["duration"]
        args = ["-i", str(f), "-loop", "1", "-framerate", str(fps), "-t", f"{rest:.3f}", "-i", str(ROOT / v["poster"])]
        chain = (f"[{idx}:v]{fit(w, h, fps)},trim=duration={v['duration']:.3f},setpts=PTS-STARTPTS[m{idx}];"
                 f"[{idx + 1}:v]{fit(w, h, fps)},trim=duration={rest:.3f},setpts=PTS-STARTPTS[p{idx}];[m{idx}][p{idx}]concat=n=2:v=1:a=0[v{idx}]")
        return args, chain, 2
    else:
        args = ["-i", str(f)]
        chain = f"[{idx}:v]{fit(w, h, fps)},tpad=stop_mode=clone:stop_duration={slot:.3f},trim=duration={slot:.3f},setpts=PTS-STARTPTS[v{idx}]"
    return args, chain, 1

def render_segment(seg: dict, length: float, w: int, h: int, fps: int, out: Path, vcodec: list[str]) -> None:
    visuals = [v for v in seg["visuals"] if v]
    n = len(visuals)
    given = [float(v.get("slot") or 0) for v in visuals]
    slots = [g * length / sum(given) for g in given] if all(g > 0 for g in given) else [length / n] * n  # timeline slots, scaled to the segment
    args, chains, labels, idx = [], [], [], 0
    for v, slot in zip(visuals, slots):
        a, c, used = visual_inputs(v, slot, w, h, fps, idx); args += a; chains.append(c); labels.append(f"[v{idx}]"); idx += used
    concat = "".join(labels) + f"concat=n={n}:v=1:a=0[vout]" if n > 1 else f"{labels[0]}null[vout]"
    if seg.get("audio"):
        args += ["-i", str(ROOT / seg["audio"])]
        achain = f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=duration={length:.3f},asetpts=PTS-STARTPTS[aout]"
    else:
        args += ["-f", "lavfi", "-t", f"{length:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
        achain = f"[{idx}:a]atrim=duration={length:.3f},asetpts=PTS-STARTPTS[aout]"
    filt = ";".join(chains + [concat, achain])
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args, "-filter_complex", filt, "-map", "[vout]", "-map", "[aout]",
           *vcodec, "-c:a", "aac", "-b:a", "192k", "-t", f"{length:.3f}", "-movflags", "+faststart", str(out)]
    run(cmd)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", choices=["review", "master"], default="review")
    ap.add_argument("--sections", help="comma-separated section numbers for a test cut")
    ap.add_argument("--music"); ap.add_argument("--sfx"); ap.add_argument("--force", action="store_true")
    ap.add_argument("--bed-stem", help="also write the ducked music alone (no voice, no effects) to this WAV, for measurement")
    args = ap.parse_args()
    tl = json.loads(TIMELINE.read_text(encoding="utf-8"))
    segs = tl["segments"]
    wanted = {int(x) for x in args.sections.split(",")} if args.sections else None
    w, h, fps = 1920, 1080, tl.get("fps_review", 60)
    seg_dir = BUILD / "segments"; seg_dir.mkdir(parents=True, exist_ok=True)
    vcodec = ["-c:v", "h264_nvenc", "-preset", "p5", "-rc", "vbr", "-cq", "19", "-b:v", "0", "-pix_fmt", "yuv420p"]
    lengths = []
    for i, seg in enumerate(segs):
        nxt = segs[i + 1]["start"] if i + 1 < len(segs) else seg["start"] + seg["duration"]
        lengths.append(round(nxt - seg["start"], 3))
    listing, missing_audio = [], []
    for seg, length in zip(segs, lengths):
        if wanted and seg.get("section", 0 if seg["kind"] != "beat" else None) not in wanted and not (seg["kind"] == "chapter" and int(seg["id"][3:]) in wanted):
            continue
        if seg["kind"] == "beat" and not seg.get("audio"): missing_audio.append(seg["id"])
        out = seg_dir / f"{seg['id']}.mp4"
        if args.force or not out.exists() or out.stat().st_mtime < TIMELINE.stat().st_mtime:
            print(f"[render] {seg['id']} {length:.1f}s x{len([v for v in seg['visuals'] if v])} visual(s)", flush=True)
            render_segment(seg, length, w, h, fps, out, vcodec)
        listing.append(out)
    if missing_audio:
        print(f"[warn] {len(missing_audio)} beats have no narration take yet (silent placeholders): {missing_audio[:5]}...")
    lst = BUILD / ("concat-test.txt" if wanted else "concat.txt")
    lst.write_text("".join(f"file '{p.as_posix()}'{LF}" for p in listing), encoding="utf-8")
    stem = "review-1080p60" + (f"-s{args.sections.replace(',', '_')}" if wanted else "")
    joined = BUILD / f"{stem}.mp4"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(joined)])
    print(f"[ok] {joined} ({sum(lengths)/60:.1f} min timeline)")
    final = joined
    if args.music or args.sfx:
        final = mix(joined, args.music, args.sfx, BUILD / f"{stem}-mixed.mp4", Path(args.bed_stem) if args.bed_stem else None)
    if args.profile == "master":
        master = BUILD / stem.replace("review-1080p60", "master-2160p60").replace("review", "master")
        master = master.with_suffix(".mp4")
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(final), "-vf", "scale=3840:2160:flags=lanczos,format=yuv420p",
             "-c:v", "hevc_nvenc", "-preset", "p6", "-rc", "vbr", "-cq", "18", "-b:v", "0", "-tag:v", "hvc1", "-c:a", "copy", "-movflags", "+faststart", str(master)])
        print(f"[ok] {master}")
    return 0

def music_plan(music: str) -> list[dict]:
    """One file, or a JSON plan: [{"file": ..., "from": seconds, "to": seconds, "gain_db": -16}, ...] covering the timeline in order."""
    if music.lower().endswith(".json"):
        return json.loads(Path(music).read_text(encoding="utf-8"))
    return [{"file": music, "from": 0, "to": None, "gain_db": -16}]

def probe_duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)

def effect_duck_expr(cues: list[dict], floor: float = 0.01, lead: float = 0.3, ramp_in: float = 0.15, tail: float = 0.2, release: float = 0.8) -> str:
    """volume expression (eval=frame) that drops the bed to `floor` from `lead` s before each effect until `tail` s after it
    ends, ramping down over `ramp_in` s and back up over `release` s. Devin (2026-09-16): a unique effect needs the music
    to duck sharply to the bottom right before it, play in its entirety, then the music returns."""
    parts = []
    for c in cues:
        a = float(c["at"]) - lead; b = float(c["at"]) + probe_duration(ROOT / c["file"]) + tail
        parts.append(f"if(lt(t,{a - ramp_in:.3f}),1,if(lt(t,{a:.3f}),1-(t-{a - ramp_in:.3f})/{ramp_in}*{1 - floor},if(lt(t,{b:.3f}),{floor},if(lt(t,{b + release:.3f}),{floor}+(t-{b:.3f})/{release}*{1 - floor},1))))")
    expr = parts[0]
    for q in parts[1:]: expr = f"min({expr},{q})"
    return expr

def mix(video: Path, music: str | None, sfx_json: str | None, out: Path, bed_stem: Path | None = None) -> Path:
    """Music bed(s) ducked under narration with sidechain compression and pushed to the floor around every sound effect;
    effects placed at timeline seconds. With bed_stem, also writes the ducked music alone (no voice, no effects) as a WAV."""
    inputs = ["-i", str(video)]; filters = []; mix_in = ["[0:a]"]; n = 1
    sfx = []
    for sj in (sfx_json or "").split(","):
        if sj.strip(): sfx += json.loads(Path(sj.strip()).read_text(encoding="utf-8"))
    effects = [c for c in sfx if c.get("effect") != "chapter-sting"]
    if music:
        beds = []
        for k, cue in enumerate(music_plan(music)):
            start = float(cue.get("from", 0)); end = cue.get("to")
            inputs += ["-stream_loop", "-1", "-i", cue["file"]]
            length = f",atrim=duration={float(end) - start:.3f}" if end is not None else ""
            fade = f",afade=t=in:d=2{',afade=t=out:st=' + str(float(end) - start - 3) + ':d=3' if end is not None else ''}"
            filters.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-18:TP=-2:LRA=9{length}{fade},volume={cue.get('gain_db', -16)}dB,adelay={int(start * 1000)}|{int(start * 1000)}[bed{k}]")
            beds.append(f"[bed{k}]"); n += 1
        duck = f",volume='{effect_duck_expr(effects)}':eval=frame" if effects else ""
        filters.append("".join(beds) + f"amix=inputs={len(beds)}:duration=longest:normalize=0{duck}[bed];[0:a]asplit[nar][key];[bed][key]sidechaincompress=threshold=0.05:ratio=6:attack=40:release=600" + ("[ducked0];[ducked0]asplit[ducked][stem]" if bed_stem else "[ducked]"))
        mix_in = ["[nar]", "[ducked]"]
    for k, item in enumerate(sfx):
        inputs += ["-i", str(ROOT / item["file"])]
        delay = int(float(item["at"]) * 1000)
        filters.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,volume={item.get('gain_db', -6)}dB,adelay={delay}|{delay}[fx{k}]")
        mix_in.append(f"[fx{k}]"); n += 1
    filters.append("".join(mix_in) + f"amix=inputs={len(mix_in)}:duration=first:normalize=0,volume=4dB,alimiter=limit=0.89:attack=5:release=80:level=0[aout]")
    stem_args = ["-map", "[stem]", "-c:a:1", "pcm_s16le", str(bed_stem)] if (bed_stem and music) else []
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "0:v", "-map", "[aout]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(out), *stem_args])
    print(f"[ok] {out}" + (f" (+ bed stem {bed_stem})" if stem_args else ""))
    return out

if __name__ == "__main__":
    raise SystemExit(main())
