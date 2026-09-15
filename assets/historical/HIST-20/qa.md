# HIST-20 — Windows 95 Solitaire: QA

**Production:** produced. **Release:** blocked (R14 rights unresolved). **Reviewer:** none yet (goes to the OPS-04 review deck).

## Delivered
| Path | What it is |
|---|---|
| `source/original.png` | Acquired native original, byte-identical to Internet Archive `solitiare-windows-95` (1920×1080 RGBA, sha256 `7bb19b94…e4e7`; md5/sha1 match the archive manifest). Uncropped. Variant `original`. |
| `exports/editorial-frame.png` | 1920×1080 editorial framing. The Solitaire window is cropped, scaled 2× nearest-neighbour and centred on #111318. Variant `editorial-frame`. |
| `evidence/proof-720p.png` | 1280×720 downscale of the frame, used for the 720p inspection. |
| `src/build_editorial_frame.py` | Reproduction script. It checks the original's hash and records the crop box, scale and offset. |
| `evidence/source.json`, `evidence/rights.json` | Source record (creator, dates, URLs, identity evidence, transformations, candidates) and layered rights record. |
| `evidence/claim-checks.json`, `evidence/provenance.json`, `evidence/source-excerpts.md` | R14 gate record, provenance classification, and verbatim excerpts. |
| `evidence/source-page/*` | Preserved source pages: IA details page, IA item metadata (JSON and XML), IA collection metadata with the uploader's permission statement, and a Wayback capture of Microsoft's copyright-permissions page with extracted text. |

Byte sizes and SHA-256 hashes for every file are listed in `delivery.json`.

## Checks actually performed (2026-09-15)
1. **Source discovery.**
   - Wikipedia "Microsoft Solitaire" (the plan lead) has only Windows 7 and Windows 10 images.
   - Commons "Windows 95 screenshots" and "Computer Solitaire games" hold no Microsoft Windows 95 Solitaire file.
   - The GUIdebook Windows 95 gallery has no Solitaire screenshot.
   - The Internet Archive advanced search returned one hit, which was selected.
   - The Wikimedia API rate-limited the scripted queries, so the Commons categories were checked via their HTML pages.
2. **Integrity.**
   - The downloaded PNG's md5 `2c9884e4…` and sha1 `827db254…` equal the archive manifest values.
   - Its size is 1,704,970 bytes.
3. **Identity (full-resolution inspection plus zoomed crops).**
   - The VirtualBox guest window title reads "Windows 95 [Running]", and the Manager list shows the "Windows 95" VM as Running; the other VMs are powered off.
   - The Solitaire window has Windows 95 caption buttons (minimize, maximize, close X), which rules out a relabelled Windows 3.1 image.
   - Felt colour is exactly RGB (0,128,0).
   - Status bar reads "Score: 245 Time: 312".
   - The guest display is 800×600 at 1:1 in the host capture; small ±1–3 colour deviations are consistent with a host-side capture.
   - **Limit:** the exact Windows 95 build is not determinable, and the image is a 2024 emulated capture, not a 1995 screenshot.
4. **Crop bounds.**
   - Border pixels were verified on all four sides: outer light edge at x=602 and y=356; outer dark edge at x=1198 and y=789.
   - Crop box (602,356)–(1199,790) exclusive gives 597×434.
5. **Determinism.**
   - The build script ran twice with identical output, sha256 `6818704c55ae69ca10caa5e3bc9acdc9e6d8f20b5d1979599e04cdfec10abdd5`.
   - The window region in the export is pixel-identical to the 2× nearest-neighbour crop of the original.
   - All background pixels are (17,19,24).
6. **Safe area.** Content spans x 363–1557 and y 106–974, inside x 120–1800 and y 72–1008. No stretching: the scale is exactly 2× on both axes.
7. **Manual visual inspection.**
   - `exports/editorial-frame.png` at full 1920×1080: title bar, menu, all cards, the green-ring deal-again stock marker and the score line are crisp. No cut-off chrome and no host or private content.
   - `evidence/proof-720p.png` at 1280×720: title, card ranks and suits, and the score text all remain legible.
   - `source/original.png` at full size, plus zooms of the title bar, caption buttons, status bar and the host taskbar and icons.
8. **Content hygiene.**
   - The frame contains no private information, remote fonts or CDN assets, added text, fictitious UI, removed watermark, or AI-generated content.
   - The original does contain private host-desktop content; it is kept for provenance only.
9. `python tools/validate_delivery.py --id HIST-20`: result recorded in `delivery.json` tests and in the worker report.

Not performed: OCR, legal clearance, or verification of the Windows 95 release date or build.

## Reproduction
From the repository root:

```
python assets/historical/HIST-20/src/build_editorial_frame.py
python tools/validate_delivery.py --id HIST-20
```

Re-acquire the original (anonymous public download, no account):

```
curl -L -o original.png "https://archive.org/download/solitiare-windows-95/Solitiare%20(Windows%2095).png"
```

Tool versions: Python 3.14.0, Pillow 12.3.0, curl 8.18.0 (x86_64-w64-mingw32), Windows 11 Pro 10.0.26200. No fonts are used or bundled. Cairo is not used.

## Variants and timing
- `original` → `source/original.png`: preservation only, not for on-screen use.
- `editorial-frame` → `exports/editorial-frame.png`: still, held for editorial timing. There is no animation and no duration.

## Review questions (evidence cannot settle these)
1. **Rights (R14).** Is this image usable in the video? There are two layers:
   - The screenshot author (Matthew Paul Argall) gives only an informal collection-level note, "Feel free to do what you wish with these screenshots", with a credit preference and no licence.
   - Microsoft's screenshot guidelines allow videos but say "Do not use portions of screenshots" and "Do not use screenshots that contain third-party content".
   
   The uncropped original contains third-party content, and the frame is a window crop. Options:
   - (a) accept under a fair-use or commentary rationale after legal review;
   - (b) accept under the Microsoft guidelines despite the crop;
   - (c) replace with a clean, uncropped capture from a licensed Windows 95 install that Devin runs himself (human handoff);
   - (d) cut.
2. **Authenticity labelling.** The image is a 2024 capture of Windows 95 running in VirtualBox, not a period screenshot. Is that acceptable for the script's "Windows 95 versions" cue, and should the edit or the credit say so?
3. **Framing.** The frame shows the Solitaire window only, at 2×. The alternative is the full 800×600 guest display, which includes an unidentified Windows 95 desktop wallpaper that adds third-party-content risk. Keep the window-only framing?
4. **Credit wording.** The proposed credit is "Microsoft Solitaire (Windows 95), screenshot by Matthew Paul Argall via Internet Archive." Should "Used with permission from Microsoft" be added? That is appropriate only if question 1 concludes the Microsoft conditions are met.

## Remaining blockers and observations
- Release is blocked on question 1. Production is complete.
- The script's claim (SCRIPT.md:593 / War/SCRIPT.md:650) that Solitaire was "written in C" was not checked. It is not a gate on this ticket, and no script change is proposed.
- Dependency OPS-01 (shared framing) is not consumed: the frame uses only the production-bible background token and safe-area values.
