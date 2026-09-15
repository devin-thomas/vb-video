# HIST-13 QA — Metrowerks CodeWarrior IDE

**Outcome:** produced as a historical proof. **Release:** blocked (R14 rights unresolved).
**Reviewer:** none yet (agent QA only; release decision belongs to the OPS-04 review deck).
**Date:** 2026-09-15

## Deliverables and variants

| Variant | File | Notes |
|---|---|---|
| `original` | `source/original.jpg` | Raw DCT stream of PDF page 63 (`/Im0`), byte-unchanged, 2045×2785 greyscale, SHA-256 `d92db892…5f5` |
| `editorial-frame` | `exports/editorial-frame.png` | 1920×1080 RGB, still (no duration, no fps) |

Supporting files: `src/build_frame.py` (framing script), `evidence/transform.json` (all crop, scale and placement parameters), `proofs/editorial-frame-720.png` (1280×720 proof), `evidence/source-page/*` (host listing capture and headers), and `evidence/candidates/metrowerks-ide-tour-fig4.gif` (alternate, not used in the export).

## Reproduction

```
python assets/historical/HIST-13/src/build_frame.py
```

To re-acquire the original, download `https://vintageapple.org/macprogramming/pdf/Metrowerks_Code_Worrior_Programming_1995.pdf` and check its SHA-256 is `b129ccb1e14e00b3b089d36b5fe3b2b219bdce197845d6a1967827a304e3d808`. Then write page 63's `/Resources/XObject/Im0` raw stream bytes, which should hash to `d92db8928ea9c2be5d8317ff0112a53fa763ec6d537bfb5edbd5b642084da5f5`. The pypdf helper `page.images[0].data` re-encodes the image, so use the raw stream (`xobject._data`) instead.

Toolchain: Windows 11 10.0.26200, Python 3.14.0, Pillow 12.3.0, pypdf 6.13.3, numpy 2.4.6 (crop-border measurement only), curl 8.18.0, git 2.53.0.windows.1. No installs performed, no font files, no network use at render time.

## Tests actually run

| Test | Result |
|---|---|
| `python tools/validate_delivery.py --id HIST-13` | see `delivery.json` → `tests`, and the final report |
| Source-file hashes `sources/ASSET_PLAN.md`, `sources/SCRIPT.md` | match `8f1769aa…` and `3821db54…`; not modified |
| Original is a real JPEG | magic `ffd8ffee`, ends `ffd9`, decodes as JPEG L 2045×2785 |
| Raw stream equals repo original | SHA-256 match, `d92db892…` |
| Export dimensions | `exports/editorial-frame.png` 1920×1080 RGB; proof 1280×720 RGB |
| Deterministic rebuild | Rebuilt once; the frame, 720p proof and `transform.json` were byte-identical before and after |
| Uniform scale, no stretch | Shared factor 0.87. Integer rounding of panel sizes gives effective x/y scales of 0.8690–0.8703 (under 1 px), with no anisotropic stretch |

## Manual visual inspection

- **Full size (1920×1080):** viewed the whole export, then 1:1 tiles of the left panel (0–1000 × 0–1080) and the right panel (1000–1920 × 300–780).
  - Window titles `New Window`, `OOPexample.cp` and `OOPexamplePPC.µ` are sharp.
  - Every code line is legible, as are the project entries `Group 1`, `OOPexample.cp`, `InterfaceLib` and `MWCRuntime.Lib`, and the footer `3 file(s)`.
  - Mac chrome is intact: close and zoom boxes, scroll bars, and the `Line: 1` status bar.
  - No crop clips a window edge.
  - Print halftone and paper texture are visible, as expected for a book scan.
  - Faint show-through from the reverse page is visible in the white paper areas, mostly left of and below the editor and under the project window. It is unretouched by design.
- **720p (`proofs/editorial-frame-720.png`):** code text, window titles and project entries all remain readable. The layout sits inside the 90% safe area (content spans x 99–1820, y 87–993 at 1080p).
- **Content check:**
  - No added text, captions, labels, watermarks, fictitious UI, private information or remote assets.
  - Book captions, page number, running head and body text were deliberately excluded by the crop.
  - The two figures sit side by side here; the book stacks them. That arrangement is recorded in `evidence/transform.json`.
- **Meaning check:** Figure 2.40 shows the program's output window above its source file. Both stay together in the left panel, so the output-and-source relation is preserved.

## Identity, version, host OS

- The window is the Macintosh CodeWarrior IDE, not a Windows-hosted build. Evidence:
  - The book is about Mac-only development.
  - The window chrome is classic Mac OS.
  - The project file uses the `µ` suffix.
  - The project lists the PowerPC Mac libraries InterfaceLib and MWCRuntime.Lib.
  - Figure 2.41's caption names the PowerPC version.
- The version is CW5-era, 1995. The copyright page reads © 1995, book p. 4 says CW5 is current and CW6 is coming, and the CD figures say "CW5 Gold".
- The exact IDE build is not stated in the source and is not claimed.
- Three Windows-hosted 1997 Metrowerks screenshots were found and rejected; see `evidence/candidates.json`.

## Rights (R14)

Blocked. The book is all-rights-reserved (M&T Books, 1995), and the depicted UI belongs to Metrowerks/NXP and Apple. The host vintageapple.org gives no license. Nothing was accessed through an account, terms prompt, payment, CAPTCHA or lending gate. Full record: `evidence/rights.json`. The only public-domain CodeWarrior image found (Wikimedia Commons) shows packaging, not the IDE.

## Remaining blockers and review questions

1. **Rights (R14):** use this 1995 book screenshot under a documentary commentary rationale, seek permission, or pick another route?
2. **Look vs. authenticity (taste):** the script cue says the IDE "looks like a Mac app — more polished than the VB IDE". This source is a greyscale halftone print scan with show-through, which may read as less polished than a native capture. The alternative is `evidence/candidates/metrowerks-ide-tour-fig4.gif`: a native-pixel Mac screenshot published by Metrowerks, but 403×413 px, 1997-era with its version unconfirmed, and showing only a project window.
3. **Writing Lead (script wording, not edited):** SCRIPT.md:649 says CodeWarrior was dominant "through most of the 90s". CodeWarrior launched in January 1994 (secondary source: Wikipedia; not verified against a primary source here), so "from the mid-90s" may be more accurate.

## Capability notes

- web.archive.org was reachable from curl only intermittently over HTTP and never from WebFetch, so the Metrowerks "IDE tour" parent article (needed to date and version the alternate) was not recovered.
- preserve.mactech.com has an expired TLS certificate. Certificate checks were not bypassed.
