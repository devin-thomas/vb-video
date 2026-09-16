# REF-05 — Production QA

**Production:** produced. **Release:** unreviewed.

## What it is
An **authored** C reference card (not a Program.vb excerpt, not recovered source): the ticket's twelve-line copy, verbatim, in the reference-code family treatment (dark card, monospace, line numbers, margin labels, gold footer note, `12 lines` at the right). Header: `shuffle.c` (a display label) and **`C (C89)`**. Title: "C89: declarations at the top of the block".

- Both variants mark line 11 (`/* int late = 0;   <- not allowed in C89 after a statement */`) as the contrast: a tinted row bar ending at a gold edge and the two-row margin label **not allowed in C89 / (C99 and later only)**. The line is a comment in the copy, so it is visibly not part of the valid C89 code.
- `top-focus` (also the poster) adds the family's highlight bar over the declaration block (lines 4–6, `int i; int j; int temp;`) with the margin label **declarations first**.
- Footer note on both: "Authored example: in C89 every declaration in a block comes before its first statement."

## Delivered
Every file is enumerated by byte count and SHA-256 in delivery.json: `src/index.html`, `src/excerpt.c` (the ticket copy plus a final newline), `src/scene.svg`, `src/scene-0000.svg`, `src/variant-clean.svg`, `src/variant-top-focus.svg`, `src/build.json`, `src/timeline.json`, `src/brief.json`, `exports/poster.png`, `exports/clean.png`, `exports/top-focus.png`, `exports/contact-sheet.png`, `proofs/poster-720.png`, `proofs/gallery.jpg`, `evidence/*` including `evidence/compile-check.json`. `poster.png` is byte-identical to `top-focus.png`.

## Compile check (actually run)
Compiler installed and used: **gcc 16.2.0 (MSYS2 UCRT64, `C:\msys64\ucrt64\bin\gcc.exe`)**. The card copy has no `#include`, so each check file is exactly one line `#include <stdlib.h>` (for `rand`) followed by the copy; the sources and full diagnostics are in `evidence/compile-check.json`.

1. Valid part: `gcc -std=c89 -pedantic-errors -Wall -Wextra -c a363_ref05_valid.c` → **exit 0, no diagnostics**. The C89-valid code (declarations first, then the loop) compiles in strict C89 mode.
2. Contrast: the same file with line 11 uncommented (`int late = 0;` after the loop) → **exit 1**: `error: ISO C90 forbids mixed declarations and code [-Wdeclaration-after-statement]`. This is the rule the card states; it was not assumed.

## Other checks actually performed
- **Copy:** `src/excerpt.c` equals the ticket's copy exactly (plus one trailing newline); the on-card text is that file's lines through the shared C tokenizer (keywords blue, comments green, numerals gold); no character was changed.
- **Render:** `python tools/render/render_assets.py --id REF-05` (CairoSVG 2.9.1, Pillow 12.3.0) asserted 1920 × 1080 for every PNG; `evidence/render-tests.json`. Still asset: no MP4, `duration` null.
- **Browser:** `src/index.html` loaded in Playwright 1.63.0's Chromium (in-memory, offline): no network request; deterministic `renderAt`; all 391 text boxes across the 4 SVG files inside the canvas; the 22 gold annotation elements (labels, bar edges, footer note) overlap **0** code text elements (`evidence/browser-tests.json`).
- **Manual inspection:** `clean.png` and `top-focus.png` at full size (1920 × 1080) and as 1280 × 720 copies. Twelve lines at 30 px and the margin labels are legible at both sizes; the longest line (line 11, 66 characters) ends well before its gold edge and label.

## Reproduction
From the repository root on Windows: `set CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` then `python tools/render/render_assets.py --id REF-05`. The SVG states in `src/` are the editable sources, authored with `tools/render/studio.py` primitives from a worker script (the shared `build_assets.py` has no REF-05 composition; do not run it for this ID). Compile check: `C:\msys64\ucrt64\bin\gcc.exe -std=c89 -pedantic-errors -Wall -Wextra -c <file>` on the files recorded in `evidence/compile-check.json`.

Toolchain: Python 3.14.0; CairoSVG 2.9.1 with MSYS2 UCRT64 Cairo; Pillow 12.3.0; ffmpeg 6.0-essentials_build (present, unused for a still); Playwright 1.63.0; gcc 16.2.0. No installs, no network, no font files distributed.

## Remaining decisions
No assigned claim gate. Rights: Devin's standing R14 ruling; the code is authored for this production. Release approval is the producer's.

## Asset-specific notes
- Authored representative C89 written for this production from the ticket's copy; not from Program.vb, a textbook, or any recovered source. The file name shuffle.c is a display label.
- The commented line 11 is the contrast: a declaration after a statement, which C89 forbids and C99 and later allow. Its tinted bar and margin label appear on both variants; the top-focus variant adds the declaration-block bar.
- Compile check recorded in evidence/compile-check.json (gcc 16.2.0, -std=c89 -pedantic-errors).
