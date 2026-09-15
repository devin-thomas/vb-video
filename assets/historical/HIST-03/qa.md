# HIST-03 QA: VB 6.0 IDE

**Outcome:** a historical proof with unresolved rights. Production status is `produced`. Release is `blocked` on R14.
**Worker:** Historical Screenshots worker (manager session vb-7a). **Reviewer:** none yet; release decisions come from the review deck.
**Date:** 2026-09-15.

## Deliverable map

| Required path | File | Notes |
|---|---|---|
| `source/original.*` | `source/original.gif` | Microsoft VB6 docs Figure 2.1, byte-exact. 779×574, GIF87a, 19,633 bytes, sha256 `cbd44443…fc0f3c951bd60a0f7479ad0872efef64d0febd08` |
| source page (separate) | `source/source-page/aa733577.html`, `fig21_headers.txt` | Page as served on 2026-09-15, plus the image response headers |
| `exports/editorial-frame.png` | 1920×1080 RGB PNG | Named variant `editorial-frame` |
| named variant `original` | `source/original.gif` | No re-encode |
| `evidence/source.json` | | Creator, title, dates, URLs, identity evidence and limits, transformations, credit |
| `evidence/rights.json` | | Terms consulted, conditions, open rights questions |
| `evidence/claim-checks.json` | | R14 blocked, plus supplementary date/identity checks |
| `evidence/provenance.json` | | Source hashes/ranges, external sources, authored additions, search log |
| `evidence/source-excerpts.md` | | Unchanged anchors and dated external quotes |
| 720p proof | `proofs/editorial-frame-720.png` | 1280×720 |
| alternate candidate | `candidates/wikipedia-vb6-on-xp/` | Original PNG, file page, headers, revision history, source.json, 1080p and 720p frames |

## Reproduction

Run from the repository root with Python 3.14.0 and Pillow 12.3.0. Acquisition used curl 8.18.0 (Schannel).

```
python assets/historical/HIST-03/src/frame.py           # renders the export, the 720p proof, and the candidate frames
python assets/historical/HIST-03/src/build_delivery.py  # writes the hashed inventory to delivery.json
python tools/validate_delivery.py --id HIST-03
```

Acquisition command (anonymous GET, run 2026-09-15):
`curl -sL -D fig21_headers.txt -o aa733577.avp02001.gif "https://learn.microsoft.com/en-us/previous-versions/visualstudio/visual-basic-6/images/aa733577.avp02001(en-us,vs.60).gif"`

No fonts, text, or remote resources are used in rendering.

## Tests actually run

1. **Framing geometry.** `frame.py` printed scale 1.630662, placed size 1270×936, origin (325,72), crop null. The placed box lies inside the safe area x 120–1800 and y 72–1008.
2. **Export/proof dimensions (Pillow).** Export is (1920, 1080) RGB; proof is (1280, 720).
3. **Plate integrity.** Every pixel outside box (325,72,1595,1008) equals #111318; the difference bbox is `None`. Nothing was added around the image.
4. **Reversibility.** Cropping the export box and Lanczos-resizing it back to 779×574 gives a mean absolute difference from the original of [5.0, 5.05, 4.85] per channel (0–255). That is resampling loss only; the geometry inverts exactly. The byte-exact original is kept anyway.
5. **Source identity.** The downloaded Wikipedia candidate's SHA-1 `b7846217…bb962` matches the Wikimedia API sha1. The Microsoft GIF has no published hash; its response headers are preserved.
6. **Validator.** `python tools/validate_delivery.py --id HIST-03` was run after `build_delivery.py` on 2026-09-15. Exit code 0. Actual output: `"ok": true, "errors": []`. It lists these limitations: no OCR or visual judgment; no MP4 validation; no historical, semantic, or legal clearance; manual 1080p/720p review still required. This file changed after that run, so the inventory was rebuilt and the validator run again before commit (see the worker report).

## Manual visual inspection

- **Full size, 1920×1080 (`exports/editorial-frame.png`), viewed.**
  - Title bar "Project1 - Microsoft Visual Basic [design]", menus, toolbar, Toolbox, Form1 designer, Project Explorer, and Properties window (Name/"Returns the name used in code to identify an object.") are all legible.
  - The Microsoft callouts are present and uncut, including "Properties window" at the right edge of the figure's own white margin.
  - No stretching or visible artifacts beyond the mild softening expected from a ×1.63 upscale of a palette GIF.
  - Neutral pillarbox; no added text or UI.
- **720p (`proofs/editorial-frame-720.png`), viewed.**
  - Menu names, the Project Explorer tree, and Properties rows remain readable. Callout labels are small but readable.
  - The composition still reads as a complete classic VB IDE.
- **Alternate candidate frame, 1920×1080, viewed.**
  - The New Project dialog (Standard EXE … Data Project) and the Query/Diagram menus are legible.
  - The workspace is mostly empty gray.
- **Content checks.**
  - No private information, identifiable person, watermark, third-party content, or modern UI appears in the delivered frame.
  - Preserved HTTP header files were scanned for private data, and session-specific values were redacted in place with a marker:
    - `candidates/wikipedia-vb6-on-xp/wp_headers.txt`: `x-client-ip` (requester IP), `set-cookie` (tracking cookie), `x-request-id`.
    - `source/source-page/fig21_headers.txt`: `x-azure-ref`.
  - All other header lines (Content-Type, ETag, Last-Modified, Content-Length, Date) are unchanged. The media files are unaffected.
  - The image is a documentation figure, not a splash screen.

## Editorial gate and evidence summary

- **R14 is blocked.** See `evidence/rights.json` and the review questions below.
- **Plan lead checked.** ASSET_PLAN's "these exist on Wikipedia" is only partly true. The Wikipedia article's VB6 IDE image is a non-free local file, not a Commons file. The Commons searches found no VB6 IDE screenshot.
- **Script date.** "VB6, released in 1998" (SCRIPT.md:691) is supported by Microsoft's 1998-06-15 press release ("general availability scheduled for late summer 1998"). No script change is needed.
- **Version identity.** Established by publication in Microsoft's VB6 documentation (not by appearance). The image carries no version string. Whether the capture was reused from VB5 documentation is unproven.

## Review questions (for the producer's review deck)

1. **Rights (legal risk, R14).** May the video use Microsoft's VB6 documentation Figure 2.1?
   - Microsoft Learn's Terms of Use restrict copying images from Microsoft sites.
   - Microsoft's screenshot permission allows unaltered, uncropped, resized screenshots of released products in videos, with "Used with permission from Microsoft." It does not say whether that covers documentation figures.
   - Options: rely on the screenshot grant, seek written permission, make a fair-use determination, or reject the image.
2. **Choice of image.**
   - The delivered original (Microsoft docs figure, 1998-era look, first-party identity, Microsoft callouts included) is identity-strong but rights-weaker.
   - The alternate (a 2019 uploader screenshot on Windows XP with VB6-only Query/Diagram menus and Data Project) may fit Microsoft's screenshot grant more directly. Its identity is uploader-stated, and it shows a mostly empty workspace.
   - Which should the edit use? A third route is a fresh screenshot captured from a licensed VB6 install, which would need a licensed copy and machine and is outside this worker's authorization.
3. **Callouts.** The figure's Microsoft callouts ("Menu bar", "Toolbox", …) are part of the source and cannot be removed under the screenshot terms. Are they acceptable on screen in section 15?
4. **Credit placement.** If a Microsoft grant is relied on, the full product name and "Used with permission from Microsoft." must appear. Is an end-credits line acceptable, or does it need to be on screen?

## Remaining blockers

- R14 rights are unresolved, so release is blocked.
- No boundary crossing was needed or attempted: no accounts, payments, CAPTCHAs, lending borrows, or software installs.
- Dependency OPS-01: the shared safe-area values from the production bible are used, and no shared template is consumed.
