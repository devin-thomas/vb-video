# HIST-21 — Production QA

**Production:** produced. **Release:** blocked (R14 review questions open).

## Delivered
| Path | What it is |
|---|---|
| `source/original.jpg` | Wikimedia Commons `File:Mac_Classic_II_System_7-5-5.jpg`, byte-identical (1443×1575 JPEG, 1,057,159 bytes) |
| `exports/editorial-frame.png` | 1920×1080 editorial frame: whole photo, uniform scale ×0.685714, pillarboxed on #111318 |
| `proofs/editorial-frame-720.png` | 1280×720 review proof of the editorial frame |
| `src/render_frame.py` | Framing script (editable source); also writes `evidence/framing.json` |
| `evidence/source.json`, `rights.json`, `provenance.json`, `claim-checks.json`, `source-excerpts.md`, `framing.json` | Source record, rights layers, provenance, gate/claim checks, excerpts, transform record |
| `evidence/source-page/*` | Snapshots (accessed 2026-09-15): Commons file page, wikitext, API record, 2023-07-16 Wayback capture, Apple Classic II spec page, TidBITS 1996-09-23 article |

Every file above is listed in `delivery.json` with its byte count and SHA-256.

## Checks actually performed
- **Integrity:** the downloaded file's SHA-1 `ec207d6f8d685ae19ea6ee0765dbb0e0de99b39d` equals the Commons API value; Commons lists one file version. The first download attempt returned HTTP 429 (rate limit) and was discarded; the spaced retry returned HTTP 200.
- **License history:** the 2023-07-16 Wayback capture shows the same author, date, description, and CC BY-SA 4.0, with no deletion or copyright notice.
- **Version, model, and context (full-resolution 1:1 crops of the original):** About This Macintosh reads "System Software 7.5.5" and "© Apple Computer, Inc. 1983-1995". The menu bar shows the Apple menu, File, Edit, View, Label, Special, and Help. A Finder "Utilities" window and the Trash are visible. The case badge reads "Macintosh Classic II". Apple's spec page lists 7.5.5 as supported on the Classic II (introduced 10/21/1991).
- **Metadata:** EXIF DateTimeOriginal is 2019:07:06 (Panasonic DMC-FZ8, native 3072×2304). The file was saved through GIMP 2.10.30 on 2023-07-09, so the uploader cropped or processed it. No sign of on-screen compositing at 1:1; this is visual inspection, not forensics.
- **Export dimensions:** export 1920×1080 RGB; proof 1280×720.
- **Framing pixel probe:** x=0 and x=1919 are #111318; x=464 and x=1454 are background; x=465 and x=1453 are image. The image spans the full height (top 0, bottom 1080). The mapping back to source pixels is in `evidence/framing.json`.
- **Full-size inspection:** viewed `exports/editorial-frame.png` at 1920×1080. The whole photo is present: screen, "Macintosh Classic II" badge, top of keyboard. There is no stretch, crop, added text or UI, or watermark. At 1:1 in the export the version line "System Software 7.5.5" is still legible, and the menu bar and Finder window read clearly. The flat side bars and warm floor and wall give a neutral read.
- **720p inspection:** viewed `proofs/editorial-frame-720.png`. The Mac, menu bar, Finder window, and About box are clearly identifiable. The version digits are small but readable. The badge is legible.
- **Content and privacy:** no personal data is visible on screen or in the room. On-screen folder and app names are generic utilities. A privacy scan of the asset's text files for the local account name and home-directory path found no hits; the only match, `appDataSchemaVersion`, is page script in Apple's saved spec page, not a local path.
- **Safe area:** no text is added, so the title-safe region does not apply. Nothing essential sits at the frame edge.
- **Validator:** `python tools/validate_delivery.py --id HIST-21` was run after `delivery.json` was built; the actual output is in the worker report. It checks structure and hashes only, not visual quality, history, or rights.

## Reproduction
From the repository root:

```
python assets/historical/HIST-21/src/render_frame.py
python tools/validate_delivery.py --id HIST-21
```

Tools: Windows 11 (10.0.26200), Python 3.14.0, Pillow 12.3.0 (LANCZOS; PNG compress_level 9), curl 8.18.0 for download. No fonts are used and no installs were performed. The original can be re-fetched from `https://upload.wikimedia.org/wikipedia/commons/0/06/Mac_Classic_II_System_7-5-5.jpg`; check SHA-1 `ec207d6f8d685ae19ea6ee0765dbb0e0de99b39d`.

## Candidates considered
1. **Selected:** `File:Mac_Classic_II_System_7-5-5.jpg` (RetroEditor, CC BY-SA 4.0).
2. `File:System_7_macintosh.jpg` (Nikopol-h, tagged CC0) shows the System 7.5.3 Rev 2 desktop. It is a direct screenshot of Apple software, so the CC0 tag cannot clear it and it conflicts with Commons:Screenshots. It looks like emulator output and has no documented date.
3. `File:System_7.5.5_Update_Apple_-_Macintosh.jpg` (Nikopol-h, tagged CC0) shows install floppies only, with no desktop.
- **Rejected:** the English Wikipedia "System 7" lead image (Mac OS 7.6.1 in SheepShaver) and "Secret About Box" are local non-free fair-use files with no license for this production.

Details are in `evidence/source.json`.

## Remaining decisions (review questions)
Full text is in `evidence/claim-checks.json`.
- **RQ-1 (legal):** The CC BY-SA 4.0 license covers the photograph only, not Apple's System 7.5.5 interface on screen. On what basis, if any, may the video show it?
- **RQ-2 (legal):** Is the resized, pillarboxed frame shown in the video Adapted Material under CC BY-SA 4.0? Checking the legal code showed the automatic "synched with moving image" rule does not apply to photographs.
- **RQ-3 (credits):** Where does the attribution go?
- **RQ-4 (framing accuracy):** The brief asks for a mid-90s Performa or PowerBook under a "1995" line. The shot is a 1991–93 Classic II running a September 1996 release, photographed in 2019. Keep it, or continue the search?
- **RQ-5 (framing taste):** Should there be an extra tighter push-in on the screen, which would drop the badge?

Not certified here: legal clearance, narration sync, final edit placement, release approval. Produced is not release-approved.

## Notes
- The photo is from 2019 and must not be captioned as a 1990s photograph.
- The working `War/SCRIPT.md` has this brief under Section 15 (line 696); the frozen source has it under Section 14. No script change is proposed.
- Reviewer: none yet (review deck, OPS-04).
