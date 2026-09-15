# BROLL-05 QA

Scout: BROLL-05 scouting worker (subagent of the B-roll Scouting Manager, vb-99). Date: 2026-09-15. Reviewer: none yet (OPS-04 review deck).

## Outcome

`production_status: scouted`, `release_status: blocked`.
- One recommended candidate: Pexels 20503026.
- One rights-blocked alternative: Mixkit 48937.
- Five rejections: two after motion review, three on page description.
- No media downloaded.

## What was checked and how

| Check | Method | Result |
|---|---|---|
| Search coverage | WebSearch; WebFetch of Pexels, Pixabay, Mixkit, Coverr, Videvo, Vista Create and Wikimedia Commons search pages; Internet Archive `advancedsearch.php` JSON; in-app Browser on Pexels search | Logged in `evidence/candidates.json` → `search_log` |
| Asset metadata (creator, duration, dimensions, fps, date) | WebFetch of each asset page; for the reviewed clips, cross-checked `duration`/`videoWidth`/`videoHeight` read from the page's own `<video>` element in the Browser | Pexels 20503026: 11.156667 s, 1920×1080. Pexels 20503027: 5.566667 s, 1920×1080. Mixkit 48937: 7.24 s, 1280×720 |
| Motion review | Opened each asset page in my own Browser tab (`tab-4`), paused the page's preview `<video>`, set `currentTime`, waited 2 s, screenshotted the 800×609 viewport | 20503026: 13 frames (0.1–10.9 s). 20503027: 5 frames. Mixkit 48937: 4 frames. 33125208: 3 frames during live playback (timecodes not captured) |
| Media size, drive type, insertion direction | Visual reading of those frames (details per frame in `evidence/candidates.json`) | 20503026: 3.5-inch confirmed from the "2HD"/"1.44" label and slot width; 3.5-inch-style push-button drive; label side up on a flat drive. The shutter end leading is **inferred** from the trailing-edge corner holes; the shutter itself isn't visible. 33125208: 5.25-inch, rejected. Mixkit: disk edge-on, so direction can't be verified |
| Download options and barrier | Opened the Pexels "Free download" size dropdown (no download clicked); read the Mixkit download panel text | Pexels: five sizes up to Full HD 1920x1080, no file size shown, no login or CAPTCHA seen. Mixkit: free 720p personal use only; 4K via Envato |
| License text | WebFetch of https://www.pexels.com/license/ and https://mixkit.co/llm-info/; Browser load of https://mixkit.co/license/ and the Mixkit asset page | Recorded in substance in `evidence/candidates.json`. The Mixkit Restricted License modal body didn't expose text to page-text extraction; the wording comes from the asset page and Mixkit's info page |
| Delivery structure | `python tools/validate_delivery.py --id BROLL-05` | See below |

## Reproduction commands

Run from the worktree root.

```sh
# Source excerpt hashes
sha256sum sources/ASSET_PLAN.md sources/SCRIPT.md
sed -n '109,122p' sources/ASSET_PLAN.md
sed -n '799,805p' sources/SCRIPT.md

# Output inventory hashes (after all edits)
python -c "import hashlib,pathlib;b=pathlib.Path('assets/broll/BROLL-05');[print(p, p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest()) for p in ['qa.md','evidence/provenance.json','evidence/source-excerpts.md','evidence/claim-checks.json','exports/candidates.md','evidence/candidates.json','exports/acquisition-handoff.md'] for p in [b/p]]"

# Structural validation
python tools/validate_delivery.py --id BROLL-05
```

**Motion review in the in-app Browser.** For each candidate:
1. Open the asset page.
2. In the console, find the largest `<video>`. On Pexels it sits inside shadow DOM, so walk shadow roots.
3. Run `v.pause(); v.currentTime = <t>`, wait about 2 s, then screenshot.

## Tool versions

- Python 3.14.0
- git 2.53.0.windows.1
- GNU coreutils sha256sum 8.32
- Claude Code in-app Browser pane (Chromium-based; version not exposed)
- WebFetch and WebSearch tools. WebFetch returns small-model summaries of page content.

## Proof paths

No 1080p or 720p proof exports exist. This is a scouting ticket with no acquired media, and the validator requires no PNG/MP4 here. Frame inspections were screenshots in the Browser session and were not saved to disk, so the per-frame observations are recorded as text in `evidence/candidates.json`.

## NOT checked

- **Downloaded file.** Actual bytes, file size, codec, audio track, true frame rate and ffprobe output are unverified. Nothing was downloaded.
- **Audio and narration.** Previews were muted and seeked; audio wasn't listened to.
- **Frame-accurate timing.** Frames were sampled every 0.5–1.5 s, not at every frame. The exact moment the hand leaves (between 3.0 and 4.5 s) and returns (between 6.0 and 6.5 s) is bracketed, not exact.
- **Metal shutter.** Not directly seen on the recommended clip; the insertion direction is inferred.
- **Pexels 20503028, 20503030 and 20503031.** Excluded on page description only; motion not reviewed.
- **Pixabay.** Checked only through WebFetch summaries and a pixabay.com-restricted WebSearch, not in the Browser.
- **Videvo and Vista Create.** HTTP 403 to WebFetch; not browser-checked, because the Browser tab cap was reached and one tab was hung.
- **Internet Archive.** Only the first 50 of 195 hits were reviewed, by title and license metadata; no item was played.
- **Paid platforms** (Shutterstock, Getty, iStock, Envato, Dreamstime, Pond5, Motion Array). Not loaded, by policy.
- **Mixkit creator.** Not shown in the rendered page, so it's unknown. An early WebFetch summary's "Berdiy88" is unconfirmed.
- **Legal sufficiency.** The Pexels license for this production (visible "IBM" text), taste and authenticity are review questions RQ1–RQ4, not settled here.
- **License snapshots.** Not saved as files; only read and summarised on 2026-09-15.

## Environment problems encountered

- A second Browser tab couldn't be opened because the tab cap was reached.
- In `tab-4`, several `left_click` actions and one recursive JS query timed out while the pane was hidden. Reloading and using direct JS seeks recovered it.
- Screenshots at `scale: 0.6` cropped instead of scaling, so full-scale screenshots were used.
- The `zoom` region crop isn't supported in the Browser pane.
