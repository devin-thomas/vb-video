---
id: "FACT-07"
title: "Four recorded runs: rounds, wars, winner"
owner_role: "design"
original_family: "R2-CODE"
priority: "required"
production_status: "planned"
release_gates: []
---

# FACT-07 — Four recorded runs: rounds, wars, winner

## Assignment and boundaries
**One ticket, one independently reviewed package.** One summary card of the four recorded simulations so "every run is different" is shown as numbers, not as four terminal captures cycling.

**Origin:** Devin's review of the first cut, [review/cut-notes-2026-09-16.md](../../review/cut-notes-2026-09-16.md), note(s) Devin's approval of proposal 3 (24:06). **Primary owner role:** design. **Type:** still. **Script section(s):** 11. **Priority:** required.

**Owned write paths:** `assets/facts/FACT-07/`. Read other assets as dependencies; do not edit them. `sources/` and `War/SCRIPT.md` are read-only for this ticket; the narration text is final.

## Required inputs and source anchors
Read this ticket, [AGENTS.md](../../AGENTS.md), [docs/roles/PRODUCER.md](../roles/PRODUCER.md) ("Operating model"), the [production bible](../PRODUCTION_BIBLE.md) and the [output contract](../OUTPUT_CONTRACT.md).

- Beats S11-B03/B04 (24:06–24:38): "Every run is different because the shuffle is random. Sometimes it's over in 150 rounds. Sometimes it takes more than 2,000." and S12-B01 (617 rounds), S12-B06 (2,008 rounds).
- `recordings/R4-01..R4-04/`, `recordings/R2/`, `recordings/R3a`, `R3b`, and the TERM-02/04/05/06 capture packages for the stdout.

**Integration dependencies:** none

## Creative and technical requirements
1. Four rows, one per recorded run (the runs behind TERM-02, TERM-04, TERM-05, TERM-06 and recordings R4-01..R4-04): run label, rounds played, wars fought, winner, and how it ended (normal win, or ran out of cards during a war). Every number is read from the run's captured stdout (`recordings/*/stdout.txt` or the capture evidence under `assets/captures/`); record the file and line for each in evidence/source-excerpts.md. No invented numbers.
2. Fact-card treatment as FACT-01..06 (dark card, one bold line per row, tabular figures). Title: "Every run is different". Footer: the shortest and longest run in one line.
3. Highlight variant marks the row the narration singles out (the 617-round run, and the 2,008-round run).

## Exact copy / source payload
~~~~text
(figures from the captures; worker fills the table from the recorded stdout)
~~~~

Text described as proposed or authored in this ticket is a production choice, not a fact from the source. Do not rewrite the narration to make a visual easier to produce.

## Composition, states, and local timing
1. Still: the four-row table.
2. Still: `highlight` with the two named runs marked.

Stills and motion use 1920×1080 with the shared safe area; motion is 30 fps with deterministic `renderAt(seconds)`. Every named state/cutdown needs a concrete file and mapping in delivery.json.

**Named variants:** `table`, `highlight`

## Deliverables
Paths below are relative to `assets/facts/FACT-07/`.

- `delivery.json`
- `qa.md`
- `evidence/provenance.json`
- `evidence/source-excerpts.md`
- `src/index.html`
- `exports/poster.png`
- `exports/table.png`
- `exports/highlight.png`

Also maintain `state.json` in this folder. Record the exact local reproduction command and tool versions in qa.md. Never create empty placeholder media.

## Acceptance checks
- [ ] Every figure traces to a captured stdout line cited in the evidence file.
- [ ] The two runs the narration names (617 rounds, 2,008 rounds) are present and match.
- [ ] 720p proof legible.
- [ ] Every required output is present and corresponds to this ID.
- [ ] All claimed tests actually ran; manual inspection is recorded at full size and 720p where applicable.
- [ ] `python tools/validate_delivery.py --id FACT-07` passes.

## Editorial, authenticity, and access gates
Rights are settled by Devin's standing R14 ruling; do not raise a rights question. New outside material still needs provenance recorded. Do not create accounts, accept terms, pay, download third-party files, publish, or place secrets in files. If a tool is missing, report the exact gap and keep partial work explicitly partial.

## Completion report
Return this ID, branch and commit, concrete output paths, variant/duration information, exact provenance, tests actually run with results, `python tools/validate_delivery.py --id <ID>` output, review questions (anything evidence cannot settle), and any boundary need. Update only your own state file. Leave GitHub issues, indexes and the timeline to the producer unless this ticket names them as owned paths.


## Embedded source context (unchanged excerpts)
### SCRIPT.md:571–571

~~~~text
Every run is different because the shuffle is random. Sometimes it's over in 150 rounds. Sometimes it takes 500. The number of wars varies too — sometimes just a handful, sometimes twenty or more. But it always terminates.
~~~~
