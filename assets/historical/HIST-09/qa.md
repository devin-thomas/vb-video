# HIST-09 QA: CompUSA storefront

**Outcome:** produced as a historical proof. **Release:** blocked (R14 rights unresolved).
**Worker:** Claude Code (Opus 5), branch `ticket/HIST-09`, 2026-09-15. **Reviewer:** none yet (review deck).

## What was delivered

| Path | What it is |
|---|---|
| `source/original.png` | Uncropped, unscaled decoded frame (854×480) from the 1995 home video. Variant `original`. |
| `exports/editorial-frame.png` | 1920×1080 editorial framing. Variant `editorial-frame`. |
| `proofs/editorial-frame-720.png` | 1280×720 review proof |
| `source/make_editorial_frame.py` | Deterministic framing script (writes the export, the proof and `evidence/framing.json`) |
| `evidence/source.json`, `rights.json`, `provenance.json`, `claim-checks.json`, `source-excerpts.md`, `framing.json` | Source record, rights analysis, provenance, gates/claims/review questions, excerpts, framing inverse |
| `evidence/archive-records/*` | Raw Internet Archive metadata (3 items) and YouTube original-upload records (5 videos) |
| `evidence/candidates/*` | Ranked candidate report, search log, two runner-up frames |

Still image: no duration, fps or timeline. It holds for editorial timing.

## Reproduction

Tools: Windows 11 (10.0.26200), PowerShell 7.6.6, Python 3.14.0, Pillow 12.3.0, ffmpeg/ffprobe 6.0 essentials build (gyan.dev).

```powershell
# 1. Fetch the archive file and verify it against IA's published hashes
Invoke-WebRequest "https://archive.org/download/1995.08.23-windows-95-midnight-madness-norwalk-ct-wg-g-7-klymsg-0-854x-480/1995.08.23-Windows95-Midnight-Madness-NorwalkCT%5BWgG7KLymsg0%5D%5B854x480%5D.mp4" -OutFile norwalk.mp4
Get-FileHash norwalk.mp4 -Algorithm SHA256   # f6d309c70d1eccbc9e3af3ba124bf123724e0427dca83789635e74310baeccb6 (IA sha1 f79a200eeee5964ef6bcbfb714f5d209595168a4)
# 2. Decode exactly frame n=1066 (pts 1067066 @ 1/30000 = 35.5689 s), no scaling
ffmpeg -i norwalk.mp4 -map 0:v:0 -vf "select='eq(n\,1066)',showinfo" -fps_mode passthrough -frames:v 1 -y assets/historical/HIST-09/source/original.png
# 3. Framing (crop black pillarbox to the 640x480 picture at x=107, uniform 2.25x Lanczos, center on 1920x1080 black) and 720p proof
python assets/historical/HIST-09/source/make_editorial_frame.py assets/historical/HIST-09
```

## Tests actually run

| Test | Result |
|---|---|
| Downloaded MP4 matches the IA file record (size 32302815, sha1, md5) | passed |
| `ffprobe` stream check: H.264 854×480, SAR 1:1, 30000/1001 fps, progressive | passed |
| Frame selection: 73 native frames (n=1019–1091) scored for edge variance in the sign and date-stamp bands; n=1066 has the sharpest stamp and a top-5 sign score | passed (n=1066 chosen) |
| Deterministic re-extraction of n=1066 is pixel-identical to the frame from the scoring pass (Pillow `ImageChops.difference(...).getbbox() is None`) | passed |
| Picture bounds measured (max luma > 24): x=111..743. Crop x=107..746 removes only columns with max luma ≤ 5 | passed |
| PNG dimensions: original 854×480, export 1920×1080, proof 1280×720 | passed |
| Uniform scaling: 640×480 → 1440×1080 (both axes ×2.25; no stretch) | passed |
| Privacy scan of every file under the asset folder for e-mail addresses, the local account name and the user's address; third-party IA uploader e-mails in the raw metadata records were replaced with `[redacted uploader email]` | passed (no hits after redaction) |
| `python tools/validate_delivery.py --id HIST-09` | result recorded in delivery.json `tests` |

## Manual visual inspection

- **Full size, `source/original.png` (854×480):** the lit fascia sign "COMP USA" with "THE COMPUTER SUPERSTORE" is fully in frame and legible. The camcorder stamp "AUG. 24 1995" is legible across the storefront glass. Pillarbox columns are black. Analog noise and night exposure are inherent. Faces aren't identifiable (only dark silhouettes near the entrance).
- **Full size, `exports/editorial-frame.png` (1920×1080):** geometry is natural (no stretch). The sign sits in the upper-middle third, and the whole fascia, columns and entrance are inside the frame. The date stamp is legible and inside the action-safe area (about x 960–1475, y 930–990). Softness from the 2.25× SD upscale is visible and acceptable for archival B-roll. There's a faint 1–2 px light line at the bottom edge from the source video, not added. No added text, UI, or watermarks, and nothing was removed.
- **720p, `proofs/editorial-frame-720.png` (1280×720):** the sign and "AUG. 24 1995" stay readable, with no aliasing artifacts beyond the source noise.

## Content and editorial checks

- The CompUSA identity rests on the in-frame sign, not appearance. The 1995 date rests on the in-frame stamp, the archive record, and the launch displays in the same continuous clip (`evidence/claim-checks.json`).
- The Norwalk, CT location is uploader attestation only, so it's not asserted in any caption.
- The image doesn't show Visual Basic, so no caption should suggest a VB purchase.
- No `War/SCRIPT.md` change proposed.

## Remaining blockers

- **R14 (blocked):** the only license marking (IA CC0) was applied by a third-party uploader. The creator's YouTube original has the standard license. Release waits on a rights decision (RQ-1). See `evidence/rights.json`.
- **OPS-01 dependency:** only the shared version string `win95-workbench-1.0.0` and the 1920×1080 canvas are used. No shared fonts or styles are needed because nothing is overlaid.
- The 32 MB source MP4 isn't committed. It's identified by URL and SHA-256 so it can be re-fetched.
