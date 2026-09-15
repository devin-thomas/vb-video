"""HIST-14: write delivery.json from the files on disk (hashes, sizes, variants, tests).

Usage: python assets/historical/HIST-14/tools/finish.py <tests.json>
tests.json holds the manually recorded test results (list of objects).
"""
import hashlib
import json
import platform
import sys
from pathlib import Path

from PIL import Image, __version__ as PIL_VERSION

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[2]

ROLES = {
    "source/original.jpg": "historical original (native JPEG, byte-identical to the Wikimedia Commons original)",
    "exports/editorial-frame.png": "editorial frame 1920x1080 (derived: scaled + matted, no crop)",
    "proofs/editorial-frame-720.png": "720p review proof",
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    tests = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    state = json.loads((BASE / "state.json").read_text(encoding="utf-8"))
    source = json.loads((BASE / "evidence/source.json").read_text(encoding="utf-8"))
    framing = json.loads((BASE / "evidence/framing.json").read_text(encoding="utf-8"))
    claims = json.loads((BASE / "evidence/claim-checks.json").read_text(encoding="utf-8"))

    outputs = []
    for p in sorted(BASE.rglob("*")):
        rel = p.relative_to(BASE).as_posix()
        if not p.is_file() or rel in ("delivery.json", "state.json") or "__pycache__" in rel:
            continue
        role = ROLES.get(rel) or ("tooling (reproduction script)" if rel.startswith("tools/") else "evidence / QA")
        outputs.append({"path": rel, "role": role, "bytes": p.stat().st_size, "sha256": sha(p)})

    src_rel = lambda name: f"../../../sources/{name}"
    delivery = {
        "id": "HIST-14",
        "title": "NeXT Cube product photograph",
        "production_status": state["production_status"],
        "release_status": state["release_status"],
        "provenance_type": "historical source (third-party licensed photograph of a museum-held NeXTcube)",
        "shared_version": "not_applicable (archive still; no shared template used)",
        "duration_seconds": None,
        "dimensions": {"width": 1920, "height": 1080},
        "fps": None,
        "outputs": outputs,
        "variants": [
            {"name": "original", "files": ["source/original.jpg"],
             "notes": f"Untouched native original, {source['original_dimensions'][0]}x{source['original_dimensions'][1]}."},
            {"name": "editorial-frame", "files": ["exports/editorial-frame.png"],
             "derived_from": "source/original.jpg",
             "notes": f"Scale {framing['scale']:.6f}, offset {framing['offset']}, matte RGB {framing['matte_rgb']}; no crop. Still: hold for editorial timing."},
        ],
        "sources": [
            {"path": "source/original.jpg", "url": source["original_file_url"], "page": source["source_url"],
             "relationship": "historical original"},
            {"path": "exports/editorial-frame.png", "relationship": "derivative crop (framing only, no crop)"},
            {"path": src_rel("SCRIPT.md"), "lines": [653, 655], "sha256": sha(ROOT / "sources/SCRIPT.md"),
             "relationship": "narration and visual brief"},
            {"path": src_rel("ASSET_PLAN.md"), "lines": [97, 97], "sha256": sha(ROOT / "sources/ASSET_PLAN.md"),
             "relationship": "source creative brief (lead only)"},
        ],
        "credits": [{"type": "third-party photograph", "credit": source["credit_text"],
                     "license": source["license_name"], "license_url": source["license_url"]}],
        "tests": tests,
        "unresolved_gates": [g["id"] for g in claims["gates"] if g["status"] not in ("approved", "not_applicable")],
        "toolchain": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "packages": {"Pillow": PIL_VERSION},
            "acquisition": "python urllib GET from upload.wikimedia.org with Retry-After backoff; SHA-1 checked against Commons API",
            "framing": "python assets/historical/HIST-14/tools/frame.py assets/historical/HIST-14/source/original.jpg assets/historical/HIST-14",
            "finishing": "python assets/historical/HIST-14/tools/finish.py <tests.json>",
            "font_files_distributed": False,
            "network_dependencies_in_outputs": False,
        },
        "notes": [
            "Editorial still only; no text, UI, or annotation is added to the photograph.",
            "Review questions HIST-14-Q1..Q3 are in evidence/claim-checks.json.",
        ],
    }
    (BASE / "delivery.json").write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"delivery.json written with {len(outputs)} outputs")


if __name__ == "__main__":
    main()
