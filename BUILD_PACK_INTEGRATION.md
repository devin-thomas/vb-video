# Build Pack Integration Log

**Source:** `Visual_Basic_Produced_Assets.zip` (41 MB, 2499 files)
**Producers:** ChatGPT — local production (session 1); Claude Code (sessions 2–3)
**Integrator:** Claude

## Current status

Counted from `build-pack/VB_Asset_Delivery/assets/*/state.json` on 2026-09-15, after session 3:

| Status | Count | Description |
|--------|------:|-------------|
| **produced** | 87 | Rendered or captured deliverables with source, evidence, QA |
| **planned** | 46 | Tickets written but not yet produced |
| **in_progress** | 1 | OPS-04 (integration QA) |
| **blocked** | 0 | — |

*Produced* is not *release-approved*. Assets with editorial gates keep `release_status: blocked` until a producer records each decision in the asset's `evidence/claim-checks.json`. See `build-pack/VB_Asset_Delivery/review/REMAINING_TICKETS.md` for everything still planned.

## Session 1 — build pack import (2026-09-15)

The pack expanded our original 26 GitHub issues into 134 fine-grained tickets. Produced on import:

- **CARD-01, CARD-02** — Opening title card (Win95 MsgBox) and end card
- **CH-01 through CH-16** — All 16 chapter title cards
- **CODE-01 through CODE-25** — 25 exact Program.vb code excerpts with syntax highlighting
- **CMP-01 through CMP-08** — 8 C# vs VB comparison cards (expanded from our original 4)
- **DIA-01 through DIA-10** — 10 diagrams/animations (event-driven, War rules, card rank, ByRef/ByVal, array-as-queue, Fisher-Yates, deck building, War mechanic, pot growth, game flowchart)
- **FACT-01 through FACT-06** — All 6 factoid cards
- **MOCK-01, MOCK-02** — VB4 GUI mockup and 1996 download dialog
- **REF-03, REF-04** — VB MsgBox 3-liner and retro BASIC terminal
- **OPS-01** — Shared visual system (card deck SVG, atlas, export contract)

## Session 2 — remaining Tier 1 assets (2026-09-15)

- **DIA-11 through DIA-14** — 1995 tools comparison, Mac vs Windows table, VB influence lineage, VB timeline
- **REF-01, REF-02** — MFC message-map snippet, Win32 Hello World
- **XTRA-04** — FORTRAN vs BASIC introductory example

## Session 3 — real .NET terminal and editor captures (2026-09-15)

The pack had blocked 8 tickets because its production machine had no .NET SDK. They are now produced on Windows 11 with .NET SDK 10.0.303. Every capture is genuine: commands were typed into a real conhost/pwsh window, screenshots are unedited window images, and the console buffer was read back and compared line-for-line with the saved stdout or source file.

| ID | Capture | Actual result | Release gates |
|---|---|---|---|
| OPS-02 | Isolated harness: SDK scaffold, byte-identical Program.vb, two derived Option nodes | Build: 0 warnings, 0 errors. Harness check run: Player 2 wins, 1001 rounds, 41 wars | R17 |
| TERM-01 | `dotnet --version`, `dotnet new console -lang VB` in an empty folder | 10.0.303; template and restore succeeded | R17 |
| TERM-02 | Primary full run | Player 2 wins, 2008 rounds, 69 wars | R06, R08 |
| TERM-03 | Program.vb in vim, 12 overlapping viewports + contact sheet | All 285 lines covered; every viewport's text verified | R03 |
| TERM-04 | Double-war highlight | Round 245: two wars, 18-card award. Found on run 1 of a 30-run bound; that run: Player 1 wins, 617 rounds, 26 wars | R05, R08 |
| TERM-05 | Independent run B | Player 2 wins, 1056 rounds, 10 wars | R06, R08 |
| TERM-06 | Independent run C + three-run results table | Player 2 wins, 150 rounds, 10 wars | R06, R08 |
| XTRA-06 | War.vbproj and Program.vb directives in vim, settings close-up | Both Option nodes present in the derived project file (diff logged) | R17 |

Notes for the producer:

- None of the script's sample results (418 rounds/10 wars, 347 rounds/13 wars) came from this code; narration that quotes them needs a decision (R08).
- TERM-02 and TERM-04 both end through the "has no cards left for the war" branch, which is what R05 asks about.
- The SDK scaffold has no `OptionExplicit`/`OptionStrict` nodes. They exist only in the derived harness project (R17).
- All three independent runs happened to be Player 2 wins; the tickets treat a different winner as a preference, and no run was repeated to get one.
- These are stills. A live screen recording (handoff H01) was not made.

Tooling and rules: `build-pack/VB_Asset_Delivery/work/war-harness/README.md`. Structure validation: `build-pack/VB_Asset_Delivery/review/capture-delivery-validation.json`.

## Mapping: GitHub issues → Build pack IDs

Our original 26 GitHub issues were coarser-grained. The build pack split many of them into individual asset tickets:

| GitHub Issue | Title | Build Pack IDs | Status |
|---|---|---|---|
| #1 | Diagram: Event-driven programming | DIA-01 | **produced** |
| #2 | Diagram: War game rules animation | DIA-02 | **produced** |
| #3 | Diagram: Card rank mapping chart | DIA-03 | **produced** |
| #4 | Diagram: ByRef vs ByVal | DIA-04 | **produced** |
| #5 | Diagram: Array-as-queue animation | DIA-05 | **produced** |
| #6 | Diagram: Fisher-Yates shuffle animation | DIA-06 | **produced** |
| #7 | Diagram: Deck building nested-loop animation | DIA-07 | **produced** |
| #8 | Diagram: War mechanic step-by-step | DIA-08 | **produced** |
| #9 | Diagram: Pot growth diagram | DIA-09 | **produced** |
| #10 | Diagram: Game flowchart | DIA-10 | **produced** |
| #11 | Diagram: 1995 tools comparison chart | DIA-11 | **produced** |
| #12 | Diagram: Mac vs Windows comparison table | DIA-12 | **produced** |
| #13 | Diagram: VB influence lineage | DIA-13 | **produced** |
| #14 | Diagram: VB version timeline | DIA-14 | **produced** |
| #15 | Slide: Title card (Win95 message box) | CARD-01 | **produced** |
| #16 | Slides: Chapter title cards (16) | CH-01 through CH-16 | **produced** (all 16) |
| #17 | Slides: VB code blocks (8) | CODE-01 through CODE-25 | **produced** (expanded to 25) |
| #18 | Slides: C# vs VB comparisons (4) | CMP-01 through CMP-08 | **produced** (expanded to 8) |
| #19 | Slides: Did you know factoid cards (6) | FACT-01 through FACT-06 | **produced** |
| #20 | Slide: End card with subscribe CTA | CARD-02 | **produced** |
| #21 | Mockup: VB4 GUI War game | MOCK-01 | **produced** |
| #22 | Mockup: 1996 download progress bar | MOCK-02 | **produced** |
| #23 | Code card: Intimidating Win32/MFC C++ (2) | REF-01, REF-02 | **produced** |
| #24 | Code card: VB MsgBox 3-liner | REF-03 | **produced** |
| #25 | Code card: Retro BASIC terminal | REF-04 | **produced** |
| #26 | Code card: Java AWT snippet | XTRA-04 | **produced** |

### Build pack extras not in our original tickets

- **XTRA-01 through XTRA-20** — Supplementary visuals drawn from the script (XTRA-04 and XTRA-06 are produced)
- **HIST-01 through HIST-21** — Individual tickets for each historical image to source
- **BROLL-01 through BROLL-06** — Stock footage scouting tickets
- **TERM-01 through TERM-06** — Terminal and editor captures (produced in session 3)
- **OPS-01 through OPS-04** — Coordination/infrastructure tickets

## Provenance

Our original specs are preserved in the GitHub issue bodies (issues #1-#26 on devin-thomas/vb-video). The build pack's own ticket definitions live in `build-pack/VB_Asset_Delivery/tickets/`. Where the build pack expanded or refined a spec, the build pack version is authoritative for the produced deliverables; our GitHub issues remain as the original intent record.

## Repository

- Default branch is `main` (renamed from `master` on 2026-09-15; GitHub redirects old links).
- `.gitattributes` stores capture evidence byte-for-byte (`-text`). With `core.autocrlf=true`, Git would otherwise rewrite line endings and break the SHA-256 hashes recorded in `delivery.json` and `harness-manifest.json`.

## File layout

```
vb-video/
├── War/                          # Source code (our work)
│   ├── Program.vb
│   ├── War.vbproj
│   ├── SCRIPT.md
│   └── ASSET_PLAN.md
├── build-pack/                   # Authoritative produced assets
│   └── VB_Asset_Delivery/
│       ├── assets/               # 134 asset directories
│       ├── tickets/              # Build pack ticket definitions
│       ├── shared/               # Visual system, rebuild tools
│       ├── work/war-harness/     # .NET harness + real-terminal capture tooling
│       ├── review/               # QA reports
│       ├── docs/                 # Documentation
│       ├── CONTACT_SHEET.jpg     # Visual overview (session 1 assets)
│       ├── PREVIEW_REEL.mp4      # Silent preview (session 1 assets)
│       ├── START_HERE.html       # Browse gallery (session 1 assets; open locally)
│       ├── asset_index.csv       # Planning index
│       └── README.md
├── BUILD_PACK_INTEGRATION.md     # This file
├── .gitattributes
└── .gitignore
```
