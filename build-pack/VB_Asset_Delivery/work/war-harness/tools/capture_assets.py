#!/usr/bin/env python3
"""Real terminal/editor captures for TERM-01..06 and XTRA-06. Run one --id at a time.

Each capture types into an actual conhost/pwsh window (see console_capture.py), keeps the raw
window PNGs unedited, and records commands, exit codes, buffer text, and hashes. Framing, proofs,
and delivery metadata are produced afterwards by finish_assets.py once the raw shots are reviewed.
"""
from __future__ import annotations

import argparse
import json
import platform
import re
import shutil
import subprocess
import time
import traceback
from pathlib import Path

import win32con

from capture_common import HARNESS, ROOT, dump, now_utc, prepare_workdir, sha256
from console_capture import ConsoleSession

GIT_USR_BIN = r"C:\Program Files\Git\usr\bin"
VIM = 'vim -u NONE -i NONE -N -n -R -c "syntax on" -c "set number" {name}'
RUN = "dotnet run --no-build 2> {err} | Tee-Object -FilePath {out}"
SOURCE_SHA = sha256(ROOT / "sources" / "Program.vb")
MAX_ATTEMPTS = 30
MAX_RETAINED_BYTES = 200 * 1024 * 1024


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.parents[1]).as_posix()


def typed_commands(prompt_log: Path) -> list[dict]:
    """History entries for typed commands. The first entry is pwsh's non-interactive -EncodedCommand
    startup script (recorded separately as terminal.startup_script), so it is excluded here."""
    entries = [json.loads(line) for line in prompt_log.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    return [e for e in entries if not e["command"].startswith("[IO.File]::WriteAllText(")]


class Capture:
    def __init__(self, asset_id: str, workdir: Path, **session_kw):
        self.id = asset_id
        self.base = ROOT / "assets" / asset_id
        self.work = workdir
        self.raw = self.base / "source" / "raw"
        if self.raw.exists():
            raise SystemExit(f"{self.raw} already exists; raw captures are never overwritten.")
        self.raw.mkdir(parents=True)
        self.sdk_version = subprocess.run(["dotnet", "--version"], capture_output=True, text=True).stdout.strip()
        self.captured_utc = now_utc()
        self.session = ConsoleSession(workdir, **session_kw)
        self.shots: list[dict] = []
        self.viewport_text: dict[str, list[str]] = {}
        self.pre_session: list[str] = []

    def shot(self, name: str, label: str) -> dict:
        record = self.session.screenshot(self.raw / f"{name}.png")
        record["label"] = label
        top, bottom = record["visible_buffer_rows"]
        self.viewport_text[record["file"]] = self.session.read_rows(top, bottom - top + 1)
        self.shots.append(record)
        return record

    def finish(self, extra: dict) -> None:
        s = self.session
        commands = typed_commands(s.prompt_log)
        evidence = self.base / "evidence"
        evidence.mkdir(exist_ok=True)
        program = self.work / "Program.vb"
        dump(evidence / "capture.json", {
            "id": self.id,
            "captured_utc": self.captured_utc,
            "capture_method": "Actual local terminal session. Commands were typed into a real conhost.exe window "
                              "running pwsh via WriteConsoleInput; raw PNGs are unedited PrintWindow images of that "
                              "window; buffer text was read back with ReadConsoleOutputCharacter.",
            "os": platform.platform(),
            "terminal": {
                "host": "conhost.exe (launched directly)", "window_class": s.window_class, "shell": "pwsh",
                "cols": s.cols, "rows": s.rows, "buffer_rows": s.buffer_rows, "font": s.font, "font_px": s.font_px,
                "window_title_set_to": s.title,
                "psreadline": "PredictionSource None (no history suggestions on screen); HistorySaveStyle SaveNothing",
                "prompt": "PS <folder>> — a custom prompt that hides the long absolute path and logs each history "
                          "entry to prompt-log.jsonl; it prints nothing else",
                "extra_path": list(s.extra_path),
                "startup_script": s.setup_script.replace(str(ROOT.parents[1]) + "\\", ""),
            },
            "dotnet_sdk_version": self.sdk_version,
            "working_directory": rel(self.work),
            "pre_session_steps": self.pre_session,
            "source_sha256": sha256(program) if program.exists() else None,
            "source_matches_original": (sha256(program) == SOURCE_SHA) if program.exists() else None,
            "commands": commands,
            "screenshots": self.shots,
            "driver_events": s.events,
            **extra,
        })
        dump(evidence / "viewport-text.json", self.viewport_text)
        shutil.copyfile(s.prompt_log, evidence / "prompt-log.jsonl")
        log = [f"# {self.id} command log — typed into a real conhost/pwsh window",
               f"# working directory: {rel(self.work)}",
               f"# dotnet SDK: {self.sdk_version}; OS: {platform.platform()}",
               "# columns: start (UTC, PowerShell history) | seconds | $? | $LASTEXITCODE at next prompt "
               "(only meaningful after a native command) | command"]
        log += [f"# pre-session: {step}" for step in self.pre_session]
        log += [f"{c['start_utc']} | {c['seconds']:>8.3f}s | ok={c['succeeded']} | exit={c['last_exit_code']} | {c['command']}"
                for c in commands]
        (evidence / "commands.log").write_text("\n".join(log) + "\n", encoding="utf-8")


# ----- War output analysis -----------------------------------------------------------------------
def run_stats(text: str) -> dict:
    lines = text.splitlines()
    result = next((l for l in lines if l.endswith("WINS THE WAR!") or l.startswith("THE WAR ENDS")), None)
    rounds = re.search(r"Total rounds played : (\d+)", text)
    wars = re.search(r"Total wars fought    : (\d+)", text)
    chains = [int(m.group(1)) for m in re.finditer(r"war number (\d+) this round", text)]
    return {"result_line": result, "total_rounds_line": int(rounds.group(1)) if rounds else None,
            "total_wars_line": int(wars.group(1)) if wars else None,
            "war_lines": sum("** WAR! **" in l for l in lines), "longest_chain_in_one_round": max(chains, default=0),
            "draw_message_present": "deck cycle detected" in text, "stdout_lines": len(lines)}


def round_blocks(lines: list[str]) -> list[dict]:
    blocks, current = [], None
    for index, line in enumerate(lines):
        match = re.match(r"Round (\d+): ", line)
        if match:
            current = {"round": int(match.group(1)), "start": index, "end": index}
            blocks.append(current)
        elif current and line.startswith("        "):
            current["end"] = index
        else:
            current = None
    return blocks


def verify_buffer(session: ConsoleSession, lines: list[str], offset: int) -> dict:
    first = max(0, -offset)
    rows = session.read_rows(offset + first, len(lines) - first)
    mismatches = [first + i for i, (row, line) in enumerate(zip(rows, lines[first:])) if row != line.rstrip()]
    return {"stdout_lines": len(lines), "first_buffer_row_of_stdout": offset,
            "lines_lost_to_scrollback_limit": first, "lines_compared": len(lines) - first,
            "mismatched_line_indexes": mismatches[:50], "all_compared_lines_match": not mismatches}


# ----- tickets -----------------------------------------------------------------------------------
def term01() -> None:
    work = ROOT / "assets" / "TERM-01" / "work" / "War"
    if work.exists():
        raise SystemExit(f"{work} exists; TERM-01 needs an empty directory.")
    work.mkdir(parents=True)
    cap = Capture("TERM-01", work, cols=100, rows=30, font_px=28)
    cap.pre_session.append(f"created empty directory {rel(work)}")
    s = cap.session
    s.start()
    s.run("dotnet --version")
    cap.shot("01-dotnet-version", "dotnet --version in the empty War directory")
    s.run("Get-ChildItem")
    s.run("dotnet new console -lang VB", timeout=300)
    cap.shot("02-dotnet-new", "dotnet new console -lang VB succeeds in the same window")
    s.run("Get-ChildItem")
    cap.shot("03-scaffold-files", "Directory listing after scaffolding: War.vbproj and Program.vb")
    transcript = s.transcript()
    s.close()
    (cap.base / "source").mkdir(exist_ok=True)
    (cap.base / "source" / "scaffold-transcript.txt").write_text(transcript, encoding="utf-8")
    scaffold = cap.base / "evidence" / "scaffold"
    scaffold.mkdir(parents=True, exist_ok=True)
    files = {}
    for name in ["War.vbproj", "Program.vb"]:
        shutil.copyfile(work / name, scaffold / name)
        files[name] = sha256(work / name)
    harness = json.loads((HARNESS / "harness-manifest.json").read_text(encoding="utf-8"))
    harness_scaffold = {f["path"].split("/")[-1]: f["sha256"] for f in harness["files"] if f["path"].startswith("scaffold/")}
    cap.finish({"scaffold_files_sha256": files,
                "matches_ops02_scaffold": {k: v == harness_scaffold.get(k) for k, v in files.items()},
                "note": "This is the default template output. It does not contain the War game."})


def run_capture(asset_id: str) -> None:
    work = prepare_workdir(asset_id)
    cap = Capture(asset_id, work, cols=100, rows=30, font_px=28)
    cap.pre_session.append(f"copied frozen harness War.vbproj and Program.vb into {rel(work)}; hashes verified")
    s = cap.session
    s.start()
    s.run("dotnet build", timeout=600)
    cap.shot("01-build", "dotnet build in this asset's private harness copy")
    s.run("Clear-Host")
    command = RUN.format(err="stderr.txt", out="stdout.txt")
    s.run(command, timeout=3600)
    lines = (work / "stdout.txt").read_text(encoding="utf-8-sig").splitlines()
    prompt_row = s.cursor()[1]
    offset = prompt_row - len(lines)
    verification = verify_buffer(s, lines, offset)
    if offset >= 1:
        s.scroll_to(0)
        cap.shot("02-start", "Top of the live run: typed command, banner, 26/26 deal, first rounds")
    first_war = next((i for i, l in enumerate(lines) if "** WAR! **" in l), None)
    if first_war is not None and offset + first_war - 6 >= 0:
        s.scroll_to(offset + first_war - 6)
        cap.shot("03-first-war", f"First ** WAR! ** of the run (stdout line {first_war + 1})")
    s.scroll_to(prompt_row - s.rows + 1)
    cap.shot("04-end", "Bottom of the live run: final result, totals, returned prompt")
    if offset < 1:
        s.run("Get-Content stdout.txt -TotalCount 26")
        cap.shot("05-log-head", "LOG VIEW of this same run's saved stdout; the live top scrolled out of the console buffer")
    s.close()
    source = cap.base / "source"
    for name in ["stdout.txt", "stderr.txt", "Program.vb"]:
        shutil.copyfile(work / name, source / name)
    stats = run_stats((work / "stdout.txt").read_text(encoding="utf-8-sig"))
    dump(cap.base / "evidence" / "run-stats.json", {"id": asset_id, "command": command, **stats,
                                                    "stdout_sha256": sha256(source / "stdout.txt"),
                                                    "first_war_stdout_line": None if first_war is None else first_war + 1})
    cap.finish({"run_command": command, "buffer_verification": verification, "run_stats": stats})


def term04() -> None:
    work = prepare_workdir("TERM-04")
    cap = Capture("TERM-04", work, cols=100, rows=30, font_px=28)
    cap.pre_session.append(f"copied frozen harness War.vbproj and Program.vb into {rel(work)}; hashes verified")
    s = cap.session
    s.start()
    s.run("dotnet build", timeout=600)
    cap.shot("01-build", "dotnet build in this asset's private harness copy")
    attempts, retained, selected = [], 0, None
    for n in range(1, MAX_ATTEMPTS + 1):
        s.run("Clear-Host")
        out, err = f"stdout-{n:02d}.txt", f"stderr-{n:02d}.txt"
        command = RUN.format(err=err, out=out)
        s.run(command, timeout=3600)
        text = (work / out).read_text(encoding="utf-8-sig")
        lines = text.splitlines()
        retained += (work / out).stat().st_size + (work / err).stat().st_size
        prompt_row = s.cursor()[1]
        offset = prompt_row - len(lines)
        blocks = round_blocks(lines)
        doubles = [b for b in blocks
                   if sum("** WAR! **" in l for l in lines[b["start"]:b["end"] + 1]) == 2
                   and any("wins the round (18 cards)" in l for l in lines[b["start"]:b["end"] + 1])]
        capturable = [b for b in doubles if offset + b["start"] >= 0]
        attempts.append({"attempt": n, "command": command, "stdout_sha256": sha256(work / out),
                         "stdout_bytes": (work / out).stat().st_size, "stderr_bytes": (work / err).stat().st_size,
                         **run_stats(text), "double_war_18_card_rounds": [b["round"] for b in doubles],
                         "longer_chain_rounds": [b["round"] for b in blocks
                                                 if sum("** WAR! **" in l for l in lines[b["start"]:b["end"] + 1]) > 2],
                         "capturable_in_console_buffer": [b["round"] for b in capturable]})
        if capturable:
            selected = {"attempt": n, "block": capturable[0], "lines": lines, "offset": offset,
                        "prompt_row": prompt_row, "out": out, "err": err, "command": command,
                        "verification": verify_buffer(s, lines, offset)}
            break
        if retained >= MAX_RETAINED_BYTES:
            break
    extra = {"search_bound": {"max_runs": MAX_ATTEMPTS, "max_retained_bytes": MAX_RETAINED_BYTES},
             "attempts_run": len(attempts), "retained_log_bytes": retained,
             "selection_rule": "First run containing a round with exactly two ** WAR! ** lines and an "
                               "'(18 cards)' award; within it, the first such round."}
    if selected:
        block, offset = selected["block"], selected["offset"]
        size = block["end"] - block["start"] + 1
        top = offset + block["start"] - (s.rows - size) // 2
        s.scroll_to(top)
        shot = cap.shot("02-double-war", f"Round {block['round']}: two ** WAR! ** lines and the 18-card award")
        window_top = shot["visible_buffer_rows"][0]
        widths = [len(l) for l in selected["lines"][block["start"]:block["end"] + 1]]
        extra["highlight"] = {"round": block["round"], "stdout_line_range": [block["start"] + 1, block["end"] + 1],
                              "window_rows": [offset + block["start"] - window_top, offset + block["end"] - window_top],
                              "max_line_chars": max(widths), "screenshot": shot["file"]}
        if offset >= 1:
            s.scroll_to(0)
            cap.shot("03-start", "Top of the same live run: typed command, banner, deal")
        s.scroll_to(selected["prompt_row"] - s.rows + 1)
        cap.shot("04-end", "Bottom of the same live run: final result and totals")
        extra.update(selected_attempt=selected["attempt"], run_command=selected["command"],
                     buffer_verification=selected["verification"])
    s.close()
    dump(cap.base / "evidence" / "search-log.json", {"id": "TERM-04", **{k: v for k, v in extra.items()
                                                                          if k != "buffer_verification"},
                                                     "attempts": attempts})
    if selected:
        source = cap.base / "source"
        shutil.copyfile(work / selected["out"], source / "stdout.txt")
        shutil.copyfile(work / selected["err"], source / "stderr.txt")
        shutil.copyfile(work / "Program.vb", source / "Program.vb")
    cap.finish(extra)


def vim_rows_expected(lines: list[str], top: int, count: int) -> list[str]:
    return [f"{n:>3} {lines[n - 1]}".rstrip() for n in range(top, min(top + count, len(lines) + 1))]


def open_vim(s: ConsoleSession, name: str, needle: str) -> None:
    s.type_line(VIM.format(name=name))
    s.wait_for_text(needle, 30)


def quit_vim(s: ConsoleSession) -> None:
    s.type_text(":q")
    s.press("\r", win32con.VK_RETURN)
    s.wait_prompt(15)


def term03() -> None:
    work = prepare_workdir("TERM-03")
    cap = Capture("TERM-03", work, cols=108, rows=30, font_px=28, extra_path=(GIT_USR_BIN,))
    cap.pre_session.append(f"copied frozen harness War.vbproj and Program.vb into {rel(work)}; hashes verified")
    s = cap.session
    source_lines = (work / "Program.vb").read_text(encoding="utf-8").splitlines()
    s.start()
    open_vim(s, "Program.vb", "Module Program")
    text_rows = s.rows - 1
    last_top = len(source_lines) - text_rows + 1
    tops = list(range(1, last_top, text_rows - 4)) + [last_top]
    viewports = []
    for index, top in enumerate(tops, 1):
        s.type_text(f"{top}Gzt")
        expected = vim_rows_expected(source_lines, top, text_rows)
        for _ in range(20):
            time.sleep(0.25)
            window_top, _ = s.window_rect()
            rows = s.read_rows(window_top, len(expected))
            if rows == expected:
                break
        last = top + len(expected) - 1
        shot = cap.shot(f"viewport-{index:02d}-lines-{top:03d}-{last:03d}", f"Program.vb lines {top}–{last} in vim")
        viewports.append({"index": index, "file": f"source/raw/{shot['file']}", "first_line": top, "last_line": last,
                          "overlap_with_previous": 0 if index == 1 else viewports[-1]["last_line"] - top + 1,
                          "visible_text_matches_source": rows == expected,
                          "mismatched_rows": [i for i, (a, b) in enumerate(zip(rows, expected)) if a != b]})
    quit_vim(s)
    s.close()
    covered = set()
    for v in viewports:
        covered.update(range(v["first_line"], v["last_line"] + 1))
    missing = sorted(set(range(1, len(source_lines) + 1)) - covered)
    shutil.copyfile(work / "Program.vb", cap.base / "source" / "Program.vb")
    dump(cap.base / "evidence" / "viewports.json", {
        "id": "TERM-03", "source": "source/Program.vb", "source_sha256": sha256(work / "Program.vb"),
        "source_lines": len(source_lines), "editor_command": VIM.format(name="Program.vb"),
        "text_rows_per_viewport": text_rows, "viewports": viewports, "missing_lines": missing,
        "complete_coverage": not missing, "all_viewports_verified": all(v["visible_text_matches_source"] for v in viewports)})
    cap.finish({"editor": "vim (Git for Windows usr/bin) in the same conhost window", "viewport_count": len(viewports),
                "complete_coverage": not missing})


def xtra06() -> None:
    work = prepare_workdir("XTRA-06")
    cap = Capture("XTRA-06", work, cols=100, rows=20, font_px=28, extra_path=(GIT_USR_BIN,))
    cap.pre_session.append(f"copied frozen harness War.vbproj and Program.vb into {rel(work)}; hashes verified")
    cap.pre_session.append("re-run: the first attempt of this capture typed the same commands but crashed after the "
                           "window closed (evidence/ folder missing when copying project-diff.txt); its raw PNGs and "
                           "logs were set aside undelivered and this capture started from a fresh harness copy")
    s = cap.session
    project_lines = (work / "War.vbproj").read_text(encoding="utf-8-sig").splitlines()
    program_lines = (work / "Program.vb").read_text(encoding="utf-8").splitlines()
    s.start()
    checks = {}
    for name, lines, needle, shot_name, label, targets in [
        ("War.vbproj", project_lines, "OptionStrict", "01-war-vbproj", "Derived harness War.vbproj open in vim",
         ["<OptionExplicit>On</OptionExplicit>", "<OptionStrict>On</OptionStrict>"]),
        ("Program.vb", program_lines, "Option Strict On", "02-program-vb-directives",
         "Program.vb source-file directives (lines 7–8) open in vim", ["Option Explicit On", "Option Strict On"]),
    ]:
        open_vim(s, name, needle)
        expected = vim_rows_expected(lines, 1, s.rows - 1)
        for _ in range(20):
            time.sleep(0.25)
            window_top, _ = s.window_rect()
            rows = s.read_rows(window_top, len(expected))
            if rows == expected:
                break
        shot = cap.shot(shot_name, label)
        found = []
        for target in targets:
            line_no = next((i + 1 for i, l in enumerate(lines) if l.strip() == target), None)
            if line_no:
                line = lines[line_no - 1]
                indent = len(line) - len(line.lstrip())
                found.append({"text": target, "line": line_no, "window_row": line_no - 1,
                              "first_col": 4 + indent, "last_col": 4 + len(line) - 1})
        checks[shot["file"]] = {"file": name, "visible_text_matches_file": rows == expected,
                                "nodes_present": found, "geometry": {k: shot[k] for k in
                                                                     ["cell_px", "client_origin_in_png", "size"]}}
        quit_vim(s)
    s.close()
    (cap.base / "evidence").mkdir(exist_ok=True)
    shutil.copyfile(work / "War.vbproj", cap.base / "source" / "War.vbproj")
    shutil.copyfile(HARNESS / "project-diff.txt", cap.base / "evidence" / "project-diff.txt")
    dump(cap.base / "evidence" / "highlight-targets.json", checks)
    cap.finish({"editor": "vim (Git for Windows usr/bin) in the same conhost window", "file_checks": checks,
                "project_file_sha256": sha256(work / "War.vbproj")})


TICKETS = {"TERM-01": term01, "TERM-02": lambda: run_capture("TERM-02"), "TERM-03": term03, "TERM-04": term04,
           "TERM-05": lambda: run_capture("TERM-05"), "TERM-06": lambda: run_capture("TERM-06"), "XTRA-06": xtra06}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", required=True, choices=sorted(TICKETS))
    args = parser.parse_args()
    error_file = ROOT / "assets" / args.id / "work" / "capture-error.txt"
    try:
        TICKETS[args.id]()
    except BaseException:
        error_file.parent.mkdir(parents=True, exist_ok=True)
        error_file.write_text(traceback.format_exc(), encoding="utf-8")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
