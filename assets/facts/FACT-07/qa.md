# FACT-07 — Production QA

**Production:** produced. **Release:** unreviewed.

## Delivered
Each media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. `exports/poster.png`, `exports/table.png` (byte-identical to the poster; both come from the same authored state) and `exports/highlight.png` are real 1920 × 1080 renders; `proofs/poster-720.png` is the 1280 × 720 proof. Sources are `src/scene.svg`, `src/scene-0000.svg`, `src/variant-table.svg`, `src/variant-highlight.svg`, the offline `src/index.html`, `src/build.json`/`src/timeline.json`, and `src/compose.py`, which authored all of them. `src/cells.json` records every cell with the capture file and line it came from.

## Figures and where each came from
Every number on the card was parsed out of the captured stdout of the four recorded runs by `src/compose.py`; nothing was typed in. File and line for each figure are in `evidence/source-excerpts.md`:

| Run | Capture | Rounds (line) | Wars (line) | Winner (line) | How it ended (line) |
|---|---|---:|---:|---|---|
| Run 1 | TERM-04 | 617 (1295) | 26 (1296) | Player 1 (1294) | Player 2 ran out of cards in a war (1291) |
| Run 2 | TERM-05 | 1,056 (2142) | 10 (2143) | Player 2 (2141) | Normal round win (2137, last round) |
| Run 3 | TERM-06 | 150 (330) | 10 (331) | Player 2 (329) | Normal round win (325, last round) |
| Run 4 | TERM-02 | 2,008 (4163) | 69 (4164) | Player 2 (4162) | Player 1 ran out of cards in a war (4159) |

Footer: shortest 150 rounds (Run 3), longest 2,008 rounds (Run 4), computed from the same values. The two runs the narration names (617 and 2,008 rounds; War/SCRIPT.md:586 and 612) are present and match; the narration's "ten in one game, sixty-nine in another" (War/SCRIPT.md:574) matches the Wars column.

## Checks actually performed
- `python assets/facts/FACT-07/src/compose.py`: parses the four transcripts, aborts if a summary line is missing or a draw/cap message is present, asserts the 617- and 2,008-round runs are present, and checks every text run against the safe area (x 120…1800, y 72…1008) with the studio font metrics. Passed.
- `python tools/render/render_assets.py --id FACT-07` (CairoSVG 2.9.1, Pillow 12.3.0, Python 3.14.0, `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` as an environment variable): poster, both variants, 720p proof and contact sheet rendered; `evidence/render-tests.json`. PNG sizes re-checked with PIL: 1920 × 1080 for all exports, 1280 × 720 for the proof.
- Offline Chromium checks (the logic of `tools/render/qa_browser.py`, run so that it writes only `evidence/browser-tests.json`; the shared script also rewrites review/browser-summary.json outside this ticket's paths): Chromium 153.0.8010.12, in-memory HTML, deterministic `renderAt`, 4 SVG files, 112 text boxes all inside the canvas, no network request. Passed.
- Manual visual review by the worker, at full size and at 720p: `exports/poster.png`, `exports/highlight.png`, `proofs/poster-720.png` (and `exports/table.png` confirmed byte-identical to the poster by SHA-256). Four rows and five columns; Rounds and Wars are right-aligned so the figures line up digit for digit; the footer reads in one line; `highlight` panels Run 1 and Run 4 with a blue bar and dims Runs 2 and 3, which remain legible. All text is readable at 720p.
- `python tools/validate_delivery.py --id FACT-07`: passed (`"ok": true`, no errors) after delivery.json was written.

## Reproduction
From the repository root, with `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` set as an environment variable (fontconfig's `fc-match` from MSYS2 on PATH resolves Liberation Sans / DejaVu Sans Mono from C:\Windows\Fonts):

```sh
python assets/facts/FACT-07/src/compose.py
python tools/render/render_assets.py --id FACT-07
python tools/validate_delivery.py --id FACT-07
```

Do not run `tools/render/build_assets.py` for this ID; the shared authoring script does not know this asset, and `finish_delivery.py --id` writes outside the owned paths (ticket file, review index). Tool versions: the toolchain in delivery.json.

## Remaining decisions
No R gate is assigned. Review questions (in `evidence/claim-checks.json`):
1. Run numbering: Run 1 = 617 rounds and Run 4 = 2,008 rounds follow the FACT-08 ticket copy; Runs 2 and 3 (TERM-05, TERM-06) follow script order. Swap them if the cut prefers ascending length.
2. Source scope: the ticket also names recordings R4-01..R4-04 (and R2, R3a, R3b). Those are different games (685, 240, 169, 112, 338, 190, 557 rounds) with no 617- or 2,008-round run, so the card is built from the TERM-02/04/05/06 captures only.

No narration sync, sound design, final video assembly or full independent editorial clearance is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- Fact-card treatment: dark card, one bold line per row, tabular figures right-aligned; title "Every run is different"; footer with the shortest and longest run.
- The subtitle "Four recorded runs of the same program" is production copy; all four captures ran the unchanged Program.vb (each capture package's `source/Program.vb` is hash-checked by its own delivery).
