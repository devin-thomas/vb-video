# DIA-13 — Production QA

**Production:** produced. **Release:** blocked.

## Delivered
Each required media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. Existing outputs are real rendered media, not placeholder filenames. Independent variants belong to this ticket. The original source brief and code remain unchanged.

## Checks actually performed
- Rasterization and PNG dimensions checked at 1920 × 1080. Motion files checked with ffprobe for H.264, 30 fps, yuv420p, frame count and expected duration; per-file results are retained. Support-only OPS-01 is not a motion asset.
- HTML/SVG content was loaded in installed Chromium, with every source/variant scene checked for out-of-canvas text. Nonlinear forward/backward seeking was compared for identical SVG output. Remote requests were monitored; none were used. This is not a full text-overlap or semantic-proof system.
- The 25 literal Program.vb excerpts are checked against their canonical source ranges by the supplied validator. Code highlighting does not alter source files. Code line-wrap arrows are display markers, not inserted VB syntax.
- Visual review: Full-resolution export and 720p proof. Viewed exports/overview.png (also the poster) and proofs/poster-720.png after the layout fix. Node labels, the dashed script-sequence arrows and the three-entry legend are readable at 720p, and all text sits within x = 120–1800. The first render put the examples note and the last legend label past x = 1800; that was fixed and re-rendered before this review.
- The source-based War and shuffle fixtures are deterministic teaching examples, not recorded program execution. Source/fixture checks are in the batch's review reports.

## Reproduction
From the repository root, `python tools/render/build_assets.py --id DIA-13` rebuilds the sources (and resets the ticket's state); `render_assets.py`, `qa_browser.py` and `finish_delivery.py` in tools/render, each with `--id DIA-13`, then render, check and finish it. For OPS-01, use `python tools/render/finish_delivery.py --ops-only`. Read tools/render/REBUILD.md first. Tool versions: the toolchain in delivery.json.

## Remaining decisions
Assigned gates: R13. See evidence/claim-checks.json and docs/EDITORIAL_REGISTER.md.

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- Node labels follow the ticket copy; the script’s visual cue says “.NET WinForms” (SCRIPT.md:711).
- The four arrows are the script’s draft sequence, kept in their own SVG layer (draft-script-sequence) and drawn only in the unverified style. src/edges.json lists each edge; none has evidence or an approved label, so R13 stays open.
- The legend defines direct-lineage and shared-ideas edges for the editorial pass; no edge uses them yet.
- React, SwiftUI and Flutter appear only as the script’s examples. No node implies VB language or runtime inheritance. The optional focus overlay was not made.
