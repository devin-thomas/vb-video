# TERM-06 — Production QA

**Production:** produced. **Release:** blocked — gates R06, R08 await a producer decision.

## Delivered
- `source/raw/` — 4 raw window captures: build, run start, first war, run end
- `exports/framed.png` (end), `framed-start.png`, `framed-first-war.png` — 1:1 framed copies
- `source/stdout.txt`, `source/stderr.txt`, `source/Program.vb` — the run's own output and exact source
- `evidence/results-table.md`
- `evidence/results-table.json`
- Every file is listed with bytes and SHA-256 in `delivery.json`.

## Method
Actual local capture on this machine. Commands were typed into a real conhost.exe window running pwsh (WriteConsoleInput), window images were taken with PrintWindow, and text was read back from the console buffer. Raw PNGs are never edited; framing and outlines exist only in `exports/`. Commands, exit codes and timings come from PowerShell's own history (`evidence/prompt-log.jsonl`, `evidence/commands.log`).

## Checks actually performed
- **source hash:** passed
- **native command exit codes (PowerShell history + $LASTEXITCODE at the next prompt):** passed
- **terminal display equals saved stdout:** passed
- **stdout/stderr retained:** passed
- **summary totals consistent:** passed
- **three independent runs:** passed
- **PNG dimensions (raw native, exports 1920×1080, proofs 1280×720):** passed
- **manual visual inspection:** passed
- **privacy scan of text outputs:** passed

## Manual visual inspection
- Full size: Viewed source/raw/01-build.png (1319×872) and exports/framed-start.png, framed-first-war.png, framed.png (1920×1080, raw at 1:1). The typed command, banner, 26/26 deal, the Round 18 war with its 10-card award, and the final block (Round 150, PLAYER 2 WINS THE WAR!, 150 rounds, 10 wars) are sharp, unclipped and inside the safe area. The title bar is in Windows' inactive state because focus had moved during capture. No other windows, notifications, or personal data.
- 720p: Viewed proofs/framed-start-720.png, framed-first-war-720.png, framed-720.png (1280×720): every line, including the summary totals, remains readable.

## Reproduction
```
python work/war-harness/tools/capture_assets.py --id TERM-06
python work/war-harness/tools/finish_assets.py --id TERM-06 --stage render
python work/war-harness/tools/finish_assets.py --id TERM-06 --stage bundle
```
A capture refuses to overwrite existing raw files. A new run of the game is a new random game and must be delivered as a new capture, never relabelled as this one.

Toolchain: Windows-11-10.0.26200-SP0; .NET SDK 10.0.303; PowerShell 7.6.6; conhost 10.0.26100.9444; Python 3.14.0; Pillow 12.3.0; pywin32 312.

## Remaining gates and limits
- **R06:** This run ended with a winner after 150 rounds, so the round-cap 'deck cycle detected' line does not appear. The counter/wording caveat still applies to any narration about draws. Awaiting producer decision.
- **R08:** Real totals from this run (PLAYER 2 WINS THE WAR!; 150 rounds; 10 wars) replace, not confirm, the script's sample results (418 rounds/10 wars, 347 rounds/13 wars). Narration quoting sample numbers still needs a producer decision.
- Stills only. A live screen recording (handoff H01) was not made.
- Structure validation (`tools/validate_delivery.py`) runs after bundling; results are in `review/capture-delivery-validation.json`.
- No independent reviewer is recorded; the capturing agent's checks are not a producer review.
