# BROLL-01 QA report

**Worker:** BROLL-01 scouting worker (B-roll Scouting Manager, session vb-99). **Date:** 2026-09-15. **Reviewer:** none yet (OPS-04 review deck).
**Result:** `scouted`, release `blocked`. No media acquired.

## What was checked, and how

| Check | Method | Result |
|---|---|---|
| Candidate search | WebFetch of site search/category pages: Mixkit, Pexels, Pixabay, Coverr, Videvo, Wikimedia Commons MediaSearch; Internet Archive advancedsearch and metadata APIs; WebSearch | Counts and outcomes are in `exports/candidates.md` ("Searched and not ranked") |
| Asset page facts (title, description, tags, duration, frame rate, file size, download options) | Claude Browser `get_page_text` on each Mixkit asset page, plus a read-only DOM query of the download radio inputs (`data-label`, `data-size`, `value`) and download button | Recorded in `evidence/candidates.json` |
| Preview duration and stream size | JS on the page's `<video>` element: `duration`, `videoWidth`, `videoHeight`, `currentSrc` | 100384: 19.394375 s; 100398: 10.135125 s; 100372: 18.101417 s; all preview streams 1280x720 |
| Motion review | Seeked the in-page `<video>` via `currentTime` (awaiting `seeked`), then took a browser screenshot at each time listed per candidate in `evidence/candidates.json`. 100398 also got about 2 s of muted playback (currentTime advanced to 1.94 s). | Done by frame sampling for 3 candidates. **Continuous real-time playback was not visually observed**, so speed changes, motion blur and judder between samples were not assessed. |
| Camera stability | Compared fixed background features across sampled frames | 100384: locked off (felt markings stationary 0.2–19.1 s). 100398 and 100372: no camera move seen in sampled frames. |
| Watermarks/captions | Visual check of sampled preview frames | None seen |
| License | Read the Stock Video Free License modal text from the rendered DOM at https://mixkit.co/license/ (element `.license-modal__inner`); read the license line on each asset page | Recorded in candidates.json |
| User Terms limits | WebFetch model summary of https://mixkit.co/terms/ | Summarized, **not read verbatim** (review question) |
| Pexels | WebFetch of video pages (HTTP 403); browser load of https://www.pexels.com/video/6813541/, which showed a Cloudflare "Performing security verification" page; waited 8 s, did not clear | Stopped; no bypass attempted |
| Cookie consent (Mixkit) | The consent dialog covered the player. Opened "Manage preferences", switched off Preferences and Statistics (Marketing was already off), and chose "Use necessary cookies only" | Privacy-preserving choice only |
| Source excerpts | `src/build_excerpts.py` copies exact line ranges from `sources/` and the R14 register entry | Written |
| Delivery structure | `python tools/validate_delivery.py --id BROLL-01` | See below |

## Reproduction commands (from the repository root)

```
git switch ticket/BROLL-01
python assets/broll/BROLL-01/src/build_excerpts.py .
python assets/broll/BROLL-01/src/finish_delivery.py
python tools/validate_delivery.py --id BROLL-01
```

Browser motion review, run in the page console of each asset page (with the consent dialog dismissed):

```
const seek=t=>new Promise(r=>{const v=document.querySelector('video');v.pause();v.addEventListener('seeked',()=>r(v.currentTime),{once:true});v.currentTime=t;});
await seek(5.0)   // then screenshot; repeat for each sampled time
```

Download option inspection (read-only):

```
[...document.querySelectorAll('input[type=radio]')].map(i=>({label:i.dataset.label,size:i.dataset.size,value:i.value}))
```

## Tool versions
- Python 3.14.0
- git 2.53.0.windows.1
- Claude Browser pane: embedded Chromium; version not exposed to the agent
- Claude Code WebFetch / WebSearch tools
- ffprobe: not used, because no media was acquired

## Validator output
Recorded in the worker's completion report after the final run (`ok: true` is required for a scouted delivery). This file is hashed into delivery.json, so the run output is not pasted here; pasting it would change the hash.

## Not checked
- **No 1080p or 720p export inspection:** there are no rendered or acquired files. Previews were 720p streams; 1080p originals were never seen.
- **Audio/narration:** previews were played muted.
- **Continuous real-time motion:** frames were sampled at roughly 1–4 s intervals.
- 100372 frames after 10 s were captured at reduced screenshot size; detail was not assessed.
- The no-login download path was not exercised (the button was not clicked).
- The Mixkit User Terms were not read verbatim; card-back and felt designs were not checked for third-party marks at full resolution.
- Pexels clips were not inspected (bot wall). The Pixabay 4925, Mixkit vertical clips and Internet Archive leads were not motion-reviewed.
- Screenshots were returned to the agent only; no frame image files are saved in this folder.
