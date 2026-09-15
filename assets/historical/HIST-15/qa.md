# HIST-15 QA: PowerBuilder DataWindow

**Outcome:** historical proof with unresolved rights. Production: `produced`. Release: `blocked` (R14).
**Reviewer:** none yet. Worker self-check only; release decision pending the review deck.

## What was delivered

| Path | Role |
|---|---|
| `source/original.dib` | Native original: `pbdatc/PD4_504.DIB` from the 1995 CBT Systems course "PowerBuilder: DataWindow Concepts". 640×480, 8-bit BMP, byte-identical to the archive file (sha256 `52ca5218…dcb6`). |
| `exports/editorial-frame.png` | Named variant `editorial-frame`: 1920×1080 pillarbox of the untouched original. |
| `qa/editorial-frame-720p.png` | 720p proof of the editorial frame (QA only). |
| `src/render_editorial_frame.py` | Editable framing source; reproduces the export. |
| `evidence/source.json`, `evidence/rights.json`, `evidence/provenance.json`, `evidence/claim-checks.json`, `evidence/source-excerpts.md` | Source, rights, provenance, gate, and excerpt records. |
| `evidence/archive/ia-item-metadata.json` | Internet Archive item metadata, uploader e-mail redacted. |
| `evidence/archive/iso-listing-pbdatc.tsv` | ISO listing rows for the course folder, manuals, and catalogue files. |

Variant `original` maps to `source/original.dib`. Both variants are stills. Duration is not applicable; editorial hold is set in the edit.

## Reproduction

```powershell
# from the repository root, on branch ticket/HIST-15
python assets/historical/HIST-15/src/render_editorial_frame.py
# re-acquire the original (anonymous HTTPS, no account):
curl.exe -sL -o PD4_504.DIB "https://archive.org/download/cbt-systems-microsoft-office-and-powersoft/CBT%20Systems%20Microsoft%20Office%20and%20Powersoft.iso/pbdatc%2FPD4_504.DIB"
# expected sha256 52ca521806db7190c1418ffa087ae6d144ca4174d86011a5178ebc658db5dcb6
```

Toolchain (as run 2026-09-15, Windows 11 Pro 10.0.26200): Python 3.14.0, Pillow 12.3.0, curl 8.21.0 (Schannel), ffmpeg/ffprobe 6.0-essentials_build (gyan.dev; used only to inspect rejected AVI leads), git 2.53.0.windows.1. No fonts are used: the frame adds no text.

Framing transform: palette to RGB, uniform scale ×1.95 (640×480 → 1248×936, Lanczos), placed at (336, 72) on a flat `#111318` ground. To reverse, crop (336, 72, 1584, 1008) and scale by 480/936. The pixel-exact original is `source/original.dib`.

## Tests actually run

1. **Hash identity.** `Get-FileHash` on the downloaded `PD4_504.DIB` and on `source/original.dib`: both `52ca521806db7190c1418ffa087ae6d144ca4174d86011a5178ebc658db5dcb6`. PASS.
2. **Original format check.** BMP header parsed with Python: signature `BM`, info header 40, 640×480, 8 bpp, compression 0, 256 colours. PASS.
3. **Export dimensions.** Pillow reports `exports/editorial-frame.png` as (1920, 1080) RGB and `qa/editorial-frame-720p.png` as (1280, 720) RGB. PASS.
4. **Identity cross-check.** The on-screen callout text matches `pbdatc/PD04.TXT` line 321; the title bar unit name matches unit 4 in `PD_UNIT.TXT` and `UNITLIST.INI`; the course name is confirmed in `CBTSETUP.INI` and on title screen `PD_1ST.DIB`. PASS.
5. **Private-data scan.** Regex for e-mail addresses on `evidence/archive/ia-item-metadata.json` after redaction: 0 matches. On `iso-listing-pbdatc.tsv`: 0 `@` characters. PASS.
6. **Delivery validator.** `python tools/validate_delivery.py --id HIST-15`. Result recorded in `delivery.json` → `tests`, and in the worker report.

## Manual visual inspection

- **Full size (1920×1080), `exports/editorial-frame.png`:** the whole 640×480 screen is visible, uncropped, with correct aspect and no stretch. It sits entirely inside the safe area (x 336–1584, y 72–1008). Menu labels (File, Edit, Display, Rows, Window, Help), the PainterBar, "DataWindow - (untitled)", the StyleBar (Arial, 8, B/I/U), field labels, and callout text are all crisp and legible. Lanczos scaling gives slight softening but no ringing that hurts reading. No watermark in the source; nothing removed or added. PASS.
- **720p (1280×720), `qa/editorial-frame-720p.png`:** the menu, sheet caption, field labels/values, and callout remain readable. PainterBar icons are small but recognisable as a toolbar. PASS.
- **Content check:** the shown data (ID 105, Matthew Cobb, R & D, MA, 62000.000) is course sample data; alternate `HIGHLIGH.DIB` shows the same names in an "Employee Information" demo app. It is not treated as personal information about a real individual, but this was not independently verified.
- **Caveat visible in frame:** CBT Systems course chrome is part of the original: the title-bar text "Displaying and validating data - Screen 19 of 19", the clock, the yellow instructional callout, and the "CBT Controls" button bar. Left in place deliberately: removing it would be a crop that changes what the image is (a training screen). See review question 2.

## Remaining blockers

- **R14 rights:** unresolved. The screen is © 1995 Powersoft Corporation and CBT Systems Ltd; no licence or permission identified; the Internet Archive item has no rights statement. Release stays `blocked`.
- **Wayback Machine:** unreachable from this environment (HTTP 000), so 1995–1998 powersoft.com captures were not searched. This does not block the delivered asset.

## Review questions

1. **Rights (legal).** Can the video show this copyrighted 1995 CBT Systems / Powersoft course screen, full frame with credit, on a fair-use or commentary basis? Or must permission be sought, or a different image found? Evidence: `evidence/rights.json`.
2. **Framing (taste).** The frame includes CBT course chrome (title bar text, clock, yellow callout, CBT Controls bar). Keep it as-is, or request a tighter reversible crop to the PowerBuilder window region? The callout would remain inside any crop. Evidence: `exports/editorial-frame.png`.
3. **Caption/version (editorial).** No source states the PowerBuilder version; evidence points to pre-5.0, most probably 4.0. Is "PowerBuilder DataWindow painter, 1995" acceptable as the caption level, or should "4.0" appear as an explicitly inferred version? Evidence: `evidence/claim-checks.json`.
