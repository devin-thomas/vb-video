# OPS-01 — Production QA

**Production:** produced. **Release:** unreviewed (revision 2, 2026-09-16; the 2026-09-15 approval covered the 1.0.0 faces and does not carry over).

## Revision 2 — regular card faces (win95-workbench-1.1.0)

Devin's review of the first cut (note 17): every shared card face drew one centre pip, so every rank read as an ace at a glance (15:58 in DIA-06). The `card()` primitive in `tools/render/studio.py` now draws regular playing cards and the 52 faces, the atlas and the version were regenerated from it.

- Corner index: rank over a small suit in the top-left, and the same pair rotated 180° in the bottom-right (1.0.0 rotated only the rank). Font sizes, offsets, colours (`#b53b34` red, `#172128` black, `#fbfaf4` face, `#c9c7bd` edge), the 164 × 226 viewBox, the 144 × 202 body, the shadow and the back are unchanged.
- 2–10: standard pip layout. 2 top and bottom centre; 3 a column of three; 4 corners; 5 corners plus centre; 6 two columns of three; 7 six plus one upper centre; 8 six plus upper and lower centre; 9 two columns of four plus centre; 10 two columns of four plus two centre pips. The upper half is authored and the lower half is the same set rotated 180°. The side columns sit just clear of the corner suit; pip size is 22 % of the width for 2–5, 20 % for 6–8 and 18 % for 9–10.
- J, Q, K: a large letter (34 % of the width) between an original vector court mark above (J a cap with visor and button, Q a two-arched coronet with pearls, K a five-point crown with balls) and one small suit pip below. No copied art.
- A: unchanged, one large centre pip.
- Cards narrower than 110 px (the 57, 78, 90 and 108 px sizes used in DIA-08, DIA-09, DIA-05 and CARD-01) keep the top-left rank, the pips or court mark and pip, and drop the rotated corner and court letter, as 1.0.0 dropped the corner suit at those sizes. Their pips are 14 % of the width.

## Delivered
Each required media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. Existing outputs are real rendered media, not placeholder filenames. The original source brief and code remain unchanged.

- `assets/shared/cards/*.svg` — 52 faces plus `back.svg`, regenerated; `evidence/card-checks.json` records the 52 distinct SHA-256 values.
- `assets/shared/card-atlas.svg` and `exports/card-atlas.png` (1920 × 1080) — atlas cells are now 116 × 163 so the atlas shows the full-size (≥ 110 px) treatment that the diagrams and mockup use; 1.0.0 used 103 × 145 cells.
- `assets/shared/VERSION.json` — `win95-workbench-1.1.0`.
- `proofs/card-atlas-720p.png` (1280 × 720) and `proofs/card-sizes.svg/.png` (1920 × 1080: 10S, 9H, KD, QC, JS, AH at 57, 72, 90, 126 and 144 px wide on felt).
- `exports/template-contract.md` — heading and card paragraph updated to 1.1.0; `assets/shared/README.md` likewise.

## Checks actually performed
- Generator: 52 identities asserted unique and 52 distinct face SHA-256 values asserted after writing (the scratch script mirrors the card section of `finish_delivery.py ops()`; that function was not run because it also rewrites REBUILD.md, template-contract.md, capabilities.json and other tickets' state files and still carries the 1.0.0 version string).
- Rasterization with CairoSVG 2.9.1 (MSYS2 Cairo via CAIROCFFI_DLL_DIRECTORIES); PNG headers checked: card-atlas.png 1920 × 1080, card-atlas-720p.png 1280 × 720, card-sizes.png 1920 × 1080. Fonts resolved by fontconfig to Liberation Sans Regular/Bold and DejaVu Sans Mono; no font files distributed; the only URL in any generated SVG is the SVG namespace.
- Manual visual review, full size (card-atlas.png viewed at 1920 × 1080 and individual faces at 4×): every 10 shows two columns of four plus two centre pips, every 9 two columns of four plus a centre pip, 2–8 match the standard layout, the lower halves are rotated, J/Q/K show cap/coronet/crown with the letter and a suit pip, aces keep the single large pip. No pip touches the corner index or suit.
- Manual visual review, 720p (proofs/card-atlas-720p.png): 10s, 9s and courts remain distinguishable from each other and from the aces.
- Manual visual review, diagram sizes (proofs/card-sizes.png): at 72 px the rank in the corner is readable and the pip count is countable; at 57 px the rank is readable and the pips read as a cluster that no longer resembles an ace; at 90 px courts show mark and pip without the letter, as designed.
- `python tools/validate_delivery.py --id OPS-01` run after delivery.json was rebuilt; result recorded in the completion report.
- Not performed: the browser/seek checks (OPS-01 is a still support ticket) and re-rendering of any dependent asset.

## Assets that carry a local copy of the faces (re-render dispatch list)
Confirmed by grepping each ticket's `src/*.svg` for the suit glyphs ♠♥♦♣; no other `src/` folder contains them. Each asset inlines the faces in its own scene SVGs, `index.html`, PNG exports and (where present) MP4s, so all of them still show the 1.0.0 single-pip faces until rebuilt with `build_assets.py` and `render_assets.py --id <ID>`.

| Ticket | src SVGs with faces | Card sizes used | Exports to refresh |
|---|---|---|---|
| DIA-02 | 17 | 170, 152 and 117 px (+ backs) | PNG + MP4 (11 files) |
| DIA-03 | 3 | 126 px | PNG (3) |
| DIA-05 | 10 | 140 and 90 px | PNG + MP4 (6) |
| DIA-06 | 19 | 151 px | PNG + MP4 (5) |
| DIA-07 | 56 | 186 px | PNG + MP4 (5) |
| DIA-08 | 26 | 128, 117 and 57 px (+ backs) | PNG + MP4 (8) |
| DIA-09 | 23 | 78 px (+ backs) | PNG + MP4 (5) |
| CARD-01 | 6 | 108 px (small mode: AS and 4H in the title dialog) | PNG + MP4 (5) |
| MOCK-01 | 4 | 165 px (+ backs) | PNG (4) |

Also outside any ticket folder, from the earlier flat layout mapped to the same GitHub issues in `tools/github_issues.py`: `assets/diagrams/card-rank-chart.svg`, `assets/diagrams/war-mechanic-steps.svg`, `assets/diagrams/array-as-queue.html`, `assets/diagrams/deck-building-loop.html`, `assets/diagrams/fisher-yates-shuffle.html`, `assets/diagrams/war-rules-animation.html`, `assets/mockups/vb4-war-gui.html`, `assets/slides/title-card.html`. They were not touched.

## Reproduction
From the repository root with `CAIROCFFI_DLL_DIRECTORIES` pointing at the Cairo DLL folder: `python tools/render/finish_delivery.py --ops-only` regenerates the cards, atlas and VERSION.json from `studio.py`, but its `VERSION` constant (and the one in `build_assets.py`) still says `win95-workbench-1.0.0` and it also rewrites REBUILD.md, template-contract.md and capabilities.json, so bump those constants first (they are outside OPS-01's write paths). Read tools/render/REBUILD.md first. Tool versions for this revision: the toolchain in delivery.json; the original batch's environment stays in exports/capabilities.json.

## Remaining decisions
No assigned claim gate. Producer publication approval of the new faces is not assumed. Review questions for the producer:

1. Both corners now carry the small suit under the rank (1.0.0 rotated only the rank into the bottom-right corner). Keep, or revert to rank-only in the rotated corner?
2. The atlas cell size changed from 103 × 145 to 116 × 163 so the atlas shows the full treatment; the 1.0.0 atlas showed the small-card mode.
3. `tools/render/finish_delivery.py` and `tools/render/build_assets.py` still hardcode `win95-workbench-1.0.0`; the next full finish run would write 1.0.0 back into VERSION.json unless they are bumped.

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- Shared system only; no .NET captures or historical verification.
- Dependent assets were not re-rendered by this ticket; the producer dispatches their rebuilds.
