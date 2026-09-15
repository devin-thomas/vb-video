# War harness (OPS-02)

A derived, isolated .NET project for running the hash-locked `sources/Program.vb` and capturing real terminal evidence. It is **not** an uploaded original: only `ASSET_PLAN.md`, `SCRIPT.md`, and `Program.vb` were supplied (register R17).

## Contents

| Path | What it is |
|---|---|
| `scaffold/War.vbproj`, `scaffold/Program.vb` | Untouched output of `dotnet new console -lang VB` (SDK 10.0.303) |
| `War/Program.vb` | Byte-identical copy of `sources/Program.vb` |
| `War/War.vbproj` | Scaffold plus two derived nodes: `<OptionExplicit>On</OptionExplicit>`, `<OptionStrict>On</OptionStrict>` |
| `project-diff.txt` | Unified diff of that project-file change |
| `harness-manifest.json` | Hashes of every snapshot file, SDK version, build/run exit codes |
| `tools/build_harness.py` | Created this harness (refuses to overwrite it) |
| `tools/console_capture.py` | Drives a real conhost/pwsh window: types commands, reads the buffer, saves window PNGs |
| `tools/capture_assets.py` | Per-ticket capture scripts for TERM-01…06 and XTRA-06 |
| `tools/capture_common.py` | Hash-verified harness copies, framing, 720p proofs, delivery bundles |
| `tools/finish_assets.py` | Framed exports, proofs, QA, and delivery metadata after raw-shot review |

`bin/` and `obj/` are build output and are ignored.

## Capture rules

1. Never build or run inside this folder again. `capture_common.prepare_workdir(ID)` copies `War/War.vbproj` and `War/Program.vb` into `assets/<family>/<ID>/work/War/`, checks both hashes against `harness-manifest.json`, and refuses to reuse an existing copy.
2. Run one capture at a time: `python tools/war-harness/tools/capture_assets.py --id TERM-02`. The window appears on the desktop; PrintWindow captures it even when covered, but do not minimize it.
3. Raw PNGs in `source/raw/` are never edited. Framing and highlight outlines are applied only to derived copies in `exports/`.
4. Program output is never altered, and no run is repeated to get a preferred result, except TERM-04's bounded double-war search (at most 30 runs or 200 MB of logs).
