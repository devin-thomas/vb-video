# XTRA-04 — Production QA

**Production:** produced. **Release:** blocked (R15, review questions Q1–Q5).

## Delivered
Still asset, 1920 × 1080, no motion. Every file is listed with byte count and SHA-256 in delivery.json.

- `exports/poster.png`: the clean comparison (source `src/scene.svg`, also `src/scene-0000.svg`).
- `exports/comparison.png`: named variant `comparison`, the same layout with a line-structure overlay (source `src/variant-comparison.svg`).
- `src/index.html`: offline, deterministic HTML (`window.__ASSET__`, still at t = 0).
- `src/excerpt-fortran2.f`, `src/excerpt-dartmouth.bas`: the exact code text.
- `src/build.py`: the authoring script. `src/build.json` and `src/timeline.json` hold build and timing metadata.
- `proofs/poster-720.png`, `proofs/comparison-720.png`: 1280 × 720 downscales used for review.
- `exports/contact-sheet.png`: an overview sheet written by the renderer.

Timing: no named cutdown. Both stills hold for editorial timing. The comparison variant shares the poster's geometry, so the edit can dissolve from one to the other without anything moving.

## Checks actually performed (2026-09-15)
- `python assets/reference-code/XTRA-04/src/build.py`: sources authored. A built-in width assertion first failed at 52 px because the FORMAT line overflowed its panel. The code size was reduced to 48 px in both panels and the script reran cleanly.
- `python tools/render/render_assets.py --id XTRA-04`: CairoSVG 2.9.1 rendered poster.png and comparison.png at 1920 × 1080 and wrote proofs/poster-720.png (evidence/render-tests.json). No video, as expected for a still.
- Pillow 12.3.0 LANCZOS resize of exports/comparison.png to proofs/comparison-720.png (1280 × 720).
- `python tools/render/qa_browser.py --id XTRA-04`: installed Chromium 153.0.8010.12 loaded the HTML in memory. 3 SVG files and 65 text boxes checked. No text left the canvas, no network request was made, seeking was deterministic, and there were no errors (evidence/browser-tests.json).
- `python tools/render/finish_delivery.py --deliveries-only --id XTRA-04`: delivery inventory, state and ticket appendix. This file and the manual-review entry in delivery.json were then corrected by hand: the generated text described motion, Program.vb excerpts and a thumbnail-only review that do not apply to this asset.
- `python tools/validate_pack.py`: exit 0, no errors.
- `python tools/validate_delivery.py --id XTRA-04`: see "Validator" below.
- Fonts resolved by fc-match: Liberation Sans Regular and Bold, and DejaVu Sans Mono, all from C:/WINDOWS/fonts. No font files are shipped.

## Manual visual review (by the producing agent)
- **exports/poster.png at full size.** The title reads "Same task, different syntax"; the FORTRAN panel is on the left and the BASIC panel on the right. Code is 48 px monospace in both panels with the same line pitch, and panel sizes are identical. The FORTRAN card columns are faithful: statement number `1` in column 5, statements starting in column 7. Highlighting is the same in both panels: keywords blue, message text gold, other text white. No clipping; all text sits inside x 120–1800 and y 72–1008. The lower part of each panel is empty in the poster. This is deliberate, because the geometry is shared with the comparison variant.
- **proofs/poster-720.png.** Headings, the 30 px dialect labels (about 20 px at 720p) and all code are readable. Nothing blurs together.
- **exports/comparison.png at full size.** Line bands sit behind each line in both panels without moving the code. The FORTRAN column guides ("cols 1-5", "col 7 onward") line up over the right character cells. Captions: "4 statements" with "6H counts the next six characters; the first, a blank, is printer carriage control." on the left, and "2 statements" with "The message sits in quotes; END carries the highest line number." on the right. Each wraps to two lines inside its panel with no overlap.
- **proofs/comparison-720.png.** Captions, the 26 px column guides (about 17 px at 720p, the smallest text) and code are readable.

## Content checks
- Same task in both programs: print one line, HELLO, then end. There is no input, loop or variable in either.
- Dialects are named on screen and in metadata: FORTRAN II for the IBM 7090/7094 (IBM form C28-6054-5), and Dartmouth BASIC from the manual of 1 October 1964. Syntax was checked page by page against scans of both manuals and the 7090/7094 FORTRAN IV manual (C28-6274-2). Citations are in evidence/claim-checks.json and evidence/source-excerpts.md; URLs are in evidence/provenance.json.
- No padding. FORTRAN has 4 statements, each required under the documented rules: PRINT, FORMAT, CALL EXIT for Monitor termination, and END as the last card. BASIC has 2: PRINT, and END with the highest line number. BASIC is honestly shorter for this task, by 2 lines.
- No run, compile result or output is shown or claimed. There are no logos, manual scans, remote resources or private information.
- Typography is identical for both programs. The overlay adds no size change.

## Validator
`python tools/validate_delivery.py --id XTRA-04` after the final metadata update: `"ok": true`, `"errors": []`. The validator's stated limits apply: no OCR, visual, historical or legal judgement.

## Reproduction
From the repository root on Windows, with `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` and that folder on PATH. Use `C:\Python314\python.exe` explicitly, because MSYS2's own python.exe comes first on that PATH and has no CairoSVG.

```sh
python assets/reference-code/XTRA-04/src/build.py
python tools/render/render_assets.py --id XTRA-04
python tools/render/qa_browser.py --id XTRA-04
python tools/render/finish_delivery.py --deliveries-only --id XTRA-04
python tools/validate_delivery.py --id XTRA-04
```

Do not use `build_assets.py --id XTRA-04`, which has no composition for this ticket. finish_delivery.py regenerates a generic qa.md, so re-apply this record afterwards. Make the comparison 720p proof with Pillow (1280 × 720, LANCZOS). Tool versions: Windows 11 10.0.26200, Python 3.14.0, CairoSVG 2.9.1, Pillow 12.3.0, Playwright 1.63.0 with Chromium 153.0.8010.12, ffmpeg 6.0 essentials build. The full toolchain is in delivery.json.

## Remaining decisions
R15 is blocked, not cleared. Its review questions are in evidence/claim-checks.json:
- **Q1:** the list-free FORTRAN II `PRINT 1` is supported only by implication, and nothing was run.
- **Q2 (Writing Lead):** "more readable" is a judgement; "shorter" holds for this task.
- **Q3:** whether to keep the on-screen dialect labels.
- **Q4:** batch deck versus terminal, where environment commands are not shown.
- **Q5:** plain O rather than the manual's slashed O.

No narration sync, sound design, final assembly or independent editorial clearance is certified. Reviewer: none yet. Release comes from the OPS-04 review deck.
