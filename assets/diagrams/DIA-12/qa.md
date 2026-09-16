# DIA-12 — Production QA

**Production:** produced. **Release:** unreviewed (revision 2, 2026-09-16; the producer has not yet approved the new exports).

## Revision 2 — row-by-row reveal
Devin approved proposal 7 of the 17:00–end pass: instead of holding the whole table for 63 s, the table is revealed row by row. The table's content and styling are unchanged; only the reveal order and the named variants changed. The asset is now a motion asset (6 s, 30 fps) with three placement stills.

- `exports/row-console.png` — only the "Console app like ours" row (the "roughly comparable" beat); ASM-03 places it at 35:25.
- `exports/row-gui.png` — adds the "GUI builder" row ("an afternoon" vs "a week, minimum"); 35:50.
- `exports/full.png` — the complete table; 36:18. Byte-identical to `exports/full-table.png` and `exports/poster.png`.
- `exports/preview.mp4` — the motion variant `reveal`: 0–0.5 s headings and rules only; console row fades in 0.5–0.9 s; GUI builder 1.5–1.9 s; Language 2.5–2.9 s; Learning curve 3.5–3.9 s; Runtime required 4.5–4.9 s; complete table held to 6 s. Rows start 1 s apart; each fade is 12 authored opacity states (0.4 s). 180 frames.
- `exports/full-table.png` and `exports/gui-row-focus.png` from the first delivery are kept unchanged (still required by the manifest).
- Row slots keep their table positions in every state, so the three stills and the motion line up frame for frame; hidden rows are text at opacity 0 with the table rules left in place.

## Delivered
Each required media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. Existing outputs are real rendered media, not placeholder filenames. Independent variants belong to this ticket. The original source brief and code remain unchanged.

## Checks actually performed (revision 2, 2026-09-16)
- `python tools/render/render_assets.py --id DIA-12` (CairoSVG 2.9.1 through MSYS2 Cairo, ffmpeg 6.0) rendered every PNG at 1920 × 1080 and encoded preview.mp4 from src/build.json. ffprobe: h264, yuv420p, 30/1, 180 frames, 6.000 s (evidence/render-tests.json); `ffprobe -count_frames` read back 180 frames.
- The checks in tools/render/qa_browser.py were re-run for this asset in installed Chromium 153.0.8010.12 (in-memory HTML, offline): deterministic seeking at 3.18 s after forward/backward seeks, renderAt at all 61 state boundaries forward and backward, 67 SVG files and 1139 text boxes with none out of canvas, no network request (evidence/browser-tests.json). They were run from a scratchpad copy scoped to DIA-12 so that review/browser-summary.json, outside this ticket's owned path, was not rewritten.
- The final motion state (src/scene-0060.svg) is byte-identical to the untouched full table src/scene.svg; exports/full.png, full-table.png, poster.png and keyframes/end.png are byte-identical.
- Visual review at full size (1920 × 1080) and at 1280 × 720: exports/poster.png, row-console.png, row-gui.png, full.png, proofs/poster-720.png, and three frames extracted from preview.mp4 with ffmpeg at 0.70 s (console row mid-fade, about half opacity), 2.00 s (console and GUI rows complete, others hidden) and 5.50 s (complete table). All five rows and both headings match the script table word for word; the partial states show exactly the intended rows; text is legible at 720p; no clipping or overlap.
- Not run this revision: build_assets.py (it would regenerate and discard the hand-authored reveal states) and finish_delivery.py (it rewrites docs/tickets and review/ outside the owned path); delivery.json was written by hand with the same inventory format and hashes.

## Reproduction
From the repository root, with `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` set: `python tools/render/render_assets.py --id DIA-12` re-renders every export from src/build.json (it expects exports/keyframes/ to exist); `python tools/render/qa_browser.py --id DIA-12` repeats the browser checks (and also updates review/browser-summary.json); `python tools/validate_delivery.py --id DIA-12` validates the inventory. Do not run build_assets.py for this ticket: it would overwrite the reveal states. The reveal states were derived from src/scene.svg by setting each row's three text cells' opacity; the authoring script is not part of the pack. Tool versions: the toolchain in delivery.json.

## Remaining decisions
Assigned gates: R03, R09, R16 — the cells are unchanged from the release-approved first delivery, so the recorded decisions in evidence/claim-checks.json still describe the content; the release status is nevertheless back to unreviewed until the producer approves the new exports.

Review questions for the producer:
1. The partial states show the empty row slots (rules only) above the revealed row. If a floating single row with no skeleton is preferred at 35:25, the rules of hidden rows can be dropped; the positions would stay fixed either way.
2. The reveal order after the two narration rows is Language, Learning curve, Runtime required (top to bottom), 1 s apart, so the full table lands at 4.9 s. If the edit wants the last three rows to land together, one state change covers it.

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- All five rows and both column headings are the script’s draft table (SCRIPT.md:661–667), word for word; src/cells.json records each row’s line.
- These cells are draft copy, not verified facts. Console support, the ResEdit characterization and the runtime claim wait on R03, R09 and R16.
- Neutral styling: no scores, bars, icons or product screenshots. gui-row-focus dims the other four rows.
- The VB column describes classic VB4 as the script does; it is not presented as this project’s VB.NET console run.
