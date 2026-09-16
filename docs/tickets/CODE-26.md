---
id: "CODE-26"
title: "Undeclared variable: created on first use as a Variant"
owner_role: "code"
original_family: "R2-CODE"
priority: "required"
production_status: "planned"
release_gates: []
---

# CODE-26 — Undeclared variable: created on first use as a Variant

## Assignment and boundaries
**One ticket, one independently reviewed package.** One code card that shows classic VB inventing a variable the moment you use it, and naming the type it gets: Variant.

**Origin:** Devin's review of the first cut, [review/cut-notes-2026-09-16.md](../../review/cut-notes-2026-09-16.md), note(s) 6. **Primary owner role:** code. **Type:** motion. **Script section(s):** 4. **Priority:** required.

**Owned write paths:** `assets/code/CODE-26/`. Read other assets as dependencies; do not edit them. `sources/` and `War/SCRIPT.md` are read-only for this ticket; the narration text is final.

## Required inputs and source anchors
Read this ticket, [AGENTS.md](../../AGENTS.md), [docs/roles/PRODUCER.md](../roles/PRODUCER.md) ("Operating model"), the [production bible](../PRODUCTION_BIBLE.md) and the [output contract](../OUTPUT_CONTRACT.md).

- Beat S04-B06 (8:31): "In classic VB, variables didn't need to be declared. You could just start using a variable called `x` and VB would create it for you on the spot as a Variant, a type that could hold anything."
- CODE-01 and CODE-02 for the family's look; `assets/shared/` for the frozen system.

**Integration dependencies:** none

## Creative and technical requirements
1. Authored teaching example in classic VB style (VB4, `Option Explicit` off, the default). Label it as such in the header ("Visual Basic 4 · Option Explicit off"); it is not an excerpt of Program.vb.
2. Two lines at most before the reveal. The reveal is a callout attached to the first use of `x`: "never declared → created here as a Variant". Keep the narration's word Variant exactly.
3. Same code font, size and dark card treatment as the CODE family (copy the frozen shared system locally). No arrows crossing text: callouts enter from the margin.
4. Motion: the line appears, then the callout; hold the final state as the poster. About 6 s, loop-safe hold at the end.

## Exact copy / source payload
~~~~text
' Visual Basic 4 · Option Explicit off
x = 42
Print x        ' 42
~~~~

Text described as proposed or authored in this ticket is a production choice, not a fact from the source. Do not rewrite the narration to make a visual easier to produce.

## Composition, states, and local timing
1. 0–1 s: header and empty editor.
2. 1–2.5 s: `x = 42` types in.
3. 2.5–4 s: callout from the right margin: "x was never declared. VB creates it here as a Variant."
4. 4–6 s: hold (poster state).

Stills and motion use 1920×1080 with the shared safe area; motion is 30 fps with deterministic `renderAt(seconds)`. Every named state/cutdown needs a concrete file and mapping in delivery.json.

**Named variants:** `clean`, `callout`

## Deliverables
Paths below are relative to `assets/code/CODE-26/`.

- `delivery.json`
- `qa.md`
- `evidence/provenance.json`
- `evidence/source-excerpts.md`
- `src/index.html`
- `exports/poster.png`
- `exports/clean.png`
- `exports/callout.png`
- `exports/preview.mp4`

Also maintain `state.json` in this folder. Record the exact local reproduction command and tool versions in qa.md. Never create empty placeholder media.

## Acceptance checks
- [ ] The word "Variant" is on screen at the end state.
- [ ] No annotation crosses code text at any frame (check the keyframes).
- [ ] 720p proof legible.
- [ ] Every required output is present and corresponds to this ID.
- [ ] All claimed tests actually ran; manual inspection is recorded at full size and 720p where applicable.
- [ ] `python tools/validate_delivery.py --id CODE-26` passes.

## Editorial, authenticity, and access gates
Rights are settled by Devin's standing R14 ruling; do not raise a rights question. New outside material still needs provenance recorded. Do not create accounts, accept terms, pay, download third-party files, publish, or place secrets in files. If a tool is missing, report the exact gap and keep partial work explicitly partial.

## Completion report
Return this ID, branch and commit, concrete output paths, variant/duration information, exact provenance, tests actually run with results, `python tools/validate_delivery.py --id <ID>` output, review questions (anything evidence cannot settle), and any boundary need. Update only your own state file. Leave GitHub issues, indexes and the timeline to the producer unless this ticket names them as owned paths.

## Embedded source context (unchanged excerpts)
### SCRIPT.md:166–166

~~~~text
Two important settings in the project file: `Option Explicit On` and `Option Strict On`. In classic VB, variables didn't need to be declared. You could just start using a variable called `x` and VB would create it for you on the spot as a Variant — a type that could hold anything. This was convenient and also the source of approximately ten million bugs, because if you misspelled a variable name, VB would just silently create a new empty variable instead of telling you something was wrong. `Option Explicit` forces you to declare everything. We're being responsible.
~~~~
