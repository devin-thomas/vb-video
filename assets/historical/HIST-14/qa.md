# HIST-14 — Production QA

**Production:** produced. **Release:** unreviewed. R14 is worked but not cleared (see Review questions).

## Delivered
- `source/original.jpg`: the native Wikimedia Commons original, byte-identical (6000×4000 JPEG).
- `exports/editorial-frame.png`: variant `editorial-frame`, 1920×1080. The original is scaled uniformly and centred on white, with no crop.
- `proofs/editorial-frame-720.png`: 1280×720 review proof.
- `evidence/source.json`: the source record, including the search record and two ranked alternates. `evidence/rights.json`: rights terms and credit. `evidence/claim-checks.json`: R14 plus the script's claims and the review questions.
- `evidence/provenance.json`, `evidence/source-excerpts.md`, `evidence/framing.json` (exact, reversible transform), `evidence/source-page.wikitext.txt` (file page source), `evidence/commons-imageinfo.json` (Commons API metadata for the candidates).
- `tools/frame.py`, `tools/finish.py`: reproduction scripts.
- Every file is listed with bytes and SHA-256 in `delivery.json`. Variant `original` = `source/original.jpg`. This is a still with no duration; hold it for editorial timing.

## Source
"NEXT Cube-IMG 7154.jpg" by Rama & Musée Bolo, Wikimedia Commons (https://commons.wikimedia.org/wiki/File:NEXT_Cube-IMG_7154.jpg). The photographer licenses it CC BY-SA 2.0 FR, with CeCILL offered as an alternative. It was first uploaded on 2014-11-14; the capture date is unknown. Accessed 2026-09-15.

The model designation "NeXTcube" comes from the source's own description ("NeXTcube workstation. On display at the Musée Bolo, EPFL, Lausanne."), not from the machine's appearance. The source does not say whether this unit is the 1988 NeXT Computer or the 1990 NeXTcube, which share the enclosure, so the label stays exactly as the source gives it.

Credit: *Photograph by Rama & Musée Bolo, Wikimedia Commons, CC BY-SA 2.0 FR (https://creativecommons.org/licenses/by-sa/2.0/fr/). Framed for video (scaled, matted; no crop).*

## Checks actually performed
- **Original integrity:** passed. SHA-1 matches the Commons API record, and SHA-256 matches between the download and the repo copy.
- **PNG dimensions:** passed. Export is 1920×1080; proof is 1280×720.
- **Framing (uniform scale, no crop, seamless matte):** passed. Scale 0.27, offset (150,0). The original's border and both seam strips are pure white.
- **Safe area:** noted. The equipment spans y 62–1034, slightly past the 72–1008 text-safe band. The frame has no text; if the editor wants clearance, scaling the still to about 94% in the edit gives it.
- **Privacy scan of text outputs:** passed, no hits.
- **Write scope:** passed. Only `assets/historical/HIST-14/` changed.

## Manual visual inspection
- **Full size:** viewed `source/original.jpg` and `exports/editorial-frame.png` (1920×1080). A black NeXT cube with its logo badge, a NeXT display, a French AZERTY NeXT keyboard and a mouse, on white. Nothing is cut off. No watermark, caption, UI, people or private information.
- **1:1:** viewed a 400×240 crop of the export at the cube logo and mouse. Edges are crisp, with no resampling ringing or blocking.
- **720p:** viewed `proofs/editorial-frame-720.png`. The cube, its grille and its logo stay clearly recognisable.

## Reproduction
```
python -u <scratchpad>/fetch_originals.py <dir> rama-IMG_7154.jpg   # GET https://upload.wikimedia.org/wikipedia/commons/9/9d/NEXT_Cube-IMG_7154.jpg, honours Retry-After, checks SHA-1
copy <dir>/rama-IMG_7154.jpg assets/historical/HIST-14/source/original.jpg
python assets/historical/HIST-14/tools/frame.py assets/historical/HIST-14/source/original.jpg assets/historical/HIST-14
python assets/historical/HIST-14/tools/finish.py <tests.json>
python tools/validate_delivery.py --id HIST-14
```
Toolchain: Windows 11 (10.0.26200); Python 3.14.0; Pillow 12.3.0 (LANCZOS resampling). No fonts, remote assets or CDN dependencies are used.

Acquisition was an anonymous HTTPS download, with no account, terms click-through, payment, watermark or CAPTCHA. Wikimedia returned HTTP 429 twice. The request was retried only after the server's Retry-After, and no workaround was used.

`tools/validate_delivery.py` runs after `delivery.json` is written, so its output cannot appear in this hashed file; the result is reported with the delivery.

## Gates and review questions
- **R14:** blocked, pending review. Creator, file-specific license, access method, access date and credit are recorded in `evidence/rights.json`. No fair-use or public-domain assumption is made.
- **HIST-14-Q1 (Writing Lead):** the narration says that in 1995 NeXT was "selling expensive workstations". The evidence says NeXT left hardware in February 1993. The proposed wording is in `evidence/claim-checks.json`. `War/SCRIPT.md` was not edited.
- **HIST-14-Q2 (rights):** accept CC BY-SA 2.0 FR share-alike for this shot, or swap to the CC BY 2.0 alternate (Michael Hicks, Computer History Museum)?
- **HIST-14-Q3 (rights):** is showing the frog-design enclosure as a museum exhibit acceptable without separate clearance?

## Limits
- The claim-check sources for the 1993 hardware exit are Wikipedia's citation of the NYT article (10 Feb 1993), a Fortune archive listing, and Low End Mac. The NYT and Wayback pages could not be opened from this environment.
- Alternates 2 and 3 were not downloaded or viewed at full size.
- Production stays `produced`, not `reviewed`. Release approval comes from the review deck.
