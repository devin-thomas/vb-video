# XTRA-10 QA — VB-for-Mac claim (evidence-gated)

**Outcome:** INTERNAL PROOF, research record only. Production status is `blocked` and release status is `blocked`. No visual was produced, because the ticket forbids producing one before the editorial decision.

**Worker:** Evidence-Gated Research Agent (Claude Opus 5)
**Branch:** `ticket/XTRA-10`
**Date:** 2026-09-15
**Reviewer:** none yet (producer)

## Result in one paragraph

Microsoft never released a product called "Visual Basic for Mac" as far as this research could establish. That conclusion does not rest only on searches that came back empty.

- **Microsoft's own KB records list its Mac BASIC products, and none is Visual Basic.** They are the BASIC Interpreter 1.00–3.00, BASIC Compiler 1.00, and QuickBASIC 1.00 for Apple Macintosh (S02–S05).
- **Period Mac trade press reports the product as absent.** MacWEEK (1996-02-05) refers to the absence of Visual Basic for the Mac (S17).

The "Visual Basic" Microsoft did put on the Mac was:

- VBA, the macro language inside Office. It was in Power Mac Office apps by October 1994 and in Word 98 Macintosh Edition, was removed in Office 2008, and was restored in Office 2011 (S28, S06, S20, S21, S23).
- VBScript for the Mac, announced for summer 1996 (S19).

The narration's "early 90s / terrible / abandoned quickly" story most resembles two things:

- QuickBASIC for Macintosh: released 1988, last update 1992, left to stagnate.
- Apple's MacBASIC: cancelled in 1985 and sold to Microsoft, never released.

Neither was Visual Basic. Full details are in `evidence/claim-checks.json`.

## Tests actually run

| Test | Command | Result |
|---|---|---|
| JSON syntax of evidence and state files | `python -c "import json; json.load(open(f))"` on `evidence/provenance.json`, `evidence/claim-checks.json`, `state.json`, `delivery.json` | Pass (see the check after `delivery.json` was generated) |
| Source script unchanged | `sha256sum sources/SCRIPT.md` | `3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb`, which matches the pack hash in FACT-01 provenance. `War/SCRIPT.md` was not edited (`git status`) |
| Delivery validator | `python tools/validate_delivery.py --id XTRA-10` | See "Validator output" below. It fails by design, as expected. |
| Retrieved-evidence integrity | `sha256sum` on each archived HTML and OCR text saved to the session scratchpad | Hashes are recorded per source in `evidence/provenance.json` (`retrieved_sha256`) |

**Not run, because not applicable:**

- Visual inspection at 1080p and 720p: no export exists.
- `qa_browser.py` and `finish_delivery.py`: no render.
- OCR checks against page images: MacWEEK hits S17–S19 were read from Internet Archive OCR text only.

## Research method and tools

**Tools:**

- curl 8.18.0 (x86_64-w64-mingw32)
- Python 3.14.0
- gh 2.88.1
- git 2.53.0.windows.1
- Claude Code WebSearch and WebFetch

**Services queried:**

- Wayback Machine CDX API and `id_` raw captures
- Internet Archive `advancedsearch.php`, the metadata API, and full-text search (`services/search/beta/page_production`, `service_backend=fts`, collections `macweekmagazine` and `applemagazines`)
- Wikimedia Commons API (`list=search`, `srnamespace=6`)
- GitHub code search over `jeffpar/kbarchive`, a mirror of Microsoft KB text

**Reproduction:**

- The query strings are recorded in `evidence/provenance.json` under `searches_without_matching_result`.
- Every source has its URL and access method recorded.
- A Wayback capture can be re-fetched with: `curl -sL "https://web.archive.org/web/<timestamp>id_/<original-url>" | sha256sum`

**Downloads:** text only (archived HTML pages and Internet Archive OCR `.txt` files), saved to the session scratchpad and not committed. No disk images, PDFs, screenshots or other media were downloaded. No accounts were used. The access-restricted Internet Archive lending item S10 (Microsoft's 1988 QuickBASIC for Macintosh manual) was **not** opened.

## Content checks

- [x] Product identity: **not substantiated**. The claim stays blocked under R09.
- [x] No absence-of-search-result argument is presented as proof. The conclusion rests on Microsoft's own applicability lists and on contemporaneous statements of absence. Empty searches are recorded separately as search coverage.
- [x] No wording changed. `sources/SCRIPT.md` and `War/SCRIPT.md` are untouched, and proposed changes are review questions only.
- [x] No fabricated evidence, no fake VB-for-Mac IDE, and no 404 graphic.
- [x] Sources, authored analysis and rights status are kept distinct (`provenance.json`, `claim-checks.json`).
- [x] Screenshot availability is documented: no authentic VB-for-Mac screenshot can exist. Candidate screenshots of adjacent products (S07, S08, S12–S14) have no rights record and are not cleared.
- [ ] Required visual outputs (`src/index.html`, `exports/poster.png`, `exports/approved-visual.png`) are **not present**. They wait on the producer's decision.

## Evidence quality caveats

- **S03–S06 and S28** are Microsoft KB text read through a third-party GitHub mirror. Only S02 (KB 31937) was read from an archived microsoft.com page.
- **S17–S19** are machine OCR. S18 is garbled and satirical, so treat it as weak.
- **Secondary-only dates:** QuickBASIC 1.00e (April 1992), its 1995 discontinuation, Microsoft BASIC 3.0 (1986), and the REALbasic 1998 release.
- **VBScript for Mac** (S19) was an announcement. Whether and when it shipped was not verified.

## Remaining blockers

1. **R09:** the script claim is contradicted. It needs a Writing Lead decision on rewording, and the script remains unchanged.
2. **Visual approach:** needs a producer decision. Options are in `evidence/claim-checks.json` → `review_questions`.
3. **R14:** there is no rights-cleared image for any option that uses a real screenshot or clipping.

## Validator output

Ran `python tools/validate_delivery.py --id XTRA-10` on 2026-09-15 after generating `delivery.json`. The exit code was 1.

```json
{
  "id": "XTRA-10",
  "ok": false,
  "errors": [
    "This is not a produced/reviewed/scouted delivery; partial work must not be certified complete.",
    "Required file missing: src/index.html",
    "Required file missing: exports/poster.png",
    "Required file missing: exports/approved-visual.png"
  ]
}
```

These four errors are the expected result for a blocked, evidence-gated delivery.

- **Status error:** the ticket must not claim `produced`.
- **Missing outputs:** the visual may not be made before the producer's decision, and placeholder media is forbidden.

No hash, size, path or state-mismatch errors were reported for the files that do exist.
