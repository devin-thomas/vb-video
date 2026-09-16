# DIA-04 — Production QA (revision 2, 2026-09-16)

**Production:** produced. **Release:** unreviewed (revision 2 replaces the approved revision-1 exports; the producer has not yet seen the new ones).

## What changed in revision 2
Devin's cut note 16 (review/cut-notes-2026-09-16.md): the diagram did not communicate copy versus reference. It is replaced by a code-driven demonstration. Left column `Sub Bump(ByVal n As Integer)` / `n = n + 1`, called with `x = 5`, and x is still 5 afterwards; middle column `Sub Bump(ByRef n As Integer)`, same call, x is now 6; right column "C++" with `void bump(int n)` versus `void bump(int& n)` and the same outcome. Value boxes beside the code update as the call runs: the ByVal copy appears, becomes 6 and is struck through as discarded; the ByRef `n` is a dashed tag whose arrow points back at x, and x itself becomes 6. Annotations (running-line marker, copy arrow, back-pointing arrow, captions) sit in the margins and the value area, never over code text. The subtitle in every state reads "One Integer, one Sub: a copy of the value versus the variable itself." (producer's wording, 2026-09-16).

**Caveat, kept here and in delivery.json rather than on screen:** the Bump / bump example is an authored teaching example, not supplied code. It shows one Integer only; nothing on screen claims or depicts what ByVal does with an array (no automatic deep copy is drawn), and no historical default-passing statement appears.

Generator: `src/make_scenes.py` (reads tools/render/studio.py for the shared colours, fonts and code colouring; writes the six scene SVGs, the three variant SVGs, scene.svg, build.json, timeline.json and index.html).

## Delivered
Each required media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. Outputs are real rendered media. Motion: exports/preview.mp4, 10 s, 300 frames, with keyframes start/middle/end. Stills: exports/poster.png (the held end state) and the named variants exports/byval.png, exports/byref.png, exports/cpp.png (each a full-canvas cut-in of one demonstration at its end state, with a separate SVG in src/). Timing (src/timeline.json and build.json): states at 0, 1.5, 3, 4.5, 6 and 7.5 s; the result holds from 7.5 s to 10 s.

## Checks actually performed (this machine, 2026-09-16)
- Render: `python tools/render/render_assets.py --id DIA-04` (CairoSVG 2.9.1 through MSYS2 Cairo, Pillow 12.3.0, ffmpeg 6.0). Every PNG is 1920 × 1080. ffprobe on preview.mp4: h264, 1920 × 1080, 30/1, yuv420p, 300 frames, 10.000 s. Record: evidence/render-tests.json.
- Offline HTML: the same checks as tools/render/qa_browser.py, run as a scratch replica restricted to this ticket (the shared script also rewrites review/browser-summary.json, outside this ticket's write paths). Playwright 1.63.0 with its bundled Chromium 153.0.8010.12, in-memory load: no network request; renderAt at 0.53 × duration identical after seeking to the end and back (deterministic); ten frame-boundary and out-of-range seeks (0, 1.5, 3, 4.5, 6, 7.5, 9.99, 1.49, 12, −1) map to the expected authored state; 10 SVG files, 1063 text boxes, none outside the canvas. Record: evidence/browser-tests.json.
- Authored example executed: a VB.NET harness (.NET SDK 10.0.303, restore against an empty local feed, no download) prints `x is now 5` for ByVal and `x is now 6` for ByRef; a C++ harness (g++ 16.2.0) prints the same for `int n` and `int& n`. Exact programs and output: evidence/harness-runs.md.
- Manual visual review at full size (1920 × 1080) with the Read tool: exports/poster.png, exports/byval.png, exports/byref.png, exports/cpp.png, and seven frames extracted from preview.mp4 at 0.5, 2.0, 3.5, 5.0, 6.5, 8.0 and 9.9 s. At 1280 wide: the poster, the three variants and the same seven frames; plus proofs/poster-720.png. Findings: the digits 5 and 6 are legible at both sizes; the ByVal/ByRef difference reads without narration (struck-through copy and "x is still 5" against the back-pointing arrow, green 6 and "x is now 6"); ByVal and ByRef labels are visible in every state; no annotation crosses code text; nothing is clipped. Two earlier renders had defects (the C++ column overflowing its panel; the "same variable" caption touching the tag; a step note running into "discarded") that were fixed before this record was written.
- Content checks: no array is drawn or mentioned as copied; the Integer values are labelled; the only source-derived text is the ByVal/ByRef keywords and the `Integer` type; `Bump(x)` follows the call style of Program.vb.
- Subtitle change (producer, 2026-09-16): the on-screen caveat was replaced by "One Integer, one Sub: a copy of the value versus the variable itself." in every state and variant; everything re-rendered, the browser check re-run, and the poster re-inspected at full size (subtitle fits on one line under the title, unchanged layout below it).

Not certified: narration sync, sound, final assembly, full editorial clearance. Produced is different from release-approved.

## Reproduction
From the repository root, with `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` set (Windows):

```sh
python assets/diagrams/DIA-04/src/make_scenes.py
python tools/render/render_assets.py --id DIA-04
python tools/validate_delivery.py --id DIA-04
```

Do not run tools/render/build_assets.py for this ticket: it would regenerate the revision-1 diagram from tools/render/diagrams.py over these sources. Tool versions: the toolchain in delivery.json.

## Remaining decisions
Assigned gate: R04a, status review_requested in evidence/claim-checks.json. The Integer example's behaviour is verified by execution; what remains is the producer's look at the new exports (the 2026-09-15 approval covered the old diagram).

Review questions for the producer:
1. The compact C++ column is a fragment (shared `int x = 5;` above the two functions, `bump(x);` under each); the cpp variant shows each version as a complete, correctly ordered listing. Fine as a supporting column, or should the compact column drop code and show only signatures and results?
2. The call is written `Bump(x)`, as Program.vb calls its Subs. Classic VB also accepts `Call Bump(x)`; `Bump (x)` with a space would force ByVal in classic VB and is deliberately not used.
3. The harness is VB.NET 10, not 1995 Visual Basic. For an Integer parameter the ByVal/ByRef keywords mean the same thing, but this is not historical evidence and the canvas makes no historical claim.
