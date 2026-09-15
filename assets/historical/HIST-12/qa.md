# HIST-12 QA: Borland Delphi 1.0 IDE

**Outcome: blocked candidate record.** A strong candidate is located and its identity is documented from the vendor's own archived page. It is not acquired and has not been viewed.

- Production status: blocked
- Release status: blocked
- Worker: HIST-12 worker under Historical Screenshots Manager (session vb-7a), 2026-09-15
- Reviewer: none

## Why blocked

1. **Download approval boundary.** The candidate image is `fig1.gif` (35,423 bytes, Wayback). My operating rules require Devin's explicit approval in chat before I download any file. A manager or agent instruction does not count as that approval. Nothing was downloaded, so there is no `source/original.*`, no `exports/editorial-frame.png` and no `delivery.json`. No placeholder media was made.
2. **R14 rights unresolved.** The image is Borland International copyright material with no license. Borland's archived 1996 site notice prohibits reproduction for redistribution. See `evidence/rights.json`.

## Search performed (2026-09-15)

| Route | Result |
|---|---|
| ASSET_PLAN lead: Wikipedia "Delphi (software)" | Rejected. The infobox shows Delphi 10.4, a much later release. |
| Wikipedia "History of Delphi (software)" | No Delphi 1 image. |
| Wikimedia Commons: Category:Delphi (software), MediaSearch "Delphi 1.0" | No Delphi 1.0 screenshots (Delphi 7, XE6 only). No free-licensed option exists there. |
| Web search: "Borland Delphi 1.0 IDE screenshot" | WinWorld shows an About box only, with rights unstated. |
| Internet Archive advanced search (Borland Delphi, 1994–1996) | 55 items. Candidates C2 (User's Guide) and C3 (1995 brochure) found. |
| Wayback CDX `borland.com/delphi*` ≤1997 | Found Borland's **Delphi 1.0 Reviewer's Guide** (`/delphi/delphi1.0/guide/`) with fig1–fig30 GIFs. This yields candidate C1. |
| Wayback page captures (guide pages, index, fact sheet, copyright notice, 1995 press index) | Identity, date and rights evidence. Hashes are in `evidence/provenance.json`. |
| IA OCR text of C2/C3 (streamed and grepped) | Figure captions and copyright lines confirmed. |
| Browser pane view of the fig1.gif Wayback URL | Navigation to web.archive.org was denied in the pane, so no visual inspection was possible without downloading. |

Ranked candidates with deficiencies are in `evidence/candidates.json`. Rejected leads include native capture from archived Delphi install media, because it would mean downloading and executing third-party software.

## Tests actually run

- `curl` against the Wayback CDX API, Wayback `id_` raw captures, IA metadata API and IA OCR derivatives. Some requests failed with transient connection refusals; I retried them with `--retry 6 --retry-delay 8 --retry-all-errors` and all needed pages were eventually retrieved.
- `sha256sum` on the inspected captures (recorded in `evidence/provenance.json`) and on `sources/SCRIPT.md` and `sources/ASSET_PLAN.md`.
- JSON parse check of every `*.json` in this folder: all 6 parsed OK (state.json and evidence/candidates, claim-checks, provenance, rights, source).
- `python tools/validate_pack.py`: exit 0, `"errors": []` (planning structure only).
- `python tools/validate_delivery.py --id HIST-12` produced this actual output, exit code 1:

  ```
  NOT DELIVERED / ERROR: HIST-12: no delivery.json; current production status is blocked. Planning scaffolds are not delivered assets.
  ```

  This failure is expected and correct: the validator refuses to certify a blocked record as delivered.

## Not run / not possible

- **Full-size and 720p visual inspection:** not applicable, because no export exists and the candidate image was never viewed.
- **Version verification at full resolution** (Windows 3.1 chrome, IDE layout, code window visible): pending acquisition.
- **Rendering:** no editorial frame was built, so no renderer command applies yet.

## Toolchain

- curl 8.18.0 (x86_64-w64-mingw32, Schannel)
- Python 3.14.0
- Windows 11 Pro 10.0.26200, Git Bash

## Next steps once unblocked

After Devin approves the download (and separately decides R14):

1. Fetch `https://web.archive.org/web/19961223104420id_/http://www.borland.com:80/delphi/delphi1.0/guide/fig1.gif` to `source/original.gif`. Check that its length is 35,423 bytes and that its SHA-1 (base32) equals `3AB42XGSKUFD5LQFFJKPEE5IAHFCWKPW`.
2. Preserve the host page capture (`8.1.1.4.html`, sha256 `bc0b1abd…35339a`) as source evidence.
3. Inspect the image at native size for Delphi 1.0 markers and record its dimensions in `evidence/source.json`.
4. Build `exports/editorial-frame.png` at 1920×1080. Scale it with integer or nearest-neighbour scaling, or place it at native size centred on a neutral ground, so no detail is invented. No stretching, no added UI, no watermark removal.
5. Write `delivery.json` with hashes, run the validator, and inspect the frame at 1080p and 720p.

If C1 turns out to be unusable (a partial view or too low resolution), fall back to C2 and then C3 (see `evidence/candidates.json`).

## Review questions

1. **Rights (R14):** may the video use this 1995 Borland marketing screenshot of the Delphi 1.0 IDE, archived on the Wayback Machine, under an editorial/commentary rationale, with the proposed credit? Or does HIST-12 stay blocked or get replaced?
2. **Download approval:** may the worker download `fig1.gif` (35,423 bytes, from web.archive.org as above) into `assets/historical/HIST-12/source/`? If C1 fails, may it also download the 3,063,958-byte User's Guide PDF (C2) and the 5,345,846-byte brochure PDF (C3) from archive.org?
3. **Script visual note, for the Writing Lead:** SCRIPT.md:621 says the IDE "looks a lot like the VB IDE." That is a subjective comparison that can only be judged once the image is viewed. No script change is proposed now.
