#!/usr/bin/env python3
"""Write HIST-11 delivery.json with byte sizes and SHA-256 for every delivered file.

Run from the repository root after build_frame.py and after qa.md/evidence are final:
    python assets/historical/HIST-11/src/make_delivery.py
"""
from __future__ import annotations
import hashlib
import json
import platform
import sys
from pathlib import Path
import PIL

ASSET = Path(__file__).resolve().parents[1]
ROLES = {
    "qa.md": "evidence / QA",
    "source/original.tif": "historical original (native archival scan)",
    "exports/editorial-frame.png": "rendered still (editorial-frame variant)",
    "proofs/editorial-frame-720.png": "720p proof",
    "src/build_frame.py": "reproduction script",
    "src/framing.json": "framing parameters",
    "src/framing-result.json": "measured framing result",
    "src/make_delivery.py": "delivery inventory script",
}


def role(rel: str) -> str:
    if rel in ROLES:
        return ROLES[rel]
    if rel.startswith("evidence/source-page/"):
        return "preserved source page"
    return "evidence / QA"


def main() -> None:
    files = sorted(
        p.relative_to(ASSET).as_posix()
        for p in ASSET.rglob("*")
        if p.is_file() and p.name not in ("delivery.json", "state.json") and "__pycache__" not in p.parts
    )
    outputs = []
    for rel in files:
        data = (ASSET / rel).read_bytes()
        outputs.append({"path": rel, "role": role(rel), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    delivery = {
        "id": "HIST-11",
        "title": "Visual Basic 4 retail box",
        "production_status": "produced",
        "release_status": "blocked",
        "provenance_type": "historical source (archival scan, unlicensed third-party artwork) with derivative editorial framing",
        "shared_version": "win95-workbench-1.0.0",
        "duration_seconds": None,
        "dimensions": {"width": 1920, "height": 1080},
        "fps": None,
        "outputs": outputs,
        "variants": [
            {"name": "original", "files": ["source/original.tif"], "note": "Native 2584x2502 500-dpi TIFF, byte-identical to the Internet Archive file (MD5/SHA-1 match). Hold for editorial timing."},
            {"name": "editorial-frame", "files": ["exports/editorial-frame.png", "src/framing.json"], "note": "Uncropped fit into 1920x1080 safe area on neutral matte; still, hold for editorial timing (no animation)."}
        ],
        "sources": [
            {"path": "../../../sources/ASSET_PLAN.md", "lines": [94, 94], "sha256": "8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7", "relationship": "source creative brief"},
            {"path": "../../../sources/SCRIPT.md", "lines": [122, 128], "sha256": "3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb", "relationship": "source creative brief"},
            {"path": "source/original.tif", "url": "https://archive.org/details/Microsoft_Visual_Basic_Enterprise_Edition_Version_4.0_Microsoft_1995", "relationship": "historical original", "record": "evidence/source.json"},
            {"path": "exports/editorial-frame.png", "relationship": "derivative crop", "record": "src/framing.json"}
        ],
        "credits": [
            {"type": "historical original", "credit": "Microsoft Visual Basic 4.0 Enterprise Edition CD-ROM (1995), (c) Microsoft Corporation. Scan via Internet Archive (textfiles.com CD-ROM software collection).", "rights_status": "blocked: no license (evidence/rights.json)"}
        ],
        "tests": [
            {"test": "archive integrity", "result": "passed: local MD5 c8eb1774a9a244d6e8ad372144f0936d and SHA-1 9da64545824a3c7e4c51bb146b11b4ad950eb0d5 match IA manifest"},
            {"test": "version/edition text read at native resolution", "result": "passed: 'Visual Basic Enterprise Edition', 'Version 4.0', '(c) 1991-1995', 'Part No. 64575'"},
            {"test": "source excerpts byte-match sources/ line ranges", "result": "passed"},
            {"test": "export dimensions, aspect, matte", "result": "passed: 1920x1080 RGB; placed 967x936 at (476,72); aspect error 0.033%", "evidence": "src/framing-result.json"},
            {"test": "manual visual review 1080p (full frame and 1:1 crops) and 720p", "result": "passed; see qa.md"},
            {"test": "tools/validate_delivery.py --id HIST-11", "result": "see qa.md (run after this file is written)"}
        ],
        "unresolved_gates": ["R14"],
        "toolchain": {
            "os": platform.platform(),
            "python": sys.version.split()[0],
            "packages": {"Pillow": PIL.__version__},
            "curl": "8.21.0 (Windows, Schannel)",
            "network_used": True,
            "network_note": "Anonymous downloads from archive.org only; web.archive.org unreachable from this environment.",
            "installs_performed": False,
            "font_files_distributed": False,
            "commands": [
                "python assets/historical/HIST-11/src/build_frame.py",
                "python assets/historical/HIST-11/src/make_delivery.py",
                "python tools/validate_delivery.py --id HIST-11"
            ]
        },
        "notes": [
            "SUBSTITUTION: the ticket names a retail box; no authorized-archive box image exists. The acquired original is the VB4 retail install CD, which SCRIPT.md:122 lists first. See evidence/candidates.json and review question RQ-2.",
            "Release blocked on R14 (RQ-1). Keep out of the cleared-media bin.",
            "Review questions RQ-1..RQ-3 are in evidence/claim-checks.json."
        ]
    }
    (ASSET / "delivery.json").write_text(json.dumps(delivery, indent=2) + "\n", encoding="utf-8")
    print(f"delivery.json written with {len(outputs)} outputs")


if __name__ == "__main__":
    main()
