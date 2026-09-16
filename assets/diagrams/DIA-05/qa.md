# DIA-05 — Production QA (revision 2)

**Production:** produced. **Release:** unreviewed.

## Delivered
Each media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. All outputs are real rendered media from the checked-in SVG states; nothing is a placeholder. Revision 2 replaces the revision-1 exports with four independent, beat-accurate cutdowns plus the continuous preview, all on the shared win95-workbench-1.1.0 card faces.

| Cutdown | File | Duration | key_second | Key moment | Serves |
|---|---|---|---|---|---|
| live-slots | exports/live-slots.mp4 | 18 s | 0.0 | the array at rest, Count = 4 marking the live boundary (hold) | S08-B01, S08-B04 |
| append | exports/append.mp4 | 12 s | 1.0 | C (A♠) lands in slot 4, position Count; Count becomes 5 at 2.3 s | S08-B05 "drop it at position Count and increment" |
| draw-shift | exports/draw-shift.mp4 | 12 s | 1.2 | the first shift movement, H.Cards(0) = H.Cards(1); last change (DrawTopCard = Top) at 5.4 s | S08-B06 "take the card at position zero, then shift everything else forward" |
| cost | exports/cost.mp4 | 20 s | 1.2 | all 25 remaining cards start moving one slot forward at once; Count becomes 25 at 2.8 s | S08-B07 "every card in the hand moves one position" |

Each cutdown starts at its named moment and holds its end state to the end of the file. live-slots and cost are longer than the 12 s minimum because ASM-03's placement gives them all of S08-B01 (16.4 s) and 18.3 s of S08-B07. Posters: exports/<name>.png is each cutdown's hold state. The legacy stills 52-slot-overview.png, draw-and-shift.png and append-at-count.png (still required by manifest.json) are the same hold states under the revision-1 names. preview.mp4 (22.5 s) is the continuous version in narration order with shorter holds.

## Checks actually performed
- Rendering: `python assets/diagrams/DIA-05/src/author.py` wrote 120 scene states, 7 variant SVGs, build.json, timeline.json, index.html and brief.json; `python assets/diagrams/DIA-05/src/render.py` called tools/render/render_assets.py's `render()` (unchanged) for preview.mp4, poster, stills, keyframes, proofs and the contact sheet, then encoded the four cutdowns with the same `encode()` (30 fps, libx264, crf 18, yuv420p). ffprobe results for all five MP4s are in evidence/render-tests.json: 1920 × 1080, 30/1, yuv420p, durations 22.5 / 18 / 12 / 12 / 20 s.
- `python tools/render/qa_browser.py --id DIA-05`: installed Chromium 153.0.8010.12, in-memory HTML, 127 SVG files, 14,315 text boxes, none out of canvas, deterministic seeking, no network request (evidence/browser-tests.json). The script's project-wide review/browser-summary.json was restored afterwards; this ticket writes only inside its own folder.
- `python tools/validate_delivery.py --id DIA-05`: passed after delivery.json was written (see the completion report).
- Manual visual review by the worker: every cutdown's poster and two frames extracted from each MP4 with ffmpeg (the key moment and the end hold) were viewed at 1920 × 1080 and at 1280 × 720. Findings: the six-slot views read as real playing cards (corner index, pips, court marks) at both sizes; Count is a line between slots, never on a card; the copied-from slot keeps a faded duplicate and the final stale slot is faded, outside the boundary and labelled "stale"; exact code lines change with each state. In the cost view the 26 cards are 56 px wide: the rank stays legible at 720p, the pips reduce to dots, and the simultaneous slide of the whole row is unmistakable. No clipping, overlap or off-canvas text was found.
- Timing of the tweens (0.5–0.8 s moves at 15 authored states per second) was checked by stepping the extracted frames; motion is discrete state animation, as the shared contract describes.
- sources/ is byte-identical (nothing outside assets/diagrams/DIA-05/ was changed on the branch).

## Reproduction
From the repository root: `python assets/diagrams/DIA-05/src/author.py`, then `python assets/diagrams/DIA-05/src/render.py`, then `python tools/render/qa_browser.py --id DIA-05` (restore review/browser-summary.json afterwards if only this ticket is being refreshed). delivery.json for this revision was written by hand from `output_inventory()` and `capabilities()` in tools/render/finish_delivery.py: running `finish_delivery.py --id DIA-05` would rewrite the variant entries in the revision-1 shape and drop `key_second`, so re-add the cutdown entries if it is ever run. Tool versions: the toolchain in delivery.json (Windows, Python 3.14, CairoSVG with MSYS2 Cairo via CAIROCFFI_DLL_DIRECTORIES, ffmpeg, Playwright Chromium).

## Remaining decisions
No assigned claim gate. Producer publication approval is not assumed.

Authored choices to review: the demonstration follows narration order (append at index 4 before the draw shifts four cards) instead of the revision-1 order (draw first, append at 3); and the cost view uses a 26-card hand (the dealt hand size) whose last 22 cards are an authored fixture.

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- Copy semantics are shown literally: H.Cards(i - 1) = H.Cards(i) leaves a faded copy at i until it is overwritten; the last copy is stale storage beyond Count, never presented as a live card. The Count decrement happens after the loop, as in Program.vb.
- No card is ever drawn from the array end; "next to draw" stays at index 0 in every state.
- The 52-slot strip under the zoom row keeps the whole array in view, with the same Count boundary.
