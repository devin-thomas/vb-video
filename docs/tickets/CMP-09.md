---
id: "CMP-09"
title: "A queue in 1995: Queue<Card>, std::queue, and a VB array with ReDim"
owner_role: "code"
original_family: "R2-CODE"
priority: "required"
production_status: "planned"
release_gates: []
---

# CMP-09 — A queue in 1995: Queue<Card>, std::queue, and a VB array with ReDim

## Assignment and boundaries
**One ticket, one independently reviewed package.** A three-column comparison so the code is on screen the moment the narration names it: C# `Queue<Card>`, C++ `std::queue<Card>`, and what 1995 VB had instead.

**Origin:** Devin's review of the first cut, [review/cut-notes-2026-09-16.md](../../review/cut-notes-2026-09-16.md), note(s) Devin's approval of proposal 2 (17:00). **Primary owner role:** code. **Type:** still. **Script section(s):** 8. **Priority:** required.

**Owned write paths:** `assets/comparisons/CMP-09/`. Read other assets as dependencies; do not edit them. `sources/` and `War/SCRIPT.md` are read-only for this ticket; the narration text is final.

## Required inputs and source anchors
Read this ticket, [AGENTS.md](../../AGENTS.md), [docs/roles/PRODUCER.md](../roles/PRODUCER.md) ("Operating model"), the [production bible](../PRODUCTION_BIBLE.md) and the [output contract](../OUTPUT_CONTRACT.md).

- Beat S08-B02 (17:00): "In C#, you'd use `Queue<Card>` and call it a day. In C++, you'd use `std::queue`. In 1995 VB? You didn't have generic collections. You didn't even have a built-in queue. You had arrays, and you had `ReDim`."
- `War/Program.vb`: the `Hand` structure and `DrawTopCard`'s shift loop (record the exact lines).

**Integration dependencies:** none

## Creative and technical requirements
1. Three equal columns headed "C#", "C++", "Visual Basic (1995)". Left (C#): `var hand = new Queue<Card>();` / `hand.Enqueue(c);` / `var top = hand.Dequeue();`. Middle: `std::queue<Card> hand;` / `hand.push(c);` / `Card top = hand.front(); hand.pop();`. Right: the real program's approach, quoted from Program.vb (the `Hand` structure with `Cards()` and `Count`, and the `ReDim`/shift), marked as the excerpt it is.
2. The point on screen: two languages have a queue; VB has an array and a counter. A one-line footer: "No generic collections, no built-in queue: an array and a counter."
3. Same comparison treatment as CMP-01..08; language headers per the round-2 rule (each column names exactly the language its snippet is valid in).
4. Still with `comparison` and `token-focus` (the queue operations highlighted) variants.

## Exact copy / source payload
~~~~text
C#
var hand = new Queue<Card>();
hand.Enqueue(c);
var top = hand.Dequeue();

C++
std::queue<Card> hand;
hand.push(c);
Card top = hand.front(); hand.pop();

Visual Basic (1995): see Program.vb, the Hand structure and its shift loop
~~~~

Text described as proposed or authored in this ticket is a production choice, not a fact from the source. Do not rewrite the narration to make a visual easier to produce.

## Composition, states, and local timing
1. Still: three columns.
2. Still: token-focus on Enqueue/push/ReDim-shift.

Stills and motion use 1920×1080 with the shared safe area; motion is 30 fps with deterministic `renderAt(seconds)`. Every named state/cutdown needs a concrete file and mapping in delivery.json.

**Named variants:** `comparison`, `token-focus`

## Deliverables
Paths below are relative to `assets/comparisons/CMP-09/`.

- `delivery.json`
- `qa.md`
- `evidence/provenance.json`
- `evidence/source-excerpts.md`
- `src/index.html`
- `exports/poster.png`
- `exports/comparison.png`
- `exports/token-focus.png`

Also maintain `state.json` in this folder. Record the exact local reproduction command and tool versions in qa.md. Never create empty placeholder media.

## Acceptance checks
- [ ] Each column's code is valid in the language its header names.
- [ ] The VB column is a byte-exact Program.vb excerpt with its line range recorded.
- [ ] 720p proof legible with three columns.
- [ ] Every required output is present and corresponds to this ID.
- [ ] All claimed tests actually ran; manual inspection is recorded at full size and 720p where applicable.
- [ ] `python tools/validate_delivery.py --id CMP-09` passes.

## Editorial, authenticity, and access gates
Rights are settled by Devin's standing R14 ruling; do not raise a rights question. New outside material still needs provenance recorded. Do not create accounts, accept terms, pay, download third-party files, publish, or place secrets in files. If a tool is missing, report the exact gap and keep partial work explicitly partial.

## Completion report
Return this ID, branch and commit, concrete output paths, variant/duration information, exact provenance, tests actually run with results, `python tools/validate_delivery.py --id <ID>` output, review questions (anything evidence cannot settle), and any boundary need. Update only your own state file. Leave GitHub issues, indexes and the timeline to the producer unless this ticket names them as owned paths.


## Embedded source context (unchanged excerpts)
### SCRIPT.md:317–317

~~~~text
In C#, you'd use `Queue<Card>` and call it a day. In C++, you'd use `std::queue`. In 1995 VB? You didn't have generic collections. You didn't even have a built-in queue. You had arrays, and you had `ReDim`, and that was about it.
~~~~
