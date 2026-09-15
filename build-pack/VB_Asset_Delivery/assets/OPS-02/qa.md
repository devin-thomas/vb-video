# OPS-02 — Production QA

**Production:** produced. **Release:** blocked — R17 awaits a producer decision.

## Delivered
- `exports/report.md` — what was built and observed
- `exports/harness-manifest.json` — snapshot hashes, SDK version, exit codes
- `evidence/commands.log`, `evidence/harness-commands.json` — every command with exit code and timing
- `evidence/dotnet-info.stdout.txt`, `dotnet-new.*`, `dotnet-build.*`, `harness-run.*` — raw command output
- Harness snapshot itself: `work/war-harness/` (owned by this ticket)

## Checks actually performed
- **source hash unchanged:** passed
- **build result recorded:** passed
- **single isolated run recorded:** passed
- **independent worker copies:** passed
- **no .vbproj presented as an uploaded original:** passed
- **manual visual inspection:** not applicable
- **privacy scan of text outputs:** passed

## Reproduction
```
python work/war-harness/tools/build_harness.py
python work/war-harness/tools/finish_assets.py --id OPS-02 --stage bundle
```
`build_harness.py` refuses to overwrite an existing harness. Toolchain: Windows-11-10.0.26200-SP0; .NET SDK 10.0.303; Python 3.14.0.

## Remaining gates and limits
- **R17:** The derived War.vbproj is generated with the installed SDK and every property change is logged; a producer still has to accept this handling.
- No independent reviewer is recorded.
