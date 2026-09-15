# TERM-01 — Production QA

**Production:** produced. **Release:** blocked — gates R17 await a producer decision.

## Delivered
- `source/raw/01-dotnet-version.png`, `02-dotnet-new.png`, `03-scaffold-files.png` — raw window captures
- `exports/framed.png` — 03-scaffold-files framed at 1:1
- `source/scaffold-transcript.txt` — console buffer text; `evidence/scaffold/` — generated files
- Every file is listed with bytes and SHA-256 in `delivery.json`.

## Method
Actual local capture on this machine. Commands were typed into a real conhost.exe window running pwsh (WriteConsoleInput), window images were taken with PrintWindow, and text was read back from the console buffer. Raw PNGs are never edited; framing and outlines exist only in `exports/`. Commands, exit codes and timings come from PowerShell's own history (`evidence/prompt-log.jsonl`, `evidence/commands.log`).

## Checks actually performed
- **native command exit codes (PowerShell history + $LASTEXITCODE at the next prompt):** passed
- **scaffold files match the OPS-02 scaffold:** passed
- **transcript source:** passed
- **PNG dimensions (raw native, exports 1920×1080, proofs 1280×720):** passed
- **manual visual inspection:** passed
- **privacy scan of text outputs:** passed

## Manual visual inspection
- Full size: Viewed source/raw/01-dotnet-version.png, 02-dotnet-new.png, 03-scaffold-files.png (1319×872) and exports/framed.png (1920×1080). Text is sharp; `dotnet --version` → 10.0.303, the empty listing, template and restore success, and the Program.vb/War.vbproj listing are legible and unclipped; the window sits inside the safe area. Only the repository work path is visible; no notifications, other windows, or personal data.
- 720p: Viewed proofs/framed-720.png (1280×720): every line stays readable, including the directory path.

## Reproduction
```
python work/war-harness/tools/capture_assets.py --id TERM-01
python work/war-harness/tools/finish_assets.py --id TERM-01 --stage render
python work/war-harness/tools/finish_assets.py --id TERM-01 --stage bundle
```
A capture refuses to overwrite existing raw files. A new run of the game is a new random game and must be delivered as a new capture, never relabelled as this one.

Toolchain: Windows-11-10.0.26200-SP0; .NET SDK 10.0.303; PowerShell 7.6.6; conhost 10.0.26100.9444; Python 3.14.0; Pillow 12.3.0; pywin32 312.

## Remaining gates and limits
- **R17:** Handled as R17 requires: the project shown is a fresh `dotnet new console -lang VB` scaffold made with the installed SDK 10.0.303, before any property change, and it is not presented as an uploaded original. Awaiting a producer decision; not self-approved.
- Stills only. A live screen recording (handoff H01) was not made.
- Structure validation (`tools/validate_delivery.py`) runs after bundling; results are in `review/capture-delivery-validation.json`.
- No independent reviewer is recorded; the capturing agent's checks are not a producer review.
