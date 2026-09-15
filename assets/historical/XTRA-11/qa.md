# XTRA-11 QA record: documented VB business application

**Subject:** INVOICE-IT for Windows v2.06, a 1993 shareware invoicing program from Eastern Digital Resources. The publisher's own documents say it was built with Microsoft Visual Basic 2.0 and needs VBRUN200.DLL.
**Source:** Internet Archive item `MEDLEY_SEC90034`, file `screenshot_01.jpg`, accessed 2026-09-15.
**Reviewer:** XTRA-11 worker (agent). This is a self-check, not release approval.
**Production status:** produced. **Release status:** blocked (R14 rights unclear; R11 narration question open).

## Files

| Role | Path | Notes |
|---|---|---|
| Original (untouched) | `source/original.jpg` | 591×423 JPEG, byte-identical to the archive file (SHA-256 `5b89f93e…a318`) |
| Editorial frame | `exports/editorial-frame.png` | 1920×1080 RGB PNG |
| Framing script | `src/make_frame.py` | deterministic; reads only the original |
| 720p proof | `qa/editorial-frame-720p.png` | 1280×720 Lanczos downscale of the export |
| 1:1 proofs | `qa/editorial-frame-1to1-left.png`, `qa/editorial-frame-1to1-right.png` | 960×1080 crops of the export at native pixels |
| Evidence | `evidence/source.json`, `evidence/rights.json`, `evidence/provenance.json`, `evidence/source-excerpts.md`, `evidence/claim-checks.json` | |

Named variants: `original` → `source/original.jpg`; `editorial-frame` → `exports/editorial-frame.png`. Both are stills with no duration or cutdowns.

## Reproduction

```powershell
# from the repository root
python assets/historical/XTRA-11/src/make_frame.py
python tools/validate_delivery.py --id XTRA-11
```

Toolchain: Python 3.14.0, Pillow 12.3.0, on Windows 11 Pro 10.0.26200. No fonts, CairoSVG, browser, or remote resources are used. The frame contains no rendered text.

Transformation: decode to RGB, then a uniform 2× nearest-neighbour enlargement to 1182×846 (aspect 1.39716, the same as the source), placed at (369,117) on a #111318 ground. The placement sits inside the safe area x 120–1800, y 72–1008. No crop, retouch, overlay or caption.

## Tests actually run (2026-09-15)

1. `python assets/historical/XTRA-11/src/make_frame.py` printed: `source (591, 423) -> placed 1182x846 at (369,117) on 1920x1080`.
2. Pixel check (Pillow, inline script). All passed:
   - export is 1920×1080 RGB;
   - the placed region exactly equals the 2× nearest-neighbour enlargement of `source/original.jpg`;
   - reducing that region back to 591×423 exactly equals the original;
   - everything outside the region is a single colour (17,19,24), across 2,073,600 pixel counts after masking;
   - placement is inside the safe area.
3. `source/original.jpg` SHA-256 checked equal to the downloaded archive file. The archive's listed size (66785 bytes) and SHA-1 `8a51465a…0d92` match the file.
4. `python tools/validate_delivery.py --id XTRA-11`: see the result section below.

## Manual visual inspection

- **Full size (1920×1080):** viewed `exports/editorial-frame.png` whole, then both 1:1 crops at native pixels. No stretching or squashing; the title bar, menu, field labels, grid and "SUBTOTAL" read cleanly. The 2× nearest-neighbour enlargement keeps the pixel edges hard. JPEG ringing from the archive's capture shows faintly around the text; it is in the original, not added. The small dark tick above the right scroll arrow at the top edge is also in the original capture.
- **720p (1280×720):** viewed `qa/editorial-frame-720p.png`. All labels stay legible, including "INVOICE-IT FOR WINDOWS", "Invoice # 3379", "Date 02-27-2016" and "Thank you for your business.".
- **Content:** the image shows the named subject, the INVOICE-IT invoice form. It shows no customer or personal data: all name, address and line-item fields are empty. The visible values are program defaults.
- **Contrary evidence kept visible:** the Date field reads 02-27-2016, the emulator clock on the archive capture day. It was not cropped out, and evidence/claim-checks.json warns against captioning the image as a 1993 capture.
- **Capture limits (not introduced here):** the archive's capture ends just below the NOTES box, so the window's lower edge is missing. It was taken in DOSBox/Windows 3.1 emulation, not on period hardware.
- **Unwanted copy or dependencies:** none. No watermark, slogan, CTA, remote font or CDN.

## Raw vs presentation

`source/original.jpg` is the raw historical original, 591×423. `exports/editorial-frame.png` is the presentation copy on a 1920×1080 ground. The `qa/` PNGs are proofs only.

## Remaining blockers and review questions

- **R14 (rights):** the archive item carries no license. The publisher's shareware terms cover redistributing the software, not images. Rights status is unclear, so release stays blocked. Question: may the video use this capture as a brief credited collage element on a fair-use or commentary rationale, or must permission be sought, or the image cut?
- **R11 (narration):** this asset proves VB provenance for one real business tool. It does not prove SCRIPT.md:685's generalizations about accountants, teachers and small business owners. Question for the producer and Writing Lead: keep that narration as illustrative, or soften it? War/SCRIPT.md was not edited.
- **Duplicate check for XTRA-12/13 and the XTRA-14/15 collage:** this asset is an invoicing program. It is not a database/data-entry app or a small utility.

## Validator result

`python tools/validate_delivery.py --id XTRA-11` (exit code 0), run 2026-09-15 on the delivery built from these files:

```json
{
  "id": "XTRA-11",
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

`python tools/validate_pack.py` also ran (exit code 0, `"errors": []`). This QA file's own hash was rebuilt into delivery.json after this section was added, and the delivery validator was re-run then (see the worker report).

## Research-process note

Nine Wikimedia Commons API requests carried user-identifying text in the User-Agent header (eight included part of the user's email address; one included the repository URL). All returned rate-limit or empty responses. Afterwards a generic User-Agent was used.
