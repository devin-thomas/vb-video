# BROLL-06 QA report

- **Ticket:** BROLL-06, Pentium-era PC booting (scout)
- **Worker:** BROLL-06 worker subagent, spawned by the B-roll Scouting Manager (session vb-99)
- **Date:** 2026-09-15 (initial pass, a motion-review rework pass, then an acquisition pass)
- **Result:** `produced`. The approved Pexels clip was downloaded and verified against the real file. Release `blocked`. R14 open.
- **Reviewer:** none yet (goes to the OPS-04 review deck)
- **Label that binds every use of this clip:** it is a **period-setting cutaway only**. It shows a beige CRT with a blank screen in a dim room. It is **not a boot and not a power-on**, and **no CPU, model or date identifies a Pentium**. Never label it a boot; never caption or imply "Pentium".

## What was checked, and how
1. **Ticket inputs.** Read `docs/tickets/BROLL-06.md`, `AGENTS.md`, `docs/roles/PRODUCER.md` (Operating model), `docs/OUTPUT_CONTRACT.md`, `docs/EDITORIAL_REGISTER.md` R14, `docs/handoffs/H02.md` and the manifest row. Source excerpts were copied verbatim from `sources/ASSET_PLAN.md:109–122` and `sources/SCRIPT.md:799–805`, with file SHA-256s recorded.
2. **Search.** Searched free stock sites and public archives. WebFetch was used for page retrieval; it returns a small-model summary of each page, so the result counts below are as reported by that tool, not hand-counted. Results:

| Site | Query / category | Reported results | Relevant |
|---|---|---|---|
| Pexels | windows 95 (videos) | 9 listed | none |
| Pexels | old computer boot | 10 | none show boot |
| Pexels | retro computer | 10 | none |
| Pexels | crt monitor turning on | 13 | none (TV static, CRT UI) |
| Pexels | computer turning on | 9 | none (laptops) |
| Pexels | 90s computer | 12 | 8888818 (set shot) |
| Pexels | vintage computer | 24 | 8888818; no boot |
| Pixabay | old computer | 97 on page 1 | none |
| Pixabay | computer boot | 50 on page 1 of 16 | none |
| Pixabay | retro computer | 100 | none show boot |
| Pixabay | bios | 46 | none |
| Pixabay | pc turning on | 50 on page 1 of 10 | 126935 (rejected after viewing) |
| Pixabay | windows 95 | 50 on page 1 of 15 | none |
| Mixkit | computer category | 24 | none |
| Coverr | old computer | 7 | none |
| Videvo | old computer boot | HTTP 403 | not inspected |
| Vecteezy | free-videos/old-computer-screen | 3 flagged | simulated animations only |
| Commons MediaSearch (video) | boot BIOS POST | 1 | BIOS_POST_IMGP9357_wp.ogv |
| Commons | Windows 95 startup / Pentium boot / MS-DOS boot / IBM PC startup / memory test BIOS | 0 each | — |
| Commons | 486 computer | 3 | none |
| Commons | booting computer | 6 | none period x86 |
| Commons | retro computer / POST screen / CRT computer / Award OR Phoenix OR AMI BIOS | 7 / 7 shown (320 total) / 8 / 24 | none |
| Commons categories | Booting; Boot screens; Microsoft Windows boot screens; BIOS POST cards | — | only POST-card videos (2); Windows boot screens are stills plus Win10 animations |
| Internet Archive advancedsearch | (pentium OR "windows 95") AND boot, movies | 39 | YouTube mirrors only |
| Internet Archive | boot terms AND era terms AND CC licenseurl | 38 | Win95 startup capture (rejected) |
| Internet Archive | power-on terms AND era terms | 12 | LGR AST Advantage 622 mirror (H02) |

3. **Page inspection.** For every candidate and lead:
   - Loaded the asset page and recorded creator, duration, dimensions, fps, date, description and download label.
   - Loaded the license page and recorded its terms.
   - For Commons, also read the API `imageinfo`/`extmetadata` response.

## Motion review (rework pass, 2026-09-15)
- **Environment.** `tabs_context` showed four tabs. I reused my own `tab-6` (no new tab) and closed it at the end.
  - The Browser pane was still reported hidden, but screenshots now succeeded at scale 0.5–0.8.
  - Region crop via `zoom` is not supported in the pane; full screenshots were used instead.
  - Clips were played in-page only. No file was saved.
- **Pixabay 126935: rejected.**
  - The page initially exposed no `<video>`; clicking the player area loaded it.
  - JavaScript read: `duration` 13.12, `videoWidth×videoHeight` 3840×2160, `readyState` 4.
  - Setting `currentTime` did not seek on this player (it stayed at 0), so I played muted in real time and screenshotted at t≈0, 2.97, 6.43, 9.48 and 12.53 s (plus 8.72 s while paused).
  - The frames show a modern black flat-panel monitor bezel: a blue LED comes on, the panel backlight glows blue, a fingertip presses a button, then everything goes off. There is no PC, CRT or boot.
- **Commons BIOS_POST_IMGP9357_wp.ogv: rank 2.**
  - Played on the file page through the lightbox player (240p VP9 transcode).
  - JavaScript read: `duration` 35.014, 370×240, `readyState` 4.
  - Screenshots at poster (0), 2.13, 6.18, 10.23 and 15.28 s show a static close-up of the POST card's four-digit yellow seven-segment display going dark and then showing changing codes.
  - In/out set to 2.0–12.0 s.
- **Pexels 8888818: rank 1.**
  - No Cloudflare check appeared, and page title and body were normal.
  - The first playback attempt played a related-clip preview (8889183) in "More like this", so I disregarded it.
  - After scrolling to the top, the main player turned out to be a `<mux-player>` with source `8888818-uhd_2732_1440_25fps.mp4`. JavaScript read: `duration` 11.8, 2732×1440, `readyState` 4.
  - Played muted, with screenshots at t=0, 3.03, 6.35 and 9.42 s; the player reset to 0 at the end.
  - The frames show a slow camera drift in a dim room with a beige CRT on a desk. The screen is blank or grey, with no power-on and no boot text.
  - In/out set to 0.5–10.5 s.
- **Scale of inspection.** Frames were viewed at in-page preview size. Full-resolution (1080p) and 720p inspection of the actual files was not possible because no media is acquired. Digits on the POST card were read from a 240p preview and are approximate.

## Acquisition pass (2026-09-15)

Devin approved one download: Pexels 8888818. The Wikimedia Commons BIOS POST clip was **not** approved and was **not** downloaded. Nothing else was fetched.

### 1. Download — exact command

```
curl.exe -L -sS -A "Mozilla/5.0" -D "$env:TEMP\broll06_headers.txt" \
  -o "assets/broll/BROLL-06/source/pexels-8888818-mart-production-vintage-computer.mp4" \
  "https://www.pexels.com/download/video/8888818/"
```

- Exit code 0.
- `HTTP/1.1 302 Found`, `Location: https://videos.pexels.com/video-files/8888818/8888818-uhd_4096_2160_25fps.mp4`, then `HTTP/1.1 200 OK`, `Content-Type: video/mp4`, `Content-Length: 29243915`, `Content-Disposition: attachment`, `last-modified: Tue, 26 Mar 2024 22:38:13 GMT`.
- **No Cloudflare check appeared, and nothing was bypassed.** No login, account, payment, terms click-through or CAPTCHA was involved. A generic `Mozilla/5.0` User-Agent was used; no personal data, email address or credential was sent.
- The `download/video/8888818/` endpoint resolved to the **4096x2160** rendition, not the 2732x1440 preview seen in the in-page player during scouting.

### 2. Real byte size and hash

```
(Get-Item $f).Length                                  -> 29243915
(Get-FileHash $f -Algorithm SHA256).Hash.ToLower()    -> 5aa6828fb8a25cc46c24a0d8229f0f1e9db6c1fb7cab7df8aa68563543107f0f
```

29,243,915 bytes (27.9 MiB), matching the HTTP `Content-Length` exactly. Well under the 500 MB stop threshold.

### 3. ffprobe — exact command and real values

```
ffprobe -v error -show_format -show_streams -print_format json \
  assets/broll/BROLL-06/source/pexels-8888818-mart-production-vintage-computer.mp4
```

| Field | Real value |
|---|---|
| Duration | 11.800000 s (295 frames) |
| Width x height | **4096 x 2160** |
| Frame rate | 25 fps (`r_frame_rate` and `avg_frame_rate` both `25/1`) |
| Video codec | h264, High profile, level 5.2, yuv420p, progressive, bt709 |
| Video bit rate | 19,823,275 bps |
| Container | mov,mp4,m4a,3gp,3g2,mj2 (major_brand mp42) |
| Audio stream | **none** — `nb_streams` is 1; the file carries a video stream only |
| Container creation_time tag | 2021-07-24T12:04:16.000000Z |

**Real resolution versus the page's claim:** the page said 4096x2160, 25 fps, about 12 s. The real file **is 4096x2160 at 25 fps**, with a measured duration of 11.8 s. The claim holds. The 2732x1440 figure recorded during scouting was the in-page player's preview rendition and is not the delivered file.

### 4. Frame extraction — exact commands

```
ffmpeg -v error -y -ss 0.5  -i <file> -frames:v 1 evidence/frames/frame-t0p5s.png
ffmpeg -v error -y -ss 5    -i <file> -frames:v 1 evidence/frames/frame-t5s.png
ffmpeg -v error -y -ss 10.5 -i <file> -frames:v 1 evidence/frames/frame-t10p5s.png
ffmpeg -v error -y -ss 5    -i <file> -frames:v 1 -vf "scale=-2:720" evidence/frames/frame-t5s-720p.png
```

The first three are native 4096x2160 PNGs; the fourth is 1366x720 for the 720p check.

### 5. What I actually saw at full size (4096x2160)

All three frames were opened and viewed at native resolution.

- **t = 0.5 s.** A dim room with warm pink/amber light on the left wall and a green cast on the right. A dark wooden desk on metal legs runs across the frame. On it: a beige CRT monitor with a beige keyboard in front of it, a pink rotary telephone, a folding bellows camera, a glass flask, a foil-wrapped object, and a stack of coloured booklets. A green metal chair back is in the left foreground; a pale pendant lamp hangs at top centre; a poster is taped to the wall at top right; wall sockets and cables are visible at floor level. **The CRT screen is blank and dark — an unlit grey/black rectangle. No text, no logo, no cursor, no glow.**
- **t = 5 s.** Same set; the camera has drifted so the desk sits slightly right and the chair moved left. Screen still blank and dark.
- **t = 10.5 s.** Drift continues; the monitor now sits centre-left and more of the right wall is visible. Screen still blank and dark.

**Boot or power-on: no.** Across the whole selected 0.5–10.5 s range the screen never lights, never flickers, and never shows POST text, a memory count, a BIOS screen or any OS. Nobody touches the machine. The only motion is the slow camera drift. **There is no PC case, tower or desktop chassis anywhere in frame at any of the three times** — only a monitor and a keyboard — so there is no CPU to see.

**Hardware marking or date legible now that I have the full-resolution file:** yes, partly, and it is not what the ticket wanted. I cropped the bezel at native resolution (`crop=500:120:1870:1370` and `crop=760:90:1880:840` with a brightness/contrast lift, into the scratchpad only — not committed) and read:

- **"ViewSonic"** as a wordmark on the lower bezel, plus the ViewSonic three-bird logo on the upper-left bezel.
- **"E70"** as a model marking on the upper-right bezel, under a small sports-car sticker.

This is a **monitor** make and model. It is **not** a CPU, not a system identification and **not a date**. It does nothing to support "Pentium-era" and must not be read as doing so. No serial, no manufacture date, no BIOS string and no OS marking is legible anywhere in the frame. Two audio cassettes rest on top of the monitor; their labels are not readable.

No watermark, baked-in caption or burned-in text appears in any frame. Nothing was removed from the file; the original is preserved byte-identical as downloaded.

### 6. What I saw at 720p

`frame-t5s-720p.png` (1366x720) was viewed at full size. The composition reads clearly: room, desk, beige CRT, keyboard, chair, lamp, poster. The screen is unmistakably dark and blank, so the "not a boot" reading survives the downscale. **Neither the "ViewSonic" wordmark nor "E70" is legible at 720p** — the wordmark is a faint smudge on the bezel and the model marking is indistinguishable from the sticker beside it. The shot holds up as a period-setting cutaway at 720p.

### 7. Still unverified after acquisition

- **CPU: unverified, and unverifiable from this clip.** No PC case is in shot.
- **Date: unverified.** No date, serial or manufacture marking is legible. "Period" rests on the visual style of the monitor, keyboard and props, not on evidence.
- **The clip is not a boot.** This is now confirmed on the real file, not merely assumed.
- Whether the ViewSonic E70 model dates to the Pentium era was **not** researched; no claim is made either way, and it would identify a monitor rather than a machine regardless.
- Only frames at 0.5 s, 5 s and 10.5 s were extracted and inspected. The intervening frames were not examined individually, though the clip is one continuous drift with no cut.
- Legal sufficiency of the Pexels License for the final video (R14 review questions) — recorded, not adjudicated.
- Everything listed under "Not checked / not verified" below still stands for the candidates that were **not** acquired.

## Earlier pass (for the record)
In the initial pass, screenshots timed out ("Browser pane is not displayed") and no frames were viewed. Later Pexels navigations then showed a Cloudflare "Performing security verification" page. I stopped at that point and did not bypass it.

## Not checked / not verified (scouting-pass list, superseded where the acquisition pass above says so)
- CPU, model, BIOS date or OS for either free candidate. Nothing readable is on screen at preview size. *(Still true for the CPU and the date on the acquired clip; see the acquisition pass for what full resolution did and did not reveal.)*
- ~~Full-resolution frames for Pexels~~ — **done in the acquisition pass**: the 4096×2160 original was acquired and inspected. For Commons, the 640×416 original was not viewed (240p played) and the clip was not acquired.
- ~~Pexels file size~~ — **now known: 29,243,915 bytes.** The full rendition list was still not enumerated; the download endpoint served the 4096×2160 file. Commons fps remains unknown.
- The YouTube license fields for PwRR7-P-8fc and WCdDKPonXXA; the WCdDKPonXXA watch page was not loaded. The duration, dimensions and hardware of PwRR7-P-8fc. The "Pentium MMX 200" claim came only from a web-search summary.
- The GFDL 1.2 page for the Commons clip (listed on the file page; not loaded).
- Legal sufficiency of any license for the final video (review questions).
- ~~No media was downloaded.~~ **One approved file was downloaded in the acquisition pass** (Pexels 8888818). No other media was downloaded. No accounts, logins, CAPTCHA, Cloudflare bypass, terms acceptance or payments were involved at any point.

## Reproduction
From the worktree root:

```
git switch ticket/BROLL-06-media
python tools/validate_delivery.py --id BROLL-06

# re-acquire and re-verify the approved clip
curl.exe -L -A "Mozilla/5.0" -o assets/broll/BROLL-06/source/pexels-8888818-mart-production-vintage-computer.mp4 https://www.pexels.com/download/video/8888818/
ffprobe -v error -show_format -show_streams -print_format json assets/broll/BROLL-06/source/pexels-8888818-mart-production-vintage-computer.mp4

python -c "import hashlib,pathlib;b=pathlib.Path('assets/broll/BROLL-06');[print(p.relative_to(b).as_posix(),p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(b.rglob('*')) if p.is_file() and p.name not in ('delivery.json','state.json')]"
```

To re-check motion:
1. Open each asset page in a browser.
2. Play the in-page player and pause at the in/out points listed in `evidence/candidates.json`.
3. On Pexels, use the top `<mux-player>`, not the related-clip previews.

The Commons metadata can be re-read with:

```
https://commons.wikimedia.org/w/api.php?action=query&titles=File:BIOS_POST_IMGP9357_wp.ogv&prop=imageinfo&iiprop=url|size|mime|extmetadata|user|timestamp&format=json
```

## Tool versions
- Python 3.14.0
- git 2.53.0.windows.1
- Claude Code WebFetch / WebSearch tools (no version exposed)
- Claude Browser in-app tab tools: javascript_tool, computer screenshot (no version exposed)
- curl 8.18.0 (x86_64-w64-mingw32), libcurl/8.18.0 Schannel
- ffprobe 6.0-essentials_build-www.gyan.dev (built with gcc 12.2.0, MSYS2)
- ffmpeg 6.0-essentials_build-www.gyan.dev (built with gcc 12.2.0, MSYS2)
- No renderer or encoder was used to author anything; ffmpeg was used only to extract frames from the acquired file.

## Proof paths
- `source/pexels-8888818-mart-production-vintage-computer.mp4` — the acquired original, byte-identical as downloaded.
- `source/source.json` — full source record: creator, URLs, access date, license, hash, size, ffprobe values, cutaway label.
- `evidence/frames/frame-t0p5s.png`, `frame-t5s.png`, `frame-t10p5s.png` — full-size 4096×2160 inspection frames at 0.5 s, 5 s and 10.5 s.
- `evidence/frames/frame-t5s-720p.png` — the 720p (1366×720) inspection frame.
- Bezel crops used to read the "ViewSonic" and "E70" markings were written to the session scratchpad only and are deliberately not committed; the commands are in the acquisition pass above and reproduce them from the committed original.
- Scouting-pass browser screenshots were viewed in-session only and not written to disk. `exports/candidates.md` and `exports/acquisition-handoff.md` are text.
