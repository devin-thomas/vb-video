# DIA-09 — Production QA

**Production:** produced. **Release:** unreviewed (revision 2, 2026-09-16; the 2026-09-15 approval covered the 1.0.0 faces and does not carry over).

## Revision 2 — card faces re-rendered (win95-workbench-1.1.0)

OPS-01 revision 2 redrew the shared card faces as regular playing cards (Devin’s note 17: every 1.0.0 face drew one centre pip, so every rank read as an ace). This asset carried its own copies of the 1.0.0 faces, inlined in every scene SVG, in `src/index.html` and in the exports, so it was re-rendered on 2026-09-16. Nothing but the card faces changed.

- Card art source: the faces are not referenced from `assets/shared/cards/`; they were emitted inline by `war_board` in tools/render/diagrams.py calling `studio.card()` when the scenes were authored.
- Replacement: 75 face groups in 23 `src/*.svg` files (78 px (small mode; backs unchanged)) were replaced by the win95-workbench-1.1.0 `card()` output from `tools/render/studio.py` at the same identity, position, size, opacity and accent. Each group’s parameters were recovered from the SVG and proved exact by re-emitting the 1.0.0 group byte for byte before it was replaced; the remainder of every file is untouched. Face-down backs are drawn identically by both versions. The scene table inlined in `src/index.html` was rebuilt from the edited SVGs after checking that the old table matched the old files; `timeline.json`, `build.json`, text, layout and file names are unchanged. `build_assets.py` was not run (it would reset this ticket and rewrite other assets).
- Exports: `python tools/render/render_assets.py --id DIA-09` (the asset’s `src/build.json` driver) re-rendered poster.png, 2-10-18-poster.png, double-war-growth.png, keyframes/start|middle|end.png, preview.mp4 (15 s, 450 frames), contact-sheet.png and proofs/poster-720.png; it also rewrote `evidence/render-tests.json`.
- Browser check: the offline in-memory Chromium check of `tools/render/qa_browser.py` was re-run through a scratch copy that writes only this asset’s `evidence/browser-tests.json` (the original also rewrites `review/browser-summary.json`, outside this ticket): 26 SVG files, 709 text boxes, no out-of-canvas text, deterministic seek, no network request.
- Manual visual review with the poster at 1920 × 1080 and 1280 wide plus one extracted frame of each MP4 at both sizes: The poster (pot growth 2 → 10 → 18) has no cards. The frame extracted from preview.mp4 at 8 s (double war, pot 16) shows the face-up 4♠, 2♠, 4♦ and 2♥ at 78 px in small mode: top-left rank, four corner pips or two end pips matching the rank, no rotated corner, as the primitive specifies under 110 px; the face-down backs, the player stacks and the counts are unchanged. At 1280 wide the ranks are readable and the pips are visible as dots.
- `python tools/validate_delivery.py --id DIA-09` was run after delivery.json was rebuilt; the result is in the completion report. Tool versions for this revision: the toolchain in delivery.json.

## Delivered
Each required media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. Existing outputs are real rendered media, not placeholder filenames. Independent variants belong to this ticket. The original source brief and code remain unchanged.

## Checks actually performed
- Rasterization and PNG dimensions checked at 1920 × 1080. Motion files checked with ffprobe for H.264, 30 fps, yuv420p, frame count and expected duration; per-file results are retained. Support-only OPS-01 is not a motion asset.
- HTML/SVG content was loaded in installed Chromium, with every source/variant scene checked for out-of-canvas text. Nonlinear forward/backward seeking was compared for identical SVG output. Remote requests were monitored; none were used. This is not a full text-overlap or semantic-proof system.
- The 25 literal Program.vb excerpts are checked against their canonical source ranges by the supplied validator. Code highlighting does not alter source files. Code line-wrap arrows are display markers, not inserted VB syntax.
- Visual review: Per-asset poster/variant/start-middle-end contact sheet plus overview. Inspected growth states and final 17 / 35 / 0 counts. Counters conserve 52; individual burn faces remain hidden. This is authored fixture animation, not observed output.
- The source-based War and shuffle fixtures are deterministic teaching examples, not recorded program execution. Source/fixture checks are in the batch's review reports.

## Reproduction
`python tools/render/render_assets.py --id DIA-09` from the package root for media assets. For OPS-01, use `python tools/render/finish_delivery.py --ops-only`. Read tools/render/REBUILD.md first. Tool versions: assets/ops/OPS-01/exports/capabilities.json.

## Remaining decisions
Assigned gates: R05, R07. See evidence/claim-checks.json and docs/EDITORIAL_REGISTER.md.

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- The double-war fixture produces live pot milestones 2, 8, 10, 16, 18 and final counts 17 / 35 / 0.
- 104 is allocation capacity in the supplied code, not the size of the physical deck. No 104-card graphic is used.
