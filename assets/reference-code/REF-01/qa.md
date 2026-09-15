# REF-01 — Production QA

**Production:** produced. **Release:** blocked.

## Delivered
Each required media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. Existing outputs are real rendered media, not placeholder filenames. Independent variants belong to this ticket. The original source brief and code remain unchanged.

## Checks actually performed
- Rasterization and PNG dimensions checked at 1920 × 1080. Motion files checked with ffprobe for H.264, 30 fps, yuv420p, frame count and expected duration; per-file results are retained. Support-only OPS-01 is not a motion asset.
- HTML/SVG content was loaded in installed Chromium, with every source/variant scene checked for out-of-canvas text. Nonlinear forward/backward seeking was compared for identical SVG output. Remote requests were monitored; none were used. This is not a full text-overlap or semantic-proof system.
- The 25 literal Program.vb excerpts are checked against their canonical source ranges by the supplied validator. Code highlighting does not alter source files. Code line-wrap arrows are display markers, not inserted VB syntax.
- Visual review: Full-resolution stills, mid-scroll keyframe and 720p proof. Viewed exports/clean.png, exports/teaching-focus.png (also the poster), exports/keyframes/middle.png and proofs/poster-720.png. preview.mp4 was probed by the renderer and decoded end to end with ffmpeg without errors; it was not watched frame by frame. Code, line numbers and highlighting are readable at 720p. The focus band covers BEGIN_MESSAGE_MAP through END_MESSAGE_MAP and the caption fits beside the line count.
- The source-based War and shuffle fixtures are deterministic teaching examples, not recorded program execution. Source/fixture checks are in the batch's review reports.

## Reproduction
From the repository root, `python tools/render/build_assets.py --id REF-01` rebuilds the sources (and resets the ticket's state); `render_assets.py`, `qa_browser.py` and `finish_delivery.py` in tools/render, each with `--id REF-01`, then render, check and finish it. For OPS-01, use `python tools/render/finish_delivery.py --ops-only`. Read tools/render/REBUILD.md first. Tool versions: the toolchain in delivery.json.

## Remaining decisions
Assigned gates: R15. See evidence/claim-checks.json and docs/EDITORIAL_REGISTER.md.

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- Agent-authored representative MFC code in the style of Visual C++ 4: ClassWizard AFX_MSG blocks and ON_COMMAND(ID, handler) without &Class::. It is not recovered historical source.
- Not compiled: Visual Studio 2022 on the production machine has no MFC libraries installed. Technical and era review stays open under R15.
- CCardDoc, FlipNextCard, Deal and IsDealt are illustrative names for this card game; their definitions are not shown.
- Line numbers and the caption are display layers; src/excerpt.cpp holds the exact text.
- Timing: a 2.5 s hold, a one-line scroll every 0.25 s through all 48 rows, then the focus from 11 s to the end.
