# CODE-28 — Production QA

**Production:** produced. **Release:** unreviewed.

## What it is
A still code card, CODE family treatment (header `Program.vb` / `VB.NET`, dark panel, line numbers, `Lines 114–126` footer), showing the literal text of **`Program.vb` lines 114–126: `Sub ShuffleDeck(ByRef Deck() As Card)` … `End Sub`**, the subroutine the section-7 narration is looking at (DIA-06's anchor). Its four `Dim` lines (115–118) are the first statements inside the Sub, which is the "declared at the top" beat.

- `clean`: the excerpt only.
- `highlighted` (also the poster): the Dim block (lines 115–118) under the family's highlight bar, which stops short of the right margin at a gold edge; the margin label reads **all declarations first**. Nothing crosses code text.
- On-card title: the short form "Every variable declared at the top"; the full ticket title is the HTML/SVG title.

## Delivered
Every file is enumerated by byte count and SHA-256 in delivery.json: `src/index.html`, `src/excerpt.vb` (the unmodified excerpt), `src/scene.svg`, `src/scene-0000.svg`, `src/variant-clean.svg`, `src/variant-highlighted.svg`, `src/build.json`, `src/timeline.json`, `src/brief.json`, `exports/poster.png`, `exports/clean.png`, `exports/highlighted.png`, `exports/contact-sheet.png`, `proofs/poster-720.png`, `proofs/gallery.jpg`, `evidence/*`. `poster.png` is byte-identical to `highlighted.png`.

## Checks actually performed
- **Excerpt, byte-exact:** `src/excerpt.vb` (LF newlines) is found verbatim, byte for byte, in `sources/Program.vb` (the validator's canonical copy, LF), and equals `War/Program.vb` lines 114–126 line for line (`War/Program.vb` uses CRLF newlines and differs from `sources/Program.vb` only in that and in its first line's file comment; the thirteen excerpt lines are identical). Both files' SHA-256 are in `evidence/provenance.json`. The manifest row's `source_hint` is `code`, not `literal-program-excerpt`, so the validator does not repeat this comparison itself; it was run with Python before finishing and is recorded here.
- **Render:** `python tools/render/render_assets.py --id CODE-28` (CairoSVG 2.9.1, Pillow 12.3.0) asserted 1920 × 1080 for every PNG; `evidence/render-tests.json`. Still asset: no MP4, `duration` null.
- **Browser:** `src/index.html` loaded in Playwright 1.63.0's Chromium (in-memory, offline): no network request; deterministic `renderAt`; all 491 text boxes across the 4 SVG files inside the canvas; the 6 gold annotation elements (label, bar edges) overlap **0** code text elements (`evidence/browser-tests.json`).
- **Manual inspection:** `clean.png` and `highlighted.png` at full size (1920 × 1080) and as 1280 × 720 copies. Thirteen lines at 34 px are legible at both sizes; the Dim block is visibly first; the bar ends before the label.
- Keywords `Sub`, `ByRef`, `As`, `Dim`, `New`, `For`, `To`, `Step`, `Next`, `End` blue; numerals gold; identifiers white. No smart quotes or truncation.

## Reproduction
From the repository root on Windows: `set CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` then `python tools/render/render_assets.py --id CODE-28`. The SVG states in `src/` are the editable sources, authored with `tools/render/studio.py` primitives from a worker script (the shared `build_assets.py` has no CODE-28 composition; do not run it for this ID).

Toolchain: Python 3.14.0; CairoSVG 2.9.1 with MSYS2 UCRT64 Cairo; Pillow 12.3.0; ffmpeg 6.0-essentials_build (present, unused for a still); Playwright 1.63.0. No installs, no network, no font files distributed.

## Remaining decisions
No assigned claim gate. Rights: Devin's standing R14 ruling. Release approval is the producer's.

No narration sync, final video assembly, or live program capture is certified here.

## Asset-specific notes
- Literal excerpt of Program.vb lines 114–126 (Sub ShuffleDeck), stored unmodified in src/excerpt.vb; line numbers are a display layer.
- The four Dim lines (115–118) are the first statements inside the Sub; the highlighted variant bars that block and labels it in the right margin.
- Literal modern VB.NET source illustration; not a live IDE or VB4 capture.
