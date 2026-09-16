"""Automated screen recordings for handoff H01, driven through the OPS-02 console harness.

Each take opens a real conhost + pwsh window (the same ConsoleSession the TERM captures used), records the window
region with ffmpeg gdigrab at 30 fps while commands are typed through WriteConsoleInput, and saves
recordings/<take>/take.mp4 with take.json (commands, timings, stdout sha256). Program output is never edited; the
war-heavy take (R4) is a bounded search like TERM-04's and every attempt is kept.

  python tools/recording/record_takes.py --list
  python tools/recording/record_takes.py --take R2
  python tools/recording/record_takes.py            # all takes, in order

Leave the desktop alone while it runs: the console window is captured from the screen.
"""
from __future__ import annotations
import argparse, ctypes, ctypes.wintypes as wt, hashlib, json, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/war-harness/tools"))
from console_capture import ConsoleSession  # noqa: E402
import win32con  # noqa: E402

HARNESS = ROOT / "tools/war-harness"
OUT = ROOT / "recordings"
GIT_USR_BIN = r"C:\Program Files\Git\usr\bin"
VIM = 'vim -u NONE -i NONE -N -n -R -c "syntax on" -c "set number" {name}'
FPS = 30
LF = "\n"
dwmapi = ctypes.windll.dwmapi
DWMWA_EXTENDED_FRAME_BOUNDS = 9

def sha256(p: Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()

def fresh_work(take: str, with_harness: bool) -> Path:
    work = OUT / take / "work" / "War"
    if work.exists(): shutil.rmtree(work.parent)
    work.mkdir(parents=True)
    if with_harness:
        manifest = json.loads((HARNESS / "harness-manifest.json").read_text(encoding="utf-8"))
        expected = {f["path"]: f["sha256"] for f in manifest["files"]}
        for name in ("War.vbproj", "Program.vb"):
            shutil.copyfile(HARNESS / "War" / name, work / name)
            assert sha256(work / name) == expected[f"War/{name}"], f"harness copy hash mismatch: {name}"
    return work

def window_region(hwnd) -> tuple[int, int, int, int]:
    ext = wt.RECT()
    dwmapi.DwmGetWindowAttribute(hwnd, DWMWA_EXTENDED_FRAME_BOUNDS, ctypes.byref(ext), ctypes.sizeof(ext))
    w, h = ext.right - ext.left, ext.bottom - ext.top
    return ext.left, ext.top, w - (w % 2), h - (h % 2)

class Recorder:
    def __init__(self, hwnd, path: Path):
        x, y, w, h = window_region(hwnd)
        self.path = path; self.region = (x, y, w, h)
        self.proc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "gdigrab", "-framerate", str(FPS),
                                      "-offset_x", str(x), "-offset_y", str(y), "-video_size", f"{w}x{h}", "-draw_mouse", "0", "-i", "desktop",
                                      "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(path)],
                                     stdin=subprocess.PIPE)
        self.t0 = time.monotonic(); time.sleep(1.0)
    def stop(self) -> float:
        try:
            self.proc.stdin.write(b"q"); self.proc.stdin.flush()
        except OSError:
            pass
        self.proc.wait(30)
        try:
            self.proc.stdin.close()
        except OSError:
            pass
        return time.monotonic() - self.t0

def session(work: Path, title: str, cols=100, rows=30, extra=()) -> ConsoleSession:
    s = ConsoleSession(work, cols=cols, rows=rows, font_px=28, title=title, extra_path=extra, prompt_log=work.parent / "prompt-log.jsonl")
    s.start(); return s

def finish(take: str, work: Path, s: ConsoleSession, rec: Recorder, extra: dict) -> dict:
    seconds = rec.stop()
    s.close()
    record = {"take": take, "file": rec.path.name, "seconds": round(seconds, 2), "fps": FPS, "region": rec.region,
              "events": s.events, "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%S"), **extra}
    for name in ("stdout.txt",):
        if (work / name).exists(): record[f"{name}_sha256"] = sha256(work / name)
    (OUT / take / "take.json").write_text(json.dumps(record, indent=1, ensure_ascii=False) + LF, encoding="utf-8")
    print(f"[ok] {take}: {seconds:.1f}s -> {rec.path}")
    return record

def r1() -> None:  # project creation in an empty folder
    work = fresh_work("R1", with_harness=False); s = session(work, "War")
    rec = Recorder(s.hwnd, OUT / "R1" / "take.mp4")
    s.run("dotnet --version"); time.sleep(1.5); s.run("Get-ChildItem"); time.sleep(1.0)
    s.run("dotnet new console -lang VB", timeout=300); time.sleep(1.5); s.run("Get-ChildItem"); time.sleep(3.0)
    finish("R1", work, s, rec, {"commands": ["dotnet --version", "Get-ChildItem", "dotnet new console -lang VB", "Get-ChildItem"]})

def run_take(take: str, hold_end: float = 4.0) -> dict:
    work = fresh_work(take, with_harness=True); s = session(work, "War")
    s.run("dotnet build", timeout=600); s.run("Clear-Host"); time.sleep(0.5)
    rec = Recorder(s.hwnd, OUT / take / "take.mp4")
    time.sleep(0.8)
    s.run("dotnet run --no-build 2> stderr.txt | Tee-Object -FilePath stdout.txt", timeout=3600)
    time.sleep(hold_end)
    lines = (work / "stdout.txt").read_text(encoding="utf-8-sig").splitlines()
    summary = {"commands": ["dotnet build (before recording)", "dotnet run --no-build | Tee-Object stdout.txt"],
               "rounds": next((l.split(":")[-1].strip() for l in lines if "Total rounds played" in l), None),
               "wars": next((l.split(":")[-1].strip() for l in lines if "Total wars fought" in l), None),
               "winner": next((l.strip() for l in lines if "WINS THE WAR" in l or "ENDS IN A DRAW" in l), None),
               "double_war": any("war number 2" in l for l in lines), "stdout_lines": len(lines)}
    shutil.copyfile(work / "stdout.txt", OUT / take / "stdout.txt")
    return finish(take, work, s, rec, summary)

def r4() -> None:  # war-heavy: bounded search for a chained war, every attempt kept
    for attempt in range(1, 13):
        rec = run_take(f"R4-{attempt:02d}", hold_end=3.0)
        if rec["double_war"]:
            (OUT / "R4-selected.json").write_text(json.dumps({"selected": f"R4-{attempt:02d}", "attempts": attempt}, indent=1) + LF, encoding="utf-8")
            print(f"[ok] R4: double war found on attempt {attempt}"); return
    (OUT / "R4-selected.json").write_text(json.dumps({"selected": None, "attempts": 12, "note": "no chained war in 12 runs"}, indent=1) + LF, encoding="utf-8")

def r5() -> None:  # slow scroll through Program.vb in vim
    work = fresh_work("R5", with_harness=True); s = session(work, "War", cols=108, rows=30, extra=(GIT_USR_BIN,))
    n_lines = len((work / "Program.vb").read_text(encoding="utf-8").splitlines())
    s.run("Clear-Host"); time.sleep(0.3)
    rec = Recorder(s.hwnd, OUT / "R5" / "take.mp4")
    s.type_line(VIM.format(name="Program.vb")); s.wait_for_text("Module Program", 30); time.sleep(2.5)
    for _ in range(n_lines - (s.rows - 1) + 2):
        s.press("\x05", 0x45)  # Ctrl-E scrolls one line
        time.sleep(0.16)
    time.sleep(3.0)
    s.type_text(":q"); s.press("\r", win32con.VK_RETURN); s.wait_prompt(15)
    finish("R5", work, s, rec, {"commands": [VIM.format(name="Program.vb"), "Ctrl-E per line", ":q"], "source_lines": n_lines, "program_vb_sha256": sha256(work / "Program.vb")})

def r6() -> None:  # the project file with the two Option nodes
    work = fresh_work("R6", with_harness=True); s = session(work, "War", cols=100, rows=20, extra=(GIT_USR_BIN,))
    s.run("Clear-Host"); time.sleep(0.3)
    rec = Recorder(s.hwnd, OUT / "R6" / "take.mp4")
    s.type_line(VIM.format(name="War.vbproj")); s.wait_for_text("OptionStrict", 30); time.sleep(6.0)
    s.type_text(":q"); s.press("\r", win32con.VK_RETURN); s.wait_prompt(15)
    finish("R6", work, s, rec, {"commands": [VIM.format(name="War.vbproj"), ":q"], "vbproj_sha256": sha256(work / "War.vbproj")})

TAKES = {"R1": r1, "R2": lambda: run_take("R2"), "R3a": lambda: run_take("R3a"), "R3b": lambda: run_take("R3b"), "R4": r4, "R5": r5, "R6": r6}

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--take"); ap.add_argument("--list", action="store_true"); args = ap.parse_args()
    if args.list: print(", ".join(TAKES)); return 0
    OUT.mkdir(exist_ok=True)
    for name, fn in TAKES.items():
        if args.take and name != args.take: continue
        fn()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
