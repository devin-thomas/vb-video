#!/usr/bin/env python3
"""Write HIST-03 delivery.json with a hashed inventory of every file except delivery.json and state.json.

Run from the repository root after src/frame.py:
    python assets/historical/HIST-03/src/build_delivery.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SKIP = {"delivery.json", "state.json"}


def role(rel: str) -> str:
    if rel == "source/original.gif":
        return "historical original (byte-exact acquisition)"
    if rel.startswith("source/source-page/"):
        return "preserved source page"
    if rel == "exports/editorial-frame.png":
        return "rendered still (editorial-frame variant)"
    if rel.startswith("proofs/"):
        return "720p inspection proof"
    if rel.startswith("candidates/"):
        return "alternate candidate record"
    if rel.startswith("evidence/pages/"):
        return "preserved evidence page"
    if rel.startswith("evidence/"):
        return "evidence / QA"
    if rel.startswith("src/"):
        return "editable input / build script"
    return "QA record" if rel == "qa.md" else "other"


def main() -> None:
    state = json.loads((HERE / "state.json").read_text(encoding="utf-8"))
    outputs = []
    for path in sorted(p for p in HERE.rglob("*") if p.is_file()):
        rel = path.relative_to(HERE).as_posix()
        if rel in SKIP or "__pycache__" in rel:
            continue
        data = path.read_bytes()
        outputs.append({"path": rel, "role": role(rel), "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest()})
    delivery = {
        "id": "HIST-03",
        "title": "VB 6.0 IDE",
        "production_status": state["production_status"],
        "release_status": state["release_status"],
        "provenance_type": "historical source (Microsoft documentation figure) with resize-only editorial framing",
        "shared_version": "win95-workbench-1.0.0",
        "duration_seconds": None,
        "dimensions": {"width": 1920, "height": 1080},
        "fps": None,
        "outputs": outputs,
        "variants": [
            {"name": "original", "path": "source/original.gif", "dimensions": {"width": 779, "height": 574},
             "timing": "still; hold for editorial timing"},
            {"name": "editorial-frame", "path": "exports/editorial-frame.png",
             "dimensions": {"width": 1920, "height": 1080}, "timing": "still; hold for editorial timing",
             "derived_from": "source/original.gif", "transform": "uniform resize x1.630662 to 1270x936 at (325,72); no crop"}
        ],
        "sources": [
            {"path": "source/original.gif", "relationship": "historical original",
             "url": "https://learn.microsoft.com/en-us/previous-versions/visualstudio/visual-basic-6/images/aa733577.avp02001(en-us,vs.60).gif",
             "record": "evidence/source.json", "sha256": "cbd44443b36479dfcb2b0f46fc0f3c951bd60a0f7479ad0872efef64d0febd08"},
            {"path": "exports/editorial-frame.png", "relationship": "derivative crop",
             "note": "Resize-only framing; nothing is cropped from the image itself."},
            {"path": "candidates/wikipedia-vb6-on-xp/original.png", "relationship": "historical original (alternate candidate, not delivered)",
             "url": "https://upload.wikimedia.org/wikipedia/en/0/0e/Visual_Basic_6.0_on_Windows_XP.png",
             "record": "candidates/wikipedia-vb6-on-xp/source.json"},
            {"path": "../../../sources/ASSET_PLAN.md", "lines": [89, 89],
             "sha256": "8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7", "relationship": "planning lead"},
            {"path": "../../../sources/SCRIPT.md", "lines": [679, 701],
             "sha256": "3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb", "relationship": "narrative context"}
        ],
        "credits": [
            {"asset": "source/original.gif, exports/editorial-frame.png",
             "text": "Microsoft Visual Basic 6.0 documentation, Figure 2.1 \"The Visual Basic integrated development environment\". (c) Microsoft Corporation. Used with permission from Microsoft.",
             "status": "proposed; permission not confirmed (R14 rights review)"}
        ],
        "tests": [
            {"name": "validate_delivery", "command": "python tools/validate_delivery.py --id HIST-03", "result": "see qa.md"},
            {"name": "framing geometry and reversibility", "command": "see qa.md", "result": "see qa.md"},
            {"name": "manual inspection 1080p and 720p", "result": "see qa.md"}
        ],
        "unresolved_gates": ["R14"],
        "toolchain": {
            "python": "3.14.0",
            "pillow": "12.3.0",
            "curl": "8.18.0 (x86_64-w64-mingw32, Schannel)",
            "render_command": "python assets/historical/HIST-03/src/frame.py",
            "inventory_command": "python assets/historical/HIST-03/src/build_delivery.py",
            "fonts": "none (no text rendered)"
        },
        "notes": [
            "Historical proof with unresolved rights. Release is blocked until the R14 rights review is recorded.",
            "Microsoft's in-figure callouts are original to the source and retained.",
            "VB6 identity rests on publication in Microsoft's VB6 documentation. Pixel capture version (6.0 vs reused 5.0 art) is not proven; see evidence/source.json identity_limits."
        ]
    }
    (HERE / "delivery.json").write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"delivery.json written with {len(outputs)} outputs")


if __name__ == "__main__":
    main()
