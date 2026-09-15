"""Write assets/historical/HIST-05/delivery.json with byte sizes and SHA-256 for every delivered file.

Run from anywhere: python assets/historical/HIST-05/tools/build_delivery.py
"""
import hashlib
import json
from pathlib import Path

ASSET = Path(__file__).resolve().parents[1]
ROOT = ASSET.parents[2]
SKIP = {"delivery.json", "state.json"}

ROLES = {
    "source/": "historical original (acquired file, byte-identical)",
    "exports/": "rendered still",
    "proofs/": "720p review proof",
    "evidence/": "evidence / QA",
    "tools/": "reproduction script",
    "qa.md": "evidence / QA",
}


def role(rel):
    for prefix, name in ROLES.items():
        if rel == prefix or rel.startswith(prefix):
            return name
    return "other"


def shared_version():
    for path in sorted(ROOT.glob("assets/*/OPS-01/delivery.json")):
        try:
            return json.loads(path.read_text(encoding="utf-8")).get("shared_version")
        except (OSError, ValueError):
            pass
    return None


outputs = []
for path in sorted(p for p in ASSET.rglob("*") if p.is_file()):
    rel = path.relative_to(ASSET).as_posix()
    if rel in SKIP or "__pycache__" in rel:
        continue
    data = path.read_bytes()
    outputs.append({"path": rel, "role": role(rel), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})

state = json.loads((ASSET / "state.json").read_text(encoding="utf-8"))
delivery = {
    "id": "HIST-05",
    "title": "Commodore 64 BASIC boot screen",
    "production_status": state["production_status"],
    "release_status": state["release_status"],
    "provenance_type": "historical source: community-uploaded digital image of the Commodore 64 power-on screen (Wikimedia Commons), with a reversible editorial framing copy",
    "shared_version": shared_version(),
    "shared_version_note": "Recorded for traceability only; the editorial frame uses no shared template or style from OPS-01.",
    "duration_seconds": None,
    "dimensions": {"width": 1920, "height": 1080},
    "fps": None,
    "outputs": outputs,
    "variants": [
        {
            "name": "original",
            "paths": ["source/original.gif"],
            "timeline": None,
            "note": "As published on Commons: 360 x 248 GIF, 2 frames of 500 ms looping (cursor blink). Unmodified."
        },
        {
            "name": "editorial-frame",
            "paths": ["exports/editorial-frame.png"],
            "timeline": None,
            "note": "Still. Frame 1 (cursor visible), 3x nearest-neighbour, centred on black 1920 x 1080. Transform in evidence/framing.json; hold length is the editor's choice."
        }
    ],
    "sources": [
        {"path": "../../../sources/ASSET_PLAN.md", "lines": [91, 91],
         "sha256": "8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7", "relationship": "source creative brief"},
        {"path": "../../../sources/SCRIPT.md", "lines": [73, 75],
         "sha256": "3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb", "relationship": "source creative brief"},
        {"path": "source/original.gif", "record": "evidence/source.json",
         "url": "https://upload.wikimedia.org/wikipedia/commons/4/48/C64_startup_animiert.gif",
         "page": "https://commons.wikimedia.org/wiki/File:C64_startup_animiert.gif",
         "sha1": "79ba302dee5ef066edd31d1e66c5f7c728b62699", "relationship": "historical original"},
        {"path": "exports/editorial-frame.png", "record": "evidence/framing.json", "relationship": "derivative crop"},
        {"url": "https://archive.org/details/commodore-64-user-guide/page/n27/mode/1up",
         "relationship": "external primary source for wording verification; not copied"}
    ],
    "credits": [
        {
            "asset": "source/original.gif and exports/editorial-frame.png",
            "creator": "Gedeon (Wikimedia Commons user)",
            "title": "File:C64 startup animiert.gif",
            "source_url": "https://commons.wikimedia.org/wiki/File:C64_startup_animiert.gif",
            "license": "Public domain as tagged: PD-ineligible, PD-text, PD-font, PD-US-1978-89",
            "license_url": "https://commons.wikimedia.org/wiki/Template:PD-ineligible",
            "rights_status": "unresolved: not independently cleared (evidence/rights.json)",
            "proposed_credit_text": "C64 startup screen, by Gedeon, via Wikimedia Commons (public domain)",
            "accessed": "2026-09-15"
        }
    ],
    "tests": [
        {"name": "SHA-1 of acquired file equals Commons imageinfo sha1", "command": "PowerShell Get-FileHash -Algorithm SHA1 source/original.gif", "result": "pass"},
        {"name": "Palette, geometry and cursor measurement", "command": "python -X utf8 assets/historical/HIST-05/tools/measure.py assets/historical/HIST-05/source/original.gif", "result": "run; transparency unused; screen area 320 x 203 (anomaly recorded)"},
        {"name": "Reversible framing, uniform blocks, untouched background, safe band", "command": "python -X utf8 assets/historical/HIST-05/tools/verify_reverse.py assets/historical/HIST-05", "result": "pass (exit 0)"},
        {"name": "Manual view at 1920 x 1080", "path": "exports/editorial-frame.png", "result": "pass: legible, undistorted, border intact"},
        {"name": "Manual view at 1280 x 720", "path": "proofs/editorial-frame-720.png", "result": "pass: text and cursor legible"},
        {"name": "Wording verified against Commodore 64 User's Guide p. 12 page image", "result": "pass"},
        {"name": "Delivery validator", "command": "python tools/validate_delivery.py --id HIST-05", "result": "see qa.md"}
    ],
    "unresolved_gates": ["R14"],
    "toolchain": {
        "python": "3.14.0",
        "pillow": "12.3.0",
        "git": "2.53.0.windows.1",
        "os": "Windows 11 Pro 10.0.26200",
        "render_command": "python -X utf8 assets/historical/HIST-05/tools/frame.py assets/historical/HIST-05/source/original.gif assets/historical/HIST-05/exports/editorial-frame.png assets/historical/HIST-05/evidence/framing.json --frame 1 --bg \"#000000\""
    },
    "notes": [
        "Model and version verified from the image text against the Commodore 64 User's Guide, not from appearance.",
        "Capture method undocumented; digital two-colour render; screen area 320 x 203 rather than 320 x 200. Authenticity is an open review question.",
        "Release blocked until the review deck records R14 and authenticity decisions."
    ]
}
(ASSET / "delivery.json").write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote delivery.json with {len(outputs)} outputs; shared_version={delivery['shared_version']}")
