# BROLL-02 — QA report

**Dates:** scouting pass 2026-09-15; acquisition pass 2026-09-15 · **Workers:** Claude (Opus 5), spawned by the B-roll Scouting Manager (scouting pass: session vb-99; acquisition pass: session vb-bf) · **Branches:** `ticket/BROLL-02` (scouting), `ticket/BROLL-02-media` (acquisition)
**Production status:** produced (one approved fallback clip acquired and verified) · **Release status:** blocked (R14 open)

> **The acquired clip does not show War.** It shows two people playing a generic draw-and-discard card game. It is an explicitly labeled fallback and must never be described as War in the edit, in narration, or in any downstream file.

---

## Part 1 — Acquisition pass (2026-09-15)

Devin approved this one download on 2026-09-15; the approval was relayed by the B-roll Scouting Manager (session vb-bf).

### Download

```
curl.exe -L -sS -A "Mozilla/5.0" \
  -o assets/broll/BROLL-02/source/pexels-38810850-jellymarketing-elderly-couple-cards-1920x1080.mp4 \
  -D "$env:TEMP\broll02-headers.txt" \
  -w "http_code=%{http_code}\nsize=%{size_download}\ncontent_type=%{content_type}\nurl_effective=%{url_effective}\nnum_redirects=%{num_redirects}\n" \
  "https://www.pexels.com/download/video/38810850/"
```

Result: `http_code=200`, `size=4393818`, `content_type=video/mp4`, `num_redirects=1`,
`url_effective=https://videos.pexels.com/video-files/38810850/16496615_1920_1080_24fps.mp4`.

The response chain was HTTP 302 from `www.pexels.com` to `videos.pexels.com`, then HTTP 200 `video/mp4` with `Content-Length: 4393818` and `Content-Disposition: attachment`. **No gate was encountered:** no login, no account creation, no payment, no terms or cookie click-through, and no Cloudflare interstitial or CAPTCHA. No personal data, email address or credential was sent; only a generic browser User-Agent. Cloudflare set `__cf_bm` / `_cfuvid` cookies on the response, but nothing had to be accepted or solved.

### Verified file facts

| Field | Value | How |
|---|---|---|
| Path | `source/pexels-38810850-jellymarketing-elderly-couple-cards-1920x1080.mp4` | — |
| Byte size | **4,393,818** | `(Get-Item $f).Length`, matching curl's `size_download` and the `Content-Length` header |
| SHA-256 | **`7b43b09327990d2b6bcd606a47a3646565c3a8788d9bde46142a244952eec188`** | `Get-FileHash -Algorithm SHA256` |
| Dimensions | **1920×1080**, SAR 1:1, DAR 16:9, `yuv420p`, progressive | ffprobe |
| Duration | **9.634625 s** (container and video stream agree) | ffprobe |
| Frame rate | **24000/1001 = 23.976 fps** (`r_frame_rate` and `avg_frame_rate`) | ffprobe |
| Codec | **H.264 High profile, level 5.0**, `avc1`; encoder tag `Lavc61.19.100 libx264` | ffprobe |
| Bit rate | 3,645,577 bit/s (video stream); 3,648,356 bit/s (container) | ffprobe |
| Colour | bt709 primaries and matrix, `tv` range, transfer unknown | ffprobe |
| Audio stream | **None.** The file has two streams: the H.264 video and a QuickTime `tmcd` timecode data track (start timecode 00:14:55:19) that carries no picture or sound | ffprobe |
| Container | `mov,mp4,m4a,3gp,3g2,mj2`, major brand `iso5`, muxer tag `Lavf61.7.100` | ffprobe |

### Match against the scouted candidate

| Expectation | Actual | Verdict |
|---|---|---|
| 1920×1080 | 1920×1080 | match |
| 23.98 fps | 23.976 fps (24000/1001) | match |
| about 9 s | 9.634625 s | close; the page's "0:09" was rounded down |
| **roughly 20 MB** | **4,393,818 bytes ≈ 4.19 MiB** | **mismatch — the file is about a fifth of the anticipated size** |
| Creator Jelly Marketing, Pexels License | Asset page and license page as recorded in `source/source.json` | match |
| Content: two people playing cards, not War | Confirmed, see below | match |

On the size mismatch: the URL served the Full HD rendition named by the page (`16496615_1920_1080_24fps.mp4`), the response was a complete HTTP 200 with a `Content-Length` equal to the bytes received, and ffprobe decodes the file cleanly end to end at `probe_score=100`. The "roughly 20 MB" figure in the download approval was an estimate that the page did not display; at 3.65 Mbit/s over 9.63 s, 4.19 MiB is the internally consistent size. Nothing indicates a truncated or partial download. It is recorded here as a mismatch against the stated expectation rather than silently accepted.

### Frame extraction

```
ffmpeg -hide_banner -v error -y -ss 1 -i <clip> -frames:v 1 evidence/frames/frame-01s.png
ffmpeg -hide_banner -v error -y -ss 4 -i <clip> -frames:v 1 evidence/frames/frame-04s.png
ffmpeg -hide_banner -v error -y -ss 8 -i <clip> -frames:v 1 evidence/frames/frame-08s.png
ffmpeg -hide_banner -v error -y -i evidence/frames/frame-04s.png -vf scale=-2:720 evidence/frames/frame-04s-720p.png
```

`frame-01s.png`, `frame-04s.png` and `frame-08s.png` are 1920×1080. `frame-04s-720p.png` is 1280×720 (confirmed with `ffprobe -show_entries stream=width,height`).

### What I actually saw — full size (1920×1080)

All three stills were opened and viewed at full size.

- **frame-01s.png** — Interior of a bright suburban dining room. A woman sits at the left and a man at the right of a round dark-wood table, facing each other across it. She wears a black-and-white patterned top and glasses; he wears a fringed tan suede vest with beaded floral motifs over a grey plaid shirt, and glasses. Behind them: a white french door onto a garden, a window at the right, framed school portraits, and a gold sunburst mirror. On the table: a glass jar of pale peonies at the front left, a blue card box, a small **face-down stock pile with blue patterned backs at the centre**, two or three face-up cards beside it, and a spread of **face-up cards in front of the man only**. She holds two or three cards **face-down toward camera** in her right hand; he holds a small fan of cards and is looking at them.
- **frame-04s.png** — Same setup, wider framing (the camera has eased back; more of the room, the french door and the floor are visible). She still holds her small fanned hand; he is handling a card at the edge of his hand. The central face-down stock, the adjacent face-up cards and his face-up spread are all still on the table, unchanged in arrangement.
- **frame-08s.png** — Widest framing of the three. He is **drawing or playing a single card out of his hand** toward the table with his left hand while his right hand holds the rest of the fan; a face-up card is visible in the fan. She watches, still holding her cards face-down. The central stock, the face-up cards beside it and his spread are still in place.

**Watermark and overlay check:** no watermark, no logo, no bug, no burned-in caption and no timecode burn-in appears anywhere in any of the three frames, at full size or at 720p. The only text-like elements are the printed card faces and the pattern on the card box.

### What I actually saw — 720p

`frame-04s-720p.png` (1280×720) was viewed as a second pass on the same moment. Everything that matters editorially survives the downscale: both players, their hands of cards, the face-down stock, the face-up cards on the table and the man's spread all remain clearly readable; faces and the room read cleanly; no compression artefacts, ringing or aliasing became visible; still no watermark or overlay. Card **suits and pips are legible at 720p but individual rank markings on the smaller table cards get soft** — irrelevant here, since nothing in the shot depends on reading a specific card.

### Confirmation that this is NOT War

Checked against the ticket's own definition of the shot (two players, **separate face-down piles**, **simultaneous rank comparison**):

- **No two per-player face-down piles.** There is a *single shared* face-down stock at the centre of the table. War requires one face-down pile in front of each player.
- **Both players hold hands of cards.** War players do not hold a hand; they flip from the top of their pile.
- **A face-up spread sits in front of one player only** — asymmetric, consistent with melds or a discard area, not with War's symmetric flip-and-compare.
- **No simultaneous flip occurs** anywhere in the 9.63 s. At 8 s one player is playing a single card while the other waits, which is turn-taking, not simultaneous comparison.
- No chips, money or betting are visible, so it is at least not a poker-style shot.

**Verdict: this is a generic two-person draw-and-discard card game — it is not War.** It is usable only as an explicitly labeled fallback for the section 5 cutaway. The standing review question (no free clip shows real War) is unchanged by this acquisition and remains open under R14.

### Acquisition-pass tool versions

- ffprobe / ffmpeg **6.0-essentials_build-www.gyan.dev** (gcc 12.2.0, MSYS2)
- curl **8.18.0** (x86_64-w64-mingw32, libcurl/8.18.0, Schannel)
- Python **3.14.0**
- git **2.53.0.windows.1**
- PowerShell 7 on Windows 11 Pro 10.0.26200

### Reproduction (acquisition pass)

From the worktree root:

```
python tools/validate_delivery.py --id BROLL-02
ffprobe -hide_banner -v error -show_format -show_streams assets/broll/BROLL-02/source/pexels-38810850-jellymarketing-elderly-couple-cards-1920x1080.mp4
sha256sum assets/broll/BROLL-02/source/pexels-38810850-jellymarketing-elderly-couple-cards-1920x1080.mp4
```

Re-downloading is not required to verify the package; compare the recorded SHA-256 against the stored file.

---

## Part 2 — Scouting pass (2026-09-15), carried forward

| Check | Method | Result |
|---|---|---|
| Search for the specified shot | WebSearch; WebFetch on Pixabay, Mixkit, Coverr, Wikimedia Commons, Internet Archive advancedsearch and YouTube oEmbed; Claude Browser pane (tabs `seed` and `tab-2`) on Pexels, Pixabay and Videvo/Magnific. The full query log is in `exports/candidates.md` | No clip visibly showing War on any free source |
| Candidate metadata | Asset pages read on 2026-09-15 (WebFetch plus in-browser page details) | Creator, duration, dimensions and fps recorded per candidate |
| Rank 1 motion | Played the Pexels in-page preview; screenshots at about 0:01, 0:04, 0:07 and 0:09 | Reviewed. Two players across a table with fanned hands: not War. **Now superseded by the acquired file above** |
| Rank 2 motion | Played the Pixabay in-page preview (muted) from 0; `video.currentTime` logged at 1.02 / 4.19 / 7.32 / 10.47 s with a screenshot at each | Reviewed. Three or more players on a floor mat: not War |
| Rank 3 motion | Two clicks on the player plus a scripted play | **Not reviewed:** the player stayed on its poster frame; no `<video>` element loaded |
| License terms | Pexels License and Pixabay license-summary pages read on 2026-09-15 | Recorded in substance in `evidence/candidates.json` and `evidence/source-excerpts.md` |
| Download barriers | Download dropdowns opened on the Pexels pages (size labels read); Pixabay dropdown rendered no options | No login shown for free download on Pexels or Pixabay |
| Cookie banners | Pixabay and Magnific: "Reject All" clicked | Non-essential cookies declined |
| Structure | `python tools/validate_delivery.py --id BROLL-02` | See the validator run in the completion report |

Seek-while-paused screenshots on Pixabay (0.3 / 5.0 / 10.4 s) produced identical frames because the hidden pane did not repaint. They were discarded and replaced by the timed playback captures above.

### Scouting-pass reproduction

```
python tools/validate_delivery.py --id BROLL-02
sha256sum sources/ASSET_PLAN.md sources/SCRIPT.md
sed -n '109,122p' sources/ASSET_PLAN.md
sed -n '799,805p' sources/SCRIPT.md
```

### Scouting-pass tool versions
- Python 3.14.0, git 2.53.0.windows.1
- Claude Code Browser pane (Claude_Browser MCP tools), WebFetch and WebSearch as provided in that session (versions not exposed)

---

## Still NOT checked / unverified

- **Only the rank 1 clip was downloaded.** Ranks 2 and 3 remain scouted URLs, not acquired media, with no file size, codec or true-fps verification. Their download approval is still outstanding.
- **Rank 3 motion** was never reviewed (the in-page player would not start); its poster frame alone was seen.
- **Playback was not watched end to end.** The acquired clip was inspected as three extracted stills plus ffprobe metadata, not as continuous motion in a player, so brief events between the sampled seconds — a moment of simultaneous play, a lens flare, a splice — would not have been caught. Nothing in the three stills or the metadata suggests any.
- **No audio was evaluated** because the file contains no audio stream; this is a fact about the container, not a listening test.
- **No model release** is published for either identifiable person; whether the Pexels License is sufficient for this use is a legal question for review, not a finding here.
- **R14 is open.** Acquisition is not clearance. Release stays `blocked` until the OPS-04 review deck.
- **The 20 MB expectation is unexplained at source**; I verified the file is complete and self-consistent, but I did not re-fetch other renditions to compare, and no file size was displayed on the asset page.
- The YouTube War leads were not played; their duration, license field and content remain unverified (title and channel from oEmbed only).
- The Pixabay full terms page and the Mixkit license page were not loaded; the Videvo/Magnific free-filter results did not render, so that site was not fully searched.
- Validator limits stand: `validate_delivery.py` checks structure, paths and hashes. It performs no OCR, no MP4 decode, and no visual, historical or legal judgment.

## Reviewer
None yet. Release review happens in the OPS-04 review deck.
