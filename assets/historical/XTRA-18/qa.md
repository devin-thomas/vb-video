# XTRA-18 — Production QA

**Production:** produced. **Release:** blocked (R14: rights unclear). This is a historical proof with unresolved rights, not cleared media.

## Delivered
- `source/original.gif`: acquired original, 640×480 GIF89a, 17,876 bytes, SHA-256 `43aed772b74691983af34bb3c5d1288e8432a5474fe7a057502ff51f948890c5`. Never modified.
- `exports/editorial-frame.png` (variant `editorial-frame`): 1920×1080.
- `proofs/editorial-frame-720.png`: 1280×720 review proof.
- `src/render_editorial_frame.py`: the framing script.
- `evidence/`: `source.json`, `rights.json`, `provenance.json`, `claim-checks.json`, `source-excerpts.md`, `framing.json`, `search-log.json`.
- `delivery.json` lists every file with its byte size and SHA-256.

The variant `original` is `source/original.gif`. `editorial-frame` is `exports/editorial-frame.png`. Both are stills with no duration.

## Subject
Microsoft Hearts, title bar "The Microsoft Hearts Network", running under Windows for Workgroups 3.11. The capture comes from Nathan Lineback's Toasty Technology GUI Gallery page http://toastytech.com/guis/win311.html, accessed 2026-09-15. The game version is not visible in the capture. Evidence and limits are in `evidence/source.json`.

This is a script-only supplement (SCRIPT-SUPPLEMENT) for `SCRIPT.md:579`, not an original asset-plan row.

## Method
1. Downloaded the one GIF with curl over plain HTTP. No login, terms, CAPTCHA or payment was involved.
2. Hashed it and copied it byte-for-byte to `source/original.gif`.
3. Framed it with `src/render_editorial_frame.py`:
   - refuses to run unless the source hash matches
   - no crop
   - exact 2× nearest-neighbour enlargement to 1280×960
   - centred at (320, 60) on #111318
   - no burned-in text
4. The script checks that every placed pixel equals its source pixel, then writes `evidence/framing.json`.
5. The 720p proof is a uniform reduction of the finished frame.

## Reproduction
From the repository root:
```
python assets/historical/XTRA-18/src/render_editorial_frame.py
python tools/validate_delivery.py --id XTRA-18
```
The render was run twice and produced identical files:
- export SHA-256 `40c5f09b705d417f5bae8f04a150b86719e31233868bccfca4e3349b2f233228`
- proof SHA-256 `d1ba4c63c5b2a06000cb1244968af2e5f6543bb8f1332d976e6ce846ed5ee915`

Toolchain:
- Windows-11-10.0.26200-SP0
- PowerShell 7.6.6
- Python 3.14.0
- Pillow 12.3.0
- curl (Git Bash) for acquisition

No CairoSVG, Playwright or tools/render pipeline was needed: this is a raster framing of an archival original. No fonts are used or bundled.

## Checks actually performed
- **Source integrity:** passed. Downloaded bytes = `source/original.gif` = the hash pinned in the script. HTTP 200, image/gif, Content-Length 17876.
- **Integer scaling, no stretch:** passed. Scale factor 2 on both axes. The per-pixel nearest-neighbour check inside the render script passed. Aspect ratio 4:3 preserved.
- **No crop:** passed. The placed size, 1280×960, is exactly 2 × 640×480.
- **Export dimensions:** passed. The export is 1920×1080 RGB PNG; the proof is 1280×720.
- **Ground colour at margins:** passed. (0,0), (319,540), (1600,540), (960,59) and (960,1020) are all #111318.
- **Safe area:** passed for essential text. The capture's status-bar text (source rows 461–473) lands at y=982–1007, inside y≤1008. The window frame reaches y=1019, in the margin.
- **JSON evidence parses:** passed for all 7 JSON files in `evidence/` (6 checked with ConvertFrom-Json, plus the regenerated framing.json).
- **Literal excerpt:** passed. `evidence/source-excerpts.md` lines equal `sources/SCRIPT.md:579–593`, asserted by the generator.
- **Structure validator:** `python tools/validate_delivery.py --id XTRA-18`. The result is recorded in `delivery.json` tests and reported to the manager.

## Manual visual inspection
- **Full size (1920×1080):**
  - Viewed `exports/editorial-frame.png` whole, then as four 960×540 quadrant crops at 1:1.
  - Pixels are crisp 2×2 blocks with no blur or resampling fringes. The title bar "The Microsoft Hearts Network", the menus, the green felt, the card backs and faces, "Pass Left", the player names and the status text are all legible.
  - The second, partly off-screen Hearts window at right is intact, as in the original; it was not cropped because the capture is full-screen.
  - Dark ground on all sides. Nothing added.
- **720p (1280×720):**
  - Viewed `proofs/editorial-frame-720.png`.
  - The title bar, player names and status text remain readable. Card ranks are readable but small.
- **Content check:**
  - No watermark.
  - No private information beyond the first names typed into the game ("Nathan", "Bill", "Anna", "Terri").
  - No remote font or CDN dependency. No VB or language label.
- **Reviewer:** the XTRA-18 worker agent only. No human media review has taken place.

## Gates, blockers and limits
- **R14: blocked.**
  - Microsoft UI copyright is subject to Microsoft's conditional screenshot permission. The capture layer (Nathan Lineback) carries no stated licence.
  - See `evidence/rights.json` and review question RQ-1 in `evidence/claim-checks.json`.
- **Not-VB claim: handled in the asset.**
  - The asset makes no language claim.
  - The script calls these "shareware" games and follows with "written in Visual Basic". That is referred to the Writing Lead as RQ-2; War/SCRIPT.md was not edited.
- **Version limits.**
  - WfW 3.1 and 3.11 cannot be told apart from the pixels.
  - The capture date and first-publication date are unknown.
  - Release dates rest on secondary sources, because web.archive.org was unreachable.
- **Windows 95.** No Windows 95 Hearts capture with period chrome was found. The Internet Archive's Windows 9x Hearts screenshot is Italian and uses a modern window frame, so it was rejected (`evidence/search-log.json`).
- **What validation covers.** `tools/validate_delivery.py` checks structure only. It does not judge image content, history or legal status.
