# CARD-01 — Production QA

**Production:** produced. **Release:** unreviewed.

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
