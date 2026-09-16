---
id: "ASM-03"
title: "Timeline stabilisation: one visual per beat, no back-and-forth, beat-accurate section 5, code scroll-through in the cold open"
owner_role: "orchestrator"
original_family: "R2-EDIT"
priority: "required"
production_status: "planned"
release_gates: []
---

# ASM-03 — Timeline stabilisation: one visual per beat, no back-and-forth, beat-accurate section 5, code scroll-through in the cold open

## Assignment and boundaries
**One ticket, one independently reviewed package.** Rebuild the editorial timeline so the picture holds steady, changes only when the script gives a reason, and the rules section is locked to the card animations at the words.

**Origin:** Devin's review of the first cut, [review/cut-notes-2026-09-16.md](../../review/cut-notes-2026-09-16.md), note(s) 3, 4, 8, 9, 10, 11 (timeline side). **Primary owner role:** orchestrator. **Type:** support. **Script section(s):** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17. **Priority:** required.

**Owned write paths:** `assets/ops/ASM-03/`. Read other assets as dependencies; do not edit them. `sources/` and `War/SCRIPT.md` are read-only for this ticket; the narration text is final.

## Required inputs and source anchors
Read this ticket, [AGENTS.md](../../AGENTS.md), [docs/roles/PRODUCER.md](../roles/PRODUCER.md) ("Operating model"), the [production bible](../PRODUCTION_BIBLE.md) and the [output contract](../OUTPUT_CONTRACT.md).

- `tools/assembly/build_timeline.py`: `ids_for_cue`, `PLACEMENTS`, the equal split of a beat between its cues, and `visuals = ... or list(last_visuals)` which carries the whole previous list forward.
- Rotation hits in the first cut (time, beat, pattern): 0:29 S01-B03, 0:44 S01-B04, 1:09 S01-B05, 1:20 S01-B06 (HIST-02/XTRA-01/XTRA-02 cycling); 1:26 S02-B01; 2:32 S02-B04; 5:28 S03-B02; 16:44 S08-B01 (CODE-06/08/09); 21:14 S10-B01 (four code cards); 23:52 S11-B02, 24:06 S11-B03, 24:20 S11-B04 (TERM captures cycling); 27:22–27:54 S13-B01..B04 (four HIST/XTRA cycling); 28:40 S13-B07; 37:13 S16-B03, 37:37 S16-B04.
- Section 5 beats and current visuals: S05-B01 9:12 19.1 s DIA-02; S05-B02 9:32 10.4 s BROLL-01 (freezes: clip shorter than slot, and it is a deck cut, not a shuffle); S05-B03 9:43 13.5 s DIA-02+BROLL-02; S05-B04 9:56 20.9 s DIA-02; S05-B05 10:18 10.2 s DIA-02; S05-B06 10:28 12.8 s DIA-02.
- Devin's words: the edit "goes back and forth between two or keeps rotating through a few clips"; the intro "should show the VB code scrolling instead"; in the rules "if we're talking about an ace beating a king, it has to be on screen at that moment"; stock video goes "at the beginning or the end of the technical explanation"; the animations "can stay on screen longer so they last".

**Integration dependencies:** [DIA-02](DIA-02.md), [DIA-15](DIA-15.md), [DIA-04](DIA-04.md), [CMP-02](CMP-02.md), [CMP-03](CMP-03.md), [CODE-26](CODE-26.md), [CODE-27](CODE-27.md), [CODE-28](CODE-28.md), [REF-05](REF-05.md), [REF-02](REF-02.md)

## Creative and technical requirements
1. One visual per beat. A beat with several cues shows only the first cue's asset unless the beat is at least 12 s long and each cue has its own asset (then at least 6 s per visual). A beat without a cue holds only the LAST visual of the previous beat, never the whole list.
2. No return trips: a visual shown in the previous 60 s is not shown again unless the script cues it by name. Use the 19 rotation hits listed under inputs as the checklist; each must be gone or justified in the report.
3. Cold open: S01-B01 ("Terminal output scrolling") shows the code scroll-through recording (TERM-03, `recordings/R5`) instead of the PowerShell run (TERM-04). TERM-04 keeps its later slots (S11 and S12-B01).
4. Section 5 is locked to the card animations: S05-B01 holds DIA-02's opening (full deck) with no motion until the rules start; S05-B02 "shuffle it ... deal it evenly" shows DIA-15 (animated shuffle) then DIA-02 `alternating-deal`; S05-B03 shows DIA-02 `normal-round` so that A♠ beats K♥ lands on "Aces are high"; S05-B04 shows DIA-02 `single-war` so the tie, the three face-down cards and the deciding flip land on those words; S05-B05 holds the collected pot; S05-B06 holds the final state. Each cutdown's start is placed at the word it illustrates using the take's word timing (proportional by word count, as captions.py does). No repeats, and no stock footage between S05-B02 and S05-B05.
5. Stock footage sits at the edges of technical stretches: BROLL-02 (the card game) moves to the tail of section 5 (S05-B06) or the head (S05-B01), not inside. BROLL-01 leaves the cut (replaced by DIA-15). The same rule applies wherever a B-roll clip currently interrupts code or diagrams.
6. A clip shorter than its slot must not freeze: loop a motion asset's action or trim the slot; never hold the last frame for more than 1 s on a motion asset (stills are unaffected).
7. New and revised assets go where the words are: CODE-26 at S04-B06 from "You could just start using a variable"; CODE-27 at S04-B07; CODE-28 then REF-05 at S07-B13; DIA-04 (revised) on S07-B05/B06 (the ByRef beats) and CMP-03 on S07-B07/B08; CMP-02 (revised) on the Sub/Function beat; REF-02 (revised) at its section 2 cue. When a dependency is not yet produced, place the current asset and mark the slot in the report.
8. Change only `tools/assembly/build_timeline.py` and `narration/timeline.json`. Do not edit assets, takes or the script.

## Exact copy / source payload
~~~~text
(none; see requirements)
~~~~

Text described as proposed or authored in this ticket is a production choice, not a fact from the source. Do not rewrite the narration to make a visual easier to produce.

## Composition, states, and local timing
1. Rebuild the timeline and render a review cut of sections 1, 4, 5 and 7 (`render.py --profile review --sections 1,4,5,7`) for Devin to check the fixes before the full re-render.
2. Full review render is the producer's step once every dependency is produced.

Stills and motion use 1920×1080 with the shared safe area; motion is 30 fps with deterministic `renderAt(seconds)`. Every named state/cutdown needs a concrete file and mapping in delivery.json.

**Named variants:** `sections-1-4-5-7`

## Deliverables
Paths below are relative to `assets/ops/ASM-03/`.

- `delivery.json`
- `qa.md`
- `evidence/provenance.json`
- `evidence/source-excerpts.md`
- `exports/report.md`

Also maintain `state.json` in this folder. Record the exact local reproduction command and tool versions in qa.md. Never create empty placeholder media.

## Acceptance checks
- [ ] `exports/report.md` lists every beat with its visual and confirms: no beat shows a visual seen in the previous 60 s without a cue; no motion asset holds its last frame over 1 s; section 5 shows only DIA-15 and DIA-02 between S05-B02 and S05-B05, with each cutdown's start time and the word it lands on.
- [ ] `narration/timeline.json` reports beats without audio 0 and unmapped cues 0, and still uses every cleared asset that the script cues.
- [ ] The sections 1, 4, 5, 7 review cut plays the code scroll-through in the cold open.
- [ ] Every required output is present and corresponds to this ID.
- [ ] All claimed tests actually ran; manual inspection is recorded at full size and 720p where applicable.
- [ ] `python tools/validate_delivery.py --id ASM-03` passes.

## Editorial, authenticity, and access gates
Rights are settled by Devin's standing R14 ruling; do not raise a rights question. New outside material still needs provenance recorded. Do not create accounts, accept terms, pay, download third-party files, publish, or place secrets in files. If a tool is missing, report the exact gap and keep partial work explicitly partial.

## Completion report
Return this ID, branch and commit, concrete output paths, variant/duration information, exact provenance, tests actually run with results, `python tools/validate_delivery.py --id <ID>` output, review questions (anything evidence cannot settle), and any boundary need. Update only your own state file. Leave GitHub issues, indexes and the timeline to the producer unless this ticket names them as owned paths.

## Embedded source context (unchanged excerpts)
### SCRIPT.md:39–39

~~~~text
**[VISUAL: Terminal output scrolling — the War simulator running, cards being flipped, "** WAR! **" appearing on screen. Fast. Dramatic. The text scrolls like something out of a 90s hacker movie. Cut to black.]**
~~~~
### SCRIPT.md:178–192

~~~~text
Here are the rules:

One. Take a standard 52-card deck and shuffle it. Deal it evenly — 26 cards to each player, face down. Neither player looks at their cards.

**[VISUAL: Animation — deck splits into two piles.]**

Two. Each round, both players flip their top card face-up at the same time. Whoever played the higher card takes both cards and puts them at the bottom of their pile. Aces are high — they beat everything.

**[VISUAL: Animation — two cards flip, the higher one "wins" and both slide to the bottom of a pile.]**

Three. If both players flip the same rank — two sevens, two kings, whatever — it's War. Each player places three cards face-down, then flips a fourth card face-up. Whoever's face-up card is higher takes the entire pot — all ten cards. If it's another tie, you do it again. War can chain.

**[VISUAL: Animation — two equal cards appear, then three face-down cards from each player, then two more face-up cards. The pot grows.]**

Four. You keep playing until one player has all 52 cards. That player wins. If a player can't put up enough cards for a war, they lose.
~~~~
