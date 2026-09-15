"""Write BROLL-01 delivery.json with byte sizes and SHA-256 of every file except delivery.json/state.json.

Usage (from the repository root): python assets/broll/BROLL-01/src/finish_delivery.py
Run last, after every other file in the folder is final.
"""
import hashlib
import json
from pathlib import Path

base = Path("assets/broll/BROLL-01")
state = json.loads((base / "state.json").read_text(encoding="utf-8"))

roles = {
    "qa.md": "QA report",
    "exports/candidates.md": "candidate report (variant: candidate-report)",
    "exports/acquisition-handoff.md": "acquisition handoff (ungated pending approval + H02)",
    "evidence/candidates.json": "structured candidates",
    "evidence/claim-checks.json": "evidence / gate record",
    "evidence/provenance.json": "evidence / provenance",
    "evidence/source-excerpts.md": "evidence / literal source excerpts",
    "src/build_excerpts.py": "reproduction script",
    "src/finish_delivery.py": "reproduction script",
}

outputs = []
for path in sorted(p for p in base.rglob("*") if p.is_file()):
    rel = path.relative_to(base).as_posix()
    if rel in ("delivery.json", "state.json"):
        continue
    data = path.read_bytes()
    outputs.append({
        "path": rel,
        "role": roles.get(rel, "supporting file"),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    })

delivery = {
    "id": "BROLL-01",
    "title": "Hands shuffling physical cards",
    "production_status": state["production_status"],
    "release_status": state["release_status"],
    "provenance_type": "stock footage scouting record (candidates inspected; no media acquired)",
    "shared_version": "win95-workbench-1.0.0",
    "duration_seconds": None,
    "dimensions": None,
    "fps": None,
    "outputs": outputs,
    "variants": [
        {"name": "candidate-report", "files": ["exports/candidates.md"]}
    ],
    "sources": [
        {"path": "../../../sources/ASSET_PLAN.md", "lines": [109, 122],
         "sha256": "8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7",
         "relationship": "literal excerpt (shot request, row 117)"},
        {"path": "../../../sources/SCRIPT.md", "lines": [799, 805],
         "sha256": "3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb",
         "relationship": "literal excerpt (B-roll suggestion 1)"},
        {"url": "https://mixkit.co/free-stock-video/deck-of-cards-being-shuffled-100384/",
         "accessed": "2026-09-15", "relationship": "stock candidate (rank 1, not acquired)"},
        {"url": "https://mixkit.co/free-stock-video/person-shuffling-playing-cards-over-green-table-100398/",
         "accessed": "2026-09-15", "relationship": "stock candidate (rank 2, not acquired)"},
        {"url": "https://mixkit.co/free-stock-video/close-up-of-hands-shuffling-playing-cards-100372/",
         "accessed": "2026-09-15", "relationship": "stock candidate (rank 3, not acquired)"}
    ],
    "credits": [
        {"asset": "all ranked candidates", "credit": "Mixkit",
         "required": False, "basis": "Mixkit Stock Video Free License: attribution not required (credit appreciated)"}
    ],
    "tests": [
        {"name": "validate_delivery", "command": "python tools/validate_delivery.py --id BROLL-01",
         "result": "see qa.md (run after this file is written)"},
        {"name": "motion review (frame sampling of in-page previews)", "result": "done for 3 candidates; continuous real-time playback not observed"},
        {"name": "1080p/720p export inspection", "result": "not applicable: no rendered or acquired media; previews were 720p streams"}
    ],
    "unresolved_gates": ["R14"],
    "toolchain": {
        "python": "3.14.0",
        "git": "2.53.0.windows.1",
        "browser": "Claude Browser pane (embedded Chromium; version not exposed)",
        "web": "Claude Code WebFetch and WebSearch tools",
        "ffprobe": "not used (no media acquired)"
    },
    "notes": [
        "Scouting complete is not cleared media acquired. No download was performed.",
        "Pexels could not be inspected (Cloudflare verification interstitial / HTTP 403); not bypassed.",
        "Release blocked pending R14 review questions and batched download approval."
    ]
}

(base / "delivery.json").write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print(f"wrote delivery.json with {len(outputs)} outputs")
