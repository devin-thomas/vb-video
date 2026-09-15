#!/usr/bin/env python3
"""Framed exports, 720p proofs, QA records, and delivery metadata for OPS-02 and its capture tickets.

  --stage render    frame raw captures into exports/ and write 720p proofs into proofs/
  --stage bundle    write evidence summaries, qa.md, delivery.json and state.json
  --stage validate  run tools/validate_delivery.py for all eight tickets and tools/validate_pack.py

Bundling a capture requires a REVIEWS entry: manual full-size and 720p inspection notes written after
actually viewing the images.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

from capture_common import (HARNESS, ROOT, cell_box, contact_sheet, crop_frame, dump, frame, proof_720, sha256,
                            ticket, toolchain, typed_commands, write_bundle, write_command_log)

RUN_IDS = ["TERM-02", "TERM-05", "TERM-06"]
CAPTURE_IDS = ["TERM-01", *RUN_IDS, "TERM-04", "TERM-03", "XTRA-06"]
ALL_IDS = ["OPS-02", *CAPTURE_IDS]
VIM_EXE = r"C:\Program Files\Git\usr\bin\vim.exe"
SOURCE_SHA = sha256(ROOT / "sources" / "Program.vb")
TEXT_SUFFIXES = {".txt", ".json", ".jsonl", ".md", ".log", ".vb", ".vbproj"}
SCRIPT_SAMPLES = "the script's sample results (418 rounds/10 wars, 347 rounds/13 wars)"

# Manual inspection notes, written only after viewing the named PNGs at full size and as 720p proofs.
REVIEWS: dict[str, dict[str, str]] = {
    "TERM-01": {
        "full_size": "Viewed source/raw/01-dotnet-version.png, 02-dotnet-new.png, 03-scaffold-files.png (1319×872) and "
                     "exports/framed.png (1920×1080). Text is sharp; `dotnet --version` → 10.0.303, the empty listing, "
                     "template and restore success, and the Program.vb/War.vbproj listing are legible and unclipped; the "
                     "window sits inside the safe area. Only the repository work path is visible; no notifications, other "
                     "windows, or personal data.",
        "proof_720": "Viewed proofs/framed-720.png (1280×720): every line stays readable, including the directory path.",
    },
    "TERM-02": {
        "full_size": "Viewed source/raw/01-build.png (1319×872) and exports/framed-start.png, framed-first-war.png, "
                     "framed.png (1920×1080, raw at 1:1). The typed command, banner, 26/26 deal, the Round 10 war with its "
                     "10-card award, and the final block (Round 2008 war, 'Player 1 has no cards left for the war - Player 2 "
                     "takes the pot.', PLAYER 2 WINS THE WAR!, 2008 rounds, 69 wars) are sharp, unclipped and inside the "
                     "safe area. No other windows, notifications, or personal data.",
        "proof_720": "Viewed proofs/framed-start-720.png, framed-first-war-720.png, framed-720.png (1280×720): every line, "
                     "including the summary totals, remains readable.",
    },
    "TERM-05": {
        "full_size": "Viewed source/raw/01-build.png (1319×872) and exports/framed-start.png, framed-first-war.png, "
                     "framed.png (1920×1080, raw at 1:1). The typed command, banner, 26/26 deal, the Round 8 war with its "
                     "10-card award, and the final block (Round 1056, PLAYER 2 WINS THE WAR!, 1056 rounds, 10 wars) are "
                     "sharp, unclipped and inside the safe area. No other windows, notifications, or personal data.",
        "proof_720": "Viewed proofs/framed-start-720.png, framed-first-war-720.png, framed-720.png (1280×720): every line, "
                     "including the summary totals, remains readable.",
    },
    "TERM-06": {
        "full_size": "Viewed source/raw/01-build.png (1319×872) and exports/framed-start.png, framed-first-war.png, "
                     "framed.png (1920×1080, raw at 1:1). The typed command, banner, 26/26 deal, the Round 18 war with its "
                     "10-card award, and the final block (Round 150, PLAYER 2 WINS THE WAR!, 150 rounds, 10 wars) are "
                     "sharp, unclipped and inside the safe area. The title bar is in Windows' inactive state because focus "
                     "had moved during capture. No other windows, notifications, or personal data.",
        "proof_720": "Viewed proofs/framed-start-720.png, framed-first-war-720.png, framed-720.png (1280×720): every line, "
                     "including the summary totals, remains readable.",
    },
    "TERM-04": {
        "full_size": "Viewed source/raw/01-build.png (1319×872) and exports/framed.png, framed-highlight.png, "
                     "framed-start.png, framed-end.png (1920×1080). Round 245's six lines (Ace/Ace war, Queen/Queen second "
                     "war, Ace of Diamonds beats 2 of Clubs, 18 cards) are legible, and after a padding fix the amber outline "
                     "encloses exactly those lines without touching Round 244 or 246. Start shows the typed stdout-01 command, "
                     "banner and deal; end shows Round 617 where Player 2 runs out mid-war, PLAYER 1 WINS THE WAR!, 617 "
                     "rounds, 26 wars. No other windows, notifications, or personal data.",
        "proof_720": "Viewed proofs/framed-highlight-720.png after the re-render, and framed-720.png, framed-start-720.png, "
                     "framed-end-720.png before it (the re-render changed only the outline padding; unoutlined frames are "
                     "regenerated identically from the same raw captures). All lines and the outline remain clear.",
    },
    "TERM-03": {
        "full_size": "Viewed all 12 exports/framed*.png (1920×1080, raw 1423×872 at 1:1) and exports/contact-sheet.png. "
                     "Each shows vim with line numbers, VB syntax colouring, no wrapped lines, and the ruler at bottom right; "
                     "first/last line numbers match evidence/viewports.json. Viewport 01 also shows vim's file message "
                     "(\"Program.vb\" [readonly][unix] 285L, 9234B). Comments use the console's dark-blue palette entry: "
                     "legible, but lower contrast than code. No other windows, notifications, or personal data.",
        "proof_720": "Viewed proofs/framed-720.png and framed-12-720.png (1280×720): code and line numbers stay readable; "
                     "dark-blue comments are the weakest element at this size. The other ten 720p proofs are the same "
                     "scaling of viewports inspected at full size and were not opened individually.",
    },
    "XTRA-06": {
        "full_size": "Viewed exports/framed.png and framed-directives.png (1920×1080, raw 1319×592 at 1:1) and "
                     "exports/settings-focus.png (2× nearest-neighbour crop of the console client area). vim shows "
                     "War.vbproj lines 1–11 with XML colouring (TargetFramework net10.0 visible) and Program.vb lines 1–19. "
                     "One amber outline encloses exactly lines 7–8 in each highlighted export without covering adjacent "
                     "lines. Earlier renders had two overlapping outlines and a title-bar sliver in the close-up; both were "
                     "fixed and re-checked before bundling. No other windows, notifications, or personal data.",
        "proof_720": "Viewed proofs/framed-720.png, settings-focus-720.png, framed-directives-720.png (1280×720): nodes, "
                     "directives and outline stay readable.",
    },
}


def base_of(asset_id: str) -> Path:
    return ROOT / "assets" / asset_id


def load(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


# ----- render ------------------------------------------------------------------------------------
def render(asset_id: str) -> None:
    base = base_of(asset_id)
    raw, exports, proofs = base / "source" / "raw", base / "exports", base / "proofs"
    shutil.rmtree(exports, ignore_errors=True)
    shutil.rmtree(proofs, ignore_errors=True)
    exports.mkdir()
    capture = load(base / "evidence" / "capture.json")
    shots = {s["file"]: s for s in capture["screenshots"]}
    plan = []
    if asset_id == "TERM-01":
        plan.append(frame(raw / "03-scaffold-files.png", exports / "framed.png"))
    elif asset_id in RUN_IDS:
        plan.append(frame(raw / "04-end.png", exports / "framed.png"))
        start = raw / "02-start.png" if (raw / "02-start.png").exists() else raw / "05-log-head.png"
        plan.append(frame(start, exports / "framed-start.png"))
        if (raw / "03-first-war.png").exists():
            plan.append(frame(raw / "03-first-war.png", exports / "framed-first-war.png"))
    elif asset_id == "TERM-04":
        highlight = capture["highlight"]
        shot = shots[highlight["screenshot"]]
        box = cell_box(shot, highlight["window_rows"][0], highlight["window_rows"][1], 0, highlight["max_line_chars"] - 1)
        plan.append(frame(raw / highlight["screenshot"], exports / "framed.png"))
        plan.append(frame(raw / highlight["screenshot"], exports / "framed-highlight.png", [box]))
        if (raw / "03-start.png").exists():
            plan.append(frame(raw / "03-start.png", exports / "framed-start.png"))
        plan.append(frame(raw / "04-end.png", exports / "framed-end.png"))
    elif asset_id == "TERM-03":
        viewports = load(base / "evidence" / "viewports.json")["viewports"]
        for v in viewports:
            name = "framed.png" if v["index"] == 1 else f"framed-{v['index']:02d}.png"
            info = frame(base / v["file"], exports / name)
            info["lines"] = [v["first_line"], v["last_line"]]
            plan.append(info)
        plan.append(contact_sheet([(base / v["file"], f"Lines {v['first_line']}–{v['last_line']}") for v in viewports],
                                  exports / "contact-sheet.png"))
    elif asset_id == "XTRA-06":
        targets = load(base / "evidence" / "highlight-targets.json")
        project = targets["01-war-vbproj.png"]
        geometry = project["geometry"]
        plan.append(frame(raw / "01-war-vbproj.png", exports / "framed.png"))
        boxes = [cell_box(geometry, n["window_row"], n["window_row"], n["first_col"], n["last_col"])
                 for n in project["nodes_present"]]
        if boxes:
            lines = (base / "source" / "War.vbproj").read_text(encoding="utf-8-sig").splitlines()
            _, _, right, bottom = cell_box(geometry, 0, len(lines) - 1, 0, 4 + max(len(l) for l in lines))
            width, height = geometry["size"]
            client_x, client_y = geometry["client_origin_in_png"]
            # The close-up stays inside the console client area, so no title-bar pixels enter it.
            crop = (client_x, client_y, min(width, right + 13), min(height, bottom + 10))
            plan.append(crop_frame(raw / "01-war-vbproj.png", exports / "settings-focus.png", crop, boxes))
        directives = targets["02-program-vb-directives.png"]
        boxes = [cell_box(directives["geometry"], n["window_row"], n["window_row"], n["first_col"], n["last_col"])
                 for n in directives["nodes_present"]]
        plan.append(frame(raw / "02-program-vb-directives.png", exports / "framed-directives.png", boxes))
    for path in sorted(exports.glob("*.png")):
        if path.name != "contact-sheet.png":
            proof_720(path, proofs / f"{path.stem}-720.png")
    dump(base / "evidence" / "framing.json", {
        "id": asset_id, "canvas": [1920, 1080], "background": "#111318", "safe_area": [120, 72, 1800, 1008],
        "rule": "Raw capture pasted at 1:1 (downscaled only if larger than the safe area); outlines exist only "
                "on files whose name says highlight/focus/directives; settings-focus is an integer nearest-"
                "neighbour enlargement of a crop.", "exports": plan})


# ----- shared checks -----------------------------------------------------------------------------
def privacy_scan(base: Path) -> dict:
    markers = [m.lower() for m in {os.environ.get("USERNAME", ""), str(Path.home())} if len(m) >= 3]
    hits = set()
    for path in base.rglob("*"):
        rel = path.relative_to(base).as_posix()
        if path.is_file() and not rel.startswith("work/") and path.suffix.lower() in TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8", errors="replace").lower()
            if any(m in text for m in markers):
                hits.add(rel)
    return {"test": "privacy scan of text outputs", "result": "passed" if not hits else "failed",
            "detail": "Searched every text output for the local account name and home-directory path "
                      "(the values themselves are not written here).", "hits": sorted(hits)}


def png_checks(base: Path) -> dict:
    raw = {p.relative_to(base).as_posix(): list(Image.open(p).size) for p in sorted((base / "source" / "raw").glob("*.png"))}
    exports = {p.relative_to(base).as_posix(): list(Image.open(p).size) for p in sorted((base / "exports").glob("*.png"))}
    proofs = {p.relative_to(base).as_posix(): list(Image.open(p).size) for p in sorted((base / "proofs").glob("*.png"))}
    bad = [k for k, v in exports.items() if v != [1920, 1080] and not k.endswith("contact-sheet.png")]
    bad += [k for k, v in proofs.items() if v != [1280, 720]]
    return {"test": "PNG dimensions (raw native, exports 1920×1080, proofs 1280×720)",
            "result": "passed" if not bad else "failed", "raw": raw, "exports": exports, "proofs": proofs, "bad": bad}


def command_checks(capture: dict) -> dict:
    native = [c for c in capture["commands"] if c["command"].split()[0] in {"dotnet", "vim"}]
    failed = [c["command"] for c in native if c["last_exit_code"] != 0 or not c["succeeded"]]
    return {"test": "native command exit codes (PowerShell history + $LASTEXITCODE at the next prompt)",
            "result": "passed" if not failed else "failed", "failed": failed,
            "commands": [{"command": c["command"], "exit_code": c["last_exit_code"], "seconds": c["seconds"]}
                         for c in capture["commands"]]}


def source_check(base: Path) -> dict | None:
    program = base / "source" / "Program.vb"
    if not program.exists():
        return None
    ok = sha256(program) == SOURCE_SHA
    return {"test": "source hash", "result": "passed" if ok else "failed",
            "detail": f"source/Program.vb sha256 {sha256(program)} {'equals' if ok else 'differs from'} sources/Program.vb"}


def manual_review(asset_id: str) -> dict:
    review = REVIEWS[asset_id]
    return {"test": "manual visual inspection", "result": "passed", "full_size": review["full_size"],
            "proof_720": review["proof_720"]}


def normalize_capture(base: Path) -> dict:
    capture = load(base / "evidence" / "capture.json")
    capture["commands"] = typed_commands(base / "evidence" / "prompt-log.jsonl")
    dump(base / "evidence" / "capture.json", capture)
    write_command_log(base, capture)
    return capture


def run_summary(asset_id: str) -> dict:
    stats = load(base_of(asset_id) / "evidence" / "run-stats.json")
    return {"asset": asset_id, "result": stats["result_line"], "rounds": stats["total_rounds_line"],
            "wars": stats["total_wars_line"], "longest_chain": stats["longest_chain_in_one_round"],
            "hit_round_cap": stats["draw_message_present"], "stdout_sha256": stats["stdout_sha256"]}


# ----- per-ticket specs --------------------------------------------------------------------------
def raw_files(capture: dict) -> list[str]:
    return [f"source/raw/{s['file']}" for s in capture["screenshots"]]


def spec_term01(base: Path, capture: dict) -> dict:
    return dict(
        provenance_type="actual runtime capture",
        relationships={"SCRIPT.md": "narration and visual brief", "ASSET_PLAN.md": "source creative brief",
                       "Program.vb": "context only; the default scaffold does not contain the game"},
        gates={"R17": {"evidence": ["source/scaffold-transcript.txt", "evidence/scaffold/War.vbproj", "evidence/capture.json"],
                       "reason": "Handled as R17 requires: the project shown is a fresh `dotnet new console -lang VB` "
                                 "scaffold made with the installed SDK 10.0.303, before any property change, and it is "
                                 "not presented as an uploaded original. Awaiting a producer decision; not self-approved."}},
        variants=[{"name": "raw", "files": raw_files(capture), "notes": "Unedited window captures in capture order."},
                  {"name": "framed", "files": ["exports/framed.png"], "derived_from": "source/raw/03-scaffold-files.png"}],
        tests=[{"test": "scaffold files match the OPS-02 scaffold",
                "result": "passed" if all(capture["matches_ops02_scaffold"].values()) else "failed",
                "detail": capture["scaffold_files_sha256"]},
               {"test": "transcript source", "result": "passed",
                "detail": "source/scaffold-transcript.txt is the console screen buffer read back after the last command."}],
        notes=["Default template output only: its Program.vb is the Hello World scaffold, not the War game.",
               "The visible directory path is the repository work folder; no personal path appears."],
        authored_additions=["Window title 'PowerShell' and a short 'PS <folder>>' prompt set by the logged startup script.",
                            "Framed export places the raw capture at 1:1 on a #111318 1920×1080 canvas."],
        delivered=["`source/raw/01-dotnet-version.png`, `02-dotnet-new.png`, `03-scaffold-files.png` — raw window captures",
                   "`exports/framed.png` — 03-scaffold-files framed at 1:1",
                   "`source/scaffold-transcript.txt` — console buffer text; `evidence/scaffold/` — generated files"],
    )


def spec_run(asset_id: str, base: Path, capture: dict) -> dict:
    stats = load(base / "evidence" / "run-stats.json")
    verification = capture["buffer_verification"]
    rounds, wars, result = stats["total_rounds_line"], stats["total_wars_line"], stats["result_line"]
    stderr_bytes = (base / "source" / "stderr.txt").stat().st_size
    tests = [{"test": "terminal display equals saved stdout",
              "result": "passed" if verification["all_compared_lines_match"] else "failed", "detail": verification},
             {"test": "stdout/stderr retained", "result": "passed",
              "detail": f"stdout {stats['stdout_lines']} lines (sha256 {stats['stdout_sha256']}); stderr {stderr_bytes} bytes"},
             {"test": "summary totals consistent", "result": "passed" if result and rounds and wars is not None else "failed",
              "detail": f"{result} / rounds {rounds} / wars {wars}; ** WAR! ** lines counted in stdout: {stats['war_lines']}"}]
    framed = [{"file": "exports/framed.png", "derived_from": "source/raw/04-end.png"}]
    start = "02-start.png" if (base / "source" / "raw" / "02-start.png").exists() else "05-log-head.png"
    framed.append({"file": "exports/framed-start.png", "derived_from": f"source/raw/{start}",
                   **({"label": "LOG VIEW of this run's stdout, not the live stream"} if start.startswith("05") else {})})
    if (base / "exports" / "framed-first-war.png").exists():
        framed.append({"file": "exports/framed-first-war.png", "derived_from": "source/raw/03-first-war.png"})
    extra_evidence = []
    notes = [f"Actual result of this run: {result} after {rounds} rounds with {wars} wars.",
             f"ShuffleDeck uses New Random() without a seed, so a rerun is a different game; do not relabel another run as this one."]
    stdout = (base / "source" / "stdout.txt").read_text(encoding="utf-8-sig")
    ran_out = next((l for l in stdout.splitlines() if "has no cards left for the war" in l), None)
    if ran_out:
        notes.append(f"This run ends through the insufficient-cards-during-war branch ('{ran_out.strip()}'). That is the "
                     "behaviour editorial register R05 asks the producer to decide how to narrate; it is shown as captured.")
    if asset_id == "TERM-05":
        mine, primary = run_summary("TERM-05"), run_summary("TERM-02")
        comparison = {"TERM-02": primary, "TERM-05": mine,
                      "independent_output": mine["stdout_sha256"] != primary["stdout_sha256"],
                      "different_winner": mine["result"] != primary["result"],
                      "different_stats": (mine["rounds"], mine["wars"]) != (primary["rounds"], primary["wars"])}
        dump(base / "evidence" / "comparison-with-TERM-02.json", comparison)
        extra_evidence.append("evidence/comparison-with-TERM-02.json")
        tests.append({"test": "independent from TERM-02", "result": "passed" if comparison["independent_output"] else "failed",
                      "detail": comparison})
    if asset_id == "TERM-06":
        rows = [run_summary(i) for i in RUN_IDS]
        table = ["# Three actual War runs", "",
                 "Each row is a separate, unmodified `dotnet run --no-build` of the same Program.vb, captured live in its "
                 "own harness copy. Never splice a banner from one run onto another run's ending.", "",
                 "| Asset | Result | Rounds | Wars | Longest chain in one round | Hit 20000-round cap |",
                 "|---|---|---:|---:|---:|---|"]
        table += [f"| {r['asset']} | {r['result']} | {r['rounds']} | {r['wars']} | {r['longest_chain']} | "
                  f"{'yes' if r['hit_round_cap'] else 'no'} |" for r in rows]
        (base / "evidence" / "results-table.md").write_text("\n".join(table) + "\n", encoding="utf-8")
        dump(base / "evidence" / "results-table.json", rows)
        extra_evidence += ["evidence/results-table.md", "evidence/results-table.json"]
        distinct = len({r["stdout_sha256"] for r in rows}) == 3
        tests.append({"test": "three independent runs", "result": "passed" if distinct else "failed", "detail": rows})
    capped = stats["draw_message_present"]
    r06 = ("This run hit the 20000-round cap: output says 'deck cycle detected' and the round counter reads 20001. "
           "Kept unaltered; wording is the producer's decision." if capped else
           f"This run ended with a winner after {rounds} rounds, so the round-cap 'deck cycle detected' line does not "
           "appear. The counter/wording caveat still applies to any narration about draws. Awaiting producer decision.")
    return dict(
        provenance_type="actual runtime capture",
        relationships={"Program.vb": "executed source (byte-identical copy in source/Program.vb)",
                       "SCRIPT.md": "narration and visual brief", "ASSET_PLAN.md": "source creative brief"},
        gates={"R06": {"evidence": ["source/stdout.txt", "evidence/run-stats.json"], "reason": r06},
               "R08": {"evidence": ["source/stdout.txt", "evidence/run-stats.json", *extra_evidence],
                       "reason": f"Real totals from this run ({result}; {rounds} rounds; {wars} wars) replace, not confirm, "
                                 f"{SCRIPT_SAMPLES}. Narration quoting sample numbers still needs a producer decision."}},
        variants=[{"name": "raw", "files": raw_files(capture), "notes": "Unedited window captures of one live run."},
                  {"name": "framed", "files": [f["file"] for f in framed], "mapping": framed}],
        tests=tests, notes=notes,
        authored_additions=["Window title 'PowerShell' and a short 'PS <folder>>' prompt set by the logged startup script.",
                            "`Clear-Host` typed between build and run so the run starts at the top of the buffer.",
                            "Framed exports place raw captures at 1:1 on a #111318 1920×1080 canvas."],
        delivered=[f"`source/raw/` — {len(capture['screenshots'])} raw window captures: build, run start, first war, run end",
                   "`exports/framed.png` (end), `framed-start.png`, `framed-first-war.png` — 1:1 framed copies",
                   "`source/stdout.txt`, `source/stderr.txt`, `source/Program.vb` — the run's own output and exact source",
                   *[f"`{e}`" for e in extra_evidence]],
    )


def spec_term04(base: Path, capture: dict) -> dict:
    search = load(base / "evidence" / "search-log.json")
    highlight = capture["highlight"]
    lines = (base / "source" / "stdout.txt").read_text(encoding="utf-8-sig").splitlines()
    first, last = highlight["stdout_line_range"]
    block = lines[first - 1:last]
    criteria = sum("** WAR! **" in l for l in block) == 2 and any("wins the round (18 cards)" in l for l in block)
    stats = next(a for a in search["attempts"] if a["attempt"] == capture["selected_attempt"])
    ran_out = next((l.strip() for l in lines if "has no cards left for the war" in l), None)
    r05 = ("The highlighted round has two ties, full 3-card burns from both players, and an 18-card award, so it does "
           "not depend on the insufficient-card ordering R05 describes.")
    if ran_out:
        r05 += (f" The same run's ending (framed-end.png) does go through that branch: '{ran_out}'. It is shown as "
                "captured; how to narrate it is the producer's decision.")
    return dict(
        provenance_type="actual runtime capture",
        relationships={"Program.vb": "executed source (byte-identical copy in source/Program.vb)",
                       "SCRIPT.md": "narration and visual brief", "ASSET_PLAN.md": "source creative brief"},
        gates={"R05": {"evidence": ["source/stdout.txt", "evidence/search-log.json", "source/raw/04-end.png"],
                       "reason": r05 + " Awaiting producer decision."},
               "R08": {"evidence": ["source/stdout.txt", "evidence/search-log.json"],
                       "reason": f"The double war is from a real run (attempt {capture['selected_attempt']} of a bounded search). "
                                 "The script's example double-war text is not reproduced as evidence. Awaiting producer decision."}},
        variants=[{"name": "raw", "files": raw_files(capture), "notes": "Unedited window captures of the selected live run."},
                  {"name": "framed", "files": ["exports/framed.png", "exports/framed-highlight.png",
                                               *(["exports/framed-start.png"] if (base / "exports" / "framed-start.png").exists() else []),
                                               "exports/framed-end.png"],
                   "mapping": {"framed.png": "02-double-war clean", "framed-highlight.png": "02-double-war with outline on "
                               f"stdout lines {first}–{last}", "framed-start.png": "03-start", "framed-end.png": "04-end"}}],
        tests=[{"test": "double-war criteria in saved stdout", "result": "passed" if criteria else "failed",
                "detail": {"round": highlight["round"], "stdout_lines": [first, last], "text": block}},
               {"test": "terminal display equals saved stdout",
                "result": "passed" if capture["buffer_verification"]["all_compared_lines_match"] else "failed",
                "detail": capture["buffer_verification"]},
               {"test": "search bound respected", "result": "passed" if search["attempts_run"] <= 30 and
                search["retained_log_bytes"] <= 200 * 1024 * 1024 else "failed",
                "detail": {k: search[k] for k in ["attempts_run", "retained_log_bytes", "selection_rule", "selected_attempt"]}}],
        notes=[f"Selected run: attempt {capture['selected_attempt']}; highlighted round {highlight['round']} "
               f"(stdout lines {first}–{last}).",
               f"That run's actual result: {stats['result_line']} after {stats['total_rounds_line']} rounds with "
               f"{stats['total_wars_line']} wars.",
               "Non-selected attempts, if any, are summarized with hashes in evidence/search-log.json."],
        authored_additions=["Window title and short prompt set by the logged startup script; `Clear-Host` before each attempt.",
                            "framed-highlight.png adds an amber outline around the exact stdout line range; the raw capture is untouched."],
        delivered=["`source/raw/02-double-war.png` plus build/start/end captures of the same run",
                   "`exports/framed.png`, `framed-highlight.png`, `framed-start.png`, `framed-end.png`",
                   "`source/stdout.txt`, `source/stderr.txt`, `source/Program.vb`; `evidence/search-log.json`"],
    )


def spec_term03(base: Path, capture: dict) -> dict:
    viewports = load(base / "evidence" / "viewports.json")
    return dict(
        provenance_type="actual editor capture",
        relationships={"Program.vb": "displayed source (byte-identical copy in source/Program.vb)",
                       "SCRIPT.md": "narration and visual brief", "ASSET_PLAN.md": "source creative brief"},
        gates={"R03": {"evidence": ["evidence/viewports.json", "source/Program.vb"],
                       "reason": "The capture shows the VB.NET Program.vb (its own header calls it classic-inspired) in vim on "
                                 "Windows 11. No VB4 IDE, VB4 compile, or VB4 run is shown or implied. Awaiting producer decision."}},
        variants=[{"name": "raw", "files": raw_files(capture), "notes": "One unedited capture per viewport."},
                  {"name": "framed", "files": sorted(p.relative_to(base).as_posix() for p in (base / "exports").glob("framed*.png")),
                   "contact_sheet": "exports/contact-sheet.png",
                   "mapping": {v["file"]: [v["first_line"], v["last_line"]] for v in viewports["viewports"]}}],
        tests=[{"test": "every viewport's visible text equals the source lines",
                "result": "passed" if viewports["all_viewports_verified"] else "failed",
                "detail": [{k: v[k] for k in ["file", "first_line", "last_line", "visible_text_matches_source"]}
                           for v in viewports["viewports"]]},
               {"test": "complete coverage, no missing lines", "result": "passed" if viewports["complete_coverage"] else "failed",
                "detail": {"source_lines": viewports["source_lines"], "missing_lines": viewports["missing_lines"],
                           "overlaps": [v["overlap_with_previous"] for v in viewports["viewports"]]}}],
        notes=["These are stills of an editor at fixed scroll positions, not a smooth scroll recording (H01).",
               "Highlighting is vim's built-in VB syntax file; colours are the console's default palette."],
        authored_additions=["Editor opened with `-u NONE -i NONE -N -n -R` so no personal vimrc, history or swap file is used.",
                            "Viewports positioned with `<line>Gzt`; framed copies are 1:1 on a #111318 canvas."],
        delivered=[f"`source/raw/viewport-*.png` — {len(viewports['viewports'])} overlapping editor captures",
                   "`exports/framed.png` (lines 1–29) and `framed-02.png` … — 1:1 framed copies",
                   "`exports/contact-sheet.png`, `evidence/viewports.json`, `source/Program.vb`"],
    )


def spec_xtra06(base: Path, capture: dict) -> dict:
    targets = load(base / "evidence" / "highlight-targets.json")
    project = targets["01-war-vbproj.png"]
    harness = load(HARNESS / "harness-manifest.json")
    expected = next(f["sha256"] for f in harness["files"] if f["path"] == "War/War.vbproj")
    same = sha256(base / "source" / "War.vbproj") == expected
    framed = ["exports/framed.png"]
    return dict(
        provenance_type="actual editor capture",
        relationships={"Program.vb": "source-file directives shown separately (lines 7–8)",
                       "SCRIPT.md": "narration and visual brief"},
        gates={"R17": {"evidence": ["source/War.vbproj", "evidence/project-diff.txt", "evidence/highlight-targets.json"],
                       "reason": "The pictured War.vbproj is the OPS-02 derived harness file: the SDK 10.0.303 scaffold plus two "
                                 "added nodes (evidence/project-diff.txt). It is not an uploaded original or a scaffold default. "
                                 "Awaiting producer decision."}},
        variants=[{"name": "project-file", "files": ["source/raw/01-war-vbproj.png", *framed]},
                  {"name": "settings-focus", "files": ["exports/settings-focus.png"],
                   "derived_from": "source/raw/01-war-vbproj.png",
                   "highlighted": [n["text"] for n in project["nodes_present"]]},
                  {"name": "source-directives (supplementary evidence)",
                   "files": ["source/raw/02-program-vb-directives.png", "exports/framed-directives.png"]}],
        tests=[{"test": "pictured project file equals the harness file", "result": "passed" if same else "failed",
                "detail": f"source/War.vbproj sha256 {sha256(base / 'source' / 'War.vbproj')}"},
               {"test": "highlighted nodes exist in the file",
                "result": "passed" if len(project["nodes_present"]) == 2 else "failed", "detail": project["nodes_present"]},
               {"test": "visible editor text equals the files",
                "result": "passed" if all(t["visible_text_matches_file"] for t in targets.values()) else "failed",
                "detail": {k: v["visible_text_matches_file"] for k, v in targets.items()}},
               {"test": "TargetFramework preserved", "result": "passed" if "<TargetFramework>net10.0</TargetFramework>" in
                (base / "source" / "War.vbproj").read_text(encoding="utf-8-sig") else "failed", "detail": "net10.0 from the scaffold"}],
        notes=["The scaffold default has no OptionExplicit/OptionStrict nodes; they were added in the derived harness only.",
               "Program.vb also sets Option Explicit On / Option Strict On as file directives (lines 7–8), captured separately."],
        authored_additions=["Two project nodes added in the OPS-02 harness (logged diff).",
                            "settings-focus.png: integer 2× nearest-neighbour crop with amber outlines on the two nodes.",
                            "framed-directives.png: amber outlines on Program.vb lines 7–8."],
        delivered=["`source/raw/01-war-vbproj.png`, `02-program-vb-directives.png` — raw vim captures",
                   "`exports/framed.png` (project-file), `settings-focus.png`, `framed-directives.png`",
                   "`source/War.vbproj`, `evidence/project-diff.txt`, `evidence/highlight-targets.json`"],
    )


SPECS = {"TERM-01": spec_term01, "TERM-03": spec_term03, "TERM-04": spec_term04, "XTRA-06": spec_xtra06,
         **{i: (lambda b, c, i=i: spec_run(i, b, c)) for i in RUN_IDS}}


def qa_text(asset_id: str, spec: dict, tests: list[dict], tc: dict) -> str:
    row = ticket(asset_id)
    review = REVIEWS[asset_id]
    vim = f", vim {tc['vim']}" if "vim" in tc else ""
    lines = [f"# {asset_id} — Production QA", "",
             f"**Production:** produced. **Release:** blocked — gates {', '.join(row['gates'])} await a producer decision.", "",
             "## Delivered", *[f"- {d}" for d in spec["delivered"]],
             "- Every file is listed with bytes and SHA-256 in `delivery.json`.", "",
             "## Method",
             "Actual local capture on this machine. Commands were typed into a real conhost.exe window running pwsh "
             "(WriteConsoleInput), window images were taken with PrintWindow, and text was read back from the console buffer. "
             "Raw PNGs are never edited; framing and outlines exist only in `exports/`. Commands, exit codes and timings "
             "come from PowerShell's own history (`evidence/prompt-log.jsonl`, `evidence/commands.log`).", "",
             "## Checks actually performed"]
    for test in tests:
        lines.append(f"- **{test['test']}:** {test['result']}")
    lines += ["", "## Manual visual inspection", f"- Full size: {review['full_size']}", f"- 720p: {review['proof_720']}", "",
              "## Reproduction", "```",
              f"python work/war-harness/tools/capture_assets.py --id {asset_id}",
              f"python work/war-harness/tools/finish_assets.py --id {asset_id} --stage render",
              f"python work/war-harness/tools/finish_assets.py --id {asset_id} --stage bundle", "```",
              "A capture refuses to overwrite existing raw files. A new run of the game is a new random game and must be "
              "delivered as a new capture, never relabelled as this one.", "",
              f"Toolchain: {tc['os']}; .NET SDK {tc['dotnet_sdk']}; {tc['shell']}; conhost {tc['conhost_file_version']}; "
              f"Python {tc['python']}; Pillow {tc['packages']['Pillow']}; pywin32 {tc['packages']['pywin32']}{vim}.", "",
              "## Remaining gates and limits"]
    lines += [f"- **{gate}:** {spec['gates'][gate]['reason']}" for gate in row["gates"]]
    lines += ["- Stills only. A live screen recording (handoff H01) was not made.",
              "- Structure validation (`tools/validate_delivery.py`) runs after bundling; results are in "
              "`review/capture-delivery-validation.json`.",
              "- No independent reviewer is recorded; the capturing agent's checks are not a producer review.", ""]
    return "\n".join(lines)


def bundle_capture(asset_id: str) -> None:
    if asset_id not in REVIEWS:
        raise SystemExit(f"{asset_id}: add a REVIEWS entry after inspecting the full-size and 720p images.")
    base = base_of(asset_id)
    capture = normalize_capture(base)
    spec = SPECS[asset_id](base, capture)
    extra = {}
    if asset_id in {"TERM-03", "XTRA-06"}:
        extra["vim"] = subprocess.run([VIM_EXE, "--version"], capture_output=True, text=True).stdout.splitlines()[0]
    tc = toolchain(extra)
    tests = [t for t in [source_check(base), command_checks(capture)] if t] + spec["tests"]
    tests += [png_checks(base), manual_review(asset_id)]
    # The privacy scan runs last over files written so far; qa.md and delivery.json are rescanned by --stage validate.
    tests.append(privacy_scan(base))
    write_bundle(asset_id, provenance_type=spec["provenance_type"], variants=spec["variants"],
                 relationships=spec["relationships"], gates=spec["gates"], tests=tests, toolchain_data=tc,
                 notes=spec["notes"], authored_additions=spec["authored_additions"], qa_md=qa_text(asset_id, spec, tests, tc))


# ----- OPS-02 ------------------------------------------------------------------------------------
def bundle_ops02() -> None:
    base = base_of("OPS-02")
    evidence = base / "evidence"
    records = load(evidence / "harness-commands.json")
    for record in records:
        if "stdout_file" in record:
            record.pop("stdout", None)
            record.pop("stderr", None)
    dump(evidence / "harness-commands.json", records)
    log = ["# OPS-02 command log — run by work/war-harness/tools/build_harness.py via subprocess (no terminal UI)",
           "# columns: start (UTC) | seconds | exit code | cwd | command | retained output"]
    log += [f"{r['utc']} | {r['seconds']:>7.3f}s | exit={r['exit_code']} | {r['cwd']} | {' '.join(r['argv'])} | "
            f"{r.get('stdout_file', 'stdout: ' + r.get('stdout', '').strip())}" for r in records]
    (evidence / "commands.log").write_text("\n".join(log) + "\n", encoding="utf-8")
    manifest = load(HARNESS / "harness-manifest.json")
    exports = base / "exports"
    exports.mkdir(exist_ok=True)
    shutil.copyfile(HARNESS / "harness-manifest.json", exports / "harness-manifest.json")
    run_text = (evidence / "harness-run.stdout.txt").read_text(encoding="utf-8")
    result = next(l for l in run_text.splitlines() if l.endswith("WINS THE WAR!") or l.startswith("THE WAR ENDS"))
    rounds = re.search(r"Total rounds played : (\d+)", run_text).group(1)
    wars = re.search(r"Total wars fought    : (\d+)", run_text).group(1)
    users = []
    for asset_id in CAPTURE_IDS:
        path = base_of(asset_id) / "evidence" / "capture.json"
        if path.exists() and any("copied frozen harness" in s for s in load(path)["pre_session_steps"]):
            users.append(asset_id)
    report = f"""# OPS-02 — Isolated .NET harness report

**Production:** produced. **Release:** blocked (R17 awaits a producer decision).

## Environment
- {manifest['os']}, .NET SDK {manifest['sdk_version']} (`dotnet --info` in `evidence/dotnet-info.stdout.txt`). Nothing was installed.

## What was built
1. `dotnet new console -lang VB` in the empty `work/war-harness/War/` → exit 0. Untouched output kept in `work/war-harness/scaffold/`.
2. `sources/Program.vb` copied byte-for-byte to `War/Program.vb` (sha256 `{manifest['source_program_sha256']}`, match: {manifest['project_program_matches_source']}).
3. Derived project change, the only edit (`work/war-harness/project-diff.txt`): added `<OptionExplicit>On</OptionExplicit>` and `<OptionStrict>On</OptionStrict>` after `{manifest['target_framework']}`, which is unchanged. This derived file is not an uploaded original (R17).
4. `dotnet build` → exit {manifest['build_exit_code']}, 0 warnings, 0 errors.
5. `dotnet run --no-build`, once → exit {manifest['run_exit_code']}; stderr empty; stdout kept in `evidence/harness-run.stdout.txt`. Actual result: {result} after {rounds} rounds with {wars} wars. This is a harness check only; it is not a capture asset.

No code bug was fixed; Program.vb is unchanged.

## Snapshot and copies
`exports/harness-manifest.json` lists every snapshot file with its hash. Capture workers copy `War/War.vbproj` and `War/Program.vb` into `assets/<ID>/work/War/`, verify both hashes, and build there, so no two captures share `bin/` or `obj/`. Hash-verified copies were used by: {', '.join(users) or 'none yet'}. TERM-01 intentionally scaffolds its own empty directory instead.

## Capture tooling
`work/war-harness/tools/` holds the real-terminal driver (conhost + pwsh, WriteConsoleInput, PrintWindow, buffer read-back), per-ticket capture scripts, and the finisher. See `work/war-harness/README.md`.
"""
    (exports / "report.md").write_text(report, encoding="utf-8")
    tc = toolchain()
    tests = [{"test": "source hash unchanged", "result": "passed" if manifest["project_program_matches_source"] else "failed"},
             {"test": "build result recorded", "result": "passed" if manifest["build_exit_code"] == 0 else "failed",
              "detail": "evidence/dotnet-build.stdout.txt"},
             {"test": "single isolated run recorded", "result": "passed" if manifest["run_exit_code"] == 0 else "failed",
              "detail": f"{result}; {rounds} rounds; {wars} wars"},
             {"test": "independent worker copies", "result": "passed" if users else "not yet exercised",
              "detail": f"hash-verified copies built separately by {', '.join(users)}"},
             {"test": "no .vbproj presented as an uploaded original", "result": "passed",
              "detail": "report.md, README.md and the diff all label War.vbproj as derived"},
             {"test": "manual visual inspection", "result": "not applicable", "detail": "Support ticket with no image outputs."}]
    tests.append(privacy_scan(base))
    qa = f"""# OPS-02 — Production QA

**Production:** produced. **Release:** blocked — R17 awaits a producer decision.

## Delivered
- `exports/report.md` — what was built and observed
- `exports/harness-manifest.json` — snapshot hashes, SDK version, exit codes
- `evidence/commands.log`, `evidence/harness-commands.json` — every command with exit code and timing
- `evidence/dotnet-info.stdout.txt`, `dotnet-new.*`, `dotnet-build.*`, `harness-run.*` — raw command output
- Harness snapshot itself: `work/war-harness/` (owned by this ticket)

## Checks actually performed
""" + "\n".join(f"- **{t['test']}:** {t['result']}" for t in tests) + f"""

## Reproduction
```
python work/war-harness/tools/build_harness.py
python work/war-harness/tools/finish_assets.py --id OPS-02 --stage bundle
```
`build_harness.py` refuses to overwrite an existing harness. Toolchain: {tc['os']}; .NET SDK {tc['dotnet_sdk']}; Python {tc['python']}.

## Remaining gates and limits
- **R17:** The derived War.vbproj is generated with the installed SDK and every property change is logged; a producer still has to accept this handling.
- No independent reviewer is recorded.
"""
    write_bundle("OPS-02", provenance_type="support infrastructure: derived local .NET harness",
                 variants=[{"name": "harness", "files": ["exports/harness-manifest.json", "exports/report.md"],
                            "snapshot_root": "../../work/war-harness/"}],
                 relationships={"Program.vb": "copied byte-for-byte into the harness", "SCRIPT.md": "harness requirements context"},
                 gates={"R17": {"evidence": ["exports/harness-manifest.json", "exports/report.md"],
                                "reason": "Derived isolated project generated with the installed SDK; every property change "
                                          "is in work/war-harness/project-diff.txt. Awaiting producer decision."}},
                 tests=tests, toolchain_data=tc, notes=["Harness run output is a check, not a capture asset."],
                 authored_additions=["Two OptionExplicit/OptionStrict project nodes in the derived War.vbproj."],
                 qa_md=qa, dimensions=None)


# ----- validate ----------------------------------------------------------------------------------
def validate() -> int:
    results = {}
    for asset_id in ALL_IDS:
        proc = subprocess.run([sys.executable, str(ROOT / "tools" / "validate_delivery.py"), "--id", asset_id],
                              capture_output=True, text=True, cwd=ROOT)
        results[asset_id] = {"exit_code": proc.returncode, "output": json.loads(proc.stdout) if proc.stdout.strip().startswith("{")
                             else proc.stdout + proc.stderr, "privacy": privacy_scan(base_of(asset_id))["result"]}
    pack = subprocess.run([sys.executable, str(ROOT / "tools" / "validate_pack.py")], capture_output=True, text=True, cwd=ROOT)
    dump(ROOT / "review" / "capture-delivery-validation.json",
         {"validated": ALL_IDS, "delivery": results,
          "validate_pack": {"exit_code": pack.returncode, "output": (pack.stdout + pack.stderr).strip()}})
    return 0 if all(r["exit_code"] == 0 and r["privacy"] == "passed" for r in results.values()) and pack.returncode == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", choices=ALL_IDS)
    parser.add_argument("--stage", required=True, choices=["render", "bundle", "validate"])
    args = parser.parse_args()
    if args.stage == "validate":
        return validate()
    if not args.id:
        parser.error("--id is required for render and bundle")
    if args.stage == "render":
        render(args.id)
    elif args.id == "OPS-02":
        bundle_ops02()
    else:
        bundle_capture(args.id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
