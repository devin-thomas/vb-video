# XTRA-05 — Production QA

**Asset:** VB4 IDE anatomy, five labeled panels (script supplement for SCRIPT.md:130–134; War/SCRIPT.md:133–137).
**Production:** produced. **Release:** blocked (R03, R14). Internal proof only, not in any cleared-media bin.
**Reviewer:** none yet. This is the producing agent's self-check, not release approval; release comes from the OPS-04 review deck.

## Delivered
Still asset, 1920 × 1080, no motion, no named cutdown, no one-panel reveal (editor request only). Every file is listed with byte count and SHA-256 in delivery.json.

| Variant | Export | Source | Proofs | Content |
|---|---|---|---|---|
| `clean-workspace` | `exports/clean-workspace.png` | `src/variant-clean-workspace.svg` | `proofs/clean-workspace-720.png` | Whole screenshot in a frame outside its edges; no annotation, no text |
| `five-callouts` | `exports/five-callouts.png`, `exports/poster.png` (byte-identical) | `src/variant-five-callouts.svg` | `proofs/five-callouts-720.png`, `proofs/poster-720.png`, `proofs/five-callouts-1to1-left.png`, `proofs/five-callouts-1to1-right.png` | Same screenshot rectangle, five margin labels, window-frame outlines, leaders |

Also delivered: `exports/contact-sheet.png` (renderer overview); `src/index.html` (offline, deterministic, `window.__ASSET__`, t = 0 shows five-callouts, `showVariant(name)` shows either); `src/layout.json` (placement, targets, all 50 annotation rectangles with the original pixels each covers); `src/build.py`, `src/verify.py`, `src/finalize.py`; `src/build.json`, `src/timeline.json`, `src/brief.json`, `src/copy.txt`; evidence `provenance.json`, `claim-checks.json`, `source-excerpts.md`, `placement-checks.json`, `render-tests.json`, `browser-tests.json`.

## Input and placement
- **Source:** `assets/historical/HIST-02/source/original.png`, read in place, never copied or modified. SHA-256 `065820c55080db7a4d23a2bbba3388d98aa2614837e8dda90b1cf97b82bde565`, 13,081 bytes, 800 × 600, palette PNG. It is WinWorld's "Microsoft Visual Basic 4.0 32 bit - Edit", with title bar "Loan - Microsoft Visual Basic [design]". build.py and verify.py both stop if the hash differs from HIST-02/delivery.json.
- **Placement (both variants):** x = 347, y = 90, 1200 × 900. Uniform scale **1.5×** on both axes (exact, no aspect rounding). There is no crop, rotation, stretch, retouch or zoom-in. The embedded scaled PNG has SHA-256 in `src/layout.json`.
- **Filter:** Pillow `Image.Resampling.BOX` (area average). An integer scale does not fit: 1× is too small for 720p and 2× is 1600 × 1200. So I compared NEAREST, BOX, LANCZOS, and NEAREST-3× followed by a BOX downscale on the Code and Properties windows at 1.44×:
  - NEAREST gave uneven 1 px / 2 px strokes in the pixel fonts.
  - LANCZOS was softer, with faint ringing (as HIST-02 also noted).
  - BOX gave even, crisp strokes, and the NEAREST-3× route looked the same.
  BOX was chosen.
- **Frame:** a #1b2027 mat 6 px wide and a 2 px #343d48 stroke, entirely outside the image, on #111318. This is the same treatment as XTRA-14.

## Annotation (five-callouts only)
- **Labels:** the ticket copy verbatim, in Liberation Sans Bold 40 px, #f1f3f5. They sit in the margins, outside the screenshot and its frame. Multi-word labels are stacked one word per line, with words and capitals unchanged.
  - Left column, right-aligned to x = 291: Toolbox, Form Designer, Code Window.
  - Right column, from x = 1603: Project Explorer, Properties Window.
- **Marks:** each mark is 5 px thick: a 1 px #111318 casing, a 3 px #eab676 core, and another 1 px casing.
  - **Outlines** sit inside each target window's outer boundary, so they cover only that window's frame bevel.
  - **Leaders** are horizontal, on original rows that are desktop teal between the image edge and the target.
  - The Form Designer outline follows the form window's visible edges. It stops 6 px short of the Code Window outline, where the Code window covers the form.

| Target | Original window px (incl.) | Canvas outline box | Leader (canvas) | Original px under outline / leader | What the marks cover |
|---|---|---|---|---|---|
| Toolbox | 4,78 – 67,400 | 353,207 – 449,691 | x 305–353, y 448–453 | 2660 / 16 | toolbox frame band; teal |
| Form Designer | 76,76 – 554,462 (lower right covered) | 461,204 – 1179,784, open: right edge to y 575, bottom edge to x 635 | x 305–461, y 733–738 | 4017 / 304 | form frame band; teal |
| Code Window | 196,327 – 588,562 | 641,581 – 1230,934 | x 305–641, y 891–896 | 4740 / 588 | code window frame band; teal |
| Project Explorer | 600,77 – 797,187 | 1247,206 – 1544,372 | x 1544–1589, y 313–318 | 2305 / 8 | project window frame band; teal |
| Properties Window | 599,338 – 792,567 | 1246,597 – 1536,942 | x 1536–1589, y 793–798 | 3142 / 32 | properties frame band; teal plus 4 px of its own black right edge |

The window edges were measured from the Win95 frame lines in the original. Light #DFD8DF runs mark the top and left edges; black runs mark the right and bottom. Full per-rectangle records are in `src/layout.json` (`annotation_edits`, 50 entries). Pixel-measured records are in `evidence/placement-checks.json`, and there is a summary in delivery.json `annotation_edit_history`.

## Checks actually performed (2026-09-15)
Run from the repository root on branch `ticket/XTRA-05`, created with `git checkout -B ticket/XTRA-05 main` at base 9e6f14a. `git merge-base --is-ancestor main HEAD` succeeded, and all HIST-02 inputs were present.

1. **`python -B assets/stills/XTRA-05/src/build.py`**: passed. Assertions:
   - the HIST-02 hash and bytes match HIST-02/delivery.json, and the source is 800 × 600;
   - the labels equal the manifest copy;
   - no label box meets the screenshot or its frame;
   - labels are inside x 120–1800, y 72–1008 and do not overlap each other;
   - no mark meets a label, and the outlines stay on the image without touching each other.
   The spare horizontal space is 15 px.
2. **`python -B tools/render/render_assets.py --id XTRA-05`**: passed. CairoSVG 2.9.1 rendered poster.png and the two variants at 1920 × 1080, plus proofs/poster-720.png and the contact sheet (`evidence/render-tests.json`). There is no video, as expected for a still.
3. **`python -B tools/render/qa_browser.py --id XTRA-05`**: passed. Chromium 153.0.8010.12 loaded the HTML in memory and checked both SVG files and all 9 text boxes: 0 outside the canvas, no network request, deterministic seeking, no errors (`evidence/browser-tests.json`).
4. **`python -B assets/stills/XTRA-05/src/verify.py`**: `"ok": true` (`evidence/placement-checks.json`). The first run reported a "total" that summed overlapping mark rectangles (37,555). The script now reports the union, and the re-run gives:
   - The HIST-02 hash still equals layout.json and HIST-02/delivery.json.
   - Each SVG embeds exactly one PNG, which decodes to exactly a fresh 1.5× BOX resample of the original.
   - **clean-workspace: 0 differing pixels of 1,080,000** in the placed rectangle, 0 non-matching mat-ring pixels, and no text in the SVG.
   - **five-callouts and poster:** 37,080 pixels changed over the image, **0 outside the declared mark rectangles**.
     - Every leader covers only desktop teal #00787f, except that the Properties leader also covers 4 px of its target's own right edge.
     - Every outline covers only its target's outer frame band (under 4 original px from its edge; the colours are the frame greys, white and black only).
     - 0 pixels break either rule, and the gold core and dark casing are present on every mark.
   - poster.png is byte-identical to five-callouts.png, and the SVG text equals the ticket copy.
   - The script also writes the -720 proofs and the native-pixel halves.
5. **`python -B tools/render/finish_delivery.py --deliveries-only --id XTRA-05`**: exit 0. It wrote the delivery inventory, the state, the ticket appendix, and XTRA-05 rows in review/production-index.json and review/browser-summary.json (diffs checked: only XTRA-05 entries were added). Its generic qa.md (motion, Program.vb excerpts, thumbnail-only review) does not describe this still, so this file replaces it. `python -B assets/stills/XTRA-05/src/finalize.py` then rewrote placement, annotation_edit_history, label_checks, variants, sources, credits, tests, notes and state, and recomputed every hash.
6. **`python -B tools/validate_pack.py`**: exit 0, `"errors": []`.
7. **`python -B tools/validate_delivery.py --id XTRA-05`**: see "Validator" below.

Fonts resolved by fc-match: Liberation Sans Regular and Bold from C:/WINDOWS/fonts. No font files are shipped.

## Manual visual inspection (by the producing agent, Read tool)
- **exports/five-callouts.png and exports/poster.png at 1920 × 1080 (identical bytes).** The whole IDE is visible, from the title bar to the taskbar clock "10:43 PM", with nothing clipped.
  - The labels sit in the dark margins: Toolbox, Form Designer and Code Window on the left; Project Explorer and Properties Window on the right. Each is joined by a gold leader to a gold outline on its window.
  - **Every target is unmistakable.**
    - Toolbox: the outline encloses the icon strip.
    - Form Designer: the outline runs along the LoanSheet form's top, left and right edges and its visible bottom-left edge. It visibly stops short of the Code window's outline, so the two targets read as separate.
    - Code Window: the closed outline is around the active LoanSheet code window.
    - Project Explorer: the outline is around the "Loan" window.
    - Properties Window: the outline is around "Properties - LoanSheet".
  - No mark covers code, menu text, a title, a property row or a toolbox icon. Leaders cross only empty teal desktop. The layout is balanced: three labels on the left, two on the right, all vertically aligned with their targets.
- **proofs/five-callouts-1to1-left.png and -right.png (native pixels).** The mark edges are crisp (rectangle fills, no anti-aliasing), and the 3 px gold core reads clearly against both the teal and the grey frames.
  - The BOX-scaled pixel text is crisp and even: "Private Sub grdPayments_Click()", comments in green, the Properties values (4815, 2655, grdPayments), "LOAN.FRM  LoanSheet" and the menu items.
  - The Form Designer leader meets the form's left edge beside the "Show Amortiza" button without touching the button.
- **exports/clean-workspace.png at 1920 × 1080.** This is the same framed screenshot with no gold, no labels and no text. The frame is outside the image.
- **proofs/five-callouts-720.png, proofs/poster-720.png, proofs/clean-workspace-720.png (1280 × 720).**
  - **All five labels are legible**, at about 27 px bold on dark ground.
  - **Every target is still unmistakable.** Outlines and leaders are about 2 px of gold and clearly visible. The Form Designer / Code Window separation is still visible.
  - The screenshot is at an effective 1.0×, and its UI text is readable: title bar, menu names, "View Form / View Code", "LOAN.FRM", every code line, Properties names and values, "Options / Down Payment / Loan Length". The Properties grid is the smallest text but still readable.
- **exports/contact-sheet.png.** Poster, clean-workspace and five-callouts thumbnails, correctly named; no swapped files.
- **Content:** no painted or invented UI, no caption over the screenshot, no on-screen credit, no year, no remote font or CDN, no private data. The taskbar shows only Start, the IDE task and a clock.

## Hand-off constraints and how they were verified
1. **Whole screenshot, uniform scale.** Exactly 1.5× BOX, 1200 × 900, with no crop, rotation, stretch, retouch or zoom-in, in both variants. clean-workspace has 0 differing pixels against a fresh resample (verify.py). In five-callouts every changed pixel is inside a declared mark.
2. **Annotations.** clean-workspace has nothing over the screenshot. In five-callouts all label text is outside the screenshot and its frame (build.py box checks, and qa_browser shows no out-of-canvas text). Only outlines on window frames and leaders over desktop cross onto the image. The edit history, with every mark's type, coordinates, colours and the original pixels it covers, is in `src/layout.json`, `evidence/placement-checks.json`, `evidence/provenance.json` and delivery.json. RQ-HIST-02-3 is carried forward as XTRA-05-RQ1.
3. **Exact copy.** The labels are verbatim, including "Project Explorer" (asserted against the manifest in build.py and against the SVG text in verify.py). Each label was checked against the screenshot and against Microsoft KB articles that apply to VB 4.0 (`evidence/claim-checks.json` label_checks, `evidence/source-excerpts.md` §6):
   - Toolbox, Properties Window and Code Window: verified.
   - Form Designer: target verified; the name is VB6-documented wording.
   - Project Explorer: target verified; the name is later-version terminology. The VB 4.0-only KB article Q140350 says "Project window".
   This goes to the Writing Lead as XTRA-05-RQ2. No UI was painted.
4. **Rights and credit.** HIST-02's record is carried forward in delivery.json credits: credit null, proposed credit marked "proposed, not approved", rights unresolved. Nothing is burned in, because source.json says the Microsoft sentence must not be used before RQ-HIST-02-1 is decided (XTRA-05-RQ4). The "Loan" project question is carried as XTRA-05-RQ5. Release is blocked on R03 and R14.
5. **R03.** Worked against the screenshot (claim-checks R03 V1, N1, L1–L4, E1, P1):
   - the toolbox is on the left and the properties panel on the right, as narrated;
   - the form is centre-left and a populated sample, not a centred blank window;
   - the Code window is in front of the form, not behind it.
   The mismatch goes to the Writing Lead as XTRA-05-RQ3. No script edit was made.

## Editorial gates (worked, not cleared)
- **R03 (blocked):** panel-name terminology (RQ2) and the fit between narration and layout (RQ3).
- **R14 (blocked):** HIST-02's rights are unresolved, callout marks may count as alteration (RQ1), and the credit placement is open (RQ4) along with third-party content (RQ5).

Review questions (full text in `evidence/claim-checks.json`):
- **XTRA-05-RQ1 (Devin, rights/edit; carries RQ-HIST-02-3):** are callout outlines and leaders over a whole Microsoft screenshot acceptable, or should the edit use clean-workspace with labels whose leaders stop at the image edge?
- **XTRA-05-RQ2 (Writing Lead; carries RQ-HIST-02-4):** "Project Explorer" or VB4's "Project window"? War/SCRIPT.md:133 already reads "Project Window" (commit 9e6f14a), while the ticket copy still says "Project Explorer". A lower-priority note covers "Form Designer" as well.
- **XTRA-05-RQ3 (Writing Lead):** the narration describes a centred blank form with the code window "behind", but the capture shows a centre-left sample form with the Code window in front.
- **XTRA-05-RQ4 (Devin, credits; carries RQ-HIST-02-1):** where the Microsoft statement goes if that permission basis is chosen. There is no room inside the safe area at 1.5×.
- **XTRA-05-RQ5 (Devin, rights; carries RQ-HIST-02-2):** third-party "Loan" project content.
- **XTRA-05-RQ6 (Devin, edit):** the cue says "Side-by-side". The two stills share one screenshot rectangle for a cut or dissolve; is a split-screen wanted instead?

## Reproduction
Run from the repository root on Windows:
- Set `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` and put that folder first on PATH.
- Use `C:\Python314\python.exe` explicitly, because MSYS2's python has no CairoSVG.
- Pass `-B` so no `__pycache__` lands in the asset folder.

```sh
python -B assets/stills/XTRA-05/src/build.py
python -B tools/render/render_assets.py --id XTRA-05
python -B tools/render/qa_browser.py --id XTRA-05
python -B assets/stills/XTRA-05/src/verify.py
python -B tools/render/finish_delivery.py --deliveries-only --id XTRA-05
#   finish_delivery.py overwrites qa.md with generic text: restore this file (git checkout) before the next step
python -B assets/stills/XTRA-05/src/finalize.py
python -B tools/validate_delivery.py --id XTRA-05
python -B tools/validate_pack.py
```

Do not use `build_assets.py --id XTRA-05`, which has no composition for this ticket.

Tool versions: Windows 11 10.0.26200, Python 3.14.0, CairoSVG 2.9.1, Pillow 12.3.0, Playwright 1.63.0 with Chromium 153.0.8010.12. ffmpeg was not used for this still. No installs and no font files. Network use was limited to read-only lookups of archived Microsoft KB and VB6 documentation pages for the label checks; nothing was downloaded into the repository.

## Validator
I ran `python -B tools/validate_delivery.py --id XTRA-05` on 2026-09-15, after `src/finalize.py` wrote the 27-file inventory. Exit code 0. Output, verbatim:

```json
{
  "id": "XTRA-05",
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

This section was added after that run. finalize.py was then re-run to re-hash this file, and the validator was run again before commit with the same result (see the worker report). `python -B tools/validate_pack.py`: exit 0, `"errors": []`. The validators' stated limits apply: no OCR, visual, historical or legal judgement.
