# HIST-16 — Production QA

**Production:** produced (internal proof). **Release:** blocked. R14 is open because the selected image is © 1995 Sun Microsystems, all rights reserved.

## Delivered
- `source/original.gif` is the byte-exact period original: 506×232 GIF87a, sha256 `e11f4e6c…b5ed`.
- `exports/editorial-frame.png` is the 1920×1080 editorial frame.
- `proofs/editorial-frame-720.png` is the 720p review proof.
- `evidence/source.json`, `evidence/rights.json`, `evidence/claim-checks.json`, `evidence/provenance.json`, `evidence/source-excerpts.md` and `evidence/framing.json` are the source, rights, gate, provenance, excerpt and framing records.
- `evidence/source-pages/` holds the preserved source page, the program source, copyright pages and HTTP headers from three mirrors.
- `evidence/candidates/` holds two public-domain fallback originals from Wikimedia Commons (2006, 2007).
- `src/build_frame.py`, `src/finish_delivery.py` and `src/tests.json` are the framing source, the bundler and the test record.
- Every file is listed with bytes and SHA-256 in `delivery.json`.

## What the image is
The window is "The AWT Components", the example window from Sun's *The Java Tutorial* (lesson "AWT Components"). It is identified by the program source `GUIWindow.java` on the same mirror, not by appearance. The copy was online by 26 Feb 1996 (HTTP Last-Modified, Princeton spring-1996 course mirror). Java 1.0 shipped 23 Jan 1996 per Sun's press release. Byte-identical copies exist on the UPenn (1997) and CMU (1998) mirrors. The exact JDK build and the platform are not stated in any source, so neither is claimed.

## Variants
| name | file | timing |
|---|---|---|
| original | `source/original.gif` | still |
| editorial-frame | `exports/editorial-frame.png` | still; holds for editorial timing |

## Checks actually performed
- **Original byte-identical across three independent mirrors:** passed
- **Identity (window title and components match GUIWindow.java):** passed
- **Commons candidates match published SHA-1:** passed
- **Framing reversibility (automated, `build_frame.py`):** passed
  - No crop, 3× nearest.
  - The export's image region downsampled back to 506×232 equals the original's pixels.
- **Safe area and dimensions (automated):** passed
- **Manual visual inspection:** passed (below)
- **Privacy:** passed
  - The selected image carries only generic widget labels.
  - The page's FileDialog picture shows an employee's home path and was not used.

## Manual visual inspection
- **Full size.** Viewed `exports/editorial-frame.png` at 1920×1080.
  - The whole window is present, including all four border corners and the title bar.
  - Pixel-doubled edges are crisp, with no smoothing or colour shift.
  - All widget labels are legible, and the credit line is readable and unclipped.
  - No watermark, personal data or added UI.
- **720p.** Viewed `proofs/editorial-frame-720.png` at 1280×720.
  - The title, menu, list items, control labels and credit stay readable.
  - The tiny canvas coordinate labels are soft but legible, and non-essential.

## Authored additions
- The neutral dark ground (RGB 27,29,34). Teal was avoided so the frame does not imply Windows 95.
- The credit line: "“The AWT Components” example window — The Java Tutorial, Sun Microsystems (online copy dated Feb. 1996)". This is production wording, and its facts are backed by `evidence/source.json`.

## Reproduction
```
python assets/historical/HIST-16/src/build_frame.py
python assets/historical/HIST-16/src/finish_delivery.py
python tools/validate_delivery.py --id HIST-16
```
Toolchain:
- Windows 11 10.0.26200, Python 3.14.0, Pillow 12.3.0.
- Font: installed LiberationSans-Regular.ttf, not distributed.
- Downloads: curl from Git for Windows, anonymous HTTPS GET.

Source commands (2026-09-15):
```
curl -D g.hdr -o GUIWindow.gif https://www.cs.princeton.edu/courses/archive/spring96/cs333/java/tutorial/ui/overview/images/GUIWindow.gif
curl -o components.html https://www.cs.princeton.edu/courses/archive/spring96/cs333/java/tutorial/ui/overview/components.html
curl -o GUIWindow.java https://www.cs.princeton.edu/courses/archive/spring96/cs333/java/tutorial/ui/overview/example/GUIWindow.java
curl -o copyright.html https://www.cs.princeton.edu/courses/archive/spring96/cs333/java/tutorial/copyright.html
```

## Validator
`python tools/validate_delivery.py --id HIST-16` was run on 2026-09-15 after bundling. It exited 0 and returned `"ok": true, "errors": []`. Its stated limitations are: no OCR or visual judgment, no historical, semantic or legal clearance, and manual 1080p/720p review still required. Because adding this paragraph changes this file's hash, the bundle was rebuilt and the validator re-run before commit. The worker's report carries that final run.

## Gates, review questions and limits
- **R14: blocked.** The selected image has no licence, and its terms forbid reproduction without Sun's written permission. Review question: use under a documented fair-use decision, request Oracle permission, or substitute the public-domain fallback `AWT_at_Linux.png`, which is 2007 / Java 5 and must not be presented as 1995.
- **Writing Lead, non-blocking.**
  - The cue "The buttons look wrong on every platform" cannot be shown with one single-platform period screenshot.
  - "Released in 1995" matches Sun's own record (alpha March 1995, announced May 1995), though 1.0 shipped January 1996.
  - `War/SCRIPT.md` was not edited.
- Sun's own server copy could not be retrieved: the Wayback Machine returned offline, then 429, then an empty result. The original comes from a university mirror.
- Reviewer: none yet. Structure validation does not certify historical or legal truth.
