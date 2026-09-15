# DIA-11 — Production QA

**Production:** produced. **Release:** blocked.

## Delivered
Each required media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. Existing outputs are real rendered media, not placeholder filenames. Independent variants belong to this ticket. The original source brief and code remain unchanged.

## Checks actually performed
- Rasterization and PNG dimensions checked at 1920 × 1080. Motion files checked with ffprobe for H.264, 30 fps, yuv420p, frame count and expected duration; per-file results are retained. Support-only OPS-01 is not a motion asset.
- HTML/SVG content was loaded in installed Chromium, with every source/variant scene checked for out-of-canvas text. Nonlinear forward/backward seeking was compared for identical SVG output. Remote requests were monitored; none were used. This is not a full text-overlap or semantic-proof system.
- The 25 literal Program.vb excerpts are checked against their canonical source ranges by the supplied validator. Code highlighting does not alter source files. Code line-wrap arrows are display markers, not inserted VB syntax.
- Visual review: Full-resolution export and 720p proof. Viewed exports/full-comparison.png (also the poster) at 1920 × 1080 and proofs/poster-720.png. All five rows and the four content columns are present and readable at 720p; the longest cell wraps to three lines inside its row. No text leaves the safe area. No price, market share, rating or logo appears.
- The source-based War and shuffle fixtures are deterministic teaching examples, not recorded program execution. Source/fixture checks are in the batch's review reports.

## Reproduction
From the repository root, `python tools/render/build_assets.py --id DIA-11` rebuilds the sources (and resets the ticket's state); `render_assets.py`, `qa_browser.py` and `finish_delivery.py` in tools/render, each with `--id DIA-11`, then render, check and finish it. For OPS-01, use `python tools/render/finish_delivery.py --ops-only`. Read tools/render/REBUILD.md first. Tool versions: the toolchain in delivery.json.

## Remaining decisions
Assigned gates: R11, R15. See evidence/claim-checks.json and docs/EDITORIAL_REGISTER.md.

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- Every cell is drafted from SCRIPT.md narration. src/cells.json gives each cell its line, verbatim quote, and whether it is script wording, a characterization, or a derivation. No cell is verified (R11, R15).
- No price, market share, rating, benchmark, logo or box art is shown. Tool labels carry no release years: whether all five belong to 1995 is unchecked.
- Tradeoffs soften the script’s harsher words (“miserable”, “brutally slow”, “invisible”); final wording needs editorial approval.
