# XTRA-06 — Production QA

**Production:** produced. **Release:** approved — producer decisions for R17 are in `evidence/claim-checks.json`.

## Delivered
- `source/raw/01-war-vbproj.png`, `02-program-vb-directives.png` — raw vim captures
- `exports/framed.png` (project-file), `settings-focus.png`, `framed-directives.png`
- `source/War.vbproj`, `evidence/project-diff.txt`, `evidence/highlight-targets.json`
- Every file is listed with bytes and SHA-256 in `delivery.json`.

## Method
Actual local capture on this machine. Commands were typed into a real conhost.exe window running pwsh (WriteConsoleInput), window images were taken with PrintWindow, and text was read back from the console buffer. Raw PNGs are never edited; framing and outlines exist only in `exports/`. Commands, exit codes and timings come from PowerShell's own history (`evidence/prompt-log.jsonl`, `evidence/commands.log`).

## Checks actually performed
- **native command exit codes (PowerShell history + $LASTEXITCODE at the next prompt):** passed
- **pictured project file equals the harness file:** passed
- **highlighted nodes exist in the file:** passed
- **visible editor text equals the files:** passed
- **TargetFramework preserved:** passed
- **PNG dimensions (raw native, exports 1920×1080, proofs 1280×720):** passed
- **manual visual inspection:** passed
- **privacy scan of text outputs:** passed

## Manual visual inspection
- Full size: Viewed exports/framed.png and framed-directives.png (1920×1080, raw 1319×592 at 1:1) and exports/settings-focus.png (2× nearest-neighbour crop of the console client area). vim shows War.vbproj lines 1–11 with XML colouring (TargetFramework net10.0 visible) and Program.vb lines 1–19. One amber outline encloses exactly lines 7–8 in each highlighted export without covering adjacent lines. Earlier renders had two overlapping outlines and a title-bar sliver in the close-up; both were fixed and re-checked before bundling. No other windows, notifications, or personal data.
- 720p: Viewed proofs/framed-720.png, settings-focus-720.png, framed-directives-720.png (1280×720): nodes, directives and outline stay readable.

## Reproduction
```
python tools/war-harness/tools/capture_assets.py --id XTRA-06
python tools/war-harness/tools/finish_assets.py --id XTRA-06 --stage render
python tools/war-harness/tools/finish_assets.py --id XTRA-06 --stage bundle
```
A capture refuses to overwrite existing raw files. A new run of the game is a new random game and must be delivered as a new capture, never relabelled as this one.

Toolchain: Windows-11-10.0.26200-SP0; .NET SDK 10.0.303; PowerShell 7.6.6; conhost 10.0.26100.9444; Python 3.14.0; Pillow 12.3.0; pywin32 312, vim VIM - Vi IMproved 9.1 (2024 Jan 02, compiled Jan 13 2026 10:32:17).

## Gates and limits
- **R17** (approved 2026-09-15 — Approved. The video description in War/SCRIPT.md carries a footnote that the OptionExplicit and OptionStrict project settings were added by hand and are not part of the dotnet new scaffold.): The pictured War.vbproj is the OPS-02 derived harness file: the SDK 10.0.303 scaffold plus two added nodes (evidence/project-diff.txt). It is not an uploaded original or a scaffold default.
- Stills only. A live screen recording (handoff H01) was not made.
- Structure validation (`tools/validate_delivery.py`) runs after bundling; results are in `review/capture-delivery-validation.json`.
- Production stays `produced`, not `reviewed`: release approval is the producer's, but no file-by-file media review by anyone other than the capturing agent is recorded.
