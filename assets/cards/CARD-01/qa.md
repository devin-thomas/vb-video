# CARD-01 — Production QA

**Production:** produced. **Release:** unreviewed (revision 2, 2026-09-16; the 2026-09-15 approval covered the 1.0.0 faces and does not carry over).

## Revision 2 — card faces re-rendered (win95-workbench-1.1.0)

OPS-01 revision 2 redrew the shared card faces as regular playing cards (Devin’s note 17: every 1.0.0 face drew one centre pip, so every rank read as an ace). This asset carried its own copies of the 1.0.0 faces, inlined in every scene SVG, in `src/index.html` and in the exports, so it was re-rendered on 2026-09-16. Nothing but the card faces changed.

- Card art source: the faces are not referenced from `assets/shared/cards/`; they were emitted inline by `title_card` in tools/render/build_assets.py calling `studio.card()` when the scenes were authored.
- Replacement: 12 face groups in 6 `src/*.svg` files (108 px (small mode)) were replaced by the win95-workbench-1.1.0 `card()` output from `tools/render/studio.py` at the same identity, position, size, opacity and accent. Each group’s parameters were recovered from the SVG and proved exact by re-emitting the 1.0.0 group byte for byte before it was replaced; the remainder of every file is untouched. Face-down backs are drawn identically by both versions. The scene table inlined in `src/index.html` was rebuilt from the edited SVGs after checking that the old table matched the old files; `timeline.json`, `build.json`, text, layout and file names are unchanged. `build_assets.py` was not run (it would reset this ticket and rewrite other assets).
- Exports: `python tools/render/render_assets.py --id CARD-01` (the asset’s `src/build.json` driver) re-rendered poster.png, title-hold.png, ok-click.png, keyframes/start|middle|end.png, preview.mp4 (7 s, 210 frames), contact-sheet.png and proofs/poster-720.png; it also rewrote `evidence/render-tests.json`.
- Browser check: the offline in-memory Chromium check of `tools/render/qa_browser.py` was re-run through a scratch copy that writes only this asset’s `evidence/browser-tests.json` (the original also rewrites `review/browser-summary.json`, outside this ticket): 7 SVG files, 66 text boxes, no out-of-canvas text, deterministic seek, no network request.
- Manual visual review with the poster at 1920 × 1080 and 1280 wide plus one extracted frame of each MP4 at both sizes: The title dialog’s A♠ and 4♥ at 108 px in the poster, title-hold.png, ok-click.png and the frame extracted from preview.mp4 at 3 s: the 4♥ shows its rank and four corner pips, the A♠ its rank with the large pip partly covered by the overlapping 4♥ exactly as before; no rotated corner at this size. Dialog, title text, OK button and cursor states are unchanged; the blank first and last frames are byte-identical to the previous render.
- `python tools/validate_delivery.py --id CARD-01` was run after delivery.json was rebuilt; the result is in the completion report. Tool versions for this revision: the toolchain in delivery.json.

## Delivered
Each required media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. Existing outputs are real rendered media, not placeholder filenames. Independent variants belong to this ticket. The original source brief and code remain unchanged.

## Checks actually performed
- Rasterization and PNG dimensions checked at 1920 × 1080. Motion files checked with ffprobe for H.264, 30 fps, yuv420p, frame count and expected duration; per-file results are retained. Support-only OPS-01 is not a motion asset.
- HTML/SVG content was loaded in installed Chromium, with every source/variant scene checked for out-of-canvas text. Nonlinear forward/backward seeking was compared for identical SVG output. Remote requests were monitored; none were used. This is not a full text-overlap or semantic-proof system.
- The 25 literal Program.vb excerpts are checked against their canonical source ranges by the supplied validator. Code highlighting does not alter source files. Code line-wrap arrows are display markers, not inserted VB syntax.
- Visual review: Standalone 1920 × 1080 poster inspection plus overview sheet. Reviewed the full-resolution still and its appearance in the overview. Type, negative space, card legibility, and annotations inspected. CODE-02 pointer, code soft wrapping, small-card details, and saved-top labeling were corrected during this pass. Not all temporal frames received independent manual review.
- The source-based War and shuffle fixtures are deterministic teaching examples, not recorded program execution. Source/fixture checks are in the batch's review reports.

## Reproduction
`python tools/render/render_assets.py --id CARD-01` from the package root for media assets. For OPS-01, use `python tools/render/finish_delivery.py --ops-only`. Read tools/render/REBUILD.md first. Tool versions: assets/ops/OPS-01/exports/capabilities.json.

## Remaining decisions
No assigned claim gate; producer publication approval is still not assumed.

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- Local timing and composition are authored production choices.
