# CMP-02 — Production QA (revision 2, 2026-09-16)

**Production:** produced. **Release:** unreviewed (revision 2 replaces the first cut's approved exports; the producer re-reviews).

## What changed in revision 2
Devin's review notes 13 and 14 (review/cut-notes-2026-09-16.md). The card is now the Sub-versus-Function comparison, animated: left column "C / C++ / C#" with `void HelloWorld() { ... }` and `int Add(int a, int b) { return a + b; }`; right column "VB" with `Sub HelloWorld() ... End Sub` and `Function Add(a As Integer, b As Integer) As Integer ... End Function`. A "When called" strip under each column shows `HelloWorld()` with an empty slot and `Add(3, 4)` with a slot that the value `7` drops into. Kind changed from still to motion (8 s, 30 fps, 240 frames). The script's literal BuildDeck pair survives unchanged as the `byref-note` still; it is no longer the poster.

## Delivered
Each media/source/evidence file is enumerated by byte count and SHA-256 in delivery.json. All outputs are real rendered media. Duration 8 s at 30 fps; 20 authored states (`src/scene-0000.svg` … `scene-0019.svg`), timing in `src/timeline.json` and `src/build.json`.

Named variants: `comparison` (end state, clean), `token-focus` (end state with `void`/`int` and `Sub`/`Function` focus rects), `byref-note` (first-cut BuildDeck still). Keyframes: `exports/keyframes/start.png` (0 s), `middle.png` (4 s), `end.png` (7.97 s). Motion: `exports/preview.mp4`.

Timeline: 0.0 s columns only; 0.4 s HelloWorld/Sub row; 1.4 s Add/Function row; 2.6 s call strip with empty slots; 3.4–4.8 s the `7` leaves the Function/int row and drops into the `Add(3, 4)` slot in 12 positions at 0.1 s each; 4.8 s value seated; 5.4 s the Sub/void slot reads "nothing"; 6.0–8.0 s hold with the summary line "A Sub, like void, gives nothing back. A Function gives back a value."

## Checks actually performed
- `python tools/render/render_assets.py --id CMP-02`: CairoSVG 2.9.1 rasterization at 1920 × 1080; ffprobe on preview.mp4: h264, yuv420p, 30/1, 240 frames, 8.000 s (evidence/render-tests.json).
- `python tools/render/qa_browser.py --id CMP-02`: installed Chromium 153.0.8010.12, in-memory HTML; 24 SVG files, 1678 text boxes, none out of canvas; nonlinear seek (4.24 s → 8 s → 0 s → 4.24 s) gave identical SVG; no network request (evidence/browser-tests.json).
- Manual inspection by the worker (Read tool on the PNGs) at full 1920 × 1080: exports/poster.png, exports/token-focus.png, exports/byref-note.png, exports/keyframes/middle.png; at 1280 × 720: proofs/poster-720.png and frames extracted from preview.mp4 with ffmpeg at 0.2, 1.0, 3.0, 4.2, 5.0 and 7.5 s (0.2, 1.0, 5.0, 7.5 s scaled to 1280 wide; 3.0 and 4.2 s at full size). Result: nothing clipped; every code line inside its panel (the longest, `Function Add(a As Integer, b As Integer)`, ends 46 px inside the VB panel); the travelling `7` never crosses code text (it moves in the empty area to the right of the function body, over the strip's edge and into the slot); punctuation, the wrapped `As Integer`, the dashed "nothing" slot and the gold `7` are legible at 720p; focus rects sit on `void`, `int`, `Sub`, `Function` only.
- `python tools/validate_delivery.py --id CMP-02`: passed (structure, hashes, required outputs, PNG dimensions).
- Not performed: compile or run of the snippets (no .NET here and none is claimed), narration sync, sound, assembly, frame-by-frame review of all 240 frames (the 20 states were reviewed through the six frames above plus the keyframes).

## Reproduction
From the repository root, with `CAIROCFFI_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` set:

```sh
python assets/comparisons/CMP-02/src/author.py          # scenes, variants, build.json, timeline.json, index.html
python tools/render/render_assets.py --id CMP-02
python tools/render/qa_browser.py --id CMP-02
python tools/render/finish_delivery.py --id CMP-02
python tools/validate_delivery.py --id CMP-02
```

Do not run `tools/render/build_assets.py --id CMP-02`: it regenerates the first-cut BuildDeck still and would discard the revision 2 sources. `src/variant-byref-note.svg` is a copy of the first cut's `variant-comparison.svg`. Tool versions: the toolchain block in delivery.json (Python 3.14.0, CairoSVG 2.9.1, Pillow 12.3.0, Playwright 1.57.0 with Chromium 153.0.8010.12, ffmpeg 6.0, Windows 11). Fonts: Liberation Sans and DejaVu Sans Mono installed locally, not distributed.

## Remaining decisions
Assigned gate: R04a, checked by the worker in evidence/claim-checks.json (the revision makes no parameter-passing claim; the BuildDeck pair with `ByRef` is only the labelled byref-note still). No evidence question is open.

Review questions for the producer:
1. Title "Sub versus Function" with the end-state summary line "A Sub, like void, gives nothing back. A Function gives back a value." — wording is authored, not script text.
2. The "When called" strip (`HelloWorld() → nothing`, `Add(3, 4) → 7`) is an authored device to make the return visible; `7` is an illustration, not program output.
3. The VB `Function` signature is soft-wrapped after the parameter list (`As Integer` on a second visual line) because the 51-character line does not fit the column at the shared 30 px code size; no `_` continuation was inserted.
4. The first-cut BuildDeck card is kept as the `byref-note` variant; drop it if it is not wanted in the deck.

No narration sync, sound design, final video assembly, full independent editorial clearance, or live program capture is certified here. Produced is intentionally different from release-approved.

## Asset-specific notes
- Revision 2 (2026-09-16, review notes 13 and 14): Sub versus Function, animated. Left header lists C / C++ / C# because both left-hand snippets are valid in all three.
- HelloWorld and Add are agent-authored teaching snippets, not Program.vb excerpts; Add(3, 4) → 7 is an illustration of a returned value, not recorded program output. No compile/run is claimed.
- The VB Function signature is soft-wrapped for display (As Integer on a second visual line); the wrap is not a source line break and inserts no line-continuation syntax.
- Syntax comparison only: the HelloWorld pair shows that a Sub, like void, returns nothing; the Add pair shows that a Function, like int, returns a value. No other equivalence is claimed.
- byref-note keeps the script's literal BuildDeck pair (void BuildDeck(Card[] deck) versus Sub BuildDeck(ByRef Deck() As Card)) as a still; the C# snippet has no ref keyword, and it makes no parameter-rebinding claim.
