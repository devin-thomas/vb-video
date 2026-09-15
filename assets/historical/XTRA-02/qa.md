# XTRA-02 QA record: Period MSDN advertisement

**Production status:** produced (historical proof). **Release status:** blocked (R14 rights unresolved).
**Reviewer:** none yet. Release decision belongs to the OPS-04 review deck.

## What was delivered

| Path | Role |
|---|---|
| `source/original.jp2` | Historical original: native 300 ppi JPEG 2000 scan leaf 96 of IA item `boardwatch-1996-06`, 2489x3228, 735,141 bytes, SHA-256 `e0108c4d…3df3`. Unmodified. |
| `exports/editorial-frame.png` | Editorial framing copy, 1920x1080: whole page pillarboxed, aspect preserved, plus an authored source caption. |
| `proofs/editorial-frame-720p.png` | 1280x720 downscale used for 720p inspection. |
| `evidence/folio-showthrough.png` | Mirrored footer crop proving the page number context. |
| `evidence/framing.json` | Exact placement, scale and transformations. |
| `evidence/source.json`, `evidence/rights.json`, `evidence/provenance.json`, `evidence/claim-checks.json`, `evidence/source-excerpts.md` | Source, rights, provenance and gate records. |
| `src/render_frame.py`, `src/write_delivery.py` | Reproduction scripts. |

Subject: full-page Microsoft advertisement for the Microsoft Developer Network (MSDN) subscription and the Visual C++ Subscription, headline "Freshness dated". It ran in Boardwatch Magazine, June 1996, printed page 97, and carries a © 1996 Microsoft Corporation notice.

## Reproduction

From the repository root on Windows:

```sh
curl -s -L -o assets/historical/XTRA-02/source/original.jp2 "https://archive.org/download/boardwatch-1996-06/boardwatch-1996-06_jp2.zip/boardwatch-1996-06_jp2%2Fboardwatch-1996-06_0096.jp2"
python assets/historical/XTRA-02/src/render_frame.py
python assets/historical/XTRA-02/src/write_delivery.py
python tools/validate_delivery.py --id XTRA-02
```

The shared CairoSVG pipeline (`tools/render/*.py`) was not used. This is a raster archive frame, so no SVG is involved and no Cairo DLL is needed. `finish_delivery.py` and `qa_browser.py` were not run; the per-asset script above writes this delivery only.

### Toolchain (installed versions actually used)

- Python 3.14.0
- Pillow 12.3.0 with OpenJPEG 2.5.4 (JPEG 2000 decode) and zlib 1.3.1.zlib-ng
- curl 8.21.0 (Windows, Schannel)
- git 2.53.0.windows.1
- Microsoft Windows 11 Pro 10.0.26200
- Fonts resolved from the system, not bundled: `C:\Windows\Fonts\segoeui.ttf`, `C:\Windows\Fonts\segoeuib.ttf`

## Tests actually run

1. **Source identity.** Downloaded dimensions 2489x3228 match IA scandata leaf 96 (`origWidth 2489`, `origHeight 3228`); the neighbour leaf 95 is 2423x3222. Pillow reports `JPEG2000 (2489, 3228) RGB`. Result: pass.
2. **Source immutability.** `render_frame.py` hashes `source/original.jp2` before and after rendering and asserts equality. Output: `source_unchanged=True`, on both render runs. Result: pass.
3. **No stretch.** Placement is x=599, y=72, 722x936 at scale 0.289963. Source aspect 0.77107, placed aspect 0.77137; the only difference is rounding of width to a whole pixel (<0.05%). Page is uncropped. Result: pass.
4. **Safe area.** Page spans y=72–1008 and x=599–1321. Caption sits at x=120–~500 and ends above y=1008. All within x=120…1800, y=72…1008. Result: pass.
5. **Export dimensions.** Pillow reads `exports/editorial-frame.png` as (1920, 1080) RGB and `proofs/editorial-frame-720p.png` as (1280, 720) RGB. Result: pass.
6. **Page-number evidence.** Checked neighbouring leaves 95 and 97 on IA (BookReader previews). Printed footers read "96 Boardwatch - June 1996" and "98 Boardwatch - June 1996". The mirrored footer crop of this leaf reads "98 Boardwatch - June 1996", which is show-through from the reverse side. Conclusion: page 97. Result: pass, after correcting an early misreading of "96" from a low-resolution preview.
7. **Subject text.** Identity phrases on the page checked against IA's ABBYY OCR for object `boardwatch-1996-06_0096.djvu` ("Microsoft Developer Network (MSDN) subscription", "http://www.microsoft.com/msdn", "© 1996 Microsoft Corporation"). Result: pass.
8. **Delivery validator.** `python tools/validate_delivery.py --id XTRA-02`, verbatim result under "Validator result".

## Manual visual inspection

| View | File | What was checked | Result |
|---|---|---|---|
| Full size 1920x1080, whole frame | `exports/editorial-frame.png` | Whole page visible edge to edge, no crop of the © line, footer tagline or top nav strip; no distortion of the glass, boxes or type; keyline visible; empty right side acceptable for editor overlays | Pass |
| Full size 1:1 crop, caption column (x100–1000, y700–1080) | derived from `exports/editorial-frame.png` | Even caption leading after a spacing fix; Segoe UI renders, no fallback boxes; smallest caption line 26 px, legible | Pass (first render had uneven line gaps; fixed in `render_frame.py` and re-rendered) |
| Full size 1:1 crop, page top (x560–1360, y40–420) | derived from `exports/editorial-frame.png` | Headline and Visual Tools nav strip sharp; page top edge at y=72 not clipped | Pass |
| Full size 1:1 crop, page bottom (x560–1360, y700–1080) | derived from `exports/editorial-frame.png` | © 1996 notice and trademark line readable; Microsoft logo and tagline intact; faint mirrored show-through visible, retained as authentic, not retouched | Pass |
| 720p | `proofs/editorial-frame-720p.png` | Headline, MSDN box and caption readable; body copy soft but it is not narrated text; no aliasing on type | Pass |
| Native evidence crop | `evidence/folio-showthrough.png` | Mirrored folio readable as "98 Boardwatch - June 1996" | Pass |

Content checks:
- No private information in the frame.
- No remote font or CDN; no network at render time.
- No invented ad copy; the only authored text is the caption, recorded in `evidence/provenance.json`.
- No modern Microsoft graphics.
- No watermark removal or retouching.

## Remaining blockers and review questions

- **R14 (blocked).** Third-party copyrighted ad (© 1996 Microsoft Corporation); no licence on record (details in `evidence/rights.json`). Question RQ-XTRA-02-1: fair-use judgement, permission, or drop?
- **RQ-XTRA-02-2 (choice).** This ad is MSDN plus Visual C++, not Visual Basic, and it ran in a BBS/ISP trade magazine rather than a developer title. Is it acceptable for "old MSDN ads"? The alternative is the VB-inclusive Microsoft Visual Tools ad in the same issue (leaf 16). That one is the second page of a spread and MSDN is a minor element in it.
- **RQ-XTRA-02-3 (choice).** Keep the burned-in source caption in the editorial frame, or have the editor supply a lower-third? The page placement leaves room either way.

## Validator result

`python tools/validate_delivery.py --id XTRA-02` (exit 0), run after `src/write_delivery.py`:

```json
{
  "id": "XTRA-02",
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

Adding this section changes qa.md's hash, so `write_delivery.py` and the validator were run again before commit. The final run's output is the same as above. The validator checks structure and hashes only; it does not certify the image content or the rights.
