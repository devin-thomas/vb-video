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
    "source/mixkit-100384-deck-of-cards-being-shuffled-1080p.mp4": "acquired original (unmodified third-party stock video)",
    "source/source.json": "source record for the acquired original",
    "evidence/frames/frame-in-05.000s.png": "inspection frame at the segment in point (5.0 s, 1920x1080)",
    "evidence/frames/frame-mid-10.500s.png": "inspection frame at the segment mid point (10.5 s, 1920x1080)",
    "evidence/frames/frame-out-16.000s.png": "inspection frame at the segment out point (16.0 s, 1920x1080)",
    "evidence/frames/frame-in-05.000s-720p.png": "720p inspection frame (in point downscaled to 1280x720)",
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
    "provenance_type": "acquired third-party stock original (rank 1 downloaded unmodified under an approved free licence) plus the scouting record for ranks 2-3",
    "shared_version": "win95-workbench-1.0.0",
    # From ffprobe on the acquired original; see source/source.json and qa.md section 3.
    "duration_seconds": 19.394375,
    "dimensions": "1920x1080",
    "fps": 23.976023976023978,
    "outputs": outputs,
    "variants": [
        {"name": "candidate-report", "files": ["exports/candidates.md"]},
        {"name": "acquired-original", "files": ["source/mixkit-100384-deck-of-cards-being-shuffled-1080p.mp4"],
         "timeline": {"selected_in_seconds": 5.0, "selected_out_seconds": 16.0, "selected_length_seconds": 11.0,
                      "head_handle_seconds": 5.0, "tail_handle_seconds": 3.394375,
                      "note": "Proposed local edit range (riffle then bridge), confirmed against the acquired file; not final narration sync."}}
    ],
    "sources": [
        {"path": "../../../sources/ASSET_PLAN.md", "lines": [109, 122],
         "sha256": "8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7",
         "relationship": "literal excerpt (shot request, row 117)"},
        {"path": "../../../sources/SCRIPT.md", "lines": [799, 805],
         "sha256": "3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb",
         "relationship": "literal excerpt (B-roll suggestion 1)"},
        {"url": "https://mixkit.co/free-stock-video/deck-of-cards-being-shuffled-100384/",
         "accessed": "2026-09-15",
         "relationship": "acquired stock original (rank 1) — real capture of a third-party work, downloaded unmodified",
         "path": "source/mixkit-100384-deck-of-cards-being-shuffled-1080p.mp4",
         "source_record": "source/source.json",
         "creator": "Mixkit (Envato); no individual creator named on the asset page",
         "license": "Mixkit Stock Video Free License",
         "license_url": "https://mixkit.co/license/",
         "sha256": "65b65dd09d9fcb074304b9e33123aaa6d4dd0da2906833a36c2b0c8727f73ff2",
         "rights_status": "recorded, not cleared (R14 open)"},
        {"url": "https://mixkit.co/free-stock-video/person-shuffling-playing-cards-over-green-table-100398/",
         "accessed": "2026-09-15", "relationship": "stock candidate (rank 2, not acquired)"},
        {"url": "https://mixkit.co/free-stock-video/close-up-of-hands-shuffling-playing-cards-100372/",
         "accessed": "2026-09-15", "relationship": "stock candidate (rank 3, not acquired)"}
    ],
    "credits": [
        {"asset": "source/mixkit-100384-deck-of-cards-being-shuffled-1080p.mp4",
         "credit": "Footage: Mixkit",
         "required": False,
         "basis": "Mixkit Stock Video Free License, read 2026-09-15: 'Attribution is not required, however, we would appreciate it if you credit Mixkit where reasonably possible.'",
         "license_url": "https://mixkit.co/license/",
         "note": "Credit wording is the producer's call (see project rulings); this is the licence-supported suggestion, not a final on-screen credit."},
        {"asset": "ranked candidates 2-3 (not acquired)", "credit": "Mixkit",
         "required": False, "basis": "Mixkit Stock Video Free License: attribution not required (credit appreciated)"}
    ],
    "tests": [
        {"name": "validate_delivery", "command": "python tools/validate_delivery.py --id BROLL-01",
         "result": "see qa.md (run after this file is written)"},
        {"name": "motion review (frame sampling of in-page previews)", "result": "done for 3 candidates; continuous real-time playback not observed"},
        {"name": "download", "command": 'curl -L -A "Mozilla/5.0" <approved 1080p download URL>',
         "result": "The approved URL returned the site's download modal (HTTP 200, text/html, 2738 B) naming the asset URL; the bytes were fetched from there (HTTP 200, video/mp4, 73935932 B). No login, payment, CAPTCHA, bot check or terms gate encountered or bypassed."},
        {"name": "ffprobe verification", "command": "ffprobe -v error -show_entries format=format_name,duration,size,bit_rate -show_streams -of json <file>",
         "result": "1920x1080, 19.394375 s, 24000/1001 (23.976) fps, h264 High, 465 frames, no audio stream. Size and sha256 recorded in source/source.json. Matches the scouted clip; fps differs from the page's stated 24."},
        {"name": "1080p/720p manual inspection",
         "result": "Three full-resolution frames (5.0, 10.5, 16.0 s) extracted with ffmpeg and viewed at full size, plus the in-point frame viewed again at 1280x720. No watermark, caption or logo. Casino felt layout confirmed present throughout the segment. Details in qa.md section 3."}
    ],
    "unresolved_gates": ["R14"],
    "toolchain": {
        "python": "3.14.0",
        "git": "2.53.0.windows.1",
        "browser": "Claude Browser pane (embedded Chromium; version not exposed)",
        "web": "Claude Code WebFetch and WebSearch tools",
        "curl": "8.18.0 (x86_64-w64-mingw32), libcurl/8.18.0 Schannel, release 2026-01-07",
        "ffprobe": "6.0-essentials_build-www.gyan.dev",
        "ffmpeg": "6.0-essentials_build-www.gyan.dev"
    },
    "notes": [
        "Produced is not cleared. The original is acquired and verified, but R14 is open and release stays blocked for the OPS-04 review deck.",
        "Devin approved this one download on 2026-09-15, relayed by the B-roll Scouting Manager (session vb-bf). Ranks 2 and 3 were not approved and were not downloaded.",
        "The acquired file is byte-identical to what the server returned: no re-encode, trim, crop or watermark change.",
        "fps mismatch: the asset page and the scouting record state 24 fps; ffprobe reports 24000/1001 (23.976). Duration, dimensions and byte size match the scouted values exactly.",
        "The file has no audio stream, so the narration/audio-clearance question is closed.",
        "Editorial review question: the printed casino felt (yellow '10', betting lines, partial 'TEXAS HOLD'EM' lettering entering frame near the 16.0 s out point) is more present in the cut than scouting implied.",
        "Only 3 of 465 frames were inspected and continuous playback was never watched; motion quality between sample points is unverified.",
        "Pexels could not be inspected (Cloudflare verification interstitial / HTTP 403); not bypassed."
    ]
}

(base / "delivery.json").write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print(f"wrote delivery.json with {len(outputs)} outputs")
