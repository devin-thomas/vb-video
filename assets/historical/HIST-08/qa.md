# HIST-08 QA: Windows 95 launch footage still

**Production:** produced (historical proof) · **Release:** blocked (R14 rights unresolved) · **Checked:** 2026-09-15 by the HIST-08 worker agent · **Reviewer:** none yet (review deck)

## What was delivered

| Variant | File | Size | Notes |
|---|---|---|---|
| original | `source/original.png` | 720×480 stored raster, SAR 8:9 (4:3 display) | Uncropped decoded frame from the IA native original `CC1301_windows_95.mpeg`, seek 419 s (00:06:59) |
| editorial-frame | `exports/editorial-frame.png` | 1920×1080 | Full frame resized to 1440×1080, pillarboxed on black at x=240. No crop. |
| (proof) | `proofs/editorial-frame-720.png` | 1280×720 | Downscale for 720p inspection |

This is a still with no duration, fps, or named cutdowns; it holds for editorial timing.

**Source:** Computer Chronicles, "Windows 95" (1995), © Stewart Cheifet Productions. The frame comes from the report on the Redmond launch event (segment 00:06:36–00:08:22). Depicted event: Windows 95 launch, Microsoft, Redmond, WA, 24 August 1995. Full record: `evidence/source.json`; rights: `evidence/rights.json`; claims: `evidence/claim-checks.json`.

## Reproduction

From the repository root, Windows 11, Python 3.14.0, Pillow 12.3.0, ffmpeg/ffprobe 6.0-essentials_build-www.gyan.dev:

```
python assets/historical/HIST-08/src/acquire.py         # decodes one frame of the IA native MPEG-2 over HTTP into source/original.png
python assets/historical/HIST-08/src/render_frame.py    # writes exports/editorial-frame.png and proofs/editorial-frame-720.png
python assets/historical/HIST-08/src/build_delivery.py  # writes delivery.json (hashed inventory)
python tools/validate_delivery.py --id HIST-08
```

`acquire.py` needs anonymous network access to archive.org. It reads only the byte ranges needed to seek and decode, not the full 1.99 GB file.

## Tests actually run

1. **Native-file decode** (`acquire.py`). ffmpeg reported `pos:514136078 fmt:yuv420p sar:8/9 s:720x480 iskey:1 type:I checksum:BBA9F720`. The written PNG's pixels are identical to an independent earlier grab of the same seek (Pillow `tobytes()` comparison: True). PNG sha256 `88c0438ad6947720689371a4488fb5b93f80f472b1b7b2ab72aed9825262224f`.
2. **Derivative cross-check.** The same seek in the IA derivative `CC1301_windows_95.mp4` (640×480) shows the same shot and caption. The shot is stable across roughly 417–420 s and cuts to an audience close-up by 421 s.
3. **Render** (`render_frame.py`). Export is 1920×1080. Pillar pixels at (100,500) and (1800,500) read (0,0,0); the centre pixel is picture content.
4. **Manual inspection at full size (1920×1080).** 4:3 picture with no visible stretching: the lectern, "Start" sign, and people have natural proportions. The whole stored raster is present. The tape's thin black side blanking is visible at the inner pillar edges; it belongs to the source and was left in. The broadcast caption "MICROSOFT / REDMOND, WA" is intact and legible. No added text, UI, or watermark. Essential content sits within x=240–1680, inside the shared safe area x=120–1800.
5. **Manual inspection of a 1:1 crop** (export region 700,300–1500,900). No visible interlace combing on this static wide shot. The image is soft, with mild chroma bleed and SD-to-HD upscale softness, which is expected for 1995 SD video enlarged 2.25×. The "Start" sign and Windows flag screens are readable.
6. **Manual inspection at 720p** (`proofs/editorial-frame-720.png`). The composition reads clearly as a crowded launch auditorium with Windows branding. The caption is legible. The presenter at the lectern is too small to identify, so the frame does not claim to show Leno or Gates identifiably.
7. **Identity check.** The event is identified by the in-frame broadcast caption and the segment narration (00:06:46, 00:06:58), not by appearance. The date comes from a Microsoft press release of 21 August 1996. See `evidence/claim-checks.json`.
8. **`tools/validate_delivery.py --id HIST-08`.** Actual output is recorded below.

## Validator output

Run on 2026-09-15 after `build_delivery.py` (exit code 0). The command was re-run after this section was written and `delivery.json` was rebuilt, so the hashes include this file.

```
{
  "id": "HIST-08",
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

## Acceptance checks

- [x] The event is substantiated by the source (caption and narration). The date comes from a Microsoft primary release. The presenter is not identified from appearance.
- [x] The raw original frame (`source/original.png`) and the source-page records (`evidence/source-page/`) are preserved separately. The full native file is identified by its IA md5/sha1.
- [x] Credits and rights status are recorded, and the uncertainty is stated in `evidence/rights.json`. Nothing is cleared.
- [x] Framing is reversible and full-frame; no context is cut.
- [x] Every required output is present under the HIST-08 ID.
- [x] The tests listed above were actually run, and full-size and 720p inspection is recorded.
- [x] Source, authored additions (black pillars only), original media, transformations, and rights/claim status are kept distinct.
- [x] No private information, remote font/CDN dependency, or fabricated evidence. The only on-image text is the 1995 broadcast caption.
- [x] Dependency and gate status: OPS-01 is `produced` (shared_version win95-workbench-1.0.0). This still does not consume OPS-01 templates beyond the canvas and safe-area convention. R14 is open, so release is blocked.

## Review questions

**RQ-1 — Rights (for the producer, review deck, and legal).** The still comes from a copyrighted 1995 TV program: Computer Chronicles, "Windows 95", © Stewart Cheifet Productions. The English item on the Internet Archive has no license. The French version of the same program is marked CC BY-NC-ND 2.0, but that is a different item, and its NonCommercial/NoDerivatives terms may not fit a YouTube release or a reframed still. Microsoft's event staging and branding are in shot, and whether the report used Microsoft-supplied footage is unknown. Options:
- (a) Request permission or confirm license terms from Stewart Cheifet Productions.
- (b) Obtain a legal fair-use assessment for a short editorial still with credit.
- (c) Keep it as an internal proof only.
- (d) Drop it.

Evidence cannot settle this.

**RQ-2 — Editorial framing (taste).**
- The frame keeps the 1995 broadcast's "MICROSOFT / REDMOND, WA" caption. It is original context that identifies the location, but it is another program's graphic. A caption-free alternate exists at 418 s (same shot, lower third not yet on screen); the caption-bearing frame was chosen because it self-documents.
- Black pillarbox versus a designed backdrop is left to the edit.
- The SD source is visibly soft at 1080p.

**RQ-3 — SCRIPT.md:114 VISUAL cue (for the Writing Lead; SCRIPT.md not edited).** The cue reads "Windows 95 launch footage — the Rolling Stones, the lines outside CompUSA, the startup sound." The evidence found:
- The Rolling Stones link is the licensed "Start Me Up" song in the commercial, which CC1301 says was "previewed" at the launch. No Stones appearance is shown.
- No examined source substantiates lines specifically outside CompUSA. CC1301 says only "stores opening at midnight."
- The startup sound is audio and outside this still.

Proposed cue wording for consideration: "[VISUAL: Windows 95 launch footage — Microsoft's Redmond launch event, midnight store lines, the 'Start Me Up' campaign, the startup sound.]" Alternatively, keep "CompUSA" if another ticket sources it. This changes the visual cue only, not narration.

## Remaining blockers

- R14 rights decision (RQ-1). Release stays blocked until it is recorded.
- There is no Wayback capture of the IA details page (CDX was rate-limited and then returned empty). IA metadata and XML copies are preserved locally instead. No Save Page Now submission was made.
