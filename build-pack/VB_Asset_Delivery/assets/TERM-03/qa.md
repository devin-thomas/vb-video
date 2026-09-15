# TERM-03 — Production QA

**Production:** produced. **Release:** blocked — gates R03 await a producer decision.

## Delivered
- `source/raw/viewport-*.png` — 12 overlapping editor captures
- `exports/framed.png` (lines 1–29) and `framed-02.png` … — 1:1 framed copies
- `exports/contact-sheet.png`, `evidence/viewports.json`, `source/Program.vb`
- Every file is listed with bytes and SHA-256 in `delivery.json`.

## Method
Actual local capture on this machine. Commands were typed into a real conhost.exe window running pwsh (WriteConsoleInput), window images were taken with PrintWindow, and text was read back from the console buffer. Raw PNGs are never edited; framing and outlines exist only in `exports/`. Commands, exit codes and timings come from PowerShell's own history (`evidence/prompt-log.jsonl`, `evidence/commands.log`).

## Checks actually performed
- **source hash:** passed
- **native command exit codes (PowerShell history + $LASTEXITCODE at the next prompt):** passed
- **every viewport's visible text equals the source lines:** passed
- **complete coverage, no missing lines:** passed
- **PNG dimensions (raw native, exports 1920×1080, proofs 1280×720):** passed
- **manual visual inspection:** passed
- **privacy scan of text outputs:** passed

## Manual visual inspection
- Full size: Viewed all 12 exports/framed*.png (1920×1080, raw 1423×872 at 1:1) and exports/contact-sheet.png. Each shows vim with line numbers, VB syntax colouring, no wrapped lines, and the ruler at bottom right; first/last line numbers match evidence/viewports.json. Viewport 01 also shows vim's file message ("Program.vb" [readonly][unix] 285L, 9234B). Comments use the console's dark-blue palette entry: legible, but lower contrast than code. No other windows, notifications, or personal data.
- 720p: Viewed proofs/framed-720.png and framed-12-720.png (1280×720): code and line numbers stay readable; dark-blue comments are the weakest element at this size. The other ten 720p proofs are the same scaling of viewports inspected at full size and were not opened individually.

## Reproduction
```
python work/war-harness/tools/capture_assets.py --id TERM-03
python work/war-harness/tools/finish_assets.py --id TERM-03 --stage render
python work/war-harness/tools/finish_assets.py --id TERM-03 --stage bundle
```
A capture refuses to overwrite existing raw files. A new run of the game is a new random game and must be delivered as a new capture, never relabelled as this one.

Toolchain: Windows-11-10.0.26200-SP0; .NET SDK 10.0.303; PowerShell 7.6.6; conhost 10.0.26100.9444; Python 3.14.0; Pillow 12.3.0; pywin32 312, vim VIM - Vi IMproved 9.1 (2024 Jan 02, compiled Jan 13 2026 10:32:17).

## Remaining gates and limits
- **R03:** The capture shows the VB.NET Program.vb (its own header calls it classic-inspired) in vim on Windows 11. No VB4 IDE, VB4 compile, or VB4 run is shown or implied. Awaiting producer decision.
- Stills only. A live screen recording (handoff H01) was not made.
- Structure validation (`tools/validate_delivery.py`) runs after bundling; results are in `review/capture-delivery-validation.json`.
- No independent reviewer is recorded; the capturing agent's checks are not a producer review.
