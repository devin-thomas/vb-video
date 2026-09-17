# Second cut — 2026-09-16

Running time **41:24**. Nothing uploaded.

| File | What it is | Size |
|---|---|---|
| `build/review-1080p60-mixed.mp4` | The cut to watch: 1080p60, narration, beds, effects (verified before the upscale) | 267 MB |
| `build/master-2160p60.mp4` | The upload master: 4K60 HEVC, same audio | 629 MB |
| `build/captions.srt`, `build/captions.vtt` | 547 caption cues | |
| `build/upload-metadata.md` | Title, description, tags, 17 chapters at the new times | |

## What changed since the first cut

- **Your 19 notes and the seven approved proposals are all in.** 13 new assets, 16 revised, every one produced, validated and approved; the full map is in `review/cut-notes-2026-09-16.md`.
- **Narration:** the two stage directions Aiden read aloud (25:43 and 26:31 in the first cut) are gone; "C++" at 17:00 is now C++.
- **Music:** beds about 6 dB lower; one music source at any moment (a bed fades to silence, the sting plays alone on the card, the next bed fades in; inside a bed's range the bed just continues, no sting); every effect pushes the bed to the floor and it returns after.
- **Picture:** one visual per beat, no return trips, the VB code scrolling in the cold open, the rules and queue animations landing on their words, the round-617 endgame with the real numbers, every tool in section 14 on its own name, the Mac section shifted onto its sentences, the petition on "petition", the outro re-ordered, real card faces everywhere.

## Watch for

- 9:32 to 10:42, the rules: the shuffle, the deal, the ace over the king on "flip their top card", the war on "it's War".
- 17:20 to 18:24, the queue: append, draw-and-shift, and the whole row sliding on "every card in the hand moves".
- 25:00 to 25:45, the endgame panels, and 26:31, the two endgames side by side.
- The music at chapter cards and around the Windows 95 chime at 4:58.

## Re-render

`bash tools/assembly/finish.sh --force` runs the whole chain; the individual steps are in `tools/assembly/` and `docs/INTEGRATION_LOG.md`, Session 10.
