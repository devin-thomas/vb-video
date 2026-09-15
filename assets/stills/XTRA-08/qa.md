# XTRA-08 — Production QA

**Production:** produced. **Release:** blocked (R15, review questions Q1–Q5).

## Delivered
Still asset, 1920 × 1080, no motion. Every file is listed with byte count and SHA-256 in delivery.json.

- `exports/poster.png`: the clean five-tile lineup (source `src/scene.svg`, also `src/scene-0000.svg`).
- `exports/lineup.png`: named variant `lineup` from the ticket. It is the same clean class photo, byte-identical to the poster (source `src/variant-lineup.svg`).
- `exports/vb-focus.png`: optional variant `vb-focus`, the ticket's "focused-VB overlay". It adds a blue outline and accent strip to the Visual Basic 4 tile only (source `src/variant-vb-focus.svg`).
- `src/index.html`: offline, deterministic HTML (`window.__ASSET__`, still at t = 0).
- `src/copy.txt`: the exact five tile names.
- `src/build.py`: the authoring script. `src/build.json` and `src/timeline.json` hold build and timing metadata; `src/brief.json` holds the ticket brief.
- `proofs/poster-720.png`, `proofs/lineup-720.png`, `proofs/vb-focus-720.png`: 1280 × 720 downscales used for review.
- `exports/contact-sheet.png`: an overview sheet written by the renderer.

Timing: no named cutdown. All stills hold for editorial timing. The variants share one geometry, so the edit can dissolve from the lineup to vb-focus without anything moving.

## Checks actually performed (2026-09-15)
- `python assets/stills/XTRA-08/src/build.py`: sources authored. The script asserts that the tile names equal the ticket copy. It picks the largest shared even type size (60 px down to 34 px) at which every name fits its tile in at most two lines: 40 px. It also asserts every text line is inside the safe area. The first render attempt failed because `proofs/` did not exist, so the script now creates `exports/`, `evidence/` and `proofs/`, then reran cleanly.
- `python tools/render/render_assets.py --id XTRA-08`: CairoSVG 2.9.1 rendered poster.png, lineup.png and vb-focus.png at 1920 × 1080 and wrote proofs/poster-720.png (evidence/render-tests.json). No video, as expected for a still.
- Pillow 12.3.0 LANCZOS resize of exports/lineup.png and exports/vb-focus.png to proofs/lineup-720.png and proofs/vb-focus-720.png. All three proofs were confirmed to be 1280 × 720 and all three exports 1920 × 1080.
- `python tools/render/qa_browser.py --id XTRA-08`: installed Chromium 153.0.8010.12 loaded the HTML in memory. 4 SVG files and 24 text boxes checked; no text left the canvas, no network request was made, seeking was deterministic, and there were no errors (evidence/browser-tests.json).
- `python tools/render/finish_delivery.py --deliveries-only --id XTRA-08`: delivery inventory, state and ticket appendix. This file, the manual-review entry in delivery.json and the state notes were then corrected by hand. The generated text described motion, Program.vb excerpts and a thumbnail-only review that do not apply to this asset. delivery.json hashes were then recomputed.
- `python tools/validate_pack.py` and `python tools/validate_delivery.py --id XTRA-08`: see "Validator" below.
- Fonts resolved by fc-match: Liberation Sans Regular and Bold from C:/WINDOWS/fonts. No font files are shipped.

## Manual visual review (by the producing agent)
- **exports/poster.png and exports/lineup.png at full size (identical).** Five tiles sit in one row, equal size, spanning x 120–1800 and centred vertically (y 372–708). Each has the same dark panel fill, grey border and grey top strip. The names are white Liberation Sans Bold at one size, centred: "Visual Basic 4", "Visual C++ 4", "Borland / Delphi 1.0" (the only two-line name), "PowerBuilder", "Java 1.0". Spelling matches the source exactly. "Visual Basic 4" is the widest single line and keeps about 25 px of margin inside its tile. There is no clipping, no heading, no year, logo, number, bracket or ranking. The frame has a wide empty band above and below the row. That is deliberate: it keeps room for a caption or heading in the edit.
- **proofs/poster-720.png and proofs/lineup-720.png.** All five names are readable, at about 27 px cap-to-baseline size at 720p, and the tile edges stay distinct. Delphi's two-line block reads as one name. It sits slightly larger in area than the one-line names, but at the same type size and weight; I don't read it as emphasis.
- **exports/vb-focus.png at full size.** Only the Visual Basic 4 tile changes: a blue 4 px outline and a blue top strip. The other four tiles and every name are unchanged and fully legible; nothing is dimmed.
- **proofs/vb-focus-720.png.** The blue outline is clearly visible, and the other four names remain as readable as in the lineup proof.
- **Transition with DIA-11** (compared with assets/diagrams/DIA-11/exports/poster.png at full size): same #111318 background, #1b2027 panel, #f1f3f5 bold Liberation Sans names, the 120–1800 px content band, and the same tool order as DIA-11's rows. The name size here is 40 px against DIA-11's 32 px tool labels. A dissolve between them does not change palette or type family.

## Content checks
- All five names match the source (SCRIPT.md:609; ticket copy). src/build.py asserts this against the manifest.
- No logos, box art, screenshots or retail packaging. The tiles are original, text-led rectangles.
- Neutral weighting: identical tiles in the lineup, one type size, script order (not a ranking), no bracket, no market share or benchmark, no dates. The script's optional bracket-tournament idea was not used because brackets imply elimination and a winner.
- No sub-lines (year or vendor) were added. Names only is the safest default.
- No remote resources, private information or UI copy.

## Editorial gate R15 (worked, not cleared)
Evidence is in evidence/claim-checks.json, with URLs in evidence/provenance.json:
- Delphi 1.0: 14 February 1995 launch, 15 February RTM (Embarcadero vendor history). Supported.
- Visual Basic 4.0: reviewed as a shipping product in GCN, 2 October 1995. Supported for 1995; exact ship date not confirmed first-party.
- Visual C++ 4.0: documentation catalogued September 1995; Microsoft's 19 February 1996 press release puts the Standard Edition in March 1996. Supported for 1995 by near-primary evidence only.
- PowerBuilder: 5.0 was still due in June 1996 (GCN, 27 May 1996), so the 1995 product was 4.x. The unversioned tile is accurate.
- Java 1.0: shipped 23 January 1996 per Sun's own press release. Java was announced in May 1995 and in alpha from March 1995. A 1996 release in a "1995" lineup; the exports show no year, so this is a framing question.

## Validator
`python tools/validate_delivery.py --id XTRA-08` after the final metadata update: `"ok": true`, `"errors": []`. `python tools/validate_pack.py`: exit 0. The validators' stated limits apply: no OCR, visual, historical or legal judgement.

## Reproduction
Run from the repository root on Windows, with `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` and that folder on PATH. Use `C:\Python314\python.exe` explicitly, because MSYS2's own python.exe comes first on that PATH and has no CairoSVG.

```sh
python assets/stills/XTRA-08/src/build.py
python tools/render/render_assets.py --id XTRA-08
python tools/render/qa_browser.py --id XTRA-08
python tools/render/finish_delivery.py --deliveries-only --id XTRA-08
python tools/validate_delivery.py --id XTRA-08
```

Do not use `build_assets.py --id XTRA-08`, which has no composition for this ticket. finish_delivery.py regenerates a generic qa.md, so re-apply this record afterwards. Make the lineup and vb-focus 720p proofs with Pillow (1280 × 720, LANCZOS). Tool versions: Windows 11 10.0.26200, Python 3.14.0, CairoSVG 2.9.1, Pillow 12.3.0, Playwright 1.63.0 with Chromium 153.0.8010.12, ffmpeg 6.0 essentials build. The full toolchain is in delivery.json.

## Remaining decisions
R15 is blocked, not cleared. The review questions are in evidence/claim-checks.json:
- **Q1 (Writing Lead):** Java 1.0 is a January 1996 release; keep the tile, drop "1.0", or reword War/SCRIPT.md:686?
- **Q2:** keep the unversioned "PowerBuilder" (accurate), or add "4.0" as authored copy?
- **Q3:** Visual C++ 4.0's exact first ship date is not confirmed first-party.
- **Q4:** whether the edit adds a heading, and whether to use vb-focus at "why VB won the market".
- **Q5:** "Borland Delphi 1.0" versus the vendor's product name "Delphi".

No narration sync, sound design, final assembly or independent editorial clearance is certified. Reviewer: none yet. Release comes from the OPS-04 review deck.
