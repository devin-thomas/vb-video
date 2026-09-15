# XTRA-19 — Production QA

**Production:** produced. **Release:** blocked. R14 is open: the image is Microsoft-copyrighted software UI from an unidentified capturer, with no license or permission (`evidence/rights.json`).

This is a script supplement for `SCRIPT.md:579` (original family SCRIPT-SUPPLEMENT). It is not a row of the categorized asset plan.

## Delivered
- `source/original.png`: the unmodified WinWorld screenshot "Microsoft Entertainment Pack 2 - Cards". It is a 640×480 palette PNG with 13 colours, 8,572 bytes, SHA-256 `e9cc2537…d846dfd`. This is the `original` variant.
- `exports/editorial-frame.png`: a 1920×1080 frame with the whole capture at integer 2× nearest-neighbour, pillarboxed. This is the `editorial-frame` variant.
- `proofs/editorial-frame-720.png`: a 1280×720 review proof.
- `src/render_frame.py`: the reversible framing script. `evidence/framing.json` holds the exact geometry.
- `evidence/source.json`, `rights.json`, `provenance.json`, `source-excerpts.md`, `claim-checks.json`.
- Every file except delivery.json and state.json is listed with bytes and SHA-256 in `delivery.json`.

This is a still asset: no duration, no fps, no motion. It holds for editorial timing.

## Source and identity
- **Host:** WinWorld.
  - Gallery "Screenshots for Microsoft Entertainment Pack 2": https://winworldpc.com/screenshot/c3b2c3af-c2b1-c3a0-4b62-11c3a4c28d58
  - Detail page: https://winworldpc.com/screenshot/c3b2c3af-c2b1-c3a0-4b62-11c3a4c28d58/c2b3c2ab-c2a4-064b-c3b0-11c3a4c28d58
  - File: https://winworldpc.com/res/img/screenshots/2-e0249a99db7492f217c030c559f6c27c-Microsoft%20Entertainment%20Pack%202%20-%20Cards.png
- **Access:** accessed 2026-09-15 and downloaded at 20:41:38 UTC by anonymous HTTPS GET. There was no account, login, CAPTCHA, payment or terms acceptance. HTTP 200, Last-Modified Fri, 02 Oct 2015 22:32:18 GMT. A second, earlier download has the same SHA-256.
- **Identity, read from the pixels at 1:1 and 4× rather than from the caption:**
  - The title bar reads "FreeCell Game #14601".
  - The menu reads Game / Options / Help, with "Cards Left: 52" at the right.
  - The FreeCell king icon sits between the free cells and the home cells, on green felt.
  - The window chrome is Windows 3.x: a system-menu box, minimize/maximize arrow buttons and no close button. The active title bar is dithered, which fits a 16-colour display.
  - A Tut's Tomb window (also Entertainment Pack 2) is behind FreeCell, and a minimized File Manager icon is on the desktop.
  - It is not the Vista+ remake, not Windows 95 chrome and not a clone.
- **Limits:**
  - The pixels cannot separate Windows 3.0 from 3.1, or the Entertainment Pack 2 FreeCell from the Best of Entertainment Pack or Win32s builds. "Entertainment Pack 2" is WinWorld's attribution, supported by Tut's Tomb.
  - The capture date is unknown. This is a later capture of period software, probably emulated, not a 1990s screenshot.
- **Period UI reference only.** It is not evidence of Visual Basic authorship; FreeCell is a Microsoft product.
- **Candidates rejected** (details in `evidence/provenance.json`):
  - Internet Archive `Freecell_Windows/Freecell.png`: genuine Italian Microsoft FreeCell, but captured in **Windows 7 chrome** with a 2018 `cards.dll`. It is kept as the alternate for Q3.
  - IA `wep_best-of` screenshot-2: a German Windows 3.1 Program Manager with a Free Cell icon. It shows the icon, not the game.
  - Marc L. Allen's 1992 shareware FreeCell.
  - A failed emulation (`freecell_20251029`).
  - Commons: only GNOME, KDE and PySol clones; Commons deletes non-free Windows UI.
  - GUIdebook and WinWorld NT 4.0: no FreeCell entries.
- **Access notes:**
  - BetaWiki returned 403.
  - The TCRF FreeCell page returned text addressed to AI agents (prompt-injection content). It was ignored and is not used as evidence.
  - No disk images, zips or executables were downloaded or run.

## Checks actually performed
- **Identity read from the image** (whole image, four 4× nearest-neighbour crops): passed.
- **Original unmodified:** the SHA-256 of `source/original.png` matches both downloads, and it is unchanged before and after rendering (the script asserts this, and `finalize.py` re-checks it). Passed.
- **Native format:** 640×480 PNG, palette mode, 13 colours, no text chunks (Pillow). Passed.
- **Integer scaling, no stretch:** 2× nearest-neighbour to 1280×960, aspect 1.33333 in and out. The render script asserts that every 2×2 output block equals its source pixel. Passed.
- **No crop:** the whole capture is placed at x=320, y=60, and sampled background pixels are #111318. The overlapping Tut's Tomb window and the clipped FreeCell columns are kept as captured. Passed.
- **Safe area:**
  - The image spans y=60..1020, which is 12 px past the y=72..1008 band at the top and bottom. That band is for essential text.
  - The top and bottom 12 px of the frame hold only window borders and grey desktop. The Tut's Tomb title text starts near y=72, and the "File Manager" label ends near y=1000.
  - This keeps an integer scale instead of a non-integer 1.95× nearest-neighbour. Accepted and recorded in `evidence/framing.json`.
- **Export 1920×1080 RGB, proof 1280×720 RGB** (Pillow): passed.
- **No added text, captions or annotations; no watermark removal** (none present): passed.
- **Privacy:** no personal data in outputs. Internet Archive uploader emails seen in public metadata are not copied. Passed.
- **`python tools/validate_delivery.py --id XTRA-19`:** run after bundling; the verbatim result is recorded in `delivery.json` tests and the worker report.

## Manual visual inspection
- **Full size (1920×1080):** I viewed `exports/editorial-frame.png` in full, plus three 1:1 crops of the export (the FreeCell title and top row 900×360, the top-left 700×360, and the bottom-left 700×220).
  - Pixels are clean 2× blocks, with no blur, ringing or colour shift.
  - "FreeCell Game #14601", the Game/Options/Help menu, "Cards Left: 52" and the king icon are sharp and easy to read. So are "Tut's Tomb", "Time: 28" and "File Manager".
  - The capture sits centered on the dark ground, with no clipping at any edge.
  - FreeCell's rightmost column and lower cards are cut off inside the FreeCell window, as in the original.
  - The mouse pointer is visible near the home cells.
- **720p (1280×720):** I viewed `proofs/editorial-frame-720.png`. The FreeCell title, menu, "Cards Left: 52", the king icon and the card faces stay readable. Tut's Tomb and the Windows 3.x chrome are clearly recognisable. At this size the menu text is small but legible.

## Reproduction
From the repository root:
```
curl -sL -o assets/historical/XTRA-19/source/original.png "https://winworldpc.com/res/img/screenshots/2-e0249a99db7492f217c030c559f6c27c-Microsoft%20Entertainment%20Pack%202%20-%20Cards.png"
python assets/historical/XTRA-19/src/render_frame.py
python tools/validate_delivery.py --id XTRA-19
```
Check that the re-downloaded file's SHA-256 is `e9cc253728498aae694371f600c86d9df52565ed7efe055d7b5c1ff4cd846dfd` before rendering. If the host has replaced the file, treat it as a new acquisition.

Toolchain: Windows-11-10.0.26200-SP0; Python 3.14.0; Pillow 12.3.0; curl 8.18.0 (x86_64-w64-mingw32). The shared render pipeline (`tools/render/*`, CairoSVG) was not used, because this asset has no SVG or HTML source. No fonts are used.

## Gates and review questions
- **R14:** blocked (`evidence/claim-checks.json`).
  - Verified by evidence: genuine Microsoft FreeCell in Windows 3.x chrome; Microsoft as UI rights holder; no license on the file; clean access route.
  - Not settled by evidence: permission to use the image, and the capturer's identity.
- **XTRA-19-Q1 (legal risk; Devin):**
  - The frame shows Microsoft-copyrighted UI: FreeCell, Tut's Tomb and Windows 3.x. The capturer is unidentified, and there is no license.
  - WinWorld's copyright page says copyright stays with the original publisher even for "abandoned" software.
  - Options:
    - (a) Brief editorial display with the credit line in `evidence/rights.json`, under a fair-use judgment. A human may first read Microsoft's own screenshot-permission guidance; no agent accepted or relied on it.
    - (b) A human re-captures FreeCell from legitimately owned Entertainment Pack or Windows media. That removes the unknown-capturer question, but not Microsoft's UI copyright.
    - (c) Cut the image.
  - Release stays blocked until one is chosen.
- **XTRA-19-Q2 (script wording; Writing Lead):**
  - The cue at `War/SCRIPT.md:636` reads "Screenshots of 90s shareware card games — Solitaire, Hearts, FreeCell. Windows 3.1 and Windows 95 versions."
  - Evidence (`evidence/claim-checks.json`, `script_check`):
    - **Not shareware.** Microsoft FreeCell, Solitaire and Hearts were commercial Microsoft software. FreeCell was sold on Microsoft Entertainment Pack 2 and later bundled with Win32s and Windows 95. The narration at `War/SCRIPT.md:650` already separates the bundled Microsoft games from the shareware alternatives, so the cue label contradicts it.
    - **"Windows 3.1" needs a qualifier.** FreeCell did run on Windows 3.x, but as an add-on:
      - Entertainment Pack 2, "for Windows 3.0 and later" per WinWorld; 1991 per WinWorld and Eli's, 1992 per Keller's FAQ.
      - The 1994 Best of Microsoft Entertainment Pack.
      - The Win32s test app, per Microsoft KB Q106715.
    - It was first bundled with Windows itself in Windows 95. Windows 3.1 did not include FreeCell.
  - Proposed cue wording (not applied): **"[VISUAL: Screenshots of Microsoft's own card games — Solitaire, Hearts, FreeCell — as they looked on Windows 3.x and Windows 95 (FreeCell came to Windows 3.x on the Microsoft Entertainment Pack before Windows 95 bundled it). The classic green felt background.]"**
  - If captions are used, the proposed on-screen label for this asset is "FreeCell — Microsoft Entertainment Pack 2, Windows 3.x". Avoid putting a year on screen, because the 1991 vs 1992 sources conflict.
  - `War/SCRIPT.md` was not edited.
- **XTRA-19-Q3 (editorial; editor or Devin):**
  - The only period-chrome FreeCell capture found has a Tut's Tomb window overlapping on the left, and the FreeCell window is sized small, so its columns are clipped. It was kept uncropped, because cropping to FreeCell only would be an editorial reframe of a partial window.
  - Options:
    - (a) Use it as delivered. It reads as an authentic busy Windows 3.x desktop.
    - (b) Add a later reversible zoom or crop onto the FreeCell window in the edit.
    - (c) Use the full, clean board from the Internet Archive `Freecell_Windows` capture instead. It has genuine 1996 Italian FreeCell, but Windows 7 chrome, and it could not be labelled a Windows 3.1 or 95 screenshot.
    - (d) Have a human re-capture it (see Q1b).

## Reviewer
Produced and inspected by the XTRA-19 worker agent under the Archive Extras Manager. No human media review or rights decision is recorded yet.
