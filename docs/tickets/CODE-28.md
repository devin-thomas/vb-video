---
id: "CODE-28"
title: "Every variable declared at the top: the Dim block of a Program.vb subroutine"
owner_role: "code"
original_family: "R2-CODE"
priority: "required"
production_status: "planned"
release_gates: []
---

# CODE-28 — Every variable declared at the top: the Dim block of a Program.vb subroutine

## Assignment and boundaries
**One ticket, one independently reviewed package.** A literal Program.vb excerpt showing a subroutine whose `Dim` lines all sit at the top, with the block highlighted, for the "declared at the top" beat.

**Origin:** Devin's review of the first cut, [review/cut-notes-2026-09-16.md](../../review/cut-notes-2026-09-16.md), note(s) 18. **Primary owner role:** code. **Type:** code. **Script section(s):** 7. **Priority:** required.

**Owned write paths:** `assets/code/CODE-28/`. Read other assets as dependencies; do not edit them. `sources/` and `War/SCRIPT.md` are read-only for this ticket; the narration text is final.

## Required inputs and source anchors
Read this ticket, [AGENTS.md](../../AGENTS.md), [docs/roles/PRODUCER.md](../roles/PRODUCER.md) ("Operating model"), the [production bible](../PRODUCTION_BIBLE.md) and the [output contract](../OUTPUT_CONTRACT.md).

- Beat S07-B13 (16:15): "every single variable is declared at the top of the subroutine with `Dim`. In classic VB, you couldn't declare variables in the middle of the code. Everything went at the top. It's like writing C89."
- `War/Program.vb` lines 114–126 (DIA-06's anchor) as the first candidate.

**Integration dependencies:** none

## Creative and technical requirements
1. Literal excerpt of `War/Program.vb` (byte-exact text; the validator checks code cards as excerpts). Choose the subroutine the narration is looking at in section 7 (the shuffle, `Program.vb` lines 114–126 per DIA-06's anchors, or the nearest subroutine whose Dims are all at the top). Record the exact line range.
2. Highlight variant: the `Dim` block gets the family's highlight bar; a margin label reads "all declarations first". Nothing crosses code text.
3. Header shows `Program.vb` and `VB.NET`, as the CODE family does.
4. Still with the standard `clean` and `highlighted` variants; the renderer holds it for the beat.

## Exact copy / source payload
~~~~text
(literal excerpt; worker records the exact Program.vb line range in delivery.json and evidence/source-excerpts.md)
~~~~

Text described as proposed or authored in this ticket is a production choice, not a fact from the source. Do not rewrite the narration to make a visual easier to produce.

## Composition, states, and local timing
1. Still: clean excerpt.
2. Still: highlighted Dim block with the margin label.

Stills and motion use 1920×1080 with the shared safe area; motion is 30 fps with deterministic `renderAt(seconds)`. Every named state/cutdown needs a concrete file and mapping in delivery.json.

**Named variants:** `clean`, `highlighted`

## Deliverables
Paths below are relative to `assets/code/CODE-28/`.

- `delivery.json`
- `qa.md`
- `evidence/provenance.json`
- `evidence/source-excerpts.md`
- `src/index.html`
- `exports/poster.png`
- `exports/clean.png`
- `exports/highlighted.png`

Also maintain `state.json` in this folder. Record the exact local reproduction command and tool versions in qa.md. Never create empty placeholder media.

## Acceptance checks
- [ ] Excerpt is byte-identical to the recorded Program.vb line range.
- [ ] The Dim block is visibly first in the subroutine.
- [ ] 720p proof legible.
- [ ] Every required output is present and corresponds to this ID.
- [ ] All claimed tests actually ran; manual inspection is recorded at full size and 720p where applicable.
- [ ] `python tools/validate_delivery.py --id CODE-28` passes.

## Editorial, authenticity, and access gates
Rights are settled by Devin's standing R14 ruling; do not raise a rights question. New outside material still needs provenance recorded. Do not create accounts, accept terms, pay, download third-party files, publish, or place secrets in files. If a tool is missing, report the exact gap and keep partial work explicitly partial.

## Completion report
Return this ID, branch and commit, concrete output paths, variant/duration information, exact provenance, tests actually run with results, `python tools/validate_delivery.py --id <ID>` output, review questions (anything evidence cannot settle), and any boundary need. Update only your own state file. Leave GitHub issues, indexes and the timeline to the producer unless this ticket names them as owned paths.

## Embedded source context (unchanged excerpts)
### SCRIPT.md:305–305

~~~~text
Also notice: every single variable is declared at the top of the subroutine with `Dim`. In classic VB, you couldn't declare variables in the middle of the code. Everything went at the top. It's like writing C89 — all declarations before any statements. C# and modern C++ let you declare variables wherever you want. VB was stricter about this.
~~~~
### Program.vb:114–126

~~~~text
    Sub ShuffleDeck(ByRef Deck() As Card)
        Dim Rnd As New Random()
        Dim i As Integer
        Dim j As Integer
        Dim Temp As Card

        For i = 51 To 1 Step -1
            j = Rnd.Next(0, i + 1)
            Temp = Deck(i)
            Deck(i) = Deck(j)
            Deck(j) = Temp
        Next i
    End Sub
~~~~
