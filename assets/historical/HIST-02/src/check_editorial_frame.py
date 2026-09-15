#!/usr/bin/env python3
"""HIST-02 machine checks for the editorial frame; writes evidence/render-tests.json.

Checks: original hash matches the source record; export is a genuine 1920x1080 PNG;
pillarbox columns are pure black; the image region equals a fresh uniform resize of the
full original (no crop, stretch or retouch); re-rendering is byte-deterministic.
Does not judge visual quality or rights.

Run from the repository root:
    python assets/historical/HIST-02/src/check_editorial_frame.py
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
import tempfile
from pathlib import Path

import PIL
from PIL import Image, ImageChops

BASE = Path(__file__).resolve().parents[1]
ORIGINAL = BASE / "source" / "original.png"
EXPORT = BASE / "exports" / "editorial-frame.png"
SOURCE_RECORD = BASE / "evidence" / "source.json"
OUT = BASE / "evidence" / "render-tests.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    results: list[dict] = []

    def record(name: str, ok: bool, detail: str) -> None:
        results.append({"test": name, "result": "passed" if ok else "failed", "detail": detail})

    expected = json.loads(SOURCE_RECORD.read_text(encoding="utf-8"))["original_file_sha256"]
    actual = sha(ORIGINAL)
    record("original matches source record hash", actual == expected, actual)

    original = Image.open(ORIGINAL)
    record("original native size", original.size == (800, 600), str(original.size))

    header = EXPORT.read_bytes()[:8]
    export = Image.open(EXPORT)
    record("export is PNG 1920x1080", header == b"\x89PNG\r\n\x1a\n" and export.size == (1920, 1080),
           f"{export.format} {export.size} {export.mode}")

    rgb = export.convert("RGB")
    left = rgb.crop((0, 0, 240, 1080))
    right = rgb.crop((1680, 0, 1920, 1080))
    bars_black = left.getextrema() == ((0, 0), (0, 0), (0, 0)) and right.getextrema() == ((0, 0), (0, 0), (0, 0))
    record("pillarbox columns x<240 and x>=1680 are pure black", bars_black,
           f"left {left.getextrema()} right {right.getextrema()}")

    reference = original.convert("RGB").resize((1440, 1080), Image.Resampling.LANCZOS)
    region = rgb.crop((240, 0, 1680, 1080))
    diff = ImageChops.difference(region, reference).getbbox()
    record("image region equals uniform 1.8x resize of full original (no crop/stretch/retouch)", diff is None,
           "identical" if diff is None else f"differs in bbox {diff}")

    with tempfile.TemporaryDirectory() as tmp:
        canvas = Image.new("RGB", (1920, 1080), (0, 0, 0))
        canvas.paste(reference, (240, 0))
        again = Path(tmp) / "again.png"
        canvas.save(again, format="PNG", optimize=True)
        record("re-render is byte-identical", sha(again) == sha(EXPORT), f"{sha(again)} vs {sha(EXPORT)}")

    payload = {
        "id": "HIST-02",
        "tool": "src/check_editorial_frame.py",
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "pillow": PIL.__version__,
        "export_sha256": sha(EXPORT),
        "tests": results,
        "all_passed": all(r["result"] == "passed" for r in results),
        "limitations": ["No visual-quality, historical or legal judgment; see qa.md for manual review."],
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, indent=2))
    return 0 if payload["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
