# XTRA-03 — Early BASIC-era terminal hardware: QA

**Production:** produced (historical proof). **Release:** blocked (R14 open, review questions below).
**Worker:** Archive Extras worker (manager session vb-25), 2026-09-15. **Reviewer:** none yet.

This is a script-supplement asset (SCRIPT.md:63, "Old terminal hardware"), not an ASSET_PLAN row.

## What is delivered

| Path | Role |
|---|---|
| `source/original.jpg` | Acquired native original, byte-identical to Wikimedia Commons (SHA-1 `5df1ff6e…6a77` matches the Commons API) |
| `exports/editorial-frame.png` | 1920×1080 editorial frame: whole photo scaled to 1440×1080 and pillarboxed. No crop, no stretch, no overlay |
| `evidence/proof-720p.png` | 1280×720 downscale of the frame, used for the 720p check |
| `evidence/framing.json` | Scale, placement box and reversal instructions written by the renderer |
| `src/render_frame.py` | Exact renderer (hash-checks the original and never writes it) |
| `evidence/source.json`, `evidence/rights.json`, `evidence/provenance.json`, `evidence/claim-checks.json`, `evidence/source-excerpts.md` | Source record, licence and candidates, provenance, gate and claim checks, excerpts |

Variants: `original` → `source/original.jpg`; `editorial-frame` → `exports/editorial-frame.png`. Still asset: no duration, fps or cutdowns.

## Reproduction

From the repository root:

```sh
python assets/historical/XTRA-03/src/render_frame.py
python tools/validate_delivery.py --id XTRA-03
```

Toolchain: Python 3.14.0, Pillow 12.3.0, Windows-11-10.0.26200-SP0. No CairoSVG, Chromium, ffmpeg or fonts are involved, because the frame contains no text. Acquisition used curl 8.18.0 (anonymous GET of the Commons original).

## Checks actually run

1. **Original integrity.** SHA-256 of `source/original.jpg` was taken before and after rendering: `8bfd08bf3a77e1632d6ec43c5b5f566b0719b2e8a3b7524c14736b5a3f5fcc16`, unchanged. SHA-1 and byte size (1,748,549) match the Commons imageinfo API.
2. **Renderer output.** Placed box `{x:240, y:0, w:1440, h:1080}`, scale 0.441176. Source 3264×2448 (4:3) and placed 1440×1080 (4:3) have exactly the same aspect, so nothing is stretched.
3. **Export structure (Pillow).** `exports/editorial-frame.png` is 1920×1080 RGB and `evidence/proof-720p.png` is 1280×720. Pixel probes: bar pixels (0,540) and (239,540) are (17,19,24) = #111318, the picture starts at x=240, and the right bar begins at x=1680.
4. **Manual viewing at full size.** I viewed the 1920×1080 frame whole, plus three native-pixel (100%) crops at 760×460 and 560×1080 from the frame (keyboard and decal, left seam, right seam):
   - The picture reads clearly as a teleprinter with paper roll, tape punch/reader and keyboard.
   - Keycap legends (CTRL, ESC, SHIFT, X-ON) and the START/STOP/FREE switch are legible.
   - No stretching, banding or resampling artefacts; the softness is the 2014 phone photo's own.
   - The pillarbox seams are clean, with no picture content cut at either edge.
   - The "TimeShare Corporation" decal, the yellow museum sign (top) and the cut-off CHM card ("ASR-33 Telet…", right) are all still visible.
5. **Manual viewing at 720p.** At 1280×720 the machine stays recognisable, and the keyboard and paper roll read at a glance. The decal is legible and the museum card text is not. No composition problem found.
6. **Safe area.** No essential text is added. The subject sits within x=120…1800 and y=72…1008, apart from the lower part of the tape unit, which runs to the bottom edge as in the original.
7. **Content checks.**
   - No people, so no overlap with HIST-04 (whose folder held only a planning state.json).
   - Not a CRT terminal.
   - No invented UI, captions, watermark removal or AI imagery.
   - No remote font/CDN dependency.
   - EXIF, including camera metadata, is not carried into the PNGs; the original keeps its EXIF untouched.
8. **Delivery validator.** `python tools/validate_delivery.py --id XTRA-03` was run after delivery.json was written. Its verbatim result is recorded in delivery.json `tests` and the completion report.

These tools do not judge historical truth or legal clearance. Those sit in the evidence files and the review questions.

## Editorial findings (worked, not assumed)

- Dartmouth's own 19 Oct 1964 description names **Model 35** teletypes. GE's 26 Mar 1965 revision names **"model 33/35"**. The pictured machine is a **Model 33 ASR** in a museum, so it is representative period hardware documented for the system by 1965, not the terminal from 1 May 1964 and not a Dartmouth unit. No caption may say otherwise. A proposed caption is in `evidence/source.json`.
- No free-licensed Model 35 photo exists on Commons (checked). Genuine 1964 Dartmouth terminal photos exist in the *Dartmouth Alumni Magazine*, Nov 1964, pp. 26–29, but they are marked all rights reserved and are only available at 600 px. They were not acquired.
- No War/SCRIPT.md change is needed: the narration names no terminal or computer model.

## Remaining blockers and review questions

- **R14: blocked.** Licence recorded (CC BY-SA 3.0 / GFDL 1.2+) but not cleared.
- **RQ1 (legal):** Is the ShareAlike licence acceptable for a still in the finished video? The fallback is a CC BY 2.0 Model 33 photo (Kai Wegner), not yet inspected because Commons rate-limited the download.
- **RQ2 (editorial/permission):** Keep this representative museum Model 33, or ask Dartmouth for permission and a high-resolution scan of the Nov 1964 College Hall terminal photo? That needs a human request; none was sent.
- **RQ3 (taste):** Are the visible "TimeShare Corporation" decal and cut-off museum card acceptable, given that cropping them was avoided?
