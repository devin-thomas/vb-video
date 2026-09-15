#!/usr/bin/env python3
"""HIST-17: inventory every delivered file (bytes + SHA-256) into delivery.json and write state.json.

Run from the repository root after acquire.py, acquire_candidates.py and build_frame.py:
    python assets/historical/HIST-17/src/finish.py
"""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[2]
SKIP = {"delivery.json", "state.json"}


def role(rel: str) -> str:
    if rel == "source/original.html":
        return "historical original (archived HTML, id_ raw bytes)"
    if rel.startswith("source/candidates/"):
        return "alternate candidate (raw HTML / capture)"
    if rel.startswith("source/raw/") and rel.endswith(".png"):
        return "uncropped capture (evidence)"
    if rel.startswith("source/"):
        return "archived original component"
    if rel.startswith("exports/"):
        return "derivative crop (editorial frame)"
    if rel.startswith("proofs/"):
        return "evidence / QA proof"
    if rel.startswith("src/"):
        return "reproduction script"
    return "evidence / QA"


def main() -> None:
    outputs = []
    for path in sorted(p for p in BASE.rglob("*") if p.is_file()):
        rel = path.relative_to(BASE).as_posix()
        if rel in SKIP or "__pycache__" in rel:
            continue
        data = path.read_bytes()
        outputs.append({"path": rel, "role": role(rel), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    frame = json.loads((BASE / "evidence/frame.json").read_text(encoding="utf-8"))

    def sha(p: str) -> str:
        return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()

    delivery = {
        "id": "HIST-17",
        "title": "TUCOWS archived site circa 1996",
        "production_status": "produced",
        "release_status": "blocked",
        "provenance_type": "historical original: Wayback Machine capture of http://www.tucows.com/ dated 1996-10-22 17:56:12 GMT, with a derivative 16:9 editorial crop",
        "shared_version": "not_applicable (archival capture; no shared template used)",
        "duration_seconds": None,
        "dimensions": {"width": 1920, "height": 1080},
        "fps": None,
        "outputs": outputs,
        "variants": [
            {"name": "original", "files": ["source/original.html", "source/raw/wayback-toolbar-fullpage.png",
                                            "source/raw/wayback-replay-fullpage.png"],
             "note": "Raw archived HTML plus uncropped Chromium captures: one with the Wayback toolbar (date and URL visible), one frame-less."},
            {"name": "editorial-frame", "files": ["exports/editorial-frame.png"],
             "crop_css_px": frame["crop_css_px"],
             "note": "Top 1280x720 CSS px of the frame-less replay, rendered at 1.5x device scale. Editorial hold; no timing is set here."},
        ],
        "sources": [
            {"path": "../../../sources/ASSET_PLAN.md", "lines": [100, 100], "sha256": sha("sources/ASSET_PLAN.md"),
             "relationship": "source creative brief"},
            {"path": "../../../sources/SCRIPT.md", "lines": [595, 597], "sha256": sha("sources/SCRIPT.md"),
             "relationship": "source creative brief"},
            {"path": "source/original.html", "url": "https://web.archive.org/web/19961022175612/http://www.tucows.com:80/",
             "relationship": "historical original"},
            {"path": "exports/editorial-frame.png", "relationship": "derivative crop"},
            {"path": "source/candidates/B-idirect-19961230/original.html",
             "url": "https://web.archive.org/web/19961230051406/http://tucows.idirect.com:80/",
             "relationship": "historical original (alternate candidate)"},
            {"path": "source/candidates/C-phoenix-win95oct96-19961117/original.html",
             "url": "https://web.archive.org/web/19961117161725/http://tucows.phoenix.net:80/archive/win95oct96.html",
             "relationship": "historical original (alternate candidate)"},
        ],
        "credits": [
            {"type": "historical web page", "credit": "TUCOWS home page, 22 October 1996 (© 1996 Scott A. Swedorski / TUCOWS)",
             "status": "proposed; rights unresolved (evidence/rights.json)"},
            {"type": "archive", "credit": "Internet Archive Wayback Machine, capture 19961022175612",
             "status": "access for scholarship and research under IA terms; not a reuse licence"},
        ],
        "tests": [
            {"test": "tools/validate_delivery.py --id HIST-17", "result": "see qa.md for the recorded run"},
            {"test": "identity and date from the archived bytes",
             "result": "passed: Memento-Datetime Tue, 22 Oct 1996 17:56:12 GMT; <title>The Ultimate Collection of Winsock Software</title>; footer Copyright © 1996 Scott A. Swedorski"},
            {"test": "editorial frame has no Wayback UI", "result": "passed: wm-ipp toolbar element absent in the if_ replay; confirmed visually"},
            {"test": "crop matches uncropped capture", "evidence": "proofs/frame-crop-check.png",
             "result": "passed: visual comparison with exports/editorial-frame.png shows the same region and layout"},
            {"test": "manual visual review", "result": "Viewed exports/editorial-frame.png at 1920x1080 and proofs/editorial-frame-720.png at 1280x720; logo, headline, banner and mirror rows are legible at 720p. See qa.md."},
        ],
        "unresolved_gates": ["R14"],
        "toolchain": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "chromium": frame["render"]["chromium"],
            "packages": {"playwright": version("playwright"), "Pillow": version("Pillow")},
            "git": subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip(),
            "network_used": True,
            "network_hosts": ["web.archive.org", "web-static.archive.org", "athena.archive.org (Wayback analytics beacon loaded by the toolbar page)"],
            "installs_performed": False,
            "font_files_distributed": False,
        },
        "notes": [
            "Rendered in a 2026 Chromium, not a 1996 browser. Arial (named by the page's CSS) is used from Windows 11, so fonts, table borders and anti-aliasing differ from Netscape Navigator 3 or IE3 in 1996.",
            "The Wayback replay draws each image from its nearest capture. The page is 1996-10-22. Logo.gif is 1996-10-22. blue.gif, fast-burst.gif and cs_ad.gif are 1996-10-23. The background tile is 1996-12-28 (background.gif; the page asks for BACKGROUND.GIF). See evidence/acquisition-log.json.",
            "The editorial frame omits the regional mirror lists below the Canada heading and the copyright footer; the Wayback toolbar is excluded.",
            "Alternate candidates B (idirect mirror, 1996-12-30) and C (phoenix mirror, 1996-11-17) are preserved with deficiencies recorded in evidence/source.json.",
            "Produced is not release approval. R14 rights review is open.",
        ],
    }
    (BASE / "delivery.json").write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    state = {
        "id": "HIST-17",
        "production_status": "produced",
        "release_status": "blocked",
        "assigned_agent": "Historical Screenshots worker (manager session vb-7a)",
        "updated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "blockers": ["R14: no licence found for the 1996 TUCOWS page, logo or ConnectSoft banner; rights review question raised."],
        "reviewer": None,
        "notes": ["Archived capture, uncropped evidence, and 16:9 editorial frame delivered; see delivery.json and qa.md.",
                  "Release stays blocked pending the rights decision in the review deck."],
    }
    (BASE / "state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print(f"inventoried {len(outputs)} files")


if __name__ == "__main__":
    main()
