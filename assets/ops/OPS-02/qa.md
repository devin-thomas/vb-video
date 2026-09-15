# OPS-02 — Production QA

**Production:** produced. **Release:** approved; the producer's R17 decision is in `evidence/claim-checks.json`.

## Delivered
- `exports/report.md` — what was built and observed
- `exports/harness-manifest.json` — snapshot hashes, SDK version, exit codes
- `evidence/commands.log`, `evidence/harness-commands.json` — every command with exit code and timing
- `evidence/dotnet-info.stdout.txt`, `dotnet-new.*`, `dotnet-build.*`, `harness-run.*` — raw command output
- Harness snapshot itself: `tools/war-harness/` (owned by this ticket)

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
python tools/war-harness/tools/build_harness.py
python tools/war-harness/tools/finish_assets.py --id OPS-02 --stage bundle
```
`build_harness.py` refuses to overwrite an existing harness. Toolchain: Windows-11-10.0.26200-SP0; .NET SDK 10.0.303; Python 3.14.0.

## Gates and limits
- **R17** (approved 2026-09-15 — Approved. The video description in War/SCRIPT.md carries a footnote that the OptionExplicit and OptionStrict project settings were added by hand and are not part of the dotnet new scaffold.): The derived War.vbproj is generated with the installed SDK and every property change is logged.
- No independent media reviewer is recorded.
