"""Synthesize narration beats with the locked narrator (Qwen3-TTS CustomVoice, speaker aiden) on this machine's GPU.

Mirrors the narration benchmark's local worker protocol and GPU lock (narration-benchmark/bench/providers.py) without
importing it, so this repository stays self-contained. One worker process keeps the model loaded; one JSON request
per beat; native float32 24 kHz WAV written unchanged to narration/takes/<beat>/<attempt>/native-audio.wav with a
metadata.json beside it. Existing takes are skipped, so an interrupted run resumes.

  python tools/narration/synth.py --dry-run             # print what would be sent
  python tools/narration/synth.py --only S01-B01,S01-B02  # a test
  python tools/narration/synth.py                       # everything missing, in script order
"""
from __future__ import annotations
import argparse, atexit, ctypes, hashlib, json, os, subprocess, sys, time, wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BEATS = ROOT / "narration/beats.json"
TAKES = ROOT / "narration/takes"
LOG = ROOT / "narration/synth.log"
BENCH = Path(r"C:\dev\youtube\video-explainers-pipeline\narration-benchmark")
TTS_HOME = Path(os.environ.get("NARRATION_TTS_HOME", r"E:\local-llm\models\narration-tts"))
VOICE = "aiden"
MODEL = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"
LF = "\n"

def log(msg: str) -> None:
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f: f.write(line + LF)

def process_alive(pid: int) -> bool:
    handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
    if not handle: return False
    code = ctypes.c_ulong(); ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(code)); ctypes.windll.kernel32.CloseHandle(handle)
    return code.value == 259

def gpu_lock() -> None:
    path = BENCH / "runs/.gpu.lock"; path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        owner = path.read_text(encoding="utf-8").strip()
        if owner.isdigit() and not process_alive(int(owner)):
            path.unlink(missing_ok=True); fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        else:
            raise SystemExit(f"another local GPU job (pid {owner}) holds {path}; wait for it")
    os.write(fd, str(os.getpid()).encode()); os.close(fd)
    atexit.register(lambda: path.unlink(missing_ok=True))

def worker() -> subprocess.Popen:
    weights = json.loads((BENCH / "providers/weights.lock.json").read_text(encoding="utf-8"))
    ckpt = weights["N02"]["local_path"] if "N02" in weights else weights["local_path"]
    python = TTS_HOME / "envs/qwen3-tts/Scripts/python.exe"
    script = BENCH / "providers/qwen3_tts/worker.py"
    for p in (python, script, Path(ckpt)):
        if not p.exists(): raise SystemExit(f"missing: {p}")
    env = {**os.environ, "HF_HOME": str(TTS_HOME / "hf-home"), "HF_HUB_OFFLINE": "1", "PYTHONIOENCODING": "utf-8"}
    errlog = (ROOT / "narration/worker.log").open("a", encoding="utf-8")
    proc = subprocess.Popen([str(python), str(script), "--ckpt-dir", ckpt], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=errlog, text=True, encoding="utf-8", env=env)
    ready = read_message(proc)
    if not ready or not ready.get("ready"): raise SystemExit("worker did not become ready; see narration/worker.log")
    log(f"worker ready on {ready.get('device')} torch {ready.get('torch')} {ready.get('dtype')}")
    atexit.register(proc.terminate)
    return proc

def read_message(proc: subprocess.Popen) -> dict | None:
    while line := proc.stdout.readline():
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(msg, dict): return msg
    return None

def wav_seconds(path: Path) -> float:
    """Duration of a RIFF WAV, including float (format 3) files the wave module refuses."""
    import struct
    data = path.read_bytes()
    pos, rate, channels, bits, frames = 12, None, None, None, None
    while pos + 8 <= len(data):
        cid, size = data[pos:pos + 4], struct.unpack("<I", data[pos + 4:pos + 8])[0]
        if cid == b"fmt ":
            _, channels, rate, _, _, bits = struct.unpack("<HHIIHH", data[pos + 8:pos + 24])
        elif cid == b"data":
            frames = size // (channels * bits // 8); break
        pos += 8 + size + (size & 1)
    return frames / rate

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--only"); ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--attempt", type=int, default=1, help="write this attempt number (regenerate with 2, 3, ...)")
    args = ap.parse_args()
    beats = json.loads(BEATS.read_text(encoding="utf-8"))["beats"]
    wanted = set(args.only.split(",")) if args.only else None
    todo = []
    for b in beats:
        if wanted and b["id"] not in wanted: continue
        out = TAKES / b["id"] / f"{args.attempt:02d}" / "native-audio.wav"
        if out.exists() and (out.parent / "metadata.json").exists() and not args.dry_run: continue
        todo.append(b)
    if args.limit: todo = todo[: args.limit]
    log(f"{len(todo)} beats to synthesize ({sum(b['words'] for b in todo)} words); voice {VOICE}; attempt {args.attempt:02d}")
    if args.dry_run:
        for b in todo: print(b["id"], "|", b["spoken"][:300])
        return 0
    gpu_lock(); proc = worker()
    started = time.time(); audio_total = 0.0
    for i, b in enumerate(todo, 1):
        out_dir = TAKES / b["id"] / f"{args.attempt:02d}"; out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / "native-audio.wav"
        seed = int(hashlib.sha256(f"{b['id']}-{args.attempt}".encode()).hexdigest()[:8], 16)
        req = {"text": b["spoken"], "voice_id": VOICE, "output_path": out.as_posix(), "seed": seed, "settings": {"language": "English"}}
        proc.stdin.write(json.dumps(req) + LF); proc.stdin.flush()
        resp = read_message(proc)
        if resp is None: raise SystemExit("worker exited mid-request; see narration/worker.log")
        if not resp.get("ok"):
            log(f"[failed] {b['id']}: {resp.get('error') or resp}"); (out_dir / "error.json").write_text(json.dumps(resp, indent=1), encoding="utf-8"); continue
        dur = wav_seconds(out); audio_total += dur
        meta = {"beat_id": b["id"], "attempt": args.attempt, "voice_id": VOICE, "model": MODEL, "seed": seed, "spoken_text": b["spoken"],
                "spoken_sha256": b["spoken_sha256"], "written_sha256": hashlib.sha256(b["written"].encode("utf-8")).hexdigest(),
                "words": b["words"], "duration_s": round(dur, 3), "wpm": round(b["words"] / dur * 60, 1) if dur else None,
                "sample_rate": resp.get("sample_rate"), "wall_s": resp.get("wall_s"), "torch_peak_allocated_mib": resp.get("torch_peak_allocated_mib"),
                "host": "titan", "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
        (out_dir / "metadata.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False) + LF, encoding="utf-8")
        elapsed = time.time() - started
        log(f"[ok] {i}/{len(todo)} {b['id']} {dur:.1f}s audio ({meta['wpm']} wpm) in {resp.get('wall_s')}s | {audio_total/60:.1f} min audio, {elapsed/60:.1f} min elapsed")
    log("done")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
