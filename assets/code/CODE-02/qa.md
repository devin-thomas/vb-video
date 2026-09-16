# CODE-02 — Production QA (revision 2, 2026-09-16)

**Production:** produced. **Release:** unreviewed (revision 2 awaits the producer's look at the new exports; the first cut's approval does not carry over).

## What changed in revision 2
Devin's review note 12: in the animated `highlighted` variant the annotation arrows crossed the code text on their way to `Dim`. Every arrow is gone. Each focus state now has:

- a row highlight bar behind the focused line(s) that starts at the panel's left edge and **stops short of the right margin** at a 5 px gold edge;
- the token box on the focus token, as before;
- the label in the **right margin**, right-aligned at x = 1770, beyond the bar's edge: `One card. Two fields.`, `Rank → comparison`, `Suit → printed name` (each with a short leader from the bar edge to the label, entirely inside the margin) and, for `Dim`, the source's "Dimension?" thought bubble (rounded outline plus two trailing dots), also entirely inside the margin.

The five timeline states and their times (0, 2, 3.5, 5.0, 6.5 s; 10 s total, 30 fps) are unchanged from the approved first cut, as is the excerpt (Program.vb lines 15–18) and the poster choice (the `Rank As Integer` state). `src/excerpt.vb` is unchanged.

## Delivered
Each media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. All exports were re-rendered on 2026-09-16: `exports/preview.mp4`, `exports/poster.png`, `exports/clean.png`, `exports/highlighted.png`, `exports/keyframes/{start,middle,end}.png`, `exports/contact-sheet.png`, `proofs/poster-720.png`, and `proofs/gallery.jpg` (refreshed from the new poster so no thumbnail of the old arrows remains).

## Checks actually performed
- **Excerpt:** `src/excerpt.vb` equals `sources/Program.vb` lines 15–18 line for line (checked with Python before finishing; the validator's `literal-program-excerpt` check repeats it).
- **Render:** `python tools/render/render_assets.py --id CODE-02` (CairoSVG 2.9.1, Pillow 12.3.0, ffmpeg 6.0) asserted 1920 × 1080 for every PNG and H.264 / 30 fps / yuv420p / 10.000 s / 300 frames for preview.mp4; probe in `evidence/render-tests.json`. Keyframes: `start.png` is byte-identical to `clean.png`, `end.png` to `highlighted.png`.
- **Browser:** `src/index.html` loaded in Playwright 1.63.0's Chromium (in-memory, offline): no network request; seeking to 5.3 s, then 10 s, then 0, then 5.3 s again gives identical SVG; `renderAt(t)` returns the authored state at each of the five start times; all 256 text boxes across the 8 SVG files (5 states, 2 variants, poster) are inside the canvas.
- **Annotation/code overlap:** in every one of the 8 SVG files, the bounding box of every gold annotation element (labels, leaders, bubble, dots, bar edges: 22 elements) was tested against every monospace code text element inside the panel: **0 overlaps** (`evidence/browser-tests.json`, `annotation_overlap_check`).
- **Manual inspection, full size (1920 × 1080):** `poster.png`, `clean.png`, `highlighted.png`, and six frames extracted from `preview.mp4` with ffmpeg at 1.0 s (clean), 2.5 s (Structure Card), 4.0 s (Rank), 5.5 s (Suit), 7.0 s and 9.9 s (Dim). Every state was seen: no annotation touches or crosses code text; bars end at the gold edge with clear dark panel between the edge and the label.
- **Manual inspection, 720p:** 1280 × 720 copies of `poster.png`, `clean.png` and `highlighted.png` viewed; labels, the bubble and the 46 px code remain legible.
- No smart quotes, truncation, or wrong VB token colours seen; keywords blue, identifiers white, as in the first cut.

## Reproduction
From the repository root on Windows: `set CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` then `python tools/render/render_assets.py --id CODE-02`. The revision-2 SVG states in `src/` are the editable sources (authored with `tools/render/studio.py` primitives from a worker script; `src/build.json` and `src/timeline.json` carry the timing). **Do not run `python tools/render/build_assets.py --id CODE-02`:** the shared authoring script still encodes the first cut's arrow annotations for CODE-02 and would overwrite this revision (see review questions).

Toolchain: Python 3.14.0; CairoSVG 2.9.1 with MSYS2 UCRT64 Cairo; Pillow 12.3.0; ffmpeg 6.0-essentials_build (gyan.dev); Playwright 1.63.0 (Chromium build recorded in `evidence/browser-tests.json` and delivery.json). No installs, no network, no font files distributed.

## Remaining decisions
- Assigned gate R03 was approved by the producer on 2026-09-15 (`evidence/claim-checks.json`); revision 2 changes only the annotation layer, not the source or any claim. The release decision for the new exports is the producer's.
- Review question for the producer: `tools/render/build_assets.py` (`code_svg`, the `CODE-02` branch) still draws the arrow annotation. A future batch rebuild would regress this revision unless that branch is updated to the bar-plus-margin-label layout; tools/ is outside this ticket's write paths.

No narration sync, sound design, final video assembly, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- Exact source text, separately stored. Soft visual wraps do not change source line breaks.
- Literal modern VB.NET source illustration; not a live IDE or VB4 capture.
- All focus targets have individually timed holds.
- Revision 2 (2026-09-16, review note 12): arrows removed; row bar plus right-margin label/bubble; nothing crosses code text in any state.
