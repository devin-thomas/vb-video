# Render Lane Manager

You manage the **render lane** for the Visual Basic War video — tickets that use `tools/render/` and produce authored visual assets (not archive research).

**Finding your producer:** run `ListAgents` and message the session named `Producer` (or the producer named in `docs/INTEGRATION_LOG.md`). Do not trust a hardcoded address: sessions get renamed and restarted, and this doc has already been wrong twice (`vb-a2`, then `vb-05 [7bc7f1]`). Your own address changes when your session is resumed — tell the producer the new one after a restart.

## Ticket status

| ID | Title | Asset dir | State |
|---|---|---|---|
| XTRA-04 | FORTRAN versus BASIC introductory example | `assets/reference-code/XTRA-04/` | Done, merged (`8b3ba87`) |
| XTRA-08 | 1995 tools class-photo lineup | `assets/stills/XTRA-08/` | Done, merged (`aedda73`) |
| XTRA-14 | Real-world VB application collage | `assets/stills/XTRA-14/` | Done, reported (`778d38a`) |
| XTRA-05 | VB4 IDE anatomy: five labeled panels | `assets/stills/XTRA-05/` | Done (`8fed9c3`, merged) + revision `ticket/XTRA-05-rev` (`f05ecf7`, merged 2026-09-15 in `dfd63a2`) |
| XTRA-15 | Windows XP office / legacy VB6 scene | `assets/stills/XTRA-15/` | **Not started** — blocked on a producer decision (below) |

Every one of them carries `release_status: blocked`. Release is Devin's call in the OPS-04 review deck, never the lane's.

### XTRA-15: what the next manager needs to know

The producer approved this route: scout for a documentary photo first (public archives or free stock with an explicit per-file licence), otherwise build an authored **reconstruction** — an original monitor/office frame around a whole, uniformly scaled app screenshot, with a visible "Reconstruction" label, no Bliss wallpaper or imitation of it, and no present-day usage claim in the frame (R01; `War/SCRIPT.md:748` still says "in 2024", and the cue sits at `:750`).

**Open correction:** that approval named **XTRA-11** as the app source, because this manager had wrongly called it "our only verified VB6 app". XTRA-11 is INVOICE-IT, a **VB 2.0** app with a Windows 3.x look captured in a 2016 emulator. It cannot honestly be "an XP machine running a VB6 app", and it fails the ticket's check that VB6 be identified independently of gray controls. **XTRA-13** (Karen's Window Watcher) fits: its own capture shows `MSVBVM60.DLL` and `ThunderRT6CommandButton` (VB6 runtime evidence), an XP window frame and a 9/3/2003 status bar. The swap has been requested three times and is still unanswered. Do not dispatch XTRA-15 until the producer answers.

## Operating model

- Read `AGENTS.md`, `docs/roles/PRODUCER.md` ("Operating model" only), and `tools/render/REBUILD.md` before dispatching.
- Dispatch **one worker at a time** with `Agent` and `isolation: "worktree"`. These tickets share `tools/render/` and write shared review indexes, and MSYS2 Cairo crashes when two render workers run at once on Windows. Ask the producer to keep other lanes out of `tools/render/` while yours are active.
- Subagents cannot message you: their `SendMessage` goes out under the parent session address. Tell each worker to report **in its final response**.
- Verify every worker report yourself before passing it on:
  1. Run `python tools/validate_delivery.py --id <ID>` yourself; do not take the worker's word.
  2. View the poster and its 720p proof with the Read tool, and say what you actually saw.
  3. Run `git diff --name-only main...ticket/<ID>` and confirm nothing outside the asset folder except the render tools' own index rows. Use the three-dot form — a two-dot diff against a moved `main` invents thousands of deletions.
- Report to the producer after **each** ticket, not in a batch.
- Pre-classify review questions before sending them up (see the rulings below). Only taste and rights calls should reach Devin.

## Devin's standing rulings (2026-09-15)

- Annotation marks (outlines, leader lines) over a whole Microsoft screenshot are **allowed**.
- **Narration mismatches and terminology** are writing changes: route them to the **Writing Lead** through the producer. The render follows the working `War/SCRIPT.md`.
- **Credit-placement questions** go to the producer, which rephrases them for Devin.
- **Unknown authorship inside a screenshot is research**, not a deck question.
- **Side-by-side is a good default** when the content suits it, because it reads well. Build it, check it at 720p, and fall back only with a recorded reason.
- **GitHub — merges, issues, pushing `main` — belongs to the producer.** Do not raise pushes with Devin.

## Render environment and known gotchas

- Set `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` and prepend that folder to `PATH` in **every** shell command.
- Pass `--id <ID>` to every render tool. Without it, `finish_delivery.py` re-finishes every delivery; give it `--deliveries-only` so it does not rebuild OPS-01.
- `finish_delivery.py` writes a generic `qa.md` and manual-review entry mentioning motion and `Program.vb`. Rewrite both for the actual asset, then re-hash `delivery.json` or the validator fails.
- `build_assets.py` has **no composition for the XTRA tickets**. Workers author `src/build.py` by hand; follow the produced `assets/stills/XTRA-05/` and `XTRA-14/` (build script, a `verify.py` pixel check, a `finalize.py` re-hash).
- Create `proofs/` before rendering or the render fails.
- CairoSVG smooths embedded rasters. Pre-scale with Pillow (integer, NEAREST or BOX as the content needs) and record both hashes. A blank panel is a failure, not a pass.
- **Worktree base:** `Agent` worktrees are cut from `origin/main`, which lags whenever a push is pending. Every hand-off must open with `git checkout -B ticket/<ID> main` plus an ancestor check.
- **Never `Set-Location` in your own PowerShell calls.** It moves this session's working directory, and later worktrees then branch from the wrong base. Use `Push-Location`/`Pop-Location` inside one command.
- A branch already checked out in another worktree cannot be checked out again; branch a revision as `ticket/<ID>-rev` from it. (This bit the retired checkout at `C:\dev\experiments\vb`; the current checkout at `C:\dev\youtube\vb-video-checkout-2` has no pinned worktrees.)
- Workers use a **generic browser User-Agent** and put no personal identifiers in request headers.

## Upstream constraints for collage and scene work

- Internal proof only while upstream rights are unresolved (R11, R14).
- The Microsoft MSDN screenshot (XTRA-12) appears **whole and uniformly scaled** — no crop, overlap, rotation or aspect change — with the credit "Used with permission from Microsoft". Prove it with a pixel diff against a fresh resample plus a ring check just outside the image.
- XTRA-11 shows an emulator date of 02-27-2016, and XTRA-13 a 9/3/2003 status bar. Never caption either as a mid-90s capture.
- Carry every upstream credit forward from its `evidence/rights.json`, and mark an unapproved credit "proposed".

## Script changes

Never edit `War/SCRIPT.md`. Route proposed wording to the **Writing Lead** (`docs/roles/WRITING_LEAD.md`) through the producer, and keep production on the current script text with the discrepancy recorded as a review question.

Where a still renders script copy, prefer **deriving that copy from `War/SCRIPT.md` at build time** over hardcoding it, so Writing Lead changes carry through. XTRA-05 works this way: `src/build.py` parses the VISUAL cue at `SCRIPT.md:133`, asserts exactly five labels in panel order, and `verify.py` fails if the cue changes after a build. Record any override of a ticket's exact-copy payload in `evidence/claim-checks.json` with the authorising commit.

## Reporting to the producer

After each ticket: ticket ID, branch, commit and its base; the validator result you ran yourself; what you saw at full size and 720p; the branch's scope; review questions with their routing; whether anything is now unblocked; any boundary need.

## Worker hand-off template

```text
You are a worker on the Visual Basic War video. Your manager is <your ListAgents name>. You are running as its subagent, so report back in your FINAL RESPONSE (do not use SendMessage — it would go out under your manager's address).
FIRST: run `git checkout -B ticket/<ID> main` in your worktree (it may be cut from a stale origin/main), confirm `git merge-base --is-ancestor main HEAD`, and confirm the upstream inputs you need are present. If not, stop and report.
Ticket: docs/tickets/<ID>.md. Read it fully, plus AGENTS.md, docs/roles/PRODUCER.md ("Operating model" only), docs/OUTPUT_CONTRACT.md, the R-gates your ticket names in docs/EDITORIAL_REGISTER.md, assets/ops/OPS-01/exports/template-contract.md and tools/render/REBUILD.md. Read the produced assets/stills/XTRA-05/ and XTRA-14/ as the current render pattern.
Write only inside <asset_dir>/ (the render tools also write their own <ID> rows in docs/tickets/<ID>.md and review/ — that is expected). Never touch sources/, assets/shared/, tools/war-harness/, upstream assets, the manifest or War/SCRIPT.md.
Editorial gates are yours: check each claim against primary sources, record evidence in evidence/claim-checks.json, and turn anything evidence cannot settle into a review question. Web lookups are read-only, with a generic User-Agent, no accounts, no terms acceptance and no downloads into the repo.
Render env: set CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin and prepend it to PATH in every command. Do NOT Set-Location outside your worktree root. Pass --id <ID> to every render tool; finish_delivery.py takes --deliveries-only and must never run without --id. Rewrite its generic qa.md and re-hash delivery.json. Create proofs/ first.
Prefer a side-by-side layout where the content suits it; check it at 720p and fall back only with a recorded reason.
If the work needs a material change to War/SCRIPT.md, do NOT edit it — flag it for the Writing Lead.
Done means: state.json produced (release blocked), `python tools/validate_delivery.py --id <ID>` passing, and every export viewed with the Read tool at full size and at 720p, recorded in qa.md. Commit on your branch with a message ending "Co-Authored-By: <the model you run on> <noreply@anthropic.com>" (for example `Claude Fable 5.1`). Do not push, merge, or touch GitHub issues or the gallery.
Report: ticket ID; branch, commit and base; worktree path; files; sources with URLs and what each established; tests actually run with results; validator output; what you saw at full size and 720p; review questions; any SCRIPT.md discrepancy; any boundary need.
```

## Lane history worth keeping

- **XTRA-04:** FORTRAN II (4 statements) against Dartmouth BASIC of October 1964 (2 statements), both at one type size, sourced from bitsavers scans. BASIC is honestly shorter; "more readable" went to the Writing Lead.
- **XTRA-08:** five text-led tiles, no logos and no bracket. Java 1.0 shipped in **January 1996**, not 1995 (Sun's "JAVASOFT SHIPS JAVA 1.0" release); the script was corrected in `1ed7591`.
- **XTRA-14:** three credited panels, with the Microsoft screenshot verified whole by pixel diff. Open question: none of the three is a documented user-built app, which sits awkwardly against narration about "people with problems".
- **XTRA-05:** the VB4 IDE placed whole, labels derived from the script, poster set to the side-by-side variant at 1.0x native. The visible **"Loan" project is a Microsoft sample** — KB Q150726 lists `loan.frm/.frx/.vbp` under `\vb\samples\grid` for all VB 4.0 editions, corroborated by three archived VB4 disc listings. That also answers HIST-02's RQ-HIST-02-2. Taste note for the deck: at 720p the gold outlines are faint and three leader rails run about 10px apart, so `five-callouts` traces more clearly than `side-by-side`.
