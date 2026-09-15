# XTRA-13 — Production QA

**Production:** produced. **Release:** blocked (R14 rights: no permission on record; R11 unreviewed). Reviewer: none yet; goes to the OPS-04 review deck.

**Subject:** *Karen's Window Watcher*, a freeware window-inspection utility written in Visual Basic 6.0 by Karen Kenworthy (karenware.com). Screenshot `ptwinwatch.gif`, 489×448, archived by the Wayback Machine on 2003-09-17.

This is a script-supplement (SCRIPT.md:685–687) addition, not an original asset-plan row.

## Delivered
- `source/original.gif` — the archived image, byte-exact (17,757 bytes, sha256 `bf77dbc0…df33`). Never edited.
- `exports/editorial-frame.png` — 1920×1080 editorial frame.
- `proofs/editorial-frame-720.png` — 1280×720 review proof.
- `src/frame.py` — the framing script.
- `evidence/source.json`, `evidence/rights.json`, `evidence/provenance.json`, `evidence/claim-checks.json`, `evidence/source-excerpts.md`, `evidence/framing.json`
- `evidence/captures/*` — stored archived and current pages plus the image response headers.

Every file is listed with bytes and SHA-256 in `delivery.json`.

## Method
1. Searched Wikimedia Commons (Category:Visual_Basic), Wikibooks, VBRUN300-era listings, and Karen's Power Tools. Candidates and rejection reasons are in `evidence/source.json`.
2. Found Window Watcher's classic-VB provenance through the author's September 28, 1999 newsletter (VB6 source code) and through the 2001 and 2003 download pages (Visual Basic Runtime v6.0 required; VB6 source code offered). All were read as Wayback raw (`id_`) replays, and stored copies are hashed.
3. Listed Wayback CDX captures for `karenware.com/powertools/images/ptwinwatch*`. The earliest good capture is 2003-09-17 (digest FNXV7VAC6J7I2JLNAWZU2JLJYSBDDHKL). Downloaded it anonymously with curl. The 2001 466×340 image was never archived (the 2003-01-09 capture is a 404) and is not claimed.
4. Framed the image with `src/frame.py`: 2× nearest-neighbour, centred, no crop, no text.

No executable was downloaded or run. No account, payment, terms acceptance, or CAPTCHA was involved.

## Checks actually performed
- **Original unmodified:** passed. SHA-256 is the same before and after framing (`evidence/framing.json`).
- **Archive identity:** passed. The downloaded file's SHA-1 (base32) equals the Wayback CDX digest. The file currently served at karenware.com/images/powertools/ptwinwatch.gif (downloaded 2026-09-15 to scratch only) has the same SHA-256.
- **Image identity against its page:** passed. The 2003-12-09 page embeds `images/ptwinwatch.gif` with WIDTH=489 HEIGHT=448, matching the original's 489×448.
- **Unstretched, reversible framing:** passed. Scale factor 2 on both axes, placed at (471,92)–(1449,988), inside the safe area 120..1800 × 72..1008. The placed region downsampled ×2 with nearest-neighbour equals the original RGB pixels exactly.
- **PNG dimensions:** passed. Export is 1920×1080 RGB; proof is 1280×720.
- **No contrary evidence cropped:** passed. The whole window is shown, including the title bar and the status-bar date 9/3/2003.
- **Script text:** `sources/SCRIPT.md:685–687` equals `War/SCRIPT.md:742–744`. No script change is proposed.
- **All JSON evidence files parse:** passed.
- **`python tools/validate_delivery.py --id XTRA-13`:** exit 0. Output, verbatim:
  ```
  {
    "id": "XTRA-13",
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
- **`python tools/validate_pack.py`:** exit 0, `"errors": []`.

## Manual visual inspection
- **Full size:** Viewed `exports/editorial-frame.png` whole, then two 1:1 crops of it. Crop (471,92)–(1271,692) covers the title bar, tree and detail pane; crop (649,388)–(1449,988) covers the buttons, counters and status bar.
  - Legible: title "Karen's Window Watcher"; tree NetDDE Agent › Karen's Window Watcher › Locate / Find Next (selected) / 5.
  - Detail pane: Handle 002B0950; Module File Name C:\WINDOWS\System32\MSVBVM60.DLL; Class Name ThunderRT6CommandButton.
  - Counters: Top-Level Windows 605/188; Child Windows 18/9. Status bar: Done, 9/3/2003, 8:19 AM.
  - Pixel edges are crisp, with no interpolation blur and no aspect distortion.
  - The XP rounded top corners show the original GIF's light corner pixels against the dark ground. This is original content and was left as is.
  - No personal data, watermark, or added text. The tree shows only generic window titles.
- **720p:** Viewed `proofs/editorial-frame-720.png` (1280×720). The window title, MSVBVM60.DLL line, ThunderRT6CommandButton line, buttons and status-bar date all stay readable. The frame is balanced, with about 315 px of dark ground at each side.

## Reproduction
```
curl -s -o original.gif "https://web.archive.org/web/20030917004917id_/http://www.karenware.com:80/powertools/images/ptwinwatch.gif"
python assets/historical/XTRA-13/src/frame.py
python tools/validate_delivery.py --id XTRA-13
```
Toolchain: Windows 11 Pro 10.0.26200; Python 3.14.0; Pillow 12.3.0; curl as listed in `delivery.json`. No Cairo, browser, or font needed: no text is rendered, and no font files are included.

## Gates, blockers, and review questions
- **R14 (blocked):** Karen Kenworthy's copyright, All Rights Reserved. The site says her IP passed to her family (Terry Starr), and the site is run by Joe Winett. The only license found covers program use, not image reuse. Review question: request permission (a human sends it), make a recorded fair-use decision, or drop the image.
- **R11 (unreviewed):** VB6 provenance is documented by author statements plus runtime and source-code listings, not by appearance. Review question on fit: the image is a 2003 Windows XP capture of a 1999 VB6 utility by a Windows Magazine columnist. Does that suit narration about VB's early years and non-programmers? The asset carries no statistics or captions, and does not evidence the narration's broad claims.
- Keep this proof out of the cleared-media bin until R14 and R11 are decided.
