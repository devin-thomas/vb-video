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

## Session 6 — new producer checkout and department merges (2026-09-15)

The producer moved to a fresh checkout at `C:\dev\youtube\vb-video-checkout-2` (the checkout at `C:\dev\experiments\vb` is retired) and now runs on Claude Fable 5.1, upgraded from Claude Opus 4.6. Current producer address: **vb-video-checkout-2-38 [20c133]**. Departments confirm it with `ListAgents` rather than trusting a role document.

- **Shallow clone.** The new checkout had been cloned with `--depth 1`, so `main` was a single parentless commit and every ticket branch reported 124 commits ahead with no merge base. `git fetch --unshallow origin` restored the history; nothing was rewritten.
- **Lost reports.** Eight finished department branches were never merged because their completion reports went to producer addresses that had stopped resolving. They were found from `git branch -r`, validated (`tools/validate_delivery.py` ok for all eight; `tools/validate_pack.py` no errors), viewed at 720p, and merged with no conflicts:

| Ticket | Branch | Tip | Merge |
|---|---|---|---|
| XTRA-05 | `ticket/XTRA-05-rev` | `f05ecf7` | `dfd63a2` |
| HIST-12 | `ticket/HIST-12-resume` | `a9b6f81` | `18d5382` |
| BROLL-01 | `ticket/BROLL-01-media` | `a74461e` | `dbbe998` |
| BROLL-02 | `ticket/BROLL-02-media` | `41fcd89` | `f623ef1` |
| BROLL-03 | `ticket/BROLL-03-media` | `25fc106` | `8ec7229` |
| BROLL-04 | `ticket/BROLL-04-media` | `05d12b2` | `6eff35f` |
| BROLL-05 | `ticket/BROLL-05-media` | `37efa0a` | `94f6bfc` |
| BROLL-06 | `ticket/BROLL-06-media` | `6861e4f` | `faccfae` |

  `ticket/HIST-12` (`94f4073`) is an ancestor of `ticket/HIST-12-resume` and came in with it.
- **Indexes and issues.** `tools/github_issues.py` closed #125 (HIST-12) and #135–#140 (BROLL-01 to BROLL-06) as produced and refreshed bodies; `tools/build_indexes.py` rebuilt the gallery, `asset_index.csv`, `review/REMAINING_TICKETS.md` and `review/summary.json`.
- **Review ledger.** `review/editorial-review.json` now exists as the single source for the OPS-04 deck, seeded with the 37 review questions (33 open) recorded by these eight tickets. Every one still carries `release_status: blocked` on R14; acquisition is not clearance.
- **Tooling.** `tools/github_issues.py` sniffed the manifest layout from raw text and, on a `core.autocrlf=true` checkout where `manifest.json` carries CRLF, wrote the whole 12,067-line file back as one line. It now normalises line endings before sniffing; the collapsed file was restored from `HEAD` (no data changed).
- **Role documents.** `docs/roles/PRODUCER.md` names the new checkout, the model, and three gotchas (shallow clone, branch suffixes, lost reports). The four department documents that still hardcoded `vb-05 [7bc7f1]` now tell managers to confirm the producer via `ListAgents` and this log. Historical evidence files under `assets/` that mention `C:\dev\experiments\vb` are byte-exact records of where the work ran and were left alone.

## Session 7 — first release decisions and the Writing Lead round (2026-09-15)

Devin ruled on the review ledger in chat with the producer, ahead of the OPS-04 deck.

- **R14, all 33 questions from the session-6 batch:** keep every asset; rights risk accepted as documented, no further clearance pursued. Recorded per question in `review/editorial-review.json` and as gate decisions in each ticket's `evidence/claim-checks.json`.
- **Release approved** (state, delivery and gate records; validator ok): HIST-12, BROLL-01, BROLL-02, BROLL-05, XTRA-05. Release now stands at 13 approved.
- **Still blocked pending Devin's choice:** BROLL-03, BROLL-04, BROLL-06, the three clips that do not match their brief. Their options (keep the labeled fallback, an alternative free source, an archive candidate, or an H02 outside request) are laid out with frames on the "B-roll Options" page at https://claude.ai/artifact/Si3a9xuQtatkKpkmuLAXtC.
- **Writing Lead round** (branch `writing/2026-09-15-r03`, commit `542f37e`, merged): `War/SCRIPT.md:135` no longer says the code window was "behind all of it" (the accepted VB4 capture shows it in front); `:151` says "today" instead of "in 2024"; the "Form Designer" label at `:133` is kept, so XTRA-05 needs no rebuild. Credit placement for XTRA-05 (RQ4) is a producer decision: end credits, nothing burned in.
- **Manifest:** BROLL-01 to BROLL-06 reclassed from kind `scout` to `archive`. Each ticket permitted ungated acquisition and now holds a verified original with provenance; `validate_delivery.py` refuses to approve a `scout` row.
- **Process:** the Writing Lead session ran inside the producer's checkout and its `git switch` moved the producer's working tree. No damage (the commit touched only the script), but `docs/roles/WRITING_LEAD.md` now requires a worktree.
- **B-roll choices (later the same evening):** Devin approved all three recommendations from the options page. BROLL-03 keeps the labeled recreation; BROLL-04 uses the 6.5 s cut 02:16.0 to 02:22.5, pillarboxed and muted; BROLL-06 uses the cutaway alone with narration carrying the boot. All three release-approved; release now stands at 16 approved.
- **Open in the ledger:** only HIST-12 RQ-2, an information item about presenting the 444×282 Delphi GIF at an exact 3× upscale on a matte rather than stretched.

## Session 8 — delegated release review, OPS-03 and OPS-04 (2026-09-15)

Devin stopped the deck-based review after seeing its size: the producer exists so that Devin does not review a hundred items, rights are settled after six rounds, and the producer should judge the rest against the words. So:

- **Rights.** Every R14 gate now records Devin's standing ruling (keep as documented). No rights question goes back to Devin.
- **Everything else.** The producer checked each of the 115 remaining produced assets against `War/SCRIPT.md` and `Program.vb` (code cards are also validator-checked as literal excerpts) and recorded a per-gate reason in each `evidence/claim-checks.json`; review questions are resolved with the decision. Script fixes the workers had proposed were confirmed already applied (properties bar, NeXT 1993, VB.NET 2000/2002, bundled Windows games, QuickBASIC for Mac, runtime size, petition 2005, Java 1996). Producer calls: CH-10 keeps the author's "Recursion" title (narration at :460 says it is a loop); the "more readable" line, the "accountants and teachers" colour, and the "this is fine" meme drop stand as decided; XTRA-14 credits stay burned in; HIST-12 stays at its 3× integer upscale.
- **One fix.** XTRA-15's frame carried two burned-in provenance sentences; the producer stripped them to the RECONSTRUCTION label, rebuilt and re-rendered (`python tools/render/render_assets.py --id XTRA-15` with `C:\Python314\python.exe`; prepending the MSYS2 bin to PATH picks up the wrong python).
- **OPS-03 and OPS-04 produced** by `tools/producer/build_ops.py`: the decision ledger, the coverage report, `editor-inventory.csv` (134 rows in script order, 130 media assets cleared), `exceptions.md` (labels and cuts that travel with specific assets, plus the credits list). Both validated.
- **State.** 134/134 produced, 134/134 release-approved, `validate_pack` and every `validate_delivery` ok. GitHub issues #30 and #161 closed. Production is complete; what remains is the human work in `docs/handoffs/`.

## Session 9 — overnight finish: narration QA, assembly, renders (2026-09-16)

Run unattended by the Video Executive Producer (`docs/roles/VIDEO_EXECUTIVE_PRODUCER.md`), session `vb-video-checkout-2-b3 [4f305e]`, after the producer's handoff at 23:30. Devin was asleep; every call below is the producer's.

- **Two holders of the brief.** Devin started this session as the Video Executive Producer; the producer separately launched a background job with the same brief (`abd4684b`, "Video Executive Producer: overnight finish"). The two sessions agreed by message that the background job would own the chain, then the producer handed the chain to this session and stood down. The background job went dormant behind a wait script that greps `synth.log` for a bare `done` line, which never matches because every log line carries a time prefix; its wait script ran its full two hours and exited at 01:27, and the job had not woken by 03:20. Stopping another session's job was outside this session's permissions, so `finish.sh` gained a guard instead: a lock directory (`build/.finish.lock`, pid inside) makes a second invocation exit at once, and once `build/master-2160p60.mp4` is newer than `narration/selection.json` the script reports itself finished and exits unless called with `--force`. The guard was installed by atomic rename while the first run was in progress (a running bash keeps its original inode) and was tested from a second shell.
- **`finish.sh` fix.** Two steps piped multi-line Python output into `head -1`; under `set -o pipefail` a closed pipe would have aborted the chain after the music step. The pipes were removed so the full output lands in the log.
- **Narration.** Synthesis finished at 23:42:57 (`done`; 166/166 beats, 39.4 min of audio, no `[failed]`). The producer's transcription QA run reached 147 takes and exited at 00:04; `finish.sh` (started 00:07) checked the remaining 19, flagged 63 beats, regenerated them as attempt 02 (00:12–00:46, 16.6 min of audio), transcribed those and re-selected. `narration/selection.json`: 166 beats, 32 use attempt 02, 53 still carry a flag. Nearly every remaining flag is the transcriber's tokenisation, not the voice: `v b` heard as `vb`, `gooey` as `gui`, `nineties` as `ninetys`, spelled numbers as digits, `queue` as `q`. Eleven beats show a real word difference and are listed in `build/MORNING-REPORT.md` with review-cut timestamps for Devin to listen to (1:49 COBOL/cobalt, 2:32 learned/learn, 5:28 disc/disk, 6:15 BASIC/basics, 16:44 queue/cue, 17:52 data sets, 18:53 assign/assigned, 23:14 pot array, 23:23 won/one, 30:50 preferred/prefer, 35:25 WriteLine). Eleven pace flags remain, seven of them on beats under six seconds where words-per-minute is noise; the four long slow beats (4:17, 24:20, 30:16, 38:32) sit at 117–120 wpm. Per the brief, none were chased past attempt 02.
- **Timeline.** `build_timeline.py`: 183 segments, 42.0 min (2519.5 s), beats without audio 0, unmapped cues 0. The first build placed 126/130 cleared assets; BROLL-06, DIA-11, FACT-06 and TERM-03 were unused because their placement patterns named sections whose beats never say the trigger words. Producer placements, made from the beat text and the H01/H05 plans: **BROLL-06** (Pentium-era PC, Devin's "cutaway alone" ruling) on S03-B03 "you ran the installer" at 5:45, 10 s alone, the section H05 lists it under; **FACT-06** (runtime in the download story) on S13-B08 "bundle the runtime" at 29:01, 15.8 s; **DIA-11** (1995 tools comparison) on S14-B11 "sweet spot: easier than C++, more established than Delphi, cheaper than PowerBuilder" at 32:49, sharing 20.4 s with the Java AWT still; **TERM-03** (R5 code scroll-through recording, "section 6 onward, whenever code is discussed") on S17-B03 "the code is straightforward" at 41:05, 23.9 s. The patterns in `tools/assembly/build_timeline.py` were corrected, the timeline rebuilt (130/130 used, running time unchanged) and every segment re-rendered in a second pass (02:06–03:05).
- **Music and effects** as planned in session 8: 8 beds from Devin's keeps with 15 chapter stings (`narration/music-plan.json`, `narration/sfx-music.json`), 6 effect cues (`narration/sfx.json`: Windows 95 chime 4:58; shuffles 9:12, 9:32, 15:54; slaps 21:43, 22:40). Blast Processor and Inverse Phase keeps untouched.
- **Renders.** `build/review-1080p60-mixed.mp4` (H.264 1920×1080 60 fps, 288.9 MB) and `build/master-2160p60.mp4` (HEVC 3840×2160 60 fps, Lanczos from the 1080p sources, 660 MB). Verified: both files probe at 2519.94 s (timeline 2519.5 s plus the end-card hold), 1920×1080 and 3840×2160 at 60 fps, AAC 48 kHz stereo. The first mix measured -15.8 LUFS integrated but true peak +0.1 dBFS: `alimiter` in `render.py` had its auto-level option on by default, which rescales the clamped signal back to full scale, so the 0.94 ceiling never held on the output. The mix now runs the limiter with `level=0` and a 0.89 ceiling (-1.0 dBFS sample); the final mix measures -16.3 LUFS integrated, LRA 5.0 LU, true peak -0.8 dBFS, and the master carries that audio unchanged (re-mixed 04:05, master re-rendered after it). A 20 s excerpt from the middle of section 10 (from 22:19) carries voice and bed at -18 dB RMS. Contact sheet (nine frames, 280 s apart) shows real framed content throughout; a 20 s excerpt from the middle of section 10 carries narration and bed. Pass-1 renders without the four late placements are kept as `build/pass1-*.mp4` (uncommitted, disposable).
- **Release package.** `build/captions.srt` and `.vtt` (553 cues, last cue ends 2511.0 s against the last beat's 2511.1 s), `build/transcript.md` (6102 words), `build/upload-metadata.md` (title, description, tags, 17 chapters at the real chapter-card times). Nothing uploaded.
- **Committed:** `narration/qa.json`, `selection.json`, `timeline.json`, `music-plan.json`, `sfx.json`, `sfx-music.json`, the four build text files (force-added), the two tool fixes, `build/MORNING-REPORT.md` and this entry. Not committed by design: `narration/takes/`, `recordings/`, `build/*.mp4`, `narration/synth.log`.
- **Status page.** Republishing the status artifact was refused by this session's permission classifier (unrequested publish); the updated page is committed as `build/status-page.html` for Devin or the producer to publish to the same URL.
- **To redo the chain** after any change: `bash tools/assembly/finish.sh --force` (full), or the individual steps in `tools/assembly/` followed by `render.py --profile master` with the music and effect arguments; the master profile regenerates the review cut and the mix on the way.

## Session 10 — round 2: Devin's review of the first cut, fixed and re-rendered (2026-09-16)

Devin watched the first cut to about 17:00, sent 19 notes, approved the producer's seven proposals for 17:00 to the end, and said "make as many of those fixes yourself as you can". The Video Executive Producer session (`vb-video-checkout-2-b3 [4f305e]`) ran the round: 13 new tickets, 16 revisions, 16 worker sessions in git worktrees (one ticket group each, branch `ticket/<ID>-r2` or a group name, merged into `main` after the producer's validator run and a look at the exports), and the tool work in this checkout.

- **Narration (NAR-01).** Two beats were stage directions read aloud (multi-line `**[VISUAL: ...]**` blocks parsed as narration): `tools/narration/beats.py` now keeps a cue open until its closing `]**`; S12-B05 and S12-B08 are gone (166 → 164 beats, takes retired under `narration/takes-retired/`), later section-12 IDs shifted and their takes, QA and selection keys were remapped by spoken text. "C++" heard as "2++" at S08-B02: a per-beat spoken-form fix (`SPOKEN_FIXES`, keyed by written text) reads "see plus plus"; attempt 03 transcribes as "C++" and is pinned in `selection.json`.
- **Mix (ASM-01, ASM-02).** Beds 6 dB lower across the plan; each bed ends fully 1 s before the next chapter card, the 8 s sting plays alone on the card, the next bed starts 0.5 s after it; every effect cue in `narration/sfx.json` drives the bed to -40 dB from 0.3 s before the effect until 0.2 s after it, releasing over 0.8 s (`effect_duck_expr` in `render.py`); `--bed-stem` writes the ducked music alone for measurement. Sections 1–3 test: bed 20 LU under the voice under speech, silent in the gap, -79 dB during the chime, whole mix -16.5 LUFS.
- **Timeline (ASM-03).** `build_timeline.py` rewritten: a placement map (beat → visuals, cutdowns, and the word each key moment lands on, using proportional word timing and each cutdown's `key_second`), one visual per beat, cue extras carried forward one per following beat instead of cycling, a 60 s no-return guard on carried extras, holds of motion assets show the end frame instead of replaying, cutdowns may resume at an offset (`name@seconds`), a report at `assets/ops/ASM-03/exports/report.md`. `render.py` honours per-visual slots, loops stock clips instead of freezing, and seeks resumed cutdowns. Cold open shows the code scroll-through (TERM-03); section 5 is locked to DIA-15 and DIA-02's cutdowns on the words; every placement Devin approved is in the map.
- **Cards (OPS-01 revision 2).** Shared faces redrawn as regular playing cards (pip layouts, court marks), `win95-workbench-1.1.0`; DIA-03, DIA-06, DIA-07, DIA-09, CARD-01, MOCK-01 re-rendered on them.
- **Assets produced this round and release-approved by the producer after viewing:** CMP-01/04/05/06/07/08 (language headers), CMP-02 (Sub vs Function, animated), CMP-03 (`i`, then the transform into the real `Rank` loop, Program.vb 104–110), CMP-09, CODE-02 (arrows from the margin), CODE-26, CODE-27, CODE-28, CODE-29, REF-02 (73-line Win16 Hello World), REF-05, DIA-02 (deck-hold, alternating-deal, normal-round, single-war, final-hold), DIA-04 (code demo with C++ column, verified by running VB.NET and C++), DIA-05 (live-slots, append, draw-shift, cost), DIA-08 (`endgame` with the round-617 numbers from TERM-04's stdout), DIA-12 (row reveal), DIA-15 (riffle), FACT-07, FACT-08 (figures cited to captured stdout). Every `validate_delivery` run ok; `validate_pack` ok (original families counted excluding `R2-*`).
- **Workers' warnings kept on record:** `finish_delivery.py` rewrites ticket files (dropping revision sections) and `review/*.json`; `build_assets.py` would regress CODE-02, REF-02 and the CMP headers and fails on CODE-26..29 (no focus sequence); `finish_delivery.py` drops `key_second`. Workers wrote delivery.json by hand for those; the producer should not run either tool without checking.
- **Render.** Second cut rendered 2026-09-16 evening. The 1080p was checked before any upscale (Devin's correction): `build/review-1080p60-mixed.mp4` (41:24, 267 MB, -16.2 LUFS, true peak -0.8 dBFS; captions 547 cues ending with the last beat; 17 chapters matching the cards; bed 20 LU under the voice, silent under every bed change with the sting alone, floor around every effect; the chime on the launch footage). Two mistakes caught by that check and fixed before the master: the music plan and effect cues had been generated from the earlier timeline (the finish script regenerates them after the timeline for this reason), and stings inside a bed's range overlapped the bed, so stings now play only at the six bed changes. `build/master-2160p60.mp4` upscaled from the verified 1080p (HEVC 3840×2160 60 fps, 629 MB, same audio). Running time 41:24, down from 42:00 with the two stage directions removed.
- **Not done:** the fourteen cleared assets left off the cut by design (retired shuffle clip, captures replaced by FACT-07, screenshots covered by the collage, extras the one-visual rule dropped); Devin's notes from 17:00 onward are still his to send.

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

- **Current producer:** `vb-video-checkout-2-38 [20c133]` (Claude Fable 5.1, since 2026-09-15) working in `C:\dev\youtube\vb-video-checkout-2`. Departments confirm this with `ListAgents` before reporting.
- Default branch is `main` (renamed from `master` on 2026-09-15; GitHub redirects old links).
- `.gitattributes` stores every asset folder and the hash-locked sources and harness byte-for-byte (`-text`). With `core.autocrlf=true`, Git would otherwise rewrite line endings on checkout and break the SHA-256 hashes recorded in `delivery.json` and `harness-manifest.json`.
