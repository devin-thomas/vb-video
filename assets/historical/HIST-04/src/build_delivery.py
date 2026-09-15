#!/usr/bin/env python3
"""Write HIST-04 delivery.json from the files actually present (hash inventory).

Run from the repository root after make_frame.py:
    python assets/historical/HIST-04/src/build_delivery.py
"""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from pathlib import Path

from PIL import __version__ as PIL_VERSION

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[2]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def role(rel: str) -> str:
    if rel.startswith("source/"):
        return "historical original (unaltered archive file)"
    if rel.startswith("exports/"):
        return "rendered still"
    if rel.startswith("src/"):
        return "editable source / build script"
    if rel.startswith("evidence/source-page/"):
        return "source page snapshot"
    if rel.startswith("evidence/proof-720p"):
        return "720p inspection proof"
    return "evidence / QA"


def curl_version() -> str:
    try:
        return subprocess.check_output(["curl", "--version"], text=True).splitlines()[0]
    except (OSError, subprocess.CalledProcessError) as exc:
        return f"unavailable: {exc}"


def main() -> None:
    outputs = []
    for p in sorted(BASE.rglob("*")):
        if not p.is_file() or p.name in ("delivery.json", "state.json") or "__pycache__" in p.parts:
            continue
        rel = p.relative_to(BASE).as_posix()
        outputs.append({"path": rel, "role": role(rel), "bytes": p.stat().st_size, "sha256": sha(p)})

    version_file = ROOT / "assets" / "shared" / "VERSION.json"
    shared_version = json.loads(version_file.read_text(encoding="utf-8"))["version"] if version_file.is_file() else None
    state = json.loads((BASE / "state.json").read_text(encoding="utf-8"))
    framing = json.loads((BASE / "evidence" / "framing.json").read_text(encoding="utf-8"))
    provenance = json.loads((BASE / "evidence" / "provenance.json").read_text(encoding="utf-8"))
    source = json.loads((BASE / "evidence" / "source.json").read_text(encoding="utf-8"))

    delivery = {
        "id": "HIST-04",
        "title": "Kemeny and Kurtz at Dartmouth",
        "production_status": state["production_status"],
        "release_status": state["release_status"],
        "provenance_type": provenance["classification"],
        "shared_version": shared_version,
        "duration_seconds": None,
        "dimensions": {"width": 1920, "height": 1080},
        "fps": None,
        "outputs": outputs,
        "variants": [
            {"name": "original", "files": ["source/original.jpg", "exports/original.png", "evidence/proof-720p-original.png"],
             "framing": framing["variants"]["original"], "timing": "still; hold for editorial timing"},
            {"name": "editorial-frame", "files": ["exports/editorial-frame.png", "evidence/proof-720p-editorial-frame.png"],
             "framing": framing["variants"]["editorial-frame"], "timing": "still; hold for editorial timing"},
        ],
        "sources": provenance["sources"],
        "credits": [
            {"type": "historical photograph", "credit": source["credit_text"], "rights_status": source["rights_status"],
             "license": None, "evidence": "evidence/rights.json"}
        ],
        "tests": [
            {"test": "original file hashes equal archive API o:sha256", "result": "passed", "evidence": "evidence/source-page/api-media-3691.json, evidence/source-page/api-media-3692.json"},
            {"test": "export and proof dimensions (1920x1080, 1280x720)", "result": "passed"},
            {"test": "crop-mark ink scan in editorial-frame image area", "result": "passed after crop top moved 52 -> 56", "evidence": "qa.md"},
            {"test": "deterministic re-render (sha256sum -c on two consecutive runs)", "result": "passed"},
            {"test": "manual visual review at 1920x1080 and 1280x720, both variants", "result": "passed with note: visible softness at 1080p from 1.53x enlargement of a 1000 px web file", "evidence": "qa.md"},
            {"test": "tools/validate_delivery.py --id HIST-04", "result": "recorded in qa.md (not self-referential here)"},
        ],
        "unresolved_gates": ["R14"],
        "toolchain": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "pillow": PIL_VERSION,
            "curl": curl_version(),
            "render_command": "python assets/historical/HIST-04/src/make_frame.py",
            "network_used": True,
            "network_note": "Anonymous HTTPS GETs to exhibits.library.dartmouth.edu, library.dartmouth.edu, dartmouth.edu, and Wikimedia APIs (rate-limited). No accounts, terms, payments or CAPTCHAs.",
            "installs_performed": False,
        },
        "notes": [
            "Photograph is c. 1969 (Kiewit Computation Center), not 1964; see evidence/source.json.",
            "Release blocked: no item-level license (R14). Review questions RQ-1..RQ-5 in qa.md.",
            "No text, labels, captions or UI were added to either export.",
        ],
    }
    (BASE / "delivery.json").write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"delivery.json written with {len(outputs)} outputs")


if __name__ == "__main__":
    main()
