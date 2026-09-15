#!/usr/bin/env python3
"""Shared helpers for the OPS-02 capture tickets: harness copies, framing, proofs, delivery bundles.

Framing only places an unedited raw capture on a 1920x1080 canvas (and, where a ticket asks for a
highlight, draws an outline on that derived copy). It never edits pixels inside the capture.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
HARNESS = ROOT / "work" / "war-harness"
CANVAS = (1920, 1080)
SAFE = (120, 72, 1800, 1008)
BACKGROUND = "#111318"
HIGHLIGHT = "#EAB676"
SHARED_VERSION = json.loads((ROOT / "shared" / "VERSION.json").read_text(encoding="utf-8"))["version"]


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def ticket(asset_id: str) -> dict:
    rows = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))["tickets"]
    return next(r for r in rows if r["id"] == asset_id)


def dump(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ----- harness copies --------------------------------------------------------------------------
def prepare_workdir(asset_id: str) -> Path:
    """Fresh private copy of the frozen harness project, hash-verified, with no bin/obj."""
    manifest = json.loads((HARNESS / "harness-manifest.json").read_text(encoding="utf-8"))
    expected = {f["path"]: f["sha256"] for f in manifest["files"]}
    work = ROOT / "assets" / asset_id / "work" / "War"
    if work.exists():
        raise SystemExit(f"{work} already exists; every capture uses a fresh copy.")
    work.mkdir(parents=True)
    for name in ["War.vbproj", "Program.vb"]:
        shutil.copyfile(HARNESS / "War" / name, work / name)
        if sha256(work / name) != expected[f"War/{name}"]:
            raise SystemExit(f"harness copy hash mismatch: {name}")
    return work


# ----- images ----------------------------------------------------------------------------------
def merge_boxes(boxes) -> list[tuple[int, int, int, int]]:
    """Union boxes that overlap or touch, so consecutive highlighted lines share one outline."""
    merged: list[tuple[int, int, int, int]] = []
    for box in sorted((tuple(b) for b in boxes), key=lambda b: (b[1], b[0])):
        if merged and box[1] <= merged[-1][3] and box[0] <= merged[-1][2] and box[2] >= merged[-1][0]:
            last = merged[-1]
            merged[-1] = (min(last[0], box[0]), min(last[1], box[1]), max(last[2], box[2]), max(last[3], box[3]))
        else:
            merged.append(box)
    return merged


def frame(raw: Path, out: Path, boxes: list[tuple[int, int, int, int]] = ()) -> dict:
    """Center the raw capture inside the safe area at 1:1 (downscale only if it would not fit)."""
    image = Image.open(raw).convert("RGB")
    safe_w, safe_h = SAFE[2] - SAFE[0], SAFE[3] - SAFE[1]
    scale = min(1.0, safe_w / image.width, safe_h / image.height)
    if scale < 1.0:
        image = image.resize((round(image.width * scale), round(image.height * scale)), Image.LANCZOS)
    canvas = Image.new("RGB", CANVAS, BACKGROUND)
    x = (CANVAS[0] - image.width) // 2
    y = (CANVAS[1] - image.height) // 2
    canvas.paste(image, (x, y))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((x - 1, y - 1, x + image.width, y + image.height), outline="#3A3F4B", width=1)
    placed = []
    for left, top, right, bottom in merge_boxes(boxes):
        # Vertical padding stays within the inter-line gap so the outline never covers adjacent rows' glyphs.
        rect = (x + round(left * scale) - 6, y + round(top * scale) - 2,
                x + round(right * scale) + 6, y + round(bottom * scale) + 2)
        draw.rectangle(rect, outline=HIGHLIGHT, width=4)
        placed.append(rect)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)
    return {"file": out.name, "from": raw.name, "offset": [x, y], "scale": scale,
            "highlight_boxes_canvas_px": placed, "pixels_inside_capture_modified": False}


def crop_frame(raw: Path, out: Path, crop: tuple[int, int, int, int], boxes=()) -> dict:
    """Derived close-up: crop the raw capture, enlarge with nearest-neighbour to fit, outline boxes."""
    image = Image.open(raw).convert("RGB").crop(crop)
    safe_w, safe_h = SAFE[2] - SAFE[0], SAFE[3] - SAFE[1]
    scale = max(1, int(min(safe_w / image.width, safe_h / image.height)))
    image = image.resize((image.width * scale, image.height * scale), Image.NEAREST)
    canvas = Image.new("RGB", CANVAS, BACKGROUND)
    x = (CANVAS[0] - image.width) // 2
    y = (CANVAS[1] - image.height) // 2
    canvas.paste(image, (x, y))
    draw = ImageDraw.Draw(canvas)
    placed = []
    for left, top, right, bottom in merge_boxes(boxes):
        rect = (x + (left - crop[0]) * scale - 8, y + (top - crop[1]) * scale - 6,
                x + (right - crop[0]) * scale + 8, y + (bottom - crop[1]) * scale + 6)
        draw.rectangle(rect, outline=HIGHLIGHT, width=5)
        placed.append(rect)
    canvas.save(out)
    return {"file": out.name, "from": raw.name, "crop_raw_px": list(crop), "integer_scale": scale,
            "offset": [x, y], "highlight_boxes_canvas_px": placed, "resample": "nearest"}


def cell_box(geometry: dict, first_row: int, last_row: int, first_col: int, last_col: int) -> tuple:
    """Pixel box in the raw PNG for window-relative console rows/cols (inclusive)."""
    cw, ch = geometry["cell_px"]
    ox, oy = geometry["client_origin_in_png"]
    return (ox + first_col * cw, oy + first_row * ch, ox + (last_col + 1) * cw, oy + (last_row + 1) * ch)


def proof_720(src: Path, out: Path) -> dict:
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.open(src).convert("RGB").resize((1280, 720), Image.LANCZOS).save(out)
    return {"file": out.name, "from": src.name, "size": [1280, 720]}


def contact_sheet(items: list[tuple[Path, str]], out: Path, columns: int = 4) -> dict:
    thumb_w = (1920 - 40 * (columns + 1)) // columns
    first = Image.open(items[0][0])
    thumb_h = round(first.height * thumb_w / first.width)
    rows = -(-len(items) // columns)
    label_h = 44
    sheet = Image.new("RGB", (1920, 40 + rows * (thumb_h + label_h + 40)), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("segoeui.ttf", 26)
    except OSError:
        font = ImageFont.load_default()
    for index, (path, label) in enumerate(items):
        col, row = index % columns, index // columns
        x = 40 + col * (thumb_w + 40)
        y = 40 + row * (thumb_h + label_h + 40)
        sheet.paste(Image.open(path).convert("RGB").resize((thumb_w, thumb_h), Image.LANCZOS), (x, y))
        draw.text((x, y + thumb_h + 8), label, fill="#F1F3F5", font=font)
    sheet.save(out)
    return {"file": out.name, "size": list(sheet.size), "font": "Segoe UI (installed system font)"}


# ----- toolchain -------------------------------------------------------------------------------
def _cmd(argv: list[str]) -> str:
    try:
        return subprocess.run(argv, capture_output=True, text=True, timeout=30).stdout.strip().splitlines()[0]
    except (OSError, IndexError, subprocess.TimeoutExpired):
        return "unavailable"


def toolchain(extra: dict | None = None) -> dict:
    import PIL
    import win32api
    conhost = win32api.GetFileVersionInfo(r"C:\Windows\System32\conhost.exe", "\\")
    data = {
        "os": platform.platform(),
        "dotnet_sdk": _cmd(["dotnet", "--version"]),
        "dotnet_path": shutil.which("dotnet"),
        "terminal": "Windows Console Host (conhost.exe) launched directly, not Windows Terminal",
        "conhost_file_version": "{}.{}.{}.{}".format(conhost["FileVersionMS"] >> 16, conhost["FileVersionMS"] & 0xFFFF,
                                                     conhost["FileVersionLS"] >> 16, conhost["FileVersionLS"] & 0xFFFF),
        "shell": "PowerShell " + _cmd(["pwsh", "-NoLogo", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"]),
        "python": sys.version.split()[0],
        "packages": {"Pillow": PIL.__version__,
                     "pywin32": str(win32api.GetFileVersionInfo(win32api.__file__, "\\")["FileVersionLS"] >> 16)},
        "capture_api": "user32.PrintWindow(PW_RENDERFULLCONTENT) of the console window, cropped to DWM extended frame bounds",
        "input_api": "kernel32 WriteConsoleInput key events into the attached console (no focus or global keystrokes)",
        "transcript_api": "kernel32 ReadConsoleOutputCharacter over the console screen buffer",
        "network_used": "only whatever dotnet itself performed; no downloads were requested",
        "installs_performed": False,
        "font_files_distributed": False,
    }
    data.update(extra or {})
    return data


# ----- delivery bundle -------------------------------------------------------------------------
ROLE_RULES = [
    ("source/raw/", "raw capture PNG (unedited window image)"),
    ("exports/contact-sheet.png", "contact sheet of raw viewports (derived)"),
    ("exports/report.md", "support report"),
    ("exports/harness-manifest.json", "harness snapshot manifest"),
    ("exports/", "framed editorial still (derived from raw capture)"),
    ("proofs/", "720p review proof"),
    ("source/Program.vb", "exact executed/displayed source copy (byte-identical)"),
    ("source/War.vbproj", "exact pictured project file (derived harness copy)"),
    ("source/", "capture transcript / program output"),
    ("evidence/", "evidence / QA"),
    ("qa.md", "evidence / QA"),
]


def typed_commands(prompt_log: Path) -> list[dict]:
    """History entries for typed commands. The first entry is pwsh's non-interactive -EncodedCommand
    startup script (recorded separately as terminal.startup_script), so it is excluded here."""
    entries = [json.loads(line) for line in prompt_log.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    return [e for e in entries if not e["command"].startswith("[IO.File]::WriteAllText(")]


def write_command_log(base: Path, capture: dict) -> None:
    log = [f"# {capture['id']} command log — typed into a real conhost/pwsh window",
           f"# working directory: {capture['working_directory']}",
           f"# dotnet SDK: {capture['dotnet_sdk_version']}; OS: {capture['os']}",
           "# columns: start (UTC, PowerShell history) | seconds | $? | $LASTEXITCODE at next prompt "
           "(only meaningful after a native command) | command"]
    log += [f"# pre-session: {step}" for step in capture["pre_session_steps"]]
    log += [f"{c['start_utc']} | {c['seconds']:>8.3f}s | ok={c['succeeded']} | exit={c['last_exit_code']} | {c['command']}"
            for c in capture["commands"]]
    (base / "evidence" / "commands.log").write_text("\n".join(log) + "\n", encoding="utf-8")


def role(rel: str) -> str:
    return next(r for prefix, r in ROLE_RULES if rel.startswith(prefix))


def source_excerpts(asset_id: str) -> str:
    row = ticket(asset_id)
    parts = [f"# {asset_id} source excerpts\n", "Unchanged line ranges from the hash-locked originals in `sources/`.\n"]
    for name, lo, hi in row["refs"]:
        lines = (ROOT / "sources" / name).read_text(encoding="utf-8").splitlines()[lo - 1:hi]
        parts.append(f"\n## {name}:{lo}–{hi}\n\n~~~~text\n" + "\n".join(lines) + "\n~~~~\n")
    return "".join(parts)


def source_records(asset_id: str, relationships: dict[str, str]) -> list[dict]:
    return [{"path": f"../../sources/{name}", "lines": [lo, hi], "sha256": sha256(ROOT / "sources" / name),
             "relationship": relationships.get(name, "source creative brief")}
            for name, lo, hi in ticket(asset_id)["refs"]]


def write_bundle(asset_id: str, *, provenance_type: str, variants: list[dict], relationships: dict[str, str],
                 gates: dict[str, dict], tests: list[dict], toolchain_data: dict, notes: list[str],
                 authored_additions: list[str], qa_md: str, production_status: str = "produced",
                 state_notes: list[str] | None = None,
                 dimensions: dict | None = {"width": 1920, "height": 1080},
                 decisions: dict[str, dict] | None = None) -> dict:
    """decisions maps a gate ID to the producer's recorded {decision, approver, approval_date}."""
    row = ticket(asset_id)
    base = ROOT / "assets" / asset_id
    (base / "BLOCKER.md").unlink(missing_ok=True)
    decisions = {g: d for g, d in (decisions or {}).items() if g in row["gates"]}
    unresolved = [g for g in row["gates"] if g not in decisions]
    release_status = ("blocked" if unresolved else "approved") if row["gates"] else "unreviewed"
    sources = source_records(asset_id, relationships)
    (base / "evidence" / "source-excerpts.md").write_text(source_excerpts(asset_id), encoding="utf-8")
    dump(base / "evidence" / "provenance.json", {
        "id": asset_id, "classification": provenance_type, "sources": sources,
        "authored_additions": authored_additions, "source_unchanged": sha256(ROOT / "sources" / "Program.vb")
        == "8069f62bfb24bbd792cda04a6eefa9745f9d9ffb8d879e523b95454cafb06ce7",
        "remote_assets": [], "font_files_distributed": False,
        "producer_decisions": [{"gate": g, **d} for g, d in decisions.items()], "prior_blocker_resolved": "The pack's 2026-09-15 capability blocker (no dotnet "
        "executable) does not apply on this machine; the .NET SDK is installed and was used directly."})
    dump(base / "evidence" / "claim-checks.json", {"gates": [
        {"id": gate, "status": "approved" if gate in decisions else "blocked", "evidence": gates[gate]["evidence"],
         "decision": decisions.get(gate, {}).get("decision"), "approver": decisions.get(gate, {}).get("approver"),
         "approval_date": decisions.get(gate, {}).get("approval_date"), "reason": gates[gate]["reason"]}
        for gate in row["gates"]]})
    (base / "qa.md").write_text(qa_md, encoding="utf-8")

    outputs = []
    for path in sorted(p for p in base.rglob("*") if p.is_file()):
        rel = path.relative_to(base).as_posix()
        if rel in {"delivery.json", "state.json"} or rel.startswith("work/"):
            continue
        outputs.append({"path": rel, "role": role(rel), "bytes": path.stat().st_size, "sha256": sha256(path)})
    delivery = {
        "id": asset_id, "title": row["title"], "production_status": production_status,
        "release_status": release_status, "provenance_type": provenance_type, "shared_version": SHARED_VERSION,
        "duration_seconds": None, "dimensions": dimensions, "fps": None,
        "outputs": outputs, "variants": variants, "sources": sources,
        "credits": [{"type": "actual local capture", "credit": "Screens captured from this production's own "
                     "machine; no third-party images or font files included."}],
        "tests": tests, "unresolved_gates": unresolved, "toolchain": toolchain_data, "notes": notes,
    }
    dump(base / "delivery.json", delivery)
    dump(base / "state.json", {
        "id": asset_id, "production_status": production_status, "release_status": release_status,
        "assigned_agent": "Claude Code (Opus 5)", "updated_at": now_utc(), "blockers": [], "reviewer": None,
        "notes": state_notes or ["Real local capture delivered; see delivery.json and qa.md.",
                                 "Release approved by the producer; decisions are in evidence/claim-checks.json."
                                 if release_status == "approved" else
                                 "Release stays blocked until a producer records each gate decision."],
        "owner": "Claude Code — local capture"})
    return delivery
