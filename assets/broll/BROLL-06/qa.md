# BROLL-06 QA report

- **Ticket:** BROLL-06, Pentium-era PC booting (scout)
- **Worker:** BROLL-06 worker subagent, spawned by the B-roll Scouting Manager (session vb-99)
- **Date:** 2026-09-15 (initial pass plus a motion-review rework pass)
- **Result:** `scouted`, with candidates motion-reviewed in-page. No media acquired. Release `blocked`. R14 open.
- **Reviewer:** none yet (goes to the OPS-04 review deck)

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

## Earlier pass (for the record)
In the initial pass, screenshots timed out ("Browser pane is not displayed") and no frames were viewed. Later Pexels navigations then showed a Cloudflare "Performing security verification" page. I stopped at that point and did not bypass it.

## Not checked / not verified
- CPU, model, BIOS date or OS for either free candidate. Nothing readable is on screen at preview size.
- Full-resolution frames. For Pexels, the 4096×2160 original was not viewed (the played rendition was 2732×1440). For Commons, the 640×416 original was not viewed (240p played).
- Pexels file size and full rendition list. Commons fps.
- The YouTube license fields for PwRR7-P-8fc and WCdDKPonXXA; the WCdDKPonXXA watch page was not loaded. The duration, dimensions and hardware of PwRR7-P-8fc. The "Pentium MMX 200" claim came only from a web-search summary.
- The GFDL 1.2 page for the Commons clip (listed on the file page; not loaded).
- Legal sufficiency of any license for the final video (review questions).
- No media was downloaded. No accounts, logins, CAPTCHA, Cloudflare bypass, terms acceptance or payments were involved.

## Reproduction
From the worktree root:

```
git switch ticket/BROLL-06
python tools/validate_delivery.py --id BROLL-06
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
- No renderer, encoder or ffprobe used (no media)

## Proof paths
None saved. Screenshots were viewed in-session only and not written to disk, because the ticket's outputs are text reports and saving captures of third-party frames was not requested. `exports/candidates.md` and `exports/acquisition-handoff.md` are text.
