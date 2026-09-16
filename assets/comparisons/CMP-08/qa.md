# CMP-08 — Production QA

**Production:** produced. **Release:** unreviewed.

## Delivered
Each required media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. Existing outputs are real rendered media, not placeholder filenames. Independent variants belong to this ticket. The original source brief and code remain unchanged.

## Checks actually performed
- Rasterization and PNG dimensions checked at 1920 × 1080. Motion files checked with ffprobe for H.264, 30 fps, yuv420p, frame count and expected duration; per-file results are retained. Support-only OPS-01 is not a motion asset.
- HTML/SVG content was loaded in installed Chromium, with every source/variant scene checked for out-of-canvas text. Nonlinear forward/backward seeking was compared for identical SVG output. Remote requests were monitored; none were used. This is not a full text-overlap or semantic-proof system.
- The 25 literal Program.vb excerpts are checked against their canonical source ranges by the supplied validator. Code highlighting does not alter source files. Code line-wrap arrows are display markers, not inserted VB syntax.
- Visual review: Poster contact-sheet review. All 71 posters inspected in eight 1920-pixel-wide review sheets, each poster at 640 × 360. No obvious title clipping or composition defect remained at overview size. This does not certify every full-resolution motion frame.
- The source-based War and shuffle fixtures are deterministic teaching examples, not recorded program execution. Source/fixture checks are in the batch's review reports.

## Reproduction
`python tools/render/render_assets.py --id CMP-08` from the package root for media assets. For OPS-01, use `python tools/render/finish_delivery.py --ops-only`. Read tools/render/REBUILD.md first. Tool versions: assets/ops/OPS-01/exports/capabilities.json.

## Remaining decisions
Assigned gates: R03. See evidence/claim-checks.json and docs/EDITORIAL_REGISTER.md.

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- This is a proposed minimal illustration of the narrated underscore contrast, not a screenshot of the supplied program. Retain the explicit underscore; do not claim every modern VB multiline expression always requires one.
- No compile/run is claimed for illustrative counterparts.

## Revision 2 — 2026-09-16 (Devin's cut note 13)

- Change: left-column header kept as "C#": `Console.WriteLine` is .NET-only (C++ would be `std::cout <<`, Java `System.out.println`), and nothing else in the snippet (`+` concatenation, the wrapped argument) implies another language, so no re-render was needed and the exports are unchanged.
- No file under `src/` or `exports/` changed; every export hash in delivery.json is the one the 2026-09-15 release review looked at. Only this section, state.json and the delivery metadata (release status, notes, this file's hash) were updated.
- Tests run: `python tools/validate_delivery.py --id CMP-08` (ok). The revision 1 render and browser checks recorded above still describe these exports.
- Gate R03: the recorded decision in evidence/claim-checks.json (2026-09-15) concerns the code as written, which revision 2 does not change; it is therefore not listed as unresolved. Release is unreviewed because revision 2 asks the producer to confirm the header decision, not because of the gate.
- Status: production produced; release unreviewed until the producer confirms the header decision. The 2026-09-15 release approval is superseded by the revision 2 review.
