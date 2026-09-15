# HIST-17 — Production QA

**Production:** produced. **Release:** blocked (R14 rights review open).

## Delivered
- `source/original.html`: raw archived HTML of http://www.tucows.com/ from Wayback capture 19961022175612 (22 Oct 1996 17:56:12 GMT), fetched in `id_` mode and byte-exact.
- `source/raw/`: the page's GIFs as archived; the 28 Dec 1996 comparison page; uncropped Chromium captures with the Wayback toolbar (`wayback-toolbar-*.png`, showing URL and OCT 22 1996) and without it (`wayback-replay-*.png`).
- `source/candidates/`: alternate candidates B (idirect mirror, 1996-12-30) and C (phoenix mirror, 1996-11-17) with raw HTML and captures.
- `exports/editorial-frame.png`: 1920×1080 editorial frame, no Wayback UI, no additions.
- `proofs/editorial-frame-720.png` (1280×720) and `proofs/frame-crop-check.png` (crop of the uncropped capture).
- Evidence: `evidence/source.json`, `rights.json`, `provenance.json`, `claim-checks.json`, `source-excerpts.md`, `acquisition-log.json`, `candidates-log.json`, `frame.json`.

Named variants: `original` → source/original.html plus the uncropped captures; `editorial-frame` → exports/editorial-frame.png. Still asset: duration and fps are null, and it holds for editorial timing.

## Checks actually performed
- **Holding verified.** Wayback CDX for tucows.com and www.tucows.com, 1994–1997, returned captures 19961022175612, 19961023235110 (same digest), 19961228134206, 19970212181139, and later. Nothing earlier than 22 Oct 1996.
- **Identity and date.** Checked in the raw bytes and headers: `Memento-Datetime: Tue, 22 Oct 1996 17:56:12 GMT`; `<title>The Ultimate Collection of Winsock Software</title>`; "Primary TUCOWS Mirrors"; footer "Copyright © 1996 Scott A. Swedorski". The toolbar capture shows URL http://www.tucows.com/ and date OCT 22 1996.
- **Embedded resources.** All raw GIFs start with GIF87a/GIF89a signatures. Sizes: Logo 200×126, cs_ad 468×60, blue 13×13, fast-burst 35×17, background 150×93. Replay timestamps come from the Playwright response log: page and Logo 1996-10-22; blue, fast-burst and cs_ad 1996-10-23; the background tile 1996-12-28 (no earlier capture exists).
- **No archive UI in the frame.** The `if_` replay has no `wm-ipp` toolbar element (script check), and none is visible in the export.
- **Reversible crop.** `exports/editorial-frame.png` is CSS region (0,0)–(1280,720) rendered at device scale 1.5. `proofs/frame-crop-check.png` is the same region cut from `source/raw/wayback-replay-fullpage.png` (1280×2397) and Lanczos-upscaled. Side by side they show identical layout and content. The frame omits the mirror rows below the Canada heading and the copyright footer. That does not change what the image means (the TUCOWS front page), and the footer stays in the originals.
- **Manual visual review at full size.** Viewed exports/editorial-frame.png at 1920×1080. The cow logo and TUCOWS wordmark, the red headline, the ConnectSoft banner, "Primary TUCOWS Mirrors", "United States" and the start of "Canada" are sharp; nothing is stretched. The headline and logo sit inside the safe area (x 120–1800, y 72–1008). The last mirror row (Ontario) is cut at the bottom edge; it is non-essential page content, not a framing error.
- **Manual visual review at 720p.** Viewed proofs/editorial-frame-720.png at 1280×720. The headline, section headings and mirror names are readable, and the "Fast" badges are legible but small.
- **Candidates.** Viewed the B toolbar capture. It reads "UDDERLY INCREDIBLE SHAREWARE CENTER" and "Software Listings for: Windows 95 | Windows 3.x | Macintosh". C was inspected as HTML: a text changelog with a "ComputerLink OnLine Inc." copyright. Deficiencies are in evidence/source.json.
- **Validator.** See "Validator run" below.

## Validator run
`python assets/historical/HIST-17/src/finish.py` (38 files inventoried), then `python tools/validate_delivery.py --id HIST-17`, exit code 0:

```
{
  "id": "HIST-17",
  "ok": true,
  "errors": [],
  "limitations": [
    "No OCR or visual quality judgment.",
    "No MP4 decode/frame-rate/codec validation; inspect with ffprobe and playback.",
    "No historical, semantic, or legal clearance.",
    "Manual 1080p/720p review remains required."
  ]
}
```

Adding this result changes qa.md's hash, so finish.py and the validator were run again after the edit. The final result is in the worker report.

## Reproduction
From the repository root (network access to web.archive.org required):

```
python assets/historical/HIST-17/src/acquire.py
curl -s -D assets/historical/HIST-17/source/raw/background-19961228134221.headers.txt -o assets/historical/HIST-17/source/raw/background-19961228134221.gif "https://web.archive.org/web/19961228134221id_/http://www.tucows.com:80/images/background.gif"
python assets/historical/HIST-17/src/acquire_candidates.py
python assets/historical/HIST-17/src/build_frame.py
python assets/historical/HIST-17/src/finish.py
python tools/validate_delivery.py --id HIST-17
```

Re-running re-fetches from the Wayback Machine. The raw payloads should hash the same; captures can differ slightly if Wayback changes its replay or the Chromium build changes. Tools: Windows 11 10.0.26200, Python 3.14.0, Playwright 1.63.0 with bundled Chromium (the version is recorded in delivery.json toolchain and evidence/frame.json), Pillow 12.3.0, curl (Git for Windows), git 2.53.0.windows.1. Cairo is not used.

## Remaining blockers and review questions
1. **R14 rights (legal risk).** No licence was found for the page, logo or ConnectSoft banner. The Internet Archive grants access for scholarship and research only. The exact question is in evidence/rights.json and claim-checks.json.
2. **Candidate choice (taste).** A is the canonical www.tucows.com page but reads as a mirror picker. B (idirect mirror, 1996-12-30) says "SHAREWARE CENTER" and shows software listings. Swap to B if the cue needs "download site" at a glance.
3. **Period rendering (authenticity).** The capture is 2026 Chromium with Windows 11 Arial, not Netscape Navigator 3/IE3. The background tile comes from a 1996-12-28 capture. Label as "archived page, rendered today" or accept.
4. **Script arithmetic (Writing Lead).** "On a 14.4 modem, that's nearly ten minutes" for 1.5 MB is about 14–17 minutes. The asset idea at War/SCRIPT.md:854 ("14.4 modem speed, 9+ minutes remaining") has the same understatement. The proposed wording is in claim-checks.json; War/SCRIPT.md was not edited.

Reviewer: none yet. Produced is not release approval.
