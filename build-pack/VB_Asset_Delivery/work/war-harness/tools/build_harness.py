#!/usr/bin/env python3
"""OPS-02: scaffold, derive, build, and run the isolated War harness once, logging every command.

Run from anywhere: python work/war-harness/tools/build_harness.py
Writes work/war-harness/{War,scaffold,project-diff.txt,harness-manifest.json} and raw evidence under
assets/OPS-02/evidence/. Refuses to overwrite an existing harness.
"""
from __future__ import annotations

import datetime as dt
import difflib
import hashlib
import json
import platform
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HARNESS = ROOT / "work" / "war-harness"
PROJECT = HARNESS / "War"
SCAFFOLD = HARNESS / "scaffold"
EVIDENCE = ROOT / "assets" / "OPS-02" / "evidence"
SOURCE = ROOT / "sources" / "Program.vb"
OPTION_NODES = ["<OptionExplicit>On</OptionExplicit>", "<OptionStrict>On</OptionStrict>"]

records: list[dict] = []


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def run(argv: list[str], cwd: Path, keep: str | None = None) -> subprocess.CompletedProcess:
    started = dt.datetime.now(dt.timezone.utc)
    t0 = time.monotonic()
    proc = subprocess.run(argv, cwd=cwd, capture_output=True)
    record = {"utc": started.isoformat(timespec="seconds"), "cwd": rel(cwd), "argv": argv,
              "exit_code": proc.returncode, "seconds": round(time.monotonic() - t0, 3),
              "stdout_bytes": len(proc.stdout), "stderr_bytes": len(proc.stderr)}
    if keep:
        (EVIDENCE / f"{keep}.stdout.txt").write_bytes(proc.stdout)
        (EVIDENCE / f"{keep}.stderr.txt").write_bytes(proc.stderr)
        record["stdout_file"] = f"evidence/{keep}.stdout.txt"
        record["stderr_file"] = f"evidence/{keep}.stderr.txt"
    record["stdout"] = proc.stdout.decode("utf-8", "replace")
    record["stderr"] = proc.stderr.decode("utf-8", "replace")
    records.append(record)
    return proc


def main() -> int:
    if PROJECT.exists():
        raise SystemExit(f"{rel(PROJECT)} already exists; the harness snapshot is immutable.")
    EVIDENCE.mkdir(parents=True, exist_ok=True)

    run(["dotnet", "--info"], ROOT, keep="dotnet-info")
    version = run(["dotnet", "--version"], ROOT).stdout.decode().strip()

    PROJECT.mkdir(parents=True)
    scaffold = run(["dotnet", "new", "console", "-lang", "VB"], PROJECT, keep="dotnet-new")
    if scaffold.returncode:
        raise SystemExit("dotnet new failed; see evidence")

    SCAFFOLD.mkdir()
    for name in ["War.vbproj", "Program.vb"]:
        shutil.copyfile(PROJECT / name, SCAFFOLD / name)

    shutil.copyfile(SOURCE, PROJECT / "Program.vb")
    if sha256(PROJECT / "Program.vb") != sha256(SOURCE):
        raise SystemExit("Program.vb copy is not byte-identical")

    original = (SCAFFOLD / "War.vbproj").read_bytes().decode("utf-8")
    newline = "\r\n" if "\r\n" in original else "\n"
    lines = original.split(newline)
    target = next(i for i, line in enumerate(lines) if "<TargetFramework>" in line)
    indent = lines[target][: len(lines[target]) - len(lines[target].lstrip())]
    derived_lines = lines[: target + 1] + [indent + node for node in OPTION_NODES] + lines[target + 1:]
    derived = newline.join(derived_lines)
    (PROJECT / "War.vbproj").write_bytes(derived.encode("utf-8"))
    diff = "".join(difflib.unified_diff(
        [l + "\n" for l in lines], [l + "\n" for l in derived_lines],
        fromfile="scaffold/War.vbproj (dotnet new console -lang VB)",
        tofile="War/War.vbproj (derived harness)"))
    (HARNESS / "project-diff.txt").write_text(diff, encoding="utf-8", newline="\n")

    build = run(["dotnet", "build"], PROJECT, keep="dotnet-build")
    execution = run(["dotnet", "run", "--no-build"], PROJECT, keep="harness-run") if build.returncode == 0 else None

    snapshot = [PROJECT / "War.vbproj", PROJECT / "Program.vb", SCAFFOLD / "War.vbproj",
                SCAFFOLD / "Program.vb", HARNESS / "project-diff.txt"]
    manifest = {
        "id": "OPS-02",
        "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "sdk_version": version,
        "os": platform.platform(),
        "target_framework": next(l.strip() for l in derived_lines if "<TargetFramework>" in l),
        "source_program_sha256": sha256(SOURCE),
        "project_program_matches_source": sha256(PROJECT / "Program.vb") == sha256(SOURCE),
        "derived_changes": [f"Added {node} after <TargetFramework> in War/War.vbproj" for node in OPTION_NODES],
        "build_exit_code": build.returncode,
        "run_exit_code": execution.returncode if execution else None,
        "files": [{"path": p.relative_to(HARNESS).as_posix(), "bytes": p.stat().st_size, "sha256": sha256(p)}
                  for p in snapshot],
        "copy_rule": "Copy War/War.vbproj and War/Program.vb into assets/<ID>/work/War/, verify both hashes, "
                     "never copy bin/ or obj/, and build inside the copy.",
    }
    (HARNESS / "harness-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (EVIDENCE / "harness-commands.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
