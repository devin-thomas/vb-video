# Integration log

**Source:** `Visual_Basic_Produced_Assets.zip` (41 MB, 2,499 files; kept locally, not committed)
**Producers:** ChatGPT — local production (session 1); Claude Code (sessions 2–5)

## Current status

Counted from `assets/*/*/state.json` after session 5:

| Status | Count | Description |
|--------|------:|-------------|
| **produced** | 86 | Rendered or captured deliverables with source, evidence and QA |
| **in_progress** | 1 | OPS-04 integration QA |
| **planned** | 47 | Not started |
| **blocked** | 0 | — |

*Produced* is not *release-approved*. Only the 8 session-3 captures have producer release approval; the other 78 produced assets await a producer decision, tracked in OPS-03. Every ticket and handoff is a [GitHub issue](https://github.com/devin-thomas/vb-video/issues); issue numbers are in `manifest.json` and `asset_index.csv`. What's left: [../review/REMAINING_TICKETS.md](../review/REMAINING_TICKETS.md).

## Session 1 — build pack import (2026-09-15)

The pack expanded the original 26 GitHub issues into 134 fine-grained tickets. Produced on import (71 assets plus OPS-01):

- **CARD-01, CARD-02** — Opening title card (Win95 MsgBox) and end card
- **CH-01 through CH-16** — All 16 chapter title cards
- **CODE-01 through CODE-25** — 25 exact Program.vb code excerpts with syntax highlighting
- **CMP-01 through CMP-08** — 8 C# vs VB comparison cards
- **DIA-01 through DIA-10** — 10 diagrams/animations (event-driven, War rules, card rank, ByRef/ByVal, array-as-queue, Fisher-Yates, deck building, War mechanic, pot growth, game flowchart)
- **FACT-01 through FACT-06** — All 6 factoid cards
- **MOCK-01, MOCK-02** — VB4 GUI mockup and 1996 download dialog
- **REF-03, REF-04** — VB MsgBox 3-liner and retro BASIC terminal
- **OPS-01** — Shared visual system (card deck SVG, atlas, export contract)

## Session 2 — Tier 1 SVGs (2026-09-15, corrected in session 4)

Commit `c9bf2e2` added one SVG each for DIA-11 to DIA-14, REF-01, REF-02 and XTRA-04, marked them produced and closed issues #11–#14, #23 and #26. The session-4 audit found:

- None of the seven has the ticket's required PNG export, `delivery.json`, evidence or `qa.md`; their state notes still read "Planning scaffold only". DIA-11 to DIA-14, REF-01 and REF-02 are now **in_progress**.
- The REF-01 and REF-02 SVGs were swapped. They were moved so REF-01 holds the MFC message map and REF-02 the Windows C Hello World.
- XTRA-04's SVG was a Java 1.0 AWT code card, not the FORTRAN versus BASIC example the ticket asks for. It now lives at `assets/slides/code-contrast-java-awt.svg` (the name issue #26 promised) and XTRA-04 is **planned**. No build-pack ticket covers the Java card.

## Session 3 — real .NET terminal and editor captures (2026-09-15)

The pack had blocked 8 tickets because its production machine had no .NET SDK. They were produced on Windows 11 with .NET SDK 10.0.303. Every capture is genuine: commands were typed into a real conhost/pwsh window, screenshots are unedited window images, and the console buffer was read back and compared line-for-line with the saved stdout or source file. Capture logs still show the `build-pack/` paths the work ran in.

| ID | Capture | Actual result | Gates (approved 2026-09-15) |
|---|---|---|---|
| OPS-02 | Isolated harness: SDK scaffold, byte-identical Program.vb, two derived Option nodes | Build: 0 warnings, 0 errors. Harness check run: Player 2 wins, 1001 rounds, 41 wars | R17 |
| TERM-01 | `dotnet --version`, `dotnet new console -lang VB` in an empty folder | 10.0.303; template and restore succeeded | R17 |
| TERM-02 | Primary full run | Player 2 wins, 2008 rounds, 69 wars | R06, R08 |
| TERM-03 | Program.vb in vim, 12 overlapping viewports + contact sheet | All 285 lines covered; every viewport's text verified | R03 |
| TERM-04 | Double-war highlight | Round 245: two wars, 18-card award. Found on run 1 of a 30-run bound; that run: Player 1 wins, 617 rounds, 26 wars | R05, R08 |
| TERM-05 | Independent run B | Player 2 wins, 1056 rounds, 10 wars | R06, R08 |
| TERM-06 | Independent run C + three-run results table | Player 2 wins, 150 rounds, 10 wars | R06, R08 |
| XTRA-06 | War.vbproj and Program.vb directives in vim, settings close-up | Both Option nodes present in the derived project file (diff logged) | R17 |

Producer decisions (2026-09-15):

- **R08, script numbers:** `War/SCRIPT.md` now quotes real capture output instead of the original samples (418 rounds/10 wars, 347/13). Section 11 follows TERM-04 from start to finish; the "run it a few more times" beat cites TERM-02, TERM-05 and TERM-06; the outro summary is TERM-02. The hash-locked `sources/SCRIPT.md` is unchanged, so `War/SCRIPT.md` is the revised script.
- **R17, Option settings:** the video description in `War/SCRIPT.md` has a footnote saying `OptionExplicit`/`OptionStrict` were added to War.vbproj by hand and are not scaffold defaults.
- **R05, running out of cards mid-war:** captures approved as shown. A new script section was requested as [issue #27](https://github.com/devin-thomas/vb-video/issues/27); commit `f32a343` added it to `War/SCRIPT.md` as Section 12, and the issue is still open for review.
- **R03, R06:** approved as captured.
- All three independent runs happened to be Player 2 wins; no run was repeated to get a different winner.
- These are stills. A live screen recording (handoff H01) was not made.

Tooling and rules: [../tools/war-harness/README.md](../tools/war-harness/README.md). Structure validation: [../review/capture-delivery-validation.json](../review/capture-delivery-validation.json).

## Session 4 — repository migration (2026-09-15)

The pack stopped living in `build-pack/VB_Asset_Delivery/` and became the repository layout described in [../README.md](../README.md). Every tracked move used `git mv`, so file history follows.

- **Assets:** `assets/<ID>/` → `assets/<family>/<ID>/`. The shared card system moved to `assets/shared/`.
- **Docs:** pack docs → `docs/`; tickets → `docs/tickets/`; handoffs → `docs/handoffs/`; schemas → `docs/schemas/`; the pack README is preserved as `docs/DELIVERY_README.md`, and this log was `BUILD_PACK_INTEGRATION.md`.
- **Tools:** validators and dispatcher → `tools/`; renderer → `tools/render/`; .NET harness and capture tooling → `tools/war-harness/`; fixtures → `tools/fixtures/`. `tools/build_indexes.py` replaces the pack's `make_gallery.py`, and `tools/github_issues.py` keeps issues in step with ticket state.
- **Other:** `sources/`, `review/` (including the contact sheet and preview reel), `AGENTS.md`, `START_HERE.html`, `manifest.json` and `asset_index.csv` moved to the root.
- **Records:** paths that must resolve (`../../../sources/…` in delivery and provenance records) and path mentions in instructions (qa.md, briefs, the export contract, tickets, docs) were updated. Every rewritten file's size and SHA-256 were refreshed in its `delivery.json`. Historical logs and captures were left as recorded.
- **Manifest:** each ticket gained `asset_dir` and `github_issue`, and its `ticket` and `owned_paths` point at the new locations.
- **Legacy names:** the 60 file names issues #1–#26 promised now exist as copies, plus the Java AWT card; see [../assets/LEGACY_NAMES.md](../assets/LEGACY_NAMES.md).
- **Issues:** every ticket (134, issues #28–#161) and handoff (7, issues #162–#168) became a GitHub issue, created by `tools/github_issues.py` and recorded in `manifest.json`. The 80 produced tickets are closed as a record; 54 tickets and all 7 handoffs are open. OPS-03 (#30) carries the checklist of 72 produced assets still awaiting a producer release decision. Each original issue (#1–#26) got a comment linking its per-ticket issues.

## Session 5 — the six SVG-only tickets, produced on Windows (2026-09-15)

DIA-11 to DIA-14, REF-01 and REF-02 are now **produced**; release stays **blocked** on their editorial gates. The session-2 SVGs were not reused. DIA-11's added prices, market positions and ratings its ticket forbids; DIA-12's added unverified specifics (VBRUN400.DLL, 68K/PPC, SIOUX); DIA-13's added nodes and dates the script doesn't have, and was not valid XML. All six were authored again in the render pipeline, then built, rendered, browser-checked and finished one ticket ID at a time.

| ID | Delivered | Open gates |
|---|---|---|
| DIA-11 | Five-tool table drafted from the narration; each cell's script line, quote and basis is in `src/cells.json`. No prices, shares, ratings or release years | R11, R15 |
| DIA-12 | The script's table word for word (`full-table`), plus `gui-row-focus` | R03, R09, R16 |
| DIA-13 | Ticket-copy nodes. The script's arrows sit in their own `draft-script-sequence` layer, drawn only as unverified; edges are in `src/edges.json` | R13 |
| DIA-14 | `early-history` (proportional, 1991–1998) and `great-divide` (schematic). Years are quoted in `src/milestones.json`; no feature callouts | R15, R12 |
| REF-01 | 16 s scroll through 48 lines of representative Visual C++ 4-style MFC, ending on the message map | R15 |
| REF-02 | 22 s scroll through representative Windows 3.0 C, hello.c (63 lines) and hello.def (10), ending on the message loop | R03, R15 |

- **Representative code:** written for this production and kept in `tools/fixtures/`. Neither sample was compiled: Visual Studio 2022 here has no MFC libraries, and there is no 16-bit toolchain. `hello.c` passed a C89 syntax check (`gcc -std=c89 -pedantic -Wall -fsyntax-only`) against a stand-in header written for the check; its one warning, WndProc assigned to the unprototyped `lpfnWndProc`, comes from that stand-in. The script said "about 80"; by producer decision (2026-09-15), `War/SCRIPT.md` now says 73 lines, in both the narration and the visual cue.
- **Review:** every export and 720p proof was viewed; notes are in `review/manual-review.json`. DIA-13's first render put two labels past x = 1800 and was fixed before review. Both MP4s decode cleanly with ffmpeg.
- **Tooling:** the render scripts now read and write UTF-8 with LF, since Python's Windows default (cp1252, CRLF) would change text and hashes. `render_assets.py` uses one worker on Windows, because MSYS2's Cairo crashed with three. `qa_browser.py` and `finish_delivery.py` take `--id` and merge into the review indexes, and a delivery finished that way records the live toolchain. The OPS routine no longer re-blocks produced captures. See [../tools/render/REBUILD.md](../tools/render/REBUILD.md).
- **Toolchain:** Windows 11, Python 3.14.0, CairoSVG 2.9.1 on MSYS2 Cairo 1.18.4, Pillow 12.3.0, Playwright 1.63.0 with Chromium 153, ffmpeg 6.0.
- **Legacy names:** the six legacy files now copy the new sources; REF-01 and REF-02 use the clean first viewport. See [../assets/LEGACY_NAMES.md](../assets/LEGACY_NAMES.md).

## Mapping: original GitHub issues → tickets

| GitHub Issue | Title | Tickets | Status |
|---|---|---|---|
| #1–#10 | Diagrams: event-driven … game flowchart | DIA-01 to DIA-10 | **produced** |
| #11–#14 | Diagrams: 1995 tools, Mac vs Windows, lineage, timeline | DIA-11 to DIA-14 | **produced** (session 5) |
| #15 | Slide: Title card | CARD-01 | **produced** |
| #16 | Slides: Chapter title cards (16) | CH-01 to CH-16 | **produced** |
| #17 | Slides: VB code blocks (8) | CODE-01 to CODE-25 | **produced** (expanded to 25) |
| #18 | Slides: C# vs VB comparisons (4) | CMP-01 to CMP-08 | **produced** (expanded to 8) |
| #19 | Slides: Factoid cards (6) | FACT-01 to FACT-06 | **produced** (different fact set) |
| #20 | Slide: End card | CARD-02 | **produced** |
| #21, #22 | Mockups: VB4 GUI, 1996 download | MOCK-01, MOCK-02 | **produced** |
| #23 | Code cards: Win32 / MFC | REF-02, REF-01 | **produced** (session 5; REF-02 is Windows 3.0 C, not Win32) |
| #24, #25 | Code cards: MsgBox, retro BASIC | REF-03, REF-04 | **produced** |
| #26 | Code card: Java AWT | none (card kept at its legacy name) | no delivery package |

## Repository

- Default branch is `main` (renamed from `master` on 2026-09-15; GitHub redirects old links).
- `.gitattributes` stores every asset folder and the hash-locked sources and harness byte-for-byte (`-text`). With `core.autocrlf=true`, Git would otherwise rewrite line endings on checkout and break the SHA-256 hashes recorded in `delivery.json` and `harness-manifest.json`.
