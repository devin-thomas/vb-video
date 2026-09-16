# CODE-26 — Production QA

**Production:** produced. **Release:** unreviewed (review deck).

## What this is
An authored teaching example in classic VB4 style, labelled on the card ("Visual Basic 4 · Option Explicit off" header, "Teaching example" label). It is not an excerpt of Program.vb and is recorded as such in delivery.json and evidence/provenance.json. Code lines are the ticket's exact copy payload (src/example.vb keeps them as text).

## Checks actually performed
- Rendered with the shared renderer from src/build.json (12 authored SVG states, 6 s). PNGs verified 1920 × 1080; preview.mp4 probed with ffprobe: h264, yuv420p, 30 fps, 180 frames, 6.000 s. Record: evidence/render-tests.json.
- Browser check (tools/render/qa_browser.py --id CODE-26, Playwright's bundled Chromium 153.0.8010.12): offline, deterministic seeking, 15 SVG files / 162 text boxes inside the canvas, no network requests. Record: evidence/browser-tests.json. The tool's shared review/browser-summary.json write was reverted so this ticket writes only inside its own folder.
- Manual visual review: Poster, clean.png, callout.png and preview frames at 1.5 s, 2.6 s and 5.9 s inspected at 1920 × 1080 and at 1280 × 720 (proofs/poster-720.png plus 1280-wide downsizes made in a scratch folder). The word Variant is on screen from 2.9 s to the end and in the poster; the callout arrow enters from the right margin and ends 26 px right of `42`, touching no code; the `x` highlight sits behind the token only; type legible at 720p.
- Fact notes: Classic VB (through VB6, Option Explicit off) creates an undeclared variable on first use with the Variant type. This is the narration's own statement (SCRIPT.md:166) and is the teaching claim of the card; no separate primary source is stored in the repository.

## Reproduction (from the repository root, Windows, CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin)
```
python assets/code/CODE-26/src/author.py
python tools/render/render_assets.py --id CODE-26
python tools/render/qa_browser.py --id CODE-26
python tools/validate_delivery.py --id CODE-26
```
Tool versions: Windows-11-10.0.26200-SP0; Python 3.14.0; ffmpeg version 6.0-essentials_build-www.gyan.dev Copyright (c) 2000-2023 the FFmpeg developers; CairoSVG 2.9.1; Pillow 12.3.0; Playwright 1.63.0 with Chromium 153.0.8010.12. No installs, no network, no font files distributed. Proof at 720p: proofs/poster-720.png.

## Remaining decisions
No assigned claim gate. Release approval comes from the review deck; produced is not release-approved.

## Asset-specific notes
- Authored teaching example in classic VB4 style with Option Explicit off; not an excerpt of Program.vb.
- The ticket's header comment line is carried by the card header ("Visual Basic 4 · Option Explicit off"); the two code lines are the exact ticket copy.
- Callout enters from the right margin and stops at the end of line 1; no annotation crosses code text.
- Discrete deterministic step states: typing 1–2.35 s, callout 2.5–2.9 s, hold to 6 s (loop-safe; last state is the poster).
