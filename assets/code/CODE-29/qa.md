# CODE-29 — Production QA

**Production:** produced. **Release:** unreviewed.
**Worker:** Claude Fable 5.1, worktree agent-a1ce4520f7cd8bd1d, branch `ticket/CMP-09-CODE-29`, 2026-09-16.

## Delivered
Still code card, 1920 × 1080, CODE-family treatment (top-left label, dialect at top-right, rule, title, dark panel with blue left bar, footer label). Variants `clean` (identical to the poster) and `gloss` (a faint English reading under each line). Each media, source and evidence file is listed with byte count and SHA-256 in delivery.json. All exports are real renders; nothing is a placeholder.

- `exports/poster.png`, `exports/clean.png`, `exports/gloss.png` (1920 × 1080), `exports/contact-sheet.png`
- `proofs/poster-720.png`, `proofs/clean-720.png`, `proofs/gloss-720.png` (1280 × 720)
- `src/scene.svg`, `src/scene-0000.svg`, `src/variant-clean.svg`, `src/variant-gloss.svg`, `src/index.html`, `src/build.json`, `src/timeline.json`, `src/brief.json`
- `src/example.vb`: the two lines as machine-readable text
- `evidence/provenance.json`, `evidence/source-excerpts.md`, `evidence/render-tests.json`, `evidence/browser-tests.json`, `evidence/claim-checks.json`

## What is on the card
- Exactly the two lines the script quotes, verbatim: `If PlayerScore > HighScore Then` and `For Each Item In Collection` (46 px DejaVu Sans Mono, VB keyword colouring). No line numbers: this is an example, not an excerpt.
- Header "Visual Basic" (top right). Top-left label "Example — not from Program.vb"; footer "Authored example · the two lines quoted in the script · not in Program.vb". Title "Reads like English".
- `gloss` variant: under each line, on its own row 62 px below the code baseline, a gold 30 px gloss at 72 % opacity ("if the player's score is higher than the high score, then…" / "for each item in the collection…") with a short lead-in line from the panel's left bar. The code layout is identical in both variants.

## Checks actually performed
- `python tools/render/render_assets.py --id CODE-29`: poster, both variants, contact sheet and `proofs/poster-720.png` rendered by CairoSVG 2.9.1; PNG dimensions asserted 1920 × 1080 by the renderer (evidence/render-tests.json). Variant 720p proofs made with Pillow LANCZOS from the 1080p exports.
- Script check (local script): each line appears backticked in `sources/SCRIPT.md` line 689 (the ticket's anchor) and in `War/SCRIPT.md` line 746 (same sentence; the working copy's numbering is offset). Neither line occurs in Program.vb. `poster.png` is byte-identical to `clean.png`.
- Gloss geometry: code text box spans baseline−46 … baseline+12; the gloss row starts at baseline+40 and is a separate `<text>` in its own group, so nothing overlaps. Confirmed by eye on `gloss.png` at full size and on `proofs/gloss-720.png`.
- Browser check (local copy of `tools/render/qa_browser.py` limited to this ID, Playwright bundled Chromium, in-memory HTML): `window.__ASSET__` present, `renderAt` deterministic across seeks, 4 SVG files / 82 text boxes all inside the canvas, no network request. Written to `evidence/browser-tests.json`; the shared `review/browser-summary.json` was not touched.
- Manual inspection (Read tool): poster, clean and gloss at 1920 × 1080 and the three 720p proofs at 1280 × 720. Legible at 1280 wide; the gloss is faint but readable.
- `python tools/validate_delivery.py --id CODE-29`: see "Validator" below.

## Validator
```
{"id": "CODE-29", "ok": true, "errors": []}
```
(Full output, including the validator's standing limitations, was captured in the completion report.)

## Reproduction
From the package root, `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` set as an environment variable:

```
python tools/render/render_assets.py --id CODE-29
python tools/validate_delivery.py --id CODE-29
```

The SVG states in `src/` are the editable sources; the authoring script that produced them (a local script importing `tools/render/studio.py` read-only) is not part of the delivery, so edit the SVGs or re-author from `src/build.json`. Tool versions: Python 3.14.0, CairoSVG 2.9.1, Pillow 12.3.0, Playwright bundled Chromium (version in evidence/browser-tests.json), ffmpeg 6.0 (not needed for a still), Windows 11 Pro 10.0.26200. Fonts: Liberation Sans and DejaVu Sans Mono from C:/WINDOWS/fonts through fc-match; no font files distributed.

## Review questions (evidence cannot settle)
1. **Gloss wording and weight.** The two glosses are the ticket's suggested phrasings, set in gold at 72 % opacity. Whether "faint" should be fainter (or in the muted grey instead of gold) is a taste call for the producer.
2. **Label wording.** "Example — not from Program.vb" (top left) and the footer label are production copy; shorten or reword at will.

No narration sync, sound design, final assembly or independent editorial clearance is certified here. Produced is intentionally different from release-approved.
