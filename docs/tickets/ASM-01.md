---
id: "ASM-01"
title: "Mix: quieter music throughout, and effects that duck the bed to the floor"
owner_role: "orchestrator"
original_family: "R2-MIX"
priority: "required"
production_status: "planned"
release_gates: []
---

# ASM-01 — Mix: quieter music throughout, and effects that duck the bed to the floor

## Assignment and boundaries
**One ticket, one independently reviewed package.** Bring every music bed down across the whole video and make each sound-effect cue push the bed to near silence for the effect's full length.

**Origin:** Devin's review of the first cut, [review/cut-notes-2026-09-16.md](../../review/cut-notes-2026-09-16.md), note(s) 1 and 7. **Primary owner role:** orchestrator. **Type:** support. **Script section(s):** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17. **Priority:** required.

**Owned write paths:** `assets/ops/ASM-01/`. Read other assets as dependencies; do not edit them. `sources/` and `War/SCRIPT.md` are read-only for this ticket; the narration text is final.

## Required inputs and source anchors
Read this ticket, [AGENTS.md](../../AGENTS.md), [docs/roles/PRODUCER.md](../roles/PRODUCER.md) ("Operating model"), the [production bible](../PRODUCTION_BIBLE.md) and the [output contract](../OUTPUT_CONTRACT.md).

- `tools/assembly/render.py` (`mix`), `tools/assembly/music_plan.py`, `narration/music-plan.json`, `narration/sfx.json`, `narration/sfx-music.json`.
- Session 8 and 9 mix notes in `docs/INTEGRATION_LOG.md`; the effect cue times are 4:58, 9:12, 9:32, 15:54, 21:43, 22:40.
- Devin's words: "music is too loud in all spots"; an effect needs the music to "sharply duck to the bottom or maybe zero right before it", play in its entirety, then the music returns.

**Integration dependencies:** [ASM-02](ASM-02.md)

## Creative and technical requirements
1. Beds are quieter everywhere: under narration the bed sits at least 18 LU below the voice; on chapter cards and in gaps it never exceeds -22 LUFS short-term. Start from a global cut of about 6 dB on every bed in `narration/music-plan.json` and adjust from measurement, not by ear alone.
2. Each cue in `narration/sfx.json` drives its own duck: the bed falls to at least -40 dB relative (effectively silent) starting 0.3 s before the cue, holds for the effect file's full duration plus 0.2 s, then returns over about 0.8 s. The voice-driven sidechain duck stays.
3. The chapter stings in `narration/sfx-music.json` are music, not effects; ASM-02 decides where they sit. Do not let a sting and a bed sound at once.
4. Keep the whole mix at -16 LUFS integrated (±1 LU) with true peak at or below -1 dBTP. The limiter runs with auto-level off (`level=0`), as it does now.
5. Change only `tools/assembly/render.py` (the `mix` function), `tools/assembly/music_plan.py` gains and `narration/music-plan.json`. Do not touch takes, the timeline or assets.

## Exact copy / source payload
~~~~text
(none; see requirements)
~~~~

Text described as proposed or authored in this ticket is a production choice, not a fact from the source. Do not rewrite the narration to make a visual easier to produce.

## Composition, states, and local timing
1. Render `build/review-1080p60-mixed.mp4` with the new mix (the master profile regenerates it).
2. Export a 30 s listening excerpt around the Windows 95 chime (4:58) and one around a bed change, as `exports/chime-excerpt.wav` and `exports/join-excerpt.wav`.

Stills and motion use 1920×1080 with the shared safe area; motion is 30 fps with deterministic `renderAt(seconds)`. Every named state/cutdown needs a concrete file and mapping in delivery.json.

**Named variants:** `mixed-review`, `chime-excerpt`, `join-excerpt`

## Deliverables
Paths below are relative to `assets/ops/ASM-01/`.

- `delivery.json`
- `qa.md`
- `evidence/provenance.json`
- `evidence/source-excerpts.md`
- `exports/report.md`
- `exports/chime-excerpt.wav`
- `exports/join-excerpt.wav`

Also maintain `state.json` in this folder. Record the exact local reproduction command and tool versions in qa.md. Never create empty placeholder media.

## Acceptance checks
- [ ] Before/after table in `exports/report.md`: integrated and short-term loudness of the bed-only stem under speech, on a chapter card, and at each effect cue.
- [ ] At every effect cue the bed-only stem is at or below -40 dB relative for the effect's full length.
- [ ] Whole mix: -16 LUFS ±1 integrated, true peak ≤ -1 dBTP, measured with `ffmpeg -af ebur128=peak=true`.
- [ ] Every required output is present and corresponds to this ID.
- [ ] All claimed tests actually ran; manual inspection is recorded at full size and 720p where applicable.
- [ ] `python tools/validate_delivery.py --id ASM-01` passes.

## Editorial, authenticity, and access gates
Rights are settled by Devin's standing R14 ruling; do not raise a rights question. New outside material still needs provenance recorded. Do not create accounts, accept terms, pay, download third-party files, publish, or place secrets in files. If a tool is missing, report the exact gap and keep partial work explicitly partial.

## Completion report
Return this ID, branch and commit, concrete output paths, variant/duration information, exact provenance, tests actually run with results, `python tools/validate_delivery.py --id <ID>` output, review questions (anything evidence cannot settle), and any boundary need. Update only your own state file. Leave GitHub issues, indexes and the timeline to the producer unless this ticket names them as owned paths.

## Embedded source context (unchanged excerpts)
### SCRIPT.md:1–809

~~~~text
(whole file: SCRIPT.md, 809 lines; see the source)
~~~~
