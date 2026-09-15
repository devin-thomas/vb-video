# CODE-17 — Production QA

**Production:** produced. **Release:** blocked.

## Delivered
Each required media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. Existing outputs are real rendered media, not placeholder filenames. Independent variants belong to this ticket. The original source brief and code remain unchanged.

## Checks actually performed
- Rasterization and PNG dimensions checked at 1920 × 1080. Motion files checked with ffprobe for H.264, 30 fps, yuv420p, frame count and expected duration; per-file results are retained. Support-only OPS-01 is not a motion asset.
- HTML/SVG content was loaded in installed Chromium, with every source/variant scene checked for out-of-canvas text. Nonlinear forward/backward seeking was compared for identical SVG output. Remote requests were monitored; none were used. This is not a full text-overlap or semantic-proof system.
- The 25 literal Program.vb excerpts are checked against their canonical source ranges by the supplied validator. Code highlighting does not alter source files. Code line-wrap arrows are display markers, not inserted VB syntax.
- Visual review: Poster contact-sheet review. All 71 posters inspected in eight 1920-pixel-wide review sheets, each poster at 640 × 360. No obvious title clipping or composition defect remained at overview size. This does not certify every full-resolution motion frame.
- The source-based War and shuffle fixtures are deterministic teaching examples, not recorded program execution. Source/fixture checks are in the batch's review reports.

## Reproduction
`python shared/render_assets.py --id CODE-17` from the package root for media assets. For OPS-01, use `python shared/finish_delivery.py --ops-only`. Read shared/REBUILD.md first. Tool versions: assets/OPS-01/exports/capabilities.json.

## Remaining decisions
Assigned gates: R04, R05. See evidence/claim-checks.json and docs/EDITORIAL_REGISTER.md.

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- Exact source text, separately stored. Soft visual wraps do not change source line breaks.
- Literal modern VB.NET source illustration; not a live IDE or VB4 capture.
- All focus targets have individually timed holds.
