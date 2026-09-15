#!/usr/bin/env python3
"""Write HIST-02 delivery.json with a hashed inventory of every file in the asset folder.

delivery.json (self) and state.json (live workflow state) are excluded, per the output contract.
Run from the repository root after all other files are final:
    python assets/historical/HIST-02/src/build_delivery.py
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path

import PIL

BASE = Path(__file__).resolve().parents[1]
EXCLUDE = {"delivery.json", "state.json"}


def role(rel: str) -> str:
    if rel == "source/original.png":
        return "historical original (acquired, unmodified)"
    if rel.startswith("exports/"):
        return "rendered still"
    if rel.startswith("src/"):
        return "editable source / script"
    if rel.startswith("evidence/pages/"):
        return "evidence / source page snapshot"
    return "evidence / QA"


def main() -> None:
    outputs = []
    for path in sorted(p for p in BASE.rglob("*") if p.is_file()):
        rel = path.relative_to(BASE).as_posix()
        if rel in EXCLUDE or "__pycache__" in rel:
            continue
        data = path.read_bytes()
        outputs.append({"path": rel, "role": role(rel), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})

    source = json.loads((BASE / "evidence" / "source.json").read_text(encoding="utf-8"))
    render = json.loads((BASE / "evidence" / "render-tests.json").read_text(encoding="utf-8"))
    delivery = {
        "id": "HIST-02",
        "title": "VB 4.0 IDE",
        "production_status": "produced",
        "release_status": "blocked",
        "provenance_type": "historical source",
        "shared_version": "win95-workbench-1.0.0",
        "duration_seconds": None,
        "dimensions": {"width": 1920, "height": 1080},
        "fps": None,
        "outputs": outputs,
        "variants": [
            {"name": "original", "files": ["source/original.png"],
             "notes": "Unmodified 800x600 WinWorld capture, Microsoft Visual Basic 4.0 32-bit on Windows 95."},
            {"name": "editorial-frame", "files": ["exports/editorial-frame.png"],
             "notes": "Full frame, uniform 1.8x resize, black pillarbox; still hold, no motion."},
        ],
        "sources": [
            {"path": "../../../sources/SCRIPT.md", "lines": [49, 49],
             "sha256": "3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb", "relationship": "source creative brief"},
            {"path": "../../../sources/SCRIPT.md", "lines": [130, 134],
             "sha256": "3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb", "relationship": "source creative brief"},
            {"path": "../../../sources/ASSET_PLAN.md", "lines": [89, 89],
             "sha256": "8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7", "relationship": "source lead"},
            {"path": "source/original.png", "url": source["source_url"], "page": source["source_page_url"],
             "sha256": source["original_file_sha256"], "accessed": source["access_date"], "relationship": "historical original"},
            {"path": "exports/editorial-frame.png", "derived_from": "source/original.png", "relationship": "derivative crop",
             "notes": "No pixels cropped from the screenshot; relationship label per output contract for framed derivatives."},
            {"path": "evidence/source.json", "relationship": "source record"},
        ],
        "credits": [
            {"type": "historical screenshot", "credit": None,
             "proposed_credit": source["proposed_credit_text"],
             "status": "Not cleared. Rights unresolved (R14); see evidence/rights.json."}
        ],
        "tests": [
            {"test": "editorial frame machine checks", "evidence": "evidence/render-tests.json",
             "result": "passed" if render["all_passed"] else "failed"},
            {"test": "manual visual review at full size (1:1) and 720p", "evidence": "qa.md", "result": "passed; see qa.md"},
            {"test": "tools/validate_delivery.py --id HIST-02", "evidence": "qa.md", "result": "see qa.md for recorded output"},
        ],
        "unresolved_gates": ["R14"],
        "toolchain": {
            "os": platform.platform(),
            "python": sys.version.split()[0],
            "packages": {"Pillow": PIL.__version__},
            "commands": [
                "python assets/historical/HIST-02/src/make_editorial_frame.py",
                "python assets/historical/HIST-02/src/check_editorial_frame.py",
                "python assets/historical/HIST-02/src/build_delivery.py",
                "python tools/validate_delivery.py --id HIST-02",
            ],
            "acquisition": "curl 8.18.0 anonymous HTTPS GET on 2026-09-15; no account, no terms accepted",
            "network_used": True,
            "installs_performed": False,
            "font_files_distributed": False,
            "remote_assets": [],
        },
        "notes": [
            "Real historical screenshot acquired from WinWorld; not an AI recreation or mockup.",
            "Edition verified as 32-bit via sibling About capture from the same session (see evidence/claim-checks.json).",
            "Release blocked on R14 rights review; production complete as an internal proof.",
            "Microsoft's screenshot terms forbid using portions of screenshots: downstream crops/zooms (e.g. XTRA-05) need the rights decision first.",
        ],
    }
    (BASE / "delivery.json").write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"delivery.json written with {len(outputs)} outputs")


if __name__ == "__main__":
    main()
