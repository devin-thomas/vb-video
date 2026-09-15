# XTRA-09 QA — Mid-1990s Macintosh hardware

**Result:** produced as a historical proof. Release **blocked** on R14 (rights not cleared; see review questions).
**Checked by:** XTRA-09 worker agent, 2026-09-15. **Human reviewer:** none yet (review deck).

## What was delivered

| Path | Role |
|---|---|
| `source/original.jpg` | Native original, byte-identical to the Commons file (5444×2921 JPEG, sha256 `f92f221b…9386f`) |
| `exports/editorial-frame.png` | 1920×1080 editorial frame (uniform downscale, no crop) |
| `proofs/editorial-frame-720.png` | 1280×720 review proof |
| `evidence/identity/performa-630cd-tag.jpg` | Rear model label of the same machine (identity evidence only) |
| `evidence/source.json`, `rights.json`, `provenance.json`, `claim-checks.json`, `candidates.json`, `framing.json`, `source-excerpts.md` | Provenance, rights, gate, and search records |
| `src/make_frame.py` | Exact framing script |

Named variants: `original` → `source/original.jpg`; `editorial-frame` → `exports/editorial-frame.png`. Still asset; no timing or motion.

## Reproduce locally

From the repository root:

```sh
python assets/historical/XTRA-09/src/make_frame.py
python tools/validate_delivery.py --id XTRA-09
```

Toolchain: Windows-11-10.0.26200-SP0, Python 3.14.0, Pillow 12.3.0. CairoSVG is not needed (raster only). It could not load its Cairo DLL in this shell and was not used. No fonts, network, or installs are needed to rebuild the frame.

Acquisition: anonymous HTTPS GET of `https://upload.wikimedia.org/wikipedia/commons/b/ba/Apple-macintosh-performa-630cd.jpg` and `https://commons.wikimedia.org/wiki/Special:FilePath/Apple-macintosh-performa-630cd-tag.jpg` (curl, 2026-09-15) into the session scratchpad, then a copy with a SHA-256 equality check.

## Tests actually run

1. **Original preserved:** SHA-256 of the scratchpad download and `source/original.jpg` both `f92f221b042a6122f5511cfed652e761adae7cee9388d56772ed69ad87f9386f` (3,966,535 bytes). The tag photo is also identical (`8c4ad23b…eb0c`). `make_frame.py` re-hashes the input after rendering and asserts it is unchanged; the assertion passed.
2. **Framing geometry** (`evidence/framing.json`): uniform scale 0.308597 → 1680×901 at offset (120, 89). Aspect in 1.86375, out 1.86459 (rounding only). No crop.
3. **Dimensions:** `exports/editorial-frame.png` is 1920×1080 RGB; `proofs/editorial-frame-720.png` is 1280×720 RGB.
4. **Safe-area pixel probe:** column 119 and column 1800 are background #111318; columns 120 and 1799 are photo. Row 88 is background, row 89 photo, row 989 photo, row 990 background. The photo lies entirely inside x=120…1800, y=72…1008.
5. **Identity check:** the front badge reads "Macintosh / Performa 630CD". The rear label reads "Model Number: M3076", "FCC ID: BCGM3076". Apple Support 112345 gives the 630/630CD as introduced 7/1/1994, Orig SSW 7.1.2P.
6. **Date check:** EXIF DateTimeOriginal 2002-02-09 contradicts the camera model (NIKON D5300, announced 2013-10-17). The photograph date is recorded as unknown.
7. **Delivery validator:** `python tools/validate_delivery.py --id XTRA-09`. The verbatim result is in `delivery.json` → `tests` and in the worker report. It is not written into this hashed file.

## Manual visual inspection

- **Full size (1920×1080):** viewed `exports/editorial-frame.png` whole, plus two exact 1:1 crops: the badge/lower-left region (x120–1080, y480–1000) and the top-right frame edge (x1000–1920, y40–560). The Performa 630CD is centred on a dark #111318 surround with an even margin top and bottom. The badge "Performa 630CD" and the rainbow Apple logo are sharp. The edges are clean with no halo, resampling ringing, stretch, or crop of the machine. No watermark, text overlay, UI, or personal data.
- **720p (1280×720):** viewed `proofs/editorial-frame-720.png`. The machine reads at a glance and "Macintosh / Performa 630CD" is still legible.
- **Physical condition (not a defect of the file):** dirt and scuff marks on the front bezel and a small mark on the lid. The "Performa 630CD" nameplate is a stick-on label with a small scuff at its left end. The CD-ROM bay opening shows a pale blank panel; whether a drive is fitted is not visible. The original photographer made the image; nothing was retouched.

## Content checks

- [x] Depicts the named subject and era: a mid-90s Macintosh Performa, model identified from its badge and rear label, release date from Apple.
- [x] Attribution and rights recorded without guessing (`evidence/rights.json`); rights_status `unverified`.
- [x] Raw (`source/original.jpg`) and presentation (`exports/editorial-frame.png`) copies are separate.
- [x] Labelled as a SCRIPT-SUPPLEMENT addition, not an original asset-plan row (`evidence/provenance.json`).
- [x] Outputs correspond to XTRA-09; no filename or asset swap.
- [x] Separate from HIST-21: HIST-21 holds only a planning state.json; this is a hardware photo with no screen content.
- [x] No remote font or CDN, no AI substitute, no fabricated evidence.

## Remaining blockers / review questions

- **R14 blocked.** RQ-XTRA09-1 (accept the CC BY 4.0 recorded on Commons?), RQ-XTRA09-2 (credit name), RQ-XTRA09-3 (1994 model for a "1995" line?). Details in `evidence/claim-checks.json`.
- **Access limits observed:** the Commons API and upload server returned HTTP 429, so alternate candidates 6200 and 580CD were not downloaded or viewed at full size. The live wiki.techtangents.net served an Anubis bot check, which was not bypassed; the Internet Archive snapshot was used instead.
