# CODE-27 — Production QA

**Production:** produced. **Release:** unreviewed (review deck).

## What this is
An authored teaching example in classic VB4 style, labelled on the card ("Visual Basic 4 · Option Explicit off" header, "Teaching example" label). It is not an excerpt of Program.vb and is recorded as such in delivery.json and evidence/provenance.json. Code lines are the ticket's exact copy payload (src/example.vb keeps them as text).

## Checks actually performed
- Rendered with the shared renderer from src/build.json (14 authored SVG states, 9 s). PNGs verified 1920 × 1080; preview.mp4 probed with ffprobe: h264, yuv420p, 30 fps, 270 frames, 9.000 s. Record: evidence/render-tests.json.
- Browser check (tools/render/qa_browser.py --id CODE-27, Playwright's bundled Chromium 153.0.8010.12): offline, deterministic seeking, 17 SVG files / 500 text boxes inside the canvas, no network requests. Record: evidence/browser-tests.json. The tool's shared review/browser-summary.json write was reverted so this ticket writes only inside its own folder.
- Manual visual review: Poster, typo.png, option-explicit.png and preview frames at 1.0 s, 3.0 s, 5.3 s, 6.3 s and 8.9 s inspected at 1920 × 1080 and at 1280 × 720 (proofs/poster-720.png plus 1280-wide downsizes made in a scratch folder). Both names are spelled exactly in both states; the error reads "Variable not defined" with Nintendont beneath it; connectors run down the right-margin lane and end 24 px right of the line-3 comment, crossing no code; the red squiggle sits under the token only. A first render had the typing caret over the O of Option at 5.3 s; fixed (row-0 line end recorded) and re-rendered before finishing.
- Fact notes: "Variable not defined" is the classic VB IDE compile error raised under Option Explicit for an undeclared name; the text is the one the ticket requires. No primary VB documentation copy is stored in the repository.

## Reproduction (from the repository root, Windows, CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin)
```
python assets/code/CODE-27/src/author.py
python tools/render/render_assets.py --id CODE-27
python tools/render/qa_browser.py --id CODE-27
python tools/validate_delivery.py --id CODE-27
```
Tool versions: Windows-11-10.0.26200-SP0; Python 3.14.0; ffmpeg version 6.0-essentials_build-www.gyan.dev Copyright (c) 2000-2023 the FFmpeg developers; CairoSVG 2.9.1; Pillow 12.3.0; Playwright 1.63.0 with Chromium 153.0.8010.12. No installs, no network, no font files distributed. Proof at 720p: proofs/poster-720.png.

## Remaining decisions
No assigned claim gate. Release approval comes from the review deck; produced is not release-approved.

## Asset-specific notes
- Authored teaching example in classic VB4 style; not an excerpt of Program.vb. Names are exactly Nintendo (declared) and Nintendont (misspelled).
- State A (Option Explicit off): the misspelled line silently creates a new, empty Nintendont; Nintendo stays 1985 and Print Nintendo outputs 1985.
- State B (Option Explicit On): the same line is flagged with the classic VB message "Variable not defined", pointing at Nintendont. The card header switches to "Option Explicit on".
- The long line 3 leaves no room beside the code, so both callouts sit below the code and their connectors enter from the right-margin lane (x=1745, right of every line end); no annotation crosses code text.
- Discrete deterministic step states: lines type in 0.4–1.6 s, State A callout 2–2.5 s, Option Explicit On types in 5–5.6 s, State B error 6–6.6 s, hold to 9 s (poster).
