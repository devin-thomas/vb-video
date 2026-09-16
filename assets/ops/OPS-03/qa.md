# OPS-03 — Production QA

**Production:** produced. **Release:** approved (coordination record, no media).

## Delivered
- `exports/decision-ledger.json` — every ticket's gates, approver, reason and review questions
- `exports/report.md` — how decisions were reached, gate table, what stays unresolved

## Checks actually performed
- Ledger regenerated from the tickets' own evidence files on 2026-09-15; every approved gate carries an approver and a reason (the validator refuses release otherwise).
- `python tools/validate_delivery.py --id <ID>` passed for every produced ticket at the time of the sweep.

## Reproduction
`python tools/producer/build_ops.py` (producer script, session 8); inputs listed in evidence/provenance.json.
