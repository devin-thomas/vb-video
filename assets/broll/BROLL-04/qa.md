# BROLL-04 QA record

**Date:** 2026-09-15. **Workers:** Claude, scouting pass (branch `ticket/BROLL-04`); Claude, acquisition pass (branch `ticket/BROLL-04-media`). **Reviewer:** none yet (review deck, OPS-04).
**Production status:** produced. **Release status:** blocked (R14 open).

Part 1 below is the original scouting record and is left as written. **Part 2 is the acquisition and media QA pass**, which supersedes the scouting pass wherever they disagree (in particular the out point and the "no media downloaded" statements).

# Part 1 — scouting record (2026-09-15)

## What was checked and how

1. **Free stock search.**
   - Pexels was opened in the Claude Browser: `software store` (5.7K videos), `computer store` (landscape) and `retro computer store`. Result links were extracted with page JavaScript.
   - Pixabay, Mixkit, Coverr and Videvo were queried with WebFetch.
   - Result: no genuine 1990s software store clip. Modern store clips (e.g. Pexels face-mask store clips 5699957/5699952/5699969/5699968) were rejected as period misrepresentation.
   - Videvo returned HTTP 403. Pixabay's `retro computer store` result extraction timed out.
2. **Public archives.**
   - Internet Archive advanced-search API: 15 queries; counts are in `exports/candidates.md`.
   - Internet Archive metadata API for four items.
   - Wikimedia Commons search API: several queries; some rate-limited with HTTP 429, and those are recorded.
   - Portal to Texas History: OAI record and IIIF manifest.
3. **Rights and terms.**
   - The license and rights text shown on each item page or metadata record was recorded.
   - Also read: the CC0 deed, the Internet Archive rights help page, the rightsstatements.org InC definition, and the UNT KXAS FAQ and research FAQ (licensing rate).
   - Original YouTube uploader identity was checked through YouTube oEmbed JSON. It confirms author names only; the YouTube license line was **not** read, because WebFetch of the watch pages returned only the footer.
4. **Motion review, in-page, no files saved.**
   - Tools: Claude Browser tab `tab-5`, the `archive.org/embed/<identifier>` player, and a short page script that pauses the `<video>` element, sets `currentTime` and waits for `seeked`. A screenshot was taken at each point, with viewport emulated at 854×560.
   - Candidate 1 was sampled at 24 timestamps, including the proposed in point 00:02:16.0 and bracketing frames 00:02:23.5 and 00:02:25.5 around the out point 00:02:24.0.
   - Candidate 2, part 1: 15 timestamps, including the in point 00:10:43 and the out point 00:10:53. Part 3: 3 timestamps.
   - Screenshots were viewed in-session only and not saved to the repository.
   - Several screenshots failed with "Browser pane is not displayed, so the page is not compositing frames". Those frames were retaken after fronting the tab; any failed frame is omitted from the frame lists in `evidence/candidates.json`.
5. **Access boundaries hit.**
   - UNT viewer `https://texashistory.unt.edu/ark:/67531/metadc2152255/m1/` showed a CAPTCHA ("Validating your request… I'm not a robot"). Stopped.
   - Pond5 item page returned HTTP 403 with a captcha marker to both WebFetch and curl. Stopped.
   - No login, terms acceptance, payment or download occurred.

## Reproduction commands

Run from any shell with curl and Python 3. These fetch **metadata only**, not media.

```sh
# IA search (example; repeat with each query listed in exports/candidates.md)
curl -s "https://archive.org/advancedsearch.php?q=%28%22windows%2095%22%20AND%20launch%29%20AND%20mediatype%3Amovies&fl[]=identifier&fl[]=title&fl[]=year&fl[]=licenseurl&rows=40&output=json"
# IA item metadata (files, sizes, durations, dimensions, license, creator, uploader, originalurl)
curl -s "https://archive.org/metadata/1995.08.23-windows-95-midnight-madness-norwalk-ct-wg-g-7-klymsg-0-854x-480"
curl -s "https://archive.org/metadata/comp-usa-windows-95-launch-pt-1-of-3"
# YouTube original author check
curl -s "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=WgG7KLymsg0&format=json"
curl -s "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=rjwidy5VEGw&format=json"
# UNT KXAS rights record
curl -s "https://texashistory.unt.edu/oai/?verb=GetRecord&metadataPrefix=untl&identifier=info:ark/67531/metadc2152255"
# Commons (rate-limited; space requests out)
curl -s -A "BROLL04Scout/1.0 research" "https://commons.wikimedia.org/w/api.php?action=query&list=search&srnamespace=6&srlimit=20&format=json&srsearch=computer%20store%20filetype%3Avideo"
# Delivery structure check
python tools/validate_delivery.py --id BROLL-04
```

**Motion review reproduction:**
1. Open `https://archive.org/embed/<identifier>` and click play.
2. In the page console, find the `video` element (searching shadow roots if needed), then run `v.pause(); v.currentTime = 136;` and view the frame. Repeat for each timestamp listed in `evidence/candidates.json`.
3. For part 3 of candidate 2, set `v.src` to `https://archive.org/download/comp-usa-windows-95-launch-pt-1-of-3/CompUSA%20Windows%2095%20Launch%20pt3%20of%203.ia.mp4`.

## Tool versions

- curl 8.18.0 (x86_64-w64-mingw32)
- Python 3.14.0
- git 2.53.0.windows.1
- Claude Browser pane (Claude desktop app built-in browser; version not exposed)
- WebFetch / WebSearch (Claude Code built-in tools)
- ffprobe is installed locally (ffmpeg-6.0 essentials build) but **was not run**, because no media was downloaded.

## Results

- `python tools/validate_delivery.py --id BROLL-04`: see the validator output in the worker report. It checks structure and hashes only.
- At least one candidate was actually inspected: **yes** (candidates 1 and 2, in-page sampled motion).
- Timecodes and fit notes are shot-specific: **yes**.
- Every rights and download restriction is stated: **yes**, including the uploader-asserted CC0 caveat, the KXAS license and CAPTCHA, and the YouTube-hosted leads.
- Scouting versus acquisition: **kept distinct**. No `source/` media exists; the handoff lists pending downloads only.

## Not checked

- Continuous real-time playback of the chosen segments. Motion was judged from frame samples spaced about 0.5–3 s apart.
- The exact out point frame 00:02:24.0 (candidate 1): bracketed only.
- Audio: not auditioned for narration, music or speech.
- fps, codec and exact frame dimensions of the original files (not probed; no download).
- Candidate 2 part 2, and most of parts 1 and 3.
- The KXAS 1993 clip content (CAPTCHA), and the Pond5 item (403).
- The YouTube license line on the creators' original uploads.
- Independent verification of depicted dates beyond the page statements and on-screen Windows 95 launch material.
- Full-size (1080p) and 720p export inspection: not applicable. This scout produces no image or video exports, only the markdown report, and no acquired media exists to inspect.
- Legal clearance, fair use and privacy judgments: handed to review questions in `evidence/claim-checks.json`.

---

# Part 2 — acquisition and media QA (2026-09-15, branch `ticket/BROLL-04-media`)

**Scope of this pass:** download the one approved file, verify it is what the item page promised, inspect the selected segment against the real frames, and take the ticket to `produced`. Release stays `blocked`; R14 stays `open`.

## Authorisation and rights, recorded exactly

Devin approved this single download on 2026-09-15 and ruled that the uploader-applied CC0 is accepted as-is, so filmmaker permission will not be pursued. The rights record, as written in `source/source.json`, `evidence/provenance.json`, `evidence/claim-checks.json` and `delivery.json`, is:

> The Internet Archive item page states CC0 1.0 Universal. That CC0 dedication was applied by the Internet Archive uploader "The Nostalgist777", not by the filmmaker Dan Lynch. Devin accepted that uploader-applied CC0 as-is on 2026-09-15 and ruled that filmmaker permission will not be pursued.

The filmmaker has **not** licensed this footage and was not contacted. Nothing in this package says otherwise. R14 stays open because the residual risk (Creative Commons does not verify the copyright status of CC0-tagged works; the Internet Archive does not guarantee item copyright status) and the recognizable-people question remain for the OPS-04 review deck.

## Download

One file only. No account, login, payment, terms click-through, CAPTCHA or bot check was involved, and no personal data, email address or credential was sent. The only header set was a generic browser User-Agent.

```powershell
curl.exe -L -A "Mozilla/5.0" --fail -s -S `
  -o "assets/broll/BROLL-04/source/1995-08-23_compusa-norwalk_dan-lynch_original.mp4" `
  "https://archive.org/download/1995.08.23-windows-95-midnight-madness-norwalk-ct-wg-g-7-klymsg-0-854x-480/1995.08.23-Windows95-Midnight-Madness-NorwalkCT%5BWgG7KLymsg0%5D%5B854x480%5D.mp4"
```

The exact remote file name came from the item metadata API (the `/download/<identifier>/` HTML listing renders its file table client-side, so the file names were read from the API instead):

```powershell
curl.exe -s -A "Mozilla/5.0" "https://archive.org/metadata/1995.08.23-windows-95-midnight-madness-norwalk-ct-wg-g-7-klymsg-0-854x-480"
```

The file taken is the one with IA `source: original` and format `MPEG4`, not the `.ia.mp4` H.264 derivative that the in-page player streams.

**The raw IA metadata JSON was deliberately not committed to the repo**: it carries the uploader's personal email address in its `uploader` field. The uploader is recorded here and in the JSON files only by the display name shown on the item page.

## Integrity check

```powershell
(Get-Item $f).Length                                  # 32302815
(Get-FileHash $f -Algorithm SHA256).Hash.ToLower()
(Get-FileHash $f -Algorithm MD5).Hash.ToLower()
(Get-FileHash $f -Algorithm SHA1).Hash.ToLower()
```

| Value | Local file | Published by IA metadata API | Match |
|---|---|---|---|
| bytes | 32,302,815 | 32,302,815 | yes (equals the expected size in the assignment) |
| sha1 | `f79a200eeee5964ef6bcbfb714f5d209595168a4` | `f79a200eeee5964ef6bcbfb714f5d209595168a4` | yes |
| md5 | `5af84982f1399c06989acd79403395fb` | `5af84982f1399c06989acd79403395fb` | yes |
| sha256 | `f6d309c70d1eccbc9e3af3ba124bf123724e0427dca83789635e74310baeccb6` | not published by IA | recorded for this pack |

The download is byte-identical to the published original.

## ffprobe

```powershell
ffprobe -v error -show_format -show_streams -print_format json "assets/broll/BROLL-04/source/1995-08-23_compusa-norwalk_dan-lynch_original.mp4"
```

Actual values:

- Container `mov,mp4,m4a,3gp,3g2,mj2`, duration **230.621 s** (page and metadata said 230.62 s — matches).
- Video stream 0: **h264** (Main profile), **854x480**, SAR 1:1, DAR 427:240, yuv420p, **`r_frame_rate` 30000/1001 = 29.97 fps**, 6911 frames, stream duration 230.597033 s, 979,135 bit/s, progressive, bt709.
- Audio stream 1: **present** — **opus**, 48 kHz, 2 channels (stereo), 119,670 bit/s, 230.621 s. Contents not auditioned.
- Stream 2: a 640x480 **PNG cover-art still** with `attached_pic` disposition (a thumbnail carried in the container, not picture content). Because of it, `-map 0:v:0` must be given explicitly to ffmpeg or it may pick the still.
- Container tags name `artist: Dan Lynch` and `comment: https://www.youtube.com/watch?v=WgG7KLymsg0`, corroborating the filmmaker attribution on the item page. The container `date` is `20231015`, an encode/upload date, **not** the depicted event date.

So the file is what the page promised: 854x480, ~230.6 s, genuine archival camcorder video, and it additionally carries an audio track that the scouting pass could not confirm.

## Active picture / pillarbox

```powershell
ffmpeg -hide_banner -ss 00:02:16 -t 7 -i $f -vf "cropdetect=24:2:0" -f null -
```

Every sampled frame reports `crop=632:480:112:0`. The 4:3 camcorder picture is **pillarboxed inside the 854x480 container**; the active image is only **632x480** (about 1.32:1).

**Consequence for the 1080p timeline required by the ticket:** the source is SD and does not fill 16:9. Filling a 1920x1080 frame from the 632x480 active area is roughly a **2.25x upscale**, and cropping it to 16:9 discards a large part of the picture. Options for the editor, none chosen here: upscale the active area and pillarbox it on the 1080p timeline; crop to 16:9 and upscale ~2.25x with visible softening; or present it inside an authored archival frame treatment. **Do not stretch the 632x480 picture to 16:9** — that distorts faces and box art. Logged as a review question under R14.

## Frame extraction and manual inspection

```powershell
foreach ($t in "00:02:16.0","00:02:20.0","00:02:24.0") {
  ffmpeg -v error -y -ss $t -i $f -map 0:v:0 -frames:v 1 "assets/broll/BROLL-04/evidence/frames/frame_<t>.png"
}
ffmpeg -v error -y -ss 00:02:20.0 -i $f -map 0:v:0 -frames:v 1 -vf "scale=-2:720" "assets/broll/BROLL-04/evidence/frames/frame_02-20-0_720p.png"
```

Committed frames, all viewed:

| File | Viewed at | What I actually saw |
|---|---|---|
| `evidence/frames/frame_02-16-0.png` | full size (854x480) | Mid-move handheld frame. A dark-haired man's head and shoulder fill the left third in profile, close to the lens and soft with motion blur. Behind him, a shelf bay of **yellow boxed software** (three tiers, faced out) with a vertical blue rebate flag down the middle of the bay. Red store banners and ceiling truss above, out of focus. Legible as "1990s software store", but too blurred and too tight to be a clean first frame. |
| `evidence/frames/frame_02-20-0.png` | full size (854x480) | The strongest frame of the segment. A man in a dark polo and light trousers walks **away down the aisle**, seen from behind, mid-stride. Left: a rack of orange-and-black boxed games, the word **BEAST** repeated across four faced-out rows. Right: a shelf bay of **yellow boxed software** under a vertical blue banner reading **"Up to $35 Rebate"**, with a blue **"New For…"** sign above it. Ceiling balloons, a red hanging banner, and a small printed shelf-talker on the left rack. Exactly the "person browsing boxed software in a 1990s store" beat. |
| `evidence/frames/frame_02-24-0.png` | full size (854x480) | **Not a browsing frame.** The camera has moved on. A man in a dark CompUSA-style polo with a name badge (left) reaches/shakes hands across a pyramid display with a second man at the right edge who is turned to camera. Signage is excellent — **"New For Windows 95"** vertical banner, **"Up to $35 Rebate"**, a **COMPUSA** wall sign, and a **Microsoft Word / Office** box display panel at right — but the action is a two-person interaction, not a browse, and two faces are recognizable. |
| `evidence/frames/frame_02-20-0_720p.png` | 1282x720, confirmed with ffprobe (`scale=-2:720` preserves the 854x480 aspect, so the width lands on 1282 rather than 1280) | Same content as the full-size 02:20 frame, and it holds up: the **"Up to $35 Rebate"** banner, the **BEAST** box titles, the yellow box-art blocks and the balloons all stay readable. The upscale shows the expected camcorder softness, chroma smear on the red banner, and the pillarbox bars, but nothing that reads as a defect rather than as period video. No baked-in captions, timecode burn-in or watermark anywhere in the frame. |

## Do the in/out points still hold?

Additional frames were sampled at 00:02:14.0, 02:15.0, 02:16.5, 02:17.0, 02:18.0, 02:19.0, 02:21.0, 02:22.0, 02:22.5 and 02:23.0 (scratch only, not committed) to settle this.

- **In point 00:02:16.0 — holds, just barely.** It sits inside a continuous handheld move and the frame is soft, with the passing man's head close to the lens. It works as a start because the motion carries into the clean aisle walk. A few frames later (about 00:02:16.3) is cleaner if the editor wants a sharper first frame. 00:02:15.0 would be wrong: it shows a promoter in a **Microsoft Office box costume**, arms raised, facing camera — a different, louder beat.
- **Out point 00:02:24.0 — does NOT hold.** The scouting pass only bracketed it (02:23.5 / 02:25.5) and called it a handshake. On the real file the browse ends earlier: 02:17–02:20 is the clean walk away down the aisle; at 02:21 the man turns back toward camera; 02:22 and 02:22.5 are a good medium of the CompUSA staffer at the "New For Windows 95" pyramid; by 02:23 he has turned to the man on the right and the two-person interaction has begun; 02:24 is mid-handshake.
- **Recommended segment: in 00:02:16.0, out 00:02:22.5 (6.5 s).** That is under the ticket's preferred 8–12 s. Honest options: keep 6.5 s and accept the shorter cut; keep the scouted 8.0 s (02:16.0–02:24.0) and accept that the last 1.5 s reads as a staff/customer interaction with two recognizable faces; or use the alternate segment recorded by the scouting pass (00:03:26.0–00:03:36.0) if a longer browse is needed. Not decided here — an editorial choice for the review deck.
- The **recognizable-people** concern grows toward the out point: 02:22.5–02:24.0 gives clear, frontal, identifiable faces of a store employee and a customer. It stays a review question.

## Tool versions (acquisition pass)

- curl 8.18.0 (bundled `curl.exe` on Windows 11)
- ffmpeg / ffprobe 6.0-essentials_build-www.gyan.dev
- Python 3.14.0
- git 2.53.0.windows.1
- PowerShell 7 (`Get-FileHash` for md5/sha1/sha256)

## Results (acquisition pass)

- Download: **1 file, succeeded**; byte size and both published hashes match. No gate, no barrier, nothing bypassed.
- File is what the page promised: **yes** (854x480, 230.621 s, h264 29.97 fps, plus an audio track).
- Frames extracted and inspected at full size and at 720p: **yes**, results in the table above.
- `python tools/validate_delivery.py --id BROLL-04`: passed (output in the worker report).
- Production status raised to **produced**. Release status stays **blocked**; R14 stays **open**.

## Still not verified after this pass

- **Rights, beyond what is recorded.** The filmmaker's own position is unknown; he was not contacted, per Devin's ruling. The CC0 remains an uploader assertion. Nothing here establishes clearance.
- **Audio content.** An opus stereo track exists and was probed, but not auditioned. If the segment is used with sound, someone must listen for speech, music or a store PA that may carry its own rights.
- **Continuous real-time playback.** Judged from single-frame samples about 0.5–1 s apart across 02:14–02:24, not from watching the clip run.
- **Frame-accurate out point.** Recommended 00:02:22.5 to the nearest half second; the exact cut frame is for the editor.
- **The rest of the 230.6 s file** outside 02:14–02:24, beyond the scouting pass's in-page sampling.
- **Depicted date 1995-08-23.** Consistent with the on-screen CompUSA and Windows 95 launch materials, but taken from the item page and the file's own description; not independently confirmed.
- **Upscale/framing treatment for 1080p.** Recorded as a constraint with options; no treatment produced or chosen.
- **Privacy / recognizable people.** Still a review question, not settled by evidence.
