# DIA-15 — Production QA

**Production:** produced. **Release:** unreviewed.

## Delivered
Every media, source and evidence file is enumerated by byte count and SHA-256 in delivery.json. All outputs are real rendered media from this ticket's own sources; nothing is a placeholder. The narration, `sources/`, `War/SCRIPT.md`, `manifest.json`, `tools/` and `assets/shared/` are untouched.

| Variant | File | Duration | Key second | What it is |
|---|---|---|---|---|
| riffle | exports/riffle.mp4 | 12 s | 2.0 | squared 0–1 s, split 1–2 s, riffle interleave 2–5 s (key moment: first cards drop at 2.0 s), square up 5–6 s, hold 6–12 s |
| loop | exports/loop.mp4 | 4 s | 0.1 | halves apart 0–0.1 s, interleave 0.1–2.8 s, square up 2.8–3.4 s, split 3.4–3.9 s, apart 3.9–4 s; frame 0 and frame 119 are the same authored state |

exports/preview.mp4 is byte-identical to exports/riffle.mp4 (riffle is the `[0, 12]` cut of the main timeline). exports/poster.png is the squared deck (the 0–1 s and 6–12 s state) for the timeline builder's hold. exports/riffle.png (main timeline at 2.5 s) and exports/loop.png (loop at 1.3 s) are the variant stills.

## How it was made
- `src/build_riffle.py build` computes every card placement as a pure function of time (seeded LCG for the drop order and pile jitter; no randomness at render time) and writes one SVG per distinct 1/30 s state: 139 main scene files over 140 state changes, 111 loop files. Consecutive identical states share a file, which is why `renderAt(1.0)` and `renderAt(6.0)` both resolve to `scene-0000.svg` (the split at u = 0 and the squared deck after the shuffle have identical geometry).
- Card art: `tools/render/studio.py` `card()` at win95-workbench-1.1.0 (revised regular faces), drawn at 240 × 336 px. The back is defined once per scene and placed with `<use>`; flashed faces are inlined.
- `python tools/render/render_assets.py --id DIA-15` rasterised the main timeline (CairoSVG 2.9.1, 1920 × 1080) and encoded preview.mp4 and the riffle cut (ffmpeg, libx264 crf 18, yuv420p, 30 fps), plus poster.png, riffle.png, loop.png, keyframes/, contact-sheet.png, proofs/poster-720.png and evidence/render-tests.json.
- `src/build_riffle.py encode-loop` rasterised the loop's 111 files and encoded exports/loop.mp4 with the same CairoSVG + ffmpeg recipe as `render_assets.encode()` (the loop is not a sub-range of the main timeline, so the shared renderer's `cuts` mechanism could not produce it); probe in evidence/loop-encode.json.

## Checks actually performed
- ffprobe on all three MP4s: h264, 1920 × 1080, yuv420p, 30/1; preview.mp4 and riffle.mp4 360 frames / 12.000 s; loop.mp4 120 frames / 4.000 s. PNG exports are 1920 × 1080 (also asserted by the renderer).
- Loop seam: the generator asserts the first and last authored loop frames are the same file; the first and last decoded frames of loop.mp4 (n = 0 and n = 119) differ only by codec noise (mean absolute difference 0.46 / 255 per channel), and `__ASSET__.variants.loop.renderAt(4)` wraps to `loop-0000.svg`.
- Browser (Playwright Chromium 153, in-memory HTML, no network): seeking 3.2 s → 12 s → loop 1.7 s → 0 s → 3.2 s reproduced identical DOM; 24 text boxes on five states all inside the canvas; evidence/browser-tests.json. `tools/render/qa_browser.py` was not run because it also writes `review/browser-summary.json` outside this ticket's owned paths.
- Manual visual review at full 1920 × 1080 (Read tool) of exports/poster.png and frames decoded from riffle.mp4 at 0.5 s (squared deck), 1.6 s (halves sliding apart and tilting), 2.47 s (8♠ face flashing mid-drop), 3.0 s and 4.2 s (mid-interleave: two arcs of cards dropping from the halves into a visibly ragged centre pile whose cards alternate tilt left/right), 5.9 s (squared). Same four checkpoints reviewed at 1280 × 720, where the two streams and the growing pile still read clearly; the interleave is visible as the pile's alternating tilts, not only as motion. Loop frames 0 and 119 viewed side by side at full size: identical composition (two tilted halves). Not every one of the 360 + 120 frames received independent manual review.

## Reproduction
From the package root, with `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` set as an environment variable:

```sh
python assets/diagrams/DIA-15/src/build_riffle.py build
python tools/render/render_assets.py --id DIA-15
python assets/diagrams/DIA-15/src/build_riffle.py encode-loop
python tools/validate_delivery.py --id DIA-15
```

Tool versions: Windows 11 Pro 10.0.26200; Python 3.14.0; CairoSVG 2.9.1 (MSYS2 ucrt64 Cairo, fontconfig fc-match); Pillow 12.3.0; ffmpeg/ffprobe 6.0-essentials_build (gyan.dev); Playwright Chromium 153.0.8010.12 for the browser check only. Fonts at render: Liberation Sans regular/bold from C:/WINDOWS/fonts (flashed faces only). No network, no installs, no font files distributed.

## Remaining decisions
No editorial gates are assigned to this ticket (`release_gates: []`). Rights are settled by Devin's standing R14 ruling; the graphics are original vectors.

Review questions for the deck (taste, not evidence):
1. The riffle is a stylised top-down "two streams into a pile" reading rather than the side-on thumbs-and-bridge view. It was chosen so the shared card backs stay recognisable at 720p; a side-on riffle would show only card edges.
2. Four faces flash per riffle (8♠, 6♠, Q♠, 6♥ in the main timeline). If the flashes read as a mistake rather than a flourish, `FLASH_MAIN`/`FLASH_LOOP` in src/build_riffle.py can be emptied and the asset re-rendered in about a minute.

No narration sync, sound design or final assembly is certified here. Produced is intentionally different from release-approved.
