#!/usr/bin/env python3
"""Write HIST-08 delivery.json: hashed inventory of every file in the asset folder except delivery.json/state.json.

Usage (from the repository root):
    python assets/historical/HIST-08/src/build_delivery.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import PIL

ASSET = Path(__file__).resolve().parents[1]
ROOT = ASSET.parents[2]

ROLES = {
    "source/original.png": "historical original (uncropped native-file frame capture)",
    "exports/editorial-frame.png": "rendered still (editorial-frame variant)",
    "proofs/editorial-frame-720.png": "evidence / QA (720p proof)",
    "qa.md": "evidence / QA",
}


def role_for(rel: str) -> str:
    if rel in ROLES:
        return ROLES[rel]
    if rel.startswith("evidence/source-page/"):
        return "evidence / preserved source-page record"
    if rel.startswith("evidence/"):
        return "evidence / QA"
    if rel.startswith("src/"):
        return "editable input / reproduction script"
    return "other"


def tool_version(cmd: list[str]) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout.splitlines()[0].strip()
    except Exception as exc:  # noqa: BLE001
        return f"unavailable: {exc}"


def main() -> int:
    ops01 = json.loads((ROOT / "assets/ops/OPS-01/delivery.json").read_text(encoding="utf-8"))
    state = json.loads((ASSET / "state.json").read_text(encoding="utf-8"))
    outputs = []
    for path in sorted(p for p in ASSET.rglob("*") if p.is_file()):
        rel = path.relative_to(ASSET).as_posix()
        if rel in ("delivery.json", "state.json") or "__pycache__" in rel:
            continue
        data = path.read_bytes()
        outputs.append({"path": rel, "role": role_for(rel), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})

    delivery = {
        "id": "HIST-08",
        "title": "Windows 95 launch footage still",
        "production_status": state["production_status"],
        "release_status": state["release_status"],
        "provenance_type": "historical source: uncropped frame capture from an archival 1995 television news program (Internet Archive native MPEG-2 original)",
        "shared_version": ops01.get("shared_version"),
        "duration_seconds": None,
        "dimensions": {"width": 1920, "height": 1080},
        "fps": None,
        "outputs": outputs,
        "variants": [
            {"name": "original", "path": "source/original.png", "dimensions": {"width": 720, "height": 480}, "timeline": None,
             "note": "Stored raster, SAR 8:9 (4:3 display). Source timecode 00:06:59 in CC1301_windows_95.mpeg."},
            {"name": "editorial-frame", "path": "exports/editorial-frame.png", "dimensions": {"width": 1920, "height": 1080}, "timeline": None,
             "framing": {"picture_box": [240, 0, 1680, 1080], "background": "#000000", "crop": None, "resample": "Lanczos"},
             "note": "Still; holds for editorial timing. No named cutdowns."},
        ],
        "sources": [
            {"path": "../../../sources/ASSET_PLAN.md", "lines": [92, 92],
             "sha256": hashlib.sha256((ROOT / "sources/ASSET_PLAN.md").read_bytes()).hexdigest(), "relationship": "literal excerpt (plan lead)"},
            {"path": "../../../sources/SCRIPT.md", "lines": [112, 114],
             "sha256": hashlib.sha256((ROOT / "sources/SCRIPT.md").read_bytes()).hexdigest(), "relationship": "literal excerpt (narrative/VISUAL cue)"},
            {"path": "source/original.png", "url": "https://archive.org/download/CC1301_windows_95/CC1301_windows_95.mpeg",
             "source_page": "https://archive.org/details/CC1301_windows_95", "timecode": "00:06:59",
             "native_md5": "e77c6e94d29e30c7b72b4cef4568c3ef", "relationship": "historical original", "record": "evidence/source.json"},
            {"path": "exports/editorial-frame.png", "from": "source/original.png", "relationship": "derivative crop (full-frame pillarbox, no pixels removed)"},
        ],
        "credits": [
            {"asset": "source/original.png, exports/editorial-frame.png",
             "text": "Computer Chronicles, \"Windows 95\" (1995) © Stewart Cheifet Productions. Courtesy of the Internet Archive.",
             "status": "proposed; rights unresolved (evidence/rights.json)"}
        ],
        "tests": [
            {"name": "acquire.py native-file frame decode", "result": "pass", "detail": "ffmpeg decoded I-frame at byte pos 514136078, 720x480 SAR 8/9, checksum BBA9F720; PNG pixels identical to an independent earlier grab"},
            {"name": "render_frame.py", "result": "pass", "detail": "exports/editorial-frame.png 1920x1080; proofs/editorial-frame-720.png 1280x720; pillar pixels (100,500) and (1800,500) are (0,0,0)"},
            {"name": "manual visual inspection at 1920x1080, 1:1 crop, and 1280x720", "result": "pass with notes", "detail": "see qa.md"},
            {"name": "tools/validate_delivery.py --id HIST-08", "result": "see qa.md (actual output recorded)"},
        ],
        "unresolved_gates": ["R14"],
        "toolchain": {
            "python": sys.version.split()[0],
            "pillow": PIL.__version__,
            "ffmpeg": tool_version(["ffmpeg", "-version"]),
            "ffprobe": tool_version(["ffprobe", "-version"]),
            "acquire_command": "python assets/historical/HIST-08/src/acquire.py",
            "render_command": "python assets/historical/HIST-08/src/render_frame.py",
            "delivery_command": "python assets/historical/HIST-08/src/build_delivery.py",
            "os": "Windows 11 Pro 10.0.26200",
        },
        "notes": [
            "Historical proof. Release blocked on R14 rights; see qa.md RQ-1..RQ-3.",
            "The full native MPEG-2 (1.99 GB) is not vendored. It is identified by IA-published md5/sha1 in evidence/source-page/CC1301_windows_95_files.xml.",
            "No audio, AI-generated content, watermark removal, or added text.",
        ],
    }
    (ASSET / "delivery.json").write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"delivery.json written with {len(outputs)} outputs; shared_version={delivery['shared_version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
