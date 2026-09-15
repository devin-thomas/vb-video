#!/usr/bin/env python3
"""Write assets/historical/XTRA-02/delivery.json with real byte sizes and SHA-256 hashes.

Run from the repository root after render_frame.py and after qa.md is final:
  python assets/historical/XTRA-02/src/write_delivery.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[2]

ROLES = {
    "source/original.jp2": "historical original (native JPEG 2000 scan leaf, unmodified)",
    "exports/editorial-frame.png": "editorial framing copy (derived, 1920x1080 pillarbox)",
    "proofs/editorial-frame-720p.png": "QA proof (720p downscale of editorial frame)",
    "evidence/folio-showthrough.png": "evidence crop (page-number show-through)",
    "evidence/framing.json": "evidence / framing geometry",
    "evidence/source.json": "evidence / source record",
    "evidence/rights.json": "evidence / rights record",
    "evidence/provenance.json": "evidence / provenance",
    "evidence/claim-checks.json": "evidence / gate and claim checks",
    "evidence/source-excerpts.md": "evidence / source excerpts",
    "qa.md": "QA record",
    "src/render_frame.py": "render script",
    "src/write_delivery.py": "delivery metadata script",
}


def record(rel: str) -> dict:
    data = (BASE / rel).read_bytes()
    return {"path": rel, "role": ROLES[rel], "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main() -> None:
    state = json.loads((BASE / "state.json").read_text(encoding="utf-8"))
    script = ROOT / "sources" / "SCRIPT.md"
    delivery = {
        "id": "XTRA-02",
        "title": "Period MSDN advertisement",
        "production_status": state["production_status"],
        "release_status": state["release_status"],
        "provenance_type": "historical source",
        "shared_version": "win95-workbench-1.0.0",
        "duration_seconds": None,
        "dimensions": {"width": 1920, "height": 1080},
        "fps": None,
        "outputs": [record(rel) for rel in sorted(ROLES)],
        "variants": [
            {"name": "original", "path": "source/original.jp2", "timeline": None,
             "note": "Uncropped native scan, 2489x3228; not 16:9 by design."},
            {"name": "editorial-frame", "path": "exports/editorial-frame.png", "timeline": None,
             "note": "Still; holds for editorial timing. 720p proof at proofs/editorial-frame-720p.png."},
        ],
        "sources": [
            {"path": "../../../sources/SCRIPT.md", "lines": [49, 49],
             "sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
             "relationship": "script cue fulfilled (\"old MSDN ads\")"},
            {"path": "source/original.jp2", "record": "evidence/source.json",
             "url": "https://archive.org/download/boardwatch-1996-06/boardwatch-1996-06_jp2.zip/boardwatch-1996-06_jp2%2Fboardwatch-1996-06_0096.jp2",
             "item": "https://archive.org/details/boardwatch-1996-06",
             "access_date_utc": "2026-09-15T20:32:43Z",
             "relationship": "historical original"},
            {"path": "exports/editorial-frame.png", "from": "source/original.jp2",
             "relationship": "derivative framing (uncropped pillarbox with authored caption)"},
        ],
        "credits": [
            {"text": "Microsoft Developer Network advertisement, Boardwatch Magazine, June 1996, p. 97. © 1996 Microsoft Corporation. Scan via Internet Archive (boardwatch-1996-06).",
             "rights_status": "unknown / not cleared", "record": "evidence/rights.json"},
        ],
        "tests": [
            {"name": "source leaf identity (dimensions vs scandata leaf 96)", "result": "pass"},
            {"name": "source unchanged across render (SHA-256 before/after)", "result": "pass"},
            {"name": "aspect preserved, uncropped, inside safe area", "result": "pass"},
            {"name": "export 1920x1080 and 720p proof 1280x720 (Pillow)", "result": "pass"},
            {"name": "printed page 97 from neighbour folios and show-through", "result": "pass"},
            {"name": "manual inspection at full size (whole frame and 1:1 crops) and 720p", "result": "pass", "record": "qa.md"},
            {"name": "python tools/validate_delivery.py --id XTRA-02", "result": "see qa.md (verbatim)"},
        ],
        "unresolved_gates": ["R14"],
        "toolchain": {
            "python": "3.14.0",
            "pillow": "12.3.0",
            "openjpeg": "2.5.4",
            "curl": "8.21.0 (Windows)",
            "os": "Microsoft Windows 11 Pro 10.0.26200",
            "fonts": ["C:\\Windows\\Fonts\\segoeui.ttf", "C:\\Windows\\Fonts\\segoeuib.ttf"],
            "commands": [
                "python assets/historical/XTRA-02/src/render_frame.py",
                "python assets/historical/XTRA-02/src/write_delivery.py",
                "python tools/validate_delivery.py --id XTRA-02",
            ],
        },
        "notes": [
            "Script-supplement asset (SCRIPT.md:49), not an original asset-plan row.",
            "Historical proof: release blocked until R14 rights question RQ-XTRA-02-1 is decided in the review deck.",
            "Caption text in the editorial frame is an authored production addition (evidence/provenance.json).",
        ],
    }
    (BASE / "delivery.json").write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote delivery.json with {len(delivery['outputs'])} outputs")


if __name__ == "__main__":
    main()
