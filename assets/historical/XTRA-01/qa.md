# XTRA-01 — Production QA

**Production:** produced. **Release:** blocked. R14 is open because the cover is copyrighted and no license or permission exists (`evidence/rights.json`).

This is a script supplement for `SCRIPT.md:49` (original family SCRIPT-SUPPLEMENT). It is not a row of the categorized asset plan.

## Delivered
- `source/original.jp2`: the unmodified Internet Archive page image of the front cover of *Visual Basic Programmer's Journal*, March 1996, Vol. 6, No. 3 (Fawcette Technical Publications). 2362×3235, 1,595,357 bytes, SHA-256 `e8f26ad7…adaa46`. This is the `original` variant.
- `exports/editorial-frame.png`: 1920×1080 pillarboxed framing of the whole cover. This is the `editorial-frame` variant.
- `proofs/editorial-frame-720.png`: 1280×720 review proof.
- `src/render_frame.py`: the reversible framing script. `evidence/framing.json` holds the exact geometry.
- `evidence/source.json`, `rights.json`, `provenance.json`, `source-excerpts.md`, `claim-checks.json`.
- Every file except delivery.json and state.json is listed with bytes and SHA-256 in `delivery.json`.

Still asset: no duration, no fps, no motion. It holds for editorial timing.

## Source and identity
- Item page: https://archive.org/details/visual_basic_programmers_journal-1996_03 (ark:/13960/s2msp7x5gnb). Individual uploader, published on the archive 2024-04-01. No license field.
- File: leaf 0 of the item's "Single Page Processed JP2 ZIP", `…_jp2.zip/…_jp2/…_0000.jp2`. The archive derived it from the uploader's CBR scan (300 ppi). The full URL is in `evidence/source.json`.
- Accessed 2026-09-15. Downloaded 20:29:42 UTC by anonymous HTTPS GET, with no account, login, CAPTCHA, payment or terms acceptance.
- Identity was verified from the scan itself, not from the catalog title:
  - The cover's printed date line reads "A FAWCETTE TECHNICAL PUBLICATION, MARCH 1996 VOL. 6, NO. 3".
  - Leaf 4 (the contents page) repeats the same image with the date line and the caption for Keith Pleas' registry article.
  - Leaf 4 also carries the ISSN 1075-1955 publication statement naming Fawcette Technical Publications.
  - The issue's content is VB4-era: VB4 add-on ads, Jet 3.0, and letters about 16-bit versus 32-bit VB 4.0.
- Cover creator: **not identified**. No photographer or illustrator is credited. The only cover-related credit is for a prop ("Jungle courtesy of Indoor Design Plant Service"). Masthead art staff are recorded as leads only.
- Other candidates checked and rejected (details in `evidence/provenance.json`):
  - VBCD March 1996 and January 1999: CD packaging photos, not magazine covers.
  - VB-CD Quarterly 1995: CD-ROM cover art.
  - The 1996 VBPJ-branded VB4 book.
  - Only one printed VBPJ issue scan was found on the Internet Archive.

## Checks actually performed
- **Identity read from page images** (leaf 0 viewed downscaled and at 1:1 in the export; leaf 4 viewed at half-page crop): passed.
- **Original unmodified:** SHA-256 of `source/original.jp2` equals the downloaded file, before and after rendering (the script asserts it, and it was re-hashed afterwards). Passed.
- **Native dimensions:** 2362×3235 JPEG 2000 RGB, matching `scandata.xml` leaf 0 (origWidth 2362, origHeight 3235, full cropBox). Passed.
- **No stretch:** input aspect 0.730139, scaled 683×936 = 0.729701. The 0.06% difference is integer rounding only. Uniform scale factor 0.289335. Passed.
- **No crop:** the whole page is placed at x=618, y=72 inside the y=72..1008 safe area. Passed.
- **Background untouched outside the cover:** every pixel outside the cover rectangle is #111318, checked programmatically. Passed.
- **No added text, captions, annotations or watermark removal:** passed. The scan has no watermark.
- **Export PNG 1920×1080 and proof 1280×720:** checked with Pillow. Passed.
- **Privacy:** the uploader's email from the public archive metadata is deliberately not copied into any file. No personal data in outputs. Passed.
- **`python tools/validate_delivery.py --id XTRA-01`:** result recorded in the producer report and in `delivery.json` tests.

## Manual visual inspection
- **Full size (1920×1080):** viewed `exports/editorial-frame.png` in full, plus a 1:1 crop of the top of the cover (683×528).
  - The cover sits centered on a dark ground, with its colors and proportions intact.
  - No stretching, and no clipping at any edge. The scan's slight paper edge and a faint vertical crease or scanner line in the left third are both present in the original.
  - The VISUAL BASIC PROGRAMMER'S JOURNAL logo and all cover lines are sharp, and the barcode is complete.
  - The printed date line is legible at 4× zoom of the export ("A FAWCETTE TECHNICAL PUBLICATION, MARCH 1996 VOL. 6, NO. 3"). At 1:1 on screen it is small, about 9 px cap height, and a viewer cannot read it at normal viewing. If the edit wants the date read on screen, that needs a caption or a zoom move, which is an editorial choice.
- **720p (1280×720):** viewed `proofs/editorial-frame-720.png`. The logo, "HACKING THE REGISTRY", the dialog box and all four cover lines stay readable. The date line is not readable at this size.

## Reproduction
From the repository root:
```
curl -sL -o assets/historical/XTRA-01/source/original.jp2 "https://archive.org/download/visual_basic_programmers_journal-1996_03/visual_basic_programmers_journal-1996_03_jp2.zip/visual_basic_programmers_journal-1996_03_jp2%2Fvisual_basic_programmers_journal-1996_03_0000.jp2"
python assets/historical/XTRA-01/src/render_frame.py
python tools/validate_delivery.py --id XTRA-01
```
Check the re-downloaded file's SHA-256 against `e8f26ad7eff39d18119e1e65c68f598965de1ab136ed1a7a568e8b1e85adaa46` before rendering. The archive may re-derive JP2s. If the hash differs, treat the file as a new acquisition and do not relabel it as this one.

Toolchain: Windows-11-10.0.26200-SP0; Python 3.14.0; Pillow 12.3.0 with OpenJPEG 2.5.4; curl 8.18.0 (x86_64-w64-mingw32). The shared render pipeline (`tools/render/*`, CairoSVG) was not used: this asset has no SVG or HTML source. No fonts are used.

## Gates and review questions
- **R14:** blocked (`evidence/claim-checks.json`).
  - Verified by evidence: genuine issue and era; publisher and printed copyright notice; no license on the file; clean access route.
  - Not settled by evidence: permission to use the cover in the video.
- **XTRA-01-Q1 (legal risk; Devin):**
  - The March 1996 VBPJ cover is © Fawcette Technical Publications, all rights reserved. There is no license or permission, and the cover photographer is uncredited.
  - Trade press reports that 1105 Media acquired Fawcette's operating assets in 2007. Whether the back-issue copyrights passed with them is unverified.
  - Options:
    - (a) Use it briefly as editorial commentary under a fair-use judgment, with the credit line in `evidence/rights.json`.
    - (b) Ask the presumed successor (1105 Media) for permission. This is a human action; no agent contacts rights holders.
    - (c) Cut it.
  - Until one of these is chosen, release stays blocked.
- **XTRA-01-Q2 (editorial; Writing Lead or Devin):**
  - The cue says "Magazine covers" (plural). This package delivers one VBPJ cover, the only printed VBPJ issue scan found on the Internet Archive.
  - Is one cover, alongside the MSDN-ad and VB4-IDE assets from other tickets, enough for the montage? Or should more issues be scouted in other archives? Any further scouting would face the same rights question.
  - No `War/SCRIPT.md` change is proposed.

## Reviewer
Produced and inspected by the XTRA-01 worker agent under the Archive Extras Manager. No human media review or rights decision is recorded yet.
