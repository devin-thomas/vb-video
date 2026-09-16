---
id: "ASM-02"
title: "Bed transitions: fade to silence, a gap, then the next bed; no crossfades"
owner_role: "orchestrator"
original_family: "R2-MIX"
priority: "required"
production_status: "planned"
release_gates: []
---

# ASM-02 — Bed transitions: fade to silence, a gap, then the next bed; no crossfades

## Assignment and boundaries
**One ticket, one independently reviewed package.** Make every music change a clean handover: the outgoing bed fades fully out, silence, then the next bed fades in, with the chapter stings placed so nothing overlaps.

**Origin:** Devin's review of the first cut, [review/cut-notes-2026-09-16.md](../../review/cut-notes-2026-09-16.md), note(s) 2 and 7. **Primary owner role:** orchestrator. **Type:** support. **Script section(s):** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17. **Priority:** required.

**Owned write paths:** `assets/ops/ASM-02/`. Read other assets as dependencies; do not edit them. `sources/` and `War/SCRIPT.md` are read-only for this ticket; the narration text is final.

## Required inputs and source anchors
Read this ticket, [AGENTS.md](../../AGENTS.md), [docs/roles/PRODUCER.md](../roles/PRODUCER.md) ("Operating model"), the [production bible](../PRODUCTION_BIBLE.md) and the [output contract](../OUTPUT_CONTRACT.md).

- `tools/assembly/render.py` (`mix`: `afade` in 2 s and out 3 s per bed, `adelay` per bed), `tools/assembly/music_plan.py`, `narration/music-plan.json`, `narration/sfx-music.json`, `narration/timeline.json` (chapter starts).
- Devin's words: "songs should fade out fully before the next one comes in instead of cross fading"; a second clash was heard at a bed change.

**Integration dependencies:** none

## Creative and technical requirements
1. At each bed change the outgoing bed fades to silence over 3 s and reaches silence at least 1.0 s before the next bed's first audible sample; the next bed fades in over 2 s. No two music sources are audible at the same time anywhere in the video.
2. Bed boundaries in `narration/music-plan.json` come from the chapter-card times in `narration/timeline.json`; `tools/assembly/music_plan.py` writes the gap explicitly (`to` of one bed and `from` of the next differ by the gap).
3. The chapter stings (`narration/sfx-music.json`) either play inside the gap, ending before the next bed starts, or are dropped for that chapter; record the choice per chapter in `exports/report.md`.
4. Render a bed-only stem (`exports/bed-stem.wav`, all music, no voice or effects) and measure a silence window of at least 1.0 s at every join.
5. Change only `tools/assembly/render.py` (`mix`), `tools/assembly/music_plan.py`, `narration/music-plan.json` and `narration/sfx-music.json`.

## Exact copy / source payload
~~~~text
(none; see requirements)
~~~~

Text described as proposed or authored in this ticket is a production choice, not a fact from the source. Do not rewrite the narration to make a visual easier to produce.

## Composition, states, and local timing
1. Bed changes at the chapter cards listed in the timeline (16 joins plus the outro change).
2. Bed-only stem for measurement.

Stills and motion use 1920×1080 with the shared safe area; motion is 30 fps with deterministic `renderAt(seconds)`. Every named state/cutdown needs a concrete file and mapping in delivery.json.

**Named variants:** `bed-stem`

## Deliverables
Paths below are relative to `assets/ops/ASM-02/`.

- `delivery.json`
- `qa.md`
- `evidence/provenance.json`
- `evidence/source-excerpts.md`
- `exports/report.md`
- `exports/bed-stem.wav`

Also maintain `state.json` in this folder. Record the exact local reproduction command and tool versions in qa.md. Never create empty placeholder media.

## Acceptance checks
- [ ] `exports/report.md` lists every join with the outgoing bed's silence time, the next bed's start, the gap length, and the sting decision.
- [ ] No join has two music sources audible at once (bed-only stem RMS below -60 dBFS for ≥1.0 s at each join).
- [ ] The whole mix still meets ASM-01's loudness targets.
- [ ] Every required output is present and corresponds to this ID.
- [ ] All claimed tests actually ran; manual inspection is recorded at full size and 720p where applicable.
- [ ] `python tools/validate_delivery.py --id ASM-02` passes.

## Editorial, authenticity, and access gates
Rights are settled by Devin's standing R14 ruling; do not raise a rights question. New outside material still needs provenance recorded. Do not create accounts, accept terms, pay, download third-party files, publish, or place secrets in files. If a tool is missing, report the exact gap and keep partial work explicitly partial.

## Completion report
Return this ID, branch and commit, concrete output paths, variant/duration information, exact provenance, tests actually run with results, `python tools/validate_delivery.py --id <ID>` output, review questions (anything evidence cannot settle), and any boundary need. Update only your own state file. Leave GitHub issues, indexes and the timeline to the producer unless this ticket names them as owned paths.

## Embedded source context (unchanged excerpts)
### SCRIPT.md:1–809

~~~~text
(whole file: SCRIPT.md, 809 lines; see the source)
~~~~
