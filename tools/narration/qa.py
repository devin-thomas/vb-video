"""Narration QA: transcribe every take with faster-whisper (CPU, int8) and compare with the spoken text.

Runs inside the benchmark's asr environment, which has faster-whisper and numpy but no soundfile:

  E:\\local-llm\\models\\narration-tts\\envs\\asr\\Scripts\\python.exe tools/narration/qa.py [--only S02-B03]

Writes narration/qa.json: per beat the transcript, word-level differences after normalisation, words per minute,
peak level, and flags. A transcript difference is a prompt to listen, not proof of a synthesis error (09A); the
flags pick the takes worth a second attempt: dropped or extra content words, pace under 120 or over 200 wpm,
clipping, or leading/trailing silence over two seconds.
"""
from __future__ import annotations
import argparse, difflib, json, os, re, struct, time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
TAKES = ROOT / "narration/takes"
OUT = ROOT / "narration/qa.json"
TTS_HOME = Path(os.environ.get("NARRATION_TTS_HOME", r"E:\local-llm\models\narration-tts"))
os.environ.setdefault("HF_HOME", str(TTS_HOME / "hf-home")); os.environ.setdefault("HF_HUB_OFFLINE", "1")
MODEL = "Systran/faster-whisper-large-v3"
LF = "\n"

def read_wav(path: Path) -> tuple[np.ndarray, int]:
    data = path.read_bytes(); pos = 12; rate = None; fmt = None; ch = None; bits = None
    while pos + 8 <= len(data):
        cid, size = data[pos:pos + 4], struct.unpack("<I", data[pos + 4:pos + 8])[0]
        if cid == b"fmt ": fmt, ch, rate, _, _, bits = struct.unpack("<HHIIHH", data[pos + 8:pos + 24])
        elif cid == b"data":
            raw = data[pos + 8:pos + 8 + size]
            if fmt == 3: audio = np.frombuffer(raw, dtype="<f4")
            elif bits == 16: audio = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
            else: raise ValueError(f"unsupported wav: fmt {fmt} bits {bits}")
            if ch and ch > 1: audio = audio.reshape(-1, ch).mean(axis=1)
            return audio, rate
        pos += 8 + size + (size & 1)
    raise ValueError("no data chunk")

STOP = {"a", "an", "the", "and", "or", "of", "to", "in", "on", "at", "is", "it", "that", "this", "you", "your", "was", "were", "be", "as", "for", "with", "by", "so", "but", "if", "then", "there", "its", "it's", "i", "we", "our", "they", "their", "from", "into", "up", "out", "just", "not", "no", "yes", "very", "also", "than", "more", "most", "all", "any", "some"}

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
def num_words(n: int) -> str:
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + (" " + ONES[n % 10] if n % 10 else "")
    if n < 1000: return ONES[n // 100] + " hundred" + (" " + num_words(n % 100) if n % 100 else "")
    if 1900 <= n <= 1999: return "nineteen " + num_words(n - 1900)
    if 2000 <= n <= 2009: return "two thousand" + (" " + ONES[n - 2000] if n - 2000 else "")
    if n < 1000000: return num_words(n // 1000) + " thousand" + (" " + num_words(n % 1000) if n % 1000 else "")
    return str(n)

def normalise(text: str) -> list[str]:
    t = text.lower().replace("’", "'")
    t = t.replace("c++", " c plus plus ").replace("c#", " c sharp ").replace(".net", " dot net ").replace("%", " percent ")
    t = re.sub(r"(\d+)s", lambda m: num_words(int(m.group(1))) + "s", t)  # 1990s -> nineteen ninetys (both sides)
    t = re.sub(r"\$(\d+)", lambda m: num_words(int(m.group(1))) + " dollars", t)
    t = re.sub(r"(\d+)\.(\d+)", lambda m: num_words(int(m.group(1))) + " point " + " ".join(ONES[int(c)] for c in m.group(2)), t)
    t = re.sub(r"\d+", lambda m: num_words(int(m.group(0))) if len(m.group(0)) < 7 else m.group(0), t)
    t = t.replace("-", " ")
    t = re.sub(r"[^a-z0-9' ]+", " ", t)
    words = [w.strip("'") for w in t.split()]
    return [w for w in words if w]

def word_diff(expected: list[str], got: list[str]) -> list[dict]:
    sm = difflib.SequenceMatcher(a=expected, b=got, autojunk=False); out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal": continue
        out.append({"op": tag, "expected": " ".join(expected[i1:i2]), "heard": " ".join(got[j1:j2])})
    return out

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--only"); ap.add_argument("--attempt", type=int, default=0, help="0 = latest attempt per beat"); args = ap.parse_args()
    from faster_whisper import WhisperModel
    model = WhisperModel(MODEL, device="cpu", compute_type="int8")
    results = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    beats = sorted(p.name for p in TAKES.iterdir() if p.is_dir())
    if args.only: beats = [b for b in beats if b in set(args.only.split(","))]
    for bid in beats:
        attempts = sorted(int(p.name) for p in (TAKES / bid).iterdir() if p.name.isdigit() and (p / "metadata.json").exists())
        if not attempts: continue
        att = args.attempt or attempts[-1]
        d = TAKES / bid / f"{att:02d}"; key = f"{bid}/{att:02d}"
        if key in results and not args.only: continue
        meta = json.loads((d / "metadata.json").read_text(encoding="utf-8"))
        audio, rate = read_wav(d / "native-audio.wav")
        dur = len(audio) / rate; peak = float(np.max(np.abs(audio))) if len(audio) else 0.0
        thresh = 0.01; idx = np.where(np.abs(audio) > thresh)[0]
        lead = idx[0] / rate if len(idx) else dur; trail = (len(audio) - idx[-1]) / rate if len(idx) else dur
        t0 = time.time()
        segs, info = model.transcribe(audio, language="en", beam_size=5, vad_filter=False, condition_on_previous_text=False)
        transcript = " ".join(s.text.strip() for s in segs)
        exp, got = normalise(meta["spoken_text"]), normalise(transcript)
        diffs = word_diff(exp, got)
        content_missing = [w for dd in diffs for w in dd["expected"].split() if w not in STOP and len(w) > 2 and w not in got]
        wpm = meta["words"] / dur * 60 if dur else 0
        flags = []
        if content_missing: flags.append(f"content words not heard: {' '.join(content_missing[:8])}")
        if wpm < 120: flags.append(f"slow ({wpm:.0f} wpm)")
        if wpm > 200: flags.append(f"fast ({wpm:.0f} wpm)")
        if peak >= 0.99: flags.append("clipping")
        if lead > 2.0 or trail > 2.0: flags.append(f"silence lead {lead:.1f}s trail {trail:.1f}s")
        if len(got) > len(exp) * 1.25 + 3: flags.append("extra content heard")
        results[key] = {"beat": bid, "attempt": att, "duration_s": round(dur, 3), "wpm": round(wpm, 1), "peak": round(peak, 4),
                        "lead_silence_s": round(lead, 2), "trail_silence_s": round(trail, 2), "transcript": transcript,
                        "word_diff_ratio": round(sum(len(dd["expected"].split()) + len(dd["heard"].split()) for dd in diffs) / max(1, len(exp) + len(got)), 4),
                        "diffs": diffs[:20], "flags": flags, "asr_seconds": round(time.time() - t0, 1)}
        print(f"{key}: {wpm:.0f} wpm, diff {results[key]['word_diff_ratio']:.3f}, {'; '.join(flags) or 'ok'}", flush=True)
        OUT.write_text(json.dumps(results, indent=1, ensure_ascii=False) + LF, encoding="utf-8")
    flagged = {k: v["flags"] for k, v in results.items() if v["flags"]}
    print(f"{len(results)} takes checked, {len(flagged)} flagged")
    for k, f in flagged.items(): print(" ", k, "|", "; ".join(f))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
