#!/usr/bin/env python3
"""HIST-16: write state.json and delivery.json (hashed inventory of every delivered file).

Run from the repository root after build_frame.py and after every evidence/QA file is final:
    python assets/historical/HIST-16/src/finish_delivery.py
"""
from __future__ import annotations

import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

from PIL import __version__ as PIL_VERSION

BASE = Path(__file__).resolve().parents[1]
PRODUCTION = "produced"
RELEASE = "blocked"

ROLES = {
    "source/original.gif": "historical original (byte-exact download, unmodified)",
    "exports/editorial-frame.png": "editorial frame 1920x1080 (derived: whole image, 3x nearest, credit line)",
    "proofs/editorial-frame-720.png": "720p review proof",
    "src/build_frame.py": "editable framing source / render driver",
    "src/finish_delivery.py": "delivery bundler",
    "qa.md": "QA record",
    "evidence/source.json": "source record",
    "evidence/rights.json": "rights record",
    "evidence/claim-checks.json": "editorial gate record",
    "evidence/provenance.json": "provenance record",
    "evidence/source-excerpts.md": "source excerpts",
    "evidence/framing.json": "framing / reversibility record",
}


def role_for(rel: str) -> str:
    if rel in ROLES:
        return ROLES[rel]
    if rel.startswith("evidence/source-pages/"):
        return "preserved source page / HTTP headers (third-party, evidence only)"
    if rel.startswith("evidence/candidates/"):
        return "fallback candidate original (public domain, evidence only)"
    return "evidence / QA"


def main() -> None:
    skip = {"delivery.json", "state.json"}
    files = sorted(p for p in BASE.rglob("*") if p.is_file() and p.relative_to(BASE).as_posix() not in skip
                   and "__pycache__" not in p.parts)
    outputs = []
    for p in files:
        rel = p.relative_to(BASE).as_posix()
        data = p.read_bytes()
        outputs.append({"path": rel, "role": role_for(rel), "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest()})

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    delivery = {
        "id": "HIST-16",
        "title": "Java AWT application",
        "production_status": PRODUCTION,
        "release_status": RELEASE,
        "provenance_type": "historical source (third-party screenshot, rights restricted) with framed derivative",
        "shared_version": "win95-workbench-1.0.0",
        "duration_seconds": None,
        "dimensions": {"width": 1920, "height": 1080},
        "fps": None,
        "outputs": outputs,
        "variants": [
            {"name": "original", "files": ["source/original.gif"],
             "notes": "Byte-exact 506x232 GIF87a from The Java Tutorial (Sun Microsystems), Princeton spring-1996 mirror."},
            {"name": "editorial-frame", "files": ["exports/editorial-frame.png"], "derived_from": "source/original.gif",
             "proof_720": "proofs/editorial-frame-720.png",
             "notes": "Still; holds for editorial timing. No crop; 3x nearest; authored credit line. See evidence/framing.json."},
        ],
        "sources": [
            {"path": "../../../sources/SCRIPT.md", "lines": [629, 631],
             "sha256": "3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb",
             "relationship": "narration and visual brief"},
            {"path": "../../../sources/ASSET_PLAN.md", "lines": [99, 99],
             "sha256": "8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7",
             "relationship": "asset-plan row (lead checked; see evidence/provenance.json)"},
            {"path": "source/original.gif", "url": "https://www.cs.princeton.edu/courses/archive/spring96/cs333/java/tutorial/ui/overview/images/GUIWindow.gif",
             "sha256": "e11f4e6c41ec798b9f663cb99d1c7950853fde2b0125060fdfaf1209b9d3b5ed",
             "relationship": "historical original"},
            {"path": "exports/editorial-frame.png", "relationship": "derivative crop (no crop applied; framed enlargement)"},
            {"path": "evidence/candidates/AWT_at_Linux.png", "relationship": "stock candidate (public domain, Commons, 2007)"},
            {"path": "evidence/candidates/Easy_Java_AWT_example.jpg", "relationship": "stock candidate (public domain, Commons, 2006)"},
        ],
        "credits": [
            {"type": "historical original (rights restricted)", "file": "source/original.gif",
             "credit": "The Java Tutorial, © 1995 Sun Microsystems, Inc. (now Oracle). “AWT Components” example window.",
             "rights_status": "restricted — all rights reserved; no licence; release blocked"},
            {"type": "candidate, not used in export", "file": "evidence/candidates/AWT_at_Linux.png",
             "credit": "“AWT at Linux” by Sven, Wikimedia Commons, public domain"},
            {"type": "candidate, not used in export", "file": "evidence/candidates/Easy_Java_AWT_example.jpg",
             "credit": "“Easy Java AWT example” by Fiete Groth, Wikimedia Commons, public domain"},
        ],
        "tests": json.loads((BASE / "src" / "tests.json").read_text(encoding="utf-8")),
        "unresolved_gates": ["R14"],
        "toolchain": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "packages": {"Pillow": PIL_VERSION},
            "downloader": "curl (Git for Windows), anonymous HTTPS GET",
            "font": "LiberationSans-Regular.ttf (installed system font, not distributed)",
            "commands": [
                "python assets/historical/HIST-16/src/build_frame.py",
                "python assets/historical/HIST-16/src/finish_delivery.py",
                "python tools/validate_delivery.py --id HIST-16",
            ],
            "installs_performed": False,
            "font_files_distributed": False,
        },
        "notes": [
            "Produced as an internal proof. Release is blocked: the selected image is Sun copyright, all rights reserved (R14 open).",
            "Two public-domain Commons fallbacks are preserved in evidence/candidates/ but are 2006-2007 captures, not 1995-96 AWT.",
            "state.json and delivery.json are excluded from the hashed inventory.",
        ],
    }
    (BASE / "delivery.json").write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    state = {
        "id": "HIST-16",
        "production_status": PRODUCTION,
        "release_status": RELEASE,
        "assigned_agent": "Claude Code (Opus 5) worker under Historical Screenshots Manager vb-7a",
        "updated_at": now,
        "blockers": [
            "R14: selected image is © 1995 Sun Microsystems (now Oracle), all rights reserved; no licence found. Needs a rights decision."
        ],
        "reviewer": None,
        "notes": [
            "Historical original, source pages, rights/source records, and framed export delivered; see delivery.json and qa.md.",
            "Public-domain fallbacks from a later era are in evidence/candidates/.",
        ],
    }
    (BASE / "state.json").write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote delivery.json with {len(outputs)} outputs; state {PRODUCTION}/{RELEASE}")


if __name__ == "__main__":
    main()
