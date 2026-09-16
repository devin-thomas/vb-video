---
id: "REF-05"
title: "C89: declarations at the top of the block"
owner_role: "code"
original_family: "R2-CODE"
priority: "required"
production_status: "planned"
release_gates: []
---

# REF-05 — C89: declarations at the top of the block

## Assignment and boundaries
**One ticket, one independently reviewed package.** A short C reference card showing what "like writing C89" means: every declaration at the top of the block, and the mid-block declaration C89 refuses.

**Origin:** Devin's review of the first cut, [review/cut-notes-2026-09-16.md](../../review/cut-notes-2026-09-16.md), note(s) 18. **Primary owner role:** code. **Type:** still. **Script section(s):** 7. **Priority:** required.

**Owned write paths:** `assets/reference-code/REF-05/`. Read other assets as dependencies; do not edit them. `sources/` and `War/SCRIPT.md` are read-only for this ticket; the narration text is final.

## Required inputs and source anchors
Read this ticket, [AGENTS.md](../../AGENTS.md), [docs/roles/PRODUCER.md](../roles/PRODUCER.md) ("Operating model"), the [production bible](../PRODUCTION_BIBLE.md) and the [output contract](../OUTPUT_CONTRACT.md).

- Beat S07-B13 (16:15), the C89 comparison.
- REF-01..REF-04 for the family's treatment.

**Integration dependencies:** none

## Creative and technical requirements
1. Authored representative C89 (about 12 lines): a function whose locals are all declared at the top, then a comment-marked line showing a declaration after a statement with the label "not allowed in C89 (C99 and later only)". Header: "C (C89)".
2. Compile-check the C89-valid part with any available C compiler in C89 mode if one is installed; if none is, say so in qa.md. Do not claim a compile that did not run.
3. Same reference-code treatment as REF-01..REF-04 (dark card, monospace, margin labels).

## Exact copy / source payload
~~~~text
/* C (C89): declarations first, then statements */
void shuffle(int *deck, int count)
{
    int i;
    int j;
    int temp;
    for (i = count - 1; i > 0; i--) {
        j = rand() % (i + 1);
        temp = deck[i]; deck[i] = deck[j]; deck[j] = temp;
    }
    /* int late = 0;   <- not allowed in C89 after a statement */
}
~~~~

Text described as proposed or authored in this ticket is a production choice, not a fact from the source. Do not rewrite the narration to make a visual easier to produce.

## Composition, states, and local timing
1. Still: full card.
2. Still: `top-focus` with the declaration block highlighted.

Stills and motion use 1920×1080 with the shared safe area; motion is 30 fps with deterministic `renderAt(seconds)`. Every named state/cutdown needs a concrete file and mapping in delivery.json.

**Named variants:** `clean`, `top-focus`

## Deliverables
Paths below are relative to `assets/reference-code/REF-05/`.

- `delivery.json`
- `qa.md`
- `evidence/provenance.json`
- `evidence/source-excerpts.md`
- `src/index.html`
- `exports/poster.png`
- `exports/clean.png`
- `exports/top-focus.png`

Also maintain `state.json` in this folder. Record the exact local reproduction command and tool versions in qa.md. Never create empty placeholder media.

## Acceptance checks
- [ ] The C89 rule is stated correctly (declarations precede statements within a block).
- [ ] The disallowed line is clearly marked as the contrast, not as valid C89.
- [ ] 720p proof legible.
- [ ] Every required output is present and corresponds to this ID.
- [ ] All claimed tests actually ran; manual inspection is recorded at full size and 720p where applicable.
- [ ] `python tools/validate_delivery.py --id REF-05` passes.

## Editorial, authenticity, and access gates
Rights are settled by Devin's standing R14 ruling; do not raise a rights question. New outside material still needs provenance recorded. Do not create accounts, accept terms, pay, download third-party files, publish, or place secrets in files. If a tool is missing, report the exact gap and keep partial work explicitly partial.

## Completion report
Return this ID, branch and commit, concrete output paths, variant/duration information, exact provenance, tests actually run with results, `python tools/validate_delivery.py --id <ID>` output, review questions (anything evidence cannot settle), and any boundary need. Update only your own state file. Leave GitHub issues, indexes and the timeline to the producer unless this ticket names them as owned paths.

## Embedded source context (unchanged excerpts)
### SCRIPT.md:305–305

~~~~text
Also notice: every single variable is declared at the top of the subroutine with `Dim`. In classic VB, you couldn't declare variables in the middle of the code. Everything went at the top. It's like writing C89 — all declarations before any statements. C# and modern C++ let you declare variables wherever you want. VB was stricter about this.
~~~~
