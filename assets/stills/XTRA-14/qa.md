# XTRA-14 — Production QA

**Asset:** Real-world VB application collage (script supplement for SCRIPT.md:685–687).
**Production:** produced. **Release:** blocked (R11, R14). Internal proof only, not in any cleared-media bin.
**Reviewer:** none yet. This is the producing agent's self-check, not release approval; release comes from the OPS-04 review deck.

## Delivered
Still asset, 1920 × 1080, no motion and no named cutdown. Every file is listed with byte count and SHA-256 in delivery.json.

| Variant | Export | Source | 720p proof | Panels |
|---|---|---|---|---|
| `collage` (required) | `exports/collage.png`, `exports/poster.png` (byte-identical) | `src/variant-collage.svg` | `proofs/collage-720.png`, `proofs/poster-720.png` | Business tools · Data entry · Utilities, one row |
| `focus-business` (optional) | `exports/focus-business.png` | `src/variant-focus-business.svg` | `proofs/focus-business-720.png` | XTRA-11 enlarged; XTRA-12, XTRA-13 reduced |
| `focus-data-entry` (optional) | `exports/focus-data-entry.png` | `src/variant-focus-data-entry.svg` | `proofs/focus-data-entry-720.png` | XTRA-12 enlarged (exact 2×); XTRA-11, XTRA-13 reduced |
| `focus-utilities` (optional) | `exports/focus-utilities.png` | `src/variant-focus-utilities.svg` | `proofs/focus-utilities-720.png` | XTRA-13 enlarged; XTRA-11, XTRA-12 reduced |

Also delivered:
- `proofs/collage-1to1-left.png`, `proofs/collage-1to1-right.png`: native-pixel halves of the collage.
- `exports/contact-sheet.png`: an overview written by the renderer.
- `src/index.html`: offline, deterministic HTML (`window.__ASSET__`, still at t = 0, collage scene).
- `src/layout.json`: the coordinate-to-source map.
- `src/build.py`, `src/verify.py`, `src/finalize.py`: authoring, pixel verification and delivery finishing.
- `src/build.json`, `src/timeline.json`, `src/brief.json`, `src/copy.txt`.
- Evidence: `evidence/provenance.json`, `evidence/claim-checks.json`, `evidence/source-excerpts.md`, `evidence/placement-checks.json`, `evidence/render-tests.json`, `evidence/browser-tests.json`.

Timing: every variant is a still held for editorial timing.

## Inputs
The three upstream originals are read in place. None is copied or modified. Both scripts stop if an original's SHA-256 differs from its upstream delivery.json.

| Panel | Asset | Source file | SHA-256 | Native size |
|---|---|---|---|---|
| Business tools | XTRA-11 | `assets/historical/XTRA-11/source/original.jpg` | `5b89f93e6161e24531c9236eabc58432dc97bc6da2d6569cfc35c9cc4608a318` | 591 × 423 |
| Data entry | XTRA-12 | `assets/historical/XTRA-12/source/original.gif` | `ef828e695c2bb25e7947c3815807611a264e87bc997a772d2b5fb96ce8dd9b2d` | 334 × 361 |
| Utilities | XTRA-13 | `assets/historical/XTRA-13/source/original.gif` | `bf77dbc0e26345ae839517045f9eb1a509d3655027792188de12c4927e86df33` | 489 × 448 |

Upstream editorial frames were checked. All three are uncropped uniform 2× enlargements (XTRA-11 and XTRA-12 qa.md; XTRA-13 `framing.json` crop null). They were not used: scaling the originals directly avoids a second resample and keeps XTRA-12's whole published figure. XTRA-11's own archive capture already ends just below the NOTES box; that limit is in the original, and nothing further is cropped.

## Placement map (x, y = top-left of the placed image; w × h exact pixels)

| Variant | Panel | Asset | x, y | w × h | Scale | Aspect error | Resampling |
|---|---|---|---|---|---|---|---|
| collage | Business tools | XTRA-11 | 132, 253 | 640 × 458 | 1.0829 | 0.016 % | LANCZOS |
| collage | Data entry | XTRA-12 | 818, 253 | 424 × 458 | 1.2695 | 0.060 % | LANCZOS |
| collage | Utilities | XTRA-13 | 1288, 253 | 500 × 458 | 1.0225 | 0.017 % | LANCZOS |
| focus-business | Business tools | XTRA-11 | 128, 142 | 1087 × 778 | 1.8393 | 0.001 % | LANCZOS |
| focus-business | Data entry | XTRA-12 | 1287, 131 | 185 × 200 | 0.5539 | 0.023 % | LANCZOS |
| focus-business | Utilities | XTRA-13 | 1287, 624 | 252 × 231 | 0.5153 | 0.056 % | LANCZOS |
| focus-data-entry | Data entry | XTRA-12 | 299, 154 | 668 × 722 | 2.0000 | 0 | nearest, integer 2× |
| focus-data-entry | Business tools | XTRA-11 | 1287, 131 | 324 × 232 | 0.5482 | 0.044 % | LANCZOS |
| focus-data-entry | Utilities | XTRA-13 | 1287, 624 | 252 × 231 | 0.5153 | 0.056 % | LANCZOS |
| focus-utilities | Utilities | XTRA-13 | 248, 142 | 848 × 777 | 1.7342 | 0.013 % | LANCZOS |
| focus-utilities | Business tools | XTRA-11 | 1287, 131 | 324 × 232 | 0.5482 | 0.044 % | LANCZOS |
| focus-utilities | Data entry | XTRA-12 | 1287, 623 | 185 × 200 | 0.5539 | 0.023 % | LANCZOS |

"Scale" is x-scale; y-scale differs only by whole-pixel rounding, which is the aspect error column. It is at most 0.3 px on the long side. The frame is identical for every panel: a #1b2027 mat 5 px wide, then a 2 px #343d48 stroke, 7 px in total, all outside the image edges.

## Checks actually performed (2026-09-15)

Run from the repository root on branch `ticket/XTRA-14` (base `main` 5e1825e):

1. **`python -B assets/stills/XTRA-14/src/build.py`** — passed. Assertions:
   - the upstream SHA-256 and byte count match each upstream delivery.json;
   - sources are opaque (alpha extrema 255/255) and single-frame;
   - the labels joined with " · " equal the manifest copy;
   - no label, credit or frame box intersects any image, and no text intersects text;
   - all frames and text are inside x 120–1800, y 72–1008;
   - the XTRA-12 panel carries the Microsoft statement.
   The first run stopped on that last assertion: `wrap()` had split "Used with permission from Microsoft." across two lines. The statement is now kept on one line. A second fix: the common-height search had used a 0.2 px aspect tolerance, which pushed the collage height to 428 and shrank XTRA-13 to 0.955×. The tolerance is now 0.3 px, and the column gap went from 40 to 32 px, giving a 458 px height (XTRA-13 at 1.02×).
2. **`python tools/render/render_assets.py --id XTRA-14`** — CairoSVG 2.9.1 rendered poster.png and the four variant PNGs at 1920 × 1080, plus proofs/poster-720.png and the contact sheet (`evidence/render-tests.json`). No video, as expected for a still.
3. **`python tools/render/qa_browser.py --id XTRA-14`** — Chromium 153.0.8010.12 loaded the HTML in memory. It checked all 4 SVG files and all 57 text boxes: none outside the canvas, no network request, deterministic seeking, no errors (`evidence/browser-tests.json`).
4. **`python -B assets/stills/XTRA-14/src/verify.py`** — `"ok": true`, no errors (`evidence/placement-checks.json`). For each of the 12 placements, and for both poster.png and collage.png:
   - the upstream original's SHA-256 still equals `src/layout.json` and the upstream delivery.json;
   - the PNG embedded in the SVG decodes to exactly the resample of that original;
   - the export's placed rectangle equals that resample pixel for pixel: **0 differing pixels in every placement** (for example 293,120 px checked for the collage XTRA-11 panel). Any overlap, crop, shift, rotation, stretch or blank panel would change pixels;
   - the 5 px mat ring just outside every image edge is uniformly the mat colour: **0 non-matching pixels**, so the frame is outside the image;
   - poster.png and collage.png are byte-identical.
   The same script writes the -720 proofs (1280 × 720, LANCZOS) and the 1:1 crops.
5. **`python tools/render/finish_delivery.py --deliveries-only --id XTRA-14`** — wrote the delivery inventory, the state and the ticket appendix. Its generic qa.md (motion, Program.vb excerpts, thumbnail-only review), its single "original graphics" credit and its generic tests do not describe this asset. This file replaces that qa.md. `python -B assets/stills/XTRA-14/src/finalize.py` then rewrote credits, sources, variants, panel_map, tests, notes and state, and recomputed every hash.
6. **`python tools/validate_pack.py`** — exit 0, `"errors": []`.
7. **`python tools/validate_delivery.py --id XTRA-14`** — see "Validator" below.

Fonts resolved by fc-match: Liberation Sans Regular and Bold from C:/WINDOWS/fonts. No font files are shipped.

## Manual visual inspection (by the producing agent)
- **exports/poster.png and exports/collage.png at full size (identical bytes).** Three framed screenshots sit in one row at the same 458 px height. The row spans x 125–1795, and the block is centred vertically. Labels "Business tools", "Data entry" and "Utilities" are bold, above each frame, left-aligned. Each credit sits below its own frame in grey, with "Used with permission from Microsoft." in white on its own line under the XTRA-12 panel. All three images are present (no blank panel). No text or frame touches any image, and every frame stays outside the image edge. Visual weight is balanced: the wider INVOICE-IT panel is wider but not taller, and the credits are the heaviest text block. That weight is inherent to the required per-panel credits.
- **proofs/collage-1to1-left.png and -right.png (native pixels).** INVOICE-IT: the title bar, menu, field labels, "Invoice # 3379", "Date 02-27-2016", column headings, "SUBTOTAL" and "Thank you for your business." are crisp. Faint JPEG ringing is in the archive original. Data Object Wizard form: every label and value is readable, including all eight drop-down rows and the navy selection; the lower-right grey dither is in Microsoft's GIF. Window Watcher: the title, tree, detail pane (MSVBVM60.DLL, ThunderRT6CommandButton), counters, buttons and "9/3/2003 8:19 AM" are all readable. The LANCZOS resample softens edges slightly but adds no artefacts.
- **proofs/poster-720.png and proofs/collage-720.png (1280 × 720).**
  - Labels read at about 27 px, credits at about 17 px. **The Microsoft credit is legible.**
  - **XTRA-11 is readable:** title, menus, field labels, 3379 and 02-27-2016.
  - **XTRA-12 is readable:** every field label and value, and the drop-down county names.
  - **XTRA-13 is mostly readable:** title, tree items, Locate/Refresh/About/Exit buttons, counters and the status-bar date. Its detail-pane lines are small (about 6 px x-height) but still legible, including MSVBVM60.DLL and ThunderRT6CommandButton.
- **Focus variants, full size and 720p.** In each, the enlarged panel is clearly readable at 720p: INVOICE-IT at 1.84×, the Microsoft form at an exact nearest-neighbour 2×, Window Watcher at 1.73×. Its credit sits on one or two lines. The two reduced context panels (0.52–0.55×) are whole, framed, labelled and credited; their UI text is not readable, by design. In focus-business and focus-utilities the reduced XTRA-12 figure is 185 × 200, still whole, with the Microsoft line legible beside it at 720p.
- **Content:** there is no generic office imagery, stock, logo, year caption, statistic or customer data. The in-image dates 02-27-2016 (XTRA-11) and 9/3/2003 (XTRA-13) are original pixels, and nothing captions them.

## Hand-off constraints and how they were verified
1. **Release.** state.json and delivery.json release_status are `blocked`, with unresolved_gates R11 and R14. Nothing was placed in a cleared-media bin.
2. **XTRA-12 whole and only uniformly scaled.** Every variant renders the whole 334 × 361 figure. The collage uses 1.2695 on x, with a y difference of 0.3 px or less. focus-data-entry uses exactly 2×. The reduced panels use 0.554. There is no crop or rotation. Verification: 0 differing pixels in each placed rectangle, 0 non-matching mat-ring pixels, and no text or frame box intersecting it. The credit "Used with permission from Microsoft." is present in the SVG text of all four variants and legible at 720p. The same checks pass for XTRA-11 and XTRA-13.
3. **Dates.** No capture date appears in authored text. The only date-like string in on-screen text is "1998", from "(December 1998)" in XTRA-12's verbatim Microsoft credit: the figure's publication date (placement-checks.json). XTRA-11's credit omits its software year "1993" on screen, so the 2016 emulator capture is not read as a 1993 capture.
4. **Per-panel credits and map.** Each credit comes from the upstream `rights.json`: `credit_text` for XTRA-11 and XTRA-12, `credit_text_proposed` for XTRA-13. The only edit is the XTRA-11 year omission, recorded in delivery.json credits. The coordinate map is in `src/layout.json` and delivery.json `panel_map`, with asset ID, source file, SHA-256, x/y/w/h, scale and resampling.
5. **Upstream crops.** Recorded above and in evidence/provenance.json. The originals were used directly, so no upstream crop or resample is inherited.

## Editorial gates (worked, not cleared)
- **R11 (blocked).** Requirement 1 was re-checked against each upstream claim-checks record; VB provenance is documented for all three (P1). The narration's "people with problems … accountants, teachers, small business owners" is not evidenced by these examples (N1). The era fit is partial (E1).
- **R14 (blocked).** All three panels are rights-blocked upstream. The collage is only as releasable as its most restricted panel.

Review questions (full text in evidence/claim-checks.json):
- **XTRA-14-RQ1** — collage release depends on the XTRA-11, XTRA-12-RQ1 and XTRA-13 rights decisions; a fallback recomposition is needed if a panel is cut.
- **XTRA-14-RQ2** — is XTRA-12, a Microsoft wizard-generated documentation sample, acceptable under the "people with problems" framing (War/SCRIPT.md:742, cue 744)? Should the narration be softened?
- **XTRA-14-RQ3** — era fit of a 2016 emulator capture, a 1998 VB6 figure and a 2003 XP capture of a 1999 utility.
- **XTRA-14-RQ4** — on-screen credits: the XTRA-11 year omission, XTRA-13's credit still unapproved, the Microsoft statement valid only if XTRA-12-RQ1 is accepted, and burned-in credits versus the description.
- **XTRA-14-RQ5** — edit use of the collage (about 1.0–1.3× scale) versus the focus variants.

No War/SCRIPT.md edit was made or is required to produce this proof; RQ2 goes to the Writing Lead.

## Reproduction
Run from the repository root on Windows. Set `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` and put that folder first on PATH. Use `C:\Python314\python.exe` explicitly (MSYS2's python.exe has no CairoSVG), and `-B` so no `__pycache__` lands in the asset folder.

```sh
python -B assets/stills/XTRA-14/src/build.py
python -B tools/render/render_assets.py --id XTRA-14
python -B tools/render/qa_browser.py --id XTRA-14
python -B assets/stills/XTRA-14/src/verify.py
python -B tools/render/finish_delivery.py --deliveries-only --id XTRA-14
#   finish_delivery.py overwrites qa.md with generic text: restore this file (git checkout) before the next step
python -B assets/stills/XTRA-14/src/finalize.py
python -B tools/validate_delivery.py --id XTRA-14
python -B tools/validate_pack.py
```

Do not use `build_assets.py --id XTRA-14`, which has no composition for this ticket. Tool versions: Windows 11 10.0.26200, Python 3.14.0, CairoSVG 2.9.1, Pillow 12.3.0, Playwright 1.63.0 with Chromium 153.0.8010.12, ffmpeg 6.0 essentials build (not used for this still). No network access, installs or font files.

## Validator
`python -B tools/validate_delivery.py --id XTRA-14`, run 2026-09-15 after `src/finalize.py` wrote the 33-file inventory. Exit code 0. Output, verbatim:

```json
{
  "id": "XTRA-14",
  "ok": true,
  "errors": [],
  "limitations": [
    "No OCR or visual quality judgment.",
    "No MP4 decode/frame-rate/codec validation; inspect with ffprobe and playback.",
    "No historical, semantic, or legal clearance.",
    "Manual 1080p/720p review remains required."
  ]
}
```

This section was added after that run. finalize.py was then re-run to re-hash this file, and the validator was run again with the same result (see the worker report). `python tools/validate_pack.py`: exit 0, `"errors": []`. The validators' stated limits apply: no OCR, visual, historical or legal judgement.
