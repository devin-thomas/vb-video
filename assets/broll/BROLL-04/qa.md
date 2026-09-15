# BROLL-04 QA record

**Date:** 2026-09-15. **Worker:** Claude (branch `ticket/BROLL-04`). **Reviewer:** none yet (review deck, OPS-04).
**Production status:** scouted. **Release status:** blocked (R14 open).

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
