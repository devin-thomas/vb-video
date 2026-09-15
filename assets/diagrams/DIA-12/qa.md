# DIA-12 — Production QA

**Production:** produced. **Release:** blocked.

## Delivered
Each required media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. Existing outputs are real rendered media, not placeholder filenames. Independent variants belong to this ticket. The original source brief and code remain unchanged.

## Checks actually performed
- Rasterization and PNG dimensions checked at 1920 × 1080. Motion files checked with ffprobe for H.264, 30 fps, yuv420p, frame count and expected duration; per-file results are retained. Support-only OPS-01 is not a motion asset.
- HTML/SVG content was loaded in installed Chromium, with every source/variant scene checked for out-of-canvas text. Nonlinear forward/backward seeking was compared for identical SVG output. Remote requests were monitored; none were used. This is not a full text-overlap or semantic-proof system.
- The 25 literal Program.vb excerpts are checked against their canonical source ranges by the supplied validator. Code highlighting does not alter source files. Code line-wrap arrows are display markers, not inserted VB syntax.
- Visual review: Full-resolution exports and 720p proof. Viewed exports/full-table.png, exports/gui-row-focus.png and proofs/poster-720.png. Five rows and both headings match the script table word for word and are readable at 720p. gui-row-focus outlines the GUI-builder row and dims the other four, which stay legible.
- The source-based War and shuffle fixtures are deterministic teaching examples, not recorded program execution. Source/fixture checks are in the batch's review reports.

## Reproduction
From the repository root, `python tools/render/build_assets.py --id DIA-12` rebuilds the sources (and resets the ticket's state); `render_assets.py`, `qa_browser.py` and `finish_delivery.py` in tools/render, each with `--id DIA-12`, then render, check and finish it. For OPS-01, use `python tools/render/finish_delivery.py --ops-only`. Read tools/render/REBUILD.md first. Tool versions: the toolchain in delivery.json.

## Remaining decisions
Assigned gates: R03, R09, R16. See evidence/claim-checks.json and docs/EDITORIAL_REGISTER.md.

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- All five rows and both column headings are the script’s draft table (SCRIPT.md:661–667), word for word; src/cells.json records each row’s line.
- These cells are draft copy, not verified facts. Console support, the ResEdit characterization and the runtime claim wait on R03, R09 and R16.
- Neutral styling: no scores, bars, icons or product screenshots. gui-row-focus dims the other four rows.
- The VB column describes classic VB4 as the script does; it is not presented as this project’s VB.NET console run.
