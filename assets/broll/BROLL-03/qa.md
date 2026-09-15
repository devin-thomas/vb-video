# BROLL-03 QA report

**Result:** scouted (3 ranked candidates). No media acquired. Release blocked; R14 open.
**Reviewer:** BROLL-03 scouting worker (agent), 2026-09-15. No human review yet.

## What was checked, and how

| Check | Method | Result |
|---|---|---|
| Candidate metadata (creator, upload date, duration, dimensions, fps, description) | WebFetch of each Pexels asset page; cross-checked in the Claude Browser pane via `get_page_text` on 8869925 and 8869644 | Recorded in `evidence/candidates.json` |
| Player-reported duration and stream size | JS on the in-page `<video>` element (shadow-DOM search) | 8869925: 27.84 s, 2732×1440 stream. 8869644: 23.92 s, 2732×1440 stream |
| Motion / frame content, rank 1 | Seeked the Pexels in-page player to 0, 1, 4, 6, 8, 11, 12, 16, 20, 24, 27.5 s and screenshotted each; muted real-time playback confirmed `currentTime` 1.00 → 6.04 s over about 5 s | CRT prominent throughout; slow push-in then pull-back; no modern items seen in sampled frames |
| Motion / frame content, rank 2 | Seeked to 0, 4, 8, 12, 16, 20, 23.4 s and screenshotted each | Near-locked medium shot; CRT cropped left; no modern items seen |
| 8869773 (rejected) | Played in-page; screenshots at 0, about 5, and about 11 s | No CRT in frame (typewriter only) |
| Rank 3 (archive) motion | Tried the Internet Archive in-page player twice | **Failed:** `networkState` 3 (NETWORK_NO_SOURCE), then 0, with `readyState` 0 and duration null. Motion not reviewed |
| Rank 3 content triage | Viewed the 20 Internet Archive thumbnail JPEGs from `jpo-automation.thumbs/` in-page, as a grid built in the tab (no file saved) | Office/CRT scenes near 238, 598, 775 s; baked caption at 174 s |
| Download options | Opened the Pexels size menu (chevron only) and read its text and link hrefs; never clicked "Download Selected Size" | Size labels recorded; no file sizes are displayed by Pexels |
| License and terms text | WebFetch of pexels.com/license, pexels.com/terms-of-service, pixabay license summary, CC PDM 1.0 deed, CC retired public-domain tool, help.archive.org rights page | Quoted in candidates files and claim-checks |
| Bot walls / CAPTCHA | Observed on every site visited | None encountered on Pexels, Pixabay, Mixkit, Internet Archive, or Wikimedia Commons |
| Delivery structure | `python tools/validate_delivery.py --id BROLL-03` | See the final section |

## Not checked

- **No full-size or 720p inspection.** No media was downloaded, so there are no export images or video to view at 1080p or 720p. Screenshots were at Browser-pane size (800×609 or 1024×768 viewport). The ticket's 1080p/720p manual inspection is not applicable until acquisition.
- **Not every frame** of the proposed segments was inspected; frames were sampled about every 3–4 s. Pexels' play-button overlay covered a small central circle in paused frames. Frame-by-frame review is a post-download task (see `exports/acquisition-handoff.md`).
- **Audio** was not reviewed (players muted).
- **Rank 3 motion**, shot boundaries, narration, and captions around the tentative in point.
- **Actual downloaded file versions**, codecs, and exact fps of the delivered files.
- **Legal clearance:** model releases for Pexels actors, and copyright status of the 1989 Japanese government film. These are review questions, not findings.
- Internet Archive Terms of Use text: WebFetch of `archive.org/about/terms` returned only the site title.
- Leads listed as "not motion reviewed" in `evidence/candidates.json`.

## Reproduction

In-page seek used for the frame samples (run in the browser console on the asset page, after finding the player's `<video>`, which may sit inside a shadow root):

```js
const v = (function all(root){let out=[...root.querySelectorAll('video')];root.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)out=out.concat(all(e.shadowRoot))});return out;})(document).find(v=>v.getBoundingClientRect().width>300);
async function seek(t){ v.pause(); const p=new Promise(r=>v.addEventListener('seeked',r,{once:true})); v.currentTime=t; await p; return v.currentTime; }
await seek(1.0);  // then screenshot; repeat for each sampled time
```

Internet Archive searches (JSON):

```
https://archive.org/advancedsearch.php?q=(title%3A(office)%20AND%20(computer%20OR%20computers))%20AND%20mediatype%3Amovies&fl[]=identifier&fl[]=title&fl[]=year&fl[]=licenseurl&fl[]=collection&rows=100&output=json
https://archive.org/advancedsearch.php?q=mediatype%3Amovies%20AND%20(computer%20OR%20computers%20OR%20workstation)%20AND%20(office%20OR%20workplace%20OR%20employees)%20AND%20year%3A%5B1990%20TO%201999%5D&fl[]=identifier&fl[]=title&fl[]=year&fl[]=licenseurl&fl[]=collection&rows=100&output=json
https://archive.org/metadata/jpo-automation
```

Validation, run from the worktree root:

```
python tools/validate_delivery.py --id BROLL-03
```

## Toolchain

- Python 3.14.0 (validator, hashing)
- git 2.53.0.windows.1
- Claude Browser pane (in-app Chromium; version not exposed), used for playback, seeking, screenshots, and page text
- WebFetch and WebSearch tools (Claude Code), used for page metadata and license text
- No renderer, encoder, or ffprobe used; no media exists to probe.

## Validator result

`python tools/validate_delivery.py --id BROLL-03` → `"ok": true`, `"errors": []` (run after final hashing on 2026-09-15). Its stated limits: no OCR or visual judgment, no MP4 decode, no legal clearance, and manual review still required.
