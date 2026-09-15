# BROLL-01 QA report

**Workers:** BROLL-01 scouting worker (session vb-99), then BROLL-01 acquisition worker (B-roll Scouting Manager, session vb-bf). **Dates:** 2026-09-15 (scouting), 2026-09-15 (acquisition). **Reviewer:** none yet (OPS-04 review deck).
**Result:** `produced`, release `blocked`. Rank 1 candidate acquired; R14 still open.

Sections 1–2 below are the original scouting record. Section 3 is the acquisition pass.

---

# 1–2. Scouting record (unchanged)

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

## Not checked (as of the scouting pass)
- **No 1080p or 720p export inspection:** there are no rendered or acquired files. Previews were 720p streams; 1080p originals were never seen.
- **Audio/narration:** previews were played muted.
- **Continuous real-time motion:** frames were sampled at roughly 1–4 s intervals.
- 100372 frames after 10 s were captured at reduced screenshot size; detail was not assessed.
- The no-login download path was not exercised (the button was not clicked).
- The Mixkit User Terms were not read verbatim; card-back and felt designs were not checked for third-party marks at full resolution.
- Pexels clips were not inspected (bot wall). The Pixabay 4925, Mixkit vertical clips and Internet Archive leads were not motion-reviewed.
- Screenshots were returned to the agent only; no frame image files were saved in this folder during scouting. (Frames were later extracted from the acquired original — see section 3.)

---

# 3. Acquisition pass (2026-09-15)

**Authorization:** Devin approved this one download on 2026-09-15, relayed by the B-roll Scouting Manager (session vb-bf). Rank 1 only. Ranks 2 and 3 were not downloaded.

## Exact commands run

Download (the `-A "Mozilla/5.0"` User-Agent is generic; no personal data, address or credential was sent):

```
curl.exe -L -A "Mozilla/5.0" --max-time 600 -D headers.txt \
  -o assets/broll/BROLL-01/source/mixkit-100384-deck-of-cards-being-shuffled-1080p.mp4 \
  -w "HTTP_CODE=%{http_code} SIZE=%{size_download} CONTENT_TYPE=%{content_type}" \
  "https://mixkit.co/free-stock-video/download/100384/?context=sidebar&type=1080p"
```

That returned **HTTP 200, `Content-Type: text/html`, 2738 bytes** — not video. The body is the Mixkit download-modal fragment headed "Your download has started", carrying
`data-download--modal-url-value="https://assets.mixkit.co/active_storage/video_items/100384/1723577320/100384-video-1080.mp4"`.
No login form, payment step, CAPTCHA, bot check or terms-acceptance control appeared, and none was bypassed: the modal is the page's own download mechanism and it names the file for the same item and the same 1080p option. The bytes were then fetched from that named URL:

```
curl.exe -L -A "Mozilla/5.0" --max-time 600 -D headers2.txt \
  -o assets/broll/BROLL-01/source/mixkit-100384-deck-of-cards-being-shuffled-1080p.mp4 \
  "https://assets.mixkit.co/active_storage/video_items/100384/1723577320/100384-video-1080.mp4"
```
→ `HTTP_CODE=200  SIZE=73935932  CONTENT_TYPE=video/mp4  REDIRECTS=0`

Size and hash:

```
(Get-Item $v).Length                               -> 73935932
(Get-FileHash $v -Algorithm SHA256).Hash.ToLower()  -> 65b65dd09d9fcb074304b9e33123aaa6d4dd0da2906833a36c2b0c8727f73ff2
```

Probe:

```
ffprobe -v error -show_entries format=format_name,duration,size,bit_rate -show_streams -of json $v
```

Frame extraction:

```
ffmpeg -y -v error -ss 5.0  -i $v -frames:v 1 evidence/frames/frame-in-05.000s.png
ffmpeg -y -v error -ss 10.5 -i $v -frames:v 1 evidence/frames/frame-mid-10.500s.png
ffmpeg -y -v error -ss 16.0 -i $v -frames:v 1 evidence/frames/frame-out-16.000s.png
ffmpeg -y -v error -ss 5.0  -i $v -frames:v 1 -vf scale=-2:720 evidence/frames/frame-in-05.000s-720p.png
```

A throwaway crop (written to the scratchpad, not committed) was used to read the felt lettering at the out point:
`ffmpeg -y -ss 16.0 -i $v -frames:v 1 -vf "crop=560:340:1360:420,scale=1120:680" felt-text-crop.png`

## ffprobe results (actual)

| Property | Value |
|---|---|
| Container | mov,mp4,m4a,3gp,3g2,mj2 |
| Duration | **19.394375 s** |
| Size | **73,935,932 bytes** (70.51 MiB) |
| Overall bit rate | 30,497,886 |
| Video codec | h264 (High, level 41), `Lavc59.37.100 libx264` |
| Dimensions | **1920x1080**, SAR 1:1, DAR 16:9 |
| Pixel format | yuv420p, bt709 primaries/transfer/space, tv range, progressive |
| Frame rate | **24000/1001 = 23.976 fps** (both r_frame_rate and avg_frame_rate) |
| Frame count | 465 |
| Audio | **none — no audio stream in the file** |

## Match against the scouted candidate and the expected values

| Expected (scouting / handoff) | Actual | Verdict |
|---|---|---|
| ~70.51 MB | 73,935,932 B = 70.51 MiB | match |
| 1920x1080 | 1920x1080 | match |
| ~19.4 s | 19.394375 s — identical to the scouted preview duration 19.394375 | match |
| 24 fps | **23.976 fps (24000/1001)** | **mismatch** |
| Content = the shuffle clip scouted | frames at 5.0/10.5/16.0 s match the scouted frame log | match |
| Watermark | none | match |
| Audio | "not checked" | settled: no audio stream |

The only numeric mismatch is frame rate: the asset page and the scouting record both say 24 fps; the delivered file is 23.976 fps. The duration matching the scouted preview to the microsecond confirms this is the same clip, not a different encode. 23.976 vs 24 matters only for conform at the edit stage; the project's 30 fps render target means this clip will be conformed regardless.

## Manual inspection — what I actually saw

All three full-resolution PNGs were viewed at full size, and the in-point frame was viewed again at 720p height.

- **`frame-in-05.000s.png` (1920x1080, in point).** The deck is cut into two packets lying on green felt, each gripped at its outer corner by a hand entering from the left and right edges — exactly the "packets separated, corners lifted ready to riffle" state the scouting log recorded at 5.0 s. Card backs are a bold abstract black-and-white geometric pattern; no brand, maker's mark or legible text on them. **Casino layout: present** — a large yellow "10" across the top edge (upside down, reading toward the dealer), a grey curved arc, and white betting lines crossing the lower third. Hands only, no face, no chips. No watermark, caption, logo or bug anywhere in frame.
- **`frame-mid-10.500s.png` (1920x1080, mid point).** The riffle is complete and the two packets are interleaved into a single block, fingers of both hands squaring it. Focus is sharp on the cards, the felt falls slightly soft. Same yellow "10" and white lines. No watermark.
- **`frame-out-16.000s.png` (1920x1080, out point).** The bridge: the interleaved deck arched under both sets of fingertips, mid-cascade, with visible motion blur on the springing cards — a natural, clean place to cut. **New detail not in the scouting record:** partial white upside-down lettering "...EX..." enters at the right edge of frame. Zoomed to roughly 2x, it is a clean sans-serif "EX" with a boxed white rule below it, consistent with a **"TEXAS HOLD'EM"** table layout. No casino name, brand or logo is legible. Scouting had noted felt lettering only at 19.1 s, i.e. outside the cut; it is in fact **inside** the selected segment.
- **`frame-in-05.000s-720p.png` (1280x720, 720p check).** Everything that carries the shot survives the downscale: the split packets, the geometric card backs, the individual card edges in each packet, the hands, and the yellow "10". The card-back pattern stays crisp rather than shimmering. Nothing in the shot depends on 1080p detail, so the clip reads correctly at 720p delivery.

**Segment in/out:** 5.0 s → 16.0 s still holds on the real file. 5.0 s lands on a settled pre-riffle state and 16.0 s on the arched bridge, giving 11.0 s of continuous riffle-then-bridge action with 5.0 s head and 3.394375 s tail handles. The one caveat is editorial, not technical: the "TEXAS HOLD'EM" felt lettering becomes visible near the out point, so an editor wanting less casino flavour could pull the out to about 14.5 s and still keep a usable 9.5 s.

## Acquisition tool versions
- curl 8.18.0 (x86_64-w64-mingw32), libcurl/8.18.0, Schannel, release 2026-01-07
- ffprobe / ffmpeg version 6.0-essentials_build-www.gyan.dev (gcc 12.2.0, MSYS2)
- Python 3.14.0
- git 2.53.0.windows.1

## Still unverified after acquisition
- **Continuous playback was never watched.** Evidence is four extracted stills plus ffprobe metadata. Judder, dropped frames, speed ramps, exposure shifts and focus pulls between the sampled points are unassessed. The file was not played end to end.
- **Only 3 of 465 frames were inspected visually.** Frames outside 5.0 / 10.5 / 16.0 s (including the whole 0–5 s head and the 16–19.4 s tail) were not viewed at any resolution in this pass.
- **Rights are recorded, not cleared.** R14 stays `open`; release stays `blocked` for the OPS-04 deck.
- **Mixkit User Terms still not read verbatim** — the s.13 third-party-component limit is known only from a WebFetch summary.
- **Card-back and felt designs**: no brand or mark was found at full resolution in the three inspected frames, but that is an absence of evidence across three frames, not a clearance.
- The Full HD option was not compared against the HD Ready option; only the 1080p file was fetched.
- Ranks 2 and 3 remain un-acquired and un-probed; Pexels leads remain uninspected (bot wall, not bypassed).
