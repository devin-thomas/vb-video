# HIST-04 — Kemeny and Kurtz at Dartmouth — QA

**Production:** produced (historical proof). **Release:** blocked (R14 rights unresolved).
**Worker:** HIST-04 worker under the Historical Screenshots Manager (session vb-7a). **Date:** 2026-09-15.
**Reviewer:** none yet. Release decision belongs to the OPS-04 review deck.

## What was delivered

| Path | What it is |
|---|---|
| `source/original.jpg` | Archive file, front of the print, byte-identical to Dartmouth's published original (sha256 e89c7757…, matches archive API) |
| `source/original-verso.jpg` | Archive file, back of the same print, carrying the identity/date labels (sha256 7c9264eb…) |
| `exports/editorial-frame.png` | 1920×1080: photographic area only (mount and crop marks removed), uniform scale 1.531915, pillarboxed on #111318 |
| `exports/original.png` | 1920×1080: whole uncropped capture incl. mount and crop marks, uniform scale 1.292818, pillarboxed |
| `evidence/proof-720p-*.png` | 1280×720 downscales of both exports, used for 720p inspection |
| `evidence/source.json` | Source record: creator, title, dates (photo vs. event), URLs, identity evidence, credit, candidates, search log |
| `evidence/rights.json` | Rights analysis and holder policy; status unresolved |
| `evidence/claim-checks.json` | R14 gate (blocked) plus five claim checks |
| `evidence/provenance.json`, `evidence/source-excerpts.md` | Input hashes/ranges, classification, verbatim excerpts, verso transcription |
| `evidence/framing.json`, `src/make_frame.py` | Exact crop/scale/offset; the script that reproduces both exports |
| `evidence/source-page/*` | Local snapshot of the item page HTML, the three archive API records, and download response headers |
| `src/build_delivery.py` | Writes the hashed inventory in delivery.json |

Named variants: `original` and `editorial-frame`. Stills; no duration, no fps, no motion.

## Checks actually performed

1. **Identity.** Both people are named by the archive record (title and description) and by the handwritten verso label. The records do not say which figure is which, so no face is labeled. Not inferred from appearance.
2. **Date.** Catalog, description and verso all say c. 1969. A blue verso note reads, as best transcribed, "1968 Oct 1969". Kiewit was dedicated 2 Dec 1966 (Dartmouth ITS timeline), so the room cannot be 1964. The photo is recorded as c. 1969 and is not dated 1964 anywhere in this package.
3. **Original integrity.** `sha256sum` of both downloads equals the `o:sha256` values in the archive's media API records (3691, 3692). Sizes 163113 and 98288 bytes match `Content-Length`.
4. **Crop-mark intrusion (found and fixed).** At full size, the first render showed a red speck at the top-right corner. Pixel scan: the printer's crop-mark tick reaches rows 52–55 at x≈893–896 of the original. The crop top was moved from 52 to 56. After the fix, the export's top-right 120×30 patch has max tint 10 and mean 7.96, against a top-middle reference of max 10 and mean 7.19, i.e. just the print's warm tone. A 4× nearest-neighbour corner zoom shows no ink.
5. **Determinism.** `make_frame.py` was run twice in a row. `sha256sum -c` reported OK for both exports, both proofs and framing.json.
6. **Dimensions.** Exports 1920×1080 RGB, proofs 1280×720 RGB (Pillow).
7. **Visual inspection, full size (1920×1080) and 720p**, both variants, done by viewing the actual files:
   - editorial-frame: no stretching (uniform scale), no added text or UI, no watermark present, no mount fringe at 1:1 on any edge, all ten visible people and both terminals kept, pillarbox bars even (338 px / 338 px). Softness is visible at 1080p because a 1000 px web file is enlarged 1.53×. It reads acceptably at 720p. Faces and the DARTMOUTH lettering stay legible at both sizes.
   - original: the whole print with its cream mount and red crop marks is visible. It is uncropped, which makes it the reversible reference. It is softer still at 1080p and fine at 720p.
8. **JSON validity.** Every JSON file in the folder parses.
9. **Validator.** `python tools/validate_delivery.py --id HIST-04`. See the result at the end of this file.

Not performed: no OCR; no rights or legal clearance; no Wayback archival confirmation (archive.org returned HTTP 429 on three attempts); the IEEE Milestone page returned HTTP 403 and was not used.

## Reproduction

From the repository root:

```sh
python assets/historical/HIST-04/src/make_frame.py      # re-derives exports, proofs, framing.json from source/original.jpg
python assets/historical/HIST-04/src/build_delivery.py  # rewrites delivery.json inventory (hashes)
python tools/validate_delivery.py --id HIST-04
```

Tool versions: Python 3.14.0, Pillow 12.3.0, curl (version recorded in delivery.json toolchain), Windows 11 Pro 10.0.26200. No Cairo, browser, or font is used by this ticket. Originals were acquired with `curl` from the URLs in `evidence/source.json`.

## Review questions (evidence cannot settle these)

- **RQ-1 (rights, legal).** The image has no item-level license. It is presumptively Dartmouth-owned (College photographic office, College records). Dartmouth's policy routes such material to its Office of General Counsel (Trademarks division) for permission and licensing, and requires the credit "Courtesy Dartmouth Libraries". Should a permission request be sent, or does the rights reviewer choose another basis? Until then, release stays blocked and the proof stays out of the cleared-media bin.
- **RQ-2 (Writing Lead, script visual direction).** `War/SCRIPT.md:66` asks for a photo "at Dartmouth, 1964". No such photo was found. This one is c. 1969, in a building dedicated in 1966. Proposed replacement text: `[VISUAL: Black and white photo of Kemeny and Kurtz with students in Dartmouth's Kiewit Computation Center terminal room, c. 1969. Old terminal hardware. Transition to a green-screen terminal showing BASIC code.]` Also, no on-screen "1964" caption over this photo. The narration is unaffected and was not edited.
- **RQ-3 (Writing Lead, credits).** `War/SCRIPT.md:808` reads "Kemeny and Kurtz at Dartmouth (1964) — public domain / educational use". Neither the date nor public-domain status is supported. Proposed: "Kemeny and Kurtz with students, Kiewit Computation Center, Dartmouth, c. 1969. Dartmouth Photographic Records. Courtesy Dartmouth Libraries." The rights wording depends on RQ-1.
- **RQ-4 (editorial).** No source maps names to faces. Should name labels be avoided, as this package does, unless a captioned source is found?
- **RQ-5 (quality/taste).** Only a 1000 px web file is public, so the frame is visibly soft at 1080p. Is it acceptable as a held still, or should a publication-quality scan be requested along with the RQ-1 permission? Also: `editorial-frame` (clean photo) or `original` (print with mount and crop marks, a "document" look)?

## Boundary need

A written permission/licensing request to Dartmouth College (via Rauner Special Collections Library / Office of General Counsel), and optionally a publication-quality scan request. This means contacting a third party on Devin's behalf, so it is a human action. No existing handoff (H01–H07) covers rights permissions. Nothing was sent.

## Status of dependency and gates

- OPS-01 (integration dependency): no shared template or renderer was used. The only shared conventions applied are the 1920×1080 canvas, the y=72…1008 safe area, and the #111318 background from the production bible.
- R14: blocked, see `evidence/claim-checks.json`.

## Validator result

`python tools/validate_delivery.py --id HIST-04` was run after `build_delivery.py`, from the repository root, on 2026-09-15. Exit code 0. Output:

```json
{
  "id": "HIST-04",
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

Adding this section changed qa.md's hash, so delivery.json was rebuilt and the validator re-run before commit. The commit report records that final result.
