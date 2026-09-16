# OPS-04 — Integration QA, coverage audit and editor handoff

Produced 2026-09-15 by the producer.

## Coverage

- Tickets: 147 (139 asset tickets, 8 coordination). Produced: 139.
- Script visual cues tracked by the manifest: 74; `docs/COVERAGE.md` maps all 50 original plan families and the 16 chapter cards to tickets.
- Release: 139 approved, 0 blocked, 8 unreviewed.
- Produced by family: broll 6, captures 7, cards 2, chapters 16, code 29, comparisons 9, diagrams 11, facts 8, historical 34, mockups 2, ops 4, reference-code 6, stills 5.

## Validation actually run

- `python tools/validate_pack.py`: errors [].
- `python tools/validate_delivery.py --id <ID>` on every produced ticket after the release review: all ok (file inventory, SHA-256 hashes, 1920×1080 export dimensions, literal code excerpts against sources/Program.vb, gate decision records).
- Manual inspection: workers viewed every export at full size and 720p (recorded in each qa.md and review/manual-review.json); the producer viewed the 720p proofs of the session-6 merges, the six B-roll frames, the XTRA-15 revision, and the word-bearing posters (DIA-11, DIA-12, DIA-14, XTRA-08, MOCK-02).

## Editor inventory

`exports/editor-inventory.csv`: one row per ticket in script order with section, script lines, primary file, exports, duration, variants, B-roll segment, credits, release eligibility and editor notes. 135 assets are cleared for the media bin; 4 blocked; support tickets are listed but are not media.
`exports/exceptions.md`: labels and constraints that travel with specific assets, plus the credits list.

## Not done here

- No final video was assembled, no narration recorded, no music or sound licensed, nothing uploaded. Those are human handoffs H01–H07 (`docs/handoffs/`).
- Screen recordings (H01) do not exist yet; the TERM captures are stills of real runs.
