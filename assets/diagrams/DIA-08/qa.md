# DIA-08 — Production QA

**Production:** produced. **Release:** unreviewed (revision 2, 2026-09-16; the 2026-09-15 approval covered the generic sequence with the 1.0.0 card faces and does not carry over).

## Revision 2 — card faces and the `endgame` cutdown

Devin's approval of proposal 4 in review/cut-notes-2026-09-16.md (25:43): the endgame walk-through needs the real numbers on screen, panels landing on the words, and every card face is now the OPS-01 1.1.0 regular playing card.

1. **Generic war sequence re-rendered, otherwise unchanged.** All 23 states, the four-panel poster and the three named variants were regenerated from `tools/render/diagrams.py war_mechanic()` through `build_assets.save_assets({'DIA-08'})`, so the only change is the `card()` primitive (corner index, standard pip layouts). Timeline, cuts, copy, fixture and counts are identical to revision 1 (`src/build.json` and `src/timeline.json` frames unchanged; scene-0022, the final state with no face-up card, is byte-identical).
2. **`endgame` cutdown added** (`exports/endgame.mp4`, 42 s, 1260 frames, plus the four-panel still `exports/endgame.png`; sources `src/endgame-0000…0014.svg`, `src/variant-endgame.svg`, `src/endgame.html`, authored by `src/endgame.py`). Round 617 of the first recorded run in four stages with the counters on screen: (1) Player 2 has 2 cards, Player 1 has 50, pot 0; (2) both play a 10 — 10♦ against 10♠ — tie, war: 49 / 1, pot 2; (3) both burn 1 face-down, all Player 2 can spare: 48 / 0, pot 4; (4) Player 2 cannot flip, Player 1 takes the 4-card pot, moved one at a time in pot order: 52 / 0, pot 0, then the program's own lines 1291 and 1294 held to the end. Stage 2 carries two sub-states for the narration's aside (ghost slots for "normally: burn 3 face-down, then flip 1" at 7.33 s; Player 2's last card highlighted for "only had 1 card left" at 11.88 s) and stage 3 two ("hand was empty" at 29.17 s; "back to the top of the loop" at 32.05 s). Burn identities are not printed by the program, so the burns are face-down. The Player 1 pile is a stack of at most eight backs with the exact counter; Player 2's pile is drawn card for card.
3. **Numbers verified against the capture**, not the ticket text: `assets/captures/TERM-04/source/stdout.txt` line 5 (26 / 26 dealt), lines 1289–1291 (the 10s, the war, line 1291), lines 1293–1297 (winner, 617 rounds); the 50 / 2 split is not printed and was replayed from lines 7–1288 (script below). The capture agrees with the ticket's numbers. Quoted lines are in `evidence/source-excerpts.md`.
4. **Word timing.** `key_second` 6.5 is the second at which the two tens are face-up; `tools/assembly/build_timeline.py` lands it on "tie, war" in S12-B03 (word 20 of 51 in a 21.12 s take: 8.28 s into the beat, so the cutdown starts 1.78 s into S12-B03). The other stages are placed by the same proportional word timing across the beat gap (0.45 s) into S12-B04 (21.28 s take): stage 3 on "so both players burned 1" (word 21 of 59) at 27.36 s, stage 4 on "Player 1 took the four-card pot" (word 50) at 37.82 s; the award finishes at 39.02 s and the final state holds to 42 s. Take durations are those in narration/timeline.json (the synthesized takes are not in this checkout).

## Delivered
Each required media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json (rebuilt by `src/endgame.py inventory`). Existing outputs are real rendered media, not placeholder filenames. Independent variants belong to this ticket. The original source brief and code remain unchanged.

| Variant | File | Duration | key_second | Notes |
|---|---|---|---|---|
| preview | exports/preview.mp4 | 12 s | — | the generic war sequence, unchanged |
| four-panel-poster | exports/four-panel-poster.png (= poster.png) | still | — | |
| single-war-motion | exports/single-war-motion.mp4 | 12 s | 0 | cut [0, 12] of preview |
| award-to-bottom | exports/award-to-bottom.mp4 | 4 s | 1.0 (first card moves) | cut [8, 12] of preview |
| endgame | exports/endgame.mp4, exports/endgame.png | 42 s | 6.5 (two tens face-up) | stage_seconds [0, 6.5, 27.36, 37.82] |

## Checks actually performed
- Rasterization with CairoSVG 2.9.1 (MSYS2 Cairo through `CAIROCFFI_DLL_DIRECTORIES`; fonts resolved by fontconfig to Liberation Sans and DejaVu Sans Mono; no font files distributed; the only URL in any SVG is the SVG namespace). PNG dimensions asserted at 1920 × 1080 by the renderer. ffprobe on the four MP4s: H.264, 1920 × 1080, yuv420p, 30/1; preview and single-war-motion 360 frames / 12.000 s, award-to-bottom 120 / 4.000 s, endgame 1260 / 42.000 s (`evidence/render-tests.json`; the tool writes paths with the platform separator).
- `tools/render/qa_browser.py --id DIA-08` in Playwright's bundled Chromium 153: `src/index.html` offline, deterministic seeking, 28 SVG files, 942 text boxes, none out of canvas. The same checks applied to `src/endgame.html` by a scratch script (the tool reads only index.html): offline, deterministic, 16 files, 526 boxes, none out of canvas; `renderAt` returns endgame-0000/0001/0004/0007 at the four stage seconds (`evidence/browser-tests.json`). The tool's project-wide summary in review/ was restored after the run; nothing outside this folder was changed.
- Manual visual review at full size (1920 × 1080, Read tool): `exports/endgame.png`; frames of endgame.mp4 extracted with ffmpeg at 0, 6.5, 7.5, 12, 27.5, 32.2, 38.3 and 41.5 s; `exports/four-panel-poster.png`; `exports/keyframes/middle.png`; a preview.mp4 frame at 9.5 s (mid-award). The 10♦ and 10♠ read as playing cards (corner index, ten pips, rotated lower half) at 117 px; the 4s, 9♦ and A♦ read at 57 px on the four-panel poster and at 117 px in the sequence; counters (76 px mono) and the pot (58 px) are legible; the stdout line in 30 px mono fits inside the safe area. A first pass of the endgame poster drew panel 4's cards twice with the caption over them; fixed in `src/endgame.py` and re-rendered before delivery.
- Manual visual review at 720p: `proofs/endgame-720.png`, `proofs/endgame-stage1…4-720.png` (the frame at each stage second, 1280 × 720), `proofs/poster-720.png`. Ranks and counters remain legible; the 57 px cards on the endgame poster read as face-up tens and backs, not as aces.
- `python tools/validate_delivery.py --id DIA-08` run after the inventory was rebuilt; result recorded in the completion report.
- Not performed: `tools/render/finish_delivery.py` (not run, by instruction); `tools/render/build_assets.py --id DIA-08` as a whole (it stops in `codes()` on CODE-26…29, which have no "Required focus sequence" requirement, before reaching the diagrams — see Remaining decisions), so the DIA-08 save step was called directly (Reproduction).

## Reproduction
From the package root, with `CAIROCFFI_DLL_DIRECTORIES` pointing at the Cairo DLLs (on this machine `C:\msys64\ucrt64\bin`):

```sh
python -c "import sys; sys.path.insert(0,'tools/render'); import build_assets, diagrams; diagrams.war_mechanic(); build_assets.save_assets({'DIA-08'}, 'Claude Fable 5.1 — local production')"
python assets/diagrams/DIA-08/src/endgame.py author
python tools/render/render_assets.py --id DIA-08
python assets/diagrams/DIA-08/src/endgame.py render
python assets/diagrams/DIA-08/src/endgame.py inventory
python tools/validate_delivery.py --id DIA-08
```

The first command is the DIA-08 part of `build_assets.py --id DIA-08`; it resets `state.json` and `evidence/claim-checks.json`, which are then maintained by hand (this revision's versions are committed). The endgame render uses the `raster()` and `encode()` functions of `render_assets.py` (CairoSVG at 1920 × 1080, ffmpeg concat at 30 fps, libx264 crf 18, yuv420p, faststart); `render_assets.py` itself renders the 12 s sequence, its cuts, the poster, the variant stills (including `exports/endgame.png`), the keyframes and the contact sheet, and ignores the `endgame` block of `src/build.json`.

Hand-size replay used for the 50 / 2 split (Python, from the package root):

```python
import re
p1=p2=26
for l in open('assets/captures/TERM-04/source/stdout.txt',encoding='utf-8').read().splitlines()[:1288]:
    m=re.search(r'Player (\d) wins the round \((\d+) cards\)',l)
    if m:
        w,n=int(m.group(1)),int(m.group(2))//2
        p1,p2=(p1+n,p2-n) if w==1 else (p1-n,p2+n)
print(p1,p2)   # 50 2
```

Tool versions: Windows 11 10.0.26200, Python 3.14.0, CairoSVG 2.9.1, Pillow 12.3.0, ffmpeg 6.0-essentials_build (gyan.dev), Playwright 1.63.0 with bundled Chromium 153.0.8010.12. Shared template win95-workbench-1.1.0.

## Remaining decisions
Assigned gate: R05. The generic sequence still shows only the fully supplied normal fixture. The endgame cutdown is a short-hand case, which the register says needs an exact-state test and a producer decision: the state is the captured run itself (line 1291 is the program's own verdict), and the revision-2 ticket is the decision; recorded in `evidence/claim-checks.json`. The register's ambiguous case (both hands empty after the burn) does not occur here because Player 1 holds 48 after the burn.

Review questions for the producer:
1. **Placement.** The placement map puts `DIA-08:endgame` on S12-B03 only, and gives all of S12-B04 (21.3 s) to CODE-20. Stages 1–2 (and the two sub-states) land inside S12-B03; stages 3 and 4 land on S12-B04's sentences ("so both players burned 1", "Player 1 took the four-card pot"), so with the current map the burn and the award are never seen. Options: split S12-B04 between CODE-20 (its line-264 cue) and the endgame, or let the endgame run through S12-B04 and move CODE-20 elsewhere. The asset is built for the second reading; the recorded stage seconds fit either.
2. **Poster hold.** After a motion asset ends, the timeline holds the asset's `exports/poster.png` (the generic four-panel poster), not the endgame poster; the endgame is 42 s so it out-lasts S12-B03 + S12-B04 (41.07 s from its start) and no hold should occur, but if the slot is longer the held image would be the wrong poster.
3. **Tooling, not this ticket:** `tools/render/build_assets.py` currently fails in `codes()` because CODE-26, CODE-27, CODE-28 and CODE-29 have no "Required focus sequence" requirement, so a whole-batch rebuild of the diagrams is blocked until that is fixed.

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- Uses the supplied single-war fixture; burns conceal their faces. This is not an actual Program.vb run.
- The ten-card award moves individually in stored play order. The final counts are 21 / 31 / pot 0.
- No insufficient-card case or recursive function is illustrated in the generic sequence; the endgame cutdown illustrates the one real short-hand case from the TERM-04 capture, quoting the program's output.
