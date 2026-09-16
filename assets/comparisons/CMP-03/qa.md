# CMP-03 — Production QA (revision 2)

**Production:** produced. **Release:** unreviewed (revision 2 awaits the producer's look at the new exports).

## What changed in revision 2 (Devin's cut notes 13 and 15)
- Both columns are now an authored teaching example whose counter is `i`: `for (int i = 2; i <= 14; i++) { ... }` and `For i = 2 To 14 ... Next i`. The card is labelled as a teaching example on screen (footer) and in delivery.json/provenance.json; it is not a Program.vb excerpt. Loop bounds 2 and 14 (inclusive) are kept.
- Left header is `C / C++ / C# / Java`.
- Kind is motion (9 s, 30 fps, 270 frames). The card opens as the `i` example, shows the token-focus overlay, then on the VB side `i` morphs in place into `Rank` on both the `For` and `Next` lines, and the real-code state holds to the end with the margin label "in the real program the counter is called Rank" and the source line `Program.vb lines 104–110 (body lines 105–109 elided as ...)`.
- New outputs: `exports/preview.mp4`, `exports/transform.png` (+ `src/variant-transform.svg`), `exports/keyframes/{start,middle,end}.png`, `src/excerpt.vb`, `src/compose.py`. `comparison` (the `i` state) and `token-focus` are kept.

## Timeline (src/timeline.json, src/build.json)
| time | state |
|---|---|
| 0.0–2.5 s | teaching example, `i` on both sides (= `comparison`) |
| 2.5–4.5 s | focus overlay on `i <= 14` and `2 To 14` (= `token-focus`) |
| 4.5–4.9 s | 12 eased one-frame steps: `i` fades out, `Rank` fades in at the same x, the rest of the line slides right, the focus box grows from one to four characters |
| 4.9–5.4 s | real loop, `Rank` highlighted on both lines, no label yet |
| 5.4–9.0 s | margin label and source line appear; held to the end (= `transform`, also the poster) |

## Source anchors
- Teaching example: agent-authored (recorded in evidence/provenance.json `authored_example`). Not compiled or run in any language.
- Real loop: `sources/Program.vb` lines 104–110 (`For Rank = 2 To 14` … `Next Rank`, in BuildDeck). `src/excerpt.vb` is those seven lines byte for byte (LF); `War/Program.vb` has the same lines at the same numbers (CRLF). compose.py asserts both and asserts that the on-screen `For`/`Next` lines equal lines 104 and 110 with the common eight-space indent removed. Lines 105–109 are elided as `...` on screen.
- The revision-2 ticket text cites "lines 244–255" for this loop. Those lines are the `If Card1.Rank > Card2.Rank` round-resolution block, not a `For` loop; the only `For Rank = 2 To 14 ... Next Rank` in Program.vb is 104–110. The asset uses 104–110 and this is raised as a review question.

## Checks actually performed
- `python assets/comparisons/CMP-03/src/compose.py` authored 16 SVG states (16 frames), three variants, the poster, index.html, timeline.json, build.json, excerpt.vb and the evidence files; its assertions on the Program.vb lines passed.
- `python tools/render/render_assets.py --id CMP-03`: PNGs at 1920 × 1080; preview.mp4 probed by the renderer and again by hand with ffprobe: h264, 1920 × 1080, 30/1, yuv420p, 270 frames, 9.000 s (evidence/render-tests.json).
- `python tools/render/qa_browser.py --id CMP-03`: installed Chromium 153, in-memory HTML, offline, deterministic seek, 20 SVG files, 658 text boxes, none out of canvas, no errors (evidence/browser-tests.json).
- `python tools/render/finish_delivery.py --id CMP-03`: inventory and hashes. It also rewrote docs/tickets/CMP-03.md (which would have dropped the Revision 2 section), review/browser-summary.json and review/production-index.json; those three files were restored with git because they are outside this ticket's write paths. The producer's index sync will refresh them.
- `python tools/validate_delivery.py --id CMP-03`: see the completion report; expected ok.
- Manual visual review at full size (1920 × 1080), viewed by the worker: exports/comparison.png, exports/token-focus.png, exports/transform.png (= poster), exports/contact-sheet.png, and frames extracted from exports/preview.mp4 with ffmpeg at 0.5, 3.0, 4.5, 4.633, 4.767, 4.9, 5.2 and 8.966 s. At 1280 × 720 (ffmpeg scale): comparison, token-focus, transform and the 4.7 s morph frame. Result: no clipped code or headers; `C / C++ / C# / Java` fits its panel with room; punctuation (`;`, `<=`, `++`, `{`, `}`, `...`) legible at 720p; the label and source line sit below the code inside the VB panel and the arrow rises through empty panel space to the `Rank` of `Next Rank` without crossing any text; mid-morph frames read as a crossfade of `i` into `Rank` with the tail of the line sliding right. Not certified: every one of the 270 frames individually (the 12 morph states were checked at three sample points), narration sync, and final assembly.
- proofs/gallery.jpg (640 × 360 JPEG of the poster) and proofs/poster-720.png were regenerated from the revision-2 poster; they are proofs, not deliverable exports.

## Reproduction
From the repository root, with `CAIROCFFI_DLL_DIRECTORIES` pointing at the Cairo DLL folder and fc-match on PATH:
```
python assets/comparisons/CMP-03/src/compose.py
python tools/render/render_assets.py --id CMP-03
python tools/render/qa_browser.py --id CMP-03
python tools/render/finish_delivery.py --id CMP-03
python tools/validate_delivery.py --id CMP-03
```
Do not run `tools/render/build_assets.py --id CMP-03`: it regenerates the revision-1 still (`rank`/`Rank`, header `C#`) and discards these scenes. Tool versions: the toolchain in delivery.json (Windows 11, Python 3.14.0, CairoSVG 2.9.1, Pillow 12.3.0, ffmpeg 6.0, Playwright 1.63.0 with Chromium 153). Font metrics come from the locally installed Liberation Sans and DejaVu Sans Mono; the mono advance measured 22.0 px at 36 px here versus 21.67 px on the original Linux batch machine, a deliberate reflow accepted by the template contract. Rendered media does not depend on viewer fonts.

## Review questions for the producer
1. Line range: the ticket says 244–255; the loop is at 104–110. The asset shows 104–110. Confirm, or say what 244–255 was meant to point at.
2. The transform keeps the `...` excerpt form (lines 104 and 110 shown, 105–109 elided) rather than expanding the nested `For SuitIndex` body. The full seven lines at the shared 36 px code size would need soft wraps inside the 810 px panel. If Devin wants the whole real loop on screen, that is a layout change to decide, not a render fix.
3. The motion includes the original token-focus beat (2.5–4.5 s) before the morph. If the editor only needs example → morph → real code, the `comparison` still plus the 4.5–9.0 s span of preview.mp4 cover it; a separate cutdown was not authored.
4. The end-state footer reads "Syntax comparison · the VB column now shows the real loop from Program.vb" and the source line names the elided lines. Both are on-screen copy the producer may want shorter.

## Remaining decisions
No assigned claim gate. No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.
