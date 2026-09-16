# DIA-02 — Production QA (revision 2, 2026-09-16)

**Production:** produced. **Release:** unreviewed (revision 2 replaces the first cut's approved exports; the producer re-reviews).

## What changed in revision 2
Devin's review notes 9 and 11 (review/cut-notes-2026-09-16.md): the rules explanation must be beat-accurate, with each named moment on screen when it is said and holding through the beat. The sequence is re-authored (`src/author.py`, drawing with the shared primitives in tools/render/studio.py and the revised win95-workbench-1.1.0 card faces) into five named cutdowns, each an independent MP4 that starts at its named moment and holds its end state to the end of the file, plus a poster PNG per cutdown. The continuous version (`preview.mp4` = `full-rules.mp4`, 35 s) keeps every moment in order with shorter holds and a visible reset card before the war example. The shuffle abstraction is gone (DIA-15 carries the "shuffle it" cue); the deck-hold is the squared deck at rest.

| Cutdown | File | Duration | key_second | Key moment | Serves |
|---|---|---|---|---|---|
| deck-hold | exports/deck-hold.mp4 | 30 s | 0 | still: the full squared deck at rest, Deck: 52 (loopable) | S05-B01 |
| alternating-deal | exports/alternating-deal.mp4 | 20 s | 0.6 | the first card leaves the deck for Player 1 (lands 0.667 s); one card every 0.1 s, 52 counted transfers; 26 / 26 from 5.767 s | S05-B02 "Deal it evenly" |
| normal-round | exports/normal-round.mp4 | 16 s | 1.2 | A♠ and K♥ land face-up at the same instant; gold accent, ">" and "Ace beats King" at 1.9 s; the pair slides under Player 1's pile 3.4–3.967 s; 27 / 25, pot 0, "Won cards go to the bottom" from 4.0 s | S05-B03 "Aces are high" |
| single-war | exports/single-war.mp4 | 20 s | 1.0 | the tie 4♠ / 4♦ is face-up; three face-down each land at 3.4, 3.9, 4.4 s (pot 8); the deciding 9♦ / A♦ flip at 6.3 s (pot 10); the ten cards travel to Player 2's bottom in play order 8.5–10.4 s; 21 / 31, pot 0 from 10.6 s | S05-B04 "it's War" |
| final-hold | exports/final-hold.mp4 | 14 s | 0 | still: the rank-only rule card, "Win all 52 cards." with "Tie? War. · Won cards go to the bottom" | S05-B05 |

`full-rules` (exports/full-rules.mp4, 35 s, key_second 0) is the continuous version: deck 0–3 s; deal 3–11 s (first card 3.6 s, 26 / 26 from 8.77 s); normal round 11–17 s (flip 12.2 s, 27 / 25 from 15 s); reset card 17–18.5 s; single war 18.5–31 s (tie 19.5 s, deciding flip 24.8 s, 21 / 31 from 29.1 s); rule card 31–35 s. Keyframes: start.png (0 s, deck), middle.png (17.5 s, reset card), end.png (34.97 s, rule card). poster.png / full-rules.png / src/scene.svg is the A♠ > K♥ compare state.

Every cutdown poster PNG is that cutdown's end (hold) state, so an editor can extend any hold with the still. Counters sum to 52 in every state (the card in flight is counted as neither pile's until it lands; a travelling won card counts for the winner only on arrival). All states come from tools/fixtures/war_storyboard.json (normal_round, single_war); they are teaching examples, not a captured game. The insufficient-cards ending (R05) is not depicted.

## Delivered
Each media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json (written by `src/make_delivery.py`; metadata authored, digests computed). All outputs are real rendered media. 206 authored states (`src/scene-0000.svg` … `scene-0205.svg`), timing in `src/timeline.json` and `src/build.json` (the `cutdowns` block holds each cutdown's own frame list, duration, key_second and poster). Named variants with MP4 and PNG: full-rules, deck-hold, alternating-deal, normal-round, single-war, final-hold; their delivery.json entries carry exactly name, file, duration_seconds and key_second. The first cut's `proofs/gallery.jpg` (old faces) was removed; `proofs/poster-720.png` is regenerated.

## Checks actually performed
- `python assets/diagrams/DIA-02/src/author.py`: 206 states, 206 continuous frames; an assertion checks the fixture counts (26/26 → 27/25; 21/31/0) and that every authored time is strictly increasing. Frame times are exact multiples of 1/30 so the renderer's `ceil(t·30)` quantisation lands each state on its own frame (verified by recomputing the frame index of every authored time: no collisions).
- `python tools/render/render_assets.py --id DIA-02`: CairoSVG 2.9.1 at 1920 × 1080 for poster, six variant PNGs, three keyframes, contact sheet and proofs/poster-720.png; ffprobe on preview.mp4 and full-rules.mp4: h264, yuv420p, 30/1, 1050 frames, 35.000 s (evidence/render-tests.json).
- `python assets/diagrams/DIA-02/src/render_cutdowns.py`: the five cutdowns through the same raster()/encode() (ffmpeg 6.0, libx264 crf 18, yuv420p, faststart); ffprobe: deck-hold 900 frames 30.000 s, alternating-deal 600 / 20.000 s, normal-round 480 / 16.000 s, single-war 600 / 20.000 s, final-hold 420 / 14.000 s (evidence/cutdown-tests.json).
- `python tools/render/qa_browser.py --id DIA-02`: installed Chromium 153.0.8010.12, in-memory HTML; 213 SVG files, 2584 text boxes, none out of canvas; deterministic seek (18.55 s → 35 s → 0 s → 18.55 s identical); no network request (evidence/browser-tests.json). The batch summary review/browser-summary.json it also touches was restored to the committed version (outside this ticket's owned paths).
- Manual inspection by the worker (Read tool on PNGs and ffmpeg-extracted frames) at full 1920 × 1080: exports/deck-hold.png, alternating-deal.png, normal-round.png, single-war.png, final-hold.png, poster.png, contact-sheet.png; cutdown frames at alternating-deal 0.667 s, normal-round 1.2 s, single-war 1.0 s and 8.6 s. At 1280 wide: deck-hold 29.5 s; alternating-deal 2.5 s and 19.5 s; normal-round 1.2 s and 15.5 s; single-war 6.3 s and 19.5 s; final-hold 13.5 s; preview 17.5 s (reset card). Result: cards read as regular playing cards (corner index and small suit, standard pip layouts on the 4s and 9, crown and K letter on the king, one large centre pip on the aces); A♠ over K♥ is unmistakable at both sizes; the 4♠ / 4♦ tie and the 9♦ / A♦ deciding pair are legible at 1280 wide; the travelling won cards pass in the open (over no text) and disappear under the winner's pile; nothing clipped; every hold frame equals its cutdown poster. Not every one of the 3000 cutdown frames was viewed individually; the 206 authored states were covered by the frames above.
- `python tools/validate_delivery.py --id DIA-02`: passed (structure, hashes, required outputs, PNG dimensions).
- Not performed: narration sync, sound, assembly, full independent editorial clearance, live program capture, or a run of Program.vb (none is claimed).

## Reproduction
From the repository root, with `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` set:

```sh
python assets/diagrams/DIA-02/src/author.py            # scenes, variants, build.json, timeline.json, index.html
python tools/render/render_assets.py --id DIA-02        # preview.mp4, full-rules.mp4, stills, keyframes, contact sheet
python assets/diagrams/DIA-02/src/render_cutdowns.py    # the five cutdown MP4s (CairoSVG + ffmpeg via the batch renderer's functions)
python tools/render/qa_browser.py --id DIA-02
python assets/diagrams/DIA-02/src/make_delivery.py      # delivery.json (do not run finish_delivery.py for this revision)
python tools/validate_delivery.py --id DIA-02
```

Do not run `tools/render/build_assets.py --id DIA-02`: it regenerates the first cut's 28 s sequence and would discard the revision 2 sources. The batch renderer's `cuts` mechanism only extracts spans of the continuous timeline, so it cannot give each cutdown its own hold; that is why the cutdowns are encoded by `src/render_cutdowns.py` from `build.json["cutdowns"]`, reusing the renderer's own raster() and encode(). Tool versions: the toolchain block in delivery.json (Python 3.14.0, CairoSVG 2.9.1, Pillow 12.3.0, Playwright with Chromium 153.0.8010.12, ffmpeg 6.0, Windows 11). Fonts: Liberation Sans and DejaVu Sans Mono installed locally, not distributed.

## Remaining decisions
Assigned gate: R05, re-checked by the worker in evidence/claim-checks.json (nothing insufficient-cards is depicted; the producer's 2026-09-15 decision stands). No evidence question is open.

Review questions for the producer:
1. The placement map (tools/assembly/build_timeline.py) lands normal-round's key moment on "Aces are high", which is the last phrase of S05-B03; the flip would then come after "takes both cards and puts them at the bottom" has been said. Landing it on "flip their top card" (key_second 1.2 s still applies) would put the flip, the compare and the collection under the words that describe them. Producer's call under ASM-03; the asset supports either.
2. Authored captions: "Ace beats King", "Same rank · tie", "Three face-down each", "Alternate one card at a time", "26 cards per player", "To Player 2's bottom", "New example · 26 cards each", the sub-heading "A second example · 26 cards each" and the deck-hold heading "52 cards". The five ticket copy lines appear verbatim. Cut any caption that reads as clutter.
3. The final rule card shows "Win all 52 cards." with "Tie? War. · Won cards go to the bottom"; the narrated "if a player runs out of cards during a war, they lose" is deliberately not on the card (R05). Confirm that is the intended treatment of S05-B05.
4. tools/assembly/render.py holds `exports/poster.png` (the A♠ > K♥ state) after any motion clip shorter than its slot. The cutdowns are longer than their beats in the current timeline (deck-hold 30 s vs 19.1 s, etc.), so the fallback should not trigger; if a beat grows past a cutdown's length, extend the cutdown rather than let the poster show a different state.

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- Revision 2 (2026-09-16, review notes 9 and 11): five named cutdowns with key_second, on the revised shared card faces (win95-workbench-1.1.0).
- Shuffle is not animated here (DIA-15 carries the shuffle cue); dealing is alternating, one card at a time, with 52 counted transfers.
- Normal-round and single-war scenes are independent supplied fixtures; the continuous version shows a visible reset between them.
- All count states conserve 52; the win-all-52 closing caption is a rule, not an alleged conclusion of the short example.
