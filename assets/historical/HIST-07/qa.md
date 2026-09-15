# HIST-07 QA: TRS-80 BASIC boot screen

**Worker:** HIST-07 agent (Historical Screenshots department), 2026-09-15
**Production status:** produced
**Release status:** blocked. R14 rights review is pending; see the review questions.
**Reviewer:** none yet (OPS-04 review deck)

## Outputs
| Variant | File | Notes |
|---|---|---|
| `original` | `source/original.jpg` | Byte-exact 2019 Commons upload of File:Trinity77.jpg, 3973×1853, sha1 `cbaeec4d22aaefe9ffc0ae7656cb0fa9e3adaf59` (matches the Commons file-history record) |
| `editorial-frame` | `exports/editorial-frame.png` | 1920×1080 still. Reversible crop, uniformly scaled and pillarboxed, with a two-line credit |

These are stills, so there is no duration or fps. Hold the frame for whatever the edit needs; the ticket's timing is only a proposal.

Review proofs: `qa/editorial-frame-720p.png` (1280×720 downscale) and `qa/editorial-frame-1080p-check.png` (1:1 crop of the export's screen area).

## Tests actually run
1. **Source integrity.** SHA-1 of the downloaded file = `cbaeec4d22aaefe9ffc0ae7656cb0fa9e3adaf59`, equal to the Commons API `sha1` for the 2019-05-26 version. The renderer re-checks this before every render. **Pass.**
2. **Identity verification at full resolution.** I inspected a native-pixel crop of the TRS-80, rechecked at 1:1 and 4× nearest-neighbour after the manager's correction. The screen reads `MEMORY SIZE?` ×2, `RADIO SHACK LEVEL II BASIC`, `READY`, `>?MEM`, ` 31956` (soft), `READY`, `>_`. The badges read Radio Shack / TRS-80, and the form factor is a Model I with Expansion Interface. The first lines match the power-up text in the 1978 Radio Shack Level II BASIC Reference Manual; the manual shows `MEMORY SIZE?` once. **Pass for identity** (ROM revision unknown).
   - **Correction:** the screen is a short session after power-up, not a clean boot screen. `>?MEM` (a typed PRINT MEM command), its result ` 31956`, the second `READY` and the `>_` cursor are not part of the documented power-up text. My first transcription read `>MEM`; that was wrong.
3. **Export structure.** Pillow reports `exports/editorial-frame.png` as 1920×1080 RGB PNG and `qa/editorial-frame-720p.png` as 1280×720. **Pass.**
4. **No stretching.** A single uniform scale factor of 0.687097 is applied to the crop 1233×1240 → 847×852. The aspect ratio is kept within rounding. **Pass.**
5. **Reversibility.** `evidence/crop.json` records the native crop box (2740,190)-(3973,1430), scale and placement. The original is unmodified. **Pass.**
6. **Safe area.** The photo occupies y 72–924 and x 536–1383. The credit text sits inside y ≤ 1008 and inside x 120–1800. **Pass.**
7. **Delivery validator.** `python tools/validate_delivery.py --id HIST-07`. The result is recorded in delivery.json `tests` and in the worker report.
8. **Evidence JSON parse.** All `evidence/*.json` files load with `json.load`. **Pass.**

## Manual visual inspection
- **Full size (1920×1080), `exports/editorial-frame.png`:** The TRS-80 Model I is fully in frame (monitor, Expansion Interface, keyboard). Nothing is cut that changes meaning. The neighbouring Apple II is excluded, and only a wood rail at the left edge remains. The on-screen prompt is legible: "MEMORY SIZE?", "RADIO SHACK LEVEL II BASIC", "READY". The credit is readable at 26 px Liberation Sans with clear separation from the photo. The upscaled screen shows no banding or JPEG blocking beyond what the source has. There is no watermark and no added UI.
- **720p (`qa/editorial-frame-720p.png`):** The banner line "RADIO SHACK LEVEL II BASIC" and "READY" can still be made out. "MEMORY SIZE?" is readable. The credit is readable. As a montage tile smaller than roughly half-frame, the prompt text will not be legible, so an editor who needs legibility at small sizes should punch in on the screen, which is available from the original at native resolution.
- **1:1 screen check (`qa/editorial-frame-1080p-check.png`):** The phone-camera source is slightly soft on the text. I did no sharpening.

## Content checks
- The source is a real photograph of real vintage hardware (2019, iPhone 6s EXIF), not an emulator, a modern terminal imitation or an AI image.
- The screen shows a short Level II BASIC session after power-up, not a clean boot screen. After the documented power-up text, someone typed `?MEM` and BASIC printed ` 31956`, then `READY` and the cursor. This is authentic and not staged by us. The caption no longer says "power-up prompt"; it now reads "TRS-80 Model I running Level II BASIC".
- The frame contains no private information. The source JPEG's EXIF carries GPS coordinates that the uploader already published on Commons. The export PNG contains no EXIF. See RQ-3.
- No remote fonts or CDN. The font is the installed system `C:\Windows\Fonts\LiberationSans-Regular.ttf` (not bundled).
- Saved source-page copies have one third-party email address redacted.

## Candidates considered
1. **Selected:** File:Trinity77.jpg, 2019 original (Tim Colegrove, CC BY-SA 4.0). Model I; Level II BASIC power-up text followed by a typed `?MEM` command and its result.
2. File:TRS-80 Model 4 (2).jpg (Blake Patterson, CC BY 2.0, 1024×768). Model 4 in Model III BASIC; power-up text followed by typed input and three ?SN Error lines. Not acquired into the repo.
3. File:TRS-80 (1977) (38333775292).jpg (Wolfgang Stief, CC0). Model I mid-session, reflection-washed, crowded frame. Not acquired.

Full search log: `evidence/source.json`.

## Review questions (for the OPS-04 deck)
- **RQ-1 (rights/legal, R14):** The photo is CC BY-SA 4.0. Is the ShareAlike obligation acceptable for use in the video, and is on-screen credit plus a description credit sufficient attribution? The worker recorded the license but cannot decide adaptation versus collection or clear release.
- **RQ-2 (rights, R14):** Radio Shack/TRS-80 trademarks and ROM BASIC banner text appear incidentally on the depicted hardware. Is any further clearance wanted? The worker makes no legal determination.
- **RQ-3 (privacy/policy):** `source/original.jpg` is kept byte-exact and so retains GPS EXIF (already public on Commons). Keep it as is for provenance, or store a metadata-stripped copy? Stripping would break the Commons SHA-1 match.
- **RQ-4 (editorial/taste):** Keep the burned-in credit line, or deliver a clean frame and carry attribution in captions or end credits? The script's cue suggests a C64 / Apple II / TRS-80 montage; the credit band may need removing for tiling.
- **RQ-5 (editorial/accuracy):** The photo is from 2019 and the narration says "in 1982". The image shows authentic hardware and ROM output but is not a period photograph. Is labeling it as a TRS-80 Model I (without a date claim) acceptable?
- **RQ-6 (editorial/accuracy):** The script cue asks for "boot screens ... showing their BASIC prompts". This screen shows the power-up text, then a typed `?MEM` command, its result ` 31956`, a second `READY` and the cursor. Is that acceptable for the boot-screen cue, or should another candidate be reconsidered? None of the three candidates is a clean boot screen. Candidate 2 (Model 4) has typed input and ?SN Error lines. Candidate 3 (Model I at VCFB 2017, CC0) is mid-session. A clean screen would need a new search or a different source.

No script discrepancy was found. `War/SCRIPT.md` was not edited and no Writing Lead change is proposed.

## Remaining blockers
- Release is blocked on RQ-1 and RQ-2 (R14). Production is complete.
- Dependency OPS-01 has no input consumed by this still (no shared template or style asset used beyond documented palette values). Its status was not checked or modified here.

## Reproduction
From the repo root on Windows:

```powershell
# 1. Acquire (already done; the file is in source/original.jpg)
Invoke-WebRequest -UserAgent "VBWarVideoResearch/1.0" -Uri "https://upload.wikimedia.org/wikipedia/commons/archive/f/ff/20240129110637%21Trinity77.jpg" -OutFile assets/historical/HIST-07/source/original.jpg
(Get-FileHash -Algorithm SHA1 assets/historical/HIST-07/source/original.jpg).Hash  # CBAEEC4D22AAEFE9FFC0AE7656CB0FA9E3ADAF59
# 2. Render the editorial frame and proofs
python assets/historical/HIST-07/src/render_editorial_frame.py
# 3. Validate
python tools/validate_delivery.py --id HIST-07
```

Commons URLs can return HTTP 429 when requests are rapid. Wait and retry.

## Toolchain
- Python 3.14.0 (MSC v.1944, AMD64)
- Pillow 12.3.0
- Font: Liberation Sans Regular, `C:\Windows\Fonts\LiberationSans-Regular.ttf`, sha256 `76d04c18ea243f426b7de1f3ad208e927008f961dc5945e5aad352d0dfde8ee8` (fontconfig 2.18.3 `fc-match "Liberation Sans"` resolves to it)
- PowerShell 7.6.6, git 2.53.0.windows.1
- No cairosvg/Playwright used. The render is Pillow only.
