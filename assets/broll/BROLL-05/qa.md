# BROLL-05 QA

Scout: BROLL-05 scouting worker (subagent of the B-roll Scouting Manager, vb-99). Date: 2026-09-15.
Acquisition: BROLL-05 acquisition worker (subagent of the B-roll Scouting Manager, vb-bf). Date: 2026-09-15.
Reviewer: none yet (OPS-04 review deck).

## Outcome

`production_status: produced`, `release_status: blocked`.
- One recommended candidate, now acquired: Pexels 20503026.
- One rights-blocked alternative, not acquired: Mixkit 48937.
- Five rejections: two after motion review, three on page description.
- One file downloaded, with Devin's approval on 2026-09-15: `source/pexels-20503026-stefan-floppy-insert-1920x1080.mp4`.
- R14 stays open; release stays blocked.

Sections below marked **[scouting pass]** describe the earlier pass, when nothing had been downloaded. The acquisition pass is recorded in "Acquisition pass (2026-09-15)".

## [scouting pass] Outcome as recorded before acquisition

`production_status: scouted`, `release_status: blocked`; no media downloaded.

## Acquisition pass (2026-09-15)

Devin approved this one download on 2026-09-15; the approval reached this worker through the B-roll Scouting Manager (session vb-bf). One file was fetched. No account, login, terms click-through, payment, CAPTCHA or bot-check bypass, and no watermark removal. No personal data, email address or credential was sent. Pexels served the file directly: HTTP 200, `Content-Type: video/mp4`, one redirect, no Cloudflare interstitial.

### Exact commands

Run from the worktree root. PowerShell 7 (`pwsh`) was the shell; the `curl` invocation is `curl.exe`, not the PowerShell alias.

```sh
# 1. Download (one file, generic User-Agent, no credentials)
curl -L -sS -A "Mozilla/5.0" \
  -o assets/broll/BROLL-05/source/pexels-20503026-stefan-floppy-insert-1920x1080.mp4 \
  -w 'HTTP:%{http_code}\nURL:%{url_effective}\nTYPE:%{content_type}\nBYTES:%{size_download}\nREDIRECTS:%{num_redirects}\n' \
  https://www.pexels.com/download/video/20503026/
# HTTP:200
# URL:https://videos.pexels.com/video-files/20503026/20503026-hd_1920_1080_24fps.mp4
# TYPE:video/mp4
# BYTES:7816241
# REDIRECTS:1

# 2. Real size and hash
cd assets/broll/BROLL-05
wc -c source/pexels-20503026-stefan-floppy-insert-1920x1080.mp4   # 7816241
sha256sum source/pexels-20503026-stefan-floppy-insert-1920x1080.mp4
# a4f8aefe35b79055d6e9c9eab1d278ecdbc7f98de6b8c8d708a75e45ccb5600c

# 3. ffprobe
ffprobe -v error -show_format -show_streams -print_format json \
  source/pexels-20503026-stefan-floppy-insert-1920x1080.mp4

# 4. Frame extraction (native 1920x1080)
for t in 1.5 2.2 3.0 6.0; do
  ffmpeg -v error -y -ss $t -i source/pexels-20503026-stefan-floppy-insert-1920x1080.mp4 \
    -frames:v 1 "evidence/frames/frame-$(echo $t | tr . p)s.png"
done

# 5. 720p check frame
ffmpeg -v error -y -ss 1.5 -i source/pexels-20503026-stefan-floppy-insert-1920x1080.mp4 \
  -frames:v 1 -vf scale=-2:720 evidence/frames/frame-1p5s-720p.png

# 6. Label reading aid (derived crop, not a clean frame)
ffmpeg -v error -y -ss 1.5 -i source/pexels-20503026-stefan-floppy-insert-1920x1080.mp4 \
  -frames:v 1 -vf "crop=700:500:450:280,transpose=1,scale=-2:1100" \
  evidence/frames/frame-1p5s-label-zoom.png

# 7. Audio level probe over the selected segment (no playback available)
ffmpeg -hide_banner -t 6 -i source/pexels-20503026-stefan-floppy-insert-1920x1080.mp4 \
  -af volumedetect -f null /dev/null
# mean_volume: -42.4 dB   max_volume: -3.6 dB

# 8. Structural validation
cd ../../..
python tools/validate_delivery.py --id BROLL-05
```

Frames at 0.70, 0.95, 1.85, 8.20, 8.60, 8.90, 9.30, 9.80 and 10.30 s were also extracted to a scratch directory while checking handles and the eject action. They are not part of the delivery; the four brief-specified frames, the 720p frame and the label crop are.

### ffprobe result (real values, not the page's claims)

| Field | Value |
|---|---|
| Container | `mov,mp4,m4a,3gp,3g2,mj2`, major brand `mp42` |
| Container duration | 11.156667 s |
| Video stream | h264, High profile, level 4.2, yuv420p, bt709, progressive |
| Dimensions | 1920 x 1080 |
| Frame rate | `24000/1001` = 23.976 fps |
| Video frames | 266 |
| Video stream duration | 11.093333 s |
| Video bit rate | 5 441 068 bps |
| Audio stream | **present** - AAC LC, 48 000 Hz, stereo, 189 387 bps, 11.156667 s, 523 frames |
| Container tags | `creation_time 2024-03-04T12:24:45Z`, handler "Vimeo Artax Video Handler" |
| Bytes | 7 816 241 |
| SHA-256 | `a4f8aefe35b79055d6e9c9eab1d278ecdbc7f98de6b8c8d708a75e45ccb5600c` |

### Match against the scouted candidate

Dimensions, container duration, frame rate and the served file name (`20503026-hd_1920_1080_24fps.mp4`) all match what scouting recorded from the asset page and its preview player. **No mismatch found.** Two additions scouting had not established: the file carries an audio stream, and the exact frame rate is `24000/1001` rather than the page's rounded "23.98". The video stream (11.093333 s) is marginally shorter than the container (11.156667 s) because the audio track runs slightly longer; the 0-6 s segment is unaffected.

### Manual inspection: full size and 720p

Inspected at full size (1920x1080): `evidence/frames/frame-1p5s.png`, `frame-2p2s.png`, `frame-3p0s.png`, `frame-6p0s.png`, plus the derived label crop `frame-1p5s-label-zoom.png`. Inspected at 720p (1280x720): `evidence/frames/frame-1p5s-720p.png`.

**3.5-inch media - PASS, directly observed.** At 1.5 s the disk is a rigid square translucent-red shell carrying a white factory label. At full size the label reads **"2HD"** and **"IBM"** clearly and **"1.44 MB"** less sharply; the black logo block on the label is not resolvable. The metal hub, with its centre hole and drive-pin slot, is visible as a silhouette through the translucent shell. There is no flexible sleeve, no exposed hub ring on the face and no oval head window in the shell - this is not 5.25-inch or 8-inch media, and "2HD"/"1.44" are the 3.5-inch high-density designations.

**Matching 3.5-inch drive - PASS, directly observed.** At 3.0 s and 6.0 s the drive is a bare beige 3.5-inch mechanism: a single narrow horizontal slot whose width matches the disk, a small rectangular push-button eject at the right end of the bezel, and a small indicator window at the left. No rotating latch lever or door, so not 5.25-inch. At 6.0 s the disk is fully swallowed with only a red sliver showing at the slot.

**Insertion direction - label side up confirmed directly; shutter-first still INFERRED.** Label side up is directly observed: at 1.5 s the printed label faces the camera on a drive lying flat, with the hub visible only through the shell, i.e. on the underside. The metal shutter is never in view in any frame sampled - at 0.95 s the leading edge is motion-blurred, from 1.5 s on it is already inside the slot, and during the 8.6 s withdrawal it is still inside the drive - so scouting's "inferred" label stands. Two direct observations strengthen the inference: at 2.2 s the exposed trailing edge is bare red plastic with an open square through-hole at its corner and no metal shutter, and on a 3.5-inch disk the write-protect and HD-detect holes sit on the edge opposite the shutter; and the head-window silhouette seen through the shell at 1.5 s lies on the half of the disk that enters the drive - it is absent from the trailing half exposed at 8.6 s - which puts the window, and so the shutter, on the leading edge. Nothing seen contradicts a possible insertion.

**"IBM" readable - YES.** Readable at full size at 1.5 s, and still discernible at 720p. "2HD" survives both sizes; "1.44 MB" is clear at full size and marginal at 720p. RQ3 (incidental visible trademark) therefore remains live at delivery resolution.

**Overlays.** No captions, watermark or burned-in timecode in any extracted frame.

**Handles and segment.** Drive empty with no hand at 0.70 s; disk enters about 0.95 s; seated about 3.0 s; static hold with no hand through 6.0 s. The hand returns after 6.0 s, and by 8.6 s the disk is being drawn back out; at 9.3 s the drive is empty. The 00:00.00-00:06.00 segment holds, and the eject is comfortably outside it.

### Still unverified after acquisition

- **Audio content.** No audio playback in this environment. `volumedetect` over 00:00-00:06 gives mean -42.4 dB / max -3.6 dB, so the track is not digital silence, but whether it contains speech or narration is unverified. The picture-only assumption has not been tested.
- **Metal shutter.** Still never directly seen; shutter-first remains an inference, now supported by the trailing-edge holes and the head-window silhouette.
- **Frame-accurate timing.** Frames were sampled at discrete seek points, not frame by frame. The exact frame where the hand leaves (between 3.0 and 6.0 s) and where the eject press begins (between 6.0 and 8.2 s) is bracketed, not exact.
- **Playback.** The file was probed and sampled with ffmpeg; it was not played end to end.
- **Label brand block.** The logo inside the black box on the disk label is unreadable at every size tried, so the disk's manufacturer is unknown. Only "IBM" is legible as a brand word.
- **Legal sufficiency.** Acquisition under the Pexels License is not clearance. RQ1-RQ4 stand and R14 stays open.
- **License snapshot.** Still not saved as a file; the license was read on 2026-09-15 and recorded in substance only.

## [scouting pass] What was checked and how

| Check | Method | Result |
|---|---|---|
| Search coverage | WebSearch; WebFetch of Pexels, Pixabay, Mixkit, Coverr, Videvo, Vista Create and Wikimedia Commons search pages; Internet Archive `advancedsearch.php` JSON; in-app Browser on Pexels search | Logged in `evidence/candidates.json` → `search_log` |
| Asset metadata (creator, duration, dimensions, fps, date) | WebFetch of each asset page; for the reviewed clips, cross-checked `duration`/`videoWidth`/`videoHeight` read from the page's own `<video>` element in the Browser | Pexels 20503026: 11.156667 s, 1920×1080. Pexels 20503027: 5.566667 s, 1920×1080. Mixkit 48937: 7.24 s, 1280×720 |
| Motion review | Opened each asset page in my own Browser tab (`tab-4`), paused the page's preview `<video>`, set `currentTime`, waited 2 s, screenshotted the 800×609 viewport | 20503026: 13 frames (0.1–10.9 s). 20503027: 5 frames. Mixkit 48937: 4 frames. 33125208: 3 frames during live playback (timecodes not captured) |
| Media size, drive type, insertion direction | Visual reading of those frames (details per frame in `evidence/candidates.json`) | 20503026: 3.5-inch confirmed from the "2HD"/"1.44" label and slot width; 3.5-inch-style push-button drive; label side up on a flat drive. The shutter end leading is **inferred** from the trailing-edge corner holes; the shutter itself isn't visible. 33125208: 5.25-inch, rejected. Mixkit: disk edge-on, so direction can't be verified |
| Download options and barrier | Opened the Pexels "Free download" size dropdown (no download clicked); read the Mixkit download panel text | Pexels: five sizes up to Full HD 1920x1080, no file size shown, no login or CAPTCHA seen. Mixkit: free 720p personal use only; 4K via Envato |
| License text | WebFetch of https://www.pexels.com/license/ and https://mixkit.co/llm-info/; Browser load of https://mixkit.co/license/ and the Mixkit asset page | Recorded in substance in `evidence/candidates.json`. The Mixkit Restricted License modal body didn't expose text to page-text extraction; the wording comes from the asset page and Mixkit's info page |
| Delivery structure | `python tools/validate_delivery.py --id BROLL-05` | See below |

## [scouting pass] Reproduction commands

Run from the worktree root. The output-inventory command below predates acquisition and no longer lists every delivered file; use `python tools/validate_delivery.py --id BROLL-05`, which hashes the full inventory in `delivery.json`.

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
- curl 8.18.0 (x86_64-w64-mingw32), libcurl/8.18.0, Schannel
- ffmpeg / ffprobe 6.0-essentials_build-www.gyan.dev
- PowerShell 7 (`pwsh`) on Windows 11 Pro 10.0.26200
- Claude Code in-app Browser pane (Chromium-based; version not exposed) — scouting pass only
- WebFetch and WebSearch tools — scouting pass only. WebFetch returns small-model summaries of page content.

## Proof paths

Full size (1920×1080): `evidence/frames/frame-1p5s.png`, `evidence/frames/frame-2p2s.png`, `evidence/frames/frame-3p0s.png`, `evidence/frames/frame-6p0s.png`.
720p (1280×720): `evidence/frames/frame-1p5s-720p.png`.
Derived reading aid (rotated, upscaled crop of the 1.5 s frame; not a clean frame): `evidence/frames/frame-1p5s-label-zoom.png`.
Clean original: `source/pexels-20503026-stefan-floppy-insert-1920x1080.mp4`.

Scouting-pass frame inspections were Browser screenshots that were never saved to disk; those observations remain as text in `evidence/candidates.json`.

## [scouting pass] NOT checked

Items marked *(resolved)* were settled by the acquisition pass above.

- **Downloaded file.** *(resolved)* Bytes, size, codec, audio track, frame rate and ffprobe output are now recorded from the real file.
- **Audio and narration.** Still open. The track exists and is not silence; it was not auditioned.
- **Frame-accurate timing.** Still open; sampled seek points only.
- **Metal shutter.** Still open. Not directly seen; insertion direction remains inferred, with two corroborating direct observations.
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
