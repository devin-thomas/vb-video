#!/usr/bin/env python3
"""Write HIST-12 delivery.json with byte sizes and SHA-256 for every delivered file.

Run from the repository root after build_frame.py and after qa.md/evidence are final:
    python assets/historical/HIST-12/src/make_delivery.py
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
    "source/original.gif": "historical original (native archived web GIF, byte-exact)",
    "exports/editorial-frame.png": "rendered still (editorial-frame variant)",
    "proofs/editorial-frame-720.png": "720p proof",
    "src/build_frame.py": "reproduction script",
    "src/framing.json": "framing parameters",
    "src/framing-result.json": "measured framing result",
    "src/make_delivery.py": "delivery inventory script",
}


def role(rel: str) -> str:
    return ROLES.get(rel, "evidence / QA")


def main() -> None:
    files = sorted(
        p.relative_to(ASSET).as_posix()
        for p in ASSET.rglob("*")
        if p.is_file()
        and p.name not in ("delivery.json", "state.json")
        and "__pycache__" not in p.parts
    )
    outputs = []
    for rel in files:
        data = (ASSET / rel).read_bytes()
        outputs.append(
            {
                "path": rel,
                "role": role(rel),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )

    delivery = {
        "id": "HIST-12",
        "title": "Borland Delphi 1.0 IDE",
        "production_status": "produced",
        "release_status": "blocked",
        "provenance_type": "historical source (archived vendor screenshot, unlicensed third-party copyright) with derivative editorial framing",
        "shared_version": "win95-workbench-1.0.0",
        "duration_seconds": None,
        "dimensions": {"width": 1920, "height": 1080},
        "fps": None,
        "outputs": outputs,
        "variants": [
            {
                "name": "original",
                "files": ["source/original.gif"],
                "note": "Native 444x282 16-colour GIF87a, byte-identical to the Wayback capture (payload SHA-1 matches the CDX digest 3AB42XGSKUFD5LQFFJKPEE5IAHFCWKPW). Hold for editorial timing.",
            },
            {
                "name": "editorial-frame",
                "files": ["exports/editorial-frame.png", "src/framing.json"],
                "note": "Uncropped 3x integer nearest-neighbour upscale (1332x846) centred on a neutral matte in 1920x1080; still, hold for editorial timing (no animation).",
            },
        ],
        "sources": [
            {
                "path": "../../../sources/ASSET_PLAN.md",
                "lines": [95, 95],
                "sha256": "8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7",
                "relationship": "source creative brief",
            },
            {
                "path": "../../../sources/SCRIPT.md",
                "lines": [619, 621],
                "sha256": "3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb",
                "relationship": "source creative brief",
            },
            {
                "path": "source/original.gif",
                "url": "https://web.archive.org/web/19961223104420id_/http://www.borland.com:80/delphi/delphi1.0/guide/fig1.gif",
                "relationship": "historical original",
                "record": "evidence/source.json",
            },
            {
                "path": "exports/editorial-frame.png",
                "relationship": "derivative crop",
                "record": "src/framing.json",
            },
        ],
        "credits": [
            {
                "type": "historical original",
                "credit": "Borland International, Inc. - Delphi 1.0 Reviewer's Guide (1995), via the Internet Archive Wayback Machine",
                "rights_status": "blocked: no licence (evidence/rights.json); credit text is an authored proposal pending the R14 decision",
            }
        ],
        "tests": [
            {
                "test": "archive integrity of the acquired original",
                "result": "passed: payload SHA-1 base32 3AB42XGSKUFD5LQFFJKPEE5IAHFCWKPW matches the Wayback CDX digest for captures 19961223104420 and 19970509094337 (payload 35,163 bytes; the CDX length 35,423 is the compressed WARC record length)",
            },
            {
                "test": "host page capture re-verified on acquisition",
                "result": "passed: guide/8.1.1.4.html re-fetched, 8,533 bytes, sha256 bc0b1abdc248f00275e21fc738c6f72a8ca5d504361be386203644bb1835339a, identical to the value recorded in the blocked candidate record",
            },
            {
                "test": "identity and version read at native resolution",
                "result": "passed: 'Delphi - Project1' title bar, Object Inspector with 'Warning: TButton' and Properties/Events tabs, Form1 designer, UNIT1.PAS code window with 'TForm1 = class(TForm)'; Delphi 1 / 16-bit confirmed by Windows 3.x window chrome and the VBX palette tab. No version string is printed in the image.",
            },
            {
                "test": "watermark / added-mark check at native and 2x",
                "result": "passed: none present; nothing removed",
            },
            {
                "test": "source excerpts byte-match sources/ line ranges",
                "result": "passed",
            },
            {
                "test": "export dimensions, aspect, matte, reversibility",
                "result": "passed: 1920x1080 RGB; placed 1332x846 at (294,117); aspect error 0.000%; decimating the placed region back to 444x282 reproduces the original raster byte for byte",
                "evidence": "src/framing-result.json",
            },
            {
                "test": "manual visual review 1080p (full frame) and 720p",
                "result": "passed; see qa.md",
            },
            {
                "test": "tools/validate_delivery.py --id HIST-12",
                "result": "see qa.md (run after this file is written)",
            },
        ],
        "unresolved_gates": ["R14"],
        "toolchain": {
            "os": platform.platform(),
            "python": sys.version.split()[0],
            "packages": {"Pillow": PIL.__version__},
            "curl": "8.18.0 (x86_64-w64-mingw32, libcurl/8.18.0, Schannel)",
            "network_used": True,
            "network_note": "Anonymous HTTPS GETs to web.archive.org with a generic User-Agent ('Mozilla/5.0'), authorised by Devin in chat for this file. No account, payment, terms acceptance or CAPTCHA. No other host was contacted for acquisition.",
            "installs_performed": False,
            "font_files_distributed": False,
            "commands": [
                "curl -sS -L --connect-timeout 30 --max-time 180 --retry 5 --retry-delay 20 --retry-all-errors -A \"Mozilla/5.0\" -o source/original.gif \"https://web.archive.org/web/19961223104420id_/http://www.borland.com:80/delphi/delphi1.0/guide/fig1.gif\"",
                "python assets/historical/HIST-12/src/build_frame.py",
                "python assets/historical/HIST-12/src/make_delivery.py",
                "python tools/validate_delivery.py --id HIST-12",
            ],
        },
        "notes": [
            "Resumes the blocked candidate record at commit 94f4073. The search and the three ranked candidates were kept; C1 was acquired once Devin approved the download in chat. C2 and C3 were approved as fallbacks but not downloaded, because C1 proved usable.",
            "The native raster is only 444x282. It is shown at an exact 3x integer upscale on a matte rather than stretched to fill the frame, so it occupies 1332x846 of 1920x1080. Review question RQ-2 asks the editor to confirm that presentation.",
            "Release blocked on R14 (RQ-1). Keep out of the cleared-media bin.",
            "SCRIPT.md:621 ('It looks a lot like the VB IDE') was checked at full resolution against the HIST-01 and HIST-02 VB IDE exports and is accurate as written. No script change is proposed and War/SCRIPT.md was not edited.",
            "Review questions RQ-1 and RQ-2 are in evidence/claim-checks.json.",
        ],
    }
    (ASSET / "delivery.json").write_text(json.dumps(delivery, indent=2) + "\n", encoding="utf-8")
    print(f"delivery.json written with {len(outputs)} outputs")


if __name__ == "__main__":
    main()
