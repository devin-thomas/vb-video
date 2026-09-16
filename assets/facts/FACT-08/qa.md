# FACT-08 — Production QA

**Production:** produced. **Release:** unreviewed.

## Delivered
Each media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. `exports/poster.png`, `exports/comparison.png` (byte-identical to the poster; same authored state) and `exports/step-focus.png` are real 1920 × 1080 renders; `proofs/poster-720.png` is the 1280 × 720 proof. Sources are `src/scene.svg`, `src/scene-0000.svg`, `src/variant-comparison.svg`, `src/variant-step-focus.svg`, the offline `src/index.html`, `src/build.json`/`src/timeline.json`, and `src/compose.py`, which authored all of them. `src/cells.json` records the verbatim copy and the check result per column.

## Copy and its check against the captures
The two columns are the script cue (War/SCRIPT.md:625–626) word for word, with the ticket's labels "Run 1 · 617 rounds" (TERM-04) and "Run 4 · 2,008 rounds" (TERM-02) in place of the capture IDs. Each step is on its own line with a drawn arrow as the connector; the final step is emphasised.

`src/compose.py` checked both sequences against the captured stdout (`assets/captures/TERM-04/source/stdout.txt`, `assets/captures/TERM-02/source/stdout.txt`); every line is cited in `evidence/source-excerpts.md`, and the derivation is in `evidence/endgame-check.json`:

| Column | Read directly from stdout | Reconstructed from the transcript |
|---|---|---|
| Run 1 · 617 rounds | line 1289 both play a 10; line 1291 "Player 2 has no cards left for the war - Player 1 takes the pot."; line 1295 total 617 | Player 2 held 2 cards (Player 1 50) going into round 617 → burn min(3, 1) = 1 → empty → pot 2 + 2 × 1 = 4 |
| Run 4 · 2,008 rounds | line 4157 both play an 8; line 4159 "Player 1 has no cards left for the war - Player 2 takes the pot."; line 4163 total 2008 | Player 1 held 3 cards (Player 2 49) going into round 2008 → burn min(3, 2) = 2 → empty → pot 2 + 2 × 2 = 6 |

Hand sizes are not printed by the program; they are reconstructed by replaying every "wins the round (N cards)" line from the 26/26 deal (each side contributes half of any pot, because Program.vb:264 burns the same count from both hands). Both reconstructions equal the script cue step for step, so the card keeps the script wording and no disagreement is raised.

## Checks actually performed
- `python assets/facts/FACT-08/src/compose.py`: reconstructs both endgames, asserts the final round is a tie that ends with a "no cards left" line and that the total-rounds line equals the labelled round, compares the derived steps with the script cue (both match), and checks every text run against the safe area (x 120…1800, y 72…1008) with the studio font metrics. Passed.
- `python tools/render/render_assets.py --id FACT-08` (CairoSVG 2.9.1, Pillow 12.3.0, Python 3.14.0, `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` as an environment variable): poster, both variants, 720p proof and contact sheet rendered; `evidence/render-tests.json`. PNG sizes re-checked with PIL: 1920 × 1080 for all exports, 1280 × 720 for the proof.
- Offline Chromium checks (the logic of `tools/render/qa_browser.py`, run so that it writes only `evidence/browser-tests.json`; the shared script also rewrites review/browser-summary.json outside this ticket's paths): Chromium 153.0.8010.12, in-memory HTML, deterministic `renderAt`, 4 SVG files, 56 text boxes all inside the canvas, no network request. Passed.
- Manual visual review by the worker, at full size and at 720p: `exports/poster.png`, `exports/step-focus.png`, `proofs/poster-720.png` (and `exports/comparison.png` confirmed byte-identical to the poster by SHA-256). The two columns share one baseline grid: "2 cards" / "3 cards", "play 10" / "play 8", "burn 1" / "burn 2", "empty" / "empty", "4-card pot" / "6-card pot" sit on the same rows; the final step is bold blue; `step-focus` boxes the final steps and dims the earlier ones. Readable at 720p.
- `python tools/validate_delivery.py --id FACT-08`: passed (`"ok": true`, no errors) after delivery.json was written.

## Reproduction
From the repository root, with `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` set as an environment variable (fontconfig's `fc-match` from MSYS2 on PATH resolves Liberation Sans / DejaVu Sans Mono from C:\Windows\Fonts):

```sh
python assets/facts/FACT-08/src/compose.py
python tools/render/render_assets.py --id FACT-08
python tools/validate_delivery.py --id FACT-08
```

Do not run `tools/render/build_assets.py` for this ID; the shared authoring script does not know this asset, and `finish_delivery.py --id` writes outside the owned paths (ticket file, review index). Tool versions: the toolchain in delivery.json.

## Remaining decisions
No R gate is assigned. Review questions (in `evidence/claim-checks.json`):
1. No capture disagreement was found; the derived hand sizes, burn counts and pot sizes are reconstructions from the transcript and Program.vb:264, recorded line by line, not lines the program printed.
2. The card carries a kicker ("When the cards run out", the script's section 12 title, War/SCRIPT.md:580) and the ticket title above the two verbatim columns; drop either if the cut wants the columns alone.

No narration sync, sound design, final video assembly or full independent editorial clearance is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- The arrows are drawn connectors (studio `arrow`), not the "→" glyph, so the render does not depend on a font's arrow coverage; the verbatim cue text with its arrows is kept in `src/cells.json` and `evidence/source-excerpts.md`.
