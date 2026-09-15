# BROLL-06 QA report

- **Ticket:** BROLL-06, Pentium-era PC booting (scout)
- **Worker:** BROLL-06 worker subagent, spawned by the B-roll Scouting Manager (session vb-99)
- **Date:** 2026-09-15
- **Result:** `scouted` (metadata/terms scout). No media acquired. Release `blocked`. R14 open.
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
| Pixabay | pc turning on | 50 on page 1 of 10 | 126935 (power button) |
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

3. **Page inspection.** For every ranked candidate and lead:
   - Loaded the asset page and recorded creator, duration, dimensions, fps, date, description and download label.
   - Loaded the license page and recorded its terms.
   - For Commons, also read the API `imageinfo`/`extmetadata` response.
4. **In-app browser (own tab `tab-6`).**
   - Pexels 8888818: read the page text.
   - Pixabay 126935: read the page text and located its "Free download" control. I did not click it.
   - Commons file page: read the DOM of its video element.
5. **Structure validation.** Ran `python tools/validate_delivery.py --id BROLL-06` after the final hashes (result reported in the completion message).

## Motion review — NOT performed
- The in-app Browser pane was hidden for the whole session. `computer screenshot` timed out ("the Browser pane is not displayed, so the page is not compositing frames").
- **Pexels 8888818:** a JavaScript playback probe played a related-clip preview (8889183, 22.04 s, 960×506), not the asset itself.
  - Later Pexels navigations returned a Cloudflare "Performing security verification" page. I stopped using Pexels in the browser there and did not attempt to pass it.
- **Pixabay 126935:** the page exposed no `<video>` elements to the hidden tab.
- **YouTube PwRR7-P-8fc:** the page title loaded, but script execution timed out (renderer hung), so the description and license were not read.
- **Commons:** the in-page player's video element stayed at readyState 0, so no frames were decoded.
- **Consequence:** no frames of any candidate were viewed. All ranks come from page text. All in/out points are provisional and derived from stated durations. There was no 1080p or 720p visual inspection, because no media exists locally.

## Not checked / not verified
- Whether candidate 1 (Pexels 8888818) shows a powered-on or booting PC.
- Whether candidate 2 (Pixabay 126935) depicts 1990s hardware.
- Any CPU, BIOS date, or POST text for the free candidates.
- Pexels and Pixabay file sizes and full rendition lists. Pexels showed no size; the Pixabay size menu was deliberately not opened.
- Whether any Pixabay size requires login.
- fps of the Commons clip.
- The YouTube license fields for PwRR7-P-8fc and WCdDKPonXXA; the WCdDKPonXXA watch page was not loaded.
- The duration, dimensions, and hardware of PwRR7-P-8fc. The "Pentium MMX 200" claim came only from a web-search summary.
- The GFDL 1.2 page for the Commons clip (listed on the file page; not loaded).
- Legal sufficiency of any license for the final video (review questions).
- No media was downloaded (hard limit for this pass). No accounts, logins, CAPTCHA, terms acceptance or payments were involved.

## Reproduction
From the worktree root:

```
git switch ticket/BROLL-06
python tools/validate_delivery.py --id BROLL-06
python -c "import hashlib,pathlib;b=pathlib.Path('assets/broll/BROLL-06');[print(p.relative_to(b).as_posix(),p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(b.rglob('*')) if p.is_file() and p.name not in ('delivery.json','state.json')]"
```

To re-check the web evidence, reload the URLs in `evidence/candidates.json` and `evidence/provenance.json`. They are live pages and may change after 2026-09-15. The Commons metadata can be re-read with:

```
https://commons.wikimedia.org/w/api.php?action=query&titles=File:BIOS_POST_IMGP9357_wp.ogv&prop=imageinfo&iiprop=url|size|mime|extmetadata|user|timestamp&format=json
```

## Tool versions
- Python 3.14.0
- git 2.53.0.windows.1
- Claude Code WebFetch / WebSearch tools (no version exposed)
- Claude Browser in-app tab tools (no version exposed)
- No renderer, encoder or ffprobe used (no media)

## Proof paths
None. No exports are images or video; `exports/candidates.md` and `exports/acquisition-handoff.md` are text.
