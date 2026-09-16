# CMP-01 — Production QA

**Production:** produced. **Release:** unreviewed.

## Delivered
Each required media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. Existing outputs are real rendered media, not placeholder filenames. Independent variants belong to this ticket. The original source brief and code remain unchanged.

## Checks actually performed
- Rasterization and PNG dimensions checked at 1920 × 1080. Motion files checked with ffprobe for H.264, 30 fps, yuv420p, frame count and expected duration; per-file results are retained. Support-only OPS-01 is not a motion asset.
- HTML/SVG content was loaded in installed Chromium, with every source/variant scene checked for out-of-canvas text. Nonlinear forward/backward seeking was compared for identical SVG output. Remote requests were monitored; none were used. This is not a full text-overlap or semantic-proof system.
- The 25 literal Program.vb excerpts are checked against their canonical source ranges by the supplied validator. Code highlighting does not alter source files. Code line-wrap arrows are display markers, not inserted VB syntax.
- Visual review (revision 2): Standalone inspection of the revision 2 exports at 1920 x 1080 and 1280 x 720 (worker, 2026-09-16). poster.png and token-focus.png viewed at full size; comparison.png is byte-identical to poster.png (same source state, verified by SHA-256). The poster was viewed again as an ffmpeg scale=1280:-1 copy made outside the asset, alongside the Pillow proofs/poster-720.png. Header "C / C++ / C#" reads on one line inside the left column; layout, code, highlight boxes and footer are unchanged from revision 1; nothing is clipped at either size and punctuation is legible at 720p.
- The source-based War and shuffle fixtures are deterministic teaching examples, not recorded program execution. Source/fixture checks are in the batch's review reports.

## Reproduction
From the repository root, `python tools/render/build_assets.py --id CMP-01` rebuilds the sources (and resets the ticket's state); `render_assets.py`, `qa_browser.py` and `finish_delivery.py` in tools/render, each with `--id CMP-01`, then render, check and finish it. For OPS-01, use `python tools/render/finish_delivery.py --ops-only`. Read tools/render/REBUILD.md first. Tool versions: the toolchain in delivery.json.

## Remaining decisions
No assigned claim gate; producer publication approval is still not assumed.

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- Names and capitalization follow the script; emphasize that VB puts the type after As. Avoid implying different numeric ranges are being taught here.
- No compile/run is claimed for illustrative counterparts.

## Revision 2 — 2026-09-16 (Devin's cut note 13)

- Change: left-column header changed from "C#" to "C / C++ / C#" (`int rank; char suit;` is the same declaration in all three).
- Edited files: the asset's own SVG states (`src/scene.svg`, `src/scene-0000.svg`, `src/variant-comparison.svg`, `src/variant-token-focus.svg`) and the inlined copy in `src/index.html` (regenerated as `json.dumps` of `scene-0000.svg`, the same way the original build wrote it). `src/brief.json` still carries the ticket's original copy payload headed "C#"; running `build_assets.py --id CMP-01` would regenerate the revision 1 header, so do not run it without re-applying this change.
- Exact reproduction (Windows, from the repository root, `python` = C:\Python314\python.exe):
  `set CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin`, then `python tools/render/render_assets.py --id CMP-01`, `python tools/render/qa_browser.py --id CMP-01`, `python tools/render/finish_delivery.py --id CMP-01 --owner "Claude Fable 5.1 worker session (revision 2)"`, `python tools/validate_delivery.py --id CMP-01`. Note that `finish_delivery.py --id` also rewrites `docs/tickets/CMP-01.md` (dropping the Revision 2 section) and `review/browser-summary.json` / `review/production-index.json`; those were restored from git after the run and are not part of this delivery.
- Toolchain actually used: Python 3.14.0, CairoSVG 2.9.1 on MSYS2 ucrt64 Cairo, Pillow 12.3.0, ffmpeg 6.0-essentials, Playwright 1.63.0 with Chromium 153.0.8010.12. Fonts resolved through fontconfig (`fc-match`): LiberationSans-Regular/Bold.ttf and DejaVuSansMono.ttf, the same families as the original Linux batch, so the code and highlight positions match the revision 1 exports. No network, no installs, no font files distributed.
- Tests run and results: `render_assets.py` (all PNGs 1920 x 1080, evidence/render-tests.json rewritten); `qa_browser.py` (offline, deterministic seek, 4 SVG files, no out-of-canvas text; evidence/browser-tests.json); `validate_delivery.py --id CMP-01` (ok). No motion files exist for this still asset.
- Visual inspection: poster.png and token-focus.png viewed at full size; comparison.png is byte-identical to poster.png (same source state, verified by SHA-256). The poster was viewed again as an ffmpeg scale=1280:-1 copy made outside the asset, alongside the Pillow proofs/poster-720.png. Header "C / C++ / C#" reads on one line inside the left column; layout, code, highlight boxes and footer are unchanged from revision 1; nothing is clipped at either size and punctuation is legible at 720p.
- Status: production produced; release unreviewed until the producer approves the new exports. The 2026-09-15 release approval covered the previous exports and does not carry over.
