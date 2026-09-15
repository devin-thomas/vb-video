# XTRA-17 QA record

**Asset:** classicvb.org "Petition for the Development of Unmanaged Visual Basic and Visual Basic for Applications", Wayback Machine snapshot **20050312064351** of `http://classicvb.org:80/petition/`.
**Worker:** Claude Code (Opus 5), branch `ticket/XTRA-17`, 2026-09-15.
**Production status:** produced. **Release status:** blocked (R14 rights: all rights reserved by classicvb.org).
**Reviewer:** none yet; the review questions go to the OPS-04 review deck.

## Files

| Role | Path | Size |
|---|---|---|
| Uncropped original (Wayback banner kept) | `source/original.png` | 1920×2457 |
| Editorial frame, variant `editorial-frame` | `exports/editorial-frame.png` | 1920×1080 |
| 720p proof of frame | `proofs/editorial-frame-720.png` | 1280×720 |
| 720-high proof of the whole original | `proofs/original-720h.png` | 563×720 |
| Raw archived HTML (digest-checked) | `source/archived-html/*.html` | 4 files |

## Reproduction

Run from the repository root:

```sh
python assets/historical/XTRA-17/evidence/capture.py   # writes into its own folder: move the PNG to source/original.png and the log to evidence/capture-log.json
python assets/historical/XTRA-17/evidence/frame.py     # crop (0,0,1920,1080) to exports/editorial-frame.png, plus proofs
python tools/validate_delivery.py --id XTRA-17
```

The capture was run from a scratch copy of `evidence/capture.py`, and the outputs were copied into the folder. A re-capture will not be byte-identical: the Wayback banner shows live values such as the capture count and the date range. Archived HTML was fetched with `curl -s -L "https://web.archive.org/web/<timestamp>id_/<original url>"`.

**Toolchain:** Windows-11-10.0.26200-SP0; Python 3.14.0; Playwright 1.63.0 with bundled Chromium 153.0.8010.12 (headless); Pillow 12.3.0; curl (Git Bash). No Cairo or ffmpeg needed. No font files were bundled: the page renders with Chromium's local system fonts.

## Tests actually run

1. **Wayback CDX digest check (passed).** For the three petition HTML files, the SHA-1 base32 of the downloaded bytes equals the CDX digest: 20050312064351 `TJRKHXRKUYHLTM6GZ65N4XL75QU4YOXR`, 20050309123704 `A5HGSJYIRM3A4RTCD6H7SIAOSBIEPELO`, 20060301204941 `OKWU44MMUMBQEHSGDPODKQDZXJ4MWRX7`.
2. **Capture replay (passed, with substitutions noted).** The final URL equals the requested replay URL, with HTTP 200 on the page. Wayback served `styles.css` from 20050313060842 and `digital-signing.gif` from 20050518021902, its nearest captures. See `evidence/capture-log.json`.
3. **Original unchanged (passed).** `frame.py` asserts that the SHA-256 of `source/original.png` is identical before and after framing (`04bf146d…6168c93`).
4. **Dimensions (passed).** Frame 1920×1080 from a 1:1 crop, with no resampling. Proofs are 1280×720 and 563×720 by uniform scale. No stretching anywhere.
5. **JSON parse (passed).** delivery.json, state.json and every file in evidence/*.json parse.
6. **Privacy scan (passed).** Searched all files in the asset folder for the local account name, the user's email address and local user-profile paths: 0 hits. The pictured page version contains no signatory names.
7. **`python tools/validate_delivery.py --id XTRA-17`** (passed). Verbatim output:

```json
{
  "id": "XTRA-17",
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

After this record was added, delivery.json was rebuilt so qa.md's hash is current, and the validator was run again.

## Manual visual inspection

- **Full size, `exports/editorial-frame.png` at 1920×1080, viewed 1:1.**
  - The top shows the Wayback banner with the original URL `http://classicvb.org/petition/`, "490 captures, 9 Mar 2005 – 9 Sep 2026", and the calendar reading **MAR 12 2005**.
  - Below it: the heading "A PETITION FOR THE DEVELOPMENT OF UNMANAGED VISUAL BASIC AND VISUAL BASIC FOR APPLICATIONS", the two intro paragraphs, OBJECTIVES, items 1 and 2 in full, and the heading of item 3, which is complete at the bottom edge with no clipped glyphs.
  - Text is crisp (1.5× device scale capture). There is no donation overlay, cookie banner or login prompt.
  - The banner and language selector occupy y≈0–125, above the y=72 safe-area line. This is accepted because the banner is the date evidence; see RQ2.
- **Full size, `source/original.png` at 1920×2457, viewed scaled to the viewer.** It shows the whole page through CONCLUSION, the counter "1376 signatories including 203 Microsoft MVPs since March 8th, 2005.", three links, the "Sign the Petition" artwork and the email-verification note. Nothing is cropped.
- **720p, `proofs/editorial-frame-720.png`.** The heading and body text are readable, and the banner date "MAR 12 2005" and URL are legible. Composition is the same as at 1080p.
- **720 high, `proofs/original-720h.png`.** The whole page layout and the counter line are legible as a reference. Body text is too small for on-screen use, which is expected for the full page.

## Content checks

- The subject and era are right: a real 2005 VB6/VBA advocacy petition, dated by the archive timestamp and by the page's own "since March 8th, 2005".
- No fake browser window. The chrome shown is the real Wayback Machine replay toolbar. No invented counts or dates, and no AI imagery.
- Raw and presentation copies are separate: `source/` holds the originals, `exports/` the frame, `proofs/` the review copies.
- This is a script-only addition (SCRIPT-SUPPLEMENT), not an ASSET_PLAN row.
- The petition's "Sign" links and form were not followed or submitted.

## Remaining blockers and review questions

- **R14, blocked.** The classicvb.org footer reads "All Rights Reserved Worldwide", with no reproduction without written permission.
- **RQ1–RQ4:** see `evidence/claim-checks.json`. They cover rights and use, keeping or masking the banner, a 2005 date cue for the Writing Lead, and an optional framing of the counter.
