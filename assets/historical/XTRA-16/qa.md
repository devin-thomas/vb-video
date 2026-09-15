# XTRA-16 QA: VB6-to-.NET migration wizard

**Reviewer:** XTRA-16 worker (agent). Release review is pending in the OPS-04 deck.
**Date:** 2026-09-15
**Production status:** produced
**Release status:** blocked (R14 rights unclear; see review questions)

## What was delivered

| Path | What it is |
| --- | --- |
| `source/original.gif` | Untouched Microsoft figure, 525×496 GIF, sha256 `139f1c1a…7ad0` |
| `exports/editorial-frame.png` | 1920×1080 reversible frame: uniform ×1.65 resize, no crop, 2-line source caption |
| `qa/editorial-frame-720p.png` | 1280×720 review proof of the frame |
| `src/render_frame.py` | Deterministic frame recipe; refuses to run if the original's hash changes |
| `evidence/framing.json` | Exact placement, scale, font and safe-area boxes written by the recipe |
| `evidence/source.json`, `evidence/rights.json` | Source record and rights record |
| `evidence/provenance.json`, `evidence/source-excerpts.md` | Provenance and source excerpts |
| `evidence/claim-checks.json` | R14 gate, claim checks C1–C4, review questions RQ1–RQ4 |
| `evidence/captures/*.html` | Wayback Machine raw captures (2002, 2007) used as identity and date evidence |

Variants: `original` → `source/original.gif`; `editorial-frame` → `exports/editorial-frame.png`. It is a still: no duration, no fps, and it holds for the editor's timing.

## Reproduction

```sh
python assets/historical/XTRA-16/src/render_frame.py
python tools/validate_delivery.py --id XTRA-16
```

The original was fetched once with curl: `curl -sSL -o original.gif "https://learn.microsoft.com/en-us/previous-versions/images/aa730876.vbuw2005_01(en-us,vs.80).gif"` (HTTP 200, image/gif, 65457 bytes). Wayback captures were fetched with curl in `id_` (raw) mode.

Toolchain: Windows 11 Pro 10.0.26200; Python 3.14.0; Pillow 12.3.0 (Lanczos resampling, PNG optimize). Caption font is the installed system font `C:\Windows\Fonts\segoeui.ttf` (Segoe UI, 28 px); no font file is bundled. No CairoSVG, Playwright or ffmpeg was needed for this still. No network access at render time.

## Tests actually run

1. **Source hash guard.** `render_frame.py` checks `source/original.gif` against sha256 `139f1c1a1f785ea0688aa96ce6a04b079136601006d530463504987b23267ad0` before rendering. Passed.
2. **Safe-area check (inside the recipe).** The first two renders failed and were fixed before delivery:
   - Scale 1.75 with a one-line caption: the caption ran off-canvas (x −61…1981).
   - Scale 1.7 with two lines: the screenshot top went above y=72.
   - Final scale 1.65: screenshot box 527,78–1393,896; caption lines 548,926–1372,953 and 393,973–1526,1000; all inside 120,72–1800,1008. Passed.
3. **No stretch.** Horizontal scale 1.64952, vertical 1.64919, aspect error 0.02% from integer rounding. No crop; the whole 525×496 figure is shown. Passed.
4. **Dimensions (Pillow).**
   - `exports/editorial-frame.png`: 1920×1080 RGB PNG.
   - `qa/editorial-frame-720p.png`: 1280×720 RGB PNG.
   - `source/original.gif`: 525×496 palette GIF, 1 frame.
   - Passed.
5. **Protected paths.** `git diff --stat -- sources War manifest.json assets/shared` was empty, so none of them was modified. Passed.
6. **Evidence JSON parses** (claim-checks, provenance, rights, source). Passed.
7. **Encoding.** framing.json, source.json, rights.json, claim-checks.json, source-excerpts.md and render_frame.py contain no U+FFFD bytes. The caption's `·` and curly quotes are valid UTF-8. The console showed `�` only because of its code page. Passed.
8. **Privacy scan.** Text outputs were searched for the local Windows account name and home path; results are recorded in delivery.json `tests`. The `U:\Authoring\MSDN\…` path inside the image is Microsoft's published authoring path, not local data.
9. **`python tools/validate_delivery.py --id XTRA-16`.** Exit code 0. Verbatim output:

```json
{
  "id": "XTRA-16",
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

   After this result was recorded, delivery.json was regenerated so qa.md's new hash is in the inventory. The validator was then re-run; the final result is in the worker report.

## Manual visual inspection

- **Full size (1920×1080), whole frame.**
  - Viewed `exports/editorial-frame.png`. The screenshot is centred, uncropped, with a gray hairline and a dark background.
  - Title bar "controls.vbp Upgrade Report - Microsoft Internet Explorer", address bar, "Upgrade Report for controls.vbp" and "Time of Upgrade: 1/5/2006 11:43 PM" are all visible.
  - The full Upgrade Summary is visible: Compile Errors 12, Design Errors 2 (1 + 1), Warnings 14, Total 28. Upgrade Settings and the status bar are visible.
  - The date and version evidence was not cropped away.
- **Full size, 1:1 crops.** Viewed two native-pixel crops (x480–1440/y40–580 and x380–1540/y540–1080).
  - Every row label, count and "Learn More" link reads without effort.
  - The GIF's own softness is enlarged by the Lanczos upscale, with mild ringing on the orange underlined links. Acceptable; there are no resampling artifacts beyond that.
  - The caption renders in Segoe UI with correct `·` and curly quotes and does not touch the screenshot.
- **720p.** Viewed `qa/editorial-frame-720p.png` (1280×720).
  - Headings, category names, all counts (12 / 2 / 1 / 1 / 14 / 14 / 28) and both caption lines are readable.
  - The small "Learn More" description text and settings paths get soft but are still legible. This is not needed for the beat.
- **Content honesty.** Compared the frame against `source/original.gif` viewed at 2×. No text, counts, highlights or overlays were added or removed. The third-party "efax" toolbar button is present in the original and was kept, not hidden (see RQ2).

## Content and gate checks

- **Subject and era.** A genuine Visual Basic Upgrade Wizard upgrade report, but from **Visual Studio 2005** (January 2006), not Visual Studio .NET 2002/2003. Identity evidence: article byline, "Applies to", article text, image content, and the 2007 Wayback capture. See `evidence/source.json`.
- **Script-only addition.** The ticket family is SCRIPT-SUPPLEMENT. Nothing here claims an original asset-plan row.
- **R14.** Blocked. Microsoft copyright, no open license. Learn Terms of Use are personal/non-commercial with no broadcast; Microsoft screenshot guidelines have conditions this image may not meet (third-party toolbar content; documentation figure).
- **Script claim "announce, in 2002".** Incorrect as worded: announced 2000, shipped Feb 2002. Not edited; routed to the Writing Lead as RQ1.
- **"This is fine" meme.** Not made (RQ4).

## Remaining blockers

- Release is blocked until someone decides the rights question in RQ2.
- Editorial choices are open in RQ3 (2005-era image and the burned-in caption) and RQ4 (meme).
- Writing Lead decision RQ1 is needed on the 2002 → 2000 wording.
- Not done: a byte-level comparison of the GIF with the 2007 Wayback copy of the image. The Wayback CDX lookup returned 504.
