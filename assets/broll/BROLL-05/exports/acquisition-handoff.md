# BROLL-05 acquisition handoff

Prepared 2026-09-15. **No file has been downloaded.** Scouting status (`scouted`) is not acquisition status, and nothing here is cleared media.

## Ungated free acquisition — pending download approval

These need Devin's batched download approval, through the B-roll Scouting Manager, before anyone downloads them.

### 1. Pexels 20503026: "Floppy Disk 80s Computer Retro Diskette" by Stefan

| Item | Value |
|---|---|
| Asset page (loaded) | https://www.pexels.com/video/floppy-disk-80s-computer-retro-diskette-20503026/ |
| Download control as shown | Green **"Free download"** button. Its chevron opens **"Choose a size:"**, then **"Full HD 1920x1080"**, then **"Download Selected Size"** |
| Size options shown | SD 426x240 · SD 640x360 · SD 960x540 · HD 1280x720 · Full HD 1920x1080 |
| Download link href on page | `https://www.pexels.com/download/video/20503026/`. I recorded this from the page's link and did **not** load it, because loading it starts a file transfer. |
| File played by the page's preview player | `https://videos.pexels.com/video-files/20503026/20503026-hd_1920_1080_24fps.mp4`. The page streamed it for in-page viewing; it wasn't saved. |
| Select | Full HD 1920x1080 |
| Dimensions / fps / duration | 1920×1080, 23.98 fps, 0:11 (11.16 s in player) |
| File size | Not shown on page |
| Save as | `assets/broll/BROLL-05/source/pexels-20503026-stefan-floppy-insert-1920x1080.mp4` |
| License to capture alongside | Pexels License, https://www.pexels.com/license/ (as read 2026-09-15). Save a copy of the license text and asset page as evidence at download time. |
| Account / CAPTCHA | None seen while browsing. The download itself wasn't attempted. |
| Proposed edit | In 00:00.00, out 00:06.00 (see review question RQ1 about length) |
| Post-download checks for the owner | Run ffprobe and confirm 1920×1080, about 11.16 s, 23.976 fps. Confirm the frames match the ones described in `evidence/candidates.json`. Check whether it has an audio track. |

## H02: gated or paid items (not agent actions)

Current producer boundary: no paid footage. These are recorded only so the decision is explicit.

### A. Mixkit 48937, commercial 4K version

- **What:** "Floppy disk being inserted into the system unit". 7 s long; 4K commercial version.
- **Where:** https://mixkit.co/free-stock-video/floppy-disk-being-inserted-into-the-system-unit-48937/, then the button **"Download 4k video from Envato"**. I didn't load the Envato destination.
- **Cost:** Requires an Envato subscription ("Premium Download - 4K Version for commercial use … covered by a lifetime commercial licence"). No price is shown on the Mixkit page, and I didn't check Envato pricing.
- **Why gated:** Paid subscription and account. It sits outside the current no-paid-footage boundary.
- **Free 720p version:** "Download low resolution for free" is **not** proposed. It's under the Mixkit Restricted License, "for Personal Use only", which doesn't fit a public video.
- **Fit caveat:** The disk is seen edge-on, so label side and shutter direction can't be verified. Even if bought, it's weaker than candidate 1.

### B. Paid-platform leads (not inspected)

The WebSearch results named several paid platforms with floppy-insertion listings: Shutterstock, Getty Images, iStock, Envato Elements, Dreamstime, Pond5 and Motion Array. The Mixkit page also shows Envato "View on Envato" tiles (for example "Closeup Of A 3Inch Floppy Disk Inserted Into The System Unit").

I didn't load or inspect any of these pages, so no URLs, prices or terms are recorded. They would all need payment and an account.

### C. Platform-hosted video (YouTube, and Internet Archive mirrors of YouTube)

The Internet Archive search returned several `youtube-*` mirror items with no license. None was identified as a matching close-up, and none is proposed. Any such clip would be rights-blocked, because a standard platform license isn't reuse permission.

## Stop rules honoured

No account, login, payment, terms acceptance, CAPTCHA bypass, watermark-preview download or file download was performed.
