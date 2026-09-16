# REF-02 — Production QA (revision 2, 2026-09-16)

**Production:** produced. **Release:** unreviewed (revision 2 replaces the exports the producer approved on 2026-09-15; it goes back through the review deck).

## What changed in revision 2
Devin's review note 5: the narration promises "a 73-line C Hello World for Windows, scrolling slowly"; the first cut showed a 63-line excerpt that read as a fragment. `src/excerpt.c` is now a complete Windows 3.x (Win16) Hello World in C of **exactly 73 lines**; `src/hello.def` (11 lines) is the module-definition file, shown separately after a rule and not counted in the 73. Both were authored for this production in Petzold-era style; nothing was copied from a book listing, tutorial or SDK sample.

**Line count (measured, not estimated):** `wc -l src/excerpt.c` → 73; Python `splitlines()` → 73; `build_scenes.py` asserts 73 and fails otherwise. `hello.def`: 11 by both counts. No tabs, LF line endings, longest line 78 characters (fits the 1680 px panel with 150 px to spare at 30 px DejaVu Sans Mono).

## Delivered
Each media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json (written by `src/build_scenes.py --inventory`). All exports are freshly rendered media, not placeholders. The revision-1 scene files were deleted and regenerated; the `clean` and `teaching-focus` variant names and every deliverable path are unchanged.

## Not compiled: no 16-bit toolchain
No Microsoft C 6/7, Windows 3.1 SDK, Borland C++ 3.x or Open Watcom 16-bit target is installed on the production machine, and installs are not permitted. Nothing was compiled, linked or run; no build output or screenshot is claimed. In its place the listing was read line by line against the Windows 3.1 SDK API by the producing agent (this session, not an independent second reader — see review questions). What was checked:

| Lines | Construct | Check against the Windows 3.1 SDK (`WINDOWS.H`, non-STRICT) |
|---|---|---|
| 1–2 | Block comment | Two-line `/* ... */`; opened on line 1, closed on line 2. |
| 4 | `#include <windows.h>` | The only header a Win16 program needs for USER/GDI/KERNEL. |
| 6 | `long FAR PASCAL __export WndProc (HWND, UINT, UINT, LONG);` | `WNDPROC` is `LRESULT (CALLBACK*)(HWND, UINT, WPARAM, LPARAM)`; in 3.1 `LRESULT`=`LONG`, `CALLBACK`=`FAR PASCAL`, `WPARAM`=`UINT`, `LPARAM`=`LONG`, so the spelled-out form matches. `__export` (Microsoft C 6/7 keyword) generates the exported-function prolog; the `.DEF` `EXPORTS` line is retained as Petzold-era practice. |
| 8–9 | `int PASCAL WinMain (HANDLE hInstance, HANDLE hPrevInstance, LPSTR lpszCmdLine, int nCmdShow)` | Win16 signature; `HANDLE` for the instance handles is the 3.0/3.1 idiom (`HINSTANCE` is also a `UINT` in non-STRICT builds). |
| 11 | `static char szAppName[] = "Hello";` | Near string in DGROUP; passes to `LPCSTR` parameters by implicit near→far conversion. |
| 12–14 | `HWND`, `MSG`, `WNDCLASS` | All defined in `WINDOWS.H`. |
| 16 | `if (!hPrevInstance)` | Win16 registers a window class once per module; later instances share it. |
| 18–27 | `WNDCLASS` filled field by field | All ten members in declaration order: `style`, `lpfnWndProc`, `cbClsExtra`, `cbWndExtra`, `hInstance`, `hIcon`, `hCursor`, `hbrBackground`, `lpszMenuName`, `lpszClassName`. `CS_HREDRAW | CS_VREDRAW` are class styles; `LoadIcon (NULL, IDI_APPLICATION)` and `LoadCursor (NULL, IDC_ARROW)` load the stock resources; `GetStockObject (WHITE_BRUSH)` returns an `HGDIOBJ` (`UINT` non-STRICT) assignable to `HBRUSH` without a cast in period code; `lpszMenuName = NULL` means no class menu. |
| 29–30 | `if (!RegisterClass (&wndclass)) return FALSE;` | `ATOM RegisterClass (const WNDCLASS FAR*)`; zero means failure. |
| 33–41 | `CreateWindow (...)` | Eleven arguments in SDK order: class name, caption, `WS_OVERLAPPEDWINDOW`, x, y, width, height, parent, menu, instance, creation parameter. `CW_USEDEFAULT` is valid for position and size of an overlapped window in Win16. `hInstance` (`HANDLE`) is passed where `HINSTANCE` is expected. |
| 43–44 | `ShowWindow (hwnd, nCmdShow); UpdateWindow (hwnd);` | Standard sequence; `UpdateWindow` sends the first `WM_PAINT`. |
| 46–50 | `while (GetMessage (&msg, NULL, 0, 0)) { TranslateMessage (&msg); DispatchMessage (&msg); }` | `BOOL GetMessage (LPMSG, HWND, UINT, UINT)` returns FALSE on `WM_QUIT`; `TranslateMessage`/`DispatchMessage` take `const MSG FAR*`. |
| 51 | `return msg.wParam;` | `WM_QUIT`'s `wParam` carries the `PostQuitMessage` exit code; `UINT`→`int` is the period idiom. |
| 54–55 | `long FAR PASCAL __export WndProc (HWND hwnd, UINT message, UINT wParam, LONG lParam)` | Definition matches the prototype on line 6 and the `WNDPROC` type. |
| 57–58 | `HDC hdc; PAINTSTRUCT ps;` | Locals for the paint handler. |
| 60–71 | `switch (message)` with `WM_PAINT` and `WM_DESTROY` | `HDC BeginPaint (HWND, PAINTSTRUCT FAR*)`; `BOOL TextOut (HDC, int, int, LPCSTR, int)` with the 15-character `"Hello, Windows!"` and count 15; `void EndPaint (HWND, const PAINTSTRUCT FAR*)`; `void PostQuitMessage (int)`. Each handled message returns 0. |
| 72 | `return DefWindowProc (hwnd, message, wParam, lParam);` | `LRESULT DefWindowProc (HWND, UINT, WPARAM, LPARAM)`; unhandled messages fall through to it. |
| `.DEF` | `NAME`, `DESCRIPTION`, `EXETYPE WINDOWS`, `STUB 'WINSTUB.EXE'`, `CODE PRELOAD MOVEABLE DISCARDABLE`, `DATA PRELOAD MOVEABLE MULTIPLE`, `HEAPSIZE 1024`, `STACKSIZE 8192`, `EXPORTS WndProc` | The statements LINK 5.x expects for a Windows 3.x executable; `DATA ... MULTIPLE` gives each instance its own data segment, which is why `hPrevInstance` matters. Comment lines start with `;`. |

Also checked: every brace pairs; every `case` ends in `return`; all identifiers are declared before use; no Win32-only names (`HINSTANCE`-typed `WinMain`, `WINAPI`, `LRESULT CALLBACK`, `GetMessage` casts, `WNDCLASSEX`, `RegisterClassEx`, `CreateWindowEx`) appear. Nothing here is a compiler run: a Win16 build is the real test and remains open under R15.

## Checks actually performed
- `python assets/reference-code/REF-02/src/build_scenes.py` — 209 unique SVG states (16-row first viewport, 207 one-third-row scroll steps, the message-loop focus), `build.json`, `timeline.json`, `index.html` (4.5 MB, every state inlined, same `window.__ASSET__.renderAt` contract as the batch). The script asserts the 73-line count and that the longest line stays inside the panel.
- `python tools/render/render_assets.py --id REF-02` (CairoSVG 2.9.1 via `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin`, ffmpeg 6.0): poster, `clean.png`, `teaching-focus.png`, start/middle/end keyframes, `contact-sheet.png`, `proofs/poster-720.png`, `exports/preview.mp4`. The renderer's ffprobe assertions passed: H.264, 1920×1080, 30/1, yuv420p, 804 frames, 26.800 s. Re-probed by hand with the same result.
- `python tools/render/qa_browser.py --id REF-02` (Playwright, installed Chromium 153.0.8010.12, in-memory HTML): 212 SVG files (209 states + poster + 2 variants), 23 203 text boxes, none outside the canvas, deterministic seeking, no network request. The script also touched `review/browser-summary.json` outside this ticket's paths; that file was reverted with `git checkout` so only `evidence/browser-tests.json` carries the result.
- `python assets/reference-code/REF-02/src/build_scenes.py --inventory` then `python tools/validate_delivery.py --id REF-02` — result recorded below.
- `tools/render/finish_delivery.py` was **not** run: for a revision it would also rewrite `docs/tickets/REF-02.md` (dropping the "Revision 2" section) and `review/production-index.json`, both outside the owned paths. delivery.json, qa.md and state.json were written directly instead.

## Visual review (this session, Read tool on the actual files)
- Full size (1920×1080): `exports/poster.png`, `exports/clean.png`, `exports/teaching-focus.png`, `exports/contact-sheet.png`, and five frames decoded from `exports/preview.mp4` at 4.0 s, 10.0 s, 15.0 s, 20.0 s and 23.3 s.
- 720p (1280×720, scaled with ffmpeg from the MP4): `proofs/frames-720/frame-01..09.png` = frames 0, 120, 300, 450, 600, 675, 690, 700, 800 (0.0 s first viewport; 4.0 s, 10.0 s, 15.0 s, 20.0 s and 22.5 s mid-scroll; 23.0 s end of scroll with the whole `.DEF` through `EXPORTS WndProc`; 23.3 s and 26.7 s the focus hold). Plus `proofs/poster-720.png`.
- Result: code is readable at 720p in every frame, including the mid-scroll ones where a row is partly clipped at the panel's top or bottom edge; the 30 px mono type renders at 20 px at 720p with clear keyword/string/comment colours; the two-line block comment is green on both lines; line numbers restart at 1 for `hello.def`; the rule separates the files; the header reads "hello.c (73 lines)   hello.def (11 lines)"; the focus band covers exactly lines 46–50 (`while (GetMessage` … `}`) and the caption has the footer to itself (the line-count footer of revision 1 was moved to the header because it collided with the caption). No text overlaps, no clipped glyph outside the panel, nothing outside the safe area.
- Motion: 2.0 s hold, then one third of a row every 0.1 s (three frames per state) = 0.3 s per row = 3.33 rows/s, under the 4 rows/s ceiling; the scroll covers all 85 rows (73 + rule + 11) in 20.7 s (2.0 s → 22.7 s), holds 0.6 s on the last viewport, then cuts to the focus at 23.3 s and holds it to 26.8 s. Total 26.8 s; the scrolling motion itself is 20.7 s, within the requested 20–25 s.

## Reproduction
From the repository root, with `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` set as an environment variable (not on PATH) and `fc-match`, `ffmpeg`/`ffprobe` on PATH:

```
python assets/reference-code/REF-02/src/build_scenes.py
python tools/render/render_assets.py --id REF-02
python tools/render/qa_browser.py --id REF-02
python assets/reference-code/REF-02/src/build_scenes.py --inventory
python tools/validate_delivery.py --id REF-02
```

Do **not** run `tools/render/build_assets.py --id REF-02`: it still reads the revision-1 fixture in `tools/fixtures/ref-02-hello.c` and would overwrite these sources (the fixture is outside this ticket's paths; see review questions). Tool versions: Windows 11 10.0.26200, Python 3.14.0, CairoSVG 2.9.1, Pillow 12.3.0, Playwright 1.63.0 with Chromium 153.0.8010.12, ffmpeg 6.0-essentials_build; recorded in delivery.json `toolchain`.

## Validator
`python tools/validate_delivery.py --id REF-02` (2026-09-16, after the final inventory): `"ok": true, "errors": []` — 244 hashed outputs, every required path present, all export PNGs 1920×1080. Its stated limitations (no OCR, no MP4 decode, no historical/legal clearance, manual 1080p/720p review still required) are covered by the checks above.

## Remaining decisions and review questions
Assigned gates: R03, R15 (`evidence/claim-checks.json`). Both were approved on 2026-09-15 for the revision-1 exports; the code is new, so both are recorded as awaiting re-review through the deck, with the evidence above.

1. **Era spelling (R15).** The narration says Windows 3.0 and 1991. The ticket asked for `long FAR PASCAL __export WndProc` and the listing follows the Windows 3.1 SDK spellings (`UINT message, UINT wParam, LONG lParam`, `__export`). A Windows 3.0 SDK (1990) programmer would more likely have written `long FAR PASCAL WndProc (HWND, unsigned, WORD, LONG)` with no `__export` and relied on `EXPORTS` alone. The on-screen label says "Windows 3.x (Win16)" to cover both. Producer's call whether to keep 3.1 idiom or switch to the older spelling (same line count either way).
2. **Second reader.** The ticket asked for a second agent to read the code line by line for API correctness; this revision was read by the producing session only (table above). If the producer wants an independent read, it is a small task with `src/excerpt.c` and `src/hello.def` as the only inputs.
3. **Stale fixture outside this ticket.** `tools/fixtures/ref-02-hello.c` / `.def` still hold the 63-line revision-1 code, and `build_assets.py` would regenerate from them. Updating the fixture (or pointing `historical_code()` at this asset's `src/`) is a tools/ change for the producer.
4. **Motion style.** Revision 1 stepped a whole row every 0.25 s; revision 2 steps a third of a row every 0.1 s, so the scroll reads as slow continuous motion rather than a stepped crawl. If Devin prefers the stepped look, set `SUB = 1`, `STEP = 0.3` in `build_scenes.py` and re-render.

No narration sync, sound design, final assembly, compile proof or live capture is certified here. Produced is intentionally different from release-approved.
