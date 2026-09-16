# CMP-09 — Production QA

**Production:** produced. **Release:** unreviewed.
**Worker:** Claude Fable 5.1, worktree agent-a1ce4520f7cd8bd1d, branch `ticket/CMP-09-CODE-29`, 2026-09-16.

## Delivered
Still, 1920 × 1080, three equal columns (C#, C++, Visual Basic (1995)) with the ticket's footer sentence. Variants `comparison` (identical to the poster) and `token-focus` (Enqueue/Dequeue, push/front/pop, ReDim and the three shift-loop lines backed by focus rectangles). Each media, source and evidence file is listed with byte count and SHA-256 in delivery.json. All exports are real renders; nothing is a placeholder.

- `exports/poster.png`, `exports/comparison.png`, `exports/token-focus.png` (1920 × 1080), `exports/contact-sheet.png`
- `proofs/poster-720.png`, `proofs/comparison-720.png`, `proofs/token-focus-720.png` (1280 × 720)
- `src/scene.svg`, `src/scene-0000.svg`, `src/variant-comparison.svg`, `src/variant-token-focus.svg`, `src/index.html`, `src/build.json`, `src/timeline.json`, `src/brief.json`
- `src/excerpt-hand.vb` (Program.vb 23–26), `src/excerpt-redim.vb` (130), `src/excerpt-shift.vb` (160–164): the untrimmed excerpt bytes
- `evidence/provenance.json`, `evidence/source-excerpts.md`, `evidence/render-tests.json`, `evidence/browser-tests.json`, `evidence/claim-checks.json`

## What is on the card
- C# and C++ columns: the ticket's authored examples, labelled `example`. The ticket's single C++ line `Card top = hand.front(); hand.pop();` is shown as its two statements on two lines so that all three columns share one code size; no token was changed. No compile or run is claimed.
- VB column: three byte-exact Program.vb excerpts, each labelled with its file and line range (`Program.vb · lines 23–26`, `line 130`, `lines 160–164`) and closed by the note "excerpt · VB.NET source as written / leading indentation trimmed for display". The leading indentation common to each block (4 spaces for 23–26, 8 spaces for 130 and 160–164) is trimmed for display; relative indentation and every token are kept. The same lines exist identically in `War/Program.vb` (CRLF) and `sources/Program.vb` (LF).
- Footer, verbatim from the ticket: "No generic collections, no built-in queue: an array and a counter."
- Code is 25 px DejaVu Sans Mono in all three columns; headers 40 px Liberation Sans bold; footer 34 px.

## Checks actually performed
- `python tools/render/render_assets.py --id CMP-09`: poster, both variants, contact sheet and `proofs/poster-720.png` rendered by CairoSVG 2.9.1; PNG dimensions asserted 1920 × 1080 by the renderer (evidence/render-tests.json). Variant 720p proofs made with Pillow LANCZOS from the 1080p exports.
- Excerpt check (local script): `src/excerpt-*.vb` equal `War/Program.vb` and `sources/Program.vb` lines 23–26, 130 and 160–164 line-for-line (newline-normalized); every excerpt line is present in `scene.svg`. `poster.png` is byte-identical to `comparison.png`.
- Browser check (local copy of `tools/render/qa_browser.py` limited to this ID, Playwright bundled Chromium, in-memory HTML): `window.__ASSET__` present, `renderAt` deterministic across seeks, 4 SVG files / 572 text boxes all inside the canvas, no network request. Written to `evidence/browser-tests.json`; the shared `review/browser-summary.json` was not touched.
- Manual inspection (Read tool): poster, comparison and token-focus at 1920 × 1080 and the three 720p proofs at 1280 × 720. All three columns legible at 1280 wide; the code at 25 px (about 17 px at 720p) is the smallest text on the card and is the size forced by the 32-character `ReDim H.Cards(HAND_CAPACITY - 1)` line in an equal third of the safe area. First render's excerpt note overran the column edge; it was split into two lines and re-rendered before delivery. Focus rectangles cover only the intended tokens/lines.
- `python tools/validate_delivery.py --id CMP-09`: see "Validator" below.

## Validator
```
{"id": "CMP-09", "ok": true, "errors": []}
```
(Full output, including the validator's standing limitations, was captured in the completion report.)

## Reproduction
From the package root, `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` set as an environment variable:

```
python tools/render/render_assets.py --id CMP-09
python tools/validate_delivery.py --id CMP-09
```

The SVG states in `src/` are the editable sources; the authoring script that produced them (a local script importing `tools/render/studio.py` read-only) is not part of the delivery, so edit the SVGs or re-author from `src/build.json`. Tool versions: Python 3.14.0, CairoSVG 2.9.1, Pillow 12.3.0, Playwright bundled Chromium (version in evidence/browser-tests.json), ffmpeg 6.0 (not needed for a still), Windows 11 Pro 10.0.26200. Fonts: Liberation Sans and DejaVu Sans Mono from C:/WINDOWS/fonts through fc-match; no font files distributed.

## Review questions (evidence cannot settle)
1. **Header versus dialect.** The ticket requires the header "Visual Basic (1995)" and a byte-exact Program.vb excerpt, and its acceptance check says each column's code must be valid in the language its header names. Program.vb is VB.NET: `Structure … End Structure` (lines 23 and 26) is VB.NET spelling; the script's own section 6 says 1995 VB spelled it `Type … End Type`. Lines 24–25, 130 and 160–164 are valid in both dialects. The card keeps the ticket's header and says "VB.NET source as written" in the excerpt note. If that is not acceptable, the options are: header "Visual Basic" (drop the year), or show only lines 24–25 of the structure. Producer's call.
2. **C++ line split.** `Card top = hand.front(); hand.pop();` is displayed as two lines (same tokens) so the three columns share one code size. If the producer prefers the ticket's one-line form, the code size drops to 22 px.
3. **Code size.** 25 px at 1080p is well below CMP-01's 54 px; it is what three equal columns of a 32-character line allow inside the 120 px safe area. Legible at 720p in my inspection, but the producer should confirm on the cut.

No narration sync, sound design, final assembly or independent editorial clearance is certified here. Produced is intentionally different from release-approved.
