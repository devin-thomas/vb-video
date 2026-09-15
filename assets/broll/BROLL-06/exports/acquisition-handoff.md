# BROLL-06 acquisition handoff

Scouting status and acquisition status are separate. **Scouted ≠ acquired**, and **acquired ≠ cleared**.
Accessed: 2026-09-15. Both candidates were motion-reviewed in-page; see `exports/candidates.md`.

## Acquisition result (2026-09-15)

Devin approved **one** download, and it succeeded.

| Item | Result |
|---|---|
| Pexels 8888818 (rank 1) | **Acquired.** `source/pexels-8888818-mart-production-vintage-computer.mp4`, 29,243,915 bytes, sha256 `5aa6828fb8a25cc46c24a0d8229f0f1e9db6c1fb7cab7df8aa68563543107f0f`. Real file: 4096×2160, 25 fps, 11.8 s, h264, no audio stream — matching the page's claim. No Cloudflare check, no login, no terms click-through, no CAPTCHA; nothing bypassed. |
| Commons `BIOS_POST_IMGP9357_wp.ogv` (rank 2) | **Not acquired.** Not part of the approval; no download attempted. |
| Pixabay 126935 | **Not acquired.** Rejected after motion review. |
| H02-A, H02-B (YouTube) | **Not acquired.** Rights-blocked; unchanged. |

**What the acquired clip is, and is not.** Verified on the real file at full size and at 720p: a beige CRT monitor and keyboard on a desk in a dim room, slow camera drift, **screen blank and dark throughout**. It is **not a boot and not a power-on**. No PC case appears in frame, so **no CPU is visible and none can be identified**; no date is legible. The only hardware marking readable at full resolution is a **ViewSonic "E70" monitor bezel marking**, which identifies a monitor, not a machine or an era. Use it as a **period-setting cutaway only** — never label it a boot, and never caption or imply "Pentium" over it.

Acquisition does not clear it: R14 stays open and release stays `blocked` pending the OPS-04 deck.

## Original request record — ungated free acquisition

These needed no account, payment, CAPTCHA or terms click-through, as far as the pages showed. Row 1 has since been approved and acquired, as recorded above; row 2 has not. After download, the owner verifies on the actual file:
- duration, dimensions and fps;
- that it is the selected asset;
- that it carries no watermark;
- the in/out points below, at full resolution.

| # | Asset page | Download option as shown | Dimensions / fps | File size shown | In/out | Save as |
|---|---|---|---|---|---|---|
| 1 | https://www.pexels.com/video/a-vintage-computer-on-a-table-8888818/ (MART PRODUCTION) — **acquired 2026-09-15** | "Free download" button. A 2732×1440 preview rendition URL was seen in the page; the download endpoint `https://www.pexels.com/download/video/8888818/` in fact served `https://videos.pexels.com/video-files/8888818/8888818-uhd_4096_2160_25fps.mp4` | Page: 4096×2160, 25 fps. **Real file: 4096×2160, 25 fps, 11.8 s** | not displayed on the page; **real size 29,243,915 bytes** | 00:00:00.500–00:00:10.500, confirmed on the acquired file | `assets/broll/BROLL-06/source/pexels-8888818-mart-production-vintage-computer.mp4` |
| 2 | https://commons.wikimedia.org/wiki/File:BIOS_POST_IMGP9357_wp.ogv (Rainer Knäpper / Smial) | Original file: `https://upload.wikimedia.org/wikipedia/commons/5/56/BIOS_POST_IMGP9357_wp.ogv` | 640×416; fps not shown; 35 s | 955,853 bytes (933 KB) | 00:00:02.000–00:00:12.000 | `assets/broll/BROLL-06/source/commons-BIOS_POST_IMGP9357_wp.ogv` |

**Not requested:** Pixabay 126935 ("Switch Off, turn on, on", Kmeel_com). It was rejected after motion review because it shows a modern flat-panel monitor, not a period PC.

Retain with each file:
- a `source.json` with creator, page URL, access date, dimensions and license URL;
- the license page URL and access date.

Pexels note: no Cloudflare check appeared in the rework pass or in the acquisition download. An earlier pass the same day saw a Cloudflare "Performing security verification" page; it was not bypassed. If one appears in future, a human handles it; an agent must not bypass it.

License reminders:
- **Pexels:** no attribution required.
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
- **What:** a boot to Windows 95 (per title). Hardware is unverified: only a search-engine summary claimed a Pentium MMX 200 with 32 MB RAM.
- **Duration, size and license:** not verified. Assume the standard YouTube license, which grants no reuse.
- **Route:** Devin checks the license on the page. If it is not Creative Commons, Devin requests permission from the creator.
- **Cost:** unknown.

### Out of scope (not pursued)
- **Paid stock:** iStock, Shutterstock and Dreamstime boot-sequence clips appeared in search results. Pages were not loaded, and paid footage is outside the authorized boundary.
- **AI or self-shot stand-in:** would need separate approval and a new labeled assignment. Not commissioned here.

## Return package after acquisition — delivered for row 1

- ✅ Downloaded original at the path above, preserved byte-identical.
- ✅ License evidence and actual local path (`source/source.json`, `evidence/provenance.json`).
- ✅ ffprobe output for duration, dimensions, fps, codec and audio-stream presence (`qa.md`, `source/source.json`).
- ✅ In/out points confirmed at full resolution.
- ✅ Full-size and 720p inspection frames (`evidence/frames/`).
- Status moved from `scouted` to `produced`. Release stays `blocked`; R14 stays open.

Row 2 (Commons) remains outstanding and un-downloaded.
