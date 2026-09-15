# HIST-01 — Production QA

**Production:** produced (historical proof). **Release:** blocked (R14 rights unresolved).

## Delivered
| Path | What it is |
|---|---|
| `source/original.png` | Byte-exact 640×480 capture "Microsoft Visual Basic 1.0 for Windows - Edit" from WinWorld (variant `original`) |
| `exports/editorial-frame.png` | 1920×1080 editorial frame: whole capture at 2× nearest-neighbour, pillarboxed on #111318 (variant `editorial-frame`) |
| `proofs/editorial-frame-720.png` | 1280×720 review proof |
| `evidence/version-evidence/about-original.png` | Companion capture with "Microsoft Visual Basic Version 1.0" About box (evidence only) |
| `evidence/source.json`, `rights.json`, `provenance.json`, `claim-checks.json`, `source-excerpts.md` | Source record, rights layers, provenance, gate and claims, excerpts |
| `evidence/source-pages/` | Preserved host pages: WinWorld product/screenshot/copyright pages, Wayback product page, Internet Archive files.xml and meta (uploader e-mail redacted), Microsoft permissions page |
| `evidence/render-tests.json` | Machine checks from the render |
| `src/frame.json`, `src/frame.py`, `src/build_delivery.py` | Framing parameters, render/test script, delivery inventory builder |

Every file except `delivery.json` and `state.json` is inventoried with bytes and SHA-256 in `delivery.json`.

## Checks actually performed (2026-09-15)
1. **Acquisition integrity.** `source/original.png` MD5 `6b76946459abf915d190f65da4cc4e33` equals the hash in WinWorld's file name. `about-original.png` MD5/SHA-1 equal the Internet Archive `files.xml` record, and a separate WinWorld download is byte-identical (`cmp`).
2. **Render checks** (`evidence/render-tests.json`, all true): the export is 1920×1080; aspect ratio is preserved; the whole screenshot is included with no crop; cropping [320,60,1600,1020] and downscaling 2× nearest gives back the original pixels exactly; every source pixel is an exact 2×2 block; the area outside the image is a single background colour.
3. **Determinism.** Re-running `frame.py` produced identical SHA-256 for the export (`3ada23af…728c`) and the 720p proof (`0531d639…5560`).
4. **Manual visual inspection, full size.** I viewed `exports/editorial-frame.png` at 1920×1080. The screenshot is intact and sharp, with no stretch, crop, watermark or added UI. The title bar "Microsoft Visual Basic [design]", menus, properties bar, toolbox, Calculator form in the designer, CALC.MAK project window and CALC.FRM code are all legible. The image spans y=60–1020, 12 px past the text safe area top and bottom; it carries no production text, and the result is recorded, not hidden.
5. **Manual visual inspection, 720p.** I viewed `proofs/editorial-frame-720.png`. The toolbox icons, form buttons, the properties-bar values and the code text are all still readable.
6. **Source views.** I viewed both 640×480 originals at native size before selecting. The About capture reads "Microsoft Visual Basic Version 1.0" and "Copyright © 1987-1991 Microsoft Corp.".
7. **Content hygiene.** The export has no private information. The About capture's serial number stays in evidence only. The Internet Archive uploader e-mail is redacted from the saved meta copy, and an e-mail pattern scan of `evidence/` was run. No remote fonts or CDN: the frame contains no text.
8. **Validator.** `python tools/validate_delivery.py --id HIST-01`, result below.

## Reproduction
From the repository root:

```
python assets/historical/HIST-01/src/frame.py
python assets/historical/HIST-01/src/build_delivery.py
python tools/validate_delivery.py --id HIST-01
```

Acquisition, with anonymous public GETs only:

```
curl -sSL -o original.png "https://winworldpc.com/res/img/screenshots/10-6b76946459abf915d190f65da4cc4e33-Microsoft%20Visual%20Basic%201.0%20for%20Windows%20-%20Edit.png"
curl -sSL -o about-original.png "https://archive.org/download/3d-4d-42c-6-9257-c-3b-1-11c-3-a-4c-2a-90f-7054-1/10-90e6baa26dbdfecab22d43996e687c4c-Microsoft%2520Visual%2520Basic%25201.0%2520for%2520Windows%2520-%2520About%5B1%5D.png"
```

Tools: Python 3.14.0, Pillow 12.3.0, curl 8.21.0 (Windows, Schannel), Windows-11-10.0.26200. No Cairo, browser or font needed.

## Variants and timing
- `original` → `source/original.png` (640×480, unmodified).
- `editorial-frame` → `exports/editorial-frame.png` (still; holds for editorial timing; no animation).

## Remaining blockers and review questions
- **R14 blocked.** No licence for the capture, capturer unknown; Microsoft screenshot-guideline fit needs rights review (RQ-HIST01-1).
- **RQ-HIST01-2 (Writing Lead).** The script asks for "the properties window". VB 1.0 shows a properties bar. `War/SCRIPT.md` was not edited.
- **RQ-HIST01-3.** Use the Edit capture alone, or also the About capture as on-screen version proof?
- The Calculator project's origin (Microsoft sample or not), the capture date and the Windows 3.0 vs 3.1 host are not established.

Reviewer: none yet. Release approval comes from the OPS-04 review deck.

## Validator output
`python tools/validate_delivery.py --id HIST-01` (2026-09-15, exit 0):

```json
{
  "id": "HIST-01",
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

This covers structure and hashes only. It does not clear rights or history.
