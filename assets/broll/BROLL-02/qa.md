# BROLL-02 — QA report

**Date:** 2026-09-15 · **Worker:** Claude (Opus 5), spawned by the B-roll Scouting Manager (vb-99) · **Branch:** ticket/BROLL-02
**Production status:** scouted (fallback candidates only; no War match) · **Release status:** blocked (R14 open)

## What was checked, and how

| Check | Method | Result |
|---|---|---|
| Search for the specified shot | WebSearch; WebFetch on Pixabay, Mixkit, Coverr, Wikimedia Commons, Internet Archive advancedsearch and YouTube oEmbed; Claude Browser pane (tabs `seed` and `tab-2`, both opened by this worker) on Pexels, Pixabay and Videvo/Magnific. The full query log is in `exports/candidates.md` | No clip visibly showing War on any free source |
| Candidate metadata | Asset pages read on 2026-09-15 (WebFetch plus in-browser page details) | Creator, duration, dimensions and fps recorded per candidate |
| Rank 1 motion | Played the Pexels in-page preview; screenshots at about 0:01 (player read 0:01 / 0:09), 0:04, 0:07 and 0:09 | Reviewed. Two players across a table with fanned hands and face-up melds: not War |
| Rank 2 motion | Played the Pixabay in-page preview (muted) from 0; `video.currentTime` logged at 1.02 / 4.19 / 7.32 / 10.47 s with a screenshot at each; `video.duration` = 10.733333, `videoWidth×videoHeight` = 1920×1080 | Reviewed. Three or more players on a floor mat: not War |
| Rank 3 motion | Two clicks on the player plus a scripted play | **Not reviewed:** the player stayed on its poster frame; no `<video>` element loaded |
| License terms | Pexels License and Pixabay license-summary pages read on 2026-09-15; the license label on each asset page noted | Recorded in substance in `evidence/candidates.json` and `evidence/source-excerpts.md` |
| Download barriers | Download dropdowns opened on the Pexels pages (size labels read, no option clicked); Pixabay dropdown opened but rendered no options | No login shown for free download on Pexels or Pixabay |
| Watermarks and captions | Visual check of the in-page preview frames | None seen in ranks 1–2; rank 3 poster only |
| Cookie banners | Pixabay and Magnific: "Reject All" clicked | Non-essential cookies declined |
| Structure | `python tools/validate_delivery.py --id BROLL-02` | See the validator run in the completion report |

Seek-while-paused screenshots on Pixabay (0.3 / 5.0 / 10.4 s) produced identical frames because the hidden pane did not repaint. They were discarded and replaced by the timed playback captures above.

## Reproduction

From the worktree root:

```
python tools/validate_delivery.py --id BROLL-02
sha256sum sources/ASSET_PLAN.md sources/SCRIPT.md
sed -n '109,122p' sources/ASSET_PLAN.md
sed -n '799,805p' sources/SCRIPT.md
```

To repeat the motion review manually, open each asset page URL in `evidence/candidates.json` in a browser, play the preview, and check the proposed in/out frames. For Pixabay, in the page console: `v=document.querySelector('video'); v.muted=true; v.currentTime=0; v.play();` then read `v.currentTime`, `v.duration`, `v.videoWidth` and `v.videoHeight`.

## Tool versions
- Python 3.14.0
- git 2.53.0.windows.1
- Claude Code Browser pane (Claude_Browser MCP tools), WebFetch and WebSearch as provided in this session (versions not exposed)

## NOT checked
- **No media downloaded**, so there was no ffprobe, no file-size, codec or true-fps verification, and no inspection at full source resolution or at 1080p/720p. Screenshots were taken of the in-page players at 0.5–0.6 scale of an 800×609 viewport. No screenshot files were saved into this package.
- Audio on any candidate (previews muted or unheard).
- Rank 3 motion (poster frame only).
- Exact frame-accurate timecodes for rank 1 after 0:01 (estimated from wait intervals).
- Pixabay download size options and any file sizes (not displayed).
- The Pexels download URL for rank 1 was seen as an href but deliberately not loaded; the Pexels and Pixabay download URLs for ranks 2–3 were not captured.
- YouTube leads: not played. Duration, license field, format and content are unverified (title and channel from oEmbed only).
- Videvo/Magnific free-filter results did not render; that site was not fully searched.
- Wikimedia Commons 1896–1904 card films were not opened (not War by title). The Pixabay full terms page (/service/terms/) and the Mixkit license page were not loaded.
- Model releases: none shown on any page; legal sufficiency is a review question, not a finding.
- Scouting is not clearance: no media is acquired or cleared, and R14 remains open.

## Reviewer
None yet. Release review happens in the OPS-04 review deck.
