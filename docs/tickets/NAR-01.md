---
id: "NAR-01"
title: "Narration re-reads: C++ and C# must be heard as spoken"
owner_role: "orchestrator"
original_family: "R2-NAR"
priority: "required"
production_status: "planned"
release_gates: []
---

# NAR-01 — Narration re-reads: C++ and C# must be heard as spoken

## Assignment and boundaries
**One ticket, one independently reviewed package.** Fix the beats where the voice says the language names wrong ("Q++" for C++ at about 17:00) by adjusting the spoken form, re-synthesizing only those beats, and re-selecting.

**Origin:** Devin's review of the first cut, [review/cut-notes-2026-09-16.md](../../review/cut-notes-2026-09-16.md), note(s) 19. **Primary owner role:** orchestrator. **Type:** support. **Script section(s):** 8. **Priority:** required.

**Owned write paths:** `assets/ops/NAR-01/`. Read other assets as dependencies; do not edit them. `sources/` and `War/SCRIPT.md` are read-only for this ticket; the narration text is final.

## Required inputs and source anchors
Read this ticket, [AGENTS.md](../../AGENTS.md), [docs/roles/PRODUCER.md](../roles/PRODUCER.md) ("Operating model"), the [production bible](../PRODUCTION_BIBLE.md) and the [output contract](../OUTPUT_CONTRACT.md).

- `tools/narration/beats.py` (spoken-form rules), `tools/narration/synth.py`, `tools/narration/qa.py`, `tools/narration/select.py`; `narration/qa.json` diffs (S08-B02/01 shows `c plus plus` heard as `two`).
- Devin's words: "~17:00 narration says Q++ instead of C++".

**Integration dependencies:** none

## Creative and technical requirements
1. Sweep `narration/qa.json`: every take whose spoken text contains "C plus plus" or "C sharp" and whose transcript does not contain "c++", "c plus plus", "c#" or "c sharp" is a candidate; S08-B02 (16:52) is confirmed by Devin.
2. Fix the pronunciation in the spoken form only (for example "see plus plus", "see sharp") in `tools/narration/beats.py`'s spoken-text rules, regenerate `narration/beats.json`, and confirm the written text of every beat is unchanged (diff the `written` fields).
3. Synthesize the affected beats as attempt 03 with `tools/narration/synth.py --attempt 3 --only <ids>`, QA them with `tools/narration/qa.py --attempt 3 --only <ids>`, and run `tools/narration/select.py`. Listen to each new take once and record what you heard.
4. Owned paths: `tools/narration/beats.py`, `narration/beats.json`, `narration/takes/<beat>/03/`, `narration/qa.json`, `narration/selection.json`. Do not edit `War/SCRIPT.md`.

## Exact copy / source payload
~~~~text
(none; see requirements)
~~~~

Text described as proposed or authored in this ticket is a production choice, not a fact from the source. Do not rewrite the narration to make a visual easier to produce.

## Composition, states, and local timing
1. For each re-read beat: attempt 03 take, its QA record, and the selection result.

Stills and motion use 1920×1080 with the shared safe area; motion is 30 fps with deterministic `renderAt(seconds)`. Every named state/cutdown needs a concrete file and mapping in delivery.json.

**Named variants:** none

## Deliverables
Paths below are relative to `assets/ops/NAR-01/`.

- `delivery.json`
- `qa.md`
- `evidence/provenance.json`
- `evidence/source-excerpts.md`
- `exports/report.md`

Also maintain `state.json` in this folder. Record the exact local reproduction command and tool versions in qa.md. Never create empty placeholder media.

## Acceptance checks
- [ ] `exports/report.md` lists every candidate beat with the old transcript, the new transcript, and which attempt is selected.
- [ ] Every `written` field in `narration/beats.json` is byte-identical to before the change.
- [ ] S08-B02's selected take is heard as "C plus plus" by the transcriber.
- [ ] Every required output is present and corresponds to this ID.
- [ ] All claimed tests actually ran; manual inspection is recorded at full size and 720p where applicable.
- [ ] `python tools/validate_delivery.py --id NAR-01` passes.

## Editorial, authenticity, and access gates
Rights are settled by Devin's standing R14 ruling; do not raise a rights question. New outside material still needs provenance recorded. Do not create accounts, accept terms, pay, download third-party files, publish, or place secrets in files. If a tool is missing, report the exact gap and keep partial work explicitly partial.

## Completion report
Return this ID, branch and commit, concrete output paths, variant/duration information, exact provenance, tests actually run with results, `python tools/validate_delivery.py --id <ID>` output, review questions (anything evidence cannot settle), and any boundary need. Update only your own state file. Leave GitHub issues, indexes and the timeline to the producer unless this ticket names them as owned paths.

## Embedded source context (unchanged excerpts)
### SCRIPT.md:317–317

~~~~text
In C#, you'd use `Queue<Card>` and call it a day. In C++, you'd use `std::queue`. In 1995 VB? You didn't have generic collections. You didn't even have a built-in queue. You had arrays, and you had `ReDim`, and that was about it.
~~~~
