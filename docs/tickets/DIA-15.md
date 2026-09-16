---
id: "DIA-15"
title: "Animated riffle shuffle of a real deck"
owner_role: "motion"
original_family: "R2-MOTION"
priority: "required"
production_status: "planned"
release_gates: []
---

# DIA-15 — Animated riffle shuffle of a real deck

## Assignment and boundaries
**One ticket, one independently reviewed package.** An animated shuffle that actually shuffles: a full deck split and riffled together, drawn with the shared card faces, replacing the stock deck-cut clip.

**Origin:** Devin's review of the first cut, [review/cut-notes-2026-09-16.md](../../review/cut-notes-2026-09-16.md), note(s) 8 and 10. **Primary owner role:** motion. **Type:** motion. **Script section(s):** 5, 7. **Priority:** required.

**Owned write paths:** `assets/diagrams/DIA-15/`. Read other assets as dependencies; do not edit them. `sources/` and `War/SCRIPT.md` are read-only for this ticket; the narration text is final.

## Required inputs and source anchors
Read this ticket, [AGENTS.md](../../AGENTS.md), [docs/roles/PRODUCER.md](../roles/PRODUCER.md) ("Operating model"), the [production bible](../PRODUCTION_BIBLE.md) and the [output contract](../OUTPUT_CONTRACT.md).

- Beat S05-B02 (9:32, 10.4 s): "Take a standard 52-card deck and shuffle it. Deal it evenly." Also the shuffle cue at S07-B12 (15:54) next to DIA-06.
- Devin's words: the stock clip "is a deck-cut clip not a shuffle at all ... a video game or animated shuffle would be fine".

**Integration dependencies:** [OPS-01](OPS-01.md)

## Creative and technical requirements
1. A recognisable riffle shuffle: the deck splits into two halves, the halves interleave card by card, then square up. Card backs from `assets/shared/cards`; a few faces may flash during the riffle. Keep it legible, not photoreal.
2. Deterministic `renderAt(seconds)` at 30 fps, 1920×1080, on the felt background the DIA family uses. Duration about 6 s, plus a seamless 4 s loop variant so the editor can fill any slot without a freeze.
3. Depends on OPS-01's card-face revision: build against the revised faces so backs and any visible faces match the rest of the deck assets.
4. Also produce a still poster of the squared deck for the timeline builder's hold logic.

## Exact copy / source payload
~~~~text
(none; see requirements)
~~~~

Text described as proposed or authored in this ticket is a production choice, not a fact from the source. Do not rewrite the narration to make a visual easier to produce.

## Composition, states, and local timing
1. 0–1 s: squared deck.
2. 1–2 s: split into two halves.
3. 2–5 s: riffle interleave.
4. 5–6 s: square up; hold (poster).

Stills and motion use 1920×1080 with the shared safe area; motion is 30 fps with deterministic `renderAt(seconds)`. Every named state/cutdown needs a concrete file and mapping in delivery.json.

**Named variants:** `riffle`, `loop`

## Deliverables
Paths below are relative to `assets/diagrams/DIA-15/`.

- `delivery.json`
- `qa.md`
- `evidence/provenance.json`
- `evidence/source-excerpts.md`
- `src/index.html`
- `exports/poster.png`
- `exports/preview.mp4`
- `exports/riffle.mp4`
- `exports/loop.mp4`

Also maintain `state.json` in this folder. Record the exact local reproduction command and tool versions in qa.md. Never create empty placeholder media.

## Acceptance checks
- [ ] The motion reads as a shuffle at 720p (the halves visibly interleave).
- [ ] The loop variant has no visible seam.
- [ ] Card art comes from the revised shared faces.
- [ ] Every required output is present and corresponds to this ID.
- [ ] All claimed tests actually ran; manual inspection is recorded at full size and 720p where applicable.
- [ ] `python tools/validate_delivery.py --id DIA-15` passes.

## Editorial, authenticity, and access gates
Rights are settled by Devin's standing R14 ruling; do not raise a rights question. New outside material still needs provenance recorded. Do not create accounts, accept terms, pay, download third-party files, publish, or place secrets in files. If a tool is missing, report the exact gap and keep partial work explicitly partial.

## Completion report
Return this ID, branch and commit, concrete output paths, variant/duration information, exact provenance, tests actually run with results, `python tools/validate_delivery.py --id <ID>` output, review questions (anything evidence cannot settle), and any boundary need. Update only your own state file. Leave GitHub issues, indexes and the timeline to the producer unless this ticket names them as owned paths.

## Embedded source context (unchanged excerpts)
### SCRIPT.md:180–180

~~~~text
One. Take a standard 52-card deck and shuffle it. Deal it evenly — 26 cards to each player, face down. Neither player looks at their cards.
~~~~
