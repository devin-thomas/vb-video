---
id: "CODE-29"
title: "Reads like English: If PlayerScore > HighScore Then, For Each Item In Collection"
owner_role: "code"
original_family: "R2-CODE"
priority: "required"
production_status: "planned"
release_gates: []
---

# CODE-29 — Reads like English: If PlayerScore > HighScore Then, For Each Item In Collection

## Assignment and boundaries
**One ticket, one independently reviewed package.** A code card for the two VB lines the narration quotes as reading like English, so the code is on screen when it is spoken.

**Origin:** Devin's review of the first cut, [review/cut-notes-2026-09-16.md](../../review/cut-notes-2026-09-16.md), note(s) Devin's approval of proposal 6 (37:13). **Primary owner role:** code. **Type:** code. **Script section(s):** 16. **Priority:** required.

**Owned write paths:** `assets/code/CODE-29/`. Read other assets as dependencies; do not edit them. `sources/` and `War/SCRIPT.md` are read-only for this ticket; the narration text is final.

## Required inputs and source anchors
Read this ticket, [AGENTS.md](../../AGENTS.md), [docs/roles/PRODUCER.md](../roles/PRODUCER.md) ("Operating model"), the [production bible](../PRODUCTION_BIBLE.md) and the [output contract](../OUTPUT_CONTRACT.md).

- Beat S16-B03 (37:13): "`If PlayerScore > HighScore Then` reads like an English sentence. `For Each Item In Collection`…". The VB application screenshots (XTRA-11..14) move to 37:04 under ASM-03.

**Integration dependencies:** none

## Creative and technical requirements
1. Exactly the two lines the script quotes, as authored teaching examples (they are not in Program.vb): `If PlayerScore > HighScore Then` and `For Each Item In Collection`. Header "Visual Basic". Label the card as an example, not an excerpt.
2. Highlight variant: a faint English gloss under each line ("if the player's score is higher than the high score, then…" / "for each item in the collection…") entering from the margin, never across the code.
3. CODE-family treatment.

## Exact copy / source payload
~~~~text
If PlayerScore > HighScore Then

For Each Item In Collection
~~~~

Text described as proposed or authored in this ticket is a production choice, not a fact from the source. Do not rewrite the narration to make a visual easier to produce.

## Composition, states, and local timing
1. Still: the two lines.
2. Still: `gloss` with the English reading under each line.

Stills and motion use 1920×1080 with the shared safe area; motion is 30 fps with deterministic `renderAt(seconds)`. Every named state/cutdown needs a concrete file and mapping in delivery.json.

**Named variants:** `clean`, `gloss`

## Deliverables
Paths below are relative to `assets/code/CODE-29/`.

- `delivery.json`
- `qa.md`
- `evidence/provenance.json`
- `evidence/source-excerpts.md`
- `src/index.html`
- `exports/poster.png`
- `exports/clean.png`
- `exports/gloss.png`

Also maintain `state.json` in this folder. Record the exact local reproduction command and tool versions in qa.md. Never create empty placeholder media.

## Acceptance checks
- [ ] Both lines are verbatim from the script.
- [ ] The gloss does not cross the code.
- [ ] 720p proof legible.
- [ ] Every required output is present and corresponds to this ID.
- [ ] All claimed tests actually ran; manual inspection is recorded at full size and 720p where applicable.
- [ ] `python tools/validate_delivery.py --id CODE-29` passes.

## Editorial, authenticity, and access gates
Rights are settled by Devin's standing R14 ruling; do not raise a rights question. New outside material still needs provenance recorded. Do not create accounts, accept terms, pay, download third-party files, publish, or place secrets in files. If a tool is missing, report the exact gap and keep partial work explicitly partial.

## Completion report
Return this ID, branch and commit, concrete output paths, variant/duration information, exact provenance, tests actually run with results, `python tools/validate_delivery.py --id <ID>` output, review questions (anything evidence cannot settle), and any boundary need. Update only your own state file. Leave GitHub issues, indexes and the timeline to the producer unless this ticket names them as owned paths.


## Embedded source context (unchanged excerpts)
### SCRIPT.md:689–689

~~~~text
The language was readable in a way that C-based languages aren't. `If PlayerScore > HighScore Then` reads like an English sentence. `For Each Item In Collection` tells you exactly what it's doing. You didn't need to know what a pointer was. You didn't need to manage memory. You didn't need to understand header files or linking or preprocessor directives. You just wrote what you meant, and it worked.
~~~~
