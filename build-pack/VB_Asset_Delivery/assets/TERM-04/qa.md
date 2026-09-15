# TERM-04 — Production QA

**Production:** produced. **Release:** blocked — gates R05, R08 await a producer decision.

## Delivered
- `source/raw/02-double-war.png` plus build/start/end captures of the same run
- `exports/framed.png`, `framed-highlight.png`, `framed-start.png`, `framed-end.png`
- `source/stdout.txt`, `source/stderr.txt`, `source/Program.vb`; `evidence/search-log.json`
- Every file is listed with bytes and SHA-256 in `delivery.json`.

## Method
Actual local capture on this machine. Commands were typed into a real conhost.exe window running pwsh (WriteConsoleInput), window images were taken with PrintWindow, and text was read back from the console buffer. Raw PNGs are never edited; framing and outlines exist only in `exports/`. Commands, exit codes and timings come from PowerShell's own history (`evidence/prompt-log.jsonl`, `evidence/commands.log`).

## Checks actually performed
- **source hash:** passed
- **native command exit codes (PowerShell history + $LASTEXITCODE at the next prompt):** passed
- **double-war criteria in saved stdout:** passed
- **terminal display equals saved stdout:** passed
- **search bound respected:** passed
- **PNG dimensions (raw native, exports 1920×1080, proofs 1280×720):** passed
- **manual visual inspection:** passed
- **privacy scan of text outputs:** passed

## Manual visual inspection
- Full size: Viewed source/raw/01-build.png (1319×872) and exports/framed.png, framed-highlight.png, framed-start.png, framed-end.png (1920×1080). Round 245's six lines (Ace/Ace war, Queen/Queen second war, Ace of Diamonds beats 2 of Clubs, 18 cards) are legible, and after a padding fix the amber outline encloses exactly those lines without touching Round 244 or 246. Start shows the typed stdout-01 command, banner and deal; end shows Round 617 where Player 2 runs out mid-war, PLAYER 1 WINS THE WAR!, 617 rounds, 26 wars. No other windows, notifications, or personal data.
- 720p: Viewed proofs/framed-highlight-720.png after the re-render, and framed-720.png, framed-start-720.png, framed-end-720.png before it (the re-render changed only the outline padding; unoutlined frames are regenerated identically from the same raw captures). All lines and the outline remain clear.

## Reproduction
```
python work/war-harness/tools/capture_assets.py --id TERM-04
python work/war-harness/tools/finish_assets.py --id TERM-04 --stage render
python work/war-harness/tools/finish_assets.py --id TERM-04 --stage bundle
```
A capture refuses to overwrite existing raw files. A new run of the game is a new random game and must be delivered as a new capture, never relabelled as this one.

Toolchain: Windows-11-10.0.26200-SP0; .NET SDK 10.0.303; PowerShell 7.6.6; conhost 10.0.26100.9444; Python 3.14.0; Pillow 12.3.0; pywin32 312.

## Remaining gates and limits
- **R05:** The highlighted round has two ties, full 3-card burns from both players, and an 18-card award, so it does not depend on the insufficient-card ordering R05 describes. The same run's ending (framed-end.png) does go through that branch: 'Player 2 has no cards left for the war - Player 1 takes the pot.'. It is shown as captured; how to narrate it is the producer's decision. Awaiting producer decision.
- **R08:** The double war is from a real run (attempt 1 of a bounded search). The script's example double-war text is not reproduced as evidence. Awaiting producer decision.
- Stills only. A live screen recording (handoff H01) was not made.
- Structure validation (`tools/validate_delivery.py`) runs after bundling; results are in `review/capture-delivery-validation.json`.
- No independent reviewer is recorded; the capturing agent's checks are not a producer review.
