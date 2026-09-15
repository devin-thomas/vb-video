#!/usr/bin/env python3
"""Real-terminal capture driver for the War harness (OPS-02).

Opens an actual conhost window running pwsh, types commands into it through
WriteConsoleInput, reads the real screen buffer back, and saves window images
with PrintWindow. Nothing here draws terminal text: every PNG is the window as
Windows rendered it, and every transcript is read from the console buffer.
"""
from __future__ import annotations

import base64
import ctypes
import ctypes.wintypes as wt
import hashlib
import subprocess
import time
from pathlib import Path

import win32con
import win32console
import win32file
import win32gui
import win32ui
from PIL import Image

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
dwmapi = ctypes.windll.dwmapi
user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))

PWSH = r"C:\Program Files\PowerShell\7\pwsh.exe"
CONHOST = r"C:\Windows\System32\conhost.exe"
PW_RENDERFULLCONTENT = 2
DWMWA_EXTENDED_FRAME_BOUNDS = 9


class COORD(ctypes.Structure):
    _fields_ = [("X", wt.SHORT), ("Y", wt.SHORT)]


class CONSOLE_FONT_INFOEX(ctypes.Structure):
    _fields_ = [("cbSize", wt.ULONG), ("nFont", wt.DWORD), ("dwFontSize", COORD),
                ("FontFamily", wt.UINT), ("FontWeight", wt.UINT), ("FaceName", wt.WCHAR * 32)]


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class ConsoleSession:
    """One visible conhost + pwsh window rooted in an isolated work directory."""

    def __init__(self, workdir: Path, cols: int = 112, rows: int = 34, font: str = "Consolas",
                 font_px: int = 24, buffer_rows: int = 32766, title: str = "PowerShell",
                 position: tuple[int, int] = (80, 80), extra_path: tuple[str, ...] = (),
                 prompt_log: Path | None = None):
        self.workdir = Path(workdir).resolve()
        self.cols, self.rows, self.buffer_rows = cols, rows, buffer_rows
        self.font, self.font_px, self.title, self.position = font, font_px, title, position
        self.extra_path = extra_path
        self.prompt_log = Path(prompt_log or self.workdir.parent / "prompt-log.jsonl").resolve()
        self.prompt = f"PS {self.workdir.name}> "
        self.events: list[dict] = []
        self.t0 = time.monotonic()

    # The prompt shows only the folder name, and silently appends each finished history entry
    # (PowerShell's own start/end times, $? and $LASTEXITCODE) to prompt_log.
    PROMPT_FUNCTION = """function global:prompt {
  $ok = $?; $code = $global:LASTEXITCODE
  $h = Get-History -Count 1
  if ($h -and $h.Id -ne $global:__captureLast) {
    $global:__captureLast = $h.Id
    $rec = [ordered]@{ id = $h.Id; command = $h.CommandLine; status = "$($h.ExecutionStatus)"; succeeded = $ok;
      last_exit_code = $code; start_utc = $h.StartExecutionTime.ToUniversalTime().ToString('o');
      end_utc = $h.EndExecutionTime.ToUniversalTime().ToString('o');
      seconds = [math]::Round(($h.EndExecutionTime - $h.StartExecutionTime).TotalSeconds, 3) }
    [IO.File]::AppendAllText('__LOG__', (ConvertTo-Json $rec -Compress) + "`n")
  }
  $global:LASTEXITCODE = $code
  'PS ' + (Split-Path -Leaf $PWD) + '> '
}"""

    # ----- lifecycle -------------------------------------------------------------------------
    def start(self) -> None:
        pidfile = self.workdir.parent / ".console.pid"
        pidfile.unlink(missing_ok=True)
        self.prompt_log.unlink(missing_ok=True)
        self.setup_script = "\n".join([
            f"[IO.File]::WriteAllText('{pidfile}', \"$PID\")",
            "Import-Module PSReadLine",
            "Set-PSReadLineOption -PredictionSource None -HistorySaveStyle SaveNothing",
            self.PROMPT_FUNCTION.replace("__LOG__", str(self.prompt_log)),
            *[f"$env:Path = $env:Path + ';{entry}'" for entry in self.extra_path],
            f"$Host.UI.RawUI.WindowTitle = '{self.title}'",
            f"Set-Location -LiteralPath '{self.workdir}'",
            "Clear-Host",
        ])
        encoded = base64.b64encode(self.setup_script.encode("utf-16-le")).decode()
        self.proc = subprocess.Popen([CONHOST, PWSH, "-NoLogo", "-NoProfile", "-NoExit",
                                      "-EncodedCommand", encoded])
        deadline = time.monotonic() + 30
        while not (pidfile.exists() and pidfile.read_text().strip()):
            if time.monotonic() > deadline:
                raise RuntimeError("pwsh did not start")
            time.sleep(0.1)
        self.pid = int(pidfile.read_text().strip())
        pidfile.unlink()
        kernel32.FreeConsole()
        if not kernel32.AttachConsole(self.pid):
            raise ctypes.WinError()
        self.hwnd = kernel32.GetConsoleWindow()
        self._in_handle = win32file.CreateFile(
            "CONIN$", win32con.GENERIC_READ | win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE, None, win32con.OPEN_EXISTING, 0, None)
        self.conin = win32console.PyConsoleScreenBufferType(self._in_handle)
        self.window_class = win32gui.GetClassName(self.hwnd)
        self._configure()
        self.wait_prompt(30)
        self.log("session-start", pid=self.pid, window_class=self.window_class)

    def _out(self):
        handle = win32file.CreateFile(
            "CONOUT$", win32con.GENERIC_READ | win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE, None, win32con.OPEN_EXISTING, 0, None)
        return handle, win32console.PyConsoleScreenBufferType(handle)

    def _configure(self) -> None:
        handle, out = self._out()
        info = CONSOLE_FONT_INFOEX()
        info.cbSize = ctypes.sizeof(info)
        info.dwFontSize = COORD(0, self.font_px)
        info.FontFamily = 54
        info.FontWeight = 400
        info.FaceName = self.font
        if not kernel32.SetCurrentConsoleFontEx(int(handle), False, ctypes.byref(info)):
            raise ctypes.WinError()
        out.SetConsoleWindowInfo(True, win32console.PySMALL_RECTType(0, 0, 1, 1))
        out.SetConsoleScreenBufferSize(win32console.PyCOORDType(self.cols, self.buffer_rows))
        out.SetConsoleWindowInfo(True, win32console.PySMALL_RECTType(0, 0, self.cols - 1, self.rows - 1))
        win32gui.SetWindowPos(self.hwnd, 0, self.position[0], self.position[1], 0, 0,
                              win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)
        time.sleep(0.5)

    def close(self) -> None:
        # conhost stays alive while this process is attached, so detach before waiting on it.
        try:
            self.type_line("exit")
            handle = kernel32.OpenProcess(0x00100000, False, self.pid)
            kernel32.WaitForSingleObject(handle, 15000)
            kernel32.CloseHandle(handle)
        finally:
            kernel32.FreeConsole()
            try:
                self.proc.wait(15)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self.log("session-end")

    # ----- input -----------------------------------------------------------------------------
    def _key_records(self, ch: str, vk: int | None = None) -> list:
        if vk is None:
            scan = user32.VkKeyScanW(ord(ch))
            vk, shift = scan & 0xFF, (scan >> 8) & 1
        else:
            shift = 0
        records = []
        for down in (True, False):
            rec = win32console.PyINPUT_RECORDType(win32console.KEY_EVENT)
            rec.KeyDown = down
            rec.RepeatCount = 1
            rec.Char = ch
            rec.VirtualKeyCode = vk
            rec.VirtualScanCode = user32.MapVirtualKeyW(vk, 0)
            rec.ControlKeyState = win32con.SHIFT_PRESSED if shift else 0
            records.append(rec)
        return records

    def type_text(self, text: str, delay: float = 0.004) -> None:
        for ch in text:
            self.conin.WriteConsoleInput(self._key_records(ch))
            time.sleep(delay)

    def press(self, ch: str, vk: int) -> None:
        self.conin.WriteConsoleInput(self._key_records(ch, vk))

    def type_line(self, text: str) -> None:
        self.type_text(text)
        time.sleep(0.15)
        self.press("\r", win32con.VK_RETURN)
        self.log("typed", text=text)

    def run(self, command: str, timeout: float = 600) -> dict:
        """Type a command at the prompt, press Enter, and wait for the prompt to return."""
        self.wait_prompt(10)
        started = time.monotonic()
        self.type_line(command)
        time.sleep(0.4)
        self.wait_prompt(timeout)
        elapsed = time.monotonic() - started
        self.log("completed", text=command, wall_seconds=round(elapsed, 3))
        return {"command": command, "wall_seconds": round(elapsed, 3)}

    # ----- buffer ----------------------------------------------------------------------------
    def buffer_info(self) -> dict:
        _, out = self._out()
        return out.GetConsoleScreenBufferInfo()

    def read_rows(self, top: int, count: int) -> list[str]:
        _, out = self._out()
        width = out.GetConsoleScreenBufferInfo()["Size"].X
        return [out.ReadConsoleOutputCharacter(width, win32console.PyCOORDType(0, y)).rstrip()
                for y in range(top, top + count)]

    def cursor(self) -> tuple[int, int]:
        pos = self.buffer_info()["CursorPosition"]
        return pos.X, pos.Y

    def at_prompt(self) -> bool:
        x, y = self.cursor()
        return x == len(self.prompt) and self.read_rows(y, 1)[0] == self.prompt.rstrip()

    def wait_prompt(self, timeout: float) -> None:
        deadline = time.monotonic() + timeout
        stable = 0
        while stable < 3:
            if time.monotonic() > deadline:
                raise TimeoutError(f"prompt did not return: {self.read_rows(self.cursor()[1], 1)}")
            stable = stable + 1 if self.at_prompt() else 0
            time.sleep(0.15)

    def wait_for_text(self, needle: str, timeout: float = 20) -> None:
        deadline = time.monotonic() + timeout
        while True:
            window = self.buffer_info()["Window"]
            if any(needle in row for row in self.read_rows(window.Top, window.Bottom - window.Top + 1)):
                time.sleep(0.4)
                return
            if time.monotonic() > deadline:
                raise TimeoutError(f"text not shown: {needle}")
            time.sleep(0.15)

    def used_rows(self) -> int:
        return self.cursor()[1] + 1

    def transcript(self) -> str:
        """Every buffer row from the top through the cursor row, exactly as the console holds it."""
        return "\n".join(self.read_rows(0, self.used_rows())) + "\n"

    def window_rect(self) -> tuple[int, int]:
        window = self.buffer_info()["Window"]
        return window.Top, window.Bottom

    def scroll_to(self, top: int) -> tuple[int, int]:
        _, out = self._out()
        top = max(0, min(top, self.buffer_rows - self.rows))
        out.SetConsoleWindowInfo(True, win32console.PySMALL_RECTType(0, top, self.cols - 1, top + self.rows - 1))
        time.sleep(0.5)
        self.log("scrolled", top=top)
        return self.window_rect()

    # ----- pixels ----------------------------------------------------------------------------
    def geometry(self) -> dict:
        handle, _ = self._out()
        info = CONSOLE_FONT_INFOEX()
        info.cbSize = ctypes.sizeof(info)
        kernel32.GetCurrentConsoleFontEx(int(handle), False, ctypes.byref(info))
        ext = wt.RECT()
        dwmapi.DwmGetWindowAttribute(self.hwnd, DWMWA_EXTENDED_FRAME_BOUNDS, ctypes.byref(ext), ctypes.sizeof(ext))
        cx, cy = win32gui.ClientToScreen(self.hwnd, (0, 0))
        return {"font_face": info.FaceName, "cell_px": [info.dwFontSize.X, info.dwFontSize.Y],
                "client_origin_in_png": [cx - ext.left, cy - ext.top],
                "png_size": [ext.right - ext.left, ext.bottom - ext.top]}

    def screenshot(self, path: Path, settle: float = 0.6) -> dict:
        time.sleep(settle)
        hwnd = self.hwnd
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        ext = wt.RECT()
        dwmapi.DwmGetWindowAttribute(hwnd, DWMWA_EXTENDED_FRAME_BOUNDS, ctypes.byref(ext), ctypes.sizeof(ext))
        width, height = right - left, bottom - top
        window_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(window_dc)
        mem_dc = mfc_dc.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        mem_dc.SelectObject(bitmap)
        ok = user32.PrintWindow(hwnd, mem_dc.GetSafeHdc(), PW_RENDERFULLCONTENT)
        bits = bitmap.GetBitmapBits(True)
        image = Image.frombuffer("RGB", (width, height), bits, "raw", "BGRX", 0, 1)
        image = image.crop((ext.left - left, ext.top - top, ext.right - left, ext.bottom - top))
        win32gui.DeleteObject(bitmap.GetHandle())
        mem_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, window_dc)
        if not ok:
            raise RuntimeError("PrintWindow failed")
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path)
        top_row, bottom_row = self.window_rect()
        record = {"file": path.name, "visible_buffer_rows": [top_row, bottom_row],
                  "size": list(image.size), "sha256": sha256(path), **self.geometry()}
        self.log("screenshot", **record)
        return record

    def log(self, event: str, **fields) -> None:
        self.events.append({"t": round(time.monotonic() - self.t0, 3), "event": event, **fields})
