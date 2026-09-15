# OPS-02 — Isolated .NET harness report

**Production:** produced. **Release:** blocked (R17 awaits a producer decision).

## Environment
- Windows-11-10.0.26200-SP0, .NET SDK 10.0.303 (`dotnet --info` in `evidence/dotnet-info.stdout.txt`). Nothing was installed.

## What was built
1. `dotnet new console -lang VB` in the empty `work/war-harness/War/` → exit 0. Untouched output kept in `work/war-harness/scaffold/`.
2. `sources/Program.vb` copied byte-for-byte to `War/Program.vb` (sha256 `8069f62bfb24bbd792cda04a6eefa9745f9d9ffb8d879e523b95454cafb06ce7`, match: True).
3. Derived project change, the only edit (`work/war-harness/project-diff.txt`): added `<OptionExplicit>On</OptionExplicit>` and `<OptionStrict>On</OptionStrict>` after `<TargetFramework>net10.0</TargetFramework>`, which is unchanged. This derived file is not an uploaded original (R17).
4. `dotnet build` → exit 0, 0 warnings, 0 errors.
5. `dotnet run --no-build`, once → exit 0; stderr empty; stdout kept in `evidence/harness-run.stdout.txt`. Actual result: PLAYER 2 WINS THE WAR! after 1001 rounds with 41 wars. This is a harness check only; it is not a capture asset.

No code bug was fixed; Program.vb is unchanged.

## Snapshot and copies
`exports/harness-manifest.json` lists every snapshot file with its hash. Capture workers copy `War/War.vbproj` and `War/Program.vb` into `assets/<ID>/work/War/`, verify both hashes, and build there, so no two captures share `bin/` or `obj/`. Hash-verified copies were used by: TERM-02, TERM-05, TERM-06, TERM-04, TERM-03, XTRA-06. TERM-01 intentionally scaffolds its own empty directory instead.

## Capture tooling
`work/war-harness/tools/` holds the real-terminal driver (conhost + pwsh, WriteConsoleInput, PrintWindow, buffer read-back), per-ticket capture scripts, and the finisher. See `work/war-harness/README.md`.
