#!/usr/bin/env python3
"""Write HIST-10 delivery.json: inventory every delivered file with bytes and
SHA-256, and check PNG sizes. Run after build_hist10.py and after qa.md,
state.json, and the evidence files are final.

    python assets/historical/HIST-10/src/finish_hist10.py
"""
from __future__ import annotations

import hashlib
import json
import platform
import struct
import subprocess
from pathlib import Path

import PIL

BASE = Path(__file__).resolve().parents[1]

ROLES = {
    "source/original.webm": "historical original (Internet Archive original file, byte-identical)",
    "source/raw/frame-000462.png": "uncropped decoded frame (native 480x360)",
    "exports/editorial-frame.png": "editorial frame 1920x1080 (pillarboxed, derived from raw frame)",
    "proofs/editorial-frame-720.png": "720p review proof",
    "qa.md": "evidence / QA",
    "evidence/provenance.json": "evidence / provenance",
    "evidence/source-excerpts.md": "evidence / source excerpts",
    "evidence/claim-checks.json": "evidence / gates and claim checks",
    "evidence/source.json": "evidence / source record",
    "evidence/rights.json": "evidence / rights record",
    "evidence/candidates.json": "evidence / candidate report",
    "evidence/search-log.md": "evidence / search log",
    "evidence/framing.json": "evidence / transform record",
    "evidence/qa-tests.json": "evidence / QA test records",
    "evidence/archive-records/youtube-CcbAC4qI9pQ_files.xml": "evidence / Internet Archive file list with hashes",
    "src/build_hist10.py": "build script",
    "src/finish_hist10.py": "delivery script",
}


def png_size(path: Path):
    head = path.read_bytes()[:24]
    return list(struct.unpack(">II", head[16:24]))


def tool_version(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.splitlines()[0]
    except Exception as exc:  # recorded, not hidden
        return f"unavailable: {exc}"


def main() -> int:
    state = json.loads((BASE / "state.json").read_text(encoding="utf-8"))
    outputs = []
    for rel, role in ROLES.items():
        data = (BASE / rel).read_bytes()
        outputs.append({"path": rel, "role": role, "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest()})

    sizes = {rel: png_size(BASE / rel) for rel in ROLES if rel.endswith(".png")}
    expected = {"source/raw/frame-000462.png": [480, 360],
                "exports/editorial-frame.png": [1920, 1080],
                "proofs/editorial-frame-720.png": [1280, 720]}
    bad = {k: v for k, v in sizes.items() if expected.get(k) != v}

    qa_tests = json.loads((BASE / "evidence" / "qa-tests.json").read_text(encoding="utf-8"))

    delivery = {
        "id": "HIST-10",
        "title": "Egghead Software storefront",
        "production_status": state["production_status"],
        "release_status": state["release_status"],
        "provenance_type": "historical original (third-party archival video frame)",
        "shared_version": "not_applicable (archival still; no shared template used)",
        "duration_seconds": None,
        "dimensions": {"width": 1920, "height": 1080},
        "fps": None,
        "outputs": outputs,
        "variants": [
            {"name": "original",
             "files": ["source/original.webm", "source/raw/frame-000462.png"],
             "notes": "Archived original video; the uncropped frame used is decoded frame 462 (15.415 s, burned-in timecode 10:46:14;06). Still: hold for editorial timing."},
            {"name": "editorial-frame",
             "files": ["exports/editorial-frame.png"],
             "derived_from": "source/raw/frame-000462.png",
             "notes": "3x Lanczos, pillarboxed at x=240 on black; no crop, stretch, or added text. Proof: proofs/editorial-frame-720.png."},
        ],
        "sources": [
            {"path": "../../../sources/ASSET_PLAN.md", "lines": [93, 93],
             "sha256": "8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7",
             "relationship": "source creative brief"},
            {"path": "../../../sources/SCRIPT.md", "lines": [126, 128],
             "sha256": "3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb",
             "relationship": "narration the still illustrates"},
            {"path": "source/original.webm",
             "url": "https://archive.org/download/youtube-CcbAC4qI9pQ/CcbAC4qI9pQ.webm",
             "relationship": "historical original"},
            {"path": "exports/editorial-frame.png", "relationship": "derivative framing (no crop)"},
        ],
        "credits": [
            {"type": "archival footage (rights unresolved)",
             "credit": "Archival footage: \"Buying Windows 95 on Launch Day\" (uploaded by Vampire Robot, 2022), via Internet Archive item youtube-CcbAC4qI9pQ. Original source unknown.",
             "license": None, "rights_status": "unresolved"},
        ],
        "tests": qa_tests + [
            {"test": "PNG dimensions (raw 480x360, export 1920x1080, proof 1280x720)",
             "result": "passed" if not bad else "failed", "sizes": sizes, "bad": bad},
        ],
        "unresolved_gates": ["R14"],
        "toolchain": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "packages": {"Pillow": PIL.__version__},
            "ffmpeg": tool_version(["ffmpeg", "-version"]),
            "ffprobe": tool_version(["ffprobe", "-version"]),
            "download": "curl (anonymous HTTPS from archive.org)",
            "font_files_distributed": False,
            "remote_dependencies_in_outputs": False,
        },
        "notes": [
            "Production produced as an archival proof; release blocked on R14 (rights holder unknown, no license).",
            "Place is not stated by any source and is not recorded. The date 1995-08-24 is the uploader's claim, partly corroborated.",
            "state.json is live workflow state and is not in the output inventory.",
        ],
    }
    (BASE / "delivery.json").write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n",
                                        encoding="utf-8", newline="\n")
    print(json.dumps({"outputs": len(outputs), "png_bad": bad}))
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
