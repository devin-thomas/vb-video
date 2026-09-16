---
id: "FACT-08"
title: "Two endgames side by side: run 1 and run 4"
owner_role: "design"
original_family: "R2-CODE"
priority: "required"
production_status: "planned"
release_gates: []
---

# FACT-08 — Two endgames side by side: run 1 and run 4

## Assignment and boundaries
**One ticket, one independently reviewed package.** The two-column card the script's side-by-side cue asks for: how the 617-round run and the 2,008-round run each ended in a war with too few cards.

**Origin:** Devin's review of the first cut, [review/cut-notes-2026-09-16.md](../../review/cut-notes-2026-09-16.md), note(s) Devin's approval of proposal 5 (26:31). **Primary owner role:** design. **Type:** still. **Script section(s):** 12. **Priority:** required.

**Owned write paths:** `assets/facts/FACT-08/`. Read other assets as dependencies; do not edit them. `sources/` and `War/SCRIPT.md` are read-only for this ticket; the narration text is final.

## Required inputs and source anchors
Read this ticket, [AGENTS.md](../../AGENTS.md), [docs/roles/PRODUCER.md](../roles/PRODUCER.md) ("Operating model"), the [production bible](../PRODUCTION_BIBLE.md) and the [output contract](../OUTPUT_CONTRACT.md).

- The script's cue ("Side-by-side comparison: TERM-04: 2 cards → play 10 → burn 1 → empty → 4-card pot / TERM-02: 3 cards → play 8 → burn 2 → empty → 6-card pot"), currently mis-mapped to CMP-02 for 47 s at 26:31–27:18.
- Beats S12-B07..B11 (26:16–27:18).

**Integration dependencies:** none

## Creative and technical requirements
1. Two columns from the script's own cue text, verbatim: left "Run 1 · 617 rounds": 2 cards → play 10 → burn 1 → empty → 4-card pot; right "Run 4 · 2,008 rounds": 3 cards → play 8 → burn 2 → empty → 6-card pot. Each step on its own line with the arrow as a connector, the final step emphasised.
2. Verify both sequences against the captured stdout of those runs (the same sources as FACT-07) and cite the lines; if the capture disagrees with the script's numbers, keep the script's wording on the card and raise a review question with the evidence.
3. Fact-card treatment; the two columns share one baseline so the steps align row by row.

## Exact copy / source payload
~~~~text
Run 1 · 617 rounds
2 cards → play 10 → burn 1 → empty → 4-card pot

Run 4 · 2,008 rounds
3 cards → play 8 → burn 2 → empty → 6-card pot
~~~~

Text described as proposed or authored in this ticket is a production choice, not a fact from the source. Do not rewrite the narration to make a visual easier to produce.

## Composition, states, and local timing
1. Still: both columns.
2. Still: `step-focus` with the final step of each column highlighted.

Stills and motion use 1920×1080 with the shared safe area; motion is 30 fps with deterministic `renderAt(seconds)`. Every named state/cutdown needs a concrete file and mapping in delivery.json.

**Named variants:** `comparison`, `step-focus`

## Deliverables
Paths below are relative to `assets/facts/FACT-08/`.

- `delivery.json`
- `qa.md`
- `evidence/provenance.json`
- `evidence/source-excerpts.md`
- `src/index.html`
- `exports/poster.png`
- `exports/comparison.png`
- `exports/step-focus.png`

Also maintain `state.json` in this folder. Record the exact local reproduction command and tool versions in qa.md. Never create empty placeholder media.

## Acceptance checks
- [ ] Both sequences match the script cue and are checked against the captures (cited).
- [ ] Rows align across the two columns.
- [ ] 720p proof legible.
- [ ] Every required output is present and corresponds to this ID.
- [ ] All claimed tests actually ran; manual inspection is recorded at full size and 720p where applicable.
- [ ] `python tools/validate_delivery.py --id FACT-08` passes.

## Editorial, authenticity, and access gates
Rights are settled by Devin's standing R14 ruling; do not raise a rights question. New outside material still needs provenance recorded. Do not create accounts, accept terms, pay, download third-party files, publish, or place secrets in files. If a tool is missing, report the exact gap and keep partial work explicitly partial.

## Completion report
Return this ID, branch and commit, concrete output paths, variant/duration information, exact provenance, tests actually run with results, `python tools/validate_delivery.py --id <ID>` output, review questions (anything evidence cannot settle), and any boundary need. Update only your own state file. Leave GitHub issues, indexes and the timeline to the producer unless this ticket names them as owned paths.


## Embedded source context (unchanged excerpts)
### SCRIPT.md:267–267

~~~~text
**[VISUAL: Side-by-side comparison:]**
~~~~
