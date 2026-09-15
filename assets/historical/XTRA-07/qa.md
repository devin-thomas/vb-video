# XTRA-07 QA — Visual Basic 4 installation media

**Outcome:** historical proof produced; release blocked on R14 (rights unresolved).
**Subject:** Microsoft Visual Basic Enterprise Edition, Version 4.0, CD-ROM (single disc). Read from the disc label, not a seller description.
**Reviewer:** none yet (agent QA only; the release decision belongs to the OPS-04 review deck).
**Date:** 2026-09-15

## Files

| Path | What it is |
|---|---|
| `source/original.png` | Unmodified download of Internet Archive `media-disc01.png`, 2932×2948 RGB |
| `exports/editorial-frame.png` | Named variant `editorial-frame`, 1920×1080 |
| `proofs/editorial-frame-720.png` | 1280×720 downscale of the export, for 720p review |
| `evidence/label-crop.png` | 1:1 crop of the printed label text, box [1900,850,2500,1250] of the original |
| `evidence/framing.json` | Every framing parameter plus the masked-pixel check |
| `evidence/source.json`, `evidence/rights.json`, `evidence/claim-checks.json`, `evidence/provenance.json`, `evidence/source-excerpts.md` | Source, rights, gate, provenance and excerpt records |
| `src/render_frame.py` | Framing script |

Named variant `original` maps to `source/original.png`. The ticket has no motion or cutdowns, so duration and fps are null.

## Reproduction

From the repository root:

```sh
python assets/historical/XTRA-07/src/render_frame.py
```

Toolchain: Windows 11 Pro 10.0.26200, PowerShell 7.6.6, Python 3.14.0, Pillow 12.3.0. No fonts, network or Cairo are used. The shared `tools/render` pipeline builds authored SVG/HTML scenes and has no archival-still path, so it was not used. The script only reads `source/original.png` and overwrites its own outputs.

## Tests actually run

1. **Original is byte-identical to the archive file: passed.** `source/original.png` SHA-256 `765b153c92588f544ac63513868f5c0cffab1e39a7f99e1c61ac8a497e43aad8` equals the download. Its MD5 `7f282de718057015c0fb1fcea02f6d3d` matches the MD5 archive.org publishes for `media-disc01.png` (size 8029368).
2. **Uniform scale, no stretch: passed.** One factor of 0.32613 for both axes. The disc crop is 2875×2870, resized to 938×936; the x/y factor ratio is 1.00039, which is integer rounding only.
3. **Mask removes scanner bed only: passed after two fixes.**
   - *First render:* rim fit came from the raw non-white box, which dust specks on the scanner bed had pushed outward, so the ellipse was too large at the top.
   - *Second render:* speck-robust fit with 3 px padding. The check reported 14,899 non-white pixels at the rim edge, meaning the disc edge was shaved.
   - *Resolution:* inspected 3× rim crops with the ellipse drawn at 3/10/15 px padding, and sampled 3,600 rays per padding value. The smallest padding with no rim pixels (luminance <200) outside the ellipse was 6 px; 10 px was chosen.
   - *Final check:* 205 non-white pixels are hidden. The 142 within 2% of the rim all have luminance 229–234 (near-white scanner-bed fade). The rest are isolated dust specks well outside the disc. No disc detail is removed.
4. **PNG dimensions: passed.** Export 1920×1080 RGB, proof 1280×720 RGB, original 2932×2948 RGB. Canvas corners and the rows just outside the safe area (y=71, y=1008) are the ground colour #111318, so the disc stays within y=72…1008 and x=491…1429.
5. **Text-output privacy scan: passed.** Every text output was searched for the local account name and uploader email addresses (values not written here). No hits.
6. **`python tools/validate_delivery.py --id XTRA-07`: passed (exit 0).** Verbatim stdout is in `evidence/validate-delivery.txt`: `"ok": true`, `"errors": []`, plus the validator's standard limitations (no OCR, visual, historical or legal judgement). After this record and that file were added, `delivery.json` was rebuilt and the validator re-run; the final result is in the worker report.

## Manual visual inspection

- **Full size (1920×1080), `exports/editorial-frame.png`, viewed 1:1:**
  - The whole disc is centred on the dark ground: outer clear rim, hub ring and centre hole all intact.
  - All label text is legible, including the small print: "© 1991–1995 Microsoft Corporation. All rights reserved.", "Version 4.0", "Disc Assy. 2031056-010", "0296 Part No. 69944", "Enterprise Edition", "Programming System for Windows Platforms", and the Designed for Windows 95 logo.
  - No stretching or colour shift; the magenta halftone and silver match the original.
  - No overlay text, UI copy or watermark.
- **Rim at 4× (nearest-neighbour crops of the export at top, right and bottom-left):** a clean anti-aliased edge; the disc's outer clear rim is preserved; no white scanner crescent and no clipping.
- **720p, `proofs/editorial-frame-720.png`, viewed 1:1:** title, edition and Microsoft wordmark are clearly readable. The small copyright and part-number lines are readable, though soft, which is acceptable for a background still. No aliasing artefacts.
- **`evidence/label-crop.png` at 1:1:** the copyright, version, Disc Assy. and part-number lines are sharp.
- **Original at full resolution:** flatbed scan with no text or version evidence outside the disc, so framing hides nothing contrary.

## Content checks

- Depicts the named subject and era: a VB4 CD-ROM, Enterprise Edition, Version 4.0 (claim-checks C1).
- 16/32-bit: not printed on the disc; no bitness claimed (C2).
- Distinct from HIST-11 (retail box): only the disc label is shown.
- Labelled as a script-only supplement (SCRIPT-SUPPLEMENT), not an asset-plan row.
- Raw and presentation copies are separate files with different roles; the transformations are listed in `evidence/framing.json`.
- The script's "purple and teal" does not match this disc (magenta on silver): C3, routed to the Writing Lead as RQ-XTRA-07-2. `War/SCRIPT.md` was not edited.

## Remaining blockers and review questions

- **R14: blocked.** No licence or permission for the anonymous scan or the Microsoft label artwork (RQ-XTRA-07-1).
- **RQ-XTRA-07-2 (Writing Lead):** "purple and teal" visual note versus the actual media colours.
- **RQ-XTRA-07-3 (taste):** is the Enterprise disc acceptable as representative, given store buyers more likely had Standard or Professional?
