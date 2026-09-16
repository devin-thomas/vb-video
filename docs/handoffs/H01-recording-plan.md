# H01 — Screen recording plan

Prepared 2026-09-15. The TERM captures are stills of real runs; these recordings replace or supplement them with motion. Record at 1920×1080, 30 fps, cursor visible, no system audio. Use a fresh window; hide notifications and other windows first.

## Set-up (once)

```
cd C:\dev\youtube\vb-video-checkout-2
python tools/war-harness/tools/capture_assets.py --help
```
The harness copies `tools/war-harness/War/` (byte-identical `Program.vb`, derived `War.vbproj`) into a work folder; never build inside `tools/war-harness/` itself. For a recording you can simply copy `tools/war-harness/War/` to a scratch folder and run `dotnet run` there.

## Takes

| Take | What | Command | Serves |
|---|---|---|---|
| R1 | Project creation | `dotnet new console -lang VB` in an empty folder, then `dotnet --version` | Section 4 (TERM-01 beat) |
| R2 | Full game, run 1 | `dotnet run` in the copied War folder; let it scroll to the summary | Sections 1 (cold open, fast) and 11 |
| R3 | Two more full runs | `dotnet run` twice more, different outcomes | Section 11, 'run it a few more times' |
| R4 | War-heavy moment | keep running until a `** WAR! **` chain appears; TERM-04 found a double war on run 1 of 30 | Sections 1 and 10 |
| R5 | Code scroll-through | `vim Program.vb` (or any editor at a readable size), scroll top to bottom slowly | Section 6 onward, whenever code is discussed; TERM-03 has the 12 viewports as stills |
| R6 | Project file | open `War.vbproj`, show `OptionExplicit` and `OptionStrict` | Section 4 (XTRA-06 beat) |

## Rules that still apply

- Output is never edited or re-run to get a preferred result (R4 may be searched, as TERM-04 did, but say so in the take log).
- Save raw files under `assets/handoffs/H01/` with a take log (command, time, outcome). A replay of a saved log must be labelled replay.
- If you skip this handoff entirely, the edit uses the TERM stills with pan and scan; that is allowed.
