#!/usr/bin/env python3
"""Build assets/historical/HIST-01/delivery.json from the files on disk.

Run from the repository root after src/frame.py:
    python assets/historical/HIST-01/src/build_delivery.py
"""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from pathlib import Path

import PIL

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[2]
EXCLUDE = {"delivery.json", "state.json"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def role(rel: str) -> str:
    if rel.startswith("source/"):
        return "historical original"
    if rel.startswith("exports/"):
        return "editorial still"
    if rel.startswith("proofs/"):
        return "evidence / QA (720p proof)"
    if rel.startswith("evidence/version-evidence/"):
        return "historical original (version evidence)"
    if rel.startswith("evidence/source-pages/"):
        return "preserved source page"
    if rel.startswith("src/"):
        return "editable source"
    return "evidence / QA"


def curl_version() -> str:
    try:
        out = subprocess.run(["curl", "--version"], capture_output=True, text=True, check=True).stdout
        return out.splitlines()[0]
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def main() -> None:
    files = sorted(p for p in BASE.rglob("*") if p.is_file() and p.relative_to(BASE).as_posix() not in EXCLUDE
                   and "__pycache__" not in p.parts)
    outputs = [{"path": p.relative_to(BASE).as_posix(), "role": role(p.relative_to(BASE).as_posix()),
                "bytes": p.stat().st_size, "sha256": sha256(p)} for p in files]

    state = json.loads((BASE / "state.json").read_text(encoding="utf-8"))
    shared = json.loads((ROOT / "assets/shared/VERSION.json").read_text(encoding="utf-8"))
    tests = json.loads((BASE / "evidence/render-tests.json").read_text(encoding="utf-8"))
    source = json.loads((BASE / "evidence/source.json").read_text(encoding="utf-8"))
    sel = source["selected_original"]
    comp = source["companion_version_evidence"]

    delivery = {
        "id": "HIST-01",
        "title": "VB 1.0 IDE",
        "production_status": state["production_status"],
        "release_status": state["release_status"],
        "provenance_type": "historical source: third-party screenshot of Microsoft Visual Basic 1.0 for Windows (WinWorld), with reversible editorial framing",
        "shared_version": shared["version"],
        "duration_seconds": None,
        "dimensions": {"width": 1920, "height": 1080},
        "fps": None,
        "outputs": outputs,
        "variants": [
            {"name": "original", "files": ["source/original.png"], "timeline": None},
            {"name": "editorial-frame", "files": ["exports/editorial-frame.png", "src/frame.json"], "timeline": None},
        ],
        "sources": [
            {"path": "../../../sources/SCRIPT.md", "lines": [94, 94], "sha256": sha256(ROOT / "sources/SCRIPT.md"),
             "relationship": "source creative brief"},
            {"path": "../../../sources/ASSET_PLAN.md", "lines": [89, 89], "sha256": sha256(ROOT / "sources/ASSET_PLAN.md"),
             "relationship": "source creative brief"},
            {"path": "source/original.png", "url": sel["source_urls"]["file"], "page": sel["source_urls"]["screenshot_page"],
             "access_date": sel["access_date"], "sha256": sel["file_integrity"]["sha256"],
             "record": "evidence/source.json", "relationship": "historical original"},
            {"path": "evidence/version-evidence/about-original.png", "url": comp["source_urls"]["internet_archive_file"],
             "page": comp["source_urls"]["internet_archive_item"], "access_date": comp["access_date"],
             "sha256": comp["file_integrity"]["sha256"], "record": "evidence/source.json",
             "relationship": "historical original (version evidence)"},
            {"path": "exports/editorial-frame.png", "derived_from": "source/original.png", "record": "src/frame.json",
             "relationship": "derivative crop (no pixels removed: 2x resize + pillarbox)"},
        ],
        "credits": [
            {"type": "historical screenshot", "credit": sel["credit_text_proposed"], "rights_status": "unresolved",
             "record": "evidence/rights.json"},
            {"type": "software depicted", "credit": "Microsoft Visual Basic 1.0 for Windows, (c) 1987-1991 Microsoft Corp.; portions developed for Microsoft by Cooper Software, Inc. (per in-frame About box)"},
        ],
        "tests": [
            {"test": "render checks (size, aspect, no crop, reversibility, exact blocks, clean pillarbox)",
             "evidence": "evidence/render-tests.json", "result": "passed" if tests["passed"] else "failed"},
            {"test": "deterministic re-render", "result": "identical SHA-256 for export and 720p proof on re-run"},
            {"test": "acquisition integrity", "result": "original MD5 matches WinWorld file-name hash; About capture MD5/SHA-1 match Internet Archive files.xml and WinWorld copy is byte-identical"},
            {"test": "manual visual review", "result": {"mode": "full size 1920x1080 and 720p proof",
             "scope": "Viewed exports/editorial-frame.png and proofs/editorial-frame-720.png; viewed both 640x480 originals.",
             "status": "Whole screenshot intact and sharp; IDE title, menus, properties bar, toolbox, form designer, project and code windows legible at 720p; no added text or UI."}},
            {"test": "tools/validate_delivery.py --id HIST-01", "result": "see qa.md 'Validator output'"},
        ],
        "unresolved_gates": ["R14"],
        "toolchain": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "packages": {"Pillow": PIL.__version__},
            "curl": curl_version(),
            "render_command": "python assets/historical/HIST-01/src/frame.py",
            "network_used": "acquisition only (anonymous HTTPS GETs on 2026-09-15); rendering is offline",
            "installs_performed": False,
            "font_files_distributed": False,
        },
        "notes": [
            "Version rests on WinWorld's VB 1.0 label plus the companion About capture reading 'Microsoft Visual Basic Version 1.0'; the Edit capture has no in-frame version string.",
            "Capturer and capture date unknown; no licence for the screenshot. Release blocked under R14 (RQ-HIST01-1).",
            "Script visual direction says 'properties window'; VB 1.0 shows a properties bar (RQ-HIST01-2, Writing Lead). War/SCRIPT.md not edited.",
            "Internet Archive meta.xml saved with the uploader e-mail redacted; unredacted MD5 c2e15eb385fad6b2006ba7859a30e01e.",
            "Produced is not release-approved; approval comes from the OPS-04 review deck.",
        ],
    }
    (BASE / "delivery.json").write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"delivery.json: {len(outputs)} outputs")


if __name__ == "__main__":
    main()
