#!/usr/bin/env python3
"""HIST-10 reproducible build: decode one uncropped frame from the archived
original video, frame it at 1920x1080 without stretching or cropping, and
write a 720p review proof.

Run from the repository root:
    python assets/historical/HIST-10/src/build_hist10.py

Inputs (never modified):
    assets/historical/HIST-10/source/original.webm   (Internet Archive original)
Outputs:
    source/raw/frame-000462.png        uncropped decoded frame, native 480x360
    exports/editorial-frame.png        1920x1080 pillarboxed editorial frame
    proofs/editorial-frame-720.png     1280x720 review proof
    evidence/framing.json              exact, reversible transform record
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parents[1]
ORIGINAL = BASE / "source" / "original.webm"
FRAME_INDEX = 462  # 0-based decoded frame number; storefront shot, sign fully in frame
RAW = BASE / "source" / "raw" / f"frame-{FRAME_INDEX:06d}.png"
EXPORT = BASE / "exports" / "editorial-frame.png"
PROOF = BASE / "proofs" / "editorial-frame-720.png"
FRAMING = BASE / "evidence" / "framing.json"
EXPECTED_ORIGINAL_SHA1 = "9bd515aa79e863e6755845e936af4c6add04bd79"  # from IA files.xml

CANVAS = (1920, 1080)
BACKGROUND = (0, 0, 0)
SCALE = 3  # integer factor: 480x360 -> 1440x1080, aspect ratio preserved


def sha(path: Path, algo: str) -> str:
    h = hashlib.new(algo)
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    if sha(ORIGINAL, "sha1") != EXPECTED_ORIGINAL_SHA1:
        print("original.webm does not match the Internet Archive SHA-1", file=sys.stderr)
        return 1

    RAW.parent.mkdir(parents=True, exist_ok=True)
    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    PROOF.parent.mkdir(parents=True, exist_ok=True)

    tmp = RAW.with_suffix(".ffmpeg.png")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(ORIGINAL),
         "-vf", f"select=eq(n\\,{FRAME_INDEX})", "-vsync", "0", "-frames:v", "1",
         str(tmp)],
        check=True,
    )
    # Re-save through Pillow so the PNG carries no ffmpeg metadata/timestamps.
    frame = Image.open(tmp).convert("RGB")
    frame.save(RAW, optimize=False)
    tmp.unlink()

    w, h = frame.size
    sw, sh = w * SCALE, h * SCALE
    if sh > CANVAS[1] or sw > CANVAS[0]:
        print("scaled frame does not fit canvas", file=sys.stderr)
        return 1
    x0, y0 = (CANVAS[0] - sw) // 2, (CANVAS[1] - sh) // 2

    canvas = Image.new("RGB", CANVAS, BACKGROUND)
    canvas.paste(frame.resize((sw, sh), Image.LANCZOS), (x0, y0))
    canvas.save(EXPORT, optimize=False)

    canvas.resize((1280, 720), Image.LANCZOS).save(PROOF, optimize=False)

    framing = {
        "source_video": "source/original.webm",
        "source_video_sha1": EXPECTED_ORIGINAL_SHA1,
        "decoded_frame_index_0_based": FRAME_INDEX,
        "decoder_select_filter": f"select=eq(n\\,{FRAME_INDEX})",
        "frame_rate": "30000/1001",
        "approx_presentation_time_seconds": round(FRAME_INDEX * 1001 / 30000, 3),
        "burned_in_timecode_visible_in_frame": "10:46:14;06",
        "raw_frame": RAW.relative_to(BASE).as_posix(),
        "raw_frame_size": [w, h],
        "export": EXPORT.relative_to(BASE).as_posix(),
        "canvas": list(CANVAS),
        "background_rgb": list(BACKGROUND),
        "scale_factor": SCALE,
        "resample": "Pillow LANCZOS",
        "placed_at": [x0, y0],
        "placed_size": [sw, sh],
        "crop": None,
        "stretch": False,
        "reverse": f"crop exports/editorial-frame.png to box ({x0},{y0},{x0 + sw},{y0 + sh}) and downscale by {SCALE} to recover the raw frame geometry (resampling is lossy; the lossless raw frame is kept in source/raw/)",
        "not_done": [
            "no crop of picture content",
            "no removal or masking of the burned-in source timecode",
            "no added text, logos, captions or UI",
            "no colour correction, sharpening or AI upscaling",
        ],
        "proof_720": PROOF.relative_to(BASE).as_posix(),
    }
    FRAMING.write_text(json.dumps(framing, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"raw": RAW.name, "export": EXPORT.name, "proof": PROOF.name,
                      "placed_at": [x0, y0], "placed_size": [sw, sh]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
