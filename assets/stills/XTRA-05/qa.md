# XTRA-05 — Production QA

**Asset:** VB4 IDE anatomy, five labeled panels (script supplement for SCRIPT.md:130–134; War/SCRIPT.md:133–137).
**Production:** produced. **Release:** blocked (R14, R03). Internal proof only, not in any cleared-media bin.
**Revision:** branch `ticket/XTRA-05-rev` from `ticket/XTRA-05` (8fed9c3), implementing Devin's rulings of 2026-09-15 (relayed by the Render Lane Manager, session vb-8c).
**Reviewer:** none yet. This is the producing agent's self-check, not release approval; release comes from the OPS-04 review deck.

## What changed in this revision
- **Q1 (marks):** Devin allowed callout marks over the Microsoft screenshot. The outline and leader treatment is kept, and no fallback was built. The resolution is recorded in `evidence/claim-checks.json` (R14 M2, XTRA-05-RQ1; carries RQ-HIST-02-3).
- **Q2 (label):** the fifth label is now **Project Window**. `src/build.py` reads the five labels from the War/SCRIPT.md VISUAL cue (line 133, the line containing "VB4 IDE with labeled callouts") and stops unless there are exactly five, each naming its panel in cue order. The override of the ticket's exact-copy payload is recorded in claim-checks `copy_override`: authority War/SCRIPT.md at 9e6f14a, classified as a writing change per Devin. "Form Designer" and its VB6-era note are unchanged (Writing Lead).
- **Q5 (Loan project):** researched. **Conclusion: Microsoft sample** (the VB 4.0 Grid sample). See "Loan project authorship" below.
- **Q6 (side-by-side):** new named variant `side-by-side`, and **poster.png = side-by-side** (see "Poster decision").
- **Q3, Q4:** left open, routed to the Writing Lead and the producer. No art change for either.

## Delivered
Still asset, 1920 × 1080, no motion, no named cutdown, no one-panel reveal (editor request only). Every file is listed with byte count and SHA-256 in delivery.json.

| Variant | Export | Source | Proofs | Content |
|---|---|---|---|---|
| `side-by-side` (poster) | `exports/side-by-side.png`, `exports/poster.png` (byte-identical) | `src/variant-side-by-side.svg` | `proofs/side-by-side-720.png`, `proofs/poster-720.png`, `proofs/side-by-side-1to1-left.png`, `proofs/side-by-side-1to1-right.png` | Clean screenshot left, annotated screenshot right, both whole at native 1.0x; label strip below the annotated side |
| `clean-workspace` | `exports/clean-workspace.png` | `src/variant-clean-workspace.svg` | `proofs/clean-workspace-720.png` | Whole screenshot at 1.5x in a frame outside its edges; no annotation, no text |
| `five-callouts` | `exports/five-callouts.png` | `src/variant-five-callouts.svg` | `proofs/five-callouts-720.png`, `proofs/five-callouts-1to1-left.png`, `proofs/five-callouts-1to1-right.png` | Same 1.5x rectangle, five margin labels, window-frame outlines, leaders |

Also delivered:
- `exports/contact-sheet.png` (renderer overview).
- `src/index.html` (offline, deterministic, `window.__ASSET__`; t = 0 shows the poster variant; `showVariant(name)` shows any of the three).
- `src/layout.json`: label source, placements, targets, and all 120 annotation rectangles (50 five-callouts, 70 side-by-side) with the original pixels each covers.
- `src/build.py`, `src/verify.py`, `src/finalize.py`, `src/build.json`, `src/timeline.json`, `src/brief.json` (manifest row, verbatim), `src/copy.txt` (the rendered labels).
- Evidence: `provenance.json`, `claim-checks.json`, `source-excerpts.md`, `placement-checks.json`, `render-tests.json`, `browser-tests.json`.

## Input and placement
- **Source:** `assets/historical/HIST-02/source/original.png`, read in place and never modified. SHA-256 `065820c55080db7a4d23a2bbba3388d98aa2614837e8dda90b1cf97b82bde565`, 13,081 bytes, 800 × 600, palette PNG with only IHDR/PLTE/IDAT/IEND chunks. It is WinWorld's "Microsoft Visual Basic 4.0 32 bit - Edit", title bar "Loan - Microsoft Visual Basic [design]". build.py and verify.py both stop if the hash differs from HIST-02/delivery.json.
- **clean-workspace and five-callouts:** x = 347, y = 90, 1200 × 900, uniform **1.5×** with Pillow `Image.Resampling.BOX` (area average). The filter comparison is unchanged from the first production: NEAREST gave uneven 1 px / 2 px strokes, LANCZOS was softer with faint ringing, and BOX gave even, crisp strokes.
- **side-by-side:** both screenshots whole at **native 1.0×** (800 × 600). **Filter: none.** The HIST-02 PNG bytes are embedded unchanged and drawn 1:1; verify.py confirms each embed is byte-identical to the HIST-02 file. Placements:
  - clean (left): x = 127, y = 156 (frame 120–934);
  - annotated (right): x = 976, y = 156 (frame 969–1783);
  - the gap between the frames is 35 px.

  The pair fills the safe width exactly, from the clean frame at x = 120 to the outer right rail at x = 1800.
  - **Why 1.0×:** two 800 px screenshots plus two 7 px frames take 1,628 of the 1,680 px safe width. The rest carries the left gutter rails and 8 px clearance to the clean frame (on the left) and the right rails (on the right), so no larger scale fits both. 1.0× is also the one scale needing no resampling, so the pixel fonts are the original pixels.
- **Frame:** a #1b2027 mat 6 px wide and a 2 px #343d48 stroke, entirely outside each image, on #111318. This is the same treatment as XTRA-14.

## Labels
Read at build time from `War/SCRIPT.md:133` (SHA-256 at build `874e019d002739bb61389329e04cbfc6202d7461782fb947436d90eb1ce2d32c`):

> **[VISUAL: Side-by-side — the VB4 IDE with labeled callouts: Form Designer, Toolbox, Properties Window, Code Window, Project Window.]**

Rule in build.py:
- There must be exactly one line containing "VB4 IDE with labeled callouts".
- The labels are the comma-separated list after "labeled callouts:", and there must be exactly five, none empty.
- In cue order, each label must contain its panel word: form, toolbox, propert, code, project. A reordered cue therefore stops the build instead of labelling the wrong window.

verify.py re-reads the cue and fails if the labels changed since the build. The only difference from the ticket copy is "Project Explorer" → "Project Window".

## Annotation
All label text in both annotated variants sits outside every screenshot and frame. Marks are filled rectangles, each a gold #eab676 core with a #111318 casing.

### five-callouts (1.5×)
Geometry is unchanged from the first production; the only difference is the label "Project Window" in place of "Project Explorer".
- Labels are Liberation Sans Bold 40 px in the side margins. Multi-word labels are stacked one word per line.
  - Left column, right-aligned to x = 291: Toolbox, Form Designer, Code Window.
  - Right column, from x = 1603: Project Window, Properties Window.
- Marks are 5 px: a 1 px casing, a 3 px core, and a 1 px casing.

| Target | Original window px (incl.) | Canvas outline box | Leader (canvas) | Original px under outline / leader | What the marks cover |
|---|---|---|---|---|---|
| Toolbox | 4,78 – 67,400 | 353,207 – 449,691 | x 305–353, y 448–453 | 2660 / 16 | toolbox frame band; teal |
| Form Designer | 76,76 – 554,462 (lower right covered) | 461,204 – 1179,784, open | x 305–461, y 733–738 | 4017 / 304 | form frame band; teal |
| Code Window | 196,327 – 588,562 | 641,581 – 1230,934 | x 305–641, y 891–896 | 4740 / 588 | code window frame band; teal |
| Project Window | 600,77 – 797,187 | 1247,206 – 1544,372 | x 1544–1589, y 313–318 | 2305 / 8 | project window frame band; teal |
| Properties Window | 599,338 – 792,567 | 1246,597 – 1536,942 | x 1536–1589, y 793–798 | 3142 / 32 | properties frame band; teal plus 4 px of its own black right edge |

### side-by-side (1.0×, right screenshot)
- **Marks are 4 px:** a 1 px casing, a 2 px core, and a 1 px casing. At 1.0× the Win95 outer window frame is exactly 4 px: pixel probe offsets 0–3 are frame colours, while offset 4 is already title bar or window content on some windows. So each outline covers only the frame.
- **Each leader has three parts:**
  - an **exit** segment over desktop teal, original rows `leader_y−2 … leader_y+1` (all teal, checked from pixels), running from the target's outline to the image edge;
  - a vertical **rail** in the dark gutter outside the image;
  - a **run** below the screenshot to the label.
- **No crossings.** The innermost rail belongs to the lowest exit, and inner rails turn first, so no leader crosses another.
- **Labels:** Liberation Sans Bold 40 px, one line each, in three rows below the annotated screenshot.
  - Left group starts at x = 1000: Code Window, Form Designer, Toolbox.
  - Right group ends at x = 1752: Properties Window, Project Window.
- **Occlusion gap:** the Form Designer outline stops 5 px short of the Code Window outline.

| Target | Canvas outline box | Exit (canvas rows) | Rail x | Label box | Original px under outline / leader | What the marks cover |
|---|---|---|---|---|---|---|
| Toolbox | 980,234 – 1044,557 | y 394–397, from x 942 | 942–946 | 1000,885 – 1153,931 | 3032 / 16 | toolbox frame band; teal (orig x 0–3) |
| Form Designer | 1052,232 – 1531,619, open (right edge to y 478, bottom edge to x 1167) | y 584–587, from x 952 | 952–956 | 1000,831 – 1281,877 | 4860 / 304 | form frame band; teal (orig x 0–75) |
| Code Window | 1172,483 – 1565,719 | y 689–692, from x 962 | 962–966 | 1000,777 – 1262,823 | 4968 / 784 | code window frame band; teal (orig x 0–195) |
| Project Window | 1576,233 – 1774,344 | y 304–307, to x 1800 | 1796–1800 | 1454,831 – 1752,877 | 2408 / 8 | project window frame band; teal (orig x 798–799) |
| Properties Window | 1575,494 – 1769,724 | y 624–627, to x 1790 | 1786–1790 | 1392,777 – 1752,823 | 3328 / 28 | properties frame band; teal (orig x 793–799) |

The per-rectangle records are in `src/layout.json` (`annotation_edits`). Pixel-measured records are in `evidence/placement-checks.json`, with a per-variant summary in delivery.json `annotation_edit_history`.

## Poster decision
**poster.png = side-by-side.** At 720p (`proofs/side-by-side-720.png`, also inspected as 2× nearest-neighbour zooms of both halves in the worker scratchpad):
- **Labels:** all five are legible, at about 27 px bold, white on dark ground.
- **Targets:** every target is unmistakable.
  - The gold outline shows on each window: toolbox strip, LoanSheet form, Code window, "Loan" project window, and Properties window.
  - Each leader can be traced from its label along its rail to the exit over teal, and into that outline.
  - The three left rails are about 7 px apart at 720p and stay separate. They turn into their rows in the same top-to-bottom order as their exits enter the image from the bottom up: Code Window, Form Designer, Toolbox.
  - The Form Designer outline stops visibly short of the Code Window outline.
- **The criterion is met.** The trade-off, recorded for the edit: in side-by-side the screenshot's own UI text is at 0.67× effective at 720p, smaller and softer than in five-callouts (1.0× effective). It is still readable: menus, "LOAN.FRM", code lines, and Properties names. five-callouts is kept for the case where the edit wants the larger screenshot.

## Checks actually performed (2026-09-15)
Run from the worktree root on branch `ticket/XTRA-05-rev`, created with `git checkout -B ticket/XTRA-05-rev ticket/XTRA-05`:
- HEAD was 8fed9c3.
- `git merge-base --is-ancestor main HEAD` succeeded (main = 9e6f14a), so no merge was needed.
- All the required XTRA-05 inputs were present.

1. **`python -B assets/stills/XTRA-05/src/build.py --id XTRA-05`**: passed.
   - The HIST-02 hash and bytes match its delivery.json, and the source is 800 × 600.
   - Five labels were read from War/SCRIPT.md:133, each naming its panel.
   - five-callouts: the first production's box checks pass, with 15 px spare.
   - side-by-side:
     - the two frames do not overlap (gap 35 px) and sit in the safe area;
     - no label meets either screenshot or frame, and the labels sit inside 120–1800 × 72–1008 without overlapping;
     - no mark meets the clean screenshot or its frame, a label, or another target's mark;
     - the outlines stay on the annotated screenshot;
     - each left rail is ≥ 8 px from the clean frame.
2. **`python -B tools/render/render_assets.py --id XTRA-05`**: passed. CairoSVG 2.9.1 rendered poster.png and the three variants at 1920 × 1080, plus proofs/poster-720.png and the contact sheet. There is no video.
3. **`python -B tools/render/qa_browser.py --id XTRA-05`**: passed. Chromium 153.0.8010.12 loaded the HTML in memory and checked all 3 SVG files and all 14 text boxes: 0 outside the canvas, offline, deterministic seeking, no errors.
4. **`python -B assets/stills/XTRA-05/src/verify.py --id XTRA-05`**: `"ok": true` (`evidence/placement-checks.json`).
   - **Source:** the HIST-02 hash still equals layout.json and HIST-02/delivery.json, and the War/SCRIPT.md cue is unchanged since the build.
   - **Embeds:** each SVG embeds exactly one PNG per declared placement (1, 1, 2). Each decodes to exactly a fresh resample at its scale, and both 1.0× embeds are byte-identical to the HIST-02 file.
   - **Clean placements (0 differing pixels each):**
     - clean-workspace: 0 of 1,080,000;
     - side-by-side left screenshot: 0 of 480,000;
     - 0 non-matching mat-ring pixels in both.
   - **Annotated placements (changed pixels only inside declared marks):**
     - five-callouts: 37,080 pixels changed, 0 outside marks;
     - side-by-side right screenshot: 19,736 pixels changed, 0 outside marks;
     - mat ring changed only where a declared mark crosses it (0 elsewhere);
     - every leader covers only desktop teal #00787f or its own target;
     - every outline covers only its target's outer frame band (< 4 original px from its edge);
     - 0 pixels break either rule, and the core and casing colours are present on every mark.
   - **Gold audit, whole export:**
     - clean-workspace: 0 gold pixels;
     - five-callouts: 22,872 gold pixels, equal to the declared core area, 0 outside declared cores;
     - side-by-side: 13,586 gold pixels, equal to the declared core area, 0 outside declared cores, **0 on the clean screenshot or its frame**.
   - **No-overlap check** (build.check_sbs, re-run on the stored layout): pass.
   - **Poster and labels:** poster.png is byte-identical to side-by-side.png, and the SVG label text equals the script cue in both annotated variants.
   - **Proofs:** the script writes the -720 proofs for all three variants and the native-pixel halves of five-callouts and side-by-side.
5. **`python -B tools/render/finish_delivery.py --deliveries-only --id XTRA-05`**: exit 0. It wrote the generic delivery, the state, the ticket appendix, and the XTRA-05 rows in `review/production-index.json` and `review/browser-summary.json`.
   - Diffs checked: the only content change outside the asset folder is the XTRA-05 browser-summary row (svg_files_checked 2 → 3, text_boxes_checked 9 → 14). The ticket appendix and production-index row are unchanged in content.
   - Its generic qa.md does not describe this still, so this file replaces it.
6. **`python -B assets/stills/XTRA-05/src/finalize.py --id XTRA-05`**: rewrote the placement, poster mapping, annotation history, label source and checks, variants, sources, credits, tests, notes and state, and re-hashed the inventory.
7. **`python -B tools/validate_delivery.py --id XTRA-05`** and **`python -B tools/validate_pack.py`**: see "Validator" below.

Fonts resolved by fc-match: Liberation Sans Regular and Bold from C:/WINDOWS/fonts. No font files are shipped.

## Manual visual inspection (by the producing agent, Read tool)
- **exports/side-by-side.png and exports/poster.png at 1920 × 1080 (identical bytes).**
  - Both screenshots are whole, from the title bar to the "10:43 PM" clock, with nothing clipped. At 1.0× the pixel text is crisp in both.
  - The left screenshot carries no gold and no text.
  - On the right, gold outlines sit on the toolbox strip, the LoanSheet form (stopping short of the Code window), the Code window, the "Loan" project window and "Properties - LoanSheet".
  - Leaders leave over empty teal. Three rails run down the gutter between the screenshots, clear of the clean frame, and two run down the right edge. Each run ends at its label in the strip below.
  - No mark covers code, a title, a menu, a property row or a toolbox icon. The dark area below the clean screenshot is empty.
- **proofs/side-by-side-1to1-right.png and -left.png (native pixels).**
  - The 2 px gold core reads clearly on teal and on the grey frames.
  - Mark edges are crisp rectangles.
  - The exit leaders touch only teal: Toolbox between the image edge and the toolbox, Form Designer beside "Show Amortiza", Code Window below the form.
  - The left half shows the clean screenshot untouched, with the rail stubs of the right half starting past its frame.
- **exports/five-callouts.png at 1920 × 1080.** The same composition as before with "Project Window" on the right; every target is unmistakable, and no mark covers text.
- **exports/clean-workspace.png at 1920 × 1080.** The framed screenshot only: no gold, no labels, no text.
- **proofs/side-by-side-720.png, proofs/poster-720.png (1280 × 720), plus 2× zooms.** See "Poster decision": all labels are legible and every target is unmistakable.
- **proofs/five-callouts-720.png.** All five labels are legible at about 27 px, and every target is still unmistakable. The screenshot's UI text is readable at 1.0× effective.
- **proofs/clean-workspace-720.png.** Screenshot UI text is readable, and there are no marks.
- **exports/contact-sheet.png.** The poster (side-by-side), clean-workspace, five-callouts and side-by-side thumbnails are correctly named, with no swapped files.
- **Content:** no painted or invented UI, no caption over any screenshot, no numbered markers, no on-screen credit, no year, no remote font or CDN, no private data.

## Loan project authorship (XTRA-05-RQ5, carries RQ-HIST-02-2)
**Microsoft sample (evidence: KB Q150726 and three VB 4.0 CD contents listings).** Full record, with URLs, access dates, quotes and page hashes, is in `evidence/claim-checks.json` → `loan_project_research` and `evidence/source-excerpts.md` §7.
1. **Microsoft KB Q150726, "INFO: Files Installed with All Editions of Visual Basic 4.0"** (VB 4.0 32-bit Standard/Professional/Enterprise; last modified 11-JAN-2001).
   - Under "F. Samples", "All Editions", it lists `loan.frm*`, `loan.frx*` and `loan.vbp*` in `\vb\samples\grid`.
   - The asterisk marks files that are also installed on a 16-bit platform.
2. **archive.org VB 4.0 Enterprise item** (1996), disc contents listing: `VB/SAMPLES/GRID/LOAN.FRM` 31,035 bytes, `LOAN.FRX` 2,336 bytes, `LOAN.VBP` 382 bytes, dated 1996-01-12.
3. **archive.org VB 4.0 Enterprise item** (1995), listing: the same three files at the same sizes, dated 1995-08-15.
4. **archive.org VB 4.0 Professional 4.0a CD**, listing: the same files at the same sizes, dated 1996-01-11.
5. **The capture itself:** the project is named "Loan", the form file is LOAN.FRM, and the selected control is a Grid.
6. **Negative checks:**
   - KB Q153838 and Q173840, returned by filename searches, contain no "loan" text.
   - 16 web searches found no attribution of a Loan / LoanSheet / grdPayments project to anyone other than Microsoft, and no VB3 LOAN.MAK listing.

**Limit:** LOAN.FRM's text was not compared with the form's contents (LoanSheet, grdPayments, cmdCalcAmort, menus), because that would mean extracting a file from a disc image, which was not done.

**Effect:** there is no third-party content concern, so RQ5 is no longer a review question. **This does not clear release**: R14 still depends on RQ-HIST-02-1. The HIST-02 record was not edited; its RQ-HIST-02-2 is answered by this evidence for the producer to carry.

## Editorial gates (worked, not cleared)
- **R03 (blocked):**
  - "Form Designer" is VB6-documented wording (the XTRA-05-RQ2 remaining note, Writing Lead).
  - The narration's centred blank form and the code window "behind" do not match the capture (XTRA-05-RQ3, Writing Lead).
  - Every label has a verified target, and "Project Window" is the VB 4.0 Microsoft term (KB Q140350).
- **R14 (blocked):**
  - Blocked on the permission basis (RQ-HIST-02-1, upstream) and the credit placement (XTRA-05-RQ4, producer).
  - Marks are allowed (RQ1, Devin).
  - The Loan project is Microsoft content (RQ5, evidence).

## Review questions
Full text is in `evidence/claim-checks.json`.

| ID | For | Status |
|---|---|---|
| XTRA-05-RQ1 (carries RQ-HIST-02-3) | Devin | **Resolved** 2026-09-15: callout marks over the whole Microsoft screenshot allowed; outline and leader treatment kept; no fallback. |
| XTRA-05-RQ2 (carries RQ-HIST-02-4) | Writing Lead | **Partly resolved.** Project part resolved (Devin, writing change): "Project Window" from War/SCRIPT.md:133, derived by build.py. Still open: the "Form Designer" wording note. |
| XTRA-05-RQ3 | Writing Lead (routed by Devin) | **Open.** The narration says the form is a centred blank window with the code window "behind"; the capture shows a centre-left populated Microsoft sample with the Code window in front. Art unchanged. |
| XTRA-05-RQ4 (carries RQ-HIST-02-1) | Producer (routed by Devin) | **Open.** Where the "Used with permission from Microsoft." statement goes if that basis is chosen. side-by-side has an empty dark area below the clean screenshot inside the safe area (about x 120–935, y 770–1008) that could hold an on-screen line without re-layout. The 1.5× variants have no room. Art unchanged. |
| XTRA-05-RQ5 (carries RQ-HIST-02-2) | none | **Resolved by evidence:** Microsoft VB 4.0 Grid sample. Not a review question any more; release still depends on RQ-HIST-02-1. |
| XTRA-05-RQ6 | Devin | **Resolved** 2026-09-15: side-by-side variant added; poster = side-by-side. |

Upstream and not owned here: **RQ-HIST-02-1** (the rights basis for the WinWorld capture) keeps R14 blocked.

## Reproduction
Run from the repository root on Windows:
- Set `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` and put that folder first on PATH.
- Use `C:\Python314\python.exe` explicitly, because MSYS2's python has no CairoSVG and the bare `python` on PATH has no Pillow.
- Pass `-B` so no `__pycache__` lands in the asset folder.
- Always pass `--id XTRA-05`.

```sh
python -B assets/stills/XTRA-05/src/build.py --id XTRA-05
python -B tools/render/render_assets.py --id XTRA-05
python -B tools/render/qa_browser.py --id XTRA-05
python -B assets/stills/XTRA-05/src/verify.py --id XTRA-05
python -B tools/render/finish_delivery.py --deliveries-only --id XTRA-05
#   finish_delivery.py overwrites qa.md with generic text: restore this file (git checkout) before the next step
python -B assets/stills/XTRA-05/src/finalize.py --id XTRA-05
python -B tools/validate_delivery.py --id XTRA-05
python -B tools/validate_pack.py
```

Do not use `build_assets.py --id XTRA-05`, which has no composition for this ticket. Never run finish_delivery.py without `--id`. A change to the War/SCRIPT.md cue flows into the labels on the next build.py run. If the new labels no longer fit the layout, build.py stops with the failing check.

**Tool versions:** Windows 11 10.0.26200, Python 3.14.0, CairoSVG 2.9.1, Pillow 12.3.0, Playwright 1.63.0 with Chromium 153.0.8010.12. ffmpeg was not used for this still. No installs and no font files.

**Network:** read-only lookups with a generic browser User-Agent:
- archived Microsoft KB and VB6 documentation pages (label checks);
- archived KB articles and archive.org item metadata and disc contents listing pages (Loan authorship).

Nothing was downloaded into the repository. No installers, disc images or files from inside disc images were fetched, and no accounts or terms were used.

## Validator
I ran `python -B tools/validate_delivery.py --id XTRA-05` on 2026-09-15, after `src/finalize.py --id XTRA-05` wrote the 32-file inventory. Exit code 0. Output, verbatim:

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

`python -B tools/validate_pack.py`: exit 0, `"errors": []` (130 asset tickets, 4 coordination tickets, 74 visual cues). This section was added after that run, so finalize.py was re-run to re-hash this file, and the delivery validator was run again before commit (result in the worker report). The validators' stated limits apply: no OCR, visual, historical or legal judgement.
