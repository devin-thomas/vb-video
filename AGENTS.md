# Agent operating rules

Read README.md, your assigned ticket, docs/PRODUCTION_BIBLE.md, docs/OUTPUT_CONTRACT.md, and the register entries named by that ticket. Read only the relevant original source ranges unless the task needs the complete source. The manifest is an index, not a substitute for the full ticket.

## Done, gates, and the review deck

A ticket is **done** when it is produced: rendered or captured deliverables exist, `tools/validate_delivery.py --id <ID>` passes, the worker has viewed exports at full size and 720p, and editorial gates have been worked. A done ticket satisfies every ticket that depends on it; no separate "reviewed" status is needed before dependents can proceed.

**Editorial gates are agent work.** The worker assigned to a ticket checks each flagged claim (R01–R17, R04a) against primary sources, fixes the asset or `War/SCRIPT.md` when the claim is wrong, and records the evidence in `evidence/claim-checks.json`. A question that evidence cannot settle — taste, narration voice, legal risk — becomes a **review question** and is handed back to the producer. Work on the ticket continues.

**OPS-03** is the project-wide evidence ledger: the single record of every editorial gate, its evidence, and its resolution or outstanding review question.

**OPS-04** builds the **review deck**: a browsable page showing every asset in script order with its review questions. Devin (the sole human) sees the work at this single moment and approves or requests changes. There is no per-asset producer approval step before the deck.

## Worker rules

1. Work on one assigned asset ID at a time. Own only `assets/<family>/<ID>/`; OPS-01 alone owns `assets/shared/`, OPS-02 alone owns `tools/war-harness/`. Never overwrite another agent’s files, update all statuses in the shared manifest, or change shared styles incidentally. Make local copies of the frozen harness for runtime work.
2. Keep `sources/` byte-identical. Use its content for exact code/copy. The script is the narrative authority and Program.vb is the executable-behavior authority; disagreements go to the editorial register, not a silent rewrite. This does not certify script history as true.
3. Use the shared frozen template version but craft and inspect the individual asset. A sixteen-card batch is not a substitute for sixteen separately reviewed outputs. Do not dump an entire folder into one agent context unnecessarily.
4. Keep source-derived content, proposed teaching examples, external evidence, and producer-approved revisions distinct. Do not invent source URLs, factual verification, licenses, runtime logs, code execution, or video captures.
5. Maintain `assets/<family>/<ID>/state.json`. Update only your file. Production: planned → in_progress → produced; use blocked when a necessary capability/input is missing. Research scouting may end scouted or no_match. Release is separately unreviewed/blocked/approved/not_applicable. A blocked fact does not prevent unrelated internal-proof work.
6. Follow the exact deliverables and named variants in the ticket. Keep clean originals and annotate derived copies. Preserve code as machine-readable text as well as images. For motion, use deterministic seeking and record a timeline.
7. Inspect actual exports at 1080p and 720p. Record manual results; automated structure validation does not certify visual quality, semantic correctness, or legal clearance. Use the two validators in tools/ for their explicitly limited checks.
8. Request access/approval only at a real boundary. Never create accounts, accept terms, pay, bypass a CAPTCHA, upload publicly, or place credentials in files. Do not claim an operation was performed when the environment cannot perform it.
9. Completion message to the producer: ID; branch and commit; files; exact source/provenance; tests actually run; validator result; review questions (anything evidence cannot settle); and any boundary need. Leave GitHub issues, gallery rebuilds, and the review deck to the producer.
10. Every ticket is also a GitHub issue (`github_issue` in manifest.json; handoffs under `handoff_issues`). Workers do not need to run `github_issues.py` or `build_indexes.py`; the producer handles index sync after merging.

## Producer

The producer dispatches tickets, receives worker reports, merges branches, syncs indexes, and builds the review deck (OPS-04). See `docs/roles/PRODUCER.md` for the full operating model. Workers report to the producer, not to Devin.
