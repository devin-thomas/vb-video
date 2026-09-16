# OPS-03 — Editorial, historical evidence and rights clearance ledger

Produced 2026-09-15 by the producer. The ledger is `exports/decision-ledger.json`; the question view is `../../../review/editorial-review.json`.

## How decisions were reached

- **Rights (R14).** Devin approved every rights item across six rounds, then ruled on 2026-09-15 that all R14 items are kept as documented and that no further rights review is requested. Each affected ticket's gate record names Devin as approver.
- **All other gates.** Devin delegated release review to the producer on 2026-09-15. The producer checked every asset against `War/SCRIPT.md` and `Program.vb` (code cards are also machine-checked against `sources/Program.vb` by `tools/validate_delivery.py`) and recorded a per-gate reason in each ticket's `evidence/claim-checks.json`.
- **Script.** Worker findings that contradicted the script were routed to the Writing Lead and applied in `War/SCRIPT.md`; `sources/SCRIPT.md` is untouched. Commits touching the working script:

  - `542f37e Writing Lead: resolve XTRA-05 RQ3 and dated wording at :151`
  - `a5988e5 Remove dated "2024" reference and broaden VB6 visual cue`
  - `9e6f14a Apply 6 HIST-sourced script corrections`
  - `1ed7591 Fix Java date in script: announced 1995, shipped Jan 1996`
  - `80d6420 Merge BROLL-01 through BROLL-06 scouting + rebuild indexes`
  - `92fcf74 Rebuild indexes after XTRA batch merge`
  - `c1158a7 Script: the Windows C Hello World is 73 lines`
  - `f32a343 Script: add Section 12 on running out of cards mid-war`
  - `b1c6822 Initial commit: War card game in VB.NET with video script`

## Gates by register entry

| Gate | Register issue | Tickets carrying it | Approved | Other |
|---|---|---|---|---|
| R01 | Stale “today” dates | 1 | 1 | 0 |
| R03 | Classic-inspired VB.NET versus actual VB4 | 9 | 9 | 0 |
| R04 | “Recursion” heading versus repeated inner loop | 3 | 3 | 0 |
| R05 | Insufficient cards and symmetric burn behavior | 7 | 7 | 0 |
| R06 | Round cap, counter reporting, and cycle wording | 7 | 7 | 0 |
| R07 | Pot allocation versus cards actually in play | 2 | 2 | 0 |
| R08 | Sample script output versus actual captures | 5 | 5 | 0 |
| R09 | Mac-product and historical-tooling claims | 2 | 2 | 0 |
| R10 | Classic declaration rules and historical return/Dim claims | 1 | 1 | 0 |
| R11 | Popularity, installed base, prices, and real VB applications | 6 | 6 | 0 |
| R12 | Current VB.NET status and migration/lifecycle claims | 2 | 2 | 0 |
| R13 | Influence diagram versus proven lineage | 1 | 1 | 0 |
| R14 | Per-image licensing, archive capture, and public availability | 44 | 44 | 0 |
| R15 | Dates, versions, and representative historical code | 11 | 11 | 0 |
| R16 | Download/runtime/version and price assumptions | 3 | 3 | 0 |
| R17 | Missing project file | 4 | 4 | 0 |
| R04a | ByRef / ByVal simplification | 5 | 5 | 0 |

Review questions recorded: 70 (6 open).

## What stays explicitly unresolved

- The narration's own claims that no asset can prove (market superlatives at :48, the legal-install confession at :151, 'VB6 applications still running today' at :748) are the author's statements and are left as narration; no artwork asserts them.
- The round-cap wording in the program output ('deck cycle detected') is real output and is described as a round cap in diagrams; the source is not patched.
- Historical claims were verified to primary sources where a ticket did so; the register's entries remain the record of what was and was not checked.
