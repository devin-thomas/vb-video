# HIST-06 — Production QA

**Production:** produced (historical proof). **Release:** blocked. R14 rights are unresolved and two review questions are open; see "Gates and review questions".

## What was delivered
- `source/original.png`: Wikimedia Commons "File:Applesoft BASIC.png" (Vadimr, PD-self), byte-identical, 560×384. This is the `original` variant.
- `exports/editorial-frame.png`: the original at an exact 2× nearest-neighbour enlargement, centred on a 1920×1080 #111318 canvas. No crop, annotation, or added UI. This is the `editorial-frame` variant.
- `proofs/editorial-frame-720.png`: 1280×720 review proof (not a variant).
- `evidence/source.json`, `rights.json`, `provenance.json`, `claim-checks.json`, `candidates.json`, `framing.json`, `source-excerpts.md`.
- `evidence/source-page/`: the preserved file page (HTML), raw wikitext, API image record, revision history, upload log, and Wayback CDX records for the page and the image.
- `src/frame.py` (framing) and `src/bundle.py` (inventory and state).
- Every file except delivery.json and state.json is listed with its bytes and SHA-256 in `delivery.json`.

## What the image is and is not
It **is** an Applesoft BASIC screen: the `]` prompt and the HOME, INVERSE and NORMAL statements match Apple's manuals (evidence/source-excerpts.md §3–4).
It **is not** a boot screen: it shows a typed Hello World after RUN and LIST, with no power-on banner (§5). The model, ROM, and emulator are unknown.
Label it only as "Applesoft BASIC prompt on an Apple II-family text screen (model and emulator unknown)". Do not call it an Apple II boot screen or an Apple II Plus.

## Checks actually performed
- **Acquisition integrity:** passed. The local SHA-1 `8cf8db22…5641` equals the Commons API SHA-1, and Commons lists a single file version.
- **Archive corroboration:** passed. The base-32 SHA-1 `RT4NWITA6FTWUBJGEMRVV6RT7UKFAVSB` equals the Wayback CDX digest for the image URL (47 captures, first 2012-08-02).
- **Framing reversibility:** passed. `src/frame.py` compared every 2×2 block of the placed image with its source pixel. The alpha channel was fully opaque before flattening.
- **PNG dimensions:** passed. The original is 560×384, the export 1920×1080, and the proof 1280×720. The placed rectangle (400,156)–(1520,924) is inside the safe area (120,72)–(1800,1008).
- **Claim checks against primary documents:** done. Results are in `evidence/claim-checks.json`: prompt verified, boot screen not supported, model not established, script sentence qualified.
- **Privacy scan of text outputs:** passed. Every text file in this folder was searched for the local account name, home path, e-mail, and the client IP returned in HTTP headers; none were found. The response headers were not saved. The saved page is the anonymous view (`wgUserName` null).
- **Manual visual inspection:** passed.
  - Full size: viewed `source/original.png` (560×384) and `exports/editorial-frame.png` (1920×1080). All eleven screen lines are legible with square pixels and no stretching or blur. The inverse "HELLO, WORLD!" bar, `]LIST`, the five program lines, and the `]` prompt with its block cursor are intact and unclipped. The frame edge of the black screen against the #111318 canvas is visible but quiet. There is no watermark, UI, or private data.
  - 720p: viewed `proofs/editorial-frame-720.png` (1280×720). Every line, including `CHR$ (7)`, stays readable.
- **Structure validation:** see "Validator" below.

## Validator
`python tools/validate_delivery.py --id HIST-06` ran after bundling and exited 0 with `"ok": true, "errors": []`. It printed its standard limitations: no OCR or visual judgement, no MP4 checks, no historical, semantic, or legal clearance, and manual 1080p/720p review still required. It was re-run after this section was written and the inventory re-bundled; that result is in the commit report.

## Reproduction
Acquisition (anonymous; no account or terms):
```
curl -A "<descriptive user agent>" -o assets/historical/HIST-06/source/original.png https://upload.wikimedia.org/wikipedia/commons/f/fc/Applesoft_BASIC.png
```
The expected SHA-256 is `69df4c7f0b3e4271f12311bc0e06e5d61cadffee4b2870875d2034a7cf6bda4e`; `frame.py` refuses any other file.

Framing, inventory, and validation:
```
python assets/historical/HIST-06/src/frame.py
python assets/historical/HIST-06/src/bundle.py
python tools/validate_delivery.py --id HIST-06
```
Toolchain: Windows 11 10.0.26200; Python 3.14.0; Pillow 12.3.0; curl 8.21.0 (Schannel). No fonts are rendered or bundled, and there are no remote assets. The OPS-01 renderer was not needed because the image is pasted, not drawn.

## Gates and review questions
- **R14 (blocked):** may the video use this Commons PD-self text-mode screenshot, credited as in `evidence/rights.json`, without further clearance? The Author field is empty, and the threshold of originality for Applesoft output and Apple glyphs is a legal judgement.
- **Visual brief:** does the Apple II tile accept an Applesoft `]` prompt screen with a typed Hello World, or must it be a true power-on screen?
- **Writing Lead (optional):** keep "Your Apple II had Applesoft BASIC" (defensible for the II Plus era), or tighten it to "Apple II Plus"? No script edit was made.

## Boundary need
Only if a true power-on screen is required: an identified Apple II Plus cold-start capture needs real hardware or an emulator with Apple ROMs. Downloading and running an emulator and Apple ROM images is outside this worker's authorization, and no freely licensed archive capture of that screen was found (`evidence/candidates.json`).

## Dependency and status
OPS-01 is produced (shared canvas and safe area used). Production is `produced`; release is `blocked` until the review deck decides R14. Reviewer: none yet; only the producing agent inspected this media.
