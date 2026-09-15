# BROLL-06 acquisition handoff

Scouting status and acquisition status are separate. **Scouted ≠ acquired.** No file has been downloaded; `source/` does not exist yet.
Accessed: 2026-09-15.

## Ungated free acquisition — pending download approval

These need no account, payment, CAPTCHA or terms click-through, as far as the pages showed. They are held for the manager's single batched download request to Devin. After download, the owner must verify on the actual file: duration, dimensions, fps, that it is the selected asset, and that it has no watermark. The owner then does the motion review that this pass could not do.

| # | Asset page | Download option as shown | Dimensions / fps | File size shown | Save as |
|---|---|---|---|---|---|
| 1 | https://www.pexels.com/video/a-vintage-computer-on-a-table-8888818/ (MART PRODUCTION) | "Free download" button. A rendition URL was seen in the page: `https://videos.pexels.com/video-files/8888818/8888818-uhd_2732_1440_25fps.mp4` | Page: 4096×2160, 25 fps. Rendition seen: 2732×1440, 25 fps | not displayed | `assets/broll/BROLL-06/source/pexels-8888818-mart-production-vintage-computer.mp4` |
| 2 | https://pixabay.com/videos/switch-off-turn-on-on-off-computer-126935/ (Kmeel_com) | "Free download" (size menu not expanded) | 3840×2160, 29 fps | not displayed | `assets/broll/BROLL-06/source/pixabay-126935-kmeel-switch-off-turn-on.mp4` |
| 3 | https://commons.wikimedia.org/wiki/File:BIOS_POST_IMGP9357_wp.ogv (Rainer Knäpper / Smial) | Original file: `https://upload.wikimedia.org/wikipedia/commons/5/56/BIOS_POST_IMGP9357_wp.ogv` | 640×416; fps not shown; 35 s | 955,853 bytes (933 KB) | `assets/broll/BROLL-06/source/commons-BIOS_POST_IMGP9357_wp.ogv` |

Retain with each file:
- a `source.json` with creator, page URL, access date, dimensions and license URL;
- the license page URL and access date.

Pexels note: in the in-app browser, pexels.com later presented a Cloudflare "Performing security verification" page. If that appears at download time, a human should handle it; an agent must not bypass it.

Pixabay note: whether any size in the download menu requires login is unverified.

License reminders:
- **Pexels:** no attribution required.
- **Pixabay:** no attribution required; trademark clause applies.
- **Commons (Free Art License):** attribution required. Proposed credit: "BIOS POST IMGP9357 wp.ogv" by Rainer Knäpper (Smial), Free Art License 1.3, via Wikimedia Commons.

## H02 — gated items (rights-blocked; no action taken)

The user owns every decision here: permission requests, any payment, and any terms. The agent performed no login, contact, purchase or download.

### H02-A — LGR, "Unboxing & Enjoying an $1,899 PC from 1996! AST Advantage 622"
- **Where:** YouTube video ID `WCdDKPonXXA`. Metadata was loaded from the Internet Archive mirror at https://archive.org/metadata/youtube-WCdDKPonXXA; the YouTube watch page itself was not loaded.
- **What:** creator's description names "a 100MHz Intel Pentium CPU" with 8 MB RAM and a Windows 95 desktop. The best-evidenced Pentium-era hardware of any lead.
- **Duration and size:** 2902 s. The mirror lists 3840×2160 (mkv) and 854×480 (mp4).
- **Boot segment:** not located (not played). The owner must find the power-on/POST/Windows 95 startup section.
- **Rights:**
  - The IA mirror has no license or rights field, and a mirror is not a rights basis.
  - The YouTube license field was not verified.
  - Background music is from Epidemic Sound, so use video only.
- **Route:** Devin contacts the creator (LGR) for written permission, clip scope and fee.
- **Cost:** unknown.

### H02-B — Jaime Cobo Vicente, "Old computer boot up Windows 95"
- **Where:** https://www.youtube.com/watch?v=PwRR7-P-8fc (channel @Jcvlasmesas, per oEmbed)
- **What:** a boot to Windows 95 (per title). Hardware is unverified: only a search-engine summary claimed a Pentium MMX 200 with 32 MB RAM, and I could not read the page description.
- **Duration, size and license:** not verified (page renderer hung in the hidden browser pane). Assume the standard YouTube license, which grants no reuse.
- **Route:** Devin checks the license on the page. If it is not Creative Commons, he requests permission from the creator.
- **Cost:** unknown.

### Out of scope (not pursued)
- **Paid stock:** iStock, Shutterstock and Dreamstime boot-sequence clips appeared in search results. Pages were not loaded, and paid footage is outside the authorized boundary.
- **AI or self-shot stand-in:** would need separate approval and a new labeled assignment. Not commissioned here.

## Return package expected after acquisition
- Downloaded original(s) at the paths above, or an explicit no-acquisition result.
- License evidence and actual local paths.
- Ffprobe output for duration, dimensions and fps.
- Owner's motion review with confirmed in/out points.
- Scouting status stays `scouted` until the files exist and are verified.
