# HIST-19 QA — Windows 3.1 Solitaire

- **Production status:** produced
- **Release status:** blocked (R14 rights review outstanding)
- **Checked by:** the HIST-19 worker, 2026-09-15. A human reviewer is still needed, via the review deck.

## Deliverables and variants

| Variant | File | Notes |
|---|---|---|
| `original` | `source/original.png` | Internet Archive original: 1920×1080 RGBA PNG, 1,202,332 bytes, SHA-256 `07fd42480f9bc4f926724703111235cc47ddfdfe479cad1b077db16c10424c1c`. It shows the capturer's whole host desktop. **Not for on-screen use.** |
| `editorial-frame` | `exports/editorial-frame.png` | 1920×1080 still. The 640×480 guest screen, scaled 2× nearest-neighbour, pillarboxed on #111318. |
| (proof) | `qa/editorial-frame-720p.png` | 1280×720 downscale, used only for the 720p review. |

- **Duration:** none. This is a still, held for editorial timing, with no motion or cutdowns.
- **Proposed placement:** script section 12, visual cue at `SCRIPT.md:579`.

## Reproduction

Run from the repository root:

```sh
python assets/historical/HIST-19/src/frame.py
```

- The script refuses to run unless `source/original.png` has the recorded SHA-256.
- Original acquisition, an anonymous public download:

```sh
curl -L -o original.png "https://archive.org/download/solitaire-windows-3.1/Solitaire%20(Windows%203.1).png"
```

- Toolchain:
  - Python 3.14.0
  - Pillow 12.3.0
  - curl 8.18.0 (x86_64-w64-mingw32)
  - Windows 11 (10.0.26200)
- Cairo, a browser and ffmpeg were not needed.

## Tests actually run

1. **Download integrity.** The downloaded file's SHA-1 `d5f767d4c4d43020bb681035daf29e6ca2e6da0b` and MD5 `2ae802371d5d7529ce5bd62825a20b5d` equal the checksums in the Internet Archive files metadata. The repository copy is byte-identical to the download (compared in Python).
2. **Alpha.** The original's alpha channel is 255 everywhere, so flattening to RGB loses nothing. `frame.py` asserts this.
3. **Crop bounds.** A pixel probe put VirtualBox chrome at x=554 and x=1195, and at y=200 and y=681. The guest display is therefore exactly (555,201)–(1195,681), 640×480.
4. **Reversible mapping.** Every one of the 1,228,800 image pixels in the frame equals original pixel (555+⌊(x−320)/2⌋, 201+⌊(y−60)/2⌋). Result: 0 mismatches.
5. **Pillarbox purity.** Every pixel outside the image rectangle is exactly #111318. Result: 0 exceptions.
6. **Determinism.** Two consecutive renders gave identical files:
   - `exports/editorial-frame.png`: `f23b7cfb696a97aa61620a4e3970884599bc514de34b7c379fd98b482998026a`
   - `qa/editorial-frame-720p.png`: `f2094145e5462e3da811091fbe03825a4dd7e38e77428efaf1b025d243516369`
7. **Output sizes.** The frame is 1920×1080 RGB; the proof is 1280×720 RGB (checked with Pillow).
8. **JSON syntax.** `evidence/source.json`, `rights.json`, `provenance.json` and `claim-checks.json` all parse.
9. **Privacy check on stored records.** The redacted `evidence/source-page/*.json` files contain no uploader e-mail address (asserted during generation).
10. **Delivery validator.** The actual output is below.

## Manual visual inspection

**Original, viewed at full 1920×1080:**
- The guest window titled "Solitaire" shows a Game/Help menu, a green playfield, Queens on all four foundations, four Kings on the tableau, and the status bar "Score: 383 Time: 311".
- The host desktop around it shows personal folder names, a Windows 11 taskbar dated 3/05/2025, and third-party anime wallpaper artwork. It also shows the VirtualBox Manager list with the VM named "Windows 3.1" running and the window title "Windows 3.1 [Running] - Oracle VirtualBox".

**Editorial frame, viewed at full 1920×1080:**
- The whole guest screen is visible and none of the host desktop or VirtualBox chrome remains.
- No text has been added.
- Pixels are crisp, with no smoothing.
- The title "Solitaire", the Game/Help menu and the score line are legible.
- 1:1 zooms of the title-bar and status-bar regions were checked.

**Editorial frame, viewed at 720p:** the title, menu, card ranks and suits, and score line are still legible, and no aliasing artefacts distract.

**Content notes for the editor.** These are properties of the source; nothing here was altered.
- The Solitaire window is larger than the 640×480 guest screen, so its right and bottom edges run past the screen edge.
- A mouse pointer sits at the top right of the playfield.
- A second window's red frame shows behind the title bar.
- The guest uses a non-default colour scheme (black title bar, red frame) and a cyan patterned wallpaper, which is not the stock Windows 3.1 look.

**Safe area.**
- The image spans y=60–1020, which is 12 px beyond the proposed text-safe band at the top and bottom.
- Only incidental screen content sits there. The one piece of text in that zone is the in-game score line, at y≈994–1018.
- If captions sit low, it can be covered without losing meaning.

## Content and authenticity checks

- **Product:** Microsoft Solitaire, verified visually.
- **Windows 3.1 identity:** supported only by the capturer's labels, meaning the file name and VM name. No in-guest version string is visible, and the capturer's own Windows 3.0 capture shows those VirtualBox labels can be misleading. Details are in `evidence/claim-checks.json`.
- **Not a period screenshot:** it is a 2025 emulator capture of 1990s software, classified as a historical source (modern emulator capture).
- **Written in VB?** Nothing in the frame implies it. There is no caption.
- **Other checks:** no watermark, no AI generation or upscaling, no fabricated UI, no remote fonts or CDN, no private information in the export.

## Gates and dependencies

- **R14:** blocked, with the rights record complete and the clearance question open. See `evidence/rights.json` and `evidence/claim-checks.json`.
- **OPS-01 (integration dependency):** not consumed by this still. It uses no shared template, fonts or styles, only the bible's #111318 token as a flat background. Final framing against the shared safe-area template can be rechecked once OPS-01 is produced.

## Review questions

1. **Rights (R14).** May this capture appear on screen?
   - Microsoft's screenshot guideline allows videos but forbids "portions" and third-party content. The frame crops a host capture down to the full Windows 3.1 guest screen.
   - Alternatives are to rely on fair use / fair dealing commentary, or to drop the shot.
2. **Capture-layer permission.** The capturer's collection says any use is fine and credit is preferred.
   - Is that enough?
   - Or should the capturer be asked for written permission before release?
3. **Version labelling.** Is the capturer-labelled "Windows 3.1" acceptable for an on-screen caption, or should captions say only "Windows 3.x Solitaire"?
4. **Writing Lead: script wording.** The visual cue at `SCRIPT.md:579` (`War/SCRIPT.md:636`) groups Solitaire under "90s shareware card games".
   - Microsoft Solitaire shipped with Windows (Windows 3.1 User's Guide, April 1992, p.73), and the narration at line 593 already says "bundled".
   - Proposed change: reword the cue so Solitaire is not labelled shareware.
   - `War/SCRIPT.md` was not edited.

## Remaining blockers

- Release is blocked on review questions 1–2 (R14).
- There are no production blockers.

## Validator output

`python tools/validate_delivery.py --id HIST-19` exited with code 0. It was re-run after this section was filled in and `delivery.json` re-hashed.

```json
{
  "id": "HIST-19",
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

The validator checks structure, hashes and PNG size only. It does not clear rights or confirm historical accuracy.
