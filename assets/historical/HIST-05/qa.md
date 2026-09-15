# HIST-05 — Production QA

**Production:** produced. **Release:** blocked (R14 rights decision and one authenticity question open). **Reviewer:** none yet; goes to the OPS-04 review deck.

## Delivered
All files are listed with byte count and SHA-256 in delivery.json.

| Variant | File | What it is |
|---|---|---|
| `original` | `source/original.gif` | Byte-identical copy of Wikimedia Commons `File:C64 startup animiert.gif` (360 × 248, 2 frames, 500 ms each, looping). |
| `editorial-frame` | `exports/editorial-frame.png` | 1920 × 1080 still: frame 1 (cursor visible), 3× nearest-neighbour, centred on black. |
| proof | `proofs/editorial-frame-720.png` | 1280 × 720 Lanczos downscale of the export, for 720p review only. |

Evidence: `evidence/source.json` (source record, candidates, search log), `evidence/rights.json`, `evidence/claim-checks.json`, `evidence/provenance.json`, `evidence/source-excerpts.md`, `evidence/framing.json` (exact transform), `evidence/commons-file-page.wikitext` and `evidence/commons-imageinfo.json` (source-page record). Scripts used: `tools/`.

Still asset: no duration, fps, motion or named cutdowns. The hold length is the editor's choice.

## Checks actually performed (2026-09-15)
1. **Integrity against the archive.** SHA-1 of the downloaded file `79ba302dee5ef066edd31d1e66c5f7c728b62699` equals the SHA-1 Commons publishes for the file (imageinfo API). The repo copy's SHA-1 was recomputed after copying (PowerShell `Get-FileHash`) and matches.
2. **Model/version from the source, not appearance.** Both GIF frames viewed at 3× enlargement: `**** COMMODORE 64 BASIC V2 ****` / `64K RAM SYSTEM  38911 BASIC BYTES FREE` / `READY.`, cursor at row 6 column 0 in frame 1. Wording matches the power-on screen on printed page 12 of the Commodore 64 User's Guide (Internet Archive `commodore-64-user-guide`, leaf n27), read from the page image at 3301 × 5100 (the archive OCR is garbled and was not relied on).
3. **Pixel measurement** (`tools/measure.py`). Only palette indices 0 and 1 are used, so the declared transparent index 2 never occurs and no pixel was silently filled. Borders are 20/20/22/23 px. Text sits on the 8-px grid: row 1 columns 4–34, row 3 columns 1–38, row 5 columns 0–5, cursor cell exactly on the grid. **Finding:** the blue screen area is 320 × 203 px, 3 lines more than a 25-row 320 × 200 text screen, so this is not an unaltered hardware-exact frame. Recorded as a review question, not corrected.
4. **Reversibility and no added content** (`tools/verify_reverse.py`, exit 0). Cropping the export at (420,168,1500,912) and downscaling 3× nearest recovers frame 1 pixel for pixel; every 3×3 block is uniform (no blending); all 1,270,080 pixels outside the image are `#000000`; the export contains only `#000000`, `#4242E7`, `#A5A5FF`; the image lies inside x 120–1800 and y 72–1008. No crop, stretch, retouch, watermark removal (none present), text, UI, remote asset or font file.
5. **Manual visual review at full size.** `exports/editorial-frame.png` viewed at 1920 × 1080: all three lines and the cursor are crisp and fully legible; border intact on all four sides; centred; no distortion.
6. **Manual visual review at 720p.** `proofs/editorial-frame-720.png` viewed at 1280 × 720: text and cursor remain clearly legible; no moiré or smearing that changes a character.
7. **Delivery validator.** `python tools/validate_delivery.py --id HIST-05`. Result: see the section below.

Not performed: OCR, legal clearance, a check of Copyright Office records or firmware copyright notices, capture of the frame 0 variant as a separate export (not requested).

## Validator
Command, from the repository root after `tools/build_delivery.py` wrote delivery.json (18 outputs):

```
python -X utf8 tools/validate_delivery.py --id HIST-05
```

Actual output (exit code 0):

```
{
  "id": "HIST-05",
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

Adding this section changed qa.md, so delivery.json was rebuilt and the validator run again before commit; the re-run result is reported in the completion report. The validator checks structure and hashes only; the visual, historical and rights checks are the numbered items above.

## Acquisition notes
- upload.wikimedia.org rate-limited this network (HTTP 429, `Retry-After: 600`) during research; about 19 other workers share it. Requests this worker sent to upload.wikimedia.org:
  - a first download job that retried on 429 before it was stopped: an unknown number of attempts, at most 6, none successful (its log was not captured);
  - 1 HEAD request to read the rate-limit headers (429);
  - a queued one-pass job: `C64_startup_animiert.gif` succeeded at about 20:46 UTC, then `C64_mainscreen.png` got a 429 and the job stopped;
  - after a single wait: `C64_startup_animiert.gif` succeeded again at about 20:50 UTC (identical bytes; this is the delivered copy), and `Commodore_64_Splash.png` got a 429.
- The backup `Commodore_64_Splash.png` was then fetched once from its Wayback Machine raw copy (SHA-1 matches Commons). It was only viewed and is not stored here.
- About 20 further metadata requests went to commons.wikimedia.org (file-page wikitext, imageinfo API, category listing), plus Internet Archive requests for the User's Guide metadata, OCR text, DjVu XML and one page image.
- No account, payment, terms acceptance, CAPTCHA or gated download was involved.

## Reproduction
From the repository root (Windows, PowerShell or Git Bash):

```
python -X utf8 assets/historical/HIST-05/tools/frame.py assets/historical/HIST-05/source/original.gif assets/historical/HIST-05/exports/editorial-frame.png assets/historical/HIST-05/evidence/framing.json --frame 1 --bg "#000000"
python -X utf8 assets/historical/HIST-05/tools/proof720.py assets/historical/HIST-05/exports/editorial-frame.png assets/historical/HIST-05/proofs/editorial-frame-720.png
python -X utf8 assets/historical/HIST-05/tools/verify_reverse.py assets/historical/HIST-05
python -X utf8 assets/historical/HIST-05/tools/measure.py assets/historical/HIST-05/source/original.gif
python -X utf8 assets/historical/HIST-05/tools/build_delivery.py
python tools/validate_delivery.py --id HIST-05
```

`tools/fetch_top.py` is the exact download script used (it contains the one-off wait time from that session). No Cairo, Playwright or shared renderer is needed; the export is a pure Pillow operation.

Tool versions: Python 3.14.0; Pillow 12.3.0; git 2.53.0.windows.1; Windows 11 Pro 10.0.26200.

## Review questions (for the review deck)
1. **Rights (R14).** Accept the Commons public-domain tagging (PD-ineligible, PD-text, PD-font, PD-US-1978-89) for this C64 start-up screen, or require a separate rights review or another source? PD-US-1978-89 asserts the C64 screen content was published without a copyright notice and never registered; that was not verified.
2. **Authenticity.** The image is a community-uploaded digital render ("Own work", capture method undocumented) with a 3-line geometry anomaly. Accept it as the C64 boot screen, or source a photographed real-hardware screen or a documented emulator capture?
3. **Credit line.** Proposed: "C64 startup screen, by Gedeon, via Wikimedia Commons (public domain)". Use as is, or follow another credits style?

## Remaining blockers
None for production. Release blocked on the review questions above. Dependency OPS-01 (shared framing) was not consumed: this archive frame uses no shared template.
