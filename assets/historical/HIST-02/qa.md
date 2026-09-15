# HIST-02 — VB 4.0 IDE — Production QA

**Production:** produced. **Release:** blocked (R14 rights unresolved). **Reviewer:** none yet (review deck, OPS-04).

## Outcome
Historical proof with unresolved rights. It is not editor-ready approved media. A real 1995-era screenshot of Microsoft Visual Basic 4.0 (32-bit edition, Windows 95) was acquired unmodified from WinWorld, and a full-frame 16:9 editorial copy was made. No AI recreation, mockup or retouch is involved.

## Delivered files
| Variant / role | Path | Notes |
|---|---|---|
| `original` | `source/original.png` | 800×600 palette PNG, sha256 `065820c5…bde565`, byte-identical to the WinWorld file |
| `editorial-frame` | `exports/editorial-frame.png` | 1920×1080 RGB, full original resized 1.8× (Lanczos) to 1440×1080 at x=240, black pillarbox |
| 720p proof | `proofs/editorial-frame-720.png` | 1280×720 downscale of the export, used for the 720p review |
| Source record | `evidence/source.json` | creator, title, dates, URL, access date, identity evidence, candidates, search log |
| Rights record | `evidence/rights.json` | rights holders, host terms, Microsoft permission route, review questions |
| Provenance | `evidence/provenance.json` | input line ranges and hashes, external files and page snapshots |
| Claims and gates | `evidence/claim-checks.json` | R14 gate plus version, bitness, panel and terminology checks |
| Excerpts | `evidence/source-excerpts.md` | script/plan excerpts, host captions, on-screen text, rights quotes |
| Machine checks | `evidence/render-tests.json` | output of `src/check_editorial_frame.py` |
| Page snapshots | `evidence/pages/*` | WinWorld product and copyright pages, Microsoft permissions page, acquisition HTTP headers |
| Scripts | `src/make_editorial_frame.py`, `src/check_editorial_frame.py`, `src/build_delivery.py` | deterministic reproduction |

Every file above is listed with byte size and SHA-256 in `delivery.json` (excluding `delivery.json` and `state.json`). Still asset: no duration, no fps, no motion, no named cutdowns.

## Checks actually performed
1. **Identity (version).** Verified from the host caption "Microsoft Visual Basic 4.0 32 bit - Edit" on WinWorld's VB 4.0 page, the in-image title bar "Loan - Microsoft Visual Basic [design]", and the sibling About capture reading "Microsoft Visual Basic Version 4.0".
2. **Edition (16-bit vs 32-bit).** The shown environment is **32-bit**. The sibling "32 bit - About" capture reads "For 32-bit Windows Development" on the same Windows 95 desktop, with the same window layout, at 10:41 PM against 10:43 PM in the acquired file. The "16 bit - About" capture reads "For 16-bit Windows Development" on Windows 3.1. The Edit image alone would not prove bitness, because 16-bit VB4 also ran on Windows 95; this caveat is recorded.
3. **Panels needed by XTRA-05.** All five are visible in the original and the export: toolbox, form designer, Project window, Properties window, Code window.
4. **Machine checks** (`python assets/historical/HIST-02/src/check_editorial_frame.py`, all passed). Original hash matches the source record; original is 800×600; export is a genuine 1920×1080 PNG; pillarbox columns are pure black; the image region is pixel-identical to a fresh uniform resize of the full original (no crop, stretch or retouch); re-render is byte-identical.
5. **Manual review at full size.** `exports/editorial-frame.png` was viewed whole and as four native-resolution 960×540 tiles (1:1 pixels, worker scratchpad). Title bar, menus, toolbar coordinates, Project window, Properties rows and all code lines are legible. Syntax colours are intact, the bar edges are clean, and nothing is clipped at the frame edge. Lanczos at 1.8× gives slight softening and faint ringing around high-contrast pixel text. That is acceptable for B-roll, but an integer or nearest-neighbour rescale could be chosen later without changing provenance.
6. **Manual review at 720p.** `proofs/editorial-frame-720.png` was viewed at 1280×720. Window titles, menu names, the Project window entries and the code are readable. The Properties grid values are small but readable. The IDE's gray chrome is clearly separated from the black bars.
7. **Original viewed at full size.** `source/original.png` was viewed at native 800×600. No watermark, no personal data, no serial number. The taskbar shows only "Start", the IDE task and a clock.
8. **Safe area.** The screenshot spans the full height (y=0…1080), which is outside the shared y=72…1008 text safe area. Resizing smaller to fit the safe area was not done, because it is an editorial choice and the export carries no authored text. Captions in the edit will overlap the taskbar region, and this is noted for the editor.
9. **Content hygiene.** No UI copy was added. No remote fonts, CDN assets or bundled fonts are used. No private data is committed: the sibling About captures show a serial number and were deliberately left out, recorded by URL and hash only.
10. **Validator.** `python tools/validate_delivery.py --id HIST-02`; actual output is recorded below.

## Validator output
First run, right after `python assets/historical/HIST-02/src/build_delivery.py` reported "delivery.json written with 17 outputs". The command was `python tools/validate_delivery.py --id HIST-02`, exit code 0:

```json
{
  "id": "HIST-02",
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

`python tools/validate_pack.py` also ran in the same session with exit code 0, `"errors": []`, confirming `sources/` is unchanged. Adding this output to qa.md changed its hash, so `delivery.json` was rebuilt and the validator re-run before commit; the producer's report carries that final run.

## Reproduction
From the repository root, on Windows 11 (10.0.26200) with Python 3.14.0 and Pillow 12.3.0:

```sh
python assets/historical/HIST-02/src/make_editorial_frame.py
python assets/historical/HIST-02/src/check_editorial_frame.py
python assets/historical/HIST-02/src/build_delivery.py
python tools/validate_delivery.py --id HIST-02
```

Acquisition (already done; repeat only to re-verify): anonymous HTTPS GET of the `source_url` in `evidence/source.json` with curl 8.18.0 on 2026-09-15T20:30:12Z. No renderer beyond Pillow is needed: no CairoSVG, Chromium or ffmpeg.

## Search summary
No VB 4.0 IDE screenshot exists on Wikimedia Commons or in the English Wikipedia Visual Basic (classic) article, so the ASSET_PLAN.md:89 lead does not hold for VB4. GUIdebook has no VB entries. Internet Archive VB4 books are borrow-only (gated, not used). IA software items carry disc and box scans, plus one 2024 emulator capture (candidate C2). WinWorld's 32-bit Edit capture was selected. C2 (IA VirtualBox capture) and C3 (WinWorld 16-bit Edit) are recorded with their deficiencies in `evidence/source.json`. Wayback lookups were partly unreachable; details are in the search log.

## Review questions
- **RQ-HIST-02-1 (rights):** may the WinWorld capture be used under Microsoft's published screenshot permission, crediting "Used with permission from Microsoft", under another basis, or not at all? The capturer is unknown and WinWorld grants no screenshot license.
- **RQ-HIST-02-2 (rights):** is the visible "Loan" project (LOAN.FRM, including its form graphic) third-party content under Microsoft's terms? Its authorship was not established.
- **RQ-HIST-02-3 (rights/edit):** Microsoft's terms forbid "portions of screenshots". Are XTRA-05 callouts over the full frame acceptable, and are editorial zooms or crops off-limits? If not, should a native capture be arranged instead?
- **RQ-HIST-02-4 (Writing Lead):** the SCRIPT.md:130 callout reads "Project Explorer". The VB4 screenshot shows a panel titled with the project name, and Microsoft's KB (Q136399) calls it the "Project window". The proposed change is "Project window", or keeping "Project Explorer" if later-version terminology is acceptable. War/SCRIPT.md was not edited.

## Remaining blockers
R14 rights decision only. No boundary action was taken: no accounts, payments, terms acceptance, CAPTCHAs, watermark removal or contact with rights holders.
