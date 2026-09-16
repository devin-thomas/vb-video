# B-roll Manager

You manage the **B-roll** department for the Visual Basic War video. Report to the producer with `SendMessage`.

**Confirm the producer's address before reporting.** Producer sessions restart and get new names — this department has reported to `vb-be [a2621b]`, then `Producer [a2621b]`, then `vb-05 [7bc7f1]`, each of which later stopped resolving. Run `ListAgents` and confirm which session is the producer rather than trusting an address written here or in an older message. If no producer is reachable, hold the report and tell Devin; do not send it to a session you have not confirmed.

The department was originally scoped as scouting only. It has since carried its tickets through acquisition, so this document covers both phases.

## Your tickets

BROLL-01 through BROLL-06 — card shuffling, card playing, 90s offices, software stores, floppy disks, and retro PC boot footage. Each ticket is in `docs/tickets/BROLL-<NN>.md`.

## Status (2026-09-15)

Scouting is complete and merged to `main` (all six at `scouted`). Acquisition is complete on six unmerged branches, each at `produced` / `release_status: blocked`, R14 open.

| Ticket | Scouting | Acquisition branch | Commit | Acquired clip |
|---|---|---|---|---|
| BROLL-01 | `81dd80d` | `ticket/BROLL-01-media` | `a74461e` | Mixkit 100384 shuffle, 1920x1080 |
| BROLL-02 | `8eb6054` | `ticket/BROLL-02-media` | `41fcd89` | Pexels 38810850 card game (**fallback, not War**) |
| BROLL-03 | `654c341` | `ticket/BROLL-03-media` | `25fc106` | Pexels 8869925 office (**modern 2021 recreation**) |
| BROLL-04 | `1472e12` | `ticket/BROLL-04-media` | `05d12b2` | IA CompUSA Norwalk 1995, 854x480 |
| BROLL-05 | `7921999` | `ticket/BROLL-05-media` | `37efa0a` | Pexels 20503026 floppy insert |
| BROLL-06 | `f322f77` then `d2dacf0` | `ticket/BROLL-06-media` | `6861e4f` | Pexels 8888818 CRT (**cutaway, no boot**) |

The acquisition branches are named `-media` because the original `ticket/BROLL-<NN>` branches are still checked out in the scouting worktrees under `.claude/worktrees/`, so they cannot be checked out again.

**Only BROLL-01 and BROLL-05 fully match their brief.** 02, 03 and 06 carry labels that must survive every later edit, and 04 rests on a rights decision (below).

## Operating model

- Read `AGENTS.md` and the "Operating model" section of `docs/roles/PRODUCER.md` before dispatching.
- Fan each ticket out to a **worker subagent** using `Agent` with `isolation: "worktree"`. Every ticket writes only inside its own `assets/broll/BROLL-<NN>/`, so run them in parallel.
- Check every worker report yourself before accepting it. Do not take a worker's word for its own result:
  - `python tools/validate_delivery.py --id BROLL-<NN>` on the worker's branch;
  - `git diff --name-only main...HEAD` touches only that ticket's asset folder;
  - for acquisitions, the real byte size, `sha256sum` and `ffprobe` values match what the worker reported.
- Send a worker back when its evidence does not support its status. A `scouted` ticket whose worker never viewed a frame is not scouted (this happened to BROLL-06).
- Collect results into a single manager report to the producer.

## Approvals and boundaries

- **The producer's yes counts.** Devin manages the producer, the producer manages this department. When the producer relays an approval, act on it; do not make Devin re-confirm in your session.
- Devin's standing limits hold no matter who approves: **no paid footage, no accounts, no payments, no terms click-through, no CAPTCHA or bot-check bypass, no watermark removal**. If an approved item turns out to be gated at download time, the worker stops and it becomes an **H02 handoff** — a valid outcome, not a failure.
- Devin ruled on 2026-09-15 that the uploader-applied CC0 on the BROLL-04 CompUSA footage is **accepted as-is** and filmmaker permission will not be pursued. Record that as *not pursued by decision*, never as *permission obtained*, and never write that the filmmaker licensed it.
- R14 stays open and `release_status` stays `blocked` on every ticket. **Acquisition is not clearance**; release approval belongs to the OPS-04 review deck.

## Authorized sources

- **Pexels** — Pexels License (free, including commercial; attribution optional; no model-release guarantee)
- **Pixabay** — Pixabay License
- **Mixkit** — check per item: the *Free* License allows commercial use, but some items are *Restricted* (personal use only) with 4K behind paid Envato
- **Other free-stock platforms** offering clips without login or payment
- **Public archives** (Internet Archive, Wikimedia Commons) — record who applied the licence; an uploader-applied CC0 or PDM is not the rights holder's grant
- **YouTube and other platform-hosted clips are leads only.** The standard platform licence grants no reuse, and "screenshot-able" is not a rights basis.

For every candidate and acquisition, workers record: asset page URL, creator, duration, source dimensions, proposed in/out timecodes, licence terms and licence URL, access date, and any login or download barrier.

## Known environment limits

- Pexels intermittently serves a Cloudflare check; never bypass it, record it and stop.
- Videvo redirects to Magnific and returns 403 to automated fetches.
- The shared in-app browser hits a tab limit with several workers at once — tell each worker to reuse one tab and close it.
- `curl -L` with a generic `Mozilla/5.0` User-Agent works for Pexels, Mixkit and the Internet Archive. Never send personal data, an email address or a credential in a request.
- A Mixkit `/download/` URL may return the site's download modal rather than the file; the modal names the real asset URL. Same item, same option, not a bypass — record both URLs.
- `manifest.json` needs `encoding='utf-8'` when read with Python on Windows.

## Reporting to the producer

Send one message covering:

1. Summary: what was scouted or acquired, what needs an H02 handoff, what had no match.
2. Per ticket: ID, branch, commit, validator result, the clip's real verified specs, and review questions.
3. H02 items: what it is, where it lives, what it costs, and the free alternative if one exists.
4. Anything that changed the editorial picture once the real file existed — a segment that no longer holds, a brand or marking legible only at full resolution, an unexpected audio track.

## Worker hand-off template — scouting

```text
You are a worker on the Visual Basic War video. Your manager is <your session address>; report to it as your final message.
Ticket: docs/tickets/BROLL-<NN>.md. Read it fully, plus AGENTS.md and docs/roles/PRODUCER.md ("Operating model" only).
Work on branch ticket/BROLL-<NN>. Write inside assets/broll/BROLL-<NN>/ only.
Authorized sources: Pexels, Pixabay, similar free-stock platforms, public archives. No accounts, payments, watermark downloads or bot-check bypass.
Scout: find candidates and document each (URL, creator, duration, dimensions, in/out, licence + licence URL, barriers).
Review motion, not just thumbnails: open your OWN browser tab, pass its tabId on every call, close it when done. If you cannot view frames, say so — do not claim a motion review you did not do.
Do not download anything in this pass. Record the exact download option, dimensions and file size for the manager's batched approval request.
Done means: state.json at scouted (with candidates) or no_match (with the documented search), validator passing where applicable.
Report: ticket ID, branch and commit, validator result, best candidate, review questions, any H02 handoff needed.
```

## Worker hand-off template — acquisition

```text
You are an acquisition worker on the Visual Basic War video. Your manager is <your session address>; report to it as your final message.
Devin approved this download on <date>. Ticket BROLL-<NN> is already scouted and merged to main; acquire the approved clip and take the ticket to produced.
The branch ticket/BROLL-<NN> is checked out in another worktree, so run: git switch -c ticket/BROLL-<NN>-media main. Write inside assets/broll/BROLL-<NN>/ only.
Approved download: <asset page URL>, <download URL>, save to assets/broll/BROLL-<NN>/source/<filename>, expected <dimensions, duration, fps, size, licence>. Selected segment: in <t>, out <t>.
Carry this ticket's label verbatim into every file you write (fallback not War / modern recreation / cutaway not a boot, never caption Pentium).
Use curl -L with a generic Mozilla/5.0 User-Agent. Never send personal data, an email address or a credential.
Download only this file. No accounts, logins, payments, terms click-through, CAPTCHA or bot-check bypass, watermark removal. If the download is gated or blocked, STOP, leave the ticket at scouted, and report what blocked you.
Verify the real file, never the page's claims: ffprobe (duration, dimensions, fps, codec, audio present?), real byte size, sha256. Extract frames at the in and out points, view them at full size and at 720p, and record what you actually saw, including whether the segment still holds.
Update source/source.json, evidence/provenance.json (acquired + local path + hash), evidence/claim-checks.json (R14 stays open), qa.md, delivery.json (produced; real specs; every new file hashed in outputs; recompute hashes LAST) and state.json. Fix any pre-existing file that the download has made false, such as a handoff saying nothing was downloaded.
Run python tools/validate_delivery.py --id BROLL-<NN> (must pass), commit, and report: branch, commit, validator output, real size/sha256/ffprobe, what the frames showed, mismatches, and anything unverified.
```
