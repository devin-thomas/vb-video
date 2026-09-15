# HIST-12 QA: Borland Delphi 1.0 IDE

**Outcome: produced.** The candidate located by the earlier blocked record was acquired byte-exact, verified against the Wayback CDX digest, inspected at full resolution, and framed for 1920x1080. Release stays **blocked** on R14: the image is unlicensed Borland copyright material.

- Production status: produced
- Release status: blocked (R14, review question RQ-1)
- Worker: HIST-12 worker under the Historical Screenshots Manager (session vb-20), 2026-09-15
- Reviewer: none (release approval comes from the OPS-04 review deck)
- Resumed from: commit `94f4073` on `ticket/HIST-12` ("HIST-12: blocked candidate record"). The documented search, the three ranked candidates and all evidence from that commit were kept, not redone.

## What changed since the blocked record

The earlier worker correctly refused to download the candidate without Devin's explicit approval. Devin has since approved it in chat (relayed by the manager). Everything below follows from that one unblocked step.

| Then | Now |
|---|---|
| C1 located, not downloaded | C1 acquired, byte-exact, SHA-1 verified (`source/original.gif`) |
| Image never viewed; identity rested on the vendor page alone | Viewed at native 444x282 and at 2x; identity and the Delphi 1 / 16-bit reading confirmed from the pixels |
| No export, no delivery.json | `exports/editorial-frame.png` (1920x1080), `proofs/editorial-frame-720.png`, `delivery.json` |
| SCRIPT.md:621 "looks a lot like the VB IDE" unjudgeable | Judged against HIST-01 and HIST-02: accurate as written, no script change proposed |
| R14 blocked | R14 still blocked. Acquiring the file added no licence evidence. |

C2 (User's Guide PDF) and C3 (1995 brochure PDF) were approved as fallbacks but were **not** downloaded, because C1 proved usable. Nothing outside the approved list was fetched.

## Acquisition

Exact command run (from the repository root; the file was fetched to scratch and copied into place):

```
curl -sS -L --connect-timeout 30 --max-time 180 --retry 5 --retry-delay 20 --retry-all-errors \
  -A "Mozilla/5.0" \
  -o source/original.gif \
  "https://web.archive.org/web/19961223104420id_/http://www.borland.com:80/delphi/delphi1.0/guide/fig1.gif"
```

Result: `HTTP=200 SIZE=35163 TYPE=image/gif`, first attempt, no retry needed, no rate limiting encountered. A generic `Mozilla/5.0` User-Agent was used; nothing identifying was sent. No account, payment, terms acceptance, CAPTCHA or access control was involved.

**Integrity.** The payload is 35,163 bytes, not the 35,423 in the CDX `length` field — CDX `length` is the compressed WARC record length, not the payload length. The authoritative check is the digest, which is computed over the payload:

| Measure | Value |
|---|---|
| SHA-1 (base32) | `3AB42XGSKUFD5LQFFJKPEE5IAHFCWKPW` — **matches the CDX record exactly** |
| SHA-1 (hex) | `d803cd5cd2550a3eae052a54f213a801ca2b29f6` |
| MD5 | `f1cc0ec6a7a233bfa60cef6ec896e4b2` |
| SHA-256 | `467a198503033616d228194120846f2d7dcd364e4b5911589ef7ce963f14314a` |
| Format | GIF87a, 444x282, 16-colour palette, single frame |

The same digest appears on both Wayback captures of this URL (1996-12-23 and 1997-05-09), so the two captures are the same bytes. The file in `source/` is unmodified.

The host page capture (`guide/8.1.1.4.html`) was re-fetched and re-hashed: 8,533 bytes, sha256 `bc0b1abd…35339a`, identical to the value the earlier worker recorded. It is deliberately **not** committed — it is Borland copyright HTML and the hash is enough to prove the same capture.

## Identity and version, verified at full resolution

The image contains no version number, so identification has two legs and both were checked.

**Documentary.** Borland's own archived page, titled "Delphi 1.0 Reviewer's Guide: Quick Tour of Delphi", links this exact file, captions it "Delphi, a visual development environment and two-way tool", and says the startup environment contains a customizable speedbar, component palette, Object Inspector, form design area and code window.

**Visual.** All five are present, and the transcription is in `evidence/source-excerpts.md`: main window `Delphi - Project1`; menu `File Edit Search View Compile Run Options Tools Help`; a two-row speedbar; a tabbed component palette; a floating `Object Inspector` with selector `Warning: TButton`, an alphabetical property grid and `Properties` / `Events` page tabs; a `Form1` design window with a dotted alignment grid and a selected TButton captioned `Warning`; and a `UNIT1.PAS` code window showing `TForm1 = class(TForm)`.

**Delphi 1 (16-bit), not a later release with the number cropped out** — two independent markers:

1. Windows 3.x window chrome throughout: control-menu box at the left of each title bar, minimise/maximise triangle pair at the right, no Windows 95 close button, no taskbar. Delphi 2 onward is 32-bit and ships into Windows 95 chrome.
2. The component palette's page tabs read `Standard  Additional  Data Access  Data Controls  Dialogs  System  VBX  Samples`. The **VBX** tab belongs to the 16-bit Delphi 1 line; the 32-bit successors use OCX/ActiveX.

No watermark, logo overlay, archive banner or added caption is present at native resolution or at 2x. Nothing was removed.

## Framing

`exports/editorial-frame.png` is an **uncropped 3x integer nearest-neighbour upscale** (444x282 → 1332x846) centred at (294,117) on a flat RGB(32,34,38) matte in a 1920x1080 canvas.

Why not scale to fill the safe area: the exact fit would be 3.319x, and a fractional LANCZOS resample of a 16-colour image with one-pixel window borders and a 6px bitmap UI font blurs exactly the detail the shot exists to show. An integer nearest-neighbour factor maps each source pixel to a 3x3 block, so no detail is invented and none is lost.

Measured (`src/framing-result.json`): aspect error **0.000%**, `cropped: false`, `reversible_bit_exact: true`. Reversibility is not asserted, it is enforced — `build_frame.py` decimates the placed region back to 444x282 and refuses to write any output unless the raster is byte-identical to the original.

Nothing was added: no text, no UI, no retouching, no colour grading, no sharpening. The dark matte is an authored production ground and is recorded as such in `evidence/provenance.json`.

## Editorial gate work

**R14 — blocked, worked not cleared.** Rights holder at creation: Borland International, Inc. No licence or permission exists for this file. The archived 1996 borland.com notice prohibits copying material from the site elsewhere for further reproduction or redistribution except as otherwise provided. Acquiring the file added no licence evidence — the image carries no copyright notice, no licence text and no attribution mark, and an absent notice is not a licence. The current rights holder was not established. No fair-use assessment was made; that is a legal question, not an agent decision. Evidence: `evidence/rights.json`. Review question **RQ-1**.

**SCRIPT.md:621 — "It looks a lot like the VB IDE" — checked, accurate, no change proposed.** The earlier worker could not judge this without the image. Judged now at full resolution against the project's own VB IDE assets, the HIST-01 (VB 1.0, Windows 3.x) and HIST-02 (VB 4.0, Windows 95) exports on `main`. The resemblance is structural, not incidental: all three are non-MDI layouts of separate floating windows on the desktop, with a thin top strip holding the menu and toolbar; a separate form-design window carrying a dotted alignment grid and a selected control drawn with black square sizing handles; a separate code window showing that control's event handler; and a component library presented as a palette of small icon buttons. HIST-02 additionally shares the alphabetical Name/Value property grid with the selected object named above it. The sample content even rhymes — a selected button with its click handler open. Against HIST-01 the match is closest, since both sit in identical Windows 3.x chrome.

Recorded for completeness, not as an objection: the parts are arranged differently. VB floats its Toolbox as a vertical palette at the left where Delphi docks a tabbed palette in the top strip; Delphi's Object Inspector has an Events tab where VB reaches events through the code window's Proc dropdown; VB shows a project window with no visible Delphi 1 counterpart. None of that contradicts a claim of family resemblance, and the narration does not say the layouts are identical. **No material change to War/SCRIPT.md is warranted, and War/SCRIPT.md was not edited.**

## Tests actually run

| Test | Result |
|---|---|
| Acquisition integrity — payload SHA-1 base32 vs CDX digest | **passed**, exact match `3AB42XGSKUFD5LQFFJKPEE5IAHFCWKPW` |
| Host page capture re-fetched and re-hashed | **passed**, 8,533 bytes, sha256 matches the recorded value |
| GIF decode, dimensions, frame count, palette | **passed**, 444x282, 1 frame, 16 colours, GIF87a |
| Identity/version read at native resolution and 2x | **passed**, see above |
| Watermark / added-mark check | **passed**, none present |
| Export dimensions and aspect | **passed**, 1920x1080 RGB; placed 1332x846 at (294,117); aspect error 0.000% |
| Framing reversibility (bit-exact decimation back to the original raster) | **passed**, enforced in `build_frame.py`; `reversible_bit_exact: true` |
| Manual visual review at full size (1920x1080) | **passed**, see below |
| Manual visual review at 720p (1280x720) | **passed**, see below |
| JSON parse check of every `*.json` in this folder | **passed** |
| `python tools/validate_delivery.py --id HIST-12` | **passed**, actual output quoted below |

### Manual visual review

**Full size — `exports/editorial-frame.png` (1920x1080), viewed at 1:1.** The IDE sits centred with even matte on all four sides. Every element is sharp and square-edged; the 3x blocks read as period pixel art rather than as blur. Legible: the menu bar, all eight palette tab names including `VBX`, every Object Inspector property name and value, the `Warning: TButton` selector, the `Properties`/`Events` tabs, the form's `Warning` button caption and its eight sizing handles, the full Object Pascal body in `UNIT1.PAS`, and the `28 1 Modified Insert` status strip. The light band running below the code window to the right edge of the Form1 window is present in the original raster (the form window's own client area), not an artefact of framing. No clipping, no stretching, no added marks.

**720p — `proofs/editorial-frame-720.png` (1280x720), viewed at 1:1.** Still legible at the level the cutaway needs: menu bar, palette tab names, Object Inspector rows, the button caption and the Pascal source all read cleanly. The smallest text (the status strip, the `Properties`/`Events` tab labels) softens but stays identifiable. Nothing is lost that carries the shot's meaning.

## Toolchain

- Windows 11 Pro 10.0.26200 (`Windows-11-10.0.26200-SP0`), Git Bash
- Python 3.14.0
- Pillow 12.3.0
- curl 8.18.0 (x86_64-w64-mingw32), libcurl/8.18.0, Schannel
- No installs performed, no fonts distributed, no renderer/CDN dependency. `CAIROCFFI_DLL_DIRECTORIES` was not needed: this asset uses Pillow only, not the Cairo/SVG toolchain.

## Exact reproduction

From the repository root:

```
curl -sS -L --connect-timeout 30 --max-time 180 --retry 5 --retry-delay 20 --retry-all-errors \
  -A "Mozilla/5.0" -o assets/historical/HIST-12/source/original.gif \
  "https://web.archive.org/web/19961223104420id_/http://www.borland.com:80/delphi/delphi1.0/guide/fig1.gif"
python assets/historical/HIST-12/src/build_frame.py
python assets/historical/HIST-12/src/make_delivery.py
python tools/validate_delivery.py --id HIST-12
```

`build_frame.py` is deterministic and writes both `exports/editorial-frame.png` and `proofs/editorial-frame-720.png`.

## Validator output

`python tools/validate_delivery.py --id HIST-12`, actual output:

```
{
  "id": "HIST-12",
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

Exit code 0. Note the validator's own limitations: it certifies structure, paths, sizes and hashes, not the rights position and not the visual judgment. Both of those are recorded above by hand.

(Order of operations: `make_delivery.py` inventories `qa.md`, so it was re-run after this block was pasted in, and the validator was then re-run against the updated inventory with the same result.)

## Remaining blockers

1. **R14 rights (RQ-1).** Unlicensed Borland copyright. Release stays `blocked`; keep this out of the cleared-media bin until the review deck records a decision.

## Review questions

1. **RQ-1 — Rights (R14).** May the video use this 1995 Borland International marketing screenshot of the Delphi 1.0 IDE — acquired byte-exact from the Wayback Machine, Borland copyright, no licence found, site notice prohibiting reproduction for redistribution — under an editorial/commentary rationale, with the proposed credit "Borland International, Inc. — Delphi 1.0 Reviewer's Guide (1995), via the Internet Archive Wayback Machine"? Or does HIST-12 stay blocked, or get replaced by a clearly labelled original reconstruction? No agent clearance has been given.
2. **RQ-2 — Presentation, for the editor.** The only authentic Delphi 1.0 workspace image on an authorised route is a 444x282 16-colour web GIF. It is shown at an exact 3x integer upscale on a matte, so it does not fill the frame and shows period pixel structure. Confirm this is acceptable for the section-13 cutaway, or ask for a different treatment (for example a tighter reversible crop on the Object Inspector and code window). Text stays legible at 720p.

There is **no** open question about SCRIPT.md:621 — it was checked and is accurate as written.
