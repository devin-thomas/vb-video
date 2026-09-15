# HIST-11 QA — Visual Basic 4 retail box

**Production:** produced (archival proof). **Release:** blocked (R14). **Reviewer:** none yet; goes to the review deck.

## Outcome in one line
No authorized public archive holds a VB4 **retail box** image. The delivered original is the VB4 **retail install CD** (Enterprise Edition, 1995), which the script's visual cue lists first. That substitution is review question RQ-2. The image is unlicensed Microsoft artwork, so rights are review question RQ-1.

## Tests actually run (2026-09-15, Windows 11, Python 3.14.0, Pillow 12.3.0)
| Test | Result |
|---|---|
| Archive integrity: local MD5/SHA-1 of `source/original.tif` vs IA manifest | Pass (md5 c8eb1774…936d, sha1 9da64545…0eb5d5 identical) |
| Version text read at native 500 dpi (crops of label text and title) | Pass: "Microsoft Visual Basic", "Enterprise Edition", "Version 4.0", "© 1991–1995 Microsoft Corporation", "Disc Assy. 2031056-002", "0895 Part No. 64575" |
| `evidence/source-excerpts.md` contains `sources/ASSET_PLAN.md:94` and `sources/SCRIPT.md:122–128` byte-exactly | Pass |
| Export PNG 1920×1080 RGB; matte pixel (32,34,38); scan placed 967×936 at (476,72), inside safe area 120–1800 × 72–1008 | Pass (`src/framing-result.json`) |
| No stretch: aspect original 1.03277 vs placed 1.03312 (0.033%, rounding only) | Pass |
| `python tools/validate_delivery.py --id HIST-11` | See "Validator" below |

## Manual visual inspection
- **Full size 1920×1080** (`exports/editorial-frame.png`): whole disc and scanner-bed margin visible, centered, nothing clipped. Title, edition, tagline, Windows 95 logo and the copyright/version block are readable. At 1:1 pixel crops the small print ("Version 4.0", "0895 Part No. 64575") and the title are sharp, with no resampling artifacts. Original scan dust and fine surface scratches remain visible, deliberately unretouched.
- **720p** (`proofs/editorial-frame-720.png`): title, "Enterprise Edition" and the Microsoft wordmark are clearly readable. The version/part-number block is small but legible. No moiré or banding seen.
- **Content check:** no added text, captions, UI, watermark or AI content. The white scanner-bed square on a dark matte reads plainly as a scan, not a staged photo.

## Reproduce
From the repository root, with Python 3.14 + Pillow 12.3.0 (no network needed after acquisition):
```
python assets/historical/HIST-11/src/build_frame.py
python assets/historical/HIST-11/src/make_delivery.py
python tools/validate_delivery.py --id HIST-11
```
Acquisition (already done, anonymous): `curl.exe -sSL -o source/original.tif "https://archive.org/download/Microsoft_Visual_Basic_Enterprise_Edition_Version_4.0_Microsoft_1995/Microsoft%20Visual%20Basic%20Enterprise%20Edition%20(Version%204.0)%20(Microsoft)%20(1995).tif"` (curl 8.21.0).

## Search limitations (not hidden)
- The Wayback Machine (web.archive.org) was unreachable from this environment, so archived 1995–97 microsoft.com product pages, a possible official box-shot source, are **unsearched**.
- eBay listings returned HTTP 403, so box leads are recorded URL-only, uninspected (`evidence/candidates.json`).
- The archive.org Terms of Use page renders client-side, so its wording was not captured. No reuse permission is inferred from public availability.

## Remaining blockers / review questions
- **RQ-1 (rights, R14):** unlicensed Microsoft disc artwork. Use it on a fair-use basis, or source a licensed or self-shot image?
- **RQ-2 (substitution):** accept the retail install CD in place of the retail box, or open a boundary item for a box image?
- **RQ-3 (script visual note):** "purple and teal". The retail disc is purple/magenta only, and box colors are unverified. Keep, soften, or drop?

## Validator
`python tools/validate_delivery.py --id HIST-11` (2026-09-15, run after `make_delivery.py`; re-run after this section was written and delivery.json regenerated):
```
{
  "id": "HIST-11",
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
Exit code 0. The validator checks structure and hashes only. It does not clear rights or verify history.
