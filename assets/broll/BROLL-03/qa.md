# BROLL-03 QA report

**Result:** produced. The approved rank 1 clip is acquired and verified. Release blocked; R14 open.
**Reviewer:** BROLL-03 acquisition worker (agent), 2026-09-15, building on the scouting pass of the same date. No human review yet.

**Label that must travel with this asset:** the acquired clip is a **modern 2021 retro-styled recreation, not genuine 1990s archive footage**, and its set dressing reads more 1970s–80s than 1990s.

## Part 1 — scouting (earlier pass, 2026-09-15)

| Check | Method | Result |
|---|---|---|
| Candidate metadata (creator, upload date, duration, dimensions, fps, description) | WebFetch of each Pexels asset page; cross-checked in the Claude Browser pane via `get_page_text` on 8869925 and 8869644 | Recorded in `evidence/candidates.json` |
| Player-reported duration and stream size | JS on the in-page `<video>` element (shadow-DOM search) | 8869925: 27.84 s, 2732×1440 stream. 8869644: 23.92 s, 2732×1440 stream |
| Motion / frame content, rank 1 | Seeked the Pexels in-page player to 0, 1, 4, 6, 8, 11, 12, 16, 20, 24, 27.5 s and screenshotted each | CRT prominent throughout; slow push-in then pull-back; no modern items seen in sampled frames |
| Motion / frame content, rank 2 | Seeked to 0, 4, 8, 12, 16, 20, 23.4 s and screenshotted each | Near-locked medium shot; CRT cropped left; no modern items seen |
| Rank 3 (archive) motion | Tried the Internet Archive in-page player twice | **Failed:** `NETWORK_NO_SOURCE`. Motion not reviewed |
| License and terms text | WebFetch of pexels.com/license, pexels.com/terms-of-service, pixabay license summary, CC PDM 1.0 deed, CC retired public-domain tool, help.archive.org rights page | Quoted in candidates files and claim-checks |
| Bot walls / CAPTCHA | Observed on every site visited | None encountered |

## Part 2 — acquisition and verification (this pass, 2026-09-15)

Devin approved this one download on 2026-09-15, relayed through the B-roll Scouting Manager (session vb-bf). Only the rank 1 file was downloaded; ranks 2 and 3 were not.

### Download

```
curl.exe -L -sS -A "Mozilla/5.0" \
  -o assets/broll/BROLL-03/source/pexels-8869925-mart-production-man-working-at-an-office-4096x2160-25fps.mp4 \
  -D "$env:TEMP\broll03-headers.txt" \
  -w "HTTPCODE=%{http_code} SIZE=%{size_download} URL=%{url_effective} CT=%{content_type}`n" \
  "https://www.pexels.com/download/video/8869925/"
```

Result: `HTTPCODE=200 SIZE=50508990 URL=https://videos.pexels.com/video-files/8869925/8869925-uhd_4096_2160_25fps.mp4 CT=video/mp4`.

Headers: `302 Found` from `pexels.com/download/video/8869925/` with `Location: https://videos.pexels.com/video-files/8869925/8869925-uhd_4096_2160_25fps.mp4`, then `200 OK`, `Content-Type: video/mp4`, `Content-Length: 50508990`. Cloudflare served both hops (`Server: cloudflare`, `cf-cache-status: EXPIRED` then `HIT`) but **no challenge, interstitial or bot check appeared**, so nothing had to be, or was, worked around. No account, login, cookie acceptance, payment or terms click-through. No personal data, email address or credential was sent; the only request header set was the generic User-Agent. No watermark is present in the file and none was removed.

### Size and hash

```
(Get-Item $f).Length                              -> 50508990
(Get-FileHash $f -Algorithm SHA256).Hash.ToLower() -> 7713cf4fd887bacdba027f82dc2d39323deddac57d350ea2c6e3c4a369cf3d66
```

### ffprobe

```
ffprobe -v error -show_format -show_streams -of json assets/broll/BROLL-03/source/pexels-8869925-mart-production-man-working-at-an-office-4096x2160-25fps.mp4
```

| Field | Value |
|---|---|
| Duration | 27.840000 s (696 frames) |
| Dimensions | 4096 × 2160 |
| Frame rate | 25/1 (both `r_frame_rate` and `avg_frame_rate`) |
| Video codec | h264, High profile, level 52, yuv420p, progressive, bt709 |
| Video bit rate | 14,511,194 |
| Audio | **None.** `nb_streams` is 1 and the only stream is video, so there is no narration or music to clear |
| Container | `mov,mp4,m4a,3gp,3g2,mj2`, major_brand mp42, `creation_time` 2021-07-23T06:24:59Z |

**Match against the scouted candidate: exact.** Scouting expected 4096×2160, ~27.84 s, 25 fps from MART PRODUCTION; the delivered file is precisely that, and the 2021 container creation time independently corroborates the modern-recreation finding. No mismatch to report. Two details are recorded for the first time rather than as corrections: there is no audio stream at all (scouting had listed audio as unreviewed), and the scouting note calling the desk phone "rotary" is **not** confirmed at full resolution — the dial face is not visible in any inspected frame, so this report only calls it a cream desk phone with a coiled cord.

### Frame extraction

```
ffmpeg -nostdin -v error -y -ss 1  -i <file> -frames:v 1 evidence/frames/frame-01s.png
ffmpeg -nostdin -v error -y -ss 6  -i <file> -frames:v 1 evidence/frames/frame-06s.png
ffmpeg -nostdin -v error -y -ss 11 -i <file> -frames:v 1 evidence/frames/frame-11s.png
ffmpeg -nostdin -v error -y -ss 6  -i <file> -frames:v 1 -vf "scale=-2:720" evidence/frames/frame-06s-720p.png
```

`frame-01s.png`, `frame-06s.png` and `frame-11s.png` are native 4096×2160 stills at the in point, the middle and the out point of the selected segment (in 00:01, out 00:11). `frame-06s-720p.png` is the 6 s frame scaled to 720 px height (1366×720) for the small-size check.

## What I actually saw in the frames

All three native frames were viewed at full size, and the 6 s frame was then viewed again at 720p height.

**Common to all three (full size):** a wood-panelled private office. Dark walnut wall panelling with inset square mouldings runs the full width; floor-to-ceiling vertical fabric blinds fill the right wall with blown-out daylight behind them; recessed round ceiling downlights above. The subject is a man with strawberry-blond hair, wire-rimmed round glasses, a pale blue striped dress shirt and a patterned mustard-yellow tie, seated behind a desk with a black padded edge. On the desk, left of him: a **beige/off-white CRT monitor** with a deep boxy rear casing, a stippled ventilation grille across its side panel and a small dark rectangular badge, sitting on top of a **beige horizontal desktop PC case** with a vented front and drive bay; a **beige full-size keyboard with a coiled cable** in front of it. Also on the desk: a **cream desk phone with a coiled handset cord**, thick stacks of dog-eared paper folders and documents, loose banknotes and small piles of coins, and a **bright orange mushroom-dome desk lamp** to the right. Behind and around: a pale pink metal filing cabinet or safe at frame left with a potted plant on top, a snake plant by the window, two brown leather-and-chrome cantilever chairs, a large polished wood conference table in the foreground, and parquet flooring.

**Per frame:**
- **1 s** — widest framing. Full room visible including both leather chairs and the far left dark cabinetry. The man is looking down, handling papers over the coins. The CRT is seen from its rear-left three-quarter angle, so the screen face is turned away from the camera.
- **6 s** — push-in has tightened slightly; the chairs are cropped at the edges. He has both hands at the keyboard and is looking off to his right. The CRT is larger in frame, still angled away.
- **11 s** — noticeably tighter; the desk fills the lower half and the CRT is large at frame left, now clearly showing its vented side and the PC case beneath it, with cabling visible running down. He has one hand near the keyboard and is looking to his right. The CRT screen face is still not visible to camera.

**Modern-item check (the specific ask):** across all three frames of the selected segment I saw **no flat panel, no smartphone, no laptop, no modern keyboard or mouse, and no contemporary interface overlay**. There is no on-screen content at all anywhere in the segment, because the CRT is angled away from the camera in every frame — so there is no risk of a period-wrong UI appearing. Nor is there any modern water bottle, badge lanyard, USB device or LED indicator visible. No watermark, no baked-in caption, no timecode burn-in. I did not find a modern item; I also did not check every one of the 250 frames in the segment (see "Not checked").

**Period read:** the CRT, desktop case and coiled-cable keyboard are plausible early-1990s hardware. Everything around them — the panelling, the orange mushroom lamp, the parquet, the leather-and-chrome chairs, the cream desk phone — reads 1970s–80s rather than 1990s, and certainly not 1990s US corporate. This is a staged retro set, not a real office of the period.

**720p check (`frame-06s-720p.png`, 1366×720):** the shot survives the downscale well. The CRT still reads unmistakably as a boxy period monitor on a desktop case, the keyboard and phone are still legible as period objects, and the orange lamp and wood panelling keep their character. What is lost is fine detail: the stippled vent texture on the CRT side panel flattens, the small badge on its casing becomes an indistinct dark mark, and the coins and banknotes on the desk turn into undifferentiated clutter. Nothing modern becomes visible at the smaller size, and nothing that reads as period at full size stops reading as period. No aliasing or moiré on the blinds or the vent grille. The shot works at 720p without a fallback.

## Not checked / still unverified

- **Not every frame.** The three extracted frames sit at the in point, the middle and the out point. The other ~247 frames of the 10 s segment (25 fps × 10 s = 250) were not individually inspected. The earlier scouting pass sampled the streamed preview at 0, 1, 4, 6, 8, 11, 12, 16, 20, 24 and 27.5 s and also saw nothing modern, but that was preview-resolution sampling, not a full-resolution frame-by-frame pass.
- **The rest of the clip** (11 s to 27.84 s) was not inspected in this pass beyond the scouting samples. Only the selected segment matters editorially, but the handles were not re-checked at full resolution.
- **The desk phone's dial type** is not established; the dial face is not visible in any frame inspected.
- **Motion itself** was not played back at full resolution; the push-in is inferred from the three stills plus the scouting pass's in-page playback and seeking.
- **Legal clearance.** Model release for the identifiable actor, and whether a recreation may stand in for a 1990s office at all, are review questions for OPS-04, not findings. R14 stays open.
- **Ranks 2 and 3** were not downloaded and remain as scouted. Rank 3's motion was never reviewed and its rights remain unverified.
- Internet Archive Terms of Use text: WebFetch of `archive.org/about/terms` returned only the site title.

## Reproduction

From the worktree root, with ffmpeg 6.0 and Python 3.14 on PATH:

```
curl.exe -L -A "Mozilla/5.0" -o assets/broll/BROLL-03/source/pexels-8869925-mart-production-man-working-at-an-office-4096x2160-25fps.mp4 "https://www.pexels.com/download/video/8869925/"
ffprobe -v error -show_format -show_streams -of json assets/broll/BROLL-03/source/pexels-8869925-mart-production-man-working-at-an-office-4096x2160-25fps.mp4
ffmpeg -nostdin -v error -y -ss 6 -i assets/broll/BROLL-03/source/pexels-8869925-mart-production-man-working-at-an-office-4096x2160-25fps.mp4 -frames:v 1 -vf "scale=-2:720" assets/broll/BROLL-03/evidence/frames/frame-06s-720p.png
python tools/validate_delivery.py --id BROLL-03
```

## Toolchain

- ffmpeg / ffprobe 6.0-essentials_build-www.gyan.dev (built with gcc 12.2.0, MSYS2)
- curl 8.18.0 (x86_64-w64-mingw32), libcurl/8.18.0 Schannel
- Python 3.14.0 (validator, hashing)
- PowerShell 7 `Get-FileHash` (SHA-256), `Get-Item` (byte size)
- git 2.53.0.windows.1
- Windows 11 Pro 10.0.26200
- Scouting pass only: Claude Browser pane (in-app Chromium, version not exposed), WebFetch/WebSearch

## Validator result

`python tools/validate_delivery.py --id BROLL-03` → `"ok": true`, `"errors": []` (run after final hashing on 2026-09-15). Its stated limits: no OCR or visual judgment, no MP4 decode, no legal clearance, and manual review still required. The ffprobe and frame inspection above are that separate manual check.
