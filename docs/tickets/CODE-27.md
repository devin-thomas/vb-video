---
id: "CODE-27"
title: "Nintendo and Nintendont: the silent typo, and what Option Explicit does about it"
owner_role: "code"
original_family: "R2-CODE"
priority: "required"
production_status: "planned"
release_gates: []
---

# CODE-27 — Nintendo and Nintendont: the silent typo, and what Option Explicit does about it

## Assignment and boundaries
**One ticket, one independently reviewed package.** One code card in two states: a misspelled variable silently becoming a new empty variable, then the same code refusing to compile under Option Explicit.

**Origin:** Devin's review of the first cut, [review/cut-notes-2026-09-16.md](../../review/cut-notes-2026-09-16.md), note(s) 6. **Primary owner role:** code. **Type:** motion. **Script section(s):** 4. **Priority:** required.

**Owned write paths:** `assets/code/CODE-27/`. Read other assets as dependencies; do not edit them. `sources/` and `War/SCRIPT.md` are read-only for this ticket; the narration text is final.

## Required inputs and source anchors
Read this ticket, [AGENTS.md](../../AGENTS.md), [docs/roles/PRODUCER.md](../roles/PRODUCER.md) ("Operating model"), the [production bible](../PRODUCTION_BIBLE.md) and the [output contract](../OUTPUT_CONTRACT.md).

- Beat S04-B07 (8:49): "if you misspelled a variable name, VB would just silently create a new empty variable instead of telling you something was wrong. `Option Explicit` forces you to declare everything."
- Devin's words: "show a variable get set and trying to use a typo'd version (use Nintendo and Nintendont as the correct and misspelled variable names)".

**Integration dependencies:** none

## Creative and technical requirements
1. Use exactly these names: `Nintendo` is the declared variable, `Nintendont` is the misspelling. Authored teaching example, labelled "Visual Basic 4" and not presented as Program.vb.
2. State A (Option Explicit off): `Nintendo` is declared and set; a later line uses `Nintendont`; a callout shows that a new, empty `Nintendont` was created and `Nintendo` is unchanged, with the printed result.
3. State B (`Option Explicit On`): the same misspelled line is flagged at edit/compile time with the classic message "Variable not defined" pointing at `Nintendont`.
4. Callouts and error markers enter from the margin; nothing crosses code text. Same treatment as the CODE family.

## Exact copy / source payload
~~~~text
' Visual Basic 4 · Option Explicit off
Dim Nintendo As Integer
Nintendo = 1985
Nintendont = Nintendo + 1   ' typo: creates a NEW empty variable
Print Nintendo              ' still 1985

' with Option Explicit On:
' Nintendont = Nintendo + 1  → Variable not defined: Nintendont
~~~~

Text described as proposed or authored in this ticket is a production choice, not a fact from the source. Do not rewrite the narration to make a visual easier to produce.

## Composition, states, and local timing
1. 0–2 s: the four lines type in.
2. 2–5 s: State A callout: "Nintendont is a new, empty variable. Nintendo is still 1985. Nothing told you."
3. 5–6 s: `Option Explicit On` appears at the top.
4. 6–9 s: State B: the misspelled line is underlined, error "Variable not defined: Nintendont". Hold as poster.

Stills and motion use 1920×1080 with the shared safe area; motion is 30 fps with deterministic `renderAt(seconds)`. Every named state/cutdown needs a concrete file and mapping in delivery.json.

**Named variants:** `typo`, `option-explicit`

## Deliverables
Paths below are relative to `assets/code/CODE-27/`.

- `delivery.json`
- `qa.md`
- `evidence/provenance.json`
- `evidence/source-excerpts.md`
- `src/index.html`
- `exports/poster.png`
- `exports/typo.png`
- `exports/option-explicit.png`
- `exports/preview.mp4`

Also maintain `state.json` in this folder. Record the exact local reproduction command and tool versions in qa.md. Never create empty placeholder media.

## Acceptance checks
- [ ] Both names spelled exactly as given, in both states.
- [ ] The error message text is a real classic VB message ("Variable not defined").
- [ ] No annotation crosses code text; 720p proof legible.
- [ ] Every required output is present and corresponds to this ID.
- [ ] All claimed tests actually ran; manual inspection is recorded at full size and 720p where applicable.
- [ ] `python tools/validate_delivery.py --id CODE-27` passes.

## Editorial, authenticity, and access gates
Rights are settled by Devin's standing R14 ruling; do not raise a rights question. New outside material still needs provenance recorded. Do not create accounts, accept terms, pay, download third-party files, publish, or place secrets in files. If a tool is missing, report the exact gap and keep partial work explicitly partial.

## Completion report
Return this ID, branch and commit, concrete output paths, variant/duration information, exact provenance, tests actually run with results, `python tools/validate_delivery.py --id <ID>` output, review questions (anything evidence cannot settle), and any boundary need. Update only your own state file. Leave GitHub issues, indexes and the timeline to the producer unless this ticket names them as owned paths.

## Embedded source context (unchanged excerpts)
### SCRIPT.md:166–166

~~~~text
Two important settings in the project file: `Option Explicit On` and `Option Strict On`. In classic VB, variables didn't need to be declared. You could just start using a variable called `x` and VB would create it for you on the spot as a Variant — a type that could hold anything. This was convenient and also the source of approximately ten million bugs, because if you misspelled a variable name, VB would just silently create a new empty variable instead of telling you something was wrong. `Option Explicit` forces you to declare everything. We're being responsible.
~~~~
